#!/usr/bin/env python3
"""Generate exercise items for C1-06: presens indicativus (A1-06+A1-07 nodes).

Targets:
  - data/graph/lat_grammatica_poc.json  (CONJ-INTRO, PRAES-C1..C4-ACT, PRAES-ESSE)
  - data/graph/lat_grammatica_leerjaar1.json (MODUS-INTRO, CONJ-HERKEN, PRAES-INTRO,
    PRAES-C3B-ACT, PRAES-POSSE, PRAES-PARAD)
~45 items total.
"""

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from gymnasium_classica.models.graph import Item

POC_IDS = {
    "LAT-G-MORF-CONJ-INTRO",
    "LAT-G-MORF-PRAES-C1-ACT",
    "LAT-G-MORF-PRAES-C2-ACT",
    "LAT-G-MORF-PRAES-C3-ACT",
    "LAT-G-MORF-PRAES-C4-ACT",
    "LAT-G-MORF-PRAES-ESSE",
}
LJ1_IDS = {
    "LAT-G-MORF-MODUS-INTRO",
    "LAT-G-MORF-CONJ-HERKEN",
    "LAT-G-MORF-PRAES-INTRO",
    "LAT-G-MORF-PRAES-C3B-ACT",
    "LAT-G-MORF-PRAES-POSSE",
    "LAT-G-MORF-PRAES-PARAD",
}


def _h(kid, nr, stim, antw, fb, moeil=-0.3, tijd=12):
    return {
        "id": f"ITEM-{kid}-{nr:03d}",
        "node_ids": [kid],
        "type": "recognition",
        "direction": "receptive",
        "difficulty_initial": moeil,
        "discrimination_initial": 1.0,
        "expected_time_sec": tijd,
        "stimulus": stim,
        "answer": antw,
        "feedback": fb,
        "source": "manual",
    }


def _p(kid, nr, stim, antw, fb, moeil=0.6, tijd=20):
    return {
        "id": f"ITEM-{kid}-{nr:03d}",
        "node_ids": [kid],
        "type": "production",
        "direction": "productive",
        "difficulty_initial": moeil,
        "discrimination_initial": 1.0,
        "expected_time_sec": tijd,
        "stimulus": stim,
        "answer": antw,
        "feedback": fb,
        "source": "manual",
    }


def _a(kid, nr, stim, antw, fb, moeil=1.0, tijd=30):
    return {
        "id": f"ITEM-{kid}-{nr:03d}",
        "node_ids": [kid],
        "type": "analysis",
        "direction": "receptive",
        "difficulty_initial": moeil,
        "discrimination_initial": 1.2,
        "expected_time_sec": tijd,
        "stimulus": stim,
        "answer": antw,
        "feedback": fb,
        "source": "manual",
    }


