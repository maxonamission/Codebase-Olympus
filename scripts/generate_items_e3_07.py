#!/usr/bin/env python3
"""Generate exercise items for E3-07: GRC praesens indicativus actief.

Target: data/graph/grc_grammatica_leerjaar1.json
Scope:  7 knopen rondom het praesens ind. act.: PRAES-THEM, CONTR-INTRO,
        CONTR-A, CONTR-E, PRAES-EIMI, INF-PRAES, PRAES-PARAD.

Drie componenten:
1. Thematische werkwoorden — λύω, γράφω: persoonsuitgangen in alle 6 personen.
2. Contracta — τιμάω (α-contr.), ποιέω (ε-contr.), δηλόω (ο-contr.).
   Productie-items tonen de 'voor-contractie'-vorm (bv. τιμά-ει) als hint.
3. εἰμί — eigen cluster met 5 kernvormen (1/2/3 sg, 1 + 3 pl).

Run:
    python scripts/generate_items_e3_07.py            # writes items to graph
    python scripts/generate_items_e3_07.py --dry-run  # only validate + print
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
# 1. Thematische verba (λύω, γράφω) — PRAES-THEM + PERSOON cross-tag
# ---------------------------------------------------------------------------


def praes_them_items() -> list[dict]:
    ps = [
        ("1 sg.", "γράφω", "ik schrijf", "-ω", -0.5),
        ("2 sg.", "γράφεις", "jij schrijft", "-εις", -0.3),
        ("3 sg.", "γράφει", "hij/zij schrijft", "-ει", -0.3),
        ("1 pl.", "γράφομεν", "wij schrijven", "-ομεν", 0.0),
        ("2 pl.", "γράφετε", "jullie schrijven", "-ετε", 0.1),
        ("3 pl.", "γράφουσι(ν)", "zij schrijven", "-ουσι(ν)", 0.2),
    ]
    items: list[dict] = []
    # Six productie-items: geef de vorm bij persoon/getal.
    for idx, (label, form, nl, uitg, diff) in enumerate(ps, start=1):
        items.append(
            {
                "id": f"ITEM-GRC-G-MORF-PRAES-THEM-{idx:03d}",
                "knoop_ids": ["GRC-G-MORF-PRAES-THEM", "GRC-G-MORF-PERSOON-INTRO"],
                "type": "productie",
                "richting": "productief",
                "moeilijkheid_initieel": diff,
                "discriminatie_initieel": 1.2,
                "verwachte_tijd_sec": 25,
                "stimulus": f"Geef de {label} praesens actief van γράφω (= 'schrijven').",
                "antwoord": form,
                "feedback": (
                    f"{label} van γράφω = {form} ({nl}). Uitgang {uitg} op stam γραφ-."
                ),
                "bron": "handmatig",
            }
        )

    # Herkenning analyse-items op λύω (persoon identificeren).
    recog = [
        ("λύεις", "2e persoon singularis", -0.2),
        ("λύομεν", "1e persoon pluralis", 0.0),
        ("λύουσι(ν)", "3e persoon pluralis", 0.1),
    ]
    for idx, (form, antw, diff) in enumerate(recog, start=7):
        items.append(
            {
                "id": f"ITEM-GRC-G-MORF-PRAES-THEM-{idx:03d}",
                "knoop_ids": ["GRC-G-MORF-PRAES-THEM", "GRC-G-MORF-PERSOON-INTRO"],
                "type": "herkenning",
                "richting": "receptief",
                "moeilijkheid_initieel": diff,
                "discriminatie_initieel": 1.2,
                "verwachte_tijd_sec": 15,
                "stimulus": f"Welke persoon en welk getal heeft {form}?",
                "antwoord": [antw, antw.replace("persoon ", "p. ").replace("singularis", "sg.").replace("pluralis", "pl.")],
                "feedback": (
                    f"{form} = {antw} praesens actief van λύω. De thematische klinker (ε/ο) zit "
                    "tussen stam en uitgang."
                ),
                "bron": "handmatig",
            }
        )

    # Eén analyse-item over de thematische klinker.
    items.append(
        {
            "id": "ITEM-GRC-G-MORF-PRAES-THEM-010",
            "knoop_ids": ["GRC-G-MORF-PRAES-THEM", "GRC-G-MORF-THEM-INTRO"],
            "type": "analyse",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.3,
            "discriminatie_initieel": 1.3,
            "verwachte_tijd_sec": 25,
            "stimulus": "Splits λύομεν in stam + thematische klinker + persoonsuitgang.",
            "antwoord": ["λυ-ο-μεν", "λυ + ο + μεν"],
            "feedback": "λυ- (stam) + -ο- (thematische klinker vóór nasaal μ) + -μεν (1 pl. uitgang). Vóór σ/τ wordt het ε: λύ-ε-τε.",
            "bron": "handmatig",
        }
    )

    return items


# ---------------------------------------------------------------------------
# 2. Contracta — CONTR-INTRO (δηλόω) + CONTR-A (τιμάω) + CONTR-E (ποιέω)
# ---------------------------------------------------------------------------


def contr_intro_items() -> list[dict]:
    return [
        {
            "id": "ITEM-GRC-G-MORF-CONTR-INTRO-001",
            "knoop_ids": ["GRC-G-MORF-CONTR-INTRO"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.3,
            "discriminatie_initieel": 1.1,
            "verwachte_tijd_sec": 15,
            "stimulus": "Welke drie soorten verba contracta kent het praesens?",
            "antwoord": [
                "α-contracta, ε-contracta, ο-contracta",
                "stammen op α, ε of ο",
            ],
            "feedback": "Drie stamklinkers contracteren met de thematische klinker: α (τιμάω), ε (ποιέω), ο (δηλόω). Lexicon-vorm toont altijd de ongecontracteerde 1 sg.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-CONTR-INTRO-002",
            "knoop_ids": ["GRC-G-MORF-CONTR-INTRO"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.5,
            "discriminatie_initueel_placeholder": 0.0,  # removed below
            "discriminatie_initieel": 1.3,
            "verwachte_tijd_sec": 25,
            "stimulus": "Geef de gecontracteerde 1 sg. praesens actief van δηλόω (voor-contractie: δηλό-ω).",
            "antwoord": "δηλῶ",
            "feedback": "Contractie ο+ω → ω (circumflex verplicht): δηλό-ω → δηλῶ. Dezelfde regel bij τιμάω → τιμῶ en ποιέω → ποιῶ.",
            "bron": "handmatig",
        },
    ]


def contr_a_items() -> list[dict]:
    """τιμάω: 7 items met voor-contractie-hint."""
    rows = [
        ("1 sg.", "τιμά-ω", "τιμῶ", "α+ω → ω (circumflex)", 0.3),
        ("2 sg.", "τιμά-εις", "τιμᾷς", "α+ει → ᾳ", 0.5),
        ("3 sg.", "τιμά-ει", "τιμᾷ", "α+ει → ᾳ", 0.5),
        ("1 pl.", "τιμά-ομεν", "τιμῶμεν", "α+ο → ω (circumflex)", 0.5),
        ("2 pl.", "τιμά-ετε", "τιμᾶτε", "α+ε → ᾱ (circumflex)", 0.6),
    ]
    items: list[dict] = []
    for idx, (label, pre, post, rule, diff) in enumerate(rows, start=1):
        items.append(
            {
                "id": f"ITEM-GRC-G-MORF-CONTR-A-{idx:03d}",
                "knoop_ids": ["GRC-G-MORF-CONTR-A"],
                "type": "productie",
                "richting": "productief",
                "moeilijkheid_initieel": diff,
                "discriminatie_initieel": 1.3,
                "verwachte_tijd_sec": 25,
                "stimulus": f"Geef de gecontracteerde {label} praesens actief van τιμάω (voor-contractie: {pre}).",
                "antwoord": post,
                "feedback": f"{pre} → {post}. Regel: {rule}.",
                "bron": "handmatig",
            }
        )
    items.append(
        {
            "id": "ITEM-GRC-G-MORF-CONTR-A-006",
            "knoop_ids": ["GRC-G-MORF-CONTR-A"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.2,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 15,
            "stimulus": "Naar welke klank contracteren α + ο in een α-contractum?",
            "antwoord": ["ω", "lange ω"],
            "feedback": "α+ο → ω (en α+ου → ω). Dit verklaart τιμῶμεν (< τιμά-ομεν) en τιμῶσι (< τιμά-ουσι).",
            "bron": "handmatig",
        }
    )
    items.append(
        {
            "id": "ITEM-GRC-G-MORF-CONTR-A-007",
            "knoop_ids": ["GRC-G-MORF-CONTR-A"],
            "type": "analyse",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.5,
            "discriminatie_initieel": 1.3,
            "verwachte_tijd_sec": 20,
            "stimulus": "Waarom heeft τιμᾷ een iota subscriptum en τιμᾶτε niet?",
            "antwoord": [
                "τιμᾷ < τιμά-ει (α+ει → ᾳ, iota blijft); τιμᾶτε < τιμά-ετε (α+ε → ᾱ, geen iota)",
                "de ει brengt een iota mee, de losse ε niet",
            ],
            "feedback": "Contractieresultaat hangt af van de tweede klinker: α+ει behoudt de iota (subscript); α+ε levert een lange α zonder iota.",
            "bron": "handmatig",
        }
    )
    return items


def contr_e_items() -> list[dict]:
    """ποιέω: 6 items met voor-contractie-hint."""
    rows = [
        ("1 sg.", "ποιέ-ω", "ποιῶ", "ε+ω → ω", 0.3),
        ("2 sg.", "ποιέ-εις", "ποιεῖς", "ε+ει → ει (circumflex)", 0.5),
        ("3 sg.", "ποιέ-ει", "ποιεῖ", "ε+ει → ει (circumflex)", 0.5),
        ("1 pl.", "ποιέ-ομεν", "ποιοῦμεν", "ε+ο → ου", 0.6),
        ("2 pl.", "ποιέ-ετε", "ποιεῖτε", "ε+ε → ει", 0.5),
    ]
    items: list[dict] = []
    for idx, (label, pre, post, rule, diff) in enumerate(rows, start=1):
        items.append(
            {
                "id": f"ITEM-GRC-G-MORF-CONTR-E-{idx:03d}",
                "knoop_ids": ["GRC-G-MORF-CONTR-E"],
                "type": "productie",
                "richting": "productief",
                "moeilijkheid_initieel": diff,
                "discriminatie_initieel": 1.3,
                "verwachte_tijd_sec": 25,
                "stimulus": f"Geef de gecontracteerde {label} praesens actief van ποιέω (voor-contractie: {pre}).",
                "antwoord": post,
                "feedback": f"{pre} → {post}. Regel: {rule}.",
                "bron": "handmatig",
            }
        )
    items.append(
        {
            "id": "ITEM-GRC-G-MORF-CONTR-E-006",
            "knoop_ids": ["GRC-G-MORF-CONTR-E"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.2,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 15,
            "stimulus": "Naar welke klank contracteren ε + ο in een ε-contractum?",
            "antwoord": ["ου", "lange ou"],
            "feedback": "ε+ο → ου. Dit verklaart ποιοῦμεν (< ποιέ-ομεν) en ποιοῦσι (< ποιέ-ουσι).",
            "bron": "handmatig",
        }
    )
    return items


# ---------------------------------------------------------------------------
# 3. εἰμί — 5 kernvormen
# ---------------------------------------------------------------------------


def eimi_items() -> list[dict]:
    return [
        {
            "id": "ITEM-GRC-G-MORF-PRAES-EIMI-001",
            "knoop_ids": ["GRC-G-MORF-PRAES-EIMI"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": -0.3,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 20,
            "stimulus": "Geef de 1 sg. praesens van εἰμί ('ik ben').",
            "antwoord": "εἰμί",
            "feedback": "1 sg. = εἰμί. Enclitisch (verliest vaak zijn accent). Onregelmatig werkwoord, deels athematisch.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-PRAES-EIMI-002",
            "knoop_ids": ["GRC-G-MORF-PRAES-EIMI"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.0,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 20,
            "stimulus": "Geef de 2 sg. praesens van εἰμί ('jij bent').",
            "antwoord": "εἶ",
            "feedback": "2 sg. = εἶ (korte vorm met circumflex). Niet te verwarren met het imperatief εἶ.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-PRAES-EIMI-003",
            "knoop_ids": ["GRC-G-MORF-PRAES-EIMI"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.0,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 20,
            "stimulus": "Geef de 3 sg. praesens van εἰμί ('hij/zij is').",
            "antwoord": ["ἐστί", "ἐστίν", "ἐστί(ν)"],
            "feedback": "3 sg. = ἐστί(ν) met bewegelijke ν. Enclitisch tenzij nadrukkelijk of aan het begin van de zin (dan ἔστι).",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-PRAES-EIMI-004",
            "knoop_ids": ["GRC-G-MORF-PRAES-EIMI"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.2,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 20,
            "stimulus": "Geef de 1 pl. praesens van εἰμί ('wij zijn').",
            "antwoord": "ἐσμέν",
            "feedback": "1 pl. = ἐσμέν. De stam ἐσ- is zichtbaar in het meervoud; in sg. 1/2 is de σ verdwenen.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-PRAES-EIMI-005",
            "knoop_ids": ["GRC-G-MORF-PRAES-EIMI"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.2,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 20,
            "stimulus": "Geef de 3 pl. praesens van εἰμί ('zij zijn').",
            "antwoord": ["εἰσί", "εἰσίν", "εἰσί(ν)"],
            "feedback": "3 pl. = εἰσί(ν) met bewegelijke ν. Compleet paradigma: εἰμί, εἶ, ἐστί(ν), ἐσμέν, ἐστέ, εἰσί(ν).",
            "bron": "handmatig",
        },
    ]


# ---------------------------------------------------------------------------
# 4. INF-PRAES — 4 items
# ---------------------------------------------------------------------------


def inf_praes_items() -> list[dict]:
    return [
        {
            "id": "ITEM-GRC-G-MORF-INF-PRAES-001",
            "knoop_ids": ["GRC-G-MORF-INF-PRAES"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.2,
            "discriminatie_initieel": 1.1,
            "verwachte_tijd_sec": 15,
            "stimulus": "Welke uitgang heeft de infinitief praesens actief bij een thematisch werkwoord?",
            "antwoord": "-ειν",
            "feedback": "Inf. praes. act. thematisch = -ειν: λύειν, γράφειν. Contracta krijgen een gecontracteerde vorm (-ᾶν, -εῖν, -οῦν).",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-INF-PRAES-002",
            "knoop_ids": ["GRC-G-MORF-INF-PRAES"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.3,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 20,
            "stimulus": "Geef de infinitief praesens actief van γράφω.",
            "antwoord": "γράφειν",
            "feedback": "Inf. = γράφειν ('schrijven'). Stam γραφ- + uitgang -ειν.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-INF-PRAES-003",
            "knoop_ids": ["GRC-G-MORF-INF-PRAES"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.6,
            "discriminatie_initieel": 1.3,
            "verwachte_tijd_sec": 25,
            "stimulus": "Geef de infinitief praesens actief van τιμάω (voor-contractie: τιμά-ειν).",
            "antwoord": "τιμᾶν",
            "feedback": "τιμά-ειν → τιμᾶν (α+ει verliest iota als de infinitief geen morfologische iota bevat). Vergelijk ποιεῖν (< ποιέ-ειν).",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-INF-PRAES-004",
            "knoop_ids": ["GRC-G-MORF-INF-PRAES"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.2,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 15,
            "stimulus": "Wat is de infinitief praesens van εἰμί?",
            "antwoord": "εἶναι",
            "feedback": "Inf. van εἰμί = εἶναι ('zijn'). Onregelmatig, eigen vorm buiten het -ειν-patroon.",
            "bron": "handmatig",
        },
    ]


# ---------------------------------------------------------------------------
# 5. PRAES-PARAD — 6 items (paradigma-drill + analyse)
# ---------------------------------------------------------------------------


def paradigma_items() -> list[dict]:
    return [
        {
            "id": "ITEM-GRC-G-MORF-PRAES-PARAD-001",
            "knoop_ids": ["GRC-G-MORF-PRAES-PARAD"],
            "type": "offline_schrijven",
            "richting": "productief",
            "moeilijkheid_initieel": 0.7,
            "discriminatie_initieel": 1.3,
            "verwachte_tijd_sec": 90,
            "stimulus": "Schrijf het volledige paradigma van λύω praesens ind. act. op (6 personen) en vergelijk met je grammaticaboek.",
            "antwoord": "λύω, λύεις, λύει, λύομεν, λύετε, λύουσι(ν)",
            "feedback": "Zes vormen: λύω / λύεις / λύει / λύομεν / λύετε / λύουσι(ν). Thematische klinker ο vóór μ/ν, ε elders.",
            "bron": "handmatig",
            "verificatie_methode": "self_report",
            "verwacht_resultaat": "6 vormen van λύω met correcte accenten en bewegelijke ν in de 3 pl.",
        },
        {
            "id": "ITEM-GRC-G-MORF-PRAES-PARAD-002",
            "knoop_ids": ["GRC-G-MORF-PRAES-PARAD"],
            "type": "analyse",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.5,
            "discriminatie_initieel": 1.3,
            "verwachte_tijd_sec": 25,
            "stimulus": "Welke persoon en welk getal heeft ποιοῦμεν?",
            "antwoord": [
                "1e persoon pluralis",
                "1 pl.",
            ],
            "feedback": "ποιοῦμεν = 1 pl. praes. ind. act. van ποιέω (< ποιέ-ομεν; ε+ο → ου).",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-PRAES-PARAD-003",
            "knoop_ids": ["GRC-G-MORF-PRAES-PARAD"],
            "type": "analyse",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.5,
            "discriminatie_initieel": 1.3,
            "verwachte_tijd_sec": 25,
            "stimulus": "Welke persoon en welk getal heeft τιμᾷς?",
            "antwoord": [
                "2e persoon singularis",
                "2 sg.",
            ],
            "feedback": "τιμᾷς = 2 sg. praes. ind. act. van τιμάω (< τιμά-εις; α+ει → ᾳ, circumflex).",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-PRAES-PARAD-004",
            "knoop_ids": ["GRC-G-MORF-PRAES-PARAD"],
            "type": "contextueel",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.5,
            "discriminatie_initieel": 1.3,
            "verwachte_tijd_sec": 25,
            "stimulus": "In 'οἱ νεανίαι γράφουσι τοὺς λόγους' — welke persoon en getal heeft γράφουσι?",
            "antwoord": [
                "3e persoon pluralis",
                "3 pl.",
            ],
            "feedback": "γράφουσι = 3 pl. praes. ind. act. Congrueert met het onderwerp οἱ νεανίαι (nom. pl.).",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-PRAES-PARAD-005",
            "knoop_ids": ["GRC-G-MORF-PRAES-PARAD"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.6,
            "discriminatie_initieel": 1.3,
            "verwachte_tijd_sec": 30,
            "stimulus": "Geef de 3 pl. praesens actief van τιμάω (voor-contractie: τιμά-ουσι).",
            "antwoord": ["τιμῶσι", "τιμῶσιν", "τιμῶσι(ν)"],
            "feedback": "τιμά-ουσι → τιμῶσι(ν). Regel α+ου → ω (circumflex). Bewegelijke ν voor klinker of zineinde.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-PRAES-PARAD-006",
            "knoop_ids": ["GRC-G-MORF-PRAES-PARAD"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.3,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 15,
            "stimulus": "Wat is aan het accent te zien dat ποιῶ, τιμῶ en δηλῶ contracta zijn?",
            "antwoord": [
                "een verplichte circumflex op de gecontracteerde lange klinker",
                "circumflex op de ultima bij 1 sg.",
            ],
            "feedback": "Contracta krijgen in de 1 sg. steeds een circumflex op de gecontracteerde ω — signaal dat daar twee klinkers zijn samengetrokken.",
            "bron": "handmatig",
        },
    ]


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------


def collect_all() -> dict[str, list[dict]]:
    primary_map: dict[str, list[dict]] = {}
    all_items: list[dict] = []
    all_items.extend(praes_them_items())
    all_items.extend(contr_intro_items())
    all_items.extend(contr_a_items())
    all_items.extend(contr_e_items())
    all_items.extend(eimi_items())
    all_items.extend(inf_praes_items())
    all_items.extend(paradigma_items())

    # Clean up placeholder fields + NFC-normaliseer
    for item in all_items:
        item.pop("discriminatie_initueel_placeholder", None)
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
    richting_counter: Counter[str] = Counter()
    per_knoop: Counter[str] = Counter()
    for knoop_id, item_list in items_by_knoop.items():
        per_knoop[knoop_id] = len(item_list)
        for item in item_list:
            type_counter[item["type"]] += 1
            richting_counter[item["richting"]] += 1

    print("\n=== E3-07 Summary ===")
    print(f"Knopen: {len(items_by_knoop)}")
    print(f"Total items: {total}")
    print("\nItems per knoop:")
    for k, c in per_knoop.most_common():
        print(f"  {k}: {c}")
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
