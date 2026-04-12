"""Tests for graph validation: cycles, orphans, connectivity, topological sort."""

import pytest

from gymnasium_classica.graph.loader import load_graph_from_dict
from gymnasium_classica.graph.validation import (
    check_connectivity,
    detect_cycles,
    find_leaf_nodes,
    find_orphan_nodes,
    find_root_nodes,
    topological_sort,
    validate_graph,
)


class TestDetectCycles:
    """Tests for cycle detection."""

    def test_acyclic_graph(self, sample_graph_data):
        g = load_graph_from_dict(sample_graph_data)
        cycles = detect_cycles(g)
        assert cycles == []

    def test_cyclic_graph(self, cyclic_graph_data):
        g = load_graph_from_dict(cyclic_graph_data)
        cycles = detect_cycles(g)
        assert len(cycles) > 0
        # All three nodes must appear in the cycle
        cycle_members = {node for cycle in cycles for node in cycle}
        assert "LAT-G-MORF-NOM-D1" in cycle_members
        assert "LAT-G-MORF-NOM-D2" in cycle_members
        assert "LAT-G-MORF-NOM-D3" in cycle_members


class TestFindOrphanNodes:
    """Tests for orphan node detection."""

    def test_no_orphans(self, sample_graph_data):
        g = load_graph_from_dict(sample_graph_data)
        orphans = find_orphan_nodes(g)
        assert orphans == []

    def test_with_orphan(self, sample_graph_data):
        g = load_graph_from_dict(sample_graph_data)
        # Add an isolated node
        g.add_node("LAT-G-MORF-ORPHAN")
        orphans = find_orphan_nodes(g)
        assert "LAT-G-MORF-ORPHAN" in orphans


class TestFindRootNodes:
    """Tests for root node identification."""

    def test_single_root(self, sample_graph_data):
        g = load_graph_from_dict(sample_graph_data)
        roots = find_root_nodes(g)
        assert roots == ["LAT-G-MORF-NAAMVAL-INTRO"]

    def test_multiple_roots(self, sample_graph_data):
        g = load_graph_from_dict(sample_graph_data)
        # Add a second root
        from gymnasium_classica.models.graph import KennisKnoop

        knoop = KennisKnoop(
            id="LAT-G-MORF-GENUS-INTRO",
            type="G",
            taal="lat",
            titel_nl="Woordgeslacht",
            beschrijving="Introductie woordgeslacht.",
            bloom_niveau="kennis",
            fase="onderbouw_1",
        )
        g.add_node(knoop.id, knoop=knoop)
        roots = find_root_nodes(g)
        assert len(roots) == 2


class TestFindLeafNodes:
    """Tests for leaf node identification."""

    def test_leaf_nodes(self, sample_graph_data):
        g = load_graph_from_dict(sample_graph_data)
        leaves = find_leaf_nodes(g)
        assert set(leaves) == {"LAT-G-MORF-NOM-D1", "LAT-G-MORF-ACC-D1"}


class TestCheckConnectivity:
    """Tests for connectivity analysis."""

    def test_single_component(self, sample_graph_data):
        g = load_graph_from_dict(sample_graph_data)
        num_comp, disconnected = check_connectivity(g)
        assert num_comp == 1
        assert disconnected == []

    def test_multiple_components(self, sample_graph_data):
        g = load_graph_from_dict(sample_graph_data)
        # Add a disconnected subgraph
        from gymnasium_classica.models.graph import KennisKnoop, PrerequisiteEdge

        k1 = KennisKnoop(
            id="GRC-G-FONL-ALFABET",
            type="G", taal="grc",
            titel_nl="Grieks alfabet",
            beschrijving="Introductie Grieks alfabet.",
            bloom_niveau="kennis", fase="onderbouw_1",
        )
        k2 = KennisKnoop(
            id="GRC-G-FONL-ALFA",
            type="G", taal="grc",
            titel_nl="De letter alfa",
            beschrijving="De Griekse letter alfa.",
            bloom_niveau="kennis", fase="onderbouw_1",
        )
        g.add_node(k1.id, knoop=k1)
        g.add_node(k2.id, knoop=k2)
        e = PrerequisiteEdge(
            source_id=k1.id, target_id=k2.id,
            type="prerequisite", encompassing_weight=0.5,
        )
        g.add_edge(k1.id, k2.id, edge=e)

        num_comp, disconnected = check_connectivity(g)
        assert num_comp == 2
        assert len(disconnected) > 0

    def test_empty_graph(self):
        g = load_graph_from_dict({"knopen": [], "edges": []})
        num_comp, disconnected = check_connectivity(g)
        assert num_comp == 0
        assert disconnected == []


class TestTopologicalSort:
    """Tests for topological sorting."""

    def test_valid_dag(self, sample_graph_data):
        g = load_graph_from_dict(sample_graph_data)
        order = topological_sort(g)
        assert order is not None
        assert len(order) == 5

    def test_ordering_correctness(self, sample_graph_data):
        g = load_graph_from_dict(sample_graph_data)
        order = topological_sort(g)
        index = {node: i for i, node in enumerate(order)}
        # Every edge (u, v) must have index(u) < index(v)
        for u, v in g.edges:
            assert index[u] < index[v], f"{u} should come before {v}"

    def test_cyclic_returns_none(self, cyclic_graph_data):
        g = load_graph_from_dict(cyclic_graph_data)
        order = topological_sort(g)
        assert order is None


class TestValidateGraph:
    """Tests for the full validate_graph() function."""

    def test_valid_graph(self, sample_graph_data):
        g = load_graph_from_dict(sample_graph_data)
        report = validate_graph(g)
        assert report.is_valid is True
        assert report.node_count == 5
        assert report.edge_count == 4
        assert report.cycles == []
        assert len(report.root_nodes) == 1
        assert report.topological_order is not None

    def test_cyclic_graph_invalid(self, cyclic_graph_data):
        g = load_graph_from_dict(cyclic_graph_data)
        report = validate_graph(g)
        assert report.is_valid is False
        assert len(report.cycles) > 0
        assert any("Cycle detected" in e for e in report.errors)
        assert report.topological_order is None

    def test_nodes_without_items_warned(self, sample_graph_data):
        g = load_graph_from_dict(sample_graph_data)
        report = validate_graph(g)
        # All nodes have empty items, so each should generate a warning
        item_warnings = [w for w in report.warnings if "has no items" in w]
        assert len(item_warnings) == 5
