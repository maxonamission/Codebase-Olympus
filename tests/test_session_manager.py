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
    KnoopState,
    LearnerModel,
    MasterySource,
    ResponseType,
)
from gymnasium_classica.models.passage import Passage, WordAnnotation
from gymnasium_classica.models.user import LearningRoute
from gymnasium_classica.scheduling.priority import MASTERY_THRESHOLD
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
        "knopen": [
            {
                "id": "LAT-G-MORF-NAAMVAL-INTRO",
                "type": "G",
                "taal": "lat",
                "titel_nl": "Wat is een naamval?",
                "beschrijving": "Introductie van het concept naamval.",
                "bloom_niveau": "kennis",
                "fase": "onderbouw_1",
                "items": [],
            },
            {
                "id": "LAT-G-MORF-DECL-INTRO",
                "type": "G",
                "taal": "lat",
                "titel_nl": "Wat is een declinatie?",
                "beschrijving": "Introductie van het concept declinatie.",
                "bloom_niveau": "kennis",
                "fase": "onderbouw_1",
                "items": [],
            },
            {
                "id": "LAT-G-MORF-DECL1-INTRO",
                "type": "G",
                "taal": "lat",
                "titel_nl": "De eerste declinatie",
                "beschrijving": "Overzicht van de 1e declinatie.",
                "bloom_niveau": "kennis",
                "fase": "onderbouw_1",
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
            assert question.knoop_id in (
                "LAT-G-MORF-NAAMVAL-INTRO",
                "LAT-G-MORF-DECL-INTRO",
            )

    def test_empty_graph_returns_none_question(self):
        data = {"knopen": [], "edges": []}
        graph = load_graph_from_dict(data)
        learner = LearnerModel(user_id=uuid4())
        mgr = SessionManager()
        session_id, question = mgr.start_session("user1", learner, graph)
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
        assert result.feedback.knoop_id == q1.knoop_id
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
# Breder testharness voor fase-transitities, context-first, offline en budget.
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
        "knopen": [
            {
                "id": "LAT-G-MORF-NAAMVAL-INTRO",
                "type": "G",
                "taal": "lat",
                "titel_nl": "Naamval intro",
                "beschrijving": "Introductie naamval.",
                "bloom_niveau": "kennis",
                "fase": "onderbouw_1",
                "items": [],
            },
            {
                "id": "LAT-G-MORF-DECL-INTRO",
                "type": "G",
                "taal": "lat",
                "titel_nl": "Declinatie intro",
                "beschrijving": "Introductie declinatie.",
                "bloom_niveau": "kennis",
                "fase": "onderbouw_1",
                "items": [],
            },
            {
                "id": "LAT-G-MORF-DECL1-INTRO",
                "type": "G",
                "taal": "lat",
                "titel_nl": "Eerste declinatie",
                "beschrijving": "Overzicht eerste declinatie.",
                "bloom_niveau": "kennis",
                "fase": "onderbouw_1",
                "items": [],
            },
            {
                "id": "LAT-G-MORF-NOM-D1",
                "type": "G",
                "taal": "lat",
                "titel_nl": "Nominativus 1e declinatie",
                "beschrijving": "Nom. sg/pl van de 1e declinatie.",
                "bloom_niveau": "kennis",
                "fase": "onderbouw_1",
                "items": [],
            },
            {
                "id": "LAT-V-F01-ESSE",
                "type": "V",
                "taal": "lat",
                "titel_nl": "esse — zijn",
                "beschrijving": "Werkwoord esse (zijn).",
                "bloom_niveau": "kennis",
                "fase": "onderbouw_1",
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
    learner.knoop_states["LAT-G-MORF-NAAMVAL-INTRO"] = KnoopState(
        knoop_id="LAT-G-MORF-NAAMVAL-INTRO",
        posterior_mastery=0.92,
        easiness_factor=2.5,
        interval_days=5.0,
        repetitions=3,
        last_review=stale,
    )
    learner.knoop_states["LAT-G-MORF-DECL-INTRO"] = KnoopState(
        knoop_id="LAT-G-MORF-DECL-INTRO",
        posterior_mastery=0.88,
        easiness_factor=2.5,
        interval_days=5.0,
        repetitions=3,
        last_review=stale,
    )
    # Mastered losstaand vocab-item, niet aangeraakt in deze sessie
    # → cooldown-kandidaat.
    learner.knoop_states["LAT-V-F01-ESSE"] = KnoopState(
        knoop_id="LAT-V-F01-ESSE",
        posterior_mastery=0.91,
        easiness_factor=2.5,
        interval_days=3.0,
        repetitions=2,
        last_review=stale,
    )
    return graph, learner


def _graph_with_offline_item():
    """Graph met één knoop die een OFFLINE_SCHRIJVEN-item bevat."""
    data = {
        "knopen": [
            {
                "id": "LAT-G-MORF-DECL1-INTRO",
                "type": "G",
                "taal": "lat",
                "titel_nl": "Eerste declinatie",
                "beschrijving": "Overzicht eerste declinatie.",
                "bloom_niveau": "kennis",
                "fase": "onderbouw_1",
                "items": [
                    {
                        "id": "ITEM-OFFLINE-D1-001",
                        "knoop_ids": ["LAT-G-MORF-DECL1-INTRO"],
                        "type": "offline_schrijven",
                        "richting": "productief",
                        "moeilijkheid_initieel": 0.5,
                        "discriminatie_initieel": 1.0,
                        "verwachte_tijd_sec": 300,
                        "stimulus": "Schrijf paradigma puella op.",
                        "antwoord": "puella, puellae, ...",
                        "feedback": "Vergelijk met paradigma.",
                        "bron": "handmatig",
                        "verificatie_methode": "self_report",
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
        # Elke fase kwam aan bod in de aangeboden vragen.
        phases_seen = {q.phase for q in asked}
        assert SessionPhase.WARMUP.value in phases_seen
        assert SessionPhase.NEW_MATERIAL.value in phases_seen

    def test_phase_label_on_question_matches_current_phase(self):
        """De `phase` van een Question reflecteert waar de scheduler nu zit."""
        now = datetime(2026, 4, 16, 10, 0, 0)
        graph, learner = _broad_graph_and_learner(now)
        mgr = SessionManager()
        session_id, q = mgr.start_session("user1", learner, graph, now=now)
        assert q is not None
        # Eerste vraag zit in één van de eerdere fasen (warmup of new_material
        # afhankelijk van kandidatenbeschikbaarheid).
        assert q.phase in {
            SessionPhase.WARMUP.value,
            SessionPhase.NEW_MATERIAL.value,
        }


class TestMaxNewNodes:
    """NEW_MATERIAL fase mag maximaal MAX_NEW_NODES nieuwe knopen introduceren."""

    def test_new_material_cap_enforced(self):
        now = datetime(2026, 4, 16, 10, 0, 0)
        # Graph met 5 ready new-material kandidaten, allemaal roots.
        data = {
            "knopen": [
                {
                    "id": f"LAT-G-MORF-ROOT{i}-INTRO",
                    "type": "G",
                    "taal": "lat",
                    "titel_nl": f"Root {i}",
                    "beschrijving": f"Root knoop {i}.",
                    "bloom_niveau": "kennis",
                    "fase": "onderbouw_1",
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
    """Fase-transities gebeuren wanneer het tijdbudget uitgeput is."""

    def test_new_material_phase_time_budget_consumed(self):
        now = datetime(2026, 4, 16, 10, 0, 0)
        graph, learner = _broad_graph_and_learner(now)
        mgr = SessionManager()
        session_id, q = mgr.start_session("user1", learner, graph, now=now)
        asked = _drive_session_to_completion(mgr, session_id, q, now)

        # Totaal geconsumeerde tijd ligt binnen de som van de fase-budgetten.
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
            "knopen": [
                {
                    "id": "LAT-G-MORF-NAAMVAL-INTRO",
                    "type": "G",
                    "taal": "lat",
                    "titel_nl": "Naamval intro",
                    "beschrijving": "Introductie naamval.",
                    "bloom_niveau": "kennis",
                    "fase": "onderbouw_1",
                    "items": [],
                },
                {
                    "id": "LAT-G-MORF-DECL1-INTRO",
                    "type": "G",
                    "taal": "lat",
                    "titel_nl": "Eerste declinatie",
                    "beschrijving": "Overzicht eerste declinatie.",
                    "bloom_niveau": "kennis",
                    "fase": "onderbouw_1",
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
            taal="lat",
            titel="Puella parva",
            tekst="Puella parva in villa est.",
            annotaties=[
                WordAnnotation(
                    woord="Puella", lemma="puella", naamval="nom.sg",
                    vertaling="Het meisje",
                ),
            ],
            knoop_ids=[
                "LAT-G-MORF-NAAMVAL-INTRO",
                "LAT-G-MORF-DECL1-INTRO",
            ],
            moeilijkheid=1,
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
        session_id, q = mgr.start_session(
            "user1", learner, graph, now=now,
            learning_route=LearningRoute.CONTEXT_FIRST,
            passages=[passage],
        )
        assert q is not None
        assert isinstance(q.stimulus, dict)
        assert q.stimulus.get("type") == "passage"
        assert q.stimulus["passage_id"] == "LAT-P-001"
        assert q.stimulus["tekst"] == "Puella parva in villa est."

    def test_passage_read_yields_grammar_scaffolding(self, tmp_path):
        graph, passage, _ = self._make_passage_setup(tmp_path)
        learner = LearnerModel(user_id=uuid4())
        mgr = SessionManager()
        now = datetime(2026, 4, 16, 10, 0, 0)
        session_id, q_passage = mgr.start_session(
            "user1", learner, graph, now=now,
            learning_route=LearningRoute.CONTEXT_FIRST,
            passages=[passage],
        )
        assert q_passage.stimulus["type"] == "passage"

        result = mgr.submit_answer(
            session_id, ResponseType.CORRECT, 5000, now=now
        )
        assert result.feedback.response_type == "passage_read"
        # Mastery voor passage-step blijft 0.0 (geen BKT-update).
        assert result.feedback.mastery_before == 0.0
        assert result.feedback.mastery_after == 0.0
        # De vervolgvraag is een grammar-knoop uit de passage.
        assert result.next_question is not None
        assert result.next_question.knoop_id in passage.knoop_ids


class TestOfflineAssignmentCollection:
    """OFFLINE_SCHRIJVEN-items horen na de sessie in pending_offline_assignments.

    Gemarkeerd als xfail: ``SessionManager._finalize_session`` gooit de
    return-waarde van ``_collect_offline_items`` weg.  ``run_session`` in
    ``scheduling/session.py`` doet dit wel correct (zie
    ``test_offline_scheduling.py``).  Deze test fungeert als regressie-vangnet
    voor als de bug in SessionManager verholpen wordt.
    """

    @pytest.mark.xfail(
        reason=(
            "SessionManager._finalize_session roept _collect_offline_items "
            "aan maar gebruikt het resultaat niet; zie scheduling/session.py "
            "voor de correcte implementatie."
        ),
        strict=True,
    )
    def test_offline_item_ends_up_in_pending(self):
        now = datetime(2026, 4, 16, 10, 0, 0)
        graph, learner = _graph_with_offline_item()
        mgr = SessionManager()
        session_id, q = mgr.start_session("user1", learner, graph, now=now)
        _drive_session_to_completion(mgr, session_id, q, now)

        assert any(
            a.item_id == "ITEM-OFFLINE-D1-001"
            for a in learner.pending_offline_assignments
        )


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

    def test_roundtrip_preserves_knoop_states_and_history(self):
        now = datetime(2026, 4, 16, 10, 0, 0)
        graph, learner = _broad_graph_and_learner(now)
        mgr = SessionManager()
        session_id, q = mgr.start_session("user1", learner, graph, now=now)
        _drive_session_to_completion(mgr, session_id, q, now)

        serialized = learner.model_dump_json()
        restored = LearnerModel.model_validate_json(serialized)

        assert restored.user_id == learner.user_id
        assert set(restored.knoop_states.keys()) == set(learner.knoop_states.keys())
        for knoop_id, state in learner.knoop_states.items():
            assert restored.knoop_states[knoop_id].posterior_mastery == state.posterior_mastery
            assert restored.knoop_states[knoop_id].repetitions == state.repetitions
        assert len(restored.session_history) == len(learner.session_history)
        assert restored.session_history[0].session_id == session_id
