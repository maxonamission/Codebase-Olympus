"""Tests for LearnerModel, KnoopState, and related models."""

from datetime import datetime
from uuid import uuid4

import pytest
from pydantic import ValidationError

from gymnasium_classica.models.learner import (
    ItemResponse,
    KnoopState,
    LearnerModel,
    SessionRecord,
)


class TestKnoopState:
    """Tests for the KnoopState model."""

    def test_defaults(self):
        state = KnoopState(knoop_id="LAT-G-MORF-NOM-D1")
        assert state.posterior_mastery == 0.0
        assert state.easiness_factor == 2.5
        assert state.interval_days == 0.0
        assert state.repetitions == 0
        assert state.last_review is None
        assert state.last_response is None
        assert state.item_history == []

    def test_mastery_boundary_zero(self):
        state = KnoopState(knoop_id="LAT-G-MORF-NOM-D1", posterior_mastery=0.0)
        assert state.posterior_mastery == 0.0

    def test_mastery_boundary_one(self):
        state = KnoopState(knoop_id="LAT-G-MORF-NOM-D1", posterior_mastery=1.0)
        assert state.posterior_mastery == 1.0

    def test_mastery_below_zero_rejected(self):
        with pytest.raises(ValidationError):
            KnoopState(knoop_id="LAT-G-MORF-NOM-D1", posterior_mastery=-0.1)

    def test_mastery_above_one_rejected(self):
        with pytest.raises(ValidationError):
            KnoopState(knoop_id="LAT-G-MORF-NOM-D1", posterior_mastery=1.1)

    def test_easiness_must_be_positive(self):
        with pytest.raises(ValidationError):
            KnoopState(knoop_id="LAT-G-MORF-NOM-D1", easiness_factor=0.0)

    def test_interval_cannot_be_negative(self):
        with pytest.raises(ValidationError):
            KnoopState(knoop_id="LAT-G-MORF-NOM-D1", interval_days=-1.0)

    def test_all_response_types(self):
        for rt in ["correct", "incorrect", "slow_correct"]:
            state = KnoopState(knoop_id="LAT-G-MORF-NOM-D1", last_response=rt)
            assert state.last_response == rt

    def test_invalid_response_type_rejected(self):
        with pytest.raises(ValidationError):
            KnoopState(knoop_id="LAT-G-MORF-NOM-D1", last_response="timeout")


class TestItemResponse:
    """Tests for the ItemResponse model."""

    def test_valid_construction(self):
        resp = ItemResponse(
            timestamp=datetime(2026, 4, 12, 10, 0),
            item_id="ITEM-001",
            correct=True,
            response_time_ms=2500,
            knoop_id="LAT-G-MORF-NOM-D1",
            richting="receptief",
            mastery_before=0.4,
        )
        assert resp.correct is True
        assert resp.response_time_ms == 2500
        assert resp.knoop_id == "LAT-G-MORF-NOM-D1"
        assert resp.richting == "receptief"
        assert resp.mastery_before == 0.4

    def test_response_time_cannot_be_negative(self):
        with pytest.raises(ValidationError):
            ItemResponse(
                timestamp=datetime.now(),
                item_id="ITEM-001",
                correct=False,
                response_time_ms=-1,
                knoop_id="LAT-G-MORF-NOM-D1",
                richting="receptief",
                mastery_before=0.4,
            )

    def test_meetlaag_fields_are_required(self):
        # L1-01: knoop_id, richting en mastery_before zijn verplicht (geen default).
        with pytest.raises(ValidationError):
            ItemResponse(
                timestamp=datetime.now(),
                item_id="ITEM-001",
                correct=True,
                response_time_ms=1000,
            )


class TestSessionRecord:
    """Tests for the SessionRecord model."""

    def test_valid_construction(self):
        session = SessionRecord(
            session_id="SES-001",
            started_at=datetime(2026, 4, 12, 10, 0),
        )
        assert session.ended_at is None
        assert session.items_reviewed == []

    def test_with_items(self):
        session = SessionRecord(
            session_id="SES-001",
            started_at=datetime(2026, 4, 12, 10, 0),
            ended_at=datetime(2026, 4, 12, 10, 30),
            items_reviewed=["ITEM-001", "ITEM-002"],
        )
        assert len(session.items_reviewed) == 2


class TestLearnerModel:
    """Tests for the LearnerModel model."""

    def test_empty_initial_state(self):
        uid = uuid4()
        model = LearnerModel(user_id=uid)
        assert model.user_id == uid
        assert model.knoop_states == {}
        assert model.session_history == []

    def test_add_knoop_state(self):
        uid = uuid4()
        model = LearnerModel(user_id=uid)
        state = KnoopState(knoop_id="LAT-G-MORF-NOM-D1", posterior_mastery=0.7)
        model.knoop_states["LAT-G-MORF-NOM-D1"] = state
        assert "LAT-G-MORF-NOM-D1" in model.knoop_states
        assert model.knoop_states["LAT-G-MORF-NOM-D1"].posterior_mastery == 0.7

    def test_serialization_roundtrip(self):
        uid = uuid4()
        model = LearnerModel(
            user_id=uid,
            knoop_states={
                "LAT-G-MORF-NOM-D1": KnoopState(
                    knoop_id="LAT-G-MORF-NOM-D1", posterior_mastery=0.85
                ),
            },
        )
        dumped = model.model_dump()
        model2 = LearnerModel(**dumped)
        assert model2.user_id == uid
        assert model2.knoop_states["LAT-G-MORF-NOM-D1"].posterior_mastery == 0.85
