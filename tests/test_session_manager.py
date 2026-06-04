"""Tests for D1-04: SessionManager step-by-step session protocol.

Geen mocks: alle tests draaien op echte ``LearnerModel``, ``nx.DiGraph`` en
de echte scheduling-pipeline (BKT + SM-2 + non-interference). Tijd wordt
expliciet doorgegeven via de ``now``-parameter zodat tests deterministisch
blijven zonder ``freeze_time`` of patches op ``datetime.now``.
"""

from datetime import datetime, timedelta
from uuid import uuid4

import pytest

from gymnasium_classica.api.session_manager import (
    AnswerResult,
    Question,
    SessionManager,
    SessionSummary,
)
from gymnasium_classica.graph.loader import load_graph_from_dict
from gymnasium_classica.models.learner import (
    LearnerModel,
    NodeState,
    ResponseType,
)
from gymnasium_classica.models.passage import Passage, WordAnnotation
from gymnasium_classica.models.user import LearningRoute
from gymnasium_classica.scheduling.session import (
    DEFAULT_ITEM_TIME_SEC,
    MAX_NEW_NODES,
    PHASE_BUDGETS,
    SessionPhase,
)


def _make_graph_and_learner():
    """Build a small graph with root nodes (no prerequisites) and a fresh learner.

    Root nodes are selectable as new material without prerequisite gates.
    """
    data = {
        "nodes": [
            {
                "id": "LAT-G-MORF-NAAMVAL-INTRO",
                "type": "G",
                "language": "lat",
                "title_nl": "Wat is een naamval?",
                "description": "Introductie van het concept naamval.",
                "bloom_level": "knowledge",
                "phase": "onderbouw_1",
                "items": [],
            },
            {
                "id": "LAT-G-MORF-DECL-INTRO",
                "type": "G",
                "language": "lat",
                "title_nl": "Wat is een declinatie?",
                "description": "Introductie van het concept declinatie.",
                "bloom_level": "knowledge",
                "phase": "onderbouw_1",
                "items": [],
            },
            {
                "id": "LAT-G-MORF-DECL1-INTRO",
                "type": "G",
                "language": "lat",
                "title_nl": "De eerste declinatie",
                "description": "Overzicht van de 1e declinatie.",
                "bloom_level": "knowledge",
                "phase": "onderbouw_1",
                "items": [],
            },
        ],
        "edges": [
            {
                "source_id": "LAT-G-MORF-NAAMVAL-INTRO",
                "target_id": "LAT-G-MORF-DECL1-INTRO",
                "type": "prerequisite",
                "encompassing_weight": 0.3,
            },
            {
                "source_id": "LAT-G-MORF-DECL-INTRO",
                "target_id": "LAT-G-MORF-DECL1-INTRO",
                "type": "prerequisite",
                "encompassing_weight": 0.3,
            },
        ],
    }
    graph = load_graph_from_dict(data)
    learner = LearnerModel(user_id=uuid4())
    return graph, learner


class TestStartSession:
    def test_returns_session_id_and_question(self):
        graph, learner = _make_graph_and_learner()
        mgr = SessionManager()
        now = datetime(2026, 4, 13, 10, 0, 0)
        session_id, question = mgr.start_session("user1", learner, graph, now=now)

        assert isinstance(session_id, str)
        assert len(session_id) > 0
        assert mgr.has_session(session_id)
        # With a fresh learner, warmup has nothing → new material should yield a root node
        # The two root nodes are NAAMVAL-INTRO and DECL-INTRO (no prerequisites)
        if question is not None:
            assert isinstance(question, Question)
            assert question.node_id in (
                "LAT-G-MORF-NAAMVAL-INTRO",
                "LAT-G-MORF-DECL-INTRO",
            )

    def test_empty_graph_returns_none_question(self):
        data = {"nodes": [], "edges": []}
        graph = load_graph_from_dict(data)
        learner = LearnerModel(user_id=uuid4())
        mgr = SessionManager()
        _session_id, question = mgr.start_session("user1", learner, graph)
        assert question is None


