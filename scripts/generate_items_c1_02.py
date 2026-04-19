#!/usr/bin/env python3
"""Generate exercise items for C1-02: 1e declinatie (A1-02 knopen).

Targets:
  - data/graph/lat_grammatica_poc.json  (DECL1-INTRO, NOM-D1..ABL-D1)
  - data/graph/lat_grammatica_leerjaar1.json (VOC-D1, DECL1-STAM, DECL1-MASC, DECL1-PARAD)
~30 items total.
"""

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from gymnasium_classica.models.graph import Item

# ── Which knopen live in which file ──────────────────────────────────
POC_KNOOP_IDS = {
    "LAT-G-MORF-DECL1-INTRO",
    "LAT-G-MORF-NOM-D1",
    "LAT-G-MORF-GEN-D1",
    "LAT-G-MORF-DAT-D1",
    "LAT-G-MORF-ACC-D1",
    "LAT-G-MORF-ABL-D1",
}
LJ1_KNOOP_IDS = {
    "LAT-G-MORF-VOC-D1",
    "LAT-G-MORF-DECL1-STAM",
    "LAT-G-MORF-DECL1-MASC",
    "LAT-G-MORF-DECL1-PARAD",
}


def define_items() -> dict[str, list[dict]]:
    """Return knoop_id -> list of item dicts."""
    items: dict[str, list[dict]] = {}

    # ── DECL1-INTRO (kennis, 2 herkenning) ───────────────────────────

    items["LAT-G-MORF-DECL1-INTRO"] = [
        {
            "id": "ITEM-LAT-G-MORF-DECL1-INTRO-001",
            "knoop_ids": ["LAT-G-MORF-DECL1-INTRO"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.6,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 12,
            "stimulus": "Op welke letter eindigen de meeste woorden van de 1e declinatie in de nominativus singularis?",
            "antwoord": "-a",
            "feedback": "Woorden van de 1e declinatie (a-stammen) eindigen in de nominativus singularis op -a. Bijv. puella, terra, aqua.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-LAT-G-MORF-DECL1-INTRO-002",
            "knoop_ids": ["LAT-G-MORF-DECL1-INTRO"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.3,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 12,
            "stimulus": "Welk woordgeslacht hebben de meeste woorden van de 1e declinatie?",
            "antwoord": "femininum (vrouwelijk)",
            "feedback": "De 1e declinatie bevat voornamelijk feminina. Uitzonderingen zijn beroepsnamen als nauta (zeeman) en poeta (dichter), die masculinum zijn.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-LAT-G-MORF-DECL1-INTRO-003",
            "knoop_ids": ["LAT-G-MORF-DECL1-INTRO"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.4,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 12,
            "stimulus": "Hoe herken je in het woordenboek dat een woord bij de 1e declinatie hoort?",
            "antwoord": "de genitivus singularis eindigt op -ae",
            "feedback": "Een woord hoort bij de 1e declinatie als de genitivus singularis op -ae eindigt. Bijv. puella, -ae.",
            "bron": "handmatig",
        },
    ]

    # ── NOM-D1 (toepassing, herkenning + productie) ──────────────────

    items["LAT-G-MORF-NOM-D1"] = [
        {
            "id": "ITEM-LAT-G-MORF-NOM-D1-001",
            "knoop_ids": ["LAT-G-MORF-NOM-D1"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.3,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 10,
            "stimulus": "Welke naamval is 'puella'?",
            "antwoord": ["nominativus singularis", "ablativus singularis"],
            "feedback": "'Puella' kan nominativus sg. of ablativus sg. zijn (de uitgang -a is gelijk). Context bepaalt de functie.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-LAT-G-MORF-NOM-D1-002",
            "knoop_ids": ["LAT-G-MORF-NOM-D1"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.5,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 20,
            "stimulus": "Geef de nominativus meervoud van 'puella'.",
            "antwoord": "puellae",
            "feedback": "De nominativus meervoud van de 1e declinatie eindigt op -ae: puella → puellae.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-LAT-G-MORF-NOM-D1-003",
            "knoop_ids": ["LAT-G-MORF-NOM-D1"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.1,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 12,
            "stimulus": "Wat is de nominativus-uitgang van de 1e declinatie in het enkelvoud?",
            "antwoord": "-a",
            "feedback": "De nominativus singularis van de 1e declinatie eindigt op -a. Let op: dit is gelijk aan de ablativus sg.",
            "bron": "handmatig",
        },
    ]

    # ── GEN-D1 ────────────────────────────────────────────────────────

    items["LAT-G-MORF-GEN-D1"] = [
        {
            "id": "ITEM-LAT-G-MORF-GEN-D1-001",
            "knoop_ids": ["LAT-G-MORF-GEN-D1"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.2,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 12,
            "stimulus": "Welke naamval(len) kan 'puellae' zijn?",
            "antwoord": ["genitivus singularis, dativus singularis, of nominativus pluralis"],
            "feedback": "'Puellae' kan genitivus sg., dativus sg. of nominativus pl. zijn. De uitgang -ae komt in drie naamvallen voor.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-LAT-G-MORF-GEN-D1-002",
            "knoop_ids": ["LAT-G-MORF-GEN-D1"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.5,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 20,
            "stimulus": "Geef de genitivus meervoud van 'terra'.",
            "antwoord": "terrarum",
            "feedback": "De genitivus meervoud van de 1e declinatie eindigt op -ārum: terra → terrārum.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-LAT-G-MORF-GEN-D1-003",
            "knoop_ids": ["LAT-G-MORF-GEN-D1"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.6,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 20,
            "stimulus": "Geef de genitivus enkelvoud van 'aqua'.",
            "antwoord": "aquae",
            "feedback": "De genitivus singularis van de 1e declinatie eindigt op -ae: aqua → aquae.",
            "bron": "handmatig",
        },
    ]

    # ── DAT-D1 ────────────────────────────────────────────────────────

    items["LAT-G-MORF-DAT-D1"] = [
        {
            "id": "ITEM-LAT-G-MORF-DAT-D1-001",
            "knoop_ids": ["LAT-G-MORF-DAT-D1"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.1,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 12,
            "stimulus": "Wat is de dativus-uitgang van de 1e declinatie in het enkelvoud?",
            "antwoord": "-ae",
            "feedback": "De dativus singularis van de 1e declinatie eindigt op -ae. Let op: dit is gelijk aan de genitivus sg. en nominativus pl.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-LAT-G-MORF-DAT-D1-002",
            "knoop_ids": ["LAT-G-MORF-DAT-D1"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.6,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 20,
            "stimulus": "Geef de dativus meervoud van 'puella'.",
            "antwoord": "puellis",
            "feedback": "De dativus meervoud van de 1e declinatie eindigt op -īs: puella → puellīs. Let op: dit is gelijk aan de ablativus pl.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-LAT-G-MORF-DAT-D1-003",
            "knoop_ids": ["LAT-G-MORF-DAT-D1"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.5,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 20,
            "stimulus": "Geef de dativus enkelvoud van 'terra'.",
            "antwoord": "terrae",
            "feedback": "De dativus singularis van de 1e declinatie eindigt op -ae: terra → terrae.",
            "bron": "handmatig",
        },
    ]

    # ── ACC-D1 ────────────────────────────────────────────────────────

    items["LAT-G-MORF-ACC-D1"] = [
        {
            "id": "ITEM-LAT-G-MORF-ACC-D1-001",
            "knoop_ids": ["LAT-G-MORF-ACC-D1"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.2,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 10,
            "stimulus": "Welke naamval is 'puellam'?",
            "antwoord": "accusativus singularis",
            "feedback": "De uitgang -am is uniek voor de accusativus singularis van de 1e declinatie.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-LAT-G-MORF-ACC-D1-002",
            "knoop_ids": ["LAT-G-MORF-ACC-D1"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.5,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 20,
            "stimulus": "Geef de accusativus meervoud van 'puella'.",
            "antwoord": "puellas",
            "feedback": "De accusativus meervoud van de 1e declinatie eindigt op -ās: puella → puellās.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-LAT-G-MORF-ACC-D1-003",
            "knoop_ids": ["LAT-G-MORF-ACC-D1"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.6,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 20,
            "stimulus": "Geef de accusativus enkelvoud van 'aqua'.",
            "antwoord": "aquam",
            "feedback": "De accusativus singularis van de 1e declinatie eindigt op -am: aqua → aquam.",
            "bron": "handmatig",
        },
    ]

    # ── ABL-D1 ────────────────────────────────────────────────────────

    items["LAT-G-MORF-ABL-D1"] = [
        {
            "id": "ITEM-LAT-G-MORF-ABL-D1-001",
            "knoop_ids": ["LAT-G-MORF-ABL-D1"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.1,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 12,
            "stimulus": "Wat is de ablativus-uitgang van de 1e declinatie in het enkelvoud?",
            "antwoord": "-ā (lang a)",
            "feedback": "De ablativus singularis van de 1e declinatie eindigt op -ā (lange a). Geschreven zonder macron lijkt het op de nominativus sg. -a.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-LAT-G-MORF-ABL-D1-002",
            "knoop_ids": ["LAT-G-MORF-ABL-D1"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.5,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 20,
            "stimulus": "Geef de ablativus meervoud van 'terra'.",
            "antwoord": "terris",
            "feedback": "De ablativus meervoud van de 1e declinatie eindigt op -īs: terra → terrīs. Dit is gelijk aan de dativus pl.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-LAT-G-MORF-ABL-D1-003",
            "knoop_ids": ["LAT-G-MORF-ABL-D1"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.6,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 20,
            "stimulus": "Geef de ablativus enkelvoud van 'puella'.",
            "antwoord": ["puellā", "puella"],
            "feedback": "De ablativus singularis van de 1e declinatie eindigt op -ā: puella → puellā. Zonder macron geschreven als 'puella'.",
            "bron": "handmatig",
        },
    ]

    # ── VOC-D1 (leerjaar1.json) ──────────────────────────────────────

    items["LAT-G-MORF-VOC-D1"] = [
        {
            "id": "ITEM-LAT-G-MORF-VOC-D1-001",
            "knoop_ids": ["LAT-G-MORF-VOC-D1"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.4,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 12,
            "stimulus": "Is de vocativus van de 1e declinatie gelijk aan een andere naamval?",
            "antwoord": "ja, de vocativus is gelijk aan de nominativus",
            "feedback": "Bij de 1e declinatie is de vocativus altijd gelijk aan de nominativus: puella! (sg.), puellae! (pl.).",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-LAT-G-MORF-VOC-D1-002",
            "knoop_ids": ["LAT-G-MORF-VOC-D1"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.3,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 15,
            "stimulus": "Hoe spreek je een meisje (puella) direct aan in het Latijn?",
            "antwoord": "puella!",
            "feedback": "De vocativus van 'puella' is 'puella!' — gelijk aan de nominativus bij de 1e declinatie.",
            "bron": "handmatig",
        },
    ]

    # ── DECL1-STAM (leerjaar1.json) ──────────────────────────────────

    items["LAT-G-MORF-DECL1-STAM"] = [
        {
            "id": "ITEM-LAT-G-MORF-DECL1-STAM-001",
            "knoop_ids": ["LAT-G-MORF-DECL1-STAM"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.2,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 12,
            "stimulus": "Hoe bepaal je de stam van een 1e-declinatiewoord?",
            "antwoord": "haal -ae van de genitivus singularis af",
            "feedback": "De stam vind je door -ae van de genitivus singularis af te halen. Bijv. puell-ae → stam puell-.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-LAT-G-MORF-DECL1-STAM-002",
            "knoop_ids": ["LAT-G-MORF-DECL1-STAM"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.5,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 20,
            "stimulus": "Wat is de stam van 'agricola, agricolae'?",
            "antwoord": "agricol-",
            "feedback": "Genitivus agricol-ae → stam agricol-. Aan deze stam plak je de naamvalsuitgangen.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-LAT-G-MORF-DECL1-STAM-003",
            "knoop_ids": ["LAT-G-MORF-DECL1-STAM"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.4,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 20,
            "stimulus": "Wat is de stam van 'terra, terrae'?",
            "antwoord": "terr-",
            "feedback": "Genitivus terr-ae → stam terr-. Aan deze stam plak je de naamvalsuitgangen.",
            "bron": "handmatig",
        },
    ]

    # ── DECL1-MASC (leerjaar1.json) ──────────────────────────────────

    items["LAT-G-MORF-DECL1-MASC"] = [
        {
            "id": "ITEM-LAT-G-MORF-DECL1-MASC-001",
            "knoop_ids": ["LAT-G-MORF-DECL1-MASC"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.0,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 12,
            "stimulus": "Noem twee mannelijke woorden die toch bij de 1e declinatie horen.",
            "antwoord": ["nauta en poeta", "nauta, poeta, pirata, agricola"],
            "feedback": "Nauta (zeeman), poeta (dichter), pirata (piraat) en agricola (boer) zijn masculinum maar volgen de 1e declinatie.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-LAT-G-MORF-DECL1-MASC-002",
            "knoop_ids": ["LAT-G-MORF-DECL1-MASC"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.2,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 15,
            "stimulus": "Verbuigen mannelijke woorden van de 1e declinatie anders dan vrouwelijke?",
            "antwoord": "nee, de uitgangen zijn identiek",
            "feedback": "Masculina van de 1e declinatie verbuigen identiek aan feminina. Alleen het genus verschilt (m. in plaats van f.).",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-LAT-G-MORF-DECL1-MASC-003",
            "knoop_ids": ["LAT-G-MORF-DECL1-MASC"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.7,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 20,
            "stimulus": "Geef de genitivus meervoud van 'nauta'.",
            "antwoord": "nautarum",
            "feedback": "Nauta verbuigt als een gewoon 1e-declinatiewoord: nauta, nautae → gen. pl. nautārum.",
            "bron": "handmatig",
        },
    ]

    # ── DECL1-PARAD (leerjaar1.json, 4 items incl. analyse) ─────────

    items["LAT-G-MORF-DECL1-PARAD"] = [
        {
            "id": "ITEM-LAT-G-MORF-DECL1-PARAD-001",
            "knoop_ids": ["LAT-G-MORF-DECL1-PARAD"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.1,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 12,
            "stimulus": "Welke twee naamvallen van de 1e declinatie meervoud hebben dezelfde uitgang -is?",
            "antwoord": "dativus pluralis en ablativus pluralis",
            "feedback": "De dativus en ablativus pluralis eindigen beiden op -īs. Context bepaalt de functie.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-LAT-G-MORF-DECL1-PARAD-002",
            "knoop_ids": ["LAT-G-MORF-DECL1-PARAD"],
            "type": "analyse",
            "richting": "receptief",
            "moeilijkheid_initieel": 1.0,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 30,
            "stimulus": "Ontleed 'puellarum' volledig.",
            "antwoord": "genitivus pluralis, 1e declinatie",
            "feedback": "Puell-ārum: stam puell- + uitgang -ārum = genitivus pluralis van de 1e declinatie.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-LAT-G-MORF-DECL1-PARAD-003",
            "knoop_ids": ["LAT-G-MORF-DECL1-PARAD"],
            "type": "analyse",
            "richting": "receptief",
            "moeilijkheid_initieel": 1.2,
            "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": 35,
            "stimulus": "Ontleed 'terris' volledig.",
            "antwoord": ["dativus pluralis of ablativus pluralis, 1e declinatie"],
            "feedback": "Terr-īs: stam terr- + uitgang -īs = dativus of ablativus pluralis van de 1e declinatie. De context bepaalt welke.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-LAT-G-MORF-DECL1-PARAD-004",
            "knoop_ids": ["LAT-G-MORF-DECL1-PARAD"],
            "type": "productie",
            "richting": "productief",
            "moeilijkheid_initieel": 0.8,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 25,
            "stimulus": "Verbuig 'puella' in de genitivus singularis en meervoud.",
            "antwoord": "puellae, puellarum",
            "feedback": "Gen. sg. puell-ae, gen. pl. puell-ārum. Let op: gen. sg. -ae is gelijk aan dat. sg. en nom. pl.",
            "bron": "handmatig",
        },
    ]

    return items


def validate_items(items_by_knoop: dict[str, list[dict]]) -> None:
    """Validate all items via Pydantic model."""
    for knoop_id, item_list in items_by_knoop.items():
        for item_dict in item_list:
            Item(**item_dict)
    print("All items validated successfully.")


def add_items_to_json(json_path: Path, items_by_knoop: dict[str, list[dict]]) -> int:
    """Load JSON, add items to matching knopen, write back. Returns count added."""
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
    """Print summary statistics."""
    total = sum(len(v) for v in items_by_knoop.values())
    type_counter: Counter[str] = Counter()
    richting_counter: Counter[str] = Counter()
    for item_list in items_by_knoop.values():
        for item in item_list:
            type_counter[item["type"]] += 1
            richting_counter[item["richting"]] += 1

    print("\n=== C1-02 Summary ===")
    print(f"Knopen: {len(items_by_knoop)}")
    print(f"Total items: {total}")
    print("\nItems per knoop:")
    for kid, item_list in sorted(items_by_knoop.items()):
        print(f"  {kid}: {len(item_list)}")
    print("\nOefentype-verdeling:")
    for t, c in type_counter.most_common():
        print(f"  {t}: {c}")
    print("\nRichting-verdeling:")
    for r, c in richting_counter.most_common():
        print(f"  {r}: {c}")


def main() -> None:
    items_by_knoop = define_items()
    validate_items(items_by_knoop)

    base = Path(__file__).parent.parent / "data" / "graph"
    poc_path = base / "lat_grammatica_poc.json"
    lj1_path = base / "lat_grammatica_leerjaar1.json"

    poc_items = {k: v for k, v in items_by_knoop.items() if k in POC_KNOOP_IDS}
    lj1_items = {k: v for k, v in items_by_knoop.items() if k in LJ1_KNOOP_IDS}

    added_poc = add_items_to_json(poc_path, poc_items)
    added_lj1 = add_items_to_json(lj1_path, lj1_items)

    print(f"Added {added_poc} items to {poc_path.name}")
    print(f"Added {added_lj1} items to {lj1_path.name}")

    print_summary(items_by_knoop)


if __name__ == "__main__":
    main()
