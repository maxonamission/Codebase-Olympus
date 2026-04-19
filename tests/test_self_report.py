"""Tests for B5-02: self-report flow and BKT integration with reduced confidence."""

from datetime import datetime
from uuid import uuid4

import pytest

from gymnasium_classica.models.learner import (
    KnoopState,
    LearnerModel,
    MasterySource,
    OfflineAssignment,
    ResponseType,
    SelfReportResponse,
)
from gymnasium_classica.scheduling.bkt import (
    DEFAULT_P_GUESS,
    DEFAULT_P_SLIP,
    SELF_REPORT_BKT_PARAMS,
    SELF_REPORT_P_GUESS,
    SELF_REPORT_P_SLIP,
    BKTParams,
    bkt_update_posterior,
    update_knoop_state,
)
from gymnasium_classica.scheduling.session import process_self_report


class TestSelfReportBKTParams:
    """Tests for the self-report BKT parameter variant."""

    def test_self_report_params_values(self):
        assert SELF_REPORT_P_GUESS == 0.35
        assert SELF_REPORT_P_SLIP == 0.15

    def test_self_report_params_higher_than_default(self):
        assert SELF_REPORT_P_GUESS > DEFAULT_P_GUESS
        assert SELF_REPORT_P_SLIP > DEFAULT_P_SLIP

    def test_self_report_params_is_bkt_params(self):
        assert isinstance(SELF_REPORT_BKT_PARAMS, BKTParams)
        assert SELF_REPORT_BKT_PARAMS.p_guess == SELF_REPORT_P_GUESS
        assert SELF_REPORT_BKT_PARAMS.p_slip == SELF_REPORT_P_SLIP

    def test_correct_update_less_informative_with_self_report(self):
        """Self-report correct should produce a smaller posterior increase
        than a normal correct, because higher P(G) means a correct answer
        is less diagnostic of true mastery."""
        prior = 0.30
        normal = bkt_update_posterior(prior, correct=True)
        self_report = bkt_update_posterior(prior, correct=True, params=SELF_REPORT_BKT_PARAMS)
        assert self_report < normal

    def test_incorrect_update_less_punishing_with_self_report(self):
        """Self-report incorrect should produce a smaller posterior decrease
        than a normal incorrect, because higher P(S) means an incorrect answer
        is less diagnostic of true lack of mastery."""
        prior = 0.70
        normal = bkt_update_posterior(prior, correct=False)
        self_report = bkt_update_posterior(prior, correct=False, params=SELF_REPORT_BKT_PARAMS)
        assert self_report > normal


class TestSelfReportResponse:
    """Tests for the SelfReportResponse enum."""

    def test_enum_values(self):
        assert SelfReportResponse.CORRECT == "correct"
        assert SelfReportResponse.PARTIAL == "partial"
        assert SelfReportResponse.INCORRECT == "incorrect"


