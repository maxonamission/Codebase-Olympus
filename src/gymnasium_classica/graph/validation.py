"""Validation functions for the knowledge graph."""

from dataclasses import dataclass, field
from pathlib import Path

import networkx as nx

from gymnasium_classica.models.graph import KennisKnoop, PrerequisiteEdge
from gymnasium_classica.schemas.id_schema import validate_knoop_id


@dataclass
class ValidationReport:
    """Result of a full graph validation run."""

    is_valid: bool = True
    node_count: int = 0
    edge_count: int = 0
    transfer_edge_count: int = 0
    root_nodes: list[str] = field(default_factory=list)
    leaf_nodes: list[str] = field(default_factory=list)
    cycles: list[list[str]] = field(default_factory=list)
    orphan_nodes: list[str] = field(default_factory=list)
    weakly_connected_components: int = 0
    disconnected_nodes: list[str] = field(default_factory=list)
    topological_order: list[str] | None = None
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


def _prerequisite_enrichment_subgraph(graph: nx.DiGraph) -> nx.DiGraph:
    """Return a view of the graph with only prerequisite and enrichment edges.

    Transfer edges are excluded because they represent bidirectional
    cross-linguistic connections and are not subject to DAG constraints.
    """
    sub = graph.copy()
    transfer_edges = [
        (u, v)
        for u, v in sub.edges
        if sub.edges[u, v].get("edge") and sub.edges[u, v]["edge"].type == "transfer"
    ]
    sub.remove_edges_from(transfer_edges)
    return sub


def detect_cycles(graph: nx.DiGraph) -> list[list[str]]:
    """Return all simple cycles in the prerequisite+enrichment subgraph.

    Transfer edges are excluded from cycle detection because they
    represent bidirectional cross-linguistic connections.
    """
    sub = _prerequisite_enrichment_subgraph(graph)
    return list(nx.simple_cycles(sub))


def find_orphan_nodes(graph: nx.DiGraph) -> list[str]:
    """Find nodes with no incoming AND no outgoing edges."""
    return [n for n in graph.nodes if graph.in_degree(n) == 0 and graph.out_degree(n) == 0]


def find_root_nodes(graph: nx.DiGraph) -> list[str]:
    """Find nodes with in-degree 0 (entry points to the learning path)."""
    return [n for n in graph.nodes if graph.in_degree(n) == 0]


def find_leaf_nodes(graph: nx.DiGraph) -> list[str]:
    """Find nodes with out-degree 0 (terminal nodes)."""
    return [n for n in graph.nodes if graph.out_degree(n) == 0]


def check_connectivity(graph: nx.DiGraph) -> tuple[int, list[str]]:
    """Check weak connectivity.

    Returns:
        (number_of_components, nodes_not_in_largest_component)
    """
    if graph.number_of_nodes() == 0:
        return (0, [])

    components = list(nx.weakly_connected_components(graph))
    num_components = len(components)

    if num_components <= 1:
        return (num_components, [])

    largest = max(components, key=len)
    disconnected = []
    for comp in components:
        if comp is not largest:
            disconnected.extend(sorted(comp))
    return (num_components, disconnected)


def topological_sort(graph: nx.DiGraph) -> list[str] | None:
    """Return a topological ordering of the prerequisite+enrichment subgraph.

    Transfer edges are excluded because they may be bidirectional.
    Returns None if the prerequisite+enrichment subgraph has cycles.
    """
    sub = _prerequisite_enrichment_subgraph(graph)
    if not nx.is_directed_acyclic_graph(sub):
        return None
    return list(nx.topological_sort(sub))


def validate_edge_weights(graph: nx.DiGraph) -> list[str]:
    """Validate that all encompassing_weight values are in [0.0, 1.0].

    Returns a list of error messages for invalid weights.
    """
    errors = []
    for u, v in graph.edges:
        edge: PrerequisiteEdge = graph.edges[u, v]["edge"]
        if not (0.0 <= edge.encompassing_weight <= 1.0):
            errors.append(
                f"Edge {u} -> {v}: encompassing_weight {edge.encompassing_weight} "
                f"is outside [0.0, 1.0]"
            )
    return errors


