#!/usr/bin/env python3
"""F1-08d — herkenningsitems voor taal en schrift in de klassieke wereld.

Vijf SHA-C-LIT-* knopen: INTRO, GRALF, LTALF, INSCR, SCHRF.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from gymnasium_classica.models.graph import Item

OUTPUT = Path(__file__).parent.parent / "data" / "graph" / "sha_cultuur_leerjaar1.json"

BATCH: list[tuple[str, str, list[str], int, str]] = [
    (
        "LIT-INTRO",
        "Welk schriftsysteem ligt aan de basis van het moderne Europese schrift?",
        [
            "Het Chinese schrift",
            "Het Egyptische hiërogliefenschrift",
            "Het Griekse alfabet (via het Latijnse)",
            "Het spijkerschrift",
        ],
        2,
        "Het Griekse alfabet vormt, via het Latijnse, de basis van vrijwel alle moderne Europese schriften.",
    ),
    (
        "LIT-GRALF",
        "Welk schrift vormt de directe bron van het Griekse alfabet?",
        ["Lineair B", "Het Fenicische schrift", "Het Etruskische schrift", "Het Aramese schrift"],
        1,
        "De Grieken ontleenden rond 800 v.Chr. hun alfabet aan het Fenicische schrift en voegden klinkertekens toe.",
    ),
    (
        "LIT-LTALF",
        "Via welk volk is het Griekse alfabet bij de Romeinen terechtgekomen?",
        ["De Galliërs", "De Feniciërs", "De Etrusken", "De Karthagers"],
        2,
        "De Romeinen namen het alfabet over van de Etrusken, die het op hun beurt uit het Griekse schrift hadden.",
    ),
    (
        "LIT-INSCR",
        "Welke van de volgende is een voorbeeld van een inscriptie?",
        [
            "Een perkamenten wetboek",
            "Een grafsteen met tekst",
            "Een papyrusrol",
            "Een mondelinge overlevering",
        ],
        1,
        "Inscripties zijn teksten in duurzaam materiaal — steen, brons of keramiek — zoals grafstenen, wetten of eerbewijzen.",
    ),
    (
        "LIT-SCHRF",
        "Welk van deze materialen werd in de oudheid NIET gebruikt om op te schrijven?",
        ["Papyrus", "Wastafels", "Perkament", "Papier"],
        3,
        "Papier kwam pas na de oudheid in Europa in gebruik. In de klassieke wereld schreef men op papyrus, wastafels of perkament.",
    ),
]


def make_item(
    suffix: str, vraag: str, options: list[str], correct_idx: int, feedback: str
) -> dict:
    knoop_id = f"SHA-C-{suffix}"
    return {
        "id": f"ITEM-{knoop_id}-001",
        "knoop_ids": [knoop_id],
        "type": "herkenning",
        "richting": "receptief",
        "moeilijkheid_initieel": -0.5,
        "discriminatie_initieel": 1.0,
        "verwachte_tijd_sec": 20,
        "stimulus": {"instruction": vraag, "options": options},
        "antwoord": options[correct_idx],
        "feedback": feedback,
        "bron": "handmatig",
    }


def build_items() -> dict[str, list[dict]]:
    items: dict[str, list[dict]] = {}
    for suffix, vraag, options, correct_idx, feedback in BATCH:
        item = make_item(suffix, vraag, options, correct_idx, feedback)
        Item(**item)
        items[f"SHA-C-{suffix}"] = [item]
    return items


def inject(json_path: Path, items_by_knoop: dict[str, list[dict]]) -> int:
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)
    added = 0
    missing = set(items_by_knoop.keys())
    for knoop in data["knopen"]:
        kid = knoop["id"]
        if kid in items_by_knoop:
            existing = {it["id"] for it in knoop.get("items", [])}
            new_items = [it for it in items_by_knoop[kid] if it["id"] not in existing]
            knoop.setdefault("items", []).extend(new_items)
            added += len(new_items)
            missing.discard(kid)
    if missing:
        raise SystemExit(f"Unknown knoop IDs: {sorted(missing)}")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return added


def main() -> None:
    items = build_items()
    added = inject(OUTPUT, items)
    print(f"F1-08d taal/schrift: {len(items)} knopen, {added} nieuwe items toegevoegd.")
    print(f"Output: {OUTPUT}")


if __name__ == "__main__":
    main()
