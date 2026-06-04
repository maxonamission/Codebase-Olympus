"""Tests voor de meetlaag (L1-01): retentie-schatting en leerlingrapport."""

from datetime import datetime, timedelta
from uuid import uuid4

from gymnasium_classica.metrics import build_learner_report, estimated_retention
from gymnasium_classica.models.learner import (
    ItemResponse,
    LearnerModel,
    NodeState,
    SessionRecord,
)

NOW = datetime(2026, 6, 4, 12, 0, 0)


def _response(knoop_id: str, *, richting: str | None, mastery_before: float) -> ItemResponse:
    return ItemResponse(
        timestamp=NOW,
        item_id=f"{knoop_id}:i",
        correct=True,
        response_time_ms=2000,
        knoop_id=knoop_id,
        richting=richting,
        mastery_before=mastery_before,
    )


class TestEstimatedRetention:
    def test_never_reviewed_falls_back_to_posterior(self):
        state = NodeState(knoop_id="LAT-G-X", posterior_mastery=0.6, last_review=None)
        assert estimated_retention(state, NOW) == 0.6

    def test_full_retention_at_review_moment(self):
        state = NodeState(knoop_id="LAT-G-X", interval_days=5.0, last_review=NOW)
        assert estimated_retention(state, NOW) == 1.0

    def test_decays_over_time(self):
        state = NodeState(
            knoop_id="LAT-G-X", interval_days=5.0, last_review=NOW - timedelta(days=5)
        )
        r = estimated_retention(state, NOW)
        # Δt == stability -> exp(-1) ≈ 0.368
        assert 0.36 < r < 0.37

    def test_monotonic_decreasing(self):
        base = dict(knoop_id="LAT-G-X", interval_days=3.0)
        early = NodeState(**base, last_review=NOW - timedelta(days=1))
        late = NodeState(**base, last_review=NOW - timedelta(days=10))
        assert estimated_retention(early, NOW) > estimated_retention(late, NOW)

    def test_result_within_bounds(self):
        state = NodeState(
            knoop_id="LAT-G-X", interval_days=1.0, last_review=NOW - timedelta(days=365)
        )
        r = estimated_retention(state, NOW)
        assert 0.0 <= r <= 1.0


class TestBuildLearnerReport:
    def _learner(self) -> LearnerModel:
        learner = LearnerModel(user_id=uuid4())
        # new (posterior < 0.3), never reviewed
        learner.knoop_states["A"] = NodeState(knoop_id="A", posterior_mastery=0.1)
        # learning, reviewed 5 days ago, two responses (receptief + productief)
        learner.knoop_states["B"] = NodeState(
            knoop_id="B",
            posterior_mastery=0.5,
            interval_days=5.0,
            last_review=NOW - timedelta(days=5),
            item_history=[
                _response("B", richting="receptief", mastery_before=0.2),
                _response("B", richting="productief", mastery_before=0.4),
            ],
        )
        # mastered, reviewed today, one self-assess response (richting None)
        learner.knoop_states["C"] = NodeState(
            knoop_id="C",
            posterior_mastery=0.9,
            interval_days=10.0,
            last_review=NOW,
            item_history=[_response("C", richting=None, mastery_before=0.85)],
        )
        learner.session_history.append(
            SessionRecord(
                session_id="s1",
                started_at=NOW - timedelta(minutes=30),
                ended_at=NOW - timedelta(minutes=2),
            )
        )
        # Unfinished session (ended_at None) must not count toward study time.
        learner.session_history.append(
            SessionRecord(session_id="s2", started_at=NOW, ended_at=None)
        )
        return learner

    def test_counts_and_distribution(self):
        report = build_learner_report(self._learner(), NOW)
        assert report.total_reviews == 3
        assert report.mastery_distribution == {"new": 1, "learning": 1, "mastered": 1}
        assert report.reviews_by_richting == {"receptief": 1, "productief": 1, "onbekend": 1}

    def test_study_time_only_finished_sessions(self):
        report = build_learner_report(self._learner(), NOW)
        assert report.total_study_seconds == 28 * 60  # 30 - 2 minuten

    def test_average_retention_over_reviewed_nodes(self):
        report = build_learner_report(self._learner(), NOW)
        # B (~0.368) and C (1.0) are reviewed; A is not.
        assert report.average_retention is not None
        assert 0.6 < report.average_retention < 0.7

    def test_empty_learner(self):
        report = build_learner_report(LearnerModel(user_id=uuid4()), NOW)
        assert report.total_reviews == 0
        assert report.average_retention is None
        assert report.mastery_distribution == {"new": 0, "learning": 0, "mastered": 0}
