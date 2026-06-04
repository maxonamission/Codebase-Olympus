#!/usr/bin/env python3
"""A4-07: Review and add missing prerequisite-edges for vocabulary orphans.

Adds edges for:
- Latin 4th/5th declension nouns → LAT-G-MORF-DECL-INTRO (general)
- Greek prepositions → GRC-G-SYNT-PREP-INTRO (if exists) or skip
- nihil → LAT-G-MORF-PRON-INTRO (indeclinable pronoun-like)

Leaves truly indeclinable words (adv, conj) as orphans — correct by design.
"""

import json
from pathlib import Path

LAT_FILE = Path("data/graph/lat_vocabulaire_leerjaar1.json")
GRC_FILE = Path("data/graph/grc_vocabulaire_leerjaar1.json")

# Manual edge assignments for orphans that should have one
EXTRA_EDGES_LAT = {
    # 4th declension → general DECL-INTRO
    "LAT-V-F01-MANUS": "LAT-G-MORF-DECL-INTRO",
    "LAT-V-F02-DOMUS": "LAT-G-MORF-DECL-INTRO",
    "LAT-V-F02-SENATUS": "LAT-G-MORF-DECL-INTRO",
    "LAT-V-F03-EXERCIT": "LAT-G-MORF-DECL-INTRO",
    "LAT-V-F03-ADVENTU": "LAT-G-MORF-DECL-INTRO",
    # 5th declension → general DECL-INTRO
    "LAT-V-F01-RES": "LAT-G-MORF-DECL-INTRO",
    "LAT-V-F01-DIES": "LAT-G-MORF-DECL-INTRO",
    # nihil (indeclinable noun-like)
    "LAT-V-F02-NIHIL": "LAT-G-MORF-PRON-INTRO",
}

# Greek prepositions → syntax prep intro (cross-file edge)
EXTRA_EDGES_GRC = {
    "GRC-V-F01-EN": "GRC-G-SYNT-PREP-INTRO",
    "GRC-V-F01-EK": "GRC-G-SYNT-PREP-INTRO",
    "GRC-V-F01-EIS": "GRC-G-SYNT-PREP-INTRO",
    "GRC-V-F01-PROS": "GRC-G-SYNT-PREP-INTRO",
    "GRC-V-F01-EPI": "GRC-G-SYNT-PREP-INTRO",
    "GRC-V-F01-KATA": "GRC-G-SYNT-PREP-INTRO",
    "GRC-V-F01-PERI": "GRC-G-SYNT-PREP-INTRO",
    "GRC-V-F01-META": "GRC-G-SYNT-PREP-INTRO",
    "GRC-V-F01-DIA": "GRC-G-SYNT-PREP-INTRO",
    "GRC-V-F01-PARA": "GRC-G-SYNT-PREP-INTRO",
    "GRC-V-F01-HUPO": "GRC-G-SYNT-PREP-INTRO",
    "GRC-V-F01-APO": "GRC-G-SYNT-PREP-INTRO",
    "GRC-V-F01-SUN": "GRC-G-SYNT-PREP-INTRO",
}


def add_edges(file_path: Path, extra: dict, label: str) -> int:
    data = json.loads(file_path.read_text("utf-8"))
    existing = {(e["source_id"], e["target_id"]) for e in data["edges"]}
    added = 0
    for target_id, source_id in extra.items():
        if (source_id, target_id) not in existing:
            data["edges"].append(
                {
                    "source_id": source_id,
                    "target_id": target_id,
                    "type": "prerequisite",
                    "encompassing_weight": 0.3,
                }
            )
            added += 1
    file_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", "utf-8")
    print(f"{label}: {added} edges toegevoegd (totaal {len(data['edges'])})")
    return added


def main() -> None:
    # Check if GRC-G-SYNT-PREP-INTRO exists in Greek grammar
    grc_gram = Path("data/graph/grc_grammatica_leerjaar1.json")
    gram_data = json.loads(grc_gram.read_text("utf-8"))
    grc_ids = {k["id"] for k in gram_data["nodes"]}

    has_prep = "GRC-G-SYNT-PREP-INTRO" in grc_ids
    if not has_prep:
        print("WARN: GRC-G-SYNT-PREP-INTRO niet gevonden — Griekse prep-edges overgeslagen")
        grc_edges = {}
    else:
        grc_edges = EXTRA_EDGES_GRC

    add_edges(LAT_FILE, EXTRA_EDGES_LAT, "Latijn")
    add_edges(GRC_FILE, grc_edges, "Grieks")

    # Validate combined graph
    from gymnasium_classica.graph.loader import load_graph
    from gymnasium_classica.graph.validation import validate_graph

    g = load_graph(Path("data/graph/"))
    r = validate_graph(g)
    print(f"\nValidatie: {r.node_count} nodes, {r.edge_count} edges")
    print(f"Valid: {r.is_valid}, Cycles: {len(r.cycles)}, Orphans: {len(r.orphan_nodes)}")

    # Show remaining orphans (should only be adv/conj/particles)
    if r.orphan_nodes:
        print(f"\nResterend orphans ({len(r.orphan_nodes)}):")
        vocab_orphans = sorted(n for n in r.orphan_nodes if "-V-" in n)
        for o in vocab_orphans:
            print(f"  {o}")
        print(f"  ({len(r.orphan_nodes) - len(vocab_orphans)} non-vocab orphans)")


if __name__ == "__main__":
    main()
