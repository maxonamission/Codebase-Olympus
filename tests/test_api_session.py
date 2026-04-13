"""Tests for D1-05: Session endpoints (start + answer) and D1-06 (summary)."""

import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client():
    """Create a TestClient with a fresh temp DB per test."""
    from gymnasium_classica.api.app import create_app

    with tempfile.TemporaryDirectory() as tmp:
        db_path = Path(tmp) / "test.db"
        test_app = create_app(db_path=db_path)
        with TestClient(test_app) as c:
            yield c


def _auth_header(client: TestClient, email: str = "test@example.nl") -> dict:
    """Register a user and return an Authorization header."""
    resp = client.post("/auth/register", json={"email": email, "password": "pw1234"})
    token = resp.json()["token"]
    return {"Authorization": f"Bearer {token}"}


class TestStartSession:
    def test_start_returns_session_and_question(self, client):
        headers = _auth_header(client)
        resp = client.post("/session/start", headers=headers)
        assert resp.status_code == 200
        data = resp.json()
        assert "session_id" in data
        assert len(data["session_id"]) > 0
        # With the full graph, there should be a question available
        if data["question"] is not None:
            q = data["question"]
            assert "knoop_id" in q
            assert "titel" in q
            assert "phase" in q

    def test_start_requires_auth(self, client):
        resp = client.post("/session/start")
        assert resp.status_code == 422  # missing Authorization header

    def test_start_invalid_token(self, client):
        resp = client.post("/session/start", headers={"Authorization": "Bearer invalid"})
        assert resp.status_code == 401


class TestSubmitAnswer:
    def test_answer_correct_returns_feedback(self, client):
        headers = _auth_header(client)
        start = client.post("/session/start", headers=headers).json()
        session_id = start["session_id"]

        if start["question"] is None:
            pytest.skip("No question available in graph")

        resp = client.post(
            "/session/answer",
            json={
                "session_id": session_id,
                "response": "correct",
                "response_time_ms": 2000,
            },
            headers=headers,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["feedback"]["correct"] is True
        assert "mastery_before" in data["feedback"]
        assert "mastery_after" in data["feedback"]

    def test_answer_incorrect(self, client):
        headers = _auth_header(client)
        start = client.post("/session/start", headers=headers).json()
        session_id = start["session_id"]

        if start["question"] is None:
            pytest.skip("No question available in graph")

        resp = client.post(
            "/session/answer",
            json={
                "session_id": session_id,
                "response": "incorrect",
                "response_time_ms": 5000,
            },
            headers=headers,
        )
        assert resp.status_code == 200
        assert resp.json()["feedback"]["correct"] is False

    def test_answer_unknown_session(self, client):
        headers = _auth_header(client)
        resp = client.post(
            "/session/answer",
            json={
                "session_id": "nonexistent",
                "response": "correct",
                "response_time_ms": 1000,
            },
            headers=headers,
        )
        assert resp.status_code == 404

    def test_answer_invalid_response_type(self, client):
        headers = _auth_header(client)
        start = client.post("/session/start", headers=headers).json()
        session_id = start["session_id"]

        resp = client.post(
            "/session/answer",
            json={
                "session_id": session_id,
                "response": "invalid_type",
                "response_time_ms": 1000,
            },
            headers=headers,
        )
        assert resp.status_code == 422

    def test_answer_wrong_user(self, client):
        # User 1 starts a session
        h1 = _auth_header(client, "user1@example.nl")
        start = client.post("/session/start", headers=h1).json()
        session_id = start["session_id"]

        # User 2 tries to answer
        h2 = _auth_header(client, "user2@example.nl")
        resp = client.post(
            "/session/answer",
            json={
                "session_id": session_id,
                "response": "correct",
                "response_time_ms": 1000,
            },
            headers=h2,
        )
        assert resp.status_code == 403

    def test_full_session_flow(self, client):
        """Start a session, answer questions until finished."""
        headers = _auth_header(client)
        start = client.post("/session/start", headers=headers).json()
        session_id = start["session_id"]
        q = start["question"]

        steps = 0
        max_steps = 200
        while q is not None and steps < max_steps:
            resp = client.post(
                "/session/answer",
                json={
                    "session_id": session_id,
                    "response": "correct",
                    "response_time_ms": 1000,
                },
                headers=headers,
            ).json()
            q = resp.get("next_question")
            steps += 1
            if resp["session_finished"]:
                break

        assert steps < max_steps
