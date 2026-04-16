"""Session orchestration: run a 30-minute adaptive learning session.

A session has four phases:
  1. Warming-up (5 min)  — quick retrieval of material near forgetting threshold
  2. New material (10 min) — introduce 1-2 new nodes whose prerequisites are green
  3. Deepening (10 min)  — contextual exercises combining new and known material
  4. Cool-down (5 min)   — spaced repetition review of older material
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from typing import Callable
from uuid import uuid4

import networkx as nx

from gymnasium_classica.diagnostic.conditional_completion import apply_fallback
from gymnasium_classica.models.graph import ItemType, KennisKnoop
from gymnasium_classica.models.learner import (
    LearnerModel,
    MasterySource,
    OfflineAssignment,
    ResponseType,
    SelfReportResponse,
    SessionRecord,
)
from gymnasium_classica.scheduling.bkt import (
    SELF_REPORT_BKT_PARAMS,
    propagate_practice_correct,
    update_knoop_state,
)
from gymnasium_classica.scheduling.non_interference import (
    NonInterferenceState,
    select_next,
)
from gymnasium_classica.models.passage import Passage
from gymnasium_classica.models.user import LearningRoute
from gymnasium_classica.scheduling.priority import (
    MASTERY_THRESHOLD,
    PREREQ_READY_THRESHOLD,
    compute_urgency_scores,
    estimate_retention,
    forget_urgency,
    readiness_score,
)
from gymnasium_classica.scheduling.sm2 import sm2_update


class SessionPhase(StrEnum):
    WARMUP = "warmup"
    NEW_MATERIAL = "new_material"
    DEEPENING = "deepening"
    COOLDOWN = "cooldown"


# Phase time budgets (seconds), total = 1800s (30 min)
PHASE_BUDGETS: dict[SessionPhase, int] = {
    SessionPhase.WARMUP: 300,
    SessionPhase.NEW_MATERIAL: 600,
    SessionPhase.DEEPENING: 600,
    SessionPhase.COOLDOWN: 300,
}

PHASE_ORDER = [
    SessionPhase.WARMUP,
    SessionPhase.NEW_MATERIAL,
    SessionPhase.DEEPENING,
    SessionPhase.COOLDOWN,
]

MAX_NEW_NODES = 2
DEFAULT_ITEM_TIME_SEC = 30
REVIEW_RETENTION_THRESHOLD = 0.85
CONTEXT_FIRST_PREREQ_THRESHOLD = 0.25

# Type alias for the answer callback
AnswerFn = Callable[[str, KennisKnoop], tuple[ResponseType, int]]


@dataclass
class SessionItem:
    """A single item presented during a session."""

    knoop_id: str
    phase: SessionPhase
    response: ResponseType | None = None
    response_time_ms: int | None = None


@dataclass
class SessionResult:
    """Summary of a completed session."""

    session_id: str = ""
    started_at: datetime | None = None
    ended_at: datetime | None = None
    items: list[SessionItem] = field(default_factory=list)
    nodes_introduced: list[str] = field(default_factory=list)
    nodes_reviewed: list[str] = field(default_factory=list)
    mastery_changes: dict[str, tuple[float, float]] = field(default_factory=dict)
    offline_assignments: list[OfflineAssignment] = field(default_factory=list)
    follow_ups: list[OfflineAssignment] = field(default_factory=list)


def _get_state_posterior(learner: LearnerModel, knoop_id: str) -> float:
    state = learner.knoop_states.get(knoop_id)
    return state.posterior_mastery if state else 0.10


def _candidates_for_warmup(
    learner: LearnerModel,
    graph: nx.DiGraph,
    now: datetime,
) -> list[tuple[float, KennisKnoop]]:
    """Mastered nodes approaching forgetting threshold."""
    candidates = []
    for node_id in graph.nodes:
        state = learner.knoop_states.get(node_id)
        if state is None or state.posterior_mastery < MASTERY_THRESHOLD:
            continue
        retention = estimate_retention(state, now)
        if retention < REVIEW_RETENTION_THRESHOLD:
            urgency = forget_urgency(state, now)
            knoop: KennisKnoop = graph.nodes[node_id]["knoop"]
            candidates.append((urgency, knoop))
    candidates.sort(key=lambda x: x[0], reverse=True)
    return candidates


def _candidates_for_new_material(
    learner: LearnerModel,
    graph: nx.DiGraph,
) -> list[tuple[float, KennisKnoop]]:
    """Unmastered nodes with all prerequisites green, sorted by pedagogical value."""
    candidates = []
    max_out_deg = max((graph.out_degree(n) for n in graph.nodes), default=1) or 1

    for node_id in graph.nodes:
        posterior = _get_state_posterior(learner, node_id)
        if posterior >= MASTERY_THRESHOLD:
            continue
        ready = readiness_score(node_id, learner, graph)
        if ready == 0.0:
            continue
        out_deg = graph.out_degree(node_id) / max_out_deg
        # Combine readiness and pedagogical value
        score = 0.6 * ready + 0.4 * out_deg
        knoop: KennisKnoop = graph.nodes[node_id]["knoop"]
        candidates.append((score, knoop))

    candidates.sort(key=lambda x: x[0], reverse=True)
    return candidates


def select_passage(
    learner: LearnerModel,
    graph: nx.DiGraph,
    passages: list[Passage],
) -> Passage | None:
    """Select a passage for context-first new-material phase.

    Picks the best passage whose grammar/vocabulary nodes are at the
    learner's knowledge frontier: not yet mastered, but reachable with
    a relaxed prerequisite threshold (CONTEXT_FIRST_PREREQ_THRESHOLD).

    Passages are scored by the number of exercised nodes that are both
    unmastered and reachable. Higher difficulty passages are penalised
    slightly to prefer accessible material first.

    Returns None if no suitable passage is found.
    """
    best_passage: Passage | None = None
    best_score = -1.0

    for passage in passages:
        reachable_unmastered = 0
        total_relevant = 0
        passage_knoop_set = set(passage.knoop_ids)

        for knoop_id in passage.knoop_ids:
            if knoop_id not in graph.nodes:
                continue
            total_relevant += 1
            posterior = _get_state_posterior(learner, knoop_id)
            if posterior >= MASTERY_THRESHOLD:
                continue  # already mastered, doesn't count

            # In context-first, a node is reachable if:
            # 1. It has no prerequisites (root node), OR
            # 2. Its prerequisites pass the relaxed threshold, OR
            # 3. All its prerequisites are also in this passage
            #    (the passage introduces them together)
            preds = list(graph.predecessors(knoop_id))
            if not preds:
                reachable_unmastered += 1
            elif all(p in passage_knoop_set for p in preds):
                reachable_unmastered += 1
            else:
                ready = readiness_score(
                    knoop_id, learner, graph,
                    prereq_threshold=CONTEXT_FIRST_PREREQ_THRESHOLD,
                )
                if ready > 0.0:
                    reachable_unmastered += 1

        if reachable_unmastered == 0:
            continue

        # Score: fraction of relevant nodes that are frontier nodes,
        # with a small penalty for higher difficulty
        coverage = reachable_unmastered / max(total_relevant, 1)
        difficulty_penalty = (passage.moeilijkheid - 1) * 0.05
        score = coverage - difficulty_penalty

        if score > best_score:
            best_score = score
            best_passage = passage

    return best_passage


def _candidates_for_new_material_context_first(
    learner: LearnerModel,
    graph: nx.DiGraph,
    passages: list[Passage],
) -> list[tuple[float, KennisKnoop]]:
    """New-material candidates for context-first route.

    Selects a passage via select_passage(), then returns the passage's
    grammar/vocabulary nodes as candidates with a relaxed prerequisite
    threshold (0.25 instead of 0.75).
    """
    passage = select_passage(learner, graph, passages)
    if passage is None:
        return []

    candidates = []
    max_out_deg = max((graph.out_degree(n) for n in graph.nodes), default=1) or 1

    for knoop_id in passage.knoop_ids:
        if knoop_id not in graph.nodes:
            continue
        posterior = _get_state_posterior(learner, knoop_id)
        if posterior >= MASTERY_THRESHOLD:
            continue
        ready = readiness_score(
            knoop_id, learner, graph,
            prereq_threshold=CONTEXT_FIRST_PREREQ_THRESHOLD,
        )
        if ready == 0.0:
            continue
        out_deg = graph.out_degree(knoop_id) / max_out_deg
        score = 0.6 * ready + 0.4 * out_deg
        knoop: KennisKnoop = graph.nodes[knoop_id]["knoop"]
        candidates.append((score, knoop))

    candidates.sort(key=lambda x: x[0], reverse=True)
    return candidates


def _candidates_for_deepening(
    learner: LearnerModel,
    graph: nx.DiGraph,
    new_node_ids: list[str],
    now: datetime,
) -> list[tuple[float, KennisKnoop]]:
    """Post-requisites of newly introduced nodes, plus general urgency candidates."""
    candidates = []
    # Post-requisites of new nodes
    for new_id in new_node_ids:
        for succ in graph.successors(new_id):
            knoop: KennisKnoop = graph.nodes[succ]["knoop"]
            posterior = _get_state_posterior(learner, succ)
            if posterior < MASTERY_THRESHOLD:
                ready = readiness_score(succ, learner, graph)
                if ready > 0:
                    candidates.append((0.8, knoop))

    # Also include general high-urgency items
    all_scores = compute_urgency_scores(learner, graph, now=now)
    for score, knoop in all_scores[:10]:
        if knoop.id not in new_node_ids:
            candidates.append((score * 0.7, knoop))

    candidates.sort(key=lambda x: x[0], reverse=True)
    return candidates


def _candidates_for_cooldown(
    learner: LearnerModel,
    graph: nx.DiGraph,
    session_node_ids: set[str],
    now: datetime,
) -> list[tuple[float, KennisKnoop]]:
    """Mastered nodes not yet reviewed in this session."""
    candidates = []
    for node_id in graph.nodes:
        if node_id in session_node_ids:
            continue
        state = learner.knoop_states.get(node_id)
        if state is None or state.posterior_mastery < MASTERY_THRESHOLD:
            continue
        urgency = forget_urgency(state, now)
        knoop: KennisKnoop = graph.nodes[node_id]["knoop"]
        candidates.append((urgency, knoop))
    candidates.sort(key=lambda x: x[0], reverse=True)
    return candidates


def _process_response(
    learner: LearnerModel,
    graph: nx.DiGraph,
    knoop_id: str,
    response: ResponseType,
    now: datetime,
) -> None:
    """Run BKT update, SM-2 update, and conditional completion check."""
    # BKT
    update_knoop_state(learner, knoop_id, response)
    if response in (ResponseType.CORRECT, ResponseType.SLOW_CORRECT):
        propagate_practice_correct(learner, graph, knoop_id)

    # SM-2
    state = learner.knoop_states[knoop_id]
    sm2_update(state, response, review_time=now)

    # Conditional completion: fallback for diagnostic-sourced failures
    if response == ResponseType.INCORRECT:
        if state.source == MasterySource.DIAGNOSTIC:
            apply_fallback(learner, graph, knoop_id)


def _collect_offline_items(
    graph: nx.DiGraph,
    session_node_ids: set[str],
    now: datetime,
) -> list[OfflineAssignment]:
    """Identify offline_schrijven items for nodes practiced in this session."""
    assignments: list[OfflineAssignment] = []
    for node_id in session_node_ids:
        if node_id not in graph.nodes:
            continue
        knoop: KennisKnoop = graph.nodes[node_id]["knoop"]
        for item in knoop.items:
            if item.type == ItemType.OFFLINE_SCHRIJVEN:
                assignments.append(
                    OfflineAssignment(
                        knoop_id=node_id,
                        item_id=item.id,
                        assigned_at=now,
                    )
                )
    return assignments


def _pending_follow_ups(learner: LearnerModel) -> list[OfflineAssignment]:
    """Return uncompleted offline assignments that need a follow-up question."""
    return [a for a in learner.pending_offline_assignments if not a.completed]


def process_self_report(
    learner: LearnerModel,
    assignment: OfflineAssignment,
    response: SelfReportResponse,
) -> None:
    """Process a self-reported outcome for an offline writing assignment.

    Maps SelfReportResponse to a BKT-compatible correct/incorrect and
    updates the learner state using SELF_REPORT_BKT_PARAMS (higher P(G)
    and P(S) to reflect reduced confidence in self-reported results).

    - CORRECT → BKT correct
    - PARTIAL → BKT correct (but the higher P(G)=0.35 tempers the update)
    - INCORRECT → BKT incorrect
    """
    correct_for_bkt = response in (
        SelfReportResponse.CORRECT,
        SelfReportResponse.PARTIAL,
    )
    bkt_response = ResponseType.CORRECT if correct_for_bkt else ResponseType.INCORRECT

    update_knoop_state(
        learner,
        assignment.knoop_id,
        bkt_response,
        params=SELF_REPORT_BKT_PARAMS,
    )

    # Mark mastery source as self-report
    state = learner.knoop_states[assignment.knoop_id]
    state.source = MasterySource.SELF_REPORT

    # Mark assignment as completed
    assignment.completed = True

    # Track self-report ratio
    learner.self_report_count += 1


def run_session(
    learner: LearnerModel,
    graph: nx.DiGraph,
    answer_fn: AnswerFn,
    session_id: str | None = None,
    now: datetime | None = None,
    learning_route: LearningRoute = LearningRoute.GRAMMAR_FIRST,
    passages: list[Passage] | None = None,
) -> SessionResult:
    """Orchestrate a complete 30-minute learning session.

    *answer_fn(knoop_id, knoop)* returns ``(ResponseType, response_time_ms)``.

    When *learning_route* is CONTEXT_FIRST the new-material phase selects
    a passage instead of picking grammar nodes topologically.  The
    prerequisite gate is relaxed (threshold 0.25 instead of 0.75) for
    nodes introduced via a passage.
    """
    if now is None:
        now = datetime.now()
    if session_id is None:
        session_id = str(uuid4())[:8]
    if passages is None:
        passages = []

    result = SessionResult(session_id=session_id, started_at=now)

    # Surface pending offline assignments as follow-ups for this session
    result.follow_ups = _pending_follow_ups(learner)

    ni_state = NonInterferenceState()
    session_node_ids: set[str] = set()
    session_type_counts: dict[str, int] = {}

    for phase in PHASE_ORDER:
        budget_remaining = PHASE_BUDGETS[phase]

        if phase == SessionPhase.WARMUP:
            candidates = _candidates_for_warmup(learner, graph, now)
        elif phase == SessionPhase.NEW_MATERIAL:
            if (
                learning_route == LearningRoute.CONTEXT_FIRST
                and passages
            ):
                candidates = _candidates_for_new_material_context_first(
                    learner, graph, passages
                )
            else:
                candidates = _candidates_for_new_material(learner, graph)
        elif phase == SessionPhase.DEEPENING:
            candidates = _candidates_for_deepening(
                learner, graph, result.nodes_introduced, now
            )
        else:  # COOLDOWN
            candidates = _candidates_for_cooldown(
                learner, graph, session_node_ids, now
            )

        if not candidates:
            continue

        items_in_phase = 0
        new_count = len(result.nodes_introduced)

        while budget_remaining > 0 and candidates:
            selected = select_next(candidates, ni_state)
            if selected is None:
                break

            # For new material phase, cap at MAX_NEW_NODES
            if phase == SessionPhase.NEW_MATERIAL:
                if new_count >= MAX_NEW_NODES:
                    break

            knoop_id = selected.id
            before = _get_state_posterior(learner, knoop_id)

            # Get response from learner
            response, time_ms = answer_fn(knoop_id, selected)

            # Process the response (BKT + SM-2 + fallback)
            _process_response(learner, graph, knoop_id, response, now)

            after = _get_state_posterior(learner, knoop_id)

            # Record
            item = SessionItem(
                knoop_id=knoop_id,
                phase=phase,
                response=response,
                response_time_ms=time_ms,
            )
            result.items.append(item)
            result.mastery_changes[knoop_id] = (before, after)
            session_node_ids.add(knoop_id)

            # Track domain balance
            domain = selected.type.value
            session_type_counts[domain] = session_type_counts.get(domain, 0) + 1

            # Track new vs review
            if before < MASTERY_THRESHOLD and phase == SessionPhase.NEW_MATERIAL:
                result.nodes_introduced.append(knoop_id)
                new_count += 1
            else:
                result.nodes_reviewed.append(knoop_id)

            # Time accounting
            item_time = DEFAULT_ITEM_TIME_SEC
            budget_remaining -= item_time
            items_in_phase += 1

            # Remove selected from current candidates to avoid re-selection
            candidates = [(s, k) for s, k in candidates if k.id != knoop_id]

    # Schedule offline assignments at end of session
    new_offline = _collect_offline_items(graph, session_node_ids, now)
    # Avoid duplicating assignments already pending for the same item
    existing_item_ids = {a.item_id for a in learner.pending_offline_assignments}
    for assignment in new_offline:
        if assignment.item_id not in existing_item_ids:
            learner.pending_offline_assignments.append(assignment)
            result.offline_assignments.append(assignment)

    # Record session in learner history
    result.ended_at = now
    learner.session_history.append(
        SessionRecord(
            session_id=session_id,
            started_at=now,
            ended_at=now,
            items_reviewed=[item.knoop_id for item in result.items],
            learning_route=learning_route.value,
        )
    )

    return result
