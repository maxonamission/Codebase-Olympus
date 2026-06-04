#!/usr/bin/env python3
"""Generate exercise items for E3-06: GRC adjectieven.

Target: data/graph/grc_grammatica_leerjaar1.json
Scope:  8 nodes rondom adjectieven: ADJ-INTRO, ADJ-D12-3U, ADJ-D12-2U,
        ADJ-D3, ADJ-MEGAS, ADJ-VERBG, SYNT-ADJ-CONGR, SYNT-ADJ-ATTRIB.

Modelwoorden: ἀγαθός en καλός (α/ο-stam drie uitgangen), βάρβαρος (twee
uitgangen), σώφρων en ἀληθής (3e decl.), μέγας en πολύς (onregelmatig).
Congruentie (≥8 items) en attributief/praedicatief onderscheid (≥5 items)
zijn expliciete kernfoci.

Run:
    python scripts/generate_items_e3_06.py            # writes items to graph
    python scripts/generate_items_e3_06.py --dry-run  # only validate + print
"""

from __future__ import annotations

import argparse
import json
import sys
import unicodedata
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from gymnasium_classica.models.graph import Item


def nfc(value):
    if isinstance(value, str):
        return unicodedata.normalize("NFC", value)
    if isinstance(value, list):
        return [nfc(v) for v in value]
    return value


# ---------------------------------------------------------------------------
# MORF-nodes
# ---------------------------------------------------------------------------


