# OmniVar Navigator — Detailed Execution Plan

**Companion to:** *OmniVar Navigator — Concept Brief & Execution Plan v1.0*
**Purpose:** Operational detail — concrete sources (URLs, access, license), code module specifications with real signatures, and methods with the underlying math.
**Scope:** Broad full-odyssey engine; priority domain = inherited bleeding & platelet disorders.
**Date:** 2026-06-11
**Reproducibility note:** Bioinformatics resources change. Every URL/version below should be re-verified at execution time (we already learned this lesson when SpliceAI was archived). Verified as of June 2026.
**Update (this revision):** added compute topology & local↔VM workflow (§2.4), self-hosted LLM integration via Ollama/Qwen + Nvidia Nemotron (§2.5), expanded GitHub/Zenodo release engineering (Phase 8), and a new deployment / web-app / hosting phase (Phase 9). The server is **Docker-only**; SSH uses **key-based auth** (no passwords in code or images).

---

## How to read this document

Each step uses a fixed template:

- **Objective** — what this step exists to achieve.
- **Goal / acceptance** — the measurable bar for "done."
- **Sources** — exact data/tools used (see also the consolidated Source Registry, §1).
- **Methods** — the algorithmic/statistical approach.
- **Code/artifacts** — module paths, key signatures, illustrative implementation.
- **Expected outcome** — the concrete deliverable.
- **Depends on** — upstream steps.

Code is specification-grade: real signatures and correct logic, with `...` for boilerplate. The math behind the novel pieces is in the Methods Appendix (§A).

---

## 1. Source Registry (consolidated)

### 1.1 Reference / knowledge sources (public, no application)

| Source | URL | Access / License | Role · maps to |
|---|---|---|---|
| gnomAD v4.1 | https://gnomad.broadinstitute.org · API: https://gnomad.broadinstitute.org/api | Public · CC0 · GraphQL API + GCS files | Ancestry-resolved allele frequencies → **PM2 / BS1 / BA1** |
| ClinVar | https://ftp.ncbi.nlm.nih.gov/pub/clinvar/ | Public domain · weekly VCF + variant_summary | Prior classifications, same-AA-change → **PS1 / PM5**; benchmark |
| ClinGen Evidence Repository (eRepo) | https://erepo.clinicalgenome.org/evrepo/ · bulk: `/api/classifications/all?format=tabbed` | Public | Expert-curated ground truth (incl. bleeding genes) — **primary benchmark** |
| ClinGen CSpec (Criteria Spec Registry) | https://cspec.genome.network | Public | Machine-readable gene-specific VCEP rules → **rule engine specs** |
| HPO | https://hpo.jax.org · releases: obophenotype/human-phenotype-ontology | Public · CC BY 4.0 | Phenotype ontology, semantic similarity → **PP4** |
| AlphaMissense | https://zenodo.org/record/8208688 | CC BY-NC-SA 4.0 | Missense effect score (calibrated) → **PP3 / BP4** |
| REVEL / CADD / BayesDel / VEST4 / MutPred2 | dbNSFP: http://database.liulab.science/dbNSFP | Academic | Calibrated in-silico evidence → **PP3 / BP4** |
| Pejaver et al. 2022 calibrated thresholds | AJHG 109:2163 (+ 2025 extension, Genet Med) | Published | Score→strength mapping for predictors (§A.3) |
| MaveDB | https://www.mavedb.org · API: github.com/VariantEffect/mavedb-api (`pip install mavedb`) | Public · REST/JSON · CSV per score set | Functional (MAVE/SGE) effect maps → **PS3 / BS3** |
| Splice predictor (SpliceAI replacement) | Pangolin: github.com/tkzeng/Pangolin | MIT · `pip install pangolin` | Splice impact → **PP3 / BP4 / BP7 / PVS1-RNA** |

### 1.2 Bleeding & platelet domain sources (priority domain)

| Source | URL | Access | Role |
|---|---|---|---|
| EAHAD F8 DB (Haemophilia A) | http://f8-db.eahad.org | Public (LOVD-mirrored) | F8 variants + lab/clinical phenotype + functional/structural effects |
| EAHAD F9 DB (Haemophilia B) | http://f9-db.eahad.org | Public | F9 variants + phenotype |
| EAHAD VWF DB (von Willebrand) | http://vwf-db.eahad.org | Public | VWF variants + subtype + functional |
| EAHAD F5 / F7 / F10 / F11 DBs | http://f{5,7,10,11}-db.eahad.org | Public | Rare factor deficiencies |
| LOVD mirrors / CoagBase | https://www.lovd.nl · http://coagbase.org | Public | Shared LOVD format; gene/RefSeq/numbering reference |
| ClinGen CFD-VCEP specs (F8, F9) | cspec.genome.network (e.g., F8 spec GN071) | Public | Gene-specific ACMG rules (RNA/splice PVS1, hemizygote PS4) |
| ClinGen VWD VCEP specs (VWF) | cspec.genome.network | Public | Subtype-aware (Types 1, 2A/2B/2M/2N, 3) rules |
| ClinGen HHT VCEP specs (ENG, ACVRL1) | cspec.genome.network | Public | HHT gene rules |
| ISTH-SSC platelet/genomics guidance | https://www.isth.org | Public guidance | IPD assay standards (LTA, flow cytometry) |

**Platelet/integrin genes (no dedicated VCEP yet → use general ACMG + ClinGen SVI):** ITGA2B, ITGB3 (Glanzmann thrombasthenia); GP1BA, GP1BB, GP9 (Bernard-Soulier). Functional readouts: LTA, CD41/CD61 & CD42 flow cytometry, clot retraction, PFA closure time.

### 1.3 Tools to orchestrate (consumed via adapters; never hard dependencies)

| Tool | URL | Role · evidence |
|---|---|---|
| Exomiser | https://github.com/exomiser/Exomiser | Phenotype-driven candidate prioritization (belief state) |
| AI-MARRVEL | https://ai.marrvel.org · code on GitHub/Zenodo | Gene prioritization (belief state) |
| autoPVS1 | https://github.com/JiguangPeng/autopvs1 (web: autopvs1.genetics.bgi.com) | **PVS1** strength (null variants; ClinGen SVI decision tree) |
| AutoPM3 | bioRxiv 2024 / Bioinformatics (PMC12263107) | **PM3** evidence extraction from literature (LLM+RAG) |
| Pangolin | https://github.com/tkzeng/Pangolin | Splice scoring |
| VEP | https://github.com/Ensembl/ensembl-vep | Annotation, HGVS, consequence (needed by autoPVS1) |

