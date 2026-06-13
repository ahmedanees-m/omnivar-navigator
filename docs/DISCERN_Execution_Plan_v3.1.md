# DISCERN — Execution Plan v3.1 (Engine Expansion, Full-Coverage & External Validation)

**Version:** 3.1.0 · **Date:** 2026-06-13
**Supersedes:** *DISCERN_Execution_Plan_v3.md* (v3.0.0) — this revision folds in the literature-grounded coverage map.
**Incorporates:** *DISCERN_Coverage_Architecture_v1.md* (the cited disease/gene/cluster map; its Part 4 sets Track A's gene panel and its Parts 2–3 set Track B's clusters).
**Builds on:** DISCERN v2 (P0–P11 code-complete, unit-tested; variant-intrinsic layer validated on real ClinGen eRepo).
**Repo:** https://github.com/ahmedanees-m/discern/ · **Author:** Anees Ahmed Mahaboob Ali (`ahmedanees-m`)
**Target venues:** *npj Genomic Medicine* / *Genetics in Medicine* (methods + variant paper); a haematology-genomics venue (clinical-discrimination paper).
**Status legend:** ✅ done · 🟡 in progress · ⏳ queued · ⛔ blocked (external/managed access)

---

## A. Executive positioning (what we are building and why it matters)

**Problem.** In inherited bleeding & platelet disorders, look-alike conditions diverge in treatment and cancer surveillance, and getting them wrong causes real harm: Glanzmann mistaken for LAD-III misses a curative transplant; type 2B VWD mistaken for platelet-type VWD inverts the treatment; inherited thrombocytopenias (RUNX1/ANKRD26/ETV6) mistaken for ITP trigger unnecessary immunosuppression **and** miss leukemia surveillance and donor-selection implications. In parallel, variants of uncertain significance accumulate because phenotype evidence is not integrated rigorously.

**What DISCERN does.** One coupled `P(D,V|E)` engine produces five auditable outputs: (1) a calibrated **differential diagnosis**; (2) a VCEP-anchored **variant reclassification** that integrates phenotype *without double-counting*; (3) a management-aware **treatment-safety flag**; (4) the cheapest **decisive next test**; (5) explicit **abstention** when the evidence cannot decide.

**Novelty (ranked by how proven it is).**
- **Proven now —** the **per-code partition**: each ACMG code enters exactly one factor, so coupled evidence is never double-counted; demonstrated on 2,653 real eRepo variants (549/20.7% band-inflations prevented). The VCEP-reclassification paradigm is already validated in other domains (e.g. HCM, 17.4% VUS reclassified) — DISCERN is the first to bring it, **coupled and safety-aware**, to bleeding/platelet disorders.
- **Novel integration —** a single engine emitting differential + VUS-call + safety-flag + next-test + abstention for a *specific confusable domain*; no existing tool (general DDx engines like Exomiser/LIRICAL/DeepRare; variant classifiers like VarSome/InterVar) does this combination.
- **Novel core, unproven —** the **coupling** (calibrated phenotype → PP4 → reclassification). Empirically unvalidated; cohort-gated (Track C). No public dataset can validate it.

**Who benefits & how.** *Clinicians:* a transparent second read that catches the traps, warns before a contraindicated drug, and names the deciding test — abstaining instead of bluffing. *Variant curators:* consistent, auditable, VCEP-anchored reclassification across the whole panel, double-count-free, at scale. *Researchers:* an open, deterministic, fully-cited engine with every value traceable.

**Input / Output.** *Input (any subset; degrades gracefully):* a variant (gene + applied ACMG codes, or raw `gene:HGVS` it scores itself), clinical/lab findings as present/absent/unknown, optional planned treatment. *Output:* ranked differential + credible intervals + verdict (confident/leaning/undecidable); variant call + reclassification drivers; treatment-safety flag; most-decisive next test; explicit abstention — each traceable to its evidence.

**Honest scope.** DISCERN *reduces un-integrated VUS and triages the rest*; *mitigates in-cluster misdiagnosis*; and its coupling is *validated on cohorts or reported negative* — never claimed before paired-data results exist (Gate G13).

---

