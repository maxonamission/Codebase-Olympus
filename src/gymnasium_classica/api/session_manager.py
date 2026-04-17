"""Step-by-step session protocol: the bridge between the API and the scheduling engine.

Decomposes run_session()'s synchronous loop into an async-compatible
request/response protocol:

  1. start_session() → session_id + first Question
  2. submit_answer() → AnswerResult (feedback + next question OR session end)
  3. get_summary()   → SessionSummary
"""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional
from uuid import uuid4

import networkx as nx

CONTENT_DIR = Path("data/content")

from gymnasium_classica.models.graph import Item, KennisKnoop
from gymnasium_classica.models.learner import (
    ItemResponse,
    LearnerModel,
    OfflineAssignment,
    ResponseType,
    SessionRecord,
)
from gymnasium_classica.models.passage import Passage
from gymnasium_classica.models.user import LearningRoute
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
    _candidates_for_new_material_context_first,
    _candidates_for_warmup,
    _collect_offline_items,
    _get_state_posterior,
    _process_response,
    select_passage,
)
from gymnasium_classica.scheduling.grading import canonical_expected_answer, grade_answer
from gymnasium_classica.scheduling.sm2 import sm2_update


# Learners get the "slow_correct" label when they answer correctly but
# took more than this factor times the item's expected duration.  Tuned
# loosely; can be revisited when telemetry is available.
SLOW_FACTOR: float = 1.5


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
    scaffolding_content: str | None = None
    # Promoted from the first item for frontend convenience. Populated by
    # `_knoop_to_question` so the React components can read a flat shape
    # (question.item_type / question.options / ...) without having to dig
    # into `question.items[0].stimulus`.
    item_type: str | None = None
    instruction: str | None = None
    options: list[str] | None = None
    hint: str | None = None
    audio_ref: str | None = None


@dataclass
class Feedback:
    """Feedback after answering a question."""

    knoop_id: str
    correct: bool
    response_type: str  # "correct", "slow_correct", or "incorrect"
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
    learning_route: LearningRoute = LearningRoute.GRAMMAR_FIRST
    show_grammar_scaffolding: bool = True
    passages: list[Passage] = field(default_factory=list)
    current_passage: Passage | None = None
    passage_presented: bool = False


def _generate_self_assess_prompt(knoop: KennisKnoop) -> str:
    """Generate a self-assessment prompt based on the node type."""
    t = knoop.type.value
    titel = knoop.titel_nl
    if t == "G":
        return f"Kun je het volgende uitleggen of opschrijven: {titel}?"
    elif t == "V":
        # V-node titles have format "lemma — translation". Show only the lemma
        # as the prompt so the learner has to recall the translation.
        if " — " in titel:
            lemma = titel.split(" — ")[0].strip()
            return f"Wat betekent: {lemma}?"
        return f"Ken je de betekenis van dit woord: {titel}?"
    elif t == "C":
        return f"Kun je het volgende uitleggen: {titel}?"
    else:
        return f"Beheers je het volgende concept: {titel}?"


def _build_item_response(
    *,
    item: Item | None,
    knoop: KennisKnoop,
    answer_text: str | None,
    correct: bool,
    response_time_ms: int,
    now: datetime,
) -> ItemResponse:
    """Construct an ItemResponse snapshotting knoop/item state at attempt-time."""
    return ItemResponse(
        timestamp=now,
        item_id=item.id if item is not None else f"{knoop.id}:self-assess",
        correct=correct,
        response_time_ms=response_time_ms,
        answer_text=answer_text,
        correct_answer=canonical_expected_answer(item) if item is not None else None,
        item_type=item.type.value if item is not None else None,
    )


def _grade_and_record(
    *,
    item: Item,
    knoop: KennisKnoop,
    answer_text: str,
    response_time_ms: int,
    now: datetime,
) -> tuple[ResponseType, ItemResponse]:
    """Grade a literal answer and produce the ItemResponse to record.

    Returns the derived ResponseType (with slow_correct when the learner
    took longer than :data:`SLOW_FACTOR` × the item's expected duration)
    and the ItemResponse that should be appended to item_history.
    """
    grading = grade_answer(answer_text, item, knoop.taal)
    if grading.correct:
        threshold_ms = int(SLOW_FACTOR * item.verwachte_tijd_sec * 1000)
        response = (
            ResponseType.SLOW_CORRECT
            if response_time_ms > threshold_ms
            else ResponseType.CORRECT
        )
    else:
        response = ResponseType.INCORRECT

    item_response = _build_item_response(
        item=item,
        knoop=knoop,
        answer_text=answer_text,
        correct=grading.correct,
        response_time_ms=response_time_ms,
        now=now,
    )
    return response, item_response