### 1.4 Validation cohorts

| Cohort | URL / archive | Access | Use |
|---|---|---|---|
| ClinGen eRepo | erepo.clinicalgenome.org | Public, immediate | Classification ground truth incl. bleeding genes |
| EAHAD / LOVD bleeding DBs | §1.2 | Public, immediate | Domain variant truth + phenotype/functional context |
| Solve-RD / RD-Connect GPAP | https://solve-rd.eu · https://rd-connect.eu | **Managed access** (Data Access Committee; EGA-archived) — multi-month | Retrospective *diagnostic journey* (action→resolution) |
| Undiagnosed Diseases Network (UDN) | https://undiagnosed.hms.harvard.edu · dbGaP | **Managed access** (dbGaP application) | Retrospective journeys |
| Simulation harness (built in-house) | this repo | Open | Controlled odysseys with known resolution paths |

> **Sequencing note on cohorts:** managed-access cohorts (Solve-RD, UDN) have long approval timelines, so they are *not* on the v1 critical path. The immediately-available public sources (eRepo + EAHAD/LOVD + simulation) carry the primary v1 results; managed cohorts are added as they clear, strengthening external validity.

---

## 2. Software environment & repository layout

Leaner than the prior plan — no quantum/JAX, no GPU hard requirement (only the optional literature-mining LLM and any local embedding model want a GPU).

### 2.1 Environment (`environment.yml`, pinned; re-verify at execution)

```yaml
name: omnivar-nav
channels: [conda-forge, bioconda]
dependencies:
  - python=3.11
  - numpy, scipy, pandas
  - scikit-learn          # calibration, ancestry classifier, baselines
  - cyvcf2, pysam, htslib  # VCF/variant I/O
  - pyhpo                  # HPO semantic similarity (PP4)
  - requests, httpx        # gnomAD/ClinVar/MaveDB/eRepo APIs
  - matplotlib, seaborn    # figures
  - pydantic               # schemas/validation
  - fastapi, uvicorn       # service
  - pytest, ruff, black    # test/lint
  - pip:
    - mavedb               # MaveDB API client
    - pangolin             # splice scoring (SpliceAI replacement)
    - somalier             # or peddy — ancestry/relatedness from VCF
    # external tools (autoPVS1, AutoPM3, Exomiser, VEP) installed separately, wrapped via adapters
```

### 2.2 Repository tree

```
omnivar-navigator/
├── core/                # schemas, adapter ABC, audit ledger
│   ├── schemas.py       # Variant, PatientContext, EvidenceContribution, PointsLedger, ...
│   ├── adapter.py       # EvidenceAdapter ABC (the swappability contract)
│   └── audit.py         # hash-chained immutable log
├── rules/               # deterministic classification
│   ├── point_engine.py  # points → classification (Tavtigian/ClinGen)
│   ├── posterior.py     # points → posterior probability (Bayesian)
│   ├── vcep_loader.py   # load CSpec specs
│   └── specs/           # F8.yaml, F9.yaml, VWF.yaml, ITGA2B.yaml, ...
├── adapters/            # one per evidence code/group (the "sources" in action)
│   ├── gnomad.py        # PM2/BS1/BA1
│   ├── insilico.py      # PP3/BP4 (calibrated)
│   ├── splice.py        # PP3/BP4/BP7 + RNA-PVS1 context (Pangolin)
│   ├── autopvs1.py      # PVS1
│   ├── litmine_pm3.py   # PM3 (AutoPM3)
│   ├── clinvar.py       # PS1/PM5
│   ├── mave.py          # PS3/BS3 (MaveDB)
│   ├── phenotype.py     # PP4 (HPO/Resnik)
│   └── prioritizer.py   # Exomiser / AI-MARRVEL belief state
├── engine/              # the novel core
│   ├── gap.py           # evidence-gap analysis
│   ├── action_map.py    # code → real-world action
│   ├── action_catalog/  # bleeding.yaml, epilepsy.yaml, cancer.yaml
│   ├── voi.py           # value-of-information ranking
│   ├── recommend.py     # recommendation assembly
│   ├── case_policy.py   # whole-odyssey (cross-modality) layer
│   └── odyssey_actions.py
├── equity/
│   ├── ancestry.py      # genetic-similarity inference
│   ├── reliability.py   # evidence-reliability flags
│   ├── routing.py       # equitable-evidence routing
│   └── dashboard.py
├── learn/
│   ├── outcome_store.py
│   └── prior_update.py
├── sim/odyssey_sim.py   # parametric simulator
├── eval/                # ablation.py, retrospective.py, calibration.py, equity_eval.py, stats.py
├── llm/                 # gateway.py (Ollama/Qwen + Nemotron router), rag/ (retrieval for PM3/PS1)
├── ui/                  # geneticist review frontend (served from the VM in production)
├── api/main.py          # FastAPI backend (engine endpoints)
├── deploy/              # remote.py (paramiko, key-auth), compose.vm.yml, Caddyfile (TLS), .env.example
├── docker/              # Dockerfile.api, Dockerfile.worker, Dockerfile.tools (VEP/autoPVS1/Pangolin/...)
├── data/sources/        # download/cache scripts + manifest.json (versions, checksums)
├── tests/
├── .github/workflows/   # ci.yml (test+lint), release.yml (build+push images → GHCR, mint Zenodo DOI)
├── environment.yml, docker-compose.yml, pyproject.toml
└── Makefile, README.md, CITATION.cff
```

### 2.3 CI / reproducibility

`pytest` + `ruff`/`black` in GitHub Actions; `data/manifest.json` records every source version + checksum; adapter **contract tests** guarantee any tool is swappable without touching the engine.

### 2.4 Compute topology & local↔VM workflow

Two machines, a strict division of labor, and a **Docker-only rule on the server** — no `apt`/`pip` on the host; every process runs in a container, for resource isolation and environment consistency.

| | Laptop (dev) | VM `sjt418scope025` (compute + host) |
|---|---|---|
| Spec | 2.5 GHz, 8 GB RAM | 24 cores, 64 GB RAM, 1 TB, 16 GB GPU, Ubuntu 22.04 |
| Role | write code, lint, unit tests on tiny fixtures, git, author Docker*files* | all heavy work: full data, feature extraction, LLM inference, validation runs, **and hosting the web app** |
| Never | run full pipelines, load LLMs, hold real data | install software on the host (Docker images only) |

