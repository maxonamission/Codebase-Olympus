"""Tests for the Misconception model and its cross-reference validation (M1-02)."""

import networkx as nx
import pytest
from pydantic import ValidationError

from gymnasium_classica.graph.validation import validate_misconceptions
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

LEGO = Misconception(
    code="LEGO_VERTALEN",
    name="Lego-vertalen",
    description="Woorden op elkaar stapelen zonder de zinsbouw te ontleden.",
    diagnostic_items=["ITEM-LAT-I-VERT-NAAMVAL-001"],
    remediation_nodes=["SHA-P-VERTAAL-POLMO-PV"],
)


class TestMisconceptionModel:
    def test_roundtrip(self):
        dumped = LEGO.model_dump()
        assert Misconception.model_validate(dumped) == LEGO

    @pytest.mark.parametrize(
        "code", ["lego_vertalen", "LEGO-VERTALEN", "1LEGO", "LEGO VERTALEN", ""]
    )
    def test_invalid_code_rejected(self, code):
        with pytest.raises(ValidationError):
            Misconception(code=code, name="x", description="y")

    @pytest.mark.parametrize("code", ["LEGO_VERTALEN", "A", "WW_UIT_ZIN_PIKKEN", "TIJD2"])
    def test_valid_code_accepted(self, code):
        assert Misconception(code=code, name="x", description="y").code == code

    def test_node_accepts_known_misconceptions(self):
        node = Node(
            id="LAT-I-VERT-NAAMVAL",
            type=NodeType.I,
            language=Language.LAT,
            title_nl="Naamval bepaalt de functie",
            description="x",
            bloom_level=BloomLevel.ANALYSIS,
            phase=Phase.ONDERBOUW_1,
            known_misconceptions=[LEGO],
        )
        assert node.known_misconceptions[0].code == "LEGO_VERTALEN"

    def test_node_defaults_to_no_misconceptions(self):
        node = Node(
            id="LAT-G-MORF-NAAMVAL-INTRO",
            type=NodeType.G,
            language=Language.LAT,
            title_nl="Naamvalsysteem",
            description="x",
            bloom_level=BloomLevel.COMPREHENSION,
            phase=Phase.ONDERBOUW_1,
        )
        assert node.known_misconceptions == []


def _node_with(node_id, items, misconceptions):
    return Node(
        id=node_id,
        type=NodeType.I,
        language=Language.LAT,
        title_nl="t",
        description="d",
        bloom_level=BloomLevel.ANALYSIS,
        phase=Phase.ONDERBOUW_1,
        items=items,
        known_misconceptions=misconceptions,
    )


def _item(item_id, node_id):
    return Item(
        id=item_id,
        node_ids=[node_id],
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


class TestMisconceptionCrossRefValidation:
    def test_resolving_refs_pass(self):
        g = nx.DiGraph()
        item = _item("ITEM-X-001", "LAT-I-VERT-NAAMVAL")
        misc = Misconception(
            code="LEGO_VERTALEN",
            name="n",
            description="d",
            diagnostic_items=["ITEM-X-001"],
            remediation_nodes=["LAT-I-VERT-NAAMVAL"],
        )
        node = _node_with("LAT-I-VERT-NAAMVAL", [item], [misc])
        g.add_node(node.id, node=node)
        assert validate_misconceptions(g) == []

    def test_missing_diagnostic_item_flagged(self):
        g = nx.DiGraph()
        misc = Misconception(
            code="LEGO_VERTALEN",
            name="n",
            description="d",
            diagnostic_items=["ITEM-GHOST-999"],
            remediation_nodes=[],
        )
        node = _node_with("LAT-I-VERT-NAAMVAL", [], [misc])
        g.add_node(node.id, node=node)
        errors = validate_misconceptions(g)
        assert len(errors) == 1
        assert "ITEM-GHOST-999" in errors[0]

    def test_missing_remediation_node_flagged(self):
        g = nx.DiGraph()
        misc = Misconception(
            code="LEGO_VERTALEN",
            name="n",
            description="d",
            diagnostic_items=[],
            remediation_nodes=["LAT-G-GHOST-INTRO"],
        )
        node = _node_with("LAT-I-VERT-NAAMVAL", [], [misc])
        g.add_node(node.id, node=node)
        errors = validate_misconceptions(g)
        assert len(errors) == 1
        assert "LAT-G-GHOST-INTRO" in errors[0]
