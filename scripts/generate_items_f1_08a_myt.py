#!/usr/bin/env python3
"""F1-08a — genereer herkenningsitems voor de 20 mythologie-knopen (SHA-C-MYT-*).

Elk item is een multiple-choice met 4 opties, type ``herkenning`` en richting
``receptief``. Stimulus is een dict met ``instruction`` + ``options``; het
juiste antwoord is de letterlijke optietekst. IRT-parameters zijn conservatief
gekozen voor kennis-niveau cultuurvragen (b ≈ -0.5, a = 1.0, ~20 sec).
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from gymnasium_classica.models.graph import Item

OUTPUT = Path(__file__).parent.parent / "data" / "graph" / "sha_cultuur_leerjaar1.json"

# (node_suffix, vraag, [optie_a, b, c, d], correcte_index, feedback)
BATCH: list[tuple[str, str, list[str], int, str]] = [
    (
        "MYT-INTRO",
        "Wat bedoelt men met 'klassieke mythologie'?",
        [
            "Wetenschappelijk onderzoek naar de natuur",
            "De verzameling Grieks-Romeinse verhalen over goden en helden",
            "Een systeem van wetten uit Rome",
            "Een stroming in de Griekse filosofie",
        ],
        1,
        "Mythologie is het geheel van overgeleverde Grieks-Romeinse verhalen over goden, helden en de oorsprong van de wereld.",
    ),
    (
        "MYT-SCHEP",
        "Welke godengeneratie ging volgens de scheppingsmythe vooraf aan de Olympische goden?",
        ["De Titanen", "De Giganten", "De halfgoden", "De Muzen"],
        0,
        "De Titanen heersten vóór de Olympiërs; na de Titanomachie namen Zeus en zijn broers en zussen de macht over.",
    ),
    (
        "MYT-OLYMP",
        "Hoeveel Olympische hoofdgoden telt men traditioneel?",
        ["Zes", "Negen", "Twaalf", "Zestien"],
        2,
        "Het klassieke pantheon op de Olympus bestaat uit twaalf hoofdgoden.",
    ),
    (
        "MYT-ZEUS",
        "Wat is de Latijnse naam van Zeus?",
        ["Mars", "Jupiter", "Neptunus", "Mercurius"],
        1,
        "Zeus heet in het Latijn Jupiter: oppergod, heerser van de hemel en de bliksem.",
    ),
    (
        "MYT-HERA",
        "Waarvan is Hera / Juno godin?",
        ["Jacht en maan", "Huwelijk en gezin", "Liefde en schoonheid", "Wijsheid"],
        1,
        "Hera / Juno is de godin van het huwelijk en het gezin, bekend om haar jaloezie op Zeus' minnaressen.",
    ),
    (
        "MYT-POSEID",
        "Over welk domein heerst Poseidon / Neptunus?",
        ["De onderwereld", "De zee", "De hemel", "De oogst"],
        1,
        "Poseidon / Neptunus is de god van de zee, aardbevingen en paarden.",
    ),
    (
        "MYT-ATHENA",
        "Waarvan is Athena / Minerva vooral godin?",
        [
            "Jacht en maan",
            "Liefde en schoonheid",
            "Wijsheid, strategie en handwerk",
            "Vuur en smeedkunst",
        ],
        2,
        "Athena / Minerva is de godin van wijsheid, strategisch oorlogvoeren en handwerk; zij beschermt Athene.",
    ),
    (
        "MYT-APOLLO",
        "Met welk orakel is Apollo vooral verbonden?",
        ["Dodona", "Olympia", "Delphi", "Eleusis"],
        2,
        "Apollo sprak via de Pythia in zijn orakel te Delphi.",
    ),
    (
        "MYT-ARTEM",
        "Wat is de familierelatie tussen Artemis en Apollo?",
        ["Moeder en zoon", "Echtgenoten", "Tweelingzus en -broer", "Nicht en neef"],
        2,
        "Artemis en Apollo zijn een tweeling, kinderen van Zeus en Leto.",
    ),
    (
        "MYT-APHROD",
        "Welke rol speelt Aphrodite / Venus in het Parisoordeel?",
        [
            "Zij veroordeelt Paris",
            "Zij belooft Paris de mooiste vrouw, Helena",
            "Zij geeft Paris macht over Azië",
            "Zij is afwezig",
        ],
        1,
        "Aphrodite wint het Parisoordeel door Paris de mooiste vrouw ter wereld (Helena) te beloven — de aanleiding voor de Trojaanse Oorlog.",
    ),
    (
        "MYT-HERMES",
        "Welke hoofdfunctie heeft Hermes / Mercurius?",
        [
            "Oorlogsgod",
            "Boodschapper van de goden en beschermer van reizigers",
            "Heerser van de onderwereld",
            "God van de oogst",
        ],
        1,
        "Hermes / Mercurius is de boodschapper van de goden en beschermt reizigers en handelaren.",
    ),
    (
        "MYT-ARES",
        "Wat is de Latijnse naam van Ares?",
        ["Mars", "Vulcanus", "Mercurius", "Jupiter"],
        0,
        "Ares heet in het Latijn Mars. Bij de Romeinen was hij populairder dan Ares bij de Grieken — Mars geldt als stamvader van Romulus en Remus.",
    ),
    (
        "MYT-HEPHAI",
        "Waarvan is Hephaistos / Vulcanus god?",
        ["Medicijnen", "Vuur en smeedkunst", "Wijn", "Scheepvaart"],
        1,
        "Hephaistos / Vulcanus is de god van het vuur en de smeedkunst; hij smeedt de wapens van de goden.",
    ),
    (
        "MYT-DEMETR",
        "Welke mythe verklaart volgens de Grieken het verloop van de seizoenen?",
        [
            "Herakles en de Nemeïsche leeuw",
            "Demeter en de roof van Persephone",
            "Apollo en Daphne",
            "Orpheus en Eurydice",
        ],
        1,
        "Demeters rouw om haar dochter Persephone (geroofd door Hades) verklaart de winter; haar terugkeer brengt de lente.",
    ),
    (
        "MYT-HADES",
        "Over welk domein heerst Hades / Pluto?",
        ["De hemel", "De zee", "De onderwereld", "De bergen"],
        2,
        "Hades / Pluto is heerser van de onderwereld. Als broer van Zeus hoort hij niet bij de twaalf Olympiërs.",
    ),
    (
        "MYT-HELD",
        "Wat is kenmerkend voor een Griekse held?",
        [
            "Hij is volledig sterfelijk en gewoon",
            "Hij is halfgod of sterveling met goddelijke hulp",
            "Hij is priester",
            "Hij is altijd koning",
        ],
        1,
        "Griekse helden zijn vaak halfgoden of stervelingen die met goddelijke bijstand buitengewone daden verrichten.",
    ),
    (
        "MYT-HERAKL",
        "Waarvoor is Herakles / Hercules vooral beroemd?",
        [
            "De twaalf werken",
            "Het stichten van Rome",
            "Het bedwingen van Troje",
            "Het doden van de Minotaurus",
        ],
        0,
        "Herakles / Hercules voerde de twaalf werken uit als boetedoening, opgelegd door Eurystheus.",
    ),
    (
        "MYT-THESEU",
        "Welk monster doodde Theseus in het labyrint?",
        ["De Cycloop", "De Minotaurus", "Medusa", "De Hydra"],
        1,
        "Theseus doodde de Minotaurus in het labyrint van Kreta, met de hulp van Ariadnes draad.",
    ),
    (
        "MYT-TROJE",
        "Wat was volgens de mythe de directe aanleiding voor de Trojaanse Oorlog?",
        [
            "Een hongersnood in Griekenland",
            "De ontvoering van Helena door Paris",
            "Een Perzische invasie",
            "Een aardbeving op Troje",
        ],
        1,
        "Paris ontvoerde Helena, de vrouw van Menelaos, uit Sparta. Dat bracht de Griekse vorsten ertoe tegen Troje ten strijde te trekken.",
    ),
    (
        "MYT-ODYSS",
        "Hoeveel jaar duurde Odysseus' thuisreis naar Ithaka volgens de Odyssee?",
        ["Drie jaar", "Zeven jaar", "Tien jaar", "Twintig jaar"],
        2,
        "De Odyssee beschrijft Odysseus' tienjarige thuisreis na de val van Troje.",
    ),
]


def make_item(
    suffix: str, vraag: str, options: list[str], correct_idx: int, feedback: str
) -> dict:
    node_id = f"SHA-C-{suffix}"
    return {
        "id": f"ITEM-{node_id}-001",
        "knoop_ids": [node_id],
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
        Item(**item)  # validate via Pydantic
        items[f"SHA-C-{suffix}"] = [item]
    return items


def inject(json_path: Path, items_by_node: dict[str, list[dict]]) -> int:
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)
    added = 0
    missing = set(items_by_node.keys())
    for node in data["knopen"]:
        kid = node["id"]
        if kid in items_by_node:
            existing = {it["id"] for it in node.get("items", [])}
            new_items = [it for it in items_by_node[kid] if it["id"] not in existing]
            node.setdefault("items", []).extend(new_items)
            added += len(new_items)
            missing.discard(kid)
    if missing:
        raise SystemExit(f"Unknown node IDs: {sorted(missing)}")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return added


def main() -> None:
    items = build_items()
    added = inject(OUTPUT, items)
    print(f"F1-08a mythologie: {len(items)} knopen, {added} nieuwe items toegevoegd.")
    print(f"Output: {OUTPUT}")


if __name__ == "__main__":
    main()
