"""Tests voor F1-12: server-side grading van leerling-antwoorden.

Dekt normalisatie, list-antwoorden, macron-tolerantie (Latijn) en
NFC-normalisatie (Grieks).  Geen mocks — grade_answer is een pure
functie die direct aangeroepen wordt.
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from gymnasium_classica.models.graph import (
    Direction,
    Item,
    ItemType,
    Language,
    Source,
)
from gymnasium_classica.scheduling.grading import (
    GradingResult,
    canonical_expected_answer,
    grade_answer,
)


def _make_item(
    antwoord: str | list[str],
    *,
    item_id: str = "ITEM-TEST-001",
    item_type: ItemType = ItemType.PRODUCTIE,
) -> Item:
    return Item(
        id=item_id,
        knoop_ids=["LAT-V-F01-TEST"],
        type=item_type,
        richting=Direction.PRODUCTIEF,
        moeilijkheid_initieel=0.0,
        discriminatie_initieel=1.0,
        verwachte_tijd_sec=10,
        stimulus="stim",
        antwoord=antwoord,
        feedback="ok",
        bron=Source.HANDMATIG,
    )


class TestBasicMatching:
    def test_exact_match(self):
        result = grade_answer("sum", _make_item("sum"), Language.LAT)
        assert result.correct is True
        assert result.normalized_answer == "sum"
        assert result.normalized_expected == "sum"

    def test_mismatch(self):
        result = grade_answer("est", _make_item("sum"), Language.LAT)
        assert result.correct is False
        assert result.normalized_answer == "est"
        assert result.normalized_expected == "sum"

    def test_empty_answer_is_never_correct(self):
        assert grade_answer("", _make_item(""), Language.LAT).correct is False
        assert grade_answer("   ", _make_item("   "), Language.LAT).correct is False

    def test_returns_frozen_result(self):
        result = grade_answer("sum", _make_item("sum"), Language.LAT)
        assert isinstance(result, GradingResult)
        with pytest.raises((AttributeError, TypeError, FrozenInstanceError)):
            result.correct = False  # frozen dataclass


class TestNormalization:
    def test_trim_whitespace(self):
        assert grade_answer("  sum  ", _make_item("sum"), Language.LAT).correct is True

    def test_collapse_internal_whitespace(self):
        assert grade_answer("de  boer", _make_item("de boer"), Language.LAT).correct is True

    def test_case_insensitive_latin(self):
        assert grade_answer("SUM", _make_item("sum"), Language.LAT).correct is True
        assert grade_answer("Sum", _make_item("sum"), Language.LAT).correct is True

    def test_case_insensitive_greek(self):
        assert grade_answer("Εἰμί", _make_item("εἰμί"), Language.GRC).correct is True


class TestLatinMacronTolerance:
    def test_missing_macron_accepted(self):
        # Expected has macron, learner types plain vowel.
        assert grade_answer("puella", _make_item("puellā"), Language.LAT).correct is True

    def test_extra_macron_accepted(self):
        # Expected is plain, learner adds a macron.
        assert grade_answer("puellā", _make_item("puella"), Language.LAT).correct is True

    def test_breve_also_stripped(self):
        # Breve (U+0306) is also accepted loosely on Latin.
        assert grade_answer("a", _make_item("ă"), Language.LAT).correct is True


class TestGreekDiacriticsPreserved:
    def test_different_accent_is_incorrect(self):
        """Grieks: accenten dragen betekenis — niet tolereren."""
        # εἰμί (I am) vs εἶμι (I go) — different circumflex position.
        result = grade_answer("εἶμι", _make_item("εἰμί"), Language.GRC)
        assert result.correct is False

    def test_nfc_normalization_accepted(self):
        """Dezelfde letter in NFD en NFC moet als gelijk worden herkend."""
        import unicodedata

        expected = "εἰμί"
        decomposed = unicodedata.normalize("NFD", expected)
        assert decomposed != expected  # sanity: really is decomposed
        assert grade_answer(decomposed, _make_item(expected), Language.GRC).correct is True


class TestListAnswer:
    def test_matches_any_variant(self):
        item = _make_item(["zijn", "bestaan"])
        assert grade_answer("zijn", item, Language.LAT).correct is True
        assert grade_answer("bestaan", item, Language.LAT).correct is True
        assert grade_answer("Zijn", item, Language.LAT).correct is True

    def test_none_matches(self):
        item = _make_item(["zijn", "bestaan"])
        assert grade_answer("zien", item, Language.LAT).correct is False

    def test_canonical_is_first_variant(self):
        item = _make_item(["zijn", "bestaan"])
        result = grade_answer("bestaan", item, Language.LAT)
        # normalized_expected is the first variant's normalization,
        # regardless of which variant matched.
        assert result.normalized_expected == "zijn"


class TestCanonicalExpectedAnswer:
    def test_single_string(self):
        assert canonical_expected_answer(_make_item("sum")) == "sum"

    def test_list_picks_first(self):
        assert canonical_expected_answer(_make_item(["zijn", "bestaan"])) == "zijn"
