#!/usr/bin/env python3
"""Generate Latin reading passages for leerjaar 1 and write to data/passages/.

Each passage has per-word annotations (lemma, morphology, Dutch translation)
and a list of node_ids that the passage exercises.

Run: python scripts/generate_lat_passages.py
"""

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
GRAPH_DIR = DATA_DIR / "graph"
OUTPUT_DIR = DATA_DIR / "passages"


def load_all_node_ids() -> set[str]:
    """Load all node IDs from graph JSON files for validation."""
    ids: set[str] = set()
    for p in GRAPH_DIR.glob("*.json"):
        with open(p, encoding="utf-8") as f:
            data = json.load(f)
        for k in data.get("nodes", []):
            ids.add(k["id"])
    return ids


def w(vorm: str, lemma: str, morfologie: str, vertaling_nl: str) -> dict:
    """Shorthand for a word annotation."""
    return {
        "vorm": vorm,
        "lemma": lemma,
        "morfologie": morfologie,
        "vertaling_nl": vertaling_nl,
    }


def zin(latijn: str, vertaling_nl: str, woorden: list[dict]) -> dict:
    """Shorthand for a sentence."""
    return {"latijn": latijn, "vertaling_nl": vertaling_nl, "woorden": woorden}


def passage(
    nr: int,
    title_nl: str,
    niveau: int,
    label: str,
    zinnen: list[dict],
    node_ids: list[str],
) -> dict:
    """Build a passage dict."""
    return {
        "id": f"LAT-PASS-LJ1-{nr:03d}",
        "title_nl": title_nl,
        "niveau": niveau,
        "complexiteit_label": label,
        "zinnen": zinnen,
        "node_ids": node_ids,
    }


# ---------------------------------------------------------------------------
# Batch 1: passages 1-5 — nominativus + accusativus + presens (D1/D2, C1/C2)
# ---------------------------------------------------------------------------

