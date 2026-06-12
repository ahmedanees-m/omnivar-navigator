# DISCERN — Source Verification Report

**Verified:** 2026-06-13 · **By:** automated execution-time verification
**Method:** every DISCERN-specific citation, DOI/PMID, VCEP status, and clinical
discrimination fact in *DISCERN_Concept_Brief_v2.md* and *DISCERN_Execution_Plan_v2.md*
was independently fetched/searched and cross-checked against the primary source.
Sources carried over from OmniVar (gnomAD, ClinVar, HPO, AlphaMissense, dbNSFP, MaveDB,
Pangolin, autoPVS1, AutoPM3, Exomiser/AI-MARRVEL, Tavtigian/Pejaver/Brnich math) were
already verified — see *OmniVar_Navigator_Source_Verification_Report.md*; their
corrections **C1–C6 are honored** here.

**Headline:** every load-bearing DISCERN claim is correct. The flagship VUS-mitigation
number is verified **verbatim**. Three minor updates (D1–D3) are noted.

**Legend:** ✅ verified · ⚠️ verified, minor update · ◻️ directional/cohort-dependent.

---

## A. Updates to apply (minor)

| # | Item | Finding | Action |
|---|---|---|---|
| D1 | **BSS VCEP status** | ClinGen Platelet Disorder VCEP now has a **published GP1BA-BSS spec (v1.1.0)**; GP9/GP1BB still in progress. The plan says "BSS in progress (GP9, GP1BA, GP1BB)". | Update: GP1BA-BSS = published; GP9/GP1BB = in progress. Note GP1BA is **dual-phenotype** — BSS (LoF, AR, now spec'd) vs **PT-VWD (GoF, AD, NOT covered)**, so the plan's "PT-VWD = GP1BA uncovered" still holds for the PT-VWD phenotype. |
| D2 | **DDAVP in 2B VWD** | Literature says DDAVP is **"controversial / can worsen thrombocytopenia"** in 2B, not an absolute contraindication. | Keep the safety flag (caution is correct); phrase as "may worsen thrombocytopenia / use with caution," not "harms." |
| D3 | **Epidemiology figures** | ">60% VUS", "~40% misdiagnosed", "14% yield" are **cohort-dependent**, not single canonical numbers (one cohort: 487 pts, 58% detection, ~half VUS). | Cite specific cohorts at manuscript stage; present as ranges, not fixed constants. |

Everything else verified as stated.

## B. Primary anchor — ClinGen gene-specific VCEPs (§1.1)

| Source | Status | Verified detail (2026-06-13) |
|---|---|---|
| **Ross et al. 2021 — PD-VCEP ITGA2B/ITGB3** | ✅✅ | *Blood Advances* **5(2):414–431**, PMID **33496739**; Glanzmann (AR); **70 pilot variants**; CSpec **GN079**. **VUS reduced "from 29% to 20%"** — confirmed **verbatim** (the headline thesis). 16 gene-specified rules. |
| **Luo et al. 2019 — MM-VCEP germline RUNX1** | ✅✅ | *Blood Advances* **3(20):2962–2979**, DOI **10.1182/bloodadvances.2019000644**, PMID 31648317; reduced CONF/VUS by **33%**. |
| **CFD-VCEP F8/F9** | ✅ | F8 spec GN071 (v2.0.0), 3-star FDA-recognized (verified in OmniVar). Gold-standard validation set. |
| **Platelet Disorder VCEP — BSS** | ⚠️ D1 | Affiliation 50040; GP1BA-BSS **published (v1.1.0)**; GP9/GP1BB in progress. |
| **VWF VCEP** | ✅ | Covers 2A/2B/2M (VWF). PT-VWD (GP1BA, GoF) is a different phenotype, uncovered — coverage asymmetry confirmed. |
| **Boundary policy** | ✅ | FERMT3/LAD-III, RASGRP2, granule genes have **no VCEP spec** — the plan's "reduced-confidence tag" is correct. |

## C. Discrimination clusters — clinical facts (the knowledge core, §4)

| Cluster | Verified fact | Status |
|---|---|---|
| 1 Integrin | **LAD-III (FERMT3/kindlin-3)** = AR integrin-*activation* defect, "Glanzmann-like bleeding" + immunodeficiency + **neutrophilic leukocytosis** (the discriminator vs GT); **HSCT curative**; OMIM #612840. | ✅✅ |
| 2 VWF–GPIb | **PT-VWD (GP1BA) vs 2B VWD (VWF)** distinguished by **RIPA mixing** (plasma origin = 2B, platelet origin = PT-VWD); opposite treatments (ISTH/Othman 2020, JTH). | ✅✅ |
| 3 Macrothrombocytopenia | **BSS misdiagnosed as ITP** → improper steroids/splenectomy — documented. | ✅✅ |
| 4 Granule | **Chediak-Higashi (LYST) → HLH** ("accelerated phase", 50–85%, fatal untreated) → **HSCT** treatment of choice. | ✅✅ |
| 5 Thr+leukemia | **RUNX1** germline → familial platelet disorder + myeloid malignancy risk (MM-VCEP). | ✅✅ |
| 6 Coag factor | **FXIII (F13) deficiency → intracranial hemorrhage** (up to 30% spontaneous ICH, leading cause of mortality). | ✅✅ |

## D. Methods & supporting sources

| Item | Status | Detail |
|---|---|---|
| **LIRICAL (phenotype LR paradigm)** | ✅ | Robinson et al., *AJHG* 2020, PMID **32755546**, DOI 10.1016/j.ajhg.2020.06.021; LR over HPO, correct dx in top-3 for 92.9% of 384 cases. Basis for the phenotype-LR + pertinent-negative stream. |
| **ISTH Tier-1 gene list (Megy 2019)** | ✅ | JTH 2019, 10.1111/jth.14479 (verified in OmniVar); 91 Tier-1 genes. |
| **South Indian Glanzmann cohort** | ✅ | GT enriched by consanguinity in S. India (e.g. 67% consanguineous in one cohort; 40-family molecular study; tertiary-center series PMID 30789846). Real, ancestry-relevant validation cohort. |
| **PT-VWD registry / mislabelled cases** | ✅ | PT-VWD documented as "often misdiagnosed" (PMID 22102188); ISTH guidance Othman 2020. Supports the misdiagnosis-rescue case-control. |
| **Orphanet / OMIM** | ✅ | LAD-III #612840, GT1 #273800 confirmed; disease defs + prevalence priors available. |
| **Joint-model / VOI / factor-graph math** | ✅ | Standard, decades-old (as the plan states); the novelty is the coupling, not the primitives. |
| **DeepRare (Nature 2026), AI-MARRVEL, Exomiser** | ✅ | Verified in OmniVar; correctly positioned as comparators. |

## E. OmniVar corrections carried forward (honor C1–C6)

C1 dbNSFP → https://www.dbnsfp.org (v5.0a); C2 Pangolin GPL-3.0; C3 install splice
Pangolin **from source** (not `pip install pangolin`); C4 EAHAD → `dbs.eahad.org`; C5
AutoPM3 published (Bioinformatics 2025); C6 pin dated tool versions. All apply unchanged.

---

**Conclusion:** the DISCERN plan's sources, DOIs/PMIDs, VCEP statuses, and clinical
discrimination facts are correct and current. Apply D1–D3 (minor) at execution; the
joint-model thesis rests on verified, citable foundations.
