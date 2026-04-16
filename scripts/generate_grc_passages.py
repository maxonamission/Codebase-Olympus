#!/usr/bin/env python3
"""Generate Greek reading passages for leerjaar 1 and write to data/passages/.

Each passage has per-word annotations (lemma, morphology, Dutch translation)
and a list of knoop_ids that the passage exercises. All Greek uses polytonic.

Run: python scripts/generate_grc_passages.py
"""

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
GRAPH_DIR = DATA_DIR / "graph"
OUTPUT_DIR = DATA_DIR / "passages"


def load_all_knoop_ids() -> set[str]:
    """Load all knoop IDs from graph JSON files for validation."""
    ids: set[str] = set()
    for p in GRAPH_DIR.glob("*.json"):
        with open(p, encoding="utf-8") as f:
            data = json.load(f)
        for k in data.get("knopen", []):
            ids.add(k["id"])
    return ids


def w(vorm: str, lemma: str, morfologie: str, vertaling_nl: str) -> dict:
    return {
        "vorm": vorm,
        "lemma": lemma,
        "morfologie": morfologie,
        "vertaling_nl": vertaling_nl,
    }


def zin(grieks: str, vertaling_nl: str, woorden: list[dict]) -> dict:
    return {"grieks": grieks, "vertaling_nl": vertaling_nl, "woorden": woorden}


def passage(
    nr: int, titel_nl: str, niveau: int, label: str,
    zinnen: list[dict], knoop_ids: list[str],
) -> dict:
    return {
        "id": f"GRC-PASS-LJ1-{nr:03d}",
        "titel_nl": titel_nl,
        "niveau": niveau,
        "complexiteit_label": label,
        "zinnen": zinnen,
        "knoop_ids": knoop_ids,
    }


# ---------------------------------------------------------------------------
# Batch 1: passages 1-5 — o-declinatie (D2) nom+acc, εἰμί, lidwoord
# ---------------------------------------------------------------------------

