"""Load a knowledge graph from JSON into a NetworkX DiGraph."""

import json
from pathlib import Path

import networkx as nx

from gymnasium_classica.models.graph import GraphData, KennisKnoop, PrerequisiteEdge


def load_graph(path: Path) -> nx.DiGraph:
    """Load a knowledge graph from a JSON file.

    The JSON file must contain keys "knopen" (list of nodes) and "edges"
    (list of prerequisite edges).

    Returns:
        A NetworkX DiGraph where each node stores a KennisKnoop instance
        under the ``"knoop"`` attribute and each edge stores a
        PrerequisiteEdge instance under the ``"edge"`` attribute.

    Raises:
        FileNotFoundError: if *path* does not exist.
        json.JSONDecodeError: if the file is not valid JSON.
        pydantic.ValidationError: if any node or edge fails schema validation.
        ValueError: if an edge references a non-existent node or duplicate IDs exist.
    """
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return load_graph_from_dict(data)


def load_graph_from_dict(data: dict) -> nx.DiGraph:
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


def graph_to_dict(graph: nx.DiGraph) -> dict:
    """Serialize a NetworkX DiGraph back to a dict compatible with the JSON schema.

    Performs a round-trip: ``load_graph_from_dict(graph_to_dict(g))``
    produces an equivalent graph.
    """
    knopen = []
    for node_id in graph.nodes:
        knoop: KennisKnoop = graph.nodes[node_id]["knoop"]
        knopen.append(knoop.model_dump())

    edges = []
    for u, v in graph.edges:
        edge: PrerequisiteEdge = graph.edges[u, v]["edge"]
        edges.append(edge.model_dump())

    return {"knopen": knopen, "edges": edges}
