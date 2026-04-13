#!/usr/bin/env python3
"""Generate exercise items for C1-04: 3e declinatie (A1-04 knopen).

Targets:
  - data/graph/lat_grammatica_poc.json  (DECL3-INTRO, NOM-D3)
  - data/graph/lat_grammatica_leerjaar1.json (rest)
~37 items total.
"""

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from gymnasium_classica.models.graph import Item

POC_IDS = {"LAT-G-MORF-DECL3-INTRO", "LAT-G-MORF-NOM-D3"}
LJ1_IDS = {
    "LAT-G-MORF-GEN-D3", "LAT-G-MORF-DAT-D3", "LAT-G-MORF-ACC-D3",
    "LAT-G-MORF-ABL-D3", "LAT-G-MORF-VOC-D3", "LAT-G-MORF-DECL3-STAM",
    "LAT-G-MORF-DECL3-CONS", "LAT-G-MORF-DECL3-ISTAM",
    "LAT-G-MORF-DECL3-NEUT", "LAT-G-MORF-DECL3-PARAD",
}

def _h(kid, nr, stim, antw, fb, moeil=-0.3, tijd=12):
    """Shorthand for herkenning/receptief item."""
    return {"id": f"ITEM-{kid}-{nr:03d}", "knoop_ids": [kid],
            "type": "herkenning", "richting": "receptief",
            "moeilijkheid_initieel": moeil, "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": tijd, "stimulus": stim,
            "antwoord": antw, "feedback": fb, "bron": "handmatig"}

def _p(kid, nr, stim, antw, fb, moeil=0.6, tijd=20):
    """Shorthand for productie/productief item."""
    return {"id": f"ITEM-{kid}-{nr:03d}", "knoop_ids": [kid],
            "type": "productie", "richting": "productief",
            "moeilijkheid_initieel": moeil, "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": tijd, "stimulus": stim,
            "antwoord": antw, "feedback": fb, "bron": "handmatig"}

def _a(kid, nr, stim, antw, fb, moeil=1.0, tijd=30):
    """Shorthand for analyse/receptief item."""
    return {"id": f"ITEM-{kid}-{nr:03d}", "knoop_ids": [kid],
            "type": "analyse", "richting": "receptief",
            "moeilijkheid_initieel": moeil, "discriminatie_initieel": 1.2,
            "verwachte_tijd_sec": tijd, "stimulus": stim,
            "antwoord": antw, "feedback": fb, "bron": "handmatig"}