BATCH_1 = [
    passage(
        1, "De mens en de god", 1, "d2_nom_eimi_lidw",
        zinnen=[
            zin("ὁ ἄνθρωπος ἀγαθός ἐστιν.", "De mens is goed.", [
                w("ὁ", "ὁ/ἡ/τό", "nom.sg.m — lidwoord", "de"),
                w("ἄνθρωπος", "ἄνθρωπος", "nom.sg.m — 2e decl.", "mens"),
                w("ἀγαθός", "ἀγαθός", "nom.sg.m — adj. D1/D2", "goed"),
                w("ἐστιν", "εἰμί", "praes.ind. 3sg", "is"),
            ]),
            zin("ὁ θεὸς σοφός ἐστιν.", "De god is wijs.", [
                w("ὁ", "ὁ/ἡ/τό", "nom.sg.m — lidwoord", "de"),
                w("θεὸς", "θεός", "nom.sg.m — 2e decl.", "god"),
                w("σοφός", "σοφός", "nom.sg.m — adj. D1/D2", "wijs"),
                w("ἐστιν", "εἰμί", "praes.ind. 3sg", "is"),
            ]),
        ],
        knoop_ids=[
            "GRC-G-MORF-NOM-D2", "GRC-G-MORF-DECL2-INTRO",
            "GRC-G-MORF-PRAES-EIMI", "GRC-G-MORF-LIDW-INTRO",
            "GRC-G-MORF-ADJ-D12-2U", "GRC-G-SYNT-NOM-FUNCTIE",
            "GRC-V-F01-ANTHRO", "GRC-V-F01-AGATHO", "GRC-V-F01-EIMI",
            "GRC-V-F01-THEOS", "GRC-V-F01-SOPHOS", "GRC-V-F01-ARTIC",
        ],
    ),
    passage(
        2, "De slaaf en het paard", 2, "d2_nom_eimi_lidw",
        zinnen=[
            zin("ὁ δοῦλος ἀγαθός ἐστιν.", "De slaaf is goed.", [
                w("ὁ", "ὁ/ἡ/τό", "nom.sg.m — lidwoord", "de"),
                w("δοῦλος", "δοῦλος", "nom.sg.m — 2e decl.", "slaaf"),
                w("ἀγαθός", "ἀγαθός", "nom.sg.m — adj. D1/D2", "goed"),
                w("ἐστιν", "εἰμί", "praes.ind. 3sg", "is"),
            ]),
            zin("ὁ ἵππος καλός ἐστιν.", "Het paard is mooi.", [
                w("ὁ", "ὁ/ἡ/τό", "nom.sg.m — lidwoord", "het"),
                w("ἵππος", "ἵππος", "nom.sg.m — 2e decl.", "paard"),
                w("καλός", "καλός", "nom.sg.m — adj. D1/D2", "mooi"),
                w("ἐστιν", "εἰμί", "praes.ind. 3sg", "is"),
            ]),
            zin("ὁ οἶκος νέος ἐστίν.", "Het huis is nieuw.", [
                w("ὁ", "ὁ/ἡ/τό", "nom.sg.m — lidwoord", "het"),
                w("οἶκος", "οἶκος", "nom.sg.m — 2e decl.", "huis"),
                w("νέος", "νέος", "nom.sg.m — adj. D1/D2", "nieuw"),
                w("ἐστίν", "εἰμί", "praes.ind. 3sg", "is"),
            ]),
        ],
        knoop_ids=[
            "GRC-G-MORF-NOM-D2", "GRC-G-MORF-DECL2-INTRO",
            "GRC-G-MORF-PRAES-EIMI", "GRC-G-MORF-LIDW-INTRO",
            "GRC-G-MORF-ADJ-D12-2U",
            "GRC-V-F02-DOULOS", "GRC-V-F01-AGATHO", "GRC-V-F01-EIMI",
            "GRC-V-F01-HIPPOS", "GRC-V-F01-KALOS", "GRC-V-F02-OIKOS",
            "GRC-V-F01-NEOS", "GRC-V-F01-ARTIC",
        ],
    ),
    passage(
        3, "De mens heeft een paard", 3, "d2_nom_acc_eimi",
        zinnen=[
            zin("ὁ ἄνθρωπος ἵππον ἔχει.", "De mens heeft een paard.", [
                w("ὁ", "ὁ/ἡ/τό", "nom.sg.m — lidwoord", "de"),
                w("ἄνθρωπος", "ἄνθρωπος", "nom.sg.m — 2e decl.", "mens"),
                w("ἵππον", "ἵππος", "acc.sg.m — 2e decl.", "paard"),
                w("ἔχει", "ἔχω", "praes.ind.act. 3sg — -ω verb", "heeft"),
            ]),
            zin("ὁ δοῦλος τὸν ἵππον ἄγει.", "De slaaf leidt het paard.", [
                w("ὁ", "ὁ/ἡ/τό", "nom.sg.m — lidwoord", "de"),
                w("δοῦλος", "δοῦλος", "nom.sg.m — 2e decl.", "slaaf"),
                w("τὸν", "ὁ/ἡ/τό", "acc.sg.m — lidwoord", "het"),
                w("ἵππον", "ἵππος", "acc.sg.m — 2e decl.", "paard"),
                w("ἄγει", "ἄγω", "praes.ind.act. 3sg — -ω verb", "leidt"),
            ]),
            zin("ὁ ἄνθρωπος τὸν δοῦλον ἔχει.", "De mens heeft een slaaf.", [
                w("ὁ", "ὁ/ἡ/τό", "nom.sg.m — lidwoord", "de"),
                w("ἄνθρωπος", "ἄνθρωπος", "nom.sg.m — 2e decl.", "mens"),
                w("τὸν", "ὁ/ἡ/τό", "acc.sg.m — lidwoord", "de"),
                w("δοῦλον", "δοῦλος", "acc.sg.m — 2e decl.", "slaaf"),
                w("ἔχει", "ἔχω", "praes.ind.act. 3sg — -ω verb", "heeft"),
            ]),
        ],
        knoop_ids=[
            "GRC-G-MORF-NOM-D2", "GRC-G-MORF-ACC-D2",
            "GRC-G-MORF-DECL2-INTRO", "GRC-G-MORF-DECL2-MASC",
            "GRC-G-MORF-LIDW-INTRO", "GRC-G-MORF-LIDW-VERBG",
            "GRC-G-MORF-PRAES-THEM", "GRC-G-SYNT-ACC-FUNCTIE",
            "GRC-V-F01-ANTHRO", "GRC-V-F01-HIPPOS", "GRC-V-F01-ECHO",
            "GRC-V-F02-DOULOS", "GRC-V-F01-AGO", "GRC-V-F01-ARTIC",
        ],
    ),
    passage(
        4, "Het werk en het geschenk", 4, "d2_nom_acc_neut",
        zinnen=[
            zin("τὸ ἔργον καλόν ἐστιν.", "Het werk is mooi.", [
                w("τὸ", "ὁ/ἡ/τό", "nom.sg.n — lidwoord", "het"),
                w("ἔργον", "ἔργον", "nom.sg.n — 2e decl.", "werk"),
                w("καλόν", "καλός", "nom.sg.n — adj. D1/D2", "mooi"),
                w("ἐστιν", "εἰμί", "praes.ind. 3sg", "is"),
            ]),
            zin("ὁ δοῦλος τὸ ἔργον ἔχει.", "De slaaf heeft het werk.", [
                w("ὁ", "ὁ/ἡ/τό", "nom.sg.m — lidwoord", "de"),
                w("δοῦλος", "δοῦλος", "nom.sg.m — 2e decl.", "slaaf"),
                w("τὸ", "ὁ/ἡ/τό", "acc.sg.n — lidwoord", "het"),
                w("ἔργον", "ἔργον", "acc.sg.n — 2e decl.", "werk"),
                w("ἔχει", "ἔχω", "praes.ind.act. 3sg — -ω verb", "heeft"),
            ]),
            zin("ὁ ἄνθρωπος τὸ δῶρον φέρει.", "De mens brengt het geschenk.", [
                w("ὁ", "ὁ/ἡ/τό", "nom.sg.m — lidwoord", "de"),
                w("ἄνθρωπος", "ἄνθρωπος", "nom.sg.m — 2e decl.", "mens"),
                w("τὸ", "ὁ/ἡ/τό", "acc.sg.n — lidwoord", "het"),
                w("δῶρον", "δῶρον", "acc.sg.n — 2e decl.", "geschenk"),
                w("φέρει", "φέρω", "praes.ind.act. 3sg — -ω verb", "brengt"),
            ]),
        ],
        knoop_ids=[
            "GRC-G-MORF-NOM-D2", "GRC-G-MORF-ACC-D2",
            "GRC-G-MORF-DECL2-INTRO", "GRC-G-MORF-DECL2-NEUT",
            "GRC-G-MORF-LIDW-INTRO", "GRC-G-MORF-LIDW-VERBG",
            "GRC-G-MORF-PRAES-EIMI", "GRC-G-MORF-PRAES-THEM",
            "GRC-G-MORF-ADJ-D12-2U",
            "GRC-V-F01-ERGON", "GRC-V-F01-KALOS", "GRC-V-F01-EIMI",
            "GRC-V-F02-DOULOS", "GRC-V-F01-ECHO", "GRC-V-F01-ANTHRO",
            "GRC-V-F02-DORON", "GRC-V-F01-PHERO", "GRC-V-F01-ARTIC",
        ],
    ),
    passage(
        5, "Mensen en paarden", 5, "d2_pluralis",
        zinnen=[
            zin("οἱ ἄνθρωποι ἀγαθοί εἰσιν.", "De mensen zijn goed.", [
                w("οἱ", "ὁ/ἡ/τό", "nom.pl.m — lidwoord", "de"),
                w("ἄνθρωποι", "ἄνθρωπος", "nom.pl.m — 2e decl.", "mensen"),
                w("ἀγαθοί", "ἀγαθός", "nom.pl.m — adj. D1/D2", "goed"),
                w("εἰσιν", "εἰμί", "praes.ind. 3pl", "zijn"),
            ]),
            zin("οἱ δοῦλοι τοὺς ἵππους ἄγουσιν.", "De slaven leiden de paarden.", [
                w("οἱ", "ὁ/ἡ/τό", "nom.pl.m — lidwoord", "de"),
                w("δοῦλοι", "δοῦλος", "nom.pl.m — 2e decl.", "slaven"),
                w("τοὺς", "ὁ/ἡ/τό", "acc.pl.m — lidwoord", "de"),
                w("ἵππους", "ἵππος", "acc.pl.m — 2e decl.", "paarden"),
                w("ἄγουσιν", "ἄγω", "praes.ind.act. 3pl — -ω verb", "leiden"),
            ]),
            zin("τὰ ἔργα καλά ἐστιν.", "De werken zijn mooi.", [
                w("τὰ", "ὁ/ἡ/τό", "nom.pl.n — lidwoord", "de"),
                w("ἔργα", "ἔργον", "nom.pl.n — 2e decl.", "werken"),
                w("καλά", "καλός", "nom.pl.n — adj. D1/D2", "mooi"),
                w("ἐστιν", "εἰμί", "praes.ind. 3sg (neutr.pl.!)", "zijn"),
            ]),
        ],
        knoop_ids=[
            "GRC-G-MORF-NOM-D2", "GRC-G-MORF-ACC-D2",
            "GRC-G-MORF-DECL2-INTRO", "GRC-G-MORF-DECL2-MASC",
            "GRC-G-MORF-DECL2-NEUT", "GRC-G-MORF-NUMERUS-INTRO",
            "GRC-G-MORF-PRAES-EIMI", "GRC-G-MORF-PRAES-THEM",
            "GRC-G-MORF-LIDW-INTRO", "GRC-G-MORF-LIDW-VERBG",
            "GRC-G-MORF-ADJ-D12-2U",
            "GRC-V-F01-ANTHRO", "GRC-V-F01-AGATHO", "GRC-V-F01-EIMI",
            "GRC-V-F02-DOULOS", "GRC-V-F01-HIPPOS", "GRC-V-F01-AGO",
            "GRC-V-F01-ERGON", "GRC-V-F01-KALOS", "GRC-V-F01-ARTIC",
        ],
    ),
]

