"""Tests for misconception-aware scheduler boosting (M1-02)."""

from uuid import uuid4

import networkx as nx

from gymnasium_classica.models.graph import (
    BloomLevel,
    Direction,
    Item,
    ItemType,
    Language,
    Misconception,
    Node,
    NodeType,
    Phase,
    Source,
)
from gymnasium_classica.models.learner import LearnerModel, NodeState
from gymnasium_classica.scheduling.misconceptie_detectie import (
    apply_lego_boost,
    evaluate_lego_translator,
    lego_session_message,
)

POLMO_ID = "SHA-P-VERTAAL-POLMO-PV"
MORPH_ID = "LAT-G-MORF-NAAMVAL-INTRO"
VERT_ID = "LAT-I-VERT-NAAMVAL"
DIAG_ITEM_ID = "ITEM-LAT-I-VERT-NAAMVAL-001"


def _node(node_id: str, node_type: NodeType, items=None, misconceptions=None) -> Node:
    return Node(
        id=node_id,
        type=node_type,
        language=Language.SHARED if node_id.startswith("SHA") else Language.LAT,
        title_nl="t",
        description="d",
        bloom_level=BloomLevel.COMPREHENSION,
        phase=Phase.ONDERBOUW_1,
        items=items or [],
        known_misconceptions=misconceptions or [],
    )


def _diag_item() -> Item:
    return Item(
        id=DIAG_ITEM_ID,
        node_ids=[VERT_ID],
        type=ItemType.ANALYSIS,
        direction=Direction.RECEPTIVE,
        difficulty_initial=0.0,
        discrimination_initial=1.0,
        expected_time_sec=30,
        stimulus={"instruction": "?", "options": ["a", "b"]},
        answer="a",
        feedback="f",
        source=Source.MANUAL,
    )


def _graph() -> nx.DiGraph:
    lego = Misconception(
        code="LEGO_VERTALEN",
        name="Lego-vertalen",
        description="d",
        diagnostic_items=[DIAG_ITEM_ID],
        remediation_nodes=[POLMO_ID, MORPH_ID],
    )
    nodes = [
        _node(POLMO_ID, NodeType.P),
        _node(MORPH_ID, NodeType.G),
        _node(VERT_ID, NodeType.I, items=[_diag_item()], misconceptions=[lego]),
        _node("LAT-V-F01-AAA", NodeType.V),
        _node("LAT-V-F01-BBB", NodeType.V),
        _node("LAT-V-F01-CCC", NodeType.V),
    ]
    g = nx.DiGraph()
    for n in nodes:
        g.add_node(n.id, node=n)
    return g


def _profile_learner() -> LearnerModel:
    return LearnerModel(
        user_id=uuid4(),
        node_states={
            "LAT-V-F01-AAA": NodeState(node_id="LAT-V-F01-AAA", posterior_mastery=0.85),
            "LAT-V-F02-BBB": NodeState(node_id="LAT-V-F02-BBB", posterior_mastery=0.80),
            MORPH_ID: NodeState(node_id=MORPH_ID, posterior_mastery=0.35),
            VERT_ID: NodeState(node_id=VERT_ID, posterior_mastery=0.25),
        },
    )


def _scored(graph: nx.DiGraph) -> list[tuple[float, Node]]:
    # Distractors rank above the remediation nodes before any boost.
    urgencies = {
        "LAT-V-F01-AAA": 0.90,
        "LAT-V-F01-BBB": 0.85,
        "LAT-V-F01-CCC": 0.80,
        POLMO_ID: 0.50,
        MORPH_ID: 0.45,
        VERT_ID: 0.40,
    }
    scored = [(urgencies[nid], graph.nodes[nid]["node"]) for nid in urgencies]
    scored.sort(key=lambda p: p[0], reverse=True)
    return scored


class TestApplyLegoBoost:
    def test_boost_promotes_remediation_node_into_top3(self):
        graph = _graph()
        learner = _profile_learner()
        scored = _scored(graph)

        # Pre-boost: top 3 are all vocabulary distractors.
        top3_before = {node.id for _, node in scored[:3]}
        assert not ({POLMO_ID, MORPH_ID} & top3_before)

        boosted, flag = apply_lego_boost(scored, learner, graph)
        assert flag.active is True
        top3_after = {node.id for _, node in boosted[:3]}
        assert {POLMO_ID, MORPH_ID} & top3_after, "expected a POLMO/morphology node in top 3"

    def test_no_boost_when_profile_inactive(self):
        graph = _graph()
        # Strong learner everywhere -> profile inactive -> scores unchanged.
        learner = LearnerModel(
            user_id=uuid4(),
            node_states={
                "LAT-V-F01-AAA": NodeState(node_id="LAT-V-F01-AAA", posterior_mastery=0.90),
                MORPH_ID: NodeState(node_id=MORPH_ID, posterior_mastery=0.88),
                VERT_ID: NodeState(node_id=VERT_ID, posterior_mastery=0.85),
            },
        )
        scored = _scored(graph)
        boosted, flag = apply_lego_boost(scored, learner, graph)
        assert flag.active is False
        assert [n.id for _, n in boosted] == [n.id for _, n in scored]

    def test_boost_is_multiplicative_not_override(self):
        graph = _graph()
        learner = _profile_learner()
        scored = _scored(graph)
        boosted, _ = apply_lego_boost(scored, learner, graph)
        boosted_map = {node.id: u for u, node in boosted}
        # A non-target distractor keeps its original urgency.
        assert boosted_map["LAT-V-F01-AAA"] == 0.90
        # POLMO node is multiplied by the default 1.75 factor.
        assert abs(boosted_map[POLMO_ID] - 0.50 * 1.75) < 1e-9


class TestSessionMessage:
    def test_active_profile_yields_plain_language_message(self):
        flag = evaluate_lego_translator(_profile_learner())
        message = lego_session_message(flag)
        assert message is not None
        assert "ontleden" in message
        # No technical jargon leaks to the learner.
        assert "Lego" not in message

    def test_inactive_profile_yields_no_message(self):
        learner = LearnerModel(user_id=uuid4(), node_states={})
        flag = evaluate_lego_translator(learner)
        assert lego_session_message(flag) is None
