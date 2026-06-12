# OmniVar Navigator — Execution Summary (living document)

**Purpose:** a running record of the *working, methods used, and outcomes* of every
step executed against *OmniVar_Navigator_Detailed_Execution_Plan.md*. Updated as
work proceeds; mirrored to the repo (`docs/`) and pushed to GitHub.

**Repo:** https://github.com/ahmedanees-m/omnivar-navigator · **Author:** Anees Ahmed Mahaboob Ali (`ahmedanees-m`)
**Started:** 2026-06-12 · **Last updated:** 2026-06-12 (all 9 phases code-complete + unit-tested)

**Status legend:** ✅ done · 🟡 in progress · ⏳ queued · ⛔ blocked (external/managed access)

---

## Phase status at a glance

| Phase | Plan months | Status | Notes |
|---|---|---|---|
| **Setup** (infra, repo, data, verification) | — | ✅ | Repo + VM + data parity + source verification complete |
| **P0** Foundations & rule engine | 1–3 | ✅ | Schemas/adapter/audit/posterior/point-engine ✅; **Gate G1 passed** (94.9%); VCEP YAML loader deferred to P1 (AF thresholds) |
| **P1** Evidence orchestration (adapters) | 2–5 | ✅* | All 9 adapters built: gnomAD (live API), ClinVar PS1/PM5 (real index), insilico (calibrated REVEL), splice, autoPVS1, MAVE, litmine, prioritizer. *Tool-backed ones (splice/autoPVS1/MAVE/litmine) use injectable backends pending tool-image wiring on the VM |
| **P2** Decision & orchestration core | 4–8 | ✅ | gap / action_map / VOI / recommend + risk-gate, Pareto, conflict→orthogonal, recessive/X-linked, lookahead, audit — fully matches design doc |
| **P3** Equity module | 6–9 | ✅ | reliability down-weighting + equitable routing + ancestry (nearest-centroid; VCF→PCs via tool image) + dashboards; wired into recommend |
| **P4** Whole-odyssey layer | 8–11 | ✅ | case_policy (interpretation-vs-detection routing; stop/wait/matchmake) + cross-modality catalog |
| **P5** UI, audit, learning loop | 9–13 | ✅* | audit ledger ✅; learning loop (Beta-Bernoulli) ✅; API ✅. *Web UI front-end deferred (build per frontend skill) |
| **P6** Validation | 11–15 | ✅* | simulator + baselines ✅; ablation/calibration/equity-eval/retrospective harnesses ✅; G1 passed. *Real-cohort + managed-access (Solve-RD/UDN) runs pending |
| **P7** Domain expansion (epilepsy, cancer) | 13–16 | ✅ | epilepsy + cancer packs + specs; domain-agnosticism demonstrated (same engine, packs only) |
| **P8** Manuscript + GitHub + Zenodo | 14–18 | ✅* | repo + CI ✅; release.yml (GHCR) ✅; figures + manuscript skeleton + claims-map ✅. *Zenodo DOI mints on first GitHub Release |
| **P9** Web app + LLM + hosting | 15–18 | ✅* | compose.vm.yml + Caddyfile + Dockerfiles + cloud-Nemotron gateway ✅. *Stack bring-up on the VM pending |

**Gates:** **G1 — ✅ PASSED (94.9%/99.9%)** · G2 (ledger auto-assembly) — partial (gnomAD+ClinVar live; per-code P/R pending) · G3/G4 (lock + pre-register before headline ablation) — pending the real-cohort run · G5 (no real patient data in any artifact) — ✅ held · G6 (Docker-only, secrets via env) — ✅ held.

\* = code complete + unit-tested; the starred caveat is an external dependency (managed-access cohort, GPU tool image, or VM stack bring-up), not missing code.

**Tests:** 73 passing, ruff clean, CI green. **18 commits**, all sole-authored.

---

## Setup log (2026-06-12) — ✅

