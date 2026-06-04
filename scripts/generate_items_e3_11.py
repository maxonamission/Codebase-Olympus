#!/usr/bin/env python3
"""Generate exercise items for E3-11: GRC voorzetsels + basissyntaxis.

Target: data/graph/grc_grammatica_leerjaar1.json
Scope:  8 nodes (GRC-G-SYNT-PREP-*, -WRDVLG, -ONTK, -ZINSBOUW).

Drie componenten:
1. Voorzetsel-items: juiste naamval-keuze bij ἀπό/ἐκ (+gen), ἐν (+dat),
   εἰς/πρός (+acc), ἐπί/μετά (+gen/+dat/+acc) — incl. betekenisverschil
   per naamval.
2. οὐ/μή-onderscheid (≥5 items): οὐ factueel in indicativus, μή
   prohibitief/final bij conj./imper./inf.
3. Vraagzin-markeringen ἆρα / μῶν en basissyntaxis (zinsdelen).

Run:
    python scripts/generate_items_e3_11.py            # writes items to graph
    python scripts/generate_items_e3_11.py --dry-run  # only validate + print
"""

from __future__ import annotations

import argparse
import json
import sys
import unicodedata
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from gymnasium_classica.models.graph import Item


def nfc(value):
    if isinstance(value, str):
        return unicodedata.normalize("NFC", value)
    if isinstance(value, list):
        return [nfc(v) for v in value]
    return value


# ---------------------------------------------------------------------------
# 1. PREP-INTRO
# ---------------------------------------------------------------------------