**Workflow:** (1) develop + unit-test locally on small fixtures, push to GitHub; (2) on the VM, pull the repo and run everything via `docker compose` (images built on the VM or pulled from GHCR); (3) automate VM control from the laptop with **paramiko/Fabric** over SSH — using **key-based auth**, never an in-code password.

**Security (do this first):** rotate the shared password, add your SSH *public* key to the VM (`~/.ssh/authorized_keys`), and connect with the key via the SSH agent. The deploy toolkit reads host/user from environment variables; no secret ever lives in code, images, or git.

`deploy/remote.py` (paramiko helper — key auth, no secrets in code):
```python
import os, paramiko
def vm() -> paramiko.SSHClient:
    c = paramiko.SSHClient(); c.load_system_host_keys()
    c.connect(hostname=os.environ["VM_HOST"], port=int(os.environ.get("VM_PORT", "22")),
              username=os.environ["VM_USER"])          # uses SSH agent / default key
    return c
def run(cmd: str) -> tuple[str, str]:
    _, out, err = vm().exec_command(cmd)
    return out.read().decode(), err.read().decode()
# e.g. run("cd ~/omnivar-navigator && docker compose -f deploy/compose.vm.yml up -d --build")
```
Use `rsync`/`scp` for data sync; reserve paramiko for orchestration (build, up/down, logs, launch validation jobs).

**Docker-only build note:** because nothing may be installed on the host, all external tools (VEP, autoPVS1, AutoPM3, Exomiser, Pangolin, somalier) are baked into service images (`docker/Dockerfile.tools`). Heavy reference data (gnomAD slices, VEP cache, CADD) live on the 1 TB disk and are bind-mounted **read-only** into containers. The `environment.yml` defines the laptop dev env *and* the contents of the API image — one source of truth.

### 2.5 LLM integration (self-hosted, reproducible)

The VM already runs **Ollama (Qwen)** and **Nvidia Nemotron** — this becomes the project's LLM layer and removes the earlier proprietary-API reproducibility risk (no DeepSeek/OpenAI dependency). The LLM is used **only for soft tasks**; it never produces the classification or the points.

| Task | Module | Model (routed via gateway) | Grounding |
|---|---|---|---|
| Notes → HPO | `adapters/phenotype.py` | Qwen (fast) | output validated against the HPO ontology |
| Literature → PM3/PS1/PS4 | `adapters/litmine_pm3.py` | Nemotron (reasoning) + RAG | citations required; **rule engine assigns points** |
| Recommendation explanation | `engine/recommend.py` | Qwen | templated from the deterministic ledger/plan |

**Gateway pattern** — abstract the model behind one OpenAI-compatible interface (Ollama already exposes `/v1`), so models are swappable and tasks routed:
```python
# llm/gateway.py
import os
from openai import OpenAI
_client = OpenAI(base_url=os.environ.get("OLLAMA_URL", "http://ollama:11434/v1"),
                 api_key="ollama")                       # Ollama ignores the key
ROUTES = {"fast": "qwen2.5:7b", "reason": "nemotron-mini"}   # choose builds that fit 16 GB GPU
def complete(task: str, prompt: str, **kw) -> str:
    return _client.chat.completions.create(
        model=ROUTES[task], messages=[{"role": "user", "content": prompt}], **kw
    ).choices[0].message.content
```
**16 GB GPU constraint:** load one model at a time (Ollama swaps on demand); use quantized 7–14 B variants; verify the specific Qwen/Nemotron builds that fit 16 GB at execution (heavier Nemotron variants that exceed 16 GB are out of scope for on-VM inference). **Guardrails:** every LLM call is logged to the audit ledger with model+version; RAG answers must carry citations; the rule engine — not the LLM — decides classification.

---

## 3. Core data model (`core/schemas.py`)

Defined once; used by every phase.

```python
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

class Strength(Enum):           # signed points (Tavtigian naturally-scaled)
    PVS = 8; PS = 4; PM = 2; PP = 1
    BP = -1; BM = -2; BS = -4; BVS = -8

class Classification(Enum):
    P = "Pathogenic"; LP = "Likely pathogenic"; VUS = "Uncertain"
    LB = "Likely benign"; B = "Benign"

@dataclass(frozen=True)
class Variant:
    chrom: str; pos: int; ref: str; alt: str
    gene: str; hgvs_c: Optional[str] = None; hgvs_p: Optional[str] = None
    build: str = "GRCh38"; transcript: Optional[str] = None

@dataclass
class PatientContext:
    hpo_terms: list[str] = field(default_factory=list)
    ancestry_group: Optional[str] = None          # inferred (equity module)
    ancestry_confidence: float = 0.0
    parents_available: bool = False
    informative_family: bool = False              # for segregation (PP1/BS4)
    existing_assays: dict = field(default_factory=dict)   # already-done results
    sex: Optional[str] = None

@dataclass
class EvidenceContribution:
    code: str                  # e.g. "PS3", "PM2", "PP3"
    strength: Strength
    applied: bool              # True = currently met; False = a potential opportunity
    source: str                # provenance: which adapter/DB/version
    reliability: float = 1.0   # equity down-weighting (0..1)
    rationale: str = ""

@dataclass
class PointsLedger:
    variant: Variant
    contributions: list[EvidenceContribution] = field(default_factory=list)
    spec_version: str = ""
    @property
    def points(self) -> float:
        return sum(c.strength.value * c.reliability
                   for c in self.contributions if c.applied)

@dataclass
class CodeOpportunity:           # an attainable, not-yet-met code
    code: str; strength_if_pos: Strength
    delta_points: float
    prerequisites: list[str]     # e.g. ["parents_available"]
    rationale: str

@dataclass
class Action:                    # a real-world orderable test/assay/modality
    name: str; yields_codes: list[str]
    cost_usd: float; turnaround_days: int
    sensitivity: float; specificity: float   # priors (literature → learning loop)
    modality: str

@dataclass
class RankedPlan:
    actions: list[tuple[Action, float]]      # (action, value_per_cost)
    explanation: str
    current_class: Classification
    current_posterior: float
```

---

## PART II — PHASED PLAN (detailed)

### Phase 0 — Foundations & rule engine (Months 1–3)

