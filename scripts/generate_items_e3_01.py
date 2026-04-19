#!/usr/bin/env python3
"""Generate exercise items for E3-01: GRC alphabet rest-knopen.

Target: data/graph/grc_alfabet.json
Scope:  the 23 alphabet nodes without items (INTRO, groeperingen, diakritiek,
        lettercombinaties). The 24 letter-knopen (GRC-G-FONL-ALFA-<LETTER>)
        already have items — those are left untouched.

Run:
    python scripts/generate_items_e3_01.py            # writes items to graph
    python scripts/generate_items_e3_01.py --dry-run  # only validate + print

Total: ~50 items, each node gets at least 2 (target 2-3).
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from gymnasium_classica.models.graph import Item

# ---------------------------------------------------------------------------
# Item definitions — split into thematic groups to keep each block readable.
# ---------------------------------------------------------------------------


def alfabet_intro_en_groepen() -> dict[str, list[dict]]:
    """Items for ALFA-INTRO and ALFA-GRP1…4 (5 knopen, ~10 items)."""
    items: dict[str, list[dict]] = {}

    items["GRC-G-FONL-ALFA-INTRO"] = [
        {
            "id": "ITEM-GRC-G-FONL-ALFA-INTRO-001",
            "knoop_ids": ["GRC-G-FONL-ALFA-INTRO"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -1.0,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 10,
            "stimulus": "Uit hoeveel letters bestaat het Griekse alfabet?",
            "antwoord": "24",
            "feedback": "Het Griekse alfabet telt 24 letters — van alfa (α) tot omega (ω).",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-FONL-ALFA-INTRO-002",
            "knoop_ids": ["GRC-G-FONL-ALFA-INTRO"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.5,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 15,
            "stimulus": "In welke vier groepen worden de Griekse letters hier verdeeld op basis van herkenbaarheid?",
            "antwoord": [
                "identieke letters, afwijkende vorm maar bekende klank, valse vrienden, unieke letters",
                "identiek, bekende klank, valse vrienden, uniek",
            ],
            "feedback": "Vier groepen: (1) identiek aan Latijn, (2) afwijkende vorm maar bekende klank, (3) valse vrienden, (4) uniek Griekse letters.",
            "bron": "handmatig",
        },
    ]

    items["GRC-G-FONL-ALFA-GRP1"] = [
        {
            "id": "ITEM-GRC-G-FONL-ALFA-GRP1-001",
            "knoop_ids": ["GRC-G-FONL-ALFA-GRP1"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.8,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 12,
            "stimulus": "Welke Griekse letter is identiek aan de Latijnse A in vorm én klank?",
            "antwoord": "alfa",
            "feedback": "Α/α (alfa) is identiek aan de Latijnse A in vorm en klank.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-FONL-ALFA-GRP1-002",
            "knoop_ids": ["GRC-G-FONL-ALFA-GRP1"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.3,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 15,
            "stimulus": "Welke letter hoort NIET bij groep 1 (identieke letters): Α, Κ, Θ, Μ?",
            "antwoord": "Θ",
            "feedback": "Θ (thèta) hoort bij groep 4 (uniek Grieks). Α, Κ en Μ zijn identiek aan Latijnse A, K en M.",
            "bron": "handmatig",
        },
    ]

    items["GRC-G-FONL-ALFA-GRP2"] = [
        {
            "id": "ITEM-GRC-G-FONL-ALFA-GRP2-001",
            "knoop_ids": ["GRC-G-FONL-ALFA-GRP2"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.4,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 15,
            "stimulus": "Hoe klinkt Γ (gamma) in het Grieks?",
            "antwoord": "g",
            "feedback": "Γ/γ (gamma) heeft een afwijkende vorm maar de bekende g-klank.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-FONL-ALFA-GRP2-002",
            "knoop_ids": ["GRC-G-FONL-ALFA-GRP2"],
            "type": "analyse",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.2,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 25,
            "stimulus": "Welke drie letters hebben een afwijkende Griekse vorm maar een Nederlandse/Latijnse klank? Kies uit: Γ, Η, Λ, Ρ, Σ.",
            "antwoord": ["Γ, Λ, Σ", "gamma, lambda, sigma"],
            "feedback": "Γ=g, Λ=l, Σ=s: afwijkende vorm, bekende klank. Η is een valse vriend (=lange e), Ρ klinkt als r.",
            "bron": "handmatig",
        },
    ]

    items["GRC-G-FONL-ALFA-GRP3"] = [
        {
            "id": "ITEM-GRC-G-FONL-ALFA-GRP3-001",
            "knoop_ids": ["GRC-G-FONL-ALFA-GRP3"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.2,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 15,
            "stimulus": "De Griekse letter Η lijkt op de Latijnse H. Hoe klinkt Η in het Grieks?",
            "antwoord": ["lange e", "ē"],
            "feedback": "Η/η (èta) is een valse vriend: vorm van een H, maar klinkt als lange e (ē).",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-FONL-ALFA-GRP3-002",
            "knoop_ids": ["GRC-G-FONL-ALFA-GRP3"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.0,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 15,
            "stimulus": "Hoe klinkt Ρ (rho) — als p of als r?",
            "antwoord": "r",
            "feedback": "Ρ/ρ (rho) is een valse vriend: vorm van een P, klinkt als r.",
            "bron": "handmatig",
        },
    ]

    items["GRC-G-FONL-ALFA-GRP4"] = [
        {
            "id": "ITEM-GRC-G-FONL-ALFA-GRP4-001",
            "knoop_ids": ["GRC-G-FONL-ALFA-GRP4"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.3,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 15,
            "stimulus": "Welke klank heeft Θ (thèta) in de Erasmiaanse uitspraak?",
            "antwoord": ["th", "tʰ"],
            "feedback": "Θ/θ (thèta) is een unieke Griekse letter: aspirata, klinkt als th.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-FONL-ALFA-GRP4-002",
            "knoop_ids": ["GRC-G-FONL-ALFA-GRP4"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.0,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 15,
            "stimulus": "Welke letter staat voor de klank /ps/: Ξ, Φ, Ψ of Χ?",
            "antwoord": "Ψ",
            "feedback": "Ψ/ψ (psi) = /ps/. Ξ = /ks/, Φ = /ph/, Χ = /kh/.",
            "bron": "handmatig",
        },
    ]

    return items


def diakritiek_items() -> dict[str, list[dict]]:
    """Items for DIAK-* knopen (9 stuks, ~18 items)."""
    items: dict[str, list[dict]] = {}

    items["GRC-G-FONL-DIAK-INTRO"] = [
        {
            "id": "ITEM-GRC-G-FONL-DIAK-INTRO-001",
            "knoop_ids": ["GRC-G-FONL-DIAK-INTRO"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.6,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 15,
            "stimulus": "Welke drie soorten diakritische tekens kent het polytoon Grieks?",
            "antwoord": [
                "spiritus, accenten en iota subscriptum",
                "ademtekens, accenten en iota subscriptum",
            ],
            "feedback": "Polytoon Grieks heeft drie soorten: spiritus (asper/lenis), accenten (acutus/gravis/circumflexus) en iota subscriptum.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-FONL-DIAK-INTRO-002",
            "knoop_ids": ["GRC-G-FONL-DIAK-INTRO"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.3,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 15,
            "stimulus": "Waarom schrijven we diakritische tekens bij polytoon Grieks?",
            "antwoord": "om uitspraak en betekenis precies vast te leggen (h-klank, klemtoon, lange klinker)",
            "feedback": "Diakritieken noteren klankinformatie die niet in de letters zelf zit: ademteken (h/geen h), accent (klemtoon) en iota subscriptum (historische klinker).",
            "bron": "handmatig",
        },
    ]

    items["GRC-G-FONL-DIAK-SPIR"] = [
        {
            "id": "ITEM-GRC-G-FONL-DIAK-SPIR-001",
            "knoop_ids": ["GRC-G-FONL-DIAK-SPIR"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.4,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 12,
            "stimulus": "Welke twee spiritus-tekens zijn er in het Grieks?",
            "antwoord": ["asper en lenis", "spiritus asper en spiritus lenis"],
            "feedback": "Twee spiritus-tekens: asper (ruw, ῾ = h-klank) en lenis (zacht, ᾿ = geen h-klank).",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-FONL-DIAK-SPIR-002",
            "knoop_ids": ["GRC-G-FONL-DIAK-SPIR"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.1,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 15,
            "stimulus": "Welke letters krijgen altijd een spiritus aan het begin van een woord?",
            "antwoord": "elke beginklinker en initiële ρ",
            "feedback": "Elke woordinitiële klinker krijgt een spiritus (asper of lenis); initiële ρ krijgt altijd asper (ῥ).",
            "bron": "handmatig",
        },
    ]

    items["GRC-G-FONL-DIAK-ASPER"] = [
        {
            "id": "ITEM-GRC-G-FONL-DIAK-ASPER-001",
            "knoop_ids": ["GRC-G-FONL-DIAK-ASPER"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.3,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 12,
            "stimulus": "Wat betekent spiritus asper voor de uitspraak?",
            "antwoord": ["h-klank toevoegen vóór de klinker", "h-klank"],
            "feedback": "Spiritus asper (῾) geeft een h-klank vóór de woordinitiële klinker of ρ: ἁμαρτία = hamartia.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-FONL-DIAK-ASPER-002",
            "knoop_ids": ["GRC-G-FONL-DIAK-ASPER"],
            "type": "analyse",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.1,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 20,
            "stimulus": "Welk woord begint met spiritus asper: ἀγαθός, ἁμαρτία, εἰρήνη of ἔργον?",
            "antwoord": "ἁμαρτία",
            "feedback": "ἁμαρτία heeft spiritus asper (῾) → h-klank. De andere drie hebben spiritus lenis (᾿) → geen h.",
            "bron": "handmatig",
        },
    ]

    items["GRC-G-FONL-DIAK-LENIS"] = [
        {
            "id": "ITEM-GRC-G-FONL-DIAK-LENIS-001",
            "knoop_ids": ["GRC-G-FONL-DIAK-LENIS"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.3,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 12,
            "stimulus": "Wat betekent spiritus lenis voor de uitspraak?",
            "antwoord": ["geen h-klank", "geen extra klank"],
            "feedback": "Spiritus lenis (᾿) markeert de afwezigheid van de h-klank: ἀγαθός = agathos, niet hagathos.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-FONL-DIAK-LENIS-002",
            "knoop_ids": ["GRC-G-FONL-DIAK-LENIS"],
            "type": "analyse",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.1,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 18,
            "stimulus": "Hoe spreek je ἄνθρωπος aan het begin uit (Erasmiaans)?",
            "antwoord": ["an-thropos", "ἄνθρωπος begint met een a, zonder h"],
            "feedback": "ἄνθρωπος heeft spiritus lenis op α: dus 'an-thropos', niet 'han-thropos'.",
            "bron": "handmatig",
        },
    ]

    items["GRC-G-FONL-DIAK-ACC"] = [
        {
            "id": "ITEM-GRC-G-FONL-DIAK-ACC-001",
            "knoop_ids": ["GRC-G-FONL-DIAK-ACC"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.5,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 12,
            "stimulus": "Welke drie accenten kent het polytoon Grieks?",
            "antwoord": [
                "acutus, gravis en circumflexus",
                "acutus (´), gravis (`) en circumflexus (῀)",
            ],
            "feedback": "Drie accenten: acutus (´), gravis (`) en circumflexus (῀ of ˜). Oorspronkelijk toonhoogte-accenten.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-FONL-DIAK-ACC-002",
            "knoop_ids": ["GRC-G-FONL-DIAK-ACC"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.1,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 15,
            "stimulus": "Op welke lettergrepen kan een accent in het Grieks vallen?",
            "antwoord": [
                "een van de laatste drie lettergrepen",
                "ultima, penultima of antepenultima",
            ],
            "feedback": "Accenten vallen alleen op een van de laatste drie lettergrepen: antepenultima, penultima of ultima.",
            "bron": "handmatig",
        },
    ]

    items["GRC-G-FONL-DIAK-ACUT"] = [
        {
            "id": "ITEM-GRC-G-FONL-DIAK-ACUT-001",
            "knoop_ids": ["GRC-G-FONL-DIAK-ACUT"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.2,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 12,
            "stimulus": "Op welke drie lettergrepen kan acutus (´) voorkomen?",
            "antwoord": [
                "antepenultima, penultima, ultima",
                "een van de laatste drie lettergrepen",
            ],
            "feedback": "Acutus kan op antepenultima, penultima of ultima staan — met restricties op lettergreeplengte.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-FONL-DIAK-ACUT-002",
            "knoop_ids": ["GRC-G-FONL-DIAK-ACUT"],
            "type": "analyse",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.3,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 20,
            "stimulus": "Welk woord heeft een acutus: λόγος, λόγων, θεῶν of θεός?",
            "antwoord": ["λόγος", "θεός"],
            "feedback": "λόγος (penultima) en θεός (ultima) hebben acutus. λόγων heeft ook acutus maar op andere plaats; θεῶν heeft circumflexus.",
            "bron": "handmatig",
        },
    ]

    items["GRC-G-FONL-DIAK-GRAV"] = [
        {
            "id": "ITEM-GRC-G-FONL-DIAK-GRAV-001",
            "knoop_ids": ["GRC-G-FONL-DIAK-GRAV"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.0,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 15,
            "stimulus": "Wanneer verandert een acutus op de ultima in een gravis?",
            "antwoord": [
                "wanneer een ander woord volgt (zonder leesteken)",
                "voor een volgend woord",
            ],
            "feedback": "Acutus op de ultima wordt gravis wanneer direct een ander woord volgt zonder leesteken: τὸν νόμον (niet τόν).",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-FONL-DIAK-GRAV-002",
            "knoop_ids": ["GRC-G-FONL-DIAK-GRAV"],
            "type": "analyse",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.2,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 20,
            "stimulus": "Op welke lettergreep staat de gravis altijd?",
            "antwoord": ["ultima", "de laatste lettergreep"],
            "feedback": "Gravis staat altijd op de ultima en vervangt daar een acutus vóór een volgend woord.",
            "bron": "handmatig",
        },
    ]

    items["GRC-G-FONL-DIAK-CIRCU"] = [
        {
            "id": "ITEM-GRC-G-FONL-DIAK-CIRCU-001",
            "knoop_ids": ["GRC-G-FONL-DIAK-CIRCU"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.0,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 15,
            "stimulus": "Op welke klinkers kan circumflexus (῀) voorkomen?",
            "antwoord": ["alleen op lange klinkers en diftongen", "lange klinkers of diftongen"],
            "feedback": "Circumflexus staat alleen op lange klinkers (η, ω, soms α/ι/υ als lang) of diftongen, en alleen op penultima of ultima.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-FONL-DIAK-CIRCU-002",
            "knoop_ids": ["GRC-G-FONL-DIAK-CIRCU"],
            "type": "analyse",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.4,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 25,
            "stimulus": "Waarom kan circumflexus nooit op een antepenultima staan?",
            "antwoord": [
                "omdat een circumflexus een lange klinker vereist en niet verder dan de penultima valt",
                "regel: circumflexus alleen op de laatste twee lettergrepen",
            ],
            "feedback": "De circumflexus vereist een lange klinker én valt alleen op een van de laatste twee lettergrepen. Antepenultima ligt te ver van het woordeinde.",
            "bron": "handmatig",
        },
    ]

    items["GRC-G-FONL-DIAK-IOTSU"] = [
        {
            "id": "ITEM-GRC-G-FONL-DIAK-IOTSU-001",
            "knoop_ids": ["GRC-G-FONL-DIAK-IOTSU"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.3,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 12,
            "stimulus": "Onder welke drie klinkers kan de iota subscriptum staan?",
            "antwoord": ["α, η en ω", "ᾳ, ῃ, ῳ"],
            "feedback": "Iota subscriptum verschijnt onder α, η en ω (ᾳ, ῃ, ῳ) — historisch een diftong, in Erasmiaanse uitspraak niet gerealiseerd.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-FONL-DIAK-IOTSU-002",
            "knoop_ids": ["GRC-G-FONL-DIAK-IOTSU"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.0,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 15,
            "stimulus": "In welke naamval verschijnt de iota subscriptum vaak bij 1e en 2e declinatie?",
            "antwoord": ["dativus singularis", "dativus enkelvoud"],
            "feedback": "De dativus singularis in 1e en 2e declinatie eindigt op ᾳ/ῃ/ῳ — voor τιμή wordt het τιμῇ, voor λόγος λόγῳ.",
            "bron": "handmatig",
        },
    ]

    items["GRC-G-FONL-DIAK-CORON"] = [
        {
            "id": "ITEM-GRC-G-FONL-DIAK-CORON-001",
            "knoop_ids": ["GRC-G-FONL-DIAK-CORON"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.2,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 15,
            "stimulus": "Wat markeert de coronis?",
            "antwoord": ["crasis (samentrekking van twee woorden)", "crasis"],
            "feedback": "De coronis (᾿) markeert crasis: twee woorden trekken samen, zoals καὶ ἐγώ → κἀγώ.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-FONL-DIAK-CORON-002",
            "knoop_ids": ["GRC-G-FONL-DIAK-CORON"],
            "type": "analyse",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.5,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 25,
            "stimulus": "Welke twee woorden gaan samen in κἀγώ?",
            "antwoord": ["καί en ἐγώ", "καὶ + ἐγώ"],
            "feedback": "κἀγώ = καί + ἐγώ. De coronis markeert deze samentrekking.",
            "bron": "handmatig",
        },
    ]

    return items


def kombi_items() -> dict[str, list[dict]]:
    """Items for KOMBI-* knopen (8 stuks, ~17 items)."""
    items: dict[str, list[dict]] = {}

    items["GRC-G-FONL-KOMBI-INTRO"] = [
        {
            "id": "ITEM-GRC-G-FONL-KOMBI-INTRO-001",
            "knoop_ids": ["GRC-G-FONL-KOMBI-INTRO"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.4,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 15,
            "stimulus": "Welke drie soorten lettercombinaties spelen een rol in het Grieks?",
            "antwoord": [
                "diftongen, nasaal-gamma en dubbele medeklinkers",
                "diftongen, nasaal-γ, dubbele medeklinkers",
            ],
            "feedback": "Drie relevante groepen: diftongen (αι, ει, οι, …), nasaal-gamma (γγ, γκ, γχ, γξ) en dubbele medeklinkers (ζ, ξ, ψ).",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-FONL-KOMBI-INTRO-002",
            "knoop_ids": ["GRC-G-FONL-KOMBI-INTRO"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.1,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 15,
            "stimulus": "Waarom is het belangrijk om lettercombinaties te leren naast losse letters?",
            "antwoord": "omdat een combinatie vaak een andere klank geeft dan de losse letters",
            "feedback": "Combinaties als ου, γγ en ξ hebben klanken die je niet zomaar uit de losse letters afleidt.",
            "bron": "handmatig",
        },
    ]

    items["GRC-G-FONL-KOMBI-DIFTE"] = [
        {
            "id": "ITEM-GRC-G-FONL-KOMBI-DIFTE-001",
            "knoop_ids": ["GRC-G-FONL-KOMBI-DIFTE"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.5,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 15,
            "stimulus": "Welke diftong klinkt in Erasmiaanse uitspraak als /oe/ (lang)?",
            "antwoord": "ου",
            "feedback": "De diftong ου is in Erasmiaans /oː/ (lang oe), zoals in Nederlands 'boer'. Een monoftongale diftong.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-FONL-KOMBI-DIFTE-002",
            "knoop_ids": ["GRC-G-FONL-KOMBI-DIFTE"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.2,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 15,
            "stimulus": "Hoe klinken αι, ει en οι in Erasmiaans Grieks?",
            "antwoord": ["als ai, ei en oi", "αι=ai, ει=ei, οι=oi"],
            "feedback": "Echte diftongen met korte eerste klinker: αι=/ai/, ει=/ei/, οι=/oi/. De tweede letter is altijd ι.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-FONL-KOMBI-DIFTE-003",
            "knoop_ids": ["GRC-G-FONL-KOMBI-DIFTE"],
            "type": "analyse",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.2,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 25,
            "stimulus": "Welke diftong zit er in het woord παιδεία?",
            "antwoord": ["αι en ει", "αι, ει"],
            "feedback": "παιδεία bevat twee diftongen: παι- (αι) en -δεί- (ει), uitgesproken als 'pai-dei-a'.",
            "bron": "handmatig",
        },
    ]

    items["GRC-G-FONL-KOMBI-DIFTO"] = [
        {
            "id": "ITEM-GRC-G-FONL-KOMBI-DIFTO-001",
            "knoop_ids": ["GRC-G-FONL-KOMBI-DIFTO"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.1,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 15,
            "stimulus": "Wat onderscheidt een oneigenlijke diftong van een echte?",
            "antwoord": ["de eerste klinker is lang", "lange eerste klinker"],
            "feedback": "Oneigenlijke diftongen hebben een lange eerste klinker: ηυ, υι en de iota-subscriptum-vormen ᾳ, ῃ, ῳ.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-FONL-KOMBI-DIFTO-002",
            "knoop_ids": ["GRC-G-FONL-KOMBI-DIFTO"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.2,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 15,
            "stimulus": "Zijn de iota-subscriptum-vormen ᾳ, ῃ en ῳ echte of oneigenlijke diftongen?",
            "antwoord": ["oneigenlijke diftongen", "oneigenlijk"],
            "feedback": "ᾳ, ῃ, ῳ zijn oneigenlijke diftongen: lange klinker + geschreven iota die niet uitgesproken wordt.",
            "bron": "handmatig",
        },
    ]

    items["GRC-G-FONL-KOMBI-NASAL"] = [
        {
            "id": "ITEM-GRC-G-FONL-KOMBI-NASAL-001",
            "knoop_ids": ["GRC-G-FONL-KOMBI-NASAL"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.0,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 15,
            "stimulus": "Hoe klinkt γγ in het Grieks?",
            "antwoord": ["ng (/ŋɡ/)", "ng"],
            "feedback": "Voor een andere velaar (γ, κ, χ, ξ) klinkt γ als nasaal /ŋ/. γγ = /ŋɡ/, zoals in Nederlands 'angel'.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-FONL-KOMBI-NASAL-002",
            "knoop_ids": ["GRC-G-FONL-KOMBI-NASAL"],
            "type": "analyse",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.3,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 20,
            "stimulus": "Hoe spreek je het woord ἄγγελος uit (Erasmiaans)?",
            "antwoord": ["angelos", "an-ge-los met ng-klank"],
            "feedback": "ἄγγελος = 'an-ge-los'. De eerste γ in γγ wordt nasaal /ŋ/.",
            "bron": "handmatig",
        },
    ]

    items["GRC-G-FONL-KOMBI-DUBBL"] = [
        {
            "id": "ITEM-GRC-G-FONL-KOMBI-DUBBL-001",
            "knoop_ids": ["GRC-G-FONL-KOMBI-DUBBL"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.3,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 12,
            "stimulus": "Welke drie Griekse letters zijn dubbele medeklinkers?",
            "antwoord": ["ζ, ξ en ψ", "zèta, xi, psi"],
            "feedback": "Drie dubbele medeklinkers: ζ (/zd/ of /dz/), ξ (/ks/) en ψ (/ps/).",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-FONL-KOMBI-DUBBL-002",
            "knoop_ids": ["GRC-G-FONL-KOMBI-DUBBL"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.0,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 15,
            "stimulus": "Welke Griekse letter spreek je uit als /ks/?",
            "antwoord": "ξ",
            "feedback": "ξ (xi) = /ks/, zoals in ξένος = 'ksenos'.",
            "bron": "handmatig",
        },
    ]

    items["GRC-G-FONL-KOMBI-ASPIR"] = [
        {
            "id": "ITEM-GRC-G-FONL-KOMBI-ASPIR-001",
            "knoop_ids": ["GRC-G-FONL-KOMBI-ASPIR"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.2,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 12,
            "stimulus": "Welke drie letters zijn de geaspireerde medeklinkers in het Grieks?",
            "antwoord": ["θ, φ en χ", "thèta, phi, chi"],
            "feedback": "De geaspireerde medeklinkers zijn θ (/tʰ/), φ (/pʰ/) en χ (/kʰ/). Erasmiaans met hoorbare adem.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-FONL-KOMBI-ASPIR-002",
            "knoop_ids": ["GRC-G-FONL-KOMBI-ASPIR"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.0,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 15,
            "stimulus": "Hoe klinkt χ in de Erasmiaanse uitspraak?",
            "antwoord": ["kh (/kʰ/)", "k met adem", "geaspireerde k"],
            "feedback": "χ = /kʰ/: een k met hoorbare adem erachter. Niet de harde Nederlandse 'ch' van 'lachen'.",
            "bron": "handmatig",
        },
    ]

    items["GRC-G-FONL-KOMBI-KWANT"] = [
        {
            "id": "ITEM-GRC-G-FONL-KOMBI-KWANT-001",
            "knoop_ids": ["GRC-G-FONL-KOMBI-KWANT"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.3,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 12,
            "stimulus": "Welke twee Griekse klinkers zijn altijd kort?",
            "antwoord": ["ε en ο", "epsilon en omicron"],
            "feedback": "ε (epsilon) en ο (omicron) zijn altijd kort. Tegenhangers: η (altijd lang) en ω (altijd lang).",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-FONL-KOMBI-KWANT-002",
            "knoop_ids": ["GRC-G-FONL-KOMBI-KWANT"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.1,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 15,
            "stimulus": "Welke klinkers kunnen zowel kort als lang zijn?",
            "antwoord": ["α, ι en υ", "alfa, iota en upsilon"],
            "feedback": "α, ι en υ zijn ambigu: kort of lang afhankelijk van het woord. ε/ο altijd kort, η/ω altijd lang.",
            "bron": "handmatig",
        },
    ]

    items["GRC-G-FONL-KOMBI-LEESV"] = [
        {
            "id": "ITEM-GRC-G-FONL-KOMBI-LEESV-001",
            "knoop_ids": ["GRC-G-FONL-KOMBI-LEESV"],
            "type": "offline_schrijven",
            "richting": "productief",
            "moeilijkheid_initieel": 0.2,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 60,
            "stimulus": "Lees hardop en schrijf de Erasmiaanse uitspraak van drie woorden op: ἄνθρωπος, λόγος, ἀγαθός.",
            "antwoord": "Controleer je uitspraak: an-thro-pos, lo-gos, a-ga-thos.",
            "feedback": "Let op: ἄνθρωπος heeft spiritus lenis (geen h), θ = /th/, χ = /kh/ (komt niet voor in deze drie).",
            "bron": "handmatig",
            "verificatie_methode": "self_report",
            "verwacht_resultaat": "an-thro-pos / lo-gos / a-ga-thos, correcte lettergreep-indeling en klanken",
        },
        {
            "id": "ITEM-GRC-G-FONL-KOMBI-LEESV-002",
            "knoop_ids": ["GRC-G-FONL-KOMBI-LEESV"],
            "type": "analyse",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.4,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 35,
            "stimulus": "Analyseer ἀγαθοί: geef spiritus, accent en alle klankwaarden van de letters.",
            "antwoord": [
                "spiritus lenis op α, acutus op οι, letters: a-g-a-th-oi",
                "lenis, acutus op de ultima, klank a-ga-thoi",
            ],
            "feedback": "ἀγαθοί: spiritus lenis (geen h), acutus op de ultima οι, uitspraak 'a-ga-thoi' met th = /tʰ/ en οι = /oi/.",
            "bron": "handmatig",
        },
    ]

    return items


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------


def collect_all() -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {}
    out.update(alfabet_intro_en_groepen())
    out.update(diakritiek_items())
    out.update(kombi_items())
    return out


def validate_all(items_by_knoop: dict[str, list[dict]]) -> None:
    for knoop_id, item_list in items_by_knoop.items():
        for item_dict in item_list:
            Item(**item_dict)
    print(f"All {sum(len(v) for v in items_by_knoop.values())} items validated.")


def add_items_to_json(json_path: Path, items_by_knoop: dict[str, list[dict]]) -> int:
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    added = 0
    for knoop in data["knopen"]:
        if knoop["id"] in items_by_knoop:
            existing_ids = {item["id"] for item in knoop.get("items", [])}
            new_items = [
                item for item in items_by_knoop[knoop["id"]] if item["id"] not in existing_ids
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

    print("\n=== E3-01 Summary ===")
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

    path = Path(__file__).parent.parent / "data" / "graph" / "grc_alfabet.json"
    added = add_items_to_json(path, items_by_knoop)
    print(f"\nAdded {added} items to {path.name}")


if __name__ == "__main__":
    main()
