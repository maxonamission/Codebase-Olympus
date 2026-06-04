"""Tests voor het A/B-experiment- en variant-framework (L1-03)."""

from uuid import UUID, uuid4

import pytest

from gymnasium_classica.experiments import framework
from gymnasium_classica.experiments.framework import (
    DEFAULT_PARAMS,
    Experiment,
    ExperimentArm,
    StrategyParams,
    assign_variants,
    resolve_params,
    strategy_params_for,
)
from gymnasium_classica.models.learner import LearnerModel, NodeState, ResponseType
from gymnasium_classica.scheduling.sm2 import sm2_update

WIDE = ExperimentArm("wide", StrategyParams(spacing_multiplier=2.0))
CONTROL = ExperimentArm("control")  # default params
SPACING_EXP = Experiment("spacing_2026", (CONTROL, WIDE))


@pytest.fixture
def active_spacing_experiment():
    """Activeer het spacing-experiment voor de duur van een test."""
    framework.ACTIVE_EXPERIMENTS.append(SPACING_EXP)
    yield SPACING_EXP
    framework.ACTIVE_EXPERIMENTS.remove(SPACING_EXP)


class TestExperimentValidation:
    def test_requires_two_arms(self):
        with pytest.raises(ValueError, match="at least 2 arms"):
            Experiment("x", (CONTROL,))

    def test_rejects_duplicate_arm_names(self):
        with pytest.raises(ValueError, match="duplicate arm"):
            Experiment("x", (CONTROL, ExperimentArm("control")))


class TestAssignment:
    def test_deterministic(self):
        uid = uuid4()
        assert SPACING_EXP.assign(uid).name == SPACING_EXP.assign(uid).name

    def test_distinct_users_can_differ(self):
        # Vaste seeds met bekende, verschillende uitkomsten.
        names = {SPACING_EXP.assign(f"user-{i}").name for i in range(20)}
        assert names == {"control", "wide"}  # beide armen komen voor

    def test_balanced_distribution(self):
        counts = {"control": 0, "wide": 0}
        for i in range(1000):
            counts[SPACING_EXP.assign(f"user-{i}").name] += 1
        # SHA-256-verdeling over 2 armen: ruim binnen 40-60%.
        assert 400 <= counts["control"] <= 600
        assert counts["control"] + counts["wide"] == 1000


class TestResolveParams:
    def test_default_when_no_arms(self):
        assert resolve_params({}) == DEFAULT_PARAMS

    def test_resolves_assigned_arm(self, active_spacing_experiment):
        params = resolve_params({"spacing_2026": "wide"})
        assert params.spacing_multiplier == 2.0

    def test_unknown_arm_falls_back_to_default(self, active_spacing_experiment):
        assert resolve_params({"spacing_2026": "ghost"}) == DEFAULT_PARAMS


class TestStrategyParamsForLearner:
    def test_no_active_experiments_is_noop(self):
        learner = LearnerModel(user_id=uuid4())
        assert strategy_params_for(learner) == DEFAULT_PARAMS
        assert learner.experiment_arms == {}  # niets vastgelegd

    def test_assigns_and_records(self, active_spacing_experiment):
        learner = LearnerModel(user_id=uuid4())
        params = strategy_params_for(learner)
        assert "spacing_2026" in learner.experiment_arms
        # vastgelegde arm en effectieve params zijn consistent
        arm = learner.experiment_arms["spacing_2026"]
        assert (params.spacing_multiplier == 2.0) == (arm == "wide")

    def test_recorded_assignment_is_stable(self, active_spacing_experiment):
        learner = LearnerModel(user_id=uuid4())
        first = strategy_params_for(learner)
        recorded = dict(learner.experiment_arms)
        second = strategy_params_for(learner)
        assert learner.experiment_arms == recorded and first == second


class TestVariantChangesBehaviour:
    def test_spacing_multiplier_changes_sm2_interval(self):
        default_state = sm2_update(NodeState(node_id="LAT-G-X"), ResponseType.CORRECT)
        wide_state = sm2_update(
            NodeState(node_id="LAT-G-X"), ResponseType.CORRECT, spacing_multiplier=2.0
        )
        assert default_state.interval_days == 1.0
        assert wide_state.interval_days == 2.0  # aantoonbaar gewijzigd gedrag

    def test_default_multiplier_reproduces_baseline(self):
        # Tweede review: vaste SECOND_INTERVAL = 6.0 dagen, ongewijzigd.
        state = NodeState(node_id="LAT-G-X", repetitions=1)
        sm2_update(state, ResponseType.CORRECT, spacing_multiplier=1.0)
        assert state.interval_days == 6.0


def test_assign_variants_empty_without_active_experiments():
    assert assign_variants(UUID(int=0)) == {}
