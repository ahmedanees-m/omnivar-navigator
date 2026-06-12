# Data infrastructure & provenance

Reference data is downloaded with checksums and recorded in `data/manifest.json`
(URL, version, date, md5). Data files themselves are git-ignored; they live on the
VM and the `G:` drive, synced via SFTP.

## Reusable raw data carried over from the predecessor project

The earlier `omnivar-q` project (same author; the quantum module is now removed)
already downloaded the public reference datasets this project needs. These are
**retained and migrated** into `omnivar-navigator/data/`:

| Source | Role | Maps to |
|---|---|---|
| gnomAD (raw) | ancestry-resolved allele frequencies | PM2 / BS1 / BA1 |
| ClinVar (raw + processed parquet) | prior classifications; benchmark | PS1 / PM5 |
| ClinGen eRepo (raw + benchmark parquet) | expert-curated ground truth | primary benchmark |
| HPO (obo + annotations) | phenotype ontology / semantic similarity | PP4 |

Everything else in `omnivar-q` (old quantum/classical code, scripts, logs, models,
manuscript) is **not** carried over.

## Sources still to add (plan §1)

ClinGen CSpec gene specs (F8/F9/VWF…), AlphaMissense, dbNSFP (REVEL/BayesDel/…),
MaveDB, Pangolin, EAHAD/LOVD bleeding databases. See `data/sources/` for the
download/adapter scripts and `data/manifest.json` for versions/checksums.

## Layout

```
data/
  manifest.json        # versions + checksums (committed)
  sources/             # download/cache + manifest builder scripts (committed)
  raw/                 # downloaded sources (git-ignored; on VM + G:)
  processed/           # parquet benchmarks/features (git-ignored; on VM + G:)
```