#### Step 0.1 — Reproducibility & adapter contract
- **Objective:** Vendor-neutral, swappable foundation.
- **Goal:** CI green; an `EvidenceAdapter` ABC with passing contract tests; one mock adapter.
- **Sources:** none (infra).
- **Methods:** Define the adapter contract so every external tool is replaceable; container + CI.
- **Code/artifacts:** `core/adapter.py`:
  ```python
  from abc import ABC, abstractmethod
  class EvidenceAdapter(ABC):
      code_group: tuple[str, ...]                      # e.g. ("PM2","BS1","BA1")
      version: str
      @abstractmethod
      def evaluate(self, v: Variant, p: PatientContext) -> list[EvidenceContribution]: ...
      @abstractmethod
      def health_check(self) -> bool: ...              # source reachable / data present
  ```
- **Expected outcome:** `make test` passes; mock adapter satisfies the contract.

#### Step 0.2 — Deterministic rule engine (points → classification)
- **Objective:** Reproducible classification from evidence codes.
- **Goal:** Reproduce ClinGen eRepo calls on a held-out bleeding-gene set at high concordance; output always carries points + applied codes + spec version.
- **Sources:** Tavtigian 2018/2020 framework; ClinGen CSpec gene specs (F8/F9/VWF).
- **Methods:** Sum signed points (with equity reliability weighting); apply Tavtigian bands; **BA1 is a pre-filter** (excluded from the sum, per ClinGen). Bands (§A.1): P ≥ 10; LP 6–9; VUS 0–5; LB −1…−6; B ≤ −7.
- **Code/artifacts:** `rules/point_engine.py`:
  ```python
  BANDS = [(10, Classification.P), (6, Classification.LP),
           (0, Classification.VUS), (-6, Classification.LB)]  # else B
  def classify(ledger: PointsLedger, spec: "VCEPSpec") -> Classification:
      if spec.ba1_met(ledger):                      # standalone benign pre-filter
          return Classification.B
      pts = ledger.points
      for threshold, cls in BANDS:
          if pts >= threshold:
              return cls
      return Classification.B
  ```
  `rules/vcep_loader.py` parses CSpec specs into a `VCEPSpec` (per-code strength overrides, AF thresholds, prior_P). Specs stored as versioned YAML in `rules/specs/`.
- **Expected outcome:** Validated classifier; concordance report vs. eRepo bleeding-gene variants.
- **Depends on:** 0.1.

#### Step 0.3 — Points → posterior (Bayesian bridge)
- **Objective:** Convert points to a probability of pathogenicity (needed by VOI).
- **Goal:** `posterior(points)` matches Tavtigian thresholds (P≈0.99 at 10 pts, LP≈0.90 at 6 pts).
- **Sources:** Tavtigian et al. 2018.
- **Methods:** OddsPath = 350^(points/8); Post_P = (OddsPath·prior)/((OddsPath−1)·prior+1), prior_P=0.1 default or gene-specific (§A.2).
- **Code/artifacts:** `rules/posterior.py`:
  ```python
  def posterior(points: float, prior_p: float = 0.10) -> float:
      odds_path = 350.0 ** (points / 8.0)
      return (odds_path * prior_p) / ((odds_path - 1) * prior_p + 1)
  ```
- **Expected outcome:** Unit-tested probability bridge.
- **Depends on:** 0.2.

#### Step 0.4 — Data infrastructure
- **Objective:** Reliable, provenance-logged reference data.
- **Goal:** `make data` produces a verified local store.
- **Sources:** §1.1–§1.2 (gnomAD, ClinVar, eRepo, HPO, CSpec, EAHAD/LOVD, MaveDB).
- **Methods:** Download/adapter scripts with checksums; `manifest.json` (URL, version, date, md5).
- **Code/artifacts:** `data/sources/*.py`, `data/manifest.json`.
- **Expected outcome:** Verified store; provenance log.

---

### Phase 1 — Evidence orchestration (Months 2–5)

Each adapter ties an ACMG code to a concrete source. This is where "sources" become executable.

#### Step 1.1 — gnomAD adapter (PM2 / BS1 / BA1)
- **Objective:** Population-frequency evidence, ancestry-resolved.
- **Goal:** Correct PM2/BS1/BA1 vs. expert curation on a benchmark set, using the gene's VCEP AF thresholds.
- **Sources:** gnomAD v4.1 GraphQL API / GCS.
- **Methods:** Query grpmax filtering AF; compare to VCEP-specified thresholds (e.g., F8 hemizygote rule); record per-ancestry AF and data density for the equity module.
- **Code/artifacts:** `adapters/gnomad.py`:
  ```python
  class GnomadAdapter(EvidenceAdapter):
      code_group = ("PM2", "BS1", "BA1"); version = "v4.1"
      def evaluate(self, v, p):
          af = self._grpmax_faf(v)                 # GraphQL query
          if af is None or af < self.spec.pm2_threshold(v.gene):
              return [EvidenceContribution("PM2", Strength.PP, True, "gnomAD v4.1")]
          if af > self.spec.ba1_threshold(v.gene):
              return [EvidenceContribution("BA1", Strength.BVS, True, "gnomAD v4.1")]
          if af > self.spec.bs1_threshold(v.gene):
              return [EvidenceContribution("BS1", Strength.BS, True, "gnomAD v4.1")]
          return []
  ```
- **Expected outcome:** Frequency codes auto-applied with provenance + per-ancestry data density.

#### Step 1.2 — Calibrated in-silico adapter (PP3 / BP4)
- **Objective:** In-silico evidence *at the correct strength*.
- **Goal:** Apply PP3/BP4 at calibrated strengths (not a flat "Supporting").
- **Sources:** AlphaMissense, REVEL/BayesDel/VEST4 (dbNSFP); Pejaver et al. 2022 thresholds (§A.3).
- **Methods:** Pick one predefined tool per VCEP rule; map score → strength via calibrated thresholds (e.g., REVEL ≥ 0.932 → Strong). Consistency: a single tool defined in advance, per ClinGen PP3/BP4 guidance.
- **Code/artifacts:** `adapters/insilico.py` with a `THRESHOLDS` table (§A.3).
- **Expected outcome:** Strength-calibrated PP3/BP4.

#### Step 1.3 — Splice adapter (PP3 / BP4 / BP7 + RNA-PVS1 context)
- **Sources:** Pangolin (SpliceAI replacement).
- **Methods:** Score splice impact vs. VCEP cutoffs; flag candidates where an **RNA assay** would yield PS3-splice (key for the synonymous-ITGB3-class case).
- **Code/artifacts:** `adapters/splice.py`.
- **Expected outcome:** Splice codes + an "RNA-resolvable" flag for the gap engine.

