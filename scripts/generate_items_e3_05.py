#!/usr/bin/env python3
"""Generate exercise items for E3-05: GRC 3e declinatie (via adjectieven).

Target: data/graph/grc_grammatica_leerjaar1.json
Scope:  8 nodes rondom de 3e declinatie: DECL3-INTRO, DECL3-KONS,
        NOM-D3..VOC-D3 en DECL3-PARAD.

Instap via de Pallas/ARGO-route: adjectieven πᾶς, πᾶσα, πᾶν (stam παντ-,
ντ-stam) en σώφρων, σῶφρον (stam σωφρον-, asigmatische nominativus).
Dentaalstammen geïllustreerd via σῶμα, σώματος (n., stam σωματ-), de
sigmatische nominativus via φύλαξ, φύλακος (stam φυλακ- + σ → φύλαξ).

Focus: stamherkenning (stam uit gen. sg. -ος) en nom.sg.-uitzonderingen.
Elk sub-paradigma (πᾶς, σώφρων, σῶμα, φύλαξ) krijgt minstens 1 contextueel
item met vormherkenning in een korte zin.
Productie-antwoorden zijn polytonisch en NFC-genormaliseerd.

Run:
    python scripts/generate_items_e3_05.py            # writes items to graph
    python scripts/generate_items_e3_05.py --dry-run  # only validate + print
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
# Item definitions per node.
# ---------------------------------------------------------------------------


def intro_en_kons() -> dict[str, list[dict]]:
    """DECL3-INTRO (3) + DECL3-KONS (3) — 6 items."""
    items: dict[str, list[dict]] = {}

    items["GRC-G-MORF-DECL3-INTRO"] = [
        {
            "id": "ITEM-GRC-G-MORF-DECL3-INTRO-001",
            "node_ids": ["GRC-G-MORF-DECL3-INTRO"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": -0.4,
            "discrimination_initial": 1.0,
            "expected_time_sec": 12,
            "stimulus": "Op welke stamklasse is de 3e declinatie gebouwd?",
            "answer": [
                "medeklinkerstammen",
                "consonantstammen",
            ],
            "feedback": "De 3e declinatie bevat medeklinkerstammen. Nominativus varieert sterk (sigmatisch of asigmatisch); de stam blijkt pas uit de gen. sg. op -ος.",
            "source": "manual",
        },
        {
            "id": "ITEM-GRC-G-MORF-DECL3-INTRO-002",
            "node_ids": ["GRC-G-MORF-DECL3-INTRO"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": -0.1,
            "discrimination_initial": 1.2,
            "expected_time_sec": 15,
            "stimulus": "Hoe leid je de stam van een 3e-decl.-substantief af?",
            "answer": [
                "door -ος weg te halen van de gen. sg.",
                "gen. sg. min -ος",
            ],
            "feedback": "De stam blijkt uit de gen. sg. op -ος: σώματ-ος → stam σωματ-; πάντ-ος (gen. m.) → stam παντ-. De nominativus kan misleidend zijn.",
            "source": "manual",
        },
        {
            "id": "ITEM-GRC-G-MORF-DECL3-INTRO-003",
            "node_ids": ["GRC-G-MORF-DECL3-INTRO"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": 0.2,
            "discrimination_initial": 1.2,
            "expected_time_sec": 15,
            "stimulus": "Welke genera komen in de 3e declinatie voor?",
            "answer": [
                "alle drie: masculinum, femininum, neutrum",
                "m., f. en n.",
            ],
            "feedback": "Alle drie genera: πᾶς (m.), πᾶσα (f.), πᾶν (n.). Het lidwoord is onmisbaar als genus-signaal.",
            "source": "manual",
        },
    ]

    items["GRC-G-MORF-DECL3-KONS"] = [
        {
            "id": "ITEM-GRC-G-MORF-DECL3-KONS-001",
            "node_ids": ["GRC-G-MORF-DECL3-KONS"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": 0.1,
            "discrimination_initial": 1.1,
            "expected_time_sec": 15,
            "stimulus": "Welke stamklasse vertegenwoordigt φύλαξ, φύλακος?",
            "answer": [
                "occlusiefstam (velaar κ)",
                "κ-stam",
                "occlusief",
            ],
            "feedback": "Stam φυλακ- + σ van de nom. → φύλαξ (κ+σ → ξ). Typische sigmatische nom. bij een velaarstam.",
            "source": "manual",
        },
        {
            "id": "ITEM-GRC-G-MORF-DECL3-KONS-002",
            "node_ids": ["GRC-G-MORF-DECL3-KONS"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": 0.3,
            "discrimination_initial": 1.3,
            "expected_time_sec": 18,
            "stimulus": "Tot welke stamklasse behoort σῶμα, σώματος?",
            "answer": [
                "dentaalstam (τ)",
                "τ-stam",
                "dentaal",
            ],
            "feedback": "σῶμα is een neutrum met dentaalstam σωματ-. In de nom./acc. sg. valt de τ weg (klankwet), gen. σώματος onthult de stam.",
            "source": "manual",
        },
        {
            "id": "ITEM-GRC-G-MORF-DECL3-KONS-003",
            "node_ids": ["GRC-G-MORF-DECL3-KONS"],
            "type": "analysis",
            "direction": "receptive",
            "difficulty_initial": 0.5,
            "discrimination_initial": 1.3,
            "expected_time_sec": 25,
            "stimulus": "Welke stamklasse heeft σώφρων, σώφρονος?",
            "answer": [
                "nasaalstam (ν)",
                "ν-stam",
                "nasaal",
            ],
            "feedback": "σώφρων hoort bij de ν-stammen (stam σωφρον-). Asigmatische nominativus: klinkerverlenging ο → ω in de nom. sg. (en verlies van de ν is hier afwezig).",
            "source": "manual",
        },
    ]

    return items


def naamvallen() -> dict[str, list[dict]]:
    """NOM-D3, GEN-D3, DAT-D3, ACC-D3, VOC-D3 — 15 items."""
    items: dict[str, list[dict]] = {}

    items["GRC-G-MORF-NOM-D3"] = [
        {
            "id": "ITEM-GRC-G-MORF-NOM-D3-001",
            "node_ids": ["GRC-G-MORF-NOM-D3"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": 0.2,
            "discrimination_initial": 1.2,
            "expected_time_sec": 15,
            "stimulus": "Welke twee patronen kent de nominativus sg. in de 3e declinatie?",
            "answer": [
                "sigmatisch (stam + σ) en asigmatisch (stam met klinkerverlenging)",
                "met -ς (sigmatisch) of zonder -ς (asigmatisch)",
            ],
            "feedback": "Sigmatisch: stam + σ levert ξ/ψ/ς (φύλαξ, πᾶς). Asigmatisch: geen -ς, maar klinkerverlenging (σώφρων < σωφρον-).",
            "source": "manual",
        },
        {
            "id": "ITEM-GRC-G-MORF-NOM-D3-002",
            "node_ids": ["GRC-G-MORF-NOM-D3"],
            "type": "analysis",
            "direction": "receptive",
            "difficulty_initial": 0.5,
            "discrimination_initial": 1.3,
            "expected_time_sec": 20,
            "stimulus": "Waarom wordt παντ- + ς in de nom. sg. masculinum tot πᾶς?",
            "answer": [
                "de ν en τ vallen weg voor de σ, met compensatieverlenging α → ᾱ",
                "ντ valt uit voor σ; α verlengt tot α-lang",
            ],
            "feedback": "παντ- + σ → πασ- (ντ valt weg), daarna compensatieverlenging van de α tot ᾱ: πᾶς. Zelfde type bij γίγας (γιγαντ-).",
            "source": "manual",
        },
        {
            "id": "ITEM-GRC-G-MORF-NOM-D3-003",
            "node_ids": ["GRC-G-MORF-NOM-D3"],
            "type": "contextual",
            "direction": "receptive",
            "difficulty_initial": 0.4,
            "discrimination_initial": 1.3,
            "expected_time_sec": 25,
            "stimulus": "In 'πᾶς ἄνθρωπος ζῷόν ἐστιν' — welke naamval en welk getal heeft πᾶς?",
            "answer": [
                "nominativus singularis",
                "nom. sg.",
            ],
            "feedback": "πᾶς is hier nom. sg. masc., congruent met ἄνθρωπος (onderwerp). Stam παντ- → πᾶς via klankwet (ντσ → σ, compensatieverlenging).",
            "source": "manual",
        },
        {
            "id": "ITEM-GRC-G-MORF-NOM-D3-004",
            "node_ids": ["GRC-G-MORF-NOM-D3"],
            "type": "production",
            "direction": "productive",
            "difficulty_initial": 0.5,
            "discrimination_initial": 1.2,
            "expected_time_sec": 20,
            "stimulus": "Geef de nominativus singularis femininum van πᾶς.",
            "answer": "πᾶσα",
            "feedback": "Nom. sg. f. = πᾶσα. De feminina van ντ-adjectieven volgen de 1e declinatie (α-stam): πᾶσα, πάσης.",
            "source": "manual",
        },
    ]

    items["GRC-G-MORF-GEN-D3"] = [
        {
            "id": "ITEM-GRC-G-MORF-GEN-D3-001",
            "node_ids": ["GRC-G-MORF-GEN-D3"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": -0.1,
            "discrimination_initial": 1.0,
            "expected_time_sec": 12,
            "stimulus": "Welke uitgang heeft de genitivus sg. in de 3e declinatie?",
            "answer": "-ος",
            "feedback": "Gen. sg. = -ος. Deze uitgang is identificerend én onthullend: haal -ος weg om de stam te vinden (σώματος → σωματ-).",
            "source": "manual",
        },
        {
            "id": "ITEM-GRC-G-MORF-GEN-D3-002",
            "node_ids": ["GRC-G-MORF-GEN-D3"],
            "type": "production",
            "direction": "productive",
            "difficulty_initial": 0.5,
            "discrimination_initial": 1.3,
            "expected_time_sec": 25,
            "stimulus": "Geef de genitivus singularis masculinum van πᾶς.",
            "answer": "παντός",
            "feedback": "Gen. sg. m. = παντός (stam παντ- + -ος). Het accent springt naar de ultima omdat -ος daar lang genoeg voor is.",
            "source": "manual",
        },
        {
            "id": "ITEM-GRC-G-MORF-GEN-D3-003",
            "node_ids": ["GRC-G-MORF-GEN-D3"],
            "type": "contextual",
            "direction": "receptive",
            "difficulty_initial": 0.6,
            "discrimination_initial": 1.3,
            "expected_time_sec": 25,
            "stimulus": "In 'τὰ μέρη τοῦ σώματος' — welke naamval is σώματος?",
            "answer": [
                "genitivus singularis",
                "gen. sg.",
            ],
            "feedback": "σώματος = gen. sg. n. van σῶμα (stam σωματ-). Bezitsgenitief: 'de delen van het lichaam'. Uitgang -ος en lidwoord τοῦ bevestigen de naamval.",
            "source": "manual",
        },
        {
            "id": "ITEM-GRC-G-MORF-GEN-D3-004",
            "node_ids": ["GRC-G-MORF-GEN-D3"],
            "type": "contextual",
            "direction": "receptive",
            "difficulty_initial": 0.6,
            "discrimination_initial": 1.3,
            "expected_time_sec": 25,
            "stimulus": "In 'ἡ ψυχὴ τοῦ σώφρονος' — welke naamval heeft σώφρονος en wat is de stam?",
            "answer": [
                "genitivus singularis, stam σωφρον-",
                "gen. sg.; stam σωφρον-",
            ],
            "feedback": "σώφρονος = gen. sg. van σώφρων. De -ος-uitgang onthult de stam σωφρον- (ν-stam). Bezitsgenitief: 'de ziel van de verstandige'.",
            "source": "manual",
        },
    ]

    items["GRC-G-MORF-DAT-D3"] = [
        {
            "id": "ITEM-GRC-G-MORF-DAT-D3-001",
            "node_ids": ["GRC-G-MORF-DAT-D3"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": 0.0,
            "discrimination_initial": 1.0,
            "expected_time_sec": 12,
            "stimulus": "Welke uitgang heeft de dativus singularis in de 3e declinatie?",
            "answer": "-ι",
            "feedback": "Dat. sg. = -ι (geen iota subscriptum!): σώματι, φύλακι, σώφρονι. Let op: écht geschreven ι, niet onder een klinker.",
            "source": "manual",
        },
        {
            "id": "ITEM-GRC-G-MORF-DAT-D3-002",
            "node_ids": ["GRC-G-MORF-DAT-D3"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": 0.3,
            "discrimination_initial": 1.3,
            "expected_time_sec": 18,
            "stimulus": "Welke uitgang heeft de dativus pluralis in de 3e declinatie?",
            "answer": ["-σι(ν)", "-σι of -σιν"],
            "feedback": "Dat. pl. = -σι(ν) met bewegelijke ν voor klinker/zin-einde. Stamveranderingen zijn vaak zichtbaar: παντ- + σι → πᾶσι (ντ valt uit).",
            "source": "manual",
        },
        {
            "id": "ITEM-GRC-G-MORF-DAT-D3-003",
            "node_ids": ["GRC-G-MORF-DAT-D3"],
            "type": "contextual",
            "direction": "receptive",
            "difficulty_initial": 0.6,
            "discrimination_initial": 1.3,
            "expected_time_sec": 25,
            "stimulus": "In 'ὁ βασιλεὺς πᾶσι τοῖς πολίταις λέγει' — welke naamval is πᾶσι?",
            "answer": [
                "dativus pluralis",
                "dat. pl.",
            ],
            "feedback": "πᾶσι = dat. pl. m. van πᾶς (stam παντ- → dat. pl. παντ-σι → πᾶσι). Meewerkend voorwerp: 'de koning zegt tegen alle burgers'.",
            "source": "manual",
        },
    ]

    items["GRC-G-MORF-ACC-D3"] = [
        {
            "id": "ITEM-GRC-G-MORF-ACC-D3-001",
            "node_ids": ["GRC-G-MORF-ACC-D3"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": -0.1,
            "discrimination_initial": 1.1,
            "expected_time_sec": 12,
            "stimulus": "Welke uitgang heeft de accusativus sg. bij masc./fem. van de 3e declinatie?",
            "answer": "-α",
            "feedback": "Acc. sg. m./f. = -α: σώφρονα, φύλακα, πάντα (m.). Bij neutra geldt nom = acc (σῶμα).",
            "source": "manual",
        },
        {
            "id": "ITEM-GRC-G-MORF-ACC-D3-002",
            "node_ids": ["GRC-G-MORF-ACC-D3"],
            "type": "production",
            "direction": "productive",
            "difficulty_initial": 0.5,
            "discrimination_initial": 1.2,
            "expected_time_sec": 25,
            "stimulus": "Geef de accusativus pluralis masculinum van πᾶς.",
            "answer": "πάντας",
            "feedback": "Acc. pl. m. = πάντας (stam παντ- + -ας, uitgang bewaard). Niet te verwarren met de dat. pl. πᾶσι (daar valt ντ juist weg).",
            "source": "manual",
        },
        {
            "id": "ITEM-GRC-G-MORF-ACC-D3-003",
            "node_ids": ["GRC-G-MORF-ACC-D3"],
            "type": "contextual",
            "direction": "receptive",
            "difficulty_initial": 0.5,
            "discrimination_initial": 1.3,
            "expected_time_sec": 25,
            "stimulus": "In 'ὁ στρατιώτης τὸ σῶμα φυλάττει' — welke naamval is σῶμα?",
            "answer": [
                "accusativus singularis",
                "acc. sg.",
            ],
            "feedback": "σῶμα = acc. sg. n. (= nom. sg., neutrum-regel). Lijdend voorwerp: 'de soldaat beschermt het lichaam'. Lidwoord τό bevestigt genus en naamval.",
            "source": "manual",
        },
    ]

    items["GRC-G-MORF-VOC-D3"] = [
        {
            "id": "ITEM-GRC-G-MORF-VOC-D3-001",
            "node_ids": ["GRC-G-MORF-VOC-D3"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": 0.2,
            "discrimination_initial": 1.1,
            "expected_time_sec": 15,
            "stimulus": "Wat is de meest voorkomende vorm van de vocativus singularis in de 3e declinatie?",
            "answer": [
                "de kale stam",
                "de kale stam, zonder uitgang",
            ],
            "feedback": "Voc. sg. is doorgaans de kale stam zonder uitgang: σῶφρον (van σώφρων), παῖ (van παῖς, παιδ-). Bij sigmatische nominativus vaak gelijk aan nom. (φύλαξ).",
            "source": "manual",
        },
        {
            "id": "ITEM-GRC-G-MORF-VOC-D3-002",
            "node_ids": ["GRC-G-MORF-VOC-D3"],
            "type": "production",
            "direction": "productive",
            "difficulty_initial": 0.6,
            "discrimination_initial": 1.3,
            "expected_time_sec": 25,
            "stimulus": "Geef de vocativus singularis masculinum van σώφρων.",
            "answer": "σῶφρον",
            "feedback": "Voc. sg. m. = σῶφρον (kale stam σωφρον-, met circumflex over lange ω). De nom. σώφρων heeft juist klinkerverlenging.",
            "source": "manual",
        },
    ]

    return items


def paradigma_items() -> dict[str, list[dict]]:
    """DECL3-PARAD — 4 items (paradigma-drill + contextueel φύλαξ)."""
    items: dict[str, list[dict]] = {}

    items["GRC-G-MORF-DECL3-PARAD"] = [
        {
            "id": "ITEM-GRC-G-MORF-DECL3-PARAD-001",
            "node_ids": ["GRC-G-MORF-DECL3-PARAD"],
            "type": "offline_writing",
            "direction": "productive",
            "difficulty_initial": 0.8,
            "discrimination_initial": 1.3,
            "expected_time_sec": 120,
            "stimulus": "Schrijf het volledige paradigma van πᾶς op voor alle drie genera (masc./fem./neut., sg. + pl.) en vergelijk met je grammaticaboek.",
            "answer": "m. sg.: πᾶς, παντός, παντί, πάντα — f. sg.: πᾶσα, πάσης, πάσῃ, πᾶσαν — n. sg.: πᾶν, παντός, παντί, πᾶν — m./f./n. pl. zoals in grammatica.",
            "feedback": "Kern: m. stam παντ-, f. stam πασ-/πασ-, n. stam παντ-. Nom. sg.: πᾶς / πᾶσα / πᾶν. Dat. pl. m./n.: πᾶσι(ν); f.: πάσαις.",
            "source": "manual",
            "verification_method": "self_report",
            "expected_result": "3 × 2 × 5 = 30 vormen van πᾶς, met correcte accenten en zichtbare klankwetten (ντ voor σ valt weg).",
        },
        {
            "id": "ITEM-GRC-G-MORF-DECL3-PARAD-002",
            "node_ids": ["GRC-G-MORF-DECL3-PARAD"],
            "type": "analysis",
            "direction": "receptive",
            "difficulty_initial": 0.6,
            "discrimination_initial": 1.3,
            "expected_time_sec": 30,
            "stimulus": "Analyseer σώφρονι volledig: naamval, getal, stam en stamklasse.",
            "answer": [
                "dativus singularis van σώφρων, stam σωφρον- (ν-stam)",
                "dat. sg. m./f., ν-stam σωφρον-",
            ],
            "feedback": "σώφρονι = dat. sg. van σώφρων, stam σωφρον- + uitgang -ι. ν-stam: asigmatische nominativus met klinkerverlenging (ο → ω).",
            "source": "manual",
        },
        {
            "id": "ITEM-GRC-G-MORF-DECL3-PARAD-003",
            "node_ids": ["GRC-G-MORF-DECL3-PARAD"],
            "type": "contextual",
            "direction": "receptive",
            "difficulty_initial": 0.6,
            "discrimination_initial": 1.3,
            "expected_time_sec": 30,
            "stimulus": "In 'οἱ φύλακες τοὺς πολεμίους ὁρῶσιν' — welke naamval en welk getal heeft φύλακες?",
            "answer": [
                "nominativus pluralis",
                "nom. pl.",
            ],
            "feedback": "φύλακες = nom. pl. van φύλαξ (stam φυλακ- + -ες). Onderwerp: 'de wachten zien de vijanden'. Lidwoord οἱ bevestigt nom. pl. m.",
            "source": "manual",
        },
    ]

    return items


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------


def collect_all() -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {}
    out.update(intro_en_kons())
    out.update(naamvallen())
    out.update(paradigma_items())
    for _node_id, item_list in out.items():
        for item in item_list:
            for key in ("stimulus", "antwoord", "feedback", "expected_result"):
                if key in item and item[key] is not None:
                    item[key] = nfc(item[key])
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

    print("\n=== E3-05 Summary ===")
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