# ---------------------------------------------------------------------------
# Batch 2: passages 6-10 — +a-declinatie (D1), -ω verba, gen/dat
# ---------------------------------------------------------------------------

BATCH_2: list[dict] = [
    passage(
        6, "De ziel en het recht", 6, "d1_eta_gen_d2",
        zinnen=[
            zin("ἡ ψυχὴ ἀγαθή ἐστιν.", "De ziel is goed.", [
                w("ἡ", "ὁ/ἡ/τό", "nom.sg.f — lidwoord", "de"),
                w("ψυχὴ", "ψυχή", "nom.sg.f — 1e decl. (η-type)", "ziel"),
                w("ἀγαθή", "ἀγαθός", "nom.sg.f — adj. D1/D2", "goed"),
                w("ἐστιν", "εἰμί", "praes.ind. 3sg", "is"),
            ]),
            zin("ἡ δίκη καλή ἐστιν.", "Het recht is mooi/rechtvaardig.", [
                w("ἡ", "ὁ/ἡ/τό", "nom.sg.f — lidwoord", "het"),
                w("δίκη", "δίκη", "nom.sg.f — 1e decl. (η-type)", "recht"),
                w("καλή", "καλός", "nom.sg.f — adj. D1/D2", "mooi"),
                w("ἐστιν", "εἰμί", "praes.ind. 3sg", "is"),
            ]),
            zin("ἡ ψυχὴ τοῦ ἀνθρώπου ἀγαθή ἐστιν.", "De ziel van de mens is goed.", [
                w("ἡ", "ὁ/ἡ/τό", "nom.sg.f — lidwoord", "de"),
                w("ψυχὴ", "ψυχή", "nom.sg.f — 1e decl. (η-type)", "ziel"),
                w("τοῦ", "ὁ/ἡ/τό", "gen.sg.m — lidwoord", "van de"),
                w("ἀνθρώπου", "ἄνθρωπος", "gen.sg.m — 2e decl.", "mens"),
                w("ἀγαθή", "ἀγαθός", "nom.sg.f — adj. D1/D2", "goed"),
                w("ἐστιν", "εἰμί", "praes.ind. 3sg", "is"),
            ]),
        ],
        knoop_ids=[
            "GRC-G-MORF-NOM-D1", "GRC-G-MORF-DECL1-INTRO",
            "GRC-G-MORF-DECL1-ETA", "GRC-G-MORF-GEN-D2",
            "GRC-G-MORF-PRAES-EIMI", "GRC-G-MORF-LIDW-INTRO",
            "GRC-G-MORF-ADJ-D12-2U", "GRC-G-SYNT-GEN-FUNCTIE",
            "GRC-V-F01-PSYCHE", "GRC-V-F01-AGATHO", "GRC-V-F01-EIMI",
            "GRC-V-F01-DIKE", "GRC-V-F01-KALOS", "GRC-V-F01-ANTHRO",
            "GRC-V-F01-ARTIC",
        ],
    ),
    passage(
        7, "Het land en de strateeg", 7, "d1_alfa_omega_verba",
        zinnen=[
            zin("ἡ χώρα καλή ἐστιν.", "Het land is mooi.", [
                w("ἡ", "ὁ/ἡ/τό", "nom.sg.f — lidwoord", "het"),
                w("χώρα", "χώρα", "nom.sg.f — 1e decl. (α-type)", "land"),
                w("καλή", "καλός", "nom.sg.f — adj. D1/D2", "mooi"),
                w("ἐστιν", "εἰμί", "praes.ind. 3sg", "is"),
            ]),
            zin("ὁ ἄνθρωπος τὴν χώραν ἔχει.", "De mens heeft het land.", [
                w("ὁ", "ὁ/ἡ/τό", "nom.sg.m — lidwoord", "de"),
                w("ἄνθρωπος", "ἄνθρωπος", "nom.sg.m — 2e decl.", "mens"),
                w("τὴν", "ὁ/ἡ/τό", "acc.sg.f — lidwoord", "het"),
                w("χώραν", "χώρα", "acc.sg.f — 1e decl. (α-type)", "land"),
                w("ἔχει", "ἔχω", "praes.ind.act. 3sg — -ω verb", "heeft"),
            ]),
            zin("ὁ στρατηγὸς τοὺς δούλους πέμπει.", "De strateeg stuurt de slaven.", [
                w("ὁ", "ὁ/ἡ/τό", "nom.sg.m — lidwoord", "de"),
                w("στρατηγὸς", "στρατηγός", "nom.sg.m — 2e decl.", "strateeg/veldheer"),
                w("τοὺς", "ὁ/ἡ/τό", "acc.pl.m — lidwoord", "de"),
                w("δούλους", "δοῦλος", "acc.pl.m — 2e decl.", "slaven"),
                w("πέμπει", "πέμπω", "praes.ind.act. 3sg — -ω verb", "stuurt"),
            ]),
        ],
        knoop_ids=[
            "GRC-G-MORF-NOM-D1", "GRC-G-MORF-ACC-D1",
            "GRC-G-MORF-DECL1-INTRO", "GRC-G-MORF-DECL1-ALFA",
            "GRC-G-MORF-NOM-D2", "GRC-G-MORF-ACC-D2",
            "GRC-G-MORF-PRAES-EIMI", "GRC-G-MORF-PRAES-THEM",
            "GRC-G-MORF-LIDW-INTRO", "GRC-G-MORF-LIDW-VERBG",
            "GRC-V-F02-CHORA", "GRC-V-F01-KALOS", "GRC-V-F01-EIMI",
            "GRC-V-F01-ANTHRO", "GRC-V-F01-ECHO", "GRC-V-F01-STRTGS",
            "GRC-V-F02-DOULOS", "GRC-V-F01-PEMPO", "GRC-V-F01-ARTIC",
        ],
    ),
    passage(
        8, "Het paard van de strateeg", 8, "gen_d12",
        zinnen=[
            zin("ὁ ἵππος τοῦ στρατηγοῦ καλός ἐστιν.", "Het paard van de strateeg is mooi.", [
                w("ὁ", "ὁ/ἡ/τό", "nom.sg.m — lidwoord", "het"),
                w("ἵππος", "ἵππος", "nom.sg.m — 2e decl.", "paard"),
                w("τοῦ", "ὁ/ἡ/τό", "gen.sg.m — lidwoord", "van de"),
                w("στρατηγοῦ", "στρατηγός", "gen.sg.m — 2e decl.", "strateeg"),
                w("καλός", "καλός", "nom.sg.m — adj. D1/D2", "mooi"),
                w("ἐστιν", "εἰμί", "praes.ind. 3sg", "is"),
            ]),
            zin("τὸ ἔργον τοῦ δούλου ἀγαθόν ἐστιν.", "Het werk van de slaaf is goed.", [
                w("τὸ", "ὁ/ἡ/τό", "nom.sg.n — lidwoord", "het"),
                w("ἔργον", "ἔργον", "nom.sg.n — 2e decl.", "werk"),
                w("τοῦ", "ὁ/ἡ/τό", "gen.sg.m — lidwoord", "van de"),
                w("δούλου", "δοῦλος", "gen.sg.m — 2e decl.", "slaaf"),
                w("ἀγαθόν", "ἀγαθός", "nom.sg.n — adj. D1/D2", "goed"),
                w("ἐστιν", "εἰμί", "praes.ind. 3sg", "is"),
            ]),
            zin("ἡ τέχνη τῆς μάχης δεινή ἐστιν.", "De kunst van de strijd is indrukwekkend.", [
                w("ἡ", "ὁ/ἡ/τό", "nom.sg.f — lidwoord", "de"),
                w("τέχνη", "τέχνη", "nom.sg.f — 1e decl. (η-type)", "kunst/vaardigheid"),
                w("τῆς", "ὁ/ἡ/τό", "gen.sg.f — lidwoord", "van de"),
                w("μάχης", "μάχη", "gen.sg.f — 1e decl. (η-type)", "strijd"),
                w("δεινή", "δεινός", "nom.sg.f — adj. D1/D2", "indrukwekkend"),
                w("ἐστιν", "εἰμί", "praes.ind. 3sg", "is"),
            ]),
        ],
        knoop_ids=[
            "GRC-G-MORF-GEN-D1", "GRC-G-MORF-GEN-D2",
            "GRC-G-MORF-NOM-D1", "GRC-G-MORF-NOM-D2",
            "GRC-G-MORF-DECL1-ETA", "GRC-G-MORF-DECL2-MASC",
            "GRC-G-MORF-DECL2-NEUT", "GRC-G-MORF-PRAES-EIMI",
            "GRC-G-MORF-LIDW-INTRO", "GRC-G-MORF-LIDW-VERBG",
            "GRC-G-MORF-ADJ-D12-2U", "GRC-G-SYNT-GEN-FUNCTIE",
            "GRC-V-F01-HIPPOS", "GRC-V-F01-STRTGS", "GRC-V-F01-KALOS",
            "GRC-V-F01-EIMI", "GRC-V-F01-ERGON", "GRC-V-F02-DOULOS",
            "GRC-V-F01-AGATHO", "GRC-V-F02-TECHNE", "GRC-V-F01-MACHE",
            "GRC-V-F01-DEINOS", "GRC-V-F01-ARTIC",
        ],
    ),
    passage(
        9, "De mens brengt een geschenk", 9, "dat_d12",
        zinnen=[
            zin("ὁ ἄνθρωπος τῷ δούλῳ δῶρον φέρει.", "De mens brengt de slaaf een geschenk.", [
                w("ὁ", "ὁ/ἡ/τό", "nom.sg.m — lidwoord", "de"),
                w("ἄνθρωπος", "ἄνθρωπος", "nom.sg.m — 2e decl.", "mens"),
                w("τῷ", "ὁ/ἡ/τό", "dat.sg.m — lidwoord", "aan de"),
                w("δούλῳ", "δοῦλος", "dat.sg.m — 2e decl.", "slaaf"),
                w("δῶρον", "δῶρον", "acc.sg.n — 2e decl.", "geschenk"),
                w("φέρει", "φέρω", "praes.ind.act. 3sg — -ω verb", "brengt"),
            ]),
            zin("ὁ στρατηγὸς τοῖς δούλοις λέγει.", "De strateeg spreekt tot de slaven.", [
                w("ὁ", "ὁ/ἡ/τό", "nom.sg.m — lidwoord", "de"),
                w("στρατηγὸς", "στρατηγός", "nom.sg.m — 2e decl.", "strateeg"),
                w("τοῖς", "ὁ/ἡ/τό", "dat.pl.m — lidwoord", "tot/aan de"),
                w("δούλοις", "δοῦλος", "dat.pl.m — 2e decl.", "slaven"),
                w("λέγει", "λέγω", "praes.ind.act. 3sg — -ω verb", "spreekt"),
            ]),
            zin("ὁ δοῦλος τῷ ἀνθρώπῳ τὸν ἵππον ἄγει.", "De slaaf leidt het paard naar de mens.", [
                w("ὁ", "ὁ/ἡ/τό", "nom.sg.m — lidwoord", "de"),
                w("δοῦλος", "δοῦλος", "nom.sg.m — 2e decl.", "slaaf"),
                w("τῷ", "ὁ/ἡ/τό", "dat.sg.m — lidwoord", "aan/naar de"),
                w("ἀνθρώπῳ", "ἄνθρωπος", "dat.sg.m — 2e decl.", "mens"),
                w("τὸν", "ὁ/ἡ/τό", "acc.sg.m — lidwoord", "het"),
                w("ἵππον", "ἵππος", "acc.sg.m — 2e decl.", "paard"),
                w("ἄγει", "ἄγω", "praes.ind.act. 3sg — -ω verb", "leidt"),
            ]),
        ],
        knoop_ids=[
            "GRC-G-MORF-DAT-D2", "GRC-G-MORF-NOM-D2",
            "GRC-G-MORF-ACC-D2", "GRC-G-MORF-DECL2-MASC",
            "GRC-G-MORF-PRAES-THEM", "GRC-G-MORF-LIDW-VERBG",
            "GRC-G-SYNT-DAT-FUNCTIE",
            "GRC-V-F01-ANTHRO", "GRC-V-F02-DOULOS", "GRC-V-F02-DORON",
            "GRC-V-F01-PHERO", "GRC-V-F01-STRTGS", "GRC-V-F01-LEGO",
            "GRC-V-F01-HIPPOS", "GRC-V-F01-AGO", "GRC-V-F01-ARTIC",
        ],
    ),
    passage(
        10, "De strateeg schrijft een rede", 10, "d12_omega_gen_dat",
        zinnen=[
            zin("ὁ στρατηγὸς λόγον γράφει.", "De strateeg schrijft een rede.", [
                w("ὁ", "ὁ/ἡ/τό", "nom.sg.m — lidwoord", "de"),
                w("στρατηγὸς", "στρατηγός", "nom.sg.m — 2e decl.", "strateeg"),
                w("λόγον", "λόγος", "acc.sg.m — 2e decl.", "rede/woord"),
                w("γράφει", "γράφω", "praes.ind.act. 3sg — -ω verb", "schrijft"),
            ]),
            zin("ὁ δοῦλος τὸν λόγον τοῦ στρατηγοῦ φέρει.", "De slaaf brengt de rede van de strateeg.", [
                w("ὁ", "ὁ/ἡ/τό", "nom.sg.m — lidwoord", "de"),
                w("δοῦλος", "δοῦλος", "nom.sg.m — 2e decl.", "slaaf"),
                w("τὸν", "ὁ/ἡ/τό", "acc.sg.m — lidwoord", "de"),
                w("λόγον", "λόγος", "acc.sg.m — 2e decl.", "rede/woord"),
                w("τοῦ", "ὁ/ἡ/τό", "gen.sg.m — lidwoord", "van de"),
                w("στρατηγοῦ", "στρατηγός", "gen.sg.m — 2e decl.", "strateeg"),
                w("φέρει", "φέρω", "praes.ind.act. 3sg — -ω verb", "brengt"),
            ]),
            zin("ὁ ἄνθρωπος τὸν λόγον λέγει.", "De mens spreekt de rede uit.", [
                w("ὁ", "ὁ/ἡ/τό", "nom.sg.m — lidwoord", "de"),
                w("ἄνθρωπος", "ἄνθρωπος", "nom.sg.m — 2e decl.", "mens"),
                w("τὸν", "ὁ/ἡ/τό", "acc.sg.m — lidwoord", "de"),
                w("λόγον", "λόγος", "acc.sg.m — 2e decl.", "rede/woord"),
                w("λέγει", "λέγω", "praes.ind.act. 3sg — -ω verb", "spreekt"),
            ]),
            zin("τὰ ἔργα τῶν δούλων καλά ἐστιν.", "De werken van de slaven zijn mooi.", [
                w("τὰ", "ὁ/ἡ/τό", "nom.pl.n — lidwoord", "de"),
                w("ἔργα", "ἔργον", "nom.pl.n — 2e decl.", "werken"),
                w("τῶν", "ὁ/ἡ/τό", "gen.pl.m — lidwoord", "van de"),
                w("δούλων", "δοῦλος", "gen.pl.m — 2e decl.", "slaven"),
                w("καλά", "καλός", "nom.pl.n — adj. D1/D2", "mooi"),
                w("ἐστιν", "εἰμί", "praes.ind. 3sg (neutr.pl.!)", "zijn"),
            ]),
        ],
        knoop_ids=[
            "GRC-G-MORF-NOM-D2", "GRC-G-MORF-ACC-D2",
            "GRC-G-MORF-GEN-D2", "GRC-G-MORF-DECL2-MASC",
            "GRC-G-MORF-DECL2-NEUT", "GRC-G-MORF-NUMERUS-INTRO",
            "GRC-G-MORF-PRAES-EIMI", "GRC-G-MORF-PRAES-THEM",
            "GRC-G-MORF-LIDW-VERBG", "GRC-G-SYNT-GEN-FUNCTIE",
            "GRC-G-MORF-ADJ-D12-2U",
            "GRC-V-F01-STRTGS", "GRC-V-F01-LOGOS", "GRC-V-F01-GRAPHO",
            "GRC-V-F02-DOULOS", "GRC-V-F01-PHERO", "GRC-V-F01-ANTHRO",
            "GRC-V-F01-LEGO", "GRC-V-F01-ERGON", "GRC-V-F01-KALOS",
            "GRC-V-F01-EIMI", "GRC-V-F01-ARTIC",
        ],
    ),
]

