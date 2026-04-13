"""Tests for Pydantic models: KennisKnoop, PrerequisiteEdge, Item."""

import pytest
from pydantic import ValidationError

from gymnasium_classica.models.graph import (
    Bron,
    EdgeType,
    GraphData,
    Item,
    ItemType,
    KennisKnoop,
    PrerequisiteEdge,
)


class TestKennisKnoop:
    """Tests for the KennisKnoop model."""

    def test_valid_construction(self, sample_knoop_data):
        knoop = KennisKnoop(**sample_knoop_data)
        assert knoop.id == "LAT-G-MORF-NOM-D1"
        assert knoop.titel_nl == "Nominativus 1e declinatie"
        assert knoop.toetsbaar is True
        assert knoop.items == []

    def test_invalid_id_rejected(self, sample_knoop_data):
        sample_knoop_data["id"] = "invalid-id"
        with pytest.raises(ValidationError, match="Invalid knoop ID"):
            KennisKnoop(**sample_knoop_data)

    def test_invalid_type_rejected(self, sample_knoop_data):
        sample_knoop_data["type"] = "X"
        with pytest.raises(ValidationError):
            KennisKnoop(**sample_knoop_data)

    def test_invalid_taal_rejected(self, sample_knoop_data):
        sample_knoop_data["taal"] = "english"
        with pytest.raises(ValidationError):
            KennisKnoop(**sample_knoop_data)

    def test_invalid_bloom_rejected(self, sample_knoop_data):
        sample_knoop_data["bloom_niveau"] = "mastery"
        with pytest.raises(ValidationError):
            KennisKnoop(**sample_knoop_data)

    def test_invalid_fase_rejected(self, sample_knoop_data):
        sample_knoop_data["fase"] = "fase_99"
        with pytest.raises(ValidationError):
            KennisKnoop(**sample_knoop_data)

    def test_optional_fields_default_none(self, sample_knoop_data):
        knoop = KennisKnoop(**sample_knoop_data)
        assert knoop.titel_terminologie is None
        assert knoop.cevte_referentie is None
        assert knoop.content_ref is None
        assert knoop.semantisch_cluster is None

    def test_semantisch_cluster_valid(self, sample_knoop_data):
        sample_knoop_data["semantisch_cluster"] = "familie"
        knoop = KennisKnoop(**sample_knoop_data)
        assert knoop.semantisch_cluster == "familie"

    def test_semantisch_cluster_with_underscore(self, sample_knoop_data):
        sample_knoop_data["semantisch_cluster"] = "dagelijks_leven"
        knoop = KennisKnoop(**sample_knoop_data)
        assert knoop.semantisch_cluster == "dagelijks_leven"

    def test_semantisch_cluster_uppercase_rejected(self, sample_knoop_data):
        sample_knoop_data["semantisch_cluster"] = "Familie"
        with pytest.raises(ValidationError, match="semantisch_cluster"):
            KennisKnoop(**sample_knoop_data)

    def test_semantisch_cluster_too_long_rejected(self, sample_knoop_data):
        sample_knoop_data["semantisch_cluster"] = "a" * 21
        with pytest.raises(ValidationError, match="semantisch_cluster"):
            KennisKnoop(**sample_knoop_data)

    def test_semantisch_cluster_spaces_rejected(self, sample_knoop_data):
        sample_knoop_data["semantisch_cluster"] = "daily life"
        with pytest.raises(ValidationError, match="semantisch_cluster"):
            KennisKnoop(**sample_knoop_data)

    def test_optional_fields_can_be_set(self, sample_knoop_data):
        sample_knoop_data["titel_terminologie"] = "nominativus"
        sample_knoop_data["cevte_referentie"] = "A1.1"
        sample_knoop_data["content_ref"] = "LAT-G-MORF-NOM-D1.md"
        knoop = KennisKnoop(**sample_knoop_data)
        assert knoop.titel_terminologie == "nominativus"
        assert knoop.content_ref == "LAT-G-MORF-NOM-D1.md"

    def test_empty_items_list_valid(self, sample_knoop_data):
        knoop = KennisKnoop(**sample_knoop_data)
        assert knoop.items == []

    def test_serialization_roundtrip(self, sample_knoop_data):
        knoop = KennisKnoop(**sample_knoop_data)
        dumped = knoop.model_dump()
        knoop2 = KennisKnoop(**dumped)
        assert knoop == knoop2


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
            "knoop_ids": ["LAT-G-MORF-NOM-D1"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.5,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 30,
            "stimulus": "Welke naamval is 'puella'?",
            "antwoord": "nominativus",
            "feedback": "Puella eindigt op -a, de uitgang van de nominativus sg. 1e declinatie.",
            "bron": "handmatig",
        }

    def test_valid_construction(self, sample_item_data):
        item = Item(**sample_item_data)
        assert item.id == "ITEM-001"
        assert item.richting == "receptief"

    def test_discriminatie_must_be_positive(self, sample_item_data):
        sample_item_data["discriminatie_initieel"] = 0
        with pytest.raises(ValidationError):
            Item(**sample_item_data)

    def test_negative_discriminatie_rejected(self, sample_item_data):
        sample_item_data["discriminatie_initieel"] = -1.0
        with pytest.raises(ValidationError):
            Item(**sample_item_data)

    def test_verwachte_tijd_must_be_positive(self, sample_item_data):
        sample_item_data["verwachte_tijd_sec"] = 0
        with pytest.raises(ValidationError):
            Item(**sample_item_data)

    def test_stimulus_can_be_dict(self, sample_item_data):
        sample_item_data["stimulus"] = {"text": "Welke naamval?", "image": "nom.png"}
        item = Item(**sample_item_data)
        assert isinstance(item.stimulus, dict)

    def test_antwoord_can_be_list(self, sample_item_data):
        sample_item_data["antwoord"] = ["nominativus", "nom."]
        item = Item(**sample_item_data)
        assert isinstance(item.antwoord, list)

    def test_all_bron_values(self, sample_item_data):
        for bron in ["handmatig", "llm_gegenereerd", "authentiek"]:
            sample_item_data["bron"] = bron
            item = Item(**sample_item_data)
            assert item.bron == bron