def morf_items() -> dict[str, list[dict]]:
    """ADJ-INTRO (2) + D12-3U (3) + D12-2U (2) + D3 (3) + MEGAS (2) + VERBG (2) = 14 items."""
    items: dict[str, list[dict]] = {}

    items["GRC-G-MORF-ADJ-INTRO"] = [
        {
            "id": "ITEM-GRC-G-MORF-ADJ-INTRO-001",
            "node_ids": ["GRC-G-MORF-ADJ-INTRO"],
            "type": "herkenning",
            "direction": "receptief",
            "difficulty_initial": -0.5,
            "discrimination_initial": 1.0,
            "expected_time_sec": 12,
            "stimulus": "Volgens welke drie categorieën moet een Grieks adjectief met zijn substantief overeenstemmen?",
            "answer": [
                "genus, numerus en naamval",
                "geslacht, getal en naamval",
            ],
            "feedback": "Congruentie: adjectief en substantief delen genus, numerus én naamval. Zes vormen per adjectief (3 genera × 2 numeri) per naamval.",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-ADJ-INTRO-002",
            "node_ids": ["GRC-G-MORF-ADJ-INTRO"],
            "type": "herkenning",
            "direction": "receptief",
            "difficulty_initial": -0.2,
            "discrimination_initial": 1.1,
            "expected_time_sec": 15,
            "stimulus": "Welke twee grote adjectief-groepen kent het Grieks qua stamtype?",
            "answer": [
                "α/ο-stammen (1e/2e decl.) en medeklinkerstammen (3e decl.)",
                "α/ο-stam en medeklinkerstam",
            ],
            "feedback": "α/ο-stammen volgen 1e/2e decl. (ἀγαθός, -ή, -όν). Medeklinkerstammen volgen de 3e decl. (σώφρων, ἀληθής).",
            "source": "handmatig",
        },
    ]

    items["GRC-G-MORF-ADJ-D12-3U"] = [
        {
            "id": "ITEM-GRC-G-MORF-ADJ-D12-3U-001",
            "node_ids": ["GRC-G-MORF-ADJ-D12-3U"],
            "type": "herkenning",
            "direction": "receptief",
            "difficulty_initial": -0.1,
            "discrimination_initial": 1.1,
            "expected_time_sec": 15,
            "stimulus": "Welke declinaties volgen de drie vormen van ἀγαθός, -ή, -όν?",
            "answer": [
                "m./n. volgen de 2e declinatie, f. volgt de 1e declinatie",
                "m. 2e decl., f. 1e decl., n. 2e decl.",
            ],
            "feedback": "ἀγαθός (m.) en ἀγαθόν (n.) volgen de 2e decl. (ο-stam); ἀγαθή (f.) volgt de 1e decl. (η-stam).",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-ADJ-D12-3U-002",
            "node_ids": ["GRC-G-MORF-ADJ-D12-3U", "GRC-G-SYNT-ADJ-CONGR"],
            "type": "productie",
            "direction": "productief",
            "difficulty_initial": 0.5,
            "discrimination_initial": 1.3,
            "expected_time_sec": 25,
            "stimulus": "Geef de vorm van ἀγαθός die congrueert met τὴν χώραν.",
            "answer": "ἀγαθήν",
            "feedback": "τὴν χώραν is acc. sg. f. → ἀγαθήν (acc. sg. f.). De f. van ἀγαθός volgt de 1e decl. (α/η-stam).",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-ADJ-D12-3U-003",
            "node_ids": ["GRC-G-MORF-ADJ-D12-3U", "GRC-G-SYNT-ADJ-CONGR"],
            "type": "productie",
            "direction": "productief",
            "difficulty_initial": 0.5,
            "discrimination_initial": 1.3,
            "expected_time_sec": 25,
            "stimulus": "Geef de vorm van καλός die congrueert met τοῖς ἀνθρώποις.",
            "answer": "καλοῖς",
            "feedback": "τοῖς ἀνθρώποις is dat. pl. m. → καλοῖς (dat. pl. m., 2e decl.). α/ο-stam adj. volgt de 2e decl. voor m./n.",
            "source": "handmatig",
        },
    ]

    items["GRC-G-MORF-ADJ-D12-2U"] = [
        {
            "id": "ITEM-GRC-G-MORF-ADJ-D12-2U-001",
            "node_ids": ["GRC-G-MORF-ADJ-D12-2U"],
            "type": "herkenning",
            "direction": "receptief",
            "difficulty_initial": 0.1,
            "discrimination_initial": 1.2,
            "expected_time_sec": 15,
            "stimulus": "Wat kenmerkt een adjectief als βάρβαρος, -ον met 'twee uitgangen'?",
            "answer": [
                "m. en f. delen dezelfde vorm (2e decl.); n. heeft aparte vorm op -ον",
                "m./f. identiek, n. apart",
            ],
            "feedback": "Bij βάρβαρος, -ον gebruikt het adjectief de 2e decl. voor m. én f.: ἡ βάρβαρος γυνή. De n. heeft wel een aparte vorm (βάρβαρον).",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-ADJ-D12-2U-002",
            "node_ids": ["GRC-G-MORF-ADJ-D12-2U", "GRC-G-SYNT-ADJ-CONGR"],
            "type": "productie",
            "direction": "productief",
            "difficulty_initial": 0.5,
            "discrimination_initial": 1.3,
            "expected_time_sec": 25,
            "stimulus": "Geef de vorm van βάρβαρος die congrueert met ἡ γυνή.",
            "answer": "βάρβαρος",
            "feedback": "ἡ γυνή is nom. sg. f. → βάρβαρος. Bij 'twee uitgangen' deelt het f. de m.-vorm van de 2e decl., ongeacht het genus van het substantief.",
            "source": "handmatig",
        },
    ]

    items["GRC-G-MORF-ADJ-D3"] = [
        {
            "id": "ITEM-GRC-G-MORF-ADJ-D3-001",
            "node_ids": ["GRC-G-MORF-ADJ-D3"],
            "type": "herkenning",
            "direction": "receptief",
            "difficulty_initial": 0.3,
            "discrimination_initial": 1.2,
            "expected_time_sec": 15,
            "stimulus": "Volgens welke declinatie worden σώφρων en ἀληθής verbogen?",
            "answer": [
                "de 3e declinatie (medeklinkerstam)",
                "3e decl.",
            ],
            "feedback": "σώφρων (stam σωφρον-, ν-stam) en ἀληθής (stam ἀληθεσ-, σ-stam) volgen de 3e decl. m./f. identiek, n. apart.",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-ADJ-D3-002",
            "node_ids": ["GRC-G-MORF-ADJ-D3", "GRC-G-SYNT-ADJ-CONGR"],
            "type": "productie",
            "direction": "productief",
            "difficulty_initial": 0.7,
            "discrimination_initial": 1.3,
            "expected_time_sec": 30,
            "stimulus": "Geef de vorm van σώφρων die congrueert met τὸν ἄνθρωπον.",
            "answer": "σώφρονα",
            "feedback": "τὸν ἄνθρωπον is acc. sg. m. → σώφρονα (acc. sg. m., stam σωφρον- + -α). Let op: -α, niet -ον — de 3e decl. is anders dan de 2e.",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-ADJ-D3-003",
            "node_ids": ["GRC-G-MORF-ADJ-D3"],
            "type": "analyse",
            "direction": "receptief",
            "difficulty_initial": 0.6,
            "discrimination_initial": 1.3,
            "expected_time_sec": 25,
            "stimulus": "Wat is de nominativus sg. neutrum van σώφρων?",
            "answer": "σῶφρον",
            "feedback": "Nom. sg. n. = σῶφρον (kale stam σωφρον-, accent naar voren geschoven omdat neut. korter is dan de m.). De m. heeft klinkerverlenging: σώφρων.",
            "source": "handmatig",
        },
    ]

    items["GRC-G-MORF-ADJ-MEGAS"] = [
        {
            "id": "ITEM-GRC-G-MORF-ADJ-MEGAS-001",
            "node_ids": ["GRC-G-MORF-ADJ-MEGAS"],
            "type": "herkenning",
            "direction": "receptief",
            "difficulty_initial": 0.4,
            "discrimination_initial": 1.2,
            "expected_time_sec": 15,
            "stimulus": "Wat maakt μέγας en πολύς onregelmatig in hun verbuiging?",
            "answer": [
                "nom./acc. sg. m./n. komen van een korte stam (μεγα-/πολυ-), de rest van een uitgebreide stam (μεγαλ-/πολλ-)",
                "twee stammen door elkaar: korte én uitgebreide",
            ],
            "feedback": "μέγας en πολύς hebben twee stammen: μέγας/μέγα (m./n. nom./acc. sg.) maar μεγάλη, μεγάλου,... vanaf de rest. Πολύς/πολύ vs. πολλή, πολλοῦ.",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-ADJ-MEGAS-002",
            "node_ids": ["GRC-G-MORF-ADJ-MEGAS", "GRC-G-SYNT-ADJ-CONGR"],
            "type": "productie",
            "direction": "productief",
            "difficulty_initial": 0.7,
            "discrimination_initial": 1.3,
            "expected_time_sec": 30,
            "stimulus": "Geef de vorm van μέγας die congrueert met τῆς χώρας.",
            "answer": "μεγάλης",
            "feedback": "τῆς χώρας is gen. sg. f. → μεγάλης. Buiten nom./acc. sg. m./n. wordt de uitgebreide stam μεγαλ- gebruikt, hier met 1e-decl.-uitgang.",
            "source": "handmatig",
        },
    ]

    items["GRC-G-MORF-ADJ-VERBG"] = [
        {
            "id": "ITEM-GRC-G-MORF-ADJ-VERBG-001",
            "node_ids": ["GRC-G-MORF-ADJ-VERBG"],
            "type": "offline_schrijven",
            "direction": "productief",
            "difficulty_initial": 0.7,
            "discrimination_initial": 1.3,
            "expected_time_sec": 90,
            "stimulus": "Schrijf het volledige paradigma van ἀγαθός, -ή, -όν op (3 genera × 2 numeri × 5 naamvallen) en vergelijk met je grammaticaboek.",
            "answer": "m. volgens 2e decl. (ἀγαθός, -οῦ, -ῷ, -όν, -έ | -οί, -ῶν, -οῖς, -ούς, -οί); f. volgens 1e decl. η-stam (ἀγαθή, -ῆς, -ῇ, -ήν, -ή | -αί, -ῶν, -αῖς, -άς, -αί); n. volgens 2e decl. (ἀγαθόν, -οῦ, -ῷ, -όν, -όν | -ά, -ῶν, -οῖς, -ά, -ά).",
            "feedback": "30 vormen. Kernregel: m./n. = 2e decl., f. = 1e decl. η-stam. Voc. sg. m. op -έ, n. identiek aan nom.",
            "source": "handmatig",
            "verification_method": "self_report",
            "expected_result": "Volledige paradigma-tabel van ἀγαθός met correcte accenten, inclusief voc. sg. m. ἀγαθέ.",
        },
        {
            "id": "ITEM-GRC-G-MORF-ADJ-VERBG-002",
            "node_ids": ["GRC-G-MORF-ADJ-VERBG"],
            "type": "analyse",
            "direction": "receptief",
            "difficulty_initial": 0.6,
            "discrimination_initial": 1.3,
            "expected_time_sec": 25,
            "stimulus": "Welke naamval, getal en genus heeft καλῶν?",
            "answer": [
                "genitivus pluralis, alle drie genera",
                "gen. pl. (m./f./n.)",
            ],
            "feedback": "καλῶν is gen. pl. voor alle drie genera. In gen. pl. vallen m., f. en n. samen op -ῶν; alleen context beslist welk substantief erbij hoort.",
            "source": "handmatig",
        },
    ]

    return items


