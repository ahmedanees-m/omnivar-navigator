# DISCERN — Concept Brief (v2)

**Working name:** **DISCERN** — *Differential-diagnosis, misdiagnosis-prevention & VUS-resolution engine for overlapping inherited bleeding & platelet disorders* (placeholder; alternatives: HemoDecode, OverlapDx).
**Clinical thesis:** *Decoding genetic overlap — classify and mitigate misdiagnosis in inherited bleeding disorders.*
**v1 → v2:** re-centered after external review. Diagnosis, misdiagnosis, and VUS resolution are now treated as **three outputs of one coupled model**, variant scoring is **anchored to ClinGen gene-specific VCEP rules** (not generic ACMG), the **evidence-circularity problem is handled explicitly**, the misdiagnosis flag is **management-aware**, **calibrated abstention** is a first-class safety property, and validation **leads with a reader study**.
**v2 → v2.1:** the circularity fix is pushed to the **per-ACMG-code** level — DISCERN decomposes each VCEP spec to its calibrated per-code strengths and routes each code to the one factor that owns it, rather than consuming the VCEP's bundled bottom-line label (which packs PS3/PP4/PM3/PP1 together and would re-introduce the double-counting). Plus: **VCEP coverage asymmetry stated plainly** — inside a cluster the index disease is usually covered and its highest-stakes confuser usually is not.
**Builds on:** OmniVar Navigator's rule-grounded evidence engine + infrastructure (reused). **Date:** 2026-06-12

---

## 1. The core idea (read this first)

Diagnosis, misdiagnosis, and VUS resolution are **not three features — they are three readouts of one engine**, because of a single fact:

> **PP4 — "this phenotype is specific for one disease" — structurally requires a disease model.** Generic variant classifiers (Varsome, Franklin, AlphaMissense) cannot compute it properly, because they do not model the disease. DISCERN can, because the disease-discrimination model *is* the thing PP4 needs.

So the disease-reasoning layer is **also** a VUS-resolution engine: the same phenotype that ranks the diagnosis supplies calibrated PP4, and the same discriminating test that separates two diseases (e.g., a RIPA mixing study, flow cytometry) usually supplies the **functional PS3** that upgrades the variant. **One information-gain calculation, two payoffs.**

DISCERN therefore answers one question with three faces: ***what is the most probable explanation, what would change it, and what is the cheapest observation that gets there?*** That coupling — calibrated, disease-model-driven VUS reclassification fused with differential diagnosis — is, as far as the literature shows, done by no existing tool, and is the project's genuine methodological contribution.

---

## 2. The problem

Inherited bleeding disorders are under-recognised, life-threatening, and **frequently misdiagnosed because distinct diseases converge on the same phenotype through shared molecular pathways**; up to ~40% are undiagnosed or misdiagnosed. The harm is concrete: **Glanzmann thrombasthenia (ITGA2B/ITGB3)** vs **LAD-III (FERMT3)** — both Glanzmann-type bleeding, but LAD-III needs a **stem-cell transplant**; **type 2B VWD (VWF)** vs **platelet-type VWD (GP1BA)** — clinically identical, **opposite treatments** (DDAVP can *harm* 2B); **Bernard-Soulier** mistaken for **ITP** → steroids/splenectomy; **Factor XIII deficiency** missed until a fatal intracranial bleed. Compounded by: >60% of variants in these genes are VUS; mechanistic overlap is poorly handled by current tools; and the settings that most need disambiguation have the least access to specialist labs.

---

## 3. How accurate evidence is built — anchored to expert rulebooks, counted once

DISCERN builds a single **joint posterior over (disease, variant)** from three evidence streams, where — critically — **each individual ACMG code enters the model exactly once** (the fix for the circularity that would otherwise make the tool confidently wrong):

