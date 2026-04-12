"""Tests for the graph loader: JSON → NetworkX DiGraph."""

import json
import pytest
from pydantic import ValidationError

from gymnasium_classica.graph.loader import (
    graph_to_dict,
    load_graph,
    load_graph_from_dict,
)
from gymnasium_classica.models.graph import KennisKnoop, PrerequisiteEdge


class TestLoadGraphFromDict:
    """Tests for load_graph_from_dict()."""

    def test_load_valid_graph(self, sample_graph_data):
        g = load_graph_from_dict(sample_graph_data)
        assert g.number_of_nodes() == 5
        assert g.number_of_edges() == 4

    def test_node_attributes(self, sample_graph_data):
        g = load_graph_from_dict(sample_graph_data)
        knoop = g.nodes["LAT-G-MORF-NOM-D1"]["knoop"]
        assert isinstance(knoop, KennisKnoop)
        assert knoop.titel_nl == "Nominativus 1e declinatie"

    def test_edge_attributes(self, sample_graph_data):
        g = load_graph_from_dict(sample_graph_data)
        edge = g.edges["LAT-G-MORF-DECL1-INTRO", "LAT-G-MORF-NOM-D1"]["edge"]
        assert isinstance(edge, PrerequisiteEdge)
        assert edge.encompassing_weight == 0.3

    def test_empty_graph(self):
        g = load_graph_from_dict({"knopen": [], "edges": []})
        assert g.number_of_nodes() == 0
        assert g.number_of_edges() == 0

    def test_duplicate_node_ids_rejected(self, sample_graph_data):
        # Add a duplicate node
        sample_graph_data["knopen"].append(sample_graph_data["knopen"][0])
        with pytest.raises(ValueError, match="Duplicate knoop ID"):
            load_graph_from_dict(sample_graph_data)

    def test_dangling_edge_source_rejected(self, sample_graph_data):
        sample_graph_data["edges"].append(
            {
                "source_id": "LAT-G-MORF-NONEXIST",
                "target_id": "LAT-G-MORF-NOM-D1",
                "type": "prerequisite",
                "encompassing_weight": 0.5,
            }
        )
        with pytest.raises(ValueError, match="Dangling edge references"):
            load_graph_from_dict(sample_graph_data)

    def test_dangling_edge_target_rejected(self, sample_graph_data):
        sample_graph_data["edges"].append(
            {
                "source_id": "LAT-G-MORF-NOM-D1",
                "target_id": "LAT-G-MORF-NONEXIST",
                "type": "prerequisite",
                "encompassing_weight": 0.5,
            }
        )
        with pytest.raises(ValueError, match="Dangling edge references"):
            load_graph_from_dict(sample_graph_data)

    def test_schema_violation_rejected(self, sample_graph_data):
        # Remove required field
        del sample_graph_data["knopen"][0]["titel_nl"]
        with pytest.raises(ValidationError):
            load_graph_from_dict(sample_graph_data)


class TestLoadGraphFromFile:
    """Tests for load_graph() from a JSON file."""

    def test_file_not_found(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            load_graph(tmp_path / "nonexistent.json")

    def test_invalid_json(self, tmp_path):
        bad_file = tmp_path / "bad.json"
        bad_file.write_text("not valid json {{{", encoding="utf-8")
        with pytest.raises(json.JSONDecodeError):
            load_graph(bad_file)

    def test_load_from_file(self, tmp_path, sample_graph_data):
        file_path = tmp_path / "test_graph.json"
        file_path.write_text(json.dumps(sample_graph_data), encoding="utf-8")
        g = load_graph(file_path)
        assert g.number_of_nodes() == 5


class TestRoundTrip:
    """Tests for graph_to_dict() round-trip serialization."""

    def test_roundtrip(self, sample_graph_data):
        g = load_graph_from_dict(sample_graph_data)
        exported = graph_to_dict(g)
        g2 = load_graph_from_dict(exported)
        assert g2.number_of_nodes() == g.number_of_nodes()
        assert g2.number_of_edges() == g.number_of_edges()
        # Verify node data survives round-trip
        for node_id in g.nodes:
            assert g.nodes[node_id]["knoop"] == g2.nodes[node_id]["knoop"]
