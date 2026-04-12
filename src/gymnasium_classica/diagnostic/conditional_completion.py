"""Conditional completion: falling backwards when post-requisite failures
reveal prerequisite gaps.

Mechanism 3 of the diagnostic intake system.  After the diagnostic sets
nodes to 0.75-0.85 ("provisionally mastered"), this module handles the
case where a later failure on a post-requisite reveals that a prerequisite
was actually not mastered.
"""

import networkx as nx

from gymnasium_classica.models.graph import PrerequisiteEdge
from gymnasium_classica.models.learner import KnoopState, LearnerModel, MasterySource

# How much a post-requisite failure reduces prerequisite posteriors
FALLBACK_PENALTY_BASE = 0.15  # Multiplied by encompassing_weight


def identify_suspect_prerequisites(
    graph: nx.DiGraph,
    failed_knoop_id: str,
) -> list[tuple[str, float]]:
    """Given a failed post-requisite node, identify prerequisites that may
    be the cause, ranked by encompassing weight (highest = most likely cause).

    Returns a list of ``(prerequisite_id, encompassing_weight)`` pairs,
    sorted by weight descending.
    """
    suspects: list[tuple[str, float]] = []

    for pred in graph.predecessors(failed_knoop_id):
        edge_data = graph.edges[pred, failed_knoop_id].get("edge")
        if not isinstance(edge_data, PrerequisiteEdge):
            continue
        suspects.append((pred, edge_data.encompassing_weight))

    suspects.sort(key=lambda x: x[1], reverse=True)
    return suspects


def apply_fallback(
    learner: LearnerModel,
    graph: nx.DiGraph,
    failed_knoop_id: str,
) -> list[str]:
    """When a learner fails on *failed_knoop_id*, reduce the posterior of
    its prerequisites proportional to their encompassing weight.

    Only affects prerequisites that were established via diagnostic (source
    ``diagnostic``) — nodes that have been verified through practice are
    less likely to be the root cause.

    Returns a list of prerequisite IDs whose posteriors were reduced
    (these should be added to the review queue with elevated priority).
    """
    suspects = identify_suspect_prerequisites(graph, failed_knoop_id)
    affected: list[str] = []

    for pred_id, weight in suspects:
        state = learner.knoop_states.get(pred_id)
        if state is None:
            continue

        # Only penalise nodes that were set during diagnostic
        if state.source != MasterySource.DIAGNOSTIC:
            continue

        penalty = FALLBACK_PENALTY_BASE * weight
        new_posterior = max(0.0, state.posterior_mastery - penalty)

        if new_posterior < state.posterior_mastery:
            state.posterior_mastery = new_posterior
            state.source = MasterySource.REVIEW
            affected.append(pred_id)

    return affected
