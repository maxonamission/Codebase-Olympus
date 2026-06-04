"""Tests for Pydantic models: Node, PrerequisiteEdge, Item."""

import pytest
from pydantic import ValidationError

from gymnasium_classica.models.graph import (
    EdgeType,
    GraphData,
    Item,
    ItemType,
    Node,
    PrerequisiteEdge,
)


class TestNode:
    """Tests for the Node model."""

    def test_valid_construction(self, sample_node_data):
        node = Node(**sample_node_data)
        assert node.id == "LAT-G-MORF-NOM-D1"
        assert node.title_nl == "Nominativus 1e declinatie"
        assert node.testable is True
        assert node.items == []

    def test_invalid_id_rejected(self, sample_node_data):
        sample_node_data["id"] = "invalid-id"
        with pytest.raises(ValidationError, match="Invalid node ID"):
            Node(**sample_node_data)

    def test_invalid_type_rejected(self, sample_node_data):
        sample_node_data["type"] = "X"
        with pytest.raises(ValidationError):
            Node(**sample_node_data)

    def test_invalid_taal_rejected(self, sample_node_data):
        sample_node_data["language"] = "english"
        with pytest.raises(ValidationError):
            Node(**sample_node_data)

    def test_invalid_bloom_rejected(self, sample_node_data):
        sample_node_data["bloom_level"] = "mastery"
        with pytest.raises(ValidationError):
            Node(**sample_node_data)

    def test_invalid_fase_rejected(self, sample_node_data):
        sample_node_data["phase"] = "fase_99"
        with pytest.raises(ValidationError):
            Node(**sample_node_data)

    def test_optional_fields_default_none(self, sample_node_data):
        node = Node(**sample_node_data)
        assert node.title_terminology is None
        assert node.cevte_reference is None
        assert node.content_ref is None
        assert node.semantic_cluster is None

    def test_semantisch_cluster_valid(self, sample_node_data):
        sample_node_data["semantic_cluster"] = "familie"
        node = Node(**sample_node_data)
        assert node.semantic_cluster == "familie"

    def test_semantisch_cluster_with_underscore(self, sample_node_data):
        sample_node_data["semantic_cluster"] = "dagelijks_leven"
        node = Node(**sample_node_data)
        assert node.semantic_cluster == "dagelijks_leven"

    def test_semantisch_cluster_uppercase_rejected(self, sample_node_data):
        sample_node_data["semantic_cluster"] = "Familie"
        with pytest.raises(ValidationError, match="semantic_cluster"):
            Node(**sample_node_data)

    def test_semantisch_cluster_too_long_rejected(self, sample_node_data):
        sample_node_data["semantic_cluster"] = "a" * 21
        with pytest.raises(ValidationError, match="semantic_cluster"):
            Node(**sample_node_data)

    def test_semantisch_cluster_spaces_rejected(self, sample_node_data):
        sample_node_data["semantic_cluster"] = "daily life"
        with pytest.raises(ValidationError, match="semantic_cluster"):
            Node(**sample_node_data)

    def test_optional_fields_can_be_set(self, sample_node_data):
        sample_node_data["title_terminology"] = "nominativus"
        sample_node_data["cevte_reference"] = "A1.1"
        sample_node_data["content_ref"] = "LAT-G-MORF-NOM-D1.md"
        node = Node(**sample_node_data)
        assert node.title_terminology == "nominativus"
        assert node.content_ref == "LAT-G-MORF-NOM-D1.md"

    def test_empty_items_list_valid(self, sample_node_data):
        node = Node(**sample_node_data)
        assert node.items == []

    def test_serialization_roundtrip(self, sample_node_data):
        node = Node(**sample_node_data)
        dumped = node.model_dump()
        node2 = Node(**dumped)
        assert node == node2


class TestPrerequisiteEdge:
    """Tests for the PrerequisiteEdge model."""

    def test_valid_construction(self, sample_edge_data):
        edge = PrerequisiteEdge(**sample_edge_data)
        assert edge.source_id == "LAT-G-MORF-DECL1-INTRO"
        assert edge.type == EdgeType.PREREQUISITE

    def test_weight_boundary_zero(self, sample_edge_data):
        sample_edge_data["encompassing_weight"] = 0.0
        edge = PrerequisiteEdge(**sample_edge_data)
        assert edge.encompassing_weight == 0.0

    def test_weight_boundary_one(self, sample_edge_data):
        sample_edge_data["encompassing_weight"] = 1.0
        edge = PrerequisiteEdge(**sample_edge_data)
        assert edge.encompassing_weight == 1.0

    def test_weight_below_zero_rejected(self, sample_edge_data):
        sample_edge_data["encompassing_weight"] = -0.1
        with pytest.raises(ValidationError):
            PrerequisiteEdge(**sample_edge_data)

    def test_weight_above_one_rejected(self, sample_edge_data):
        sample_edge_data["encompassing_weight"] = 1.1
        with pytest.raises(ValidationError):
            PrerequisiteEdge(**sample_edge_data)

    def test_invalid_edge_type_rejected(self, sample_edge_data):
        sample_edge_data["type"] = "dependency"
        with pytest.raises(ValidationError):
            PrerequisiteEdge(**sample_edge_data)

    def test_all_edge_types(self, sample_edge_data):
        for etype in ["prerequisite", "enrichment", "transfer"]:
            sample_edge_data["type"] = etype
            edge = PrerequisiteEdge(**sample_edge_data)
            assert edge.type == etype


