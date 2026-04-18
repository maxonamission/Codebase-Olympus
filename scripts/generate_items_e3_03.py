#!/usr/bin/env python3
"""Generate exercise items for E3-03: GRC 1e declinatie (α/η-stammen).

Target: data/graph/grc_grammatica_leerjaar1.json
Scope:  10 knopen rondom de 1e declinatie: DECL1-INTRO, DECL1-ETA, DECL1-ALFA,
        DECL1-MASC, NOM-D1, GEN-D1, DAT-D1, ACC-D1, VOC-D1, DECL1-PARAD.

Mix per knoop: herkenning + productie + paradigma-drill (vorm-analyse).
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
# Item definitions per knoop.
# ---------------------------------------------------------------------------


def decl1_intro_en_varianten() -> dict[str, list[dict]]:
    """DECL1-INTRO, -ETA, -ALFA, -MASC — 12 items."""
    items: dict[str, list[dict]] = {}

    items["GRC-G-MORF-DECL1-INTRO"] = [
        {
            "id": "ITEM-GRC-G-MORF-DECL1-INTRO-001",
            "knoop_ids": ["GRC-G-MORF-DECL1-INTRO"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.7,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 12,
            "stimulus": "Welke twee stamklinkers komen voor in de 1e declinatie?",
            "antwoord": ["α en η", "η en α"],
            "feedback": "De 1e declinatie heet 'α/η-stammen': feminina eindigen in de nom. sg. op -η (τιμή) of -α (χώρα).",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-DECL1-INTRO-002",
            "knoop_ids": ["GRC-G-MORF-DECL1-INTRO"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.3,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 12,
            "stimulus": "Welk genus hebben de meeste woorden van de 1e declinatie?",
            "antwoord": ["femininum", "vrouwelijk"],
            "feedback": "De 1e declinatie is overwegend femininum. Mannelijke uitzonderingen zijn νεανίας (jongeman) en κριτής (rechter).",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-DECL1-INTRO-003",
            "knoop_ids": ["GRC-G-MORF-DECL1-INTRO"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.0,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 15,
            "stimulus": "Hoe herken je in het woordenboek dat ἡ τιμή bij de 1e declinatie hoort?",
            "antwoord": [
                "aan de genitivus sg. op -ης of -ας",
                "τιμή, -ῆς → gen. sg. op -ης",
            ],
            "feedback": "De lemma-vorm geeft nom. + gen. sg. Voor 1e declinatie eindigt de gen. sg. op -ης (τιμή, -ῆς) of -ας (χώρα, -ας).",
            "bron": "handmatig",
        },
    ]

    items["GRC-G-MORF-DECL1-ETA"] = [
        {
            "id": "ITEM-GRC-G-MORF-DECL1-ETA-001",
            "knoop_ids": ["GRC-G-MORF-DECL1-ETA"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.5,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 12,
            "stimulus": "Op welke uitgang eindigt de nominativus sg. van een η-stam femininum?",
            "antwoord": "-η",
            "feedback": "η-stammen hebben in nom. sg. altijd de uitgang -η. Modelwoord: τιμή.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-DECL1-ETA-002",
            "knoop_ids": ["GRC-G-MORF-DECL1-ETA"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.4,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 25,
            "stimulus": "Geef de genitivus singularis van τιμή.",
            "antwoord": "τιμῆς",
            "feedback": "Gen. sg. van τιμή = τιμῆς. De uitgang -ης krijgt een circumflex op de stamklinker η.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-DECL1-ETA-003",
            "knoop_ids": ["GRC-G-MORF-DECL1-ETA"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.6,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 25,
            "stimulus": "Geef de dativus singularis van τιμή.",
            "antwoord": "τιμῇ",
            "feedback": "Dat. sg. = τιμῇ: lange η met iota subscriptum, circumflex is verplicht op de ultima als de stam lang is.",
            "bron": "handmatig",
        },
    ]

    items["GRC-G-MORF-DECL1-ALFA"] = [
        {
            "id": "ITEM-GRC-G-MORF-DECL1-ALFA-001",
            "knoop_ids": ["GRC-G-MORF-DECL1-ALFA"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.1,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 15,
            "stimulus": "Na welke drie letters blijft de α bewaard in alle naamvallen (α pura)?",
            "antwoord": ["ε, ι, ρ", "na ε, ι of ρ"],
            "feedback": "α pura (zoals χώρα) heeft α vóór de stam-klinker ε, ι of ρ — α blijft dan in alle naamvallen bewaard.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-DECL1-ALFA-002",
            "knoop_ids": ["GRC-G-MORF-DECL1-ALFA"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.4,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 25,
            "stimulus": "Geef de genitivus singularis van χώρα.",
            "antwoord": "χώρας",
            "feedback": "χώρα is α pura (stam op ρ), dus gen. sg. = χώρας. De α blijft bewaard.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-DECL1-ALFA-003",
            "knoop_ids": ["GRC-G-MORF-DECL1-ALFA"],
            "type": "analyse",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.8,
            "discriminatie_initieel": 1.3,
            "verwachte_tijd_sec": 30,
            "stimulus": "Waarin verschilt θάλαττα (α impura) van χώρα in het enkelvoud?",
            "antwoord": [
                "in gen. en dat. sg. staat η i.p.v. α (θαλάττης, θαλάττῃ)",
                "gen./dat. sg. op -ης/-ῃ in plaats van -ας/-ᾳ",
            ],
            "feedback": "α impura volgt niet de ε/ι/ρ-regel: in gen./dat. sg. vervangt η de α (θαλάττης, θαλάττῃ). In het meervoud komt de α terug.",
            "bron": "handmatig",
        },
    ]

    items["GRC-G-MORF-DECL1-MASC"] = [
        {
            "id": "ITEM-GRC-G-MORF-DECL1-MASC-001",
            "knoop_ids": ["GRC-G-MORF-DECL1-MASC"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.2,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 15,
            "stimulus": "Op welke twee uitgangen kan de nominativus sg. van een masculinum van de 1e declinatie eindigen?",
            "antwoord": ["-ας en -ης", "-ας of -ης"],
            "feedback": "Masc. 1e decl.: νεανίας-type op -ας en κριτής-type op -ης. De rest van de naamvallen volgt de feminine vorm.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-DECL1-MASC-002",
            "knoop_ids": ["GRC-G-MORF-DECL1-MASC"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.6,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 25,
            "stimulus": "Geef de genitivus singularis van νεανίας.",
            "antwoord": "νεανίου",
            "feedback": "Mannelijke 1e declinatie leent de gen. sg. van de 2e declinatie: νεανίας → νεανίου. Uitzondering op het paradigma.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-DECL1-MASC-003",
            "knoop_ids": ["GRC-G-MORF-DECL1-MASC"],
            "type": "analyse",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.7,
            "discriminatie_initieel": 1.3,
            "verwachte_tijd_sec": 30,
            "stimulus": "Welke naamval is κριτοῦ en welke uitgang signaleert dat?",
            "antwoord": [
                "genitivus singularis, uitgang -ου",
                "gen. sg.; -ου",
            ],
            "feedback": "κριτοῦ is gen. sg. van κριτής: uitgang -ου, identiek aan de 2e declinatie. Zonder lidwoord makkelijk te verwarren met 2e decl.",
            "bron": "handmatig",
        },
    ]

    return items


def naamval_items() -> dict[str, list[dict]]:
    """NOM-D1, GEN-D1, DAT-D1, ACC-D1, VOC-D1 — 15 items."""
    items: dict[str, list[dict]] = {}

    items["GRC-G-MORF-NOM-D1"] = [
        {
            "id": "ITEM-GRC-G-MORF-NOM-D1-001",
            "knoop_ids": ["GRC-G-MORF-NOM-D1"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.3,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 12,
            "stimulus": "Welke uitgang heeft de nominativus pluralis in de 1e declinatie?",
            "antwoord": "-αι",
            "feedback": "Nom. pl. = -αι voor alle varianten: τιμαί, χῶραι, θάλατται, νεανίαι, κριταί. Let op: -αι is kort in de accentregels.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-NOM-D1-002",
            "knoop_ids": ["GRC-G-MORF-NOM-D1"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.3,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 25,
            "stimulus": "Geef de nominativus pluralis van τιμή.",
            "antwoord": "τιμαί",
            "feedback": "Nom. pl. van τιμή = τιμαί. De acutus op de ultima is de standaardpositie van het accent.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-NOM-D1-003",
            "knoop_ids": ["GRC-G-MORF-NOM-D1"],
            "type": "analyse",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.5,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 25,
            "stimulus": "Waarom krijgt χῶραι een circumflex op de penult en τιμαί niet?",
            "antwoord": [
                "omdat de lange penult ω bij een korte ultima -αι een circumflex eist",
                "lange penult + korte ultima → circumflex",
            ],
            "feedback": "Finale -αι telt als kort. Bij χώρα is de penult lang (ω), dus lange penult + korte ultima eist circumflex: χῶραι. Bij τιμή staat het accent al op de (nu kort geworden) ultima.",
            "bron": "handmatig",
        },
    ]

    items["GRC-G-MORF-GEN-D1"] = [
        {
            "id": "ITEM-GRC-G-MORF-GEN-D1-001",
            "knoop_ids": ["GRC-G-MORF-GEN-D1"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.1,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 12,
            "stimulus": "Welke uitgang heeft de genitivus pluralis in de 1e declinatie?",
            "antwoord": "-ῶν",
            "feedback": "Gen. pl. is voor alle woorden van de 1e declinatie -ῶν, altijd met circumflex: τιμῶν, χωρῶν, νεανιῶν.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-GEN-D1-002",
            "knoop_ids": ["GRC-G-MORF-GEN-D1"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.4,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 25,
            "stimulus": "Geef de genitivus pluralis van χώρα.",
            "antwoord": "χωρῶν",
            "feedback": "Gen. pl. = χωρῶν. De circumflex op -ῶν is een vast kenmerk van de 1e declinatie — betrouwbaarder dan -ῆς/-ας in het enkelvoud.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-GEN-D1-003",
            "knoop_ids": ["GRC-G-MORF-GEN-D1"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.2,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 15,
            "stimulus": "Welke naamval is τιμῆς?",
            "antwoord": ["genitivus singularis", "gen. sg."],
            "feedback": "τιμῆς is gen. sg. van τιμή — kenmerkend is -ῆς met circumflex. Niet verwarren met de acc. pl. τιμάς (met acutus).",
            "bron": "handmatig",
        },
    ]

    items["GRC-G-MORF-DAT-D1"] = [
        {
            "id": "ITEM-GRC-G-MORF-DAT-D1-001",
            "knoop_ids": ["GRC-G-MORF-DAT-D1"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.0,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 12,
            "stimulus": "Welk diakritisch teken kenmerkt de dativus sg. van de 1e declinatie?",
            "antwoord": ["iota subscriptum", "een iota onder de klinker"],
            "feedback": "Dat. sg. heeft altijd een iota subscriptum: τιμῇ, χώρᾳ, θαλάττῃ. Dit iota is stom maar kenmerkend.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-DAT-D1-002",
            "knoop_ids": ["GRC-G-MORF-DAT-D1"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.6,
            "discriminatie_initieel": 1.3,
            "verwachte_tijd_sec": 30,
            "stimulus": "Geef de dativus singularis en de dativus pluralis van χώρα.",
            "antwoord": [
                "χώρᾳ, χώραις",
                "χώρᾳ en χώραις",
            ],
            "feedback": "Dat. sg. = χώρᾳ (met iota subscriptum), dat. pl. = χώραις. In het meervoud geen iota subscriptum meer.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-DAT-D1-003",
            "knoop_ids": ["GRC-G-MORF-DAT-D1"],
            "type": "analyse",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.5,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 25,
            "stimulus": "Welke naamval is τιμαῖς?",
            "antwoord": ["dativus pluralis", "dat. pl."],
            "feedback": "τιμαῖς = dat. pl. van τιμή. Uitgang -αις met circumflex op de αι (lang) is typerend voor de dat. pl. van de 1e decl.",
            "bron": "handmatig",
        },
    ]

    items["GRC-G-MORF-ACC-D1"] = [
        {
            "id": "ITEM-GRC-G-MORF-ACC-D1-001",
            "knoop_ids": ["GRC-G-MORF-ACC-D1"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.1,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 12,
            "stimulus": "Welke uitgang heeft de accusativus singularis bij η-stammen?",
            "antwoord": "-ην",
            "feedback": "Acc. sg. van η-stammen: -ην (τιμήν). Bij α-stammen: -αν (χώραν, θάλατταν).",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-ACC-D1-002",
            "knoop_ids": ["GRC-G-MORF-ACC-D1"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.4,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 25,
            "stimulus": "Geef de accusativus pluralis van τιμή.",
            "antwoord": "τιμάς",
            "feedback": "Acc. pl. van τιμή = τιμάς (-άς lang). Niet verwarren met gen. sg. τιμῆς — ander accent én andere stamklinker.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-ACC-D1-003",
            "knoop_ids": ["GRC-G-MORF-ACC-D1"],
            "type": "analyse",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.6,
            "discriminatie_initieel": 1.3,
            "verwachte_tijd_sec": 25,
            "stimulus": "Welke naamval(len) kan χώρας zijn?",
            "antwoord": [
                "genitivus singularis of accusativus pluralis",
                "gen. sg. of acc. pl.",
            ],
            "feedback": "χώρας is ambivalent: gen. sg. (-ας kort) of acc. pl. (-ας lang). Lidwoord (τῆς vs. τάς) en context beslissen.",
            "bron": "handmatig",
        },
    ]

    items["GRC-G-MORF-VOC-D1"] = [
        {
            "id": "ITEM-GRC-G-MORF-VOC-D1-001",
            "knoop_ids": ["GRC-G-MORF-VOC-D1"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.2,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 12,
            "stimulus": "Hoe vormt een feminienum van de 1e declinatie de vocativus singularis?",
            "antwoord": [
                "gelijk aan de nominativus singularis",
                "identiek aan nom. sg.",
            ],
            "feedback": "Voc. sg. van fem. 1e decl. = nom. sg.: ὦ τιμή, ὦ χώρα. In het meervoud ook (τιμαί, χῶραι).",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-VOC-D1-002",
            "knoop_ids": ["GRC-G-MORF-VOC-D1"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.5,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 25,
            "stimulus": "Geef de vocativus singularis van νεανίας.",
            "antwoord": "νεανία",
            "feedback": "Masc. 1e decl. op -ας krijgt voc. sg. op korte α: νεανία. De nom. en voc. zijn hier dus niet identiek.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-VOC-D1-003",
            "knoop_ids": ["GRC-G-MORF-VOC-D1"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.4,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 15,
            "stimulus": "Wat is de vocativus singularis van κριτής?",
            "antwoord": "κριτά",
            "feedback": "κριτής-type vormt voc. sg. op -α: κριτά. Afwijkend van de nom. sg. — kenmerkend voor masc. 1e decl.",
            "bron": "handmatig",
        },
    ]

    return items


def paradigma_items() -> dict[str, list[dict]]:
    """DECL1-PARAD — 3 items (paradigma-drill)."""
    items: dict[str, list[dict]] = {}

    items["GRC-G-MORF-DECL1-PARAD"] = [
        {
            "id": "ITEM-GRC-G-MORF-DECL1-PARAD-001",
            "knoop_ids": ["GRC-G-MORF-DECL1-PARAD"],
            "type": "offline_schrijven",
            "richting": "productief",
            "moeilijkheid_initieel": 0.7,
            "discriminatie_initieel": 1.3,
            "verwachte_tijd_sec": 90,
            "stimulus": "Schrijf het volledige paradigma van τιμή op (alle vijf naamvallen, sg. en pl.) en vergelijk met je grammaticaboek.",
            "antwoord": "τιμή, τιμῆς, τιμῇ, τιμήν, τιμή | τιμαί, τιμῶν, τιμαῖς, τιμάς, τιμαί",
            "feedback": "Volledig: sg. τιμή / τιμῆς / τιμῇ / τιμήν / τιμή — pl. τιμαί / τιμῶν / τιμαῖς / τιμάς / τιμαί. Let op de circumflex op gen./dat. sg. en op gen. pl.",
            "bron": "handmatig",
            "verificatie_methode": "self_report",
            "verwacht_resultaat": "Paradigma van τιμή in 10 vormen, met correcte accenten (circumflex op τιμῆς, τιμῇ, τιμῶν, τιμαῖς).",
        },
        {
            "id": "ITEM-GRC-G-MORF-DECL1-PARAD-002",
            "knoop_ids": ["GRC-G-MORF-DECL1-PARAD"],
            "type": "analyse",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.8,
            "discriminatie_initieel": 1.3,
            "verwachte_tijd_sec": 35,
            "stimulus": "Analyseer χώραις volledig: naamval, getal en modelwoord-type.",
            "antwoord": [
                "dativus pluralis van χώρα (α-stam pura)",
                "dat. pl., α pura",
            ],
            "feedback": "χώραις = dat. pl. van χώρα (α-stam pura). Uitgang -αις is gelijk voor alle feminina 1e decl.; de behouden α verraadt de α pura.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-DECL1-PARAD-003",
            "knoop_ids": ["GRC-G-MORF-DECL1-PARAD"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.9,
            "discriminatie_initieel": 1.4,
            "verwachte_tijd_sec": 40,
            "stimulus": "Geef alle vier dativus-vormen (sg. en pl.) voor τιμή en χώρα.",
            "antwoord": [
                "τιμῇ, τιμαῖς, χώρᾳ, χώραις",
                "τιμῇ τιμαῖς χώρᾳ χώραις",
            ],
            "feedback": "Dat. sg. τιμῇ / χώρᾳ (iota subscriptum), dat. pl. τιμαῖς / χώραις. Zelfde uitgangen, alleen de stamklinker verschilt.",
            "bron": "handmatig",
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
    # NFC-normalize alle strings (stimulus, antwoord, feedback, verwacht_resultaat)
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
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    added = 0
    for knoop in data["knopen"]:
        if knoop["id"] in items_by_knoop:
            existing_ids = {item["id"] for item in knoop.get("items", [])}
            new_items = [
                item
                for item in items_by_knoop[knoop["id"]]
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
    for item_list in items_by_knoop.values():
        for item in item_list:
            type_counter[item["type"]] += 1
            richting_counter[item["richting"]] += 1

    print("\n=== E3-03 Summary ===")
    print(f"Knopen: {len(items_by_knoop)}")
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
