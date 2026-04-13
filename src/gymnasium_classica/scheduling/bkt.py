"""Bayesian Knowledge Tracing: update posterior mastery after each response.

Standard BKT with two-step update (Corbett & Anderson, 1995):
  1. Bayesian update: P(L|obs) given the observation (correct/incorrect).
  2. Learning transition: P(L_n) = P(L|obs) + (1 - P(L|obs)) * P(T).

After a correct response, prerequisites are boosted proportionally to their
encompassing weight (implicit diagnostics during practice).
"""

from dataclasses import dataclass

import networkx as nx

from gymnasium_classica.models.graph import PrerequisiteEdge
from gymnasium_classica.models.learner import (
    KnoopState,
    LearnerModel,
    MasterySource,
    ResponseType,
)

# Default BKT parameters
DEFAULT_P_TRANSIT = 0.10  # Conservative for classical languages
DEFAULT_P_GUESS = 0.20  # Reasonable for 5-option morphology recognition
DEFAULT_P_SLIP = 0.05  # Low — experienced students rarely make careless errors

# Self-report BKT parameters: higher P(G) and P(S) to reflect reduced confidence
# in self-reported results vs. objectively verified (online or OCR) responses.
SELF_REPORT_P_GUESS = 0.35
SELF_REPORT_P_SLIP = 0.15

# Practice propagation (smaller than diagnostic to reflect incremental learning)
PRACTICE_ENCOMPASSING_BOOST = 0.10
PRACTICE_SIBLING_FACTOR = 0.3

# Posterior bounds to prevent mathematical degeneracy
POSTERIOR_MIN = 0.001
POSTERIOR_MAX = 0.999


@dataclass
class BKTParams:
    """BKT parameters for a single knowledge node."""

    p_transit: float = DEFAULT_P_TRANSIT
    p_guess: float = DEFAULT_P_GUESS
    p_slip: float = DEFAULT_P_SLIP


SELF_REPORT_BKT_PARAMS = BKTParams(
    p_transit=DEFAULT_P_TRANSIT,
    p_guess=SELF_REPORT_P_GUESS,
    p_slip=SELF_REPORT_P_SLIP,
)


def bkt_update_posterior(
    prior: float,
    correct: bool,
    params: BKTParams | None = None,
) -> float:
    """Compute the updated posterior P(L_n) given an observation.

    Two-step update:
      1. Bayesian: P(L|obs) using guess/slip probabilities
      2. Transition: P(L_n) = P(L|obs) + (1 - P(L|obs)) * P(T)

    Returns the new posterior, clamped to [0.001, 0.999].
    """
    if params is None:
        params = BKTParams()

    p_l = prior
    p_g = params.p_guess
    p_s = params.p_slip
    p_t = params.p_transit

    if correct:
        # P(L | correct) = P(L)*(1-P(S)) / [P(L)*(1-P(S)) + (1-P(L))*P(G)]
        numerator = p_l * (1.0 - p_s)
        denominator = p_l * (1.0 - p_s) + (1.0 - p_l) * p_g
    else:
        # P(L | incorrect) = P(L)*P(S) / [P(L)*P(S) + (1-P(L))*(1-P(G))]
        numerator = p_l * p_s
        denominator = p_l * p_s + (1.0 - p_l) * (1.0 - p_g)

    if denominator == 0:
        p_l_given_obs = prior
    else:
        p_l_given_obs = numerator / denominator

    # Learning transition
    p_l_new = p_l_given_obs + (1.0 - p_l_given_obs) * p_t

    return max(POSTERIOR_MIN, min(POSTERIOR_MAX, p_l_new))


def _get_or_create_state(learner: LearnerModel, knoop_id: str) -> KnoopState:
    """Get existing state or create one with default untreated prior."""
    if knoop_id not in learner.knoop_states:
        learner.knoop_states[knoop_id] = KnoopState(
            knoop_id=knoop_id,
            posterior_mastery=0.10,
        )
    return learner.knoop_states[knoop_id]


def update_knoop_state(
    learner: LearnerModel,
    knoop_id: str,
    response: ResponseType,
    params: BKTParams | None = None,
) -> KnoopState:
    """Update a single node's BKT posterior given a response.

    ``slow_correct`` is treated as ``correct`` for BKT (BKT does not
    model response speed).  The speed distinction is used by SM-2 only.
    """
    state = _get_or_create_state(learner, knoop_id)
    correct = response in (ResponseType.CORRECT, ResponseType.SLOW_CORRECT)
    state.posterior_mastery = bkt_update_posterior(
        state.posterior_mastery, correct, params
    )
    state.source = MasterySource.PRACTICE
    return state


def propagate_practice_correct(
    learner: LearnerModel,
    graph: nx.DiGraph,
    knoop_id: str,
) -> list[str]:
    """After a correct practice response, boost prerequisite and sibling
    posteriors via encompassing weights.

    Follows the same pattern as diagnostic propagation but with smaller
    boosts (PRACTICE_ENCOMPASSING_BOOST * weight for prereqs,
    further reduced by PRACTICE_SIBLING_FACTOR for siblings).

    Returns list of affected node IDs.
    """
    affected: list[str] = []
    parents = set(graph.predecessors(knoop_id))

    # Boost direct prerequisites
    for pred in parents:
        edge_data = graph.edges[pred, knoop_id].get("edge")
        if not isinstance(edge_data, PrerequisiteEdge):
            continue
        weight = edge_data.encompassing_weight
        boost = PRACTICE_ENCOMPASSING_BOOST * weight

        state = _get_or_create_state(learner, pred)
        new_val = min(POSTERIOR_MAX, state.posterior_mastery + boost)
        if new_val > state.posterior_mastery:
            state.posterior_mastery = new_val
            affected.append(pred)

    # Boost siblings (nodes sharing a common prerequisite)
    siblings_seen: set[str] = set()
    for parent in parents:
        for sibling in graph.successors(parent):
            if sibling == knoop_id or sibling in siblings_seen:
                continue
            siblings_seen.add(sibling)
            edge_data = graph.edges[parent, sibling].get("edge")
            if not isinstance(edge_data, PrerequisiteEdge):
                continue
            weight = edge_data.encompassing_weight
            boost = PRACTICE_ENCOMPASSING_BOOST * weight * PRACTICE_SIBLING_FACTOR

            state = _get_or_create_state(learner, sibling)
            new_val = min(POSTERIOR_MAX, state.posterior_mastery + boost)
            if new_val > state.posterior_mastery:
                state.posterior_mastery = new_val
                affected.append(sibling)

    return affected
