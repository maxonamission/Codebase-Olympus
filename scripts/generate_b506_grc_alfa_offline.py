#!/usr/bin/env python3
"""B5-06: Generate offline_schrijven items for Greek alphabet letter nodes.

Adds 24 traceer- en kopieeroefeningen to individual letter nodes in
grc_alfabet.json.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from gymnasium_classica.models.graph import Item  # noqa: E402

# --- Greek letter data ---
# (knoop_id_suffix, upper, lower, name, tip)
LETTERS = [
    ("ALFA", "Α", "α", "alfa", "Lijkt op de Latijnse A, maar de kleine letter is rond."),
    (
        "BETA",
        "Β",
        "β",
        "bèta",
        "De kleine letter lijkt op een Duitse ß. Trek de lus naar beneden.",
    ),
    (
        "GAMMA",
        "Γ",
        "γ",
        "gamma",
        "De hoofdletter is een omgekeerde L. De kleine letter hangt onder de regel.",
    ),
    (
        "DELTA",
        "Δ",
        "δ",
        "delta",
        "De hoofdletter is een driehoek. De kleine letter lijkt op een omgekeerde 6.",
    ),
    ("EPSIL", "Ε", "ε", "epsilon", "Kort! Lijkt op een kleine halve maan of omgekeerde 3."),
    (
        "DZETA",
        "Ζ",
        "ζ",
        "dzèta",
        "De kleine letter heeft een staart onder de regel. Begin bovenaan met een horizontale streep.",
    ),
    (
        "ETA",
        "Η",
        "η",
        "èta",
        "Lang! De kleine letter lijkt op een n met een lange staart naar beneden.",
    ),
    (
        "THETA",
        "Θ",
        "θ",
        "thèta",
        "Een cirkel met een horizontale streep erdoor (hoofdletter) of een ronde 0 met bovenstok.",
    ),
    ("IOTA", "Ι", "ι", "iota", "De eenvoudigste letter: één verticale streep. Geen punt erboven."),
    (
        "KAPPA",
        "Κ",
        "κ",
        "kappa",
        "Lijkt sterk op de Latijnse K. De kleine letter heeft twee schuine streepjes.",
    ),
    (
        "LAMBD",
        "Λ",
        "λ",
        "lambda",
        "De hoofdletter is een omgekeerde V. De kleine letter begint met een bovenstok.",
    ),
    (
        "MU",
        "Μ",
        "μ",
        "mu",
        "De hoofdletter = M. De kleine letter heeft een staart onder de regel.",
    ),
    (
        "NU",
        "Ν",
        "ν",
        "nu",
        "Valse vriend! De hoofdletter = N, maar de kleine letter lijkt op een v.",
    ),
    (
        "XI",
        "Ξ",
        "ξ",
        "xi",
        "Drie horizontale strepen (hoofdletter). De kleine letter kronkelt naar beneden.",
    ),
    (
        "OMIKR",
        "Ο",
        "ο",
        "omikron",
        "Kort! Identiek aan de Latijnse O/o. Let op: niet verwarren met omega.",
    ),
    (
        "PI",
        "Π",
        "π",
        "pi",
        "De hoofdletter lijkt op een poort. De kleine letter heeft twee poten.",
    ),
    (
        "RHO",
        "Ρ",
        "ρ",
        "rho",
        "Valse vriend! Lijkt op P/p maar is een R-klank. Kleine letter hangt onder de regel.",
    ),
    (
        "SIGMA",
        "Σ",
        "σ/ς",
        "sigma",
        "Twee vormen! σ midden in een woord, ς aan het einde. De hoofdletter heeft puntige hoeken.",
    ),
    (
        "TAU",
        "Τ",
        "τ",
        "tau",
        "Lijkt op de Latijnse T/t. De kleine letter is een kort streepje met een boog.",
    ),
    ("UPSIL", "Υ", "υ", "upsilon", "Valse vriend! Lijkt op Y, maar klinkt als u of uu."),
    (
        "PHI",
        "Φ",
        "φ",
        "phi",
        "Een cirkel met een verticale streep erdoor. De kleine letter steekt boven en onder uit.",
    ),
    ("CHI", "Χ", "χ", "chi", "Valse vriend! Lijkt op X, maar klinkt als ch (als in 'loch')."),
    (
        "PSI",
        "Ψ",
        "ψ",
        "psi",
        "Een drietand. De kleine letter lijkt op een drietand met een staart.",
    ),
    (
        "OMEGA",
        "Ω",
        "ω",
        "omega",
        "Lang! De hoofdletter is een hoefijzer. De kleine letter lijkt op een w.",
    ),
]


def next_item_nr(knoop: dict) -> int:
    """Return the next available item number for a node."""
    existing = knoop.get("items", [])
    max_nr = 0
    for item in existing:
        parts = item["id"].rsplit("-", 1)
        if len(parts) == 2 and parts[1].isdigit():
            max_nr = max(max_nr, int(parts[1]))
    return max_nr + 1


def main():
    data_dir = ROOT / "data" / "graph"
    fpath = data_dir / "grc_alfabet.json"

    with open(fpath) as f:
        graph = json.load(f)

    node_index = {k["id"]: k for k in graph["knopen"]}
    added = 0

    for suffix, upper, lower, name, tip in LETTERS:
        knoop_id = f"GRC-G-FONL-ALFA-{suffix}"
        if knoop_id not in node_index:
            print(f"  SKIP: {knoop_id} not found")
            continue

        node = node_index[knoop_id]
        nr = next_item_nr(node)

        item_data = {
            "id": f"ITEM-{knoop_id}-{nr:03d}",
            "knoop_ids": [knoop_id],
            "type": "offline_schrijven",
            "richting": "productief",
            "moeilijkheid_initieel": -0.5,
            "discriminatie_initieel": 1.0,
            "verwachte_tijd_sec": 60,
            "stimulus": (
                f"Schrijf de Griekse letter {name} vijf keer op papier: "
                f"hoofdletter ({upper}) en kleine letter ({lower}). "
                f"Let op de schrijfrichting en verhoudingen."
            ),
            "antwoord": f"Controleer je lettervormen met het voorbeeld: {upper} {lower}.",
            "feedback": tip,
            "bron": "handmatig",
            "verificatie_methode": "self_report",
            "verwacht_resultaat": f"5× {upper} en 5× {lower} — herkenbare lettervorm",
        }

        # Validate via Pydantic
        Item(**item_data)

        if "items" not in node:
            node["items"] = []
        node["items"].append(item_data)
        added += 1

    # Write back
    with open(fpath, "w") as f:
        json.dump(graph, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print("\n=== B5-06: Grieks alfabet schrijfoefeningen ===")
    print("Bestand: grc_alfabet.json")
    print(f"Totaal toegevoegd: {added} items")
    print(f"Letters: {', '.join(l[3] for l in LETTERS[:12])}...")


if __name__ == "__main__":
    main()
