# OmniVar Navigator — Phase 2: The Decision Engine (Design Document)

**Companion to:** *Detailed Execution Plan* (this expands Phase 2) and the *Concept Brief*.
**What this is:** the deep design of the engine's novel core — the layer that decides *what to do next* to resolve a stuck variant or case. Everything else in the system feeds this, and this is where the genuine novelty concentrates.
**Date:** 2026-06-11
**Domain coverage in this doc:** full inherited bleeding & platelet disorder scope, anchored on the **ISTH-SSC Tier-1 gene list** (Megy et al. 2019, annually updated via the ISTH Gold Variants project; www.isth.org/page/GinTh_GeneLists) — coagulation factors, VWD, platelet function/integrin disorders, the LADs, granule and signaling disorders, and inherited thrombocytopenias.

---

## 0. Where Phase 2 sits

```
Phase 1 (orchestration) ──► per-candidate PointsLedger + posterior  ──►  ┌──────────────┐
PatientContext (ancestry, family, prior assays, budget/preferences) ──► │  PHASE 2     │ ──► RankedPlan
Domain pack (rules + action catalog + assay priors)                ──► │  decision    │     (next action(s),
Equity reliability (Phase 3)                                       ──► │  engine      │      expected post-action
                                                                        └──────────────┘      class, confidence,
                                                                                               Pareto frontier, audit)
                                                                              │
                                                                    Human review UI (sign-off)
```

Phase 2 **consumes** the rule-grounded ledger (it never re-derives classification) and **produces** a ranked, explained, costed recommendation for the next evidence-acquisition or workup action — for a human to accept or override.

---

## 1. The problem, stated precisely

A variant is a **VUS for one of two reasons**, and the engine must handle both:

1. **Evidence deficit** — not enough points accumulated either way (the common case). Resolution = *acquire* the evidence code(s) that close the points gap to a reporting threshold.
2. **Evidence conflict** — opposing evidence present (e.g., PM3 pathogenic *and* BS3 benign). Resolution = *acquire the disambiguating evidence* that breaks the tie, not merely add points.

The engine's job: for a given unsolved variant/case, choose the **single most informative, cost-effective, ancestry-fair next action**, quantify what it would do to the classification, and present it with calibrated uncertainty — as decision *support*, never an automated verdict.

---

## 2. Formal model — Bayesian sequential experimental design

Optimal "what test next" is exactly **Bayesian sequential experimental design / value-of-information** (a finite-horizon POMDP). We do **not** attempt a globally optimal POMDP policy (intractable and unnecessary); we use **myopic (1-step) VOI as the default** with **shallow finite-horizon lookahead (depth 2–3)** when it matters (§3.8). The pieces:

| Element | Definition in our setting |
|---|---|
| **Belief** `b` | per candidate variant: `PointsLedger` → posterior probability of pathogenicity `p = posterior(points)`; for recessive genes, the *genotype-causality* belief over the diplotype; plus case-level state (solved?, modalities already run) |
| **Action** `a ∈ A` | an orderable real-world action that yields ACMG code(s): functional assay → PS3/BS3, RNA → PS3-splice, trio → PS2, segregation → PP1/BS4, more cases → PS4/PM3, phenotyping → PP4; **plus** whole-odyssey modality actions (long-read GS, optical mapping, methylation, proteomics), **plus** `wait/reanalyze`, `matchmaking`, `stop/report` |
| **Observation** `o` | the assay result (binary, categorical, or quantitative) with a likelihood model (§3.2) |
| **Transition** `T` | deterministic ledger update via the rule engine given the resulting code(s) |
| **Utility** `R` | information gain and/or probability of reaching an actionable classification, **minus** cost (money + time + patient burden), with **risk-aversion** and **equity** weighting |

Objective: choose the action (or short action-sequence) that maximizes **expected utility per unit cost**.

---

## 3. The math (the heart of the engine)

