#!/usr/bin/env python3
"""Generate exercise items for C1-05: adjectieven (A1-05 nodes).

Targets:
  - data/graph/lat_grammatica_poc.json  (ADJ-D12-INTRO, ADJ-D12-VERBG, ADJ-CONGR)
  - data/graph/lat_grammatica_leerjaar1.json (rest)
~26 items total.
"""

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from gymnasium_classica.models.graph import Item

POC_IDS = {"LAT-G-MORF-ADJ-D12-INTRO", "LAT-G-MORF-ADJ-D12-VERBG", "LAT-G-SYNT-ADJ-CONGR"}
LJ1_IDS = {
    "LAT-G-MORF-ADJ-INTRO",
    "LAT-G-MORF-ADJ-D3-INTRO",
    "LAT-G-MORF-ADJ-D3-3EIND",
    "LAT-G-MORF-ADJ-D3-2EIND",
    "LAT-G-MORF-ADJ-D3-1EIND",
    "LAT-G-MORF-ADJ-D3-VERBG",
    "LAT-G-MORF-ADJ-COMPAR",
}


def _h(kid, nr, stim, antw, fb, moeil=-0.3, tijd=12):
    return {
        "id": f"ITEM-{kid}-{nr:03d}",
        "node_ids": [kid],
        "type": "herkenning",
        "direction": "receptief",
        "difficulty_initial": moeil,
        "discrimination_initial": 1.0,
        "expected_time_sec": tijd,
        "stimulus": stim,
        "answer": antw,
        "feedback": fb,
        "source": "handmatig",
    }


def _p(kid, nr, stim, antw, fb, moeil=0.6, tijd=20):
    return {
        "id": f"ITEM-{kid}-{nr:03d}",
        "node_ids": [kid],
        "type": "productie",
        "direction": "productief",
        "difficulty_initial": moeil,
        "discrimination_initial": 1.0,
        "expected_time_sec": tijd,
        "stimulus": stim,
        "answer": antw,
        "feedback": fb,
        "source": "handmatig",
    }


def _c(kid, nr, stim, antw, fb, moeil=0.3, tijd=35):
    return {
        "id": f"ITEM-{kid}-{nr:03d}",
        "node_ids": [kid],
        "type": "contextueel",
        "direction": "receptief",
        "difficulty_initial": moeil,
        "discrimination_initial": 1.0,
        "expected_time_sec": tijd,
        "stimulus": stim,
        "answer": antw,
        "feedback": fb,
        "source": "handmatig",
    }