## Changelog: v3.0 → v3.1

| # | Change | Rationale |
|---|---|---|
| 1 | **Coverage is now specified, not sketched.** Track A's gene panel = the full ISTH TIER1 curated set (Coverage Arch. Part 4); Track B's clusters = the cited **C1–C10 catalog** (Coverage Arch. Part 2), built in the harm-ranked **priority order** (Part 3). | "Most diseases" was motion; the confusable space is finite and now enumerated from the classification bodies. |
| 2 | Added the **executive positioning** (Section A): problems solved, novelty vs global tools, beneficiaries, I/O. | Locks the claim set to evidence and makes the value legible. |
| 3 | Cluster priority reorders the build: **C4 (RUNX1/ANKRD26/ETV6 vs ITP/MDS) is first** — gravest miss (cancer surveillance + donor selection). | Maximize clinical value per unit build; not effort-gated. |
| 4 | Safety-interlock map (B3) is extended **per cluster** (DDAVP↛2B, avoid-splenectomy-when-inherited, rFXIII-A₂↛F13B, antifibrinolytics-not-platelets for Quebec, HSCT flags for LAD-III/Chediak) — each sourced. | Each new cluster carries a real, citable management-divergence. |
| 5 | The curated case benchmark (B4) is populated **per cluster** from the misdiagnosis case literature (e.g. ANKRD26-as-MDS, RUNX1/ANKRD26-as-ITP). | Real, cited diagnosis-accuracy cases now exist across clusters. |

*(All v3.0 content — hypotheses, gates G9–G13, risk model, sequencing — carried forward, refined below.)*

---

## 0. Where v3 starts (verified end state of v2)

