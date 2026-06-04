#!/usr/bin/env python3
"""B5-05: Generate offline_schrijven vertaal-op-papier items for SYNT nodes.

Adds ~30 translation exercises to syntax nodes in
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
    # === POC: naamvalfuncties & basissyntaxis ===
    (
        "LAT-G-SYNT-NOM-FUNCTIE",
        "lat_grammatica_poc.json",
        "Vertaal op papier: 'Puella cantat.' Onderstreep het onderwerp.",
        "Het meisje zingt. Onderwerp: puella (nominativus).",
        "De nominativus geeft het onderwerp aan. Puella is nom.sg. 1e declinatie.",
        -0.3,
    ),
    (
        "LAT-G-SYNT-ACC-FUNCTIE",
        "lat_grammatica_poc.json",
        "Vertaal op papier: 'Dominus servum vocat.' Markeer het lijdend voorwerp.",
        "De heer roept de slaaf. Lijdend voorwerp: servum (accusativus).",
        "De accusativus markeert het lijdend voorwerp. Servum = acc.sg. 2e declinatie.",
        -0.2,
    ),
    (
        "LAT-G-SYNT-GEN-FUNCTIE",
        "lat_grammatica_poc.json",
        "Vertaal op papier: 'Liber puellae est bonus.' Markeer de genitivus.",
        "Het boek van het meisje is goed. Genitivus: puellae.",
        "De genitivus drukt bezit uit ('van'). Puellae = gen.sg. 1e declinatie.",
        0.0,
    ),
    (
        "LAT-G-SYNT-DAT-FUNCTIE",
        "lat_grammatica_poc.json",
        "Vertaal op papier: 'Magister puero librum dat.' Markeer het meewerkend voorwerp.",
        "De leraar geeft de jongen een boek. Meewerkend voorwerp: puero (dativus).",
        "De dativus markeert het meewerkend voorwerp ('aan/voor'). Puero = dat.sg. 2e decl.",
        0.1,
    ),
    (
        "LAT-G-SYNT-ABL-FUNCTIE",
        "lat_grammatica_poc.json",
        "Vertaal op papier: 'Miles gladio pugnat.' Markeer de ablativus.",
        "De soldaat vecht met een zwaard. Ablativus: gladio (instrumentalis).",
        "De ablativus kan 'met' (instrumentalis) uitdrukken. Gladio = abl.sg. 2e declinatie.",
        0.2,
    ),
    (
        "LAT-G-SYNT-ADJ-CONGR",
        "lat_grammatica_poc.json",
        "Vertaal op papier: 'Puella bona librum magnum legit.' Let op de congruentie.",
        "Het goede meisje leest een groot boek. Bona hoort bij puella, magnum bij librum.",
        "Bijvoeglijk naamwoord stemt overeen in naamval, getal en geslacht met het zelfstandig naamwoord.",
        0.3,
    ),
    (
        "LAT-G-SYNT-PREP-ACC",
        "lat_grammatica_poc.json",
        "Vertaal op papier: 'Servi ad templum ambulant.'",
        "De slaven lopen naar de tempel. Ad + acc. = richting.",
        "Ad + accusativus drukt richting uit ('naar'). Templum = acc.sg. 2e decl. neutrum.",
        0.1,
    ),
    (
        "LAT-G-SYNT-PREP-ABL",
        "lat_grammatica_poc.json",
        "Vertaal op papier: 'Rex cum militibus venit.'",
        "De koning komt met de soldaten. Cum + abl. = samen met.",
        "Cum + ablativus drukt vergezelling uit ('met'). Militibus = abl.pl. 3e declinatie.",
        0.2,
    ),
    (
        "LAT-G-SYNT-OVEREENK",
        "lat_grammatica_poc.json",
        "Vertaal op papier: 'Puellae in horto ludunt.' Let op congruentie onderwerp-persoonsvorm.",
        "De meisjes spelen in de tuin. Puellae (pl.) → ludunt (3e pers. pl.).",
        "Onderwerp en persoonsvorm moeten overeenstemmen in getal. Meervoud → -nt uitgang.",
        0.2,
    ),
    (
        "LAT-G-SYNT-WRDVLG",
        "lat_grammatica_poc.json",
        "Vertaal op papier: 'Magnum periculum nautae timent.' Let op de Latijnse woordvolgorde.",
        "De zeelieden vrezen het grote gevaar. SOV-volgorde: object vooraan, werkwoord achteraan.",
        "Latijn heeft vrije woordvolgorde maar vaak SOV. Hier staat het object vooraan voor nadruk.",
        0.5,
    ),
    (
        "LAT-G-SYNT-ONTK",
        "lat_grammatica_poc.json",
        "Vertaal op papier: 'Servus dominum non timet.'",
        "De slaaf vreest de heer niet. Non staat direct voor het werkwoord.",
        "Non ontkent het werkwoord en staat er direct voor. Non timet = vreest niet.",
        0.0,
    ),
    (
        "LAT-G-SYNT-VRAAGZIN",
        "lat_grammatica_poc.json",
        "Vertaal op papier: 'Cur puella lacrimat?'",
        "Waarom huilt het meisje? Cur = waarom (vragend bijwoord).",
        "Latijnse vraagzinnen beginnen met een vraagwoord. Cur = waarom, quis = wie, ubi = waar.",
        0.0,
    ),
    (
        "LAT-G-SYNT-ZINSDEEL-INTRO",
        "lat_grammatica_poc.json",
        "Vertaal op papier en ontleed in zinsdelen: 'Dominus servo pecuniam dat.'",
        "De heer geeft de slaaf geld. Dominus=ow, servo=mwv, pecuniam=lv, dat=gezegde.",
        "Bepaal eerst het gezegde (pv), dan het onderwerp (nom.), lijdend vw (acc.), meewerkend vw (dat.).",
        0.4,
    ),
    # === LEERJAAR1: uitgebreide syntaxis ===
    (
        "LAT-G-SYNT-VOC-FUNCTIE",
        "lat_grammatica_leerjaar1.json",
        "Vertaal op papier: 'Serve, veni!' Markeer de vocativus.",
        "Slaaf, kom! Vocativus: serve (aanspreekvorm van servus).",
        "De vocativus is de aanspreekvorm. 2e decl. -us → -e (servus → serve).",
        -0.2,
    ),
    (
        "LAT-G-SYNT-SUBJ",
        "lat_grammatica_leerjaar1.json",
        "Vertaal op papier: 'Rex et regina in regia habitant.' Bepaal het onderwerp.",
        "De koning en de koningin wonen in het paleis. Onderwerp: rex et regina (meervoudig).",
        "Een samengesteld onderwerp staat in de nominativus. Het werkwoord is meervoud.",
        0.1,
    ),
    (
        "LAT-G-SYNT-OBJDIR",
        "lat_grammatica_leerjaar1.json",
        "Vertaal op papier: 'Milites urbem defendunt.' Onderstreep het lijdend voorwerp.",
        "De soldaten verdedigen de stad. Lijdend voorwerp: urbem (acc.sg. 3e decl.).",
        "Het lijdend voorwerp staat in de accusativus. Urbem = acc.sg. van urbs.",
        0.0,
    ),
    (
        "LAT-G-SYNT-OBJIND",
        "lat_grammatica_leerjaar1.json",
        "Vertaal op papier: 'Pater filio gladium donat.' Markeer mwv en lv.",
        "De vader schenkt zijn zoon een zwaard. Mwv: filio (dat.), lv: gladium (acc.).",
        "Meewerkend voorwerp = dativus, lijdend voorwerp = accusativus. Let op het verschil.",
        0.2,
    ),
    (
        "LAT-G-SYNT-PREP-IN",
        "lat_grammatica_leerjaar1.json",
        "Vertaal beide zinnen op papier: 'Miles in urbem currit.' / 'Miles in urbe stat.'",
        "De soldaat rent de stad in. / De soldaat staat in de stad. In+acc=richting, in+abl=plaats.",
        "In + accusativus = richting ('waarheen'). In + ablativus = plaats ('waar').",
        0.4,
    ),
    (
        "LAT-G-SYNT-PREP-RICHT",
        "lat_grammatica_leerjaar1.json",
        "Vertaal op papier: 'Nautae per mare ad insulam navigant.'",
        "De zeelieden varen over zee naar het eiland. Per+acc, ad+acc.",
        "Per = door/over, ad = naar. Beide met accusativus (richting/beweging).",
        0.3,
    ),
    (
        "LAT-G-SYNT-PREP-TIJD",
        "lat_grammatica_leerjaar1.json",
        "Vertaal op papier: 'Post proelium milites in castra redeunt.'",
        "Na de slag keren de soldaten terug naar het kamp. Post + acc = na.",
        "Post + accusativus drukt 'na' uit (tijd). In castra = richting (acc.pl.n.).",
        0.3,
    ),
    (
        "LAT-G-SYNT-PREP-HERK",
        "lat_grammatica_leerjaar1.json",
        "Vertaal op papier: 'Consul ex urbe discedit.'",
        "De consul vertrekt uit de stad. Ex + abl = uit (herkomst).",
        "Ex/e + ablativus drukt herkomst of scheiding uit. Urbe = abl.sg. 3e decl.",
        0.2,
    ),
    (
        "LAT-G-SYNT-PREP-OVERIG",
        "lat_grammatica_leerjaar1.json",
        "Vertaal op papier: 'Sine armis pugnare non possumus.'",
        "Zonder wapens kunnen wij niet vechten. Sine + abl = zonder.",
        "Sine + ablativus = 'zonder'. Armis = abl.pl. 2e decl. neutrum.",
        0.2,
    ),
    (
        "LAT-G-SYNT-GEZEGDE",
        "lat_grammatica_leerjaar1.json",
        "Vertaal op papier en markeer het gezegde: 'Milites fortes hostes vicerunt.'",
        "De dappere soldaten hebben de vijanden overwonnen. Gezegde: vicerunt (perf.).",
        "Het gezegde is de persoonsvorm. Vicerunt = 3e pers.pl. perfectum van vincere.",
        0.3,
    ),
    (
        "LAT-G-SYNT-NWG",
        "lat_grammatica_leerjaar1.json",
        "Vertaal op papier: 'Roma magna urbs est.' Bepaal het naamwoordelijk gezegde.",
        "Rome is een grote stad. Nwg: magna urbs (nom., congruent met Roma).",
        "Bij een naamwoordelijk gezegde staat het naamwoordelijk deel in de nominativus.",
        0.4,
    ),
    (
        "LAT-G-SYNT-BIJV-BEP",
        "lat_grammatica_leerjaar1.json",
        "Vertaal op papier: 'Gladius militis fortis est longus.' Markeer de bijvoeglijke bepaling.",
        "Het zwaard van de dappere soldaat is lang. Bijv. bep.: militis fortis (gen.).",
        "Een genitivus bij een zelfstandig naamwoord is een bijvoeglijke bepaling.",
        0.5,
    ),
    (
        "LAT-G-SYNT-BIJW-BEP",
        "lat_grammatica_leerjaar1.json",
        "Vertaal op papier: 'Pueri in horto laeti ludunt.' Markeer de bijwoordelijke bepaling.",
        "De jongens spelen vrolijk in de tuin. Bijw. bep. van plaats: in horto.",
        "Voorzetselgroepen (in horto) en bijwoorden fungeren als bijwoordelijke bepaling.",
        0.4,
    ),
    (
        "LAT-G-SYNT-BEPVZ",
        "lat_grammatica_leerjaar1.json",
        "Vertaal op papier: 'Pro patria pugnamus.' Bepaal de functie van de voorzetselgroep.",
        "Wij vechten voor het vaderland. Pro patria = bijw. bep. van reden/doel.",
        "Pro + ablativus = 'voor/ten behoeve van'. Voorzetselgroep als bijw. bepaling.",
        0.3,
    ),
    (
        "LAT-G-SYNT-HOOFDBIJ",
        "lat_grammatica_leerjaar1.json",
        "Vertaal op papier: 'Rex, qui bonus est, populum amat.' Markeer hoofd- en bijzin.",
        "De koning, die goed is, houdt van het volk. Hoofdzin: Rex populum amat. Bijzin: qui bonus est.",
        "De bijzin begint met een betrekkelijk voornaamwoord (qui) en geeft extra informatie.",
        0.6,
    ),
    (
        "LAT-G-SYNT-ACI-INTRO",
        "lat_grammatica_leerjaar1.json",
        "Vertaal op papier: 'Puella servum venire videt.' Herken de AcI-constructie.",
        "Het meisje ziet dat de slaaf komt. AcI: servum (acc.) + venire (inf.).",
        "AcI: accusativus (onderwerp bijzin) + infinitivus (gezegde bijzin). Vertaal met 'dat'-zin.",
        0.8,
    ),
    (
        "LAT-G-SYNT-ACI-INTRO",
        "lat_grammatica_leerjaar1.json",
        "Vertaal op papier: 'Consul milites fortes esse dicit.' Herken de AcI.",
        "De consul zegt dat de soldaten dapper zijn. AcI: milites (acc.) + fortes esse (inf.).",
        "Dicere + AcI: 'zeggen dat...'. Milites = acc.pl., fortes esse = nwg in infinitivus.",
        1.0,
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
    """Build an offline_schrijven vertaal-op-papier item dict."""
    return {
        "id": f"ITEM-{node_id}-{nr:03d}",
        "knoop_ids": [node_id],
        "type": "offline_schrijven",
        "richting": "productief",
        "moeilijkheid_initieel": moeilijkheid,
        "discriminatie_initieel": 1.0,
        "verwachte_tijd_sec": 180,
        "stimulus": stimulus,
        "antwoord": "Controleer je vertaling met de modelvertaling in de app.",
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

    print("\n=== B5-05: Vertaal-op-papier oefeningen ===")
    print(f"Totaal toegevoegd: {total_added} items")


if __name__ == "__main__":
    main()