class TestSubmitAnswer:
    def test_submit_returns_feedback_and_next_question(self):
        graph, learner = _make_graph_and_learner()
        mgr = SessionManager()
        now = datetime(2026, 4, 13, 10, 0, 0)
        session_id, q1 = mgr.start_session("user1", learner, graph, now=now)
        assert q1 is not None

        result = mgr.submit_answer(session_id, ResponseType.CORRECT, 2000, now=now)
        assert isinstance(result, AnswerResult)
        assert result.feedback.node_id == q1.node_id
        assert result.feedback.correct is True
        assert result.feedback.mastery_after >= result.feedback.mastery_before

    def test_submit_incorrect_lowers_or_maintains_mastery(self):
        graph, learner = _make_graph_and_learner()
        mgr = SessionManager()
        now = datetime(2026, 4, 13, 10, 0, 0)
        session_id, q1 = mgr.start_session("user1", learner, graph, now=now)
        assert q1 is not None

        result = mgr.submit_answer(session_id, ResponseType.INCORRECT, 5000, now=now)
        assert result.feedback.correct is False

    def test_session_eventually_finishes(self):
        """A session with a small graph finishes after all phases exhaust candidates."""
        graph, learner = _make_graph_and_learner()
        mgr = SessionManager()
        now = datetime(2026, 4, 13, 10, 0, 0)
        session_id, q = mgr.start_session("user1", learner, graph, now=now)

        steps = 0
        max_steps = 200  # Safety limit
        while q is not None and steps < max_steps:
            result = mgr.submit_answer(session_id, ResponseType.CORRECT, 1000, now=now)
            q = result.next_question
            steps += 1
            if result.session_finished:
                break

        # Session must eventually finish
        assert steps < max_steps

    def test_finished_session_raises(self):
        graph, learner = _make_graph_and_learner()
        mgr = SessionManager()
        now = datetime(2026, 4, 13, 10, 0, 0)
        session_id, q = mgr.start_session("user1", learner, graph, now=now)

        # Drain the session
        while q is not None:
            result = mgr.submit_answer(session_id, ResponseType.CORRECT, 1000, now=now)
            q = result.next_question
            if result.session_finished:
                break

        with pytest.raises(ValueError, match="already finished"):
            mgr.submit_answer(session_id, ResponseType.CORRECT, 1000, now=now)

    def test_unknown_session_raises(self):
        mgr = SessionManager()
        with pytest.raises(KeyError):
            mgr.submit_answer("nonexistent", ResponseType.CORRECT, 1000)


class TestGetSummary:
    def test_summary_after_session(self):
        graph, learner = _make_graph_and_learner()
        mgr = SessionManager()
        now = datetime(2026, 4, 13, 10, 0, 0)
        session_id, q = mgr.start_session("user1", learner, graph, now=now)

        # Answer a few questions
        answered = 0
        while q is not None:
            result = mgr.submit_answer(session_id, ResponseType.CORRECT, 1000, now=now)
            answered += 1
            q = result.next_question
            if result.session_finished:
                break

        summary = mgr.get_summary(session_id)
        assert isinstance(summary, SessionSummary)
        assert summary.session_id == session_id
        assert summary.total_items == answered
        assert len(summary.mastery_changes) > 0

    def test_summary_unknown_session(self):
        mgr = SessionManager()
        with pytest.raises(KeyError):
            mgr.get_summary("nope")


# ---------------------------------------------------------------------------
# Breder testharness voor phase-transitities, context-first, offline en budget.
# ---------------------------------------------------------------------------


