#!/usr/bin/env python3
"""Generate exercise items for C1-03: 2e declinatie (A1-03 nodes).

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

# ── Which nodes live in which file ──────────────────────────────────
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
            "node_ids": ["LAT-G-MORF-DECL2-INTRO"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": -0.6,
            "discrimination_initial": 1.0,
            "expected_time_sec": 12,
            "stimulus": "Op welke uitgang eindigen de meeste masculina van de 2e declinatie in de nominativus singularis?",
            "answer": "-us",
            "feedback": "Het hoofdpatroon van de 2e declinatie masculinum is nominativus sg. op -us. Bijv. dominus, servus, amicus.",
            "source": "manual",
        },
        {
            "id": "ITEM-LAT-G-MORF-DECL2-INTRO-002",
            "node_ids": ["LAT-G-MORF-DECL2-INTRO"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": -0.3,
            "discrimination_initial": 1.0,
            "expected_time_sec": 12,
            "stimulus": "Hoe herken je in het woordenboek dat een woord bij de 2e declinatie hoort?",
            "answer": "de genitivus singularis eindigt op -i",
            "feedback": "Een woord hoort bij de 2e declinatie als de genitivus singularis op -i eindigt. Bijv. dominus, -i (m.).",
            "source": "manual",
        },
        {
            "id": "ITEM-LAT-G-MORF-DECL2-INTRO-003",
            "node_ids": ["LAT-G-MORF-DECL2-INTRO"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": -0.2,
            "discrimination_initial": 1.0,
            "expected_time_sec": 15,
            "stimulus": "Welke drie nominativus-uitgangen komen voor bij de 2e declinatie?",
            "answer": "-us, -er, -um",
            "feedback": "De 2e declinatie kent drie subtypen: -us (dominus), -er (puer/ager) en -um (bellum, neutrum).",
            "source": "manual",
        },
    ]

    # ── NOM-D2 ────────────────────────────────────────────────────────

    items["LAT-G-MORF-NOM-D2"] = [
        {
            "id": "ITEM-LAT-G-MORF-NOM-D2-001",
            "node_ids": ["LAT-G-MORF-NOM-D2"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": -0.3,
            "discrimination_initial": 1.0,
            "expected_time_sec": 10,
            "stimulus": "Welke naamval is 'domini'?",
            "answer": ["genitivus singularis of nominativus pluralis"],
            "feedback": "'Domini' kan genitivus sg. (-i) of nominativus pl. (-i) zijn. Context bepaalt de functie.",
            "source": "manual",
        },
        {
            "id": "ITEM-LAT-G-MORF-NOM-D2-002",
            "node_ids": ["LAT-G-MORF-NOM-D2"],
            "type": "production",
            "direction": "productive",
            "difficulty_initial": 0.5,
            "discrimination_initial": 1.0,
            "expected_time_sec": 20,
            "stimulus": "Geef de nominativus meervoud van 'dominus'.",
            "answer": "domini",
            "feedback": "De nominativus meervoud van de 2e declinatie masc. eindigt op -i: dominus → domini.",
            "source": "manual",
        },
        {
            "id": "ITEM-LAT-G-MORF-NOM-D2-003",
            "node_ids": ["LAT-G-MORF-NOM-D2"],
            "type": "production",
            "direction": "productive",
            "difficulty_initial": 0.7,
            "discrimination_initial": 1.0,
            "expected_time_sec": 20,
            "stimulus": "Geef de nominativus meervoud van 'bellum'.",
            "answer": "bella",
            "feedback": "Bij neutra eindigt de nominativus meervoud op -a: bellum → bella (neutrumregel).",
            "source": "manual",
        },
    ]

    # ── GEN-D2 ────────────────────────────────────────────────────────

    items["LAT-G-MORF-GEN-D2"] = [
        {
            "id": "ITEM-LAT-G-MORF-GEN-D2-001",
            "node_ids": ["LAT-G-MORF-GEN-D2"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": -0.2,
            "discrimination_initial": 1.0,
            "expected_time_sec": 10,
            "stimulus": "Wat is de genitivus-uitgang van de 2e declinatie in het enkelvoud?",
            "answer": "-i",
            "feedback": "De genitivus singularis van de 2e declinatie eindigt op -i. Dit geldt voor alle subtypen (-us, -er, -um).",
            "source": "manual",
        },
        {
            "id": "ITEM-LAT-G-MORF-GEN-D2-002",
            "node_ids": ["LAT-G-MORF-GEN-D2"],
            "type": "production",
            "direction": "productive",
            "difficulty_initial": 0.5,
            "discrimination_initial": 1.0,
            "expected_time_sec": 20,
            "stimulus": "Geef de genitivus meervoud van 'servus'.",
            "answer": "servorum",
            "feedback": "De genitivus meervoud van de 2e declinatie eindigt op -ōrum: servus → servōrum.",
            "source": "manual",
        },
        {
            "id": "ITEM-LAT-G-MORF-GEN-D2-003",
            "node_ids": ["LAT-G-MORF-GEN-D2"],
            "type": "production",
            "direction": "productive",
            "difficulty_initial": 0.6,
            "discrimination_initial": 1.0,
            "expected_time_sec": 20,
            "stimulus": "Geef de genitivus enkelvoud van 'bellum'.",
            "answer": "belli",
            "feedback": "De genitivus singularis van neutra van de 2e declinatie eindigt op -i: bellum → belli.",
            "source": "manual",
        },
    ]

    # ── DAT-D2 ────────────────────────────────────────────────────────

    items["LAT-G-MORF-DAT-D2"] = [
        {
            "id": "ITEM-LAT-G-MORF-DAT-D2-001",
            "node_ids": ["LAT-G-MORF-DAT-D2"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": -0.1,
            "discrimination_initial": 1.0,
            "expected_time_sec": 10,
            "stimulus": "Wat is de dativus-uitgang van de 2e declinatie in het enkelvoud?",
            "answer": "-o",
            "feedback": "De dativus singularis van de 2e declinatie eindigt op -ō. Dit geldt voor alle subtypen.",
            "source": "manual",
        },
        {
            "id": "ITEM-LAT-G-MORF-DAT-D2-002",
            "node_ids": ["LAT-G-MORF-DAT-D2"],
            "type": "production",
            "direction": "productive",
            "difficulty_initial": 0.6,
            "discrimination_initial": 1.0,
            "expected_time_sec": 20,
            "stimulus": "Geef de dativus enkelvoud van 'dominus'.",
            "answer": "domino",
            "feedback": "De dativus singularis van de 2e declinatie eindigt op -ō: dominus → dominō.",
            "source": "manual",
        },
        {
            "id": "ITEM-LAT-G-MORF-DAT-D2-003",
            "node_ids": ["LAT-G-MORF-DAT-D2"],
            "type": "production",
            "direction": "productive",
            "difficulty_initial": 0.6,
            "discrimination_initial": 1.0,
            "expected_time_sec": 20,
            "stimulus": "Geef de dativus meervoud van 'servus'.",
            "answer": "servis",
            "feedback": "De dativus meervoud van de 2e declinatie eindigt op -īs: servus → servīs. Dit is gelijk aan de ablativus pl.",
            "source": "manual",
        },
    ]

    # ── ACC-D2 ────────────────────────────────────────────────────────

    items["LAT-G-MORF-ACC-D2"] = [
        {
            "id": "ITEM-LAT-G-MORF-ACC-D2-001",
            "node_ids": ["LAT-G-MORF-ACC-D2"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": -0.2,
            "discrimination_initial": 1.0,
            "expected_time_sec": 10,
            "stimulus": "Welke naamval is 'dominum'?",
            "answer": "accusativus singularis",
            "feedback": "De uitgang -um is bij masculina van de 2e declinatie de accusativus singularis.",
            "source": "manual",
        },
        {
            "id": "ITEM-LAT-G-MORF-ACC-D2-002",
            "node_ids": ["LAT-G-MORF-ACC-D2"],
            "type": "production",
            "direction": "productive",
            "difficulty_initial": 0.5,
            "discrimination_initial": 1.0,
            "expected_time_sec": 20,
            "stimulus": "Geef de accusativus meervoud van 'dominus'.",
            "answer": "dominos",
            "feedback": "De accusativus meervoud van de 2e declinatie masc. eindigt op -ōs: dominus → dominōs.",
            "source": "manual",
        },
        {
            "id": "ITEM-LAT-G-MORF-ACC-D2-003",
            "node_ids": ["LAT-G-MORF-ACC-D2"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": 0.2,
            "discrimination_initial": 1.0,
            "expected_time_sec": 12,
            "stimulus": "Wat is de accusativus enkelvoud van een neutrum van de 2e declinatie (bijv. 'bellum')?",
            "answer": "bellum (gelijk aan de nominativus)",
            "feedback": "Bij neutra zijn nominativus en accusativus altijd gelijk (neutrumregel): bellum blijft bellum.",
            "source": "manual",
        },
    ]

    # ── ABL-D2 ────────────────────────────────────────────────────────

    items["LAT-G-MORF-ABL-D2"] = [
        {
            "id": "ITEM-LAT-G-MORF-ABL-D2-001",
            "node_ids": ["LAT-G-MORF-ABL-D2"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": -0.1,
            "discrimination_initial": 1.0,
            "expected_time_sec": 10,
            "stimulus": "Wat is de ablativus-uitgang van de 2e declinatie in het enkelvoud?",
            "answer": "-o",
            "feedback": "De ablativus singularis van de 2e declinatie eindigt op -ō. Dit is gelijk aan de dativus sg.",
            "source": "manual",
        },
        {
            "id": "ITEM-LAT-G-MORF-ABL-D2-002",
            "node_ids": ["LAT-G-MORF-ABL-D2"],
            "type": "production",
            "direction": "productive",
            "difficulty_initial": 0.5,
            "discrimination_initial": 1.0,
            "expected_time_sec": 20,
            "stimulus": "Geef de ablativus meervoud van 'bellum'.",
            "answer": "bellis",
            "feedback": "De ablativus meervoud van de 2e declinatie eindigt op -īs: bellum → bellīs. Dit geldt voor alle subtypen.",
            "source": "manual",
        },
        {
            "id": "ITEM-LAT-G-MORF-ABL-D2-003",
            "node_ids": ["LAT-G-MORF-ABL-D2"],
            "type": "production",
            "direction": "productive",
            "difficulty_initial": 0.6,
            "discrimination_initial": 1.0,
            "expected_time_sec": 20,
            "stimulus": "Geef de ablativus enkelvoud van 'amicus'.",
            "answer": "amico",
            "feedback": "De ablativus singularis van de 2e declinatie eindigt op -ō: amicus → amicō.",
            "source": "manual",
        },
    ]

    # ── VOC-D2 ────────────────────────────────────────────────────────

    items["LAT-G-MORF-VOC-D2"] = [
        {
            "id": "ITEM-LAT-G-MORF-VOC-D2-001",
            "node_ids": ["LAT-G-MORF-VOC-D2"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": 0.0,
            "discrimination_initial": 1.0,
            "expected_time_sec": 12,
            "stimulus": "Wat is de vocativus singularis van woorden op -us in de 2e declinatie?",
            "answer": "-e (bijv. domine!)",
            "feedback": "Bij -us woorden eindigt de vocativus sg. op -e: dominus → domine! Dit is de enige naamval die afwijkt van de nominativus.",
            "source": "manual",
        },
        {
            "id": "ITEM-LAT-G-MORF-VOC-D2-002",
            "node_ids": ["LAT-G-MORF-VOC-D2"],
            "type": "production",
            "direction": "productive",
            "difficulty_initial": 0.7,
            "discrimination_initial": 1.0,
            "expected_time_sec": 20,
            "stimulus": "Hoe spreek je een heer (dominus) direct aan in het Latijn?",
            "answer": "domine!",
            "feedback": "De vocativus singularis van dominus is domine! (uitgang -e in plaats van -us).",
            "source": "manual",
        },
        {
            "id": "ITEM-LAT-G-MORF-VOC-D2-003",
            "node_ids": ["LAT-G-MORF-VOC-D2"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": 0.5,
            "discrimination_initial": 1.2,
            "expected_time_sec": 15,
            "stimulus": "Wat is de vocativus singularis van 'filius'?",
            "answer": "fili",
            "feedback": "Woorden op -ius hebben een bijzondere vocativus sg. op -i (niet -ie): filius → fili!",
            "source": "manual",
        },
    ]

    # ── DECL2-STAM (leerjaar1.json) ──────────────────────────────────

    items["LAT-G-MORF-DECL2-STAM"] = [
        {
            "id": "ITEM-LAT-G-MORF-DECL2-STAM-001",
            "node_ids": ["LAT-G-MORF-DECL2-STAM"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": -0.2,
            "discrimination_initial": 1.0,
            "expected_time_sec": 12,
            "stimulus": "Hoe bepaal je de stam van een 2e-declinatiewoord?",
            "answer": "haal -i van de genitivus singularis af",
            "feedback": "De stam vind je door -i van de genitivus singularis af te halen. Bijv. domin-i → stam domin-.",
            "source": "manual",
        },
        {
            "id": "ITEM-LAT-G-MORF-DECL2-STAM-002",
            "node_ids": ["LAT-G-MORF-DECL2-STAM"],
            "type": "production",
            "direction": "productive",
            "difficulty_initial": 0.4,
            "discrimination_initial": 1.0,
            "expected_time_sec": 20,
            "stimulus": "Wat is de stam van 'servus, servi'?",
            "answer": "serv-",
            "feedback": "Genitivus serv-i → stam serv-. Aan deze stam plak je de naamvalsuitgangen.",
            "source": "manual",
        },
        {
            "id": "ITEM-LAT-G-MORF-DECL2-STAM-003",
            "node_ids": ["LAT-G-MORF-DECL2-STAM"],
            "type": "production",
            "direction": "productive",
            "difficulty_initial": 0.7,
            "discrimination_initial": 1.0,
            "expected_time_sec": 20,
            "stimulus": "Wat is de stam van 'ager, agri'?",
            "answer": "agr-",
            "feedback": "Genitivus agr-i → stam agr-. Let op: de -e- uit de nominativus 'ager' valt weg. De genitivus toont de ware stam.",
            "source": "manual",
        },
    ]

    # ── DECL2-MASC (leerjaar1.json) ──────────────────────────────────

    items["LAT-G-MORF-DECL2-MASC"] = [
        {
            "id": "ITEM-LAT-G-MORF-DECL2-MASC-001",
            "node_ids": ["LAT-G-MORF-DECL2-MASC"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": -0.3,
            "discrimination_initial": 1.0,
            "expected_time_sec": 10,
            "stimulus": "Wat is het modelwoord voor het -us-patroon van de 2e declinatie?",
            "answer": "dominus, -i (m.)",
            "feedback": "Dominus, -i (m.) is het modelwoord voor het hoofdpatroon van de 2e declinatie masculinum.",
            "source": "manual",
        },
        {
            "id": "ITEM-LAT-G-MORF-DECL2-MASC-002",
            "node_ids": ["LAT-G-MORF-DECL2-MASC"],
            "type": "production",
            "direction": "productive",
            "difficulty_initial": 0.5,
            "discrimination_initial": 1.0,
            "expected_time_sec": 20,
            "stimulus": "Geef de accusativus enkelvoud van 'amicus'.",
            "answer": "amicum",
            "feedback": "De accusativus singularis van -us woorden eindigt op -um: amicus → amicum.",
            "source": "manual",
        },
        {
            "id": "ITEM-LAT-G-MORF-DECL2-MASC-003",
            "node_ids": ["LAT-G-MORF-DECL2-MASC"],
            "type": "production",
            "direction": "productive",
            "difficulty_initial": 0.6,
            "discrimination_initial": 1.0,
            "expected_time_sec": 25,
            "stimulus": "Geef de dativus meervoud van 'amicus'.",
            "answer": "amicis",
            "feedback": "De dativus meervoud van de 2e declinatie eindigt op -īs: amicus → amicīs.",
            "source": "manual",
        },
    ]

    # ── DECL2-ER (leerjaar1.json) ────────────────────────────────────

    items["LAT-G-MORF-DECL2-ER"] = [
        {
            "id": "ITEM-LAT-G-MORF-DECL2-ER-001",
            "node_ids": ["LAT-G-MORF-DECL2-ER"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": 0.2,
            "discrimination_initial": 1.2,
            "expected_time_sec": 15,
            "stimulus": "Wat is het verschil tussen 'puer, pueri' en 'ager, agri'?",
            "answer": "puer behoudt de -e- in de stam (puer-), ager verliest de -e- (agr-)",
            "feedback": "Bij puer, pueri blijft de -e- in alle vormen (stam puer-). Bij ager, agri valt de -e- weg (stam agr-). De genitivus toont de ware stam.",
            "source": "manual",
        },
        {
            "id": "ITEM-LAT-G-MORF-DECL2-ER-002",
            "node_ids": ["LAT-G-MORF-DECL2-ER"],
            "type": "production",
            "direction": "productive",
            "difficulty_initial": 0.8,
            "discrimination_initial": 1.2,
            "expected_time_sec": 25,
            "stimulus": "Geef de genitivus meervoud van 'ager'.",
            "answer": "agrorum",
            "feedback": "De stam van ager is agr- (genitivus agri). Gen. pl.: agr- + -ōrum = agrōrum.",
            "source": "manual",
        },
        {
            "id": "ITEM-LAT-G-MORF-DECL2-ER-003",
            "node_ids": ["LAT-G-MORF-DECL2-ER"],
            "type": "production",
            "direction": "productive",
            "difficulty_initial": 0.6,
            "discrimination_initial": 1.0,
            "expected_time_sec": 25,
            "stimulus": "Geef de accusativus enkelvoud van 'puer'.",
            "answer": "puerum",
            "feedback": "De stam van puer is puer- (genitivus pueri). Acc. sg.: puer- + -um = puerum.",
            "source": "manual",
        },
        {
            "id": "ITEM-LAT-G-MORF-DECL2-ER-004",
            "node_ids": ["LAT-G-MORF-DECL2-ER"],
            "type": "production",
            "direction": "productive",
            "difficulty_initial": 0.9,
            "discrimination_initial": 1.2,
            "expected_time_sec": 25,
            "stimulus": "Geef de ablativus enkelvoud van 'ager'.",
            "answer": "agro",
            "feedback": "Stam agr- + uitgang -ō = agrō. Let op: niet 'agero' — de -e- uit de nominativus valt weg.",
            "source": "manual",
        },
    ]

    # ── DECL2-NEUT (leerjaar1.json) ──────────────────────────────────

    items["LAT-G-MORF-DECL2-NEUT"] = [
        {
            "id": "ITEM-LAT-G-MORF-DECL2-NEUT-001",
            "node_ids": ["LAT-G-MORF-DECL2-NEUT"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": -0.1,
            "discrimination_initial": 1.0,
            "expected_time_sec": 12,
            "stimulus": "Wat is de neutrumregel?",
            "answer": "bij neutra zijn nominativus en accusativus altijd gelijk; in het meervoud eindigen ze op -a",
            "feedback": "De neutrumregel: nom. = acc. in alle numeri. In het meervoud eindigen nom. en acc. altijd op -a.",
            "source": "manual",
        },
        {
            "id": "ITEM-LAT-G-MORF-DECL2-NEUT-002",
            "node_ids": ["LAT-G-MORF-DECL2-NEUT"],
            "type": "production",
            "direction": "productive",
            "difficulty_initial": 0.6,
            "discrimination_initial": 1.0,
            "expected_time_sec": 20,
            "stimulus": "Geef de accusativus meervoud van 'bellum'.",
            "answer": "bella",
            "feedback": "Neutrumregel: acc. pl. = nom. pl. Bij neutra van de 2e declinatie is dat -a: bellum → bella.",
            "source": "manual",
        },
        {
            "id": "ITEM-LAT-G-MORF-DECL2-NEUT-003",
            "node_ids": ["LAT-G-MORF-DECL2-NEUT"],
            "type": "production",
            "direction": "productive",
            "difficulty_initial": 0.7,
            "discrimination_initial": 1.0,
            "expected_time_sec": 20,
            "stimulus": "Geef de nominativus meervoud van 'templum'.",
            "answer": "templa",
            "feedback": "Neutrumregel: nom. pl. van neutra eindigt op -a: templum → templa. Niet verwarren met 1e declinatie femininum -a (sg.).",
            "source": "manual",
        },
    ]

    # ── DECL2-PARAD (leerjaar1.json, 5 items incl. analyse) ─────────

    items["LAT-G-MORF-DECL2-PARAD"] = [
        {
            "id": "ITEM-LAT-G-MORF-DECL2-PARAD-001",
            "node_ids": ["LAT-G-MORF-DECL2-PARAD"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": 0.0,
            "discrimination_initial": 1.0,
            "expected_time_sec": 12,
            "stimulus": "Welke twee naamvallen van de 2e declinatie enkelvoud hebben dezelfde uitgang -o?",
            "answer": "dativus singularis en ablativus singularis",
            "feedback": "De dativus en ablativus singularis van de 2e declinatie eindigen beiden op -ō. Context bepaalt de functie.",
            "source": "manual",
        },
        {
            "id": "ITEM-LAT-G-MORF-DECL2-PARAD-002",
            "node_ids": ["LAT-G-MORF-DECL2-PARAD"],
            "type": "analysis",
            "direction": "receptive",
            "difficulty_initial": 1.0,
            "discrimination_initial": 1.2,
            "expected_time_sec": 30,
            "stimulus": "Ontleed 'dominorum' volledig.",
            "answer": "genitivus pluralis, 2e declinatie",
            "feedback": "Domin-ōrum: stam domin- + uitgang -ōrum = genitivus pluralis van de 2e declinatie.",
            "source": "manual",
        },
        {
            "id": "ITEM-LAT-G-MORF-DECL2-PARAD-003",
            "node_ids": ["LAT-G-MORF-DECL2-PARAD"],
            "type": "analysis",
            "direction": "receptive",
            "difficulty_initial": 1.3,
            "discrimination_initial": 1.2,
            "expected_time_sec": 35,
            "stimulus": "Ontleed 'agris' volledig.",
            "answer": ["dativus pluralis of ablativus pluralis, 2e declinatie"],
            "feedback": "Agr-īs: stam agr- (van ager, agri) + uitgang -īs = dativus of ablativus pluralis van de 2e declinatie.",
            "source": "manual",
        },
        {
            "id": "ITEM-LAT-G-MORF-DECL2-PARAD-004",
            "node_ids": ["LAT-G-MORF-DECL2-PARAD"],
            "type": "production",
            "direction": "productive",
            "difficulty_initial": 0.8,
            "discrimination_initial": 1.0,
            "expected_time_sec": 25,
            "stimulus": "Verbuig 'bellum' in de genitivus singularis en meervoud.",
            "answer": "belli, bellorum",
            "feedback": "Gen. sg. bell-i, gen. pl. bell-ōrum. Bij neutra volgt de genitivus hetzelfde patroon als bij masculina.",
            "source": "manual",
        },
        {
            "id": "ITEM-LAT-G-MORF-DECL2-PARAD-005",
            "node_ids": ["LAT-G-MORF-DECL2-PARAD"],
            "type": "analysis",
            "direction": "receptive",
            "difficulty_initial": 1.5,
            "discrimination_initial": 1.2,
            "expected_time_sec": 35,
            "stimulus": "Ontleed 'bella' volledig. Geef alle mogelijke analyses.",
            "answer": [
                "nominativus pluralis neutrum of accusativus pluralis neutrum, 2e declinatie"
            ],
            "feedback": "'Bella' kan nom. pl. of acc. pl. zijn (neutrumregel). Niet verwarren met 1e-declinatie nom. sg. fem. — 'bella' als neutrum pl. van 'bellum'.",
            "source": "manual",
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
    """Load JSON, add items to matching nodes, write back. Returns count added."""
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
    """Print summary statistics."""
    total = sum(len(v) for v in items_by_node.values())
    type_counter: Counter[str] = Counter()
    richting_counter: Counter[str] = Counter()
    for item_list in items_by_node.values():
        for item in item_list:
            type_counter[item["type"]] += 1
            richting_counter[item["direction"]] += 1

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
