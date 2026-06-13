# DISCERN — Real-Data Validation & Benchmarking Plan

**Goal:** replace every placeholder with real, citable data; benchmark DISCERN against the
tools the field uses; produce results publishable in a strong genomic-medicine journal.
**Honest boundary up front:** controlled patient cohorts cannot be downloaded on demand —
**your institution must apply** to each Data Access Committee (DAC). But (a) the entire
**variant-level** validation is **open and downloadable today**, (b) a **standardized open
patient benchmark** exists for the diagnosis claim now, and (c) the **gold-standard
bleeding-disorder cohort** is real and obtainable via application. No synthetic data is used
as a headline result anywhere. **Date:** 2026-06-13

---

> ## Editorial correction (2026-06-13) - supersedes the "no-inflation / G3-as-calibration" framing in this document
>
> Tier A was executed on real open data. Wherever this plan says the VCEP-reconstruction test gives
> "no inflation," "calibration, not just plumbing," or "G3 becomes a calibration result," read this:
>
> - The original "100% no-inflation rate" was a **tautology** (it summed the same points twice and returned 100% for any input) and was **removed**, not reported.
> - **Gate G3 = no double-counting**, verified two ways: (i) the variant-marginal invariance unit test, and (ii) per-code routing on **2,653 real VCEP variants** - 100% partition coverage (0 unknown), owned non-genetic codes in 31.7% of variants, naive all-codes over-classifies 549 (20.7%). G3 is **not** a calibration of the disease->variant coupling; that needs paired-phenotype cohorts (Tier B/C).
> - The reconstruction test is **ACMG combining-rule fidelity**: 93.0% exact / 100% within-one-bin, point-engine arithmetic given the experts' own codes (not code assignment, not coupling).
> - "Kills the placeholders" is now largely DONE (2026-06-13): the per-gene CSpec frequency criteria (BA1/BS1/PM2) + PM2_Supporting strength were extracted and verified for GT/F8/F9/VWF/GP1BA from the CSpec registry (GN071/GN079/GN081) cross-checked with the VCEPs' eRepo records. Residual = the variant-dependent PVS1/PS4 strength trees (documented simplification) + RUNX1 BA1/BS1. See `DISCERN_VCEP_Spec_Verification_Report.md`. (NB: GN079 is the GP1BA spec, not GT.)
>
> Executed results: `DISCERN_Validation_Results.md` and `docs/DISCERN_Execution_Summary.md`.

---

## 1. Access tiers (read this first)

| Tier | Meaning | Timeline | Use |
|---|---|---|---|
| **A — Open** | download/API now, no permission | days–weeks | variant validation, open diagnosis benchmark, head-to-head |
| **B — Application** | DAC / managed access, institutional + IRB + DAA | weeks–months | gold-standard cohort validation |
| **C — Own / collaboration** | your data or a partner's | your control | equity + real-patient centerpiece |

The first paper can stand on **Tier A alone**; Tiers B/C elevate it and should run in parallel.

---

## 2. Variant-level validation — **TIER A, fully open** (do this first; it kills the placeholders)

This is the layer that directly fixes the "per-code strengths are placeholders" gap and turns the reconstruction test into a real partition result on expert data (combining fidelity + no double-counting); calibration of the coupling awaits the cohorts.

> **[Corrected 2026-06-13]** Run on real ERepo: the reconstruction test is **ACMG combining-rule fidelity** (93.0% exact), and the per-code partition gives a real no-double-counting result (100% coverage; over-classifies 549/2,653). It is not a coupling "calibration." The per-gene CSpec *rule* tables in `rules/vcep/specs/*.yaml` were subsequently extracted/verified (frequency criteria + PM2_Supporting for GT/F8/F9/VWF/GP1BA); residual = PVS1/PS4 trees + RUNX1. See the top-of-doc correction.

