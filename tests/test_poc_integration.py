"""Integration test: load and validate the PoC graph file."""

import pytest

from gymnasium_classica.graph.loader import load_graph
from gymnasium_classica.graph.validation import validate_graph


class TestPoCIntegration:
    """End-to-end test against data/graph/lat_grammatica_poc.json."""

    def test_load_poc_graph(self, poc_graph_path):
        if not poc_graph_path.exists():
            pytest.skip("PoC graph file not found")
        g = load_graph(poc_graph_path)
        assert g.number_of_nodes() == 50

    def test_validate_poc_graph(self, poc_graph_path):
        if not poc_graph_path.exists():
            pytest.skip("PoC graph file not found")
        g = load_graph(poc_graph_path)
        report = validate_graph(g)

        assert report.is_valid is True
        assert report.node_count == 50
        assert report.cycles == []
        assert report.orphan_nodes == []
        assert report.weakly_connected_components == 1
        assert report.topological_order is not None
        assert len(report.topological_order) == 50

    def test_poc_root_nodes(self, poc_graph_path):
        if not poc_graph_path.exists():
            pytest.skip("PoC graph file not found")
        g = load_graph(poc_graph_path)
        report = validate_graph(g)

        expected_roots = {
            "LAT-G-MORF-NAAMVAL-INTRO",
            "LAT-G-MORF-GENUS-INTRO",
            "LAT-G-MORF-NUMERUS-INTRO",
            "LAT-G-MORF-TEMPUS-INTRO",
            "LAT-G-SYNT-ZINSDEEL-INTRO",
        }
        assert set(report.root_nodes) == expected_roots

    def test_poc_topological_order_correctness(self, poc_graph_path):
        if not poc_graph_path.exists():
            pytest.skip("PoC graph file not found")
        g = load_graph(poc_graph_path)
        report = validate_graph(g)

        index = {node: i for i, node in enumerate(report.topological_order)}
        for u, v in g.edges:
            assert index[u] < index[v], (
                f"Topological violation: {u} (index {index[u]}) "
                f"should come before {v} (index {index[v]})"
            )