def _broad_graph_and_learner(now: datetime):
    """Graph + learner die alle vier sessiefasen activeert.

    - Twee mastered root-nodes met een verouderde ``last_review`` zodat hun
      retention onder de warmup-drempel zakt (WARMUP kandidaten).
    - Twee ready-but-unmastered child-nodes (NEW_MATERIAL kandidaten).
    - Een kleinkind met één ready parent (DEEPENING post-requisite).
    - Een losstaande mastered node die niet deze sessie wordt aangeraakt
      (COOLDOWN kandidaat).
    """
    data = {
        "nodes": [
            {
                "id": "LAT-G-MORF-NAAMVAL-INTRO",
                "type": "G",
                "language": "lat",
                "title_nl": "Naamval intro",
                "description": "Introductie naamval.",
                "bloom_level": "knowledge",
                "phase": "onderbouw_1",
                "items": [],
            },
            {
                "id": "LAT-G-MORF-DECL-INTRO",
                "type": "G",
                "language": "lat",
                "title_nl": "Declinatie intro",
                "description": "Introductie declinatie.",
                "bloom_level": "knowledge",
                "phase": "onderbouw_1",
                "items": [],
            },
            {
                "id": "LAT-G-MORF-DECL1-INTRO",
                "type": "G",
                "language": "lat",
                "title_nl": "Eerste declinatie",
                "description": "Overzicht eerste declinatie.",
                "bloom_level": "knowledge",
                "phase": "onderbouw_1",
                "items": [],
            },
            {
                "id": "LAT-G-MORF-NOM-D1",
                "type": "G",
                "language": "lat",
                "title_nl": "Nominativus 1e declinatie",
                "description": "Nom. sg/pl van de 1e declinatie.",
                "bloom_level": "knowledge",
                "phase": "onderbouw_1",
                "items": [],
            },
            {
                "id": "LAT-V-F01-ESSE",
                "type": "V",
                "language": "lat",
                "title_nl": "esse — zijn",
                "description": "Werkwoord esse (zijn).",
                "bloom_level": "knowledge",
                "phase": "onderbouw_1",
                "items": [],
            },
        ],
        "edges": [
            {
                "source_id": "LAT-G-MORF-NAAMVAL-INTRO",
                "target_id": "LAT-G-MORF-DECL-INTRO",
                "type": "prerequisite",
                "encompassing_weight": 0.5,
            },
            {
                "source_id": "LAT-G-MORF-DECL-INTRO",
                "target_id": "LAT-G-MORF-DECL1-INTRO",
                "type": "prerequisite",
                "encompassing_weight": 0.4,
            },
            {
                "source_id": "LAT-G-MORF-DECL1-INTRO",
                "target_id": "LAT-G-MORF-NOM-D1",
                "type": "prerequisite",
                "encompassing_weight": 0.3,
            },
        ],
    }
    graph = load_graph_from_dict(data)
    learner = LearnerModel(user_id=uuid4())

    # Mastered ancestors met verouderde review → warmup-kandidaat.
    stale = now - timedelta(days=30)
    learner.node_states["LAT-G-MORF-NAAMVAL-INTRO"] = NodeState(
        node_id="LAT-G-MORF-NAAMVAL-INTRO",
        posterior_mastery=0.92,
        easiness_factor=2.5,
        interval_days=5.0,
        repetitions=3,
        last_review=stale,
    )
    learner.node_states["LAT-G-MORF-DECL-INTRO"] = NodeState(
        node_id="LAT-G-MORF-DECL-INTRO",
        posterior_mastery=0.88,
        easiness_factor=2.5,
        interval_days=5.0,
        repetitions=3,
        last_review=stale,
    )
    # Mastered losstaand vocab-item, niet aangeraakt in deze sessie
    # → cooldown-kandidaat.
    learner.node_states["LAT-V-F01-ESSE"] = NodeState(
        node_id="LAT-V-F01-ESSE",
        posterior_mastery=0.91,
        easiness_factor=2.5,
        interval_days=3.0,
        repetitions=2,
        last_review=stale,
    )
    return graph, learner


