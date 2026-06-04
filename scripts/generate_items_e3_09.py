#!/usr/bin/env python3
"""Generate exercise items for E3-09: GRC aoristus indicativus actief.

Target: data/graph/grc_grammatica_leerjaar1.json
Scope:  9 nodes: AOR-INTRO, AOR-SIGMA, AOR-UIT, AOR-THEM, AOR-ROOT,
        AOR-LIJST, INF-AOR, AOR-PARAD en SYNT-AOR-ASPECT.

Drie componenten:
1. Stamtijden-herkenning — gegeven aoristus-vorm → lemma en aoristype
   (sigmatisch ἔλυσα of thematisch ἔλαβον).
2. Productie van aoristus-vormen met secundaire/specifieke uitgangen.
3. Aspectueel verschil aoristus vs. imperfectum (≥5 items).

Run:
    python scripts/generate_items_e3_09.py            # writes items to graph
    python scripts/generate_items_e3_09.py --dry-run  # only validate + print
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
# 1. AOR-INTRO — 3 items
# ---------------------------------------------------------------------------


def aor_intro_items() -> list[dict]:
    return [
        {
            "id": "ITEM-GRC-G-MORF-AOR-INTRO-001",
            "node_ids": ["GRC-G-MORF-AOR-INTRO"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": -0.4,
            "discrimination_initial": 1.1,
            "expected_time_sec": 15,
            "stimulus": "Welk aspect drukt de aoristus uit?",
            "answer": [
                "eenmalige of afgeronde handeling",
                "punctueel / perfectief",
            ],
            "feedback": "De aoristus is punctueel: de handeling wordt als één afgeronde gebeurtenis gezien. Tegenhanger: imperfectum (duur/herhaling).",
            "source": "manual",
        },
        {
            "id": "ITEM-GRC-G-MORF-AOR-INTRO-002",
            "node_ids": ["GRC-G-MORF-AOR-INTRO"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": -0.2,
            "discrimination_initial": 1.2,
            "expected_time_sec": 15,
            "stimulus": "Welke twee hoofdtypen aoristus onderscheiden we in leerjaar 1?",
            "answer": [
                "sigmatisch (zwak) en thematisch (sterk)",
                "sigmatisch en thematisch",
            ],
            "feedback": "Sigmatisch/zwak: stam + σ + α-uitgangen (ἔλυσα). Thematisch/sterk: eigen aoriststam + thematische klinker + secundaire uitgangen (ἔλαβον).",
            "source": "manual",
        },
        {
            "id": "ITEM-GRC-G-MORF-AOR-INTRO-003",
            "node_ids": ["GRC-G-MORF-AOR-INTRO"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": 0.1,
            "discrimination_initial": 1.2,
            "expected_time_sec": 15,
            "stimulus": "Uit welke drie ingrediënten bestaat elke aoristusvorm?",
            "answer": [
                "augment + aoriststam + persoonsuitgang",
                "augment, aoriststam, uitgang",
            ],
            "feedback": "Aoristus = augment (ἐ-/klinkerverlenging) + aoriststam (σ-stam of eigen stam) + uitgang (α-uitgangen bij sigm., secundair bij them.).",
            "source": "manual",
        },
    ]


# ---------------------------------------------------------------------------
# 2. AOR-SIGMA — 5 items (ἔλυσα paradigma)
# ---------------------------------------------------------------------------


def aor_sigma_items() -> list[dict]:
    rows = [
        ("1 sg.", "ἔλυσα", "ik maakte los", -0.2),
        ("2 sg.", "ἔλυσας", "jij maakte los", 0.1),
        ("3 sg.", "ἔλυσε(ν)", "hij/zij maakte los", 0.1),
        ("1 pl.", "ἐλύσαμεν", "wij maakten los", 0.3),
    ]
    items: list[dict] = []
    for idx, (label, form, nl, diff) in enumerate(rows, start=1):
        items.append(
            {
                "id": f"ITEM-GRC-G-MORF-AOR-SIGMA-{idx:03d}",
                "node_ids": ["GRC-G-MORF-AOR-SIGMA"],
                "type": "production",
                "direction": "productive",
                "difficulty_initial": diff,
                "discrimination_initial": 1.2,
                "expected_time_sec": 25,
                "stimulus": f"Geef de {label} aoristus ind. act. van λύω.",
                "answer": [form, form.replace("(ν)", "")] if "(ν)" in form else form,
                "feedback": f"{label} = {form} ({nl}). Augment ἐ- + stam λυ- + σ + α-uitgang.",
                "source": "manual",
            }
        )
    items.append(
        {
            "id": "ITEM-GRC-G-MORF-AOR-SIGMA-005",
            "node_ids": ["GRC-G-MORF-AOR-SIGMA"],
            "type": "production",
            "direction": "productive",
            "difficulty_initial": 0.5,
            "discrimination_initial": 1.3,
            "expected_time_sec": 25,
            "stimulus": "Geef de 1 sg. sigmatische aoristus van γράφω.",
            "answer": "ἔγραψα",
            "feedback": "γράφω → ἔγραψα: φ + σ → ψ. Bij labiaalstammen (π/β/φ) smelt de σ-aorist de stamconsonant tot ψ.",
            "source": "manual",
        }
    )
    return items


# ---------------------------------------------------------------------------
# 3. AOR-UIT — 2 items
# ---------------------------------------------------------------------------


def aor_uit_items() -> list[dict]:
    return [
        {
            "id": "ITEM-GRC-G-MORF-AOR-UIT-001",
            "node_ids": ["GRC-G-MORF-AOR-UIT"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": 0.0,
            "discrimination_initial": 1.1,
            "expected_time_sec": 15,
            "stimulus": "Noem de zes uitgangen van de sigmatische aoristus actief.",
            "answer": [
                "-α, -ας, -ε(ν), -αμεν, -ατε, -αν",
                "-α -ας -ε -αμεν -ατε -αν",
            ],
            "feedback": "Sigmatische uitgangen: -α, -ας, -ε(ν), -αμεν, -ατε, -αν. Let op: 1 sg. op -α (niet -ον); 3 sg. op -ε (niet -ε van impf.).",
            "source": "manual",
        },
        {
            "id": "ITEM-GRC-G-MORF-AOR-UIT-002",
            "node_ids": ["GRC-G-MORF-AOR-UIT"],
            "type": "analysis",
            "direction": "receptive",
            "difficulty_initial": 0.3,
            "discrimination_initial": 1.3,
            "expected_time_sec": 20,
            "stimulus": "Welke uitgangen heeft een thematische (sterke) aoristus — sigmatisch of secundair?",
            "answer": [
                "secundaire uitgangen (-ον, -ες, -ε(ν), -ομεν, -ετε, -ον)",
                "secundair, zoals imperfectum",
            ],
            "feedback": "Thematische aoristus gebruikt de secundaire uitgangen (impf.-stijl) op een ándere stam: ἔλαβον lijkt op ἔγραφον qua uitgang.",
            "source": "manual",
        },
    ]


# ---------------------------------------------------------------------------
# 4. AOR-THEM — 4 items (ἔλαβον)
# ---------------------------------------------------------------------------


def aor_them_items() -> list[dict]:
    rows = [
        ("1 sg.", "ἔλαβον", "ik nam / pakte", 0.0),
        ("2 sg.", "ἔλαβες", "jij nam", 0.2),
        ("3 pl.", "ἔλαβον", "zij namen", 0.3),
    ]
    items: list[dict] = []
    for idx, (label, form, nl, diff) in enumerate(rows, start=1):
        items.append(
            {
                "id": f"ITEM-GRC-G-MORF-AOR-THEM-{idx:03d}",
                "node_ids": ["GRC-G-MORF-AOR-THEM"],
                "type": "production",
                "direction": "productive",
                "difficulty_initial": diff,
                "discrimination_initial": 1.2,
                "expected_time_sec": 25,
                "stimulus": f"Geef de {label} thematische aoristus ind. act. van λαμβάνω.",
                "answer": form,
                "feedback": f"{label} = {form} ({nl}). Aoriststam λαβ- (niet λαμβαν-!) + augment + secundaire uitgangen.",
                "source": "manual",
            }
        )
    items.append(
        {
            "id": "ITEM-GRC-G-MORF-AOR-THEM-004",
            "node_ids": ["GRC-G-MORF-AOR-THEM"],
            "type": "analysis",
            "direction": "receptive",
            "difficulty_initial": 0.5,
            "discrimination_initial": 1.3,
            "expected_time_sec": 20,
            "stimulus": "Wat onderscheidt ἔλαβον van een imperfectum van hetzelfde werkwoord?",
            "answer": [
                "ἔλαβον heeft de aoriststam λαβ-; imperf. gebruikt de praesensstam λαμβαν-",
                "de stam: λαβ- (aorist) vs. λαμβαν- (praesens/impf.)",
            ],
            "feedback": "ἐλάμβανον (impf.) < λαμβαν- + secundair. ἔλαβον (aorist) < λαβ- + secundair. Zelfde uitgang, andere stam → ander aspect.",
            "source": "manual",
        }
    )
    return items


# ---------------------------------------------------------------------------
# 5. AOR-ROOT — 2 items (stamaoristi)
# ---------------------------------------------------------------------------


def aor_root_items() -> list[dict]:
    return [
        {
            "id": "ITEM-GRC-G-MORF-AOR-ROOT-001",
            "node_ids": ["GRC-G-MORF-AOR-ROOT"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": 0.3,
            "discrimination_initial": 1.2,
            "expected_time_sec": 15,
            "stimulus": "Wat kenmerkt een stamaoristus zoals ἔβην of ἔστην?",
            "answer": [
                "geen thematische klinker; uitgangen direct aan de kale stam",
                "athematisch: stam + uitgang zonder ε/ο",
            ],
            "feedback": "Stamaoristi (ἔβην van βαίνω, ἔστην van ἵστημι, ἔγνων van γιγνώσκω) hebben geen thematische klinker: uitgang plakt direct aan de stam.",
            "source": "manual",
        },
        {
            "id": "ITEM-GRC-G-MORF-AOR-ROOT-002",
            "node_ids": ["GRC-G-MORF-AOR-ROOT"],
            "type": "production",
            "direction": "productive",
            "difficulty_initial": 0.6,
            "discrimination_initial": 1.3,
            "expected_time_sec": 25,
            "stimulus": "Welk lemma hoort bij ἔγνων (1 sg. stamaorist, 'ik leerde kennen')?",
            "answer": [
                "γιγνώσκω",
                "γιγνώσκω, -γνώσομαι, -ἔγνων",
            ],
            "feedback": "ἔγνων is 1 sg. stamaorist van γιγνώσκω. Aoriststam γνω- (zonder thematische klinker, met lange ω).",
            "source": "manual",
        },
    ]


# ---------------------------------------------------------------------------
# 6. AOR-LIJST — 4 items (stamtijden-herkenning: aor-vorm → lemma + type)
# ---------------------------------------------------------------------------


def aor_lijst_items() -> list[dict]:
    rows = [
        ("εἶπον", "λέγω", "thematisch", "zeggen", 0.3),
        ("ἦλθον", "ἔρχομαι", "thematisch", "gaan, komen", 0.4),
        ("εἶδον", "ὁράω", "thematisch", "zien", 0.4),
        ("ἔλυσα", "λύω", "sigmatisch", "losmaken", 0.1),
    ]
    items: list[dict] = []
    for idx, (form, lemma, typ, nl, diff) in enumerate(rows, start=1):
        items.append(
            {
                "id": f"ITEM-GRC-G-MORF-AOR-LIJST-{idx:03d}",
                "node_ids": ["GRC-G-MORF-AOR-LIJST", "GRC-G-MORF-STAMTIJD"],
                "type": "recognition",
                "direction": "receptive",
                "difficulty_initial": diff,
                "discrimination_initial": 1.3,
                "expected_time_sec": 20,
                "stimulus": f"Van welk lemma is {form} de 1 sg. aoristus, en welk aoristype is het?",
                "answer": [
                    f"{lemma}, {typ}",
                    f"lemma: {lemma}; type: {typ}",
                ],
                "feedback": f"{form} = 1 sg. aorist ({typ}) van {lemma} ('{nl}'). De aoriststam staat los van de praesensstam.",
                "source": "manual",
            }
        )
    return items


# ---------------------------------------------------------------------------
# 7. INF-AOR — 2 items
# ---------------------------------------------------------------------------


def inf_aor_items() -> list[dict]:
    return [
        {
            "id": "ITEM-GRC-G-MORF-INF-AOR-001",
            "node_ids": ["GRC-G-MORF-INF-AOR"],
            "type": "production",
            "direction": "productive",
            "difficulty_initial": 0.3,
            "discrimination_initial": 1.2,
            "expected_time_sec": 20,
            "stimulus": "Geef de infinitief aoristus actief van λύω.",
            "answer": "λῦσαι",
            "feedback": "Sigmatische inf. aor. = λῦσαι (stam λυ- + σ + -αι). Geen augment in infinitief (augment blijft bij de indicatief).",
            "source": "manual",
        },
        {
            "id": "ITEM-GRC-G-MORF-INF-AOR-002",
            "node_ids": ["GRC-G-MORF-INF-AOR"],
            "type": "production",
            "direction": "productive",
            "difficulty_initial": 0.5,
            "discrimination_initial": 1.3,
            "expected_time_sec": 25,
            "stimulus": "Geef de infinitief aoristus actief van λαμβάνω.",
            "answer": "λαβεῖν",
            "feedback": "Thematische inf. aor. = λαβεῖν (aoriststam λαβ- + -εῖν). Kenmerkende circumflex op de ultima.",
            "source": "manual",
        },
    ]


# ---------------------------------------------------------------------------
# 8. AOR-PARAD — 3 items
# ---------------------------------------------------------------------------


def aor_parad_items() -> list[dict]:
    return [
        {
            "id": "ITEM-GRC-G-MORF-AOR-PARAD-001",
            "node_ids": ["GRC-G-MORF-AOR-PARAD"],
            "type": "offline_writing",
            "direction": "productive",
            "difficulty_initial": 0.7,
            "discrimination_initial": 1.3,
            "expected_time_sec": 100,
            "stimulus": "Schrijf het volledige paradigma van ἔλυσα op (6 personen) en vergelijk met je grammaticaboek.",
            "answer": "ἔλυσα, ἔλυσας, ἔλυσε(ν), ἐλύσαμεν, ἐλύσατε, ἔλυσαν",
            "feedback": "Kern: augment ἐ- + stam λυ- + σ + α-uitgangen. Zes vormen: ἔλυσα / ἔλυσας / ἔλυσε(ν) / ἐλύσαμεν / ἐλύσατε / ἔλυσαν.",
            "source": "manual",
            "verification_method": "self_report",
            "expected_result": "6 vormen van ἔλυσα met correcte accenten en bewegelijke ν in de 3 sg.",
        },
        {
            "id": "ITEM-GRC-G-MORF-AOR-PARAD-002",
            "node_ids": ["GRC-G-MORF-AOR-PARAD", "GRC-G-MORF-STAMTIJD"],
            "type": "analysis",
            "direction": "receptive",
            "difficulty_initial": 0.6,
            "discrimination_initial": 1.3,
            "expected_time_sec": 25,
            "stimulus": "Bij welk lemma hoort ἤνεγκον en welk aoristype is het?",
            "answer": [
                "φέρω, thematisch (onregelmatig)",
                "lemma: φέρω; type: thematisch",
            ],
            "feedback": "ἤνεγκον is 1 sg. (suppletieve) thematische aorist van φέρω ('dragen/brengen'). Sterk onregelmatig, moet uit het hoofd geleerd.",
            "source": "manual",
        },
        {
            "id": "ITEM-GRC-G-MORF-AOR-PARAD-003",
            "node_ids": ["GRC-G-MORF-AOR-PARAD"],
            "type": "contextual",
            "direction": "receptive",
            "difficulty_initial": 0.5,
            "discrimination_initial": 1.3,
            "expected_time_sec": 25,
            "stimulus": "In 'ὁ διδάσκαλος ἔγραψε τὸν λόγον' — welke tijd, persoon en getal heeft ἔγραψε?",
            "answer": [
                "aoristus 3e persoon singularis",
                "aor. 3 sg.",
            ],
            "feedback": "ἔγραψε = 3 sg. sigm. aorist van γράφω (augment ἐ- + stam γραφ- + σ → γραψ- + -ε). Punctueel: 'schreef één keer' — tegenover impf. 'was aan het schrijven'.",
            "source": "manual",
        },
    ]


# ---------------------------------------------------------------------------
# 9. SYNT-AOR-ASPECT — 5 items (aspectueel verschil)
# ---------------------------------------------------------------------------


def aspect_items() -> list[dict]:
    return [
        {
            "id": "ITEM-GRC-G-SYNT-AOR-ASPECT-001",
            "node_ids": ["GRC-G-SYNT-AOR-ASPECT"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": -0.1,
            "discrimination_initial": 1.2,
            "expected_time_sec": 15,
            "stimulus": "Wat is het aspectueel verschil tussen aoristus en imperfectum?",
            "answer": [
                "aoristus = punctueel/afgerond; imperfectum = duratief/herhaald",
                "aorist punctueel, imperfectum duratief",
            ],
            "feedback": "Beide zijn verleden tijd, maar verschillen in aspect: aoristus noemt één afgeronde gebeurtenis, imperfectum beschrijft een lopende of herhaalde handeling.",
            "source": "manual",
        },
        {
            "id": "ITEM-GRC-G-SYNT-AOR-ASPECT-002",
            "node_ids": ["GRC-G-SYNT-AOR-ASPECT"],
            "type": "contextual",
            "direction": "receptive",
            "difficulty_initial": 0.3,
            "discrimination_initial": 1.3,
            "expected_time_sec": 25,
            "stimulus": "Welke tijd zou je kiezen voor 'hij schreef (één keer) een brief': aoristus of imperfectum?",
            "answer": ["aoristus", "aorist"],
            "feedback": "Eenmalige, afgeronde actie → aoristus: ἔγραψε ἐπιστολήν. Het imperfectum (ἔγραφε) zou suggereren 'hij was aan het schrijven'.",
            "source": "manual",
        },
        {
            "id": "ITEM-GRC-G-SYNT-AOR-ASPECT-003",
            "node_ids": ["GRC-G-SYNT-AOR-ASPECT"],
            "type": "contextual",
            "direction": "receptive",
            "difficulty_initial": 0.3,
            "discrimination_initial": 1.3,
            "expected_time_sec": 25,
            "stimulus": "Welke tijd past bij 'iedere dag offerde zij aan de goden': aoristus of imperfectum?",
            "answer": ["imperfectum", "impf."],
            "feedback": "Herhaalde handeling in het verleden → imperfectum: ἔθυεν τοῖς θεοῖς. Aoristus zou één specifieke offermoment noemen.",
            "source": "manual",
        },
        {
            "id": "ITEM-GRC-G-SYNT-AOR-ASPECT-004",
            "node_ids": ["GRC-G-SYNT-AOR-ASPECT"],
            "type": "contextual",
            "direction": "receptive",
            "difficulty_initial": 0.4,
            "discrimination_initial": 1.3,
            "expected_time_sec": 25,
            "stimulus": "Vertaal het aspectueel verschil: 'ὁ ἄνθρωπος ἔλεγε' vs. 'ὁ ἄνθρωπος εἶπε'.",
            "answer": [
                "ἔλεγε = hij was aan het spreken / sprak (telkens); εἶπε = hij zei (één keer)",
                "impf. durend, aorist eenmalig",
            ],
            "feedback": "ἔλεγε (impf.) = duratief 'hij sprak / was aan het spreken'. εἶπε (aor.) = punctueel 'hij zei/sprak (één keer)'. Zelfde werkwoord, verschillend aspect.",
            "source": "manual",
        },
        {
            "id": "ITEM-GRC-G-SYNT-AOR-ASPECT-005",
            "node_ids": ["GRC-G-SYNT-AOR-ASPECT"],
            "type": "analysis",
            "direction": "receptive",
            "difficulty_initial": 0.5,
            "discrimination_initial": 1.3,
            "expected_time_sec": 25,
            "stimulus": "Waarom is de keuze tussen aoristus en imperfectum niet alleen een kwestie van 'wanneer', maar vooral van 'hoe'?",
            "answer": [
                "beide zijn verleden tijd; het verschil zit in het aspect (perfectief vs. imperfectief)",
                "de aspectkeuze betreft de manier waarop de spreker de handeling ziet",
            ],
            "feedback": "Tempus (verleden) is bij beide gelijk. De spreker kiest het aspect: wil hij de handeling als één punt zien (aor.) of als proces/herhaling (impf.)?",
            "source": "manual",
        },
    ]


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------


def collect_all() -> dict[str, list[dict]]:
    all_items: list[dict] = []
    all_items.extend(aor_intro_items())
    all_items.extend(aor_sigma_items())
    all_items.extend(aor_uit_items())
    all_items.extend(aor_them_items())
    all_items.extend(aor_root_items())
    all_items.extend(aor_lijst_items())
    all_items.extend(inf_aor_items())
    all_items.extend(aor_parad_items())
    all_items.extend(aspect_items())

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

    print("\n=== E3-09 Summary ===")
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
