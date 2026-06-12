"""Reader-study harness (plan Phase 9.1) — the headline "does it help".

Scores standardized vignettes: does DISCERN identify the correct disease, recommend the
correct next test, and avoid harmful management (fire the right safety flag)? The
randomized with-vs-without reader study (non-specialists) is run on top of this bank;
here we provide the vignette type + the DISCERN-side scoring.
"""
from __future__ import annotations

from dataclasses import dataclass

from diseases.ontology import route_clusters
from jointdx.factorgraph import Evidence
from jointdx.orchestrate import diagnose


@dataclass
class Vignette:
    id: str
    ev: Evidence
    correct_disease_id: str
    correct_next_obs_id: str
    harmful_tx: str | None = None        # a treatment that must be flagged/avoided


@dataclass
class ReaderScore:
    n: int
    disease_accuracy: float
    next_test_accuracy: float
    harmful_avoidance: float             # fraction where the harmful tx was flagged


def score_discern(vignettes: list[Vignette]) -> ReaderScore:
    n = len(vignettes)
    dx = nt = harm = 0
    harm_total = 0
    for v in vignettes:
        if not route_clusters([v.ev.variant_gene]):
            continue
        rec = diagnose(v.ev, planned_tx=v.harmful_tx, n_mc=40)
        if rec is None:
            continue
        if rec.posterior.leading == v.correct_disease_id:
            dx += 1
        if rec.next_observation is not None and rec.next_observation.id == v.correct_next_obs_id:
            nt += 1
        if v.harmful_tx is not None:
            harm_total += 1
            if any(v.harmful_tx in f.message.lower() or f.severity == "high"
                   for f in rec.safety_flags):
                harm += 1
    return ReaderScore(
        n=n, disease_accuracy=dx / n if n else 0.0,
        next_test_accuracy=nt / n if n else 0.0,
        harmful_avoidance=harm / harm_total if harm_total else 1.0,
    )
