"""Tests voor de effectgrootte-metriek (L1-02): baseline + voortgang + cohort."""

from datetime import datetime
from uuid import uuid4

from gymnasium_classica.metrics import (
    capture_baseline,
    cohort_report,
    learner_progress,
)
from gymnasium_classica.models.learner import BaselineSnapshot, KnoopState, LearnerModel

NOW = datetime(2026, 6, 4, 12, 0, 0)


def _learner(current: dict[str, float], baseline: dict[str, float] | None) -> LearnerModel:
    learner = LearnerModel(user_id=uuid4())
    for kid, mastery in current.items():
        learner.knoop_states[kid] = KnoopState(knoop_id=kid, posterior_mastery=mastery)
    if baseline is not None:
        learner.baseline = BaselineSnapshot(captured_at=NOW, mastery=dict(baseline))
    return learner


class TestCaptureBaseline:
    def test_snapshots_current_posterior(self):
        learner = _learner({"A": 0.3, "B": 0.7}, baseline=None)
        snap = capture_baseline(learner, NOW)
        assert snap.captured_at == NOW
        assert snap.mastery == {"A": 0.3, "B": 0.7}

    def test_snapshot_is_independent_copy(self):
        learner = _learner({"A": 0.3}, baseline=None)
        snap = capture_baseline(learner, NOW)
        learner.knoop_states["A"].posterior_mastery = 0.9
        assert snap.mastery["A"] == 0.3  # niet meebewogen


class TestLearnerProgress:
    def test_none_without_baseline(self):
        assert learner_progress(_learner({"A": 0.5}, baseline=None)) is None

    def test_none_with_empty_baseline(self):
        learner = _learner({"A": 0.5}, baseline={})
        assert learner_progress(learner) is None

    def test_mean_delta_and_standardized_gain(self):
        # baseline mean 0.3, pstdev 0.1; current mean 0.7 -> delta 0.4 -> z = 4.0
        learner = _learner({"A": 0.6, "B": 0.8}, baseline={"A": 0.2, "B": 0.4})
        progress = learner_progress(learner)
        assert progress is not None
        assert abs(progress.baseline_mean - 0.3) < 1e-9
        assert abs(progress.current_mean - 0.7) < 1e-9
        assert abs(progress.mean_delta - 0.4) < 1e-9
        assert progress.standardized_gain is not None
        assert abs(progress.standardized_gain - 4.0) < 1e-9
        assert progress.n_nodes == 2

    def test_single_node_baseline_sd_zero_gives_none_z(self):
        learner = _learner({"A": 0.9}, baseline={"A": 0.5})
        progress = learner_progress(learner)
        assert progress is not None
        assert abs(progress.mean_delta - 0.4) < 1e-9
        assert progress.standardized_gain is None  # SD == 0

    def test_ignores_baseline_nodes_no_longer_present(self):
        learner = _learner({"A": 0.6}, baseline={"A": 0.2, "GONE": 0.4})
        progress = learner_progress(learner)
        assert progress is not None
        assert progress.n_nodes == 1
        assert abs(progress.mean_delta - 0.4) < 1e-9


class TestCohortReport:
    def _learner_with_delta(self, delta: float) -> LearnerModel:
        # one node, baseline 0.1, current 0.1 + delta -> mean_delta == delta
        return _learner({"A": 0.1 + delta}, baseline={"A": 0.1})

    def test_empty_cohort(self):
        report = cohort_report([])
        assert report.n_learners == 0
        assert report.mean_delta is None
        assert report.cohen_d is None

    def test_single_learner_no_sd(self):
        report = cohort_report([self._learner_with_delta(0.3)])
        assert report.n_learners == 1
        assert report.mean_delta is not None and abs(report.mean_delta - 0.3) < 1e-9
        assert report.sd_delta is None
        assert report.cohen_d is None

    def test_cohort_cohen_d(self):
        learners = [self._learner_with_delta(d) for d in (0.2, 0.4, 0.6)]
        report = cohort_report(learners)
        assert report.n_learners == 3
        assert abs(report.mean_delta - 0.4) < 1e-9
        assert report.sd_delta is not None and abs(report.sd_delta - 0.2) < 1e-9
        assert report.cohen_d is not None and abs(report.cohen_d - 2.0) < 1e-9

    def test_learners_without_baseline_are_skipped(self):
        learners = [self._learner_with_delta(0.4), _learner({"A": 0.9}, baseline=None)]
        report = cohort_report(learners)
        assert report.n_learners == 1
