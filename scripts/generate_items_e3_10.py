#!/usr/bin/env python3
"""Generate exercise items for E3-10: GRC pronomina.

Target: data/graph/grc_grammatica_leerjaar1.json
Scope:  10 knopen (GRC-G-MORF-PRON-*, GRC-G-SYNT-PRON-*).

Drie componenten:
1. Paradigma-drill voor αὐτός (~8 van de lastigste vormen uit m/f/n × 6 nv).
2. Gebruik-items voor αὐτός in de drie betekenissen (zelf / dezelfde /
   hem-haar-het), 3 contextuele items per betekenis.
3. Aanwijzend-trio οὗτος / ἐκεῖνος / ὅδε met semantische keuze-items,
   plus verbuigings- en syntaxis-items voor de pronomen-knopen.

Run:
    python scripts/generate_items_e3_10.py            # writes items to graph
    python scripts/generate_items_e3_10.py --dry-run  # only validate + print
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
# 1. PRON-INTRO
# ---------------------------------------------------------------------------


def pron_intro_items() -> list[dict]:
    return [
        {
            "id": "ITEM-GRC-G-MORF-PRON-INTRO-001",
            "knoop_ids": ["GRC-G-MORF-PRON-INTRO"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.6,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 15,
            "stimulus": "Welke vier hoofdcategorieën voornaamwoorden kent het Grieks in leerjaar 1?",
            "antwoord": [
                "persoonlijk, bezittelijk, aanwijzend, αὐτός",
                "persoonlijk / bezittelijk / aanwijzend / αὐτός",
            ],
            "feedback": "Vier categorieën: persoonlijk (ἐγώ, σύ), bezittelijk (ἐμός, σός), aanwijzend (οὗτος, ἐκεῖνος, ὅδε) en het veelzijdige αὐτός (zelf / dezelfde / hem).",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-PRON-INTRO-002",
            "knoop_ids": ["GRC-G-MORF-PRON-INTRO"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.3,
            "discriminatie_initieel": 1.1,
            "verwachte_tijd_sec": 15,
            "stimulus": "Waarom neemt αὐτός een aparte plaats in tussen de Griekse voornaamwoorden?",
            "antwoord": [
                "het heeft drie functies: zelf, dezelfde, en hij/zij/het",
                "drie betekenissen afhankelijk van positie en lidwoord",
            ],
            "feedback": "αὐτός is intensivum (zelf, predicatief), identiteit (dezelfde, attributief met lidwoord) én 3e-persoons-pronomen in de oblique naamvallen.",
            "bron": "handmatig",
        },
    ]


# ---------------------------------------------------------------------------
# 2. PRON-PERS (persoonlijk ἐγώ, σύ, ἡμεῖς, ὑμεῖς)
# ---------------------------------------------------------------------------


def pron_pers_items() -> list[dict]:
    return [
        {
            "id": "ITEM-GRC-G-MORF-PRON-PERS-001",
            "knoop_ids": ["GRC-G-MORF-PRON-PERS"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.2,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 20,
            "stimulus": "Geef de genitivus enkelvoud van het persoonlijk voornaamwoord 'ik' (nadrukkelijke vorm).",
            "antwoord": ["ἐμοῦ", "ἐμοῦ (μου)"],
            "feedback": "Nadrukkelijk: ἐμοῦ ('van mij'). Enclitisch/zonder nadruk: μου. Dezelfde betekenis, verschillend gewicht in de zin.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-PRON-PERS-002",
            "knoop_ids": ["GRC-G-MORF-PRON-PERS"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.0,
            "discriminatie_initieel": 1.1,
            "verwachte_tijd_sec": 15,
            "stimulus": "Welke naamval en persoon is ἡμῖν?",
            "antwoord": [
                "dativus 1e persoon meervoud (aan ons)",
                "dat. pl. 1e pers.",
            ],
            "feedback": "ἡμῖν = dat. pl. van ἡμεῖς ('wij'). Paradigma: ἡμεῖς / ἡμῶν / ἡμῖν / ἡμᾶς.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-PRON-PERS-003",
            "knoop_ids": ["GRC-G-MORF-PRON-PERS"],
            "type": "contextueel",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.3,
            "discriminatie_initieel": 1.3,
            "verwachte_tijd_sec": 25,
            "stimulus": "Waarom schrijft men 'ἐγὼ λέγω' i.p.v. alleen 'λέγω'? Wat voegt ἐγώ toe?",
            "antwoord": [
                "nadruk/contrast (IK zeg, in tegenstelling tot iemand anders)",
                "expliciet onderwerp voor nadruk",
            ],
            "feedback": "De persoonsuitgang -ω zegt al 'ik'. ἐγώ toevoegen = nadruk of contrast: 'IK zeg (maar jij niet)'. Zonder contrast blijft het vnw. meestal weg.",
            "bron": "handmatig",
        },
    ]


# ---------------------------------------------------------------------------
# 3. PRON-BEZ (bezittelijk ἐμός, σός, ἡμέτερος, ὑμέτερος)
# ---------------------------------------------------------------------------


def pron_bez_items() -> list[dict]:
    return [
        {
            "id": "ITEM-GRC-G-MORF-PRON-BEZ-001",
            "knoop_ids": ["GRC-G-MORF-PRON-BEZ"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.1,
            "discriminatie_initieel": 1.1,
            "verwachte_tijd_sec": 20,
            "stimulus": "Geef de nom. sg. vrouwelijk van het bezittelijk voornaamwoord 'mijn'.",
            "antwoord": ["ἐμή", "ἡ ἐμή"],
            "feedback": "ἐμός / ἐμή / ἐμόν — verbuigt als α/ο-stam adjectief. Vrouwelijk enkelvoud: ἐμή, ἐμῆς, ἐμῇ, ἐμήν.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-PRON-BEZ-002",
            "knoop_ids": ["GRC-G-MORF-PRON-BEZ"],
            "type": "contextueel",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.4,
            "discriminatie_initieel": 1.3,
            "verwachte_tijd_sec": 25,
            "stimulus": "Vertaal: ὁ ἐμὸς φίλος καὶ ὁ σὸς ἀδελφός. Welke twee bezittelijke vnw. staan hier, en hoe vertaal je ze?",
            "antwoord": [
                "ἐμός = mijn, σός = jouw; 'mijn vriend en jouw broer'",
                "ἐμός (mijn) en σός (jouw)",
            ],
            "feedback": "Bezittelijke vnw. staan attributief bij het lidwoord: ὁ ἐμὸς φίλος = 'mijn vriend', ὁ σὸς ἀδελφός = 'jouw broer'. Ze verbuigen met het substantief mee.",
            "bron": "handmatig",
        },
    ]


# ---------------------------------------------------------------------------
# 4. PRON-AANW (trio-introductie + semantische keuze οὗτος/ἐκεῖνος/ὅδε)
# ---------------------------------------------------------------------------


def pron_aanw_items() -> list[dict]:
    return [
        {
            "id": "ITEM-GRC-G-MORF-PRON-AANW-001",
            "knoop_ids": ["GRC-G-MORF-PRON-AANW"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.2,
            "discriminatie_initieel": 1.3,
            "verwachte_tijd_sec": 20,
            "stimulus": "Welk aanwijzend voornaamwoord gebruik je voor 'deze hier, die ik nú ga noemen' (vooruitwijzend)?",
            "antwoord": ["ὅδε", "ὅδε / ἥδε / τόδε"],
            "feedback": "ὅδε verwijst naar wat vólgt (cataforisch): 'deze (die ik nu ga noemen)'. οὗτος verwijst terug naar het net genoemde; ἐκεῖνος naar iets ver weg of eerder.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-PRON-AANW-002",
            "knoop_ids": ["GRC-G-MORF-PRON-AANW"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.1,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 20,
            "stimulus": "Welk aanwijzend voornaamwoord past bij 'die (veraf) / die gene' — bijv. over een persoon uit lang vervlogen tijden?",
            "antwoord": ["ἐκεῖνος", "ἐκεῖνος / ἐκείνη / ἐκεῖνο"],
            "feedback": "ἐκεῖνος = 'die, gene' — verwijst naar wat ver weg is in ruimte, tijd of gedachte. Tegenhanger van οὗτος (dichtbij, zojuist genoemd).",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-PRON-AANW-003",
            "knoop_ids": ["GRC-G-MORF-PRON-AANW"],
            "type": "contextueel",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.4,
            "discriminatie_initieel": 1.4,
            "verwachte_tijd_sec": 30,
            "stimulus": "Kies het juiste demonstratief: 'Ik heb zojuist een verhaal verteld. ___ verhaal is waar.' (οὗτος / ἐκεῖνος / ὅδε?)",
            "antwoord": ["οὗτος", "οὗτος (ὁ λόγος)"],
            "feedback": "οὗτος verwijst terug naar wat net gezegd is (anaforisch): 'dit/dat verhaal (dat ik zojuist vertelde)'. ὅδε zou vooruitwijzen, ἐκεῖνος naar iets ver weg.",
            "bron": "handmatig",
        },
    ]


# ---------------------------------------------------------------------------
# 5. PRON-HOUTOS (verbuiging οὗτος/αὕτη/τοῦτο)
# ---------------------------------------------------------------------------


def pron_houtos_items() -> list[dict]:
    return [
        {
            "id": "ITEM-GRC-G-MORF-PRON-HOUTOS-001",
            "knoop_ids": ["GRC-G-MORF-PRON-HOUTOS"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.5,
            "discriminatie_initieel": 1.3,
            "verwachte_tijd_sec": 25,
            "stimulus": "Geef de nom. sg. vrouwelijk van οὗτος.",
            "antwoord": "αὕτη",
            "feedback": "Vrouwelijk nom. sg. = αὕτη (stam ταυτ- met α-klinker, spiritus asper). Niet verwarren met dat. sg. vr. ταύτῃ.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-PRON-HOUTOS-002",
            "knoop_ids": ["GRC-G-MORF-PRON-HOUTOS"],
            "type": "analyse",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.6,
            "discriminatie_initieel": 1.4,
            "verwachte_tijd_sec": 25,
            "stimulus": "Welke naamval, geslacht en getal is τούτων?",
            "antwoord": [
                "genitivus pluralis (alle geslachten)",
                "gen. pl. m/f/n",
            ],
            "feedback": "τούτων = gen. pl. — één vorm voor alle drie de geslachten, net als bij het lidwoord τῶν. Stamwisseling: sg. heeft ου-/αυ-, pl. heeft ου-/αυ- alternerend per vorm.",
            "bron": "handmatig",
        },
    ]


# ---------------------------------------------------------------------------
# 6. PRON-EKEIN (verbuiging ἐκεῖνος/ἐκείνη/ἐκεῖνο)
# ---------------------------------------------------------------------------


def pron_ekein_items() -> list[dict]:
    return [
        {
            "id": "ITEM-GRC-G-MORF-PRON-EKEIN-001",
            "knoop_ids": ["GRC-G-MORF-PRON-EKEIN"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.3,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 20,
            "stimulus": "Geef de acc. sg. mannelijk van ἐκεῖνος.",
            "antwoord": "ἐκεῖνον",
            "feedback": "ἐκεῖνος verbuigt als een α/ο-stam adjectief: ἐκεῖνος, ἐκείνου, ἐκείνῳ, ἐκεῖνον. Let op: nom. en acc. sg. n. = ἐκεῖνο (zónder -ν).",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-PRON-EKEIN-002",
            "knoop_ids": ["GRC-G-MORF-PRON-EKEIN"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.4,
            "discriminatie_initieel": 1.3,
            "verwachte_tijd_sec": 20,
            "stimulus": "Welke naamval, geslacht en getal is ἐκείναις?",
            "antwoord": [
                "dativus pluralis vrouwelijk",
                "dat. pl. vr.",
            ],
            "feedback": "ἐκείναις = dat. pl. vr. (α-stam uitgang -αις). Verschilt van ἐκείνοις (dat. pl. m./n.).",
            "bron": "handmatig",
        },
    ]


# ---------------------------------------------------------------------------
# 7. PRON-AUTOS (drie betekenissen — 3 contextuele items per betekenis)
# ---------------------------------------------------------------------------


def pron_autos_items() -> list[dict]:
    items: list[dict] = []
    items.extend(_autos_zelf_items())
    items.extend(_autos_dezelfde_items())
    items.extend(_autos_hem_items())
    return items


def _autos_zelf_items() -> list[dict]:
    return [
        {
            "id": "ITEM-GRC-G-MORF-PRON-AUTOS-001",
            "knoop_ids": ["GRC-G-MORF-PRON-AUTOS", "GRC-G-SYNT-PRON-GEBR"],
            "type": "contextueel",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.5,
            "discriminatie_initieel": 1.4,
            "verwachte_tijd_sec": 30,
            "stimulus": "Vertaal: ὁ βασιλεὺς αὐτὸς ἔρχεται. Waarom staat αὐτός zó (predicatief, zonder lidwoord vóór)?",
            "antwoord": [
                "de koning zelf komt; predicatieve positie → intensivum 'zelf'",
                "'de koning zelf komt' — αὐτός predicatief = zelf",
            ],
            "feedback": "Predicatieve positie (ὁ βασιλεὺς αὐτὸς of αὐτὸς ὁ βασιλεύς) geeft de betekenis 'zelf'. Attributief (ὁ αὐτὸς βασιλεύς) zou 'dezelfde' betekenen.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-PRON-AUTOS-002",
            "knoop_ids": ["GRC-G-MORF-PRON-AUTOS", "GRC-G-SYNT-PRON-GEBR"],
            "type": "contextueel",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.5,
            "discriminatie_initieel": 1.3,
            "verwachte_tijd_sec": 30,
            "stimulus": "Vertaal: αὐτὴ ἡ θεὰ τὸν νεὼν οἰκοδομεῖ. Wat betekent αὐτή hier?",
            "antwoord": [
                "de godin zelf bouwt de tempel",
                "zelf — 'de godin zelf bouwt de tempel'",
            ],
            "feedback": "αὐτὴ ἡ θεά = predicatieve positie → 'de godin zélf'. Nadruk: niemand anders dan zij persoonlijk.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-PRON-AUTOS-003",
            "knoop_ids": ["GRC-G-MORF-PRON-AUTOS", "GRC-G-SYNT-PRON-GEBR"],
            "type": "contextueel",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.6,
            "discriminatie_initieel": 1.4,
            "verwachte_tijd_sec": 30,
            "stimulus": "Vertaal: ὁ διδάσκαλος αὐτὸς γράφει τὴν ἐπιστολήν. Welke drie woorden dragen de nadruk van αὐτός?",
            "antwoord": [
                "'de leraar zelf schrijft de brief' — nadruk op 'de leraar zelf'",
                "de leraar zelf — niet een slaaf of leerling",
            ],
            "feedback": "αὐτός predicatief = intensivum 'zelf'. Context: hij delegeert het niet, dóét het eigenhandig. Vergelijk Latijn ipse.",
            "bron": "handmatig",
        },
    ]


def _autos_dezelfde_items() -> list[dict]:
    return [
        {
            "id": "ITEM-GRC-G-MORF-PRON-AUTOS-004",
            "knoop_ids": ["GRC-G-MORF-PRON-AUTOS", "GRC-G-SYNT-PRON-GEBR"],
            "type": "contextueel",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.5,
            "discriminatie_initieel": 1.4,
            "verwachte_tijd_sec": 30,
            "stimulus": "Vertaal: ὁ αὐτὸς ἀνὴρ πάλιν λέγει. Waarom betekent αὐτός hier 'dezelfde' en niet 'zelf'?",
            "antwoord": [
                "dezelfde man spreekt opnieuw; attributieve positie (lidwoord + αὐτός) → 'dezelfde'",
                "attributief tussen lidwoord en substantief = 'dezelfde'",
            ],
            "feedback": "ὁ αὐτὸς ἀνήρ (lidwoord + αὐτός + substantief) = attributieve positie → 'dezelfde man'. Zonder lidwoord vóór αὐτός zou het 'zelf' betekenen.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-PRON-AUTOS-005",
            "knoop_ids": ["GRC-G-MORF-PRON-AUTOS", "GRC-G-SYNT-PRON-GEBR"],
            "type": "contextueel",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.6,
            "discriminatie_initieel": 1.4,
            "verwachte_tijd_sec": 30,
            "stimulus": "Vertaal: ἡ αὐτὴ γνώμη ἐστὶν καὶ ἐμοὶ καὶ σοί.",
            "antwoord": [
                "Dezelfde mening heb ik en jij / wij hebben dezelfde mening",
                "ik en jij hebben dezelfde mening",
            ],
            "feedback": "ἡ αὐτὴ γνώμη (attributief) = 'dezelfde mening'. Dativus van bezit: ἐμοί καὶ σοί = 'voor mij en voor jou'. Αὐτός met lidwoord = identiteit.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-PRON-AUTOS-006",
            "knoop_ids": ["GRC-G-MORF-PRON-AUTOS", "GRC-G-SYNT-PRON-GEBR"],
            "type": "contextueel",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.7,
            "discriminatie_initieel": 1.4,
            "verwachte_tijd_sec": 30,
            "stimulus": "Welk verschil in betekenis geven deze twee zinnen? (a) ὁ στρατηγὸς αὐτὸς ἔρχεται. (b) ὁ αὐτὸς στρατηγὸς ἔρχεται.",
            "antwoord": [
                "(a) de generaal zelf komt; (b) dezelfde generaal komt",
                "(a) zelf (predicatief); (b) dezelfde (attributief)",
            ],
            "feedback": "Positie t.o.v. het lidwoord beslist alles. Predicatief (αὐτός buiten lidwoord+subst.) = 'zelf'. Attributief (lidwoord + αὐτός + subst.) = 'dezelfde'.",
            "bron": "handmatig",
        },
    ]


def _autos_hem_items() -> list[dict]:
    return [
        {
            "id": "ITEM-GRC-G-MORF-PRON-AUTOS-007",
            "knoop_ids": ["GRC-G-MORF-PRON-AUTOS", "GRC-G-SYNT-PRON-GEBR"],
            "type": "contextueel",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.4,
            "discriminatie_initieel": 1.3,
            "verwachte_tijd_sec": 25,
            "stimulus": "Vertaal: ὁ δοῦλος ὁρᾷ αὐτόν. Welke functie heeft αὐτόν hier?",
            "antwoord": [
                "de slaaf ziet hem; αὐτόν = 3e pers. pronomen (hem) in acc.",
                "αὐτόν = 'hem' (lijdend voorwerp)",
            ],
            "feedback": "In de oblique naamvallen (gen./dat./acc.) vervangt αὐτός het ontbrekende 3e-persoons pronomen: 'hem/haar/het'. Nom. wordt alleen als intensivum gebruikt.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-PRON-AUTOS-008",
            "knoop_ids": ["GRC-G-MORF-PRON-AUTOS", "GRC-G-SYNT-PRON-GEBR"],
            "type": "contextueel",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.5,
            "discriminatie_initieel": 1.3,
            "verwachte_tijd_sec": 30,
            "stimulus": "Vertaal: ὁ πατὴρ δίδωσιν αὐτῷ τὸ βιβλίον. Welke vormen en welke betekenis heeft αὐτῷ?",
            "antwoord": [
                "dat. sg. m. — 'aan hem'; 'de vader geeft hem het boek'",
                "αὐτῷ = 'aan hem' (dat. sg.)",
            ],
            "feedback": "αὐτῷ = dativus sg. m./n. — meewerkend voorwerp 'aan hem'. In de oblique naamvallen fungeert αὐτός als 3e-persoons pronomen.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-PRON-AUTOS-009",
            "knoop_ids": ["GRC-G-MORF-PRON-AUTOS", "GRC-G-SYNT-PRON-GEBR"],
            "type": "contextueel",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.6,
            "discriminatie_initieel": 1.4,
            "verwachte_tijd_sec": 30,
            "stimulus": "Vertaal: ἡ μήτηρ φιλεῖ αὐτήν. Wat betekent αὐτήν hier, en waarom niet 'zelf'?",
            "antwoord": [
                "de moeder houdt van haar; αὐτήν in acc. = 'haar' (geen lidwoord in context → pronomen, geen intensivum)",
                "αὐτήν = 'haar' (3e pers. pron., acc. sg. vr.)",
            ],
            "feedback": "αὐτός in oblique naamvallen zonder koppeling aan een gezamenlijk substantief = 3e-pers. pronomen. 'Zelf'-lezing vereist dat αὐτός predicatief bij een substantief staat.",
            "bron": "handmatig",
        },
    ]


# ---------------------------------------------------------------------------
# 8. PRON-PARAD (αὐτός paradigma-drill, lastigste ~8 vormen)
# ---------------------------------------------------------------------------


def pron_parad_items() -> list[dict]:
    items: list[dict] = []
    items.extend(_autos_parad_part1())
    items.extend(_autos_parad_part2())
    return items


def _autos_parad_part1() -> list[dict]:
    rows = [
        ("gen. sg. vr.", "αὐτῆς", "van haar"),
        ("dat. sg. vr.", "αὐτῇ", "aan haar"),
        ("gen. sg. m.", "αὐτοῦ", "van hem"),
        ("dat. sg. m.", "αὐτῷ", "aan hem"),
    ]
    items: list[dict] = []
    for idx, (label, form, nl) in enumerate(rows, start=1):
        items.append(
            {
                "id": f"ITEM-GRC-G-MORF-PRON-PARAD-{idx:03d}",
                "knoop_ids": ["GRC-G-MORF-PRON-PARAD", "GRC-G-MORF-PRON-AUTOS"],
                "type": "productie",
                "richting": "productief",
                "moeilijkheid_initieel": 0.4,
                "discriminatie_initieel": 1.3,
                "verwachte_tijd_sec": 20,
                "stimulus": f"Geef de {label} van αὐτός.",
                "antwoord": form,
                "feedback": f"{label} = {form} ('{nl}'). Uitgangen α/ο-stam, maar let op: gen./dat. sg. vr. eindigt op -ῆς / -ῇ (met iota subscript).",
                "bron": "handmatig",
            }
        )
    return items


def _autos_parad_part2() -> list[dict]:
    rows = [
        ("acc. sg. vr.", "αὐτήν", "haar", 0.3),
        ("nom. pl. onz.", "αὐτά", "zij (onz.) / ze", 0.4),
        ("dat. pl. m./n.", "αὐτοῖς", "aan hen", 0.4),
        ("dat. pl. vr.", "αὐταῖς", "aan hen (vr.)", 0.5),
    ]
    items: list[dict] = []
    for idx, (label, form, nl, diff) in enumerate(rows, start=5):
        items.append(
            {
                "id": f"ITEM-GRC-G-MORF-PRON-PARAD-{idx:03d}",
                "knoop_ids": ["GRC-G-MORF-PRON-PARAD", "GRC-G-MORF-PRON-AUTOS"],
                "type": "productie",
                "richting": "productief",
                "moeilijkheid_initieel": diff,
                "discriminatie_initieel": 1.3,
                "verwachte_tijd_sec": 20,
                "stimulus": f"Geef de {label} van αὐτός.",
                "antwoord": form,
                "feedback": f"{label} = {form} ('{nl}'). Let op: nom./acc. pl. onz. is αὐτά (kort -α, geen -ος/-α verwarring met 1e decl.).",
                "bron": "handmatig",
            }
        )
    return items


# ---------------------------------------------------------------------------
# 9. SYNT-PRON-AANW (predicatieve positie demonstrativa)
# ---------------------------------------------------------------------------


def synt_pron_aanw_items() -> list[dict]:
    return [
        {
            "id": "ITEM-GRC-G-SYNT-PRON-AANW-001",
            "knoop_ids": ["GRC-G-SYNT-PRON-AANW"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.3,
            "discriminatie_initieel": 1.3,
            "verwachte_tijd_sec": 20,
            "stimulus": "Welke van deze woordvolgordes is correct voor 'deze mens' met οὗτος?",
            "antwoord": [
                "οὗτος ὁ ἄνθρωπος of ὁ ἄνθρωπος οὗτος",
                "predicatieve positie: οὗτος staat buiten de lidwoord-substantief-groep",
            ],
            "feedback": "Demonstrativa staan in predicatieve positie: óf vóór het lidwoord (οὗτος ὁ ἄνθρωπος) óf na het substantief (ὁ ἄνθρωπος οὗτος). Nooit *ὁ οὗτος ἄνθρωπος.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-SYNT-PRON-AANW-002",
            "knoop_ids": ["GRC-G-SYNT-PRON-AANW"],
            "type": "contextueel",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.5,
            "discriminatie_initieel": 1.4,
            "verwachte_tijd_sec": 25,
            "stimulus": "Wat is er fout aan *ἡ ἐκείνη πόλις en hoe verbeter je het?",
            "antwoord": [
                "demonstrativa moeten predicatief staan: ἐκείνη ἡ πόλις of ἡ πόλις ἐκείνη",
                "verkeerde positie; correct: ἐκείνη ἡ πόλις",
            ],
            "feedback": "*ἡ ἐκείνη πόλις plaatst het demonstratief attributief — fout. Demonstrativa staan altijd predicatief: ἐκείνη ἡ πόλις ('die stad').",
            "bron": "handmatig",
        },
    ]


# ---------------------------------------------------------------------------
# 10. SYNT-PRON-GEBR (gebruik van pronomina in de zin)
# ---------------------------------------------------------------------------


def synt_pron_gebr_items() -> list[dict]:
    return [
        {
            "id": "ITEM-GRC-G-SYNT-PRON-GEBR-001",
            "knoop_ids": ["GRC-G-SYNT-PRON-GEBR"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.2,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 15,
            "stimulus": "Waarom is een persoonlijk voornaamwoord als onderwerp meestal overbodig in het Grieks?",
            "antwoord": [
                "de persoonsuitgang van het werkwoord drukt de persoon al uit",
                "uitgangen zijn expliciet; vnw. alleen bij nadruk",
            ],
            "feedback": "De werkwoordsuitgangen -ω, -εις, -ει, -ομεν, -ετε, -ουσι(ν) wijzen de persoon al ondubbelzinnig aan. Het vnw. voegt je alleen toe bij nadruk of contrast.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-SYNT-PRON-GEBR-002",
            "knoop_ids": ["GRC-G-SYNT-PRON-GEBR"],
            "type": "contextueel",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.4,
            "discriminatie_initieel": 1.3,
            "verwachte_tijd_sec": 25,
            "stimulus": "Wat is het verschil in gebruik tussen ἐμοῦ en μου?",
            "antwoord": [
                "ἐμοῦ = nadrukkelijk/aan begin van zin; μου = enclitisch, zonder nadruk",
                "ἐμοῦ met klemtoon, μου als enclisis",
            ],
            "feedback": "Nadrukkelijk ἐμοῦ (eigen accent) gebruik je bij contrast of na een voorzetsel. Enclitisch μου leunt op het voorgaande woord: 'ὁ πατήρ μου' (mijn vader).",
            "bron": "handmatig",
        },
    ]


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------


def collect_all() -> dict[str, list[dict]]:
    all_items: list[dict] = []
    all_items.extend(pron_intro_items())
    all_items.extend(pron_pers_items())
    all_items.extend(pron_bez_items())
    all_items.extend(pron_aanw_items())
    all_items.extend(pron_houtos_items())
    all_items.extend(pron_ekein_items())
    all_items.extend(pron_autos_items())
    all_items.extend(pron_parad_items())
    all_items.extend(synt_pron_aanw_items())
    all_items.extend(synt_pron_gebr_items())

    primary_map: dict[str, list[dict]] = {}
    for item in all_items:
        for key in ("stimulus", "antwoord", "feedback", "verwacht_resultaat"):
            if key in item and item[key] is not None:
                item[key] = nfc(item[key])
        primary_map.setdefault(item["knoop_ids"][0], []).append(item)
    return primary_map


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
    per_knoop: Counter[str] = Counter()
    for knoop_id, item_list in items_by_knoop.items():
        per_knoop[knoop_id] = len(item_list)
        for item in item_list:
            type_counter[item["type"]] += 1

    print("\n=== E3-10 Summary ===")
    print(f"Knopen: {len(items_by_knoop)}")
    print(f"Total items: {total}")
    print("\nItems per knoop:")
    for k, c in per_knoop.most_common():
        print(f"  {k}: {c}")
    print("\nOefentype-verdeling:")
    for t, c in type_counter.most_common():
        print(f"  {t}: {c}")


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
