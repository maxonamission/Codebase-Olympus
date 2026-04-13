#!/usr/bin/env python3
"""Generate exercise items for C1-01: INTRO concept nodes and case-function nodes.

Target: data/graph/lat_grammatica_poc.json
Nodes:  7 INTRO + 5 FUNCTIE = 12 nodes, ~24 items total.
"""

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from gymnasium_classica.models.graph import Item


def define_items() -> dict[str, list[dict]]:
    """Return knoop_id -> list of item dicts."""
    items: dict[str, list[dict]] = {}

    # ── INTRO nodes: herkenning / receptief ──────────────────────────

    items["LAT-G-MORF-NAAMVAL-INTRO"] = [
        {
            "id": "ITEM-LAT-G-MORF-NAAMVAL-INTRO-001",
            "knoop_ids": ["LAT-G-MORF-NAAMVAL-INTRO"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.8,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 12,
            "stimulus": "Hoeveel naamvallen kent het Latijn?",
            "antwoord": "6",
            "feedback": "Het Latijn kent zes naamvallen: nominativus, genitivus, dativus, accusativus, ablativus en vocativus.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-LAT-G-MORF-NAAMVAL-INTRO-002",
            "knoop_ids": ["LAT-G-MORF-NAAMVAL-INTRO"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.5,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 15,
            "stimulus": "Wat verandert er aan een Latijns woord als het een andere functie in de zin krijgt?",
            "antwoord": "de uitgang (het woord krijgt een andere naamvalsuitgang)",
            "feedback": "In het Latijn verandert de uitgang van een woord afhankelijk van de functie in de zin. Dit heet verbuiging (declinatie).",
            "bron": "handmatig",
        },
    ]

    items["LAT-G-MORF-DECL-INTRO"] = [
        {
            "id": "ITEM-LAT-G-MORF-DECL-INTRO-001",
            "knoop_ids": ["LAT-G-MORF-DECL-INTRO"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.7,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 12,
            "stimulus": "Hoeveel declinaties kent het Latijn?",
            "antwoord": "5",
            "feedback": "Het Latijn kent vijf declinaties. Elke declinatie is een groep zelfstandige naamwoorden met dezelfde uitgangen.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-LAT-G-MORF-DECL-INTRO-002",
            "knoop_ids": ["LAT-G-MORF-DECL-INTRO"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.5,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 12,
            "stimulus": "Wat is een declinatie?",
            "antwoord": "een groep zelfstandige naamwoorden met dezelfde verbuigingsuitgangen",
            "feedback": "Een declinatie is een groep zelfstandige naamwoorden die dezelfde set naamvalsuitgangen delen.",
            "bron": "handmatig",
        },
    ]

    items["LAT-G-MORF-GENUS-INTRO"] = [
        {
            "id": "ITEM-LAT-G-MORF-GENUS-INTRO-001",
            "knoop_ids": ["LAT-G-MORF-GENUS-INTRO"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.8,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 10,
            "stimulus": "Welke drie woordgeslachten kent het Latijn?",
            "antwoord": ["masculinum, femininum, neutrum", "mannelijk, vrouwelijk, onzijdig"],
            "feedback": "Het Latijn kent drie genera: masculinum (mannelijk), femininum (vrouwelijk) en neutrum (onzijdig).",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-LAT-G-MORF-GENUS-INTRO-002",
            "knoop_ids": ["LAT-G-MORF-GENUS-INTRO"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.4,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 12,
            "stimulus": "Hoe kun je het woordgeslacht van een Latijns zelfstandig naamwoord achterhalen?",
            "antwoord": "in het woordenboek staat het genus vermeld (m., f., n.)",
            "feedback": "Het woordenboek vermeldt het genus met de afkortingen m. (masculinum), f. (femininum) en n. (neutrum).",
            "bron": "handmatig",
        },
    ]

    items["LAT-G-MORF-NUMERUS-INTRO"] = [
        {
            "id": "ITEM-LAT-G-MORF-NUMERUS-INTRO-001",
            "knoop_ids": ["LAT-G-MORF-NUMERUS-INTRO"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -1.0,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 10,
            "stimulus": "Welke twee numeri (getallen) kent het Latijn?",
            "antwoord": ["singularis en pluralis", "enkelvoud en meervoud"],
            "feedback": "Het Latijn kent twee numeri: singularis (enkelvoud) en pluralis (meervoud).",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-LAT-G-MORF-NUMERUS-INTRO-002",
            "knoop_ids": ["LAT-G-MORF-NUMERUS-INTRO"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.6,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 12,
            "stimulus": "Hoe heet het enkelvoud met de Latijnse term?",
            "antwoord": "singularis",
            "feedback": "Enkelvoud heet in het Latijn singularis. Meervoud heet pluralis.",
            "bron": "handmatig",
        },
    ]

    items["LAT-G-MORF-PERSOON-INTRO"] = [
        {
            "id": "ITEM-LAT-G-MORF-PERSOON-INTRO-001",
            "knoop_ids": ["LAT-G-MORF-PERSOON-INTRO"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.7,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 12,
            "stimulus": "Hoeveel persoonsvormen heeft een Latijns werkwoord in totaal?",
            "antwoord": "6",
            "feedback": "Een Latijns werkwoord heeft zes persoonsvormen: 1e, 2e en 3e persoon, elk in enkelvoud en meervoud.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-LAT-G-MORF-PERSOON-INTRO-002",
            "knoop_ids": ["LAT-G-MORF-PERSOON-INTRO"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.4,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 15,
            "stimulus": "Welke persoon gebruik je als je over jezelf en anderen samen spreekt?",
            "antwoord": "1e persoon meervoud",
            "feedback": "De 1e persoon meervoud ('wij') gebruik je als je over jezelf en anderen samen spreekt.",
            "bron": "handmatig",
        },
    ]

    items["LAT-G-MORF-TEMPUS-INTRO"] = [
        {
            "id": "ITEM-LAT-G-MORF-TEMPUS-INTRO-001",
            "knoop_ids": ["LAT-G-MORF-TEMPUS-INTRO"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.6,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 15,
            "stimulus": "Noem de drie werkwoordstijden die je in leerjaar 1 Latijn leert.",
            "antwoord": ["praesens, imperfectum, perfectum"],
            "feedback": "De drie belangrijkste tempora in leerjaar 1 zijn praesens (tegenwoordige tijd), imperfectum (onvoltooid verleden) en perfectum (voltooid verleden).",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-LAT-G-MORF-TEMPUS-INTRO-002",
            "knoop_ids": ["LAT-G-MORF-TEMPUS-INTRO"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.3,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 12,
            "stimulus": "Hoe heet de tegenwoordige tijd in het Latijn?",
            "antwoord": "praesens",
            "feedback": "De tegenwoordige tijd heet praesens. Het imperfectum is de onvoltooid verleden tijd, het perfectum de voltooid verleden tijd.",
            "bron": "handmatig",
        },
    ]

    items["LAT-G-SYNT-ZINSDEEL-INTRO"] = [
        {
            "id": "ITEM-LAT-G-SYNT-ZINSDEEL-INTRO-001",
            "knoop_ids": ["LAT-G-SYNT-ZINSDEEL-INTRO"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.6,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 15,
            "stimulus": "Noem vier zinsdelen die je in een Latijnse zin kunt onderscheiden.",
            "antwoord": ["onderwerp, gezegde, lijdend voorwerp, meewerkend voorwerp"],
            "feedback": "De belangrijkste zinsdelen zijn: onderwerp (nominativus), gezegde (werkwoord), lijdend voorwerp (accusativus) en meewerkend voorwerp (dativus).",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-LAT-G-SYNT-ZINSDEEL-INTRO-002",
            "knoop_ids": ["LAT-G-SYNT-ZINSDEEL-INTRO"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.4,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 12,
            "stimulus": "Waardoor weet je in het Latijn welk woord het onderwerp is — woordvolgorde of uitgang?",
            "antwoord": "de uitgang (naamvalsuitgang)",
            "feedback": "In het Latijn bepaalt de naamvalsuitgang de zinsfunctie, niet de woordvolgorde. Het onderwerp staat in de nominativus.",
            "bron": "handmatig",
        },
    ]

    # ── FUNCTIE nodes: 1 herkenning + 1 contextueel ─────────────────

    items["LAT-G-SYNT-NOM-FUNCTIE"] = [
        {
            "id": "ITEM-LAT-G-SYNT-NOM-FUNCTIE-001",
            "knoop_ids": ["LAT-G-SYNT-NOM-FUNCTIE"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.3,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 12,
            "stimulus": "Welke naamval gebruik je voor het onderwerp van een zin?",
            "antwoord": "nominativus",
            "feedback": "De nominativus is de naamval van het onderwerp en van het naamwoordelijk deel van het gezegde.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-LAT-G-SYNT-NOM-FUNCTIE-002",
            "knoop_ids": ["LAT-G-SYNT-NOM-FUNCTIE"],
            "type": "contextueel",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.2,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 30,
            "stimulus": "Welke functie heeft 'puella' in de zin: 'Puella cantat.'?",
            "antwoord": "onderwerp",
            "feedback": "'Puella' staat in de nominativus en is het onderwerp van 'cantat' (zingt).",
            "bron": "handmatig",
        },
    ]

    items["LAT-G-SYNT-GEN-FUNCTIE"] = [
        {
            "id": "ITEM-LAT-G-SYNT-GEN-FUNCTIE-001",
            "knoop_ids": ["LAT-G-SYNT-GEN-FUNCTIE"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.3,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 12,
            "stimulus": "Welke naamval drukt bezit uit in het Latijn?",
            "antwoord": "genitivus",
            "feedback": "De genitivus is de naamval van bezit ('van'), maar ook van het deel (partitief) en de eigenschap.",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-LAT-G-SYNT-GEN-FUNCTIE-002",
            "knoop_ids": ["LAT-G-SYNT-GEN-FUNCTIE"],
            "type": "contextueel",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.3,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 35,
            "stimulus": "Welke functie heeft 'puellae' in de zin: 'Liber puellae est.'?",
            "antwoord": "bezit (genitivus van bezit)",
            "feedback": "'Puellae' is hier genitivus singularis en drukt bezit uit: 'Het boek is van het meisje.'",
            "bron": "handmatig",
        },
    ]

    items["LAT-G-SYNT-DAT-FUNCTIE"] = [
        {
            "id": "ITEM-LAT-G-SYNT-DAT-FUNCTIE-001",
            "knoop_ids": ["LAT-G-SYNT-DAT-FUNCTIE"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.3,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 12,
            "stimulus": "Welke naamval gebruik je voor het meewerkend voorwerp?",
            "antwoord": "dativus",
            "feedback": "De dativus is de naamval van het meewerkend voorwerp ('aan/voor wie').",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-LAT-G-SYNT-DAT-FUNCTIE-002",
            "knoop_ids": ["LAT-G-SYNT-DAT-FUNCTIE"],
            "type": "contextueel",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.3,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 35,
            "stimulus": "Welke functie heeft 'puellae' in de zin: 'Dominus puellae librum dat.'?",
            "antwoord": "meewerkend voorwerp",
            "feedback": "'Puellae' is hier dativus singularis en meewerkend voorwerp: 'De heer geeft het boek aan het meisje.'",
            "bron": "handmatig",
        },
    ]

    items["LAT-G-SYNT-ACC-FUNCTIE"] = [
        {
            "id": "ITEM-LAT-G-SYNT-ACC-FUNCTIE-001",
            "knoop_ids": ["LAT-G-SYNT-ACC-FUNCTIE"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.3,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 12,
            "stimulus": "Welke naamval gebruik je voor het lijdend voorwerp?",
            "antwoord": "accusativus",
            "feedback": "De accusativus is de naamval van het lijdend voorwerp en van de richting ('waarheen').",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-LAT-G-SYNT-ACC-FUNCTIE-002",
            "knoop_ids": ["LAT-G-SYNT-ACC-FUNCTIE"],
            "type": "contextueel",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.2,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 30,
            "stimulus": "Welke functie heeft 'puellam' in de zin: 'Dominus puellam videt.'?",
            "antwoord": "lijdend voorwerp",
            "feedback": "'Puellam' is accusativus singularis en lijdend voorwerp: 'De heer ziet het meisje.'",
            "bron": "handmatig",
        },
    ]

    items["LAT-G-SYNT-ABL-FUNCTIE"] = [
        {
            "id": "ITEM-LAT-G-SYNT-ABL-FUNCTIE-001",
            "knoop_ids": ["LAT-G-SYNT-ABL-FUNCTIE"],
            "type": "herkenning",
            "richting": "receptief",
            "moeilijkheid_initieel": -0.2,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 15,
            "stimulus": "Welke naamval drukt middel, oorzaak of plaats uit?",
            "antwoord": "ablativus",
            "feedback": "De ablativus is de naamval van middel ('waarmee'), oorzaak ('waardoor'), plaats ('waar') en tijd ('wanneer').",
            "bron": "handmatig",
        },
        {
            "id": "ITEM-LAT-G-SYNT-ABL-FUNCTIE-002",
            "knoop_ids": ["LAT-G-SYNT-ABL-FUNCTIE"],
            "type": "contextueel",
            "richting": "receptief",
            "moeilijkheid_initieel": 0.4,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 35,
            "stimulus": "Welke functie heeft 'gladio' in de zin: 'Miles gladio pugnat.'?",
            "antwoord": "middel (ablativus van middel)",
            "feedback": "'Gladio' is ablativus singularis en drukt het middel uit: 'De soldaat vecht met het zwaard.'",
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
                item
                for item in items_by_knoop[knoop["id"]]
                if item["id"] not in existing_ids
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

    print(f"\n=== C1-01 Summary ===")
    print(f"Knopen: {len(items_by_knoop)}")
    print(f"Total items: {total}")
    print(f"\nItems per knoop:")
    for kid, item_list in sorted(items_by_knoop.items()):
        print(f"  {kid}: {len(item_list)}")
    print(f"\nOefentype-verdeling:")
    for t, c in type_counter.most_common():
        print(f"  {t}: {c}")
    print(f"\nRichting-verdeling:")
    for r, c in richting_counter.most_common():
        print(f"  {r}: {c}")


def main() -> None:
    items_by_knoop = define_items()
    validate_items(items_by_knoop)

    poc_path = Path(__file__).parent.parent / "data" / "graph" / "lat_grammatica_poc.json"
    added = add_items_to_json(poc_path, items_by_knoop)
    print(f"Added {added} items to {poc_path.name}")

    print_summary(items_by_knoop)


if __name__ == "__main__":
    main()