- **Genetic** — scored with the **ClinGen gene-specific VCEP specifications** where they exist (the authoritative rulebook), not generic ACMG. *This is also the VUS-mitigation thesis, already demonstrated:* the ClinGen Platelet Disorder VCEP's Glanzmann-specific ITGA2B/ITGB3 criteria, on 70 pilot variants, **cut VUS from 29% to 20%** (Ross et al., Blood Adv 2021). But DISCERN **does not consume the VCEP's bottom-line label** — that label bundles PS3 (functional), PP4 (phenotype), PM3 (phasing), PP1 (segregation), which DISCERN owns in *other* factors. Instead it **decomposes the spec to per-code strengths** and uses **only the variant-intrinsic codes here** (PM2/BS1/BA1, PP3/BP4, PVS1, PM5/PS1); PP4 → the disease coupling, PS3 → the functional factor, PP1/PM3 → next-observations. (VCEPs already split into sub-teams of exactly this shape, so the partition is given.)
- **Phenotypic** — HPO features (including **pertinent negatives**: *no leukocytosis* argues against LAD-III) via likelihood ratios (the LIRICAL principle). Phenotype enters **once**, informing the disease — and its effect on the variant flows through the disease→variant coupling (calibrated PP4), **never added a second time**.
- **Lab/functional** — each disease predicts a pattern (GT → αIIbβ3 **absent**; LAD-III → αIIbβ3 **present-but-inactive** + leukocytosis). A functional result informs **both** the disease and the variant (PS3) through **one** factor, so it is counted once.

Why trustworthy: rule-grounded and curated (ClinGen VCEPs, ISTH, published criteria); every item shows source + strength; the verdict is computed by transparent math; the **LLM only reads notes and writes the explanation — never invents evidence or the diagnosis**; and where **no VCEP spec exists** (FERMT3/LAD-III, RASGRP2, granule genes) the output is explicitly tagged *"no gene-specific specification — reduced confidence."*

---

## 4. The disease-discrimination clusters (the knowledge core)

| # | Cluster | Look-alike diseases (genes) | VCEP rule status | Deciding observation | Misdiagnosis harm |
|---|---|---|---|---|---|
| 1 | **Integrin / aggregation** | Glanzmann (ITGA2B/ITGB3) · LAD-III (FERMT3) · RASGRP2 · LAD-I (ITGB2) | **GT: published** · others: none (flagged) | flow expression **+ activation**, WBC | LAD-III/I need **HSCT** |
| 2 | **Enhanced-RIPA / VWF–GPIb** | 2B VWD (VWF) · PT-VWD (GP1BA) · 2A VWD | VWF VCEP | **RIPA mixing** (plasma vs platelet) | DDAVP harms 2B; opposite Rx |
| 3 | **Macrothrombocytopenia / "looks like ITP"** | Bernard-Soulier (GP1BA/B/GP9) · MYH9 · others · vs ITP | **BSS specs: in progress** (GP9/GP1BA/GP1BB) | smear/immunofluorescence, flow | avoids **steroids/splenectomy** |
| 4 | **Granule disorders** | dense: HPS1–11, Chediak-Higashi (LYST) · alpha: Gray platelet (NBEAL2) | none (flagged) | EM, mepacrine, secretion | CHS → HLH (**HSCT**) |
| 5 | **Thrombocytopenia + leukaemia risk** | RUNX1 · ETV6 · ANKRD26 | **RUNX1: Myeloid Malignancy VCEP** | genetics, family history | surveillance; **donor selection** |
| 6 | **Coagulation factor deficiencies** | F8/F9/F11/F7/F10/F5/F13/fibrinogen | **F8/F9: CFD-VCEP (3-star, FDA-recognized)** | factor assays | FXIII miss → ICH |

Cluster knowledge is a **versioned, provenance-tagged knowledge base** — every likelihood ratio and discriminator linked to a source PMID and strength — curatable and citable like a mini-ClinGen for discrimination logic.

**On VCEP coverage (stated, not hidden):** inside a cluster the **index disease is usually VCEP-covered and its highest-stakes confuser usually is not** — GT is covered but LAD-III/RASGRP2 are not; 2B VWD (VWF) is covered but PT-VWD (GP1BA) sits in the in-progress platelet panel. So anchored variant-scoring is strongest where it matters least and absent where it matters most. This is survivable because discrimination at that boundary leans on **phenotype/functional features** (leukocytosis, αIIbβ3 activation, RIPA origin) — the real-world discriminators anyway — but the table above must not be read as uniform coverage.

