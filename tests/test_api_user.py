"""Tests for E7-08: User settings endpoints (profile + learning route)."""

import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client():
    """Create a TestClient with a fresh temporary database per test."""
    from gymnasium_classica.api.app import create_app

    with tempfile.TemporaryDirectory() as tmp:
        db_path = Path(tmp) / "test.db"
        test_app = create_app(db_path=db_path)
        with TestClient(test_app) as c:
            yield c


def _register_and_get_token(client) -> tuple[str, str]:
    """Helper: register a user and return (user_id, token)."""
    resp = client.post(
        "/auth/register", json={"email": "test@example.com", "password": "test1234"}
    )
    data = resp.json()
    return data["user_id"], data["token"]


class TestGetProfile:
    def test_get_profile_success(self, client):
        user_id, token = _register_and_get_token(client)
        resp = client.get("/user/profile", headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["user_id"] == user_id
        assert data["email"] == "test@example.com"
        assert data["learning_route"] == "grammar_first"

    def test_get_profile_no_auth(self, client):
        resp = client.get("/user/profile")
        assert resp.status_code == 422 or resp.status_code == 401


class TestUpdateLearningRoute:
    def test_update_to_context_first(self, client):
        _, token = _register_and_get_token(client)
        resp = client.put(
            "/user/learning-route",
            json={"learning_route": "context_first"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["learning_route"] == "context_first"

    def test_update_to_grammar_first(self, client):
        _, token = _register_and_get_token(client)
        # First switch to context_first
        client.put(
            "/user/learning-route",
            json={"learning_route": "context_first"},
            headers={"Authorization": f"Bearer {token}"},
        )
        # Then switch back
        resp = client.put(
            "/user/learning-route",
            json={"learning_route": "grammar_first"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 200
        assert resp.json()["learning_route"] == "grammar_first"

    def test_update_invalid_route(self, client):
        _, token = _register_and_get_token(client)
        resp = client.put(
            "/user/learning-route",
            json={"learning_route": "invalid_route"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 422

    def test_persists_after_profile_reload(self, client):
        _, token = _register_and_get_token(client)
        client.put(
            "/user/learning-route",
            json={"learning_route": "context_first"},
            headers={"Authorization": f"Bearer {token}"},
        )
        # Reload profile
        resp = client.get("/user/profile", headers={"Authorization": f"Bearer {token}"})
        assert resp.json()["learning_route"] == "context_first"

    def test_no_auth(self, client):
        resp = client.put(
            "/user/learning-route",
            json={"learning_route": "context_first"},
        )
        assert resp.status_code == 422 or resp.status_code == 401