def define_items() -> dict[str, list[dict]]:
    I = {}  # noqa: E741 - script-lokale conventie

    # ── Concept-nodes (A1-06) ───────────────────────────────────────

    K = "LAT-G-MORF-CONJ-INTRO"
    I[K] = [
        _h(
            K,
            1,
            "Hoeveel conjugaties kent het Latijn (inclusief de gemengde)?",
            "5 (4 reguliere + de gemengde conjugatie)",
            "Het Latijn kent vier reguliere conjugaties plus de gemengde conjugatie (soms '3b' genoemd).",
            -0.5,
            12,
        ),
        _h(
            K,
            2,
            "Wat is een conjugatie?",
            "een groep werkwoorden met hetzelfde vervoegingspatroon",
            "Een conjugatie is een groep werkwoorden die dezelfde persoonsuitgangen en stamklinkers delen.",
            -0.3,
            12,
        ),
    ]

    K = "LAT-G-MORF-MODUS-INTRO"
    I[K] = [
        _h(
            K,
            1,
            "Welke drie modi kent het Latijnse werkwoord?",
            "indicativus, imperativus, conjunctivus",
            "De indicativus (werkelijkheid), imperativus (bevel) en conjunctivus (wens/mogelijkheid). In klas 1 staat de indicativus centraal.",
            -0.4,
            15,
        ),
        _h(
            K,
            2,
            "Welke modus gebruik je om een feit of werkelijkheid uit te drukken?",
            "indicativus",
            "De indicativus is de modus van de werkelijkheid: 'hij loopt', 'zij heeft geschreven'.",
            -0.5,
            10,
        ),
    ]

    K = "LAT-G-MORF-PRAES-INTRO"
    I[K] = [
        _h(
            K,
            1,
            "Hoe wordt het praesens indicativus actief gevormd?",
            "praesens-stam + persoonsuitgang",
            "Vorming: praesensstam (= infinitivus minus uitgang) + persoonsuitgangen (-o/-m, -s, -t, -mus, -tis, -nt).",
            -0.2,
            15,
        ),
        _h(
            K,
            2,
            "Welke zes persoonsuitgangen heeft het praesens actief?",
            "-o/-m, -s, -t, -mus, -tis, -nt",
            "De standaard persoonsuitgangen: -o (1e sg.), -s (2e sg.), -t (3e sg.), -mus (1e pl.), -tis (2e pl.), -nt (3e pl.).",
            -0.1,
            15,
        ),
    ]

    K = "LAT-G-MORF-CONJ-HERKEN"
    I[K] = [
        _h(
            K,
            1,
            "Hoe herken je de conjugatie aan de infinitivus?",
            "-are (1e), -ēre (2e), -ĕre (3e), -ire (4e)",
            "Infinitivusuitgangen: -āre = 1e (amāre), -ēre = 2e (monēre), -ĕre = 3e (regĕre), -īre = 4e (audīre).",
            -0.1,
            15,
        ),
        _h(
            K,
            2,
            "Tot welke conjugatie hoort 'audire'?",
            "de 4e conjugatie",
            "Audīre eindigt op -īre: 4e conjugatie. Vergelijk: amāre (1e), monēre (2e), regĕre (3e).",
            -0.3,
            10,
        ),
        _h(
            K,
            3,
            "Tot welke conjugatie hoort 'monere' (met lange e)?",
            "de 2e conjugatie",
            "Monēre (lange -ē-) hoort bij de 2e conjugatie. Let op: regĕre (korte -ĕ-) is 3e conjugatie.",
            0.0,
            12,
        ),
    ]

    # ── Praesens per conjugatie (A1-07) ──────────────────────────────

    K = "LAT-G-MORF-PRAES-C1-ACT"
    I[K] = [
        _h(
            K,
            1,
            "Welke persoon en getal is 'amat'?",
            "3e persoon enkelvoud praesens",
            "Am-a-t: stam am- + stamklinker -a- + uitgang -t = 3e persoon singularis.",
            -0.3,
            10,
        ),
        _p(
            K,
            2,
            "Vervoeg 'amare' in de 1e persoon enkelvoud praesens.",
            "amo",
            "1e conjugatie: stam am- + -o = amo. De stamklinker -a- valt weg voor -o.",
            0.5,
            15,
        ),
        _p(
            K,
            3,
            "Vervoeg 'amare' in de 3e persoon meervoud praesens.",
            "amant",
            "1e conjugatie: stam am- + -a- + -nt = amant.",
            0.6,
            15,
        ),
        _p(
            K,
            4,
            "Vervoeg 'laudare' in de 2e persoon enkelvoud praesens.",
            "laudas",
            "1e conjugatie: stam laud- + -a- + -s = laudas.",
            0.5,
            15,
        ),
    ]

    K = "LAT-G-MORF-PRAES-C2-ACT"
    I[K] = [
        _h(
            K,
            1,
            "Welke persoon en getal is 'monet'?",
            "3e persoon enkelvoud praesens",
            "Mon-e-t: stam mon- + stamklinker -e- + uitgang -t = 3e persoon singularis.",
            -0.3,
            10,
        ),
        _p(
            K,
            2,
            "Vervoeg 'monere' in de 1e persoon enkelvoud praesens.",
            "moneo",
            "2e conjugatie: stam mon- + -e- + -o = moneo. De stamklinker blijft (anders dan bij 1e conj.).",
            0.5,
            15,
        ),
        _p(
            K,
            3,
            "Vervoeg 'monere' in de 1e persoon meervoud praesens.",
            "monemus",
            "2e conjugatie: stam mon- + -e- + -mus = monemus.",
            0.6,
            15,
        ),
        _p(
            K,
            4,
            "Vervoeg 'habere' in de 3e persoon meervoud praesens.",
            "habent",
            "2e conjugatie: stam hab- + -e- + -nt = habent.",
            0.5,
            15,
        ),
    ]

    K = "LAT-G-MORF-PRAES-C3-ACT"
    I[K] = [
        _h(
            K,
            1,
            "Welke persoon en getal is 'regit'?",
            "3e persoon enkelvoud praesens",
            "Reg-i-t: stam reg- + bindklinker -i- + uitgang -t. Bij de 3e conj. varieert de bindklinker.",
            -0.2,
            10,
        ),
        _p(
            K,
            2,
            "Vervoeg 'regere' in de 1e persoon enkelvoud praesens.",
            "rego",
            "3e conjugatie: stam reg- + -o = rego (geen bindklinker voor -o).",
            0.5,
            15,
        ),
        _p(
            K,
            3,
            "Vervoeg 'regere' in de 3e persoon meervoud praesens.",
            "regunt",
            "3e conjugatie: stam reg- + -u- + -nt = regunt. Let op: -u- als bindklinker voor -nt.",
            0.7,
            15,
        ),
        _p(
            K,
            4,
            "Vervoeg 'ducere' in de 2e persoon meervoud praesens.",
            "ducitis",
            "3e conjugatie: stam duc- + -i- + -tis = ducitis.",
            0.6,
            15,
        ),
    ]

    K = "LAT-G-MORF-PRAES-C4-ACT"
    I[K] = [
        _h(
            K,
            1,
            "Welke persoon en getal is 'audit'?",
            "3e persoon enkelvoud praesens",
            "Aud-i-t: stam aud- + stamklinker -i- + uitgang -t = 3e persoon singularis.",
            -0.3,
            10,
        ),
        _p(
            K,
            2,
            "Vervoeg 'audire' in de 1e persoon enkelvoud praesens.",
            "audio",
            "4e conjugatie: stam aud- + -i- + -o = audio.",
            0.5,
            15,
        ),
        _p(
            K,
            3,
            "Vervoeg 'audire' in de 3e persoon meervoud praesens.",
            "audiunt",
            "4e conjugatie: stam aud- + -iu- + -nt = audiunt. Let op: -iu- voor -nt (net als 3e conj.).",
            0.7,
            15,
        ),
    ]

    K = "LAT-G-MORF-PRAES-C3B-ACT"
    I[K] = [
        _h(
            K,
            1,
            "Wat is de gemengde conjugatie?",
            "werkwoorden met infinitivus op -ĕre maar 1e sg. op -io (zoals capio)",
            "De gemengde conjugatie (3b) lijkt op de 3e conj. (inf. -ĕre) maar heeft -io in de 1e sg. en -iu-nt in de 3e pl.",
            0.1,
            15,
        ),
        _p(
            K,
            2,
            "Vervoeg 'capere' in de 1e persoon enkelvoud praesens.",
            "capio",
            "Gemengde conj.: stam cap- + -i- + -o = capio (niet *capo). De -i- onderscheidt het van de 3e conj.",
            0.7,
            15,
        ),
        _p(
            K,
            3,
            "Vervoeg 'capere' in de 3e persoon meervoud praesens.",
            "capiunt",
            "Gemengde conj.: cap- + -iu- + -nt = capiunt (net als 4e conj. audiunt).",
            0.8,
            15,
        ),
    ]

    # ── Onregelmatig ─────────────────────────────────────────────────

    K = "LAT-G-MORF-PRAES-ESSE"
    I[K] = [
        _h(
            K,
            1,
            "Vervoeg 'esse' volledig in het praesens.",
            "sum, es, est, sumus, estis, sunt",
            "Esse is onregelmatig: sum, es, est, sumus, estis, sunt. De stam wisselt tussen s- en es-.",
            -0.1,
            15,
        ),
        _h(
            K,
            2,
            "Welke persoon en getal is 'sunt'?",
            "3e persoon meervoud praesens",
            "Sunt = 3e persoon pluralis van esse (zij zijn).",
            -0.4,
            10,
        ),
        _p(
            K,
            3,
            "Geef de 1e persoon meervoud van 'esse'.",
            "sumus",
            "Esse praesens: sumus (wij zijn). Let op: stam su- + -mus.",
            0.3,
            15,
        ),
        _p(
            K,
            4,
            "Geef de 2e persoon enkelvoud van 'esse'.",
            "es",
            "Esse praesens: es (jij bent). De kortste vorm van het paradigma.",
            0.2,
            10,
        ),
    ]

    K = "LAT-G-MORF-PRAES-POSSE"
    I[K] = [
        _h(
            K,
            1,
            "Hoe is 'posse' samengesteld?",
            "pot- + esse (kunnen = machtig-zijn)",
            "Posse = pot- + esse. De -t- wordt -s- voor een s: pot+sum → possum, pot+es → potes.",
            0.1,
            15,
        ),
        _p(
            K,
            2,
            "Vervoeg 'posse' in de 1e persoon enkelvoud praesens.",
            "possum",
            "Pot- + sum = possum (t → s voor s). Vergelijk: potes (pot+es), potest (pot+est).",
            0.7,
            15,
        ),
        _p(
            K,
            3,
            "Vervoeg 'posse' in de 3e persoon meervoud praesens.",
            "possunt",
            "Pot- + sunt = possunt (t → s voor s).",
            0.7,
            15,
        ),
    ]

    # ── Paradigma-overzicht ──────────────────────────────────────────

    K = "LAT-G-MORF-PRAES-PARAD"
    I[K] = [
        _a(
            K,
            1,
            "Ontleed 'regunt' volledig.",
            "3e persoon meervoud praesens indicativus actief, 3e conjugatie",
            "Reg-u-nt: stam reg- + bindklinker -u- + uitgang -nt. De -u- voor -nt is kenmerkend voor de 3e conj.",
            1.0,
            30,
        ),
        _a(
            K,
            2,
            "Ontleed 'audiunt' volledig.",
            "3e persoon meervoud praesens indicativus actief, 4e conjugatie",
            "Aud-iu-nt: stam aud- + -iu- + -nt. Vergelijk capiunt (gem. conj.) — dezelfde uitgang.",
            1.1,
            30,
        ),
        _a(
            K,
            3,
            "Welke conjugatie is 'monemus'? Leg uit.",
            "2e conjugatie — stam mon- + stamklinker -e- + uitgang -mus",
            "De lange -e- is kenmerkend voor de 2e conjugatie. Vergelijk: amamus (1e, -a-), regimus (3e, -i-).",
            1.2,
            35,
        ),
        _h(
            K,
            4,
            "Welke twee conjugaties lijken op elkaar in de 3e pers. mv. (-iunt)?",
            "de 4e conjugatie en de gemengde conjugatie",
            "Zowel 4e conj. (audiunt) als gem. conj. (capiunt) hebben -iunt in de 3e pers. pl.",
            0.3,
            15,
        ),
    ]

    return I