# ---------------------------------------------------------------------------
# SYNT-nodes — congruentie (6) + attributief/praedicatief (5)
# ---------------------------------------------------------------------------


def synt_items() -> dict[str, list[dict]]:
    items: dict[str, list[dict]] = {}

    items["GRC-G-SYNT-ADJ-CONGR"] = [
        {
            "id": "ITEM-GRC-G-SYNT-ADJ-CONGR-001",
            "node_ids": ["GRC-G-SYNT-ADJ-CONGR"],
            "type": "herkenning",
            "direction": "receptief",
            "difficulty_initial": -0.3,
            "discrimination_initial": 1.1,
            "expected_time_sec": 12,
            "stimulus": "Een Grieks adjectief congrueert met zijn substantief in welke drie categorieën?",
            "answer": [
                "genus, numerus, naamval",
                "geslacht, getal, casus",
            ],
            "feedback": "Congruentie gaat altijd over drie dimensies: genus (m./f./n.), numerus (sg./pl.) en naamval (nom./gen./dat./acc./voc.).",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-SYNT-ADJ-CONGR-002",
            "node_ids": ["GRC-G-SYNT-ADJ-CONGR"],
            "type": "productie",
            "direction": "productief",
            "difficulty_initial": 0.5,
            "discrimination_initial": 1.3,
            "expected_time_sec": 25,
            "stimulus": "Geef de vorm van ἀγαθός die congrueert met τοῦ δώρου.",
            "answer": "ἀγαθοῦ",
            "feedback": "τοῦ δώρου is gen. sg. n. → ἀγαθοῦ (gen. sg. n. = m.-vorm in 2e decl.). 'Van het goede geschenk'.",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-SYNT-ADJ-CONGR-003",
            "node_ids": ["GRC-G-SYNT-ADJ-CONGR"],
            "type": "productie",
            "direction": "productief",
            "difficulty_initial": 0.5,
            "discrimination_initial": 1.3,
            "expected_time_sec": 25,
            "stimulus": "Geef de vorm van καλός die congrueert met ταῖς χώραις.",
            "answer": "καλαῖς",
            "feedback": "ταῖς χώραις is dat. pl. f. → καλαῖς (dat. pl. f., 1e decl.). α/ο-stam adj. volgt voor f. de 1e decl.",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-SYNT-ADJ-CONGR-004",
            "node_ids": ["GRC-G-SYNT-ADJ-CONGR"],
            "type": "productie",
            "direction": "productief",
            "difficulty_initial": 0.6,
            "discrimination_initial": 1.3,
            "expected_time_sec": 25,
            "stimulus": "Geef de vorm van καλός die congrueert met τὰ δῶρα.",
            "answer": "καλά",
            "feedback": "τὰ δῶρα is nom./acc. pl. n. → καλά (nom./acc. pl. n., 2e decl.). Neutrum pl. op -α voor zowel adjectief als substantief.",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-SYNT-ADJ-CONGR-005",
            "node_ids": ["GRC-G-SYNT-ADJ-CONGR"],
            "type": "contextueel",
            "direction": "receptief",
            "difficulty_initial": 0.5,
            "discrimination_initial": 1.3,
            "expected_time_sec": 25,
            "stimulus": "In 'ὁ ἀγαθὸς στρατιώτης' — welke naamval, getal en genus delen adjectief en substantief?",
            "answer": [
                "nominativus singularis masculinum",
                "nom. sg. m.",
            ],
            "feedback": "ἀγαθός en στρατιώτης zijn beide nom. sg. m. Het lidwoord ὁ bevestigt dat: alle drie delen deze drie categorieën.",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-SYNT-ADJ-CONGR-006",
            "node_ids": ["GRC-G-SYNT-ADJ-CONGR"],
            "type": "analyse",
            "direction": "receptief",
            "difficulty_initial": 0.6,
            "discrimination_initial": 1.3,
            "expected_time_sec": 25,
            "stimulus": "Is 'ὁ σώφρων ἄνθρωπος καλά λέγει' grammaticaal correct qua congruentie tussen σώφρων en ἄνθρωπος?",
            "answer": [
                "ja, beide nom. sg. m.",
                "ja",
            ],
            "feedback": "σώφρων (nom. sg. m.) en ἄνθρωπος (nom. sg. m.) delen genus, numerus én naamval. σώφρων in deze vorm is 3e-decl. nom. sg. m./f.",
            "source": "handmatig",
        },
    ]

    items["GRC-G-SYNT-ADJ-ATTRIB"] = [
        {
            "id": "ITEM-GRC-G-SYNT-ADJ-ATTRIB-001",
            "node_ids": ["GRC-G-SYNT-ADJ-ATTRIB"],
            "type": "herkenning",
            "direction": "receptief",
            "difficulty_initial": -0.1,
            "discrimination_initial": 1.1,
            "expected_time_sec": 15,
            "stimulus": "Wat bepaalt of een adjectief attributief of praedicatief staat?",
            "answer": [
                "de positie t.o.v. het lidwoord",
                "de plaats van het adjectief ten opzichte van het lidwoord",
            ],
            "feedback": "Attributief: adjectief staat binnen de lidwoord-substantief-groep (ὁ ἀγαθὸς ἄνθρωπος). Praedicatief: erbuiten (ἀγαθὸς ὁ ἄνθρωπος).",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-SYNT-ADJ-ATTRIB-002",
            "node_ids": ["GRC-G-SYNT-ADJ-ATTRIB"],
            "type": "contextueel",
            "direction": "receptief",
            "difficulty_initial": 0.3,
            "discrimination_initial": 1.3,
            "expected_time_sec": 20,
            "stimulus": "Attributief of praedicatief: 'ὁ ἀγαθὸς ἄνθρωπος'?",
            "answer": "attributief",
            "feedback": "Attributief: ἀγαθός staat tussen lidwoord en substantief (ὁ … ἄνθρωπος). Betekenis: 'de goede mens'.",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-SYNT-ADJ-ATTRIB-003",
            "node_ids": ["GRC-G-SYNT-ADJ-ATTRIB"],
            "type": "contextueel",
            "direction": "receptief",
            "difficulty_initial": 0.3,
            "discrimination_initial": 1.3,
            "expected_time_sec": 20,
            "stimulus": "Attributief of praedicatief: 'ἀγαθὸς ὁ ἄνθρωπος'?",
            "answer": "praedicatief",
            "feedback": "Praedicatief: ἀγαθός staat buiten de lidwoord-substantief-groep. Vertaal met koppelwerkwoord: 'de mens is goed'.",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-SYNT-ADJ-ATTRIB-004",
            "node_ids": ["GRC-G-SYNT-ADJ-ATTRIB"],
            "type": "contextueel",
            "direction": "receptief",
            "difficulty_initial": 0.4,
            "discrimination_initial": 1.3,
            "expected_time_sec": 25,
            "stimulus": "Attributief of praedicatief: 'ὁ ἄνθρωπος ὁ ἀγαθός'?",
            "answer": "attributief",
            "feedback": "Tweede attributieve positie: lidwoord wordt herhaald vóór het adjectief (ὁ ἄνθρωπος ὁ ἀγαθός). Betekenis nog steeds 'de goede mens'.",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-SYNT-ADJ-ATTRIB-005",
            "node_ids": ["GRC-G-SYNT-ADJ-ATTRIB"],
            "type": "contextueel",
            "direction": "receptief",
            "difficulty_initial": 0.4,
            "discrimination_initial": 1.3,
            "expected_time_sec": 25,
            "stimulus": "Vertaal gegeven de positie: 'ὁ ἄνθρωπος ἀγαθός'.",
            "answer": [
                "de mens is goed",
                "de mens (is) goed",
            ],
            "feedback": "Praedicatief (adjectief erbuiten, zonder tweede lidwoord). Vertaal met koppelwerkwoord: 'de mens is goed'. Tegenover attributief 'ὁ ἀγαθὸς ἄνθρωπος' = 'de goede mens'.",
            "source": "handmatig",
        },
    ]

    return items


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------


