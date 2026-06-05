"""Validation functions for the knowledge graph."""

from dataclasses import dataclass, field
from pathlib import Path

import networkx as nx

from gymnasium_classica.models.graph import EdgeType, Node, PrerequisiteEdge
from gymnasium_classica.schemas.id_schema import validate_node_id


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


# Edge-types waarover de graph acyclisch moet zijn. Eén plek voor het
# beleid: cycle-detectie en topologische sortering gebruiken precies deze
# set. `transfer` staat er bewust NIET in — transfer-edges zijn
# bidirectionele, cross-linguïstische verbanden (LAT <-> GRC) die per
# definitie cyclisch mogen zijn en geen leervolgorde opleggen. Een vierde
# edge-type toevoegen kost één regel: opnemen in of weglaten uit deze set.
ACYCLIC_EDGE_TYPES: frozenset[str] = frozenset({"prerequisite", "enrichment", "procedure_step"})


def acyclic_subgraph(
    graph: nx.DiGraph, *, include_edge_types: frozenset[str] | set[str]
) -> nx.DiGraph:
    """Return a copy of *graph* keeping only edges of *include_edge_types*.

    Edges whose attached ``edge`` object has a ``type`` outside the given
    set are removed; nodes and edges without a typed ``edge`` object are
    left untouched. Used to isolate the subgraph that must satisfy the
    DAG constraint (see :data:`ACYCLIC_EDGE_TYPES`).
    """
    sub = graph.copy()
    excluded = [
        (u, v)
        for u, v in sub.edges
        if (edge := sub.edges[u, v].get("edge")) is not None
        and edge.type not in include_edge_types
    ]
    sub.remove_edges_from(excluded)
    return sub


def detect_cycles(graph: nx.DiGraph) -> list[list[str]]:
    """Return all simple cycles in the acyclic-edge-type subgraph.

    Transfer edges are excluded from cycle detection because they
    represent bidirectional cross-linguistic connections.
    """
    sub = acyclic_subgraph(graph, include_edge_types=ACYCLIC_EDGE_TYPES)
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
    """Return a topological ordering of the acyclic-edge-type subgraph.

    Transfer edges are excluded because they may be bidirectional.
    Returns None if that subgraph has cycles.
    """
    sub = acyclic_subgraph(graph, include_edge_types=ACYCLIC_EDGE_TYPES)
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
        if not validate_node_id(node_id):
            errors.append(f"Invalid node ID: {node_id!r}")
    return errors


def validate_content_refs(graph: nx.DiGraph, repo_root: Path) -> list[str]:
    """Check that every node's ``content_ref`` points at an existing file.

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
        node: Node | None = graph.nodes[node_id].get("node")
        if node is None or node.content_ref is None:
            continue
        ref_path = Path(node.content_ref)
        resolved = ref_path if ref_path.is_absolute() else repo_root / ref_path
        if not resolved.is_file():
            errors.append(
                f"Knoop {node_id}: content_ref {node.content_ref!r} "
                f"verwijst naar niet-bestaand bestand ({resolved})."
            )
    return errors


def validate_procedures(graph: nx.DiGraph) -> list[str]:
    """Validate that every procedure (type-P) is a well-formed linear path.

    A procedure is a weakly-connected group of nodes joined by
    ``procedure_step`` edges (e.g. the POLMO chain PV -> OND -> LV -> MV
    -> OV). Each such group must be a single, non-branching chain:

      - no node has more than one incoming or one outgoing
        ``procedure_step`` edge (no branching/merging),
      - exactly one node has no incoming ``procedure_step`` edge (start),
      - exactly one node has no outgoing ``procedure_step`` edge (end).

    Acyclicity of ``procedure_step`` is already enforced globally via
    :data:`ACYCLIC_EDGE_TYPES`; here we additionally require linearity.

    Returns a list of error messages (empty if all procedures are valid).
    """
    step_edges = [
        (u, v)
        for u, v in graph.edges
        if (edge := graph.edges[u, v].get("edge")) is not None
        and edge.type == EdgeType.PROCEDURE_STEP
    ]
    if not step_edges:
        return []

    proc = nx.DiGraph()
    proc.add_edges_from(step_edges)

    errors: list[str] = []
    for component in nx.weakly_connected_components(proc):
        sub = proc.subgraph(component)
        label = min(component)  # stable, deterministic label for messages
        branching = sorted(n for n in sub if sub.in_degree(n) > 1 or sub.out_degree(n) > 1)
        starts = [n for n in sub if sub.in_degree(n) == 0]
        ends = [n for n in sub if sub.out_degree(n) == 0]
        if branching:
            errors.append(
                f"Procedure '{label}' vertakt (procedure_step is geen lineair pad) "
                f"bij: {', '.join(branching)}"
            )
        if len(starts) != 1:
            errors.append(
                f"Procedure '{label}' heeft {len(starts)} startknopen "
                f"(verwacht precies 1): {', '.join(sorted(starts))}"
            )
        if len(ends) != 1:
            errors.append(
                f"Procedure '{label}' heeft {len(ends)} eindknopen "
                f"(verwacht precies 1): {', '.join(sorted(ends))}"
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
      10. Procedure linearity (type-P procedure_step chains)

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
        node = graph.nodes[node_id].get("node")
        if node and not node.items:
            report.warnings.append(f"Node {node_id} has no items")

    # 9. content_ref existence (opt-in)
    if content_root is not None:
        content_errors = validate_content_refs(graph, content_root)
        if content_errors:
            report.is_valid = False
            report.errors.extend(content_errors)

    # 10. Procedure linearity (type-P nodes joined by procedure_step)
    procedure_errors = validate_procedures(graph)
    if procedure_errors:
        report.is_valid = False
        report.errors.extend(procedure_errors)

    return report