BATCH_1 = [
    passage(
        1,
        "Puella en de slaaf",
        1,
        "nom_acc_praes_d12_c12",
        zinnen=[
            zin(
                "Puella aquam portat.",
                "Het meisje draagt water.",
                [
                    w("Puella", "puella", "nom.sg.f — 1e decl.", "meisje"),
                    w("aquam", "aqua", "acc.sg.f — 1e decl.", "water"),
                    w("portat", "porto", "praes.ind.act. 3sg — 1e conj.", "draagt"),
                ],
            ),
            zin(
                "Servus equum videt.",
                "De slaaf ziet het paard.",
                [
                    w("Servus", "servus", "nom.sg.m — 2e decl.", "slaaf"),
                    w("equum", "equus", "acc.sg.m — 2e decl.", "paard"),
                    w("videt", "video", "praes.ind.act. 3sg — 2e conj.", "ziet"),
                ],
            ),
        ],
        node_ids=[
            "LAT-G-MORF-NOM-D1",
            "LAT-G-MORF-NOM-D2",
            "LAT-G-MORF-ACC-D1",
            "LAT-G-MORF-ACC-D2",
            "LAT-G-MORF-PRAES-C1-ACT",
            "LAT-G-MORF-PRAES-C2-ACT",
            "LAT-V-F02-PUELLA",
            "LAT-V-F01-AQUA",
            "LAT-V-F02-PORTO",
            "LAT-V-F01-SERVUS",
            "LAT-V-F02-EQUUS",
            "LAT-V-F01-VIDEO",
        ],
    ),
    passage(
        2,
        "De meester roept",
        2,
        "nom_acc_praes_d12_c12",
        zinnen=[
            zin(
                "Dominus servum vocat.",
                "De meester roept de slaaf.",
                [
                    w("Dominus", "dominus", "nom.sg.m — 2e decl.", "meester/heer"),
                    w("servum", "servus", "acc.sg.m — 2e decl.", "slaaf"),
                    w("vocat", "voco", "praes.ind.act. 3sg — 1e conj.", "roept"),
                ],
            ),
            zin(
                "Servus dominum timet.",
                "De slaaf vreest de meester.",
                [
                    w("Servus", "servus", "nom.sg.m — 2e decl.", "slaaf"),
                    w("dominum", "dominus", "acc.sg.m — 2e decl.", "meester/heer"),
                    w("timet", "timeo", "praes.ind.act. 3sg — 2e conj.", "vreest"),
                ],
            ),
            zin(
                "Filia aquam portat.",
                "De dochter draagt water.",
                [
                    w("Filia", "filia", "nom.sg.f — 1e decl.", "dochter"),
                    w("aquam", "aqua", "acc.sg.f — 1e decl.", "water"),
                    w("portat", "porto", "praes.ind.act. 3sg — 1e conj.", "draagt"),
                ],
            ),
        ],
        node_ids=[
            "LAT-G-MORF-NOM-D1",
            "LAT-G-MORF-NOM-D2",
            "LAT-G-MORF-ACC-D1",
            "LAT-G-MORF-ACC-D2",
            "LAT-G-MORF-PRAES-C1-ACT",
            "LAT-G-MORF-PRAES-C2-ACT",
            "LAT-V-F01-DOMINUS",
            "LAT-V-F01-SERVUS",
            "LAT-V-F01-VOCO",
            "LAT-V-F01-TIMEO",
            "LAT-V-F01-FILIA",
            "LAT-V-F01-AQUA",
            "LAT-V-F02-PORTO",
        ],
    ),
    passage(
        3,
        "Bij de villa",
        3,
        "nom_acc_praes_d12_c12",
        zinnen=[
            zin(
                "Servi villam vident.",
                "De slaven zien de villa.",
                [
                    w("Servi", "servus", "nom.pl.m — 2e decl.", "slaven"),
                    w("villam", "villa", "acc.sg.f — 1e decl.", "villa/landhuis"),
                    w("vident", "video", "praes.ind.act. 3pl — 2e conj.", "zien"),
                ],
            ),
            zin(
                "Puellae aquam portant.",
                "De meisjes dragen water.",
                [
                    w("Puellae", "puella", "nom.pl.f — 1e decl.", "meisjes"),
                    w("aquam", "aqua", "acc.sg.f — 1e decl.", "water"),
                    w("portant", "porto", "praes.ind.act. 3pl — 1e conj.", "dragen"),
                ],
            ),
            zin(
                "Dominus filium amat.",
                "De meester houdt van zijn zoon.",
                [
                    w("Dominus", "dominus", "nom.sg.m — 2e decl.", "meester/heer"),
                    w("filium", "filius", "acc.sg.m — 2e decl.", "zoon"),
                    w("amat", "amo", "praes.ind.act. 3sg — 1e conj.", "houdt van"),
                ],
            ),
        ],
        node_ids=[
            "LAT-G-MORF-NOM-D1",
            "LAT-G-MORF-NOM-D2",
            "LAT-G-MORF-ACC-D1",
            "LAT-G-MORF-ACC-D2",
            "LAT-G-MORF-PRAES-C1-ACT",
            "LAT-G-MORF-PRAES-C2-ACT",
            "LAT-G-MORF-NUMERUS-INTRO",
            "LAT-V-F01-SERVUS",
            "LAT-V-F02-VILLA",
            "LAT-V-F01-VIDEO",
            "LAT-V-F02-PUELLA",
            "LAT-V-F01-AQUA",
            "LAT-V-F02-PORTO",
            "LAT-V-F01-DOMINUS",
            "LAT-V-F01-FILIUS",
            "LAT-V-F01-AMO",
        ],
    ),
    passage(
        4,
        "Zoon en dochter",
        4,
        "nom_acc_praes_d12_c12",
        zinnen=[
            zin(
                "Filius equum habet.",
                "De zoon heeft een paard.",
                [
                    w("Filius", "filius", "nom.sg.m — 2e decl.", "zoon"),
                    w("equum", "equus", "acc.sg.m — 2e decl.", "paard"),
                    w("habet", "habeo", "praes.ind.act. 3sg — 2e conj.", "heeft"),
                ],
            ),
            zin(
                "Filia silvam amat.",
                "De dochter houdt van het bos.",
                [
                    w("Filia", "filia", "nom.sg.f — 1e decl.", "dochter"),
                    w("silvam", "silva", "acc.sg.f — 1e decl.", "bos"),
                    w("amat", "amo", "praes.ind.act. 3sg — 1e conj.", "houdt van"),
                ],
            ),
            zin(
                "Servus filium et filiam vocat.",
                "De slaaf roept de zoon en de dochter.",
                [
                    w("Servus", "servus", "nom.sg.m — 2e decl.", "slaaf"),
                    w("filium", "filius", "acc.sg.m — 2e decl.", "zoon"),
                    w("et", "et", "nevenschikkend voegwoord", "en"),
                    w("filiam", "filia", "acc.sg.f — 1e decl.", "dochter"),
                    w("vocat", "voco", "praes.ind.act. 3sg — 1e conj.", "roept"),
                ],
            ),
        ],
        node_ids=[
            "LAT-G-MORF-NOM-D1",
            "LAT-G-MORF-NOM-D2",
            "LAT-G-MORF-ACC-D1",
            "LAT-G-MORF-ACC-D2",
            "LAT-G-MORF-PRAES-C1-ACT",
            "LAT-G-MORF-PRAES-C2-ACT",
            "LAT-V-F01-FILIUS",
            "LAT-V-F02-EQUUS",
            "LAT-V-F01-HABEO",
            "LAT-V-F01-FILIA",
            "LAT-V-F01-SILVA",
            "LAT-V-F01-AMO",
            "LAT-V-F01-SERVUS",
            "LAT-V-F01-ET",
            "LAT-V-F01-VOCO",
        ],
    ),
    passage(
        5,
        "Jongens en meisjes",
        5,
        "nom_acc_praes_d12_c12",
        zinnen=[
            zin(
                "Pueri equos amant.",
                "De jongens houden van de paarden.",
                [
                    w("Pueri", "puer", "nom.pl.m — 2e decl.", "jongens"),
                    w("equos", "equus", "acc.pl.m — 2e decl.", "paarden"),
                    w("amant", "amo", "praes.ind.act. 3pl — 1e conj.", "houden van"),
                ],
            ),
            zin(
                "Puellae viam vident.",
                "De meisjes zien de weg.",
                [
                    w("Puellae", "puella", "nom.pl.f — 1e decl.", "meisjes"),
                    w("viam", "via", "acc.sg.f — 1e decl.", "weg"),
                    w("vident", "video", "praes.ind.act. 3pl — 2e conj.", "zien"),
                ],
            ),
            zin(
                "Dominus servos vocat.",
                "De meester roept de slaven.",
                [
                    w("Dominus", "dominus", "nom.sg.m — 2e decl.", "meester/heer"),
                    w("servos", "servus", "acc.pl.m — 2e decl.", "slaven"),
                    w("vocat", "voco", "praes.ind.act. 3sg — 1e conj.", "roept"),
                ],
            ),
            zin(
                "Servi dominum timent.",
                "De slaven vrezen de meester.",
                [
                    w("Servi", "servus", "nom.pl.m — 2e decl.", "slaven"),
                    w("dominum", "dominus", "acc.sg.m — 2e decl.", "meester/heer"),
                    w("timent", "timeo", "praes.ind.act. 3pl — 2e conj.", "vrezen"),
                ],
            ),
        ],
        node_ids=[
            "LAT-G-MORF-NOM-D1",
            "LAT-G-MORF-NOM-D2",
            "LAT-G-MORF-ACC-D1",
            "LAT-G-MORF-ACC-D2",
            "LAT-G-MORF-PRAES-C1-ACT",
            "LAT-G-MORF-PRAES-C2-ACT",
            "LAT-G-MORF-NUMERUS-INTRO",
            "LAT-V-F02-PUER",
            "LAT-V-F02-EQUUS",
            "LAT-V-F01-AMO",
            "LAT-V-F02-PUELLA",
            "LAT-V-F01-VIA",
            "LAT-V-F01-VIDEO",
            "LAT-V-F01-DOMINUS",
            "LAT-V-F01-SERVUS",
            "LAT-V-F01-VOCO",
            "LAT-V-F01-TIMEO",
        ],
    ),
]

# ---------------------------------------------------------------------------
# Batch 2: passages 6-10 — +genitivus/dativus/ablativus, voorzetsels, esse
# ---------------------------------------------------------------------------