def validate_items(items_by_node):
    for _kid, il in items_by_node.items():
        for d in il:
            Item(**d)
    print("All items validated successfully.")


def add_items_to_json(json_path, items_by_node):
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)
    added = 0
    for node in data["nodes"]:
        if node["id"] in items_by_node:
            existing = {i["id"] for i in node.get("items", [])}
            new = [i for i in items_by_node[node["id"]] if i["id"] not in existing]
            node.setdefault("items", []).extend(new)
            added += len(new)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return added


def print_summary(items_by_node):
    total = sum(len(v) for v in items_by_node.values())
    tc = Counter()
    for il in items_by_node.values():
        for i in il:
            tc[i["type"]] += 1
    print(f"\n=== C1-06 Summary ===\nKnopen: {len(items_by_node)}\nTotal items: {total}")
    for k, v in sorted(items_by_node.items()):
        print(f"  {k}: {len(v)}")
    print("\nOefentype-verdeling:")
    for t, c in tc.most_common():
        print(f"  {t}: {c}")


def main():
    items = define_items()
    validate_items(items)
    base = Path(__file__).parent.parent / "data" / "graph"
    a1 = add_items_to_json(
        base / "lat_grammatica_poc.json", {k: v for k, v in items.items() if k in POC_IDS}
    )
    a2 = add_items_to_json(
        base / "lat_grammatica_leerjaar1.json", {k: v for k, v in items.items() if k in LJ1_IDS}
    )
    print(f"Added {a1} items to poc, {a2} items to leerjaar1")
    print_summary(items)


if __name__ == "__main__":
    main()