#### Step 1.4 — autoPVS1 adapter (PVS1)
- **Sources:** github.com/JiguangPeng/autopvs1 (+ VEP cache).
- **Methods:** Wrap autoPVS1 (Python import or subprocess) to get PVS1 strength per the ClinGen SVI null-variant decision tree; honor gene-specific overrides where a VCEP defines them.
- **Code/artifacts:** `adapters/autopvs1.py`:
  ```python
  from autopvs1 import AutoPVS1
  class AutoPVS1Adapter(EvidenceAdapter):
      code_group = ("PVS1",); version = "JiguangPeng@master"
      def evaluate(self, v, p):
          r = AutoPVS1(f"{v.chrom}-{v.pos}-{v.ref}-{v.alt}", v.build.lower())
          if not r.islof: return []
          strength = {"Very Strong": Strength.PVS, "Strong": Strength.PS,
                      "Moderate": Strength.PM, "Supporting": Strength.PP}[r.strength_raw]
          return [EvidenceContribution("PVS1", strength, True, "autoPVS1", rationale=r.criterion)]
  ```
- **Expected outcome:** PVS1 strength auto-assigned for null variants.

#### Step 1.5 — Literature-mining adapter (PM3 / PS1 / PS4)
- **Sources:** AutoPM3 (LLM+RAG); ClinVar; PubTator.
- **Methods:** AutoPM3 for PM3 (in-trans with pathogenic). RAG over literature for PS1 (same AA change known pathogenic) and PS4 (case enrichment). **All LLM output is a *proposal*; the rule engine assigns points** — never the LLM.
- **Code/artifacts:** `adapters/litmine_pm3.py`, `adapters/clinvar.py`.
- **Expected outcome:** Literature-derived codes with citations; per-code precision/recall reported.

#### Step 1.6 — Functional (MAVE) adapter (PS3 / BS3)
- **Sources:** MaveDB (`pip install mavedb`, REST/CSV).
- **Methods:** Look up the variant in any score set for the gene; map the functional score → strength via OddsPath calibration (Brnich et al. 2020). If saturation data exists (e.g., for a covered gene), this can resolve directly.
- **Code/artifacts:** `adapters/mave.py`.
- **Expected outcome:** Functional codes where MAVE data exist; "MAVE-available" flag for the gap engine.

#### Step 1.7 — Phenotype adapter (PP4)
- **Sources:** HPO; gene-disease HPO annotations; VWD/EAHAD phenotype data.
- **Methods:** Resnik/semantic similarity between patient HPO and gene-disease profile; apply PP4 at the VCEP-specified strength (recent guidance allows up to +5 points; subtype-specific for VWD).
- **Code/artifacts:** `adapters/phenotype.py` (uses `pyhpo`).
- **Expected outcome:** PP4 with subtype awareness (e.g., VWD type 2N).

#### Step 1.8 — Prioritizer adapter (belief state)
- **Sources:** Exomiser, AI-MARRVEL.
- **Methods:** Normalize outputs to a `CandidateSet`; record cross-tool disagreement (→ human-review flag).
- **Code/artifacts:** `adapters/prioritizer.py`.
- **Expected outcome:** Ranked candidates, each with an attached, auto-assembled ledger.
- **Phase-1 acceptance:** End-to-end: VCF + HPO → candidates each with a rule-grounded `PointsLedger`; per-code precision/recall vs. expert curation reported on a bleeding benchmark.

---

### Phase 2 — Decision & orchestration engine (the novel core) (Months 4–8)

#### Step 2.1 — Evidence-gap analysis
- **Objective:** Quantify the points gap and what can close it.
- **Goal:** For each VUS, a list of *attainable* missing codes with Δpoints and prerequisites.
- **Sources:** the ledger (Phase 1) + VCEP spec + `PatientContext`.
- **Methods:** For each code not currently applied, test attainability against biology + patient context (PS2 only if `parents_available`; PS3-splice only if splice-region/RNA-resolvable; PP1 only if `informative_family`; PS3-functional only if an assay exists for the gene). Δpoints = the strength the code would contribute under the spec.
- **Code/artifacts:** `engine/gap.py`:
  ```python
  def attainable_codes(ledger, spec, patient) -> list[CodeOpportunity]:
      out = []
      applied = {c.code for c in ledger.contributions if c.applied}
      for code, rule in spec.codes.items():
          if code in applied: continue
          ok, prereqs = rule.attainable(ledger, patient)     # context-aware test
          if ok:
              out.append(CodeOpportunity(code, rule.strength,
                          rule.strength.value, prereqs, rule.describe()))
      return out

  def gap_to_target(ledger, spec, target=Classification.LP) -> float:
      return spec.threshold(target) - ledger.points          # points still needed
  ```
- **Expected outcome:** Per-VUS "what would move it and by how much," consistent with ClinGen's functional-evidence-potential logic.
- **Depends on:** Phase 1, 0.2–0.3.

#### Step 2.2 — Code → action mapping (domain catalog)
- **Objective:** Translate code opportunities into orderable real-world actions.
- **Goal:** Each opportunity → ≥1 concrete action with cost/turnaround/sensitivity priors.
- **Sources:** ISTH/EAHAD assay descriptions; literature priors; (later) the learning loop.
- **Methods:** A versioned domain pack. Bleeding pack maps, e.g.:
  - PS3 → {factor activity assay, VWF:FVIII binding, VWF multimers, ristocetin cofactor, LTA, CD41/CD61 flow cytometry, clot retraction, thrombin generation}
  - PS3-splice → {RNA-seq, RT-PCR, minigene}
  - PS2 → {parental/trio testing}; PP1 → {family segregation study}
  - whole-modality → {long-read genome, optical genome mapping, methylation}
- **Code/artifacts:** `engine/action_catalog/bleeding.yaml` (each action: yields_codes, cost_usd, turnaround_days, sensitivity, specificity, modality), loaded by `engine/action_map.py`.

  ```yaml
  # engine/action_catalog/bleeding.yaml (excerpt; priors to be calibrated)
  vwf_fviii_binding:   {yields: [PS3, BS3], cost_usd: 600,  days: 14, sens: 0.85, spec: 0.90, modality: functional}
  rna_seq_splice:      {yields: [PS3, BS3], cost_usd: 900,  days: 28, sens: 0.78, spec: 0.92, modality: rna}
  flow_cd41_cd61:      {yields: [PS3],      cost_usd: 450,  days: 7,  sens: 0.88, spec: 0.90, modality: functional}  # Glanzmann
  trio_testing:        {yields: [PS2],      cost_usd: 1200, days: 21, sens: 0.72, spec: 0.99, modality: segregation}
  ```
  > Sensitivity/specificity here are **initial literature-seeded priors**, explicitly versioned and updated per-institution by the learning loop (Phase 5.2). They are not asserted as final values.