BATCH_2: list[dict] = [
    passage(
        6,
        "De familie van de meester",
        6,
        "gen_dat_abl_praes_esse",
        zinnen=[
            zin(
                "Servus domini aquam portat.",
                "De slaaf van de meester draagt water.",
                [
                    w("Servus", "servus", "nom.sg.m — 2e decl.", "slaaf"),
                    w("domini", "dominus", "gen.sg.m — 2e decl.", "van de meester"),
                    w("aquam", "aqua", "acc.sg.f — 1e decl.", "water"),
                    w("portat", "porto", "praes.ind.act. 3sg — 1e conj.", "draagt"),
                ],
            ),
            zin(
                "Filia domini villam amat.",
                "De dochter van de meester houdt van de villa.",
                [
                    w("Filia", "filia", "nom.sg.f — 1e decl.", "dochter"),
                    w("domini", "dominus", "gen.sg.m — 2e decl.", "van de meester"),
                    w("villam", "villa", "acc.sg.f — 1e decl.", "villa/landhuis"),
                    w("amat", "amo", "praes.ind.act. 3sg — 1e conj.", "houdt van"),
                ],
            ),
            zin(
                "Filius domini equum habet.",
                "De zoon van de meester heeft een paard.",
                [
                    w("Filius", "filius", "nom.sg.m — 2e decl.", "zoon"),
                    w("domini", "dominus", "gen.sg.m — 2e decl.", "van de meester"),
                    w("equum", "equus", "acc.sg.m — 2e decl.", "paard"),
                    w("habet", "habeo", "praes.ind.act. 3sg — 2e conj.", "heeft"),
                ],
            ),
        ],
        node_ids=[
            "LAT-G-MORF-NOM-D1",
            "LAT-G-MORF-NOM-D2",
            "LAT-G-MORF-GEN-D2",
            "LAT-G-SYNT-GEN-FUNCTIE",
            "LAT-G-MORF-ACC-D1",
            "LAT-G-MORF-ACC-D2",
            "LAT-G-MORF-PRAES-C1-ACT",
            "LAT-G-MORF-PRAES-C2-ACT",
            "LAT-V-F01-SERVUS",
            "LAT-V-F01-DOMINUS",
            "LAT-V-F01-AQUA",
            "LAT-V-F02-PORTO",
            "LAT-V-F01-FILIA",
            "LAT-V-F02-VILLA",
            "LAT-V-F01-AMO",
            "LAT-V-F01-FILIUS",
            "LAT-V-F02-EQUUS",
            "LAT-V-F01-HABEO",
        ],
    ),
    passage(
        7,
        "De meester geeft",
        7,
        "gen_dat_abl_praes_esse",
        zinnen=[
            zin(
                "Dominus servo equum dat.",
                "De meester geeft de slaaf een paard.",
                [
                    w("Dominus", "dominus", "nom.sg.m — 2e decl.", "meester/heer"),
                    w("servo", "servus", "dat.sg.m — 2e decl.", "aan de slaaf"),
                    w("equum", "equus", "acc.sg.m — 2e decl.", "paard"),
                    w("dat", "do", "praes.ind.act. 3sg — onregelm.", "geeft"),
                ],
            ),
            zin(
                "Servus domino aquam portat.",
                "De slaaf brengt de meester water.",
                [
                    w("Servus", "servus", "nom.sg.m — 2e decl.", "slaaf"),
                    w("domino", "dominus", "dat.sg.m — 2e decl.", "aan de meester"),
                    w("aquam", "aqua", "acc.sg.f — 1e decl.", "water"),
                    w("portat", "porto", "praes.ind.act. 3sg — 1e conj.", "brengt"),
                ],
            ),
            zin(
                "Dominus filio villam dat.",
                "De meester geeft zijn zoon de villa.",
                [
                    w("Dominus", "dominus", "nom.sg.m — 2e decl.", "meester/heer"),
                    w("filio", "filius", "dat.sg.m — 2e decl.", "aan de zoon"),
                    w("villam", "villa", "acc.sg.f — 1e decl.", "villa/landhuis"),
                    w("dat", "do", "praes.ind.act. 3sg — onregelm.", "geeft"),
                ],
            ),
        ],
        node_ids=[
            "LAT-G-MORF-NOM-D2",
            "LAT-G-MORF-DAT-D2",
            "LAT-G-MORF-ACC-D1",
            "LAT-G-MORF-ACC-D2",
            "LAT-G-SYNT-DAT-FUNCTIE",
            "LAT-G-SYNT-OBJIND",
            "LAT-G-MORF-PRAES-C1-ACT",
            "LAT-V-F01-DOMINUS",
            "LAT-V-F01-SERVUS",
            "LAT-V-F02-EQUUS",
            "LAT-V-F01-DO",
            "LAT-V-F01-AQUA",
            "LAT-V-F02-PORTO",
            "LAT-V-F01-FILIUS",
            "LAT-V-F02-VILLA",
        ],
    ),
    passage(
        8,
        "In het bos",
        8,
        "gen_dat_abl_praes_esse",
        zinnen=[
            zin(
                "Servus in silva est.",
                "De slaaf is in het bos.",
                [
                    w("Servus", "servus", "nom.sg.m — 2e decl.", "slaaf"),
                    w("in", "in", "voorzetsel + abl.", "in"),
                    w("silva", "silva", "abl.sg.f — 1e decl.", "bos"),
                    w("est", "sum", "praes.ind. 3sg — onregelm.", "is"),
                ],
            ),
            zin(
                "Puella in via aquam portat.",
                "Het meisje draagt water op de weg.",
                [
                    w("Puella", "puella", "nom.sg.f — 1e decl.", "meisje"),
                    w("in", "in", "voorzetsel + abl.", "op"),
                    w("via", "via", "abl.sg.f — 1e decl.", "weg"),
                    w("aquam", "aqua", "acc.sg.f — 1e decl.", "water"),
                    w("portat", "porto", "praes.ind.act. 3sg — 1e conj.", "draagt"),
                ],
            ),
            zin(
                "Filius cum servo in horto est.",
                "De zoon is met de slaaf in de tuin.",
                [
                    w("Filius", "filius", "nom.sg.m — 2e decl.", "zoon"),
                    w("cum", "cum", "voorzetsel + abl.", "met"),
                    w("servo", "servus", "abl.sg.m — 2e decl.", "slaaf"),
                    w("in", "in", "voorzetsel + abl.", "in"),
                    w("horto", "hortus", "abl.sg.m — 2e decl.", "tuin"),
                    w("est", "sum", "praes.ind. 3sg — onregelm.", "is"),
                ],
            ),
        ],
        node_ids=[
            "LAT-G-MORF-NOM-D1",
            "LAT-G-MORF-NOM-D2",
            "LAT-G-MORF-ABL-D1",
            "LAT-G-MORF-ABL-D2",
            "LAT-G-MORF-ACC-D1",
            "LAT-G-MORF-PRAES-ESSE",
            "LAT-G-MORF-PRAES-C1-ACT",
            "LAT-G-SYNT-ABL-FUNCTIE",
            "LAT-G-SYNT-PREP-ABL",
            "LAT-V-F01-SERVUS",
            "LAT-V-F01-IN",
            "LAT-V-F01-SILVA",
            "LAT-V-F01-SUM",
            "LAT-V-F02-PUELLA",
            "LAT-V-F01-VIA",
            "LAT-V-F01-AQUA",
            "LAT-V-F02-PORTO",
            "LAT-V-F01-FILIUS",
            "LAT-V-F01-CUM",
            "LAT-V-F02-HORTUS",
        ],
    ),
    passage(
        9,
        "De boodschapper",
        9,
        "gen_dat_abl_praes_esse",
        zinnen=[
            zin(
                "Nuntius domini in via est.",
                "De boodschapper van de meester is op de weg.",
                [
                    w("Nuntius", "nuntius", "nom.sg.m — 2e decl.", "boodschapper"),
                    w("domini", "dominus", "gen.sg.m — 2e decl.", "van de meester"),
                    w("in", "in", "voorzetsel + abl.", "op"),
                    w("via", "via", "abl.sg.f — 1e decl.", "weg"),
                    w("est", "sum", "praes.ind. 3sg — onregelm.", "is"),
                ],
            ),
            zin(
                "Servus nuntio aquam dat.",
                "De slaaf geeft de boodschapper water.",
                [
                    w("Servus", "servus", "nom.sg.m — 2e decl.", "slaaf"),
                    w("nuntio", "nuntius", "dat.sg.m — 2e decl.", "aan de boodschapper"),
                    w("aquam", "aqua", "acc.sg.f — 1e decl.", "water"),
                    w("dat", "do", "praes.ind.act. 3sg — onregelm.", "geeft"),
                ],
            ),
            zin(
                "Dominus nuntium vocat.",
                "De meester roept de boodschapper.",
                [
                    w("Dominus", "dominus", "nom.sg.m — 2e decl.", "meester/heer"),
                    w("nuntium", "nuntius", "acc.sg.m — 2e decl.", "boodschapper"),
                    w("vocat", "voco", "praes.ind.act. 3sg — 1e conj.", "roept"),
                ],
            ),
        ],
        node_ids=[
            "LAT-G-MORF-NOM-D2",
            "LAT-G-MORF-GEN-D2",
            "LAT-G-MORF-DAT-D2",
            "LAT-G-MORF-ACC-D2",
            "LAT-G-MORF-ABL-D1",
            "LAT-G-MORF-PRAES-ESSE",
            "LAT-G-MORF-PRAES-C1-ACT",
            "LAT-G-SYNT-GEN-FUNCTIE",
            "LAT-G-SYNT-DAT-FUNCTIE",
            "LAT-G-SYNT-PREP-ABL",
            "LAT-V-F02-NUNTIUS",
            "LAT-V-F01-DOMINUS",
            "LAT-V-F01-VIA",
            "LAT-V-F01-SUM",
            "LAT-V-F01-SERVUS",
            "LAT-V-F01-AQUA",
            "LAT-V-F01-DO",
            "LAT-V-F01-VOCO",
            "LAT-V-F01-IN",
        ],
    ),
    passage(
        10,
        "In de tuin van de meester",
        10,
        "gen_dat_abl_praes_esse",
        zinnen=[
            zin(
                "In horto domini servi sunt.",
                "In de tuin van de meester zijn slaven.",
                [
                    w("In", "in", "voorzetsel + abl.", "in"),
                    w("horto", "hortus", "abl.sg.m — 2e decl.", "tuin"),
                    w("domini", "dominus", "gen.sg.m — 2e decl.", "van de meester"),
                    w("servi", "servus", "nom.pl.m — 2e decl.", "slaven"),
                    w("sunt", "sum", "praes.ind. 3pl — onregelm.", "zijn"),
                ],
            ),
            zin(
                "Servus aquam ad villam portat.",
                "De slaaf draagt water naar de villa.",
                [
                    w("Servus", "servus", "nom.sg.m — 2e decl.", "slaaf"),
                    w("aquam", "aqua", "acc.sg.f — 1e decl.", "water"),
                    w("ad", "ad", "voorzetsel + acc.", "naar"),
                    w("villam", "villa", "acc.sg.f — 1e decl.", "villa/landhuis"),
                    w("portat", "porto", "praes.ind.act. 3sg — 1e conj.", "draagt"),
                ],
            ),
            zin(
                "Filia domini in villa est.",
                "De dochter van de meester is in de villa.",
                [
                    w("Filia", "filia", "nom.sg.f — 1e decl.", "dochter"),
                    w("domini", "dominus", "gen.sg.m — 2e decl.", "van de meester"),
                    w("in", "in", "voorzetsel + abl.", "in"),
                    w("villa", "villa", "abl.sg.f — 1e decl.", "villa/landhuis"),
                    w("est", "sum", "praes.ind. 3sg — onregelm.", "is"),
                ],
            ),
            zin(
                "Dominus filio equum dat.",
                "De meester geeft zijn zoon een paard.",
                [
                    w("Dominus", "dominus", "nom.sg.m — 2e decl.", "meester/heer"),
                    w("filio", "filius", "dat.sg.m — 2e decl.", "aan de zoon"),
                    w("equum", "equus", "acc.sg.m — 2e decl.", "paard"),
                    w("dat", "do", "praes.ind.act. 3sg — onregelm.", "geeft"),
                ],
            ),
        ],
        node_ids=[
            "LAT-G-MORF-NOM-D1",
            "LAT-G-MORF-NOM-D2",
            "LAT-G-MORF-GEN-D2",
            "LAT-G-MORF-DAT-D2",
            "LAT-G-MORF-ACC-D1",
            "LAT-G-MORF-ACC-D2",
            "LAT-G-MORF-ABL-D1",
            "LAT-G-MORF-ABL-D2",
            "LAT-G-MORF-PRAES-ESSE",
            "LAT-G-MORF-PRAES-C1-ACT",
            "LAT-G-SYNT-GEN-FUNCTIE",
            "LAT-G-SYNT-DAT-FUNCTIE",
            "LAT-G-SYNT-ABL-FUNCTIE",
            "LAT-G-SYNT-PREP-ABL",
            "LAT-G-SYNT-PREP-ACC",
            "LAT-G-MORF-NUMERUS-INTRO",
            "LAT-V-F01-IN",
            "LAT-V-F02-HORTUS",
            "LAT-V-F01-DOMINUS",
            "LAT-V-F01-SERVUS",
            "LAT-V-F01-SUM",
            "LAT-V-F01-AQUA",
            "LAT-V-F01-AD",
            "LAT-V-F02-VILLA",
            "LAT-V-F02-PORTO",
            "LAT-V-F01-FILIA",
            "LAT-V-F01-FILIUS",
            "LAT-V-F02-EQUUS",
            "LAT-V-F01-DO",
        ],
    ),
]

