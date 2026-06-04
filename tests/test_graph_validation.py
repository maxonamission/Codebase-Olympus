"""Tests for graph validation: cycles, orphans, connectivity, topological sort."""

import copy

from gymnasium_classica.graph.loader import load_graph_from_dict
from gymnasium_classica.graph.validation import (
    ACYCLIC_EDGE_TYPES,
    acyclic_subgraph,
    check_connectivity,
    detect_cycles,
    find_leaf_nodes,
    find_orphan_nodes,
    find_root_nodes,
    topological_sort,
    validate_content_refs,
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

    def test_bidirectional_transfer_no_cycles(self, bidirectional_transfer_graph_data):
        """Bidirectional transfer edges should NOT be detected as cycles."""
        g = load_graph_from_dict(bidirectional_transfer_graph_data)
        cycles = detect_cycles(g)
        assert cycles == []


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
        from gymnasium_classica.models.graph import Node

        node = Node(
            id="LAT-G-MORF-GENUS-INTRO",
            type="G",
            language="lat",
            title_nl="Woordgeslacht",
            description="Introductie woordgeslacht.",
            bloom_level="knowledge",
            phase="onderbouw_1",
        )
        g.add_node(node.id, node=node)
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
        from gymnasium_classica.models.graph import Node, PrerequisiteEdge

        k1 = Node(
            id="GRC-G-FONL-ALFABET",
            type="G",
            language="grc",
            title_nl="Grieks alfabet",
            description="Introductie Grieks alfabet.",
            bloom_level="knowledge",
            phase="onderbouw_1",
        )
        k2 = Node(
            id="GRC-G-FONL-ALFA",
            type="G",
            language="grc",
            title_nl="De letter alfa",
            description="De Griekse letter alfa.",
            bloom_level="knowledge",
            phase="onderbouw_1",
        )
        g.add_node(k1.id, node=k1)
        g.add_node(k2.id, node=k2)
        e = PrerequisiteEdge(
            source_id=k1.id,
            target_id=k2.id,
            type="prerequisite",
            encompassing_weight=0.5,
        )
        g.add_edge(k1.id, k2.id, edge=e)

        num_comp, disconnected = check_connectivity(g)
        assert num_comp == 2
        assert len(disconnected) > 0

    def test_empty_graph(self):
        g = load_graph_from_dict({"nodes": [], "edges": []})
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

    def test_bidirectional_transfer_valid(self, bidirectional_transfer_graph_data):
        """A graph with bidirectional transfer edges should be valid."""
        g = load_graph_from_dict(bidirectional_transfer_graph_data)
        report = validate_graph(g)
        assert report.is_valid is True
        assert report.cycles == []
        assert report.transfer_edge_count == 4
        assert report.topological_order is not None

    def test_transfer_edge_count(self, bidirectional_transfer_graph_data):
        g = load_graph_from_dict(bidirectional_transfer_graph_data)
        report = validate_graph(g)
        assert report.edge_count == 6  # 2 prerequisite + 4 transfer
        assert report.transfer_edge_count == 4


class TestAcyclicSubgraph:
    """Tests for the generic acyclic_subgraph helper and ACYCLIC_EDGE_TYPES."""

    def test_excludes_transfer_edges(self, bidirectional_transfer_graph_data):
        g = load_graph_from_dict(bidirectional_transfer_graph_data)
        sub = acyclic_subgraph(g, include_edge_types=ACYCLIC_EDGE_TYPES)
        assert sub.number_of_edges() == 2  # only prerequisite edges
        assert sub.number_of_nodes() == 4  # all nodes preserved

    def test_preserves_prerequisite_edges(self, sample_graph_data):
        g = load_graph_from_dict(sample_graph_data)
        sub = acyclic_subgraph(g, include_edge_types=ACYCLIC_EDGE_TYPES)
        assert sub.number_of_edges() == g.number_of_edges()  # no transfer edges to remove

    def test_does_not_modify_original(self, bidirectional_transfer_graph_data):
        g = load_graph_from_dict(bidirectional_transfer_graph_data)
        original_edges = g.number_of_edges()
        acyclic_subgraph(g, include_edge_types=ACYCLIC_EDGE_TYPES)
        assert g.number_of_edges() == original_edges

    def test_acyclic_subgraph_excludes_specified_types(self, bidirectional_transfer_graph_data):
        """Restricting to a type set drops all other edge types, so the
        bidirectional transfer edges cannot show up as cycles."""
        g = load_graph_from_dict(bidirectional_transfer_graph_data)
        only_prereq = acyclic_subgraph(g, include_edge_types={"prerequisite"})
        # No transfer edges survive the filter -> prerequisite-only view.
        assert only_prereq.number_of_edges() == 2
        assert detect_cycles(g) == []
        # The policy constant deliberately excludes transfer.
        assert "transfer" not in ACYCLIC_EDGE_TYPES
        assert frozenset({"prerequisite", "enrichment"}) == ACYCLIC_EDGE_TYPES


class TestValidateContentRefs:
    """Controleert dat dangling content_ref-paden als fout worden gemeld."""

    def test_missing_content_file_is_reported(self, sample_graph_data, tmp_path):
        data = copy.deepcopy(sample_graph_data)
        data["nodes"][0]["content_ref"] = "data/content/DOES-NOT-EXIST.md"
        g = load_graph_from_dict(data)

        errors = validate_content_refs(g, tmp_path)
        assert len(errors) == 1
        assert "DOES-NOT-EXIST.md" in errors[0]
        assert data["nodes"][0]["id"] in errors[0]

    def test_existing_content_file_is_accepted(self, sample_graph_data, tmp_path):
        (tmp_path / "data" / "content").mkdir(parents=True)
        (tmp_path / "data" / "content" / "foo.md").write_text("# hi\n", encoding="utf-8")

        data = copy.deepcopy(sample_graph_data)
        data["nodes"][0]["content_ref"] = "data/content/foo.md"
        g = load_graph_from_dict(data)

        errors = validate_content_refs(g, tmp_path)
        assert errors == []

    def test_no_content_ref_is_ignored(self, sample_graph_data, tmp_path):
        """Knopen zonder content_ref worden overgeslagen (ID-fallback)."""
        g = load_graph_from_dict(sample_graph_data)
        assert validate_content_refs(g, tmp_path) == []

    def test_validate_graph_bubbles_up_content_errors(self, sample_graph_data, tmp_path):
        """`validate_graph` markeert ontbrekende content als fout."""
        data = copy.deepcopy(sample_graph_data)
        data["nodes"][0]["content_ref"] = "data/content/DOES-NOT-EXIST.md"
        g = load_graph_from_dict(data)

        report = validate_graph(g, content_root=tmp_path)
        assert report.is_valid is False
        assert any("DOES-NOT-EXIST.md" in err for err in report.errors)

    def test_validate_graph_without_content_root_skips_check(self, sample_graph_data, tmp_path):
        """Zonder content_root blijft content_ref ongecontroleerd."""
        data = copy.deepcopy(sample_graph_data)
        data["nodes"][0]["content_ref"] = "data/content/DOES-NOT-EXIST.md"
        g = load_graph_from_dict(data)

        report = validate_graph(g)
        assert report.is_valid is True
