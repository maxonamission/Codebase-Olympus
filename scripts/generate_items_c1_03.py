#!/usr/bin/env python3
"""Generate exercise items for C1-03: 2e declinatie (A1-03 knopen).

Targets:
  - data/graph/lat_grammatica_poc.json  (DECL2-INTRO, NOM-D2..VOC-D2)
  - data/graph/lat_grammatica_leerjaar1.json (DECL2-STAM, DECL2-MASC, DECL2-ER, DECL2-NEUT, DECL2-PARAD)
~35 items total.
"""

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from gymnasium_classica.models.graph import Item

# ── Which knopen live in which file ──────────────────────────────────
POC_KNOOP_IDS = {
    "LAT-G-MORF-DECL2-INTRO",
    "LAT-G-MORF-NOM-D2",
    "LAT-G-MORF-GEN-D2",
    "LAT-G-MORF-DAT-D2",
    "LAT-G-MORF-ACC-D2",
    "LAT-G-MORF-ABL-D2",
    "LAT-G-MORF-VOC-D2",
}
LJ1_KNOOP_IDS = {
    "LAT-G-MORF-DECL2-STAM",
    "LAT-G-MORF-DECL2-MASC",
    "LAT-G-MORF-DECL2-ER",
    "LAT-G-MORF-DECL2-NEUT",
    "LAT-G-MORF-DECL2-PARAD",
}


