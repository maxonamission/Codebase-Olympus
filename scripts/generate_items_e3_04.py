#!/usr/bin/env python3
"""Generate exercise items for E3-04: GRC 2e declinatie (ο-stammen).

Target: data/graph/grc_grammatica_leerjaar1.json
Scope:  10 knopen rondom de 2e declinatie: DECL2-INTRO, DECL2-MASC, DECL2-NEUT,
        NOM-D2..VOC-D2, DECL2-NOUS en DECL2-PARAD.

Modelwoorden: ἄνθρωπος (m.), λόγος (m.), δῶρον (n.). De neutrum-regel
(nom = acc sg op -ον, nom = acc pl op -α) krijgt minstens 5 expliciete items.
Lidwoord-congruentie (ὁ, ἡ, τό) is verweven in masc/neut-items.
Productie-antwoorden zijn polytonisch en NFC-genormaliseerd voor compat met
frontend GreekInput.jsx.

Run:
    python scripts/generate_items_e3_04.py            # writes items to graph
    python scripts/generate_items_e3_04.py --dry-run  # only validate + print
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
# Item definitions per node.
# ---------------------------------------------------------------------------


def intro_masc_neut() -> dict[str, list[dict]]:
    """DECL2-INTRO, -MASC, -NEUT — 10 items, neutrum-regel krijgt 4."""
    items: dict[str, list[dict]] = {}

    items["GRC-G-MORF-DECL2-INTRO"] = [
        {
            "id": "ITEM-GRC-G-MORF-DECL2-INTRO-001",
            "knoop_ids": ["GRC-G-MORF-DECL2-INTRO"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.7,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 12,
            "stimulus": "Welke stamklinker kenmerkt de 2e declinatie?",
            "antwoord": ["ο", "o-stam"],
            "feedback": "De 2e declinatie heet ο-stammen. Modelwoorden: ἄνθρωπος, λόγος (m.), δῶρον (n.).",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-DECL2-INTRO-002",
            "knoop_ids": ["GRC-G-MORF-DECL2-INTRO"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.4,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 12,
            "stimulus": "Welke twee genera komen in de 2e declinatie voor?",
            "antwoord": [
                "masculinum en neutrum",
                "mannelijk en onzijdig",
            ],
            "feedback": "2e declinatie is overwegend masc. (ἄνθρωπος) of neut. (δῶρον). Femininum komt voor (ἡ ὁδός) maar is zeldzaam — dan volgt alleen het lidwoord het genus.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-DECL2-INTRO-003",
            "knoop_ids": ["GRC-G-MORF-DECL2-INTRO"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.0,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 15,
            "stimulus": "Hoe herken je in het woordenboek dat ὁ λόγος bij de 2e declinatie hoort?",
            "antwoord": [
                "aan de genitivus sg. op -ου",
                "λόγος, -ου → gen. sg. op -ου",
            ],
            "feedback": "Het lemma λόγος, -ου laat zien: gen. sg. op -ου is het onmiskenbare kenmerk van de 2e declinatie (m. of n.).",
            "bron": "handmatig",
        },
    ]

    items["GRC-G-MORF-DECL2-MASC"] = [
        {
            "id": "ITEM-GRC-G-MORF-DECL2-MASC-001",
            "knoop_ids": ["GRC-G-MORF-DECL2-MASC"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.4,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 12,
            "stimulus": "Welk lidwoord hoort bij ἄνθρωπος?",
            "antwoord": "ὁ",
            "feedback": "ἄνθρωπος is masculinum → lidwoord ὁ. Niet τό (dat zou neutrum zijn).",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-DECL2-MASC-002",
            "knoop_ids": ["GRC-G-MORF-DECL2-MASC"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.4,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 25,
            "stimulus": "Geef de genitivus singularis van λόγος.",
            "antwoord": "λόγου",
            "feedback": "Gen. sg. van λόγος = λόγου. De uitgang -ου is kenmerkend voor de 2e declinatie.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-DECL2-MASC-003",
            "knoop_ids": ["GRC-G-MORF-DECL2-MASC"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.3,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 25,
            "stimulus": "Geef de nominativus pluralis van ἄνθρωπος.",
            "antwoord": "ἄνθρωποι",
            "feedback": "Nom. pl. masc. = ἄνθρωποι (-οι). Accent blijft op de antepenult omdat -οι in accentregels als kort telt.",
            "bron": "handmatig",
        },
    ]

    items["GRC-G-MORF-DECL2-NEUT"] = [
        {
            "id": "ITEM-GRC-G-MORF-DECL2-NEUT-001",
            "knoop_ids": ["GRC-G-MORF-DECL2-NEUT"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.3,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 12,
            "stimulus": "Welke algemene regel geldt voor nom. en acc. bij elk neutrum?",
            "antwoord": [
                "nom. en acc. zijn altijd gelijk, zowel sg. als pl.",
                "nom = acc in sg en pl",
            ],
            "feedback": "Neutrum-regel: nom. = acc. — altijd, en voor alle declinaties. Context en lidwoord bepalen welke functie (onderwerp of lijdend voorwerp) de vorm vervult.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-DECL2-NEUT-002",
            "knoop_ids": ["GRC-G-MORF-DECL2-NEUT"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.1,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 12,
            "stimulus": "Op welke uitgang eindigt de nominativus en accusativus pluralis van een neutrum van de 2e declinatie?",
            "antwoord": "-α",
            "feedback": "Neutrum pl. nom./acc. eindigt op -α, niet op -οι of -ους. δῶρον → δῶρα.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-DECL2-NEUT-003",
            "knoop_ids": ["GRC-G-MORF-DECL2-NEUT"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.2,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 20,
            "stimulus": "Geef de accusativus singularis van δῶρον.",
            "antwoord": "δῶρον",
            "feedback": "Acc. sg. = δῶρον, identiek aan de nom. sg. Voor neutra geldt altijd nom = acc.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-DECL2-NEUT-004",
            "knoop_ids": ["GRC-G-MORF-DECL2-NEUT"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.3,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 20,
            "stimulus": "Geef de nominativus pluralis van δῶρον.",
            "antwoord": "δῶρα",
            "feedback": "Nom. pl. neut. = δῶρα (uitgang -α). Dezelfde vorm is ook acc. pl. (neutrum-regel).",
            "bron": "handmatig",
        },
    ]

    return items


def naamval_items() -> dict[str, list[dict]]:
    """NOM-D2, GEN-D2, DAT-D2, ACC-D2, VOC-D2 — 14 items."""
    items: dict[str, list[dict]] = {}

    items["GRC-G-MORF-NOM-D2"] = [
        {
            "id": "ITEM-GRC-G-MORF-NOM-D2-001",
            "knoop_ids": ["GRC-G-MORF-NOM-D2"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.4,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 12,
            "stimulus": "Welke uitgang heeft de nominativus pluralis bij een masculinum van de 2e declinatie?",
            "antwoord": "-οι",
            "feedback": "Nom. pl. masc. = -οι (ἄνθρωποι, λόγοι). Bij neutra is het -α (δῶρα).",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-NOM-D2-002",
            "knoop_ids": ["GRC-G-MORF-NOM-D2"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.3,
            "discriminatie_initieel": 1.3,
            "verwachte_tijd_sec": 18,
            "stimulus": "Welke naamval(len) kan δῶρα zijn?",
            "antwoord": [
                "nominativus of accusativus pluralis",
                "nom. pl. of acc. pl.",
            ],
            "feedback": "δῶρα is nom. pl. óf acc. pl. — de neutrum-regel maakt die vormen identiek. Context of lidwoord (τὰ δῶρα) beslist.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-NOM-D2-003",
            "knoop_ids": ["GRC-G-MORF-NOM-D2"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.4,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 25,
            "stimulus": "Geef de nominativus singularis met bepaald lidwoord voor λόγος.",
            "antwoord": [
                "ὁ λόγος",
                "ὁ λόγος (nom. sg. m.)",
            ],
            "feedback": "ὁ λόγος — masc. nom. sg. krijgt lidwoord ὁ. Het lidwoord is het beste genus-signaal.",
            "bron": "handmatig",
        },
    ]

    items["GRC-G-MORF-GEN-D2"] = [
        {
            "id": "ITEM-GRC-G-MORF-GEN-D2-001",
            "knoop_ids": ["GRC-G-MORF-GEN-D2"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.3,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 12,
            "stimulus": "Welke uitgang heeft de genitivus singularis in de 2e declinatie?",
            "antwoord": "-ου",
            "feedback": "Gen. sg. = -ου voor alle geslachten: λόγου, ἀνθρώπου, δώρου. Dit is hét kenmerk van de 2e declinatie.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-GEN-D2-002",
            "knoop_ids": ["GRC-G-MORF-GEN-D2"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.4,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 25,
            "stimulus": "Geef de genitivus pluralis van ἄνθρωπος.",
            "antwoord": "ἀνθρώπων",
            "feedback": "Gen. pl. = ἀνθρώπων (-ων). Accent verspringt naar de penult (wet van de drie lettergrepen: lange ultima -ων).",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-GEN-D2-003",
            "knoop_ids": ["GRC-G-MORF-GEN-D2"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.2,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 15,
            "stimulus": "Welke naamval is τοῦ δώρου?",
            "antwoord": ["genitivus singularis", "gen. sg."],
            "feedback": "τοῦ δώρου = gen. sg. van τὸ δῶρον. Lidwoord τοῦ (neut. gen. sg.) + uitgang -ου bevestigen de naamval.",
            "bron": "handmatig",
        },
    ]

    items["GRC-G-MORF-DAT-D2"] = [
        {
            "id": "ITEM-GRC-G-MORF-DAT-D2-001",
            "knoop_ids": ["GRC-G-MORF-DAT-D2"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.2,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 12,
            "stimulus": "Welke uitgang heeft de dativus singularis in de 2e declinatie?",
            "antwoord": ["-ῳ", "ω met iota subscriptum"],
            "feedback": "Dat. sg. = -ῳ (lange ω met iota subscriptum): λόγῳ, ἀνθρώπῳ, δώρῳ. Parallel met 1e decl. -ᾳ/-ῃ.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-DAT-D2-002",
            "knoop_ids": ["GRC-G-MORF-DAT-D2"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.5,
            "discriminatie_initieel": 1.3,
            "verwachte_tijd_sec": 30,
            "stimulus": "Geef de dativus sg. en dativus pl. van δῶρον.",
            "antwoord": [
                "δώρῳ, δώροις",
                "δώρῳ en δώροις",
            ],
            "feedback": "Dat. sg. = δώρῳ (iota subscriptum), dat. pl. = δώροις (-οις). Neutrum volgt hier het masculine patroon; alleen nom./acc. wijken af.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-DAT-D2-003",
            "knoop_ids": ["GRC-G-MORF-DAT-D2"],
            "type": "analyse",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.4,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 20,
            "stimulus": "Welke naamval is λόγοις?",
            "antwoord": ["dativus pluralis", "dat. pl."],
            "feedback": "λόγοις = dat. pl. van λόγος. Uitgang -οις is in de 2e decl. altijd dat. pl. (m. of n.).",
            "bron": "handmatig",
        },
    ]

    items["GRC-G-MORF-ACC-D2"] = [
        {
            "id": "ITEM-GRC-G-MORF-ACC-D2-001",
            "knoop_ids": ["GRC-G-MORF-ACC-D2"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.1,
            "discriminatie_initieel": 1.1,
            "verwachte_tijd_sec": 12,
            "stimulus": "Welke uitgang heeft de accusativus pluralis bij een masculinum van de 2e declinatie?",
            "antwoord": "-ους",
            "feedback": "Acc. pl. masc. = -ους (λόγους, ἀνθρώπους). Bij neutra staat daar -α (δῶρα) — de neutrum-regel.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-ACC-D2-002",
            "knoop_ids": ["GRC-G-MORF-ACC-D2"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.5,
            "discriminatie_initieel": 1.3,
            "verwachte_tijd_sec": 25,
            "stimulus": "Geef de accusativus singularis van ἄνθρωπος.",
            "antwoord": "ἄνθρωπον",
            "feedback": "Acc. sg. = ἄνθρωπον (uitgang -ον). Niet verwarren met neut. nom. sg. die óók op -ον eindigt — lidwoord (τόν vs. τό) beslist.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-ACC-D2-003",
            "knoop_ids": ["GRC-G-MORF-ACC-D2"],
            "type": "analyse",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.6,
            "discriminatie_initieel": 1.3,
            "verwachte_tijd_sec": 25,
            "stimulus": "In welke naamval staat het tweede woord van de frase τὰ δῶρα?",
            "antwoord": [
                "nominativus of accusativus pluralis",
                "nom. of acc. pl.",
            ],
            "feedback": "τὰ δῶρα: lidwoord τά is nom./acc. pl. neut. De neutrum-regel maakt beide vormen identiek — context van de zin geeft de functie.",
            "bron": "handmatig",
        },
    ]

    items["GRC-G-MORF-VOC-D2"] = [
        {
            "id": "ITEM-GRC-G-MORF-VOC-D2-001",
            "knoop_ids": ["GRC-G-MORF-VOC-D2"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.0,
            "discriminatie_initieel": 1.1,
            "verwachte_tijd_sec": 15,
            "stimulus": "Welke uitgang heeft de vocativus singularis van een masculinum op -ος?",
            "antwoord": "-ε",
            "feedback": "Masc. 2e decl. krijgt voc. sg. op -ε: ὦ ἄνθρωπε, ὦ λόγε. Dit is de enige declinatie waar voc. sg. duidelijk afwijkt van nom. sg.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-VOC-D2-002",
            "knoop_ids": ["GRC-G-MORF-VOC-D2"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.4,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 20,
            "stimulus": "Geef de vocativus singularis van ἄνθρωπος.",
            "antwoord": "ἄνθρωπε",
            "feedback": "Voc. sg. = ἄνθρωπε (uitgang -ε). Neutrum heeft geen aparte voc.: die is gelijk aan de nom. (= acc.).",
            "bron": "handmatig",
        },
    ]

    return items


def nous_en_paradigma() -> dict[str, list[dict]]:
    """DECL2-NOUS (2) + DECL2-PARAD (4) — 6 items."""
    items: dict[str, list[dict]] = {}

    items["GRC-G-MORF-DECL2-NOUS"] = [
        {
            "id": "ITEM-GRC-G-MORF-DECL2-NOUS-001",
            "knoop_ids": ["GRC-G-MORF-DECL2-NOUS"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.3,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 15,
            "stimulus": "Uit welke vormsamensmelting is νοῦς ontstaan?",
            "antwoord": [
                "νόος (contractie ο+ο → ου)",
                "νόος → νοῦς",
            ],
            "feedback": "νοῦς is een contractum: de stam νόο- trekt samen (ο+ο → ου). De hele verbuiging volgt hetzelfde samentrekkingspatroon.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-DECL2-NOUS-002",
            "knoop_ids": ["GRC-G-MORF-DECL2-NOUS"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.7,
            "discriminatie_initieel": 1.3,
            "verwachte_tijd_sec": 30,
            "stimulus": "Geef de genitivus singularis van νοῦς.",
            "antwoord": "νοῦ",
            "feedback": "Gen. sg. = νοῦ (< νόου, met contractie ο+ου → ου). Korte paradigma: νοῦς, νοῦ, νῷ, νοῦν, νοῦ.",
            "bron": "handmatig",
        },
    ]

    items["GRC-G-MORF-DECL2-PARAD"] = [
        {
            "id": "ITEM-GRC-G-MORF-DECL2-PARAD-001",
            "knoop_ids": ["GRC-G-MORF-DECL2-PARAD"],
            "type": "offline_schrijven",
            "richting": "productief",
            "moeilijkheid_initieel": 0.7,
            "discriminatie_initieel": 1.3,
            "verwachte_tijd_sec": 90,
            "stimulus": "Schrijf het volledige paradigma van ἄνθρωπος op (5 naamvallen sg. en pl.) en vergelijk met je grammaticaboek.",
            "antwoord": "ἄνθρωπος, ἀνθρώπου, ἀνθρώπῳ, ἄνθρωπον, ἄνθρωπε | ἄνθρωποι, ἀνθρώπων, ἀνθρώποις, ἀνθρώπους, ἄνθρωποι",
            "feedback": "Volledig: sg. ἄνθρωπος / ἀνθρώπου / ἀνθρώπῳ / ἄνθρωπον / ἄνθρωπε — pl. ἄνθρωποι / ἀνθρώπων / ἀνθρώποις / ἀνθρώπους / ἄνθρωποι. Let op accentverspringing bij lange ultima (-ου, -ῳ, -ων, -οις, -ους).",
            "bron": "handmatig",
            "verificatie_methode": "self_report",
            "verwacht_resultaat": "10 vormen van ἄνθρωπος, correcte accenten (antepenult voor -ος, -ον, -ε, -οι; penult voor lange ultima).",
        },
        {
            "id": "ITEM-GRC-G-MORF-DECL2-PARAD-002",
            "knoop_ids": ["GRC-G-MORF-DECL2-PARAD"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.5,
            "discriminatie_initieel": 1.3,
            "verwachte_tijd_sec": 30,
            "stimulus": "Geef de nominativus singularis met bepaald lidwoord voor ἄνθρωπος, λόγος én δῶρον.",
            "antwoord": [
                "ὁ ἄνθρωπος, ὁ λόγος, τὸ δῶρον",
                "ὁ ἄνθρωπος — ὁ λόγος — τὸ δῶρον",
            ],
            "feedback": "ὁ ἄνθρωπος, ὁ λόγος (masc. → ὁ), τὸ δῶρον (neut. → τό). Het lidwoord is het betrouwbaarste genus-signaal in de 2e declinatie.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-DECL2-PARAD-003",
            "knoop_ids": ["GRC-G-MORF-DECL2-PARAD"],
            "type": "analyse",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.7,
            "discriminatie_initieel": 1.3,
            "verwachte_tijd_sec": 30,
            "stimulus": "Analyseer τοῖς δώροις volledig: lidwoord, naamval, getal, genus.",
            "antwoord": [
                "dativus pluralis neutrum",
                "dat. pl. neut. (lidwoord τοῖς + δώροις)",
            ],
            "feedback": "τοῖς δώροις = dat. pl. neut. Lidwoord τοῖς is dat. pl. (m./n. samen); uitgang -οις bevestigt dat. pl. in de 2e decl.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-DECL2-PARAD-004",
            "knoop_ids": ["GRC-G-MORF-DECL2-PARAD"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.8,
            "discriminatie_initieel": 1.4,
            "verwachte_tijd_sec": 40,
            "stimulus": "Geef van δῶρον alle vier de nom./acc.-vormen (sg. en pl., met lidwoord).",
            "antwoord": [
                "τὸ δῶρον, τὰ δῶρα, τὸ δῶρον, τὰ δῶρα",
                "sg. τὸ δῶρον — pl. τὰ δῶρα (nom. = acc.)",
            ],
            "feedback": "Nom. = acc. voor neutra: sg. τὸ δῶρον, pl. τὰ δῶρα. Lidwoord τό/τά verraadt genus en naamval ineen.",
            "bron": "handmatig",
        },
    ]

    return items


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------


def collect_all() -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {}
    out.update(intro_masc_neut())
    out.update(naamval_items())
    out.update(nous_en_paradigma())
    for _node_id, item_list in out.items():
        for item in item_list:
            for key in ("stimulus", "antwoord", "feedback", "verwacht_resultaat"):
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
    for node in data["knopen"]:
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
            richting_counter[item["richting"]] += 1

    print("\n=== E3-04 Summary ===")
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
