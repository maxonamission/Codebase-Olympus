"""Tests for D1-02: Auth endpoints (register + login)."""

import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from gymnasium_classica.api.auth import hash_password, verify_password


@pytest.fixture()
def client():
    """Create a TestClient with a fresh temporary database per test."""
    from gymnasium_classica.api.app import create_app

    with tempfile.TemporaryDirectory() as tmp:
        db_path = Path(tmp) / "test.db"
        test_app = create_app(db_path=db_path)
        with TestClient(test_app) as c:
            yield c


class TestPasswordHashing:
    def test_hash_and_verify(self):
        pw = "geheim123"
        hashed = hash_password(pw)
        assert hashed != pw
        assert verify_password(pw, hashed)

    def test_wrong_password(self):
        hashed = hash_password("correct")
        assert not verify_password("wrong", hashed)


class TestRegister:
    def test_register_success(self, client):
        resp = client.post("/auth/register", json={"email": "a@b.nl", "password": "test1234"})
        assert resp.status_code == 200
        data = resp.json()
        assert "user_id" in data
        assert "token" in data
        assert len(data["token"]) > 0

    def test_register_duplicate_email(self, client):
        client.post("/auth/register", json={"email": "dup@b.nl", "password": "test1234"})
        resp = client.post("/auth/register", json={"email": "dup@b.nl", "password": "other"})
        assert resp.status_code == 409

    def test_register_invalid_email(self, client):
        resp = client.post("/auth/register", json={"email": "not-an-email", "password": "test"})
        assert resp.status_code == 422


class TestLogin:
    def test_login_success(self, client):
        client.post("/auth/register", json={"email": "login@b.nl", "password": "pw123"})
        resp = client.post("/auth/login", json={"email": "login@b.nl", "password": "pw123"})
        assert resp.status_code == 200
        data = resp.json()
        assert "user_id" in data
        assert "token" in data

    def test_login_wrong_password(self, client):
        client.post("/auth/register", json={"email": "login2@b.nl", "password": "pw123"})
        resp = client.post("/auth/login", json={"email": "login2@b.nl", "password": "wrong"})
        assert resp.status_code == 401

    def test_login_nonexistent_user(self, client):
        resp = client.post("/auth/login", json={"email": "noone@b.nl", "password": "pw"})
        assert resp.status_code == 401


class TestTokenAuth:
    def test_valid_token_stored_in_db(self, client):
        resp = client.post("/auth/register", json={"email": "tok@b.nl", "password": "pw"})
        token = resp.json()["token"]
        user_id = resp.json()["user_id"]
        # Verify the token is in the database

        db = client.app.state.db
        row = db.execute("SELECT user_id FROM auth_tokens WHERE token = ?", (token,)).fetchone()
        assert row is not None
        assert row["user_id"] == user_id

    def test_each_login_gets_unique_token(self, client):
        client.post("/auth/register", json={"email": "multi@b.nl", "password": "pw"})
        t1 = client.post("/auth/login", json={"email": "multi@b.nl", "password": "pw"}).json()[
            "token"
        ]
        t2 = client.post("/auth/login", json={"email": "multi@b.nl", "password": "pw"}).json()[
            "token"
        ]
        assert t1 != t2


class TestAuthSettings:
    """Tests for POST /auth/settings (E7-08)."""

    def test_update_learning_route(self, client):
        resp = client.post("/auth/register", json={"email": "set@b.nl", "password": "pw"})
        token = resp.json()["token"]
        headers = {"Authorization": f"Bearer {token}"}

        resp = client.post(
            "/auth/settings",
            json={"learning_route": "context_first"},
            headers=headers,
        )
        assert resp.status_code == 200
        assert resp.json()["learning_route"] == "context_first"

    def test_update_to_grammar_first(self, client):
        resp = client.post("/auth/register", json={"email": "gf@b.nl", "password": "pw"})
        token = resp.json()["token"]
        headers = {"Authorization": f"Bearer {token}"}

        client.post(
            "/auth/settings",
            json={"learning_route": "context_first"},
            headers=headers,
        )
        resp = client.post(
            "/auth/settings",
            json={"learning_route": "grammar_first"},
            headers=headers,
        )
        assert resp.status_code == 200
        assert resp.json()["learning_route"] == "grammar_first"

    def test_invalid_route_rejected(self, client):
        resp = client.post("/auth/register", json={"email": "inv@b.nl", "password": "pw"})
        token = resp.json()["token"]
        headers = {"Authorization": f"Bearer {token}"}

        resp = client.post(
            "/auth/settings",
            json={"learning_route": "invalid"},
            headers=headers,
        )
        assert resp.status_code == 422

    def test_no_auth_rejected(self, client):
        resp = client.post(
            "/auth/settings",
            json={"learning_route": "context_first"},
        )
        assert resp.status_code in (401, 422)

    def test_persists_to_profile(self, client):
        resp = client.post("/auth/register", json={"email": "per@b.nl", "password": "pw"})
        token = resp.json()["token"]
        headers = {"Authorization": f"Bearer {token}"}

        client.post(
            "/auth/settings",
            json={"learning_route": "context_first"},
            headers=headers,
        )
        # Check via /user/profile
        profile = client.get("/user/profile", headers=headers).json()
        assert profile["learning_route"] == "context_first"