def prep_intro_items() -> list[dict]:
    return [
        {
            "id": "ITEM-GRC-G-SYNT-PREP-INTRO-001",
            "node_ids": ["GRC-G-SYNT-PREP-INTRO"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": -0.5,
            "discrimination_initial": 1.0,
            "expected_time_sec": 15,
            "stimulus": "Wat heeft elk Grieks voorzetsel nodig van het zelfstandig naamwoord dat erop volgt?",
            "answer": [
                "een specifieke naamval (gen., dat. of acc.)",
                "een vaste naamval",
            ],
            "feedback": "Elk voorzetsel stuurt één of meer vaste naamvallen. Sommige (ἐν, εἰς) alleen één; andere (ἐπί, παρά, μετά) drie — met betekenisverschil per naamval.",
            "source": "manual",
        },
        {
            "id": "ITEM-GRC-G-SYNT-PREP-INTRO-002",
            "node_ids": ["GRC-G-SYNT-PREP-INTRO"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": -0.3,
            "discrimination_initial": 1.1,
            "expected_time_sec": 15,
            "stimulus": "Welke ruwe vuistregel verbindt naamval en betekenis bij plaatsvoorzetsels?",
            "answer": [
                "gen. = vanwaar (beweging vanaf); dat. = waar (rust/plaats); acc. = waarheen (beweging naartoe)",
                "gen. vandaan, dat. waar, acc. waarheen",
            ],
            "feedback": "Vuistregel: genitivus = herkomst (ἐκ τῆς οἰκίας), dativus = plaats/rust (ἐν τῇ οἰκίᾳ), accusativus = direction/doel (εἰς τὴν οἰκίαν).",
            "source": "manual",
        },
    ]


# ---------------------------------------------------------------------------
# 2. PREP-GEN (ἀπό, ἐκ)
# ---------------------------------------------------------------------------


def prep_gen_items() -> list[dict]:
    return [
        {
            "id": "ITEM-GRC-G-SYNT-PREP-GEN-001",
            "node_ids": ["GRC-G-SYNT-PREP-GEN"],
            "type": "production",
            "direction": "productive",
            "difficulty_initial": 0.2,
            "discrimination_initial": 1.2,
            "expected_time_sec": 20,
            "stimulus": "Welke naamval eist ἀπό? Geef als voorbeeld 'van de stad af' (ἡ πόλις, πόλεως).",
            "answer": [
                "genitivus — ἀπὸ τῆς πόλεως",
                "gen.; ἀπὸ τῆς πόλεως",
            ],
            "feedback": "ἀπό staat altijd met genitivus en betekent 'vanaf, (weg) van'. Beweging uit de buurt van iets: ἀπὸ τῆς πόλεως = 'van de stad weg'.",
            "source": "manual",
        },
        {
            "id": "ITEM-GRC-G-SYNT-PREP-GEN-002",
            "node_ids": ["GRC-G-SYNT-PREP-GEN"],
            "type": "contextual",
            "direction": "receptive",
            "difficulty_initial": 0.3,
            "discrimination_initial": 1.3,
            "expected_time_sec": 25,
            "stimulus": "Vertaal: οἱ παῖδες ἐκ τῆς οἰκίας ἔρχονται. Welke naamval heeft τῆς οἰκίας en waarom?",
            "answer": [
                "genitivus; ἐκ eist de gen. ('uit het huis komen de kinderen')",
                "gen. bij ἐκ — 'uit het huis'",
            ],
            "feedback": "ἐκ (vóór klinker: ἐξ) + gen. = 'uit'. Herkomst uit het binnenste van iets. Contrast met ἀπό (gen.) = 'vanaf, weg van'.",
            "source": "manual",
        },
        {
            "id": "ITEM-GRC-G-SYNT-PREP-GEN-003",
            "node_ids": ["GRC-G-SYNT-PREP-GEN"],
            "type": "contextual",
            "direction": "receptive",
            "difficulty_initial": 0.4,
            "discrimination_initial": 1.3,
            "expected_time_sec": 25,
            "stimulus": "Vul de juiste vorm in: ἀπὸ ___ (ὁ ποταμός) ἔρχεται ὁ στρατηγός.",
            "answer": [
                "τοῦ ποταμοῦ",
                "ἀπὸ τοῦ ποταμοῦ",
            ],
            "feedback": "ἀπό + gen. → ὁ ποταμός wordt τοῦ ποταμοῦ (gen. sg. m.). 'De generaal komt vanaf de rivier.'",
            "source": "manual",
        },
    ]


# ---------------------------------------------------------------------------
# 3. PREP-DAT (ἐν)
# ---------------------------------------------------------------------------


def prep_dat_items() -> list[dict]:
    return [
        {
            "id": "ITEM-GRC-G-SYNT-PREP-DAT-001",
            "node_ids": ["GRC-G-SYNT-PREP-DAT"],
            "type": "production",
            "direction": "productive",
            "difficulty_initial": 0.2,
            "discrimination_initial": 1.2,
            "expected_time_sec": 20,
            "stimulus": "Welke naamval eist ἐν? Geef 'in het huis' (ἡ οἰκία).",
            "answer": [
                "dativus — ἐν τῇ οἰκίᾳ",
                "dat.; ἐν τῇ οἰκίᾳ",
            ],
            "feedback": "ἐν + dat. = 'in, op' (rust/plaats). Geen beweging: waar iets zich bevindt. ἐν τῇ οἰκίᾳ = 'in het huis'.",
            "source": "manual",
        },
        {
            "id": "ITEM-GRC-G-SYNT-PREP-DAT-002",
            "node_ids": ["GRC-G-SYNT-PREP-DAT"],
            "type": "contextual",
            "direction": "receptive",
            "difficulty_initial": 0.4,
            "discrimination_initial": 1.3,
            "expected_time_sec": 25,
            "stimulus": "Waarom is *ἐν τὴν οἰκίαν fout, en wat zou je moeten schrijven voor 'naar het huis toe'?",
            "answer": [
                "ἐν eist dativus, niet accusativus; 'naar het huis toe' = εἰς τὴν οἰκίαν",
                "ἐν + dat. voor rust; εἰς + acc. voor beweging naartoe",
            ],
            "feedback": "ἐν + dat. = plaats/rust ('in'). Voor beweging naar een doel gebruik je εἰς + acc. Twee verschillende voorzetsels, twee verschillende naamvallen.",
            "source": "manual",
        },
    ]


# ---------------------------------------------------------------------------
# 4. PREP-ACC (εἰς, πρός)
# ---------------------------------------------------------------------------


def prep_acc_items() -> list[dict]:
    return [
        {
            "id": "ITEM-GRC-G-SYNT-PREP-ACC-001",
            "node_ids": ["GRC-G-SYNT-PREP-ACC"],
            "type": "production",
            "direction": "productive",
            "difficulty_initial": 0.2,
            "discrimination_initial": 1.2,
            "expected_time_sec": 20,
            "stimulus": "Welke naamval eist εἰς? Geef 'naar de agora' (ἡ ἀγορά).",
            "answer": [
                "accusativus — εἰς τὴν ἀγοράν",
                "acc.; εἰς τὴν ἀγοράν",
            ],
            "feedback": "εἰς + acc. = 'naar...toe' (beweging, direction, doel). Altijd accusativus, nooit dativus of genitivus.",
            "source": "manual",
        },
        {
            "id": "ITEM-GRC-G-SYNT-PREP-ACC-002",
            "node_ids": ["GRC-G-SYNT-PREP-ACC"],
            "type": "contextual",
            "direction": "receptive",
            "difficulty_initial": 0.4,
            "discrimination_initial": 1.3,
            "expected_time_sec": 25,
            "stimulus": "Vertaal: ὁ ἀνὴρ πρὸς τὸν φίλον λέγει. Welke naamval heeft τὸν φίλον en waarom?",
            "answer": [
                "accusativus; πρός + acc. = 'tegen, tot, naar' (gericht aan iemand)",
                "acc. bij πρός — 'tegen de vriend'",
            ],
            "feedback": "πρός + acc. = direction, spreker die iets zegt 'tegen' iemand. 'De man spreekt tegen de vriend.'",
            "source": "manual",
        },
        {
            "id": "ITEM-GRC-G-SYNT-PREP-ACC-003",
            "node_ids": ["GRC-G-SYNT-PREP-ACC"],
            "type": "contextual",
            "direction": "receptive",
            "difficulty_initial": 0.5,
            "discrimination_initial": 1.4,
            "expected_time_sec": 30,
            "stimulus": "Vul aan met de juiste vorm: οἱ μαθηταὶ ἔρχονται εἰς ___ (τὸ διδασκαλεῖον).",
            "answer": [
                "τὸ διδασκαλεῖον",
                "εἰς τὸ διδασκαλεῖον",
            ],
            "feedback": "εἰς + acc. Onzijdig enkelvoud τὸ διδασκαλεῖον is in nom. én acc. identiek (neutrum-regel). 'De leerlingen gaan naar de school.'",
            "source": "manual",
        },
    ]


# ---------------------------------------------------------------------------
# 5. PREP-MRV (ἐπί, μετά — betekenisverschil per naamval)
# ---------------------------------------------------------------------------


def prep_mrv_items() -> list[dict]:
    items: list[dict] = []
    items.extend(_prep_mrv_epi())
    items.extend(_prep_mrv_meta())
    return items


def _prep_mrv_epi() -> list[dict]:
    return [
        {
            "id": "ITEM-GRC-G-SYNT-PREP-MRV-001",
            "node_ids": ["GRC-G-SYNT-PREP-MRV"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": 0.4,
            "discrimination_initial": 1.3,
            "expected_time_sec": 20,
            "stimulus": "ἐπί kent drie naamvallen. Welke betekenis hoort bij ἐπί + gen.?",
            "answer": [
                "op (rust/plaats, historisch context: ten tijde van)",
                "op (plaats); ten tijde van",
            ],
            "feedback": "ἐπί + gen. = 'op' (plaats) of historisch 'ten tijde van' (ἐπὶ Περικλέους = onder/ten tijde van Perikles).",
            "source": "manual",
        },
        {
            "id": "ITEM-GRC-G-SYNT-PREP-MRV-002",
            "node_ids": ["GRC-G-SYNT-PREP-MRV"],
            "type": "contextual",
            "direction": "receptive",
            "difficulty_initial": 0.5,
            "discrimination_initial": 1.4,
            "expected_time_sec": 25,
            "stimulus": "Vertaal het verschil: (a) ἐπὶ τῇ τραπέζῃ — (b) ἐπὶ τὴν τράπεζαν.",
            "answer": [
                "(a) op de tafel (rust, dat.); (b) op de tafel toe (beweging, acc.)",
                "dat. = op (rust), acc. = op (beweging naartoe)",
            ],
            "feedback": "ἐπί + dat. = 'op' (rust: iets ligt erop). ἐπί + acc. = 'op...toe' (iets wordt erop gelegd of beweegt erheen). Naamval verschuift de betekenis van rust naar direction.",
            "source": "manual",
        },
        {
            "id": "ITEM-GRC-G-SYNT-PREP-MRV-003",
            "node_ids": ["GRC-G-SYNT-PREP-MRV"],
            "type": "contextual",
            "direction": "receptive",
            "difficulty_initial": 0.6,
            "discrimination_initial": 1.4,
            "expected_time_sec": 30,
            "stimulus": "Vul de juiste naamval in: οἱ στρατιῶται μάχονται ἐπὶ ___ (οἱ πολέμιοι) — 'de soldaten strijden tegen de vijanden'.",
            "answer": [
                "τοὺς πολεμίους",
                "ἐπὶ τοὺς πολεμίους (acc.)",
            ],
            "feedback": "ἐπί + acc. in vijandige context = 'tegen, op af' (direction/doel). Soldaten die oprukken 'tegen' de vijand: ἐπὶ τοὺς πολεμίους.",
            "source": "manual",
        },
    ]


def _prep_mrv_meta() -> list[dict]:
    return [
        {
            "id": "ITEM-GRC-G-SYNT-PREP-MRV-004",
            "node_ids": ["GRC-G-SYNT-PREP-MRV"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": 0.4,
            "discrimination_initial": 1.3,
            "expected_time_sec": 20,
            "stimulus": "μετά + gen. en μετά + acc. hebben heel verschillende betekenissen. Welke?",
            "answer": [
                "μετά + gen. = met (samen met); μετά + acc. = na (tijd of plaats)",
                "gen. = met; acc. = na",
            ],
            "feedback": "μετά + gen. = 'met, samen met' (gezelschap). μετά + acc. = 'na' (temporeel of ruimtelijk volgend). Zelfde voorzetsel, fundamenteel ander concept.",
            "source": "manual",
        },
        {
            "id": "ITEM-GRC-G-SYNT-PREP-MRV-005",
            "node_ids": ["GRC-G-SYNT-PREP-MRV"],
            "type": "contextual",
            "direction": "receptive",
            "difficulty_initial": 0.5,
            "discrimination_initial": 1.4,
            "expected_time_sec": 30,
            "stimulus": "Vertaal en verklaar het naamvalsverschil: (a) μετὰ τῶν φίλων — (b) μετὰ τοὺς φίλους.",
            "answer": [
                "(a) met de vrienden (gen. = gezelschap); (b) na de vrienden (acc. = temporeel/volgorde)",
                "gen. 'met', acc. 'na'",
            ],
            "feedback": "μετὰ τῶν φίλων (gen.) = 'met/samen met de vrienden'. μετὰ τοὺς φίλους (acc.) = 'na de vrienden' (later dan zij, of achter hen aan).",
            "source": "manual",
        },
        {
            "id": "ITEM-GRC-G-SYNT-PREP-MRV-006",
            "node_ids": ["GRC-G-SYNT-PREP-MRV"],
            "type": "contextual",
            "direction": "receptive",
            "difficulty_initial": 0.5,
            "discrimination_initial": 1.4,
            "expected_time_sec": 30,
            "stimulus": "Welke naamval bij μετά voor 'na de slag' (ἡ μάχη)?",
            "answer": [
                "accusativus — μετὰ τὴν μάχην",
                "acc.; μετὰ τὴν μάχην",
            ],
            "feedback": "'Na de slag' = temporeel → μετά + acc. → μετὰ τὴν μάχην. Zou de vertaling 'met de slag' zijn geweest, dan μετὰ τῆς μάχης (gen.) — maar dat slaat hier nergens op.",
            "source": "manual",
        },
    ]


# ---------------------------------------------------------------------------
# 6. WRDVLG (woordvolgorde)
# ---------------------------------------------------------------------------


def wrdvlg_items() -> list[dict]:
    return [
        {
            "id": "ITEM-GRC-G-SYNT-WRDVLG-001",
            "node_ids": ["GRC-G-SYNT-WRDVLG"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": -0.2,
            "discrimination_initial": 1.0,
            "expected_time_sec": 15,
            "stimulus": "Waarom kan het Grieks vrijer dan het Nederlands met woordvolgorde omgaan?",
            "answer": [
                "de naamvallen geven de zinsfunctie aan, niet de positie",
                "naamvalsysteem neemt de taak van de woordvolgorde over",
            ],
            "feedback": "Door naamvalsuitgangen is onderwerp (nom.) vs. lijdend voorwerp (acc.) altijd duidelijk, ook bij afwijkende volgorde. Positie geeft dus nadruk, niet grammaticale functie.",
            "source": "manual",
        },
        {
            "id": "ITEM-GRC-G-SYNT-WRDVLG-002",
            "node_ids": ["GRC-G-SYNT-WRDVLG"],
            "type": "contextual",
            "direction": "receptive",
            "difficulty_initial": 0.4,
            "discrimination_initial": 1.3,
            "expected_time_sec": 25,
            "stimulus": "Wat doet de schrijver met de positie van 'τὸν παῖδα' in 'τὸν παῖδα ὁ πατὴρ φιλεῖ'?",
            "answer": [
                "hij zet het lijdend voorwerp vooraan voor nadruk ('de jongen is het die de vader liefheeft')",
                "nadruk op τὸν παῖδα door plaats aan het begin",
            ],
            "feedback": "Neutrale volgorde zou ὁ πατὴρ φιλεῖ τὸν παῖδα zijn. Door τὸν παῖδα vóóraan te plaatsen benadrukt de schrijver juist dit element (topic/focus).",
            "source": "manual",
        },
    ]


# ---------------------------------------------------------------------------
# 7. ONTK (οὐ/μή-onderscheid, ≥5 items)
# ---------------------------------------------------------------------------


def ontk_items() -> list[dict]:
    items: list[dict] = []
    items.extend(_ontk_ou_items())
    items.extend(_ontk_me_items())
    return items


def _ontk_ou_items() -> list[dict]:
    return [
        {
            "id": "ITEM-GRC-G-SYNT-ONTK-001",
            "node_ids": ["GRC-G-SYNT-ONTK"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": -0.2,
            "discrimination_initial": 1.1,
            "expected_time_sec": 15,
            "stimulus": "Welke ontkenning gebruik je in een feitelijke bewering in de indicativus?",
            "answer": ["οὐ", "οὐ (οὐκ / οὐχ)"],
            "feedback": "οὐ bij indicativus = factuele ontkenning: ontkent dát iets het geval is. Varianten: οὐ vóór medeklinker, οὐκ vóór zachte klinker, οὐχ vóór ruwe klinker.",
            "source": "manual",
        },
        {
            "id": "ITEM-GRC-G-SYNT-ONTK-002",
            "node_ids": ["GRC-G-SYNT-ONTK"],
            "type": "production",
            "direction": "productive",
            "difficulty_initial": 0.2,
            "discrimination_initial": 1.2,
            "expected_time_sec": 20,
            "stimulus": "Vul de juiste vorm van 'niet' in: ὁ διδάσκαλος ___ ἀκούει τοὺς παῖδας.",
            "answer": [
                "οὐκ",
                "οὐκ (vóór klinker)",
            ],
            "feedback": "οὐκ vóór een klinker met zachte ademing (ἀκούει). Indicativus feitelijk ontkennen → οὐ-reeks (οὐ / οὐκ / οὐχ afhankelijk van volgklank).",
            "source": "manual",
        },
        {
            "id": "ITEM-GRC-G-SYNT-ONTK-003",
            "node_ids": ["GRC-G-SYNT-ONTK"],
            "type": "contextual",
            "direction": "receptive",
            "difficulty_initial": 0.3,
            "discrimination_initial": 1.3,
            "expected_time_sec": 25,
            "stimulus": "Vertaal en geef de ontkenning aan: οὐχ ὁρᾶτε τὸν στρατηγόν;",
            "answer": [
                "'Zien jullie de generaal niet?' — οὐχ (vóór ruwe klinker ὁρ-)",
                "οὐχ (vóór ὁ met spiritus asper)",
            ],
            "feedback": "Vragende zin met indicatieve werkwoordsvorm ὁρᾶτε → οὐ-reeks. De ὁ in ὁρᾶτε heeft spiritus asper, dus οὐχ. Indicativus blijft ook in een vraag feitelijk ontkennen met οὐ.",
            "source": "manual",
        },
    ]


def _ontk_me_items() -> list[dict]:
    return [
        {
            "id": "ITEM-GRC-G-SYNT-ONTK-004",
            "node_ids": ["GRC-G-SYNT-ONTK"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": 0.1,
            "discrimination_initial": 1.2,
            "expected_time_sec": 15,
            "stimulus": "Welke ontkenning hoort bij een verbod (imperatief of conjunctief met prohibitieve functie)?",
            "answer": ["μή", "μή (prohibitief)"],
            "feedback": "μή bij imperatief of conj. aor. ontkent een wens/verbod: 'doe dat niet!'. Niet feitelijk, maar modaal/prohibitief — daarom niet οὐ.",
            "source": "manual",
        },
        {
            "id": "ITEM-GRC-G-SYNT-ONTK-005",
            "node_ids": ["GRC-G-SYNT-ONTK"],
            "type": "contextual",
            "direction": "receptive",
            "difficulty_initial": 0.3,
            "discrimination_initial": 1.3,
            "expected_time_sec": 25,
            "stimulus": "Kies οὐ of μή: '___ λέγε ταῦτα!' (Zeg dat niet!)",
            "answer": ["μή", "μὴ λέγε"],
            "feedback": "Imperatief (λέγε) met verbod → μή. Feitelijk zou 'hij zegt dat niet' oὐ λέγει zijn; hier is het een appèl, dus μή.",
            "source": "manual",
        },
        {
            "id": "ITEM-GRC-G-SYNT-ONTK-006",
            "node_ids": ["GRC-G-SYNT-ONTK"],
            "type": "contextual",
            "direction": "receptive",
            "difficulty_initial": 0.5,
            "discrimination_initial": 1.4,
            "expected_time_sec": 30,
            "stimulus": "In een finale bijzin ('opdat niet...') met conjunctief, welke ontkenning gebruik je? Geef de combinatie met ἵνα.",
            "answer": [
                "μή — ἵνα μή (+ conj.)",
                "μή; ἵνα μή",
            ],
            "feedback": "Finale bijzinnen met ἵνα + conj. drukken doel uit; ontkennend doel = ἵνα μή ('opdat niet'). Conjunctief is modaal → altijd μή, nooit οὐ.",
            "source": "manual",
        },
    ]


# ---------------------------------------------------------------------------
# 8. ZINSBOUW (basissyntaxis + vraagzinnen ἆρα/μῶν)
# ---------------------------------------------------------------------------


def zinsbouw_items() -> list[dict]:
    return [
        {
            "id": "ITEM-GRC-G-SYNT-ZINSBOUW-001",
            "node_ids": ["GRC-G-SYNT-ZINSBOUW"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": -0.3,
            "discrimination_initial": 1.0,
            "expected_time_sec": 15,
            "stimulus": "Welke naamval dragen onderwerp, lijdend voorwerp en meewerkend voorwerp in het Grieks?",
            "answer": [
                "onderwerp nom., lijdend voorwerp acc., meewerkend voorwerp dat.",
                "nom. / acc. / dat.",
            ],
            "feedback": "Onderwerp = nominativus, lijdend voorwerp = accusativus, meewerkend voorwerp = dativus. De persoonsvorm congrueert met het onderwerp.",
            "source": "manual",
        },
        {
            "id": "ITEM-GRC-G-SYNT-ZINSBOUW-002",
            "node_ids": ["GRC-G-SYNT-ZINSBOUW"],
            "type": "contextual",
            "direction": "receptive",
            "difficulty_initial": 0.3,
            "discrimination_initial": 1.3,
            "expected_time_sec": 25,
            "stimulus": "Ontleed de zin 'ὁ πατὴρ δίδωσιν τῷ παιδὶ τὸ βιβλίον': wie is onderwerp, lv, mv?",
            "answer": [
                "onderwerp: ὁ πατήρ; mv (dat.): τῷ παιδί; lv (acc.): τὸ βιβλίον",
                "ow ὁ πατήρ, mv τῷ παιδί, lv τὸ βιβλίον",
            ],
            "feedback": "ὁ πατήρ (nom.) = onderwerp van δίδωσιν. τὸ βιβλίον (acc.) = lijdend voorwerp. τῷ παιδί (dat.) = meewerkend voorwerp. 'De vader geeft het kind het boek.'",
            "source": "manual",
        },
        {
            "id": "ITEM-GRC-G-SYNT-ZINSBOUW-003",
            "node_ids": ["GRC-G-SYNT-ZINSBOUW"],
            "type": "recognition",
            "direction": "receptive",
            "difficulty_initial": 0.2,
            "discrimination_initial": 1.2,
            "expected_time_sec": 20,
            "stimulus": "Welk partikel markeert een neutrale ja/nee-vraag aan het begin van een Griekse zin?",
            "answer": ["ἆρα", "ἆρα (of niets, met stijgende intonatie)"],
            "feedback": "ἆρα aan het zinsbegin = neutrale vraagmarkering, zoals Engels 'Is it the case that...?' Antwoord kan positief of negatief zijn — het partikel zelf stuurt niet.",
            "source": "manual",
        },
        {
            "id": "ITEM-GRC-G-SYNT-ZINSBOUW-004",
            "node_ids": ["GRC-G-SYNT-ZINSBOUW"],
            "type": "contextual",
            "direction": "receptive",
            "difficulty_initial": 0.5,
            "discrimination_initial": 1.4,
            "expected_time_sec": 25,
            "stimulus": "Wat is het verschil tussen een vraag met ἆρα en een vraag met μῶν?",
            "answer": [
                "ἆρα is neutraal; μῶν verwacht een ontkennend antwoord ('toch niet?')",
                "ἆρα neutraal, μῶν = 'toch niet?' (negatief verwachtingspatroon)",
            ],
            "feedback": "ἆρα stelt een open vraag zonder vooroordeel. μῶν (= μὴ οὖν) verwacht 'nee' als antwoord: 'μῶν ὁ ἀνὴρ ἀπέθανεν; = 'Hij is toch niet dood?' (verwacht: nee).",
            "source": "manual",
        },
    ]


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------


def collect_all() -> dict[str, list[dict]]:
    all_items: list[dict] = []
    all_items.extend(prep_intro_items())
    all_items.extend(prep_gen_items())
    all_items.extend(prep_dat_items())
    all_items.extend(prep_acc_items())
    all_items.extend(prep_mrv_items())
    all_items.extend(wrdvlg_items())
    all_items.extend(ontk_items())
    all_items.extend(zinsbouw_items())

    primary_map: dict[str, list[dict]] = {}
    for item in all_items:
        for key in ("stimulus", "antwoord", "feedback", "expected_result"):
            if key in item and item[key] is not None:
                item[key] = nfc(item[key])
        primary_map.setdefault(item["node_ids"][0], []).append(item)
    return primary_map


def validate_all(items_by_node: dict[str, list[dict]]) -> None:
    for _node_id, item_list in items_by_node.items():
        for item_dict in item_list:
            Item(**item_dict)
    total = sum(len(v) for v in items_by_node.values())
    print(f"All {total} items validated.")


def add_items_to_json(json_path: Path, items_by_node: dict[str, list[dict]]) -> int:
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    added = 0
    for node in data["nodes"]:
        if node["id"] in items_by_node:
            existing_ids = {item["id"] for item in node.get("items", [])}
            new_items = [
                item for item in items_by_node[node["id"]] if item["id"] not in existing_ids
            ]
            node.setdefault("items", []).extend(new_items)
            added += len(new_items)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    return added


def print_summary(items_by_node: dict[str, list[dict]]) -> None:
    total = sum(len(v) for v in items_by_node.values())
    type_counter: Counter[str] = Counter()
    per_node: Counter[str] = Counter()
    for node_id, item_list in items_by_node.items():
        per_node[node_id] = len(item_list)
        for item in item_list:
            type_counter[item["type"]] += 1

    print("\n=== E3-11 Summary ===")
    print(f"Knopen: {len(items_by_node)}")
    print(f"Total items: {total}")
    print("\nItems per node:")
    for k, c in per_node.most_common():
        print(f"  {k}: {c}")
    print("\nOefentype-verdeling:")
    for t, c in type_counter.most_common():
        print(f"  {t}: {c}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    items_by_node = collect_all()
    validate_all(items_by_node)
    print_summary(items_by_node)

    if args.dry_run:
        print("\nDry-run: geen wijzigingen geschreven.")
        return

    path = Path(__file__).parent.parent / "data" / "graph" / "grc_grammatica_leerjaar1.json"
    added = add_items_to_json(path, items_by_node)
    print(f"\nAdded {added} items to {path.name}")


if __name__ == "__main__":
    main()
