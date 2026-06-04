"""Tests for F2-02: last wrong/right attempts per learner per node."""

import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from gymnasium_classica.api.database import (
    create_mentor_assignment,
    get_user,
    save_learner_model,
    update_user,
)
from gymnasium_classica.models.learner import ItemResponse, LearnerModel, NodeState
from gymnasium_classica.models.user import Role

_NODE = "LAT-G-MORF-NAAMVAL-INTRO"  # exists in data/graph (PoC)


@pytest.fixture()
def client():
    from gymnasium_classica.api.app import create_app

    with tempfile.TemporaryDirectory() as tmp:
        db_path = Path(tmp) / "test.db"
        test_app = create_app(db_path=db_path)
        with TestClient(test_app) as c:
            yield c


def _register(client: TestClient, email: str) -> tuple[str, str]:
    resp = client.post("/auth/register", json={"email": email, "password": "pw123456"})
    assert resp.status_code == 200, resp.text
    return resp.json()["user_id"], resp.json()["token"]


def _promote(client: TestClient, user_id: str) -> None:
    db = client.app.state.db
    user = get_user(db, user_id)
    assert user is not None
    user.role = Role.MENTOR
    update_user(db, user)


def _ir(answer: str | None, *, correct: bool, minutes: int, item_id: str = "I1") -> ItemResponse:
    return ItemResponse(
        timestamp=datetime(2026, 6, 1, 12, 0) + timedelta(minutes=minutes),
        item_id=item_id,
        correct=correct,
        response_time_ms=4000,
        answer_text=answer,
        correct_answer="puellam",
        item_type="production",
        node_id=_NODE,
        direction="productive",
        mastery_before=0.3,
    )


def _seed_history(client: TestClient, user_id: str, responses: list[ItemResponse]) -> None:
    model = LearnerModel(user_id=UUID(user_id))
    model.node_states[_NODE] = NodeState(node_id=_NODE, item_history=responses)
    save_learner_model(client.app.state.db, model)


def _setup_mentor_with_learner(client: TestClient) -> tuple[str, str]:
    """Return (learner_id, mentor_token) with the assignment in place."""
    mentor_id, mentor_tok = _register(client, "mentor@y.nl")
    learner_id, _ = _register(client, "learner@y.nl")
    _promote(client, mentor_id)
    create_mentor_assignment(client.app.state.db, mentor_id, learner_id)
    return learner_id, mentor_tok


class TestNodeAttempts:
    def test_returns_literal_attempts_newest_first(self, client):
        learner_id, tok = _setup_mentor_with_learner(client)
        _seed_history(
            client,
            learner_id,
            [
                _ir("puellae", correct=False, minutes=0),
                _ir("puella", correct=False, minutes=5),
                _ir("puellam", correct=True, minutes=10),
            ],
        )
        resp = client.get(
            f"/mentor/{learner_id}/knoop/{_NODE}/attempts",
            headers={"Authorization": f"Bearer {tok}"},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["knoop_id"] == _NODE
        assert body["knoop_title"]  # title resolved from graph
        answers = [a["answer_text"] for a in body["attempts"]]
        assert answers == ["puellam", "puella", "puellae"]  # newest first

    def test_filters_out_self_assess_null_answers(self, client):
        learner_id, tok = _setup_mentor_with_learner(client)
        _seed_history(
            client,
            learner_id,
            [
                _ir(None, correct=True, minutes=0),  # self-assess: dropped
                _ir("puellae", correct=False, minutes=5),
            ],
        )
        resp = client.get(
            f"/mentor/{learner_id}/knoop/{_NODE}/attempts",
            headers={"Authorization": f"Bearer {tok}"},
        )
        assert resp.status_code == 200
        attempts = resp.json()["attempts"]
        assert len(attempts) == 1
        assert attempts[0]["answer_text"] == "puellae"

    def test_limit_caps_results(self, client):
        learner_id, tok = _setup_mentor_with_learner(client)
        _seed_history(
            client,
            learner_id,
            [_ir(f"ans{i}", correct=False, minutes=i) for i in range(20)],
        )
        resp = client.get(
            f"/mentor/{learner_id}/knoop/{_NODE}/attempts?limit=3",
            headers={"Authorization": f"Bearer {tok}"},
        )
        assert resp.status_code == 200
        assert len(resp.json()["attempts"]) == 3

    def test_exposes_correct_answer_and_metadata(self, client):
        learner_id, tok = _setup_mentor_with_learner(client)
        _seed_history(client, learner_id, [_ir("puellae", correct=False, minutes=0)])
        resp = client.get(
            f"/mentor/{learner_id}/knoop/{_NODE}/attempts",
            headers={"Authorization": f"Bearer {tok}"},
        )
        a = resp.json()["attempts"][0]
        assert a["correct_answer"] == "puellam"
        assert a["correct"] is False
        assert a["response_time_ms"] == 4000
        assert a["item_type"] == "production"

    def test_empty_when_no_history(self, client):
        learner_id, tok = _setup_mentor_with_learner(client)
        resp = client.get(
            f"/mentor/{learner_id}/knoop/{_NODE}/attempts",
            headers={"Authorization": f"Bearer {tok}"},
        )
        assert resp.status_code == 200
        assert resp.json()["attempts"] == []

    def test_unknown_knoop_404(self, client):
        learner_id, tok = _setup_mentor_with_learner(client)
        resp = client.get(
            f"/mentor/{learner_id}/knoop/LAT-G-DOES-NOT-EXIST/attempts",
            headers={"Authorization": f"Bearer {tok}"},
        )
        assert resp.status_code == 404

    def test_unassigned_learner_403(self, client):
        mentor_id, tok = _register(client, "mentor@y.nl")
        other_id, _ = _register(client, "other@y.nl")
        _promote(client, mentor_id)
        resp = client.get(
            f"/mentor/{other_id}/knoop/{_NODE}/attempts",
            headers={"Authorization": f"Bearer {tok}"},
        )
        assert resp.status_code == 403

    def test_learner_role_403(self, client):
        learner_id, learner_tok = _register(client, "learner@y.nl")
        resp = client.get(
            f"/mentor/{learner_id}/knoop/{_NODE}/attempts",
            headers={"Authorization": f"Bearer {learner_tok}"},
        )
        assert resp.status_code == 403
