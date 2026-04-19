"""Adaptive diagnostic placement test.

Mechanism 2 of the diagnostic intake system.  Uses the graph's topological
order and encompassing weights to efficiently find the learner's knowledge
frontier in ≤ 30 questions.
"""

from collections.abc import Callable
from dataclasses import dataclass, field

import networkx as nx

from gymnasium_classica.models.graph import PrerequisiteEdge
from gymnasium_classica.models.learner import KnoopState, LearnerModel, MasterySource

# Convergence thresholds
MASTERED_THRESHOLD = 0.75  # Above this → considered mastered
UNMASTERED_THRESHOLD = 0.25  # Below this → considered unmastered
MAX_QUESTIONS = 30
SKIP_ON_CORRECT = 5  # How many positions to jump forward on correct answer
SKIP_ON_INCORRECT = 1  # Fall back to the first unresolved prerequisite

# How much a correct answer on a post-requisite boosts prerequisites
ENCOMPASSING_BOOST = 0.25  # Multiplied by encompassing_weight


@dataclass
class DiagnosticResult:
    """Result of a completed diagnostic session."""

    questions_asked: int = 0
    knoop_ids_tested: list[str] = field(default_factory=list)
    converged: bool = False


def _topo_order(graph: nx.DiGraph) -> list[str]:
    """Return a stable topological ordering of nodes."""
    return list(nx.topological_sort(graph))


def _get_or_init_state(learner: LearnerModel, knoop_id: str) -> KnoopState:
    """Get existing state or create a new one with default prior."""
    if knoop_id not in learner.knoop_states:
        learner.knoop_states[knoop_id] = KnoopState(
            knoop_id=knoop_id,
            posterior_mastery=0.10,
            source=MasterySource.DIAGNOSTIC,
        )
    return learner.knoop_states[knoop_id]


def _is_resolved(state: KnoopState) -> bool:
    """A node is resolved when its posterior is clearly mastered or unmastered."""
    return (
        state.posterior_mastery >= MASTERED_THRESHOLD
        or state.posterior_mastery <= UNMASTERED_THRESHOLD
    )


def _all_resolved(learner: LearnerModel, graph: nx.DiGraph) -> bool:
    """Check whether every node in the graph has a resolved posterior."""
    for node_id in graph.nodes:
        state = _get_or_init_state(learner, node_id)
        if not _is_resolved(state):
            return False
    return True


def _find_start_position(learner: LearnerModel, topo: list[str]) -> int:
    """Find the starting position: the first node along topological order
    whose posterior is *not* clearly resolved.

    Falls back to the midpoint if all are unresolved (no method profile).
    """
    for i, knoop_id in enumerate(topo):
        state = _get_or_init_state(learner, knoop_id)
        if not _is_resolved(state):
            return i

    # All resolved already (unlikely, means intake is done)
    return len(topo) // 2


SIBLING_BOOST_FACTOR = 0.6  # Siblings get 60% of the direct boost


def _propagate_correct(
    learner: LearnerModel,
    graph: nx.DiGraph,
    knoop_id: str,
) -> None:
    """After a correct answer, boost prerequisites and siblings.

    1. **Prerequisites** are boosted proportional to their encompassing weight.
       This is *implicit diagnostics*: a correct answer on a post-requisite
       implies partial mastery of its prerequisites.
    2. **Siblings** (nodes sharing a common prerequisite with the tested node)
       are boosted by a smaller amount.  Rationale: if a learner knows
       NOM-D1, they likely know GEN-D1 and ACC-D1 too, since they share
       the prerequisite DECL1-INTRO.
    """
    # 1. Boost direct prerequisites
    for pred in graph.predecessors(knoop_id):
        edge_data = graph.edges[pred, knoop_id].get("edge")
        if not isinstance(edge_data, PrerequisiteEdge):
            continue
        weight = edge_data.encompassing_weight
        boost = ENCOMPASSING_BOOST * weight

        state = _get_or_init_state(learner, pred)
        state.posterior_mastery = min(1.0, state.posterior_mastery + boost)
        state.source = MasterySource.DIAGNOSTIC

    # 2. Boost siblings: nodes that share at least one prerequisite
    parents = set(graph.predecessors(knoop_id))
    siblings_boosted: set[str] = set()
    for parent in parents:
        for sibling in graph.successors(parent):
            if sibling == knoop_id or sibling in siblings_boosted:
                continue
            siblings_boosted.add(sibling)
            # Get the edge weight from the shared parent
            edge_data = graph.edges[parent, sibling].get("edge")
            if not isinstance(edge_data, PrerequisiteEdge):
                continue
            weight = edge_data.encompassing_weight
            boost = ENCOMPASSING_BOOST * weight * SIBLING_BOOST_FACTOR

            state = _get_or_init_state(learner, sibling)
            state.posterior_mastery = min(1.0, state.posterior_mastery + boost)
            state.source = MasterySource.DIAGNOSTIC


