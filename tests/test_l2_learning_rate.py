"""Tests voor learner-niveau leersnelheid (L2-03)."""

from datetime import datetime
from uuid import uuid4

from gymnasium_classica.models.learner import (
    ItemResponse,
    LearnerModel,
    NodeState,
    ResponseType,
)
from gymnasium_classica.scheduling.bkt import (
    LEARNING_RATE_MAX,
    LEARNING_RATE_MIN,
    bkt_update_posterior,
    estimate_learning_rate,
    update_node_state,
)

NOW = datetime(2026, 6, 4, 12, 0, 0)


def _resp(correct: bool, mastery_before: float) -> ItemResponse:
    return ItemResponse(
        timestamp=NOW,
        item_id="ITEM-X",
        correct=correct,
        response_time_ms=1000,
        node_id="LAT-G-X",
        direction=None,
        mastery_before=mastery_before,
    )


def _learner_with_history(*responses: ItemResponse) -> LearnerModel:
    learner = LearnerModel(user_id=uuid4())
    learner.node_states["LAT-G-X"] = NodeState(node_id="LAT-G-X", item_history=list(responses))
    return learner


class TestBktLearningRateModifier:
    def test_neutral_rate_reproduces_default(self):
        assert bkt_update_posterior(0.3, True) == bkt_update_posterior(
            0.3, True, learning_rate=1.0
        )

    def test_higher_rate_raises_posterior(self):
        base = bkt_update_posterior(0.3, True)
        fast = bkt_update_posterior(0.3, True, learning_rate=2.0)
        assert fast > base

    def test_transition_is_capped(self):
        # Zelfs een extreme rate houdt de posterior <= 0.999.
        assert bkt_update_posterior(0.5, True, learning_rate=50.0) <= 0.999


class TestEstimateLearningRate:
    def test_no_history_is_neutral(self):
        assert estimate_learning_rate(LearnerModel(user_id=uuid4())) == 1.0

    def test_outperforming_learner_above_one(self):
        learner = _learner_with_history(_resp(True, 0.2), _resp(True, 0.2), _resp(True, 0.2))
        assert estimate_learning_rate(learner) > 1.0

    def test_underperforming_learner_below_one(self):
        learner = _learner_with_history(_resp(False, 0.8), _resp(False, 0.8), _resp(False, 0.8))
        assert estimate_learning_rate(learner) < 1.0

    def test_clamped_to_bounds(self):
        high = _learner_with_history(_resp(True, 0.0))
        low = _learner_with_history(_resp(False, 1.0))
        assert estimate_learning_rate(high) <= LEARNING_RATE_MAX
        assert estimate_learning_rate(low) >= LEARNING_RATE_MIN


class TestUpdateNodeStateUsesLearnerRate:
    def test_faster_learner_gains_more_per_observation(self):
        slow = LearnerModel(user_id=uuid4(), learning_rate=1.0)
        fast = LearnerModel(user_id=uuid4(), learning_rate=2.0)
        update_node_state(slow, "LAT-G-X", ResponseType.CORRECT)
        update_node_state(fast, "LAT-G-X", ResponseType.CORRECT)
        assert (
            fast.node_states["LAT-G-X"].posterior_mastery
            > slow.node_states["LAT-G-X"].posterior_mastery
        )

    def test_faster_learner_reaches_mastery_in_fewer_steps(self):
        def steps_to_mastery(rate: float) -> int:
            learner = LearnerModel(user_id=uuid4(), learning_rate=rate)
            steps = 0
            while learner.node_states.get("LAT-G-X") is None or (
                learner.node_states["LAT-G-X"].posterior_mastery < 0.75 and steps < 50
            ):
                update_node_state(learner, "LAT-G-X", ResponseType.CORRECT)
                steps += 1
            return steps

        assert steps_to_mastery(2.0) <= steps_to_mastery(1.0)