# ---------------------------------------------------------------------------
# Batch 3: passages 11-15 — +3e declinatie, imperfectum, adjectieven
# ---------------------------------------------------------------------------

BATCH_3: list[dict] = [
    passage(
        11,
        "De koning en de soldaat",
        11,
        "decl3_impf_adj",
        zinnen=[
            zin(
                "Rex militem vocat.",
                "De koning roept de soldaat.",
                [
                    w("Rex", "rex", "nom.sg.m — 3e decl.", "koning"),
                    w("militem", "miles", "acc.sg.m — 3e decl.", "soldaat"),
                    w("vocat", "voco", "praes.ind.act. 3sg — 1e conj.", "roept"),
                ],
            ),
            zin(
                "Miles regem timet.",
                "De soldaat vreest de koning.",
                [
                    w("Miles", "miles", "nom.sg.m — 3e decl.", "soldaat"),
                    w("regem", "rex", "acc.sg.m — 3e decl.", "koning"),
                    w("timet", "timeo", "praes.ind.act. 3sg — 2e conj.", "vreest"),
                ],
            ),
            zin(
                "Rex urbem magnam habet.",
                "De koning heeft een grote stad.",
                [
                    w("Rex", "rex", "nom.sg.m — 3e decl.", "koning"),
                    w("urbem", "urbs", "acc.sg.f — 3e decl.", "stad"),
                    w("magnam", "magnus", "acc.sg.f — adj. D1/D2", "groot"),
                    w("habet", "habeo", "praes.ind.act. 3sg — 2e conj.", "heeft"),
                ],
            ),
        ],
        node_ids=[
            "LAT-G-MORF-NOM-D3",
            "LAT-G-MORF-ACC-D3",
            "LAT-G-MORF-DECL3-INTRO",
            "LAT-G-MORF-PRAES-C1-ACT",
            "LAT-G-MORF-PRAES-C2-ACT",
            "LAT-G-MORF-ADJ-D12-INTRO",
            "LAT-G-MORF-ADJ-D12-VERBG",
            "LAT-G-SYNT-ADJ-CONGR",
            "LAT-V-F01-REX",
            "LAT-V-F01-MILES",
            "LAT-V-F01-VOCO",
            "LAT-V-F01-TIMEO",
            "LAT-V-F01-URBS",
            "LAT-V-F01-MAGNUS",
            "LAT-V-F01-HABEO",
        ],
    ),
    passage(
        12,
        "Vader en moeder",
        12,
        "decl3_impf_adj",
        zinnen=[
            zin(
                "Pater bonus est.",
                "De vader is goed.",
                [
                    w("Pater", "pater", "nom.sg.m — 3e decl.", "vader"),
                    w("bonus", "bonus", "nom.sg.m — adj. D1/D2", "goed"),
                    w("est", "sum", "praes.ind. 3sg — onregelm.", "is"),
                ],
            ),
            zin(
                "Mater filiam amat.",
                "De moeder houdt van haar dochter.",
                [
                    w("Mater", "mater", "nom.sg.f — 3e decl.", "moeder"),
                    w("filiam", "filia", "acc.sg.f — 1e decl.", "dochter"),
                    w("amat", "amo", "praes.ind.act. 3sg — 1e conj.", "houdt van"),
                ],
            ),
            zin(
                "Filius patrem magnum videt.",
                "De zoon ziet zijn grote vader.",
                [
                    w("Filius", "filius", "nom.sg.m — 2e decl.", "zoon"),
                    w("patrem", "pater", "acc.sg.m — 3e decl.", "vader"),
                    w("magnum", "magnus", "acc.sg.m — adj. D1/D2", "groot"),
                    w("videt", "video", "praes.ind.act. 3sg — 2e conj.", "ziet"),
                ],
            ),
        ],
        node_ids=[
            "LAT-G-MORF-NOM-D3",
            "LAT-G-MORF-ACC-D3",
            "LAT-G-MORF-NOM-D2",
            "LAT-G-MORF-ACC-D1",
            "LAT-G-MORF-PRAES-ESSE",
            "LAT-G-MORF-PRAES-C1-ACT",
            "LAT-G-MORF-PRAES-C2-ACT",
            "LAT-G-MORF-ADJ-D12-INTRO",
            "LAT-G-MORF-ADJ-D12-VERBG",
            "LAT-G-SYNT-ADJ-CONGR",
            "LAT-V-F01-PATER",
            "LAT-V-F01-BONUS",
            "LAT-V-F01-SUM",
            "LAT-V-F01-MATER",
            "LAT-V-F01-FILIA",
            "LAT-V-F01-AMO",
            "LAT-V-F01-FILIUS",
            "LAT-V-F01-MAGNUS",
            "LAT-V-F01-VIDEO",
        ],
    ),
    passage(
        13,
        "Vroeger op het landgoed",
        13,
        "decl3_impf_adj",
        zinnen=[
            zin(
                "Olim dominus servum habebat.",
                "Vroeger had de meester een slaaf.",
                [
                    w("Olim", "olim", "bijwoord", "vroeger/eens"),
                    w("dominus", "dominus", "nom.sg.m — 2e decl.", "meester/heer"),
                    w("servum", "servus", "acc.sg.m — 2e decl.", "slaaf"),
                    w("habebat", "habeo", "impf.ind.act. 3sg — 2e conj.", "had"),
                ],
            ),
            zin(
                "Servus in villa aquam portabat.",
                "De slaaf droeg water in de villa.",
                [
                    w("Servus", "servus", "nom.sg.m — 2e decl.", "slaaf"),
                    w("in", "in", "voorzetsel + abl.", "in"),
                    w("villa", "villa", "abl.sg.f — 1e decl.", "villa/landhuis"),
                    w("aquam", "aqua", "acc.sg.f — 1e decl.", "water"),
                    w("portabat", "porto", "impf.ind.act. 3sg — 1e conj.", "droeg"),
                ],
            ),
            zin(
                "Filia domini equum amabat.",
                "De dochter van de meester hield van het paard.",
                [
                    w("Filia", "filia", "nom.sg.f — 1e decl.", "dochter"),
                    w("domini", "dominus", "gen.sg.m — 2e decl.", "van de meester"),
                    w("equum", "equus", "acc.sg.m — 2e decl.", "paard"),
                    w("amabat", "amo", "impf.ind.act. 3sg — 1e conj.", "hield van"),
                ],
            ),
        ],
        node_ids=[
            "LAT-G-MORF-IMPF-INTRO",
            "LAT-G-MORF-IMPF-C1C2-ACT",
            "LAT-G-MORF-NOM-D1",
            "LAT-G-MORF-NOM-D2",
            "LAT-G-MORF-ACC-D1",
            "LAT-G-MORF-ACC-D2",
            "LAT-G-MORF-ABL-D1",
            "LAT-G-MORF-GEN-D2",
            "LAT-G-SYNT-PREP-ABL",
            "LAT-V-F02-OLIM",
            "LAT-V-F01-DOMINUS",
            "LAT-V-F01-SERVUS",
            "LAT-V-F01-HABEO",
            "LAT-V-F02-VILLA",
            "LAT-V-F01-AQUA",
            "LAT-V-F02-PORTO",
            "LAT-V-F01-FILIA",
            "LAT-V-F02-EQUUS",
            "LAT-V-F01-AMO",
            "LAT-V-F01-IN",
        ],
    ),
    passage(
        14,
        "Burgers en de koning",
        14,
        "decl3_impf_adj",
        zinnen=[
            zin(
                "Multi cives in urbe sunt.",
                "Veel burgers zijn in de stad.",
                [
                    w("Multi", "multus", "nom.pl.m — adj. D1/D2", "veel"),
                    w("cives", "civis", "nom.pl.m — 3e decl.", "burgers"),
                    w("in", "in", "voorzetsel + abl.", "in"),
                    w("urbe", "urbs", "abl.sg.f — 3e decl.", "stad"),
                    w("sunt", "sum", "praes.ind. 3pl — onregelm.", "zijn"),
                ],
            ),
            zin(
                "Rex bonus cives amat.",
                "De goede koning houdt van de burgers.",
                [
                    w("Rex", "rex", "nom.sg.m — 3e decl.", "koning"),
                    w("bonus", "bonus", "nom.sg.m — adj. D1/D2", "goed"),
                    w("cives", "civis", "acc.pl.m — 3e decl.", "burgers"),
                    w("amat", "amo", "praes.ind.act. 3sg — 1e conj.", "houdt van"),
                ],
            ),
            zin(
                "Milites urbem magnam tenent.",
                "De soldaten bezetten de grote stad.",
                [
                    w("Milites", "miles", "nom.pl.m — 3e decl.", "soldaten"),
                    w("urbem", "urbs", "acc.sg.f — 3e decl.", "stad"),
                    w("magnam", "magnus", "acc.sg.f — adj. D1/D2", "groot"),
                    w("tenent", "teneo", "praes.ind.act. 3pl — 2e conj.", "bezetten/houden"),
                ],
            ),
        ],
        node_ids=[
            "LAT-G-MORF-NOM-D3",
            "LAT-G-MORF-ACC-D3",
            "LAT-G-MORF-ABL-D3",
            "LAT-G-MORF-DECL3-INTRO",
            "LAT-G-MORF-PRAES-ESSE",
            "LAT-G-MORF-PRAES-C1-ACT",
            "LAT-G-MORF-PRAES-C2-ACT",
            "LAT-G-MORF-NUMERUS-INTRO",
            "LAT-G-MORF-ADJ-D12-INTRO",
            "LAT-G-MORF-ADJ-D12-VERBG",
            "LAT-G-SYNT-ADJ-CONGR",
            "LAT-G-SYNT-PREP-ABL",
            "LAT-V-F01-MULTUS",
            "LAT-V-F01-CIVIS",
            "LAT-V-F01-URBS",
            "LAT-V-F01-SUM",
            "LAT-V-F01-REX",
            "LAT-V-F01-BONUS",
            "LAT-V-F01-AMO",
            "LAT-V-F01-MILES",
            "LAT-V-F01-MAGNUS",
            "LAT-V-F01-TENEO",
            "LAT-V-F01-IN",
        ],
    ),
    passage(
        15,
        "Tijd van oorlog",
        15,
        "decl3_impf_adj",
        zinnen=[
            zin(
                "Tempus belli erat.",
                "Het was tijd van oorlog.",
                [
                    w("Tempus", "tempus", "nom.sg.n — 3e decl.", "tijd"),
                    w("belli", "bellum", "gen.sg.n — 2e decl.", "van oorlog"),
                    w("erat", "sum", "impf.ind. 3sg — onregelm.", "was"),
                ],
            ),
            zin(
                "Milites in via erant.",
                "De soldaten waren op de weg.",
                [
                    w("Milites", "miles", "nom.pl.m — 3e decl.", "soldaten"),
                    w("in", "in", "voorzetsel + abl.", "op"),
                    w("via", "via", "abl.sg.f — 1e decl.", "weg"),
                    w("erant", "sum", "impf.ind. 3pl — onregelm.", "waren"),
                ],
            ),
            zin(
                "Rex multos milites habebat.",
                "De koning had veel soldaten.",
                [
                    w("Rex", "rex", "nom.sg.m — 3e decl.", "koning"),
                    w("multos", "multus", "acc.pl.m — adj. D1/D2", "veel"),
                    w("milites", "miles", "acc.pl.m — 3e decl.", "soldaten"),
                    w("habebat", "habeo", "impf.ind.act. 3sg — 2e conj.", "had"),
                ],
            ),
            zin(
                "Cives hostes timebant.",
                "De burgers vreesden de vijanden.",
                [
                    w("Cives", "civis", "nom.pl.m — 3e decl.", "burgers"),
                    w("hostes", "hostis", "acc.pl.m — 3e decl.", "vijanden"),
                    w("timebant", "timeo", "impf.ind.act. 3pl — 2e conj.", "vreesden"),
                ],
            ),
        ],
        node_ids=[
            "LAT-G-MORF-NOM-D3",
            "LAT-G-MORF-ACC-D3",
            "LAT-G-MORF-GEN-D2",
            "LAT-G-MORF-ABL-D1",
            "LAT-G-MORF-DECL3-INTRO",
            "LAT-G-MORF-DECL3-CONS",
            "LAT-G-MORF-IMPF-INTRO",
            "LAT-G-MORF-IMPF-C1C2-ACT",
            "LAT-G-MORF-IMPF-ESSE",
            "LAT-G-MORF-NUMERUS-INTRO",
            "LAT-G-MORF-ADJ-D12-VERBG",
            "LAT-G-SYNT-GEN-FUNCTIE",
            "LAT-G-SYNT-PREP-ABL",
            "LAT-V-F01-TEMPUS",
            "LAT-V-F01-BELLUM",
            "LAT-V-F01-SUM",
            "LAT-V-F01-MILES",
            "LAT-V-F01-VIA",
            "LAT-V-F01-IN",
            "LAT-V-F01-REX",
            "LAT-V-F01-MULTUS",
            "LAT-V-F01-HABEO",
            "LAT-V-F01-CIVIS",
            "LAT-V-F01-HOSTIS",
            "LAT-V-F01-TIMEO",
        ],
    ),
]