def _should_scaffold(
    state: "_SessionState",
    knoop: KennisKnoop,
    phase: SessionPhase,
) -> bool:
    """Decide whether to attach markdown-scaffolding to the next question.

    Rules (both routes):

    * Only during :class:`SessionPhase.NEW_MATERIAL`.
    * Only on the **first** introduction of the knoop for this learner —
      i.e. the knoop has no :class:`ItemResponse` entries in
      ``KnoopState.item_history`` yet.  This prevents scaffolding from
      re-appearing on SM-2 reviews.

    Path-specific gating:

    * **context-first**: scaffolding appears on grammar nodes that follow
      a passage reading step (existing behaviour, preserved).
    * **grammar-first**: opt-in via ``User.show_grammar_scaffolding``.
      The flag is threaded through on :meth:`SessionManager.start_session`
      and stored on ``_SessionState.show_grammar_scaffolding``.
    """
    if phase != SessionPhase.NEW_MATERIAL:
        return False

    knoop_state = state.learner.knoop_states.get(knoop.id)
    never_presented = knoop_state is None or len(knoop_state.item_history) == 0
    if not never_presented:
        return False

    if state.learning_route == LearningRoute.CONTEXT_FIRST:
        return state.passage_presented
    # grammar-first
    return state.show_grammar_scaffolding


def _passage_to_question(passage: Passage, phase: SessionPhase) -> Question:
    """Convert a Passage to a Question for the API.

    The stimulus is a dict with type="passage" so the frontend can
    distinguish it from a regular knoop question and render the
    PassageReader component.
    """
    return Question(
        knoop_id=passage.id,
        titel=passage.titel,
        beschrijving="Lees de passage en probeer de tekst te begrijpen.",
        stimulus={
            "type": "passage",
            "passage_id": passage.id,
            "taal": passage.taal.value,
            "tekst": passage.tekst,
            "annotaties": [a.model_dump() for a in passage.annotaties],
            "knoop_ids": passage.knoop_ids,
            "moeilijkheid": passage.moeilijkheid,
        },
        phase=phase.value,
    )


def _load_scaffolding_content(
    knoop: KennisKnoop,
    content_dir: Path = CONTENT_DIR,
) -> str | None:
    """Load markdown scaffolding content for a knowledge node.

    Looks for ``data/content/{knoop.id}.md`` (or the explicit
    ``content_ref`` path if set).  Returns the markdown string,
    or None when no content file exists.
    """
    if knoop.content_ref:
        path = Path(knoop.content_ref)
        if not path.is_absolute():
            path = content_dir.parent.parent / knoop.content_ref
    else:
        path = content_dir / f"{knoop.id}.md"

    if path.is_file():
        return path.read_text(encoding="utf-8")
    return None


def _knoop_to_question(
    knoop: KennisKnoop,
    phase: SessionPhase,
    include_scaffolding: bool = False,
    content_dir: Path = CONTENT_DIR,
) -> Question:
    """Convert a KennisKnoop to a Question for the API.

    When *include_scaffolding* is True (context-first scaffolding after
    a passage), the markdown content from ``data/content/`` is attached
    as ``scaffolding_content`` so the frontend can show an inline
    grammar explanation.
    """
    items = []
    for item in knoop.items:
        items.append({
            "id": item.id,
            "type": item.type.value,
            "stimulus": item.stimulus,
            "feedback": item.feedback,
            "verwachte_tijd_sec": item.verwachte_tijd_sec,
        })

    if knoop.items:
        stimulus = knoop.items[0].stimulus
    else:
        stimulus = _generate_self_assess_prompt(knoop)

    # For V-nodes: show only the lemma in the title, hide the translation
    titel = knoop.titel_nl
    if knoop.type.value == "V" and " — " in titel and not knoop.items:
        titel = titel.split(" — ")[0].strip()

    content = None
    if include_scaffolding:
        content = _load_scaffolding_content(knoop, content_dir)

    item_type, instruction, options, hint, audio_ref = _promote_first_item(knoop)

    return Question(
        knoop_id=knoop.id,
        titel=titel,
        beschrijving=knoop.beschrijving,
        stimulus=stimulus,
        phase=phase.value,
        items=items,
        scaffolding_content=content,
        item_type=item_type,
        instruction=instruction,
        options=options,
        hint=hint,
        audio_ref=audio_ref,
    )