# ---------------------------------------------------------------------------
# Batch 3: passages 11-15 — +imperfectum, aoristus intro, voorzetsels, D3
# ---------------------------------------------------------------------------

BATCH_3: list[dict] = []

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

ALL_PASSAGES = BATCH_1 + BATCH_2 + BATCH_3


def validate(passages: list[dict], known_ids: set[str]) -> list[str]:
    warnings = []
    for p in passages:
        for kid in p["knoop_ids"]:
            if kid not in known_ids:
                warnings.append(f"  {p['id']}: onbekend knoop_id {kid}")
    return warnings


def main() -> None:
    known = load_all_knoop_ids()
    passages = [p for p in ALL_PASSAGES if p]

    if not passages:
        print("Geen passages om te genereren.")
        sys.exit(0)

    warnings = validate(passages, known)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / "grc_leespassages_leerjaar1.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"passages": passages}, f, ensure_ascii=False, indent=2)

    print(f"Geschreven: {out_path}")
    print(f"Aantal passages: {len(passages)}")
    print(f"Totaal zinnen: {sum(len(p['zinnen']) for p in passages)}")
    total_w = sum(len(z["woorden"]) for p in passages for z in p["zinnen"])
    print(f"Totaal woorden: {total_w}")
    if warnings:
        print(f"\n⚠ {len(warnings)} onbekende knoop_ids:")
        for ww in warnings:
            print(ww)
        sys.exit(1)
    else:
        print("\n✓ Alle knoop_ids gevalideerd.")


if __name__ == "__main__":
    main()
