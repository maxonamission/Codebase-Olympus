#!/usr/bin/env python3
"""CLI script: print summary statistics for a knowledge graph.

Accepts either a single JSON file or a directory with multiple graph JSONs
(cross-file edges are resolved when loading a directory)."""

import sys
from pathlib import Path

import networkx as nx

from gymnasium_classica.graph.loader import load_graph
from gymnasium_classica.graph.validation import find_leaf_nodes, find_root_nodes


def main() -> None:
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <graph.json | graph_dir>", file=sys.stderr)
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

    # Count by type + item coverage per type
    type_counts: dict[str, int] = {}
    bloom_counts: dict[str, int] = {}
    items_per_type: dict[str, int] = {}
    nodes_with_items_per_type: dict[str, int] = {}
    zero_item_nodes: list[str] = []
    for node_id in graph.nodes:
        node = graph.nodes[node_id].get("node")
        if node is None:
            continue
        t = node.type
        type_counts[t] = type_counts.get(t, 0) + 1
        bloom_counts[node.bloom_niveau] = bloom_counts.get(node.bloom_niveau, 0) + 1
        n_items = len(node.items)
        items_per_type[t] = items_per_type.get(t, 0) + n_items
        if n_items > 0:
            nodes_with_items_per_type[t] = nodes_with_items_per_type.get(t, 0) + 1
        else:
            zero_item_nodes.append(node_id)

    print(f"=== Graph Statistics: {path.name} ===")
    print(f"Nodes:              {graph.number_of_nodes()}")
    print(f"Edges:              {graph.number_of_edges()}")
    print(f"Root nodes:         {len(roots)}")
    print(f"Leaf nodes:         {len(leaves)}")
    print(f"Topological depth:  {topo_depth}")
    print(
        f"Avg in-degree:      {sum(d for _, d in graph.in_degree()) / max(graph.number_of_nodes(), 1):.1f}"
    )
    print(
        f"Avg out-degree:     {sum(d for _, d in graph.out_degree()) / max(graph.number_of_nodes(), 1):.1f}"
    )

    if type_counts:
        print("\nNodes by type (with items / total, total items):")
        for t in sorted(type_counts):
            total = type_counts[t]
            covered = nodes_with_items_per_type.get(t, 0)
            items = items_per_type.get(t, 0)
            pct = 100.0 * covered / total if total else 0.0
            print(f"  {t}: {covered}/{total} nodes with items ({pct:.1f}%), {items} items total")

    if bloom_counts:
        print("\nNodes by Bloom level:")
        for b in sorted(bloom_counts):
            print(f"  {b}: {bloom_counts[b]}")

    if zero_item_nodes:
        print(f"\nNodes with 0 items: {len(zero_item_nodes)}")
        for nid in sorted(zero_item_nodes)[:20]:
            print(f"  {nid}")
        if len(zero_item_nodes) > 20:
            print(f"  ... en {len(zero_item_nodes) - 20} meer")


if __name__ == "__main__":
    main()