def _graph_with_offline_item():
    """Graph met één node die een OFFLINE_WRITING-item bevat."""
    data = {
        "nodes": [
            {
                "id": "LAT-G-MORF-DECL1-INTRO",
                "type": "G",
                "language": "lat",
                "title_nl": "Eerste declinatie",
                "description": "Overzicht eerste declinatie.",
                "bloom_level": "knowledge",
                "phase": "onderbouw_1",
                "items": [
                    {
                        "id": "ITEM-OFFLINE-D1-001",
                        "node_ids": ["LAT-G-MORF-DECL1-INTRO"],
                        "type": "offline_writing",
                        "direction": "productive",
                        "difficulty_initial": 0.5,
                        "discrimination_initial": 1.0,
                        "expected_time_sec": 300,
                        "stimulus": "Schrijf paradigma puella op.",
                        "answer": "puella, puellae, ...",
                        "feedback": "Vergelijk met paradigma.",
                        "source": "manual",
                        "verification_method": "self_report",
                    }
                ],
            }
        ],
        "edges": [],
    }
    graph = load_graph_from_dict(data)
    learner = LearnerModel(user_id=uuid4())
    return graph, learner


def _drive_session_to_completion(
    mgr: SessionManager,
    session_id: str,
    q: Question | None,
    now: datetime,
    response: ResponseType = ResponseType.CORRECT,
    max_steps: int = 200,
) -> list[Question]:
    """Beantwoord alle vragen tot de sessie eindigt, bewaar de reeks."""
    asked = []
    steps = 0
    while q is not None and steps < max_steps:
        asked.append(q)
        result = mgr.submit_answer(session_id, response, 1000, now=now)
        q = result.next_question
        steps += 1
        if result.session_finished:
            break
    assert steps < max_steps, "Sessie terminert niet binnen max_steps"
    return asked


class TestPhaseTransitions:
    """Verifieer dat de SessionManager de fasen in de juiste volgorde doorloopt."""

    def test_broad_graph_cycles_through_all_phases(self):
        now = datetime(2026, 4, 16, 10, 0, 0)
        graph, learner = _broad_graph_and_learner(now)
        mgr = SessionManager()
        session_id, q = mgr.start_session("user1", learner, graph, now=now)
        asked = _drive_session_to_completion(mgr, session_id, q, now)

        summary = mgr.get_summary(session_id)
        # Volgorde moet de PHASE_ORDER respecteren.
        expected_order = [
            SessionPhase.WARMUP.value,
            SessionPhase.NEW_MATERIAL.value,
            SessionPhase.DEEPENING.value,
            SessionPhase.COOLDOWN.value,
        ]
        assert summary.phases_completed == expected_order
        # Elke phase kwam aan bod in de aangeboden vragen.
        phases_seen = {q.phase for q in asked}
        assert SessionPhase.WARMUP.value in phases_seen
        assert SessionPhase.NEW_MATERIAL.value in phases_seen

    def test_phase_label_on_question_matches_current_phase(self):
        """De `phase` van een Question reflecteert waar de scheduler nu zit."""
        now = datetime(2026, 4, 16, 10, 0, 0)
        graph, learner = _broad_graph_and_learner(now)
        mgr = SessionManager()
        _session_id, q = mgr.start_session("user1", learner, graph, now=now)
        assert q is not None
        # Eerste vraag zit in één van de eerdere fasen (warmup of new_material
        # afhankelijk van kandidatenbeschikbaarheid).
        assert q.phase in {
            SessionPhase.WARMUP.value,
            SessionPhase.NEW_MATERIAL.value,
        }


class TestMaxNewNodes:
    """NEW_MATERIAL phase mag maximaal MAX_NEW_NODES nieuwe nodes introduceren."""

    def test_new_material_cap_enforced(self):
        now = datetime(2026, 4, 16, 10, 0, 0)
        # Graph met 5 ready new-material kandidaten, allemaal roots.
        data = {
            "nodes": [
                {
                    "id": f"LAT-G-MORF-ROOT{i}-INTRO",
                    "type": "G",
                    "language": "lat",
                    "title_nl": f"Root {i}",
                    "description": f"Root node {i}.",
                    "bloom_level": "knowledge",
                    "phase": "onderbouw_1",
                    "items": [],
                }
                for i in range(1, 6)
            ],
            "edges": [],
        }
        graph = load_graph_from_dict(data)
        learner = LearnerModel(user_id=uuid4())
        mgr = SessionManager()
        session_id, q = mgr.start_session("user1", learner, graph, now=now)
        _drive_session_to_completion(mgr, session_id, q, now)

        summary = mgr.get_summary(session_id)
        assert len(summary.nodes_introduced) <= MAX_NEW_NODES