- **Expected outcome:** A populated, versioned action catalog for bleeding (epilepsy/cancer packs in Phase 7).

#### Step 2.3 — Value-of-information ranking & recommendation
- **Objective:** Recommend the best next action.
- **Goal:** Rank actions by expected information gain (or expected probability of reaching a confident call) per dollar/week; output an explained recommendation with the *expected post-action classification*; beat greedy/random in simulation.
- **Sources:** posterior bridge (0.3); action catalog (2.2); assay priors.
- **Methods (full derivation in §A.4):** From current points → posterior `p`. For action `a` yielding `+k` points if positive / `−k'` if negative, with sensitivity/specificity, compute predictive `P(positive)`, the two branch posteriors, and **EIG = H(p) − E[H(p')]** (Bernoulli entropy), plus a decision-utility `E[ΔU]` = expected gain in P(reaching an actionable call). Rank by value-per-cost with a cost scalarization `cost = α·$ + β·weeks`.
- **Code/artifacts:** `engine/voi.py`:
  ```python
  import numpy as np
  from rules.posterior import posterior
  def _H(p): return 0.0 if p in (0,1) else -(p*np.log2(p)+(1-p)*np.log2(1-p))

  def expected_info_gain(points, action: Action, prior_p=0.10) -> float:
      p = posterior(points, prior_p)
      k_pos = Strength.PS.value         # e.g., functional positive → PS3 (+4)
      k_neg = Strength.BS.value         # functional negative → BS3 (−4)
      q = action.sensitivity*p + (1-action.specificity)*(1-p)   # P(positive result)
      p_pos = posterior(points + k_pos, prior_p)
      p_neg = posterior(points + k_neg, prior_p)
      return _H(p) - (q*_H(p_pos) + (1-q)*_H(p_neg))

  def value_per_cost(points, a: Action, alpha=1.0, beta=50.0) -> float:
      eig = expected_info_gain(points, a)
      return eig / (alpha*a.cost_usd + beta*a.turnaround_days/7.0)

  def rank_actions(points, actions, **kw):
      scored = sorted(((a, value_per_cost(points, a, **kw)) for a in actions),
                      key=lambda t: t[1], reverse=True)
      return scored
  ```
  `engine/recommend.py` assembles the human-readable output: *"Recommended: VWF:FVIII binding (~$600, ~2 wks) → expected PS3 (+4) → posterior 0.91 → Likely Pathogenic; alternative: family segregation (PP1)."*
- **Expected outcome:** Ranked, explained, calibrated recommendation per case; simulation shows superiority over greedy/random baselines.
- **Depends on:** 2.1, 2.2, 0.3.

---

### Phase 3 — Equity module (Months 6–9)

#### Step 3.1 — Ancestry inference + evidence-reliability flags
- **Objective:** Make the engine ancestry-aware.
- **Goal:** Infer genetic-similarity group from VCF; flag/down-weight PM2/PP3 reliability where reference data are sparse.
- **Sources:** gnomAD per-ancestry AFs + data density; reference PC panel; `somalier`/`peddy`.
- **Methods:** Project sample onto reference PCs → similarity group + confidence. Reliability `r∈[0,1]` for PM2/PP3 as a function of group-specific reference N and predictor training composition; `r` multiplies the contribution's effective points in the ledger (already wired via `EvidenceContribution.reliability`).
- **Code/artifacts:** `equity/ancestry.py`, `equity/reliability.py`:
  ```python
  def reliability_pm2(gene, group, gnomad_group_n) -> float:
      # sparse reference data for this group → lower reliability of an "absent/rare" call
      return float(np.clip(np.log10(gnomad_group_n + 1) / 5.0, 0.3, 1.0))
  ```
- **Expected outcome:** Per-variant reliability annotations; documented behavior on under-represented-ancestry test cases.

#### Step 3.2 — Equitable-evidence routing + reporting
- **Objective:** Reduce ancestry disparities in resolution.
- **Goal:** Bias recommendations toward ancestry-robust evidence; equity dashboards.
- **Methods:** In VOI, apply a penalty to actions whose only yield is a low-reliability code, and a preference for functional/segregation actions (ancestry-equitable). Cohort metric: gap in resolution rate across groups.
- **Code/artifacts:** `equity/routing.py`, `equity/dashboard.py`.
- **Expected outcome:** Narrower resolution-rate gap vs. the non-equity-aware configuration (measured in §6).

---

### Phase 4 — Whole-odyssey (cross-modality) layer (Months 8–11)

#### Step 4.1 — Case-level state & modality escalation
- **Objective:** Lift from single-variant to whole-case decisions.
- **Goal:** Recommend the optimal next *modality* (RNA-seq, long-read GS, optical mapping, methylation, proteomics), reanalysis timing, or matchmaking — across the case.
- **Sources:** the per-variant ledgers + case context; conditional-yield priors from the multimodal-escalation literature.
- **Methods:** A case policy over the modality action space, routed by failure mode: *interpretation* failure (VUS in candidate) → variant-level VOI (Phase 2); *detection* failure (no candidate / missing second hit / hard region) → modality escalation (long-read/optical → new variants; RNA → expression/splicing; methylation → imprinting). Reanalysis modeled as a low-cost "wait" action with a knowledge-growth prior; matchmaking as an action for novel-gene candidates.
- **Code/artifacts:** `engine/case_policy.py`, `engine/odyssey_actions.py`.
- **Expected outcome:** A ranked whole-workup plan per unsolved case; validated on retrospective journeys (§6).

---

### Phase 5 — UI, audit & learning loop (Months 9–13)

#### Step 5.1 — Reasoning-trace review UI
- **Objective:** Clinician-facing decision support.
- **Goal:** Show ledger + gap + ranked recommendations + provenance; capture accept/override.
- **Sources:** engine outputs; audit ledger.
- **Methods:** Lightweight web UI (build per `frontend-design` skill when implemented); every element links to its source + VCEP rule version; immutable hash-chained audit log.
- **Code/artifacts:** `ui/`, `api/main.py`, `core/audit.py`.
- **Expected outcome:** A geneticist reviews a case, sees *why* it's a VUS and the cheapest path out, accepts/overrides — all logged.

#### Step 5.2 — Verifiable learning loop
- **Objective:** Improve from use, auditably.
- **Goal:** Feed accept/override + realized assay outcomes back into cost/yield/attainability priors; show measurable, attributable improvement.
- **Methods:** Outcome store; per-institution Bayesian updating of action priors (Beta posteriors on assay sensitivity per gene/assay); the verdict logic is **never** opaquely retrained — only the priors update, and each update is attributable to specific cases.
- **Code/artifacts:** `learn/outcome_store.py`, `learn/prior_update.py`:
  ```python
  def update_sensitivity(prior_alpha, prior_beta, resolved: bool):
      # Beta-Bernoulli update of an assay's sensitivity prior
      return (prior_alpha + resolved, prior_beta + (not resolved))
  ```
- **Expected outcome:** Demonstrable, auditable improvement as outcomes accumulate (simulation + retrospective).

---

### Phase 6 — Validation (Months 11–15)

#### Step 6.1 — Core ablation (headline)
- **Objective:** Prove the decision layer's added value.
- **Goal:** Full system vs. the same underlying tools *without* the decision layer, on identical cohorts.
- **Sources:** eRepo + EAHAD/LOVD bleeding variants; simulation; (as available) Solve-RD/UDN.
- **Methods:** Paired comparison; metrics = VUS resolution rate, Δpoints, cost/time per resolved case, concordance with VCEP truth. Stats (§A.5): McNemar (paired resolution), Wilcoxon signed-rank (cost/time), DeLong (AUC), bootstrap CIs, Bonferroni across the ablation set. **Pre-register before running.**
- **Code/artifacts:** `eval/ablation.py`, `eval/stats.py`.
- **Expected outcome:** Pre-registered, honest result (including negatives) on whether the layer improves resolution/cost.

#### Step 6.2 — Retrospective journeys + simulation + calibration/equity
- **Objective:** External + stress validation.
- **Goal:** Recommended vs. actually-resolving action concordance (retrospective); beat greedy/random (simulation); calibrated confidence; reduced equity gap.
- **Sources:** Solve-RD/RD-Connect GPAP, UDN (as access clears); `sim/odyssey_sim.py`.
- **Methods:** Journey replay (does the engine's #1 action match what resolved the case, at lower predicted cost?); simulator sweeps; reliability diagram + ECE (§A.5); ancestry-stratified resolution-gap with CIs.
- **Code/artifacts:** `eval/retrospective.py`, `sim/odyssey_sim.py`, `eval/calibration.py`, `eval/equity_eval.py`.
- **Expected outcome:** Concordance with real resolving actions; baseline superiority in simulation; good calibration; reduced equity gap.

---

### Phase 7 — Domain expansion (Months 13–16)

- **Objective / Goal:** Prove domain-agnosticism — same engine, new packs only.
- **Sources:** ClinGen VCEP specs + assay catalogs for epilepsy (SCN1A/2A, KCNQ2, CACNA1A, STXBP1; ion-channel/patch-clamp functional data) and cancer predisposition (BRCA1/2, MMR/Lynch, TP53, PTEN, CDH1 — **MAVE-rich**, ideal for functional routing + equity).
- **Methods:** Add `rules/specs/*` + `engine/action_catalog/{epilepsy,cancer}.yaml` + phenotype maps; **no core changes**.
- **Code/artifacts:** the new pack files.
- **Expected outcome:** Valid plans in new domains via pack additions only — the key generalization claim, with the cancer pack showcasing MAVE-based PS3 routing.

---

### Phase 8 — Manuscript, GitHub & Zenodo release (Months 14–18)

- **Objective / Goal:** Peer-reviewed publication + an open, reproducible, *runnable* release.
- **Targets:** npj Genomic Medicine (primary); Genetics in Medicine / Genome Medicine (secondary); bioRxiv/medRxiv preprint; OSF pre-registration; Zenodo via the **GitHub–Zenodo integration** (a GitHub Release auto-mints a DOI).
- **Methods (release engineering):**
  - **CI/CD** (`.github/workflows/`): `ci.yml` runs tests+lint on every push; `release.yml` builds the service Docker images and pushes them to **GHCR** (GitHub Container Registry) tagged by version — so anyone can `docker compose up` and reproduce without manual setup.
  - **Reproducibility bundle:** pinned `environment.yml` + Dockerfiles + `data/manifest.json` (source versions/checksums) + the seeded simulator + the LLM model-config (which Qwen/Nemotron build + quantization).
  - **Zenodo deposits:** (1) code snapshot (auto via Release); (2) simulator + seeded synthetic odysseys (CC0, no patient data); (3) trained priors/weights + benchmark results (JSON/CSV). DOIs cited in the paper's Data/Code Availability.
  - **Manuscript:** lock skeleton + claims-map before the headline ablation; programmatic 300-dpi figures; the hosted demo and one-command Docker reproduction are themselves selling points to reviewers.
- **Code/artifacts:** `manuscript/{outline,claims_map}.md`, `figures/generate_all.py`, `CITATION.cff`, `.github/workflows/release.yml`.
- **Expected outcome:** Journal submission + preprint; public repo with CI badges; Zenodo DOIs; a release anyone can run. **No real patient data in any public artifact.**

---

### Phase 9 — Web application, LLM service & hosting (Months 15–18, overlaps P8)

- **Objective:** A deployable web app, served from the VM, that a geneticist/MDT uses through a browser, with the self-hosted LLM integrated.
- **Goal:** `docker compose -f deploy/compose.vm.yml up -d` on the VM brings up the full stack; a user reaches the review UI, submits a case (VCF + HPO), and gets the rule-grounded ledger + ranked next-action recommendation + LLM-written explanation, all audited.
- **Sources / components:** the engine (Phases 1–5); the existing Ollama (Qwen) + Nemotron on the VM; the containerized tool images (Phases 0/8).
- **Methods (stack — all Docker on the VM):**
  - `api` — FastAPI engine endpoints (`/classify`, `/recommend`, `/case`).
  - `ui` — the geneticist review frontend (Phase 5), now served in production.
  - `llm-gateway` → `ollama` — the LLM layer (§2.5), GPU-attached (`deploy.resources … gpus`).
  - `worker` — async long jobs (batch validation, reanalysis sweeps).
  - `db` (Postgres) — outcome store + hash-chained audit ledger; `vectorstore` (Qdrant/Chroma) — RAG + case memory.
  - `proxy` (Caddy) — TLS + routing + authentication in front of everything.
  - **`deploy/compose.vm.yml`** wires these; GPU attached only to `ollama`; reference data bind-mounted read-only.
- **Access & safety:**
  - The VM has a private IP (10.30.x.x). For dev, reach the UI via an **SSH tunnel** (`ssh -L 8443:localhost:443 …`); for broader internal use, expose through the Caddy proxy with authentication on the institutional network.
  - **The public/shareable demo uses synthetic + public data only** — never real patient data — keeping the hosted demo clear of privacy/regulatory constraints. Real-case use stays inside the institution behind auth, with **no PHI written to logs**.
  - This remains **decision support**: the UI always shows the evidence basis and requires human sign-off; nothing is auto-actioned.
- **Code/artifacts:** `deploy/compose.vm.yml`, `deploy/Caddyfile`, `deploy/remote.py`, `api/main.py`, `ui/`, `llm/gateway.py`.
- **Expected outcome:** A running, authenticated web app on the VM; a public synthetic-data demo; one-command bring-up; LLM-assisted explanations grounded in the deterministic engine.

---

## Roadmap & gates

```
Month:        1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18
P0 Foundations/rules  [=====]
P1 Orchestration         [======]
P2 Decision core             [=========]
P3 Equity                        [======]
P4 Whole-odyssey                    [======]
P5 UI+audit+learning                   [=======]
P6 Validation                              [=======]
P7 Domain expansion                            [=====]
P8 Manuscript+GitHub+Zenodo                       [=======]
P9 Web app + LLM + hosting                           [=====]
```

**Gates:** (G1) rule engine reproduces eRepo before adapters are trusted; (G2) Phase-1 ledger auto-assembly validated before the decision core; (G3) **ablation config locked before any external benchmarking**; (G4) pre-registration filed before the headline run; (G5) **no real patient data in any public/hosted artifact — the public demo runs on synthetic data only**; (G6) server is **Docker-only**, secrets via env/SSH-agent (no passwords in code or images).

---

## Appendix A — Methods (the math)

### A.1 Point bands (Tavtigian 2020, naturally-scaled)
Combined points C → class: **P** C≥10 · **LP** 6≤C≤9 · **VUS** 0≤C≤5 · **LB** −6≤C≤−1 · **B** C≤−7. Strengths: PVS/PS/PM/PP = +8/+4/+2/+1; benign mirror = −8/−4/−2/−1. PP4 may reach +5 under recent ClinGen guidance. BA1 is a standalone pre-filter, excluded from the sum.

### A.2 Points → posterior (Tavtigian 2018)
OddsPath_total = 350^(C/8); Post_P = (OddsPath·Prior_P)/((OddsPath−1)·Prior_P + 1), Prior_P=0.10 default (gene/VCEP-specific where defined). Check: C=10→Post_P≈0.99; C=6→≈0.90; C=0→0.10; C=−7→<0.001 — matching the class thresholds.

### A.3 Predictor calibration (Pejaver et al. 2022; example REVEL thresholds)
Map a single, predefined predictor's score to ACMG strength via calibrated local posteriors. Example (REVEL): ≥0.932 → PP3_Strong; ≥0.773 → PP3_Moderate; ≥0.644 → PP3_Supporting; ≤0.290 → BP4_Supporting; ≤0.183 → BP4_Moderate; ≤0.016 → BP4_Strong (illustrative — use the published tables, and the 2025 extension, at execution). BayesDel/VEST4/MutPred2 similarly support up to Strong.

### A.4 Value of information (decision core)
Given current points C, prior `p = posterior(C)`. Action `a` yields `+k` points if positive (e.g., PS3=+4) and `−k'` if negative (e.g., BS3=−4), with sensitivity `s=P(pos|path)`, specificity `t=P(neg|benign)`.
- Predictive: `q = s·p + (1−t)·(1−p)`.
- Branch posteriors: `p₊ = posterior(C+k)`, `p₋ = posterior(C−k')`.
- **Expected information gain:** `EIG(a) = H(p) − [q·H(p₊) + (1−q)·H(p₋)]`, with `H` the binary (Bernoulli) entropy.
- **Decision utility:** `U(p)=1` if `p` crosses an actionable band (≥0.90 or ≤0.10), else a graded function; `E[ΔU] = q·U(p₊)+(1−q)·U(p₋) − U(p)`.
- **Ranking:** value-per-cost = `EIG(a) / (α·cost$ + β·weeks)` (or report the cost/EIG Pareto frontier). Functional-assay strengths derive from OddsPath calibration (Brnich et al. 2020): OddsPath ≥18.7→Strong, ≥4.3→Moderate, ≥2.1→Supporting (benign inverse).

### A.5 Validation statistics
- **Resolution (paired binary):** McNemar's test.
- **Cost/time (paired continuous, non-normal):** Wilcoxon signed-rank + Cohen's d (or rank-biserial).
- **AUC (paired):** DeLong's test.
- **Uncertainty:** 95% bootstrap CIs on all point estimates.
- **Calibration:** reliability diagram + Expected Calibration Error (ECE).
- **Equity:** difference in resolution rate across ancestry groups with bootstrap CIs; target = the equity-aware config narrows it.
- **Multiplicity:** Bonferroni across the ablation family (α=0.05 → α_corrected).

---

## Appendix B — Carried over vs. removed

**Carried over (good practice):** pre-registration; lock-before-benchmark; report negatives; pinned/containerized reproducibility; parametric simulator; GitHub + Zenodo. **Removed:** quantum module (deferred); synthetic-only as the *primary* validation (now supplemented by public expert/registry truth + retrospective journeys); fixed-panel framing (now full-odyssey + domain packs).

## Appendix C — Key references (to formalize in manuscript)
Richards et al. 2015 (ACMG/AMP); Tavtigian et al. 2018 (Bayesian framework) & 2020 (point system); Pejaver et al. 2022 + 2025 extension (predictor calibration); Brnich et al. 2020 (PS3/BS3 / OddsPath); Abou Tayoun et al. 2018 (PVS1); Xiang et al. 2020 (AutoPVS1); AutoPM3 2024; Esposito et al. 2019 + MaveDB 2024 (MaveDB); McVey et al. 2020 (EAHAD databases); ClinGen CFD-VCEP (F8/F9), VWD VCEP (VWF), HHT VCEP (ENG/ACVRL1); AI-MARRVEL (NEJM AI 2024); DeepRare (Nature 2026); ancestry/equity-in-classification literature. Full citations at manuscript stage.