- **Engine:** P0–P11 code-complete, **107 tests passing, CI green**. Coupled `P(D,V|E)`; per-code partition (Gate G3 verified); abstention + Beta credible intervals; management-aware safety flag + hard-stop interlock; EIG next-observation; free-text→HPO intake; `/diagnose` API; web app (diagnosis + partition tools).
- **Variant-intrinsic validation (real eRepo):** 2,653 bleeding-gene variants → **93.0%** ACMG combining fidelity (100% within-one-bin; arithmetic given experts' codes, not coupling), **100% partition coverage**, owned non-genetic codes in **31.7%**, **549 (20.7%)** inflations prevented. Per-gene CSpec frequency criteria extracted/verified for GT/F8/F9/VWF/GP1BA.
- **Diagnosis validation:** Phenopacket Store → 4 in-cluster cases, 4/4 Top-1 (honestly non-headline).
- **The gap v3 closes or bounds:** the **coupling** (no paired phenotype in eRepo — untestable there); diagnosis accuracy at scale; per-patient VUS-reclassification rate.
- **Known defect to fix (B3):** the contraindication hard-stop skips the leading call (`safety/interlock.py`), so "DDAVP planned + 2B leading" emits only a divergence flag.

---

## 1. The honest split (doable-now vs gated) — the organizing spine

| Lane | Public data / code (do now) | Managed access (paperwork now, run later) |
|---|---|---|
| **Variant** | Full-panel genome-wide partition validation; ClinVar concordance; gnomAD frequency cross-check; wire Pangolin/REVEL/AlphaMissense; strength trees; novel-variant scoring; variant calibration | — |
| **Diagnosis** | Curate C1–C10 (C4 first); conformal/selective prediction; curated published-case benchmark; safety-interlock fix + per-cluster map | Diagnosis accuracy at cohort scale; reader study; per-patient VUS-reclassification rate |
| **Coupling (novel core)** | Pre-register protocol; synthetic-coupling sanity harness | **The coupling validation itself** (BRIDGE-BPD/ITP DAC; South Indian Glanzmann IRB) |

**Principles (non-negotiable):** no fabricated LRs (every value → source); abstention before usefulness claims (G4); report negative results; keep partition/arithmetic ≠ coupling ≠ diagnosis-accuracy validation distinct in every claim.

---

## 2. Objectives & Hypotheses

| # | Hypothesis | Success criterion | Negative result & how reported |
|---|---|---|---|
| **H1** | The per-code partition **generalizes genome-wide**. | Partition coverage ≥ 99% of applied codes across all eRepo genes; the ≤1% enumerated/resolved. | Coverage < 99% → publish the uncovered code vocabulary as a limitation table; extend the partition. |
| **H2** | Routing once **prevents inflation at genome scale**. | Inflation-prevented rate + 95% CI across all genes; consistent with the 20.7% panel result. | Lower rate → report plainly; the panel was enriched; the method still prevents every double-count it finds. |
| **H3** | Intrinsic-only band **agrees with ClinVar** consensus. | Agreement (exact + within-one-bin) vs ClinVar 2★+, per gene and overall; disagreements characterised. | Low agreement → a real VCEP-vs-aggregate finding; reported as a concordance table. |
| **H4** | With predictors wired, DISCERN **scores novel variants** competitively. | Held-out ClinVar AUC/accuracy vs points-only and vs InterVar, stratified by predictor availability. | Underperformance → reported in the benchmark table. |
| **H5** | Confidence is **calibrated**; selective prediction gives a **coverage guarantee**. | ECE/Brier on held-out labels; Mondrian split-conformal empirical coverage within ±tolerance of (1−α) per class. | Miscalibration → reliability diagrams; failed coverage → re-derive threshold, document. |
| **H6** | The **coupling improves reclassification** over intrinsic-only **on paired data**. *(Gated.)* | Pre-registered primary endpoint, coupling vs intrinsic-only, circularity guard active. | **Explicit falsification:** no improvement on paired data is the headline negative result; pre-registration fixes this before data is seen. |
| **H7** | DISCERN **reduces in-cluster misdiagnosis** and surfaces treatment-changing competitors. *(Partly gated.)* | Curated case Top-1/Top-3 (now); cohort misdiagnosis-rescue (gated); safety-flag sensitivity on known confusable pairs. | Small-n caveat now; cohort result vs pre-registered endpoint. |

---

## 3. Tracks & Phases

### Track A — Variant engine: generalize, complete, calibrate *(public; now)*

**Gene panel = ISTH TIER1 full curated set** (Coverage Arch. Part 4): all platelet (~70), VWD (VWF + GP1BA), coagulation (F8/F9/F11/F2/F5/F7/F10/F12/F13A1/F13B/FGA/FGB/FGG/LMAN1/MCFD2/GGCX/VKORC1), and vascular/fibrinolytic catalog genes. VCEP anchors: Platelet Disorders (ITGA2B/ITGB3, GP1BA), Coagulation Factor (F8, F9), VWD (VWF), RUNX1.

- **A1 — Genome-wide partition validation + external concordance (was 38-gene; now full panel).** Drop the gene restriction; add ClinVar concordance (`eval/clinvar_concordance.py`) and gnomAD frequency cross-check (`eval/gnomad_freq_check.py`); re-run; record numbers + 95% CIs. **Acceptance:** H1/H2/H3. **Data:** VM (eRepo, ClinVar, gnomAD v4.1.1).
- **A2 — Complete variant-intrinsic scoring (novel-variant capable).** Wire REVEL + **Pangolin v1.1** (SpliceAI archived) → PP3/BP4 at CSpec cut-offs; AlphaMissense as secondary feature; variant-dependent PVS1 (NMD/domain) and PS4 (proband ratio) strength trees; RUNX1 BA1/BS1; `score_variant(gene, hgvs)` end-to-end. **Acceptance:** H4 on held-out ClinVar vs points-only and InterVar.
- **A3 — Variant calibration.** Isotonic (Platt baseline) points→P(pathogenic) vs ClinVar 2★+; reliability/ECE/Brier; expose calibrated probabilities. **Acceptance:** H5 (variant half).

### Track B — Diagnosis: full-coverage clusters & rigor *(public; now)*

**Clusters = Coverage Arch. C1–C10, built in priority order (Part 3):**

| Order | Cluster | Build note |
|---|---|---|
| ✅ | **C1** GT/LAD-III/RASGRP2 · **C2** 2B/PT-VWD/2A | already built |
| 1 | **C4** RUNX1/ANKRD26/ETV6 vs ITP/MDS | gravest miss; RUNX1 VCEP anchors |
| 2 | **C3** macrothrombocytopenia (BSS/MYH9/ACTN1/TUBB1/FLNA) vs ITP | unnecessary-splenectomy trap |
| 3 | **C5** 2N VWD vs mild hemophilia A | two-gene coupled story (VWF + F8 VCEPs) |
| 4 | **C8** FXIII (F13A1 vs F13B) | genotype changes the drug |
| 5 | **C6** HPS/Chediak/δ-SPD | syndromic clues → HSCT/surveillance |
| 6 | **C7** α-granule (NBEAL2/GFI1B/ARC/Quebec) | myelofibrosis surveillance |
| 7 | **C9** mild VWD / low VWF | high volume; calibration/abstention demo |
| 8 | **C10** Scott syndrome (ANO6) | optional capstone |

- **B1 — Cluster curation.** Each cluster = YAML + sourced `(freq, n_cases, PMID)` LRs + pertinent negatives, at the VCEP-spec provenance bar; each cluster's decisive observation feeds the EIG next-observation module. Each new cluster = data only, no engine change (the generalization claim). Mini source-verification appended to `DISCERN_Source_Verification_Report.md`.
- **B2 — Uncertainty + selective/conformal prediction.** Principled posterior credible intervals; Mondrian (per-class) split-conformal so "when DISCERN commits, it is right ≥ (1−α)"; abstention threshold from a calibration split. **Acceptance:** H5 (diagnosis half).
- **B3 — Safety-interlock hardening.** **Fix** the leading-call contraindication defect (run the hard-stop over all non-excluded diseases incl. the leading call; keep divergence competitor-only) + regression test. Extend the divergence/contraindication map per cluster — at minimum: DDAVP↛2B (C2), avoid splenectomy/immunosuppression when an inherited thrombocytopenia is plausible (C3/C4), rFXIII-A₂↛F13B (C8), antifibrinolytics-not-platelets for Quebec (C7), HSCT-relevant flags for LAD-III/Chediak (C1/C6) — each sourced.
- **B4 — Curated published-case benchmark.** Per-cluster phenopacket-style records from the cited case literature (e.g. ANKRD26-as-MDS [Zaninetti 2017], RUNX1/ANKRD26-as-ITP); citations only, no identifiers (G7); Top-1/Top-3 + abstention; head-to-head vs Exomiser (PhEval) where images exist. **Acceptance:** H7 (now-half, small-n caveat).

### Track C — The coupling & cohorts *(the prize; gated; start now)*

- **C1 — Pre-register (OSF), then locked.** Coupling primary endpoint (H6, with the explicit falsification condition) + reader-study protocol; pre-specify figures/tables and negative-result reporting; build `eval/synthetic_coupling_harness.py` (sanity, not validation). **Gate G12.**
- **C2 — Data access (the rate-limiter; submit Month 1–2).** NIHR BioResource/BRIDGE-BPD DAC (`EGAS00001001172`) + 80-patient ITP cohort; South Indian Glanzmann local IRB (aggregate-only); Solve-RD/UDN as off-critical-path. ⛔ External; months-long.
- **C3 — Coupling validation + cohort diagnosis + reader study (gated by C2).** Run the pre-registered endpoints (H6/H7); per-patient reclassification + misdiagnosis-rescue; reader study; cohort calibration; report regardless of direction. **Gate G7** held throughout.

### Track D — Positioning & release *(parallel)*

- **D1 — Manuscripts & honest scope.** Methods+variant paper (defensible now: partition, genome-wide generalization, concordance, calibration, novel-variant scoring) split from the coupling/clinical paper (gated on C3); claims-map; scope language audited against Section A.
- **D2 — Release & reproducibility.** Hosting (Docker-only, env secrets — G8); Zenodo DOI on first Release; finalize the public web app as demonstrator; reproducibility checklist; clean-clone reproduction of every public number.

---

## 4. Gates (carry G1–G8 from v2; add)

- **G9 — Partition generality.** Genome-wide coverage table + enumerated uncovered vocabulary before any "generalizes" claim (H1).
- **G10 — External concordance reported.** ClinVar + gnomAD cross-checks run and reported (incl. disagreements) before the variant paper's claims (H3).
- **G11 — Calibration & coverage.** Calibrated probabilities + conformal coverage on held-out labels before any "calibrated/selective" claim (H5).
- **G12 — Pre-registration before cohort analysis.** OSF registration time-stamped before any cohort data is analysed (H6/H7) — extends G5.
- **G13 — Coupling claim requires paired data.** No "the coupling works / improves reclassification" claim in any artifact until C3 reports the pre-registered endpoint on real paired data. Partition/arithmetic never stands in for coupling.

---

## 5. Risks & mitigations

| Risk | Likelihood | Mitigation |
|---|---|---|
| Cohort access denied/delayed (Track C). | High | Start C2 day one; ship the methods+variant paper (A/B/D1) independently — it needs no cohorts. Coupling becomes a follow-up. |
| Genome-wide inflation rate << panel (H2). | Medium | Frame honestly (panel enriched); report the true rate; method still prevents every double-count found. |
| Predictor licensing/version drift. | Medium | Pin versions; predictors injectable; AlphaMissense feature-only; re-verify at execution. |
| ClinVar/VCEP disagreement misread as DISCERN error (H3). | Medium | Report as concordance finding, stratified by review status — not ground-truth error. |
| Cluster scope drifts toward unvalidated breadth. | Medium | Hard rule (B1): only the C1–C10 confusable, opposite-management groups; every LR sourced; coverage ≠ accuracy stated in every claim. |
| Over-claiming the platform pre-C3. | Medium | G13; scope audited in D1 against Section A; coupling is "pending"/"negative", never "validated", until paired-data results. |

---

## 6. Sequencing & milestones

```
Month 1     C1 pre-registration locked · C2 DAC + IRB SUBMITTED (rate-limiter starts)
Month 1–2   A1 full-panel genome-wide eRepo + ClinVar + gnomAD           → H1/H2/H3
Month 2–4   A2 wire predictors + strength trees + novel-variant path     → H4
            B1 curate C4 then C3 then C5 (parallel)                       → sourced coverage
Month 4–6   A3 variant calibration · B2 conformal coverage · B3 safety fix + per-cluster map → H5, guarantee, regression
Month 5–8   B1 continue C8/C6/C7/C9 · B4 curated per-cluster benchmark    → H7 (now-half)
Month 6–10  D1 methods+variant paper from locked results
Month N+    C3 coupling + cohort diagnosis + reader study (gated by C2)   → H6/H7 (pre-registered)
On results  D2 release · Zenodo DOI · hosted demo
```

**Milestone gates:** generality/concordance table before any generality claim (G9/G10); calibration+coverage before any calibrated claim (G11); pre-registration before cohort analysis (G12); paired-data result before any coupling claim (G13).

---

## 7. Document control

| Version | Date | Changes |
|---|---|---|
| 2.x | 2026-06-13 | P0–P11 engine; variant-intrinsic layer validated on bleeding-panel eRepo; CSpec frequency criteria for 5 genes. |
| 3.0.0 | 2026-06-13 | Expansion + external-validation arc (genome-wide partition + ClinVar/gnomAD; novel-variant scoring; calibration; conformal; safety fix; cohort coupling track; manuscript split). Gates G9–G13. |
| 3.1.0 | 2026-06-13 | Folded in `DISCERN_Coverage_Architecture_v1.md`: Track A panel = full ISTH TIER1; Track B clusters = cited C1–C10 in harm-ranked order (C4 first); per-cluster safety map + per-cluster case benchmark; added executive positioning (Section A: problems/novelty/beneficiaries/I/O). |

---

*Verification note: re-pull the ISTH TIER1 list and dataset versions (eRepo, ClinVar `variant_summary`, gnomAD v4.1.1, REVEL, Pangolin v1.1, AlphaMissense) at execution; new clusters undergo the same source-verification pass as the VCEP specs. The coupling remains the one claim no public dataset can validate — Track C, on paired cohort data, is the only path, reported regardless of outcome.*

*End of DISCERN Execution Plan v3.1.0*
