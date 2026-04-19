#!/usr/bin/env python3
"""Enrich V-nodes in the vocabulary graph files with text-based items.

Every V-node in the Latin/Greek vocabulary files today has two items:
``luister_herkenning`` and ``luister_productie``.  Both depend on the audio
pipeline.  This script adds two text-based items per node so the scheduler
always has a receptive and a productive alternative available without audio:

* ``herkenning``  — read lemma, pick NL translation (4 options)
* ``productie``   — given NL translation, type the lemma

Idempotent: existing items of these types are left untouched, so a second
run is a no-op.  Distractor selection is deterministic (``random.seed(42)``)
so the output JSON is reproducible.

Usage::

    python scripts/generate_vocab_enrichment.py
    python scripts/generate_vocab_enrichment.py --graph-dir data/graph
"""

from __future__ import annotations

import argparse
import random
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _SCRIPT_DIR.parent

sys.path.insert(0, str(_PROJECT_ROOT / "src"))

# Reuse the text-handling helpers from the luister-items generator so both
# scripts agree on how to parse titles, pick first-word lemmata, and shorten
# translations.  Import path is relative to the scripts directory.
sys.path.insert(0, str(_SCRIPT_DIR))
from generate_luister_items import (  # type: ignore
    build_translation_pool,
    extract_first_word,
    extract_short_translation,
    load_vocab_json,
    next_item_nr,
    parse_titel,
    pick_distractors,
    save_vocab_json,
)

HERKENNING_B_RANGE = (-0.8, 0.2)
PRODUCTIE_B_RANGE = (0.3, 1.8)
HERKENNING_TIME_SEC = 10
PRODUCTIE_TIME_SEC = 20


def _taal_labels(knoop_id: str) -> tuple[str, str]:
    """Return ('Latijnse', 'Latijn') or ('Griekse', 'Grieks')."""
    if knoop_id.startswith("LAT"):
        return "Latijnse", "Latijn"
    return "Griekse", "Grieks"


def generate_herkenning_item(node: dict, translation_pool: list[str], item_nr: int) -> dict:
    """Text-based herkenning: read lemma, pick the Dutch translation."""
    knoop_id = node["id"]
    lemma, translation = parse_titel(node["titel_nl"])
    first_word = extract_first_word(lemma)
    correct = extract_short_translation(translation)
    distractors = pick_distractors(correct, translation_pool)

    options = [correct, *distractors]
    random.shuffle(options)

    taal_adj, _ = _taal_labels(knoop_id)

    return {
        "id": f"ITEM-{knoop_id}-{item_nr:03d}",
        "knoop_ids": [knoop_id],
        "type": "herkenning",
        "richting": "receptief",
        "moeilijkheid_initieel": round(random.uniform(*HERKENNING_B_RANGE), 2),
        "discriminatie_initieel": 1.0,
        "verwachte_tijd_sec": HERKENNING_TIME_SEC,
        "stimulus": {
            "instruction": f"Lees het {taal_adj} woord en kies de juiste vertaling.",
            "lemma": first_word,
            "options": options,
        },
        "antwoord": correct,
        "feedback": f"{first_word} = {correct}.",
        "bron": "llm_gegenereerd",
    }


def generate_productie_item(node: dict, item_nr: int) -> dict:
    """Text-based productie: given NL translation, type the lemma."""
    knoop_id = node["id"]
    lemma, translation = parse_titel(node["titel_nl"])
    first_word = extract_first_word(lemma)
    correct = extract_short_translation(translation)

    taal_adj, _ = _taal_labels(knoop_id)

    return {
        "id": f"ITEM-{knoop_id}-{item_nr:03d}",
        "knoop_ids": [knoop_id],
        "type": "productie",
        "richting": "productief",
        "moeilijkheid_initieel": round(random.uniform(*PRODUCTIE_B_RANGE), 2),
        "discriminatie_initieel": 1.0,
        "verwachte_tijd_sec": PRODUCTIE_TIME_SEC,
        "stimulus": {
            "instruction": f"Typ het {taal_adj} woord voor deze vertaling.",
            "translation": correct,
        },
        "antwoord": first_word,
        "feedback": f"Het {taal_adj} woord is '{first_word}' ({correct}).",
        "bron": "llm_gegenereerd",
    }


def enrich_file(json_path: Path) -> tuple[int, int, int]:
    """Add text herkenning/productie items to every V-node in *json_path*.

    Returns ``(nodes_updated, herkenning_added, productie_added)``.
    """
    data = load_vocab_json(json_path)
    v_nodes = [k for k in data["knopen"] if k["type"] == "V"]

    if not v_nodes:
        return 0, 0, 0

    # Build the distractor pool from every V-node's translation in the file.
    translation_pool = build_translation_pool(v_nodes)

    nodes_updated = 0
    herk_added = 0
    prod_added = 0

    for node in v_nodes:
        if "items" not in node:
            node["items"] = []

        existing_types = {i["type"] for i in node["items"]}
        added_here = 0

        if "herkenning" not in existing_types:
            nr = next_item_nr(node)
            node["items"].append(generate_herkenning_item(node, translation_pool, nr))
            herk_added += 1
            added_here += 1

        if "productie" not in existing_types:
            nr = next_item_nr(node)
            node["items"].append(generate_productie_item(node, nr))
            prod_added += 1
            added_here += 1

        if added_here > 0:
            nodes_updated += 1

    # Validate the resulting JSON against the Pydantic model before writing.
    from gymnasium_classica.models.graph import GraphData

    GraphData(**data)

    save_vocab_json(json_path, data)
    return nodes_updated, herk_added, prod_added


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Enrich V-nodes in the vocabulaire graph files with text-based "
            "herkenning/productie items (F1-19)."
        ),
    )
    parser.add_argument(
        "--graph-dir",
        type=Path,
        default=_PROJECT_ROOT / "data" / "graph",
        help="Path to graph JSON directory (default: data/graph).",
    )
    args = parser.parse_args(argv)

    # Seed once, before any random operation, for a deterministic output.
    random.seed(42)

    vocab_files = sorted(args.graph_dir.glob("*vocabulaire*.json"))
    if not vocab_files:
        print("ERROR: No vocabulaire JSON files found.", file=sys.stderr)
        return 1

    total_nodes = 0
    total_herk = 0
    total_prod = 0

    for vf in vocab_files:
        print(f"Processing {vf.name} ...")
        nodes_updated, herk_added, prod_added = enrich_file(vf)
        print(
            f"  {nodes_updated} knopen bijgewerkt, "
            f"{herk_added} herkenning + {prod_added} productie toegevoegd"
        )
        total_nodes += nodes_updated
        total_herk += herk_added
        total_prod += prod_added

    print("\n=== Samenvatting ===")
    print(f"Knopen bijgewerkt: {total_nodes}")
    print(f"Herkenning items:  {total_herk}")
    print(f"Productie items:   {total_prod}")
    print(f"Totaal toegevoegd: {total_herk + total_prod}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
