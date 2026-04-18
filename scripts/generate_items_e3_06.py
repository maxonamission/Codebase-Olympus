#!/usr/bin/env python3
"""Generate exercise items for E3-06: GRC adjectieven.

Target: data/graph/grc_grammatica_leerjaar1.json
Scope:  8 knopen rondom adjectieven: ADJ-INTRO, ADJ-D12-3U, ADJ-D12-2U,
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
# MORF-knopen
# ---------------------------------------------------------------------------


def morf_items() -> dict[str, list[dict]]:
    """ADJ-INTRO (2) + D12-3U (3) + D12-2U (2) + D3 (3) + MEGAS (2) + VERBG (2) = 14 items."""
    items: dict[str, list[dict]] = {}

    items["GRC-G-MORF-ADJ-INTRO"] = [
        {
            "id": "ITEM-GRC-G-MORF-ADJ-INTRO-001",
            "knoop_ids": ["GRC-G-MORF-ADJ-INTRO"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.5,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 12,
            "stimulus": "Volgens welke drie categorieën moet een Grieks adjectief met zijn substantief overeenstemmen?",
            "antwoord": [
                "genus, numerus en naamval",
                "geslacht, getal en naamval",
            ],
            "feedback": "Congruentie: adjectief en substantief delen genus, numerus én naamval. Zes vormen per adjectief (3 genera × 2 numeri) per naamval.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-ADJ-INTRO-002",
            "knoop_ids": ["GRC-G-MORF-ADJ-INTRO"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.2,
            "discriminatie_initieel": 1.1,
            "verwachte_tijd_sec": 15,
            "stimulus": "Welke twee grote adjectief-groepen kent het Grieks qua stamtype?",
            "antwoord": [
                "α/ο-stammen (1e/2e decl.) en medeklinkerstammen (3e decl.)",
                "α/ο-stam en medeklinkerstam",
            ],
            "feedback": "α/ο-stammen volgen 1e/2e decl. (ἀγαθός, -ή, -όν). Medeklinkerstammen volgen de 3e decl. (σώφρων, ἀληθής).",
            "bron": "handmatig",
        },
    ]

    items["GRC-G-MORF-ADJ-D12-3U"] = [
        {
            "id": "ITEM-GRC-G-MORF-ADJ-D12-3U-001",
            "knoop_ids": ["GRC-G-MORF-ADJ-D12-3U"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.1,
            "discriminatie_initieel": 1.1,
            "verwachte_tijd_sec": 15,
            "stimulus": "Welke declinaties volgen de drie vormen van ἀγαθός, -ή, -όν?",
            "antwoord": [
                "m./n. volgen de 2e declinatie, f. volgt de 1e declinatie",
                "m. 2e decl., f. 1e decl., n. 2e decl.",
            ],
            "feedback": "ἀγαθός (m.) en ἀγαθόν (n.) volgen de 2e decl. (ο-stam); ἀγαθή (f.) volgt de 1e decl. (η-stam).",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-ADJ-D12-3U-002",
            "knoop_ids": ["GRC-G-MORF-ADJ-D12-3U", "GRC-G-SYNT-ADJ-CONGR"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.5,
            "discriminatie_initieel": 1.3,
            "verwachte_tijd_sec": 25,
            "stimulus": "Geef de vorm van ἀγαθός die congrueert met τὴν χώραν.",
            "antwoord": "ἀγαθήν",
            "feedback": "τὴν χώραν is acc. sg. f. → ἀγαθήν (acc. sg. f.). De f. van ἀγαθός volgt de 1e decl. (α/η-stam).",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-ADJ-D12-3U-003",
            "knoop_ids": ["GRC-G-MORF-ADJ-D12-3U", "GRC-G-SYNT-ADJ-CONGR"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.5,
            "discriminatie_initieel": 1.3,
            "verwachte_tijd_sec": 25,
            "stimulus": "Geef de vorm van καλός die congrueert met τοῖς ἀνθρώποις.",
            "antwoord": "καλοῖς",
            "feedback": "τοῖς ἀνθρώποις is dat. pl. m. → καλοῖς (dat. pl. m., 2e decl.). α/ο-stam adj. volgt de 2e decl. voor m./n.",
            "bron": "handmatig",
        },
    ]

    items["GRC-G-MORF-ADJ-D12-2U"] = [
        {
            "id": "ITEM-GRC-G-MORF-ADJ-D12-2U-001",
            "knoop_ids": ["GRC-G-MORF-ADJ-D12-2U"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.1,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 15,
            "stimulus": "Wat kenmerkt een adjectief als βάρβαρος, -ον met 'twee uitgangen'?",
            "antwoord": [
                "m. en f. delen dezelfde vorm (2e decl.); n. heeft aparte vorm op -ον",
                "m./f. identiek, n. apart",
            ],
            "feedback": "Bij βάρβαρος, -ον gebruikt het adjectief de 2e decl. voor m. én f.: ἡ βάρβαρος γυνή. De n. heeft wel een aparte vorm (βάρβαρον).",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-ADJ-D12-2U-002",
            "knoop_ids": ["GRC-G-MORF-ADJ-D12-2U", "GRC-G-SYNT-ADJ-CONGR"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.5,
            "discriminatie_initieel": 1.3,
            "verwachte_tijd_sec": 25,
            "stimulus": "Geef de vorm van βάρβαρος die congrueert met ἡ γυνή.",
            "antwoord": "βάρβαρος",
            "feedback": "ἡ γυνή is nom. sg. f. → βάρβαρος. Bij 'twee uitgangen' deelt het f. de m.-vorm van de 2e decl., ongeacht het genus van het substantief.",
            "bron": "handmatig",
        },
    ]

    items["GRC-G-MORF-ADJ-D3"] = [
        {
            "id": "ITEM-GRC-G-MORF-ADJ-D3-001",
            "knoop_ids": ["GRC-G-MORF-ADJ-D3"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.3,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 15,
            "stimulus": "Volgens welke declinatie worden σώφρων en ἀληθής verbogen?",
            "antwoord": [
                "de 3e declinatie (medeklinkerstam)",
                "3e decl.",
            ],
            "feedback": "σώφρων (stam σωφρον-, ν-stam) en ἀληθής (stam ἀληθεσ-, σ-stam) volgen de 3e decl. m./f. identiek, n. apart.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-ADJ-D3-002",
            "knoop_ids": ["GRC-G-MORF-ADJ-D3", "GRC-G-SYNT-ADJ-CONGR"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.7,
            "discriminatie_initieel": 1.3,
            "verwachte_tijd_sec": 30,
            "stimulus": "Geef de vorm van σώφρων die congrueert met τὸν ἄνθρωπον.",
            "antwoord": "σώφρονα",
            "feedback": "τὸν ἄνθρωπον is acc. sg. m. → σώφρονα (acc. sg. m., stam σωφρον- + -α). Let op: -α, niet -ον — de 3e decl. is anders dan de 2e.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-ADJ-D3-003",
            "knoop_ids": ["GRC-G-MORF-ADJ-D3"],
            "type": "analyse",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.6,
            "discriminatie_initieel": 1.3,
            "verwachte_tijd_sec": 25,
            "stimulus": "Wat is de nominativus sg. neutrum van σώφρων?",
            "antwoord": "σῶφρον",
            "feedback": "Nom. sg. n. = σῶφρον (kale stam σωφρον-, accent naar voren geschoven omdat neut. korter is dan de m.). De m. heeft klinkerverlenging: σώφρων.",
            "bron": "handmatig",
        },
    ]

    items["GRC-G-MORF-ADJ-MEGAS"] = [
        {
            "id": "ITEM-GRC-G-MORF-ADJ-MEGAS-001",
            "knoop_ids": ["GRC-G-MORF-ADJ-MEGAS"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.4,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 15,
            "stimulus": "Wat maakt μέγας en πολύς onregelmatig in hun verbuiging?",
            "antwoord": [
                "nom./acc. sg. m./n. komen van een korte stam (μεγα-/πολυ-), de rest van een uitgebreide stam (μεγαλ-/πολλ-)",
                "twee stammen door elkaar: korte én uitgebreide",
            ],
            "feedback": "μέγας en πολύς hebben twee stammen: μέγας/μέγα (m./n. nom./acc. sg.) maar μεγάλη, μεγάλου,... vanaf de rest. Πολύς/πολύ vs. πολλή, πολλοῦ.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-ADJ-MEGAS-002",
            "knoop_ids": ["GRC-G-MORF-ADJ-MEGAS", "GRC-G-SYNT-ADJ-CONGR"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.7,
            "discriminatie_initieel": 1.3,
            "verwachte_tijd_sec": 30,
            "stimulus": "Geef de vorm van μέγας die congrueert met τῆς χώρας.",
            "antwoord": "μεγάλης",
            "feedback": "τῆς χώρας is gen. sg. f. → μεγάλης. Buiten nom./acc. sg. m./n. wordt de uitgebreide stam μεγαλ- gebruikt, hier met 1e-decl.-uitgang.",
            "bron": "handmatig",
        },
    ]

    items["GRC-G-MORF-ADJ-VERBG"] = [
        {
            "id": "ITEM-GRC-G-MORF-ADJ-VERBG-001",
            "knoop_ids": ["GRC-G-MORF-ADJ-VERBG"],
            "type": "offline_schrijven",
            "richting": "productief",
            "moeilijkheid_initieel": 0.7,
            "discriminatie_initieel": 1.3,
            "verwachte_tijd_sec": 90,
            "stimulus": "Schrijf het volledige paradigma van ἀγαθός, -ή, -όν op (3 genera × 2 numeri × 5 naamvallen) en vergelijk met je grammaticaboek.",
            "antwoord": "m. volgens 2e decl. (ἀγαθός, -οῦ, -ῷ, -όν, -έ | -οί, -ῶν, -οῖς, -ούς, -οί); f. volgens 1e decl. η-stam (ἀγαθή, -ῆς, -ῇ, -ήν, -ή | -αί, -ῶν, -αῖς, -άς, -αί); n. volgens 2e decl. (ἀγαθόν, -οῦ, -ῷ, -όν, -όν | -ά, -ῶν, -οῖς, -ά, -ά).",
            "feedback": "30 vormen. Kernregel: m./n. = 2e decl., f. = 1e decl. η-stam. Voc. sg. m. op -έ, n. identiek aan nom.",
            "bron": "handmatig",
            "verificatie_methode": "self_report",
            "verwacht_resultaat": "Volledige paradigma-tabel van ἀγαθός met correcte accenten, inclusief voc. sg. m. ἀγαθέ.",
        },
        {
            "id": "ITEM-GRC-G-MORF-ADJ-VERBG-002",
            "knoop_ids": ["GRC-G-MORF-ADJ-VERBG"],
            "type": "analyse",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.6,
            "discriminatie_initieel": 1.3,
            "verwachte_tijd_sec": 25,
            "stimulus": "Welke naamval, getal en genus heeft καλῶν?",
            "antwoord": [
                "genitivus pluralis, alle drie genera",
                "gen. pl. (m./f./n.)",
            ],
            "feedback": "καλῶν is gen. pl. voor alle drie genera. In gen. pl. vallen m., f. en n. samen op -ῶν; alleen context beslist welk substantief erbij hoort.",
            "bron": "handmatig",
        },
    ]

    return items


# ---------------------------------------------------------------------------
# SYNT-knopen — congruentie (6) + attributief/praedicatief (5)
# ---------------------------------------------------------------------------


def synt_items() -> dict[str, list[dict]]:
    items: dict[str, list[dict]] = {}

    items["GRC-G-SYNT-ADJ-CONGR"] = [
        {
            "id": "ITEM-GRC-G-SYNT-ADJ-CONGR-001",
            "knoop_ids": ["GRC-G-SYNT-ADJ-CONGR"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.3,
            "discriminatie_initieel": 1.1,
            "verwachte_tijd_sec": 12,
            "stimulus": "Een Grieks adjectief congrueert met zijn substantief in welke drie categorieën?",
            "antwoord": [
                "genus, numerus, naamval",
                "geslacht, getal, casus",
            ],
            "feedback": "Congruentie gaat altijd over drie dimensies: genus (m./f./n.), numerus (sg./pl.) en naamval (nom./gen./dat./acc./voc.).",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-SYNT-ADJ-CONGR-002",
            "knoop_ids": ["GRC-G-SYNT-ADJ-CONGR"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.5,
            "discriminatie_initieel": 1.3,
            "verwachte_tijd_sec": 25,
            "stimulus": "Geef de vorm van ἀγαθός die congrueert met τοῦ δώρου.",
            "antwoord": "ἀγαθοῦ",
            "feedback": "τοῦ δώρου is gen. sg. n. → ἀγαθοῦ (gen. sg. n. = m.-vorm in 2e decl.). 'Van het goede geschenk'.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-SYNT-ADJ-CONGR-003",
            "knoop_ids": ["GRC-G-SYNT-ADJ-CONGR"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.5,
            "discriminatie_initieel": 1.3,
            "verwachte_tijd_sec": 25,
            "stimulus": "Geef de vorm van καλός die congrueert met ταῖς χώραις.",
            "antwoord": "καλαῖς",
            "feedback": "ταῖς χώραις is dat. pl. f. → καλαῖς (dat. pl. f., 1e decl.). α/ο-stam adj. volgt voor f. de 1e decl.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-SYNT-ADJ-CONGR-004",
            "knoop_ids": ["GRC-G-SYNT-ADJ-CONGR"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.6,
            "discriminatie_initieel": 1.3,
            "verwachte_tijd_sec": 25,
            "stimulus": "Geef de vorm van καλός die congrueert met τὰ δῶρα.",
            "antwoord": "καλά",
            "feedback": "τὰ δῶρα is nom./acc. pl. n. → καλά (nom./acc. pl. n., 2e decl.). Neutrum pl. op -α voor zowel adjectief als substantief.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-SYNT-ADJ-CONGR-005",
            "knoop_ids": ["GRC-G-SYNT-ADJ-CONGR"],
            "type": "contextueel",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.5,
            "discriminatie_initieel": 1.3,
            "verwachte_tijd_sec": 25,
            "stimulus": "In 'ὁ ἀγαθὸς στρατιώτης' — welke naamval, getal en genus delen adjectief en substantief?",
            "antwoord": [
                "nominativus singularis masculinum",
                "nom. sg. m.",
            ],
            "feedback": "ἀγαθός en στρατιώτης zijn beide nom. sg. m. Het lidwoord ὁ bevestigt dat: alle drie delen deze drie categorieën.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-SYNT-ADJ-CONGR-006",
            "knoop_ids": ["GRC-G-SYNT-ADJ-CONGR"],
            "type": "analyse",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.6,
            "discriminatie_initieel": 1.3,
            "verwachte_tijd_sec": 25,
            "stimulus": "Is 'ὁ σώφρων ἄνθρωπος καλά λέγει' grammaticaal correct qua congruentie tussen σώφρων en ἄνθρωπος?",
            "antwoord": [
                "ja, beide nom. sg. m.",
                "ja",
            ],
            "feedback": "σώφρων (nom. sg. m.) en ἄνθρωπος (nom. sg. m.) delen genus, numerus én naamval. σώφρων in deze vorm is 3e-decl. nom. sg. m./f.",
            "bron": "handmatig",
        },
    ]

    items["GRC-G-SYNT-ADJ-ATTRIB"] = [
        {
            "id": "ITEM-GRC-G-SYNT-ADJ-ATTRIB-001",
            "knoop_ids": ["GRC-G-SYNT-ADJ-ATTRIB"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.1,
            "discriminatie_initieel": 1.1,
            "verwachte_tijd_sec": 15,
            "stimulus": "Wat bepaalt of een adjectief attributief of praedicatief staat?",
            "antwoord": [
                "de positie t.o.v. het lidwoord",
                "de plaats van het adjectief ten opzichte van het lidwoord",
            ],
            "feedback": "Attributief: adjectief staat binnen de lidwoord-substantief-groep (ὁ ἀγαθὸς ἄνθρωπος). Praedicatief: erbuiten (ἀγαθὸς ὁ ἄνθρωπος).",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-SYNT-ADJ-ATTRIB-002",
            "knoop_ids": ["GRC-G-SYNT-ADJ-ATTRIB"],
            "type": "contextueel",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.3,
            "discriminatie_initieel": 1.3,
            "verwachte_tijd_sec": 20,
            "stimulus": "Attributief of praedicatief: 'ὁ ἀγαθὸς ἄνθρωπος'?",
            "antwoord": "attributief",
            "feedback": "Attributief: ἀγαθός staat tussen lidwoord en substantief (ὁ … ἄνθρωπος). Betekenis: 'de goede mens'.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-SYNT-ADJ-ATTRIB-003",
            "knoop_ids": ["GRC-G-SYNT-ADJ-ATTRIB"],
            "type": "contextueel",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.3,
            "discriminatie_initieel": 1.3,
            "verwachte_tijd_sec": 20,
            "stimulus": "Attributief of praedicatief: 'ἀγαθὸς ὁ ἄνθρωπος'?",
            "antwoord": "praedicatief",
            "feedback": "Praedicatief: ἀγαθός staat buiten de lidwoord-substantief-groep. Vertaal met koppelwerkwoord: 'de mens is goed'.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-SYNT-ADJ-ATTRIB-004",
            "knoop_ids": ["GRC-G-SYNT-ADJ-ATTRIB"],
            "type": "contextueel",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.4,
            "discriminatie_initieel": 1.3,
            "verwachte_tijd_sec": 25,
            "stimulus": "Attributief of praedicatief: 'ὁ ἄνθρωπος ὁ ἀγαθός'?",
            "antwoord": "attributief",
            "feedback": "Tweede attributieve positie: lidwoord wordt herhaald vóór het adjectief (ὁ ἄνθρωπος ὁ ἀγαθός). Betekenis nog steeds 'de goede mens'.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-SYNT-ADJ-ATTRIB-005",
            "knoop_ids": ["GRC-G-SYNT-ADJ-ATTRIB"],
            "type": "contextueel",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.4,
            "discriminatie_initieel": 1.3,
            "verwachte_tijd_sec": 25,
            "stimulus": "Vertaal gegeven de positie: 'ὁ ἄνθρωπος ἀγαθός'.",
            "antwoord": [
                "de mens is goed",
                "de mens (is) goed",
            ],
            "feedback": "Praedicatief (adjectief erbuiten, zonder tweede lidwoord). Vertaal met koppelwerkwoord: 'de mens is goed'. Tegenover attributief 'ὁ ἀγαθὸς ἄνθρωπος' = 'de goede mens'.",
            "bron": "handmatig",
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
    for _knoop_id, item_list in out.items():
        for item in item_list:
            for key in ("stimulus", "antwoord", "feedback", "verwacht_resultaat"):
                if key in item and item[key] is not None:
                    item[key] = nfc(item[key])
    return out


def validate_all(items_by_knoop: dict[str, list[dict]]) -> None:
    for _knoop_id, item_list in items_by_knoop.items():
        for item_dict in item_list:
            Item(**item_dict)
    total = sum(len(v) for v in items_by_knoop.values())
    print(f"All {total} items validated.")


def add_items_to_json(json_path: Path, items_by_knoop: dict[str, list[dict]]) -> int:
    """Attach items to their primary knoop (first element of knoop_ids)."""
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    # Flatten list of (primary_knoop_id, item) voor toevoegen
    primary_map: dict[str, list[dict]] = {}
    for _knoop_id, item_list in items_by_knoop.items():
        for item in item_list:
            primary = item["knoop_ids"][0]
            primary_map.setdefault(primary, []).append(item)

    added = 0
    for knoop in data["knopen"]:
        if knoop["id"] in primary_map:
            existing_ids = {item["id"] for item in knoop.get("items", [])}
            new_items = [
                item
                for item in primary_map[knoop["id"]]
                if item["id"] not in existing_ids
            ]
            knoop.setdefault("items", []).extend(new_items)
            added += len(new_items)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    return added


def print_summary(items_by_knoop: dict[str, list[dict]]) -> None:
    total = sum(len(v) for v in items_by_knoop.values())
    type_counter: Counter[str] = Counter()
    richting_counter: Counter[str] = Counter()
    congr_count = 0
    attrib_count = 0
    for item_list in items_by_knoop.values():
        for item in item_list:
            type_counter[item["type"]] += 1
            richting_counter[item["richting"]] += 1
            if "GRC-G-SYNT-ADJ-CONGR" in item["knoop_ids"]:
                congr_count += 1
            if "GRC-G-SYNT-ADJ-ATTRIB" in item["knoop_ids"]:
                attrib_count += 1

    print("\n=== E3-06 Summary ===")
    print(f"Knopen: {len(items_by_knoop)}")
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

    items_by_knoop = collect_all()
    validate_all(items_by_knoop)
    print_summary(items_by_knoop)

    if args.dry_run:
        print("\nDry-run: geen wijzigingen geschreven.")
        return

    path = Path(__file__).parent.parent / "data" / "graph" / "grc_grammatica_leerjaar1.json"
    added = add_items_to_json(path, items_by_knoop)
    print(f"\nAdded {added} items to {path.name}")


if __name__ == "__main__":
    main()
