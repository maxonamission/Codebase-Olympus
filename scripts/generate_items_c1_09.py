#!/usr/bin/env python3
"""Generate items for C1-09: pronomina."""

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from gymnasium_classica.models.graph import Item

BASE = Path(__file__).parent.parent / "data" / "graph"
ITEMS_FILE = Path(__file__).parent / "items_c1_09.json"


def add_items_to_json(json_path, items_by_node):
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)
    added = 0
    for node in data["knopen"]:
        if node["id"] in items_by_node:
            existing = {i["id"] for i in node.get("items", [])}
            new = [i for i in items_by_node[node["id"]] if i["id"] not in existing]
            node.setdefault("items", []).extend(new)
            added += len(new)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return added


def main():
    raw = json.loads(ITEMS_FILE.read_text(encoding="utf-8"))
    for _kid, il in raw.items():
        for d in il:
            Item(**d)
    print("All items validated.")
    # All C1-09 nodes are in leerjaar1
    a2 = add_items_to_json(BASE / "lat_grammatica_leerjaar1.json", raw)
    total = sum(len(v) for v in raw.values())
    tc = Counter(i["type"] for il in raw.values() for i in il)
    print(f"Added {a2} to leerjaar1. Total: {total} items, {len(raw)} knopen.")
    for t, c in tc.most_common():
        print(f"  {t}: {c}")


if __name__ == "__main__":
    main()
