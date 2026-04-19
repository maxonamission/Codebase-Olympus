"""Step-by-step diagnostic intake protocol.

Decomposes diagnostic/placement.py's run_diagnostic() into request/response
steps, analogous to SessionManager for regular sessions.

  1. start_intake() → intake_id + first question
  2. submit_answer() → next question or intake finished
"""

from dataclasses import dataclass, field
from uuid import uuid4

import networkx as nx

from gymnasium_classica.diagnostic.placement import (
    MAX_QUESTIONS,
    SKIP_ON_CORRECT,
    MasterySource,
    _all_resolved,
    _find_next_unresolved,
    _find_start_position,
    _get_or_init_state,
    _is_resolved,
    _propagate_correct,
    _propagate_incorrect,
)
from gymnasium_classica.models.graph import EdgeType, KennisKnoop, PrerequisiteEdge
from gymnasium_classica.models.learner import LearnerModel


def _topo_order_safe(graph: nx.DiGraph) -> list[str]:
    """Topological ordering on the prerequisite-only subgraph.

    The full graph may contain bidirectional transfer/enrichment edges that
    form cycles.  We filter to prerequisite edges only before sorting, then
    append any remaining nodes not reached by prerequisite edges.
    """
    prereq_graph = nx.DiGraph()
    prereq_graph.add_nodes_from(graph.nodes)
    for u, v, data in graph.edges(data=True):
        edge = data.get("edge")
        if isinstance(edge, PrerequisiteEdge) and edge.type == EdgeType.PREREQUISITE:
            prereq_graph.add_edge(u, v)
    return list(nx.topological_sort(prereq_graph))


@dataclass
class IntakeQuestion:
    """A question to present during the diagnostic intake."""

    knoop_id: str
    titel: str
    beschrijving: str
    questions_asked: int
    max_questions: int


@dataclass
class IntakeAnswerResult:
    """Result of submitting an intake answer."""

    questions_asked: int
    next_question: IntakeQuestion | None = None
    finished: bool = False
    converged: bool = False


@dataclass
class _IntakeState:
    """Mutable state for an active intake session."""

    intake_id: str
    user_id: str
    learner: LearnerModel
    graph: nx.DiGraph
    topo: list[str]
    cursor: int = 0
    questions_asked: int = 0
    knoop_ids_tested: list[str] = field(default_factory=list)
    current_knoop_id: str | None = None
    finished: bool = False
    converged: bool = False


