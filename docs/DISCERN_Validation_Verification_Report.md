# DISCERN Validation and Benchmarking - Source Verification Report

**Verified:** 2026-06-13. **Method:** every dataset, accession, DOI/PMID, and benchmark
number in *DISCERN_Validation_Data_and_Benchmarking_Plan.md* was independently checked
against the primary source.

**Headline:** every load-bearing validation source is real and correctly identified.
Two updates (V1, V2). Tier A (open) is runnable now; Tiers B and C require DAC/IRB
applications and cannot be downloaded.

Legend: OK verified - UP verified with update.

## Updates

| # | Item | Finding |
|---|---|---|
| V1 | Phenopacket Store size | The plan states 5,213 cases / 378 diseases. The current corpus is LARGER: ~8,207 phenopackets / 521 Mendelian and chromosomal diseases / 423 genes / 959 publications (HGG Advances 2024). Use the current release; the plan's number was an earlier version and is conservative. |
| V2 | CSpec host | Canonical host is `cspec.genome.network` (also `genboree.org/cspec`); the plan's `cspec.genboree.org` is a related mirror. GN079 (ITGA2B/GT), GN071 (F8), GN081 (VWF, v1.0.0, 2A/2B/2M) confirmed. |

## Tier A - open, runnable now

| Source | Status | Detail |
|---|---|---|
| ClinGen ERepo API | OK | `erepo.clinicalgenome.org`; bulk export (`/api/classifications/all?format=tabbed`) is real and large (>10 MB; ~10,500 variants, 140+ genes, 37+ VCEPs). The tabbed export carries the applied evidence codes per variant. **Already held on the VM** (`data/raw/erepo/erepo_classifications.tab`, 12,499 records). |
| ClinGen CSpec | OK UP V2 | GN079 GT, GN071 F8, GN081 VWF (v1.0.0) confirmed at cspec.genome.network. |
| ClinVar | OK | 3-star VCEP submissions = the gold-standard truth label; held on the VM (variant_summary + clinvar VCF). |
| Phenopacket Store | OK UP V1 | GA4GH corpus, HGG Advances 2024 (medRxiv 2024.05.29.24308104, PMC11564936); GitHub `monarch-initiative/phenopacket-store` + Zenodo; HPO observed + excluded, OMIM/Mondo diagnosis, variants. |
| RareBench | OK | KDD2024 (arXiv 2402.06341); 1,197 cases (MME/LIRICAL/HMS/RAMEDIS/PUMCH-ADM); github.com/chenxz1111/RareBench. |
| PhEval | OK | Monarch Initiative; BMC Bioinformatics 2025 (10.1186/s12859-025-06105-4, PMC11195176); github.com/monarch-initiative/pheval (+ pheval.exomiser). |
| EAHAD / LOVD / MaveDB | OK | Verified previously (OmniVar report); EAHAD now at dbs.eahad.org. |

## Tier B - application (DAC), cannot download

| Source | Status | Detail |
|---|---|---|
| BRIDGE-BPD / ThromboGenomics | OK | Downes et al., *Blood* 2019; **134(23):2082-2091**; **2,396 patients, 37.3% yield** (coagulation 63.6%, thrombotic 48.9%, thrombocytopenia 47.8%, platelet function 26.1%). EGA **EGAS00001001172**; NIHR BioResource **EGAS00001001012**. REC 10/H0304/66. Access: NIHR BioResource DAC (bioresource.nihr.ac.uk, DAA023). |
| ITP misdiagnosis cohort | OK | *Blood Advances* 2025; **9(7):1497**, PMID 39808791, PMC11985033; **80 chronic-ITP patients** (ThromboGenomics n=72 + immune panel n=50); P/LP 11%, VUS 32.5%; explicitly motivated by inherited-thrombocytopenia mislabelled as ITP. Same NIHR route. |

## Tier C - own / collaboration

| Source | Status | Detail |
|---|---|---|
| South Indian Glanzmann cohort | OK | GT enriched by consanguinity in South India (verified; e.g. tertiary-center series PMID 30789846). Local IRB; aggregate-only; no patient data in public artifacts. |

## Benchmark bars (to contextualize, verified)

| Claim | Status | Detail |
|---|---|---|
| Exomiser top-1 ~35.5% | OK | EJHG benchmark (medRxiv 2024.07.22.24310816, PMC11302616): Exomiser 35.5% top-1, 46.3% top-3, 58.5% top-10; best LLM (o1-preview) 23.6% top-1. |
| DeepRare R@1 29-73% | OK | DeepRare (Nature 2026), verified previously; range is benchmark-dependent. |
| GIAB spike-in template | OK | NIST Genome-in-a-Bottle reference samples (HG001-007) are the standard template-exome source. |

## Conclusion and runnable scope

The variant layer (Tier A: ERepo per-code reconstruction, VUS reclassification) and the
diagnosis layer (Tier A: Phenopacket Store bleeding subset, PhEval head-to-head harness)
are executed now on real, open data. Tiers B/C are correctly identified and require
applications outside this scope; the harnesses for them are built so they run as soon as
access clears. No synthetic data is used as a headline result.