def define_items() -> dict[str, list[dict]]:
    I = {}  # knoop_id -> list[dict]
    K = "LAT-G-MORF-DECL3-INTRO"
    I[K] = [
        _h(K,1,"Waarom is de 3e declinatie lastiger dan de 1e en 2e?",
           "de nominativus heeft geen vaste uitgang — er is grote variatie",
           "De 3e declinatie kent diverse nominativus-uitgangen (rex, corpus, nomen). De genitivus sg. op -is is het herkenningsteken.", -0.5, 15),
        _h(K,2,"Hoe herken je in het woordenboek dat een woord bij de 3e declinatie hoort?",
           "de genitivus singularis eindigt op -is",
           "Een woord hoort bij de 3e declinatie als de genitivus singularis op -is eindigt. Bijv. rex, reg-is.", -0.3, 12),
        _h(K,3,"Welke twee subtypes onderscheidt de 3e declinatie?",
           "consonantstammen en i-stammen",
           "De 3e declinatie kent consonantstammen (stam op medeklinker, bijv. rex) en i-stammen (stam op -i, bijv. mare).", -0.1, 15),
    ]

    K = "LAT-G-MORF-NOM-D3"
    I[K] = [
        _h(K,1,"Noem drie verschillende nominativus-vormen van de 3e declinatie.",
           ["rex, corpus, nomen", "miles, lex, caput"],
           "De nominativus sg. van de 3e declinatie varieert sterk: rex, miles, corpus, nomen, mare, etc.", -0.2, 15),
        _p(K,2,"Geef de nominativus meervoud van 'rex, regis'.",
           "reges",
           "De nominativus pl. van consonantstammen van de 3e declinatie eindigt op -es: rex → reges.", 0.5, 20),
        _p(K,3,"Geef de nominativus meervoud van 'mare, maris (n.)'.",
           "maria",
           "Bij neutra i-stammen eindigt de nom. pl. op -ia: mare → maria (neutrumregel + i-stam).", 0.8, 20),
    ]

    K = "LAT-G-MORF-GEN-D3"
    I[K] = [
        _h(K,1,"Wat is de genitivus-uitgang van de 3e declinatie in het enkelvoud?",
           "-is",
           "De genitivus singularis van de 3e declinatie eindigt altijd op -is. Dit geldt voor alle subtypes.", -0.3, 10),
        _p(K,2,"Geef de genitivus meervoud van 'rex, regis'.",
           "regum",
           "Consonantstammen: gen. pl. op -um: rex, regis → regum.", 0.7, 20),
        _p(K,3,"Geef de genitivus meervoud van 'mare, maris (n.)'.",
           "marium",
           "I-stammen: gen. pl. op -ium: mare, maris → marium. Dit onderscheidt i-stammen van consonantstammen.", 0.9, 20),
    ]

    K = "LAT-G-MORF-DAT-D3"
    I[K] = [
        _h(K,1,"Wat is de dativus-uitgang van de 3e declinatie in het enkelvoud?",
           "-i",
           "De dativus singularis van de 3e declinatie eindigt op -i: regi, corpori, mari.", -0.2, 10),
        _p(K,2,"Geef de dativus meervoud van 'miles, militis'.",
           "militibus",
           "De dativus pl. van de 3e declinatie eindigt op -ibus: miles → militibus.", 0.7, 20),
        _p(K,3,"Geef de dativus enkelvoud van 'corpus, corporis'.",
           "corpori",
           "Stam corpor- + uitgang -i = corpori.", 0.5, 20),
    ]

    K = "LAT-G-MORF-ACC-D3"
    I[K] = [
        _h(K,1,"Wat is de accusativus-uitgang van de 3e declinatie sg. bij masculina/feminina?",
           "-em",
           "De acc. sg. van masc./fem. van de 3e declinatie eindigt op -em: regem, militem. Bij neutra: nom.=acc.", -0.2, 12),
        _p(K,2,"Geef de accusativus enkelvoud van 'rex, regis'.",
           "regem",
           "Stam reg- + uitgang -em = regem.", 0.5, 20),
        _p(K,3,"Geef de accusativus meervoud van 'mare, maris (n.)'.",
           "maria",
           "Bij neutra i-stammen: acc. pl. = nom. pl. = -ia: mare → maria (neutrumregel).", 0.8, 20),
    ]

    K = "LAT-G-MORF-ABL-D3"
    I[K] = [
        _h(K,1,"Wat is het verschil in ablativus sg. tussen consonantstammen en i-stammen?",
           "consonantstammen: -e, i-stammen: -i",
           "Consonantstammen: abl. sg. op -e (rege). I-stammen: abl. sg. op -i (mari). Dit is een belangrijk onderscheid.", 0.0, 15),
        _p(K,2,"Geef de ablativus enkelvoud van 'rex, regis'.",
           "rege",
           "Rex is een consonantstam: abl. sg. op -e: reg- + -e = rege.", 0.5, 20),
        _p(K,3,"Geef de ablativus enkelvoud van 'mare, maris (n.)'.",
           "mari",
           "Mare is een i-stam: abl. sg. op -i: mar- + -i = mari.", 0.7, 20),
    ]

    K = "LAT-G-MORF-VOC-D3"
    I[K] = [
        _h(K,1,"Is de vocativus van de 3e declinatie gelijk aan een andere naamval?",
           "ja, de vocativus is gelijk aan de nominativus",
           "Bij de 3e declinatie is de vocativus altijd gelijk aan de nominativus: rex!, reges!", -0.4, 10),
        _p(K,2,"Hoe spreek je een soldaat (miles) direct aan in het Latijn?",
           "miles!",
           "De vocativus van miles is miles! — gelijk aan de nominativus bij de 3e declinatie.", 0.3, 15),
    ]

    K = "LAT-G-MORF-DECL3-STAM"
    I[K] = [
        _h(K,1,"Hoe bepaal je de stam van een 3e-declinatiewoord?",
           "haal -is van de genitivus singularis af",
           "De stam vind je door -is van de gen. sg. af te halen. Bijv. reg-is → stam reg-, corpor-is → stam corpor-.", -0.2, 12),
        _p(K,2,"Wat is de stam van 'miles, militis'?",
           "milit-",
           "Genitivus milit-is → stam milit-. Let op: de stam verschilt sterk van de nominativus 'miles'.", 0.5, 20),
        _p(K,3,"Wat is de stam van 'nomen, nominis'?",
           "nomin-",
           "Genitivus nomin-is → stam nomin-. De genitivus toont de ware stam.", 0.6, 20),
    ]

    K = "LAT-G-MORF-DECL3-CONS"
    I[K] = [
        _h(K,1,"Noem twee modelwoorden voor consonantstammen van de 3e declinatie.",
           ["rex, regis (m.) en corpus, corporis (n.)"],
           "Rex (stam reg-, medeklinker) en corpus (stam corpor-) zijn typische consonantstammen.", -0.2, 12),
        _h(K,2,"Op welke uitgang eindigt de genitivus meervoud van consonantstammen?",
           "-um",
           "Consonantstammen: gen. pl. op -um (regum, corporum). I-stammen: gen. pl. op -ium.", 0.0, 12),
        _p(K,3,"Geef de ablativus enkelvoud en de genitivus meervoud van 'rex, regis'.",
           "rege, regum",
           "Consonantstam: abl. sg. reg- + -e = rege, gen. pl. reg- + -um = regum.", 0.8, 25),
    ]

    K = "LAT-G-MORF-DECL3-ISTAM"
    I[K] = [
        _h(K,1,"Noem drie kenmerken waarmee je een i-stam herkent.",
           ["gen. pl. -ium, abl. sg. -i, nom./acc. pl. neutra -ia"],
           "I-stammen herken je aan: gen. pl. -ium, abl. sg. -i, en bij neutra nom./acc. pl. -ia.", 0.1, 15),
        _h(K,2,"Wat is het modelwoord voor neutra i-stammen?",
           "mare, maris (n.)",
           "Mare, maris (n.) is het modelwoord voor neutra i-stammen: gen. pl. marium, abl. sg. mari, nom. pl. maria.", -0.1, 12),
        _p(K,3,"Geef de genitivus meervoud van 'civis, civis'.",
           "civium",
           "Civis is een i-stam: gen. pl. op -ium: civ- + -ium = civium.", 0.8, 20),
    ]

    K = "LAT-G-MORF-DECL3-NEUT"
    I[K] = [
        _h(K,1,"Hoe werkt de neutrumregel bij de 3e declinatie?",
           "nom.=acc.; pl. op -a (consonantstam) of -ia (i-stam)",
           "Neutrumregel: nom.=acc. altijd gelijk. Meervoud: consonantstammen -a (corpora), i-stammen -ia (maria).", 0.0, 15),
        _p(K,2,"Geef de nominativus meervoud van 'corpus, corporis (n.)'.",
           "corpora",
           "Corpus is een neutrum consonantstam: nom. pl. op -a: corpor- + -a = corpora.", 0.6, 20),
        _p(K,3,"Geef de accusativus meervoud van 'nomen, nominis (n.)'.",
           "nomina",
           "Nomen is een neutrum consonantstam: acc. pl. = nom. pl. = -a: nomin- + -a = nomina.", 0.7, 20),
    ]

    K = "LAT-G-MORF-DECL3-PARAD"
    I[K] = [
        _h(K,1,"Welke twee naamvallen van de 3e declinatie meervoud hebben dezelfde uitgang -ibus?",
           "dativus pluralis en ablativus pluralis",
           "Dativus en ablativus pl. van de 3e declinatie eindigen beiden op -ibus (regibus, corporibus).", -0.1, 12),
        _a(K,2,"Ontleed 'regum' volledig.",
           "genitivus pluralis, 3e declinatie (consonantstam)",
           "Reg-um: stam reg- + uitgang -um = gen. pl. De uitgang -um (niet -ium) wijst op een consonantstam.", 1.0, 30),
        _a(K,3,"Ontleed 'maria' volledig (3e declinatie).",
           ["nominativus pluralis of accusativus pluralis neutrum, 3e declinatie (i-stam)"],
           "Mar-ia: stam mar- + uitgang -ia = nom./acc. pl. neutrum i-stam. Niet verwarren met de eigennaam Maria.", 1.3, 35),
        _p(K,4,"Verbuig 'corpus' in de genitivus enkelvoud en meervoud.",
           "corporis, corporum",
           "Gen. sg. corpor-is, gen. pl. corpor-um. Let op de stamuitbreiding: corpus → corpor-.", 0.9, 25),
        _a(K,5,"Ontleed 'militibus' volledig.",
           ["dativus pluralis of ablativus pluralis, 3e declinatie"],
           "Milit-ibus: stam milit- + uitgang -ibus = dat./abl. pl. van miles, militis.", 1.2, 35),
    ]
    return I


