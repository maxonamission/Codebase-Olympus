"""Step-by-step session protocol: the bridge between the API and the scheduling engine.

Decomposes run_session()'s synchronous loop into an async-compatible
request/response protocol:

  1. start_session() → session_id + first Question
  2. submit_answer() → AnswerResult (feedback + next question OR session end)
  3. get_summary()   → SessionSummary
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import uuid4

import networkx as nx

from gymnasium_classica.models.graph import KennisKnoop
from gymnasium_classica.models.learner import (
    LearnerModel,
    OfflineAssignment,
    ResponseType,
    SessionRecord,
)
from gymnasium_classica.scheduling.bkt import propagate_practice_correct, update_knoop_state
from gymnasium_classica.scheduling.non_interference import NonInterferenceState, select_next
from gymnasium_classica.scheduling.priority import MASTERY_THRESHOLD, compute_urgency_scores
from gymnasium_classica.scheduling.session import (
    DEFAULT_ITEM_TIME_SEC,
    MAX_NEW_NODES,
    PHASE_BUDGETS,
    PHASE_ORDER,
    SessionPhase,
    _candidates_for_cooldown,
    _candidates_for_deepening,
    _candidates_for_new_material,
    _candidates_for_warmup,
    _collect_offline_items,
    _get_state_posterior,
    _process_response,
)
from gymnasium_classica.scheduling.sm2 import sm2_update


# -- Data classes for the step-by-step protocol --


@dataclass
class Question:
    """A question to present to the learner."""

    knoop_id: str
    titel: str
    beschrijving: str
    stimulus: str | dict
    phase: str
    items: list[dict] = field(default_factory=list)


@dataclass
class Feedback:
    """Feedback after answering a question."""

    knoop_id: str
    correct: bool
    mastery_before: float
    mastery_after: float


@dataclass
class AnswerResult:
    """Result of submit_answer: feedback + next question (or session end)."""

    feedback: Feedback
    next_question: Question | None = None
    session_finished: bool = False


@dataclass
class SessionSummary:
    """Summary of a completed session."""

    session_id: str
    started_at: str
    ended_at: str
    total_items: int
    nodes_introduced: list[str]
    nodes_reviewed: list[str]
    mastery_changes: dict[str, tuple[float, float]]
    phases_completed: list[str]


# -- Internal session state --


@dataclass
class _SessionState:
    """All mutable state for an active session."""

    session_id: str
    user_id: str
    learner: LearnerModel
    graph: nx.DiGraph
    started_at: datetime
    phase_index: int = 0
    budget_remaining: int = 0
    candidates: list[tuple[float, KennisKnoop]] = field(default_factory=list)
    ni_state: NonInterferenceState = field(default_factory=NonInterferenceState)
    session_node_ids: set[str] = field(default_factory=set)
    nodes_introduced: list[str] = field(default_factory=list)
    nodes_reviewed: list[str] = field(default_factory=list)
    mastery_changes: dict[str, tuple[float, float]] = field(default_factory=dict)
    current_knoop: KennisKnoop | None = None
    current_before: float = 0.0
    items_presented: int = 0
    phases_completed: list[str] = field(default_factory=list)
    finished: bool = False
    ended_at: datetime | None = None


def _knoop_to_question(knoop: KennisKnoop, phase: SessionPhase) -> Question:
    """Convert a KennisKnoop to a Question for the API."""
    items = []
    for item in knoop.items:
        items.append({
            "id": item.id,
            "type": item.type.value,
            "stimulus": item.stimulus,
            "feedback": item.feedback,
            "verwachte_tijd_sec": item.verwachte_tijd_sec,
        })
    return Question(
        knoop_id=knoop.id,
        titel=knoop.titel_nl,
        beschrijving=knoop.beschrijving,
        stimulus=knoop.items[0].stimulus if knoop.items else knoop.beschrijving,
        phase=phase.value,
        items=items,
    )


class SessionManager:
    """Manages active sessions as a step-by-step protocol.

    Sessions live in-memory, keyed by session_id.
    """

    def __init__(self) -> None:
        self._sessions: dict[str, _SessionState] = {}

    def start_session(
        self,
        user_id: str,
        learner: LearnerModel,
        graph: nx.DiGraph,
        now: datetime | None = None,
    ) -> tuple[str, Question | None]:
        """Start a new session. Returns (session_id, first_question).

        first_question is None if the graph has no actionable candidates.
        """
        if now is None:
            now = datetime.now()

        session_id = uuid4().hex[:12]
        state = _SessionState(
            session_id=session_id,
            user_id=user_id,
            learner=learner,
            graph=graph,
            started_at=now,
        )
        self._sessions[session_id] = state

        # Find the first question
        question = self._advance(state, now)
        if question is None:
            state.finished = True
            state.ended_at = now

        return session_id, question

    def submit_answer(
        self,
        session_id: str,
        response: ResponseType,
        response_time_ms: int,
        now: datetime | None = None,
    ) -> AnswerResult:
        """Process an answer and return feedback + next question.

        Raises KeyError if session_id is unknown.
        Raises ValueError if session is already finished or no question is pending.
        """
        state = self._sessions[session_id]
        if state.finished:
            raise ValueError(f"Session {session_id} is already finished")
        if state.current_knoop is None:
            raise ValueError(f"No pending question for session {session_id}")

        if now is None:
            now = datetime.now()

        knoop = state.current_knoop
        knoop_id = knoop.id
        before = state.current_before

        # Process the response (BKT + SM-2 + conditional completion)
        _process_response(state.learner, state.graph, knoop_id, response, now)
        after = _get_state_posterior(state.learner, knoop_id)

        # Record results
        state.mastery_changes[knoop_id] = (before, after)
        state.session_node_ids.add(knoop_id)
        state.items_presented += 1

        # Track new vs review
        current_phase = PHASE_ORDER[state.phase_index]
        if before < MASTERY_THRESHOLD and current_phase == SessionPhase.NEW_MATERIAL:
            state.nodes_introduced.append(knoop_id)
        else:
            state.nodes_reviewed.append(knoop_id)

        # Consume time budget
        state.budget_remaining -= DEFAULT_ITEM_TIME_SEC

        # Remove answered knoop from current candidates
        state.candidates = [(s, k) for s, k in state.candidates if k.id != knoop_id]

        # Build feedback
        is_correct = response in (ResponseType.CORRECT, ResponseType.SLOW_CORRECT)
        feedback = Feedback(
            knoop_id=knoop_id,
            correct=is_correct,
            mastery_before=round(before, 3),
            mastery_after=round(after, 3),
        )

        # Advance to next question
        state.current_knoop = None
        next_q = self._advance(state, now)

        if next_q is None:
            self._finalize_session(state, now)
            return AnswerResult(feedback=feedback, session_finished=True)

        return AnswerResult(feedback=feedback, next_question=next_q)

    def get_summary(self, session_id: str) -> SessionSummary:
        """Return a session summary. Raises KeyError if unknown."""
        state = self._sessions[session_id]
        return SessionSummary(
            session_id=state.session_id,
            started_at=state.started_at.isoformat(),
            ended_at=state.ended_at.isoformat() if state.ended_at else "",
            total_items=state.items_presented,
            nodes_introduced=list(state.nodes_introduced),
            nodes_reviewed=list(state.nodes_reviewed),
            mastery_changes={k: v for k, v in state.mastery_changes.items()},
            phases_completed=list(state.phases_completed),
        )

    def get_session_state(self, session_id: str) -> _SessionState:
        """Access internal state (for persistence). Raises KeyError if unknown."""
        return self._sessions[session_id]

    def has_session(self, session_id: str) -> bool:
        return session_id in self._sessions

    # -- Internal helpers --

    def _advance(self, state: _SessionState, now: datetime) -> Question | None:
        """Find the next question, advancing phases as needed.

        Returns None when no more questions are available.
        """
        while state.phase_index < len(PHASE_ORDER):
            phase = PHASE_ORDER[state.phase_index]

            # If we haven't computed candidates for this phase yet, do so now
            if not state.candidates and state.budget_remaining <= 0:
                state.budget_remaining = PHASE_BUDGETS[phase]
                state.candidates = self._get_candidates(state, phase, now)

            # Try to select within current phase
            while state.budget_remaining > 0 and state.candidates:
                # Cap new-material introductions
                if (
                    phase == SessionPhase.NEW_MATERIAL
                    and len(state.nodes_introduced) >= MAX_NEW_NODES
                ):
                    break

                selected = select_next(state.candidates, state.ni_state)
                if selected is None:
                    break

                state.current_knoop = selected
                state.current_before = _get_state_posterior(state.learner, selected.id)
                return _knoop_to_question(selected, phase)

            # Phase exhausted — record and move on
            state.phases_completed.append(phase.value)
            state.phase_index += 1
            state.candidates = []
            state.budget_remaining = 0

        return None

    def _get_candidates(
        self, state: _SessionState, phase: SessionPhase, now: datetime
    ) -> list[tuple[float, KennisKnoop]]:
        """Compute candidate items for the given phase."""
        if phase == SessionPhase.WARMUP:
            return _candidates_for_warmup(state.learner, state.graph, now)
        elif phase == SessionPhase.NEW_MATERIAL:
            return _candidates_for_new_material(state.learner, state.graph)
        elif phase == SessionPhase.DEEPENING:
            return _candidates_for_deepening(
                state.learner, state.graph, state.nodes_introduced, now
            )
        else:  # COOLDOWN
            return _candidates_for_cooldown(
                state.learner, state.graph, state.session_node_ids, now
            )

    def _finalize_session(self, state: _SessionState, now: datetime) -> None:
        """Mark the session as finished, record in learner history."""
        state.finished = True
        state.ended_at = now

        # Collect offline assignments
        _collect_offline_items(state.graph, state.session_node_ids, now)

        # Record session in learner model
        state.learner.session_history.append(
            SessionRecord(
                session_id=state.session_id,
                started_at=state.started_at,
                ended_at=now,
                items_reviewed=list(state.session_node_ids),
            )
        )
