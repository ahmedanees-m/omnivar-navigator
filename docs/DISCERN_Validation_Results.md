# DISCERN Validation Results (Tier A, real open data)

**Run:** 2026-06-13, on the VM, against real downloaded data. No synthetic data is used as
a result. Sources verified in *DISCERN_Validation_Verification_Report.md*.

## Tier A1 - VCEP reconstruction on real ClinGen ERepo (the headline variant result)

Ran `eval/erepo_reconstruction.py` over the real ClinGen Evidence Repository export
(`erepo_classifications.tab`), restricted to the DISCERN bleeding/platelet cluster genes.

| Metric | Result |
|---|---|
| Real VCEP-classified variants (bleeding genes) | **2,653** across 9 genes (RUNX1 1620, ITGA2B 358, ITGB3 250, VWF 119, F8 95, F9 71, GP1BA 66, GP1BB 37) |
| Reconstruction, exact | **93.0%** |
| Reconstruction, within one bin | **100.0%** |
| **No-inflation rate (per-code partition re-sum == direct total)** | **100.0%** (all 2,653 variants) |

**Real per-code applied strengths** (top, from the VCEPs themselves): PM2 1862, BP4 1010,
PP4 593, BP7 564, PP3 523, PVS1 492, PM3 427, PS4 266, PM5 244, PM1 196, PS3 167, PP1 155.
These are the actual VCEP per-code strengths - they retire the "per-code strengths are
placeholders" gap.

**Points routed by owning factor:** variant_intrinsic 3998, **disease_pp4 1443**,
phasing 534, functional 393, segregation 260, denovo 67. This quantifies the circularity
fix: 1,443 points of PP4 evidence are routed to the disease-to-variant coupling rather than
double-counted in the genetic factor, and 393 points of functional (PS3/BS3) and 794 of
segregation/phasing are owned by their own factors - never re-added in the genetic stream.

**Interpretation:** DISCERN reconstructs ClinGen VCEP classifications from their own
applied per-code evidence with high concordance and, on every single real variant, with no
inflation (no code double-counted). Gate G3 is now a real calibration result, not just a
unit test.

## Tier A3 - diagnosis benchmark on the open GA4GH Phenopacket Store

Ran `eval/phenopacket_benchmark.py` over the cloned `phenopacket-store` (11,155
phenopackets). After extracting the causal gene from the interpretation and excluding
thrombophilia cases (elevated factor VIII / DVT / PE - outside DISCERN's bleeding clusters):

| Metric | Result |
|---|---|
| In-cluster cases found | **4** (1 LAD-III/FERMT3, 3 Chediak-Higashi/LYST) |
| Top-1 accuracy | **100%** (4/4) |
| Top-3 accuracy | **100%** |

**Honest finding:** Phenopacket Store is a general rare-disease corpus and is thin on
inherited bleeding/platelet disorders - only 4 cases fall in DISCERN's clusters (consistent
with the plan's section 3D). DISCERN diagnoses all 4 correctly, but the diagnosis-accuracy
headline cannot rest on n=4. The PhEval-compatible runner is in place; the diagnosis
benchmark headline requires the curated published-case set (Tier A, hand-built) and the
cohorts (Tier B/C).

## Tier A2 - VUS reclassification

The variant-layer validation is delivered by A1 (reconstruction on real VCEP variants,
including the uncertain ones, with no inflation). The per-patient VUS-reclassification
*rate* concordant with 3-star truth requires per-patient phenotype paired with VUS, which
the open variant databases do not provide standalone; it is run on the cohorts (Tier B/C)
where phenotype + variant co-occur. ClinVar 3-star remains the truth label for that run.

## Claim -> result crosswalk (what is proven now)

| Claim | Dataset | Result | Status |
|---|---|---|---|
| No double-counting (G3, calibrated) | real ERepo per-code variants | 100% no-inflation on 2,653 variants | **DONE (A)** |
| Classifier reproduces experts | real ERepo bleeding genes | 93.0% exact / 100% within-1-bin | **DONE (A)** |
| Per-code strengths are real, not placeholders | real ERepo | extracted true strength distribution | **DONE (A)** |
| Differential-diagnosis accuracy | Phenopacket Store bleeding subset | 4/4 Top-1 (small N; corpus thin) | **partial (A); needs curated + cohorts** |
| VUS reclassification rate | ClinVar 3-star + cohorts | variant layer done; rate needs cohorts | pending (B/C) |
| Misdiagnosis rescue | ITP cohort (Blood Adv 2025), BRIDGE-BPD | harness built; needs DAC access | pending (B) |
| Equity / real patient | South Indian Glanzmann cohort | harness built; needs IRB | pending (C) |
| Calibration / abstention | labeled sets | harness built (eval/calibration.py, abstain.py) | runs on labeled cohorts |

## What remains (external access, not missing code)

Tier B (BRIDGE-BPD `EGAS00001001172`, the 80-patient ITP cohort): apply to the NIHR
BioResource DAC (`dac@bioresource.nihr.ac.uk`) - institutional affiliation, IRB, proposal,
signed DAA; weeks to months. Tier C (South Indian Glanzmann cohort): local IRB,
aggregate-only, no patient data in public artifacts. Pre-register the full protocol and the
reader study on OSF before those analyses. The harnesses (`eval/misdx_rescue.py`,
`eval/vus_reclass.py`, `eval/reader_study.py`, `eval/phenopacket_benchmark.py`) run as soon
as access clears.
