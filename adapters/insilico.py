"""Calibrated in-silico adapter — PP3 / BP4 (plan Step 1.2, §A.3).

Maps a single predefined predictor's score to ACMG strength via the *calibrated* local
posteriors of Pejaver et al. 2022 (AJHG 109:2163) — not a flat "Supporting". One tool
is chosen per VCEP rule, per ClinGen PP3/BP4 guidance.

Verified REVEL thresholds (Pejaver 2022, Table 2):
  PP3  Supporting >= 0.644, Moderate >= 0.773, Strong >= 0.932
  BP4  Supporting <= 0.290, Moderate <= 0.183, Strong <= 0.016 (Very Strong <= 0.003)

The score lookup is injectable (a dbNSFP/AlphaMissense reader runs in a tool image);
the calibration logic here is exact and unit-tested.
"""
from __future__ import annotations

from collections.abc import Callable

from core.adapter import EvidenceAdapter
from core.schemas import EvidenceContribution, PatientContext, Strength, Variant

# Calibrated thresholds per predictor. Each is an ordered list of
# (low, high, code, strength); a score in [low, high) maps to that code/strength.
THRESHOLDS = {
    "REVEL": {
        "pp3": [(0.644, 0.773, Strength.PP), (0.773, 0.932, Strength.PM), (0.932, 1.01, Strength.PS)],
        "bp4": [(0.183, 0.290, Strength.BP), (0.016, 0.183, Strength.BM), (-0.01, 0.016, Strength.BS)],
    },
}


def revel_strength(score: float) -> tuple[str, Strength] | None:
    t = THRESHOLDS["REVEL"]
    for lo, hi, st in t["pp3"]:
        if lo <= score < hi:
            return "PP3", st
    for lo, hi, st in t["bp4"]:
        if lo <= score < hi:
            return "BP4", st
    return None


class InSilicoAdapter(EvidenceAdapter):
    code_group = ("PP3", "BP4")
    version = "REVEL/Pejaver2022"

    def __init__(self, predictor: str = "REVEL",
                 score_lookup: Callable[[Variant], float | None] | None = None):
        self.predictor = predictor
        self._lookup = score_lookup

    def health_check(self) -> bool:
        return self._lookup is not None and self.predictor in THRESHOLDS

    def evaluate(self, v: Variant, p: PatientContext) -> list[EvidenceContribution]:
        if self._lookup is None:
            return []
        score = self._lookup(v)
        if score is None:
            return []
        hit = revel_strength(score) if self.predictor == "REVEL" else None
        if not hit:
            return []
        code, strength = hit
        return [EvidenceContribution(code, strength, True,
                f"{self.predictor} (Pejaver2022 calibrated)",
                rationale=f"{self.predictor}={score:.3f} -> {code} {strength.name}")]