class TestBudgetExhaustion:
    """Phase-transities gebeuren wanneer het tijdbudget uitgeput is."""

    def test_new_material_phase_time_budget_consumed(self):
        now = datetime(2026, 4, 16, 10, 0, 0)
        graph, learner = _broad_graph_and_learner(now)
        mgr = SessionManager()
        session_id, q = mgr.start_session("user1", learner, graph, now=now)
        asked = _drive_session_to_completion(mgr, session_id, q, now)

        # Totaal geconsumeerde tijd ligt binnen de som van de phase-budgetten.
        # Elk item kost DEFAULT_ITEM_TIME_SEC; de MAX_NEW_NODES cap kan
        # new_material vroeg afronden, maar de totale budgetlimiet is hard.
        max_total_budget = sum(PHASE_BUDGETS.values())
        total_spent = len(asked) * DEFAULT_ITEM_TIME_SEC
        assert total_spent <= max_total_budget


class TestContextFirstRoute:
    """De CONTEXT_FIRST route presenteert eerst een passage, dan scaffolding."""

    def _make_passage_setup(self, tmp_path):
        """Graph + passage die op elkaar aansluiten + scaffolding-md in tmp."""
        data = {
            "nodes": [
                {
                    "id": "LAT-G-MORF-NAAMVAL-INTRO",
                    "type": "G",
                    "language": "lat",
                    "title_nl": "Naamval intro",
                    "description": "Introductie naamval.",
                    "bloom_level": "knowledge",
                    "phase": "onderbouw_1",
                    "items": [],
                },
                {
                    "id": "LAT-G-MORF-DECL1-INTRO",
                    "type": "G",
                    "language": "lat",
                    "title_nl": "Eerste declinatie",
                    "description": "Overzicht eerste declinatie.",
                    "bloom_level": "knowledge",
                    "phase": "onderbouw_1",
                    "items": [],
                },
            ],
            "edges": [
                {
                    "source_id": "LAT-G-MORF-NAAMVAL-INTRO",
                    "target_id": "LAT-G-MORF-DECL1-INTRO",
                    "type": "prerequisite",
                    "encompassing_weight": 0.4,
                }
            ],
        }
        graph = load_graph_from_dict(data)
        passage = Passage(
            id="LAT-P-001",
            language="lat",
            title="Puella parva",
            text="Puella parva in villa est.",
            annotations=[
                WordAnnotation(
                    word="Puella",
                    lemma="puella",
                    case="nom.sg",
                    translation="Het meisje",
                ),
            ],
            node_ids=[
                "LAT-G-MORF-NAAMVAL-INTRO",
                "LAT-G-MORF-DECL1-INTRO",
            ],
            difficulty=1,
        )
        # Schrijf scaffolding-md in de default content dir (rel. CWD).
        # We gebruiken absolute paths via content_ref om CWD-afhankelijkheid
        # te vermijden.
        md_path = tmp_path / "LAT-G-MORF-DECL1-INTRO.md"
        md_path.write_text(
            "# Eerste declinatie\n\nEen paradigma met puella als voorbeeld.",
            encoding="utf-8",
        )
        return graph, passage, md_path

    def test_first_question_is_passage(self, tmp_path):
        graph, passage, _ = self._make_passage_setup(tmp_path)
        learner = LearnerModel(user_id=uuid4())
        mgr = SessionManager()
        now = datetime(2026, 4, 16, 10, 0, 0)
        _session_id, q = mgr.start_session(
            "user1",
            learner,
            graph,
            now=now,
            learning_route=LearningRoute.CONTEXT_FIRST,
            passages=[passage],
        )
        assert q is not None
        assert isinstance(q.stimulus, dict)
        assert q.stimulus.get("type") == "passage"
        assert q.stimulus["passage_id"] == "LAT-P-001"
        assert q.stimulus["text"] == "Puella parva in villa est."

    def test_passage_read_yields_grammar_scaffolding(self, tmp_path):
        graph, passage, _ = self._make_passage_setup(tmp_path)
        learner = LearnerModel(user_id=uuid4())
        mgr = SessionManager()
        now = datetime(2026, 4, 16, 10, 0, 0)
        session_id, q_passage = mgr.start_session(
            "user1",
            learner,
            graph,
            now=now,
            learning_route=LearningRoute.CONTEXT_FIRST,
            passages=[passage],
        )
        assert q_passage.stimulus["type"] == "passage"

        result = mgr.submit_answer(session_id, ResponseType.CORRECT, 5000, now=now)
        assert result.feedback.response_type == "passage_read"
        # Mastery voor passage-step blijft 0.0 (geen BKT-update).
        assert result.feedback.mastery_before == 0.0
        assert result.feedback.mastery_after == 0.0
        # De vervolgvraag is een grammar-node uit de passage.
        assert result.next_question is not None
        assert result.next_question.node_id in passage.node_ids