def _propagate_incorrect(
    learner: LearnerModel,
    graph: nx.DiGraph,
    knoop_id: str,
) -> None:
    """After an incorrect answer, lower the posterior of the node and its
    successors (post-requisites) since they depend on this knowledge.
    """
    # Mark the tested node as likely unmastered
    state = _get_or_init_state(learner, knoop_id)
    state.posterior_mastery = max(0.0, state.posterior_mastery - 0.25)
    state.source = MasterySource.DIAGNOSTIC

    # Successors are now also suspect
    for succ in graph.successors(knoop_id):
        succ_state = _get_or_init_state(learner, succ)
        if succ_state.posterior_mastery > UNMASTERED_THRESHOLD:
            succ_state.posterior_mastery = max(0.0, succ_state.posterior_mastery - 0.10)
            succ_state.source = MasterySource.DIAGNOSTIC


def _find_next_unresolved(
    learner: LearnerModel,
    topo: list[str],
    start: int,
    direction: int,
) -> int | None:
    """Scan from *start* in *direction* (+1 or -1) to find the next
    unresolved node.  Returns the index or None if none found.
    """
    i = start
    while 0 <= i < len(topo):
        state = _get_or_init_state(learner, topo[i])
        if not _is_resolved(state):
            return i
        i += direction
    return None


def run_diagnostic(
    learner: LearnerModel,
    graph: nx.DiGraph,
    answer_fn: Callable[[str], bool],
) -> DiagnosticResult:
    """Run the adaptive diagnostic placement test.

    *answer_fn(knoop_id: str) -> bool* simulates or collects a learner's
    answer for the given knowledge node.  Returns True for correct, False
    for incorrect.  In production this would be the frontend presenting an
    item and collecting the response.

    The algorithm:
      1. Compute topological order.
      2. Start at the knowledge frontier (first unresolved node).
      3. Ask a question for the current node.
      4. Correct → boost the node and its prerequisites, skip forward.
      5. Incorrect → lower the node and its successors, step back.
      6. Repeat until convergence or MAX_QUESTIONS.
    """
    topo = _topo_order(graph)
    if not topo:
        return DiagnosticResult(converged=True)

    # Initialize any missing states
    for node_id in topo:
        _get_or_init_state(learner, node_id)

    result = DiagnosticResult()
    cursor = _find_start_position(learner, topo)

    while result.questions_asked < MAX_QUESTIONS:
        if _all_resolved(learner, graph):
            result.converged = True
            break

        knoop_id = topo[cursor]
        state = _get_or_init_state(learner, knoop_id)

        # Skip already-resolved nodes
        if _is_resolved(state):
            next_pos = _find_next_unresolved(learner, topo, cursor + 1, +1)
            if next_pos is None:
                next_pos = _find_next_unresolved(learner, topo, cursor - 1, -1)
            if next_pos is None:
                result.converged = True
                break
            cursor = next_pos
            continue

        # Ask the question
        correct = answer_fn(knoop_id)
        result.questions_asked += 1
        result.knoop_ids_tested.append(knoop_id)

        if correct:
            # Boost this node
            state.posterior_mastery = min(1.0, state.posterior_mastery + 0.35)
            state.source = MasterySource.DIAGNOSTIC
            # Implicit diagnostics: boost prerequisites
            _propagate_correct(learner, graph, knoop_id)
            # Jump forward
            next_pos = _find_next_unresolved(
                learner, topo, min(cursor + SKIP_ON_CORRECT, len(topo) - 1), +1
            )
            if next_pos is not None:
                cursor = next_pos
            else:
                # No more unresolved ahead, scan backward
                next_pos = _find_next_unresolved(learner, topo, cursor - 1, -1)
                if next_pos is None:
                    result.converged = True
                    break
                cursor = next_pos
        else:
            _propagate_incorrect(learner, graph, knoop_id)
            # Step back to prerequisites
            preds = list(graph.predecessors(knoop_id))
            unresolved_pred = None
            for pred in preds:
                pred_state = _get_or_init_state(learner, pred)
                if not _is_resolved(pred_state):
                    idx = topo.index(pred)
                    unresolved_pred = idx
                    break
            if unresolved_pred is not None:
                cursor = unresolved_pred
            else:
                # All prereqs resolved, find any remaining unresolved
                next_pos = _find_next_unresolved(learner, topo, cursor + 1, +1)
                if next_pos is None:
                    next_pos = _find_next_unresolved(learner, topo, cursor - 1, -1)
                if next_pos is None:
                    result.converged = True
                    break
                cursor = next_pos

    learner.intake_completed = True
    return result