def define_items() -> dict[str, list[dict]]:
    I = {}  # noqa: E741 - script-lokale conventie

    K = "LAT-G-MORF-ADJ-INTRO"
    I[K] = [
        _h(
            K,
            1,
            "Welke twee hoofdgroepen adjectieven kent het Latijn?",
            "type bonus (1e/2e declinatie) en type fortis (3e declinatie)",
            "Adjectieven volgen de 1e/2e declinatie (bonus, -a, -um) of de 3e declinatie (fortis, -e).",
            -0.4,
            15,
        ),
        _h(
            K,
            2,
            "Wat moet een Latijns adjectief overnemen van het zelfstandig naamwoord?",
            "genus, numerus en casus",
            "Een adjectief congrueert met het zelfstandig naamwoord in genus (geslacht), numerus (getal) en casus (naamval).",
            -0.2,
            12,
        ),
    ]

    K = "LAT-G-MORF-ADJ-D12-INTRO"
    I[K] = [
        _h(
            K,
            1,
            "Hoe staat een adjectief als 'bonus' in het woordenboek?",
            "bonus, -a, -um (drie uitgangen: m., f., n.)",
            "Adjectieven van de 1e/2e declinatie worden opgegeven met drie nominativusvormen: bonus (m.), bona (f.), bonum (n.).",
            -0.3,
            12,
        ),
        _h(
            K,
            2,
            "Welke declinatie volgt het femininum van 'bonus'?",
            "de 1e declinatie",
            "Het femininum (bona) volgt de 1e declinatie (a-stam). Het masculinum en neutrum volgen de 2e declinatie.",
            -0.1,
            12,
        ),
    ]

    K = "LAT-G-MORF-ADJ-D12-VERBG"
    I[K] = [
        _p(
            K,
            1,
            "Verbuig 'bonus' in de accusativus enkelvoud voor alle drie genera.",
            "bonum (m.), bonam (f.), bonum (n.)",
            "Masc. en neutr. volgen 2e decl. (-um), fem. volgt 1e decl. (-am). Acc. sg. masc. = neutr. bij dit type.",
            0.7,
            25,
        ),
        _p(
            K,
            2,
            "Geef de genitivus meervoud van 'bonus' (alle genera).",
            "bonorum (m./n.), bonarum (f.)",
            "Masc./neutr. gen. pl. -orum (2e decl.), fem. gen. pl. -arum (1e decl.).",
            0.8,
            25,
        ),
        _h(
            K,
            3,
            "Wat is de ablativus enkelvoud femininum van 'magnus, -a, -um'?",
            "magna",
            "Het femininum volgt de 1e declinatie: abl. sg. op -ā. Magna (met lange a).",
            0.2,
            15,
        ),
    ]

    K = "LAT-G-SYNT-ADJ-CONGR"
    I[K] = [
        _h(
            K,
            1,
            "Wat is congruentie bij adjectieven?",
            "het adjectief neemt genus, numerus en casus over van het zelfstandig naamwoord",
            "Congruentie betekent dat het adjectief zich aanpast aan het zelfstandig naamwoord in genus, numerus en casus.",
            -0.2,
            15,
        ),
        _c(
            K,
            2,
            "'Puella bona cantat.' — waarom staat 'bona' in deze vorm?",
            "puella is femininum sg. nominativus, dus het adjectief wordt bona (fem. sg. nom.)",
            "Het adjectief congrueert: puella = fem. sg. nom., dus bonus → bona.",
            0.3,
            35,
        ),
        _c(
            K,
            3,
            "Welke vorm van 'bonus' past bij 'bellum' (acc. sg.)?",
            "bonum",
            "Bellum is neutrum: acc. sg. neutrum van bonus = bonum. Neutrumregel: nom.=acc.",
            0.4,
            30,
        ),
    ]

    K = "LAT-G-MORF-ADJ-D3-INTRO"
    I[K] = [
        _h(
            K,
            1,
            "Welke drie subtypen adjectieven van de 3e declinatie bestaan er?",
            "drieuitgangig (acer), tweeuitgangig (fortis), eenuitgangig (prudens)",
            "De 3e-declinatieadjectieven hebben drie subtypen: 3-uitgangig (acer, acris, acre), 2-uitgangig (fortis, -e), 1-uitgangig (prudens, -ntis).",
            0.0,
            15,
        ),
        _h(
            K,
            2,
            "Welk subtype 3e-declinatieadjectief komt het meest voor?",
            "tweeuitgangig (fortis-type)",
            "Het tweeuitgangig type (fortis, -e) is het meest voorkomend. Eén vorm voor m.+f., één voor n.",
            -0.1,
            12,
        ),
    ]

    K = "LAT-G-MORF-ADJ-D3-3EIND"
    I[K] = [
        _h(
            K,
            1,
            "Hoeveel nominativusvormen heeft een drieuitgangig adjectief?",
            "drie: een voor masculinum, femininum en neutrum",
            "Drieuitgangig: acer (m.), acris (f.), acre (n.). Drie aparte nominativusvormen.",
            -0.2,
            10,
        ),
        _p(
            K,
            2,
            "Geef de nominativus enkelvoud van 'acer' voor alle genera.",
            "acer (m.), acris (f.), acre (n.)",
            "Acer heeft drie vormen: acer (m.), acris (f.), acre (n.). Alleen de nom. sg. verschilt per genus.",
            0.5,
            20,
        ),
        _p(
            K,
            3,
            "Geef de ablativus enkelvoud van 'acer'.",
            "acri",
            "3e-declinatie adjectieven volgen het i-stampatroon: abl. sg. op -i: acr- + -i = acri.",
            0.7,
            20,
        ),
    ]

    K = "LAT-G-MORF-ADJ-D3-2EIND"
    I[K] = [
        _h(
            K,
            1,
            "Hoe staat een tweeuitgangig adjectief in het woordenboek?",
            "fortis, -e (twee vormen: m./f. en n.)",
            "Tweeuitgangig: fortis (m.+f.), forte (n.). Het woordenboek geeft de tweede vorm na een komma.",
            -0.2,
            12,
        ),
        _p(
            K,
            2,
            "Geef de genitivus enkelvoud van 'fortis'.",
            "fortis",
            "Gen. sg. van fortis is fortis (gelijk aan de nom. sg. m./f.). Stam: fort-.",
            0.4,
            15,
        ),
        _p(
            K,
            3,
            "Geef de nominativus meervoud neutrum van 'fortis, -e'.",
            "fortia",
            "Neutra i-stammen: nom. pl. op -ia: fort- + -ia = fortia.",
            0.8,
            20,
        ),
    ]

    K = "LAT-G-MORF-ADJ-D3-1EIND"
    I[K] = [
        _h(
            K,
            1,
            "Hoe herken je de stam van een eenuitgangig adjectief?",
            "via de genitivus: prudens, prudent-is → stam prudent-",
            "Bij eenuitgangige adjectieven heeft de nom. sg. één vorm voor alle genera. De genitivus toont de stam.",
            0.0,
            15,
        ),
        _p(
            K,
            2,
            "Geef de accusativus enkelvoud masculinum van 'prudens, prudentis'.",
            "prudentem",
            "Stam prudent- + uitgang -em = prudentem (m./f.). Bij neutrum: prudens (nom.=acc.).",
            0.7,
            20,
        ),
        _p(
            K,
            3,
            "Geef de genitivus meervoud van 'prudens, prudentis'.",
            "prudentium",
            "I-stampatroon: gen. pl. op -ium: prudent- + -ium = prudentium.",
            0.8,
            20,
        ),
    ]

    K = "LAT-G-MORF-ADJ-D3-VERBG"
    I[K] = [
        _h(
            K,
            1,
            "Welk stampatroon volgen 3e-declinatie adjectieven: consonantstam of i-stam?",
            "i-stam",
            "Alle 3e-declinatie adjectieven volgen het i-stampatroon: abl. sg. -i, gen. pl. -ium, nom./acc. pl. n. -ia.",
            0.0,
            12,
        ),
        _p(
            K,
            2,
            "Geef de ablativus enkelvoud en genitivus meervoud van 'fortis, -e'.",
            "forti, fortium",
            "I-stampatroon: abl. sg. fort-i, gen. pl. fort-ium.",
            0.8,
            25,
        ),
    ]

    K = "LAT-G-MORF-ADJ-COMPAR"
    I[K] = [
        _h(
            K,
            1,
            "Noem de drie trappen van vergelijking in het Latijn.",
            "positivus, comparativus, superlativus",
            "De drie gradus: positivus (stellend, fortis), comparativus (vergrotend, fortior), superlativus (overtreffend, fortissimus).",
            -0.3,
            12,
        ),
        _h(
            K,
            2,
            "Wat zijn de uitgangen van de comparativus?",
            "-ior (m./f.) en -ius (n.)",
            "De comparativus wordt gevormd met -ior (m./f.) en -ius (n.): fortis → fortior, fortius.",
            0.1,
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
    print(f"\n=== C1-05 Summary ===\nKnopen: {len(items_by_node)}\nTotal items: {total}")
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
