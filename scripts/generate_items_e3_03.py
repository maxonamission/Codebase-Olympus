#!/usr/bin/env python3
"""Generate exercise items for E3-03: GRC 1e declinatie (α/η-stammen).

Target: data/graph/grc_grammatica_leerjaar1.json
Scope:  10 nodes rondom de 1e declinatie: DECL1-INTRO, DECL1-ETA, DECL1-ALFA,
        DECL1-MASC, NOM-D1, GEN-D1, DAT-D1, ACC-D1, VOC-D1, DECL1-PARAD.

Mix per node: herkenning + productie + paradigma-drill (vorm-analyse).
Modelwoorden: τιμή (η-stam), χώρα (α-stam pura), θάλαττα (α-impura),
νεανίας en κριτής (masculina). Productie-antwoorden zijn polytonisch en
NFC-genormaliseerd, zodat ze werken met frontend GreekInput.jsx.

Run:
    python scripts/generate_items_e3_03.py            # writes items to graph
    python scripts/generate_items_e3_03.py --dry-run  # only validate + print
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

# ---------------------------------------------------------------------------
# Helper: ensure NFC normalization on every stimulus/antwoord/feedback string
# (matches the normalization done client-side in GreekInput.jsx).
# ---------------------------------------------------------------------------


def nfc(value):
    if isinstance(value, str):
        return unicodedata.normalize("NFC", value)
    if isinstance(value, list):
        return [nfc(v) for v in value]
    return value


# ---------------------------------------------------------------------------
# Item definitions per node.
# ---------------------------------------------------------------------------


def decl1_intro_en_varianten() -> dict[str, list[dict]]:
    """DECL1-INTRO, -ETA, -ALFA, -MASC — 12 items."""
    items: dict[str, list[dict]] = {}

    items["GRC-G-MORF-DECL1-INTRO"] = [
        {
            "id": "ITEM-GRC-G-MORF-DECL1-INTRO-001",
            "node_ids": ["GRC-G-MORF-DECL1-INTRO"],
            "type": "herkenning",
            "direction": "receptief",
            "difficulty_initial": -0.7,
            "discrimination_initial": 1.0,
            "expected_time_sec": 12,
            "stimulus": "Welke twee stamklinkers komen voor in de 1e declinatie?",
            "answer": ["α en η", "η en α"],
            "feedback": "De 1e declinatie heet 'α/η-stammen': feminina eindigen in de nom. sg. op -η (τιμή) of -α (χώρα).",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-DECL1-INTRO-002",
            "node_ids": ["GRC-G-MORF-DECL1-INTRO"],
            "type": "herkenning",
            "direction": "receptief",
            "difficulty_initial": -0.3,
            "discrimination_initial": 1.0,
            "expected_time_sec": 12,
            "stimulus": "Welk genus hebben de meeste woorden van de 1e declinatie?",
            "answer": ["femininum", "vrouwelijk"],
            "feedback": "De 1e declinatie is overwegend femininum. Mannelijke uitzonderingen zijn νεανίας (jongeman) en κριτής (rechter).",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-DECL1-INTRO-003",
            "node_ids": ["GRC-G-MORF-DECL1-INTRO"],
            "type": "herkenning",
            "direction": "receptief",
            "difficulty_initial": 0.0,
            "discrimination_initial": 1.2,
            "expected_time_sec": 15,
            "stimulus": "Hoe herken je in het woordenboek dat ἡ τιμή bij de 1e declinatie hoort?",
            "answer": [
                "aan de genitivus sg. op -ης of -ας",
                "τιμή, -ῆς → gen. sg. op -ης",
            ],
            "feedback": "De lemma-vorm geeft nom. + gen. sg. Voor 1e declinatie eindigt de gen. sg. op -ης (τιμή, -ῆς) of -ας (χώρα, -ας).",
            "source": "handmatig",
        },
    ]

    items["GRC-G-MORF-DECL1-ETA"] = [
        {
            "id": "ITEM-GRC-G-MORF-DECL1-ETA-001",
            "node_ids": ["GRC-G-MORF-DECL1-ETA"],
            "type": "herkenning",
            "direction": "receptief",
            "difficulty_initial": -0.5,
            "discrimination_initial": 1.0,
            "expected_time_sec": 12,
            "stimulus": "Op welke uitgang eindigt de nominativus sg. van een η-stam femininum?",
            "answer": "-η",
            "feedback": "η-stammen hebben in nom. sg. altijd de uitgang -η. Modelwoord: τιμή.",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-DECL1-ETA-002",
            "node_ids": ["GRC-G-MORF-DECL1-ETA"],
            "type": "productie",
            "direction": "productief",
            "difficulty_initial": 0.4,
            "discrimination_initial": 1.2,
            "expected_time_sec": 25,
            "stimulus": "Geef de genitivus singularis van τιμή.",
            "answer": "τιμῆς",
            "feedback": "Gen. sg. van τιμή = τιμῆς. De uitgang -ης krijgt een circumflex op de stamklinker η.",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-DECL1-ETA-003",
            "node_ids": ["GRC-G-MORF-DECL1-ETA"],
            "type": "productie",
            "direction": "productief",
            "difficulty_initial": 0.6,
            "discrimination_initial": 1.2,
            "expected_time_sec": 25,
            "stimulus": "Geef de dativus singularis van τιμή.",
            "answer": "τιμῇ",
            "feedback": "Dat. sg. = τιμῇ: lange η met iota subscriptum, circumflex is verplicht op de ultima als de stam lang is.",
            "source": "handmatig",
        },
    ]

    items["GRC-G-MORF-DECL1-ALFA"] = [
        {
            "id": "ITEM-GRC-G-MORF-DECL1-ALFA-001",
            "node_ids": ["GRC-G-MORF-DECL1-ALFA"],
            "type": "herkenning",
            "direction": "receptief",
            "difficulty_initial": 0.1,
            "discrimination_initial": 1.2,
            "expected_time_sec": 15,
            "stimulus": "Na welke drie letters blijft de α bewaard in alle naamvallen (α pura)?",
            "answer": ["ε, ι, ρ", "na ε, ι of ρ"],
            "feedback": "α pura (zoals χώρα) heeft α vóór de stam-klinker ε, ι of ρ — α blijft dan in alle naamvallen bewaard.",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-DECL1-ALFA-002",
            "node_ids": ["GRC-G-MORF-DECL1-ALFA"],
            "type": "productie",
            "direction": "productief",
            "difficulty_initial": 0.4,
            "discrimination_initial": 1.2,
            "expected_time_sec": 25,
            "stimulus": "Geef de genitivus singularis van χώρα.",
            "answer": "χώρας",
            "feedback": "χώρα is α pura (stam op ρ), dus gen. sg. = χώρας. De α blijft bewaard.",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-DECL1-ALFA-003",
            "node_ids": ["GRC-G-MORF-DECL1-ALFA"],
            "type": "analyse",
            "direction": "receptief",
            "difficulty_initial": 0.8,
            "discrimination_initial": 1.3,
            "expected_time_sec": 30,
            "stimulus": "Waarin verschilt θάλαττα (α impura) van χώρα in het enkelvoud?",
            "answer": [
                "in gen. en dat. sg. staat η i.p.v. α (θαλάττης, θαλάττῃ)",
                "gen./dat. sg. op -ης/-ῃ in plaats van -ας/-ᾳ",
            ],
            "feedback": "α impura volgt niet de ε/ι/ρ-regel: in gen./dat. sg. vervangt η de α (θαλάττης, θαλάττῃ). In het meervoud komt de α terug.",
            "source": "handmatig",
        },
    ]

    items["GRC-G-MORF-DECL1-MASC"] = [
        {
            "id": "ITEM-GRC-G-MORF-DECL1-MASC-001",
            "node_ids": ["GRC-G-MORF-DECL1-MASC"],
            "type": "herkenning",
            "direction": "receptief",
            "difficulty_initial": 0.2,
            "discrimination_initial": 1.2,
            "expected_time_sec": 15,
            "stimulus": "Op welke twee uitgangen kan de nominativus sg. van een masculinum van de 1e declinatie eindigen?",
            "answer": ["-ας en -ης", "-ας of -ης"],
            "feedback": "Masc. 1e decl.: νεανίας-type op -ας en κριτής-type op -ης. De rest van de naamvallen volgt de feminine vorm.",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-DECL1-MASC-002",
            "node_ids": ["GRC-G-MORF-DECL1-MASC"],
            "type": "productie",
            "direction": "productief",
            "difficulty_initial": 0.6,
            "discrimination_initial": 1.2,
            "expected_time_sec": 25,
            "stimulus": "Geef de genitivus singularis van νεανίας.",
            "answer": "νεανίου",
            "feedback": "Mannelijke 1e declinatie leent de gen. sg. van de 2e declinatie: νεανίας → νεανίου. Uitzondering op het paradigma.",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-DECL1-MASC-003",
            "node_ids": ["GRC-G-MORF-DECL1-MASC"],
            "type": "analyse",
            "direction": "receptief",
            "difficulty_initial": 0.7,
            "discrimination_initial": 1.3,
            "expected_time_sec": 30,
            "stimulus": "Welke naamval is κριτοῦ en welke uitgang signaleert dat?",
            "answer": [
                "genitivus singularis, uitgang -ου",
                "gen. sg.; -ου",
            ],
            "feedback": "κριτοῦ is gen. sg. van κριτής: uitgang -ου, identiek aan de 2e declinatie. Zonder lidwoord makkelijk te verwarren met 2e decl.",
            "source": "handmatig",
        },
    ]

    return items


def naamval_items() -> dict[str, list[dict]]:
    """NOM-D1, GEN-D1, DAT-D1, ACC-D1, VOC-D1 — 15 items."""
    items: dict[str, list[dict]] = {}

    items["GRC-G-MORF-NOM-D1"] = [
        {
            "id": "ITEM-GRC-G-MORF-NOM-D1-001",
            "node_ids": ["GRC-G-MORF-NOM-D1"],
            "type": "herkenning",
            "direction": "receptief",
            "difficulty_initial": -0.3,
            "discrimination_initial": 1.0,
            "expected_time_sec": 12,
            "stimulus": "Welke uitgang heeft de nominativus pluralis in de 1e declinatie?",
            "answer": "-αι",
            "feedback": "Nom. pl. = -αι voor alle varianten: τιμαί, χῶραι, θάλατται, νεανίαι, κριταί. Let op: -αι is kort in de accentregels.",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-NOM-D1-002",
            "node_ids": ["GRC-G-MORF-NOM-D1"],
            "type": "productie",
            "direction": "productief",
            "difficulty_initial": 0.3,
            "discrimination_initial": 1.2,
            "expected_time_sec": 25,
            "stimulus": "Geef de nominativus pluralis van τιμή.",
            "answer": "τιμαί",
            "feedback": "Nom. pl. van τιμή = τιμαί. De acutus op de ultima is de standaardpositie van het accent.",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-NOM-D1-003",
            "node_ids": ["GRC-G-MORF-NOM-D1"],
            "type": "analyse",
            "direction": "receptief",
            "difficulty_initial": 0.5,
            "discrimination_initial": 1.2,
            "expected_time_sec": 25,
            "stimulus": "Waarom krijgt χῶραι een circumflex op de penult en τιμαί niet?",
            "answer": [
                "omdat de lange penult ω bij een korte ultima -αι een circumflex eist",
                "lange penult + korte ultima → circumflex",
            ],
            "feedback": "Finale -αι telt als kort. Bij χώρα is de penult lang (ω), dus lange penult + korte ultima eist circumflex: χῶραι. Bij τιμή staat het accent al op de (nu kort geworden) ultima.",
            "source": "handmatig",
        },
    ]

    items["GRC-G-MORF-GEN-D1"] = [
        {
            "id": "ITEM-GRC-G-MORF-GEN-D1-001",
            "node_ids": ["GRC-G-MORF-GEN-D1"],
            "type": "herkenning",
            "direction": "receptief",
            "difficulty_initial": -0.1,
            "discrimination_initial": 1.0,
            "expected_time_sec": 12,
            "stimulus": "Welke uitgang heeft de genitivus pluralis in de 1e declinatie?",
            "answer": "-ῶν",
            "feedback": "Gen. pl. is voor alle woorden van de 1e declinatie -ῶν, altijd met circumflex: τιμῶν, χωρῶν, νεανιῶν.",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-GEN-D1-002",
            "node_ids": ["GRC-G-MORF-GEN-D1"],
            "type": "productie",
            "direction": "productief",
            "difficulty_initial": 0.4,
            "discrimination_initial": 1.2,
            "expected_time_sec": 25,
            "stimulus": "Geef de genitivus pluralis van χώρα.",
            "answer": "χωρῶν",
            "feedback": "Gen. pl. = χωρῶν. De circumflex op -ῶν is een vast kenmerk van de 1e declinatie — betrouwbaarder dan -ῆς/-ας in het enkelvoud.",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-GEN-D1-003",
            "node_ids": ["GRC-G-MORF-GEN-D1"],
            "type": "herkenning",
            "direction": "receptief",
            "difficulty_initial": 0.2,
            "discrimination_initial": 1.2,
            "expected_time_sec": 15,
            "stimulus": "Welke naamval is τιμῆς?",
            "answer": ["genitivus singularis", "gen. sg."],
            "feedback": "τιμῆς is gen. sg. van τιμή — kenmerkend is -ῆς met circumflex. Niet verwarren met de acc. pl. τιμάς (met acutus).",
            "source": "handmatig",
        },
    ]

    items["GRC-G-MORF-DAT-D1"] = [
        {
            "id": "ITEM-GRC-G-MORF-DAT-D1-001",
            "node_ids": ["GRC-G-MORF-DAT-D1"],
            "type": "herkenning",
            "direction": "receptief",
            "difficulty_initial": 0.0,
            "discrimination_initial": 1.0,
            "expected_time_sec": 12,
            "stimulus": "Welk diakritisch teken kenmerkt de dativus sg. van de 1e declinatie?",
            "answer": ["iota subscriptum", "een iota onder de klinker"],
            "feedback": "Dat. sg. heeft altijd een iota subscriptum: τιμῇ, χώρᾳ, θαλάττῃ. Dit iota is stom maar kenmerkend.",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-DAT-D1-002",
            "node_ids": ["GRC-G-MORF-DAT-D1"],
            "type": "productie",
            "direction": "productief",
            "difficulty_initial": 0.6,
            "discrimination_initial": 1.3,
            "expected_time_sec": 30,
            "stimulus": "Geef de dativus singularis en de dativus pluralis van χώρα.",
            "answer": [
                "χώρᾳ, χώραις",
                "χώρᾳ en χώραις",
            ],
            "feedback": "Dat. sg. = χώρᾳ (met iota subscriptum), dat. pl. = χώραις. In het meervoud geen iota subscriptum meer.",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-DAT-D1-003",
            "node_ids": ["GRC-G-MORF-DAT-D1"],
            "type": "analyse",
            "direction": "receptief",
            "difficulty_initial": 0.5,
            "discrimination_initial": 1.2,
            "expected_time_sec": 25,
            "stimulus": "Welke naamval is τιμαῖς?",
            "answer": ["dativus pluralis", "dat. pl."],
            "feedback": "τιμαῖς = dat. pl. van τιμή. Uitgang -αις met circumflex op de αι (lang) is typerend voor de dat. pl. van de 1e decl.",
            "source": "handmatig",
        },
    ]

    items["GRC-G-MORF-ACC-D1"] = [
        {
            "id": "ITEM-GRC-G-MORF-ACC-D1-001",
            "node_ids": ["GRC-G-MORF-ACC-D1"],
            "type": "herkenning",
            "direction": "receptief",
            "difficulty_initial": -0.1,
            "discrimination_initial": 1.0,
            "expected_time_sec": 12,
            "stimulus": "Welke uitgang heeft de accusativus singularis bij η-stammen?",
            "answer": "-ην",
            "feedback": "Acc. sg. van η-stammen: -ην (τιμήν). Bij α-stammen: -αν (χώραν, θάλατταν).",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-ACC-D1-002",
            "node_ids": ["GRC-G-MORF-ACC-D1"],
            "type": "productie",
            "direction": "productief",
            "difficulty_initial": 0.4,
            "discrimination_initial": 1.2,
            "expected_time_sec": 25,
            "stimulus": "Geef de accusativus pluralis van τιμή.",
            "answer": "τιμάς",
            "feedback": "Acc. pl. van τιμή = τιμάς (-άς lang). Niet verwarren met gen. sg. τιμῆς — ander accent én andere stamklinker.",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-ACC-D1-003",
            "node_ids": ["GRC-G-MORF-ACC-D1"],
            "type": "analyse",
            "direction": "receptief",
            "difficulty_initial": 0.6,
            "discrimination_initial": 1.3,
            "expected_time_sec": 25,
            "stimulus": "Welke naamval(len) kan χώρας zijn?",
            "answer": [
                "genitivus singularis of accusativus pluralis",
                "gen. sg. of acc. pl.",
            ],
            "feedback": "χώρας is ambivalent: gen. sg. (-ας kort) of acc. pl. (-ας lang). Lidwoord (τῆς vs. τάς) en context beslissen.",
            "source": "handmatig",
        },
    ]

    items["GRC-G-MORF-VOC-D1"] = [
        {
            "id": "ITEM-GRC-G-MORF-VOC-D1-001",
            "node_ids": ["GRC-G-MORF-VOC-D1"],
            "type": "herkenning",
            "direction": "receptief",
            "difficulty_initial": -0.2,
            "discrimination_initial": 1.0,
            "expected_time_sec": 12,
            "stimulus": "Hoe vormt een feminienum van de 1e declinatie de vocativus singularis?",
            "answer": [
                "gelijk aan de nominativus singularis",
                "identiek aan nom. sg.",
            ],
            "feedback": "Voc. sg. van fem. 1e decl. = nom. sg.: ὦ τιμή, ὦ χώρα. In het meervoud ook (τιμαί, χῶραι).",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-VOC-D1-002",
            "node_ids": ["GRC-G-MORF-VOC-D1"],
            "type": "productie",
            "direction": "productief",
            "difficulty_initial": 0.5,
            "discrimination_initial": 1.2,
            "expected_time_sec": 25,
            "stimulus": "Geef de vocativus singularis van νεανίας.",
            "answer": "νεανία",
            "feedback": "Masc. 1e decl. op -ας krijgt voc. sg. op korte α: νεανία. De nom. en voc. zijn hier dus niet identiek.",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-VOC-D1-003",
            "node_ids": ["GRC-G-MORF-VOC-D1"],
            "type": "herkenning",
            "direction": "receptief",
            "difficulty_initial": 0.4,
            "discrimination_initial": 1.2,
            "expected_time_sec": 15,
            "stimulus": "Wat is de vocativus singularis van κριτής?",
            "answer": "κριτά",
            "feedback": "κριτής-type vormt voc. sg. op -α: κριτά. Afwijkend van de nom. sg. — kenmerkend voor masc. 1e decl.",
            "source": "handmatig",
        },
    ]

    return items


def paradigma_items() -> dict[str, list[dict]]:
    """DECL1-PARAD — 3 items (paradigma-drill)."""
    items: dict[str, list[dict]] = {}

    items["GRC-G-MORF-DECL1-PARAD"] = [
        {
            "id": "ITEM-GRC-G-MORF-DECL1-PARAD-001",
            "node_ids": ["GRC-G-MORF-DECL1-PARAD"],
            "type": "offline_schrijven",
            "direction": "productief",
            "difficulty_initial": 0.7,
            "discrimination_initial": 1.3,
            "expected_time_sec": 90,
            "stimulus": "Schrijf het volledige paradigma van τιμή op (alle vijf naamvallen, sg. en pl.) en vergelijk met je grammaticaboek.",
            "answer": "τιμή, τιμῆς, τιμῇ, τιμήν, τιμή | τιμαί, τιμῶν, τιμαῖς, τιμάς, τιμαί",
            "feedback": "Volledig: sg. τιμή / τιμῆς / τιμῇ / τιμήν / τιμή — pl. τιμαί / τιμῶν / τιμαῖς / τιμάς / τιμαί. Let op de circumflex op gen./dat. sg. en op gen. pl.",
            "source": "handmatig",
            "verification_method": "self_report",
            "expected_result": "Paradigma van τιμή in 10 vormen, met correcte accenten (circumflex op τιμῆς, τιμῇ, τιμῶν, τιμαῖς).",
        },
        {
            "id": "ITEM-GRC-G-MORF-DECL1-PARAD-002",
            "node_ids": ["GRC-G-MORF-DECL1-PARAD"],
            "type": "analyse",
            "direction": "receptief",
            "difficulty_initial": 0.8,
            "discrimination_initial": 1.3,
            "expected_time_sec": 35,
            "stimulus": "Analyseer χώραις volledig: naamval, getal en modelwoord-type.",
            "answer": [
                "dativus pluralis van χώρα (α-stam pura)",
                "dat. pl., α pura",
            ],
            "feedback": "χώραις = dat. pl. van χώρα (α-stam pura). Uitgang -αις is gelijk voor alle feminina 1e decl.; de behouden α verraadt de α pura.",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-DECL1-PARAD-003",
            "node_ids": ["GRC-G-MORF-DECL1-PARAD"],
            "type": "productie",
            "direction": "productief",
            "difficulty_initial": 0.9,
            "discrimination_initial": 1.4,
            "expected_time_sec": 40,
            "stimulus": "Geef alle vier dativus-vormen (sg. en pl.) voor τιμή en χώρα.",
            "answer": [
                "τιμῇ, τιμαῖς, χώρᾳ, χώραις",
                "τιμῇ τιμαῖς χώρᾳ χώραις",
            ],
            "feedback": "Dat. sg. τιμῇ / χώρᾳ (iota subscriptum), dat. pl. τιμαῖς / χώραις. Zelfde uitgangen, alleen de stamklinker verschilt.",
            "source": "handmatig",
        },
    ]

    return items


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------


def collect_all() -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {}
    out.update(decl1_intro_en_varianten())
    out.update(naamval_items())
    out.update(paradigma_items())
    # NFC-normalize alle strings (stimulus, antwoord, feedback, expected_result)
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
    type_counter: Counter[str] = Counter()
    richting_counter: Counter[str] = Counter()
    for item_list in items_by_node.values():
        for item in item_list:
            type_counter[item["type"]] += 1
            richting_counter[item["direction"]] += 1

    print("\n=== E3-03 Summary ===")
    print(f"Knopen: {len(items_by_node)}")
    print(f"Total items: {total}")
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
