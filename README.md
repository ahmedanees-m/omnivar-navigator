# OmniVar Navigator

**A rule-grounded, value-of-information clinical decision-support engine for the diagnostic odyssey.**

OmniVar Navigator sits on top of existing variant-prioritization and pathogenicity
tools and answers a question none of them answer: *for this specific unsolved
patient and this specific uncertain variant, what is the single most informative,
cost-effective, ancestry-fair next action — and what would it do to the
classification?*

It is **decision support, not an autonomous classifier**. The deterministic rule
engine computes every verdict from a ClinGen/Tavtigian points ledger; a language
model only reads, retrieves, and explains — it never produces the classification.

- **Scope:** broad, full post-negative-workup engine across all modalities.
- **Priority domain:** inherited bleeding & platelet disorders (epilepsy and
  cancer-predisposition packs follow).

> Status: **Phase 0 — foundations & rule engine.** This repository is under active
> development. No real patient data is stored here or in any public artifact.

## Why it's novel

The crowded field classifies or ranks from the evidence *already available*. None
decides *what new evidence to acquire* to break a stuck case, prices that decision,
or corrects for the fact that the evidence it leans on (allele-frequency PM2/BS1,
in-silico PP3/BP4) is ancestry-biased. The genuine contributions here are the
**value-of-information decision layer over ACMG evidence codes**, the
**rule-grounded (neurosymbolic) architecture**, the **built-in equity mechanism**,
and the **verifiable learning loop**.

## Architecture (layers)

```
HUMAN-IN-THE-LOOP UI  (geneticist / MDT: recommendation + reasoning trace + accept/override)
        |
L5  DECISION & ORCHESTRATION ENGINE   <- the novel core (engine/)
      gap analysis -> code->action mapping -> value-of-information ranking -> whole-odyssey
        |                    |                         |
L4  RULE ENGINE (rules/)   EQUITY (equity/)        LEARNING STORE (learn/)
      deterministic         ancestry-aware           outcomes + priors
      ClinGen/VCEP points   down-weighting
        |
L3  EVIDENCE ORCHESTRATION (adapters/)  one swappable adapter per ACMG code/group
        |
L1/L2  INGESTION & FEATURE LAYER  VCF + notes->HPO + ancestry + assays + family
```

## Repository layout

| Path | Role |
|---|---|
| `core/` | shared schemas, the adapter contract, the hash-chained audit ledger |
| `rules/` | deterministic point engine, posterior bridge, VCEP spec loader, `specs/` |
| `adapters/` | one per evidence code/group (gnomAD, in-silico, splice, autoPVS1, …) |
| `engine/` | the novel core: gap, action mapping, VOI, recommend, case policy |
| `equity/` | ancestry inference, reliability flags, equitable routing, dashboards |
| `learn/` | outcome store + auditable Bayesian prior updates |
| `sim/`, `eval/` | parametric simulator + validation (ablation, retrospective, calibration) |
| `llm/` | model gateway (cloud Nemotron) + RAG; soft tasks only, never the verdict |
| `api/`, `ui/` | FastAPI engine + geneticist review frontend |
| `deploy/`, `docker/` | VM orchestration (SSH/SFTP) + service images (Docker-only on the VM) |
| `data/` | source download/cache scripts + `manifest.json` (versions, checksums) |
| `docs/` | concept brief, detailed execution plan, Phase-2 design |

## Compute topology

- **Laptop (dev):** write code, lint, unit tests on tiny fixtures, git, author Dockerfiles.
- **VM (`sjt418scope025`):** all heavy work — full data, feature extraction, LLM
  orchestration, validation runs, and hosting the web app. **Docker-only**: nothing
  is installed on the host; every process runs in a container.
- **Cloud Nemotron** (NVIDIA NIM) is the reasoning/soft-task LLM.
- **Storage:** reference data + checkpoints live on both the VM and the `G:` drive,
  synced via **SFTP** (not rclone). See `docs/COMPUTE_TOPOLOGY.md`.

## Quick start (dev)

```bash
conda env create -f environment.yml        # or: pip install -e .[dev]
conda activate omnivar-nav
make test                                   # ruff + pytest on fixtures
```

## Reproducibility & safety

Pinned `environment.yml` + Dockerfiles + `data/manifest.json` (source versions /
checksums) + the seeded simulator. Secrets are read from the environment, never
committed. The server is Docker-only. No real patient data in any public artifact.

## License

Code: MIT (see `LICENSE`). Reference datasets retain their own upstream licenses
(see `data/manifest.json`).

## Citation

See `CITATION.cff`. Author: **Anees Ahmed Mahaboob Ali** (`ahmedanees-m`).
