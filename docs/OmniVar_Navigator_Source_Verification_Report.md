# OmniVar Navigator — Source Verification Report

**Verified:** 2026-06-12 · **By:** automated execution-time verification
**Method:** every URL, DOI, accession ID, and load-bearing numeric claim in
*OmniVar_Navigator_Detailed_Execution_Plan.md* was independently visited / fetched
and cross-checked against its primary source. This satisfies the plan's own
reproducibility mandate ("re-verify every URL/version at execution time — we
already learned this with SpliceAI").

**Headline:** All ~30 sources are real and reachable, and the engine's core
calibration math is confirmed against the primary literature. Six corrections
were found; the one that affects code (the Pangolin pip pitfall) is already fixed.

**Legend:** ✅ verified · ⚠️ verified, correction needed · ◻️ not independently re-derived.

---

## A. Corrections / action items

| # | Item | Finding | Action taken / needed |
|---|---|---|---|
| C1 | **dbNSFP URL** | `http://database.liulab.science/dbNSFP` refuses connection (dead link). | Use **https://www.dbnsfp.org** (downloads `/download`, releases `/releases`). Current **v5.0a** (also v4.9a). REVEL/CADD/BayesDel/VEST4/MutPred2 ship in the **academic** build only. |
| C2 | **Pangolin license** | Plan §1.1 says MIT; the repo github.com/tkzeng/Pangolin is **GPL-3.0**. | Corrected here. GPL-3.0 is fine for an orchestrated tool image (not statically linked into our code). |
| C3 | **`pip install pangolin`** | That PyPI name is the **SARS-CoV-2 lineage tool** (cov-lineages/pangolin), NOT the splice predictor. | Install the splice Pangolin **from source** in `docker/Dockerfile.tools`. **Already fixed in `environment.yml`.** |
| C4 | **EAHAD databases** | Per-gene subdomains (`f8-db.eahad.org`, …) now **302-redirect** to `dbs.eahad.org/<FACTOR>`. | Treat **https://dbs.eahad.org/** as canonical (old links still redirect). |
| C5 | **AutoPM3 status** | Now formally **published in *Bioinformatics* (2025)** — plan said "bioRxiv 2024". | Update citation. **PMC12263107 confirmed correct.** |
| C6 | **Tool maintenance age** | autoPVS1 latest v2.0 (Oct 2021); Pangolin v1.0.1 (Mar 2022). | Functional but dated — pin versions; adapters remain swappable (already the design). |

---

## B. Reference / knowledge sources (plan §1.1)

| Source | Status | Verified detail (2026-06-12) |
|---|---|---|
| gnomAD v4.1 | ✅ | Latest release (Apr 2024). License **CC0** (Creative Commons Zero) — confirmed at gnomad.broadinstitute.org/policies. GraphQL API + GCS as described. |
| ClinVar | ✅ | `ftp.ncbi.nlm.nih.gov/pub/clinvar/` live; `vcf_GRCh38/` + `tab_delimited/` (variant_summary.txt.gz) present, refreshed 2026-06-08; weekly VCF. |
| ClinGen eRepo | ✅ | FDA-recognized DB; tab/comma export + API (`erepo.genome.network/docs/cg-erepo`). |
| ClinGen CSpec | ✅ | cspec.genome.network live; machine-readable VCEP specs (see F8 GN071). |
| HPO | ✅ | Latest release **v2026-06-06**; license **CC BY 4.0** (matches plan). |
| AlphaMissense | ✅ | Zenodo **record 8208688**, DOI **10.5281/zenodo.8208688**, **CC BY-NC-SA 4.0**, Google DeepMind (Cheng et al. 2023). Exact match. |
| dbNSFP | ⚠️ C1 | Real; URL moved → https://www.dbnsfp.org; **v5.0a**. |
| Pejaver et al. 2022 | ✅ | *Am J Hum Genet* **109(12):2163–2177** (plan "109:2163" ✓). REVEL thresholds match Table 2 exactly. |
| MaveDB | ✅ | "MaveDB 2024" (*Genome Biology*, PMC11753097); >7M effects, 2,700+ datasets, 700+ genes; REST API + **`mavedb` PyPI** confirmed. |
| Pangolin (splice) | ⚠️ C2,C3 | github.com/tkzeng/Pangolin real; **GPL-3.0**; source install; PyPI `pangolin` ≠ this tool. |

## C. Bleeding & platelet domain (plan §1.2)

| Source | Status | Verified detail |
|---|---|---|
| EAHAD F8/F9/VWF/F5/F7/F10/F11 | ⚠️ C4 | Live; migrated to `dbs.eahad.org/<FACTOR>`; LOVD-based; variant + phenotype. |
| LOVD / CoagBase | ✅ | lovd.nl = LOVD v3.0 (IRDiRC-recognized); coagbase.org = "Coagulation Sequence and Structure Database". |
| ClinGen CFD-VCEP F8 **GN071** | ✅ | cspec.genome.network/cspec/ui/svi/svi/GN071 — F8 **v2.0.0**, Hemophilia A, X-linked. Confirms plan: PVS1 RNA rules, PP3/BP4/BP7 splice updates, **ratio-based hemizygote PS4** (gnomAD v4.1). |
| VWD VCEP (VWF), HHT VCEP (ENG/ACVRL1) | ✅ | Exist on ClinGen; specs on CSpec. |
| ISTH-SSC / Megy 2019 | ✅ | *J Thromb Haemost* 2019, **DOI 10.1111/jth.14479**, PMID 31179617. **91 Tier-1 genes** (21 coagulation, 9 thrombosis, 61 platelet). |

## D. Orchestrated tools (plan §1.3)

| Tool | Status | Verified detail |
|---|---|---|
| Exomiser | ✅ | AGPL-3.0; latest **v15.1.0** (2026-06-09); active. |
| AI-MARRVEL | ✅ | **NEJM AI 2024** (Baylor); code github.com/LiuzLab/AI_MARRVEL. |
| autoPVS1 | ✅⚠️ | GPL-3.0; v2.0 (2021); needs **VEP** cache. Xiang 2020 *Hum Mutat* (10.1002/humu.24051); 93% concordance. |
| AutoPM3 | ✅ C5 | **PMC12263107**, ***Bioinformatics* 2025** (86.1% acc / 72.5% recall). |
| VEP | ✅ | Apache-2.0; latest **release/116.0** (2026-06-10); active. |
| DeepRare | ✅ | **Nature 2026** (s41586-025-10097-9, PMID 41708847). |

## E. Validation cohorts (plan §1.4)

| Cohort | Status | Verified detail |
|---|---|---|
| Solve-RD | ✅ | EGA storage via **DAC** managed access; 4 ERNs. |
| RD-Connect GPAP | ✅ | Genome-Phenome Analysis Platform (Solve-RD analysis component). |
| UDN | ✅ | undiagnosed.hms.harvard.edu; managed access via **dbGaP**. |

## F. Core math / Appendix A (the engine hardcodes these)

| Claim | Status | Verified detail |
|---|---|---|
| `OddsPath = 350^(C/8)`, prior 0.10 | ✅ | Tavtigian 2020 (*Hum Mutat* 41:1734) uses X=2.0, Prior_P=0.10, **OPVSt=350**. Tavtigian 2018 (*Genet Med*, PMC6336098) Bayesian basis. |
| Point bands P≥10 / LP 6–9 / VUS 0–5 / LB −1…−6 / B≤−7 | ✅ | Tavtigian 2020 naturally-scaled system. |
| REVEL strengths (§A.3) | ✅ | Pejaver 2022 Table 2 — exact. |
| OddsPath PS3/BS3: 2.1/4.3/18.7 (§A.4) | ✅ | Brnich et al., *Genome Medicine* 2020 (10.1186/s13073-019-0690-2). |
| Richards 2015; Abou Tayoun 2018 PVS1 | ✅ | *Genet Med* 2015 (gim201530); *Hum Mutat* 2018 (10.1002/humu.23626). |
| Epidemiology ~25–30% dx, ~6 yr | ✅ | Corroborated by AI-MARRVEL/NIH sources. |
| Ancestry VUS disparity 1.5–2× | ◻️ | Consistent with published equity literature; to be cited at manuscript stage. |