class TestItem:
    """Tests for the Item model."""

    @pytest.fixture
    def sample_item_data(self) -> dict:
        return {
            "id": "ITEM-001",
            "node_ids": ["LAT-G-MORF-NOM-D1"],
            "type": "herkenning",
            "direction": "receptief",
            "difficulty_initial": -0.5,
            "discrimination_initial": 1.2,
            "expected_time_sec": 30,
            "stimulus": "Welke naamval is 'puella'?",
            "answer": "nominativus",
            "feedback": "Puella eindigt op -a, de uitgang van de nominativus sg. 1e declinatie.",
            "source": "handmatig",
        }

    def test_valid_construction(self, sample_item_data):
        item = Item(**sample_item_data)
        assert item.id == "ITEM-001"
        assert item.direction == "receptief"

    def test_discriminatie_must_be_positive(self, sample_item_data):
        sample_item_data["discrimination_initial"] = 0
        with pytest.raises(ValidationError):
            Item(**sample_item_data)

    def test_negative_discriminatie_rejected(self, sample_item_data):
        sample_item_data["discrimination_initial"] = -1.0
        with pytest.raises(ValidationError):
            Item(**sample_item_data)

    def test_verwachte_tijd_must_be_positive(self, sample_item_data):
        sample_item_data["expected_time_sec"] = 0
        with pytest.raises(ValidationError):
            Item(**sample_item_data)

    def test_stimulus_can_be_dict(self, sample_item_data):
        sample_item_data["stimulus"] = {"text": "Welke naamval?", "image": "nom.png"}
        item = Item(**sample_item_data)
        assert isinstance(item.stimulus, dict)

    def test_antwoord_can_be_list(self, sample_item_data):
        sample_item_data["answer"] = ["nominativus", "nom."]
        item = Item(**sample_item_data)
        assert isinstance(item.answer, list)

    def test_all_bron_values(self, sample_item_data):
        for source in ["handmatig", "llm_gegenereerd", "authentiek"]:
            sample_item_data["source"] = source
            item = Item(**sample_item_data)
            assert item.source == source


class TestLuisterItemTypes:
    """Tests for the luister_herkenning and luister_productie ItemType values."""

    @pytest.fixture
    def base_item_data(self) -> dict:
        return {
            "id": "ITEM-LUISTER-001",
            "node_ids": ["LAT-V-F01-SUM"],
            "direction": "receptief",
            "difficulty_initial": -0.3,
            "discrimination_initial": 1.0,
            "expected_time_sec": 20,
            "stimulus": "Luister en kies de juiste vertaling.",
            "answer": "zijn",
            "feedback": "sum = zijn",
            "source": "handmatig",
            "audio_ref": "LAT-V-F01-SUM.wav",
        }

    def test_luister_herkenning_valid(self, base_item_data):
        base_item_data["type"] = "luister_herkenning"
        item = Item(**base_item_data)
        assert item.type == ItemType.LUISTER_HERKENNING

    def test_luister_productie_valid(self, base_item_data):
        base_item_data["type"] = "luister_productie"
        base_item_data["direction"] = "productief"
        item = Item(**base_item_data)
        assert item.type == ItemType.LUISTER_PRODUCTIE

    def test_luister_herkenning_enum_value(self):
        assert ItemType.LUISTER_HERKENNING == "luister_herkenning"
        assert ItemType.LUISTER_HERKENNING.value == "luister_herkenning"

    def test_luister_productie_enum_value(self):
        assert ItemType.LUISTER_PRODUCTIE == "luister_productie"
        assert ItemType.LUISTER_PRODUCTIE.value == "luister_productie"

    def test_all_item_types_present(self):
        expected = {
            "herkenning",
            "productie",
            "analyse",
            "synthese",
            "contextueel",
            "offline_schrijven",
            "luister_herkenning",
            "luister_productie",
        }
        actual = {t.value for t in ItemType}
        assert actual == expected

    def test_luister_item_with_audio_ref(self, base_item_data):
        base_item_data["type"] = "luister_herkenning"
        item = Item(**base_item_data)
        assert item.audio_ref == "LAT-V-F01-SUM.wav"

    def test_existing_item_types_unchanged(self, base_item_data):
        """Ensure existing item types still work — no breaking change."""
        for existing_type in [
            "herkenning",
            "productie",
            "analyse",
            "synthese",
            "contextueel",
            "offline_schrijven",
        ]:
            base_item_data["type"] = existing_type
            item = Item(**base_item_data)
            assert item.type == existing_type


class TestGraphData:
    """Tests for the GraphData wrapper model."""

    def test_valid_construction(self, sample_graph_data):
        gd = GraphData(**sample_graph_data)
        assert len(gd.nodes) == 5
        assert len(gd.edges) == 4

    def test_empty_graph(self):
        gd = GraphData(nodes=[], edges=[])
        assert len(gd.nodes) == 0
        assert len(gd.edges) == 0
