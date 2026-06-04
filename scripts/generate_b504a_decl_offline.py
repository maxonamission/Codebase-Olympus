#!/usr/bin/env python3
"""B5-04a: Generate offline_schrijven items for declination paradigm nodes.

Adds ~15 paradigma-schrijfoefeningen to declinatie-nodes in
lat_grammatica_leerjaar1.json.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from gymnasium_classica.models.graph import Item

# --- Item specifications (compact) ---
# (node_id, stimulus, expected_result, feedback, difficulty)

ITEMS = [
    # === 1e declinatie ===
    (
        "LAT-G-MORF-DECL1-PARAD",
        "Schrijf de volledige verbuiging van 'puella, puellae f.' (alle naamvallen, enkelvoud en meervoud) op papier.",
        "puella, puellae, puellae, puellam, puella, puellā / puellae, puellarum, puellis, puellas, puellae, puellis",
        "Controleer of je zes naamvallen hebt in beide numeri. Let op: gen.sg. en dat.sg. zijn allebei -ae.",
        0.5,
    ),
    (
        "LAT-G-MORF-DECL1-PARAD",
        "Schrijf de volledige verbuiging van 'terra, terrae f.' op papier.",
        "terra, terrae, terrae, terram, terra, terrā / terrae, terrarum, terris, terras, terrae, terris",
        "Controleer dat abl.sg. op -ā eindigt (lang) en dat dat.pl. en abl.pl. beide -is zijn.",
        0.5,
    ),
    (
        "LAT-G-MORF-DECL1-MASC",
        "Schrijf de volledige verbuiging van 'nauta, nautae m.' op papier en markeer het grammaticale geslacht.",
        "nauta, nautae, nautae, nautam, nauta, nautā / nautae, nautarum, nautis, nautas, nautae, nautis (masculinum)",
        "Nauta is mannelijk ondanks de 1e-declinatie. De uitgangen zijn identiek aan puella-type.",
        0.7,
    ),
    # === 2e declinatie ===
    (
        "LAT-G-MORF-DECL2-PARAD",
        "Schrijf de volledige verbuiging van 'dominus, domini m.' op papier.",
        "dominus, domini, domino, dominum, domine, domino / domini, dominorum, dominis, dominos, domini, dominis",
        "Let op: voc.sg. is -e (niet -us). Nom.pl. en voc.pl. zijn beide -i.",
        0.5,
    ),
    (
        "LAT-G-MORF-DECL2-PARAD",
        "Schrijf de volledige verbuiging van 'bellum, belli n.' op papier.",
        "bellum, belli, bello, bellum, bellum, bello / bella, bellorum, bellis, bella, bella, bellis",
        "Neutrum-regel: nom.=acc.=voc. in beide numeri. Meervoud: -a (niet -i).",
        0.6,
    ),
    (
        "LAT-G-MORF-DECL2-MASC",
        "Schrijf de volledige verbuiging van 'servus, servi m.' op papier.",
        "servus, servi, servo, servum, serve, servo / servi, servorum, servis, servos, servi, servis",
        "Let op: voc.sg. is serve (niet servus). Acc.pl. kan ook servōs zijn.",
        0.5,
    ),
    (
        "LAT-G-MORF-DECL2-ER",
        "Schrijf de volledige verbuiging van 'puer, pueri m.' op papier.",
        "puer, pueri, puero, puerum, puer, puero / pueri, puerorum, pueris, pueros, pueri, pueris",
        "Puer behoudt de -e- in alle vormen. Vergelijk met ager (agri) waar de -e- wegvalt.",
        0.7,
    ),
    (
        "LAT-G-MORF-DECL2-NEUT",
        "Schrijf de volledige verbuiging van 'templum, templi n.' op papier.",
        "templum, templi, templo, templum, templum, templo / templa, templorum, templis, templa, templa, templis",
        "Neutrum: nom.=acc.=voc. Meervoud nom./acc./voc. eindigen op -a.",
        0.5,
    ),
    # === 3e declinatie ===
    (
        "LAT-G-MORF-DECL3-PARAD",
        "Schrijf de volledige verbuiging van 'rex, regis m.' op papier.",
        "rex, regis, regi, regem, rex, rege / reges, regum, regibus, reges, reges, regibus",
        "Consonantstam: gen.pl. -um (niet -ium). Nom.sg. rex is onregelmatig (reg+s > rex).",
        0.8,
    ),
    (
        "LAT-G-MORF-DECL3-PARAD",
        "Schrijf de volledige verbuiging van 'mare, maris n.' op papier.",
        "mare, maris, mari, mare, mare, mari / maria, marium, maribus, maria, maria, maribus",
        "I-stam neutrum: abl.sg. -i, nom./acc.pl. -ia, gen.pl. -ium.",
        1.0,
    ),
    (
        "LAT-G-MORF-DECL3-CONS",
        "Schrijf de volledige verbuiging van 'consul, consulis m.' op papier.",
        "consul, consulis, consuli, consulem, consul, consule / consules, consulum, consulibus, consules, consules, consulibus",
        "Consonantstam: abl.sg. -e, gen.pl. -um. Nom.sg. = voc.sg. zonder uitgang.",
        0.8,
    ),
    (
        "LAT-G-MORF-DECL3-ISTAM",
        "Schrijf de volledige verbuiging van 'civis, civis c.' op papier.",
        "civis, civis, civi, civem, civis, cive / cives, civium, civibus, cives, cives, civibus",
        "I-stam: gen.pl. -ium. Herken i-stammen aan gelijk lettergreeptal nom./gen.sg.",
        0.9,
    ),
    (
        "LAT-G-MORF-DECL3-NEUT",
        "Schrijf de volledige verbuiging van 'corpus, corporis n.' op papier.",
        "corpus, corporis, corpori, corpus, corpus, corpore / corpora, corporum, corporibus, corpora, corpora, corporibus",
        "Neutrum consonantstam: nom.=acc.=voc., meervoud -a. Gen.pl. -um (niet -ium).",
        0.8,
    ),
]


def next_item_nr(node: dict) -> int:
    """Return the next available item number for a node."""
    existing = node.get("items", [])
    max_nr = 0
    for item in existing:
        parts = item["id"].rsplit("-", 1)
        if len(parts) == 2 and parts[1].isdigit():
            max_nr = max(max_nr, int(parts[1]))
    return max_nr + 1


def build_item(
    node_id: str, nr: int, stimulus: str, verwacht: str, feedback: str, difficulty: float
) -> dict:
    """Build an offline_schrijven item dict."""
    return {
        "id": f"ITEM-{node_id}-{nr:03d}",
        "node_ids": [node_id],
        "type": "offline_writing",
        "direction": "productive",
        "difficulty_initial": difficulty,
        "discrimination_initial": 1.0,
        "expected_time_sec": 120,
        "stimulus": stimulus,
        "answer": "Controleer je werk met het paradigma in je lesboek of de app.",
        "feedback": feedback,
        "source": "manual",
        "verification_method": "self_report",
        "expected_result": verwacht,
    }


def main():
    data_dir = ROOT / "data" / "graph"
    target_file = "lat_grammatica_leerjaar1.json"

    # Load JSON
    fpath = data_dir / target_file
    with open(fpath) as f:
        graph = json.load(f)

    # Index nodes by ID
    node_index = {k["id"]: k for k in graph["nodes"]}

    # Track counters per node
    counters: dict[str, int] = {}
    added = 0
    per_node: dict[str, int] = {}

    for node_id, stimulus, verwacht, feedback, difficulty in ITEMS:
        if node_id not in node_index:
            print(f"  SKIP: {node_id} not in {target_file}")
            continue

        node = node_index[node_id]
        if node_id not in counters:
            counters[node_id] = next_item_nr(node)

        nr = counters[node_id]
        item_data = build_item(node_id, nr, stimulus, verwacht, feedback, difficulty)

        # Validate via Pydantic
        Item(**item_data)

        if "items" not in node:
            node["items"] = []
        node["items"].append(item_data)
        counters[node_id] = nr + 1
        added += 1
        per_node[node_id] = per_node.get(node_id, 0) + 1

    # Write back
    with open(fpath, "w") as f:
        json.dump(graph, f, indent=2, ensure_ascii=False)
        f.write("\n")

    # Summary
    print("\n=== B5-04a: Declinatie paradigma-schrijfoefeningen ===")
    print(f"Bestand: {target_file}")
    print(f"Totaal toegevoegd: {added} items")
    print(f"Knopen geraakt: {len(per_node)}")
    for kid, count in sorted(per_node.items()):
        print(f"  {kid}: +{count} item(s)")


if __name__ == "__main__":
    main()
