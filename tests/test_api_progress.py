"""Tests for D1-07: Progress endpoints (overview + per knoop)."""

import tempfile
from pathlib import Path
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from gymnasium_classica.api.database import save_learner_model
from gymnasium_classica.models.learner import KnoopState, LearnerModel, MasterySource


@pytest.fixture()
def client():
    from gymnasium_classica.api.app import create_app

    with tempfile.TemporaryDirectory() as tmp:
        db_path = Path(tmp) / "test.db"
        test_app = create_app(db_path=db_path)
        with TestClient(test_app) as c:
            yield c


def _auth_header(client, email="progress@example.nl"):
    resp = client.post("/auth/register", json={"email": email, "password": "pw1234"})
    return resp.json()["user_id"], {"Authorization": f"Bearer {resp.json()['token']}"}


class TestProgressOverview:
    def test_overview_no_learner_model(self, client):
        """New user without learner model: everything unseen."""
        _, headers = _auth_header(client)
        resp = client.get("/progress/overview", headers=headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["total_nodes"] > 0
        assert data["mastered"] == 0
        assert data["in_progress"] == 0
        assert data["unseen"] == data["total_nodes"]
        assert data["streak_days"] == 0
        assert data["intake_completed"] is False

    def test_overview_with_some_mastery(self, client):
        """User with a few mastered nodes."""
        user_id, headers = _auth_header(client, "mastered@example.nl")
        db = client.app.state.db
        graph = client.app.state.graph

        # Pick a real knoop_id from the graph
        knoop_ids = list(graph.nodes)[:3]
        learner = LearnerModel(user_id=UUID(user_id))
        learner.knoop_states[knoop_ids[0]] = KnoopState(
            knoop_id=knoop_ids[0], posterior_mastery=0.85, source=MasterySource.PRACTICE
        )
        learner.knoop_states[knoop_ids[1]] = KnoopState(
            knoop_id=knoop_ids[1], posterior_mastery=0.40, source=MasterySource.PRACTICE
        )
        save_learner_model(db, learner)

        resp = client.get("/progress/overview", headers=headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["mastered"] >= 1
        assert data["in_progress"] >= 1

    def test_overview_requires_auth(self, client):
        resp = client.get("/progress/overview")
        assert resp.status_code == 422

    def test_overview_domains_structure(self, client):
        _, headers = _auth_header(client, "domains@example.nl")
        data = client.get("/progress/overview", headers=headers).json()
        assert isinstance(data["domains"], dict)
        for domain, dp in data["domains"].items():
            assert "total" in dp
            assert "mastered" in dp
            assert "in_progress" in dp
            assert "unseen" in dp
            assert dp["total"] == dp["mastered"] + dp["in_progress"] + dp["unseen"]


class TestKnoopProgress:
    def test_knoop_not_found(self, client):
        _, headers = _auth_header(client, "knoop404@example.nl")
        resp = client.get("/progress/knoop/NONEXISTENT-ID", headers=headers)
        assert resp.status_code == 404

    def test_knoop_no_learner_state(self, client):
        """Knoop exists in graph but user hasn't interacted with it."""
        _, headers = _auth_header(client, "knoop_unseen@example.nl")
        graph = client.app.state.graph
        knoop_id = list(graph.nodes)[0]
        resp = client.get(f"/progress/knoop/{knoop_id}", headers=headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["knoop_id"] == knoop_id
        assert data["posterior_mastery"] == 0.0
        assert data["repetitions"] == 0
        assert data["item_history"] == []

    def test_knoop_with_state(self, client):
        user_id, headers = _auth_header(client, "knoop_state@example.nl")
        db = client.app.state.db
        graph = client.app.state.graph
        knoop_id = list(graph.nodes)[0]

        learner = LearnerModel(user_id=UUID(user_id))
        learner.knoop_states[knoop_id] = KnoopState(
            knoop_id=knoop_id,
            posterior_mastery=0.6,
            easiness_factor=2.2,
            interval_days=3.0,
            repetitions=5,
            source=MasterySource.PRACTICE,
        )
        save_learner_model(db, learner)

        resp = client.get(f"/progress/knoop/{knoop_id}", headers=headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["posterior_mastery"] == pytest.approx(0.6)
        assert data["repetitions"] == 5
        assert data["source"] == "practice"

    def test_knoop_requires_auth(self, client):
        resp = client.get("/progress/knoop/LAT-G-MORF-NOM-D1")
        assert resp.status_code == 422
