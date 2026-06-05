"""Tests for the bijspijker API endpoints (M1-03)."""

import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client():
    from gymnasium_classica.api.app import create_app

    with tempfile.TemporaryDirectory() as tmp:
        db_path = Path(tmp) / "test.db"
        test_app = create_app(db_path=db_path)
        with TestClient(test_app) as c:
            yield c


def _auth_header(client, email="bijspijker@example.nl"):
    resp = client.post("/auth/register", json={"email": email, "password": "pw1234"})
    return resp.json()["user_id"], {"Authorization": f"Bearer {resp.json()['token']}"}


class TestBijspijkerIntake:
    def test_intake_with_pallas_returns_plan(self, client):
        _, headers = _auth_header(client, "pallas@example.nl")
        resp = client.post(
            "/intake/bijspijker",
            json={"methode_grc": "pallas", "hoofdstuk_grc": 4},
            headers=headers,
        )
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert data["doelset_size"] > 0
        assert data["diagnose_size"] > 0
        assert data["eta_dagen"] > 0
        assert 0.0 <= data["fractie_bij"] <= 1.0
        assert len(data["eerste_diagnose_node_ids"]) > 0

    def test_intake_two_languages(self, client):
        _, headers = _auth_header(client, "beide@example.nl")
        resp = client.post(
            "/intake/bijspijker",
            json={
                "methode_lat": "fortuna",
                "hoofdstuk_lat": 3,
                "methode_grc": "pallas",
                "hoofdstuk_grc": 2,
            },
            headers=headers,
        )
        assert resp.status_code == 200, resp.text
        assert resp.json()["doelset_size"] > 0

    def test_intake_without_any_language_is_400(self, client):
        _, headers = _auth_header(client, "leeg@example.nl")
        resp = client.post("/intake/bijspijker", json={}, headers=headers)
        assert resp.status_code == 400

    def test_intake_unknown_method_is_400(self, client):
        _, headers = _auth_header(client, "onbekend@example.nl")
        resp = client.post(
            "/intake/bijspijker",
            json={"methode_lat": "nonexistent", "hoofdstuk_lat": 1},
            headers=headers,
        )
        assert resp.status_code == 400

    def test_intake_requires_auth(self, client):
        resp = client.post(
            "/intake/bijspijker", json={"methode_grc": "pallas", "hoofdstuk_grc": 1}
        )
        assert resp.status_code == 422


class TestBijspijkerProgress:
    def test_progress_after_intake(self, client):
        _, headers = _auth_header(client, "voortgang@example.nl")
        client.post(
            "/intake/bijspijker",
            json={"methode_grc": "pallas", "hoofdstuk_grc": 4},
            headers=headers,
        )
        resp = client.get("/progress/bijspijker", headers=headers)
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert data["modus"] == "bijspijker"
        assert data["doelset_size"] > 0
        assert data["diagnose_size"] >= 0
        assert isinstance(data["open_topics"], list)
        if data["open_topics"]:
            assert "title_nl" in data["open_topics"][0]

    def test_progress_in_staatsexamen_mode_is_400(self, client):
        # Fresh user defaults to staatsexamen and never set a bijspijker goal.
        _, headers = _auth_header(client, "staats@example.nl")
        resp = client.get("/progress/bijspijker", headers=headers)
        assert resp.status_code == 400

    def test_progress_requires_auth(self, client):
        resp = client.get("/progress/bijspijker")
        assert resp.status_code == 422
