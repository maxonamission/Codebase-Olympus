"""Tests for D1-01: FastAPI app startup and health endpoint."""

import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from gymnasium_classica.api.database import init_db


@pytest.fixture()
def client():
    """Create a TestClient with a fresh temporary database."""
    from gymnasium_classica.api.app import create_app

    with tempfile.TemporaryDirectory() as tmp:
        db_path = Path(tmp) / "test.db"
        test_app = create_app(db_path=db_path)
        with TestClient(test_app) as c:
            yield c


class TestHealth:
    def test_health_returns_ok(self, client):
        resp = client.get("/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"
        assert isinstance(data["graph_nodes"], int)
        assert data["graph_nodes"] > 0
        assert isinstance(data["graph_edges"], int)
        assert data["graph_edges"] > 0


class TestDatabase:
    def test_init_db_creates_tables(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "test.db"
            conn = init_db(db_path)
            cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
            )
            tables = [row[0] for row in cursor.fetchall()]
            conn.close()
            assert "users" in tables
            assert "learner_models" in tables
            assert "auth_tokens" in tables

    def test_init_db_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "test.db"
            conn1 = init_db(db_path)
            conn1.close()
            conn2 = init_db(db_path)
            cursor = conn2.execute(
                "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
            )
            tables = [row[0] for row in cursor.fetchall()]
            conn2.close()
            assert "users" in tables
