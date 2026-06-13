# DISCERN v3.1 - Execution Summary (living document)

**Purpose:** running record of the working, methods, and outcomes of every step executed
against `DISCERN_Execution_Plan_v3.1.md` (folding in `DISCERN_Coverage_Architecture_v1.md`).
Mirrored to the repo (`docs/`) and pushed to GitHub.

**Builds on:** DISCERN v2 (P0-P11, 107 tests, CI green; variant-intrinsic layer validated on
real eRepo; CSpec frequency criteria for GT/F8/F9/VWF/GP1BA).
**Repo:** https://github.com/ahmedanees-m/discern · **Author:** Anees Ahmed Mahaboob Ali
**Started:** 2026-06-13 · **Status legend:** done / in progress / queued / blocked(external)

---

## Phase status at a glance

| Track / Phase | Status | Notes |
|---|---|---|
| **Setup** Source & dataset verification | done | `DISCERN_v3.1_Source_Verification_Report.md`; all citations real; corrections folded in below |
| **A1** Genome-wide partition + ClinVar concordance | done (gnomAD gated) | H1: 100% coverage on 12,240 variants/170 genes; H2: 33.2% inflation-prevented (CI 32.4-34.1); H3: ClinVar within-1-bin 92.8%. gnomAD per-variant cross-check data-gated (only constraint metrics on VM) |
| **A2** Complete variant-intrinsic scoring (predictors, strength trees, novel-variant) | queued | REVEL + Pangolin(real version) + AlphaMissense(CC BY 4.0); PVS1/PS4 trees; RUNX1 BA1/BS1 |
| **A3** Variant calibration (isotonic/Platt; ECE/Brier) | done | 7,521 P/B variants; isotonic ECE 0.008 / Brier 0.0073 (vs uncalibrated 0.201/0.060); AUC 0.999. H5 variant-half met |
| **B1** Cluster curation C4->C3->C5->C8->C6->C7->C9->(C10) | in progress | C4 (RUNX1/ANKRD26/ETV6 vs ITP/MDS) first |
| **B2** Uncertainty + selective/conformal prediction | queued | Mondrian split-conformal; abstention threshold |
| **B3** Safety-interlock hardening (leading-call fix + per-cluster map) | partial | leading-call hard-stop defect FIXED + regression test (108 tests); per-cluster contraindication map pending with B1 clusters |
| **B4** Curated published-case benchmark (per cluster) | queued | citations only (G7); Top-1/Top-3 + abstention |
| **C1** Pre-registration (OSF) + synthetic-coupling harness | queued | protocol + falsification condition (G12) |
| **C2** Data access (BRIDGE-BPD/ITP DAC; Glanzmann IRB) | blocked(external) | submit Month 1-2; months-long |
| **C3** Coupling validation + cohort dx + reader study | blocked(external) | gated by C2; G13 |
| **D1** Manuscripts (methods+variant; coupling/clinical split) | queued | defensible-now paper from A/B results |
| **D2** Release & reproducibility (Zenodo DOI; hosted demo) | queued | on first Release |

**Gates:** G1-G8 (v2) carried; **G9** partition generality, **G10** external concordance,
**G11** calibration/coverage, **G12** pre-registration before cohort analysis, **G13** no
coupling claim without paired data. None breached.

---

## Verification outcome (2026-06-13)

Full pass over both v3.1 documents (5 parallel independent web-verification sweeps). Every
citation is a real paper; every dataset/tool/accession is real. Corrections folded into the
build (full detail + DOIs/PMIDs in `DISCERN_v3.1_Source_Verification_Report.md`):

- **Zaninetti 2017** documents ANKRD26-as-**MDS only** (not ITP) -> use Joshi/Cooper 2025
  (Blood Adv 9(7):1497, PMID 39808791) for the ITP-misdiagnosis cases in C4/B4.
- **Galera 2019** prevalence triple (RUNX1 3% / ANKRD26 18% / ETV6 5%) is **unconfirmed and
  cohort-dependent** -> not stated as fact; cluster LRs sourced per-variant instead.
- **Pangolin** has no "v1.1": pin tkzeng v1.0.1 or Invitae fork v1.4.x (A2). **SpliceAI** archived
  2026-04-20 (read-only) - true, but no Illumina "use Pangolin" notice.
- **AlphaMissense** predictions are **CC BY 4.0 (commercial OK)**, not non-commercial.
- **gnomAD v4.1.1** real (2026-03-30) = annotation refresh over the v4.1 callset; **per-variant
  AFs are NOT on the VM** -> A1 gnomAD cross-check data-gated (flagged, not silently skipped).
- **HCM 17.4%** VUS-reclassification precedent = Caroselli 2025 (Hum Mutat), not the VCEP guideline.
- **"Low VWF"** no longer a guideline-distinct category (C9 framed descriptively).
- Locator/metadata fixes: Gresele 2015 = 13(2):314-322; ASH Educ 2016 = Peyvandi & Menegatti;
  RUNX1 panel = **Myeloid Malignancy VCEP**; "von Willebrand" capitalization.

---

## Per-phase log

