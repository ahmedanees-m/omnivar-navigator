# DISCERN v3.1 - Claims Map (claim -> evidence -> status)

**Purpose (Track D1):** lock every public claim to its evidence and its honest status, and split
the **defensible-now methods+variant paper** from the **cohort-gated coupling/clinical paper**.
Scope language is audited against Execution Plan Section A. Gate G13: no "the coupling works"
claim until paired-cohort data reports the pre-registered endpoint.

## Paper 1 - Methods + Variant engine (DEFENSIBLE NOW; needs no cohorts)

| Claim | Evidence | Status |
|---|---|---|
| The per-code partition prevents evidence double-counting | Genome-wide: **100% partition coverage** on 12,240 variants / 170 genes; **33.2%** inflation-prevented (Wilson 95% CI 32.4-34.1); + the variant-marginal invariance unit test | **DONE (open data)** |
| Gene-specific freq thresholds reproduce VCEP freq codes on real gnomAD AFs | gnomAD per-variant cross-check: **97.8%** concordance on 629 variants (curator-cited gnomAD AFs) | **DONE** |
| ACMG combining-rule fidelity | **93.0% exact / 100% within-one-bin** on 2,653 bleeding-panel eRepo variants (arithmetic given experts' codes) | **DONE** |
| Intrinsic-only band concords with the ClinVar community label | **62.4% exact / 92.8% within-one-bin** on 10,780 matched; intrinsic-only is a *designed lower bound* (omits routed PP4/PS3/PP1/PM3) - disagreements characterised, not errors | **DONE (characterised)** |
| Variant probabilities are calibratable | Isotonic **ECE 0.008 / Brier 0.0073** (vs uncalibrated 0.201/0.060) on 7,521 ClinVar-labelled variants; AUC 0.999 (P/B extremes) | **DONE (H5 variant half)** |
| Gene-specific CSpec criteria extracted | BA1/BS1/PM2 + PM2_Supporting for GT/F8/F9/VWF/GP1BA (CSpec GN071/GN079/GN081 + eRepo) | **DONE** |
| Novel-variant scoring (freq codes + PVS1/PS4 trees + injectable predictors) | `rules/variant_scoring.py` + tests; H4 in-text run (483 variants): gene-specific AUC 0.900, generic-ACMG/InterVar-paradigm 0.903, REVEL-alone 0.961 | **code-complete; H4 partial (honest)** - on freq+REVEL only the thin score trails REVEL; full H4 needs all predictors per-variant + literal InterVar (ANNOVAR) |
| Full confusable-cluster coverage C1-C10 | 10 clusters, every LR PMID-sourced (CI-guarded), per-cluster safety map | **DONE (B)** |
| Management-aware safety incl. leading-call hard-stop | interlock fix + per-cluster contraindications (DDAVP/2B, splenectomy/inherited-IT, rFXIII-A2/F13B, platelets/Quebec, HSCT) + regression tests | **DONE (B)** |
| Selective/conformal coverage guarantee | Mondrian split-conformal machinery + synthetic-faithful sanity | **machinery DONE**; real-label coverage cohort-gated |

## Paper 2 - Coupling + Clinical (COHORT-GATED; pre-registered)

| Claim | Evidence path | Status |
|---|---|---|
| The coupling improves VUS reclassification over intrinsic-only | Pre-registered endpoint H6 (+ explicit falsification), on BRIDGE-BPD / ITP / Glanzmann paired data | **NOT CLAIMED** until paired data (G12 reg, G13 gate) |
| Misdiagnosis rescue (label-hidden case-control) | `eval/misdx_rescue.py` on the ITP cohort / BRIDGE-BPD | gated (DAC) |
| Diagnosis accuracy at scale | curated cases **Top-1 80% / Top-3 100% (n=10)** + Phenopacket 4/4 now; cohorts for the headline | **partial (A); gated (B/C)** |
| Per-patient VUS-reclassification rate vs 3-star truth | needs paired phenotype+variant | gated (B/C) |
| Reader study (usefulness) | pre-registered vignette protocol | own (pre-reg) |

## Scope-language rules (audited)
"Partition / arithmetic fidelity / calibration / cluster coverage" = **proven on open data**.
"Coupling" = **pending or negative**, never "validated", until Paper 2's paired-data result.
"Coverage" (cluster breadth) is never conflated with "accuracy". Every synthetic result is
labelled sanity, never a headline. No patient data appears in any public artifact (G7).
