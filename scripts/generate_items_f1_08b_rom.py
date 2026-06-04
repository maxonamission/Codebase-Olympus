#!/usr/bin/env python3
"""F1-08b — herkenningsitems voor Romeins leven (SHA-C-POL-*, Romeinse kant) en
Romeinse geschiedenis (SHA-C-GES-*). 15 + 15 = 30 items.

Griekse POL-knopen (GRIEK/POLIS/AGORA/...) komen in batch F1-08c.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from gymnasium_classica.models.graph import Item

OUTPUT = Path(__file__).parent.parent / "data" / "graph" / "sha_cultuur_leerjaar1.json"

BATCH: list[tuple[str, str, list[str], int, str]] = [
    # ── Romeins dagelijks leven (SHA-C-POL-*, Romeinse helft) ──────────
    (
        "POL-INTRO",
        "Welke onderwerpen vallen onder 'Romeins dagelijks leven'?",
        [
            "Alleen politiek en oorlog",
            "Gezin, wonen, voeding en onderwijs",
            "Alleen religie",
            "Uitsluitend bouwkunst",
        ],
        1,
        "Romeins dagelijks leven beslaat gezin, wonen, onderwijs, voeding en sociale verhoudingen.",
    ),
    (
        "POL-FAMIL",
        "Wat is de Romeinse familia in juridische zin?",
        [
            "Alleen vader, moeder en kinderen",
            "Het huishouden onder gezag van de paterfamilias (inclusief slaven)",
            "Een militaire eenheid",
            "Een religieus genootschap",
        ],
        1,
        "De familia is de juridische huishoudeenheid onder de paterfamilias — inclusief vrouw, kinderen, vrijgelatenen en slaven.",
    ),
    (
        "POL-PATER",
        "Wat houdt de patria potestas in?",
        [
            "Militair opperbevel van een consul",
            "Absolute juridische macht van de paterfamilias over het huishouden",
            "Het stemrecht in de comitia",
            "De macht van de Senaat over de provincies",
        ],
        1,
        "Patria potestas is de absolute juridische macht van de paterfamilias over zijn huishouden, inclusief recht over leven en dood.",
    ),
    (
        "POL-MATER",
        "Wat is de kerntaak van de materfamilias?",
        [
            "Aanvoerder van het leger",
            "Het huishouden leiden en de kinderen opvoeden",
            "Het bestuur van een provincie",
            "Debatten in de Senaat",
        ],
        1,
        "De materfamilias leidt het huishouden en voedt de kinderen op; ze heeft geen juridische, maar wel sociale invloed.",
    ),
    (
        "POL-LIBERI",
        "Welke toga droeg een vrijgeboren Romeins kind?",
        ["Toga virilis", "Toga picta", "Toga praetexta", "Toga candida"],
        2,
        "Vrijgeboren kinderen droegen de toga praetexta met purperen zoom; bij volwassenwording ruilden jongens die voor de witte toga virilis.",
    ),
    (
        "POL-SERVUS",
        "Hoe heet de vrijlating van een Romeinse slaaf?",
        ["Manumissio", "Patrocinium", "Adoptio", "Emancipatio"],
        0,
        "De formele vrijlating van een slaaf heet manumissio; de vrijgelatene (libertus) bleef via het patronaat verbonden aan zijn voormalige eigenaar.",
    ),
    (
        "POL-DOMUS",
        "Welke ruimte vormt het centrum van de Romeinse domus?",
        ["De bibliotheek", "Het atrium", "De stal", "De keuken"],
        1,
        "Het atrium met impluvium is het centrale ontvangstdeel van de domus.",
    ),
    (
        "POL-INSULA",
        "Wie woonden typisch in een insula?",
        [
            "Uitsluitend senatoren",
            "De gewone, minder welgestelde Romeinse bevolking",
            "Alleen slaven",
            "Alleen soldaten",
        ],
        1,
        "Insulae waren huurkazernes voor gewone burgers; meerdere verdiepingen, kleine appartementen, brandgevaar.",
    ),
    (
        "POL-LUDUS",
        "Wat was de ludus in het Romeinse onderwijs?",
        ["De retoricaschool", "De basisschool", "Een senaatsgebouw", "Een tempel"],
        1,
        "De ludus is de basisschool (lezen, schrijven, rekenen). Daarna volgen grammaticus en rhetor.",
    ),
    (
        "POL-CENA",
        "In welke ruimte at men de cena?",
        ["Atrium", "Peristylium", "Triclinium", "Tablinum"],
        2,
        "De cena werd geserveerd in het triclinium, waar men liggend op aanligbedden at.",
    ),
    (
        "POL-KLEED",
        "Welk kledingstuk was typisch voor de mannelijke Romeinse burger?",
        ["Tunica", "Stola", "Toga", "Palla"],
        2,
        "De toga is het kenmerkende kledingstuk van de mannelijke burger; de stola is voor de vrouw, de tunica een onderkleed voor iedereen.",
    ),
    (
        "POL-THERM",
        "Welke ruimte hoort NIET bij de Romeinse thermen?",
        ["Frigidarium", "Tepidarium", "Caldarium", "Tablinum"],
        3,
        "Frigidarium (koud), tepidarium (lauw) en caldarium (heet) zijn onderdelen van de thermen. Het tablinum is een kamer in de domus.",
    ),
    (
        "POL-LARES",
        "Waar in de domus werden offers gebracht aan Lares en Penates?",
        ["Bij het lararium", "In het tablinum", "In de taberna", "In het atrium bij de deur"],
        0,
        "Bij het lararium, het huisaltaar, brachten Romeinen dagelijks offers aan de Lares (beschermgeesten) en Penates (voorraadgoden).",
    ),
    (
        "POL-PATRON",
        "Wat kenmerkt de relatie tussen patronus en cliens?",
        [
            "Eenzijdige dienstbaarheid van de cliens",
            "Wederzijdse verplichtingen van bescherming en dienstverlening",
            "Uitsluitend familiebanden",
            "Alleen militaire trouw",
        ],
        1,
        "Patronus en cliens zijn wederzijds verplicht: de patronus biedt bescherming en juridische steun, de cliens verleent eer en diensten.",
    ),
    (
        "POL-OTIUM",
        "Wat is het tegenovergestelde begrip van otium?",
        ["Imperium", "Negotium", "Virtus", "Libertas"],
        1,
        "Otium (vrije tijd, studie) staat tegenover negotium (werk, handel, openbaar leven).",
    ),
    # ── Romeinse geschiedenis (SHA-C-GES-*) ────────────────────────────
    (
        "GES-INTRO",
        "Welke driedeling is gebruikelijk voor de Romeinse geschiedenis?",
        [
            "Koningschap, Republiek, Keizerrijk",
            "Alleen Republiek en Keizerrijk",
            "Vier dynastieën",
            "Zeven eeuwen",
        ],
        0,
        "Men onderscheidt koningschap (753-509 v.Chr.), Republiek (509-27 v.Chr.) en Keizerrijk (27 v.Chr.-476 n.Chr.).",
    ),
    (
        "GES-STICHT",
        "In welk jaar stichtte Romulus volgens de mythe Rome?",
        ["509 v.Chr.", "753 v.Chr.", "27 v.Chr.", "476 n.Chr."],
        1,
        "Volgens de stichtingsmythe sticht Romulus Rome in 753 v.Chr.",
    ),
    (
        "GES-KONIG",
        "Wie was de laatste koning van Rome?",
        ["Romulus", "Numa Pompilius", "Tarquinius Superbus", "Servius Tullius"],
        2,
        "Tarquinius Superbus werd in 509 v.Chr. verdreven; daarna begon de Republiek.",
    ),
    (
        "GES-REPUB",
        "In welk jaar begon de Romeinse Republiek?",
        ["753 v.Chr.", "509 v.Chr.", "27 v.Chr.", "146 v.Chr."],
        1,
        "Na de verdrijving van Tarquinius Superbus in 509 v.Chr. begon de res publica.",
    ),
    (
        "GES-SENAAT",
        "Waaruit bestonden de leden van de Senaat voornamelijk?",
        ["Zittende magistraten", "Oud-magistraten", "Legeraanvoerders", "Patronen uit het volk"],
        1,
        "De Senaat bestond uit oud-magistraten (circa 300, later 600) die het buitenlands beleid en de financiën aanstuurden.",
    ),
    (
        "GES-CONSUL",
        "Hoeveel consuls werden jaarlijks gekozen?",
        ["Een", "Twee", "Vier", "Tien"],
        1,
        "Twee consuls werden jaarlijks gekozen; collegialiteit gold als waarborg tegen machtsmisbruik.",
    ),
    (
        "GES-MAGIST",
        "Welke magistraat was verantwoordelijk voor de rechtspraak?",
        ["Praetor", "Censor", "Aedilis", "Quaestor"],
        0,
        "De praetor sprak recht. Censor doet volkstelling en zedentoezicht, aedilis openbare werken, quaestor financiën.",
    ),
    (
        "GES-COMITI",
        "Wat was de comitia centuriata?",
        [
            "Een rechtbank",
            "Een volksvergadering die magistraten koos en oorlog verklaarde",
            "Een tempel",
            "Een legerformatie",
        ],
        1,
        "De comitia centuriata koos de hoge magistraten (consul, praetor) en besloot over oorlog en vrede.",
    ),
    (
        "GES-PATRIC",
        "Welke magistratuur bevochten de plebejers tijdens de standenstrijd?",
        ["Consul suffectus", "Tribunus plebis", "Dictator", "Imperator"],
        1,
        "De plebejers verwierven het recht op eigen tribuni plebis, die hun belangen beschermden met het vetorecht.",
    ),
    (
        "GES-LEGIO",
        "Uit hoeveel soldaten bestond een Romeins legioen ongeveer?",
        ["500", "1.000", "5.000", "20.000"],
        2,
        "Een legioen telde ongeveer 5.000 milites, opgedeeld in cohorten en centuriae.",
    ),
    (
        "GES-CENTUR",
        "Hoeveel soldaten commandeerde een centurio?",
        ["20", "50", "80", "500"],
        2,
        "Een centurio voerde het bevel over een centuria van circa 80 man; in de praktijk dus minder dan honderd.",
    ),
    (
        "GES-FORUM",
        "Wat is het Forum Romanum?",
        [
            "Een amfitheater",
            "Het politieke, religieuze en commerciële hart van Rome",
            "Een havenstad",
            "Een militair kamp",
        ],
        1,
        "Het Forum Romanum is het politieke, religieuze en economische centrum van de stad, met de Curia (Senaat) en tempels.",
    ),
    (
        "GES-VIA",
        "Welke weg geldt als prototype van het Romeinse wegennet?",
        ["Via Flaminia", "Via Latina", "Via Appia", "Via Aemilia"],
        2,
        "De Via Appia (aangelegd vanaf 312 v.Chr.) geldt als prototype van de Romeinse wegen.",
    ),
    (
        "GES-CURSUS",
        "Wat is de cursus honorum?",
        [
            "Een militaire graad",
            "Een religieuze processie",
            "De vaste politieke carrièreladder",
            "Een onderwijsprogramma",
        ],
        2,
        "De cursus honorum is de vaste volgorde quaestor → aedilis → praetor → consul, met minimumleeftijden per ambt.",
    ),
    (
        "GES-PROVNC",
        "Welke functionaris bestuurde een Romeinse provincie?",
        ["Een dictator", "Een tribunus plebis", "Een proconsul of propraetor", "Een censor"],
        2,
        "Een provincie werd bestuurd door een proconsul of propraetor: een oud-magistraat met verlengd imperium.",
    ),
]


def make_item(
    suffix: str, vraag: str, options: list[str], correct_idx: int, feedback: str
) -> dict:
    node_id = f"SHA-C-{suffix}"
    return {
        "id": f"ITEM-{node_id}-001",
        "knoop_ids": [node_id],
        "type": "herkenning",
        "richting": "receptief",
        "moeilijkheid_initieel": -0.5,
        "discriminatie_initieel": 1.0,
        "verwachte_tijd_sec": 20,
        "stimulus": {"instruction": vraag, "options": options},
        "antwoord": options[correct_idx],
        "feedback": feedback,
        "bron": "handmatig",
    }


def build_items() -> dict[str, list[dict]]:
    items: dict[str, list[dict]] = {}
    for suffix, vraag, options, correct_idx, feedback in BATCH:
        item = make_item(suffix, vraag, options, correct_idx, feedback)
        Item(**item)
        items[f"SHA-C-{suffix}"] = [item]
    return items


def inject(json_path: Path, items_by_node: dict[str, list[dict]]) -> int:
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)
    added = 0
    missing = set(items_by_node.keys())
    for node in data["knopen"]:
        kid = node["id"]
        if kid in items_by_node:
            existing = {it["id"] for it in node.get("items", [])}
            new_items = [it for it in items_by_node[kid] if it["id"] not in existing]
            node.setdefault("items", []).extend(new_items)
            added += len(new_items)
            missing.discard(kid)
    if missing:
        raise SystemExit(f"Unknown node IDs: {sorted(missing)}")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return added


def main() -> None:
    items = build_items()
    added = inject(OUTPUT, items)
    print(f"F1-08b romeins: {len(items)} knopen, {added} nieuwe items toegevoegd.")
    print(f"Output: {OUTPUT}")


if __name__ == "__main__":
    main()
