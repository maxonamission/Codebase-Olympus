"""Tests voor F2-04: fout-classificatie in de grading-module.

Dekt de vijf heuristieken (macron/accent, naamval, verbuiging, spelling,
synoniem) plus ONBEKEND, de inflectie-inferentie uit node-IDs, en de
integratie via grade_answer.  Edge cases: korte woorden, Grieks met
accent-variatie en list-antwoorden.
"""

from __future__ import annotations

from gymnasium_classica.models.graph import (
    Direction,
    Item,
    ItemType,
    Language,
    Source,
)
from gymnasium_classica.scheduling.grading import (
    InflectionKind,
    MismatchType,
    classify_mismatch,
    grade_answer,
    infer_inflection,
)

_NOUN_NODE = "LAT-G-MORF-NOM-D1"
_VERB_NODE = "LAT-G-MORF-PRAES-C1"
_VOCAB_NODE = "LAT-V-F01-TEST"


def _item(
    antwoord: str | list[str],
    *,
    node_ids: list[str] | None = None,
) -> Item:
    return Item(
        id="ITEM-TEST-001",
        node_ids=node_ids or [_VOCAB_NODE],
        type=ItemType.PRODUCTION,
        direction=Direction.PRODUCTIVE,
        difficulty_initial=0.0,
        discrimination_initial=1.0,
        expected_time_sec=10,
        stimulus="stim",
        answer=antwoord,
        feedback="ok",
        source=Source.MANUAL,
    )


# ---------------------------------------------------------------------------
# infer_inflection
# ---------------------------------------------------------------------------


class TestInferInflection:
    def test_verbal_segment(self):
        assert infer_inflection(_item("x", node_ids=[_VERB_NODE])) == InflectionKind.VERBAL

    def test_nominal_segment(self):
        assert infer_inflection(_item("x", node_ids=[_NOUN_NODE])) == InflectionKind.NOMINAL

    def test_vocab_node_is_none(self):
        assert infer_inflection(_item("x", node_ids=[_VOCAB_NODE])) is None

    def test_verbal_wins_over_nominal(self):
        item = _item("x", node_ids=["LAT-G-MORF-NOM-D1", "LAT-G-MORF-PRAES-C2"])
        assert infer_inflection(item) == InflectionKind.VERBAL

    def test_greek_aorist_is_verbal(self):
        assert infer_inflection(_item("x", node_ids=["GRC-G-MORF-AOR-X"])) == InflectionKind.VERBAL


# ---------------------------------------------------------------------------
# classify_mismatch — direct unit tests
# ---------------------------------------------------------------------------


class TestClassifyMacron:
    def test_latin_diaeresis_only(self):
        kind, hint = classify_mismatch("coëgi", "coegi", language=Language.LAT)
        assert kind == MismatchType.MACRON
        assert hint is not None and "macron" in hint.lower()

    def test_greek_accent_only(self):
        # ἁ vs ἀ — only the breathing/accent differs
        kind, hint = classify_mismatch("ἀνήρ", "ἁνήρ", language=Language.GRC)
        assert kind == MismatchType.MACRON
        assert hint is not None and "accent" in hint.lower()


class TestClassifyNaamval:
    def test_case_ending_noun(self):
        kind, hint = classify_mismatch(
            "puellam", "puellae", language=Language.LAT, inflection=InflectionKind.NOMINAL
        )
        assert kind == MismatchType.NAAMVAL
        assert hint is not None

    def test_default_without_inflection_is_naamval(self):
        kind, _ = classify_mismatch("puellam", "puellae", language=Language.LAT)
        assert kind == MismatchType.NAAMVAL

    def test_greek_case_ending(self):
        kind, _ = classify_mismatch(
            "λόγον", "λόγου", language=Language.GRC, inflection=InflectionKind.NOMINAL
        )
        assert kind == MismatchType.NAAMVAL


class TestClassifyVerbuiging:
    def test_personal_ending(self):
        kind, hint = classify_mismatch(
            "amas", "amat", language=Language.LAT, inflection=InflectionKind.VERBAL
        )
        assert kind == MismatchType.VERBUIGING
        assert hint is not None

    def test_short_verb_form(self):
        # es vs est — adding/removing a one-char ending on a 2-char stem
        kind, _ = classify_mismatch(
            "es", "est", language=Language.LAT, inflection=InflectionKind.VERBAL
        )
        assert kind == MismatchType.VERBUIGING

    def test_amo_amas(self):
        kind, _ = classify_mismatch(
            "amo", "amas", language=Language.LAT, inflection=InflectionKind.VERBAL
        )
        assert kind == MismatchType.VERBUIGING


