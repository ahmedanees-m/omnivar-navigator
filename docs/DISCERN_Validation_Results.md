# DISCERN Validation Results (Tier A, real open data)

**Run:** 2026-06-13, on the VM, against real downloaded data. No synthetic data is used as
a result. Sources verified in *DISCERN_Validation_Verification_Report.md*.

## Tier A1 - ACMG combining fidelity + per-code partition on real ClinGen ERepo (headline variant result)

Ran `eval/erepo_reconstruction.py` over the real ClinGen Evidence Repository export
(`erepo_classifications.tab`), restricted to the DISCERN bleeding/platelet cluster genes.

| Metric | Result |
|---|---|
| Real VCEP-classified variants (bleeding genes) | **2,653** across 9 genes (RUNX1 1620, ITGA2B 358, ITGB3 250, VWF 119, F8 95, F9 71, GP1BA 66, GP1BB 37) |
| ACMG combining-rule fidelity, exact (vs VCEP label, from the experts' own codes) | **93.0%** |
| ACMG combining-rule fidelity, within one bin | **100.0%** |
| Partition vocabulary coverage (0 unknown codes) | **100%** |
| Variants carrying non-genetic codes (at risk of double-count) | **841** (**31.7%**) |
| Points routed out of the genetic stream | PP4 **1,443**, functional **393**, seg/phasing **794** |
| Variants a naive bottom-line score would over-classify (inflation prevented) | **549** (**20.7%**) |

**Observed per-code applied-strength distribution** (the VCEPs' own applied codes): PM2
1862, BP4 1010, PP4 593, BP7 564, PP3 523, PVS1 492, PM3 427, PS4 266, PM5 244, BA1 198,
PM1 196, PS3 167. This is the real *observed frequency* of applied strengths. The per-gene
*rule* strength tables in `rules/vcep/specs/*.yaml` were subsequently EXTRACTED and verified
(2026-06-13): the CSpec frequency criteria (BA1/BS1/PM2) and the PM2_Supporting strength are
now real for GT/F8/F9/VWF/GP1BA, from the CSpec registry (GN071 F8/F9, GN079 GP1BA, GN081 VWF -
note GN079 is the GP1BA spec, NOT GT, an earlier mislabel) cross-checked against the VCEPs'
own eRepo records. See `DISCERN_VCEP_Spec_Verification_Report.md`. The only residual
placeholders are the variant-dependent PVS1/PS4 strength decision trees (a documented
simplification, not a fillable value) and RUNX1's BA1/BS1 numeric thresholds.

**Points routed out of the genetic stream, by owning factor:** PP4 **1,443** (to the
disease-to-variant coupling), phasing 534, functional 393, segregation 260, de-novo 67.
This quantifies the motivation for the per-code partition: a tool that consumed the VCEP's
bundled bottom-line label would re-count this evidence in the genetic factor; here it is
owned by a single factor each and never re-added.

**Interpretation:** Gate G3 (no double-counting) is verified two ways: (i) a unit test
that the variant marginal is invariant to bundled PP4/PS3/PP1/PM3 codes, and (ii) the
per-code routing on 2,653 real variants above - owned codes appear in 31.7% of variants,
and for 549 (20.7%) the moved evidence is band-determining (a naive all-codes score would
over-classify them). It is **not** a calibration of the disease-variant coupling, which
awaits paired-phenotype cohorts. (The earlier "100% no-inflation rate" was a tautology -
it summed the same points twice - and has been replaced.)

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

The variant-layer validation is delivered by A1 (ACMG combining fidelity + the per-code
partition on real VCEP variants, including the uncertain ones). The per-patient VUS-reclassification
*rate* concordant with 3-star truth requires per-patient phenotype paired with VUS, which
the open variant databases do not provide standalone; it is run on the cohorts (Tier B/C)
where phenotype + variant co-occur. ClinVar 3-star remains the truth label for that run.

## Claim -> result crosswalk (what is proven now)

| Claim | Dataset | Result | Status |
|---|---|---|---|
| No double-counting (G3) | real ERepo per-code variants | invariant marginal (unit test) + 100% partition coverage on 2,653; owned codes in 31.7%, naive over-classifies 549 (20.7%) | **DONE (A); coupling calibration pending (B/C)** |
| ACMG combining-rule fidelity | real ERepo bleeding genes | 93.0% exact / 100% within-1-bin (arithmetic only) | **DONE (A)** |
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
