#!/usr/bin/env python3
"""Generate items for C1-10: voorzetsels + syntaxis."""
import json, sys
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from gymnasium_classica.models.graph import Item

BASE = Path(__file__).parent.parent / "data" / "graph"
ITEMS_FILE = Path(__file__).parent / "items_c1_10.json"
POC_IDS = {"LAT-G-SYNT-PREP-ACC","LAT-G-SYNT-PREP-ABL","LAT-G-SYNT-ONTK","LAT-G-SYNT-VRAAGZIN"}

def add_items_to_json(json_path, items_by_knoop):
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)
    added = 0
    for knoop in data["knopen"]:
        if knoop["id"] in items_by_knoop:
            existing = {i["id"] for i in knoop.get("items", [])}
            new = [i for i in items_by_knoop[knoop["id"]] if i["id"] not in existing]
            knoop.setdefault("items", []).extend(new)
            added += len(new)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return added

def main():
    raw = json.loads(ITEMS_FILE.read_text(encoding="utf-8"))
    for kid, il in raw.items():
        for d in il:
            Item(**d)
    print("All items validated.")
    poc = {k:v for k,v in raw.items() if k in POC_IDS}
    lj1 = {k:v for k,v in raw.items() if k not in POC_IDS}
    a1 = add_items_to_json(BASE/"lat_grammatica_poc.json", poc)
    a2 = add_items_to_json(BASE/"lat_grammatica_leerjaar1.json", lj1)
    total = sum(len(v) for v in raw.values())
    tc = Counter(i["type"] for il in raw.values() for i in il)
    print(f"Added {a1} to poc, {a2} to leerjaar1. Total: {total} items, {len(raw)} knopen.")
    for t,c in tc.most_common(): print(f"  {t}: {c}")

if __name__ == "__main__":
    main()
