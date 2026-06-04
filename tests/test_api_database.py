"""Tests for D1-03: Database CRUD (users + learner_models)."""

import tempfile
from pathlib import Path
from uuid import uuid4

import pytest

from gymnasium_classica.api.database import (
    create_user,
    get_user,
    get_user_by_email,
    init_db,
    load_learner_model,
    save_learner_model,
    update_user,
)
from gymnasium_classica.models.learner import LearnerModel
from gymnasium_classica.models.user import User


@pytest.fixture()
def db():
    """Provide a fresh SQLite connection per test."""
    with tempfile.TemporaryDirectory() as tmp:
        conn = init_db(Path(tmp) / "test.db")
        yield conn
        conn.close()


# ---------------------------------------------------------------------------
# User CRUD
# ---------------------------------------------------------------------------


class TestCreateUser:
    def test_create_and_get(self, db):
        user = User(email="test@example.nl")
        create_user(db, user, "hash123")
        loaded = get_user(db, str(user.id))
        assert loaded is not None
        assert loaded.id == user.id
        assert loaded.email == "test@example.nl"

    def test_get_nonexistent_returns_none(self, db):
        assert get_user(db, "nonexistent-id") is None


class TestGetUserByEmail:
    def test_found(self, db):
        user = User(email="found@example.nl")
        create_user(db, user, "hash")
        loaded = get_user_by_email(db, "found@example.nl")
        assert loaded is not None
        assert loaded.id == user.id

    def test_not_found(self, db):
        assert get_user_by_email(db, "nope@x.nl") is None


class TestUpdateUser:
    def test_update_preserves_changes(self, db):
        user = User(email="upd@example.nl")
        create_user(db, user, "hash")
        user.examenjaar_ltc = 2027
        update_user(db, user)
        loaded = get_user(db, str(user.id))
        assert loaded is not None
        assert loaded.examenjaar_ltc == 2027


# ---------------------------------------------------------------------------
# LearnerModel CRUD
# ---------------------------------------------------------------------------


class TestLearnerModel:
    def test_save_and_load(self, db):
        uid = uuid4()
        model = LearnerModel(user_id=uid)
        save_learner_model(db, model)
        loaded = load_learner_model(db, str(uid))
        assert loaded is not None
        assert loaded.user_id == uid
        assert loaded.knoop_states == {}

    def test_load_nonexistent_returns_none(self, db):
        assert load_learner_model(db, "nonexistent") is None

    def test_upsert_overwrites(self, db):
        uid = uuid4()
        model = LearnerModel(user_id=uid)
        save_learner_model(db, model)

        # Update and save again
        model.intake_completed = True
        save_learner_model(db, model)

        loaded = load_learner_model(db, str(uid))
        assert loaded is not None
        assert loaded.intake_completed is True

    def test_roundtrip_with_knoop_states(self, db):
        from gymnasium_classica.models.learner import NodeState

        uid = uuid4()
        model = LearnerModel(user_id=uid)
        model.knoop_states["LAT-G-MORF-NOM-D1"] = NodeState(
            knoop_id="LAT-G-MORF-NOM-D1",
            posterior_mastery=0.75,
            easiness_factor=2.3,
            interval_days=5.0,
            repetitions=3,
        )
        save_learner_model(db, model)

        loaded = load_learner_model(db, str(uid))
        assert loaded is not None
        ks = loaded.knoop_states["LAT-G-MORF-NOM-D1"]
        assert ks.posterior_mastery == pytest.approx(0.75)
        assert ks.repetitions == 3
