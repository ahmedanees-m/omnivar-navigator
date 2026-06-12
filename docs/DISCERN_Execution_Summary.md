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
| **Setup** verification + governance docs | — | 🟡 | DISCERN source verification ✅; summary doc ✅ |
| **P0** Foundations + VCEP loaders | 1–2 | ⏳ | extend schemas; rules/vcep/ specs (ITGA2B/ITGB3, F8/F9, RUNX1) |
| **P1** Evidence streams | 2–4 | ⏳ | genetic per-code partition, phenotype LR (+ negatives), lab |
| **P2** Cluster KB | 3–6 | ⏳ | 6 provenance-tagged discrimination clusters |
| **P3** Joint model (NOVEL CORE) | 5–8 | ⏳ | factor graph P(D,V\|E); reclassify; VCEP-reconstruction (G3) |
| **P4** Abstention + uncertainty | 7–9 | ⏳ | sparse-LR credible intervals; decide/abstain |
| **P5** Management-aware safety flag | 8–10 | ⏳ | treatment-danger interlock |
| **P6** Cheapest next observation | 9–11 | ⏳ | EIG over joint; partial-input; what-if |
| **P7** Equity & access | 10–11 | ⏳ | reuse reliability/routing + accessibility |
| **P8** Intake + UI + audit + learning | 9–13 | ⏳ | free-text→HPO; /diagnose orchestration |
| **P9** Validation (reader-first) | 11–16 | ⏳ | reader study, VUS-reclass, misdx-rescue, calibration |
| **P10** VUS-triage + expansion | 14–16 | ⏳ | assay-priority; new clusters via YAML only |
| **P11** Manuscript/release/host/KB | 14–18 | ⏳ | README→DISCERN, release, citable KB |

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

*(Phase sections appended below as they are executed.)*
