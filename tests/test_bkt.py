"""Tests for the BKT (Bayesian Knowledge Tracing) module."""

from uuid import uuid4

import pytest

from gymnasium_classica.graph.loader import load_graph_from_dict
from gymnasium_classica.models.learner import (
    LearnerModel,
    MasterySource,
    NodeState,
    ResponseType,
)
from gymnasium_classica.scheduling.bkt import (
    POSTERIOR_MAX,
    POSTERIOR_MIN,
    BKTParams,
    bkt_update_posterior,
    propagate_practice_correct,
    update_knoop_state,
)


class TestBKTUpdatePosterior:
    """Tests for the pure BKT update function."""

    def test_correct_increases_posterior(self):
        prior = 0.50
        result = bkt_update_posterior(prior, correct=True)
        assert result > prior

    def test_incorrect_decreases_posterior(self):
        prior = 0.50
        result = bkt_update_posterior(prior, correct=False)
        assert result < prior

    def test_low_prior_correct_increases(self):
        result = bkt_update_posterior(0.10, correct=True)
        assert result > 0.10

    def test_high_prior_incorrect_decreases(self):
        result = bkt_update_posterior(0.90, correct=False)
        assert result < 0.90

    def test_posterior_clamped_above_minimum(self):
        # Very low prior + incorrect should not go below POSTERIOR_MIN
        result = bkt_update_posterior(0.001, correct=False)
        assert result >= POSTERIOR_MIN

    def test_posterior_clamped_below_maximum(self):
        # Very high prior + correct should not exceed POSTERIOR_MAX
        result = bkt_update_posterior(0.999, correct=True)
        assert result <= POSTERIOR_MAX

    def test_transition_applied(self):
        # After Bayesian update, P(T) should push posterior higher
        params = BKTParams(p_transit=0.30, p_guess=0.20, p_slip=0.05)
        low_transit = bkt_update_posterior(0.50, True, BKTParams(p_transit=0.01))
        high_transit = bkt_update_posterior(0.50, True, params)
        assert high_transit > low_transit

    def test_custom_params(self):
        # High guess rate should push correct-update lower (less informative)
        high_guess = bkt_update_posterior(
            0.30, True, BKTParams(p_guess=0.50, p_slip=0.05, p_transit=0.10)
        )
        low_guess = bkt_update_posterior(
            0.30, True, BKTParams(p_guess=0.10, p_slip=0.05, p_transit=0.10)
        )
        assert low_guess > high_guess  # Low guess → correct is more informative


class TestUpdateNodeState:
    """Tests for updating NodeState via BKT."""

    def test_correct_updates_posterior(self):
        learner = LearnerModel(user_id=uuid4())
        state = update_knoop_state(learner, "LAT-G-MORF-NOM-D1", ResponseType.CORRECT)
        assert state.posterior_mastery > 0.10
        assert state.source == MasterySource.PRACTICE

    def test_slow_correct_treated_as_correct(self):
        learner = LearnerModel(user_id=uuid4())
        correct_state = update_knoop_state(
            LearnerModel(user_id=uuid4()), "LAT-G-MORF-NOM-D1", ResponseType.CORRECT
        )
        slow_state = update_knoop_state(learner, "LAT-G-MORF-NOM-D1", ResponseType.SLOW_CORRECT)
        assert slow_state.posterior_mastery == pytest.approx(correct_state.posterior_mastery)

    def test_incorrect_lowers_posterior(self):
        learner = LearnerModel(user_id=uuid4())
        # First set a moderate prior
        learner.knoop_states["LAT-G-MORF-NOM-D1"] = NodeState(
            knoop_id="LAT-G-MORF-NOM-D1", posterior_mastery=0.70
        )
        state = update_knoop_state(learner, "LAT-G-MORF-NOM-D1", ResponseType.INCORRECT)
        assert state.posterior_mastery < 0.70

    def test_creates_state_if_missing(self):
        learner = LearnerModel(user_id=uuid4())
        assert "LAT-G-MORF-NOM-D1" not in learner.knoop_states
        update_knoop_state(learner, "LAT-G-MORF-NOM-D1", ResponseType.CORRECT)
        assert "LAT-G-MORF-NOM-D1" in learner.knoop_states


class TestPropagation:
    """Tests for prerequisite/sibling propagation after correct responses."""

    def test_correct_boosts_prerequisites(self, sample_graph_data):
        graph = load_graph_from_dict(sample_graph_data)
        learner = LearnerModel(user_id=uuid4())

        # Initialize all nodes
        for node_id in graph.nodes:
            learner.knoop_states[node_id] = NodeState(knoop_id=node_id, posterior_mastery=0.50)

        # NOM-D1 has prerequisite DECL1-INTRO
        initial = learner.knoop_states["LAT-G-MORF-DECL1-INTRO"].posterior_mastery
        affected = propagate_practice_correct(learner, graph, "LAT-G-MORF-NOM-D1")
        assert "LAT-G-MORF-DECL1-INTRO" in affected
        assert learner.knoop_states["LAT-G-MORF-DECL1-INTRO"].posterior_mastery > initial

    def test_propagation_respects_weights(self, sample_graph_data):
        graph = load_graph_from_dict(sample_graph_data)
        learner = LearnerModel(user_id=uuid4())

        for node_id in graph.nodes:
            learner.knoop_states[node_id] = NodeState(knoop_id=node_id, posterior_mastery=0.50)

        propagate_practice_correct(learner, graph, "LAT-G-MORF-NOM-D1")

        # The boost should be proportional to encompassing_weight
        # DECL1-INTRO → NOM-D1 has weight 0.3, so boost = 0.10 * 0.3 = 0.03
        assert learner.knoop_states["LAT-G-MORF-DECL1-INTRO"].posterior_mastery == pytest.approx(
            0.53, abs=0.01
        )

    def test_siblings_get_smaller_boost(self, sample_graph_data):
        graph = load_graph_from_dict(sample_graph_data)
        learner = LearnerModel(user_id=uuid4())

        for node_id in graph.nodes:
            learner.knoop_states[node_id] = NodeState(knoop_id=node_id, posterior_mastery=0.50)

        # NOM-D1 and ACC-D1 share parent DECL1-INTRO
        propagate_practice_correct(learner, graph, "LAT-G-MORF-NOM-D1")

        # ACC-D1 should get a sibling boost (smaller than direct prereq boost)
        acc_posterior = learner.knoop_states["LAT-G-MORF-ACC-D1"].posterior_mastery
        assert acc_posterior > 0.50  # got some boost
        assert (
            acc_posterior < learner.knoop_states["LAT-G-MORF-DECL1-INTRO"].posterior_mastery
        )  # less than direct prereq

    def test_no_propagation_on_incorrect(self, sample_graph_data):
        graph = load_graph_from_dict(sample_graph_data)
        learner = LearnerModel(user_id=uuid4())

        for node_id in graph.nodes:
            learner.knoop_states[node_id] = NodeState(knoop_id=node_id, posterior_mastery=0.50)

        # propagate_practice_correct should NOT be called on incorrect
        # (this is the caller's responsibility, but verify the function only boosts)
        initial = learner.knoop_states["LAT-G-MORF-DECL1-INTRO"].posterior_mastery
        affected = propagate_practice_correct(learner, graph, "LAT-G-MORF-NOM-D1")
        # All affected nodes should have higher posteriors
        for nid in affected:
            assert learner.knoop_states[nid].posterior_mastery >= initial