---

## 5. Three outputs of one engine

From the joint posterior, DISCERN produces:

**(a) Ranked diagnosis + measured VUS reclassification.** The leading disease(s) with the evidence for/against/missing — *and*, because the model is coupled, an updated variant classification. **Falsifiable headline metric:** % of input VUS reclassified, **concordant with VCEP/ClinVar 3-star assertions** — turning "mitigates VUS" from a slogan into a number.

**(b) Management-aware misdiagnosis flag.** Not "competitor B is plausible," but **"the likely treatment is dangerous if B is true."** Firing is tied to **management divergence**, not posterior gap: a small probability of a *treatment-changing* competitor fires; a large probability of a management-irrelevant one does not. The flagship traps become hard stops — *DDAVP planned + 2B/PT-VWD ambiguity → resolve with RIPA mixing first; steroids/splenectomy + macrothrombocytopenia → confirm BSS first; LAD-III plausible → HSCT indicated, immunodeficiency risk acute.* (This is the load-bearing feature for the **narrative**.)

**(c) The cheapest decisive next observation.** Ranked by expected information gain over the **joint** (disease × variant) posterior — extended beyond lab tests to the cheap, ignored evidence everyone forgets: **family segregation, trans-phasing, functional assays** — weighted by decisiveness and accessibility. The output a clinician can act on with a blood draw: *"Testing the unaffected father for this variant (cheap, local) moves the variant VUS→Likely Pathogenic and the diagnosis 60%→92% Glanzmann."* (This is the load-bearing feature for **usefulness**, and the equity story made concrete.)

---

## 6. Safety: calibrated abstention

A tool that confidently misdiagnoses is worse than none. DISCERN is built to **say "undecidable — here is the deciding observation" exactly when it should.** It reports reliability diagrams, Brier score, and ECE, and its **headline safety metric is the confident-and-wrong rate.** Because likelihood ratios for ultra-rare diseases come from tiny samples, that estimation uncertainty is **propagated into the posterior** (wide credible intervals → abstention; hierarchical shrinkage as the rigorous form), so sparse data widens uncertainty rather than fabricating confidence.

---

## 7. Equity & access (corrected)

The settings that most need disambiguation have the **least** complete structured input (real inherited-platelet-disorder yields are low — e.g., 14% in one cohort). So usefulness cannot assume clean inputs. DISCERN therefore (a) runs in **partial-input mode** on any subset of {genetics, phenotype, labs} and quantifies what each missing piece would add, and (b) makes the **"single cheapest decisive next observation"** — including segregation/phasing data nobody collected — the feature that survives incomplete data. That is specialist-grade triage with a blood draw, for labs without a specialist; it fits the South Indian / consanguineous context where these disorders are enriched.

---

## 8. Why it's novel — the precise claim

The *components* — likelihood ratios, factor-graph inference, value-of-information — are standard and decades old. The **formulation and coupling are novel**: a calibrated joint disease × variant model, anchored to gene-specific VCEP rules, that resolves diagnosis, misdiagnosis-safety, and VUS in one pass. Claimed precisely, it is bulletproof; claimed as a new inference primitive, a methods reviewer objects; claimed as mere plumbing, it is undersold.

✓ does it · ◑ partial · ✗ no

