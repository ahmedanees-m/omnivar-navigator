# OmniVar Navigator — manuscript outline (Phase 8)

**Target:** npj Genomic Medicine (primary); Genetics in Medicine / Genome Medicine
(secondary). Preprint: medRxiv. Pre-registration: OSF. Code/DOI: GitHub + Zenodo.

> Lock this skeleton and `claims_map.md` BEFORE the headline ablation (gate G3/G4).

1. **Introduction** — the diagnostic odyssey is long and mostly unsolved; what resolves
   hard cases is *evidence acquisition*, not better ranking; a VUS is formally an
   evidence deficit; no tool decides *what evidence to acquire*, prices it, or corrects
   for ancestry bias.
2. **Methods**
   - Rule-grounded deterministic engine (ClinGen/Tavtigian point system; posterior bridge).
   - Evidence orchestration (swappable adapters; per-code provenance).
   - Decision core: evidence-gap analysis, mechanism-aware code→action mapping,
     value-of-information ranking (EIG + decision utility, cost-normalized, Pareto,
     risk gate, lookahead), conflict disambiguation, recessive/X-linked handling.
   - Equity mechanism: reliability down-weighting + equitable routing.
   - Verifiable learning loop (Beta-Bernoulli priors; verdict logic never retrained).
   - Reproducibility: pinned env, Dockerized, source manifest, seeded simulator.
3. **Results**
   - Gate G1: rule engine reproduces ClinGen eRepo (concordance).
   - Phase-1 ledger auto-assembly: per-code precision/recall vs expert curation.
   - Headline ablation: full system vs tools-only (resolution, cost/time) — pre-registered.
   - Simulation: VOI vs greedy/random/fixed (honest, incl. negatives).
   - Calibration (reliability diagram + ECE) and equity (resolution-gap narrowing).
   - Domain generalization: epilepsy + cancer packs (no core change).
4. **Discussion** — contributions, limitations (managed cohorts/prospective deferred to
   Paper 2), decision-support-not-automation, honest negatives.
5. **Data & Code Availability** — GitHub repo; Zenodo DOIs (code snapshot; simulator +
   seeded synthetic odysseys; trained priors + benchmark results). No real patient data.

**Figures** (regenerable via `figures/generate_all.py`): posterior bridge; policy
comparison; eRepo concordance confusion matrix; calibration diagram; equity gap.
