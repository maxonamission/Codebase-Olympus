#!/usr/bin/env python3
"""E3-12 supplementary items: 5 GRC-G-SYNT-*-FUNCTIE nodes.

Deze nodes bleven over na E3-01..E3-11 zonder items. Deze story (E3-12)
is de validatie-sluitsteen en vult de laatste gaten.

Target: data/graph/grc_grammatica_leerjaar1.json
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from gymnasium_classica.models.graph import Item


def define_items() -> dict[str, list[dict]]:
    items: dict[str, list[dict]] = {}

    items["GRC-G-SYNT-NOM-FUNCTIE"] = [
        {
            "id": "ITEM-GRC-G-SYNT-NOM-FUNCTIE-001",
            "node_ids": ["GRC-G-SYNT-NOM-FUNCTIE"],
            "type": "herkenning",
            "direction": "receptief",
            "difficulty_initial": -0.5,
            "discrimination_initial": 1.0,
            "expected_time_sec": 12,
            "stimulus": "Welke naamval gebruik je in het Grieks voor het onderwerp van een zin?",
            "answer": "nominativus",
            "feedback": "De nominativus is de naamval van het onderwerp en van het naamwoordelijk deel van het gezegde.",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-SYNT-NOM-FUNCTIE-002",
            "node_ids": ["GRC-G-SYNT-NOM-FUNCTIE"],
            "type": "contextueel",
            "direction": "receptief",
            "difficulty_initial": 0.1,
            "discrimination_initial": 1.0,
            "expected_time_sec": 25,
            "stimulus": "Welke functie heeft ὁ ἄνθρωπος in: ὁ ἄνθρωπος τρέχει.",
            "answer": "onderwerp",
            "feedback": "ὁ ἄνθρωπος staat in de nominativus en is het onderwerp van τρέχει (loopt).",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-SYNT-NOM-FUNCTIE-003",
            "node_ids": ["GRC-G-SYNT-NOM-FUNCTIE"],
            "type": "contextueel",
            "direction": "receptief",
            "difficulty_initial": 0.3,
            "discrimination_initial": 1.2,
            "expected_time_sec": 30,
            "stimulus": "Welke functie heeft σοφός in: ὁ διδάσκαλος σοφός ἐστιν.",
            "answer": ["naamwoordelijk deel van het gezegde", "predicaatsnomen"],
            "feedback": "σοφός is nominativus en vormt met ἐστίν het gezegde: 'de leraar is wijs'.",
            "source": "handmatig",
        },
    ]

    items["GRC-G-SYNT-GEN-FUNCTIE"] = [
        {
            "id": "ITEM-GRC-G-SYNT-GEN-FUNCTIE-001",
            "node_ids": ["GRC-G-SYNT-GEN-FUNCTIE"],
            "type": "herkenning",
            "direction": "receptief",
            "difficulty_initial": -0.3,
            "discrimination_initial": 1.0,
            "expected_time_sec": 12,
            "stimulus": "Welke naamval drukt in het Grieks bezit uit?",
            "answer": "genitivus",
            "feedback": "De genitivus is de naamval van bezit, partitief, vergelijking en tijd — en speelt een hoofdrol in de genitivus absolutus.",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-SYNT-GEN-FUNCTIE-002",
            "node_ids": ["GRC-G-SYNT-GEN-FUNCTIE"],
            "type": "contextueel",
            "direction": "receptief",
            "difficulty_initial": 0.3,
            "discrimination_initial": 1.0,
            "expected_time_sec": 30,
            "stimulus": "Welke functie heeft τοῦ φίλου in: ὁ οἶκος τοῦ φίλου μέγας ἐστίν.",
            "answer": ["bezit", "genitivus van bezit"],
            "feedback": "τοῦ φίλου is genitivus van bezit: 'het huis van de vriend is groot'.",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-SYNT-GEN-FUNCTIE-003",
            "node_ids": ["GRC-G-SYNT-GEN-FUNCTIE"],
            "type": "contextueel",
            "direction": "receptief",
            "difficulty_initial": 0.6,
            "discrimination_initial": 1.2,
            "expected_time_sec": 35,
            "stimulus": "Welke functie heeft τῶν Ἑλλήνων in: πολλοὶ τῶν Ἑλλήνων ἦλθον.",
            "answer": ["partitief", "genitivus partitivus"],
            "feedback": "τῶν Ἑλλήνων is genitivus partitivus: 'velen van de Grieken kwamen'. Drukt het geheel uit waarvan een deel genomen wordt.",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-SYNT-GEN-FUNCTIE-004",
            "node_ids": ["GRC-G-SYNT-GEN-FUNCTIE"],
            "type": "analyse",
            "direction": "receptief",
            "difficulty_initial": 0.7,
            "discriminatie_initueel": 1.2,
            "discrimination_initial": 1.2,
            "expected_time_sec": 30,
            "stimulus": "Wat is een genitivus absolutus in het Grieks?",
            "answer": [
                "een los zinsdeel van genitivus + participium",
                "een bijzin-vervanger met participium en substantief in de genitivus",
            ],
            "feedback": "De genitivus absolutus is een los bijvoeglijk zinsdeel, bestaand uit een substantief en een participium beide in de genitivus, zonder grammaticale band met de hoofdzin.",
            "source": "handmatig",
        },
    ]

    items["GRC-G-SYNT-DAT-FUNCTIE"] = [
        {
            "id": "ITEM-GRC-G-SYNT-DAT-FUNCTIE-001",
            "node_ids": ["GRC-G-SYNT-DAT-FUNCTIE"],
            "type": "herkenning",
            "direction": "receptief",
            "difficulty_initial": -0.3,
            "discrimination_initial": 1.0,
            "expected_time_sec": 12,
            "stimulus": "Welke naamval gebruik je in het Grieks voor het meewerkend voorwerp?",
            "answer": "dativus",
            "feedback": "De dativus is de naamval van het meewerkend voorwerp, middel, wijze, tijd en van de bezitter bij εἶναι.",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-SYNT-DAT-FUNCTIE-002",
            "node_ids": ["GRC-G-SYNT-DAT-FUNCTIE"],
            "type": "contextueel",
            "direction": "receptief",
            "difficulty_initial": 0.3,
            "discrimination_initial": 1.0,
            "expected_time_sec": 30,
            "stimulus": "Welke functie heeft τῷ πατρί in: τῷ πατρὶ βιβλίον δίδωμι.",
            "answer": "meewerkend voorwerp",
            "feedback": "τῷ πατρί is dativus en meewerkend voorwerp: 'ik geef een boek aan de vader'.",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-SYNT-DAT-FUNCTIE-003",
            "node_ids": ["GRC-G-SYNT-DAT-FUNCTIE"],
            "type": "contextueel",
            "direction": "receptief",
            "difficulty_initial": 0.5,
            "discrimination_initial": 1.2,
            "expected_time_sec": 35,
            "stimulus": "Welke functie heeft ξίφει in: οἱ στρατιῶται ξίφει μάχονται.",
            "answer": ["middel", "dativus van middel", "instrumentalis"],
            "feedback": "ξίφει is dativus van middel: 'de soldaten vechten met het zwaard'.",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-SYNT-DAT-FUNCTIE-004",
            "node_ids": ["GRC-G-SYNT-DAT-FUNCTIE"],
            "type": "contextueel",
            "direction": "receptief",
            "difficulty_initial": 0.6,
            "discrimination_initial": 1.2,
            "expected_time_sec": 35,
            "stimulus": "Welke functie heeft τῷ παιδί in: τῷ παιδὶ βιβλίον ἐστίν.",
            "answer": ["bezitter", "bezitter bij εἶναι", "dativus possessivus"],
            "feedback": "τῷ παιδί is dativus possessivus bij ἐστίν: letterlijk 'aan het kind is een boek', dus 'het kind heeft een boek'.",
            "source": "handmatig",
        },
    ]

    items["GRC-G-SYNT-ACC-FUNCTIE"] = [
        {
            "id": "ITEM-GRC-G-SYNT-ACC-FUNCTIE-001",
            "node_ids": ["GRC-G-SYNT-ACC-FUNCTIE"],
            "type": "herkenning",
            "direction": "receptief",
            "difficulty_initial": -0.3,
            "discrimination_initial": 1.0,
            "expected_time_sec": 12,
            "stimulus": "Welke naamval gebruik je in het Grieks voor het lijdend voorwerp?",
            "answer": "accusativus",
            "feedback": "De accusativus is de naamval van het lijdend voorwerp, direction, tijdsduur en betrekking (respectus).",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-SYNT-ACC-FUNCTIE-002",
            "node_ids": ["GRC-G-SYNT-ACC-FUNCTIE"],
            "type": "contextueel",
            "direction": "receptief",
            "difficulty_initial": 0.2,
            "discrimination_initial": 1.0,
            "expected_time_sec": 30,
            "stimulus": "Welke functie heeft τὸν λόγον in: ὁ διδάσκαλος τὸν λόγον λέγει.",
            "answer": "lijdend voorwerp",
            "feedback": "τὸν λόγον is accusativus en lijdend voorwerp: 'de leraar zegt het woord'.",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-SYNT-ACC-FUNCTIE-003",
            "node_ids": ["GRC-G-SYNT-ACC-FUNCTIE"],
            "type": "contextueel",
            "direction": "receptief",
            "difficulty_initial": 0.5,
            "discrimination_initial": 1.0,
            "expected_time_sec": 30,
            "stimulus": "Welke functie heeft τρεῖς ἡμέρας in: τρεῖς ἡμέρας ἐμένομεν.",
            "answer": ["tijdsduur", "accusativus van tijdsduur"],
            "feedback": "τρεῖς ἡμέρας is accusativus van tijdsduur: 'drie dagen lang wachtten wij'.",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-SYNT-ACC-FUNCTIE-004",
            "node_ids": ["GRC-G-SYNT-ACC-FUNCTIE"],
            "type": "contextueel",
            "direction": "receptief",
            "difficulty_initial": 0.7,
            "discrimination_initial": 1.2,
            "expected_time_sec": 35,
            "stimulus": "Welke functie heeft τοὺς πόδας in: κάμνει τοὺς πόδας.",
            "answer": ["betrekking", "accusativus van respectus", "respectus"],
            "feedback": "τοὺς πόδας is accusativus van betrekking (respectus): 'hij heeft pijn aan zijn voeten' — de acc. preciseert waarin.",
            "source": "handmatig",
        },
    ]

    items["GRC-G-SYNT-VOC-FUNCTIE"] = [
        {
            "id": "ITEM-GRC-G-SYNT-VOC-FUNCTIE-001",
            "node_ids": ["GRC-G-SYNT-VOC-FUNCTIE"],
            "type": "herkenning",
            "direction": "receptief",
            "difficulty_initial": -0.4,
            "discrimination_initial": 1.0,
            "expected_time_sec": 12,
            "stimulus": "Wat is de functie van de vocativus in het Grieks?",
            "answer": ["aanspreekvorm", "iemand direct aanspreken"],
            "feedback": "De vocativus is de aanspreekvorm — gebruikt om iemand direct toe te spreken, vaak voorafgegaan door ὦ.",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-SYNT-VOC-FUNCTIE-002",
            "node_ids": ["GRC-G-SYNT-VOC-FUNCTIE"],
            "type": "contextueel",
            "direction": "receptief",
            "difficulty_initial": 0.2,
            "discrimination_initial": 1.0,
            "expected_time_sec": 25,
            "stimulus": "Wie wordt aangesproken in: ὦ παῖ, ἄκουε!",
            "answer": ["παῖ", "het kind", "de jongen"],
            "feedback": "παῖ is vocativus: 'O kind, luister!' De partikel ὦ maakt de aanspreking nog duidelijker.",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-SYNT-VOC-FUNCTIE-003",
            "node_ids": ["GRC-G-SYNT-VOC-FUNCTIE"],
            "type": "herkenning",
            "direction": "receptief",
            "difficulty_initial": 0.3,
            "discrimination_initial": 1.0,
            "expected_time_sec": 20,
            "stimulus": "In welke declinatiesubgroep wijkt de vocativus enkelvoud af van de nominativus?",
            "answer": ["2e declinatie masculinum op -ος", "2e declinatie op -ος"],
            "feedback": "De vocativus enkelvoud wijkt af bij de 2e declinatie -ος → -ε: ὁ λόγος → ὦ λόγε. In de meeste andere gevallen valt voc. samen met nom.",
            "source": "handmatig",
        },
    ]

    return items


def validate_items(items_by_node: dict[str, list[dict]]) -> None:
    for item_list in items_by_node.values():
        for item_dict in item_list:
            # Remove accidental typo field if present
            item_dict.pop("discriminatie_initueel", None)
            Item(**item_dict)
    print(f"All {sum(len(v) for v in items_by_node.values())} items validated.")


def add_items_to_json(json_path: Path, items_by_node: dict[str, list[dict]]) -> int:
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    added = 0
    for node in data["nodes"]:
        if node["id"] in items_by_node:
            existing_ids = {item["id"] for item in node.get("items", [])}
            new_items = [
                item for item in items_by_node[node["id"]] if item["id"] not in existing_ids
            ]
            node.setdefault("items", []).extend(new_items)
            added += len(new_items)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    return added


def print_summary(items_by_node: dict[str, list[dict]]) -> None:
    total = sum(len(v) for v in items_by_node.values())
    types = Counter(i["type"] for lst in items_by_node.values() for i in lst)

    print("\n=== E3-12 Summary ===")
    print(f"Knopen: {len(items_by_node)}")
    print(f"Total items: {total}")
    print("\nOefentype-verdeling:")
    for t, c in types.most_common():
        print(f"  {t}: {c}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    items_by_node = define_items()
    validate_items(items_by_node)
    print_summary(items_by_node)

    if args.dry_run:
        print("\nDry-run: geen wijzigingen geschreven.")
        return

    path = Path(__file__).parent.parent / "data" / "graph" / "grc_grammatica_leerjaar1.json"
    added = add_items_to_json(path, items_by_node)
    print(f"\nAdded {added} items to {path.name}")


if __name__ == "__main__":
    main()