class TestProcessSelfReport:
    """Tests for the process_self_report function."""

    def _make_assignment(self) -> OfflineAssignment:
        return OfflineAssignment(
            knoop_id="LAT-G-MORF-DECL1-INTRO",
            item_id="ITEM-OFFLINE-D1-001",
            assigned_at=datetime(2026, 4, 13),
        )

    def test_correct_increases_posterior(self):
        learner = LearnerModel(user_id=uuid4())
        learner.knoop_states["LAT-G-MORF-DECL1-INTRO"] = KnoopState(
            knoop_id="LAT-G-MORF-DECL1-INTRO", posterior_mastery=0.30
        )
        assignment = self._make_assignment()

        process_self_report(learner, assignment, SelfReportResponse.CORRECT)

        state = learner.knoop_states["LAT-G-MORF-DECL1-INTRO"]
        assert state.posterior_mastery > 0.30

    def test_partial_increases_posterior(self):
        learner = LearnerModel(user_id=uuid4())
        learner.knoop_states["LAT-G-MORF-DECL1-INTRO"] = KnoopState(
            knoop_id="LAT-G-MORF-DECL1-INTRO", posterior_mastery=0.30
        )
        assignment = self._make_assignment()

        process_self_report(learner, assignment, SelfReportResponse.PARTIAL)

        state = learner.knoop_states["LAT-G-MORF-DECL1-INTRO"]
        assert state.posterior_mastery > 0.30

    def test_incorrect_decreases_posterior(self):
        learner = LearnerModel(user_id=uuid4())
        learner.knoop_states["LAT-G-MORF-DECL1-INTRO"] = KnoopState(
            knoop_id="LAT-G-MORF-DECL1-INTRO", posterior_mastery=0.70
        )
        assignment = self._make_assignment()

        process_self_report(learner, assignment, SelfReportResponse.INCORRECT)

        state = learner.knoop_states["LAT-G-MORF-DECL1-INTRO"]
        assert state.posterior_mastery < 0.70

    def test_uses_self_report_params_not_default(self):
        """Verify that self-report uses the higher P(G)/P(S) params."""
        learner_sr = LearnerModel(user_id=uuid4())
        learner_sr.knoop_states["LAT-G-MORF-DECL1-INTRO"] = KnoopState(
            knoop_id="LAT-G-MORF-DECL1-INTRO", posterior_mastery=0.30
        )
        assignment = self._make_assignment()
        process_self_report(learner_sr, assignment, SelfReportResponse.CORRECT)
        sr_posterior = learner_sr.knoop_states["LAT-G-MORF-DECL1-INTRO"].posterior_mastery

        # Compare with normal BKT update
        learner_normal = LearnerModel(user_id=uuid4())
        learner_normal.knoop_states["LAT-G-MORF-DECL1-INTRO"] = KnoopState(
            knoop_id="LAT-G-MORF-DECL1-INTRO", posterior_mastery=0.30
        )
        update_knoop_state(learner_normal, "LAT-G-MORF-DECL1-INTRO", ResponseType.CORRECT)
        normal_posterior = learner_normal.knoop_states["LAT-G-MORF-DECL1-INTRO"].posterior_mastery

        # Self-report should produce a lower posterior (less informative)
        assert sr_posterior < normal_posterior

    def test_marks_assignment_completed(self):
        learner = LearnerModel(user_id=uuid4())
        assignment = self._make_assignment()

        process_self_report(learner, assignment, SelfReportResponse.CORRECT)

        assert assignment.completed is True

    def test_sets_mastery_source(self):
        learner = LearnerModel(user_id=uuid4())
        assignment = self._make_assignment()

        process_self_report(learner, assignment, SelfReportResponse.CORRECT)

        state = learner.knoop_states["LAT-G-MORF-DECL1-INTRO"]
        assert state.source == MasterySource.SELF_REPORT

    def test_increments_self_report_count(self):
        learner = LearnerModel(user_id=uuid4())
        assignment = self._make_assignment()

        assert learner.self_report_count == 0
        process_self_report(learner, assignment, SelfReportResponse.CORRECT)
        assert learner.self_report_count == 1

    def test_creates_state_if_missing(self):
        learner = LearnerModel(user_id=uuid4())
        assignment = self._make_assignment()

        assert "LAT-G-MORF-DECL1-INTRO" not in learner.knoop_states
        process_self_report(learner, assignment, SelfReportResponse.CORRECT)
        assert "LAT-G-MORF-DECL1-INTRO" in learner.knoop_states


class TestSelfReportRatioTracking:
    """Tests for self-report vs OCR ratio tracking on LearnerModel."""

    def test_initial_counts_zero(self):
        learner = LearnerModel(user_id=uuid4())
        assert learner.self_report_count == 0
        assert learner.ocr_verified_count == 0

    def test_self_report_ratio_after_multiple_reports(self):
        learner = LearnerModel(user_id=uuid4())
        now = datetime(2026, 4, 13)

        for i in range(3):
            assignment = OfflineAssignment(
                knoop_id="LAT-G-MORF-DECL1-INTRO",
                item_id=f"ITEM-{i}",
                assigned_at=now,
            )
            process_self_report(learner, assignment, SelfReportResponse.CORRECT)

        assert learner.self_report_count == 3
        # OCR count stays 0 — ratio is 3:0
        assert learner.ocr_verified_count == 0

    def test_ratio_with_mixed_sources(self):
        learner = LearnerModel(user_id=uuid4())
        now = datetime(2026, 4, 13)

        # 2 self-reports
        for i in range(2):
            assignment = OfflineAssignment(
                knoop_id="LAT-G-MORF-DECL1-INTRO",
                item_id=f"ITEM-SR-{i}",
                assigned_at=now,
            )
            process_self_report(learner, assignment, SelfReportResponse.CORRECT)

        # Simulate 1 OCR-verified (direct increment, as OCR pipeline is B6)
        learner.ocr_verified_count += 1

        total = learner.self_report_count + learner.ocr_verified_count
        sr_ratio = learner.self_report_count / total
        assert sr_ratio == pytest.approx(2 / 3)

    def test_serialization_roundtrip(self):
        learner = LearnerModel(user_id=uuid4())
        learner.self_report_count = 5
        learner.ocr_verified_count = 3
        data = learner.model_dump()
        learner2 = LearnerModel(**data)
        assert learner2.self_report_count == 5
        assert learner2.ocr_verified_count == 3