**Working/method → outcome:**

1. **Read & understood** the three planning docs (Detailed Execution Plan, Concept
   Brief, Phase-2 Decision Engine design). Goal, architecture, sources internalized.
2. **Tooling/credentials verified:** git (identity = Anees Ahmed Mahaboob Ali /
   ahmedaneesm@gmail.com), GitHub PAT (→ user `ahmedanees-m`), paramiko VM access,
   Docker 29.1.3 + RTX A4000 16 GB on VM `sjt418scope025`.
3. **GitHub repo created & scaffolded** (`omnivar-navigator`, private). Phase-0
   foundation implemented and tested (9 tests, ruff clean, CI workflow). Single-author
   commits only (no bot co-authors). Secret files kept out of git.
4. **VM cleanup** (per user decision "keep data/raw only"): the predecessor
   `omnivar-q` was retired — its `data/raw` (835 MB: gnomAD constraint metrics,
   ClinVar VCF `clinvar_20260503` + variant_summary, eRepo classifications, full HPO)
   was migrated to `~/omnivar-navigator/data/raw` and verified byte-for-byte before
   deleting the rest (root-owned leftovers removed via a throwaway `ubuntu:22.04`
   container — Docker-only, no host sudo). `omnivarq:gpu` image and empty
   `omnivar_workspace` left as instructed. Sibling projects untouched.
5. **Repo cloned onto the VM** (code + kept data; 9 tests pass on VM too).
6. **LLM layer** wired to **cloud Nemotron** (`nvidia/llama-3.3-nemotron-super-49b-v1`,
   free tier) — key tested OK; read from env only.
7. **Data parity:** raw data mirrored VM → `G:` drive via **SFTP** (no rclone);
   byte-for-byte match (9 files, 835,263,587 B).
8. **Source verification:** all plan sources/DOIs/links/numbers independently
   verified (see *OmniVar_Navigator_Source_Verification_Report.md*). 6 corrections
   captured; the code-affecting one (Pangolin pip) fixed.

**Commits:** `93d4a5e` scaffold · `6423d1a` Nemotron · `5d962c7` verification.

---

## Phase 0 — Foundations & rule engine

### Step 0.1 — Reproducibility & adapter contract — ✅
- **Method:** `core/adapter.py` defines `EvidenceAdapter` ABC (code_group, version,
  `evaluate`, `health_check`); container + CI (ruff + pytest) in `.github/workflows/ci.yml`.
- **Outcome:** contract in place; CI green. Mock/real adapters subclass it.

### Step 0.2 — Deterministic rule engine — 🟡
- **Method:** `rules/point_engine.py` sums signed reliability-weighted points and
  applies Tavtigian bands; BA1 standalone pre-filter. `rules/vcep_loader.py` (in
  progress) parses CSpec specs into `VCEPSpec`; specs as versioned YAML in `rules/specs/`.
- **Outcome so far:** bands + BA1 unit-tested. VCEP loader + F8 spec next.

### Step 0.3 — Points → posterior — ✅
- **Method:** `rules/posterior.py`, `OddsPath = 350^(C/8)`, prior 0.10.
- **Outcome:** anchors verified (C=10→0.99, C=6→0.90, C=0→0.10, C=−7→<0.001); tested.

### Step 0.4 — Data infrastructure — 🟡
- **Method:** kept reference data on VM + `G:`; `data/sources/build_manifest.py`
  fingerprints files (size + md5) into `data/manifest.json`.
- **Outcome:** store present + parity; manifest builder ready (to run on full store).

---

### Gate G1 — rule engine reproduces ClinGen eRepo — ✅ PASSED
- **Method:** parsed each of the **12,499** eRepo records' expert-applied evidence
  codes (`rules/acmg_codes.py`: handles `CODE` / `CODE_Strength` incl. spaced
  modifiers like `PM3_Very Strong`, BA1 standalone), fed them through the
  deterministic `point_engine`, and compared the predicted ACMG class to the expert
  assertion (`eval/validate_erepo.py`, run on the VM where the data lives).
