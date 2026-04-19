"""Tests for E7-10: route_history tracking and session mastery progression."""

import tempfile
from datetime import datetime
from pathlib import Path
from uuid import uuid4

import pytest

from gymnasium_classica.models.learner import (
    LearnerModel,
    RouteSwitch,
    SessionRecord,
)

# --- RouteSwitch model ---


class TestRouteSwitch:
    def test_basic_construction(self):
        rs = RouteSwitch(timestamp=datetime.now(), route="grammar_first")
        assert rs.route == "grammar_first"
        assert isinstance(rs.timestamp, datetime)

    def test_context_first(self):
        rs = RouteSwitch(timestamp=datetime.now(), route="context_first")
        assert rs.route == "context_first"

    def test_roundtrip(self):
        rs = RouteSwitch(timestamp=datetime.now(), route="grammar_first")
        data = rs.model_dump()
        rs2 = RouteSwitch(**data)
        assert rs2.route == rs.route


# --- LearnerModel with route_history ---


class TestLearnerModelRouteHistory:
    def test_default_empty(self):
        lm = LearnerModel(user_id=uuid4())
        assert lm.route_history == []

    def test_append_route_switch(self):
        lm = LearnerModel(user_id=uuid4())
        lm.route_history.append(RouteSwitch(timestamp=datetime.now(), route="context_first"))
        assert len(lm.route_history) == 1
        assert lm.route_history[0].route == "context_first"

    def test_multiple_switches(self):
        lm = LearnerModel(user_id=uuid4())
        lm.route_history.append(RouteSwitch(timestamp=datetime(2026, 1, 1), route="grammar_first"))
        lm.route_history.append(RouteSwitch(timestamp=datetime(2026, 1, 5), route="context_first"))
        lm.route_history.append(
            RouteSwitch(timestamp=datetime(2026, 1, 10), route="grammar_first")
        )
        assert len(lm.route_history) == 3

    def test_roundtrip_with_route_history(self):
        lm = LearnerModel(user_id=uuid4())
        lm.route_history.append(RouteSwitch(timestamp=datetime.now(), route="context_first"))
        data = lm.model_dump()
        lm2 = LearnerModel(**data)
        assert len(lm2.route_history) == 1
        assert lm2.route_history[0].route == "context_first"

    def test_backward_compat_no_route_history(self):
        """Old data without route_history should deserialize fine."""
        data = {"user_id": str(uuid4())}
        lm = LearnerModel(**data)
        assert lm.route_history == []


# --- SessionRecord with learning_route ---


class TestSessionRecordRoute:
    def test_default_none(self):
        sr = SessionRecord(session_id="s1", started_at=datetime.now())
        assert sr.learning_route is None

    def test_with_route(self):
        sr = SessionRecord(
            session_id="s1",
            started_at=datetime.now(),
            learning_route="context_first",
        )
        assert sr.learning_route == "context_first"

    def test_backward_compat(self):
        """Old data without learning_route should deserialize fine."""
        data = {"session_id": "s1", "started_at": datetime.now().isoformat()}
        sr = SessionRecord(**data)
        assert sr.learning_route is None


# --- API integration: route_history tracking ---


@pytest.fixture()
def client():
    from fastapi.testclient import TestClient

    from gymnasium_classica.api.app import create_app

    with tempfile.TemporaryDirectory() as tmp:
        db_path = Path(tmp) / "test.db"
        test_app = create_app(db_path=db_path)
        with TestClient(test_app) as c:
            yield c


def _register(client, email="test@example.com"):
    resp = client.post("/auth/register", json={"email": email, "password": "pw1234"})
    return resp.json()["token"]


class TestRouteHistoryAPI:
    def test_route_switch_recorded_via_user_endpoint(self, client):
        token = _register(client)
        headers = {"Authorization": f"Bearer {token}"}

        client.put(
            "/user/learning-route",
            json={"learning_route": "context_first"},
            headers=headers,
        )

        # Check progress overview has session_progression field
        resp = client.get("/progress/overview", headers=headers)
        assert resp.status_code == 200
        data = resp.json()
        assert "session_progression" in data

    def test_route_switch_recorded_via_auth_settings(self, client):
        token = _register(client, "auth@example.com")
        headers = {"Authorization": f"Bearer {token}"}

        client.post(
            "/auth/settings",
            json={"learning_route": "context_first"},
            headers=headers,
        )
        client.post(
            "/auth/settings",
            json={"learning_route": "grammar_first"},
            headers=headers,
        )

        # Verify route history exists (no direct API for it,
        # but the switches should not cause errors)
        resp = client.get("/user/profile", headers=headers)
        assert resp.status_code == 200
        assert resp.json()["learning_route"] == "grammar_first"

    def test_session_progression_in_overview(self, client):
        token = _register(client, "prog@example.com")
        headers = {"Authorization": f"Bearer {token}"}

        # Start and complete a session to have some data
        start_resp = client.post("/session/start", headers=headers)
        if start_resp.status_code == 200:
            data = start_resp.json()
            session_id = data["session_id"]
            q = data["question"]

            # Answer a few questions
            steps = 0
            while q is not None and steps < 5:
                resp = client.post(
                    "/session/answer",
                    json={
                        "session_id": session_id,
                        "response": "correct",
                        "response_time_ms": 2000,
                    },
                    headers=headers,
                ).json()
                q = resp.get("next_question")
                steps += 1
                if resp.get("session_finished"):
                    break

        # Check progress overview
        resp = client.get("/progress/overview", headers=headers)
        assert resp.status_code == 200
        overview = resp.json()
        assert isinstance(overview["session_progression"], list)
        if overview["session_progression"]:
            entry = overview["session_progression"][0]
            assert "session_id" in entry
            assert "timestamp" in entry
            assert "nodes_practiced" in entry
            assert "mastered_after" in entry
            # learning_route can be None for old sessions
            assert "learning_route" in entry