# ---------------------------------------------------------------------------
# Batch 4: passages 16-20 — +perfectum, pronomina, AcI-intro
# ---------------------------------------------------------------------------

BATCH_4: list[dict] = [
    passage(
        16,
        "De meester riep",
        16,
        "perf_pron_aci",
        zinnen=[
            zin(
                "Dominus servum vocavit.",
                "De meester heeft de slaaf geroepen.",
                [
                    w("Dominus", "dominus", "nom.sg.m — 2e decl.", "meester/heer"),
                    w("servum", "servus", "acc.sg.m — 2e decl.", "slaaf"),
                    w("vocavit", "voco", "perf.ind.act. 3sg — 1e conj.", "heeft geroepen/riep"),
                ],
            ),
            zin(
                "Servus aquam portavit.",
                "De slaaf heeft water gedragen.",
                [
                    w("Servus", "servus", "nom.sg.m — 2e decl.", "slaaf"),
                    w("aquam", "aqua", "acc.sg.f — 1e decl.", "water"),
                    w("portavit", "porto", "perf.ind.act. 3sg — 1e conj.", "heeft gedragen/droeg"),
                ],
            ),
            zin(
                "Filia dominum amavit.",
                "De dochter hield van de meester.",
                [
                    w("Filia", "filia", "nom.sg.f — 1e decl.", "dochter"),
                    w("dominum", "dominus", "acc.sg.m — 2e decl.", "meester/heer"),
                    w("amavit", "amo", "perf.ind.act. 3sg — 1e conj.", "hield van"),
                ],
            ),
        ],
        node_ids=[
            "LAT-G-MORF-PERF-INTRO",
            "LAT-G-MORF-PERF-C1-ACT",
            "LAT-G-MORF-PERF-UITG",
            "LAT-G-MORF-PERF-STAMT-V",
            "LAT-G-MORF-NOM-D1",
            "LAT-G-MORF-NOM-D2",
            "LAT-G-MORF-ACC-D1",
            "LAT-G-MORF-ACC-D2",
            "LAT-V-F01-DOMINUS",
            "LAT-V-F01-SERVUS",
            "LAT-V-F01-VOCO",
            "LAT-V-F01-AQUA",
            "LAT-V-F02-PORTO",
            "LAT-V-F01-FILIA",
            "LAT-V-F01-AMO",
        ],
    ),
    passage(
        17,
        "Ik en jij",
        17,
        "perf_pron_aci",
        zinnen=[
            zin(
                "Ego equum vocavi.",
                "Ik heb het paard geroepen.",
                [
                    w("Ego", "ego", "nom. — pers. vnw. 1sg", "ik"),
                    w("equum", "equus", "acc.sg.m — 2e decl.", "paard"),
                    w("vocavi", "voco", "perf.ind.act. 1sg — 1e conj.", "heb geroepen"),
                ],
            ),
            zin(
                "Tu servum laudavisti.",
                "Jij hebt de slaaf geprezen.",
                [
                    w("Tu", "tu", "nom. — pers. vnw. 2sg", "jij"),
                    w("servum", "servus", "acc.sg.m — 2e decl.", "slaaf"),
                    w("laudavisti", "laudo", "perf.ind.act. 2sg — 1e conj.", "hebt geprezen"),
                ],
            ),
            zin(
                "Dominus equum habuit.",
                "De meester heeft een paard gehad.",
                [
                    w("Dominus", "dominus", "nom.sg.m — 2e decl.", "meester/heer"),
                    w("equum", "equus", "acc.sg.m — 2e decl.", "paard"),
                    w("habuit", "habeo", "perf.ind.act. 3sg — 2e conj.", "heeft gehad"),
                ],
            ),
        ],
        node_ids=[
            "LAT-G-MORF-PERF-INTRO",
            "LAT-G-MORF-PERF-C1-ACT",
            "LAT-G-MORF-PERF-C2-ACT",
            "LAT-G-MORF-PERF-UITG",
            "LAT-G-MORF-PERF-STAMT-V",
            "LAT-G-MORF-PERF-STAMT-U",
            "LAT-G-MORF-PRON-INTRO",
            "LAT-G-MORF-PRON-PERS",
            "LAT-G-MORF-PRON-EGO",
            "LAT-V-F01-EGO",
            "LAT-V-F02-EQUUS",
            "LAT-V-F01-VOCO",
            "LAT-V-F01-TU",
            "LAT-V-F01-SERVUS",
            "LAT-V-F02-LAUDO",
            "LAT-V-F01-DOMINUS",
            "LAT-V-F01-HABEO",
        ],
    ),
    passage(
        18,
        "Deze en die",
        18,
        "perf_pron_aci",
        zinnen=[
            zin(
                "Hic servus dominum amat.",
                "Deze slaaf houdt van de meester.",
                [
                    w("Hic", "hic", "nom.sg.m — aanwijzend vnw.", "deze"),
                    w("servus", "servus", "nom.sg.m — 2e decl.", "slaaf"),
                    w("dominum", "dominus", "acc.sg.m — 2e decl.", "meester/heer"),
                    w("amat", "amo", "praes.ind.act. 3sg — 1e conj.", "houdt van"),
                ],
            ),
            zin(
                "Ille servus dominum timet.",
                "Die slaaf vreest de meester.",
                [
                    w("Ille", "ille", "nom.sg.m — aanwijzend vnw.", "die/gene"),
                    w("servus", "servus", "nom.sg.m — 2e decl.", "slaaf"),
                    w("dominum", "dominus", "acc.sg.m — 2e decl.", "meester/heer"),
                    w("timet", "timeo", "praes.ind.act. 3sg — 2e conj.", "vreest"),
                ],
            ),
            zin(
                "Hic aquam portat, ille equum habet.",
                "Deze draagt water, die heeft een paard.",
                [
                    w("Hic", "hic", "nom.sg.m — aanwijzend vnw.", "deze"),
                    w("aquam", "aqua", "acc.sg.f — 1e decl.", "water"),
                    w("portat", "porto", "praes.ind.act. 3sg — 1e conj.", "draagt"),
                    w("ille", "ille", "nom.sg.m — aanwijzend vnw.", "die/gene"),
                    w("equum", "equus", "acc.sg.m — 2e decl.", "paard"),
                    w("habet", "habeo", "praes.ind.act. 3sg — 2e conj.", "heeft"),
                ],
            ),
        ],
        node_ids=[
            "LAT-G-MORF-PRON-INTRO",
            "LAT-G-MORF-PRON-HIC",
            "LAT-G-MORF-PRON-ILLE",
            "LAT-G-MORF-PRON-AANW",
            "LAT-G-MORF-NOM-D2",
            "LAT-G-MORF-ACC-D1",
            "LAT-G-MORF-ACC-D2",
            "LAT-G-MORF-PRAES-C1-ACT",
            "LAT-G-MORF-PRAES-C2-ACT",
            "LAT-V-F01-HIC",
            "LAT-V-F01-ILLE",
            "LAT-V-F01-SERVUS",
            "LAT-V-F01-DOMINUS",
            "LAT-V-F01-AMO",
            "LAT-V-F01-TIMEO",
            "LAT-V-F01-AQUA",
            "LAT-V-F02-PORTO",
            "LAT-V-F02-EQUUS",
            "LAT-V-F01-HABEO",
        ],
    ),
    passage(
        19,
        "Een verhaal van oorlog",
        19,
        "perf_pron_aci",
        zinnen=[
            zin(
                "Rex milites ad urbem misit.",
                "De koning stuurde soldaten naar de stad.",
                [
                    w("Rex", "rex", "nom.sg.m — 3e decl.", "koning"),
                    w("milites", "miles", "acc.pl.m — 3e decl.", "soldaten"),
                    w("ad", "ad", "voorzetsel + acc.", "naar"),
                    w("urbem", "urbs", "acc.sg.f — 3e decl.", "stad"),
                    w("misit", "mitto", "perf.ind.act. 3sg — 3e conj.", "stuurde/zond"),
                ],
            ),
            zin(
                "Milites hostes vicerunt.",
                "De soldaten hebben de vijanden overwonnen.",
                [
                    w("Milites", "miles", "nom.pl.m — 3e decl.", "soldaten"),
                    w("hostes", "hostis", "acc.pl.m — 3e decl.", "vijanden"),
                    w("vicerunt", "vinco", "perf.ind.act. 3pl — 3e conj.", "hebben overwonnen"),
                ],
            ),
            zin(
                "Cives regem laudaverunt.",
                "De burgers prezen de koning.",
                [
                    w("Cives", "civis", "nom.pl.m — 3e decl.", "burgers"),
                    w("regem", "rex", "acc.sg.m — 3e decl.", "koning"),
                    w("laudaverunt", "laudo", "perf.ind.act. 3pl — 1e conj.", "prezen"),
                ],
            ),
        ],
        node_ids=[
            "LAT-G-MORF-PERF-INTRO",
            "LAT-G-MORF-PERF-C1-ACT",
            "LAT-G-MORF-PERF-C3-ACT",
            "LAT-G-MORF-PERF-UITG",
            "LAT-G-MORF-PERF-STAMT-S",
            "LAT-G-MORF-PERF-STAMT-V",
            "LAT-G-MORF-NOM-D3",
            "LAT-G-MORF-ACC-D3",
            "LAT-G-MORF-NUMERUS-INTRO",
            "LAT-G-SYNT-PREP-ACC",
            "LAT-V-F01-REX",
            "LAT-V-F01-MILES",
            "LAT-V-F01-AD",
            "LAT-V-F01-URBS",
            "LAT-V-F01-MITTO",
            "LAT-V-F01-HOSTIS",
            "LAT-V-F02-VINCO",
            "LAT-V-F01-CIVIS",
            "LAT-V-F02-LAUDO",
        ],
    ),
    passage(
        20,
        "De meester ziet dat…",
        20,
        "perf_pron_aci",
        zinnen=[
            zin(
                "Dominus servum aquam portare videt.",
                "De meester ziet dat de slaaf water draagt.",
                [
                    w("Dominus", "dominus", "nom.sg.m — 2e decl.", "meester/heer"),
                    w("servum", "servus", "acc.sg.m — 2e decl. (AcI-subject)", "slaaf"),
                    w("aquam", "aqua", "acc.sg.f — 1e decl.", "water"),
                    w("portare", "porto", "inf.praes.act. — 1e conj.", "dragen"),
                    w("videt", "video", "praes.ind.act. 3sg — 2e conj.", "ziet"),
                ],
            ),
            zin(
                "Pater filium bonum esse dicit.",
                "De vader zegt dat zijn zoon goed is.",
                [
                    w("Pater", "pater", "nom.sg.m — 3e decl.", "vader"),
                    w("filium", "filius", "acc.sg.m — 2e decl. (AcI-subject)", "zoon"),
                    w("bonum", "bonus", "acc.sg.m — adj. D1/D2 (AcI-predicaat)", "goed"),
                    w("esse", "sum", "inf.praes. — onregelm.", "zijn"),
                    w("dicit", "dico", "praes.ind.act. 3sg — 3e conj.", "zegt"),
                ],
            ),
            zin(
                "Rex hostes venire timet.",
                "De koning vreest dat de vijanden komen.",
                [
                    w("Rex", "rex", "nom.sg.m — 3e decl.", "koning"),
                    w("hostes", "hostis", "acc.pl.m — 3e decl. (AcI-subject)", "vijanden"),
                    w("venire", "venio", "inf.praes.act. — 4e conj.", "komen"),
                    w("timet", "timeo", "praes.ind.act. 3sg — 2e conj.", "vreest"),
                ],
            ),
            zin(
                "Milites urbem magnam esse sciunt.",
                "De soldaten weten dat de stad groot is.",
                [
                    w("Milites", "miles", "nom.pl.m — 3e decl.", "soldaten"),
                    w("urbem", "urbs", "acc.sg.f — 3e decl. (AcI-subject)", "stad"),
                    w("magnam", "magnus", "acc.sg.f — adj. D1/D2 (AcI-predicaat)", "groot"),
                    w("esse", "sum", "inf.praes. — onregelm.", "zijn"),
                    w("sciunt", "scio", "praes.ind.act. 3pl — 4e conj.", "weten"),
                ],
            ),
        ],
        node_ids=[
            "LAT-G-SYNT-ACI-INTRO",
            "LAT-G-MORF-INF-PRAES-ACT",
            "LAT-G-MORF-INF-INTRO",
            "LAT-G-MORF-NOM-D2",
            "LAT-G-MORF-NOM-D3",
            "LAT-G-MORF-ACC-D1",
            "LAT-G-MORF-ACC-D2",
            "LAT-G-MORF-ACC-D3",
            "LAT-G-MORF-PRAES-C2-ACT",
            "LAT-G-MORF-PRAES-ESSE",
            "LAT-G-MORF-ADJ-D12-VERBG",
            "LAT-G-SYNT-ADJ-CONGR",
            "LAT-V-F01-DOMINUS",
            "LAT-V-F01-SERVUS",
            "LAT-V-F01-AQUA",
            "LAT-V-F02-PORTO",
            "LAT-V-F01-VIDEO",
            "LAT-V-F01-PATER",
            "LAT-V-F01-FILIUS",
            "LAT-V-F01-BONUS",
            "LAT-V-F01-SUM",
            "LAT-V-F01-DICO",
            "LAT-V-F01-REX",
            "LAT-V-F01-HOSTIS",
            "LAT-V-F01-VENIO",
            "LAT-V-F01-TIMEO",
            "LAT-V-F01-MILES",
            "LAT-V-F01-URBS",
            "LAT-V-F01-MAGNUS",
            "LAT-V-F02-SCIO",
        ],
    ),
]

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