def validate_items(items_by_knoop):
    for kid, il in items_by_knoop.items():
        for d in il:
            Item(**d)
    print("All items validated successfully.")

def add_items_to_json(json_path, items_by_knoop):
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)
    added = 0
    for knoop in data["knopen"]:
        if knoop["id"] in items_by_knoop:
            existing = {i["id"] for i in knoop.get("items", [])}
            new = [i for i in items_by_knoop[knoop["id"]] if i["id"] not in existing]
            knoop.setdefault("items", []).extend(new)
            added += len(new)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return added

def print_summary(items_by_knoop):
    total = sum(len(v) for v in items_by_knoop.values())
    tc = Counter()
    rc = Counter()
    for il in items_by_knoop.values():
        for i in il:
            tc[i["type"]] += 1
            rc[i["richting"]] += 1
    print(f"\n=== C1-04 Summary ===\nKnopen: {len(items_by_knoop)}\nTotal items: {total}")
    print("\nItems per knoop:")
    for k, v in sorted(items_by_knoop.items()):
        print(f"  {k}: {len(v)}")
    print("\nOefentype-verdeling:")
    for t, c in tc.most_common():
        print(f"  {t}: {c}")
    print("\nRichting-verdeling:")
    for r, c in rc.most_common():
        print(f"  {r}: {c}")

def main():
    items = define_items()
    validate_items(items)
    base = Path(__file__).parent.parent / "data" / "graph"
    a1 = add_items_to_json(base / "lat_grammatica_poc.json", {k:v for k,v in items.items() if k in POC_IDS})
    a2 = add_items_to_json(base / "lat_grammatica_leerjaar1.json", {k:v for k,v in items.items() if k in LJ1_IDS})
    print(f"Added {a1} items to poc, {a2} items to leerjaar1")
    print_summary(items)

if __name__ == "__main__":
    main()
