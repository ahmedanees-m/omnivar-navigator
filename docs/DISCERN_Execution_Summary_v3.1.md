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
| **A1** Genome-wide partition + ClinVar concordance | in progress | partition genome-wide + ClinVar 2*+ concordance runnable on VM; gnomAD per-variant cross-check data-gated |
| **A2** Complete variant-intrinsic scoring (predictors, strength trees, novel-variant) | queued | REVEL + Pangolin(real version) + AlphaMissense(CC BY 4.0); PVS1/PS4 trees; RUNX1 BA1/BS1 |
| **A3** Variant calibration (isotonic/Platt; ECE/Brier) | queued | vs ClinVar 2*+ |
| **B1** Cluster curation C4->C3->C5->C8->C6->C7->C9->(C10) | in progress | C4 (RUNX1/ANKRD26/ETV6 vs ITP/MDS) first |
| **B2** Uncertainty + selective/conformal prediction | queued | Mondrian split-conformal; abstention threshold |
| **B3** Safety-interlock hardening (leading-call fix + per-cluster map) | in progress | fix the documented leading-call defect first |
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

*(appended as steps execute)*