| Source | What you get | How | DISCERN use |
|---|---|---|---|
| **ClinGen Evidence Repository (ERepo) API** | **FDA-recognized public DB**; VCEP-classified variants **with per-code SEPIO evidence + provenance**, JSON/JSON-LD; ~10,527 variants, 140+ genes, 37+ VCEPs, **versioned** | `erepo.clinicalgenome.org` REST API (search/filter/**download**) | (1) extract **real per-code applied strengths** per variant; (2) run the **reconstruction test on real VCEP variants** (G3 → calibration, not just plumbing); (3) VUS-reclassification truth |
| **ClinGen CSpec Registry** | the VCEP **criteria specifications in machine-readable form** (the calibrated per-code strength rules themselves) | `cspec.genboree.org` (GN079 GT, GN071 F8, GN081 VWF, RUNX1, GP1BA-BSS) | the **actual strength tables** to replace the placeholders in `rules/vcep/` |
| **ClinVar** | classifications + **3-star VCEP submissions** (gold-standard) + dated reclassification history | FTP/`variant_summary` + monthly archives | VUS-reduction benchmark; 3-star = the truth label |
| **EAHAD coag DBs + LOVD** | F8/F9/VWF variants **+ phenotype + functional** | `dbs.eahad.org`, `lovd.nl` | gene-specific variant + phenotype evidence |
| **MaveDB** | saturation **functional** maps (OddsPath-calibrated) | `mavedb.org` API | PS3/BS3 functional ground truth |

**Target genes (your clusters):** ITGA2B, ITGB3 (GT) · F8, F9, F11, F13, FGA/B/G (coag) · VWF (2A/2B/2M) · GP1BA, GP1BB, GP9 (BSS / PT-VWD) · RUNX1, ETV6, ANKRD26 · MYH9 · NBEAL2. Pull each gene's ERepo records + CSpec spec; FERMT3/RASGRP2/granule genes have **no spec** (keep the reduced-confidence tag).

> **Deliverable from Tier A alone:** "DISCERN reconstructs ClinGen VCEP classifications from their own per-code evidence with no inflation, and reclassifies X% of bleeding-gene VUS concordant with 3-star truth." That is a real, citable, publishable methods+validation result — obtainable in weeks, no permissions.

> **[Corrected 2026-06-13]** The achieved Tier-A deliverable is: "DISCERN reproduces ClinGen VCEP bottom-line labels from the experts' own per-code evidence at 93.0% exact / 100% within-one-bin, and partitions every applied code to one owning factor (100% coverage), preventing the double-counting that would over-classify 549 of 2,653 variants." The VUS-reclassification *rate* needs paired phenotype (Tier B/C); the open variant DBs do not supply it standalone. "No inflation" here = the per-code partition, not the deleted tautological metric.

---

## 3. Patient-level diagnosis validation

### 3A — Open standardized benchmark (**TIER A** — use now)
**GA4GH Phenopacket Store** — **5,213 structured real cases across ~378 rare diseases**, each with HPO terms (observed **and excluded**), a diagnosis (OMIM/Mondo), and variant annotations, curated from **600+ published case reports**; public on GitHub (`phenopacket-store`) + Zenodo. Filter for the cluster diseases (Glanzmann, BSS, MYH9, VWD subtypes, HPS, RUNX1, etc.) → a **real, standardized, citable diagnosis benchmark** with no access barrier. *Caveat: published-case selection bias toward cleanly-resolved cases — acknowledge it.*

Supplementary open phenotype-only sets: **RareBench** (1,197 cases aggregating MME/LIRICAL/HMS/RAMEDIS/PUMCH-ADM) and the **LIRICAL corpus** (385 cases).

### 3B — Gold-standard bleeding-disorder cohort (**TIER B** — apply in parallel)
**BRIDGE-BPD / ThromboGenomics** — the field's gold standard: **2,396 deeply-phenotyped, sequenced BPD patients** with molecular diagnoses (Downes et al., *Blood* 2019; 37.3% diagnostic yield), classified into platelet-function / platelet-count / coagulation / thrombotic / unexplained classes that map onto your clusters. Sub-cohorts exist per cluster (e.g., 50 MYH9 patients with phenotype).
- **Raw data:** EGA studies **EGAS00001001172** (BRIDGE-BPD) and **EGAS00001001012** (NIHR BioResource Rare Diseases).
- **Access:** apply to the **NIHR BioResource DAC** — `dac@bioresource.nihr.ac.uk` — with institutional affiliation, IRB approval, a research proposal, and a signed Data Access Agreement. **Start this early; it takes weeks–months.**

### 3C — Misdiagnosis-rescue cohort (**TIER B** — the cluster-3 headline)
**ITP genetic-sequencing cohort** — **80 chronic-ITP patients** sequenced with the ThromboGenomics + immune panels precisely because *"misdiagnosis of primary ITP occurs in patients with inherited thrombocytopenia"* (Blood Adv 2025). This is a **real misdiagnosis-rescue testbed** for the BSS/inherited-thrombocytopenia-mislabelled-as-ITP claim. Same NIHR BioResource access route.

### 3D — Curated published-case benchmark (**TIER A** — real, hand-built)
For the rarest, mechanism-distinct confusers where Phenopacket Store is thin (LAD-III, RASGRP2, PT-VWD), curate per-patient phenotype+variant+confirmed-diagnosis from published series/supplements (MYH9 n=50; GT cohorts; **PT-VWD international registry**, Othman 2020; LAD-III case series). Real cases, no access barrier, but labor-intensive — encode as phenopackets for reuse.

### 3E — Your equity centerpiece (**TIER C**)
The **South Indian Glanzmann clinical-exome cohort** — real, ancestry-relevant, mechanism-distinct (GT vs LAD-III), in-hand. Run under local IRB; aggregate-only; **no patient data in public artifacts**. This is the validation that makes the paper *matter* and is uniquely yours.

---

## 4. Head-to-head benchmarking — the machinery reviewers expect

**Framework: PhEval** (open, GitHub) — the standard harness for phenotype-driven diagnostic tools; benchmarks **Exomiser, LIRICAL, AI-MARRVEL** (and you add **DISCERN** + **DeepRare** where runnable) on the **same cases** with the **same metric (Recall@K, Top-1/Top-3)**.

**Established, reproducible methodology:** take real cases (Phenopacket Store / your cohort) → **spike the causal variant into a Genome-in-a-Bottle template exome VCF** → run each tool with the case's HPO + VCF → compute Recall@K. *(State plainly that spike-in is a standard but artificial detection setting — it benchmarks prioritization/reasoning, not detection.)*

**Current bars to contextualize against:** Exomiser ranks the correct diagnosis first in ~**35.5%** of cases; the best general LLMs ~**23.6%**; DeepRare R@1 ranges **29–73%** depending on benchmark. DISCERN is **specialized to one bounded domain**, so the honest, defensible story is: *a specialist matches/beats generalists in-domain on the high-stakes clusters, and does what none of them do — flag the management-changing misdiagnosis, reclassify the VUS, and name the discriminating test.* Don't claim a universal DDx win; claim a **bounded-domain, safety-first** win.

---

## 5. Claim → dataset → metric crosswalk

| DISCERN claim | Dataset(s) | Metric | Tier |
|---|---|---|---|
| Classifier reproduces experts | ERepo, ClinVar 3-star | exact/within-1-bin concordance, κ | A |
| **No double-counting (G3, calibrated)** | **ERepo per-code variants** | **VCEP reconstruction, no inflation** | **A** |
| VUS reclassification | ClinVar 3-star, ERepo | % VUS reclassified, concordant | A |
| Differential-diagnosis accuracy | Phenopacket Store (bleeding subset), curated cases | Top-1/Top-3, Recall@K vs Exomiser/LIRICAL/AI-MARRVEL | A |
| **Misdiagnosis rescue** | **ITP cohort (3C)**, PT-VWD registry, BRIDGE-BPD | flag precision/recall, rescue rate (label hidden) | B (+A curated) |
| Discriminating-test concordance | curated cases + cohort | top-k test match | A/B/C |
| Equity / real-patient | **Glanzmann cohort** | dx accuracy + ancestry gap | C |
| Calibration / abstention | all labeled sets | reliability, Brier, ECE, confident-wrong rate | A/B |
| Clinical usefulness | **reader study** (vignettes) | accuracy & time, with vs without | own (pre-reg) |

> **[Corrected 2026-06-13]** The "No double-counting (G3, calibrated)" row should read **"No double-counting (G3), VCEP per-code partition"** - the metric is partition coverage + points routed out + inflation prevented on 2,653 real variants, not a "calibrated reconstruction." The "calibrated" qualifier and "no inflation" wording reflect the deleted tautological metric. See the top-of-doc correction.

---

## 6. The honest order of operations

1. **NOW (Tier A, weeks):** pull **ERepo + CSpec** → real per-code strengths into `rules/vcep/` → run `test_vcep_reconstruction.py` on **real VCEP variants** → placeholders gone, G3 becomes a calibration result.
   > **[Corrected 2026-06-13 - done]** ERepo was pulled and the reconstruction ran on 2,653 real variants (93.0% exact fidelity; 100% partition coverage; G3 = no double-counting confirmed). The CSpec machine-readable pull was then completed too: the frequency criteria (BA1/BS1/PM2) + PM2_Supporting strength are extracted/verified for GT/F8/F9/VWF/GP1BA (GN071/GN079/GN081 + eRepo). Residual = PVS1/PS4 variant-dependent trees + RUNX1 BA1/BS1. G3 is no-double-counting, not a coupling calibration. See the top-of-doc correction and `DISCERN_VCEP_Spec_Verification_Report.md`.
2. **NOW (Tier A, weeks):** **VUS-reclassification** vs ClinVar 3-star.
3. **NOW (Tier A, weeks):** **Phenopacket Store** bleeding subset + curated cases → **PhEval head-to-head** vs Exomiser/LIRICAL/AI-MARRVEL.
4. **PARALLEL (Tier B, start immediately — long lead):** NIHR BioResource DAC application for **BRIDGE-BPD (EGAS00001001172)** + the **ITP cohort**.
5. **PARALLEL (Tier C, IRB):** the **Glanzmann cohort** run.
6. **PARALLEL:** **pre-register** the whole protocol + the **reader study** on OSF *before* analysis.
7. **Write up** when 1–3 (+ at least one of 4/5) land. Steps 1–3 + reader study are already a complete paper; the cohort elevates it or becomes Paper 2.

---

## 7. What NOT to do (so the results survive review)

- **No synthetic/fabricated data as a result.** Keep synthetic only for unit tests and clearly-labelled illustration — never in a results table.
- Don't present spike-in prioritization as real-world *detection* performance — state the setting.
- Don't over-claim from Phenopacket Store alone (published-case selection bias) — triangulate with the cohort.
- Don't gate the first paper on Tier B — the DAC timeline is outside your control.
- Don't claim a general-DDx win — claim the bounded-domain, safety-first, VUS-coupled win that is actually yours.

---

## 8. Publication framing

The package — **(A)** VCEP-anchored, reconstruction-validated variant scoring + VUS reclassification on open expert data, **(B)** a standardized differential-diagnosis benchmark **against the field's tools** on real published cases, **(C)** a misdiagnosis-rescue result on a real ITP cohort, **(D)** an equity result on a real under-represented cohort, **(E)** calibration/abstention safety, and **(F)** a reader study — is novel, rigorous, honest, and clinically pointed. Targets: **npj Genomic Medicine** (primary), **Genome Medicine** / **Genetics in Medicine** (secondary). The bounded-domain + safety + equity + LMIC framing is the impact multiplier.

---

### One-paragraph summary
Everything DISCERN needs to stop being a demo is reachable: the variant layer (per-code strengths, the reconstruction test, VUS reclassification) runs **now** on the open, FDA-recognized **ClinGen ERepo/CSpec** and **ClinVar**; the diagnosis layer benchmarks **now** against Exomiser/LIRICAL/AI-MARRVEL via the open **GA4GH Phenopacket Store** + **PhEval**; the **gold-standard BRIDGE-BPD cohort** (2,396 patients, EGA) and a real **ITP misdiagnosis cohort** are obtainable by DAC application started in parallel; and your **South Indian Glanzmann cohort** carries the equity claim. Real data throughout, honestly tiered by access, sequenced so the first publishable paper depends only on what is open today.
