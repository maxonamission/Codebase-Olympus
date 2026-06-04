"""Load a knowledge graph from JSON into a NetworkX DiGraph."""

import json
from pathlib import Path
from typing import Any

import networkx as nx

from gymnasium_classica.models.graph import GraphData, Node, PrerequisiteEdge


def load_graph(path: Path) -> nx.DiGraph:
    """Load a knowledge graph from a JSON file or a directory of JSON files.

    When *path* is a file, it must contain keys "knopen" and "edges".
    When *path* is a directory, all ``*.json`` files in it are loaded and
    merged into a single graph.  Nodes are collected first from all files,
    then edges — so cross-file edges (e.g. transfer edges in a separate
    file referencing nodes defined elsewhere) are resolved correctly.

    Returns:
        A NetworkX DiGraph where each node stores a Node instance
        under the ``"knoop"`` attribute and each edge stores a
        PrerequisiteEdge instance under the ``"edge"`` attribute.

    Raises:
        FileNotFoundError: if *path* does not exist.
        json.JSONDecodeError: if any file is not valid JSON.
        pydantic.ValidationError: if any node or edge fails schema validation.
        ValueError: if an edge references a non-existent node or duplicate IDs exist.
    """
    if path.is_dir():
        return _load_graph_directory(path)
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return load_graph_from_dict(data)


def _load_graph_directory(directory: Path) -> nx.DiGraph:
    """Load and merge all JSON graph files in *directory*."""
    json_files = sorted(directory.glob("*.json"))
    if not json_files:
        raise FileNotFoundError(f"No .json files found in {directory}")

    all_knopen: list[dict[str, Any]] = []
    all_edges: list[dict[str, Any]] = []

    for file_path in json_files:
        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)
        all_knopen.extend(data.get("knopen", []))
        all_edges.extend(data.get("edges", []))

    return load_graph_from_dict({"knopen": all_knopen, "edges": all_edges})


def load_graph_from_dict(data: dict[str, Any]) -> nx.DiGraph:
    """Load a knowledge graph from an already-parsed dict.

    Validates all data through Pydantic models before building the graph.
    """
    graph_data = GraphData(**data)

    graph = nx.DiGraph()

    # Add nodes — check for duplicates
    seen_ids: set[str] = set()
    for knoop in graph_data.knopen:
        if knoop.id in seen_ids:
            raise ValueError(f"Duplicate knoop ID: {knoop.id!r}")
        seen_ids.add(knoop.id)
        graph.add_node(knoop.id, knoop=knoop)

    # Add edges — validate that both endpoints exist
    dangling: list[str] = []
    for edge in graph_data.edges:
        if edge.source_id not in seen_ids:
            dangling.append(f"Edge source {edge.source_id!r} not found in nodes")
        if edge.target_id not in seen_ids:
            dangling.append(f"Edge target {edge.target_id!r} not found in nodes")

    if dangling:
        raise ValueError(
            "Dangling edge references:\n" + "\n".join(f"  - {msg}" for msg in dangling)
        )

    for edge in graph_data.edges:
        graph.add_edge(edge.source_id, edge.target_id, edge=edge)

    return graph


def graph_to_dict(graph: nx.DiGraph) -> dict[str, Any]:
    """Serialize a NetworkX DiGraph back to a dict compatible with the JSON schema.

    Performs a round-trip: ``load_graph_from_dict(graph_to_dict(g))``
    produces an equivalent graph.
    """
    knopen = []
    for node_id in graph.nodes:
        knoop: Node = graph.nodes[node_id]["knoop"]
        knopen.append(knoop.model_dump())

    edges = []
    for u, v in graph.edges:
        edge: PrerequisiteEdge = graph.edges[u, v]["edge"]
        edges.append(edge.model_dump())

    return {"knopen": knopen, "edges": edges}
