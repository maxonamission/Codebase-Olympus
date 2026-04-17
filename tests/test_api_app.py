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


class TestAudioEndpoint:
    """F1-04: `/audio/{filename}` serves .wav/.mp3 from data/audio/."""

    @pytest.fixture()
    def audio_client(self, tmp_path):
        from gymnasium_classica.api.app import create_app

        audio_dir = tmp_path / "audio"
        audio_dir.mkdir()
        (audio_dir / "LAT-V-F01-TEST.wav").write_bytes(b"RIFF____WAVEfmt ")
        (audio_dir / "LAT-V-F01-TEST.mp3").write_bytes(b"ID3mp3-fake")
        (audio_dir / "notallowed.txt").write_text("nope")

        db_path = tmp_path / "test.db"
        app = create_app(db_path=db_path, audio_dir=audio_dir)
        with TestClient(app) as c:
            yield c

    def test_wav_returns_200_and_audio_wav(self, audio_client):
        resp = audio_client.get("/audio/LAT-V-F01-TEST.wav")
        assert resp.status_code == 200
        assert resp.headers["content-type"] == "audio/wav"
        assert resp.content.startswith(b"RIFF")

    def test_mp3_returns_200_and_audio_mpeg(self, audio_client):
        resp = audio_client.get("/audio/LAT-V-F01-TEST.mp3")
        assert resp.status_code == 200
        assert resp.headers["content-type"] == "audio/mpeg"

    def test_unknown_file_returns_404(self, audio_client):
        resp = audio_client.get("/audio/DOES-NOT-EXIST.wav")
        assert resp.status_code == 404

    def test_disallowed_extension_returns_404(self, audio_client):
        resp = audio_client.get("/audio/notallowed.txt")
        assert resp.status_code == 404

    def test_path_traversal_rejected(self, audio_client):
        # FastAPI's path param doesn't span slashes, so ../secret reaches
        # the handler only via URL-encoded forms.  The explicit guard
        # covers ".." and backslashes too.
        resp = audio_client.get("/audio/..%2Fsecret.wav")
        assert resp.status_code == 404


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
