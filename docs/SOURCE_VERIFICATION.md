# Source verification log

**Verified:** 2026-06-12 · **Method:** each URL / DOI / ID / numeric claim in the
execution plan was independently visited or fetched and cross-checked against the
primary source. This satisfies the plan's reproducibility mandate ("re-verify every
URL/version at execution time — we already learned this with SpliceAI").

**Legend:** ✅ verified · ⚠️ verified with a correction/update needed · ❌ broken.

## Summary of corrections (action items)

| # | Item | Finding | Action |
|---|---|---|---|
| C1 | **dbNSFP URL** | `http://database.liulab.science/dbNSFP` refuses connection (dead). | Use **https://www.dbnsfp.org** (download `/download`, releases `/releases`). Current **v5.0a** (also v4.9a). REVEL/CADD/BayesDel/VEST4/MutPred2 are in the **academic** build only. |
| C2 | **Pangolin license** | Plan says MIT; the repo (github.com/tkzeng/Pangolin) is **GPL-3.0**. | Correct the license note. GPL-3.0 is fine for an orchestrated tool image (not linked into our code). |
| C3 | **`pip install pangolin`** | That PyPI name is the **SARS-CoV-2 lineage tool** (cov-lineages/pangolin), not the splice predictor. | Install the splice Pangolin **from source** (`git clone … && pip install .`) inside `docker/Dockerfile.tools`. **Fixed in `environment.yml`.** |
| C4 | **EAHAD DBs** | Per-gene subdomains (`f8-db.eahad.org`, …) now **302-redirect to `dbs.eahad.org/<FACTOR>`**. | Update canonical URLs to `https://dbs.eahad.org/` (old links still redirect). |
| C5 | **AutoPM3 status** | Now formally **published in *Bioinformatics* 2025** (was "bioRxiv 2024"). | Update citation; PMC12263107 confirmed correct. |
| C6 | **Maintenance age** | autoPVS1 latest v2.0 (Oct 2021); Pangolin v1.0.1 (Mar 2022). | Functional but dated — pin versions and keep the adapter swappable (already the design). |

Everything else below verified as stated in the plan.

## §1.1 Reference / knowledge sources

| Source | Status | Verified detail (2026-06-12) |
|---|---|---|
| gnomAD v4.1 | ✅ | v4.1 is the latest (released Apr 2024). License = **CC0** (Creative Commons Zero Public Domain Dedication) — confirmed on gnomad.broadinstitute.org/policies. GraphQL API + GCS as described. |
| ClinVar | ✅ | `ftp.ncbi.nlm.nih.gov/pub/clinvar/` live; `vcf_GRCh38/` + `tab_delimited/` (variant_summary.txt.gz) present, updated 2026-06-08. Weekly VCF release. |
| ClinGen eRepo | ✅ | erepo.clinicalgenome.org confirmed (FDA-recognized DB). Tab-/comma-delimited export + API (`erepo.genome.network/docs/cg-erepo`). |
| ClinGen CSpec | ✅ | cspec.genome.network live; hosts machine-readable VCEP specs (see F8 GN071 below). |
| HPO | ✅ | hpo.jax.org / obophenotype repo confirmed; latest release **v2026-06-06**. License = **CC BY 4.0** (matches plan). |
| AlphaMissense | ✅ | Zenodo **record 8208688** = "Predictions for AlphaMissense", DOI **10.5281/zenodo.8208688**, **CC BY-NC-SA 4.0**, Google DeepMind (Cheng et al. 2023). Exact match. |
| dbNSFP (REVEL/CADD/BayesDel/VEST4/MutPred2) | ⚠️ C1 | Resource real; **URL changed** → https://www.dbnsfp.org, current **v5.0a**. |
| Pejaver et al. 2022 | ✅ | *Am J Hum Genet* **109(12):2163–2177** (plan: "109:2163" ✓). REVEL thresholds **match Table 2 exactly**: PP3 ≥0.932 Strong / ≥0.773 Mod / ≥0.644 Supp; BP4 ≤0.290 Supp / ≤0.183 Mod / ≤0.016 Strong. |
| MaveDB | ✅ | mavedb.org + "MaveDB 2024" (*Genome Biology*, PMC11753097); >7M variant effects, 2,700+ datasets, 700+ genes. REST API + **`mavedb` PyPI** package confirmed (pypi.org/project/mavedb/). |
| Pangolin (splice) | ⚠️ C2,C3 | github.com/tkzeng/Pangolin real (deep-learning splice predictor); **GPL-3.0**; install from source; **PyPI `pangolin` ≠ this tool**. |

## §1.2 Bleeding & platelet domain

