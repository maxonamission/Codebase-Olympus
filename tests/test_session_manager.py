"""Tests for D1-04: SessionManager step-by-step session protocol."""

from datetime import datetime
from uuid import uuid4

import pytest

from gymnasium_classica.api.session_manager import (
    AnswerResult,
    Question,
    SessionManager,
    SessionSummary,
)
from gymnasium_classica.graph.loader import load_graph_from_dict
from gymnasium_classica.models.learner import KnoopState, LearnerModel, ResponseType
from gymnasium_classica.scheduling.priority import MASTERY_THRESHOLD


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
