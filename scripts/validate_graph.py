#!/usr/bin/env python3
"""CLI script: load a knowledge graph JSON file and print a validation report."""

import sys
from pathlib import Path

from gymnasium_classica.graph.loader import load_graph
from gymnasium_classica.graph.validation import validate_graph


def main() -> None:
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <graph.json>", file=sys.stderr)
        sys.exit(1)

    path = Path(sys.argv[1])
    graph = load_graph(path)
    report = validate_graph(graph)

    print(f"=== Validation Report: {path.name} ===")
    print(f"Nodes:      {report.node_count}")
    print(f"Edges:      {report.edge_count}")
    print(f"Valid:      {report.is_valid}")
    print(f"Components: {report.weakly_connected_components}")
    print(f"Cycles:     {len(report.cycles)}")
    print(f"Orphans:    {len(report.orphan_nodes)}")
    print(f"Root nodes: {len(report.root_nodes)}")
    for root in sorted(report.root_nodes):
        print(f"  - {root}")
    print(f"Leaf nodes: {len(report.leaf_nodes)}")
    for leaf in sorted(report.leaf_nodes):
        print(f"  - {leaf}")

    if report.errors:
        print(f"\nErrors ({len(report.errors)}):")
        for err in report.errors:
            print(f"  [ERROR] {err}")

    if report.warnings:
        non_item_warnings = [w for w in report.warnings if "has no items" not in w]
        item_warnings = len(report.warnings) - len(non_item_warnings)
        if non_item_warnings:
            print(f"\nWarnings ({len(non_item_warnings)}):")
            for warn in non_item_warnings:
                print(f"  [WARN] {warn}")
        if item_warnings:
            print(f"\n  ({item_warnings} nodes have no items — expected in phase 0)")

    sys.exit(0 if report.is_valid else 1)


if __name__ == "__main__":
    main()
