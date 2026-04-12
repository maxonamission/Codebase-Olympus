#!/usr/bin/env python3
"""CLI script: print summary statistics for a knowledge graph."""

import sys
from pathlib import Path

import networkx as nx

from gymnasium_classica.graph.loader import load_graph
from gymnasium_classica.graph.validation import find_leaf_nodes, find_root_nodes


def main() -> None:
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <graph.json>", file=sys.stderr)
        sys.exit(1)

    path = Path(sys.argv[1])
    graph = load_graph(path)

    roots = find_root_nodes(graph)
    leaves = find_leaf_nodes(graph)

    # Compute topological depth (longest path from any root)
    if nx.is_directed_acyclic_graph(graph):
        topo_depth = nx.dag_longest_path_length(graph)
    else:
        topo_depth = "N/A (graph has cycles)"

    # Count by type
    type_counts: dict[str, int] = {}
    bloom_counts: dict[str, int] = {}
    for node_id in graph.nodes:
        knoop = graph.nodes[node_id].get("knoop")
        if knoop:
            type_counts[knoop.type] = type_counts.get(knoop.type, 0) + 1
            bloom_counts[knoop.bloom_niveau] = bloom_counts.get(knoop.bloom_niveau, 0) + 1

    print(f"=== Graph Statistics: {path.name} ===")
    print(f"Nodes:              {graph.number_of_nodes()}")
    print(f"Edges:              {graph.number_of_edges()}")
    print(f"Root nodes:         {len(roots)}")
    print(f"Leaf nodes:         {len(leaves)}")
    print(f"Topological depth:  {topo_depth}")
    print(f"Avg in-degree:      {sum(d for _, d in graph.in_degree()) / max(graph.number_of_nodes(), 1):.1f}")
    print(f"Avg out-degree:     {sum(d for _, d in graph.out_degree()) / max(graph.number_of_nodes(), 1):.1f}")

    if type_counts:
        print("\nNodes by type:")
        for t in sorted(type_counts):
            print(f"  {t}: {type_counts[t]}")

    if bloom_counts:
        print("\nNodes by Bloom level:")
        for b in sorted(bloom_counts):
            print(f"  {b}: {bloom_counts[b]}")


if __name__ == "__main__":
    main()
