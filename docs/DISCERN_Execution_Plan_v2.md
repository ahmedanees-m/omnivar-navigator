# DISCERN — Full Execution Plan (v2)

**Project:** DISCERN — coupled differential-diagnosis, misdiagnosis-prevention & VUS-resolution engine for overlapping inherited bleeding & platelet disorders.
**Companion to:** *DISCERN — Concept Brief (v2).* **Builds on:** OmniVar Navigator (reused, not rebuilt).
**v1 → v2 (after external review):** re-architected around a **joint disease × variant model**; variant scoring **anchored to ClinGen VCEP rules** with **measured VUS-reclassification**; **evidence circularity handled explicitly** (factor graph, each evidence once, PP4 via disease→variant coupling); **management-aware** misdiagnosis flag; **calibrated abstention** with sparse-LR uncertainty propagation; **partial-input + cheapest-next-observation** usefulness core; **free-text→HPO** front end; **scientist-facing VUS-triage**; **living provenance-tagged** knowledge base; **reader-study-first** validation.
**v2 → v2.1 (precision fix):** the circularity fix is pushed to the **per-ACMG-code** level — DISCERN **decomposes each VCEP spec to its calibrated per-code strengths and routes each code to the one factor that owns it** (never consuming the VCEP's bottom-line label, which bundles PS3/PP4/PM3/PP1 and would re-introduce double-counting through the anchor we trust most). Gate G3 becomes "each **code** enters once," with a VCEP-reconstruction unit test. Plus: stated **VCEP coverage asymmetry** (the index disease is usually covered; its highest-stakes confuser usually is not).
**Step template:** Objective · Goal/acceptance · Sources · Methods · Code/artifacts · Expected outcome · Depends on. Math in Appendix A. **Date:** 2026-06-12

---

> ## Editorial correction (2026-06-13) - supersedes the "no-inflation / G3-as-calibration" framing in this document
>
> The Tier-A real-data run replaced one metric and reframed another. Wherever this plan says the
> VCEP-reconstruction test yields "no inflation" or "a calibration result," read the corrected version:
>
> - The original "100% no-inflation rate" was a **tautology** (it summed the same points twice and returned 100% for any input). It has been **removed**, not reported.
> - **Gate G3 = no double-counting**, verified two ways: (i) a unit test that the variant marginal is invariant to bundled PP4/PS3/PP1/PM3 codes, and (ii) per-code routing on **2,653 real VCEP variants** - 100% partition coverage (0 unknown), owned non-genetic codes in 31.7% of variants, and a naive all-codes score would over-classify 549 (20.7%). G3 is **not** a calibration of the disease->variant coupling; that awaits paired-phenotype cohorts (Tier B/C).
> - The reconstruction test is **ACMG combining-rule fidelity** (93.0% exact / 100% within-one-bin) - point-engine arithmetic given the experts' own codes; it does not test code assignment and does not test the coupling.
> - "Placeholders gone" is now largely DONE (2026-06-13): the per-gene CSpec frequency criteria (BA1/BS1/PM2) + PM2_Supporting strength were extracted and verified for GT/F8/F9/VWF/GP1BA from the CSpec registry (GN071/GN079/GN081) cross-checked with the VCEPs' eRepo records. Residual = the variant-dependent PVS1/PS4 strength trees (documented simplification) + RUNX1 BA1/BS1. See `DISCERN_VCEP_Spec_Verification_Report.md`. (NB: GN079 is the GP1BA spec, not GT.)
>
> Executed results: `DISCERN_Validation_Results.md` and `docs/DISCERN_Execution_Summary.md`.

---

## 1. Source Registry

### 1.1 NEW & primary — ClinGen gene-specific VCEP rules (the anchor)
| VCEP / source | Genes / status | Role |
|---|---|---|
| **ClinGen Platelet Disorder VCEP** (Ross et al., Blood Adv 2021; specs v2.1) | **ITGA2B/ITGB3 published** (cut VUS 29%→20% on 70 pilot variants); **Bernard-Soulier in progress** (GP9, GP1BA, GP1BB) | GT/BSS variant rules **adopted verbatim** |
| **ClinGen Coagulation Factor Deficiency VCEP** | **F8, F9** classifications in ClinVar at **3-star, FDA-recognized** | coag-factor rules **+ gold-standard validation set** |
| **ClinGen Myeloid Malignancy VCEP** (Luo et al., Blood Adv 2019) | **germline RUNX1** | thrombocytopenia-leukaemia cluster rules |
| ClinGen VWF / RASopathy VCEPs, CSpec registry | VWF; (RASGRP2 context) | rules where available |
| **Boundary policy** | FERMT3/LAD-III, RASGRP2, granule genes: **no spec** | tag classifications *"no gene-specific specification — reduced confidence"* |

**Coverage asymmetry (state plainly — do not let tables imply uniform coverage).** VCEP rigor is distributed unevenly *inside* clusters: the **index disease is usually covered and its highest-stakes confuser usually is not**. Cluster 2 — VWD VCEP covers 2A/2B/2M (VWF), but **PT-VWD = GP1BA sits in the in-progress Platelet Disorder panel** (uncovered). Cluster 1 — **GT (ITGA2B/ITGB3) covered; LAD-III (FERMT3)/RASGRP2 not.** So anchored variant-scoring is strongest where it matters least (the disease one would likely get right) and absent where it matters most (the look-alike). This is survivable — discrimination at that boundary leans on **phenotype/functional features** (leukocytosis, αIIbβ3 activation, RIPA origin), which are the real-world discriminators anyway — but it is stated, not hidden.

### 1.2 Carried from OmniVar (evidence engine)
gnomAD v4.1 (PM2/BS1/BA1) · ClinVar (PS1/PM5; **3-star = validation truth**) · ClinGen eRepo + CSpec · HPO + `phenotype.hpoa` (LRs, **pertinent negatives**) · AlphaMissense + dbNSFP/REVEL (PP3/BP4, Pejaver-calibrated) · MaveDB (PS3/BS3) · Pangolin-from-source (splice) · autoPVS1 · AutoPM3 · Exomiser/AI-MARRVEL. *(Honor OmniVar verification corrections C1–C6.)*

### 1.3 Disease & validation sources
ISTH Tier-1 list (Megy 2019) · ISTH SSC diagnostic guidance + expert reviews (discrimination features/tests) · Orphanet/OMIM (disease defs, prevalence priors) · EAHAD `dbs.eahad.org` + LOVD · published confirmed & **documented-mislabelled** case series (e.g., PT-VWD registry) · **South Indian Glanzmann clinical-exome cohort** · Solve-RD/UDN (managed, off critical path).

---

## 2. Software environment & repository

Reuse OmniVar's stack (Python 3.11 pinned, Docker-only on the VM, cloud Nemotron LLM, paramiko/SFTP, key-auth). New modules in **bold**.

```
discern/
├── core/                  # schemas (extended), adapter ABC, hash-chained audit      [reuse+extend]
├── rules/                 # ACMG point engine, posterior, ** VCEP spec loader **      [reuse+extend]
│   └── vcep/              #   ** PD-VCEP (ITGA2B/ITGB3), CFD-VCEP (F8/F9), RUNX1, ... as machine-readable specs **
├── adapters/              # gnomAD, ClinVar, insilico, splice, autoPVS1, MAVE, phenotype, prioritizer [reuse]
├── evidence/              # ** evidence streams (genetic-via-VCEP, phenotype LRs + negatives, lab) **
├── diseases/              # ** disease ontology + discrimination clusters (provenance-tagged KB) **
│   └── clusters/          #   integrin · vwf_gpib · macrothrombocytopenia · granule · thr_leukemia · coag_factor
├── jointdx/               # ** THE NOVEL CORE: coupled disease × variant inference **
│   ├── factorgraph.py     #   joint P(D,V | E); each evidence once; PP4 = disease→variant coupling
│   ├── infer.py           #   exact enumeration + marginals P(D|E), P(V|E)
│   ├── uncertainty.py     #   sparse-LR uncertainty propagation → credible intervals
│   └── abstain.py         #   calibrated decide/abstain policy
├── safety/                # ** management-aware misdiagnosis / treatment-safety interlock **
├── nextobs/               # ** cheapest decisive next observation (info gain over joint; segregation/phasing) **
├── triage/                # ** scientist-facing: which VUS to assay next (cohort-level info gain) **
├── intake/                # ** free-text → HPO extractor (LLM soft task) + pertinent-negative capture **
├── equity/  learn/        # reliability/routing/ancestry [reuse]; auditable prior updates [reuse pattern]
├── sim/  eval/            # ** simulator; reader-study harness, VUS-reclass, misdx-rescue, calibration **
├── llm/ api/ ui/ deploy/ docker/ data/ figures/ manuscript/ tests/                    [reuse]
```

---

## 3. Core data model (`core/schemas.py`, extended)

```python
from dataclasses import dataclass, field
from enum import Enum

class VariantState(Enum): PATH="pathogenic"; LP="likely_path"; VUS="vus"; LB="likely_benign"; BEN="benign"
class FeatureKind(Enum): CLINICAL="clinical"; LAB="lab"; FUNCTIONAL="functional"; GENETIC="genetic"

@dataclass
class Feature: id:str; kind:FeatureKind; value:object; observed:bool=True; source:str=""   # observed=False ⇒ pertinent negative

@dataclass
class Disease:
    id:str; name:str; genes:list[str]; inheritance:str; mechanism:str
    prior:float                                  # prevalence
    feature_lr: dict                             # feature_id -> (LR, n_cases, pmid)  ← uncertainty + provenance
    p_path_given_disease: float                  # P(variant pathogenic | this is the disease)  ← the PP4 coupling
    treatment: str; contraindications: list      # for the safety interlock
    vcep_spec: str|None                          # rules/vcep/... or None (→ reduced-confidence tag)

@dataclass
class DiscriminationCluster:
    id:str; name:str; diseases:list[Disease]
    discriminating_features:list[str]; next_observations:list["Observation"]

@dataclass
class Observation:                               # a candidate next step (test OR segregation OR phasing OR functional)
    id:str; name:str; kind:str                   # "lab"|"functional"|"segregation"|"phasing"
    informs:list[str]                            # feature ids and/or "V" (variant) and/or "D" (disease)
    outcome_lr: dict                             # outcome -> {disease_id|"V": LR}
    changes_management:bool; accessibility:str   # high|moderate|low  (NO currency)

@dataclass
class JointPosterior:
    cluster:DiscriminationCluster
    p_disease: dict                              # disease_id -> (prob, lo, hi)   credible interval
    p_variant: dict                              # variant_id -> {VariantState: prob}
    leading: str; confidence: float; decided: bool   # abstain if not decided

@dataclass
class SafetyFlag:
    leading_id:str; competitor_id:str
    management_divergence:str                     # what changes (e.g., "DDAVP contraindicated if 2B")
    p_competitor:float; severity:str; resolving_observation:"Observation"; message:str

@dataclass
class Recommendation:                             # the engine's output
    posterior: JointPosterior
    reclassified_variants: dict                   # variant_id -> (old_state, new_state, drivers)
    safety_flags: list[SafetyFlag]
    next_observation: Observation|None            # cheapest decisive step (with predicted joint shift)
    explanation: str; audit: dict
```

---

## PART II — PHASES

### Phase 0 — Foundations + VCEP loaders (Months 1–2) — *reuse + extend*
- **Objective/Goal:** DISCERN repo on the reused OmniVar foundation; CI green; **VCEP specs machine-readable**.
- **Methods:** port `core/rules/adapters/equity/llm/deploy/docker`; add `rules/vcep/` loader; encode PD-VCEP (ITGA2B/ITGB3) and CFD-VCEP (F8/F9) rules as versioned specs; extend schemas + audit.
- **Code:** `rules/vcep/loader.py`, `rules/vcep/specs/{ITGA2B_ITGB3, F8, F9, RUNX1}.yaml`; `core/schemas.py` (extended).
- **Expected:** OmniVar genetic stack runs inside DISCERN; G1 reproducible; VCEP rules selectable per gene.

---

### Phase 1 — Evidence streams (Months 2–4)

**1.1 Genetic evidence — VCEP specs decomposed to per-code strengths, partitioned by owning factor**
- **Objective/Goal:** use the gene's VCEP spec where it exists (else generic ACMG **+ reduced-confidence tag**) — but **never run the spec to a bottom-line classification and consume that label.** A VCEP verdict bundles PS3, PP4, PM3, PP1 etc. (e.g., a real VWD VCEP call: `PS3, PM5_supporting, PP3, PP4, BP5, BS1`), which are precisely the codes DISCERN separates into other factors; consuming the label double-counts them.
- **Methods — the per-code partition (the deep circularity fix).** Decompose the VCEP spec into its calibrated per-code strengths and route **each code to exactly one factor** (VCEPs already organize into sub-teams of this exact shape — computational/functional/splicing vs. segregation/allelic/de-novo — so the partition is given):

  | ACMG codes | Owning factor | Where they enter |
  |---|---|---|
  | PM2/BS1/BA1, PP3/BP4, PVS1, PM5/PS1, PM4/BP3, BP7 | **variant-intrinsic** | `P(E_geno\|V)` (this step) |
  | **PP4** | disease specificity | the `P(V\|D)` **coupling** (Phase 3) — not added here |
  | **PS3 / BS3** | functional | the functional factor `P(E_func\|D,V)` (Phase 3) |
  | **PP1 / BS4** | segregation | a **next-observation** (Phase 6); its code enters only if/when performed |
  | **PM3 / BP2** | phasing/in-trans | a **next-observation** (Phase 6); enters only if/when performed |
  | **PS2 / PM6** | de novo | a de-novo factor (enters once) |

  This step emits a likelihood over `VariantState` using **only the variant-intrinsic codes**; everything else is owned elsewhere, so each code enters the joint model exactly once.
- **Code:** `evidence/genetic.py::variant_intrinsic_likelihood(variant, ledger, spec) -> dict[VariantState,float]`; `rules/vcep/partition.py` (code→factor map per spec).
- **Acceptance test (also a calibration check):** feed DISCERN the *same* evidence the VCEP had and confirm the joint model **reconstructs the VCEP's classification with no inflation** — `tests/test_vcep_reconstruction.py`.
  > **[Corrected 2026-06-13]** This is ACMG combining-rule fidelity (point-engine arithmetic, 93.0% exact on real ERepo), not a coupling "calibration." The no-inflation guarantee is the per-code partition (no double-counting), verified by the invariance unit test plus per-code routing on 2,653 real variants - not the tautological "100% no-inflation rate," which was removed. See the top-of-doc correction.
- **Expected:** calibrated, VCEP-anchored genetic likelihood from variant-intrinsic codes only; provenance + confidence tag; no code double-counted downstream.

**1.2 Phenotype likelihood ratios with pertinent negatives**
- **Objective/Goal:** HPO terms → per-disease LR, including **absent** terms as evidence.
- **Sources:** `phenotype.hpoa`, HPO DAG.
- **Methods:** LR(term|disease)=freq(term|disease)/freq(term|bg), DAG-propagated; **explicit negative terms** (observed=False) contribute (1−freq)-based LRs (LIRICAL-style). Each LR carries `(value, n_cases, pmid)`.
- **Code:** `evidence/phenotype_lr.py`.
- **Expected:** signed phenotype LRs (present + absent), with uncertainty + provenance.

**1.3 Lab/functional ingestion**
- **Objective/Goal:** normalize flow %, RIPA pattern, aggregometry, multimers, factor activity, smear features → `Feature`s with per-disease and per-variant LRs.
- **Methods:** map quantitative readouts to likelihoods under (disease, variant) jointly (a functional result is one factor touching both — see 3.1).
- **Code:** `evidence/lab.py`.
- **Expected:** lab/functional evidence ready for the joint factor.

---

### Phase 2 — Discrimination-cluster knowledge base (Months 3–6) — *provenance-tagged living KB*

**2.1 Disease ontology + 2.2 cluster curation**
- **Objective/Goal:** the six clusters as discrimination matrices with **every LR/discriminator linked to a PMID + strength + sample size**, plus `p_path_given_disease`, treatments, contraindications.
- **Sources:** ISTH SSC guidance, expert reviews, disease literature; VCEP docs.
- **Methods:** build `diseases/clusters/*.yaml`; record provenance per cell; set `n_cases` per LR (drives uncertainty, Phase 6); define `Observation`s incl. **segregation & phasing** generically.
- **Code:** `diseases/ontology.py`, `diseases/clusters/{integrin,vwf_gpib,macrothrombocytopenia,granule,thr_leukemia,coag_factor}.yaml`.
- **Expected:** six cited, versioned clusters; a KB that can be released/maintained as a standalone resource (ISTH/VCEP partnership target).

**2.3 Cluster routing**
- **Code:** `diseases/ontology.py::route_clusters(patient)`; gene→cluster + phenotype-signature→cluster; multi-cluster allowed.

---

### Phase 3 — The coupled disease × variant model (Months 5–8) — *THE NOVEL CORE*

**3.1 Joint factor graph (each evidence once; circularity handled)**
- **Objective:** one joint posterior `P(D, V | E)` where phenotype/functional evidence is **not** double-counted.
- **Goal:** marginals `P(D|E)` and `P(V|E)`; phenotype's effect on V flows **only** through the disease→variant coupling.
- **Methods (Appendix A.1):** `P(D,V|E) ∝ P(E_pheno|D)·P(E_geno|V)·P(E_func|D,V)·P(V|D)·P(D)`. Phenotype enters once (→D); functional enters once (→D,V); **`P(V|D)` is the calibrated PP4** (a pathogenic variant is more likely given the matching disease), replacing the additive PP4 code. The cluster is small → **exact enumeration** over D×V.
- **Code:** `jointdx/factorgraph.py`, `jointdx/infer.py`:
  ```python
  import numpy as np
  def joint(cluster, variant_states, ev):
      tbl={}
      for d in cluster.diseases:
          lp_ph = pheno_loglik(ev.phenotype, d)            # P(E_pheno|D) — ONCE
          for v in variant_states:
              lp_ge = geno_loglik(ev.genetic, v, d.vcep_spec)   # P(E_geno|V) via VCEP — NO PP4 here
              lp_fn = func_loglik(ev.functional, d, v)          # P(E_func|D,V) — ONCE, touches both
              lp_pr = np.log(p_path_given_disease(v,d)) + np.log(d.prior)   # P(V|D)·P(D) = coupled PP4
              tbl[(d.id,v)] = lp_ph+lp_ge+lp_fn+lp_pr
      return normalize(tbl)            # → joint; sum out V for P(D|E), sum out D for P(V|E)
  ```
- **Expected:** a coherent joint posterior; the variant's class correctly shifts with phenotype **without** double-counting — the answer to the circularity critique.

**3.2 VUS reclassification as a first-class, measured output**
- **Objective/Goal:** report, per variant, old→new `VariantState` with the drivers, and the **headline metric**: % input VUS reclassified, **concordant with VCEP/ClinVar 3-star**.
- **Code:** `jointdx/infer.py::reclassify(...)`; `eval/vus_reclass.py`.
- **Expected:** a falsifiable VUS-mitigation number (the v2 thesis), not a slogan.

---

### Phase 4 — Calibrated abstention & uncertainty (Months 7–9) — *safety*

**4.1 Sparse-LR uncertainty propagation**
- **Objective/Goal:** turn each LR's `n_cases` into posterior **credible intervals**; wide → abstain.
- **Methods (A.4):** treat each disease-feature frequency as Beta/Dirichlet with pseudo-counts from `n_cases`; Monte-Carlo (or hierarchical-shrinkage, the rigorous form) propagate to `P(D|E)` interval. (v1: wide intervals + abstention; v2: shrinkage.)
- **Code:** `jointdx/uncertainty.py`.

**4.2 Decide / abstain policy**
- **Objective/Goal:** return a call **only** when justified; else "undecidable — here is the deciding observation."
- **Methods:** abstain if `max P(D|E) < τ`, OR credible interval too wide, OR a **management-divergent** competitor isn't excluded (link to Phase 5). Headline safety metric = **confident-and-wrong rate**.
- **Code:** `jointdx/abstain.py`.
- **Expected:** the tool stays silent exactly when sparse data can't support a call — directly answering the calibration risk.

---

### Phase 5 — Management-aware misdiagnosis / treatment-safety interlock (Months 8–10) — *narrative-load-bearing*
- **Objective:** flag on **treatment danger**, not posterior gap.
- **Goal:** for leader `d*`, each competitor `d'`: fire if `P(d'|E) > 0` **and** management(`d*`)≠management(`d'`) **and** confusing them is harmful — even at small `P(d')` — attaching the resolving observation. Suppress when management is identical.
- **Methods (A.3):** `fire if  p(d') · 1[treatment_changes(d*,d')] · severity(d*,d') ≥ τ_mgmt`. Hard-stop interlocks on planned-treatment contraindications.
- **Code:** `safety/interlock.py`:
  ```python
  def flags(post, cluster, planned_tx=None, tau=0.05):
      out=[]; d_star=post.leading
      for d in cluster.diseases:
          if d.id==d_star: continue
          p=post.p_disease[d.id][0]
          if treatment_changes(d_star,d) and p*severity(d_star,d)>=tau:
              out.append(SafetyFlag(d_star,d.id,_divergence(d_star,d),p,_sev(d_star,d),
                                    _resolving_obs(cluster,d_star,d),_msg(d_star,d)))
          if planned_tx and planned_tx in d.contraindications and p>0:   # interlock
              out.append(_hard_stop(planned_tx,d,cluster))
      return out
  ```
- **Expected:** the flagship hard stops fire — DDAVP+2B/PT-VWD, splenectomy+BSS, HSCT+LAD-III; flag precision/recall measured (Phase 9).

---

### Phase 6 — Cheapest decisive next observation (Months 9–11) — *usefulness-load-bearing*
- **Objective:** recommend the single observation that most reduces **joint** uncertainty — including the cheap, ignored ones.
- **Goal:** rank `Observation`s (lab/functional **+ segregation + phasing**) by EIG over `P(D,V|E)`, weighted by `changes_management`, then accessibility (no currency); show the predicted shift.
- **Methods (A.2):** `EIG(o)=H(D,V|E) − Σ_outcome P(outcome|E)·H(D,V|E,outcome)`. One calculation values disease-resolving and variant-upgrading steps together (e.g., father-segregation upgrades V *and* sharpens D).
- **Code:** `nextobs/recommend.py`:
  ```python
  def recommend(post, cluster):
      scored=[(o, eig_joint(post,o), o.changes_management, o.accessibility)
              for o in cluster.next_observations]
      return sorted(scored, key=lambda x:(x[2], x[1]), reverse=True)  # management, then info
  ```
- **Expected:** outputs like *"father-segregation (cheap, local): variant VUS→LP, diagnosis 60%→92% GT"*; beats a "most-common-test" baseline.

**6b Partial-input mode (same phase):** run on any subset of {genetics, phenotype, labs}; quantify each missing piece's expected contribution. **Code:** `nextobs/partial.py`. **Expected:** maximal usefulness exactly when data is incomplete (the equity case).

**6c Interactive what-if:** show ranking shift *before* ordering ("RIPA platelet-origin→PT-VWD 95%; plasma-origin→2B 90%"). **Code:** `nextobs/whatif.py`.

---

### Phase 7 — Equity & access (Months 10–11) — *reuse + extend*
- **Objective/Goal:** ancestry-aware reliability (reuse) + the partial-input/next-observation core as the access mechanism (Phase 6).
- **Methods:** reuse `equity/reliability.py`+`routing.py` (down-weight PM2/PP3 for sparse ancestry); accessibility-aware `recommend` returns the most decisive **available** observation.
- **Expected:** narrower ancestry gap; decisive guidance under partial data.

---

### Phase 8 — Intake (free-text→HPO), integration, UI, audit, learning (Months 9–13)

**8.1 Free-text→HPO extractor with pertinent-negative capture**
- **Objective/Goal:** turn clinical narrative into HPO terms (present **and explicitly excluded**), with human confirmation. (The legitimate LLM soft task.)
- **Code:** `intake/extract.py` (Qwen via gateway) + confirmation UI.
- **Expected:** robust phenotype input from real notes; negatives captured.

**8.2 Orchestration + explanation + 8.3 UI + 8.4 learning**
- **Methods:** `diagnose(patient)` → route → streams → joint → abstain → flags → next-obs → assemble; LLM **only phrases**. UI shows per-disease evidence (for/against/missing/**excluded**), the joint posterior with credible intervals, the safety flag, the what-if, the next observation; accept/override; hash-chained audit. Learning updates **feature/observation LRs** (with `n_cases`), attributable; verdict logic + matrices never opaquely retrained.
- **Code:** `jointdx/explain.py`, `api/main.py` (`/diagnose`,`/evidence`,`/whatif`,`/nextobs`), `ui/`, `learn/*`.
- **Expected:** one auditable call returns diagnosis + reclassification + safety flag + next observation.

---

### Phase 9 — Validation (Months 11–16) — *reader-study-first*

**9.1 Reader study (the headline "does it help")**
- **Objective/Goal:** do **non-specialists** diagnose more accurately and faster **with** DISCERN vs without, on standardized vignettes?
- **Method:** pre-registered, randomized vignette study (crossover or parallel); outcomes = diagnostic accuracy, time, correct next-test choice, harmful-management avoidance.
- **Code:** `eval/reader_study.py` (vignette bank + scoring).
- **Expected:** the operational proof of clinical usefulness — achievable now, no managed-access needed.

**9.2 VUS-reclassification accuracy**
- **Goal:** % input VUS reclassified, **concordant with VCEP/ClinVar 3-star**; vs InterVar/Varsome (which can't use a disease model).
- **Calibration prerequisite (the cleanest joint-model check):** on the VCEP's own published variants, feeding DISCERN the *same* evidence must reconstruct the VCEP classification **with no inflation** (`tests/test_vcep_reconstruction.py`). Passing this is the precondition for trusting any reclassification claim — it proves the per-code partition prevents double-counting.
  > **[Corrected 2026-06-13]** Done on real data: 93.0% exact ACMG combining-rule fidelity and a 100%-coverage per-code partition (over-classifies 549/2,653 under a naive all-codes score). This proves no double-counting (the stated purpose) but is arithmetic fidelity, not a calibration of the disease->variant coupling, which still awaits cohorts. See the top-of-doc correction.
- **Code:** `eval/vus_reclass.py`.

**9.3 Management-aware misdiagnosis-rescue (honest case-control)**
- **Goal:** on documented **mislabelled** cases (e.g., "2B"→PT-VWD; "ITP"→BSS), does DISCERN flag the danger from **pre-correction** evidence? No leakage (corrected label hidden). **Pre-registered case-control; reported as small/not powered.**
- **Code:** `eval/misdx_rescue.py`.

**9.4 Calibration & abstention** — reliability diagram, Brier, ECE, **confident-and-wrong rate**; coverage of credible intervals. `eval/calibration.py`.

**9.5 Silent/shadow prospective** — run alongside real workup; compare to adjudicated final diagnosis. (As access allows.)

**9.6 Glanzmann cohort** — real, ancestry-relevant, mechanism-distinct (GT vs LAD-III); equity behavior; ethics/IRB; **no patient data in public artifacts**. `eval/cohort_glanzmann.py`.

**Stats:** bootstrap CIs; McNemar (paired accuracy/flag); reader-study mixed-effects; Bonferroni; honest power reporting.

---

### Phase 10 — Scientist-facing VUS-triage + domain expansion (Months 14–16)
- **10.1 VUS-triage for labs:** of all VUS in a cohort, which — if functionally assayed — resolve the **most** diagnoses (highest expected information gain toward resolution)? Turns DISCERN into a **wet-lab prioritization engine**. Note: most Tier-1 genes lack DMS (not growth-selectable), so per-patient functional tests carry the load → prioritizing *which to assay* is genuinely valuable. **Code:** `triage/assay_priority.py`.
- **10.2 Domain expansion:** new clusters via YAML only, **no core changes** (the generalization claim).

---

### Phase 11 — Manuscript, release, hosting, sustainability (Months 14–18)
- **Methods:** pre-register (OSF) before validation; TRIPOD+AI/DECIDE-AI; CI→GHCR images; GitHub→Zenodo DOI; web app on the VM (api/ui/intake/llm-gateway/Caddy; cloud Nemotron); **public demo on synthetic + published-case data only**, real cohort behind auth, no PHI in logs. **Release the discrimination KB as a versioned, citable resource; pursue ISTH SSC / ClinGen VCEP partnership** (the maintenance answer).
- **Targets:** npj Genomic Medicine / Genome Medicine / Genetics in Medicine.
- **Figures:** (1) reader-study accuracy/time with-vs-without; (2) VUS-reclass vs baselines (concordant with 3-star); (3) management-aware misdiagnosis-rescue; (4) GT/LAD-III mechanism case; (5) calibration + confident-wrong rate; (6) equity/partial-input next-observation; (7) joint-model schematic (circularity handling).
- **Expected:** submission + preprint + reproducible release + hosted demo + standalone KB.

---

## Roadmap & gates

```
Month:        1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18
P0 Foundations+VCEP [==]
P1 Evidence streams   [=====]
P2 Cluster KB            [=======]
P3 Joint model (core)        [=======]
P4 Abstention/uncertainty       [=====]
P5 Mgmt-aware flag                 [=====]
P6 Next observation+partial          [=====]
P7 Equity                              [===]
P8 Intake/UI/learn                       [======]
P9 Validation (reader-first)               [=======]
P10 VUS-triage/expansion                       [=====]
P11 Manuscript/release/host/KB                    [=======]
```

**Gates:** (G1) reused engine reproduces eRepo before it feeds dx; (G2) **variant scoring uses the VCEP spec where one exists; else tagged reduced-confidence**; (G3) **circularity audit — each ACMG *code* verifiably enters the joint model exactly once** (the VCEP spec is decomposed per-code and partitioned by owning factor; its bottom-line label is never consumed), **verified by the VCEP-reconstruction unit test** (`tests/test_vcep_reconstruction.py`: same evidence in → VCEP classification out, no inflation); (G4) **abstention validated — confident-and-wrong rate reported** before any usefulness claim; (G5) **reader study + all validation pre-registered**; (G6) misdiagnosis-rescue evaluated with corrected label hidden; (G7) no patient data in public/hosted artifacts; (G8) Docker-only, secrets via env.

---

## Appendix A — Methods (the math)

### A.1 Coupled disease × variant model (circularity-safe)
Latent: disease `D∈cluster`, variant state `V`. Evidence `E={pheno, geno, func}`.
`P(D,V|E) ∝ P(E_pheno|D) · P(E_geno|V) · P(E_func|D,V) · P(V|D) · P(D)`.
Each **ACMG code** enters **once**, partitioned by owning factor (§Phase 1.1): variant-intrinsic codes (PM2/BS1/BA1, PP3/BP4, PVS1, PM5/PS1, PM4) → `P(E_geno|V)`; **PP4** → `P(V|D)`; **PS3/BS3** → `P(E_func|D,V)`; **PP1/PM3/PS2** → segregation/phasing/de-novo factors that enter only when those observations are performed. Critically, DISCERN **does not consume the VCEP's bundled bottom-line label** — it decomposes the spec to per-code strengths, so phenotype (PP4), functional (PS3), and segregation/phasing (PP1/PM3) are never counted in both the genetic factor and their own. **`P(V|D)` is the calibrated PP4** — the disease-conditioned pathogenicity prior — so phenotype's pull on `V` flows through `D` and is never double-counted. Marginalize for `P(D|E)=Σ_V` and `P(V|E)=Σ_D`. Cluster is small ⇒ exact enumeration. *Verification: feeding the model the VCEP's own evidence must reconstruct the VCEP classification (no inflation).*

### A.2 Expected information gain over the joint posterior (next observation)
`H(D,V|E)=−Σ_{d,v} P(d,v|E) log P(d,v|E)`. For observation `o` with `P(outcome|d,v)`:
`EIG(o)=H(D,V|E) − Σ_o P(o|E) H(D,V|E,o)`. One score values disease-resolving and variant-upgrading observations together (segregation/phasing/functional). Rank by (`changes_management`, then `EIG`); accessibility breaks ties; **no currency in the primary ranking.**

### A.3 Management-aware flag
Leader `d*`. Competitor `d'` fires iff `P(d'|E)·1[treat(d*)≠treat(d')]·severity(d*,d') ≥ τ_mgmt` — small probability + dangerous divergence fires; large probability + same management does not. Planned-treatment **interlock**: if `planned_tx ∈ contraindications(d')` and `P(d'|E)>0` → hard stop + resolving observation.

### A.4 Sparse-LR uncertainty & abstention
Each disease-feature frequency ~ Beta(`a+k`, `b+n−k`) with `n=n_cases` (Dirichlet for multi-category); propagate (MC or hierarchical shrinkage) to a **credible interval** on `P(D|E)`. **Abstain** if `max P(D|E)<τ`, interval too wide, or a management-divergent competitor unexcluded. Headline safety metric: **confident-and-wrong rate**; report interval coverage.

### A.5 Carried ACMG/VCEP math
VCEP-specified strengths per gene; otherwise Tavtigian `OddsPath=350^(points/8)`, prior 0.10, bands P≥10/LP6–9/VUS0–5/LB−1..−6/B≤−7; predictor calibration (Pejaver 2022); functional OddsPath (Brnich 2020). The variant likelihood over `VariantState` feeds A.1.

### A.6 Validation statistics
Bootstrap CIs; McNemar (paired); reader-study mixed-effects (reader random effect); reliability/Brier/ECE; Bonferroni; honest N reporting (mislabelled-case scarcity).

---

## Appendix B — What changed (v1→v2) and what's reused
**New in v2:** VCEP-anchored genetic scoring + measured VUS-reclassification; the **coupled joint model with explicit circularity handling**; **calibrated abstention** + sparse-LR uncertainty; **management-aware** flag; **partial-input + cheapest-next-observation** core (incl. segregation/phasing) with what-if; **free-text→HPO** intake with pertinent negatives; **scientist-facing VUS-triage**; **provenance-tagged living KB**; **reader-study-first** validation.
**Reused from OmniVar (unchanged):** rule engine, adapters, equity layer, LLM gateway, audit, Docker/VM/Nemotron infra, release machinery. **Net:** ≈70% foundation reused; the novelty is the coupled, VCEP-anchored, safety-first formulation.

---

### One-paragraph summary
DISCERN computes a single **joint posterior over disease and variant**, anchored to **ClinGen VCEP rules**, with each evidence stream entering **once** (phenotype→disease, genetics→variant, functional→both; PP4 expressed as the disease→variant coupling) — which simultaneously yields a ranked diagnosis, a **measured VUS reclassification** (concordant with 3-star truth), a **management-aware** treatment-safety flag, and the **cheapest decisive next observation** (including the cheap segregation/phasing data nobody collects), while **abstaining** when sparse likelihood ratios can't support a call. It runs on partial inputs, is validated **first by a reader study**, reuses OmniVar's foundation, and releases its discrimination knowledge as a citable, maintainable resource.