ALL_PASSAGES = BATCH_1 + BATCH_2 + BATCH_3 + BATCH_4


def validate(passages: list[dict], known_ids: set[str]) -> list[str]:
    """Validate node_ids in passages against the graph. Return warnings."""
    warnings = []
    for p in passages:
        for kid in p["node_ids"]:
            if kid not in known_ids:
                warnings.append(f"  {p['id']}: onbekend node_id {kid}")
    return warnings


def main() -> None:
    known = load_all_node_ids()
    passages = [p for p in ALL_PASSAGES if p]  # skip empty batches

    if not passages:
        print("Geen passages om te genereren.")
        sys.exit(0)

    warnings = validate(passages, known)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / "lat_leespassages_leerjaar1.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"passages": passages}, f, ensure_ascii=False, indent=2)

    print(f"Geschreven: {out_path}")
    print(f"Aantal passages: {len(passages)}")
    print(f"Totaal zinnen: {sum(len(p['zinnen']) for p in passages)}")
    print(
        f"Totaal woorden: {sum(len(wo) for p in passages for z in p['zinnen'] for wo in [z['woorden']])}"
    )
    if warnings:
        print(f"\n⚠ {len(warnings)} onbekende node_ids:")
        for ww in warnings:
            print(ww)
        sys.exit(1)
    else:
        print("\n✓ Alle node_ids gevalideerd.")


if __name__ == "__main__":
    main()
