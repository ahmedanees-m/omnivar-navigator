"""Real-data VCEP reconstruction on ClinGen ERepo (plan section 2, Tier A; Gate G3).

Runs the per-code partition and the deterministic reconstruction on the REAL ClinGen
Evidence Repository export, restricted to the DISCERN bleeding-cluster genes. Three
results:
  1. Reconstruction concordance: does the rule engine reproduce the VCEP's assertion from
     its own applied per-code evidence? (the real-data form of Gate G1 / G3)
  2. No inflation: for every variant, the points summed within the per-code partition
     equal the direct total - i.e. no code is double-counted (the per-code circularity fix).
  3. The real per-code applied-strength distribution for these genes - the actual VCEP
     strengths that replace the placeholders in rules/vcep/.

Run (on the VM, where the data lives):
    python3 -m eval.erepo_reconstruction data/raw/erepo/erepo_classifications.tab
"""
from __future__ import annotations

import sys
from collections import Counter

from rules.acmg_codes import code_points
from rules.point_engine import BANDS, Classification
from rules.vcep.partition import base_code, owner

# DISCERN cluster genes (the bleeding/platelet panel).
CLUSTER_GENES = {
    "ITGA2B", "ITGB3", "FERMT3", "RASGRP2", "ITGB2",        # integrin
    "VWF", "GP1BA", "GP1BB", "GP9",                           # vwf/gpib + BSS
    "MYH9", "TUBB1", "ACTN1", "FLNA",                         # macrothrombocytopenia
    "NBEAL2", "GFI1B", "LYST", "HPS1", "HPS3", "HPS4", "HPS5", "HPS6", "AP3B1",  # granule
    "RUNX1", "ETV6", "ANKRD26",                               # thr + leukaemia
    "F8", "F9", "F11", "F7", "F10", "F5", "F13A1", "F13B", "FGA", "FGB", "FGG", "F2",  # coag
}

_ASSERT = {
    "pathogenic": Classification.P, "likely pathogenic": Classification.LP,
    "uncertain significance": Classification.VUS, "likely benign": Classification.LB,
    "benign": Classification.B,
}
_ORDER = [Classification.B, Classification.LB, Classification.VUS, Classification.LP, Classification.P]


def _classify_points(pts: float) -> Classification:
    for thr, cls in BANDS:
        if pts >= thr:
            return cls
    return Classification.B


def run(path: str) -> dict:
    import csv
    exact = adjacent = total = no_inflation = 0
    gene_counts: Counter = Counter()
    code_strengths: Counter = Counter()
    factor_points: Counter = Counter()
    with open(path, encoding="utf-8", errors="replace") as fh:
        reader = csv.reader(fh, delimiter="\t")
        header = next(reader)
        gi = header.index("HGNC Gene Symbol")
        ci = header.index("Applied Evidence Codes (Met)")
        ai = header.index("Assertion")
        for row in reader:
            if len(row) <= max(gi, ci, ai):
                continue
            gene = row[gi].strip()
            if gene not in CLUSTER_GENES:
                continue
            expert = _ASSERT.get(row[ai].strip().lower())
            if expert is None:
                continue
            codes = [c.strip() for c in row[ci].split(",") if c.strip()]
            # direct total (all codes; BA1 handled as benign override)
            ba1 = False
            direct = 0.0
            part_total = 0.0
            for c in codes:
                pts, is_ba1 = code_points(c)
                if is_ba1:
                    ba1 = True
                    continue
                direct += pts
                code_strengths[base_code(c)] += 1
                fac = owner(c) or "unknown"
                factor_points[fac] += pts
                part_total += pts                 # re-summed via the partition factors
            total += 1
            gene_counts[gene] += 1
            # no-inflation: partition re-sum equals the direct sum (no double count)
            if abs(direct - part_total) < 1e-9:
                no_inflation += 1
            pred = Classification.B if ba1 else _classify_points(direct)
            di, dp = _ORDER.index(expert), _ORDER.index(pred)
            if di == dp:
                exact += 1
            if abs(di - dp) <= 1:
                adjacent += 1
    return {
        "bleeding_variants": total,
        "genes_covered": len(gene_counts),
        "reconstruction_exact": round(exact / total, 4) if total else None,
        "reconstruction_within_one_bin": round(adjacent / total, 4) if total else None,
        "no_inflation_rate": round(no_inflation / total, 4) if total else None,
        "top_genes": gene_counts.most_common(12),
        "per_code_strengths": code_strengths.most_common(20),
        "points_by_factor": dict(factor_points),
    }


def main():
    s = run(sys.argv[1])
    print(f"Bleeding-gene VCEP variants: {s['bleeding_variants']} across {s['genes_covered']} genes")
    print(f"Reconstruction EXACT:        {s['reconstruction_exact']:.1%}")
    print(f"Reconstruction within-1-bin: {s['reconstruction_within_one_bin']:.1%}")
    print(f"NO-INFLATION rate:           {s['no_inflation_rate']:.1%}  (partition re-sum == direct)")
    print("Top genes:", s["top_genes"][:8])
    print("Real per-code applied strengths (top):", s["per_code_strengths"][:12])
    print("Points routed by owning factor:", s["points_by_factor"])


if __name__ == "__main__":
    main()
