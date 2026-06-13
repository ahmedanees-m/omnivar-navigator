# DISCERN v3.1 - Source & Dataset Verification Report

**Date:** 2026-06-13 · **Scope:** every citation, dataset, ID, DOI, and load-bearing factual
claim in `DISCERN_Execution_Plan_v3.1.md` and `DISCERN_Coverage_Architecture_v1.md`, verified
independently against primary sources (PubMed, journal sites, ClinGen, NCBI ClinVar, gnomAD,
EGA, the predictor projects) before any v3.1 work is built on them. Method mirrors the v2
verification pass. **Verdict legend:** VERIFIED / CORRECTION / FLAG (use with care).

## 1. Citations (bibliographic)

| # | Citation (as planned) | Verdict | Correct metadata |
|---|---|---|---|
| 1 | Megy, Downes, Simeoni et al., *J Thromb Haemost* 2019;17(8):1253-1260 (ISTH TIER1) | **VERIFIED** | DOI 10.1111/jth.14479; PMID 31179617; PMC6852472. Defines "diagnostic-grade (TIER1)" genes. Original list 91 TIER1 (61 platelet). |
| 2 | Gresele/SSC, *J Thromb Haemost* 2015 (IPFD diagnosis) | **CORRECTION (locator)** | Add locator: **13(2):314-322**; DOI 10.1111/jth.12792; PMID 25403439. |
| 3 | Lentaigne, Freson, Laffan et al., *Blood* 2016;127(23):2814-2823 | **VERIFIED** | DOI 10.1182/blood-2016-03-378588; PMID 27095789. |
| 4 | *Diagnosis of VWD*, *Blood Adv* 2025;9(22):5870 | **VERIFIED** | Bowman M, James P; 9(22):5870-5879; DOI 10.1182/bloodadvances.2025016485; PMID 40845253. A review (not the guideline). Do NOT confuse with the monitoring report 9(14):3553. |
| 5 | *How I treat type 2 VWD*, *Blood* 2015;125(6):907 | **VERIFIED** | Tosetto A, Castaman G; 125(6):907-914; DOI 10.1182/blood-2014-08-551960; PMID 25477497. |
| 6 | *Treatment of rare factor deficiencies in 2016*, ASH Educ Program | **VERIFIED (add authors)** | Peyvandi F, Menegatti M; *Hematol Am Soc Hematol Educ Program* 2016;2016(1):663-669; DOI 10.1182/asheducation-2016.1.663; PMID 27913544. |
| 7 | de Moerloose, Schved, Nugent, *Haemophilia* 2016, PMID 27405678 | **VERIFIED** | Title: "Rare coagulation disorders: fibrinogen, factor VII and factor XIII." 22 Suppl 5:61-65; DOI 10.1111/hae.12965. PMID maps correctly. |
| 8 | Galera et al., *Int J Lab Hematol* 2019, doi:10.1111/ijlh.12999 | **VERIFIED (paper) / FLAG (numbers)** | Galera P, Dulau-Florea A, Calvo KR; 41(Suppl 1):131-141; PMID 31069978. **The prevalence triple RUNX1 ~3% / ANKRD26 ~18% / ETV6 ~5% could NOT be confirmed verbatim and conflicts with published cohorts (cohort-dependent). See note below; do not state as fact without the article text.** |
| 9 | Zaninetti et al., *J Thromb Haemost* 2017, doi:10.1111/jth.13855 | **CORRECTION (scope)** | Zaninetti C et al.; 15(12):2388-2392; PMID 28976612. Title is "...misdiagnosed and treated as **myelodysplastic syndrome**" - **MDS only, NOT ITP.** Cite it for ANKRD26-as-MDS; cite #10 (Joshi/Cooper) for ITP misdiagnosis. |
| 10 | *Genetic sequencing in chronic ITP*, *Blood Adv* 2025;9(7):1497 | **VERIFIED** | Joshi N, ... Cooper N; 9(7):1497-1507; DOI 10.1182/bloodadvances.2024014639; PMID 39808791. ~9-11% of "chronic ITP" carried diagnostic-grade inherited variants. |
| 11 | FXIII review, *PMC12825037* | **VERIFIED** | Jacobs JW et al., "Factor XIII Deficiency: A Review of Biology, Testing, and Treatment," *Clin Hematol Int* 2026. Resolves live. |
| 12 | Diagnostic review, *Biomolecules* 2025;15(6):846 | **VERIFIED** | Sanchez-Fuentes A et al.; DOI 10.3390/biom15060846; PMID 40563486. |

