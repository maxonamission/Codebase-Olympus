"""Tests for the graph loader: JSON → NetworkX DiGraph."""

import json

import pytest
from pydantic import ValidationError

from gymnasium_classica.graph.loader import (
    graph_to_dict,
    load_graph,
    load_graph_from_dict,
)
from gymnasium_classica.models.graph import Node, PrerequisiteEdge


class TestLoadGraphFromDict:
    """Tests for load_graph_from_dict()."""

    def test_load_valid_graph(self, sample_graph_data):
        g = load_graph_from_dict(sample_graph_data)
        assert g.number_of_nodes() == 5
        assert g.number_of_edges() == 4

    def test_node_attributes(self, sample_graph_data):
        g = load_graph_from_dict(sample_graph_data)
        node = g.nodes["LAT-G-MORF-NOM-D1"]["node"]
        assert isinstance(node, Node)
        assert node.title_nl == "Nominativus 1e declinatie"

    def test_edge_attributes(self, sample_graph_data):
        g = load_graph_from_dict(sample_graph_data)
        edge = g.edges["LAT-G-MORF-DECL1-INTRO", "LAT-G-MORF-NOM-D1"]["edge"]
        assert isinstance(edge, PrerequisiteEdge)
        assert edge.encompassing_weight == 0.3

    def test_empty_graph(self):
        g = load_graph_from_dict({"nodes": [], "edges": []})
        assert g.number_of_nodes() == 0
        assert g.number_of_edges() == 0

    def test_duplicate_node_ids_rejected(self, sample_graph_data):
        # Add a duplicate node
        sample_graph_data["nodes"].append(sample_graph_data["nodes"][0])
        with pytest.raises(ValueError, match="Duplicate node ID"):
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
        del sample_graph_data["nodes"][0]["title_nl"]
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


class TestLoadGraphFromDirectory:
    """Tests for load_graph() from a directory of JSON files."""

    def test_load_single_file_in_directory(self, tmp_path, sample_graph_data):
        graph_dir = tmp_path / "graph"
        graph_dir.mkdir()
        (graph_dir / "base.json").write_text(json.dumps(sample_graph_data), encoding="utf-8")
        g = load_graph(graph_dir)
        assert g.number_of_nodes() == 5
        assert g.number_of_edges() == 4

    def test_load_multiple_files_merged(self, tmp_path):
        """Two files with separate nodes + cross-file edge."""
        graph_dir = tmp_path / "graph"
        graph_dir.mkdir()

        file_a = {
            "nodes": [
                {
                    "id": "LAT-G-MORF-NOM-D1",
                    "type": "G",
                    "language": "lat",
                    "title_nl": "Knoop A",
                    "description": "Test A.",
                    "bloom_level": "knowledge",
                    "phase": "onderbouw_1",
                    "testable": True,
                    "items": [],
                },
            ],
            "edges": [],
        }
        file_b = {
            "nodes": [
                {
                    "id": "GRC-G-MORF-NOM-D1",
                    "type": "G",
                    "language": "grc",
                    "title_nl": "Knoop B",
                    "description": "Test B.",
                    "bloom_level": "knowledge",
                    "phase": "onderbouw_1",
                    "testable": True,
                    "items": [],
                },
            ],
            "edges": [
                {
                    "source_id": "LAT-G-MORF-NOM-D1",
                    "target_id": "GRC-G-MORF-NOM-D1",
                    "type": "transfer",
                    "encompassing_weight": 0.3,
                },
            ],
        }

        (graph_dir / "a_latin.json").write_text(json.dumps(file_a), encoding="utf-8")
        (graph_dir / "b_greek.json").write_text(json.dumps(file_b), encoding="utf-8")

        g = load_graph(graph_dir)
        assert g.number_of_nodes() == 2
        assert g.number_of_edges() == 1
        # Cross-file edge resolved correctly
        assert g.has_edge("LAT-G-MORF-NOM-D1", "GRC-G-MORF-NOM-D1")

    def test_empty_directory_raises(self, tmp_path):
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()
        with pytest.raises(FileNotFoundError, match=r"No \.json files"):
            load_graph(empty_dir)

    def test_duplicate_ids_across_files_rejected(self, tmp_path):
        graph_dir = tmp_path / "graph"
        graph_dir.mkdir()

        node = {
            "nodes": [
                {
                    "id": "LAT-G-MORF-NOM-D1",
                    "type": "G",
                    "language": "lat",
                    "title_nl": "Same ID",
                    "description": "Test.",
                    "bloom_level": "knowledge",
                    "phase": "onderbouw_1",
                    "testable": True,
                    "items": [],
                }
            ],
            "edges": [],
        }

        (graph_dir / "a.json").write_text(json.dumps(node), encoding="utf-8")
        (graph_dir / "b.json").write_text(json.dumps(node), encoding="utf-8")

        with pytest.raises(ValueError, match="Duplicate node ID"):
            load_graph(graph_dir)


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
            assert g.nodes[node_id]["node"] == g2.nodes[node_id]["node"]