### 3.1 Belief — points → posterior (and diplotypes)
Single variant: `p = posterior(points) = (Λ·π)/((Λ−1)·π + 1)`, with `Λ = 350^(points/8)` and prior `π` (default 0.10, gene/VCEP-specific; phenotype-conditioned — §6).

**Recessive genes (most platelet/bleeding disorders — Glanzmann, BSS, LAD).** Disease causality is a property of the **genotype**, not a single allele. Track both alleles; the engine reasons over the pair:
- two pathogenic alleles in *trans* ⇒ causal genotype;
- the in-*trans* relationship itself is evidence (**PM3**), attainable by phasing/parental testing;
- a single confirmed pathogenic allele + a phenotype-confirming **functional assay on the gene product** (e.g., absent αIIbβ3) strongly supports the genotype even before the second allele is fully resolved.

So for recessive disorders the engine often has *two* productive targets: (a) resolve/raise the VUS allele, or (b) establish *trans* + functional protein loss — and it costs them both.

### 3.2 Observation likelihood model
For action `a` whose positive result yields a code contributing `+k_pos` points (e.g., PS3 = +4) and whose negative result yields `−k_neg` (e.g., BS3 = −4):
- assay performance: `s_a = P(o=pos | causal)` (sensitivity), `t_a = P(o=neg | benign)` (specificity);
- these connect to the assay's **OddsPath** (Brnich et al. 2020): a validated assay's OddsPath sets both the strength `k` and informs `s_a/t_a`;
- **quantitative readouts** (e.g., flow-cytometry % surface αIIbβ3, factor activity %) get a likelihood from the readout distribution under causal vs. benign (often bimodal — e.g., Glanzmann type I < 5% expression), not a hard threshold.

Predictive probability of a positive result: `q = s_a·p + (1−t_a)·(1−p)`.

### 3.3 Posterior update (deterministic, via the rule engine)
- positive ⇒ `points + k_pos` ⇒ `p₊ = posterior(points + k_pos)`
- negative ⇒ `points − k_neg` ⇒ `p₋ = posterior(points − k_neg)`

### 3.4 Utility — value of information
Two complementary objectives; the engine computes both and exposes them.

**(a) Information-theoretic (entropy reduction):**
`EIG(a) = H(p) − [q·H(p₊) + (1−q)·H(p₋)]`, `H` = binary entropy (or the 5-class classification entropy for a fuller picture).

**(b) Decision-theoretic (clinically preferred):** define an **actionability utility** `U(p)` that rewards reaching a *reporting* threshold (P/LP at `p ≥ 0.90`, or B/LB at `p ≤ 0.10`); between, `U` ramps. Then
`E[ΔU](a) = q·U(p₊) + (1−q)·U(p₋) − U(p)`
— i.e., the expected gain in probability of producing an *actionable* call. This is what a lab actually wants ("will this test let me sign the variant out?").

**Interpretable secondary metric:** expected points-to-resolution / expected number of further tests.

### 3.5 Cost model & Pareto selection
`cost(a) = c$ + β·weeks + γ·burden` (β converts turnaround to a $-equivalent; γ penalizes invasiveness/patient burden). **Value density** = `utility(a) / cost(a)`. Rather than commit to one scalarization, the engine reports the **cost–EIG Pareto frontier** and lets the clinician choose (e.g., "cheapest path to LP" vs. "fastest"); the default recommendation is the top of a transparent default scalarization.

### 3.6 Risk aversion
Plain VOI is risk-neutral. The engine adds tunable risk-aversion so it won't recommend an invasive/expensive assay with low expected yield: penalize high outcome-variance actions, or apply a CVaR-style criterion on the utility, or hard-gate actions by `expected ΔU ≥ τ`. Clinician-tunable (a cautious lab and an aggressive research setting want different τ).

### 3.7 Equity weighting
Reliability `r ∈ [0,1]` already down-weights ancestry-biased codes (PM2/PP3) in the ledger (Phase 3). In *action selection*, the engine additionally **penalizes actions whose only yield is a low-reliability code** and **prefers ancestry-robust actions** (functional assays, segregation) for under-represented-ancestry patients — turning the documented equity gap into a routing rule. (Concretely relevant: Glanzmann/BSS/LAD cohorts are enriched in consanguineous populations where allele-frequency evidence is least reliable.)