class TestClassifySpelling:
    def test_missing_middle_letter(self):
        # amcus vs amicus: prefix too short for an ending story, lev=1
        kind, hint = classify_mismatch("amcus", "amicus", language=Language.LAT)
        assert kind == MismatchType.SPELLING
        assert hint is not None

    def test_transposition_near_start(self):
        kind, _ = classify_mismatch("tmepus", "tempus", language=Language.LAT)
        assert kind == MismatchType.SPELLING

    def test_single_char_typo(self):
        kind, _ = classify_mismatch("a", "e", language=Language.LAT)
        assert kind == MismatchType.SPELLING


class TestClassifySynoniem:
    def test_match_in_pool(self):
        kind, hint = classify_mismatch(
            "ingens",
            "magnus",
            language=Language.LAT,
            synonym_pool=frozenset({"ingens"}),
        )
        assert kind == MismatchType.SYNONIEM
        assert hint is not None

    def test_pool_wins_over_stem(self):
        # Shares no stem here, but pool match must dominate regardless
        kind, _ = classify_mismatch(
            "magnae",
            "magnus",
            language=Language.LAT,
            inflection=InflectionKind.NOMINAL,
            synonym_pool=frozenset({"magnae"}),
        )
        assert kind == MismatchType.SYNONIEM

    def test_pool_present_but_no_match_falls_through(self):
        kind, _ = classify_mismatch(
            "puellam",
            "puellae",
            language=Language.LAT,
            synonym_pool=frozenset({"rosa"}),
        )
        assert kind == MismatchType.NAAMVAL


class TestClassifyOnbekend:
    def test_unrelated_words(self):
        kind, hint = classify_mismatch("xyz", "puella", language=Language.LAT)
        assert kind == MismatchType.ONBEKEND
        assert hint is None

    def test_empty_answer(self):
        kind, hint = classify_mismatch("", "puella", language=Language.LAT)
        assert kind == MismatchType.ONBEKEND
        assert hint is None


# ---------------------------------------------------------------------------
# grade_answer — integration (fields wired end-to-end)
# ---------------------------------------------------------------------------


class TestGradeAnswerIntegration:
    def test_correct_answer_has_no_mismatch(self):
        result = grade_answer("sum", _item("sum"), Language.LAT)
        assert result.correct is True
        assert result.mismatch_type is None
        assert result.hint is None

    def test_empty_answer_no_mismatch(self):
        result = grade_answer("", _item("sum"), Language.LAT)
        assert result.correct is False
        assert result.mismatch_type is None

    def test_wrong_ending_verb_node(self):
        result = grade_answer("amas", _item("amat", node_ids=[_VERB_NODE]), Language.LAT)
        assert result.correct is False
        assert result.mismatch_type == MismatchType.VERBUIGING

    def test_wrong_ending_noun_node(self):
        result = grade_answer("puellam", _item("puellae", node_ids=[_NOUN_NODE]), Language.LAT)
        assert result.mismatch_type == MismatchType.NAAMVAL

    def test_greek_accent_mismatch(self):
        result = grade_answer("εἶμι", _item("εἰμί"), Language.GRC)
        assert result.correct is False
        assert result.mismatch_type == MismatchType.MACRON

    def test_spelling_mismatch(self):
        result = grade_answer("amcus", _item("amicus"), Language.LAT)
        assert result.mismatch_type == MismatchType.SPELLING

    def test_synonym_via_pool(self):
        result = grade_answer(
            "ingens", _item("magnus"), Language.LAT, synonym_pool=frozenset({"ingens"})
        )
        assert result.mismatch_type == MismatchType.SYNONIEM

    def test_unknown_mismatch(self):
        result = grade_answer("xyz", _item("puella"), Language.LAT)
        assert result.mismatch_type == MismatchType.ONBEKEND
        assert result.hint is None

    def test_list_answer_diagnosed_against_closest(self):
        # "bsetaan" (s/e swap) is a typo of "bestaan", far from "zijn".
        # Proves we diagnose against the closest variant, not the first.
        result = grade_answer("bsetaan", _item(["zijn", "bestaan"]), Language.LAT)
        assert result.correct is False
        assert result.mismatch_type == MismatchType.SPELLING

    def test_macron_only_latin_still_correct(self):
        # Sanity: macron tolerance keeps exact-match-with-macron green,
        # so it never reaches the classifier.
        result = grade_answer("puella", _item("puellā"), Language.LAT)
        assert result.correct is True
        assert result.mismatch_type is None
