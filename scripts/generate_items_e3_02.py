#!/usr/bin/env python3
"""Generate exercise items for E3-02: GRC INTRO-nodes (conceptknopen).

Target: data/graph/grc_grammatica_leerjaar1.json
Scope:  13 Greek concept nodes — naamval, numerus, genus, declinatie, conj.,
        tempus, persoon, thematisch, stamtijd, secundaire uitgangen, diathese
        en lidwoord (INTRO + VERBG).

Elke node krijgt 2 items: herkenning + self_assess (offline_schrijven met
verification_method=self_report) of productie. Voorbeelden zijn Grieks-specifiek
(ἄνθρωπος, λόγος, γράφω) — geen Latijnse overlap.

Run:
    python scripts/generate_items_e3_02.py            # writes items to graph
    python scripts/generate_items_e3_02.py --dry-run  # only validate + print
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
# Item definitions — grouped by theme.
# ---------------------------------------------------------------------------


def naamval_numerus_genus() -> dict[str, list[dict]]:
    """NAAMVAL, NUMERUS, GENUS — 6 items."""
    items: dict[str, list[dict]] = {}

    items["GRC-G-MORF-NAAMVAL-INTRO"] = [
        {
            "id": "ITEM-GRC-G-MORF-NAAMVAL-INTRO-001",
            "node_ids": ["GRC-G-MORF-NAAMVAL-INTRO"],
            "type": "herkenning",
            "direction": "receptief",
            "difficulty_initial": -1.0,
            "discrimination_initial": 1.0,
            "expected_time_sec": 10,
            "stimulus": "Hoeveel naamvallen kent het Grieks?",
            "answer": "5",
            "feedback": "Het Grieks kent vijf naamvallen: nominativus, genitivus, dativus, accusativus en vocativus.",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-NAAMVAL-INTRO-002",
            "node_ids": ["GRC-G-MORF-NAAMVAL-INTRO"],
            "type": "productie",
            "direction": "productief",
            "difficulty_initial": 0.2,
            "discrimination_initial": 1.0,
            "expected_time_sec": 25,
            "stimulus": "Noem de vijf Griekse naamvallen in de conventionele volgorde.",
            "answer": [
                "nominativus, genitivus, dativus, accusativus, vocativus",
                "nom, gen, dat, acc, voc",
            ],
            "feedback": "De conventionele volgorde is nominativus, genitivus, dativus, accusativus, vocativus — anders dan in het Latijn (zonder ablativus, met vocativus als aparte vorm).",
            "source": "handmatig",
        },
    ]

    items["GRC-G-MORF-NUMERUS-INTRO"] = [
        {
            "id": "ITEM-GRC-G-MORF-NUMERUS-INTRO-001",
            "node_ids": ["GRC-G-MORF-NUMERUS-INTRO"],
            "type": "herkenning",
            "direction": "receptief",
            "difficulty_initial": -1.0,
            "discrimination_initial": 1.0,
            "expected_time_sec": 10,
            "stimulus": "Welke twee numeri worden in het schoolgrieks onderscheiden?",
            "answer": ["singularis en pluralis", "enkelvoud en meervoud"],
            "feedback": "In het schoolgrieks gebruiken we singularis (enkelvoud) en pluralis (meervoud). De klassieke dualis wordt niet bekend verondersteld.",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-NUMERUS-INTRO-002",
            "node_ids": ["GRC-G-MORF-NUMERUS-INTRO"],
            "type": "herkenning",
            "direction": "receptief",
            "difficulty_initial": 0.0,
            "discrimination_initial": 1.0,
            "expected_time_sec": 15,
            "stimulus": "Is ἄνθρωποι singularis of pluralis?",
            "answer": ["pluralis", "meervoud"],
            "feedback": "ἄνθρωποι is pluralis (nominativus meervoud van ἄνθρωπος). De uitgang -οι signaleert meervoud in de ο-declinatie.",
            "source": "handmatig",
        },
    ]

    items["GRC-G-MORF-GENUS-INTRO"] = [
        {
            "id": "ITEM-GRC-G-MORF-GENUS-INTRO-001",
            "node_ids": ["GRC-G-MORF-GENUS-INTRO"],
            "type": "herkenning",
            "direction": "receptief",
            "difficulty_initial": -1.0,
            "discrimination_initial": 1.0,
            "expected_time_sec": 10,
            "stimulus": "Welke drie genera kent het Grieks?",
            "answer": [
                "masculinum, femininum, neutrum",
                "mannelijk, vrouwelijk, onzijdig",
            ],
            "feedback": "Het Grieks kent drie genera: masculinum, femininum en neutrum. Het lidwoord (ὁ, ἡ, τό) verraadt het genus.",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-GENUS-INTRO-002",
            "node_ids": ["GRC-G-MORF-GENUS-INTRO"],
            "type": "herkenning",
            "direction": "receptief",
            "difficulty_initial": -0.3,
            "discrimination_initial": 1.2,
            "expected_time_sec": 12,
            "stimulus": "Welk genus heeft ὁ λόγος?",
            "answer": ["masculinum", "mannelijk"],
            "feedback": "ὁ λόγος is masculinum — het lidwoord ὁ wijst op mannelijk genus, ook al eindigt het woord op -ος (niet automatisch m: vgl. ἡ ὁδός).",
            "source": "handmatig",
        },
    ]

    return items


def declinatie_conj_tempus() -> dict[str, list[dict]]:
    """DECL, CONJ, TEMPUS — 6 items."""
    items: dict[str, list[dict]] = {}

    items["GRC-G-MORF-DECL-INTRO"] = [
        {
            "id": "ITEM-GRC-G-MORF-DECL-INTRO-001",
            "node_ids": ["GRC-G-MORF-DECL-INTRO"],
            "type": "herkenning",
            "direction": "receptief",
            "difficulty_initial": -0.5,
            "discrimination_initial": 1.0,
            "expected_time_sec": 15,
            "stimulus": "Welke drie hoofdgroepen van declinaties onderscheidt men in het Grieks?",
            "answer": [
                "α/η-stammen, ο-stammen, medeklinkerstammen",
                "eerste, tweede, derde declinatie",
            ],
            "feedback": "De drie hoofdgroepen zijn α/η-stammen (1e decl.), ο-stammen (2e decl.) en medeklinkerstammen (3e decl.).",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-DECL-INTRO-002",
            "node_ids": ["GRC-G-MORF-DECL-INTRO"],
            "type": "herkenning",
            "direction": "receptief",
            "difficulty_initial": 0.0,
            "discrimination_initial": 1.2,
            "expected_time_sec": 15,
            "stimulus": "Tot welke declinatie behoort ἄνθρωπος?",
            "answer": [
                "tweede declinatie",
                "ο-stammen",
                "2e declinatie",
            ],
            "feedback": "ἄνθρωπος is een ο-stam (tweede declinatie) — de stam ἀνθρωπ- krijgt de kenmerkende ο/ε-klinker voor de uitgang.",
            "source": "handmatig",
        },
    ]

    items["GRC-G-MORF-CONJ-INTRO"] = [
        {
            "id": "ITEM-GRC-G-MORF-CONJ-INTRO-001",
            "node_ids": ["GRC-G-MORF-CONJ-INTRO"],
            "type": "herkenning",
            "direction": "receptief",
            "difficulty_initial": -0.4,
            "discrimination_initial": 1.0,
            "expected_time_sec": 12,
            "stimulus": "Welke twee hoofdtypes van Griekse werkwoorden onderscheidt men?",
            "answer": [
                "thematisch (-ω) en athematisch (-μι)",
                "thematische en athematische verba",
            ],
            "feedback": "Thematische verba eindigen in het praesens op -ω (γράφω); athematische op -μι (δίδωμι). Thematisch is veruit de grootste groep.",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-CONJ-INTRO-002",
            "node_ids": ["GRC-G-MORF-CONJ-INTRO"],
            "type": "herkenning",
            "direction": "receptief",
            "difficulty_initial": -0.1,
            "discrimination_initial": 1.0,
            "expected_time_sec": 15,
            "stimulus": "Op welke vijf dimensies wordt een Grieks werkwoord vervoegd?",
            "answer": [
                "persoon, getal, tijd, wijs, diathese",
                "persoon, numerus, tempus, modus, genus verbi",
            ],
            "feedback": "Een Griekse werkwoordsvorm draagt informatie over persoon, getal (numerus), tijd (tempus), wijs (modus) en diathese (genus verbi).",
            "source": "handmatig",
        },
    ]

    items["GRC-G-MORF-TEMPUS-INTRO"] = [
        {
            "id": "ITEM-GRC-G-MORF-TEMPUS-INTRO-001",
            "node_ids": ["GRC-G-MORF-TEMPUS-INTRO"],
            "type": "herkenning",
            "direction": "receptief",
            "difficulty_initial": -0.2,
            "discrimination_initial": 1.0,
            "expected_time_sec": 15,
            "stimulus": "Welke Griekse tijd drukt een eenmalige, afgeronde handeling in het verleden uit?",
            "answer": "aoristus",
            "feedback": "De aoristus noemt een eenmalige/afgeronde verleden handeling (punctueel). Het imperfectum drukt juist duur of herhaling uit.",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-TEMPUS-INTRO-002",
            "node_ids": ["GRC-G-MORF-TEMPUS-INTRO"],
            "type": "productie",
            "direction": "productief",
            "difficulty_initial": 0.3,
            "discrimination_initial": 1.0,
            "expected_time_sec": 25,
            "stimulus": "Noem de vijf werkwoordstijden die in leerjaar 1 aan bod komen.",
            "answer": [
                "praesens, imperfectum, aoristus, futurum, perfectum",
                "presens, imperfectum, aoristus, futurum, perfectum",
            ],
            "feedback": "De vijf tijden zijn praesens, imperfectum, aoristus, futurum en perfectum. De aoristus is uniek voor het Grieks t.o.v. het Latijn.",
            "source": "handmatig",
        },
    ]

    return items


def persoon_them_stamtijd() -> dict[str, list[dict]]:
    """PERSOON, THEM, STAMTIJD — 6 items."""
    items: dict[str, list[dict]] = {}

    items["GRC-G-MORF-PERSOON-INTRO"] = [
        {
            "id": "ITEM-GRC-G-MORF-PERSOON-INTRO-001",
            "node_ids": ["GRC-G-MORF-PERSOON-INTRO"],
            "type": "herkenning",
            "direction": "receptief",
            "difficulty_initial": -0.5,
            "discrimination_initial": 1.0,
            "expected_time_sec": 10,
            "stimulus": "Hoeveel persoonsvormen heeft een Grieks werkwoord per tijd?",
            "answer": "6",
            "feedback": "Zes vormen: 1e/2e/3e persoon × singularis/pluralis. Een dualis bestaat, maar wordt in het schoolgrieks niet actief geleerd.",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-PERSOON-INTRO-002",
            "node_ids": ["GRC-G-MORF-PERSOON-INTRO"],
            "type": "herkenning",
            "direction": "receptief",
            "difficulty_initial": 0.2,
            "discrimination_initial": 1.2,
            "expected_time_sec": 15,
            "stimulus": "Welke persoon en welk getal is γράφομεν?",
            "answer": [
                "1e persoon pluralis",
                "1e persoon meervoud",
            ],
            "feedback": "γράφομεν = 1e persoon pluralis praesens actief (uitgang -ομεν). De primaire uitgang -μεν markeert de 1e persoon meervoud.",
            "source": "handmatig",
        },
    ]

    items["GRC-G-MORF-THEM-INTRO"] = [
        {
            "id": "ITEM-GRC-G-MORF-THEM-INTRO-001",
            "node_ids": ["GRC-G-MORF-THEM-INTRO"],
            "type": "herkenning",
            "direction": "receptief",
            "difficulty_initial": -0.3,
            "discrimination_initial": 1.0,
            "expected_time_sec": 15,
            "stimulus": "Welke twee thematische klinkers komen afwisselend voor tussen stam en uitgang?",
            "answer": ["ο en ε", "ο/ε"],
            "feedback": "Thematische verba plakken een klinker ο of ε tussen stam en uitgang: ο vóór μ/ν (γράφομεν), ε elders (γράφετε).",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-THEM-INTRO-002",
            "node_ids": ["GRC-G-MORF-THEM-INTRO"],
            "type": "productie",
            "direction": "productief",
            "difficulty_initial": 0.4,
            "discrimination_initial": 1.2,
            "expected_time_sec": 25,
            "stimulus": "Splits γράφομεν in stam + thematische klinker + uitgang.",
            "answer": [
                "γραφ-ο-μεν",
                "γραφ + ο + μεν",
            ],
            "feedback": "Stam γραφ- + thematische klinker -ο- + persoonsuitgang -μεν. Vóór de nasaal μ kiest het Grieks ο, niet ε.",
            "source": "handmatig",
        },
    ]

    items["GRC-G-MORF-STAMTIJD"] = [
        {
            "id": "ITEM-GRC-G-MORF-STAMTIJD-001",
            "node_ids": ["GRC-G-MORF-STAMTIJD"],
            "type": "herkenning",
            "direction": "receptief",
            "difficulty_initial": -0.2,
            "discrimination_initial": 1.0,
            "expected_time_sec": 15,
            "stimulus": "Welke drie stammen onderscheiden we bij een regulier Grieks werkwoord in leerjaar 1?",
            "answer": [
                "praesensstam, aoriststam, perfectumstam",
                "praesens-, aorist- en perfectumstam",
            ],
            "feedback": "Drie stammen: praesensstam (γραφ-), aoriststam (γραψ-) en perfectumstam (γεγραφ-). Elke stam levert eigen tijdsvormen.",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-STAMTIJD-002",
            "node_ids": ["GRC-G-MORF-STAMTIJD"],
            "type": "offline_schrijven",
            "direction": "productief",
            "difficulty_initial": 0.5,
            "discrimination_initial": 1.0,
            "expected_time_sec": 60,
            "stimulus": "Schrijf de eerste drie stamtijden van γράφω op (1 sg. praesens, 1 sg. aoristus, 1 sg. perfectum) en controleer in je grammaticaboek.",
            "answer": "γράφω — ἔγραψα — γέγραφα",
            "feedback": "γράφω → ἔγραψα (aorist σ-stam) → γέγραφα (perfectum met reduplicatie γε-). Het leren van stamtijden is de sleutel tot de aorist en het perfectum.",
            "source": "handmatig",
            "verification_method": "self_report",
            "expected_result": "γράφω, ἔγραψα, γέγραφα — drie stamtijden met augment/reduplicatie correct genoteerd",
        },
    ]

    return items


def uit_diath_lidw() -> dict[str, list[dict]]:
    """UIT-SEC, DIATH, LIDW-INTRO, LIDW-VERBG — 8 items."""
    items: dict[str, list[dict]] = {}

    items["GRC-G-MORF-UIT-SEC"] = [
        {
            "id": "ITEM-GRC-G-MORF-UIT-SEC-001",
            "node_ids": ["GRC-G-MORF-UIT-SEC"],
            "type": "herkenning",
            "direction": "receptief",
            "difficulty_initial": -0.2,
            "discrimination_initial": 1.0,
            "expected_time_sec": 15,
            "stimulus": "Noem de zes secundaire uitgangen actief (thematisch).",
            "answer": [
                "-ον, -ες, -ε(ν), -ομεν, -ετε, -ον",
                "-ον -ες -ε -ομεν -ετε -ον",
            ],
            "feedback": "Secundaire uitgangen actief: -ον, -ες, -ε(ν), -ομεν, -ετε, -ον. Let op: 1 sg. en 3 pl. zijn identiek (-ον).",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-UIT-SEC-002",
            "node_ids": ["GRC-G-MORF-UIT-SEC"],
            "type": "herkenning",
            "direction": "receptief",
            "difficulty_initial": 0.0,
            "discrimination_initial": 1.2,
            "expected_time_sec": 15,
            "stimulus": "In welke twee werkwoordstijden gebruik je de secundaire uitgangen actief?",
            "answer": [
                "imperfectum en aoristus",
                "imperfectum + aoristus",
            ],
            "feedback": "Secundaire uitgangen horen bij verleden tijden op een indicatieve stam: imperfectum en (sigma-)aoristus — allebei met augment.",
            "source": "handmatig",
        },
    ]

    items["GRC-G-MORF-DIATH-INTRO"] = [
        {
            "id": "ITEM-GRC-G-MORF-DIATH-INTRO-001",
            "node_ids": ["GRC-G-MORF-DIATH-INTRO"],
            "type": "herkenning",
            "direction": "receptief",
            "difficulty_initial": -0.4,
            "discrimination_initial": 1.0,
            "expected_time_sec": 12,
            "stimulus": "Welke drie diathesen kent het Grieks?",
            "answer": [
                "activum, medium, passivum",
                "actief, medium, passief",
            ],
            "feedback": "Het Grieks kent drie diathesen (genera verbi): activum, medium en passivum. Het medium ontbreekt in het Latijn.",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-DIATH-INTRO-002",
            "node_ids": ["GRC-G-MORF-DIATH-INTRO"],
            "type": "herkenning",
            "direction": "receptief",
            "difficulty_initial": 0.2,
            "discrimination_initial": 1.2,
            "expected_time_sec": 18,
            "stimulus": "Waarom vallen medium en passivum in het praesens formeel samen?",
            "answer": [
                "omdat ze in praesens, imperfectum en perfectum dezelfde uitgangen delen",
                "de vormen zijn identiek; pas in aoristus/futurum verschillen ze",
            ],
            "feedback": "In praesens, imperfectum en perfectum delen medium en passivum dezelfde vormen. Alleen in aoristus en futurum krijgen ze aparte uitgangen.",
            "source": "handmatig",
        },
    ]

    items["GRC-G-MORF-LIDW-INTRO"] = [
        {
            "id": "ITEM-GRC-G-MORF-LIDW-INTRO-001",
            "node_ids": ["GRC-G-MORF-LIDW-INTRO"],
            "type": "herkenning",
            "direction": "receptief",
            "difficulty_initial": -0.8,
            "discrimination_initial": 1.0,
            "expected_time_sec": 10,
            "stimulus": "Geef de drie nominatief singularis-vormen van het bepaald lidwoord.",
            "answer": [
                "ὁ, ἡ, τό",
                "ὁ ἡ τό",
            ],
            "feedback": "Nom. sg. van het bepaald lidwoord: ὁ (m.), ἡ (f.), τό (n.). Er is geen onbepaald lidwoord in het Grieks.",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-LIDW-INTRO-002",
            "node_ids": ["GRC-G-MORF-LIDW-INTRO"],
            "type": "herkenning",
            "direction": "receptief",
            "difficulty_initial": -0.3,
            "discrimination_initial": 1.2,
            "expected_time_sec": 15,
            "stimulus": "Heeft het Grieks een onbepaald lidwoord (zoals Nederlands 'een')?",
            "answer": ["nee", "geen"],
            "feedback": "Het Grieks kent geen onbepaald lidwoord. Een los substantief zonder bepaald lidwoord is meestal onbepaald: ἄνθρωπος = 'een mens'.",
            "source": "handmatig",
        },
    ]

    items["GRC-G-MORF-LIDW-VERBG"] = [
        {
            "id": "ITEM-GRC-G-MORF-LIDW-VERBG-001",
            "node_ids": ["GRC-G-MORF-LIDW-VERBG"],
            "type": "productie",
            "direction": "productief",
            "difficulty_initial": 0.0,
            "discrimination_initial": 1.2,
            "expected_time_sec": 20,
            "stimulus": "Geef de genitivus pluralis van het lidwoord voor alle drie de genera.",
            "answer": [
                "τῶν",
                "τῶν, τῶν, τῶν",
            ],
            "feedback": "Gen. pl. is voor alle drie de genera τῶν. In de gen. en dat. pluralis vallen m./f./n. samen.",
            "source": "handmatig",
        },
        {
            "id": "ITEM-GRC-G-MORF-LIDW-VERBG-002",
            "node_ids": ["GRC-G-MORF-LIDW-VERBG"],
            "type": "productie",
            "direction": "productief",
            "difficulty_initial": 0.4,
            "discrimination_initial": 1.2,
            "expected_time_sec": 25,
            "stimulus": "Geef het lidwoord dat hoort bij ἀνθρώπῳ.",
            "answer": "τῷ",
            "feedback": "ἀνθρώπῳ is dat. sg. m. → lidwoord τῷ. De iota subscriptum onder de ω is typisch voor dat. sg. in de 2e declinatie.",
            "source": "handmatig",
        },
    ]

    return items


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------


def collect_all() -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {}
    out.update(naamval_numerus_genus())
    out.update(declinatie_conj_tempus())
    out.update(persoon_them_stamtijd())
    out.update(uit_diath_lidw())
    return out


def validate_all(items_by_node: dict[str, list[dict]]) -> None:
    for _node_id, item_list in items_by_node.items():
        for item_dict in item_list:
            Item(**item_dict)
    total = sum(len(v) for v in items_by_node.values())
    print(f"All {total} items validated.")


def add_items_to_json(json_path: Path, items_by_node: dict[str, list[dict]]) -> int:
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
    total = sum(len(v) for v in items_by_node.values())
    type_counter: Counter[str] = Counter()
    richting_counter: Counter[str] = Counter()
    for item_list in items_by_node.values():
        for item in item_list:
            type_counter[item["type"]] += 1
            richting_counter[item["direction"]] += 1

    print("\n=== E3-02 Summary ===")
    print(f"Knopen: {len(items_by_node)}")
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

    items_by_node = collect_all()
    validate_all(items_by_node)
    print_summary(items_by_node)

    if args.dry_run:
        print("\nDry-run: geen wijzigingen geschreven.")
        return

    path = Path(__file__).parent.parent / "data" / "graph" / "grc_grammatica_leerjaar1.json"
    added = add_items_to_json(path, items_by_node)
    print(f"\nAdded {added} items to {path.name}")


if __name__ == "__main__":
    main()
