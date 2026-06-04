"""Tests voor F1-12: answer_text door de SessionManager en item_history.

Geen mocks — een minimale LearnerModel + graph, echte grading en echte
SessionManager.  Dekt het samenspel dat de API-integratietest in
``test_api_session.py`` niet kan aantonen (daar weten we het juiste
antwoord niet zonder de scheduler te fixeren).
"""

from __future__ import annotations

from datetime import datetime
from uuid import uuid4

import pytest

from gymnasium_classica.api.session_manager import SessionManager
from gymnasium_classica.graph.loader import load_graph_from_dict
from gymnasium_classica.models.learner import LearnerModel, ResponseType


def _build_graph_with_gradeable_item() -> dict:
    """A tiny graph with one root V-node that has a single productie-item."""
    return {
        "nodes": [
            {
                "id": "LAT-V-F01-TEST",
                "type": "V",
                "language": "lat",
                "title_nl": "sum, esse — zijn",
                "description": "Het werkwoord 'zijn'.",
                "bloom_level": "kennis",
                "phase": "onderbouw_1",
                "items": [
                    {
                        "id": "ITEM-LAT-V-F01-TEST-001",
                        "node_ids": ["LAT-V-F01-TEST"],
                        "type": "productie",
                        "direction": "productief",
                        "difficulty_initial": 0.0,
                        "discrimination_initial": 1.0,
                        "expected_time_sec": 10,
                        "stimulus": "Vertaal 'zijn' naar het Latijn.",
                        "answer": "sum",
                        "feedback": "sum betekent 'zijn'.",
                        "source": "handmatig",
                    }
                ],
            }
        ],
        "edges": [],
    }


@pytest.fixture()
def session_and_manager():
    graph = load_graph_from_dict(_build_graph_with_gradeable_item())
    learner = LearnerModel(user_id=uuid4())
    manager = SessionManager()
    now = datetime(2026, 4, 17, 10, 0, 0)
    session_id, question = manager.start_session(
        user_id=str(learner.user_id),
        learner=learner,
        graph=graph,
        now=now,
    )
    assert question is not None
    return manager, session_id, learner, now


class TestAnswerTextGrading:
    def test_correct_answer_text_is_graded_correct(self, session_and_manager):
        manager, session_id, _learner, now = session_and_manager

        result = manager.submit_answer(
            session_id,
            response=None,
            response_time_ms=2000,
            now=now,
            answer_text="sum",
        )

        assert result.feedback.correct is True
        assert result.feedback.response_type == "correct"

    def test_slow_correct_detected_from_response_time(self, session_and_manager):
        manager, session_id, _learner, now = session_and_manager

        # Item.expected_time_sec = 10 → threshold = 15_000 ms.
        result = manager.submit_answer(
            session_id,
            response=None,
            response_time_ms=20_000,
            now=now,
            answer_text="sum",
        )

        assert result.feedback.correct is True
        assert result.feedback.response_type == "slow_correct"

    def test_wrong_answer_is_graded_incorrect(self, session_and_manager):
        manager, session_id, _learner, now = session_and_manager

        result = manager.submit_answer(
            session_id,
            response=None,
            response_time_ms=2000,
            now=now,
            answer_text="est",
        )

        assert result.feedback.correct is False
        assert result.feedback.response_type == "incorrect"

    def test_case_and_macron_insensitive(self, session_and_manager):
        manager, session_id, _learner, now = session_and_manager

        # "SUM" (uppercase) should still count as correct.
        result = manager.submit_answer(
            session_id,
            response=None,
            response_time_ms=2000,
            now=now,
            answer_text="  SUM  ",
        )
        assert result.feedback.correct is True


class TestItemHistoryRecording:
    def test_answer_text_records_literal_answer(self, session_and_manager):
        manager, session_id, learner, now = session_and_manager

        manager.submit_answer(
            session_id,
            response=None,
            response_time_ms=3000,
            now=now,
            answer_text="est",
        )

        state = learner.node_states["LAT-V-F01-TEST"]
        assert len(state.item_history) == 1
        entry = state.item_history[0]
        assert entry.answer_text == "est"
        assert entry.correct is False
        assert entry.correct_answer == "sum"
        assert entry.item_type == "productie"
        assert entry.item_id == "ITEM-LAT-V-F01-TEST-001"

    def test_self_assess_records_without_answer_text(self, session_and_manager):
        manager, session_id, learner, now = session_and_manager

        manager.submit_answer(
            session_id,
            response=ResponseType.CORRECT,
            response_time_ms=3000,
            now=now,
        )

        state = learner.node_states["LAT-V-F01-TEST"]
        assert len(state.item_history) == 1
        entry = state.item_history[0]
        assert entry.answer_text is None
        assert entry.correct is True
        # correct_answer is still snapshotted from the item
        assert entry.correct_answer == "sum"

    def test_requires_response_or_answer_text(self, session_and_manager):
        manager, session_id, _, now = session_and_manager

        with pytest.raises(ValueError, match="answer_text or response"):
            manager.submit_answer(
                session_id,
                response=None,
                response_time_ms=1000,
                now=now,
            )