## 2. Datasets, predictors & accessions

| Item | Verdict | Authoritative status (cite this) |
|---|---|---|
| ClinGen eRepo (erepo.clinicalgenome.org) | **VERIFIED (nuance)** | Public home of VCEP classifications with per-code SEPIO evidence; downloadable .tab. FDA recognition applies to ClinGen/VCEP **curated data/process**, not "eRepo the database." ~8,000+ classifications (don't state a precise count). On the VM: 170 genes. |
| ClinVar variant_summary | **VERIFIED** | `variant_summary.txt.gz` on NCBI FTP, monthly; review-status stars (3*=expert panel, 4*=practice guideline, 2*=multiple no-conflict). >=2* is a defensible concordance truth set. On VM: `variant_summary.txt.gz` (2026-05-04) + `clinvar_20260503.vcf.gz`. |
| gnomAD v4.1.1 | **VERIFIED (nuance)** | v4.1.1 is real, dated **2026-03-30**, but it is a constraint/annotation refresh over the **v4.1 callset** (807,162 individuals). Cite "frequencies from gnomAD v4.1 callset (v4.1.1 annotations)." **On the VM only the gene-level `gnomad.v4.0.constraint_metrics.tsv` is present - NOT per-variant AFs**, so the per-variant gnomAD frequency cross-check (A1) is data-gated until per-variant AFs are pulled. |
| REVEL | **VERIFIED** | Ensemble missense predictor, 0-1; Ioannidis et al. AJHG 2016; scores via REVEL site / dbNSFP. |
| Pangolin "v1.1" | **CORRECTION** | No such tag. Author repo tkzeng/Pangolin tops at **v1.0.1** (2022, Zeng & Li, *Genome Biol*); the **Invitae fork** (used for gnomAD annotation) is **v1.4.x**. Pin a real version and name the fork. |
| SpliceAI "archived" | **VERIFIED (nuance)** | Illumina/SpliceAI repo archived (read-only) **2026-04-20**. True that it is no longer maintained; but Illumina gives **no "use Pangolin instead" notice** - "archived in favor of Pangolin" overstates it. |
| AlphaMissense | **CORRECTION (license)** | DeepMind, Cheng et al. *Science* 2023 (10.1126/science.adg7492). Precomputed predictions are **CC BY 4.0 (commercial use allowed)** - NOT non-commercial/CC BY-NC-SA. Code Apache-2.0. |
| EGA `EGAS00001001172` | **VERIFIED** | Exists; title "Sequencing of heritable Bleeding and Platelet Disorders" (BRIDGE-BPD, NIHR BioResource); data behind Downes et al. *Blood* 2019 (PMID 31064749). |
| ClinGen VCEPs (4) | **VERIFIED (names)** | Platelet Disorders VCEP (aff 50040); Coagulation Factor Deficiency VCEP (50041, F8/F9 approved Oct 2023); **von Willebrand Disease** VCEP (50051, approved Jun 2024); **Myeloid Malignancy VCEP** (50034) - the RUNX1 panel is the MM-VCEP (covers RUNX1/ANKRD26/ETV6/GATA2/DDX41/CEBPA), **not a standalone "RUNX1 VCEP."** |

## 3. Factual / clinical claims

All **VERIFIED** against primary sources: DDAVP contraindicated/harmful in type 2B VWD (worsens
thrombocytopenia); type 2B = VWF A1 GoF, ~40% thrombocytopenic (Tosetto/Castaman); PT-VWD =
GP1BA GoF mimic, treated with platelets vs 2B with VWF concentrate; type 2N mimics mild
hemophilia A, distinguished by VWF:FVIIIB assay, AR vs X-linked; recombinant FXIII-A2
(catridecacog) corrects F13A1 but NOT F13B deficiency; FXIII deficiency has normal PT/aPTT +
delayed umbilical bleeding + high ICH risk; Quebec platelet disorder = PLAU duplication,
treated with antifibrinolytics not platelets; combined FV+FVIII = LMAN1/MCFD2, combined
vit-K-dependent = GGCX/VKORC1; WHO "myeloid neoplasms with germline predisposition and
pre-existing platelet disorder" = RUNX1/ANKRD26/ETV6; RUNX1=FPDMM, ANKRD26=THC2, ETV6=THC5.

**Two nuances:**
- **"Low VWF"** is no longer a guideline-distinct diagnostic category (2021 ASH/ISTH/NBDF/WFH;
  2025 review): type 1 VWD is now VWF <0.30 IU/mL and 0.30-0.50 is part of the type-1 spectrum.
  Type 1 ~75% of VWD and ~35% lacking an identifiable VWF variant are both supported. C9 should
  be framed as "type 1 / low VWF" descriptively, not as a separate nosological class.
- **HCM 17.4% VUS-reclassification** (cited as the cross-domain precedent for the
  VCEP-reclassification paradigm): the 17.4% is **correct** (12/69 VUS) but traces to **Caroselli
  et al., *Human Mutation* 2025 (10.1155/humu/6500093)**, a retrospective application study - NOT
  the foundational ClinGen Cardiomyopathy VCEP guideline. Attribute it to Caroselli 2025.

## 4. Corrections to apply to the plan / coverage doc

1. **Galera prevalence triple (3%/18%/5%)** - remove or re-source; cite as "cohort-dependent" or
   pull the exact figures from the Galera 2019 full text. (Coverage Arch. Part 1C.)
2. **Zaninetti 2017** - cite only for ANKRD26-as-**MDS**; use Joshi/Cooper 2025 (Blood Adv 9(7):1497)
   for ANKRD26/RUNX1-as-**ITP**. (Coverage Arch. C4; Exec Plan B4.)
3. **Pangolin "v1.1"** -> pin a real version (tkzeng v1.0.1 or Invitae fork v1.4.x), name the fork. (A2.)
4. **AlphaMissense** is CC BY 4.0 (commercial OK) - do not treat as non-commercial. (A2/risk table.)
5. **gnomAD** - cite "v4.1 callset / v4.1.1 annotations"; **per-variant AFs not on VM** -> A1's
   gnomad_freq_check is data-gated; pull per-variant AFs or scope it to eRepo-embedded AFs.
6. **RUNX1 VCEP** -> "Myeloid Malignancy VCEP (RUNX1 specifications)"; **VWD VCEP** capitalization "von Willebrand."
7. **Gresele 2015** add locator 13(2):314-322; **ASH Educ 2016** add authors Peyvandi & Menegatti.
8. **eRepo "FDA-recognized"** -> recognition is of ClinGen/VCEP data, not the database object.

**Bottom line:** every citation is a real paper and every dataset/tool is real; the plan's
scientific scaffolding holds. The fixes are metadata locators, two mis-scoped attributions
(Zaninetti=MDS-only; HCM 17.4%=Caroselli 2025), one unverified statistic to re-source (Galera
triple), a tool version/license correction (Pangolin/AlphaMissense), and one data-availability
gate (gnomAD per-variant AFs absent on the VM). These are folded into the v3.1 execution summary
and respected during the build.
