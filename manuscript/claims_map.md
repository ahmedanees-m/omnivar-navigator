# Claims map (Phase 8) — every claim -> its evidence + code

Lock before the headline ablation. Each claim must map to a reproducible artifact.

| # | Claim | Evidence / metric | Code | Status |
|---|---|---|---|---|
| C1 | The rule engine reproduces expert ACMG calls | concordance vs ClinGen eRepo (12,499 records) | `eval/validate_erepo.py` | **done: 94.9% exact / 99.9% within-one-bin** |
| C2 | The points→posterior bridge matches Tavtigian anchors | C=10→0.99, 6→0.90, 0→0.10 | `rules/posterior.py`, `tests/test_posterior.py` | done |
| C3 | Adapters auto-assemble a rule-grounded ledger from real data | gnomAD live API; ClinVar PS1/PM5 (70,723 P/LP missense) | `adapters/*`, end-to-end demo | done (PS1/gnomAD); per-code P/R pending |
| C4 | Mechanism-aware routing avoids the wrong assay | expression flow excluded for activation defects (FERMT3) | `engine/action_map.py`, `tests/test_engine.py` | done |
| C5 | VOI decision layer adds yield / reduces cost vs tools-only | paired ablation (McNemar/Wilcoxon) | `eval/ablation.py` | harness done; run on cohorts (pre-register) |
| C6 | VOI beats naive baselines in simulation | resolved/cost vs greedy/random/fixed | `sim/odyssey_sim.py` | done — VOI > random; ties cost-aware greedy (honest) |
| C7 | Confidence is calibrated | reliability diagram + ECE | `eval/calibration.py` | harness done |
| C8 | Equity routing narrows the ancestry resolution gap | gap equity-on vs -off + bootstrap CI | `equity/*`, `eval/equity_eval.py` | mechanism done; cohort run pending |
| C9 | The engine generalizes across domains via packs only | epilepsy + cancer packs route correctly, no core change | `engine/action_catalog/{epilepsy,cancer}.yaml` | done |
| C10 | The learning loop improves auditably, never retraining the verdict | Beta-Bernoulli priors attributable to cases | `learn/*` | done |
| C11 | Recommendations are fully audited / reproducible | hash-chained ledger; per-source provenance | `core/audit.py`, `engine/recommend.py` | done |

**Negatives to report honestly:** C6 (VOI does not dominate a cost-aware greedy on a
homogeneous cohort); any null ablation result; modest absolute reclassification rates.