class TestLuisterItemTypes:
    """Tests for the luister_herkenning and luister_productie ItemType values."""

    @pytest.fixture
    def base_item_data(self) -> dict:
        return {
            "id": "ITEM-LUISTER-001",
            "knoop_ids": ["LAT-V-F01-SUM"],
            "richting": "receptief",
            "moeilijkheid_initieel": -0.3,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 20,
            "stimulus": "Luister en kies de juiste vertaling.",
            "antwoord": "zijn",
            "feedback": "sum = zijn",
            "bron": "handmatig",
            "audio_ref": "LAT-V-F01-SUM.wav",
        }

    def test_luister_herkenning_valid(self, base_item_data):
        base_item_data["type"] = "luister_herkenning"
        item = Item(**base_item_data)
        assert item.type == ItemType.LUISTER_HERKENNING

    def test_luister_productie_valid(self, base_item_data):
        base_item_data["type"] = "luister_productie"
        base_item_data["richting"] = "productief"
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
            "herkenning", "productie", "analyse", "synthese",
            "contextueel", "offline_schrijven",
            "luister_herkenning", "luister_productie",
        }
        actual = {t.value for t in ItemType}
        assert actual == expected

    def test_luister_item_with_audio_ref(self, base_item_data):
        base_item_data["type"] = "luister_herkenning"
        item = Item(**base_item_data)
        assert item.audio_ref == "LAT-V-F01-SUM.wav"

    def test_existing_item_types_unchanged(self, base_item_data):
        """Ensure existing item types still work — no breaking change."""
        for existing_type in ["herkenning", "productie", "analyse",
                              "synthese", "contextueel", "offline_schrijven"]:
            base_item_data["type"] = existing_type
            item = Item(**base_item_data)
            assert item.type == existing_type


class TestGraphData:
    """Tests for the GraphData wrapper model."""

    def test_valid_construction(self, sample_graph_data):
        gd = GraphData(**sample_graph_data)
        assert len(gd.knopen) == 5
        assert len(gd.edges) == 4

    def test_empty_graph(self):
        gd = GraphData(knopen=[], edges=[])
        assert len(gd.knopen) == 0
        assert len(gd.edges) == 0
