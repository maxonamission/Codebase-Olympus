#!/usr/bin/env python3
"""Generate luister-oefening items for vocabulary nodes with audio_ref.

Produces two item types:
- luister_herkenning: hear audio, pick the correct translation (receptief)
- luister_productie: hear audio, type the word in the original language (productief)

Items are added to the `items` list on existing V-nodes in the graph JSON files.

Usage:
    python scripts/generate_luister_items.py --type herkenning
    python scripts/generate_luister_items.py --type productie
    python scripts/generate_luister_items.py --type both
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _SCRIPT_DIR.parent

# Seed for reproducible distractor selection
random.seed(42)

# ---------------------------------------------------------------------------
# Lemma / translation extraction from titel_nl
# ---------------------------------------------------------------------------


def parse_titel(titel_nl: str) -> tuple[str, str]:
    """Split titel_nl into (lemma, translation).

    Format: "lemma — translation"
    Example: "sum, esse — zijn" -> ("sum, esse", "zijn")
    """
    if " — " in titel_nl:
        parts = titel_nl.split(" — ", maxsplit=1)
        return parts[0].strip(), parts[1].strip()
    return titel_nl.strip(), ""


def extract_first_word(lemma: str) -> str:
    """Extract the citation form (first word) from a lemma string.

    "sum, esse" -> "sum"
    "εἰμί, εἶναι" -> "εἰμί"
    "in (+acc/abl)" -> "in"
    "καί (part.)" -> "καί"
    """
    # Take everything before first comma or opening paren
    word = lemma.split(",")[0].split("(")[0].strip()
    # If multi-word, take first word
    return word.split()[0] if word else lemma


def extract_short_translation(translation: str) -> str:
    """Extract a short translation suitable for multiple choice.

    "in, naar; in, op" -> "in, naar"
    "die, dat; wie, wat" -> "die, dat"
    "zijn" -> "zijn"
    """
    # Take first option before semicolon
    return translation.split(";")[0].strip()


# ---------------------------------------------------------------------------
# Load and filter nodes
# ---------------------------------------------------------------------------


def load_vocab_json(json_path: Path) -> dict:
    """Load a graph JSON file."""
    with open(json_path, encoding="utf-8") as f:
        return json.load(f)


def save_vocab_json(json_path: Path, data: dict) -> None:
    """Save a graph JSON file with consistent formatting."""
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def get_vocab_with_audio(data: dict) -> list[dict]:
    """Return V-nodes that have audio_ref set."""
    return [k for k in data["knopen"] if k["type"] == "V" and k.get("audio_ref")]


# ---------------------------------------------------------------------------
# Distractor generation
# ---------------------------------------------------------------------------


def build_translation_pool(nodes: list[dict]) -> list[str]:
    """Build a pool of short translations for distractor generation."""
    pool = []
    for node in nodes:
        _, translation = parse_titel(node["titel_nl"])
        short = extract_short_translation(translation)
        if short:
            pool.append(short)
    return pool


def pick_distractors(correct: str, pool: list[str], n: int = 3) -> list[str]:
    """Pick n distractors from pool that differ from the correct answer."""
    candidates = [t for t in pool if t != correct]
    if len(candidates) < n:
        return candidates
    return random.sample(candidates, n)


# ---------------------------------------------------------------------------
# Item ID management
# ---------------------------------------------------------------------------


def next_item_nr(node: dict) -> int:
    """Determine the next item number for a node."""
    existing = node.get("items", [])
    if not existing:
        return 1
    max_nr = 0
    for item in existing:
        # Parse NR from ITEM-{KNOOP_ID}-{NR}
        parts = item["id"].rsplit("-", 1)
        if len(parts) == 2:
            try:
                max_nr = max(max_nr, int(parts[1]))
            except ValueError:
                pass
    return max_nr + 1


# ---------------------------------------------------------------------------
# Item generation: luister_herkenning
# ---------------------------------------------------------------------------


def generate_herkenning_item(node: dict, translation_pool: list[str], item_nr: int) -> dict:
    """Generate a luister_herkenning item for a V-node.

    Stimulus: listen to audio, choose the correct translation from 4 options.
    """
    knoop_id = node["id"]
    lemma, translation = parse_titel(node["titel_nl"])
    first_word = extract_first_word(lemma)
    correct = extract_short_translation(translation)
    distractors = pick_distractors(correct, translation_pool)

    options = [correct] + distractors
    random.shuffle(options)

    taal_label = "Latijnse" if knoop_id.startswith("LAT") else "Griekse"

    return {
        "id": f"ITEM-{knoop_id}-{item_nr:03d}",
        "knoop_ids": [knoop_id],
        "type": "luister_herkenning",
        "richting": "receptief",
        "moeilijkheid_initieel": round(random.uniform(-1.0, 0.0), 2),
        "discriminatie_initieel": 1.0,
        "verwachte_tijd_sec": 15,
        "stimulus": {
            "instruction": f"Luister naar het {taal_label} woord en kies de juiste vertaling.",
            "audio_ref": node["audio_ref"],
            "options": options,
        },
        "antwoord": correct,
        "feedback": f"{first_word} = {correct}.",
        "bron": "llm_gegenereerd",
        "audio_ref": node["audio_ref"],
    }


# ---------------------------------------------------------------------------
# Item generation: luister_productie
# ---------------------------------------------------------------------------


def generate_productie_item(node: dict, item_nr: int) -> dict:
    """Generate a luister_productie item for a V-node.

    Stimulus: listen to audio, type the word you hear in the original language.
    """
    knoop_id = node["id"]
    lemma, translation = parse_titel(node["titel_nl"])
    first_word = extract_first_word(lemma)
    correct = extract_short_translation(translation)

    taal_label = "Latijnse" if knoop_id.startswith("LAT") else "Griekse"
    taal_naam = "Latijn" if knoop_id.startswith("LAT") else "Grieks"

    return {
        "id": f"ITEM-{knoop_id}-{item_nr:03d}",
        "knoop_ids": [knoop_id],
        "type": "luister_productie",
        "richting": "productief",
        "moeilijkheid_initieel": round(random.uniform(0.0, 1.5), 2),
        "discriminatie_initieel": 1.0,
        "verwachte_tijd_sec": 25,
        "stimulus": {
            "instruction": f"Luister naar het {taal_label} woord en typ het in het {taal_naam}.",
            "audio_ref": node["audio_ref"],
            "hint": correct,
        },
        "antwoord": first_word,
        "feedback": f"Het woord is '{first_word}' ({correct}).",
        "bron": "llm_gegenereerd",
        "audio_ref": node["audio_ref"],
    }


# ---------------------------------------------------------------------------
# Main generation loop
# ---------------------------------------------------------------------------


def generate_items_for_file(json_path: Path, item_type: str) -> tuple[int, int]:
    """Generate items for all V-nodes with audio_ref in a JSON file.

    Args:
        json_path: Path to graph JSON file.
        item_type: "herkenning", "productie", or "both".

    Returns:
        (nodes_updated, items_added)
    """
    data = load_vocab_json(json_path)
    nodes = get_vocab_with_audio(data)

    if not nodes:
        return 0, 0

    translation_pool = build_translation_pool(nodes)

    nodes_updated = 0
    items_added = 0

    # Build a lookup for fast access
    node_map = {k["id"]: k for k in data["knopen"]}

    for node in nodes:
        knoop_id = node["id"]
        target = node_map[knoop_id]
        if "items" not in target:
            target["items"] = []

        # Check what types already exist
        existing_types = {i["type"] for i in target["items"]}
        added_here = 0

        if item_type in ("herkenning", "both"):
            if "luister_herkenning" not in existing_types:
                nr = next_item_nr(target)
                item = generate_herkenning_item(node, translation_pool, nr)
                target["items"].append(item)
                added_here += 1

        if item_type in ("productie", "both"):
            if "luister_productie" not in existing_types:
                nr = next_item_nr(target)
                item = generate_productie_item(node, nr)
                target["items"].append(item)
                added_here += 1

        if added_here > 0:
            nodes_updated += 1
            items_added += added_here

    save_vocab_json(json_path, data)
    return nodes_updated, items_added


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate luister-oefening items for V-nodes with audio_ref.",
    )
    parser.add_argument(
        "--type",
        choices=["herkenning", "productie", "both"],
        required=True,
        help="Which item type(s) to generate",
    )
    parser.add_argument(
        "--graph-dir",
        type=Path,
        default=_PROJECT_ROOT / "data" / "graph",
        help="Path to graph JSON directory (default: data/graph)",
    )
    args = parser.parse_args(argv)

    vocab_files = sorted(args.graph_dir.glob("*vocabulaire*.json"))
    if not vocab_files:
        print("ERROR: No vocabulaire JSON files found.", file=sys.stderr)
        return 1

    total_nodes = 0
    total_items = 0

    for vf in vocab_files:
        print(f"Processing {vf.name} ...")
        nodes_updated, items_added = generate_items_for_file(vf, args.type)
        print(f"  {nodes_updated} nodes updated, {items_added} items added")
        total_nodes += nodes_updated
        total_items += items_added

    print("\n=== Summary ===")
    print(f"Type:          {args.type}")
    print(f"Nodes updated: {total_nodes}")
    print(f"Items added:   {total_items}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
