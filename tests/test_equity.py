"""Tests voor de equity-waarborgen (L3-03)."""

from uuid import uuid4

import networkx as nx

from gymnasium_classica.models.graph import (
    BloomLevel,
    EdgeType,
    Language,
    Node,
    NodeType,
    Phase,
    PrerequisiteEdge,
)
from gymnasium_classica.models.learner import LearnerModel, NodeState
from gymnasium_classica.scheduling.equity import (
    EQUITY_MAX_BOOST,
    equity_prereq_threshold,
    is_low_mastery_trajectory,
)
from gymnasium_classica.scheduling.priority import PREREQ_READY_THRESHOLD
from gymnasium_classica.scheduling.session import _candidates_for_new_material


def _node(node_id: str) -> Node:
    return Node(
        id=node_id,
        type=NodeType.G,
        language=Language.LAT,
        title_nl="t",
        description="d",
        bloom_level=BloomLevel.KNOWLEDGE,
        phase=Phase.ONDERBOUW_1,
    )


def _graph() -> nx.DiGraph:
    """A (prereq) → B; plus losse root C. Allen type G."""
    g = nx.DiGraph()
    for nid in ("LAT-G-MORF-AAA", "LAT-G-MORF-BBB", "LAT-G-MORF-CCC"):
        g.add_node(nid, node=_node(nid))
    g.add_edge(
        "LAT-G-MORF-AAA",
        "LAT-G-MORF-BBB",
        edge=PrerequisiteEdge(
            source_id="LAT-G-MORF-AAA",
            target_id="LAT-G-MORF-BBB",
            type=EdgeType.PREREQUISITE,
            encompassing_weight=1.0,
        ),
    )
    return g


def _learner(rate: float) -> LearnerModel:
    # Prerequisite A op 0.80: boven de base-drempel (0.75), onder de
    # equity-drempel voor een zwakke leerling.
    learner = LearnerModel(user_id=uuid4(), learning_rate=rate)
    learner.node_states["LAT-G-MORF-AAA"] = NodeState(
        node_id="LAT-G-MORF-AAA", posterior_mastery=0.80
    )
    return learner


class TestEquityThreshold:
    def test_on_track_uses_base(self):
        assert equity_prereq_threshold(_learner(1.0)) == PREREQ_READY_THRESHOLD
        assert equity_prereq_threshold(_learner(1.5)) == PREREQ_READY_THRESHOLD

    def test_weak_learner_raises_threshold_capped(self):
        threshold = equity_prereq_threshold(_learner(0.5))
        assert threshold == PREREQ_READY_THRESHOLD + EQUITY_MAX_BOOST

    def test_gradual_between(self):
        mid = equity_prereq_threshold(_learner(0.8))
        assert PREREQ_READY_THRESHOLD < mid < PREREQ_READY_THRESHOLD + EQUITY_MAX_BOOST

    def test_self_recovering(self):
        # Naarmate de rate richting 1.0 kruipt, daalt de drempel naar base.
        assert equity_prereq_threshold(_learner(0.6)) > equity_prereq_threshold(_learner(0.9))

    def test_is_low_mastery_trajectory(self):
        assert is_low_mastery_trajectory(_learner(0.7)) is True
        assert is_low_mastery_trajectory(_learner(1.0)) is False


class TestNewMaterialShareDrops:
    def test_weak_learner_gets_fewer_new_nodes(self):
        graph = _graph()
        on_track = _candidates_for_new_material(_learner(1.0), graph)
        weak = _candidates_for_new_material(_learner(0.5), graph)

        on_track_ids = {n.id for _, n in on_track}
        weak_ids = {n.id for _, n in weak}

        # B (prereq A=0.80) is wél nieuw materiaal voor de leerling op koers,
        # maar valt voor de zwakke leerling buiten de hogere drempel.
        assert "LAT-G-MORF-BBB" in on_track_ids
        assert "LAT-G-MORF-BBB" not in weak_ids
        # De root C blijft beschikbaar voor beiden — geen harde "stempel".
        assert "LAT-G-MORF-CCC" in on_track_ids and "LAT-G-MORF-CCC" in weak_ids
        assert len(weak) < len(on_track)
