"""Tests voor de motivatielaag-triggerlogica (L3-02)."""

from datetime import datetime, timedelta
from uuid import uuid4

from gymnasium_classica.experiments import framework
from gymnasium_classica.experiments.framework import (
    Experiment,
    ExperimentArm,
    StrategyParams,
)
from gymnasium_classica.models.learner import ItemResponse, LearnerModel, NodeState
from gymnasium_classica.motivation import (
    DEFAULT_MOTIVATION_CONFIG,
    MotivationConfig,
    MotivationMoment,
    evaluate_motivation,
    motivation_config_for,
)

BASE = datetime(2026, 6, 4, 12, 0, 0)


def _resp(correct: bool, mastery_before: float, node_id: str, offset: int) -> ItemResponse:
    return ItemResponse(
        timestamp=BASE + timedelta(minutes=offset),
        item_id=f"ITEM-{offset}",
        correct=correct,
        response_time_ms=1000,
        node_id=node_id,
        direction=None,
        mastery_before=mastery_before,
    )


def _learner(responses: list[ItemResponse], posterior: float = 0.8) -> LearnerModel:
    learner = LearnerModel(user_id=uuid4())
    by_node: dict[str, list[ItemResponse]] = {}
    for r in responses:
        by_node.setdefault(r.node_id, []).append(r)
    for node_id, history in by_node.items():
        learner.node_states[node_id] = NodeState(
            node_id=node_id, posterior_mastery=posterior, item_history=history
        )
    return learner


class TestEvaluateMotivation:
    def test_disabled_config_returns_none(self):
        learner = _learner([_resp(True, 0.2, "LAT-G-X", 0)])
        cue = evaluate_motivation(learner, MotivationConfig(enabled=False))
        assert cue is None

    def test_no_history_returns_none(self):
        assert evaluate_motivation(LearnerModel(user_id=uuid4())) is None

    def test_retrieval_dip_detected(self):
        # Laatste antwoord fout op een eerder-beheerste knoop.
        learner = _learner(
            [
                _resp(True, 0.8, "LAT-G-X", 0),
                _resp(False, 0.85, "LAT-G-X", 1),
            ]
        )
        cue = evaluate_motivation(learner)
        assert cue is not None and cue.moment == MotivationMoment.RETRIEVAL_DIP

    def test_desirable_difficulty_detected(self):
        # Reeks moeilijke-maar-correcte items (lage mastery_before, toch goed).
        learner = _learner([_resp(True, 0.3, "LAT-G-X", i) for i in range(3)], posterior=0.35)
        cue = evaluate_motivation(learner)
        assert cue is not None and cue.moment == MotivationMoment.DESIRABLE_DIFFICULTY

    def test_progress_gain_detected(self):
        # Niet alle correct (geen desirable), laatste correct (geen dip),
        # maar duidelijke mastery-winst t.o.v. mastery_before.
        learner = _learner(
            [
                _resp(True, 0.2, "LAT-G-X", 0),
                _resp(False, 0.3, "LAT-G-X", 1),
                _resp(True, 0.4, "LAT-G-X", 2),
            ],
            posterior=0.8,
        )
        cue = evaluate_motivation(learner)
        assert cue is not None and cue.moment == MotivationMoment.PROGRESS_GAIN
        assert cue.mastery_gain > 0.0

    def test_message_is_dutch_and_nonempty(self):
        learner = _learner([_resp(True, 0.3, "LAT-G-X", i) for i in range(3)], 0.35)
        cue = evaluate_motivation(learner)
        assert cue is not None and "werkt" in cue.message.lower()


class TestMotivationConfigVariant:
    def test_default_enabled(self):
        assert motivation_config_for(LearnerModel(user_id=uuid4())).enabled is True

    def test_experiment_arm_can_disable(self):
        exp = Experiment(
            "motiv_off",
            (
                ExperimentArm("a", StrategyParams(motivation_enabled=False)),
                ExperimentArm("b", StrategyParams(motivation_enabled=False)),
            ),
        )
        framework.ACTIVE_EXPERIMENTS.append(exp)
        try:
            cfg = motivation_config_for(LearnerModel(user_id=uuid4()))
            assert cfg.enabled is False
        finally:
            framework.ACTIVE_EXPERIMENTS.remove(exp)


def test_default_config_is_enabled():
    assert DEFAULT_MOTIVATION_CONFIG.enabled is True
