"""Tests for F2-01: mentor role + learner linking."""

import sys
import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Make the scripts directory importable (for link_mentor.py)
_SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(_SCRIPTS_DIR))

from gymnasium_classica.api.database import (
    create_mentor_assignment,
    get_user,
    is_mentor_of,
    list_mentees,
    update_user,
)
from gymnasium_classica.models.user import Role


@pytest.fixture()
def client():
    """TestClient with a fresh temporary database per test."""
    from gymnasium_classica.api.app import create_app

    with tempfile.TemporaryDirectory() as tmp:
        db_path = Path(tmp) / "test.db"
        test_app = create_app(db_path=db_path)
        with TestClient(test_app) as c:
            yield c


def _register(client: TestClient, email: str, password: str = "pw123456") -> tuple[str, str]:
    """Register a user, returning (user_id, token)."""
    resp = client.post("/auth/register", json={"email": email, "password": password})
    assert resp.status_code == 200, resp.text
    body = resp.json()
    return body["user_id"], body["token"]


def _promote_to_mentor(client: TestClient, user_id: str) -> None:
    """Flip a freshly registered user to the MENTOR role via the DB."""
    db = client.app.state.db
    user = get_user(db, user_id)
    assert user is not None
    user.role = Role.MENTOR
    update_user(db, user)


# ---------------------------------------------------------------------------
# Model + DB layer
# ---------------------------------------------------------------------------


class TestRoleModel:
    def test_user_defaults_to_learner(self):
        from gymnasium_classica.models.user import User

        user = User(email="x@y.nl")
        assert user.role == Role.LEARNER

    def test_role_survives_json_roundtrip(self):
        from gymnasium_classica.models.user import User

        user = User(email="m@y.nl", role=Role.MENTOR)
        restored = User.model_validate_json(user.model_dump_json())
        assert restored.role == Role.MENTOR

    def test_legacy_user_json_without_role_defaults_learner(self):
        from gymnasium_classica.models.user import User

        # Simulate a row stored before F2-01 (no "role" key)
        user = User.model_validate_json('{"email": "old@y.nl"}')
        assert user.role == Role.LEARNER


class TestAssignmentCrud:
    def test_create_and_check(self, client):
        db = client.app.state.db
        m, _ = _register(client, "mentor@y.nl")
        learner, _ = _register(client, "learner@y.nl")
        assert not is_mentor_of(db, m, learner)
        create_mentor_assignment(db, m, learner)
        assert is_mentor_of(db, m, learner)

    def test_create_is_idempotent(self, client):
        db = client.app.state.db
        m, _ = _register(client, "mentor@y.nl")
        learner, _ = _register(client, "learner@y.nl")
        create_mentor_assignment(db, m, learner)
        create_mentor_assignment(db, m, learner)
        assert list_mentees(db, m) == [learner]

    def test_list_mentees_multiple(self, client):
        db = client.app.state.db
        m, _ = _register(client, "mentor@y.nl")
        l1, _ = _register(client, "l1@y.nl")
        l2, _ = _register(client, "l2@y.nl")
        create_mentor_assignment(db, m, l1)
        create_mentor_assignment(db, m, l2)
        assert set(list_mentees(db, m)) == {l1, l2}

    def test_list_mentees_empty(self, client):
        db = client.app.state.db
        m, _ = _register(client, "mentor@y.nl")
        assert list_mentees(db, m) == []


# ---------------------------------------------------------------------------
# Guard paths via endpoints (the three AC scenarios)
# ---------------------------------------------------------------------------