def collect_all() -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {}
    out.update(morf_items())
    out.update(synt_items())
    for _node_id, item_list in out.items():
        for item in item_list:
            for key in ("stimulus", "antwoord", "feedback", "expected_result"):
                if key in item and item[key] is not None:
                    item[key] = nfc(item[key])
    return out


def validate_all(items_by_node: dict[str, list[dict]]) -> None:
    for _node_id, item_list in items_by_node.items():
        for item_dict in item_list:
            Item(**item_dict)
    total = sum(len(v) for v in items_by_node.values())
    print(f"All {total} items validated.")


def add_items_to_json(json_path: Path, items_by_node: dict[str, list[dict]]) -> int:
    """Attach items to their primary node (first element of node_ids)."""
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    # Flatten list of (primary_node_id, item) voor toevoegen
    primary_map: dict[str, list[dict]] = {}
    for _node_id, item_list in items_by_node.items():
        for item in item_list:
            primary = item["node_ids"][0]
            primary_map.setdefault(primary, []).append(item)

    added = 0
    for node in data["nodes"]:
        if node["id"] in primary_map:
            existing_ids = {item["id"] for item in node.get("items", [])}
            new_items = [
                item for item in primary_map[node["id"]] if item["id"] not in existing_ids
            ]
            node.setdefault("items", []).extend(new_items)
            added += len(new_items)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    return added


