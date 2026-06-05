"""Tests for the translation-integration layer (M1-04): first I-VERT nodes."""

from pathlib import Path

from gymnasium_classica.graph.loader import load_graph
from gymnasium_classica.graph.validation import validate_graph

REPO_ROOT = Path(__file__).resolve().parent.parent
GRAPH_DIR = REPO_ROOT / "data" / "graph"

LAT_VERT = ["LAT-I-VERT-INTRO", "LAT-I-VERT-NAAMVAL", "LAT-I-VERT-POLMO"]
GRC_VERT = ["GRC-I-VERT-INTRO", "GRC-I-VERT-NAAMVAL", "GRC-I-VERT-POLMO"]


def _graph():
    return load_graph(GRAPH_DIR)


class TestIntegratielaagLoads:
    """The six I-VERT nodes load and the full graph stays valid."""

    def test_all_six_ivert_nodes_present(self):
        g = _graph()
        for node_id in [*LAT_VERT, *GRC_VERT]:
            assert node_id in g.nodes, f"{node_id} ontbreekt in de graph"

    def test_ivert_nodes_are_type_i(self):
        g = _graph()
        for node_id in [*LAT_VERT, *GRC_VERT]:
            node = g.nodes[node_id]["node"]
            assert node.type == "I", f"{node_id} heeft type {node.type}, verwacht I"

    def test_graph_still_valid(self):
        g = _graph()
        report = validate_graph(g, content_root=REPO_ROOT)
        assert report.is_valid, report.errors
        assert report.cycles == []


class TestPolmoCoupling:
    """M1-01 -> M1-04: the POLMO procedure feeds the I-VERT-POLMO node."""

    def test_polmo_end_is_prerequisite_of_ivert_polmo(self):
        g = _graph()
        for target in ["LAT-I-VERT-POLMO", "GRC-I-VERT-POLMO"]:
            assert g.has_edge("SHA-P-VERTAAL-POLMO-OV", target), (
                f"prerequisite-edge POLMO-OV -> {target} ontbreekt"
            )

    def test_naamval_nodes_have_diagnostic_items(self):
        """The NAAMVAL nodes host >=3 items each (future M1-02 diagnose_items)."""
        g = _graph()
        for node_id in ["LAT-I-VERT-NAAMVAL", "GRC-I-VERT-NAAMVAL"]:
            node = g.nodes[node_id]["node"]
            assert len(node.items) >= 3, f"{node_id} heeft {len(node.items)} items, verwacht >=3"
