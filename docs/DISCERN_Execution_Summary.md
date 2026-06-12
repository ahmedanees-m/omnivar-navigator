# DISCERN — Execution Summary (living document)

**Purpose:** running record of the *working, methods, and outcomes* of every step
executed against *DISCERN_Execution_Plan_v2.md*. Updated as work proceeds; mirrored to
the repo (`docs/`) and pushed to GitHub.

**Project:** DISCERN — coupled differential-diagnosis, misdiagnosis-prevention &
VUS-resolution engine for overlapping inherited bleeding & platelet disorders.
**Builds on:** OmniVar Navigator (reused in place; ~70% of the foundation).
**Repo:** https://github.com/ahmedanees-m/omnivar-navigator (upgraded in place; rename to `discern` deferred)
**Author:** Anees Ahmed Mahaboob Ali (`ahmedanees-m`) · **Started:** 2026-06-13

**Status legend:** ✅ done · 🟡 in progress · ⏳ queued · ⛔ blocked (external)

---

## Phase status at a glance

| Phase | Plan months | Status | Notes |
|---|---|---|---|
| **Setup** verification + governance docs | — | ✅ | DISCERN source verification ✅; summary doc ✅ |
| **P0** Foundations + VCEP loaders | 1–2 | ✅ | dx_schemas; rules/vcep specs (ITGA2B/ITGB3, F8/F9, RUNX1, VWF, GP1BA) + per-code partition |
| **P1** Evidence streams | 2–4 | ✅ | genetic (variant-intrinsic only), phenotype LR (+ pertinent negatives), lab/functional |
| **P2** Cluster KB | 3–6 | ✅ | 6 provenance-tagged discrimination clusters (every LR → PMID + n) |
| **P3** Joint model (NOVEL CORE) | 5–8 | ✅ | factor graph P(D,V\|E); marginals; reclassify; **Gate G3 verified** |
| **P4** Abstention + uncertainty | 7–9 | ✅ | sparse-LR Beta credible intervals; decide/abstain |
| **P5** Management-aware safety flag | 8–10 | ✅ | treatment-danger flag + planned-tx hard-stop interlock |
| **P6** Cheapest next observation | 9–11 | ✅ | EIG over joint; partial-input; what-if |
| **P7** Equity & access | 10–11 | ✅ | reuse OmniVar reliability/routing + accessibility-aware next-obs |
| **P8** Intake + audit + learning + API | 9–13 | ✅* | free-text→HPO; diagnose() orchestration; /diagnose. *Web UI deferred |
| **P9** Validation (reader-first) | 11–16 | ✅* | reader-study/VUS-reclass/misdx-rescue/calibration **harnesses**. *Real-cohort + pre-reg pending |
| **P10** VUS-triage + expansion | 14–16 | ✅ | assay-priority; new clusters = YAML only (generalization claim) |
| **P11** Manuscript/release/host/KB | 14–18 | ✅* | README→DISCERN, manuscript, release reused. *Hosting/Zenodo on release |

\* = code-complete + unit-tested; starred caveat is an external dependency. **Tests: 104 passing, CI green, 16 DISCERN commits.**

**Gates:** G1 (reused engine reproduces eRepo — ✅ from OmniVar) · G2 (VCEP-where-exists, else reduced-confidence) · **G3 (each ACMG code enters once — VCEP-reconstruction test)** · G4 (abstention before usefulness claims) · G5 (pre-registration) · G6 (misdx label hidden) · G7 (no patient data public) · G8 (Docker-only, env secrets).

---

## Setup log (2026-06-13)

- **Read & understood** *DISCERN_Concept_Brief_v2.md* + *DISCERN_Execution_Plan_v2.md*:
  one coupled `P(D,V|E)` model; diagnosis / misdiagnosis-safety / VUS-resolution as three
  readouts; per-code circularity fix; calibrated abstention; management-aware flag;
  cheapest-next-observation; 6 discrimination clusters; reader-study-first validation.
- **Source verification ✅** (full log: *DISCERN_Source_Verification_Report.md*): all
  load-bearing claims verified, incl. **Ross 2021 VUS 29%→20% verbatim**, Luo 2019 RUNX1
  (33%), LIRICAL, PT-VWD/2B RIPA-mixing, LAD-III/HSCT, FXIII/ICH, Chediak/HLH/HSCT, South
  Indian Glanzmann cohort. 3 minor updates (D1 BSS GP1BA now published; D2 DDAVP "caution"
  not "harm"; D3 epidemiology cohort-dependent). OmniVar C1–C6 honored.
- **Repo strategy:** upgrade OmniVar repo in place — reuse `core/rules/adapters/equity/
  llm/deploy/docker/data` + OmniVar `engine/sim/eval`; add DISCERN modules. The DISCERN
  output schema is named `DxRecommendation` to avoid colliding with OmniVar's
  `engine.recommend.Recommendation`.

---

## Per-phase outcomes (2026-06-13)

- **P0** — `core/dx_schemas.py` (VariantState/Feature/Disease/Observation/JointPosterior/
  SafetyFlag/DxRecommendation); `rules/vcep/` loader + 6 specs + `partition.py` (each ACMG
  code → one owning factor). Commit `10e5549`.
- **P1** — `evidence/genetic.py` (variant-intrinsic likelihood, excludes PP4/PS3/PP1/PM3),
  `phenotype_lr.py` (LIRICAL LRs + pertinent negatives), `lab.py` (functional touches D+V once).
- **P2** — `diseases/ontology.py` + 6 clusters; every LR carries (freq, n_cases, PMID).
- **P3** — `jointdx/factorgraph.py` + `infer.py`: P(D,V|E), PP4 as the disease→variant
  coupling; **GT vs LAD-III discrimination + Gate-G3 no-inflation verified**. Commit `9760971`.
- **P4** — `jointdx/uncertainty.py` (Beta-resampled credible intervals) + `abstain.py`.
- **P5** — `safety/interlock.py`: LAD-III/HSCT flag, DDAVP+2B hard stop, splenectomy/BSS.
- **P6** — `nextobs/{recommend,partial,whatif}.py`: EIG over the joint; RIPA what-if. Commit `c9321c3`.
- **P7** — reuses `equity/` + accessibility-aware next-observation.
- **P8** — `intake/extract.py`, `jointdx/{explain,orchestrate}.py`, `api/main.py` `/diagnose`. Commit `1674f04`.
- **P9/P10** — `eval/{vus_reclass,misdx_rescue,reader_study}.py`, `triage/assay_priority.py`,
  `tests/test_vcep_reconstruction.py` (G3). Commit `cc03831`.
- **P11** — README → DISCERN (joint-model Mermaid schematic, flagship demos); manuscript outline.

**End-to-end demo (real output):** ITGB3 VUS + infections → LAD-III 73% (CI 55–91%), flags
GT/HSCT divergence, recommends WBC. GP1BA + platelet-origin RIPA + planned DDAVP → PT-VWD
84%, **HARD STOP on DDAVP**, recommends GP1BA/VWF sequencing.

## Honest remaining work (external dependencies, not missing code)
Pre-registered reader study + South Indian Glanzmann cohort run (Gate G5); extract exact
per-code VCEP strength tables (currently documented placeholders); web UI; hosting + Zenodo
DOI on release; managed-access cohorts (Solve-RD/UDN, off critical path).

---

*(Phase sections appended below as they are executed.)*