def define_items() -> dict[str, list[dict]]:
    """Return node_id -> list of item dicts."""
    items: dict[str, list[dict]] = {}

    # ── DECL2-INTRO (kennis, 3 herkenning) ───────────────────────────

    items["LAT-G-MORF-DECL2-INTRO"] = [
        {
            "id": "ITEM-LAT-G-MORF-DECL2-INTRO-001",
            "knoop_ids": ["LAT-G-MORF-DECL2-INTRO"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.6,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 12,
            "stimulus": "Op welke uitgang eindigen de meeste masculina van de 2e declinatie in de nominativus singularis?",
            "antwoord": "-us",
            "feedback": "Het hoofdpatroon van de 2e declinatie masculinum is nominativus sg. op -us. Bijv. dominus, servus, amicus.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-LAT-G-MORF-DECL2-INTRO-002",
            "knoop_ids": ["LAT-G-MORF-DECL2-INTRO"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.3,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 12,
            "stimulus": "Hoe herken je in het woordenboek dat een woord bij de 2e declinatie hoort?",
            "antwoord": "de genitivus singularis eindigt op -i",
            "feedback": "Een woord hoort bij de 2e declinatie als de genitivus singularis op -i eindigt. Bijv. dominus, -i (m.).",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-LAT-G-MORF-DECL2-INTRO-003",
            "knoop_ids": ["LAT-G-MORF-DECL2-INTRO"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.2,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 15,
            "stimulus": "Welke drie nominativus-uitgangen komen voor bij de 2e declinatie?",
            "antwoord": "-us, -er, -um",
            "feedback": "De 2e declinatie kent drie subtypen: -us (dominus), -er (puer/ager) en -um (bellum, neutrum).",
            "bron": "handmatig",
        },
    ]

    # ── NOM-D2 ────────────────────────────────────────────────────────

    items["LAT-G-MORF-NOM-D2"] = [
        {
            "id": "ITEM-LAT-G-MORF-NOM-D2-001",
            "knoop_ids": ["LAT-G-MORF-NOM-D2"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.3,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 10,
            "stimulus": "Welke naamval is 'domini'?",
            "antwoord": ["genitivus singularis of nominativus pluralis"],
            "feedback": "'Domini' kan genitivus sg. (-i) of nominativus pl. (-i) zijn. Context bepaalt de functie.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-LAT-G-MORF-NOM-D2-002",
            "knoop_ids": ["LAT-G-MORF-NOM-D2"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.5,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 20,
            "stimulus": "Geef de nominativus meervoud van 'dominus'.",
            "antwoord": "domini",
            "feedback": "De nominativus meervoud van de 2e declinatie masc. eindigt op -i: dominus → domini.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-LAT-G-MORF-NOM-D2-003",
            "knoop_ids": ["LAT-G-MORF-NOM-D2"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.7,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 20,
            "stimulus": "Geef de nominativus meervoud van 'bellum'.",
            "antwoord": "bella",
            "feedback": "Bij neutra eindigt de nominativus meervoud op -a: bellum → bella (neutrumregel).",
            "bron": "handmatig",
        },
    ]

    # ── GEN-D2 ────────────────────────────────────────────────────────

    items["LAT-G-MORF-GEN-D2"] = [
        {
            "id": "ITEM-LAT-G-MORF-GEN-D2-001",
            "knoop_ids": ["LAT-G-MORF-GEN-D2"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.2,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 10,
            "stimulus": "Wat is de genitivus-uitgang van de 2e declinatie in het enkelvoud?",
            "antwoord": "-i",
            "feedback": "De genitivus singularis van de 2e declinatie eindigt op -i. Dit geldt voor alle subtypen (-us, -er, -um).",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-LAT-G-MORF-GEN-D2-002",
            "knoop_ids": ["LAT-G-MORF-GEN-D2"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.5,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 20,
            "stimulus": "Geef de genitivus meervoud van 'servus'.",
            "antwoord": "servorum",
            "feedback": "De genitivus meervoud van de 2e declinatie eindigt op -ōrum: servus → servōrum.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-LAT-G-MORF-GEN-D2-003",
            "knoop_ids": ["LAT-G-MORF-GEN-D2"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.6,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 20,
            "stimulus": "Geef de genitivus enkelvoud van 'bellum'.",
            "antwoord": "belli",
            "feedback": "De genitivus singularis van neutra van de 2e declinatie eindigt op -i: bellum → belli.",
            "bron": "handmatig",
        },
    ]

    # ── DAT-D2 ────────────────────────────────────────────────────────

    items["LAT-G-MORF-DAT-D2"] = [
        {
            "id": "ITEM-LAT-G-MORF-DAT-D2-001",
            "knoop_ids": ["LAT-G-MORF-DAT-D2"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.1,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 10,
            "stimulus": "Wat is de dativus-uitgang van de 2e declinatie in het enkelvoud?",
            "antwoord": "-o",
            "feedback": "De dativus singularis van de 2e declinatie eindigt op -ō. Dit geldt voor alle subtypen.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-LAT-G-MORF-DAT-D2-002",
            "knoop_ids": ["LAT-G-MORF-DAT-D2"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.6,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 20,
            "stimulus": "Geef de dativus enkelvoud van 'dominus'.",
            "antwoord": "domino",
            "feedback": "De dativus singularis van de 2e declinatie eindigt op -ō: dominus → dominō.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-LAT-G-MORF-DAT-D2-003",
            "knoop_ids": ["LAT-G-MORF-DAT-D2"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.6,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 20,
            "stimulus": "Geef de dativus meervoud van 'servus'.",
            "antwoord": "servis",
            "feedback": "De dativus meervoud van de 2e declinatie eindigt op -īs: servus → servīs. Dit is gelijk aan de ablativus pl.",
            "bron": "handmatig",
        },
    ]

    # ── ACC-D2 ────────────────────────────────────────────────────────

    items["LAT-G-MORF-ACC-D2"] = [
        {
            "id": "ITEM-LAT-G-MORF-ACC-D2-001",
            "knoop_ids": ["LAT-G-MORF-ACC-D2"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.2,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 10,
            "stimulus": "Welke naamval is 'dominum'?",
            "antwoord": "accusativus singularis",
            "feedback": "De uitgang -um is bij masculina van de 2e declinatie de accusativus singularis.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-LAT-G-MORF-ACC-D2-002",
            "knoop_ids": ["LAT-G-MORF-ACC-D2"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.5,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 20,
            "stimulus": "Geef de accusativus meervoud van 'dominus'.",
            "antwoord": "dominos",
            "feedback": "De accusativus meervoud van de 2e declinatie masc. eindigt op -ōs: dominus → dominōs.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-LAT-G-MORF-ACC-D2-003",
            "knoop_ids": ["LAT-G-MORF-ACC-D2"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.2,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 12,
            "stimulus": "Wat is de accusativus enkelvoud van een neutrum van de 2e declinatie (bijv. 'bellum')?",
            "antwoord": "bellum (gelijk aan de nominativus)",
            "feedback": "Bij neutra zijn nominativus en accusativus altijd gelijk (neutrumregel): bellum blijft bellum.",
            "bron": "handmatig",
        },
    ]

    # ── ABL-D2 ────────────────────────────────────────────────────────

    items["LAT-G-MORF-ABL-D2"] = [
        {
            "id": "ITEM-LAT-G-MORF-ABL-D2-001",
            "knoop_ids": ["LAT-G-MORF-ABL-D2"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.1,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 10,
            "stimulus": "Wat is de ablativus-uitgang van de 2e declinatie in het enkelvoud?",
            "antwoord": "-o",
            "feedback": "De ablativus singularis van de 2e declinatie eindigt op -ō. Dit is gelijk aan de dativus sg.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-LAT-G-MORF-ABL-D2-002",
            "knoop_ids": ["LAT-G-MORF-ABL-D2"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.5,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 20,
            "stimulus": "Geef de ablativus meervoud van 'bellum'.",
            "antwoord": "bellis",
            "feedback": "De ablativus meervoud van de 2e declinatie eindigt op -īs: bellum → bellīs. Dit geldt voor alle subtypen.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-LAT-G-MORF-ABL-D2-003",
            "knoop_ids": ["LAT-G-MORF-ABL-D2"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.6,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 20,
            "stimulus": "Geef de ablativus enkelvoud van 'amicus'.",
            "antwoord": "amico",
            "feedback": "De ablativus singularis van de 2e declinatie eindigt op -ō: amicus → amicō.",
            "bron": "handmatig",
        },
    ]

    # ── VOC-D2 ────────────────────────────────────────────────────────

    items["LAT-G-MORF-VOC-D2"] = [
        {
            "id": "ITEM-LAT-G-MORF-VOC-D2-001",
            "knoop_ids": ["LAT-G-MORF-VOC-D2"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.0,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 12,
            "stimulus": "Wat is de vocativus singularis van woorden op -us in de 2e declinatie?",
            "antwoord": "-e (bijv. domine!)",
            "feedback": "Bij -us woorden eindigt de vocativus sg. op -e: dominus → domine! Dit is de enige naamval die afwijkt van de nominativus.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-LAT-G-MORF-VOC-D2-002",
            "knoop_ids": ["LAT-G-MORF-VOC-D2"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.7,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 20,
            "stimulus": "Hoe spreek je een heer (dominus) direct aan in het Latijn?",
            "antwoord": "domine!",
            "feedback": "De vocativus singularis van dominus is domine! (uitgang -e in plaats van -us).",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-LAT-G-MORF-VOC-D2-003",
            "knoop_ids": ["LAT-G-MORF-VOC-D2"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.5,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 15,
            "stimulus": "Wat is de vocativus singularis van 'filius'?",
            "antwoord": "fili",
            "feedback": "Woorden op -ius hebben een bijzondere vocativus sg. op -i (niet -ie): filius → fili!",
            "bron": "handmatig",
        },
    ]

    # ── DECL2-STAM (leerjaar1.json) ──────────────────────────────────

    items["LAT-G-MORF-DECL2-STAM"] = [
        {
            "id": "ITEM-LAT-G-MORF-DECL2-STAM-001",
            "knoop_ids": ["LAT-G-MORF-DECL2-STAM"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.2,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 12,
            "stimulus": "Hoe bepaal je de stam van een 2e-declinatiewoord?",
            "antwoord": "haal -i van de genitivus singularis af",
            "feedback": "De stam vind je door -i van de genitivus singularis af te halen. Bijv. domin-i → stam domin-.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-LAT-G-MORF-DECL2-STAM-002",
            "knoop_ids": ["LAT-G-MORF-DECL2-STAM"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.4,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 20,
            "stimulus": "Wat is de stam van 'servus, servi'?",
            "antwoord": "serv-",
            "feedback": "Genitivus serv-i → stam serv-. Aan deze stam plak je de naamvalsuitgangen.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-LAT-G-MORF-DECL2-STAM-003",
            "knoop_ids": ["LAT-G-MORF-DECL2-STAM"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.7,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 20,
            "stimulus": "Wat is de stam van 'ager, agri'?",
            "antwoord": "agr-",
            "feedback": "Genitivus agr-i → stam agr-. Let op: de -e- uit de nominativus 'ager' valt weg. De genitivus toont de ware stam.",
            "bron": "handmatig",
        },
    ]

    # ── DECL2-MASC (leerjaar1.json) ──────────────────────────────────

    items["LAT-G-MORF-DECL2-MASC"] = [
        {
            "id": "ITEM-LAT-G-MORF-DECL2-MASC-001",
            "knoop_ids": ["LAT-G-MORF-DECL2-MASC"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.3,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 10,
            "stimulus": "Wat is het modelwoord voor het -us-patroon van de 2e declinatie?",
            "antwoord": "dominus, -i (m.)",
            "feedback": "Dominus, -i (m.) is het modelwoord voor het hoofdpatroon van de 2e declinatie masculinum.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-LAT-G-MORF-DECL2-MASC-002",
            "knoop_ids": ["LAT-G-MORF-DECL2-MASC"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.5,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 20,
            "stimulus": "Geef de accusativus enkelvoud van 'amicus'.",
            "antwoord": "amicum",
            "feedback": "De accusativus singularis van -us woorden eindigt op -um: amicus → amicum.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-LAT-G-MORF-DECL2-MASC-003",
            "knoop_ids": ["LAT-G-MORF-DECL2-MASC"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.6,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 25,
            "stimulus": "Geef de dativus meervoud van 'amicus'.",
            "antwoord": "amicis",
            "feedback": "De dativus meervoud van de 2e declinatie eindigt op -īs: amicus → amicīs.",
            "bron": "handmatig",
        },
    ]

    # ── DECL2-ER (leerjaar1.json) ────────────────────────────────────

    items["LAT-G-MORF-DECL2-ER"] = [
        {
            "id": "ITEM-LAT-G-MORF-DECL2-ER-001",
            "knoop_ids": ["LAT-G-MORF-DECL2-ER"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.2,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 15,
            "stimulus": "Wat is het verschil tussen 'puer, pueri' en 'ager, agri'?",
            "antwoord": "puer behoudt de -e- in de stam (puer-), ager verliest de -e- (agr-)",
            "feedback": "Bij puer, pueri blijft de -e- in alle vormen (stam puer-). Bij ager, agri valt de -e- weg (stam agr-). De genitivus toont de ware stam.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-LAT-G-MORF-DECL2-ER-002",
            "knoop_ids": ["LAT-G-MORF-DECL2-ER"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.8,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 25,
            "stimulus": "Geef de genitivus meervoud van 'ager'.",
            "antwoord": "agrorum",
            "feedback": "De stam van ager is agr- (genitivus agri). Gen. pl.: agr- + -ōrum = agrōrum.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-LAT-G-MORF-DECL2-ER-003",
            "knoop_ids": ["LAT-G-MORF-DECL2-ER"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.6,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 25,
            "stimulus": "Geef de accusativus enkelvoud van 'puer'.",
            "antwoord": "puerum",
            "feedback": "De stam van puer is puer- (genitivus pueri). Acc. sg.: puer- + -um = puerum.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-LAT-G-MORF-DECL2-ER-004",
            "knoop_ids": ["LAT-G-MORF-DECL2-ER"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.9,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 25,
            "stimulus": "Geef de ablativus enkelvoud van 'ager'.",
            "antwoord": "agro",
            "feedback": "Stam agr- + uitgang -ō = agrō. Let op: niet 'agero' — de -e- uit de nominativus valt weg.",
            "bron": "handmatig",
        },
    ]

    # ── DECL2-NEUT (leerjaar1.json) ──────────────────────────────────

    items["LAT-G-MORF-DECL2-NEUT"] = [
        {
            "id": "ITEM-LAT-G-MORF-DECL2-NEUT-001",
            "knoop_ids": ["LAT-G-MORF-DECL2-NEUT"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.1,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 12,
            "stimulus": "Wat is de neutrumregel?",
            "antwoord": "bij neutra zijn nominativus en accusativus altijd gelijk; in het meervoud eindigen ze op -a",
            "feedback": "De neutrumregel: nom. = acc. in alle numeri. In het meervoud eindigen nom. en acc. altijd op -a.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-LAT-G-MORF-DECL2-NEUT-002",
            "knoop_ids": ["LAT-G-MORF-DECL2-NEUT"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.6,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 20,
            "stimulus": "Geef de accusativus meervoud van 'bellum'.",
            "antwoord": "bella",
            "feedback": "Neutrumregel: acc. pl. = nom. pl. Bij neutra van de 2e declinatie is dat -a: bellum → bella.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-LAT-G-MORF-DECL2-NEUT-003",
            "knoop_ids": ["LAT-G-MORF-DECL2-NEUT"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.7,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 20,
            "stimulus": "Geef de nominativus meervoud van 'templum'.",
            "antwoord": "templa",
            "feedback": "Neutrumregel: nom. pl. van neutra eindigt op -a: templum → templa. Niet verwarren met 1e declinatie femininum -a (sg.).",
            "bron": "handmatig",
        },
    ]

    # ── DECL2-PARAD (leerjaar1.json, 5 items incl. analyse) ─────────

    items["LAT-G-MORF-DECL2-PARAD"] = [
        {
            "id": "ITEM-LAT-G-MORF-DECL2-PARAD-001",
            "knoop_ids": ["LAT-G-MORF-DECL2-PARAD"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.0,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 12,
            "stimulus": "Welke twee naamvallen van de 2e declinatie enkelvoud hebben dezelfde uitgang -o?",
            "antwoord": "dativus singularis en ablativus singularis",
            "feedback": "De dativus en ablativus singularis van de 2e declinatie eindigen beiden op -ō. Context bepaalt de functie.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-LAT-G-MORF-DECL2-PARAD-002",
            "knoop_ids": ["LAT-G-MORF-DECL2-PARAD"],
            "type": "analyse",
            "richting": "receptief",
            "moeilijkheid_initieel": 1.0,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 30,
            "stimulus": "Ontleed 'dominorum' volledig.",
            "antwoord": "genitivus pluralis, 2e declinatie",
            "feedback": "Domin-ōrum: stam domin- + uitgang -ōrum = genitivus pluralis van de 2e declinatie.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-LAT-G-MORF-DECL2-PARAD-003",
            "knoop_ids": ["LAT-G-MORF-DECL2-PARAD"],
            "type": "analyse",
            "richting": "receptief",
            "moeilijkheid_initieel": 1.3,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 35,
            "stimulus": "Ontleed 'agris' volledig.",
            "antwoord": ["dativus pluralis of ablativus pluralis, 2e declinatie"],
            "feedback": "Agr-īs: stam agr- (van ager, agri) + uitgang -īs = dativus of ablativus pluralis van de 2e declinatie.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-LAT-G-MORF-DECL2-PARAD-004",
            "knoop_ids": ["LAT-G-MORF-DECL2-PARAD"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.8,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 25,
            "stimulus": "Verbuig 'bellum' in de genitivus singularis en meervoud.",
            "antwoord": "belli, bellorum",
            "feedback": "Gen. sg. bell-i, gen. pl. bell-ōrum. Bij neutra volgt de genitivus hetzelfde patroon als bij masculina.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-LAT-G-MORF-DECL2-PARAD-005",
            "knoop_ids": ["LAT-G-MORF-DECL2-PARAD"],
            "type": "analyse",
            "richting": "receptief",
            "moeilijkheid_initieel": 1.5,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 35,
            "stimulus": "Ontleed 'bella' volledig. Geef alle mogelijke analyses.",
            "antwoord": [
                "nominativus pluralis neutrum of accusativus pluralis neutrum, 2e declinatie"
            ],
            "feedback": "'Bella' kan nom. pl. of acc. pl. zijn (neutrumregel). Niet verwarren met 1e-declinatie nom. sg. fem. — 'bella' als neutrum pl. van 'bellum'.",
            "bron": "handmatig",
        },
    ]

    return items


def validate_items(items_by_node: dict[str, list[dict]]) -> None:
    """Validate all items via Pydantic model."""
    for _node_id, item_list in items_by_node.items():
        for item_dict in item_list:
            Item(**item_dict)
    print("All items validated successfully.")


def add_items_to_json(json_path: Path, items_by_node: dict[str, list[dict]]) -> int:
    """Load JSON, add items to matching knopen, write back. Returns count added."""
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
    """Print summary statistics."""
    total = sum(len(v) for v in items_by_node.values())
    type_counter: Counter[str] = Counter()
    richting_counter: Counter[str] = Counter()
    for item_list in items_by_node.values():
        for item in item_list:
            type_counter[item["type"]] += 1
            richting_counter[item["richting"]] += 1

    print("\n=== C1-03 Summary ===")
    print(f"Knopen: {len(items_by_node)}")
    print(f"Total items: {total}")
    print("\nItems per node:")
    for kid, item_list in sorted(items_by_node.items()):
        print(f"  {kid}: {len(item_list)}")
    print("\nOefentype-verdeling:")
    for t, c in type_counter.most_common():
        print(f"  {t}: {c}")
    print("\nRichting-verdeling:")
    for r, c in richting_counter.most_common():
        print(f"  {r}: {c}")


def main() -> None:
    items_by_node = define_items()
    validate_items(items_by_node)

    base = Path(__file__).parent.parent / "data" / "graph"
    poc_path = base / "lat_grammatica_poc.json"
    lj1_path = base / "lat_grammatica_leerjaar1.json"

    poc_items = {k: v for k, v in items_by_node.items() if k in POC_KNOOP_IDS}
    lj1_items = {k: v for k, v in items_by_node.items() if k in LJ1_KNOOP_IDS}

    added_poc = add_items_to_json(poc_path, poc_items)
    added_lj1 = add_items_to_json(lj1_path, lj1_items)

    print(f"Added {added_poc} items to {poc_path.name}")
    print(f"Added {added_lj1} items to {lj1_path.name}")

    print_summary(items_by_node)


if __name__ == "__main__":
    main()