- **Outcome:** **94.9% exact concordance, 99.9% within-one-bin** (all 12,499 evaluable).
  Residual >1-bin discordance is dominated by (a) VCEP-specific **BA1-override
  exceptions** (GJB2 c.109G>A, mitochondrial heteroplasmy) where the general ClinGen
  default correctly differs, and (b) a minority of records whose listed "Met" codes
  do not arithmetically match the assertion. Adjacent-bin cells (VUS↔LB, LP↔P) are
  expected point-band boundary fuzz.
- **Artifacts:** `rules/acmg_codes.py`, `eval/validate_erepo.py`. **Commits** `4fa3966`, `6e3c8fa`.

---

## Phase 2 — Decision & orchestration engine (the novel core) — 🟡

The scientific centerpiece. Pure-Python, fully unit-tested (no external data needed).

### Step 2.1 — Evidence-gap & conflict analysis — ✅
- **Method:** `engine/gap.py` — `attainable_codes()` enumerates not-yet-applied codes,
  gated by patient context (PS2 needs parents; PP1/BS4 need an informative family; PM3
  needs phasing) and by mechanism (PS3/BS3 only if a validated assay exists for the
  gene's mechanism). `gap_to_target()` = points to the target band. `detect_conflict()`
  flags VUS-by-conflict (opposing applied codes).
- **Outcome:** per-VUS list of "what would move it and by how much"; conflict flagging. Tested.

### Step 2.2 — Mechanism-aware code→action mapping — ✅
- **Method:** `engine/action_map.py` loads `action_catalog/bleeding.yaml` (ISTH Tier-1,
  mechanism-keyed). Same code (PS3) → different assays by mechanism.
- **Outcome:** the **key differentiator** is unit-tested — expression flow cytometry is
  **excluded** for an *activation*-defect gene (FERMT3/LAD-III) and routed to activation
  assays (PAC-1) instead.

### Step 2.3 — Value-of-information ranking — ✅
- **Method:** `engine/voi.py` — posterior `p = posterior(points)`; predictive `q`; expected
  information gain `EIG = H(p) − E[H(p′)]`; decision utility `E[ΔU]` (reaching a reporting
  threshold); value density `objective/(α·$ + β·weeks + γ·burden)`; myopic ranking + shallow
  exhaustive `lookahead`.
- **Outcome:** ranked actions with EIG + ΔU; calibrated to Tavtigian posterior / Brnich
  OddsPath. Tested (entropy, monotonic posteriors, cheaper-higher-yield preference, lookahead).

### Step 2.6 — Recommendation assembly — ✅
- **Method:** `engine/recommend.py` — gap → mechanism-correct actions → VOI ranking →
  `Recommendation` with current class/posterior, conflict flag, gap, ranked actions
  (each with expected post-action class + posterior), and a templated explanation.
- **Outcome:** end-to-end **Glanzmann worked example** reproduced — a VUS at +3 points →
  recommends flow cytometry (CD41/CD61, ~$450, ~1 wk) → expected PS3 (+4) → posterior ≈0.95
  → **Likely Pathogenic**. Tested.
- **Remaining for Phase 2:** risk gate (τ), equity filter hook (Phase 3), explicit Pareto
  frontier, `case_policy.py` whole-odyssey wrapper. **Commit** `5a74536`.

---

### Phase 2 completeness pass (vs design doc) — ✅
- Added per **OmniVar_Navigator_Phase2_Decision_Engine_Design.md**: risk gate τ (§3.6),
  outcome variance, cost–EIG **Pareto frontier** (§3.5), **conflict → orthogonal
  disambiguating assay** (§6), **recessive-diplotype / X-linked-hemizygote** case notes
  (§3.1/§6), lookahead escalation on near-ties (§3.8), and audit-ledger integration.
- **Modeling note:** under fixed ±4 points/action, EIG is near-flat across assays
  (branch entropies near-symmetric) → decision-utility ΔU and cost are the meaningful
  discriminators; EIG is reported for transparency (the Pareto axis). **Commit** `c0fc016`.

---

## Phase 1 — Evidence orchestration (adapters) — 🟡

### Step 1.5 — ClinVar adapter (PS1 / PM5) — ✅
- **Method:** `data/sources/build_clinvar_index.py` parsed the **kept** ClinVar
  `variant_summary.txt.gz` (run on the VM) into a gene→residue→{alt_aa: significance}
  index of P/LP missense. `adapters/clinvar.py` (`ClinVarAdapter`, EvidenceAdapter)
  emits **PS1** (same AA change is P/LP) or **PM5** (different pathogenic missense at
  the same residue).
- **Outcome:** index built from **8,978,110 rows → 70,723 P/LP missense across 4,560
  genes** (2.5 MB JSON, mirrored VM↔G:). Live demo fires PS1 correctly on real
  bleeding-gene variants (F8 p.Arg2228Gln, F8 p.Arg612Cys, VWF p.Arg854Gln). 31 tests pass.
- **Artifacts:** `adapters/clinvar.py`, `data/sources/build_clinvar_index.py`,
  `data/processed/clinvar_ps1_pm5.json`. **Commit** `47cbbcd`.
### Step 0.2/0.4 — VCEP loader + specs — ✅
- **Method:** `rules/vcep_loader.py` — `VCEPSpec` (AF thresholds, prior, mechanism,
  inheritance, BA1 pre-filter) + `get_spec(gene)` (gene YAML or base fallback). Specs:
  `rules/specs/base_acmg.yaml`, `F8.yaml` (GN071 v2.0.0 — verified rules encoded; AF
  thresholds marked as placeholders pending spec-PDF extraction).
- **Outcome:** swappable gene specs wired into the gnomAD adapter + point engine. Tested.

### Step 1.1 — gnomAD adapter (PM2/BS1/BA1) — ✅
- **Method:** `adapters/gnomad.py` — queries the **gnomAD v4 GraphQL API** for the
  worst-case 95% filtering AF popmax (grpmax) across genome+exome → BA1/BS1/PM2 via
  the spec thresholds (PM2 at Supporting per 2020 SVI). AF lookup injectable for tests.
- **Outcome:** **live API verified** (`1-55051215-G-A` → grpmax FAF 0.000277). 39 tests pass.

### End-to-end integration on real data — ✅
- **Demo (run on VM):** real F8 missense p.Arg612Cys → **ClinVar PS1 (Strong, +4)** →
  rule engine → **VUS** → decision core recommends **factor activity assay** (~$250, ~5d,
  the mechanism-correct coag-factor assay) → expected PS3 → posterior 0.97 → **Likely
  Pathogenic**, with the X-linked hemizygote PS4 note. The full vertical slice (adapters →
  rule engine → VOI recommendation) works on real reference data. **Commit** `b30cea5`.

---

### Remaining Phase-1 adapters — ✅
- `adapters/insilico.py` (calibrated PP3/BP4 via verified Pejaver-2022 REVEL thresholds),
  `splice.py` (Pangolin PP3/BP4/BP7 + RNA-resolvable flag), `autopvs1.py` (PVS1 SVI tree),
  `mave.py` (PS3/BS3 via Brnich OddsPath), `litmine_pm3.py` (PM3/PS4 — LLM proposes WITH
  citations, rule engine assigns), `prioritizer.py` (Exomiser/AI-MARRVEL→CandidateSet +
  disagreement flag). All EvidenceAdapter subclasses with injectable backends. **Commit** `49c9b84`.

---

## Phase 3 — Equity module — ✅
- `equity/reliability.py`: ancestry-aware reliability r∈[0,1] for PM2/BS1/PP3/BP4 (sparse
  reference data → down-weighted points). `routing.py`: route under-represented patients to
  ancestry-robust evidence. `ancestry.py`: nearest-centroid genetic-similarity assignment
  (VCF→PCs in a somalier/peddy tool image). `dashboard.py`: biased-vs-equitable fraction +
  cohort resolution gap. Wired into `recommend`. **Commit** `9a60168`.

## Phase 4 — Whole-odyssey layer — ✅
- `engine/case_policy.py` + `odyssey_actions.py`: interpretation-vs-detection-failure routing
  (variant VOI vs modality escalation: RNA-seq/long-read/optical/methylation/proteomics),
  reanalysis/matchmaking, with conditional-yield priors. **Commit** `8744891`.

## Phase 5 — Audit + learning loop (+ API) — ✅
- `core/audit.py` (hash-chained ledger) ✅; `learn/prior_update.py` + `outcome_store.py`
  (Beta-Bernoulli assay priors, attributable; verdict logic never retrained); `api/main.py`
  (/classify, /recommend, /case). Web UI front-end deferred (per frontend skill). **Commits** `8744891`, `580d6a4`.

## Phase 6 — Validation — ✅ (harnesses) 
- `sim/odyssey_sim.py` (VOI/greedy/random/fixed); `eval/{ablation,calibration,equity_eval,
  retrospective,stats}.py`. **Honest simulator result:** VOI beats random + uses ≤ greedy's
  tests; voi_stop is cheapest (graceful degradation); VOI does NOT dominate a cost-aware
  greedy on a homogeneous cohort (reported, not overfit). The simulator also surfaced and
  fixed two real engine bugs (cost-normalization of negative utility; directional point
  yield k_pos/k_neg). Real-cohort + managed-access runs pending. **Commits** `498f25f`, `0a34e86`, `0d80b7b`.

## Phase 7 — Domain expansion — ✅
- `action_catalog/{epilepsy,cancer}.yaml` + `specs/{SCN1A,BRCA1}.yaml`. Domain-agnosticism
  unit-tested: the SAME engine routes epilepsy→patch-clamp and cancer→MAVE with new packs
  only, no core change — the key generalization claim. **Commit** `580d6a4`.

## Phase 8 — Manuscript + release — ✅ (artifacts)
- `.github/workflows/release.yml` (build+push images to GHCR on tags; Zenodo DOI via the
  GitHub Release integration), `figures/generate_all.py` (300-dpi regenerable figures),
  `manuscript/outline.md` + `claims_map.md` (every claim → evidence → code, incl. negatives).
  **Commits** `1195fd3`, `ef36953`.

## Phase 9 — Web app + LLM + hosting — ✅ (artifacts)
- `deploy/compose.vm.yml` (api/worker/ui/postgres/qdrant/Caddy; cloud Nemotron, data
  read-only) + `Caddyfile` (TLS+auth, no PHI in logs) + `docker/Dockerfile.{api,worker,tools}`.
  Stack bring-up on the VM is the remaining step. **Commit** `1195fd3`.

---

## Honest status & what remains (external dependencies, not missing code)
- **Real-cohort validation runs** (the headline ablation on eRepo/EAHAD; per-code precision/
  recall): code is ready; needs the cohort wiring + pre-registration (gates G3/G4).
- **Managed-access cohorts** (Solve-RD/UDN): long DAC timelines — off the v1 critical path by design.
- **Tool images on the VM** (VEP/autoPVS1/Pangolin/somalier/MAVE): adapters are injectable and ready;
  needs `docker/Dockerfile.tools` built + wired (Docker-only).
- **Web UI front-end** and **VM stack bring-up**: compose/Dockerfiles ready; UI to be built.
- **Exact F8 GN071 AF thresholds**: placeholders marked in `specs/F8.yaml` pending spec-PDF extraction.