| Source | Status | Verified detail |
|---|---|---|
| EAHAD F8/F9/VWF/F5/F7/F10/F11 DBs | ⚠️ C4 | Live; migrated to `dbs.eahad.org/<FACTOR>` (e.g. `/FVIII`); LOVD-based, variant + phenotype. f7-db / factorix.org confirmed reachable. |
| LOVD / CoagBase | ✅ | lovd.nl = LOVD v3.0 (IRDiRC-recognized, active). coagbase.org = "Coagulation Sequence and Structure Database" live. |
| ClinGen CFD-VCEP F8 spec **GN071** | ✅ | cspec.genome.network/cspec/ui/svi/svi/GN071 — F8 **v2.0.0**, Hemophilia A, X-linked. Confirms the plan's claims: PVS1 RNA rules, PP3/BP4/BP7 splice updates, **ratio-based hemizygote PS4** (gnomAD v4.1). |
| ClinGen VWD VCEP (VWF), HHT VCEP (ENG/ACVRL1) | ✅ | CFD/VWD/HHT VCEPs exist on ClinGen; specs hosted on CSpec. |
| ISTH-SSC / Megy et al. 2019 Tier-1 | ✅ | *J Thromb Haemost* 2019, **DOI 10.1111/jth.14479**, PMID 31179617. **91 Tier-1 genes** (21 coagulation, 9 thrombosis, 61 platelet), annually updated. Matches plan ("~91"). |

## §1.3 Orchestrated tools

| Tool | Status | Verified detail |
|---|---|---|
| Exomiser | ✅ | github.com/exomiser/Exomiser, **AGPL-3.0**, latest **v15.1.0** (2026-06-09), actively maintained. |
| AI-MARRVEL | ✅ | ai.marrvel.org + **NEJM AI 2024** (Baylor); code github.com/LiuzLab/AI_MARRVEL. |
| autoPVS1 | ✅⚠️ | github.com/JiguangPeng/autopvs1, **GPL-3.0**, v2.0 (2021); needs **VEP** cache (refseq 104). Xiang 2020 *Hum Mutat* (10.1002/humu.24051), web autopvs1.genetics.bgi.com — 93% concordance. |
| AutoPM3 | ✅ C5 | **PMC12263107** = "AutoPM3… LLM-driven PM3 extraction", ***Bioinformatics* 2025** (86.1% acc / 72.5% recall). |
| VEP | ✅ | github.com/Ensembl/ensembl-vep, **Apache-2.0**, latest **release/116.0** (2026-06-10), active. |
| DeepRare | ✅ | "An agentic system for rare disease diagnosis with traceable reasoning", **Nature 2026** (s41586-025-10097-9, PMID 41708847). |

## §1.4 Validation cohorts

| Cohort | Status | Verified detail |
|---|---|---|
| Solve-RD | ✅ | solve-rd.eu; data at **EGA** via **DAC-controlled** managed access; 4 ERNs. Matches plan. |
| RD-Connect GPAP | ✅ | Genome-Phenome Analysis Platform confirmed as the Solve-RD analysis component. |
| UDN | ✅ | undiagnosed.hms.harvard.edu; managed access via **dbGaP** (established resource). |

## Core math / Appendix A (the engine hardcodes these)

| Claim | Status | Verified detail |
|---|---|---|
| Posterior `OddsPath = 350^(C/8)`, prior 0.10 | ✅ | Tavtigian 2020 (*Hum Mutat* 41:1734) uses X=2.0, Prior_P=0.10, **OPVSt=350** — exactly the plan's formula. Tavtigian 2018 (*Genet Med*, PMC6336098) is the Bayesian basis. |
| Point bands P≥10 / LP 6–9 / VUS 0–5 / LB −1…−6 / B≤−7 | ✅ | Tavtigian 2020 naturally-scaled point system. |
| REVEL strength thresholds (§A.3) | ✅ | Pejaver 2022 Table 2 (above). |
| OddsPath PS3/BS3: ≥2.1 Supp, ≥4.3 Mod, ≥18.7 Strong (§A.4) | ✅ | Brnich et al., *Genome Medicine* 2020 (10.1186/s13073-019-0690-2) — the standard ClinGen SVI functional-evidence OddsPath thresholds. |
| Richards 2015 ACMG/AMP; Abou Tayoun 2018 PVS1 | ✅ | *Genet Med* 2015 (gim201530); *Hum Mutat* 2018 (10.1002/humu.23626). |
| Epidemiology: ~25–30% dx rate, ~6 yr to dx | ✅ | Corroborated by the AI-MARRVEL/NIH sources (~30% diagnostic rate, ~6 years). |
| Ancestry VUS disparity 1.5–2× | ◻️ | Consistent with the published equity-in-classification literature; not independently re-derived in this pass (claim retained, to be cited at manuscript stage). |
