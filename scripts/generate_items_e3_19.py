#!/usr/bin/env python3
"""E3-19: stamtijd-items voor V-werkwoorden.

Achtergrond: alle 450 V-nodes hebben al 4 items (luister_herkenning,
luister_productie, herkenning, productie). De resterende E3-19 scope is
het toevoegen van één stamtijd-productie-item per werkwoord met >= 2
stamtijden (gen-veld in vocab_sources).

Latijn: vraag de 2e stamtijd (perfectum 1sg, bv. dico → dixi).
Grieks: vraag de 2e stamtijd (aoristus 1sg, bv. ἔχω → ἔσχον).

Werkwoorden met maar 1 stamtijd (sum/possum/εἰμί/βούλομαι) worden
geskipt — geen tweede stamtijd om naar te vragen.

Run:
    python scripts/generate_items_e3_19.py            # write
    python scripts/generate_items_e3_19.py --dry-run  # validate only
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from gymnasium_classica.models.graph import Item

ROOT = Path(__file__).parent.parent
VOCAB_SOURCES = ROOT / "data" / "vocab_sources"
GRAPH_DIR = ROOT / "data" / "graph"

# vocab_sources filename → (graph file, node-id-prefix)
SOURCES = [
    ("lat_f01_words.json", "lat_vocabulaire_leerjaar1.json", "LAT-V-F01"),
    ("lat_f02_words.json", "lat_vocabulaire_leerjaar1.json", "LAT-V-F02"),
    ("lat_f03_words.json", "lat_vocabulaire_leerjaar1.json", "LAT-V-F03"),
    ("grc_f01_words.json", "grc_vocabulaire_leerjaar1.json", "GRC-V-F01"),
    ("grc_f02_words.json", "grc_vocabulaire_leerjaar1.json", "GRC-V-F02"),
]


def _stamtijd_label(language: str) -> str:
    return (
        "perfectum (1e persoon enkelvoud)"
        if language == "lat"
        else "aoristus (1e persoon enkelvoud)"
    )


def _short_label(language: str) -> str:
    return "perfectum" if language == "lat" else "aoristus"


def make_stamtijd_item(
    node_id: str, lemma: str, mean: str, gen: str, language: str
) -> dict[str, Any] | None:
    """Build one stamtijd productie-item, or return None if not applicable."""
    parts = [p.strip() for p in (gen or "").split(",") if p.strip()]
    if len(parts) < 2:
        return None
    second = parts[1]
    return {
        "id": f"ITEM-{node_id}-005",
        "node_ids": [node_id],
        "type": "productie",
        "direction": "productief",
        # Stamtijden zijn moeilijker dan basis NL↔lemma
        "difficulty_initial": 1.0,
        "discrimination_initial": 1.2,
        "expected_time_sec": 25,
        "stimulus": {
            "instruction": (
                f"Geef de {_stamtijd_label(language)} van dit "
                f"{'Latijnse' if language == 'lat' else 'Griekse'} werkwoord."
            ),
            "lemma": lemma,
            "translation": mean,
        },
        "answer": second,
        "feedback": (
            f"Stamtijden van {lemma}: {gen}. De {_short_label(language)} (1sg) is {second}."
        ),
        "source": "handmatig",
    }


def collect_items() -> dict[str, list[dict]]:
    """Return {graph_file_name: [item, ...]} for items to add per file."""
    by_file: dict[str, list[tuple[str, dict]]] = {}
    skipped: list[tuple[str, str]] = []
    for src_name, graph_name, prefix in SOURCES:
        language = "lat" if prefix.startswith("LAT") else "grc"
        with open(VOCAB_SOURCES / src_name, encoding="utf-8") as f:
            entries = json.load(f)
        for entry in entries:
            if entry["pos"] != "verb":
                continue
            node_id = f"{prefix}-{entry['id']}"
            item = make_stamtijd_item(
                node_id, entry["lemma"], entry["mean"], entry.get("gen") or "", language
            )
            if item is None:
                skipped.append((node_id, entry.get("gen") or ""))
                continue
            by_file.setdefault(graph_name, []).append((node_id, item))

    print(f"Geskipt (gen heeft < 2 stamtijden): {len(skipped)}")
    for kid, gen in skipped:
        print(f"  - {kid}: gen='{gen}'")

    return by_file


def validate_items(by_file: dict[str, list[tuple[str, dict]]]) -> int:
    """Validate via Pydantic. Returns total item count."""
    total = 0
    for items in by_file.values():
        for _, item in items:
            Item(**item)
            total += 1
    print(f"Gevalideerd: {total} items.")
    return total


def add_items(by_file: dict[str, list[tuple[str, dict]]]) -> int:
    """Append items to graph JSONs. Idempotent."""
    added = 0
    for graph_name, items in by_file.items():
        path = GRAPH_DIR / graph_name
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        # index nodes by id
        node_index = {k["id"]: k for k in data["nodes"]}
        for node_id, item in items:
            node = node_index.get(node_id)
            if node is None:
                print(f"  ⚠ node niet gevonden: {node_id}")
                continue
            existing_ids = {it["id"] for it in node.get("items", [])}
            if item["id"] in existing_ids:
                continue
            node.setdefault("items", []).append(item)
            added += 1
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print(f"  ✓ {graph_name}: items toegevoegd")
    return added


def print_summary(by_file: dict[str, list[tuple[str, dict]]]) -> None:
    total = sum(len(items) for items in by_file.values())
    by_taal = Counter()
    for items in by_file.values():
        for kid, _ in items:
            by_taal["lat" if kid.startswith("LAT") else "grc"] += 1
    print("\n=== E3-19 stamtijd-items ===")
    print(f"Totaal: {total}")
    print(f"  LAT: {by_taal['lat']}")
    print(f"  GRC: {by_taal['grc']}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    by_file = collect_items()
    validate_items(by_file)
    print_summary(by_file)

    if args.dry_run:
        print("\nDry-run: geen wijzigingen geschreven.")
        return

    print("\nWijzigingen schrijven…")
    added = add_items(by_file)
    print(f"\nToegevoegd: {added} items.")


if __name__ == "__main__":
    main()