### 3.8 Multi-step lookahead
Myopic VOI is near-optimal for monotone information acquisition and is the fast default. But two situations need lookahead: (i) a cheap test *enables* a more informative one (dependency); (ii) two cheap tests *jointly* cross the threshold while neither alone does. Because `|A|` is modest (tens of actions) and useful depth is shallow (2–3), the engine does **exhaustive/beam tree search over action-sequences** under the observation model, pruning dominated branches. Default = myopic; escalate to lookahead when the top myopic actions are within ε of each other or when budget allows.

---

## 4. Module design

### 4.1 `engine/gap.py` — evidence-gap & conflict analysis
- **Attainability** is mechanism- and context-aware (not just "is the code missing"):
  ```python
  def attainable_codes(ledger, spec, patient) -> list[CodeOpportunity]:
      out, applied = [], {c.code for c in ledger.contributions if c.applied}
      for code, rule in spec.codes.items():
          if code in applied:
              continue
          ok, prereqs, mech = rule.attainable(ledger, patient)   # context + mechanism gate
          if ok:
              out.append(CodeOpportunity(code, rule.strength, rule.strength.value, prereqs, mech))
      return out
  ```
  Examples of the predicates: `PS2` attainable only if `patient.parents_available`; `PP1/BS4` only if `patient.informative_family`; `PS3-splice` only if the variant is splice-relevant (from the splice adapter's "RNA-resolvable" flag); `PS3-functional` only if a validated assay exists for the gene's **mechanism** (see §7 — and not, e.g., expression flow cytometry for an *activation*-defect gene).
- **Conflict detection:** if the ledger contains opposing applied codes, flag *VUS-by-conflict* and target the **disambiguating** action (e.g., a second, orthogonal functional assay) rather than just any point-adding action.
- **Diplotype gap** for recessive genes: compute the genotype-level gap and surface both productive targets (raise the allele vs. establish *trans* + functional loss).

### 4.2 `engine/action_map.py` + `action_catalog/` — mechanism-aware code→action
The catalog maps each code opportunity to concrete actions **conditioned on the gene's disease mechanism**. This is essential — the same code (PS3) is generated by different assays depending on mechanism:

```yaml
# action_catalog/bleeding.yaml (mechanism-keyed excerpt; priors to be calibrated)
mechanisms:
  integrin_expression:        # ITGA2B, ITGB3 (Glanzmann) — protein absent/reduced
    PS3: [flow_cd41_cd61, ltA_panel, clot_retraction]
  integrin_activation:        # FERMT3 (LAD-III), RASGRP2 — protein PRESENT but inactive
    PS3: [platelet_activation_pac1, soluble_fibrinogen_binding, ltA_panel]   # NOT expression flow
  gpib_complex:               # GP1BA/B, GP9 (Bernard-Soulier)
    PS3: [flow_cd42a_cd42b, ripa_absent]
  leukocyte_adhesion_b2:      # ITGB2 (LAD-I)
    PS3: [flow_cd18_cd11a]
  coag_factor:                # F8, F9, F7, F10, F11, F5, F13, FGA/B/G
    PS3: [factor_activity_assay, thrombin_generation, mixing_study]
  vwf:                        # VWF (subtype-aware)
    PS3: [vwf_fviii_binding, vwf_multimers, vwf_rco_gpibm, ripa_low_dose]
  dense_granule:              # HPS1-11, LYST, AP3B1
    PS3: [wholemount_em, mepacrine_uptake, lumiaggregometry_secretion]
  alpha_granule:              # NBEAL2, GFI1B (Gray platelet)
    PS3: [immunofluorescence_granule, electron_microscopy, blood_film]
actions:
  flow_cd41_cd61:            {yields: [PS3],      cost_usd: 450,  days: 7,  sens: 0.90, spec: 0.92, modality: functional}
  platelet_activation_pac1:  {yields: [PS3],      cost_usd: 700,  days: 10, sens: 0.85, spec: 0.90, modality: functional}
  vwf_fviii_binding:         {yields: [PS3, BS3], cost_usd: 600,  days: 14, sens: 0.85, spec: 0.90, modality: functional}
  rna_seq_splice:            {yields: [PS3, BS3], cost_usd: 900,  days: 28, sens: 0.78, spec: 0.92, modality: rna}
  trio_testing:              {yields: [PS2, PM3], cost_usd: 1200, days: 21, sens: 0.72, spec: 0.99, modality: segregation}
```
> The sens/spec/cost values are **literature-seeded priors, explicitly versioned**, and updated per-institution by the learning loop (Phase 5.2). They are not asserted as final.

### 4.3 `engine/voi.py` — scoring (myopic + lookahead)
```python
import numpy as np
from rules.posterior import posterior

def _H(p): return 0.0 if p in (0.0, 1.0) else -(p*np.log2(p) + (1-p)*np.log2(1-p))
def _U(p, hi=0.90, lo=0.10):                 # actionability utility (reaches a reporting call)
    if p >= hi or p <= lo: return 1.0
    return max((p-0.5)/(hi-0.5), (0.5-p)/(0.5-lo), 0.0)   # ramps toward the nearer threshold

def score_action(points, a, prior_p=0.10, k_pos=None, k_neg=None):
    p = posterior(points, prior_p)
    k_pos = k_pos if k_pos is not None else 4      # PS3 strong
    k_neg = k_neg if k_neg is not None else 4      # BS3 strong
    q = a.sensitivity*p + (1-a.specificity)*(1-p)
    p_pos, p_neg = posterior(points+k_pos, prior_p), posterior(points-k_neg, prior_p)
    eig  = _H(p) - (q*_H(p_pos) + (1-q)*_H(p_neg))
    dU   = q*_U(p_pos) + (1-q)*_U(p_neg) - _U(p)
    return {"eig": eig, "delta_utility": dU, "p_pos": p_pos, "p_neg": p_neg, "q": q}

def value_density(points, a, alpha=1.0, beta=50.0, gamma=0.0, objective="delta_utility", **kw):
    s = score_action(points, a, **kw)
    cost = alpha*a.cost_usd + beta*a.turnaround_days/7.0 + gamma*getattr(a, "burden", 0.0)
    return s[objective] / cost, s

def lookahead(points, actions, depth=2, prior_p=0.10):
    """Expected utility of best action-sequences; exhaustive over a small A, shallow depth."""
    if depth == 0 or not actions:
        return _U(posterior(points, prior_p)), []
    best_val, best_seq = -np.inf, []
    for a in actions:
        s = score_action(points, a, prior_p=prior_p)
        rest = [x for x in actions if x is not a]
        v_pos, _ = lookahead(points + 4, rest, depth-1, prior_p)
        v_neg, _ = lookahead(points - 4, rest, depth-1, prior_p)
        val = s["q"]*v_pos + (1-s["q"])*v_neg
        if val > best_val:
            best_val, best_seq = val, [a]
    return best_val, best_seq
```

### 4.4 `engine/recommend.py` — assembly
1. pick target classification (LP for a leaning-pathogenic VUS, LB for leaning-benign, or "either actionable call");
2. score attainable actions (myopic), escalate to `lookahead` if the top scores tie;
3. apply risk gate (τ) and equity routing;
4. rank by value density; build the **Pareto frontier** for transparency;
5. compose the explanation — **templated from the deterministic plan**, with the LLM (Qwen, via the gateway) only phrasing it, e.g.: *"This is a VUS at +3 points. Cheapest path to Likely Pathogenic: flow cytometry for αIIbβ3 (CD41/CD61) — ~$450, ~1 wk — expected to add PS3 (+4) → posterior 0.91. Alternative: confirm de novo / trans via parental testing (PS2/PM3)."*;
6. attach calibrated confidence + full audit (every input, source, rule version, model version).

### 4.5 `engine/case_policy.py` — whole-odyssey wrapper
Decides, across the case: **which candidate variant to pursue** (highest expected resolution value), **whether to resolve a variant vs. escalate a modality** (interpretation- vs. detection-failure routing), and **when to stop/report/wait/matchmake**. Reanalysis is modeled as a low-cost "wait" action with a knowledge-growth prior; matchmaking as an action for novel-gene candidates.

---

## 5. End-to-end algorithm

```python
def recommend_next_action(case, budget=None, prefs=None):
    plans = []
    for cand in case.candidates:                      # multi-candidate handling
        ledger, spec = cand.ledger, cand.spec
        if classify(ledger, spec) in (P, LP, B, LB):  # already actionable → no action needed
            continue
        opps = attainable_codes(ledger, spec, case.patient)
        if not opps:                                  # honest fallback
            plans.append(reanalysis_or_matchmaking(cand)); continue
        actions = expand_actions(opps, domain_pack, mechanism=spec.mechanism(cand.variant))
        actions = equity_filter(actions, case.patient)        # Phase 3 routing
        ranked  = sorted(((a, *value_density(ledger.points, a, **prefs)) for a in actions),
                         key=lambda t: t[1], reverse=True)
        ranked  = risk_gate(ranked, tau=prefs.get("tau", 0.0))
        plans.append(assemble_plan(cand, ranked, pareto=pareto_front(ledger.points, actions)))
    return case_policy(plans, case)                   # variant-vs-modality, stop/wait/matchmake
```

---

## 6. Edge cases & honest handling

| Situation | Handling |
|---|---|
| **Conflicting evidence** (PM3 + BS3) | Flag VUS-by-conflict; recommend an *orthogonal disambiguating* assay, not point-stacking |
| **Recessive / biallelic** (Glanzmann, BSS, LAD) | Diplotype belief; target *trans*+functional-loss as well as raising the allele; PM3 via phasing |
| **X-linked** (F8/F9 hemophilia, WAS) | Hemizygote handling; F8/F9 use the CFD-VCEP hemizygote **PS4** rule; males need one allele |
| **Phenotype-conditioned prior** | Strong gene–phenotype match raises `π` (and PP4 strength, subtype-specific for VWD type 2N) — changes the posterior and the VOI |
| **Mechanism mismatch** | For an *activation*-defect gene (FERMT3/LAD-III) the engine must **not** recommend expression flow cytometry (expression is normal) — it routes to activation assays (PAC-1/soluble-fibrinogen binding) |
| **Strength upgrade vs. new code** | An action may *upgrade* an existing code's strength (e.g., a better-calibrated assay) rather than add a new code — modeled as a Δpoints on the existing contribution |
| **Unsolvable now** | No attainable evidence ⇒ honest "not currently resolvable" + reanalysis cadence + matchmaking |
| **Leukemia-predisposition platelet genes** (RUNX1, ETV6, ANKRD26) | Flag the germline-cancer-risk/unsolicited-finding implication; links to the cancer pack; handle per consent (ISTH guidance) |

---

## 7. Bleeding & Platelet Domain Pack — coverage (anchored on ISTH Tier-1)

**Gene scope = the ISTH-SSC Tier-1 BTPD list** (Megy et al. 2019; ~91 curated gene-disease associations, annually updated via Gold Variants; 2024 added Tier-1 *ERG*, Tier-2 *MASTL*/*SERPINA1*). Adopting this list wholesale is what makes coverage *complete and principled* rather than ad-hoc. Genes are organized into mechanism clusters, each with its diagnostic functional assays (the PS3/BS3 generators the engine recommends):

| Cluster | Representative genes | Inheritance | Diagnostic functional assays (PS3/BS3 generators) |
|---|---|---|---|
| Coagulation factor deficiencies | F8, F9, F7, F10, F11, F5, F13A1/F13B, FGA/FGB/FGG, F2 | XLR (F8/F9); AR (most) | factor activity, mixing study, thrombin generation, antigen assay |
| von Willebrand disease | VWF | AD/AR by subtype | VWF:Ag, VWF:RCo/GPIbM, **VWF:FVIII binding** (2N), multimers, low-dose RIPA (2B) |
| Platelet integrin — expression | **ITGA2B, ITGB3** (Glanzmann) | AR | **flow CD41/CD61** (absent/↓), LTA (absent to all but ristocetin), clot retraction |
| Platelet integrin — activation | **FERMT3** (LAD-III), RASGRP2 (CalDAG-GEFI) | AR | **activation assays** (PAC-1, soluble-fibrinogen binding), LTA — *expression is normal* |
| GPIb-IX-V complex | GP1BA, GP1BB, GP9 (Bernard-Soulier) | AR (some AD) | flow CD42a/CD42b (↓), absent ristocetin agglutination, giant platelets |
| Leukocyte adhesion (β2) | **ITGB2** (LAD-I), SLC35C1 (LAD-II) | AR | flow CD18/CD11a (LAD-I); CD15s/sialyl-LewisX (LAD-II) |
| Dense-granule disorders | HPS1–11, LYST (Chediak-Higashi), AP3B1 | AR | whole-mount EM, mepacrine uptake, lumi-aggregometry secretion |
| α-granule disorders | NBEAL2, GFI1B (Gray platelet) | AR/AD | granule immunofluorescence, EM, blood film |
| Secretion/signaling receptors | P2RY12, TBXA2R, PTGS1 | AR/AD | agonist-specific LTA, secretion assays |
| Thrombocytopenia + leukemia risk | **RUNX1, ETV6, ANKRD26** | AD | count/film; **germline cancer-risk flag** (consent/ethics) |
| Thrombocytopenia — structural | MYH9, TUBB1, ACTN1, FLNA | AD (FLNA XL) | blood film (MYH9 leukocyte inclusions), platelet size |
| Amegakaryocytic / TAR | MPL, RBM8A (TAR), THPO | AR | marrow, platelet count |
| X-linked | WAS, GATA1 | XLR | flow (WASP), small platelets |

**Worked examples that exercise the engine:**
1. **Glanzmann, synonymous-but-not-silent.** A homozygous *synonymous* ITGB3 variant scores benign on every missense predictor. The splice adapter flags it RNA-resolvable; gap analysis sees the only path out of VUS is **PS3-splice via RNA-seq/RT-PCR**; the engine recommends it (and, because AR, notes the homozygous *trans* status supports the genotype).
2. **LAD-III, mechanism-aware routing.** A *FERMT3* missense VUS in a child with Glanzmann-type bleeding **plus infections**. Naive logic would order αIIbβ3 flow cytometry — but FERMT3 is an *activation* defect with **normal expression**, so the engine routes instead to **platelet-activation assays (PAC-1/soluble-fibrinogen binding)** → PS3, and conditions the prior on the dual bleeding+immunodeficiency phenotype (PP4). This mechanism-awareness is a concrete differentiator.
3. **VWD type 2N.** A VWF missense VUS reaches Pathogenic via **PS3 (VWF:FVIII binding) + PM3 + PP4 (2N-specific phenotype) + PP1**; the engine names VWF:FVIII binding as the single highest-value assay up front.

---

## 8. Phase-2-specific validation

- **Simulation (`sim/odyssey_sim.py`):** synthetic variants/cases with known resolution paths drawn from the cluster/assay priors; metric = cost & time to resolution, % resolved. **Baselines:** greedy (best sensitivity/cost), random, and "fixed clinical default pathway." Target: the VOI policy dominates on the cost–resolution frontier.
- **Retrospective journey replay:** on cases with a known resolving action (eRepo/EAHAD curated trails; Solve-RD/UDN as access clears), test whether the engine's #1 recommended action matches what actually resolved the case, at lower predicted cost.
- **VOI calibration:** predicted Δposterior and predicted yield vs. realized — reliability diagrams; the engine's *promises* must be calibrated, not just its classifications.
- **Internal ablations:** myopic vs. lookahead; risk-gate on/off; equity-routing on/off; mechanism-aware vs. mechanism-blind action mapping (expected to matter most for the activation-defect cluster).

---

## 9. Interface contract

```python
# api/main.py  (engine endpoints)
POST /recommend
  body:  {case: CandidateSet, patient: PatientContext, budget?: Budget, prefs?: {tau, alpha, beta, gamma, objective}}
  returns: RankedPlan {
     current_class, current_posterior,
     actions: [{action, value_density, eig, delta_utility, expected_post_action_class, p_pos, p_neg, cost}],
     pareto_frontier: [...],
     explanation: str,                 # LLM-phrased, deterministic-grounded
     audit: {inputs, sources, spec_version, model_version}
  }
```

---

## 10. Build order (Phase 2 sub-steps)

| Sub-step | Deliverable | Depends on | Acceptance |
|---|---|---|---|
| 2.0 | `RankedPlan`/`CodeOpportunity`/`Action` schemas finalized | core schemas | round-trips; typed |
| 2.1 | `engine/gap.py` (attainability + conflict + diplotype) | Phase 1 ledgers, specs | matches ClinGen functional-evidence-potential logic on test set |
| 2.2 | `action_catalog/bleeding.yaml` + `action_map.py` (mechanism-keyed) | ISTH Tier-1 + assay priors | every opportunity → ≥1 mechanism-correct action |
| 2.3 | `engine/voi.py` (myopic) | posterior bridge | unit-tested EIG/ΔU; monotonic sanity checks |
| 2.4 | `engine/voi.py` (lookahead) + risk gate | 2.3 | beats myopic on the dependency/joint-threshold test cases |
| 2.5 | `equity_filter` hook | Phase 3 reliability | down-weights low-reliability-only actions |
| 2.6 | `engine/recommend.py` (assembly + explanation) | 2.1–2.5, LLM gateway | end-to-end recommendation with audit on a bleeding case |
| 2.7 | `engine/case_policy.py` (whole-odyssey) | 2.6 | variant-vs-modality + stop/wait/matchmake decisions |
| 2.8 | Phase-2 validation harness | 2.6, simulator | dominates baselines in simulation; VOI calibration reported |

---

## 11. Risks specific to the decision engine

| Risk | Mitigation |
|---|---|
| Assay priors wrong/lab-specific → bad rankings | Priors versioned + learning-loop-updated; report sensitivity of recommendations to priors |
| Myopic VOI misses multi-step paths | Lookahead escalation (§3.8) on ties / when budget allows |
| Over-confident recommendations | VOI calibration as a first-class validation target; risk-gate; always human sign-off |
| Mechanism mis-mapping (e.g., activation vs expression) | Mechanism-keyed catalog; the LAD-III example is an explicit test case |
| "Optimizes cost over patient welfare" perception | Burden term in cost; risk aversion; clinician chooses on the Pareto frontier; decision-support not automation |

---

### One-paragraph summary
Phase 2 treats a stuck variant or case as a Bayesian sequential-decision problem: from the rule-grounded points ledger it computes a posterior, enumerates the *attainable* evidence codes (mechanism- and context-aware), maps each to a real, costed, ancestry-fair lab action, and ranks them by expected information gain (or expected probability of reaching an actionable call) per dollar and week — myopically by default, with shallow lookahead when it matters — then hands a human a transparent, audited recommendation with the expected post-action classification. The deterministic rule engine always computes the verdict; the LLM only explains. Anchored on the ISTH Tier-1 gene list with mechanism-aware functional-assay routing, it covers the full bleeding/platelet landscape — coagulation factors, VWD, Glanzmann, Bernard-Soulier, the LADs, granule and signaling disorders, and the inherited thrombocytopenias — and it is, as far as the literature shows, the piece no existing tool provides.
