"""Tests voor de learner-model-strategie-interface (L2-02)."""

from uuid import uuid4

import networkx as nx
import pytest

from gymnasium_classica.learner_strategy import (
    BKTStrategy,
    GraphAwareBKTStrategy,
    LearnerModelStrategy,
    get_strategy,
    set_strategy,
)
from gymnasium_classica.models.graph import EdgeType, PrerequisiteEdge
from gymnasium_classica.models.learner import LearnerModel, NodeState, ResponseType
from gymnasium_classica.scheduling.bkt import propagate_practice_correct, update_node_state


def _prereq_graph(weight: float = 1.0) -> nx.DiGraph:
    g = nx.DiGraph()
    g.add_node("LAT-G-A")
    g.add_node("LAT-G-B")
    g.add_edge(
        "LAT-G-A",
        "LAT-G-B",
        edge=PrerequisiteEdge(
            source_id="LAT-G-A",
            target_id="LAT-G-B",
            type=EdgeType.PREREQUISITE,
            encompassing_weight=weight,
        ),
    )
    return g


def _learner_with_mastered_a() -> LearnerModel:
    learner = LearnerModel(user_id=uuid4())
    learner.node_states["LAT-G-A"] = NodeState(node_id="LAT-G-A", posterior_mastery=0.9)
    return learner


class TestInterfaceContract:
    def test_bkt_is_a_strategy(self):
        assert isinstance(BKTStrategy(), LearnerModelStrategy)
        assert isinstance(GraphAwareBKTStrategy(), LearnerModelStrategy)

    def test_predict_returns_prior_for_unknown_node(self):
        learner = LearnerModel(user_id=uuid4())
        assert BKTStrategy().predict(learner, "LAT-G-X") == 0.10


class TestActiveStrategyRegistry:
    def test_default_is_bkt(self):
        assert isinstance(get_strategy(), BKTStrategy)

    def test_set_and_restore(self):
        original = get_strategy()
        try:
            ga = GraphAwareBKTStrategy()
            set_strategy(ga)
            assert get_strategy() is ga
        finally:
            set_strategy(original)
        assert get_strategy() is original


class TestBKTParity:
    def test_update_matches_direct_bkt_plus_propagation(self):
        g = _prereq_graph()
        via_strategy = _learner_with_mastered_a()
        direct = _learner_with_mastered_a()

        BKTStrategy().update(via_strategy, g, "LAT-G-B", ResponseType.CORRECT)

        update_node_state(direct, "LAT-G-B", ResponseType.CORRECT)
        propagate_practice_correct(direct, g, "LAT-G-B")

        assert (
            via_strategy.node_states["LAT-G-B"].posterior_mastery
            == direct.node_states["LAT-G-B"].posterior_mastery
        )
        # Propagatie naar de prerequisite is identiek meegelopen.
        assert (
            via_strategy.node_states["LAT-G-A"].posterior_mastery
            == direct.node_states["LAT-G-A"].posterior_mastery
        )


class TestGraphAwareAdjustment:
    def test_strong_prerequisites_raise_posterior_vs_plain_bkt(self):
        g = _prereq_graph()
        plain = _learner_with_mastered_a()
        aware = _learner_with_mastered_a()

        BKTStrategy().update(plain, g, "LAT-G-B", ResponseType.CORRECT)
        GraphAwareBKTStrategy(graph_influence=0.3).update(
            aware, g, "LAT-G-B", ResponseType.CORRECT
        )

        # De prior van B is opgetrokken richting A's mastery → hogere posterior.
        assert (
            aware.node_states["LAT-G-B"].posterior_mastery
            > plain.node_states["LAT-G-B"].posterior_mastery
        )

    def test_no_neighbours_is_identical_to_bkt(self):
        g = nx.DiGraph()
        g.add_node("LAT-G-ROOT")  # geen prerequisites
        plain = LearnerModel(user_id=uuid4())
        aware = LearnerModel(user_id=uuid4())

        BKTStrategy().update(plain, g, "LAT-G-ROOT", ResponseType.CORRECT)
        GraphAwareBKTStrategy().update(aware, g, "LAT-G-ROOT", ResponseType.CORRECT)

        assert (
            aware.node_states["LAT-G-ROOT"].posterior_mastery
            == plain.node_states["LAT-G-ROOT"].posterior_mastery
        )

    def test_invalid_graph_influence_rejected(self):
        with pytest.raises(ValueError, match="graph_influence"):
            GraphAwareBKTStrategy(graph_influence=1.5)