def _promote_first_item(
    knoop: KennisKnoop,
) -> tuple[str | None, str | None, list[str] | None, str | None, str | None]:
    """Extract structured stimulus fields from the first item, if present.

    The frontend expects a flat Question shape: ``question.item_type``,
    ``question.options``, ``question.instruction``, ``question.hint``,
    ``question.audio_ref``.  This helper pulls those out of the first
    item so the React components don't need to understand the nested
    ``items[0].stimulus`` structure.

    Returns (item_type, instruction, options, hint, audio_ref).  Every
    field is None when the knoop has no items or when the field is
    absent on the first item.
    """
    if not knoop.items:
        return None, None, None, None, None

    first = knoop.items[0]
    item_type = first.type.value
    audio_ref = first.audio_ref

    instruction: str | None = None
    options: list[str] | None = None
    hint: str | None = None

    stim = first.stimulus
    if isinstance(stim, dict):
        raw_instruction = stim.get("instruction")
        if isinstance(raw_instruction, str):
            instruction = raw_instruction
        raw_options = stim.get("options")
        if isinstance(raw_options, list) and all(isinstance(o, str) for o in raw_options):
            options = list(raw_options)
        raw_hint = stim.get("hint")
        if isinstance(raw_hint, str):
            hint = raw_hint
        # audio_ref on the stimulus-dict wins over the item-level field
        # because generated vocabulary items put the filename there.
        stim_audio = stim.get("audio_ref")
        if isinstance(stim_audio, str):
            audio_ref = stim_audio

    return item_type, instruction, options, hint, audio_ref


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
        learning_route: LearningRoute = LearningRoute.GRAMMAR_FIRST,
        passages: list[Passage] | None = None,
        show_grammar_scaffolding: bool = True,
    ) -> tuple[str, Question | None]:
        """Start a new session. Returns (session_id, first_question).

        first_question is None if the graph has no actionable candidates.

        When *learning_route* is CONTEXT_FIRST and *passages* are provided,
        the new-material phase selects a passage instead of topological
        grammar nodes.

        *show_grammar_scaffolding* is the grammar-first-only opt-in
        (from ``User.show_grammar_scaffolding``): when True, the first
        introduction of a G-knoop in grammar-first includes its markdown
        scaffolding content.  Ignored on the context-first path, which
        always shows scaffolding after a passage.
        """
        if now is None:
            now = datetime.now()
        if passages is None:
            passages = []

        session_id = uuid4().hex[:12]
        state = _SessionState(
            session_id=session_id,
            user_id=user_id,
            learner=learner,
            graph=graph,
            started_at=now,
            learning_route=learning_route,
            show_grammar_scaffolding=show_grammar_scaffolding,
            passages=passages,
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
        response: ResponseType | None,
        response_time_ms: int,
        now: datetime | None = None,
        *,
        answer_text: str | None = None,
    ) -> AnswerResult:
        """Process an answer and return feedback + next question.

        Two paths:

        * *answer_text* is supplied → the server grades it against the
          current knoop's first item via :func:`grade_answer` and derives
          the ``ResponseType`` itself.  ``response`` may be ``None``.
        * *answer_text* is ``None`` → this is a self-assessment outcome;
          the caller tells us whether the learner reports themselves as
          correct/slow_correct/incorrect and ``response`` is required.

        Either way the raw answer and the expected answer at time of
        attempt are snapshotted on the resulting ``ItemResponse``.

        Raises KeyError if session_id is unknown.
        Raises ValueError if session is already finished or no question is pending.

        For passage questions (context-first reading step), BKT is skipped:
        the passage is not a knowledge node, so no mastery update occurs.
        """
        state = self._sessions[session_id]
        if state.finished:
            raise ValueError(f"Session {session_id} is already finished")

        if now is None:
            now = datetime.now()

        # --- Passage question handling (no BKT) ---
        if state.current_knoop is None and state.current_passage is not None:
            passage = state.current_passage
            state.items_presented += 1
            # Don't consume time budget for the passage reading step;
            # the full NEW_MATERIAL budget is reserved for the grammar
            # scaffolding nodes that follow.

            feedback = Feedback(
                knoop_id=passage.id,
                correct=True,
                response_type="passage_read",
                mastery_before=0.0,
                mastery_after=0.0,
            )

            # Advance to grammar scaffolding (next call to _advance
            # will compute candidates for the passage's nodes)
            next_q = self._advance(state, now)

            if next_q is None:
                self._finalize_session(state, now)
                return AnswerResult(feedback=feedback, session_finished=True)

            return AnswerResult(feedback=feedback, next_question=next_q)

        # --- Normal knoop question handling ---
        if state.current_knoop is None:
            raise ValueError(f"No pending question for session {session_id}")

        knoop = state.current_knoop
        knoop_id = knoop.id
        before = state.current_before

        # Derive the response from grading when a literal answer was
        # supplied; otherwise trust the self-assess value from the caller.
        item = knoop.items[0] if knoop.items else None
        if answer_text is not None:
            if item is None:
                # No gradeable item on this knoop — fall back to incorrect.
                response = ResponseType.INCORRECT
                item_response = _build_item_response(
                    item=None,
                    knoop=knoop,
                    answer_text=answer_text,
                    correct=False,
                    response_time_ms=response_time_ms,
                    now=now,
                )
            else:
                response, item_response = _grade_and_record(
                    item=item,
                    knoop=knoop,
                    answer_text=answer_text,
                    response_time_ms=response_time_ms,
                    now=now,
                )
        else:
            if response is None:
                raise ValueError(
                    "submit_answer requires either answer_text or response"
                )
            item_response = _build_item_response(
                item=item,
                knoop=knoop,
                answer_text=None,
                correct=response in (ResponseType.CORRECT, ResponseType.SLOW_CORRECT),
                response_time_ms=response_time_ms,
                now=now,
            )

        # Process the response (BKT + SM-2 + conditional completion)
        _process_response(
            state.learner,
            state.graph,
            knoop_id,
            response,
            now,
            item_response=item_response,
        )
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
            response_type=response.value,
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

        For context-first sessions, the new-material phase first presents
        a passage (reading step), then scaffolds the grammar nodes from
        that passage as individual questions.
        """
        while state.phase_index < len(PHASE_ORDER):
            phase = PHASE_ORDER[state.phase_index]

            # Context-first: present passage before grammar scaffolding
            if (
                phase == SessionPhase.NEW_MATERIAL
                and state.learning_route == LearningRoute.CONTEXT_FIRST
                and state.passages
                and not state.passage_presented
            ):
                passage = select_passage(
                    state.learner, state.graph, state.passages
                )
                if passage is not None:
                    state.current_passage = passage
                    state.passage_presented = True
                    state.current_knoop = None
                    # Don't set budget_remaining here: the passage is a
                    # reading step, not a timed item.  When _advance is
                    # called again after the passage answer, the normal
                    # "budget <= 0" check will initialise the phase with
                    # grammar candidates and the full time budget.
                    return _passage_to_question(passage, phase)
                # No suitable passage → fall through to normal flow

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

                scaffolding = _should_scaffold(state, selected, phase)
                return _knoop_to_question(
                    selected, phase, include_scaffolding=scaffolding
                )

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
            if (
                state.learning_route == LearningRoute.CONTEXT_FIRST
                and state.passages
            ):
                return _candidates_for_new_material_context_first(
                    state.learner, state.graph, state.passages
                )
            return _candidates_for_new_material(state.learner, state.graph)
        elif phase == SessionPhase.DEEPENING:
            # Context-first: deepen on passage-related nodes, not random urgency
            if (
                state.learning_route == LearningRoute.CONTEXT_FIRST
                and state.current_passage
            ):
                candidates = []
                for knoop_id in state.current_passage.knoop_ids:
                    if knoop_id not in state.graph.nodes:
                        continue
                    if knoop_id in state.session_node_ids:
                        continue  # already practiced this session
                    knoop = state.graph.nodes[knoop_id]["knoop"]
                    posterior = _get_state_posterior(state.learner, knoop_id)
                    if posterior < MASTERY_THRESHOLD:
                        candidates.append((0.8, knoop))
                if candidates:
                    return candidates
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

        # Collect offline assignments and attach them to the learner,
        # deduplicating on item_id against already-pending assignments.
        new_offline = _collect_offline_items(
            state.graph, state.session_node_ids, now
        )
        existing_item_ids = {
            a.item_id for a in state.learner.pending_offline_assignments
        }
        for assignment in new_offline:
            if assignment.item_id not in existing_item_ids:
                state.learner.pending_offline_assignments.append(assignment)

        # Record session in learner model
        state.learner.session_history.append(
            SessionRecord(
                session_id=state.session_id,
                started_at=state.started_at,
                ended_at=now,
                items_reviewed=list(state.session_node_ids),
                learning_route=state.learning_route.value,
            )
        )