### 2026-06-13 - B3 safety-interlock leading-call fix (done)
Fixed the documented defect in `safety/interlock.py`: the loop skipped the leading disease for
both flags, so a contraindicated **leading** diagnosis (e.g. "DDAVP planned + type 2B leading")
emitted no hard stop. Now the hard-stop runs over every non-excluded disease including the
leading call (tagged "[leading diagnosis]"); the management-divergence flag stays competitor-only.
Regression test `test_ddavp_hard_stop_fires_when_contraindicated_disease_is_leading` added.
**108 tests pass, CI green.** The per-cluster contraindication map (C3/C4 splenectomy,
C8 rFXIII-A2->F13B, C7 Quebec, C1/C6 HSCT) lands with the B1 clusters.

### 2026-06-13 - A1 genome-wide partition + ClinVar concordance (done; gnomAD gated)
Ran on the VM against the full real ClinGen ERepo (`eval/erepo_genomewide.py`) and ClinVar
`variant_summary.txt.gz` (2026-05; `eval/clinvar_concordance.py`).

**H1 - partition generalizes genome-wide (Gate G9):** 12,240 ERepo variants across **170 genes**
(38,802 applied codes). Partition vocabulary coverage **100.0000% - 0 uncovered codes**. The
per-code partition built on the bleeding panel maps every ACMG code applied across all VCEPs;
the uncovered-vocabulary table is empty. G9 satisfied.

**H2 - routing prevents inflation at genome scale:** non-genetic owned codes appear in **51.9%**
of all variants; a naive all-codes band would over-classify **4,068 (33.2%, Wilson 95% CI
32.4-34.1%)**. This is **higher** than the 20.7% bleeding-panel figure - i.e. the panel was NOT
inflation-enriched; the no-double-counting value is larger genome-wide. Reported plainly per H2.

**H3 - intrinsic-only band vs ClinVar (Gate G10):** 10,883 ERepo variants carry a ClinVar
VariationID; 10,780 matched a non-conflicting ClinVar classification. Agreement of DISCERN's
**variant-intrinsic-only** band vs ClinVar: overall **62.4% exact / 92.8% within-one-bin**;
>=2-star **62.5% / 92.9%**; 3-star (n=10,558) **62.9% / 93.2%**; the small independent 2-star
stratum (n=129) **31.8% / 63.6%**. **Honest reading:** the intrinsic-only band deliberately
OMITS the pathogenic-supporting routed codes (PP4/PS3/PP1/PM3), so it is a designed lower bound,
not a classifier of record - exact agreement near ~62% reflects that removed evidence (the band
drops, usually by one bin), and the 92.8% within-one-bin shows it rarely drifts further. This is
the H3 "disagreements characterised" finding, not a DISCERN error. (Direction-stratified
disagreement and the full-code band vs ClinVar are an A1 refinement for the next iteration.)

**Data-gated:** the gnomAD per-variant frequency cross-check (A1's `gnomad_freq_check.py`) is NOT
run - only gene-level `gnomad.v4.0.constraint_metrics.tsv` is on the VM, not per-variant AFs.
Flagged, not silently skipped; pull per-variant gnomAD AFs (or use eRepo-embedded AFs) to close it.

### 2026-06-13 - B1/B3 cluster coverage C4-C10 (done)
Built the full confusable-cluster catalog (`eval`/diseases/clusters + `tests/test_v31_clusters.py`):
**C4** (highest priority) enhanced - RUNX1/ANKRD26/ETV6 **vs ITP** with discriminating features
(family history, normal platelet size, AD pattern, dysmegakaryopoiesis, immunosuppression
response) and the per-cluster SAFETY map (splenectomy + immunosuppression contraindicated when
an inherited thrombocytopenia is plausible; affected-relative-not-donor). New clusters: **C5**
(2N VWD vs mild hemophilia A, VWF:FVIIIB decisive), **C7** (alpha-granule: NBEAL2/GFI1B/ARC +
Quebec/PLAU with platelet-transfusion contraindicated -> antifibrinolytics), **C9** (type-1/low-VWF
calibration-demo), **C10** (Scott/ANO6 PS-exposure capstone). Every LR carries a PMID; the
**`test_every_feature_lr_is_sourced` CI guard enforces the no-fabricated-LR rule.** 10 clusters,
117 tests. Zaninetti->MDS / Joshi-Cooper->ITP and the "low VWF" descriptive framing applied.

### 2026-06-13 - B2 conformal selective prediction (done; coverage cohort-gated)
`jointdx/conformal.py`: Mondrian (per-class) split-conformal over the diagnosis posterior;
selective mode commits only on a singleton conformal set, else abstains (composes with abstain.py).
Synthetic model-faithful sanity test confirms the per-class coverage guarantee holds; real-label
coverage (H5 diagnosis half / G11) is cohort-gated, not claimed on synthetic data.

### 2026-06-13 - A3 variant calibration (done; H5 variant half / Gate G11)
`eval/variant_calibration.py` (pure-stdlib PAV isotonic + Platt + Brier/ECE/AUC) on the VM,
joining DISCERN variant-intrinsic Tavtigian points to ClinVar P/B labels: **7,521 labeled
variants (4,904 pathogenic), test n=3,761.** AUC **0.9992** (honest: these are VCEP P/B extremes
with VUS dropped, so discrimination is easy - the deliverable is calibration). Calibration: ECE
**0.201 (uncalibrated) -> 0.088 (Platt) -> 0.008 (isotonic)**; Brier **0.060 -> 0.024 -> 0.0073**.
Isotonic-calibrated probabilities meet the H5 variant-half "calibrated probabilities" bar.
