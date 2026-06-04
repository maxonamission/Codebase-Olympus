"""Priority queue: compute urgency scores for knowledge nodes.

Each node's urgency is a weighted sum of five components:
  1. Forget urgency   (0.35) — how close to forgetting
  2. Readiness         (0.25) — prerequisites met for new material
  3. Pedagogical value (0.20) — how many post-requisites this unlocks
  4. Encompassing      (0.10) — integration node bonus
  5. Domain balance    (0.10) — keep G/V/C/I balanced in a session
"""

import math
from datetime import datetime

import networkx as nx

from gymnasium_classica.models.graph import Node, PrerequisiteEdge
from gymnasium_classica.models.learner import LearnerModel, NodeState

# Component weights
W_FORGET = 0.35
W_READINESS = 0.25
W_PEDAGOGICAL = 0.20
W_ENCOMPASSING = 0.10
W_DOMAIN_BALANCE = 0.10

# Thresholds
MASTERY_THRESHOLD = 0.75
PREREQ_READY_THRESHOLD = 0.75

# Domain balance targets
DOMAIN_BALANCE_TARGETS: dict[str, float] = {
    "G": 0.40,
    "V": 0.40,
    "C": 0.15,
    "I": 0.05,
}


def estimate_retention(
    state: NodeState,
    now: datetime | None = None,
) -> float:
    """Estimate current retention probability using exponential decay.

    ``R(t) = exp(-t / (interval * EF / 2.5))``

    Returns 0.0 for never-reviewed unmastered nodes, 0.5 for diagnostic-only
    mastered nodes (uncertain), and the decay value for reviewed nodes.
    """
    if state.last_review is None:
        if state.posterior_mastery >= MASTERY_THRESHOLD:
            return 0.5  # Diagnostic-set, uncertain
        return 0.0  # Never seen

    if now is None:
        now = datetime.now()

    elapsed_days = max(0.0, (now - state.last_review).total_seconds() / 86400.0)
    if state.interval_days <= 0:
        return 0.0

    stability = state.interval_days * state.easiness_factor / 2.5
    if stability <= 0:
        return 0.0

    return math.exp(-elapsed_days / stability)


def forget_urgency(state: NodeState, now: datetime | None = None) -> float:
    """Forget urgency: 1.0 - estimated_retention. Higher = more urgent."""
    return 1.0 - estimate_retention(state, now)


def readiness_score(
    knoop_id: str,
    learner: LearnerModel,
    graph: nx.DiGraph,
    prereq_threshold: float | None = None,
) -> float:
    """Readiness for an unmastered node: minimum posterior of all prerequisites.

    Returns 1.0 if no prerequisites exist.
    Returns 0.0 if any prerequisite is below *prereq_threshold*.
    Returns 0.0 for already-mastered nodes (not relevant as "new material").

    The *prereq_threshold* parameter allows context-first scheduling to
    relax the gate (e.g. 0.25 instead of the default 0.75).
    """
    if prereq_threshold is None:
        prereq_threshold = PREREQ_READY_THRESHOLD

    state = learner.knoop_states.get(knoop_id)
    if state and state.posterior_mastery >= MASTERY_THRESHOLD:
        return 0.0  # Already mastered — not a "new material" candidate

    predecessors = list(graph.predecessors(knoop_id))
    if not predecessors:
        return 1.0  # Root node — always ready

    min_posterior = 1.0
    for pred_id in predecessors:
        pred_state = learner.knoop_states.get(pred_id)
        posterior = pred_state.posterior_mastery if pred_state else 0.0
        if posterior < prereq_threshold:
            return 0.0  # Hard gate: prerequisite not met
        min_posterior = min(min_posterior, posterior)

    return min_posterior


def pedagogical_value(
    knoop_id: str,
    graph: nx.DiGraph,
    max_out_degree: int = 1,
) -> float:
    """Pedagogical value: normalized out-degree. High = unlocks many nodes."""
    out_deg = int(graph.out_degree(knoop_id))
    if max_out_degree <= 0:
        return 0.0
    return min(1.0, out_deg / max_out_degree)


def encompassing_bonus(
    knoop_id: str,
    graph: nx.DiGraph,
) -> float:
    """Bonus for nodes with high total incoming encompassing weight.

    Integration nodes (type I) and nodes exercising many prerequisites
    score higher.
    """
    total_weight = 0.0
    for pred in graph.predecessors(knoop_id):
        edge_data = graph.edges[pred, knoop_id].get("edge")
        if isinstance(edge_data, PrerequisiteEdge):
            total_weight += edge_data.encompassing_weight

    # Normalize: assume max realistic total is ~3.0
    return min(1.0, total_weight / 3.0)


def domain_balance_penalty(
    knoop: Node,
    session_type_counts: dict[str, int],
) -> float:
    """Penalty/bonus for domain balance within a session.

    Over-represented domains get a penalty, under-represented get a bonus.
    Returns a value in [-0.5, 0.5].
    """
    total = sum(session_type_counts.values())
    if total == 0:
        return 0.0

    domain = knoop.type.value
    target = DOMAIN_BALANCE_TARGETS.get(domain, 0.25)
    actual = session_type_counts.get(domain, 0) / total

    # Positive when under-represented, negative when over
    return max(-0.5, min(0.5, (target - actual) * 2.0))


def compute_urgency_scores(
    learner: LearnerModel,
    graph: nx.DiGraph,
    session_type_counts: dict[str, int] | None = None,
    now: datetime | None = None,
) -> list[tuple[float, Node]]:
    """Compute urgency scores for all nodes in the graph.

    Returns a list of ``(urgency, Node)`` tuples, sorted by
    urgency descending.  Nodes with unmet prerequisites are excluded
    unless they are mastered and due for review.
    """
    if session_type_counts is None:
        session_type_counts = {}

    # Precompute max out-degree for normalization
    max_out_deg = max((graph.out_degree(n) for n in graph.nodes), default=1)
    if max_out_deg == 0:
        max_out_deg = 1

    results: list[tuple[float, Node]] = []

    for node_id in graph.nodes:
        knoop: Node = graph.nodes[node_id]["knoop"]
        state = learner.knoop_states.get(node_id)

        if state is None:
            state = NodeState(knoop_id=node_id, posterior_mastery=0.10)

        is_mastered = state.posterior_mastery >= MASTERY_THRESHOLD
        ready = readiness_score(node_id, learner, graph)

        if not is_mastered and ready == 0.0:
            continue  # Prerequisites not met, skip

        # Compute components
        f_urgency = forget_urgency(state, now)
        p_value = pedagogical_value(node_id, graph, max_out_deg)
        e_bonus = encompassing_bonus(node_id, graph)
        d_balance = domain_balance_penalty(knoop, session_type_counts)

        # For mastered nodes: readiness is 0 (they're review candidates, not new)
        # For new nodes: readiness contributes
        urgency = (
            W_FORGET * f_urgency
            + W_READINESS * ready
            + W_PEDAGOGICAL * p_value
            + W_ENCOMPASSING * e_bonus
            + W_DOMAIN_BALANCE * max(0.0, d_balance)
        )

        results.append((urgency, knoop))

    results.sort(key=lambda x: x[0], reverse=True)
    return results