def print_summary(items_by_node: dict[str, list[dict]]) -> None:
    total = sum(len(v) for v in items_by_node.values())
    type_counter: Counter[str] = Counter()
    richting_counter: Counter[str] = Counter()
    congr_count = 0
    attrib_count = 0
    for item_list in items_by_node.values():
        for item in item_list:
            type_counter[item["type"]] += 1
            richting_counter[item["direction"]] += 1
            if "GRC-G-SYNT-ADJ-CONGR" in item["node_ids"]:
                congr_count += 1
            if "GRC-G-SYNT-ADJ-ATTRIB" in item["node_ids"]:
                attrib_count += 1

    print("\n=== E3-06 Summary ===")
    print(f"Knopen: {len(items_by_node)}")
    print(f"Total items: {total}")
    print(f"Congruentie-items (incl. multi-tag): {congr_count}")
    print(f"Attributief/praedicatief-items: {attrib_count}")
    print("\nOefentype-verdeling:")
    for t, c in type_counter.most_common():
        print(f"  {t}: {c}")
    print("\nRichting-verdeling:")
    for r, c in richting_counter.most_common():
        print(f"  {r}: {c}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    items_by_node = collect_all()
    validate_all(items_by_node)
    print_summary(items_by_node)

    if args.dry_run:
        print("\nDry-run: geen wijzigingen geschreven.")
        return

    path = Path(__file__).parent.parent / "data" / "graph" / "grc_grammatica_leerjaar1.json"
    added = add_items_to_json(path, items_by_node)
    print(f"\nAdded {added} items to {path.name}")


if __name__ == "__main__":
    main()
