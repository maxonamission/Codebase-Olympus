#!/usr/bin/env python3
"""Generate Greek vocabulary F01 (top-75) nodes and save to JSON."""

import json
from pathlib import Path

BAND = "F01"
TAAL = "grc"
OUTPUT = Path("data/graph/grc_vocabulaire_leerjaar1.json")
WORDS = Path("data/vocab_sources/grc_f01_words.json")

# Greek has fewer specific CONJ-INTRO nodes; use CONJ-INTRO for all verbs
GRAMMAR_MAP = {
    ("noun", "1"): "GRC-G-MORF-DECL1-INTRO",
    ("noun", "2"): "GRC-G-MORF-DECL2-INTRO",
    ("noun", "3"): "GRC-G-MORF-DECL3-INTRO",
    ("verb", "them"): "GRC-G-MORF-CONJ-INTRO",
    ("verb", "cta"): "GRC-G-MORF-CONJ-INTRO",
    ("verb", "irreg"): "GRC-G-MORF-CONJ-INTRO",
    ("adj", None): "GRC-G-MORF-DECL2-INTRO",  # most adj follow o/a-declension
    ("pron", None): "GRC-G-MORF-DECL-INTRO",
    ("prep", None): None,  # no syntax PREP-INTRO for Greek yet
}

CONJ_NAMES = {"them": "thematisch", "cta": "contractum", "irreg": "onregelmatig"}

DESC_TEMPLATES = {
    "noun": "Het zelfstandig naamwoord {lemma}, {gen}: {mean}. {decl}e declinatie. Frequentieband {band}.",
    "verb": "Het werkwoord {lemma} ({mean}): {gen}. {conj_str}. Frequentieband {band}.",
    "verb_irreg": "Het werkwoord {lemma} ({mean}): onregelmatig. Frequentieband {band}.",
    "adj": "Het bijvoeglijk naamwoord {lemma}, {gen}: {mean}. Frequentieband {band}.",
    "pron": "Het voornaamwoord {lemma}: {mean}. Frequentieband {band}.",
    "prep": "Het voorzetsel {lemma} ({gen}): {mean}. Onverbuigbaar. Frequentieband {band}.",
    "conj": "Het partikel {lemma}: {mean}. Onverbuigbaar. Frequentieband {band}.",
    "adv": "Het bijwoord {lemma}: {mean}. Onverbuigbaar. Frequentieband {band}.",
}

TITEL_TEMPLATES = {
    "noun": "{lemma}, {gen} — {mean}",
    "verb": "{lemma}, {gen} — {mean}",
    "adj": "{lemma}, {gen} — {mean}",
    "pron": "{lemma} — {mean}",
    "pron_gen": "{lemma}, {gen} — {mean}",
    "prep": "{lemma} ({gen}) — {mean}",
    "conj": "{lemma} (part.) — {mean}",
    "adv": "{lemma} (bijw.) — {mean}",
}


def make_titel(w: dict) -> str:
    pos = w["pos"]
    tmpl = ("pron_gen" if w.get("gen") else "pron") if pos == "pron" else pos
    return TITEL_TEMPLATES[tmpl].format(**w)


def make_beschrijving(w: dict, band: str) -> str:
    pos = w["pos"]
    if pos == "noun":
        decl = w["conj"]
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
        "id": f"GRC-V-{band}-{w['id']}",
        "type": "V",
        "taal": TAAL,
        "titel_nl": make_titel(w),
        "titel_terminologie": None,
        "beschrijving": make_beschrijving(w, band),
        "bloom_niveau": "kennis",
        "fase": "onderbouw_1",
        "toetsbaar": True,
        "pensum_jaren": [],
        "semantisch_cluster": w["cl"],
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
        "target_id": f"GRC-V-{band}-{w['id']}",
        "type": "prerequisite",
        "encompassing_weight": 0.3,
    }


def main() -> None:
    words = json.loads(WORDS.read_text("utf-8"))
    knopen = [make_node(w, BAND) for w in words]
    edges = [e for w in words if (e := make_edge(w, BAND)) is not None]

    from gymnasium_classica.models.graph import GraphData

    data = {"knopen": knopen, "edges": edges}
    GraphData(**data)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", "utf-8")

    clusters = {}
    for k in knopen:
        c = k.get("semantisch_cluster") or "(geen)"
        clusters[c] = clusters.get(c, 0) + 1

    print(f"Band {BAND}: {len(knopen)} knopen, {len(edges)} edges")
    print(f"Output: {OUTPUT}")
    print("Clusters:")
    for c, n in sorted(clusters.items()):
        print(f"  {c}: {n}")


if __name__ == "__main__":
    main()