def validate_node_ids(graph: nx.DiGraph) -> list[str]:
    """Validate that all node IDs conform to the ID schema.

    Returns a list of error messages for invalid IDs.
    """
    errors = []
    for node_id in graph.nodes:
        if not validate_knoop_id(node_id):
            errors.append(f"Invalid node ID: {node_id!r}")
    return errors


def validate_content_refs(graph: nx.DiGraph, repo_root: Path) -> list[str]:
    """Check that every knoop's ``content_ref`` points at an existing file.

    Relative paths are resolved against *repo_root*.  Absolute paths are
    used as-is.  Knopen without a ``content_ref`` are ignored — the
    loader falls back to ``data/content/{id}.md`` in that case, which is
    checked separately by the content-coverage script.

    Returns:
        A list of error messages for dangling references. Empty if all
        ``content_ref`` values resolve to existing files.
    """
    errors: list[str] = []
    for node_id in graph.nodes:
        knoop: KennisKnoop | None = graph.nodes[node_id].get("knoop")
        if knoop is None or knoop.content_ref is None:
            continue
        ref_path = Path(knoop.content_ref)
        resolved = ref_path if ref_path.is_absolute() else repo_root / ref_path
        if not resolved.is_file():
            errors.append(
                f"Knoop {node_id}: content_ref {knoop.content_ref!r} "
                f"verwijst naar niet-bestaand bestand ({resolved})."
            )
    return errors


def validate_graph(
    graph: nx.DiGraph,
    *,
    content_root: Path | None = None,
) -> ValidationReport:
    """Run all validation checks on a knowledge graph.

    Checks:
      1. Cycle detection (graph must be a DAG)
      2. Orphan detection (nodes with no edges)
      3. Connectivity analysis
      4. Topological sort (only if acyclic)
      5. Root/leaf node identification
      6. Edge weight validation
      7. Node ID format validation
      8. Nodes without items (warning)
      9. content_ref existence (only when *content_root* is supplied)

    Args:
        graph: The NetworkX DiGraph to validate.
        content_root: Optional repo-root Path against which relative
            ``content_ref`` paths are resolved.  When None, the
            content_ref check is skipped (useful for pure in-memory
            unit tests).
    """
    report = ValidationReport()
    report.node_count = graph.number_of_nodes()
    report.edge_count = graph.number_of_edges()
    report.transfer_edge_count = sum(
        1
        for _, _, data in graph.edges(data=True)
        if data.get("edge") and data["edge"].type == "transfer"
    )

    # 1. Cycles (prerequisite+enrichment only; transfer edges excluded)
    report.cycles = detect_cycles(graph)
    if report.cycles:
        report.is_valid = False
        for cycle in report.cycles:
            report.errors.append(f"Cycle detected: {' -> '.join(cycle)}")

    # 2. Orphans
    report.orphan_nodes = find_orphan_nodes(graph)
    if report.orphan_nodes:
        report.warnings.append(f"Orphan nodes (no edges): {', '.join(report.orphan_nodes)}")

    # 3. Connectivity
    num_comp, disconnected = check_connectivity(graph)
    report.weakly_connected_components = num_comp
    report.disconnected_nodes = disconnected
    if num_comp > 1:
        report.warnings.append(
            f"Graph has {num_comp} weakly connected components. "
            f"Disconnected nodes: {', '.join(disconnected)}"
        )

    # 4. Topological sort
    report.topological_order = topological_sort(graph)

    # 5. Root and leaf nodes
    report.root_nodes = find_root_nodes(graph)
    report.leaf_nodes = find_leaf_nodes(graph)

    # 6. Edge weights
    weight_errors = validate_edge_weights(graph)
    if weight_errors:
        report.is_valid = False
        report.errors.extend(weight_errors)

    # 7. Node IDs
    id_errors = validate_node_ids(graph)
    if id_errors:
        report.is_valid = False
        report.errors.extend(id_errors)

    # 8. Nodes without items (non-fatal)
    for node_id in graph.nodes:
        knoop = graph.nodes[node_id].get("knoop")
        if knoop and not knoop.items:
            report.warnings.append(f"Node {node_id} has no items")

    # 9. content_ref existence (opt-in)
    if content_root is not None:
        content_errors = validate_content_refs(graph, content_root)
        if content_errors:
            report.is_valid = False
            report.errors.extend(content_errors)

    return report