class IntakeManager:
    """Manages active intake sessions in-memory."""

    def __init__(self) -> None:
        self._intakes: dict[str, _IntakeState] = {}

    def start_intake(
        self,
        user_id: str,
        learner: LearnerModel,
        graph: nx.DiGraph,
    ) -> tuple[str, IntakeQuestion | None]:
        """Start a diagnostic intake. Returns (intake_id, first_question).

        first_question is None if the graph is empty or already fully resolved.
        """
        intake_id = uuid4().hex[:12]
        topo = _topo_order_safe(graph)

        if not topo:
            state = _IntakeState(
                intake_id=intake_id,
                user_id=user_id,
                learner=learner,
                graph=graph,
                topo=topo,
                finished=True,
                converged=True,
            )
            self._intakes[intake_id] = state
            return intake_id, None

        # Initialize missing states
        for node_id in topo:
            _get_or_init_state(learner, node_id)

        cursor = _find_start_position(learner, topo)

        state = _IntakeState(
            intake_id=intake_id,
            user_id=user_id,
            learner=learner,
            graph=graph,
            topo=topo,
            cursor=cursor,
        )
        self._intakes[intake_id] = state

        question = self._find_question(state)
        if question is None:
            state.finished = True
            state.converged = True

        return intake_id, question

    def submit_answer(self, intake_id: str, correct: bool) -> IntakeAnswerResult:
        """Process an intake answer. Returns next question or finish status.

        Raises KeyError for unknown intake_id.
        Raises ValueError if intake is already finished or no question is pending.
        """
        state = self._intakes[intake_id]
        if state.finished:
            raise ValueError(f"Intake {intake_id} is already finished")
        if state.current_knoop_id is None:
            raise ValueError(f"No pending question for intake {intake_id}")

        knoop_id = state.current_knoop_id
        knoop_state = _get_or_init_state(state.learner, knoop_id)

        state.questions_asked += 1
        state.knoop_ids_tested.append(knoop_id)
        state.current_knoop_id = None

        if correct:
            # Boost this node
            knoop_state.posterior_mastery = min(1.0, knoop_state.posterior_mastery + 0.35)
            knoop_state.source = MasterySource.DIAGNOSTIC
            _propagate_correct(state.learner, state.graph, knoop_id)

            # Jump forward
            next_pos = _find_next_unresolved(
                state.learner,
                state.topo,
                min(state.cursor + SKIP_ON_CORRECT, len(state.topo) - 1),
                +1,
            )
            if next_pos is not None:
                state.cursor = next_pos
            else:
                next_pos = _find_next_unresolved(state.learner, state.topo, state.cursor - 1, -1)
                if next_pos is None:
                    return self._finish(state, converged=True)
                state.cursor = next_pos
        else:
            _propagate_incorrect(state.learner, state.graph, knoop_id)

            # Step back to unresolved prerequisite
            preds = list(state.graph.predecessors(knoop_id))
            unresolved_pred = None
            for pred in preds:
                pred_state = _get_or_init_state(state.learner, pred)
                if not _is_resolved(pred_state):
                    try:
                        unresolved_pred = state.topo.index(pred)
                    except ValueError:
                        continue
                    break

            if unresolved_pred is not None:
                state.cursor = unresolved_pred
            else:
                next_pos = _find_next_unresolved(state.learner, state.topo, state.cursor + 1, +1)
                if next_pos is None:
                    next_pos = _find_next_unresolved(
                        state.learner, state.topo, state.cursor - 1, -1
                    )
                if next_pos is None:
                    return self._finish(state, converged=True)
                state.cursor = next_pos

        # Check stopping conditions
        if state.questions_asked >= MAX_QUESTIONS:
            return self._finish(state, converged=False)

        if _all_resolved(state.learner, state.graph):
            return self._finish(state, converged=True)

        # Find next question
        question = self._find_question(state)
        if question is None:
            return self._finish(state, converged=True)

        return IntakeAnswerResult(
            questions_asked=state.questions_asked,
            next_question=question,
        )

    def has_intake(self, intake_id: str) -> bool:
        return intake_id in self._intakes

    def get_intake_state(self, intake_id: str) -> _IntakeState:
        return self._intakes[intake_id]

    def _find_question(self, state: _IntakeState) -> IntakeQuestion | None:
        """Find the next unresolved node to ask about, starting at cursor."""
        topo = state.topo
        cursor = state.cursor

        # Skip resolved nodes from cursor position
        knoop_id = topo[cursor]
        ks = _get_or_init_state(state.learner, knoop_id)
        if _is_resolved(ks):
            next_pos = _find_next_unresolved(state.learner, topo, cursor + 1, +1)
            if next_pos is None:
                next_pos = _find_next_unresolved(state.learner, topo, cursor - 1, -1)
            if next_pos is None:
                return None
            state.cursor = next_pos
            cursor = next_pos

        knoop_id = topo[cursor]
        knoop: KennisKnoop = state.graph.nodes[knoop_id]["knoop"]
        state.current_knoop_id = knoop_id

        return IntakeQuestion(
            knoop_id=knoop_id,
            titel=knoop.titel_nl,
            beschrijving=knoop.beschrijving,
            questions_asked=state.questions_asked,
            max_questions=MAX_QUESTIONS,
        )

    def _finish(self, state: _IntakeState, converged: bool) -> IntakeAnswerResult:
        """Mark intake as finished."""
        state.finished = True
        state.converged = converged
        state.learner.intake_completed = True
        return IntakeAnswerResult(
            questions_asked=state.questions_asked,
            finished=True,
            converged=converged,
        )
