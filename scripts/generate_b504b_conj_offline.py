#!/usr/bin/env python3
"""B5-04b: Generate offline_schrijven items for conjugation paradigm nodes.

Adds ~37 paradigma-schrijfoefeningen to conjugatie-knopen in both
lat_grammatica_poc.json and lat_grammatica_leerjaar1.json.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from gymnasium_classica.models.graph import Item

# --- Compact item specs ---
# (node_id, file, stimulus, verwacht_resultaat, feedback, moeilijkheid)

ITEMS = [
    # === PRAESENS (poc) ===
    (
        "LAT-G-MORF-PRAES-C1-ACT",
        "lat_grammatica_poc.json",
        "Schrijf de volledige vervoeging van 'amare' in de presens indicativus actief op papier.",
        "amo, amas, amat, amamus, amatis, amant",
        "Stam ama- + persoonsuitgangen. Let op: 1e pers.sg. amo (niet amao).",
        0.4,
    ),
    (
        "LAT-G-MORF-PRAES-C2-ACT",
        "lat_grammatica_poc.json",
        "Schrijf de volledige vervoeging van 'monēre' in de presens indicativus actief op papier.",
        "moneo, mones, monet, monemus, monetis, monent",
        "Stam mone- + persoonsuitgangen. De stamklinker -e- is lang (ē) en blijft in alle vormen.",
        0.4,
    ),
    (
        "LAT-G-MORF-PRAES-C3-ACT",
        "lat_grammatica_poc.json",
        "Schrijf de volledige vervoeging van 'legere' in de presens indicativus actief op papier.",
        "lego, legis, legit, legimus, legitis, legunt",
        "3e conjugatie: stamklinker wisselt (e/i/u). Let op: 3e pl. -unt (niet -ent).",
        0.5,
    ),
    (
        "LAT-G-MORF-PRAES-C4-ACT",
        "lat_grammatica_poc.json",
        "Schrijf de volledige vervoeging van 'audīre' in de presens indicativus actief op papier.",
        "audio, audis, audit, audimus, auditis, audiunt",
        "4e conjugatie: stamklinker -i- lang. Let op: 3e pl. audiunt (met -i-).",
        0.4,
    ),
    (
        "LAT-G-MORF-PRAES-ESSE",
        "lat_grammatica_poc.json",
        "Schrijf de volledige vervoeging van 'esse' in de presens indicativus op papier.",
        "sum, es, est, sumus, estis, sunt",
        "Onregelmatig werkwoord. Let op de stamwisseling su-/es-.",
        0.3,
    ),
    (
        "LAT-G-MORF-INF-PRAES-ACT",
        "lat_grammatica_poc.json",
        "Schrijf de infinitivus presens actief van alle vier conjugaties + esse op papier.",
        "1e: -āre (amare), 2e: -ēre (monere), 3e: -ere (legere), 4e: -īre (audire), esse",
        "Let op het verschil tussen 2e conj. -ēre (lang) en 3e conj. -ere (kort).",
        0.5,
    ),
    (
        "LAT-G-MORF-IMPF-C1C2-ACT",
        "lat_grammatica_poc.json",
        "Schrijf de volledige vervoeging van 'amare' in het imperfectum indicativus actief op papier.",
        "amabam, amabas, amabat, amabamus, amabatis, amabant",
        "Kenmerk: -ba- tussen stam en persoonsuitgang. 1e pers.sg. -bam.",
        0.5,
    ),
    (
        "LAT-G-MORF-IMPF-C3C4-ACT",
        "lat_grammatica_poc.json",
        "Schrijf de volledige vervoeging van 'audīre' in het imperfectum indicativus actief op papier.",
        "audiebam, audiebas, audiebat, audiebamus, audiebatis, audiebant",
        "3e/4e conjugatie: -eba- (met extra -e-). Vergelijk met 1e/2e: -ba-.",
        0.6,
    ),
    # === PRAESENS (leerjaar1) ===
    (
        "LAT-G-MORF-PRAES-C3B-ACT",
        "lat_grammatica_leerjaar1.json",
        "Schrijf de volledige vervoeging van 'capere' (gemengde conjugatie) in de presens indicativus actief op papier.",
        "capio, capis, capit, capimus, capitis, capiunt",
        "Gemengde conjugatie: als 3e maar met -i- in 1e sg. en 3e pl. (capio, capiunt).",
        0.7,
    ),
    (
        "LAT-G-MORF-PRAES-POSSE",
        "lat_grammatica_leerjaar1.json",
        "Schrijf de volledige vervoeging van 'posse' in de presens indicativus op papier.",
        "possum, potes, potest, possumus, potestis, possunt",
        "Pot- voor klinker (potes), pos- voor s (possum). Samengesteld uit pot+esse.",
        0.6,
    ),
    (
        "LAT-G-MORF-PRAES-PARAD",
        "lat_grammatica_leerjaar1.json",
        "Schrijf de presens indicativus actief van alle vier conjugaties naast elkaar op papier (1e pers. sg. t/m 3e pers. pl.).",
        "1e: amo/as/at/amus/atis/ant, 2e: moneo/es/et/emus/etis/ent, 3e: lego/is/it/imus/itis/unt, 4e: audio/is/it/imus/itis/iunt",
        "Vergelijk de stamklinkers: -a-, -e-, wisselend, -i-. 3e pl.: -ant/-ent/-unt/-iunt.",
        0.8,
    ),
    (
        "LAT-G-MORF-PRAES-PARAD",
        "lat_grammatica_leerjaar1.json",
        "Schrijf de presens indicativus actief van 'esse' en 'posse' naast elkaar op papier.",
        "sum/possum, es/potes, est/potest, sumus/possumus, estis/potestis, sunt/possunt",
        "Posse = pot/pos + esse. Let op: pos- voor s, pot- voor klinker.",
        0.7,
    ),
    # === IMPERFECTUM (leerjaar1) ===
    (
        "LAT-G-MORF-IMPF-ESSE",
        "lat_grammatica_leerjaar1.json",
        "Schrijf de volledige vervoeging van 'esse' in het imperfectum indicativus op papier.",
        "eram, eras, erat, eramus, eratis, erant",
        "Imperfectum van esse: stam era- + persoonsuitgangen. Regelmatig patroon.",
        0.4,
    ),
    (
        "LAT-G-MORF-IMPF-C3B-ACT",
        "lat_grammatica_leerjaar1.json",
        "Schrijf de volledige vervoeging van 'capere' in het imperfectum indicativus actief op papier.",
        "capiebam, capiebas, capiebat, capiebamus, capiebatis, capiebant",
        "Gemengde conjugatie: imperfectum met -ieba- (als 4e conjugatie).",
        0.7,
    ),
    (
        "LAT-G-MORF-IMPF-POSSE",
        "lat_grammatica_leerjaar1.json",
        "Schrijf de volledige vervoeging van 'posse' in het imperfectum indicativus op papier.",
        "poteram, poteras, poterat, poteramus, poteratis, poterant",
        "Pot- + eram: regelmatig imperfectum op basis van esse.",
        0.5,
    ),
    (
        "LAT-G-MORF-IMPF-PARAD",
        "lat_grammatica_leerjaar1.json",
        "Schrijf het imperfectum indicativus actief van conj. 1, 3 en esse naast elkaar op papier.",
        "1e: amabam/-bas/-bat/-bamus/-batis/-bant, 3e: legebam/-bas/-bat/-bamus/-batis/-bant, esse: eram/-as/-at/-amus/-atis/-ant",
        "Kenmerk imperfectum: -ba- (1e/2e) of -eba- (3e/4e). Esse heeft era-.",
        0.8,
    ),
    (
        "LAT-G-MORF-IMPF-PARAD",
        "lat_grammatica_leerjaar1.json",
        "Schrijf het imperfectum indicativus actief van alle vier conjugaties op papier (alleen 1e pers.sg. + 3e pers.pl.).",
        "1e: amabam/amabant, 2e: monebam/monebant, 3e: legebam/legebant, 4e: audiebam/audiebant",
        "Let op het verschil: 1e/2e -ba-, 3e/4e -eba-. Uitgang 3e pl. altijd -nt.",
        0.6,
    ),
    # === PERFECTUM (leerjaar1) ===
    (
        "LAT-G-MORF-PERF-C1-ACT",
        "lat_grammatica_leerjaar1.json",
        "Schrijf de volledige vervoeging van 'amāre' in het perfectum indicativus actief op papier.",
        "amavi, amavisti, amavit, amavimus, amavistis, amaverunt",
        "V-perfectum: stam amav-. Uitgangen: -i, -isti, -it, -imus, -istis, -erunt.",
        0.6,
    ),
    (
        "LAT-G-MORF-PERF-C2-ACT",
        "lat_grammatica_leerjaar1.json",
        "Schrijf de volledige vervoeging van 'monēre' in het perfectum indicativus actief op papier.",
        "monui, monuisti, monuit, monuimus, monuistis, monuerunt",
        "U-perfectum: stam monu-. Perfectumstam kan afwijken van de presensstam.",
        0.7,
    ),
    (
        "LAT-G-MORF-PERF-C3-ACT",
        "lat_grammatica_leerjaar1.json",
        "Schrijf de volledige vervoeging van 'legere' in het perfectum indicativus actief op papier.",
        "legi, legisti, legit, legimus, legistis, legerunt",
        "Stam-perfectum (zonder extra kenmerk). Let op: legit kan presens of perfectum zijn.",
        0.8,
    ),
    (
        "LAT-G-MORF-PERF-C4-ACT",
        "lat_grammatica_leerjaar1.json",
        "Schrijf de volledige vervoeging van 'audīre' in het perfectum indicativus actief op papier.",
        "audivi, audivisti, audivit, audivimus, audivistis, audiverunt",
        "V-perfectum: stam audiv-. Regelmatig als 1e conjugatie.",
        0.6,
    ),
    (
        "LAT-G-MORF-PERF-ESSE",
        "lat_grammatica_leerjaar1.json",
        "Schrijf de volledige vervoeging van 'esse' in het perfectum indicativus op papier.",
        "fui, fuisti, fuit, fuimus, fuistis, fuerunt",
        "Perfectumstam fu- (suppletief). Uitgangen zijn regulier.",
        0.5,
    ),
    (
        "LAT-G-MORF-PERF-PARAD",
        "lat_grammatica_leerjaar1.json",
        "Schrijf de perfectum-uitgangen (alle personen) op papier, met een voorbeeld per perfectumtype (v, u, s, stam).",
        "-i, -isti, -it, -imus, -istis, -erunt. V: amavi, U: monui, S: dixi, Stam: legi",
        "De perfectum-uitgangen zijn altijd gelijk, alleen de perfectumstam verschilt per type.",
        0.7,
    ),
    (
        "LAT-G-MORF-PERF-PARAD",
        "lat_grammatica_leerjaar1.json",
        "Schrijf het perfectum indicativus actief van 'amare' en 'esse' naast elkaar op papier.",
        "amavi/fui, amavisti/fuisti, amavit/fuit, amavimus/fuimus, amavistis/fuistis, amaverunt/fuerunt",
        "Beide regelmatig in uitgangen. Verschil zit in de perfectumstam: amav- vs. fu-.",
        0.6,
    ),
    # === PLUSQUAMPERFECTUM (leerjaar1) ===
    (
        "LAT-G-MORF-PLQPF-REG-ACT",
        "lat_grammatica_leerjaar1.json",
        "Schrijf de volledige vervoeging van 'amare' in het plusquamperfectum indicativus actief op papier.",
        "amaveram, amaveras, amaverat, amaveramus, amaveratis, amaverant",
        "Perfectumstam + era- + persoonsuitgangen. Herkenbaar aan -era-.",
        0.7,
    ),
    (
        "LAT-G-MORF-PLQPF-ESSE",
        "lat_grammatica_leerjaar1.json",
        "Schrijf de volledige vervoeging van 'esse' in het plusquamperfectum indicativus op papier.",
        "fueram, fueras, fuerat, fueramus, fueratis, fuerant",
        "Perfectumstam fu- + eram. Regelmatig patroon.",
        0.6,
    ),
    (
        "LAT-G-MORF-PLQPF-POSSE",
        "lat_grammatica_leerjaar1.json",
        "Schrijf de volledige vervoeging van 'posse' in het plusquamperfectum indicativus op papier.",
        "potueram, potueras, potuerat, potueramus, potueratis, potuerant",
        "Perfectumstam potu- + eram. Vergelijk met imperfectum poteram.",
        0.7,
    ),
    (
        "LAT-G-MORF-PLQPF-PARAD",
        "lat_grammatica_leerjaar1.json",
        "Schrijf het plusquamperfectum van 'amare', 'legere' en 'esse' naast elkaar op papier (alle personen).",
        "amaveram/legeram/fueram, amaveras/legeras/fueras, amaverat/legerat/fuerat, amaveramus/legeramus/fueramus, amaveratis/legeratis/fueratis, amaverant/legerant/fuerant",
        "Alle drie: perfectumstam + era-uitgangen. Herken het -era- kenmerk.",
        0.9,
    ),
    # === IMPERATIVUS (leerjaar1) ===
    (
        "LAT-G-MORF-IMPER-SG",
        "lat_grammatica_leerjaar1.json",
        "Schrijf de imperativus singularis van alle vier conjugaties + esse op papier.",
        "1e: ama, 2e: mone, 3e: lege, 4e: audi, esse: es",
        "Imperativus sg. = zuivere stam (zonder uitgang). Esse: es.",
        0.4,
    ),
    (
        "LAT-G-MORF-IMPER-PL",
        "lat_grammatica_leerjaar1.json",
        "Schrijf de imperativus pluralis van alle vier conjugaties + esse op papier.",
        "1e: amate, 2e: monete, 3e: legite, 4e: audite, esse: este",
        "Imperativus pl. = stam + -te. Let op: 3e conj. -ite, 4e conj. -ite.",
        0.5,
    ),
    (
        "LAT-G-MORF-IMPER-ESSE",
        "lat_grammatica_leerjaar1.json",
        "Schrijf de imperativus singularis en pluralis van 'esse' op papier.",
        "sg.: es, pl.: este",
        "Es = 'wees!', este = 'weest!'. Onregelmatig maar eenvoudig.",
        0.3,
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
    node_id: str, nr: int, stimulus: str, verwacht: str, feedback: str, moeilijkheid: float
) -> dict:
    """Build an offline_schrijven item dict."""
    return {
        "id": f"ITEM-{node_id}-{nr:03d}",
        "knoop_ids": [node_id],
        "type": "offline_schrijven",
        "richting": "productief",
        "moeilijkheid_initieel": moeilijkheid,
        "discriminatie_initieel": 1.0,
        "verwachte_tijd_sec": 120,
        "stimulus": stimulus,
        "antwoord": "Controleer je werk met het paradigma in je lesboek of de app.",
        "feedback": feedback,
        "bron": "handmatig",
        "verificatie_methode": "self_report",
        "verwacht_resultaat": verwacht,
    }


def main():
    data_dir = ROOT / "data" / "graph"

    # Group items by file
    by_file: dict[str, list] = {}
    for node_id, fname, stimulus, verwacht, feedback, moeilijkheid in ITEMS:
        by_file.setdefault(fname, []).append((node_id, stimulus, verwacht, feedback, moeilijkheid))

    total_added = 0

    for fname, item_specs in by_file.items():
        fpath = data_dir / fname
        with open(fpath) as f:
            graph = json.load(f)

        node_index = {k["id"]: k for k in graph["knopen"]}
        counters: dict[str, int] = {}
        added = 0
        per_node: dict[str, int] = {}

        for node_id, stimulus, verwacht, feedback, moeilijkheid in item_specs:
            if node_id not in node_index:
                print(f"  SKIP: {node_id} not in {fname}")
                continue

            node = node_index[node_id]
            if node_id not in counters:
                counters[node_id] = next_item_nr(node)

            nr = counters[node_id]
            item_data = build_item(node_id, nr, stimulus, verwacht, feedback, moeilijkheid)

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

        print(f"\n--- {fname} ---")
        print(f"Toegevoegd: {added} items over {len(per_node)} knopen")
        for kid, count in sorted(per_node.items()):
            print(f"  {kid}: +{count}")
        total_added += added

    print("\n=== B5-04b: Conjugatie paradigma-schrijfoefeningen ===")
    print(f"Totaal toegevoegd: {total_added} items")


if __name__ == "__main__":
    main()
