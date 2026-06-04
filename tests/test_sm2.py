"""Tests for the SM-2 spaced repetition module."""

from datetime import datetime

import pytest

from gymnasium_classica.models.learner import NodeState, ResponseType
from gymnasium_classica.scheduling.sm2 import (
    MIN_EASINESS_FACTOR,
    compute_quality,
    sm2_update,
)


class TestComputeQuality:
    def test_correct_maps_to_5(self):
        assert compute_quality(ResponseType.CORRECT) == 5

    def test_slow_correct_maps_to_3(self):
        assert compute_quality(ResponseType.SLOW_CORRECT) == 3

    def test_incorrect_maps_to_0(self):
        assert compute_quality(ResponseType.INCORRECT) == 0


class TestSM2Update:
    def _fresh_state(self) -> NodeState:
        return NodeState(node_id="LAT-G-MORF-NOM-D1")

    def test_first_correct_sets_interval_1(self):
        state = self._fresh_state()
        sm2_update(state, ResponseType.CORRECT)
        assert state.repetitions == 1
        assert state.interval_days == pytest.approx(1.0)

    def test_second_correct_sets_interval_6(self):
        state = self._fresh_state()
        sm2_update(state, ResponseType.CORRECT)
        sm2_update(state, ResponseType.CORRECT)
        assert state.repetitions == 2
        assert state.interval_days == pytest.approx(6.0)

    def test_third_correct_applies_ef(self):
        state = self._fresh_state()
        sm2_update(state, ResponseType.CORRECT)
        sm2_update(state, ResponseType.CORRECT)
        sm2_update(state, ResponseType.CORRECT)
        assert state.repetitions == 3
        # interval = 6.0 * EF (EF starts at 2.5, increases with quality 5)
        assert state.interval_days > 6.0

    def test_incorrect_resets_repetitions(self):
        state = self._fresh_state()
        # Build up some repetitions
        sm2_update(state, ResponseType.CORRECT)
        sm2_update(state, ResponseType.CORRECT)
        assert state.repetitions == 2
        # Now fail
        sm2_update(state, ResponseType.INCORRECT)
        assert state.repetitions == 0
        assert state.interval_days == pytest.approx(1.0)

    def test_ef_increases_on_easy(self):
        state = self._fresh_state()
        initial_ef = state.easiness_factor
        sm2_update(state, ResponseType.CORRECT)  # quality 5
        assert state.easiness_factor > initial_ef

    def test_ef_decreases_on_difficult(self):
        state = self._fresh_state()
        initial_ef = state.easiness_factor
        sm2_update(state, ResponseType.INCORRECT)  # quality 0
        assert state.easiness_factor < initial_ef

    def test_ef_minimum_1_3(self):
        state = self._fresh_state()
        # Repeatedly fail to drive EF down
        for _ in range(20):
            sm2_update(state, ResponseType.INCORRECT)
        assert state.easiness_factor >= MIN_EASINESS_FACTOR

    def test_slow_correct_is_threshold(self):
        state = self._fresh_state()
        sm2_update(state, ResponseType.SLOW_CORRECT)  # quality 3
        # quality 3 is the boundary: repetitions should increase
        assert state.repetitions == 1

    def test_last_review_updated(self):
        state = self._fresh_state()
        now = datetime(2026, 4, 12, 10, 0)
        sm2_update(state, ResponseType.CORRECT, review_time=now)
        assert state.last_review == now

    def test_last_response_updated(self):
        state = self._fresh_state()
        sm2_update(state, ResponseType.SLOW_CORRECT)
        assert state.last_response == ResponseType.SLOW_CORRECT

    def test_interval_progression_over_5_reviews(self):
        """After 5 correct reviews, interval should grow substantially."""
        state = self._fresh_state()
        intervals = []
        for _ in range(5):
            sm2_update(state, ResponseType.CORRECT)
            intervals.append(state.interval_days)
        # 1, 6, 6*EF, 6*EF*EF, ...
        assert intervals[0] == pytest.approx(1.0)
        assert intervals[1] == pytest.approx(6.0)
        assert intervals[2] > 6.0
        assert intervals[3] > intervals[2]
        assert intervals[4] > intervals[3]
