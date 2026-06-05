"""Tests for the BijspijkerPlanner catch-up algorithm (M1-03)."""

from datetime import datetime
from pathlib import Path
from uuid import uuid4

import networkx as nx
import pytest

from gymnasium_classica.diagnostic.methode_profile import load_methode_mapping
from gymnasium_classica.graph.loader import load_graph
from gymnasium_classica.models.learner import ItemResponse, LearnerModel, NodeState
from gymnasium_classica.scheduling.bijspijker import (
    BijspijkerPlanner,
    BijspijkerTarget,
)

REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="module")
def graph() -> nx.DiGraph:
    return load_graph(REPO_ROOT / "data" / "graph")


@pytest.fixture(scope="module")
def mapping():
    return load_methode_mapping()


def _mastered_state(node_id: str) -> NodeState:
    return NodeState(
        node_id=node_id,
        posterior_mastery=0.90,
        item_history=[
            ItemResponse(
                timestamp=datetime(2026, 1, 1),
                item_id=f"ITEM-{node_id}",
                correct=True,
                response_time_ms=1000,
                node_id=node_id,
                direction="receptive",
                mastery_before=0.85,
            )
        ],
    )


def _empty_learner() -> LearnerModel:
    return LearnerModel(user_id=uuid4())


class TestDoelsetBoundary:
    def test_target_includes_chapters_up_to_h_and_excludes_later(self, graph, mapping):
        planner = BijspijkerPlanner(graph, mapping)
        plan = planner.plan(_empty_learner(), [BijspijkerTarget("fortuna", 3)])

        chapters = mapping["methoden"]["fortuna"]["hoofdstukken"]
        for h in ("1", "2", "3"):
            for node_id in chapters[h]["node_ids"]:
                assert node_id in plan.doelset, f"{node_id} (h{h}) hoort in doelset"

        # There exist later-chapter nodes that are NOT prerequisites and are excluded.
        later_nodes = set(chapters["5"]["node_ids"])
        excluded = later_nodes - set(plan.doelset)
        assert excluded, "verwacht knopen uit latere hoofdstukken buiten de doelset"

    def test_empty_learner_diagnoses_whole_doelset(self, graph, mapping):
        planner = BijspijkerPlanner(graph, mapping)
        plan = planner.plan(_empty_learner(), [BijspijkerTarget("fortuna", 3)])
        assert set(plan.diagnose) == set(plan.doelset)
        assert plan.is_bij is False

    def test_diagnose_is_topologically_ordered(self, graph, mapping):
        planner = BijspijkerPlanner(graph, mapping)
        plan = planner.plan(_empty_learner(), [BijspijkerTarget("fortuna", 3)])
        prereq_sub = nx.DiGraph()
        # Build prerequisite edges restricted to the diagnose set.
        diag = set(plan.diagnose)
        position = {nid: i for i, nid in enumerate(plan.diagnose)}
        for u, v in graph.edges:
            edge = graph.edges[u, v].get("edge")
            if edge and edge.type == "prerequisite" and u in diag and v in diag:
                prereq_sub.add_edge(u, v)
        for u, v in prereq_sub.edges:
            assert position[u] < position[v], f"prereq {u} moet vóór {v} komen"


class TestPartialKnowledge:
    def test_mastered_nodes_excluded_from_diagnose(self, graph, mapping):
        planner = BijspijkerPlanner(graph, mapping)
        learner = _empty_learner()
        target = BijspijkerTarget("pallas", 4)
        full = planner.plan(learner, [target])

        # Master the first three diagnose nodes.
        already = full.diagnose[:3]
        for node_id in already:
            learner.node_states[node_id] = _mastered_state(node_id)

        plan = planner.plan(learner, [target])
        for node_id in already:
            assert node_id not in plan.diagnose
        assert plan.fractie_bij > full.fractie_bij


class TestBijAndBump:
    def test_fully_mastered_learner_is_bij(self, graph, mapping):
        planner = BijspijkerPlanner(graph, mapping)
        learner = _empty_learner()
        target = BijspijkerTarget("pallas", 4)
        doelset = planner.plan(learner, [target]).doelset
        for node_id in doelset:
            learner.node_states[node_id] = _mastered_state(node_id)

        plan = planner.plan(learner, [target])
        assert plan.is_bij is True
        assert plan.suggest_chapter_bump is True
        assert plan.diagnose == []
        assert plan.eta_dagen == 0
        assert plan.fractie_bij == pytest.approx(1.0)


class TestCooldownAndTempo:
    def test_cooldown_nodes_are_chapter_h(self, graph, mapping):
        planner = BijspijkerPlanner(graph, mapping)
        plan = planner.plan(_empty_learner(), [BijspijkerTarget("pallas", 4)])
        expected = set(mapping["methoden"]["pallas"]["hoofdstukken"]["4"]["node_ids"])
        assert set(plan.cooldown_node_ids) == expected

    def test_intro_tempo_is_catch_up_rate(self, graph, mapping):
        planner = BijspijkerPlanner(graph, mapping)
        plan = planner.plan(_empty_learner(), [BijspijkerTarget("fortuna", 2)])
        assert 3 <= plan.intro_per_sessie <= 5
        # ETA reflects diagnose size / tempo.
        import math

        assert plan.eta_dagen == math.ceil(len(plan.diagnose) / plan.intro_per_sessie)
