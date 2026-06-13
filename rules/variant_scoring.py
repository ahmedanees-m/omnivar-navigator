"""Novel-variant intrinsic scoring with the variant-dependent strength trees (v3.1 Track A2).

`score_variant(gene, hgvs, ann)` assembles the variant-INTRINSIC ACMG codes from raw inputs
against the gene's CSpec thresholds (the loader's per-gene af + PM2 strength), applies the
variant-dependent PVS1 (NMD/domain) and PS4 (proband ratio) strength trees, sums Tavtigian
points, and returns the band. Predictors (gnomAD AF, REVEL, Pangolin/SpliceAI, AlphaMissense)
are INJECTABLE via the Annotations object so real data sources are wired at execution; missing
predictors degrade gracefully to a reduced-confidence call (Gate G2).

Routed codes (PP4/PS3/PM3/PP1) are deliberately NOT assembled here - they belong to the other
DISCERN factors (the per-code partition). Held-out ClinVar AUC vs InterVar (H4) needs real
per-variant predictor scores and is run when those are wired in.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from core.schemas import Strength
from rules.acmg_codes import code_points
from rules.point_engine import BANDS, Classification
from rules.vcep.loader import get_spec

# Verified per-spec computational cut-offs (REVEL / splice). Documented in the spec YAML notes.
# (pp3_revel, pp3_splice, bp4_revel, bp4_splice)
_COMPUTATIONAL = {
    "CFD-VCEP-F8": (0.60, 0.20, 0.30, 0.10),
    "CFD-VCEP-F9": (0.60, 0.20, 0.30, 0.10),
    "VWD-VCEP-VWF": (0.644, 0.50, 0.290, 0.10),
    "PD-VCEP-GP1BA": (0.644, 0.50, 0.290, 0.01),
}
_COMPUTATIONAL_DEFAULT = (0.644, 0.50, 0.290, 0.10)

_STRENGTH_WORD = {Strength.PVS: "VeryStrong", Strength.PS: "Strong", Strength.PM: "Moderate",
                  Strength.PP: "Supporting"}
_LOF_CONSEQUENCES = {"nonsense", "frameshift", "stop_gained", "canonical_splice",
                     "splice_donor", "splice_acceptor", "start_lost", "deletion"}


@dataclass
class Annotations:
    """Raw per-variant inputs; any field may be None (unknown) -> graceful degradation."""
    af: float | None = None                  # gnomAD popmax/grpmax filtering allele frequency
    revel: float | None = None
    splice: float | None = None              # Pangolin (preferred) or SpliceAI score
    alphamissense: float | None = None       # secondary feature only (not a primary code)
    consequence: str = ""
    nmd_predicted: bool | None = None
    in_functional_domain: bool | None = None
    proband_count: int | None = None
    expected_proband: float | None = None


@dataclass
class ScoredVariant:
    gene: str
    hgvs: str
    spec_id: str
    covered: bool
    codes: list[str]
    points: float
    classification: Classification
    confidence: str
    drivers: dict = field(default_factory=dict)


def pvs1_strength(ann: Annotations) -> Strength | None:
    """Simplified Tayoun/Walker PVS1 decision tree (baseline; full tree is a documented refinement)."""
    if ann.consequence not in _LOF_CONSEQUENCES:
        return None
    if ann.nmd_predicted is True:
        return Strength.PVS                  # predicted NMD -> VeryStrong
    if ann.in_functional_domain is True:
        return Strength.PS                   # escapes NMD but hits a critical domain -> Strong
    return Strength.PM                       # LoF, NMD-escaping, outside known domain -> Moderate


def ps4_strength(ann: Annotations) -> Strength | None:
    """Proband-ratio PS4 (CFD-VCEP style). Ratio = observed/expected if expected given, else count."""
    if ann.proband_count is None:
        return None
    if ann.expected_proband:
        ratio = ann.proband_count / max(ann.expected_proband, 1e-9)
        if ratio >= 10:
            return Strength.PS
        if ratio >= 4:
            return Strength.PM
        if ratio >= 2:
            return Strength.PP
        return None
    n = ann.proband_count
    return Strength.PS if n >= 15 else Strength.PM if n >= 5 else Strength.PP if n >= 2 else None


def _code(base: str, strength: Strength) -> str:
    word = _STRENGTH_WORD.get(strength)
    return f"{base}_{word}" if word else base


def score_variant(gene: str, hgvs: str = "", ann: Annotations | None = None) -> ScoredVariant:
    ann = ann or Annotations()
    spec = get_spec(gene)
    codes: list[str] = []
    drivers: dict = {}
    missing: list[str] = []

    # --- frequency (BA1/BS1/PM2) against the gene-specific CSpec thresholds ---
    if ann.af is not None:
        ba1, bs1, pm2 = spec.af_threshold("ba1"), spec.af_threshold("bs1"), spec.af_threshold("pm2")
        if ann.af >= ba1:
            codes.append("BA1")
            drivers["BA1"] = f"AF {ann.af:g} >= {ba1:g}"
        elif ann.af >= bs1:
            codes.append("BS1")
            drivers["BS1"] = f"AF {ann.af:g} >= {bs1:g}"
        elif ann.af < pm2:
            pm2_strength = spec.strength_for("PM2")
            codes.append(_code("PM2", pm2_strength))
            drivers["PM2"] = f"AF {ann.af:g} < {pm2:g} ({pm2_strength.name})"
    else:
        missing.append("gnomAD AF")

    # --- computational PP3 / BP4 (REVEL + splice) at the spec cut-offs ---
    pp3r, pp3s, bp4r, bp4s = _COMPUTATIONAL.get(spec.spec_id, _COMPUTATIONAL_DEFAULT)
    if ann.revel is not None or ann.splice is not None:
        revel_hi = ann.revel is not None and ann.revel >= pp3r
        splice_hi = ann.splice is not None and ann.splice >= pp3s
        revel_lo = ann.revel is not None and ann.revel <= bp4r
        splice_lo = ann.splice is None or ann.splice <= bp4s
        if revel_hi or splice_hi:
            codes.append("PP3_Supporting")
            drivers["PP3"] = f"REVEL={ann.revel}, splice={ann.splice}"
        elif revel_lo and splice_lo:
            codes.append("BP4_Supporting")
            drivers["BP4"] = f"REVEL={ann.revel}, splice={ann.splice}"
    else:
        missing.append("REVEL/Pangolin")

    # --- variant-dependent strength trees ---
    pvs = pvs1_strength(ann)
    if pvs:
        codes.append(_code("PVS1", pvs))
        drivers["PVS1"] = pvs.name
    ps4 = ps4_strength(ann)
    if ps4:
        codes.append(_code("PS4", ps4))
        drivers["PS4"] = ps4.name

    # --- sum Tavtigian points -> band ---
    pts = 0.0
    ba1_hit = False
    for c in codes:
        p, is_ba1 = code_points(c)
        if is_ba1:
            ba1_hit = True
        pts += p
    cls = Classification.B if ba1_hit else _classify(pts)
    confidence = ("full" if spec.covered and not missing
                  else "reduced: " + (("no VCEP spec; " if not spec.covered else "")
                                      + ("missing " + ", ".join(missing) if missing else "")).strip("; "))
    return ScoredVariant(gene=gene, hgvs=hgvs, spec_id=spec.spec_id, covered=spec.covered,
                         codes=codes, points=round(pts, 2), classification=cls,
                         confidence=confidence or "full", drivers=drivers)


def _classify(pts: float) -> Classification:
    for thr, cls in BANDS:
        if pts >= thr:
            return cls
    return Classification.B
