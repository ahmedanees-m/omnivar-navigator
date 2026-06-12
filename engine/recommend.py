"""Recommendation assembly (plan Phase 2.6 / design §4.4).

Ties the decision core together: from a points ledger + patient context + the gene's
disease mechanism, it (1) finds attainable evidence codes, (2) maps them to concrete
mechanism-correct actions, (3) ranks by value-of-information per cost, and (4) emits
an explained, audited recommendation with the *expected post-action classification*.

The explanation is templated from the deterministic plan — an LLM (via llm/gateway)
may phrase it, but never decides it.
"""
from __future__ import annotations

from dataclasses import dataclass

from core.schemas import Action, Classification, PatientContext, PointsLedger
from engine.action_map import expand_actions
from engine.gap import attainable_codes, detect_conflict, gap_to_target
from engine.voi import rank_actions
from rules.point_engine import classify
from rules.posterior import posterior


@dataclass
class Recommendation:
    current_class: Classification
    current_posterior: float
    in_conflict: bool
    gap_to_lp: float
    ranked: list[dict]                 # [{action, value_density, eig, delta_utility, ...}]
    explanation: str


def _expected_post_class(points: float, action: Action) -> tuple[Classification, float]:
    """Best-case (positive-result) class + posterior if this action yields its top code."""
    # strongest positive code the action can yield: PS-class -> +4, else PM-class -> +2
    k = 4.0 if any(c.startswith("PS") for c in action.yields_codes) else 2.0
    pts = points + k
    return _class_for_points(pts), posterior(pts)


def _class_for_points(points: float) -> Classification:
    from rules.point_engine import BANDS
    for threshold, cls in BANDS:
        if points >= threshold:
            return cls
    return Classification.B


def recommend_next_action(ledger: PointsLedger, patient: PatientContext, mechanism: str,
                          domain: str = "bleeding", prior_p: float = 0.10,
                          objective: str = "delta_utility", alpha: float = 1.0,
                          beta: float = 50.0, gamma: float = 0.0,
                          target: Classification = Classification.LP) -> Recommendation:
    points = ledger.points
    current_class = classify(ledger)
    conflict = detect_conflict(ledger)

    opps = attainable_codes(ledger, patient, mechanism, domain)
    codes = [o.code for o in opps if o.delta_points > 0 or not conflict.in_conflict]
    actions = expand_actions(codes, mechanism, domain)
    ranked = rank_actions(points, actions, prior_p=prior_p, objective=objective,
                          alpha=alpha, beta=beta, gamma=gamma)

    rows = []
    for a, vd, s in ranked:
        post_cls, post_p = _expected_post_class(points, a)
        rows.append({
            "action": a.name, "modality": a.modality, "yields": a.yields_codes,
            "cost_usd": a.cost_usd, "turnaround_days": a.turnaround_days,
            "value_density": round(vd, 6), "eig_bits": round(s["eig"], 4),
            "delta_utility": round(s["delta_utility"], 4),
            "expected_post_class": post_cls.name, "expected_post_posterior": round(post_p, 3),
        })

    explanation = _explain(points, current_class, rows, gap_to_target(ledger, target),
                           target, conflict.in_conflict)
    return Recommendation(
        current_class=current_class,
        current_posterior=round(posterior(points, prior_p), 3),
        in_conflict=conflict.in_conflict,
        gap_to_lp=gap_to_target(ledger, target),
        ranked=rows,
        explanation=explanation,
    )


def _explain(points, current_class, rows, gap, target, in_conflict) -> str:
    if not rows:
        return (f"{current_class.value} at {points:+.0f} points. No attainable evidence "
                "for this patient/mechanism — recommend reanalysis or matchmaking.")
    top = rows[0]
    head = "VUS-by-conflict" if in_conflict else current_class.value
    msg = (f"{head} at {points:+.0f} points ({gap:.0f} to {target.name}). "
           f"Recommended: {top['action']} (~${top['cost_usd']:.0f}, "
           f"~{top['turnaround_days']}d) → expected {'/'.join(top['yields'])} → "
           f"posterior {top['expected_post_posterior']:.2f} → {top['expected_post_class']}.")
    if len(rows) > 1:
        alt = rows[1]
        msg += f" Alternative: {alt['action']} (~${alt['cost_usd']:.0f})."
    return msg