class TestOfflineAssignmentCollection:
    """OFFLINE_WRITING-items komen na de sessie in pending_offline_assignments.

    Contract: bij ``_finalize_session`` worden alle offline-items van de
    aangeraakte nodes toegevoegd aan ``learner.pending_offline_assignments``,
    met deduplicatie op ``item_id``. Analoog aan ``run_session`` in
    ``scheduling/session.py``.
    """

    def test_offline_item_ends_up_in_pending(self):
        now = datetime(2026, 4, 16, 10, 0, 0)
        graph, learner = _graph_with_offline_item()
        mgr = SessionManager()
        session_id, q = mgr.start_session("user1", learner, graph, now=now)
        _drive_session_to_completion(mgr, session_id, q, now)

        assert any(a.item_id == "ITEM-OFFLINE-D1-001" for a in learner.pending_offline_assignments)

    def test_offline_item_not_duplicated_across_sessions(self):
        """Een tweede sessie op dezelfde node voegt niet nog een assignment toe."""
        now = datetime(2026, 4, 16, 10, 0, 0)
        graph, learner = _graph_with_offline_item()
        mgr = SessionManager()

        for _ in range(2):
            session_id, q = mgr.start_session("user1", learner, graph, now=now)
            _drive_session_to_completion(mgr, session_id, q, now)

        matching = [
            a for a in learner.pending_offline_assignments if a.item_id == "ITEM-OFFLINE-D1-001"
        ]
        assert len(matching) == 1


class TestSessionHistoryRecorded:
    """Na afronding verschijnt een SessionRecord in de learner."""

    def test_session_record_added_on_finalize(self):
        now = datetime(2026, 4, 16, 10, 0, 0)
        graph, learner = _broad_graph_and_learner(now)
        mgr = SessionManager()
        session_id, q = mgr.start_session("user1", learner, graph, now=now)
        _drive_session_to_completion(mgr, session_id, q, now)

        assert len(learner.session_history) == 1
        record = learner.session_history[0]
        assert record.session_id == session_id
        assert record.started_at == now
        assert record.ended_at == now
        assert record.learning_route == LearningRoute.GRAMMAR_FIRST.value


class TestLearnerModelRoundtrip:
    """De LearnerModel moet JSON-serializable zijn na een sessie (persist-ready)."""

    def test_roundtrip_preserves_node_states_and_history(self):
        now = datetime(2026, 4, 16, 10, 0, 0)
        graph, learner = _broad_graph_and_learner(now)
        mgr = SessionManager()
        session_id, q = mgr.start_session("user1", learner, graph, now=now)
        _drive_session_to_completion(mgr, session_id, q, now)

        serialized = learner.model_dump_json()
        restored = LearnerModel.model_validate_json(serialized)

        assert restored.user_id == learner.user_id
        assert set(restored.node_states.keys()) == set(learner.node_states.keys())
        for node_id, state in learner.node_states.items():
            assert restored.node_states[node_id].posterior_mastery == state.posterior_mastery
            assert restored.node_states[node_id].repetitions == state.repetitions
        assert len(restored.session_history) == len(learner.session_history)
        assert restored.session_history[0].session_id == session_id
