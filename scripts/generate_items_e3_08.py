#!/usr/bin/env python3
"""Generate exercise items for E3-08: GRC imperfectum indicativus actief.

Target: data/graph/grc_grammatica_leerjaar1.json
Scope:  7 nodes: IMPF-INTRO, AUGMENT, IMPF-THEM, IMPF-CTA, IMPF-CTE,
        IMPF-EIMI, IMPF-PARAD.

Focus:
- Augment-items: van gegeven praesens → juiste imperfectum-vorm.
- Temporeel augment (α→η, ε→η, ο→ω) expliciet getoetst (≥5 items).
- Secundaire uitgangen (-ον, -ες, -ε, -ομεν, -ετε, -ον) in alle 6 personen.
- Imperfectum van contracta τιμάω en ποιέω.
- Imperfectum van εἰμί (ἦν, ἦσθα, ἦν, ἦμεν, ἦτε, ἦσαν) als eigen cluster.

Run:
    python scripts/generate_items_e3_08.py            # writes items to graph
    python scripts/generate_items_e3_08.py --dry-run  # only validate + print
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
# 1. IMPF-INTRO — 3 items
# ---------------------------------------------------------------------------


def impf_intro_items() -> list[dict]:
    return [
        {
            "id": "ITEM-GRC-G-MORF-IMPF-INTRO-001",
            "node_ids": ["GRC-G-MORF-IMPF-INTRO"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": -0.5,
            "discrimination_initial": 1.1,
            "expected_time_sec": 15,
            "stimulus": "Welk aspect drukt het imperfectum uit?",
            "answer": [
                "duur of herhaling in het verleden",
                "durende/herhalende handeling in het verleden",
            ],
            "feedback": "Het imperfectum drukt een durende of herhaalde verleden handeling uit. Tegenhanger is de aoristus (eenmalig, afgerond).",
            "source": "manual",
        },
        {
            "id": "ITEM-GRC-G-MORF-IMPF-INTRO-002",
            "node_ids": ["GRC-G-MORF-IMPF-INTRO"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": -0.3,
            "discrimination_initial": 1.2,
            "expected_time_sec": 15,
            "stimulus": "Uit welke drie ingrediënten bestaat een imperfectum-vorm?",
            "answer": [
                "augment + praesensstam + secundaire uitgang",
                "augment, praesensstam, secundaire persoonsuitgang",
            ],
            "feedback": "Imperfectum = augment (ἐ-/klinkerverlenging) + praesensstam + secundaire uitgang (-ον, -ες, -ε, -ομεν, -ετε, -ον).",
            "source": "manual",
        },
        {
            "id": "ITEM-GRC-G-MORF-IMPF-INTRO-003",
            "node_ids": ["GRC-G-MORF-IMPF-INTRO"],
            "type": "analysis",
            "direction": "receptive",
            "difficulty_initial": 0.3,
            "discrimination_initial": 1.3,
            "expected_time_sec": 25,
            "stimulus": "Splits ἐλύομεν in augment + stam + thematische klinker + uitgang.",
            "answer": ["ἐ-λυ-ο-μεν", "ἐ + λυ + ο + μεν"],
            "feedback": "ἐ- (syllabisch augment) + λυ- (stam) + -ο- (thematisch) + -μεν (secundaire uitgang 1 pl.). Vergelijk praesens λύ-ο-μεν.",
            "source": "manual",
        },
    ]


# ---------------------------------------------------------------------------
# 2. AUGMENT — 7 items (2 syllabisch + 5 temporeel)
# ---------------------------------------------------------------------------


def augment_items() -> list[dict]:
    items: list[dict] = []

    items.append(
        {
            "id": "ITEM-GRC-G-MORF-AUGMENT-001",
            "node_ids": ["GRC-G-MORF-AUGMENT"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": -0.3,
            "discrimination_initial": 1.1,
            "expected_time_sec": 15,
            "stimulus": "Wanneer krijgt een werkwoord een syllabisch augment?",
            "answer": [
                "als de stam met een medeklinker begint",
                "bij consonant-initiële werkwoorden",
            ],
            "feedback": "Syllabisch augment ἐ- wordt geplakt vóór een medeklinker-stam: λύω → ἔλυον, γράφω → ἔγραφον.",
            "source": "manual",
        }
    )
    items.append(
        {
            "id": "ITEM-GRC-G-MORF-AUGMENT-002",
            "node_ids": ["GRC-G-MORF-AUGMENT"],
            "type": "production",
            "direction": "productive",
            "difficulty_initial": 0.2,
            "discrimination_initial": 1.2,
            "expected_time_sec": 20,
            "stimulus": "Geef de 1 sg. imperfectum van γράφω (praesens 'ik schrijf').",
            "answer": "ἔγραφον",
            "feedback": "γράφω → ἔγραφον: syllabisch augment ἐ- vóór γ, secundaire uitgang -ον (1 sg.). 'Ik was aan het schrijven'.",
            "source": "manual",
        }
    )

    # Temporeel-augment items: ≥5.
    temp_rows = [
        ("ἀκούω", "ἤκουον", "α → η", "ik hoorde"),
        ("ἐθέλω", "ἤθελον", "ε → η", "ik wilde"),
        ("ἄρχω", "ἦρχον", "α → η", "ik heerste / begon"),
        ("ὀνομάζω", "ὠνόμαζον", "ο → ω", "ik noemde"),
    ]
    for idx, (praes, impf, rule, nl) in enumerate(temp_rows, start=3):
        items.append(
            {
                "id": f"ITEM-GRC-G-MORF-AUGMENT-{idx:03d}",
                "node_ids": ["GRC-G-MORF-AUGMENT"],
                "type": "production",
                "direction": "productive",
                "difficulty_initial": 0.5,
                "discrimination_initial": 1.3,
                "expected_time_sec": 25,
                "stimulus": f"Geef de 1 sg. imperfectum van {praes}.",
                "answer": impf,
                "feedback": f"{praes} → {impf} ({nl}). Temporeel augment: {rule}. Vowelstam krijgt geen ἐ-, maar een verlenging.",
                "source": "manual",
            }
        )

    # Concept-item over temporeel augment + kort quizvraag.
    items.append(
        {
            "id": "ITEM-GRC-G-MORF-AUGMENT-007",
            "node_ids": ["GRC-G-MORF-AUGMENT"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": 0.2,
            "discrimination_initial": 1.2,
            "expected_time_sec": 15,
            "stimulus": "Tot welke klinkers verlengen initiële α, ε en ο bij temporeel augment?",
            "answer": [
                "α → η, ε → η, ο → ω",
                "α→η, ε→η, ο→ω",
            ],
            "feedback": "Temporeel augment: α → η, ε → η, ο → ω. Lange klinkers (η, ω) en diftongen blijven meestal onveranderd (ηὐξάνομεν, niet ἤυξάνομεν).",
            "source": "manual",
        }
    )

    return items


# ---------------------------------------------------------------------------
# 3. IMPF-THEM — 7 items (6 vormen + 1 analyse)
# ---------------------------------------------------------------------------


def impf_them_items() -> list[dict]:
    rows = [
        ("1 sg.", "ἔλυον", "ik maakte los / was aan het losmaken", -0.3),
        ("2 sg.", "ἔλυες", "jij maakte los", 0.0),
        ("3 sg.", "ἔλυε(ν)", "hij/zij maakte los", 0.0),
        ("1 pl.", "ἐλύομεν", "wij maakten los", 0.2),
        ("2 pl.", "ἐλύετε", "jullie maakten los", 0.3),
        ("3 pl.", "ἔλυον", "zij maakten los", 0.3),
    ]
    items: list[dict] = []
    for idx, (label, form, nl, diff) in enumerate(rows, start=1):
        items.append(
            {
                "id": f"ITEM-GRC-G-MORF-IMPF-THEM-{idx:03d}",
                "node_ids": ["GRC-G-MORF-IMPF-THEM"],
                "type": "production",
                "direction": "productive",
                "difficulty_initial": diff,
                "discrimination_initial": 1.2,
                "expected_time_sec": 25,
                "stimulus": f"Geef de {label} imperfectum ind. act. van λύω.",
                "answer": [form, form.replace("(ν)", "")] if "(ν)" in form else form,
                "feedback": f"{label} = {form} ({nl}). Augment ἐ- + stam λυ- + thematische klinker + secundaire uitgang.",
                "source": "manual",
            }
        )

    items.append(
        {
            "id": "ITEM-GRC-G-MORF-IMPF-THEM-007",
            "node_ids": ["GRC-G-MORF-IMPF-THEM"],
            "type": "analysis",
            "direction": "receptive",
            "difficulty_initial": 0.3,
            "discrimination_initial": 1.2,
            "expected_time_sec": 20,
            "stimulus": "Waarom zijn de 1 sg. en de 3 pl. imperfectum vaak identiek (ἔλυον)?",
            "answer": [
                "omdat beide de secundaire uitgang -ον hebben",
                "secundaire uitgang -ον voor 1 sg. én 3 pl.",
            ],
            "feedback": "Beide eindigen op -ον: 1 sg. stam + -ον, 3 pl. stam + -ον. Alleen context of onderwerp beslist welke functie de vorm heeft.",
            "source": "manual",
        }
    )

    return items


# ---------------------------------------------------------------------------
# 4. IMPF-CTA — 4 items (τιμάω)
# ---------------------------------------------------------------------------


def impf_cta_items() -> list[dict]:
    rows = [
        ("1 sg.", "τιμά-ον", "ἐτίμων", "α+ο → ω"),
        ("3 sg.", "τιμά-ε(ν)", "ἐτίμα", "α+ε → ᾱ"),
        ("1 pl.", "τιμά-ομεν", "ἐτιμῶμεν", "α+ο → ω (circumflex)"),
    ]
    items: list[dict] = []
    for idx, (label, pre, post, rule) in enumerate(rows, start=1):
        items.append(
            {
                "id": f"ITEM-GRC-G-MORF-IMPF-CTA-{idx:03d}",
                "node_ids": ["GRC-G-MORF-IMPF-CTA"],
                "type": "production",
                "direction": "productive",
                "difficulty_initial": 0.6,
                "discrimination_initial": 1.3,
                "expected_time_sec": 30,
                "stimulus": f"Geef de {label} imperfectum ind. act. van τιμάω (voor-contractie: ἐ-{pre}).",
                "answer": post,
                "feedback": f"ἐ-{pre} → {post}. Syllabisch augment ἐ- + contractie {rule}.",
                "source": "manual",
            }
        )
    items.append(
        {
            "id": "ITEM-GRC-G-MORF-IMPF-CTA-004",
            "node_ids": ["GRC-G-MORF-IMPF-CTA"],
            "type": "analysis",
            "direction": "receptive",
            "difficulty_initial": 0.5,
            "discrimination_initial": 1.3,
            "expected_time_sec": 20,
            "stimulus": "Welke persoon en welk getal heeft ἐτίμων?",
            "answer": [
                "1e persoon singularis of 3e persoon pluralis",
                "1 sg. of 3 pl.",
            ],
            "feedback": "ἐτίμων is 1 sg. óf 3 pl. imperfectum (identieke vormen wegens -ον in beide; na contractie α+ο → ω).",
            "source": "manual",
        }
    )
    return items


# ---------------------------------------------------------------------------
# 5. IMPF-CTE — 3 items (ποιέω)
# ---------------------------------------------------------------------------


def impf_cte_items() -> list[dict]:
    rows = [
        ("1 sg.", "ποιέ-ον", "ἐποίουν", "ε+ο → ου"),
        ("3 sg.", "ποιέ-ε(ν)", "ἐποίει", "ε+ε → ει"),
        ("1 pl.", "ποιέ-ομεν", "ἐποιοῦμεν", "ε+ο → ου (circumflex)"),
    ]
    items: list[dict] = []
    for idx, (label, pre, post, rule) in enumerate(rows, start=1):
        items.append(
            {
                "id": f"ITEM-GRC-G-MORF-IMPF-CTE-{idx:03d}",
                "node_ids": ["GRC-G-MORF-IMPF-CTE"],
                "type": "production",
                "direction": "productive",
                "difficulty_initial": 0.6,
                "discrimination_initial": 1.3,
                "expected_time_sec": 30,
                "stimulus": f"Geef de {label} imperfectum ind. act. van ποιέω (voor-contractie: ἐ-{pre}).",
                "answer": post,
                "feedback": f"ἐ-{pre} → {post}. Syllabisch augment ἐ- + contractie {rule}.",
                "source": "manual",
            }
        )
    return items


# ---------------------------------------------------------------------------
# 6. IMPF-EIMI — 4 items (ἦν, ἦσθα, ἦμεν, ἦσαν)
# ---------------------------------------------------------------------------


def impf_eimi_items() -> list[dict]:
    rows = [
        ("1 sg.", "ἦν", "ik was", -0.1),
        ("2 sg.", "ἦσθα", "jij was", 0.2),
        ("1 pl.", "ἦμεν", "wij waren", 0.2),
        ("3 pl.", "ἦσαν", "zij waren", 0.3),
    ]
    items: list[dict] = []
    for idx, (label, form, nl, diff) in enumerate(rows, start=1):
        items.append(
            {
                "id": f"ITEM-GRC-G-MORF-IMPF-EIMI-{idx:03d}",
                "node_ids": ["GRC-G-MORF-IMPF-EIMI"],
                "type": "production",
                "direction": "productive",
                "difficulty_initial": diff,
                "discrimination_initial": 1.2,
                "expected_time_sec": 20,
                "stimulus": f"Geef de {label} imperfectum van εἰμί ('{nl}').",
                "answer": form,
                "feedback": (
                    f"{label} = {form} ({nl}). Paradigma: ἦν, ἦσθα, ἦν, ἦμεν, ἦτε, ἦσαν. "
                    "Onregelmatig — geen zichtbaar augment, maar wel verleden-tijd-betekenis."
                ),
                "source": "manual",
            }
        )
    return items


# ---------------------------------------------------------------------------
# 7. IMPF-PARAD — 3 items (paradigma-drill)
# ---------------------------------------------------------------------------


def impf_parad_items() -> list[dict]:
    return [
        {
            "id": "ITEM-GRC-G-MORF-IMPF-PARAD-001",
            "node_ids": ["GRC-G-MORF-IMPF-PARAD"],
            "type": "offline_writing",
            "direction": "productive",
            "difficulty_initial": 0.7,
            "discrimination_initial": 1.3,
            "expected_time_sec": 100,
            "stimulus": "Schrijf het volledige paradigma van het imperfectum van λύω op (6 personen) en vergelijk met je grammaticaboek.",
            "answer": "ἔλυον, ἔλυες, ἔλυε(ν), ἐλύομεν, ἐλύετε, ἔλυον",
            "feedback": "Kern: augment ἐ- + stam λυ- + thematische klinker + secundaire uitgangen. 1 sg. = 3 pl. = ἔλυον.",
            "source": "manual",
            "verification_method": "self_report",
            "expected_result": "6 vormen van ἔλυον met correcte accenten en bewegelijke ν in de 3 sg.",
        },
        {
            "id": "ITEM-GRC-G-MORF-IMPF-PARAD-002",
            "node_ids": ["GRC-G-MORF-IMPF-PARAD"],
            "type": "contextual",
            "direction": "receptive",
            "difficulty_initial": 0.5,
            "discrimination_initial": 1.3,
            "expected_time_sec": 25,
            "stimulus": "In 'οἱ παῖδες ἔγραφον τοὺς λόγους' — welke tijd, persoon en getal heeft ἔγραφον?",
            "answer": [
                "imperfectum 3e persoon pluralis",
                "impf. 3 pl.",
            ],
            "feedback": "ἔγραφον = impf. 3 pl. (augment ἐ- + stam γραφ- + thematisch + -ον). Onderwerp οἱ παῖδες (nom. pl.) bepaalt 3 pl.",
            "source": "manual",
        },
        {
            "id": "ITEM-GRC-G-MORF-IMPF-PARAD-003",
            "node_ids": ["GRC-G-MORF-IMPF-PARAD"],
            "type": "analysis",
            "direction": "receptive",
            "difficulty_initial": 0.6,
            "discrimination_initial": 1.3,
            "expected_time_sec": 25,
            "stimulus": "Hoe herken je aan ἠκούομεν dat dit een imperfectum is?",
            "answer": [
                "temporeel augment (α → η) en secundaire uitgang -ομεν",
                "augment + secundaire uitgang",
            ],
            "feedback": "ἀκούω → ἠκούομεν: α → η (temporeel augment) + thematische ο + -μεν (secundaire 1 pl.). Praesens zou ἀκούομεν zijn.",
            "source": "manual",
        },
    ]


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------


def collect_all() -> dict[str, list[dict]]:
    all_items: list[dict] = []
    all_items.extend(impf_intro_items())
    all_items.extend(augment_items())
    all_items.extend(impf_them_items())
    all_items.extend(impf_cta_items())
    all_items.extend(impf_cte_items())
    all_items.extend(impf_eimi_items())
    all_items.extend(impf_parad_items())

    primary_map: dict[str, list[dict]] = {}
    for item in all_items:
        for key in ("stimulus", "antwoord", "feedback", "expected_result"):
            if key in item and item[key] is not None:
                item[key] = nfc(item[key])
        primary_map.setdefault(item["node_ids"][0], []).append(item)
    return primary_map


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
    per_node: Counter[str] = Counter()
    for node_id, item_list in items_by_node.items():
        per_node[node_id] = len(item_list)
        for item in item_list:
            type_counter[item["type"]] += 1

    print("\n=== E3-08 Summary ===")
    print(f"Knopen: {len(items_by_node)}")
    print(f"Total items: {total}")
    print("\nItems per node:")
    for k, c in per_node.most_common():
        print(f"  {k}: {c}")
    print("\nOefentype-verdeling:")
    for t, c in type_counter.most_common():
        print(f"  {t}: {c}")


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