class TestMentorProfileGuard:
    def test_mentor_sees_own_mentee(self, client):
        mentor_id, mentor_tok = _register(client, "mentor@y.nl")
        learner_id, _ = _register(client, "learner@y.nl")
        _promote_to_mentor(client, mentor_id)
        create_mentor_assignment(client.app.state.db, mentor_id, learner_id)

        resp = client.get(
            f"/mentor/{learner_id}/profile",
            headers={"Authorization": f"Bearer {mentor_tok}"},
        )
        assert resp.status_code == 200
        assert resp.json()["email"] == "learner@y.nl"
        assert resp.json()["role"] == "learner"

    def test_mentor_403_on_unassigned_learner(self, client):
        mentor_id, mentor_tok = _register(client, "mentor@y.nl")
        other_id, _ = _register(client, "other@y.nl")
        _promote_to_mentor(client, mentor_id)
        # No assignment created on purpose

        resp = client.get(
            f"/mentor/{other_id}/profile",
            headers={"Authorization": f"Bearer {mentor_tok}"},
        )
        assert resp.status_code == 403

    def test_learner_403_on_mentor_endpoint(self, client):
        # A plain learner (never promoted) is forbidden even for themselves
        learner_id, learner_tok = _register(client, "learner@y.nl")
        resp = client.get(
            f"/mentor/{learner_id}/profile",
            headers={"Authorization": f"Bearer {learner_tok}"},
        )
        assert resp.status_code == 403

    def test_unauthenticated_401(self, client):
        learner_id, _ = _register(client, "learner@y.nl")
        resp = client.get(f"/mentor/{learner_id}/profile")
        assert resp.status_code == 422  # missing required Authorization header

    def test_invalid_token_401(self, client):
        learner_id, _ = _register(client, "learner@y.nl")
        resp = client.get(
            f"/mentor/{learner_id}/profile",
            headers={"Authorization": "Bearer nope"},
        )
        assert resp.status_code == 401


class TestMenteeList:
    def test_mentor_lists_mentees(self, client):
        mentor_id, mentor_tok = _register(client, "mentor@y.nl")
        l1, _ = _register(client, "l1@y.nl")
        l2, _ = _register(client, "l2@y.nl")
        _promote_to_mentor(client, mentor_id)
        create_mentor_assignment(client.app.state.db, mentor_id, l1)
        create_mentor_assignment(client.app.state.db, mentor_id, l2)

        resp = client.get("/mentor/mentees", headers={"Authorization": f"Bearer {mentor_tok}"})
        assert resp.status_code == 200
        emails = {m["email"] for m in resp.json()["mentees"]}
        assert emails == {"l1@y.nl", "l2@y.nl"}

    def test_learner_403_on_mentee_list(self, client):
        _, learner_tok = _register(client, "learner@y.nl")
        resp = client.get("/mentor/mentees", headers={"Authorization": f"Bearer {learner_tok}"})
        assert resp.status_code == 403


class TestLinkMentorScript:
    def test_script_promotes_and_links(self, monkeypatch, tmp_path):
        import importlib

        from gymnasium_classica.api.database import (
            create_user,
            get_user_by_email,
            init_db,
        )
        from gymnasium_classica.models.user import User

        db_path = tmp_path / "cli.db"
        conn = init_db(db_path)
        mentor = User(email="mentor@y.nl")
        learner = User(email="learner@y.nl")
        create_user(conn, mentor, "x")
        create_user(conn, learner, "y")
        conn.close()

        link_mentor = importlib.import_module("link_mentor")
        monkeypatch.setattr(
            "sys.argv",
            ["link_mentor", "--db", str(db_path), "mentor@y.nl", "learner@y.nl"],
        )
        link_mentor.main()

        conn = init_db(db_path)
        promoted = get_user_by_email(conn, "mentor@y.nl")
        assert promoted is not None
        assert promoted.role == Role.MENTOR
        assert is_mentor_of(conn, str(promoted.id), str(learner.id))
        conn.close()

    def test_script_errors_on_missing_user(self, monkeypatch, tmp_path):
        import importlib

        from gymnasium_classica.api.database import init_db

        db_path = tmp_path / "cli2.db"
        init_db(db_path).close()

        link_mentor = importlib.import_module("link_mentor")
        monkeypatch.setattr(
            "sys.argv",
            ["link_mentor", "--db", str(db_path), "ghost@y.nl", "nobody@y.nl"],
        )
        with pytest.raises(SystemExit) as exc:
            link_mentor.main()
        assert exc.value.code == 1
