#!/usr/bin/env python3
"""Generate Latin vocabulary F02 (words 101-200) and append to existing file."""

import json
from pathlib import Path

BAND = "F02"
TAAL = "lat"
OUTPUT = Path("data/graph/lat_vocabulaire_leerjaar1.json")
WORDS = Path("data/vocab_sources/lat_f02_words.json")

GRAMMAR_MAP = {
    ("noun", "1"): "LAT-G-MORF-DECL1-INTRO",
    ("noun", "2"): "LAT-G-MORF-DECL2-INTRO",
    ("noun", "3"): "LAT-G-MORF-DECL3-INTRO",
    ("verb", "1"): "LAT-G-MORF-CONJ1-INTRO",
    ("verb", "2"): "LAT-G-MORF-CONJ2-INTRO",
    ("verb", "3"): "LAT-G-MORF-CONJ3-INTRO",
    ("verb", "3b"): "LAT-G-MORF-CONJ3B-INTRO",
    ("verb", "4"): "LAT-G-MORF-CONJ4-INTRO",
    ("verb", "irreg"): "LAT-G-MORF-PRAES-INTRO",
    ("adj", None): "LAT-G-MORF-ADJ-INTRO",
    ("pron", None): "LAT-G-MORF-PRON-INTRO",
    ("prep", None): "LAT-G-SYNT-PREP-INTRO",
}

DESC_TEMPLATES = {
    "noun": "Het zelfstandig naamwoord {lemma}, {gen}: {mean}. {decl}e declinatie. Frequentieband {band}.",
    "verb": "Het werkwoord {lemma} ({mean}): {gen}. {conj_str}. Frequentieband {band}.",
    "verb_irreg": "Het werkwoord {lemma} ({mean}): onregelmatig. Frequentieband {band}.",
    "adj": "Het bijvoeglijk naamwoord {lemma}, {gen}: {mean}. Frequentieband {band}.",
    "pron": "Het voornaamwoord {lemma}: {mean}. Frequentieband {band}.",
    "prep": "Het voorzetsel {lemma} ({gen}): {mean}. Onverbuigbaar. Frequentieband {band}.",
    "conj": "Het voegwoord {lemma}: {mean}. Onverbuigbaar. Frequentieband {band}.",
    "adv": "Het bijwoord {lemma}: {mean}. Onverbuigbaar. Frequentieband {band}.",
}

TITEL_TEMPLATES = {
    "noun": "{lemma}, {gen} — {mean}",
    "verb": "{lemma}, {gen} — {mean}",
    "adj": "{lemma}, {gen} — {mean}",
    "pron": "{lemma} — {mean}",
    "pron_gen": "{lemma}, {gen} — {mean}",
    "prep": "{lemma} ({gen}) — {mean}",
    "conj": "{lemma} (voegw.) — {mean}",
    "adv": "{lemma} (bijw.) — {mean}",
}

CONJ_NAMES = {
    "1": "1e conjugatie",
    "2": "2e conjugatie",
    "3": "3e conjugatie",
    "3b": "3e conjugatie (-io)",
    "4": "4e conjugatie",
}


def make_titel(w: dict) -> str:
    pos = w["pos"]
    if pos == "pron":
        tmpl = "pron_gen" if w.get("gen") else "pron"
    elif pos in TITEL_TEMPLATES:
        tmpl = pos
    else:
        tmpl = pos
    return TITEL_TEMPLATES[tmpl].format(**w)


def make_beschrijving(w: dict, band: str) -> str:
    pos = w["pos"]
    if pos == "noun":
        decl = w["conj"]
        if decl is None:
            return f"Het zelfstandig naamwoord {w['lemma']}: {w['mean']}. Onverbuigbaar. Frequentieband {band}."
        return DESC_TEMPLATES["noun"].format(
            lemma=w["lemma"], gen=w["gen"], mean=w["mean"], decl=decl, band=band
        )
    elif pos == "verb":
        if w["conj"] == "irreg":
            return DESC_TEMPLATES["verb_irreg"].format(lemma=w["lemma"], mean=w["mean"], band=band)
        return DESC_TEMPLATES["verb"].format(
            lemma=w["lemma"],
            gen=w["gen"],
            mean=w["mean"],
            conj_str=CONJ_NAMES[w["conj"]],
            band=band,
        )
    elif pos == "adj":
        return DESC_TEMPLATES["adj"].format(
            lemma=w["lemma"], gen=w["gen"], mean=w["mean"], band=band
        )
    elif pos in ("conj", "adv", "prep"):
        return DESC_TEMPLATES[pos].format(
            lemma=w["lemma"], gen=w.get("gen", ""), mean=w["mean"], band=band
        )
    elif pos == "pron":
        return DESC_TEMPLATES["pron"].format(lemma=w["lemma"], mean=w["mean"], band=band)
    return f"{w['lemma']}: {w['mean']}. Frequentieband {band}."


def make_node(w: dict, band: str) -> dict:
    return {
        "id": f"LAT-V-{band}-{w['id']}",
        "type": "V",
        "language": TAAL,
        "title_nl": make_titel(w),
        "title_terminology": None,
        "description": make_beschrijving(w, band),
        "bloom_level": "knowledge",
        "phase": "onderbouw_1",
        "testable": True,
        "pensum_years": [],
        "semantic_cluster": w["cl"],
        "items": [],
    }


def make_edge(w: dict, band: str) -> dict | None:
    pos = w["pos"]
    conj = w.get("conj")
    key = (pos, conj) if pos in ("noun", "verb") else (pos, None)
    target = GRAMMAR_MAP.get(key)
    if not target:
        return None
    return {
        "source_id": target,
        "target_id": f"LAT-V-{band}-{w['id']}",
        "type": "prerequisite",
        "encompassing_weight": 0.3,
    }


def main() -> None:
    # Load existing data
    existing = json.loads(OUTPUT.read_text("utf-8"))
    existing_ids = {k["id"] for k in existing["nodes"]}

    # Generate new nodes
    words = json.loads(WORDS.read_text("utf-8"))
    new_knopen = [make_node(w, BAND) for w in words]
    new_edges = [e for w in words if (e := make_edge(w, BAND)) is not None]

    # Check for duplicates
    for k in new_knopen:
        assert k["id"] not in existing_ids, f"Duplicate ID: {k['id']}"

    # Merge
    existing["nodes"].extend(new_knopen)
    existing["edges"].extend(new_edges)

    # Validate via Pydantic
    from gymnasium_classica.models.graph import GraphData

    GraphData(**existing)

    OUTPUT.write_text(json.dumps(existing, ensure_ascii=False, indent=2) + "\n", "utf-8")

    # Summary
    clusters = {}
    for k in new_knopen:
        c = k.get("semantic_cluster") or "(geen)"
        clusters[c] = clusters.get(c, 0) + 1

    total_k = len(existing["nodes"])
    total_e = len(existing["edges"])
    print(f"Band {BAND}: {len(new_knopen)} nieuwe nodes, {len(new_edges)} nieuwe edges")
    print(f"Totaal in bestand: {total_k} nodes, {total_e} edges")
    print(f"Output: {OUTPUT}")
    print("Nieuwe clusters:")
    for c, n in sorted(clusters.items()):
        print(f"  {c}: {n}")


if __name__ == "__main__":
    main()
