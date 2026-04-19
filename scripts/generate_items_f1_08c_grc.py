#!/usr/bin/env python3
"""F1-08c — herkenningsitems voor het Griekse dagelijks leven (10 knopen).

De Griekse helft van SHA-C-POL-*: GRIEK, POLIS, AGORA, ACROP, DEMOC,
GYMNA, SYMPO, THEAT, OLYMP (Olympische Spelen), OIKOS.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from gymnasium_classica.models.graph import Item

OUTPUT = Path(__file__).parent.parent / "data" / "graph" / "sha_cultuur_leerjaar1.json"

BATCH: list[tuple[str, str, list[str], int, str]] = [
    (
        "POL-GRIEK",
        "Welke sociale eenheid staat centraal in het Griekse leven?",
        ["Het koninkrijk", "De polis", "De familia", "Het legioen"],
        1,
        "In de Griekse wereld is de polis — de stadstaat — de kern van politiek, religie en samenleving.",
    ),
    (
        "POL-POLIS",
        "Wat is een polis?",
        [
            "Een stadstaat met eigen bestuur en wetten",
            "Een tempelcomplex",
            "Een militair kamp",
            "Een Romeinse kolonie",
        ],
        0,
        "De polis is een onafhankelijke stadstaat met eigen wetten, bestuur en identiteit.",
    ),
    (
        "POL-AGORA",
        "Wat was de hoofdfunctie van de agora?",
        [
            "Begraafplaats",
            "Uitsluitend een militaire basis",
            "Markt- en ontmoetingsplaats en politiek centrum",
            "Een heilig bos",
        ],
        2,
        "De agora was het centrale plein: markt, ontmoetingsplaats en politiek centrum (volksvergadering).",
    ),
    (
        "POL-ACROP",
        "Welke tempel op de Atheense Acropolis is gewijd aan Athena?",
        ["Het Erechtheion", "Het Parthenon", "De Tholos", "Het Hephaisteion"],
        1,
        "Het Parthenon op de Acropolis van Athene is gewijd aan Athena Parthenos.",
    ),
    (
        "POL-DEMOC",
        "Door wie is de Atheense democratie grotendeels ingevoerd?",
        ["Solon", "Perikles", "Kleisthenes", "Themistokles"],
        2,
        "Kleisthenes voerde rond 508 v.Chr. de democratische hervormingen door die de directe democratie in Athene vestigden.",
    ),
    (
        "POL-GYMNA",
        "Wat deed men vooral in het Griekse gymnasium?",
        [
            "Handel drijven",
            "Lichaamstraining én intellectuele vorming",
            "Strafprocessen voeren",
            "Begrafenissen voorbereiden",
        ],
        1,
        "Het gymnasium was trainingsplaats voor atletiek én voor intellectuele en filosofische vorming.",
    ),
    (
        "POL-SYMPO",
        "Wie namen typisch deel aan een symposion?",
        ["Mannelijke burgers", "Alleen slaven", "Uitsluitend priesters", "Alleen buitenlanders"],
        0,
        "Een symposion was een drinkgelag voor mannelijke burgers, met muziek, poëzie en filosofisch gesprek.",
    ),
    (
        "POL-THEAT",
        "Ter ere van welke god werd het Griekse theater georganiseerd?",
        ["Apollo", "Zeus", "Dionysos", "Hermes"],
        2,
        "De tragedies en komedies werden opgevoerd tijdens de feesten voor Dionysos.",
    ),
    (
        "POL-OLYMP",
        "Waar en om de hoeveel jaar werden de Olympische Spelen gehouden?",
        [
            "Athene, jaarlijks",
            "Olympia, elke vier jaar",
            "Delphi, elke vier jaar",
            "Sparta, elke acht jaar",
        ],
        1,
        "De Olympische Spelen vonden elke vier jaar plaats in Olympia, ter ere van Zeus, met een heilige wapenstilstand.",
    ),
    (
        "POL-OIKOS",
        "Wat is de oikos?",
        [
            "Een tempel",
            "Een Griekse marktplaats",
            "Het Griekse huishouden als economische en sociale eenheid",
            "De volksvergadering",
        ],
        2,
        "De oikos is het huishouden onder de kyrios — de economische en sociale basiseenheid van de Griekse samenleving.",
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
    print(f"F1-08c grieks: {len(items)} knopen, {added} nieuwe items toegevoegd.")
    print(f"Output: {OUTPUT}")


if __name__ == "__main__":
    main()