| Capability | Predictors (AlphaMissense/REVEL) | ACMG classifiers/CDSS (InterVar, Varsome, Franklin) | Phenotype→gene (Exomiser, LIRICAL, AI-MARRVEL) | Agentic DDx (DeepRare, *Nature* 2026) | IPD panels | **DISCERN** |
|---|---|---|---|---|---|---|
| Classify a variant | ✓ | ✓ | ◑ | ◑ | ✗ | ✓ **(VCEP-anchored)** |
| Rank diseases from phenotype | ✗ | ◑ | ✓ | ✓ | ✗ | ✓ |
| **Reason across look-alike / shared-pathway diseases** | ✗ | ✗ | ✗ | ◑ general | ✗ | **✓ clusters** |
| **Calibrated PP4 / disease-model-driven VUS reclassification** | ✗ | ✗ | ✗ | ✗ | ✗ | **✓ unique** |
| **Coupled disease × variant joint model** | ✗ | ✗ | ✗ | ✗ | ✗ | **✓ unique** |
| **Management-aware misdiagnosis / treatment-safety flag** | ✗ | ✗ | ✗ | ✗ | ✗ | **✓ unique** |
| **Cheapest decisive next observation (incl. segregation/phasing)** | ✗ | ✗ | ✗ | ✗ | ✗ | **✓ unique** |
| **Calibrated abstention (confident-wrong rate)** | ✗ | ✗ | ✗ | ✗ | ✗ | **✓** |
| Verdict deterministic (not LLM-generated) | n/a | ✓ | ✗ | ✗ | n/a | **✓** |
| Partial-input / equity-aware | ✗ | ✗ | ✗ | ✗ | ✗ | **✓** |

DeepRare does general agentic DDx but the verdict is LLM-generated and it is not specialised, not coupled to variant scoring, not management-aware, not abstaining. LIRICAL pioneered LR phenotype diagnosis — DISCERN extends it to a coupled multi-evidence model with VCEP-anchored variant scoring and the safety layer. **None prevents the wrong diagnosis or reclassifies VUS via a disease model.**

---

## 9. What carries over from OmniVar Navigator

Rule engine → the **VCEP-anchored genetic-evidence factor**. Evidence adapters → the genetic/phenotype streams. Mechanism knowledge → the discrimination matrices. Functional-assay catalog → the next-observation catalog. Equity layer, LLM gateway, audit, Docker/VM/Nemotron infra, release machinery → reused unchanged. ≈70% of the foundation transfers; the new science is the **joint model, the management-aware flag, abstention, and the partial-input next-observation core**.

---

## 10. Validation (summary; full protocol in the execution plan)

Leads with a **reader study** — do non-specialists diagnose better and faster *with* DISCERN vs without, on vignettes (the operational definition of "does it help," pre-registerable and achievable) — supported by: the **VUS-reclassification metric** vs VCEP/ClinVar 3-star truth; a **management-aware misdiagnosis-rescue** set assembled from documented mislabelled cases (honest, pre-registered **case-control**, accepted as small/not powered); a **silent/shadow prospective** run against adjudicated diagnosis; **calibration/abstention** metrics; and the **South Indian Glanzmann cohort** for real, ancestry-relevant, mechanism-distinct validation. Pre-registered; TRIPOD+AI/DECIDE-AI; negatives included.

---

## 11. Honest limitations & sustainability

DISCERN disambiguates *within known clusters of known diseases* — not a novel-gene discovery engine. Its calibration is bounded by sparse likelihood ratios (hence abstention). It recommends; it never auto-diagnoses or auto-treats. **Maintenance is a real question:** discrimination matrices decay as guidelines evolve — so the knowledge base is versioned and provenance-tagged from day one, with an explicit aim to partner with the **ISTH SSC / ClinGen VCEPs** so it outlives the PhD and becomes a standalone, citable resource. Prospective clinical validation is a later phase.

---

### One-paragraph summary
DISCERN treats diagnosis, misdiagnosis-safety, and VUS resolution as three readouts of **one coupled disease × variant model** — because the disease-discrimination model is exactly what computing PP4 (and thus resolving VUS) requires, and the test that separates two diseases is usually the functional assay that upgrades the variant. Variant scoring is anchored to **ClinGen VCEP rules** (already shown to cut Glanzmann VUS 29%→20%), every evidence stream enters **once** (handling the circularity that would otherwise inflate confidence), the misdiagnosis flag fires on **treatment danger** not posterior gap, the engine **abstains** when sparse data can't support a call, and its load-bearing usefulness feature is the **cheapest decisive next observation** that works even on partial inputs. The components are standard; the coupled, VCEP-anchored, safety-first formulation is the novelty — and no existing tool does it.
