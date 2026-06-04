"""Tests for F2-03: per-learner stumbling-block overview."""

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

# Two nodes that exist in data/graph (PoC)
_NODE_A = "LAT-G-MORF-NAAMVAL-INTRO"
_NODE_B = "LAT-G-MORF-DECL-INTRO"


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


def _ir(node: str, *, correct: bool, minutes: int) -> ItemResponse:
    return ItemResponse(
        timestamp=datetime(2026, 6, 1, 12, 0) + timedelta(minutes=minutes),
        item_id="I1",
        correct=correct,
        response_time_ms=4000,
        answer_text="x",
        correct_answer="y",
        item_type="production",
        node_id=node,
        direction="productive",
        mastery_before=0.3,
    )


def _seed(client: TestClient, user_id: str, states: dict[str, list[ItemResponse]]) -> None:
    model = LearnerModel(user_id=UUID(user_id))
    for node, history in states.items():
        model.node_states[node] = NodeState(node_id=node, item_history=history)
    save_learner_model(client.app.state.db, model)


def _setup(client: TestClient) -> tuple[str, str]:
    mentor_id, tok = _register(client, "mentor@y.nl")
    learner_id, _ = _register(client, "learner@y.nl")
    _promote(client, mentor_id)
    create_mentor_assignment(client.app.state.db, mentor_id, learner_id)
    return learner_id, tok


class TestStruikelpunten:
    def test_aggregates_per_node(self, client):
        learner_id, tok = _setup(client)
        _seed(
            client,
            learner_id,
            {
                _NODE_A: [
                    _ir(_NODE_A, correct=False, minutes=0),
                    _ir(_NODE_A, correct=False, minutes=1),
                    _ir(_NODE_A, correct=True, minutes=2),
                ],
            },
        )
        resp = client.get(
            f"/mentor/{learner_id}/struikelpunten?min_attempts=1",
            headers={"Authorization": f"Bearer {tok}"},
        )
        assert resp.status_code == 200
        entries = resp.json()["struikelpunten"]
        assert len(entries) == 1
        e = entries[0]
        assert e["knoop_id"] == _NODE_A
        assert e["knoop_title"]
        assert e["total_attempts"] == 3
        assert e["wrong_attempts"] == 2
        assert e["error_rate"] == round(2 / 3, 4)

    def test_min_attempts_filters_noise(self, client):
        learner_id, tok = _setup(client)
        _seed(
            client,
            learner_id,
            {
                _NODE_A: [_ir(_NODE_A, correct=False, minutes=0)],  # 1 attempt
                _NODE_B: [_ir(_NODE_B, correct=False, minutes=i) for i in range(3)],  # 3
            },
        )
        resp = client.get(
            f"/mentor/{learner_id}/struikelpunten?min_attempts=3",
            headers={"Authorization": f"Bearer {tok}"},
        )
        ids = [e["knoop_id"] for e in resp.json()["struikelpunten"]]
        assert ids == [_NODE_B]

    def test_nodes_without_errors_excluded(self, client):
        learner_id, tok = _setup(client)
        _seed(
            client,
            learner_id,
            {_NODE_A: [_ir(_NODE_A, correct=True, minutes=i) for i in range(5)]},
        )
        resp = client.get(
            f"/mentor/{learner_id}/struikelpunten?min_attempts=1",
            headers={"Authorization": f"Bearer {tok}"},
        )
        assert resp.json()["struikelpunten"] == []

    def test_default_sort_recent_wrong_first(self, client):
        learner_id, tok = _setup(client)
        _seed(
            client,
            learner_id,
            {
                _NODE_A: [_ir(_NODE_A, correct=False, minutes=0)],  # older wrong
                _NODE_B: [_ir(_NODE_B, correct=False, minutes=100)],  # recent wrong
            },
        )
        resp = client.get(
            f"/mentor/{learner_id}/struikelpunten?min_attempts=1",
            headers={"Authorization": f"Bearer {tok}"},
        )
        ids = [e["knoop_id"] for e in resp.json()["struikelpunten"]]
        assert ids == [_NODE_B, _NODE_A]

    def test_empty_without_learner_model(self, client):
        learner_id, tok = _setup(client)
        resp = client.get(
            f"/mentor/{learner_id}/struikelpunten",
            headers={"Authorization": f"Bearer {tok}"},
        )
        assert resp.status_code == 200
        assert resp.json()["struikelpunten"] == []

    def test_unassigned_learner_403(self, client):
        mentor_id, tok = _register(client, "mentor@y.nl")
        other_id, _ = _register(client, "other@y.nl")
        _promote(client, mentor_id)
        resp = client.get(
            f"/mentor/{other_id}/struikelpunten",
            headers={"Authorization": f"Bearer {tok}"},
        )
        assert resp.status_code == 403

    def test_learner_role_403(self, client):
        learner_id, learner_tok = _register(client, "learner@y.nl")
        resp = client.get(
            f"/mentor/{learner_id}/struikelpunten",
            headers={"Authorization": f"Bearer {learner_tok}"},
        )
        assert resp.status_code == 403
