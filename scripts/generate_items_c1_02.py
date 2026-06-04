#!/usr/bin/env python3
"""Generate exercise items for C1-02: 1e declinatie (A1-02 nodes).

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

# ── Which nodes live in which file ──────────────────────────────────
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
    """Return node_id -> list of item dicts."""
    items: dict[str, list[dict]] = {}

    # ── DECL1-INTRO (kennis, 2 herkenning) ───────────────────────────

    items["LAT-G-MORF-DECL1-INTRO"] = [
        {
            "id": "ITEM-LAT-G-MORF-DECL1-INTRO-001",
            "node_ids": ["LAT-G-MORF-DECL1-INTRO"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": -0.6,
            "discrimination_initial": 1.0,
            "expected_time_sec": 12,
            "stimulus": "Op welke letter eindigen de meeste woorden van de 1e declinatie in de nominativus singularis?",
            "answer": "-a",
            "feedback": "Woorden van de 1e declinatie (a-stammen) eindigen in de nominativus singularis op -a. Bijv. puella, terra, aqua.",
            "source": "manual",
        },
        {
            "id": "ITEM-LAT-G-MORF-DECL1-INTRO-002",
            "node_ids": ["LAT-G-MORF-DECL1-INTRO"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": -0.3,
            "discrimination_initial": 1.0,
            "expected_time_sec": 12,
            "stimulus": "Welk woordgeslacht hebben de meeste woorden van de 1e declinatie?",
            "answer": "femininum (vrouwelijk)",
            "feedback": "De 1e declinatie bevat voornamelijk feminina. Uitzonderingen zijn beroepsnamen als nauta (zeeman) en poeta (dichter), die masculinum zijn.",
            "source": "manual",
        },
        {
            "id": "ITEM-LAT-G-MORF-DECL1-INTRO-003",
            "node_ids": ["LAT-G-MORF-DECL1-INTRO"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": -0.4,
            "discrimination_initial": 1.0,
            "expected_time_sec": 12,
            "stimulus": "Hoe herken je in het woordenboek dat een woord bij de 1e declinatie hoort?",
            "answer": "de genitivus singularis eindigt op -ae",
            "feedback": "Een woord hoort bij de 1e declinatie als de genitivus singularis op -ae eindigt. Bijv. puella, -ae.",
            "source": "manual",
        },
    ]

    # ── NOM-D1 (toepassing, herkenning + productie) ──────────────────

    items["LAT-G-MORF-NOM-D1"] = [
        {
            "id": "ITEM-LAT-G-MORF-NOM-D1-001",
            "node_ids": ["LAT-G-MORF-NOM-D1"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": -0.3,
            "discrimination_initial": 1.0,
            "expected_time_sec": 10,
            "stimulus": "Welke naamval is 'puella'?",
            "answer": ["nominativus singularis", "ablativus singularis"],
            "feedback": "'Puella' kan nominativus sg. of ablativus sg. zijn (de uitgang -a is gelijk). Context bepaalt de functie.",
            "source": "manual",
        },
        {
            "id": "ITEM-LAT-G-MORF-NOM-D1-002",
            "node_ids": ["LAT-G-MORF-NOM-D1"],
            "type": "production",
            "direction": "productive",
            "difficulty_initial": 0.5,
            "discrimination_initial": 1.0,
            "expected_time_sec": 20,
            "stimulus": "Geef de nominativus meervoud van 'puella'.",
            "answer": "puellae",
            "feedback": "De nominativus meervoud van de 1e declinatie eindigt op -ae: puella → puellae.",
            "source": "manual",
        },
        {
            "id": "ITEM-LAT-G-MORF-NOM-D1-003",
            "node_ids": ["LAT-G-MORF-NOM-D1"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": -0.1,
            "discrimination_initial": 1.0,
            "expected_time_sec": 12,
            "stimulus": "Wat is de nominativus-uitgang van de 1e declinatie in het enkelvoud?",
            "answer": "-a",
            "feedback": "De nominativus singularis van de 1e declinatie eindigt op -a. Let op: dit is gelijk aan de ablativus sg.",
            "source": "manual",
        },
    ]

    # ── GEN-D1 ────────────────────────────────────────────────────────

    items["LAT-G-MORF-GEN-D1"] = [
        {
            "id": "ITEM-LAT-G-MORF-GEN-D1-001",
            "node_ids": ["LAT-G-MORF-GEN-D1"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": -0.2,
            "discrimination_initial": 1.0,
            "expected_time_sec": 12,
            "stimulus": "Welke naamval(len) kan 'puellae' zijn?",
            "answer": ["genitivus singularis, dativus singularis, of nominativus pluralis"],
            "feedback": "'Puellae' kan genitivus sg., dativus sg. of nominativus pl. zijn. De uitgang -ae komt in drie naamvallen voor.",
            "source": "manual",
        },
        {
            "id": "ITEM-LAT-G-MORF-GEN-D1-002",
            "node_ids": ["LAT-G-MORF-GEN-D1"],
            "type": "production",
            "direction": "productive",
            "difficulty_initial": 0.5,
            "discrimination_initial": 1.0,
            "expected_time_sec": 20,
            "stimulus": "Geef de genitivus meervoud van 'terra'.",
            "answer": "terrarum",
            "feedback": "De genitivus meervoud van de 1e declinatie eindigt op -ārum: terra → terrārum.",
            "source": "manual",
        },
        {
            "id": "ITEM-LAT-G-MORF-GEN-D1-003",
            "node_ids": ["LAT-G-MORF-GEN-D1"],
            "type": "production",
            "direction": "productive",
            "difficulty_initial": 0.6,
            "discrimination_initial": 1.0,
            "expected_time_sec": 20,
            "stimulus": "Geef de genitivus enkelvoud van 'aqua'.",
            "answer": "aquae",
            "feedback": "De genitivus singularis van de 1e declinatie eindigt op -ae: aqua → aquae.",
            "source": "manual",
        },
    ]

    # ── DAT-D1 ────────────────────────────────────────────────────────

    items["LAT-G-MORF-DAT-D1"] = [
        {
            "id": "ITEM-LAT-G-MORF-DAT-D1-001",
            "node_ids": ["LAT-G-MORF-DAT-D1"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": -0.1,
            "discrimination_initial": 1.0,
            "expected_time_sec": 12,
            "stimulus": "Wat is de dativus-uitgang van de 1e declinatie in het enkelvoud?",
            "answer": "-ae",
            "feedback": "De dativus singularis van de 1e declinatie eindigt op -ae. Let op: dit is gelijk aan de genitivus sg. en nominativus pl.",
            "source": "manual",
        },
        {
            "id": "ITEM-LAT-G-MORF-DAT-D1-002",
            "node_ids": ["LAT-G-MORF-DAT-D1"],
            "type": "production",
            "direction": "productive",
            "difficulty_initial": 0.6,
            "discrimination_initial": 1.0,
            "expected_time_sec": 20,
            "stimulus": "Geef de dativus meervoud van 'puella'.",
            "answer": "puellis",
            "feedback": "De dativus meervoud van de 1e declinatie eindigt op -īs: puella → puellīs. Let op: dit is gelijk aan de ablativus pl.",
            "source": "manual",
        },
        {
            "id": "ITEM-LAT-G-MORF-DAT-D1-003",
            "node_ids": ["LAT-G-MORF-DAT-D1"],
            "type": "production",
            "direction": "productive",
            "difficulty_initial": 0.5,
            "discrimination_initial": 1.0,
            "expected_time_sec": 20,
            "stimulus": "Geef de dativus enkelvoud van 'terra'.",
            "answer": "terrae",
            "feedback": "De dativus singularis van de 1e declinatie eindigt op -ae: terra → terrae.",
            "source": "manual",
        },
    ]

    # ── ACC-D1 ────────────────────────────────────────────────────────

    items["LAT-G-MORF-ACC-D1"] = [
        {
            "id": "ITEM-LAT-G-MORF-ACC-D1-001",
            "node_ids": ["LAT-G-MORF-ACC-D1"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": -0.2,
            "discrimination_initial": 1.0,
            "expected_time_sec": 10,
            "stimulus": "Welke naamval is 'puellam'?",
            "answer": "accusativus singularis",
            "feedback": "De uitgang -am is uniek voor de accusativus singularis van de 1e declinatie.",
            "source": "manual",
        },
        {
            "id": "ITEM-LAT-G-MORF-ACC-D1-002",
            "node_ids": ["LAT-G-MORF-ACC-D1"],
            "type": "production",
            "direction": "productive",
            "difficulty_initial": 0.5,
            "discrimination_initial": 1.0,
            "expected_time_sec": 20,
            "stimulus": "Geef de accusativus meervoud van 'puella'.",
            "answer": "puellas",
            "feedback": "De accusativus meervoud van de 1e declinatie eindigt op -ās: puella → puellās.",
            "source": "manual",
        },
        {
            "id": "ITEM-LAT-G-MORF-ACC-D1-003",
            "node_ids": ["LAT-G-MORF-ACC-D1"],
            "type": "production",
            "direction": "productive",
            "difficulty_initial": 0.6,
            "discrimination_initial": 1.0,
            "expected_time_sec": 20,
            "stimulus": "Geef de accusativus enkelvoud van 'aqua'.",
            "answer": "aquam",
            "feedback": "De accusativus singularis van de 1e declinatie eindigt op -am: aqua → aquam.",
            "source": "manual",
        },
    ]

    # ── ABL-D1 ────────────────────────────────────────────────────────

    items["LAT-G-MORF-ABL-D1"] = [
        {
            "id": "ITEM-LAT-G-MORF-ABL-D1-001",
            "node_ids": ["LAT-G-MORF-ABL-D1"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": -0.1,
            "discrimination_initial": 1.0,
            "expected_time_sec": 12,
            "stimulus": "Wat is de ablativus-uitgang van de 1e declinatie in het enkelvoud?",
            "answer": "-ā (lang a)",
            "feedback": "De ablativus singularis van de 1e declinatie eindigt op -ā (lange a). Geschreven zonder macron lijkt het op de nominativus sg. -a.",
            "source": "manual",
        },
        {
            "id": "ITEM-LAT-G-MORF-ABL-D1-002",
            "node_ids": ["LAT-G-MORF-ABL-D1"],
            "type": "production",
            "direction": "productive",
            "difficulty_initial": 0.5,
            "discrimination_initial": 1.0,
            "expected_time_sec": 20,
            "stimulus": "Geef de ablativus meervoud van 'terra'.",
            "answer": "terris",
            "feedback": "De ablativus meervoud van de 1e declinatie eindigt op -īs: terra → terrīs. Dit is gelijk aan de dativus pl.",
            "source": "manual",
        },
        {
            "id": "ITEM-LAT-G-MORF-ABL-D1-003",
            "node_ids": ["LAT-G-MORF-ABL-D1"],
            "type": "production",
            "direction": "productive",
            "difficulty_initial": 0.6,
            "discrimination_initial": 1.0,
            "expected_time_sec": 20,
            "stimulus": "Geef de ablativus enkelvoud van 'puella'.",
            "answer": ["puellā", "puella"],
            "feedback": "De ablativus singularis van de 1e declinatie eindigt op -ā: puella → puellā. Zonder macron geschreven als 'puella'.",
            "source": "manual",
        },
    ]

    # ── VOC-D1 (leerjaar1.json) ──────────────────────────────────────

    items["LAT-G-MORF-VOC-D1"] = [
        {
            "id": "ITEM-LAT-G-MORF-VOC-D1-001",
            "node_ids": ["LAT-G-MORF-VOC-D1"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": -0.4,
            "discrimination_initial": 1.0,
            "expected_time_sec": 12,
            "stimulus": "Is de vocativus van de 1e declinatie gelijk aan een andere naamval?",
            "answer": "ja, de vocativus is gelijk aan de nominativus",
            "feedback": "Bij de 1e declinatie is de vocativus altijd gelijk aan de nominativus: puella! (sg.), puellae! (pl.).",
            "source": "manual",
        },
        {
            "id": "ITEM-LAT-G-MORF-VOC-D1-002",
            "node_ids": ["LAT-G-MORF-VOC-D1"],
            "type": "production",
            "direction": "productive",
            "difficulty_initial": 0.3,
            "discrimination_initial": 1.0,
            "expected_time_sec": 15,
            "stimulus": "Hoe spreek je een meisje (puella) direct aan in het Latijn?",
            "answer": "puella!",
            "feedback": "De vocativus van 'puella' is 'puella!' — gelijk aan de nominativus bij de 1e declinatie.",
            "source": "manual",
        },
    ]

    # ── DECL1-STAM (leerjaar1.json) ──────────────────────────────────

    items["LAT-G-MORF-DECL1-STAM"] = [
        {
            "id": "ITEM-LAT-G-MORF-DECL1-STAM-001",
            "node_ids": ["LAT-G-MORF-DECL1-STAM"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": -0.2,
            "discrimination_initial": 1.0,
            "expected_time_sec": 12,
            "stimulus": "Hoe bepaal je de stam van een 1e-declinatiewoord?",
            "answer": "haal -ae van de genitivus singularis af",
            "feedback": "De stam vind je door -ae van de genitivus singularis af te halen. Bijv. puell-ae → stam puell-.",
            "source": "manual",
        },
        {
            "id": "ITEM-LAT-G-MORF-DECL1-STAM-002",
            "node_ids": ["LAT-G-MORF-DECL1-STAM"],
            "type": "production",
            "direction": "productive",
            "difficulty_initial": 0.5,
            "discrimination_initial": 1.0,
            "expected_time_sec": 20,
            "stimulus": "Wat is de stam van 'agricola, agricolae'?",
            "answer": "agricol-",
            "feedback": "Genitivus agricol-ae → stam agricol-. Aan deze stam plak je de naamvalsuitgangen.",
            "source": "manual",
        },
        {
            "id": "ITEM-LAT-G-MORF-DECL1-STAM-003",
            "node_ids": ["LAT-G-MORF-DECL1-STAM"],
            "type": "production",
            "direction": "productive",
            "difficulty_initial": 0.4,
            "discrimination_initial": 1.0,
            "expected_time_sec": 20,
            "stimulus": "Wat is de stam van 'terra, terrae'?",
            "answer": "terr-",
            "feedback": "Genitivus terr-ae → stam terr-. Aan deze stam plak je de naamvalsuitgangen.",
            "source": "manual",
        },
    ]

    # ── DECL1-MASC (leerjaar1.json) ──────────────────────────────────

    items["LAT-G-MORF-DECL1-MASC"] = [
        {
            "id": "ITEM-LAT-G-MORF-DECL1-MASC-001",
            "node_ids": ["LAT-G-MORF-DECL1-MASC"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": 0.0,
            "discrimination_initial": 1.0,
            "expected_time_sec": 12,
            "stimulus": "Noem twee mannelijke woorden die toch bij de 1e declinatie horen.",
            "answer": ["nauta en poeta", "nauta, poeta, pirata, agricola"],
            "feedback": "Nauta (zeeman), poeta (dichter), pirata (piraat) en agricola (boer) zijn masculinum maar volgen de 1e declinatie.",
            "source": "manual",
        },
        {
            "id": "ITEM-LAT-G-MORF-DECL1-MASC-002",
            "node_ids": ["LAT-G-MORF-DECL1-MASC"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": 0.2,
            "discrimination_initial": 1.0,
            "expected_time_sec": 15,
            "stimulus": "Verbuigen mannelijke woorden van de 1e declinatie anders dan vrouwelijke?",
            "answer": "nee, de uitgangen zijn identiek",
            "feedback": "Masculina van de 1e declinatie verbuigen identiek aan feminina. Alleen het genus verschilt (m. in plaats van f.).",
            "source": "manual",
        },
        {
            "id": "ITEM-LAT-G-MORF-DECL1-MASC-003",
            "node_ids": ["LAT-G-MORF-DECL1-MASC"],
            "type": "production",
            "direction": "productive",
            "difficulty_initial": 0.7,
            "discrimination_initial": 1.0,
            "expected_time_sec": 20,
            "stimulus": "Geef de genitivus meervoud van 'nauta'.",
            "answer": "nautarum",
            "feedback": "Nauta verbuigt als een gewoon 1e-declinatiewoord: nauta, nautae → gen. pl. nautārum.",
            "source": "manual",
        },
    ]

    # ── DECL1-PARAD (leerjaar1.json, 4 items incl. analyse) ─────────

    items["LAT-G-MORF-DECL1-PARAD"] = [
        {
            "id": "ITEM-LAT-G-MORF-DECL1-PARAD-001",
            "node_ids": ["LAT-G-MORF-DECL1-PARAD"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": -0.1,
            "discrimination_initial": 1.0,
            "expected_time_sec": 12,
            "stimulus": "Welke twee naamvallen van de 1e declinatie meervoud hebben dezelfde uitgang -is?",
            "answer": "dativus pluralis en ablativus pluralis",
            "feedback": "De dativus en ablativus pluralis eindigen beiden op -īs. Context bepaalt de functie.",
            "source": "manual",
        },
        {
            "id": "ITEM-LAT-G-MORF-DECL1-PARAD-002",
            "node_ids": ["LAT-G-MORF-DECL1-PARAD"],
            "type": "analysis",
            "direction": "receptive",
            "difficulty_initial": 1.0,
            "discrimination_initial": 1.2,
            "expected_time_sec": 30,
            "stimulus": "Ontleed 'puellarum' volledig.",
            "answer": "genitivus pluralis, 1e declinatie",
            "feedback": "Puell-ārum: stam puell- + uitgang -ārum = genitivus pluralis van de 1e declinatie.",
            "source": "manual",
        },
        {
            "id": "ITEM-LAT-G-MORF-DECL1-PARAD-003",
            "node_ids": ["LAT-G-MORF-DECL1-PARAD"],
            "type": "analysis",
            "direction": "receptive",
            "difficulty_initial": 1.2,
            "discrimination_initial": 1.2,
            "expected_time_sec": 35,
            "stimulus": "Ontleed 'terris' volledig.",
            "answer": ["dativus pluralis of ablativus pluralis, 1e declinatie"],
            "feedback": "Terr-īs: stam terr- + uitgang -īs = dativus of ablativus pluralis van de 1e declinatie. De context bepaalt welke.",
            "source": "manual",
        },
        {
            "id": "ITEM-LAT-G-MORF-DECL1-PARAD-004",
            "node_ids": ["LAT-G-MORF-DECL1-PARAD"],
            "type": "production",
            "direction": "productive",
            "difficulty_initial": 0.8,
            "discrimination_initial": 1.0,
            "expected_time_sec": 25,
            "stimulus": "Verbuig 'puella' in de genitivus singularis en meervoud.",
            "answer": "puellae, puellarum",
            "feedback": "Gen. sg. puell-ae, gen. pl. puell-ārum. Let op: gen. sg. -ae is gelijk aan dat. sg. en nom. pl.",
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

    print("\n=== C1-02 Summary ===")
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
