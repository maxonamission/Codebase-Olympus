"""Server-side grading of learner answers.

A small, deliberately simple layer between the raw answer the learner
typed/selected and the boolean the BKT/SM-2 pipeline needs.  The
function is pure and returns a structured result so future stories can
extend it with richer diagnostics (mismatch type, confidence, hints)
without touching callers.
"""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass

from gymnasium_classica.models.graph import Item, Language

# --- Public types ---


@dataclass(frozen=True)
class GradingResult:
    """Outcome of grading a single answer.

    Kept intentionally small.  Downstream stories that introduce
    error classification can add fields (mismatch_type, hints, ...) —
    existing callers keep working because they only read ``correct``.
    """

    correct: bool
    normalized_answer: str
    normalized_expected: str


# --- Normalization ---


def _strip_macrons(text: str) -> str:
    """Remove combining macrons (and breves) from decomposed characters.

    After NFD-decomposition the macron (U+0304) sits as a combining mark
    on the base letter.  Many learners can't easily type macrons, so we
    accept answers with or without them for Latin.
    """
    decomposed = unicodedata.normalize("NFD", text)
    stripped = "".join(ch for ch in decomposed if ch not in ("\u0304", "\u0306"))
    return unicodedata.normalize("NFC", stripped)


def _normalize(raw: str, taal: Language) -> str:
    """Normalize a piece of text for comparison.

    * trim + collapse internal whitespace
    * NFC-compose so visually-identical Greek strings compare equal
    * Latin: case-fold and strip macrons/breves
    * Greek: case-fold (diacritics preserved — they carry meaning)
    """
    text = unicodedata.normalize("NFC", raw).strip()
    text = " ".join(text.split())
    text = text.casefold()
    if taal == Language.LAT:
        text = _strip_macrons(text)
    return text


def _expected_variants(antwoord: str | list[str]) -> list[str]:
    """Return the list of acceptable raw answers from an item."""
    if isinstance(antwoord, list):
        return [a for a in antwoord if isinstance(a, str)]
    return [antwoord]


# --- Public API ---


def grade_answer(raw_answer: str, item: Item, taal: Language) -> GradingResult:
    """Compare a learner's answer against the item's expected answer.

    Args:
        raw_answer: Exactly what the learner typed (or the MC-option
            they selected).  Leading/trailing whitespace is tolerated.
        item: The Item being graded.  ``item.antwoord`` may be a single
            string or a list of acceptable strings.
        taal: The language of the knoop, used to pick normalization
            rules (macron-tolerant for Latin).

    Returns:
        A :class:`GradingResult` with the boolean and the normalized
        strings that were compared.  The raw answer is intentionally
        not echoed back — callers store it separately.
    """
    normalized_answer = _normalize(raw_answer, taal)
    variants = _expected_variants(item.antwoord)
    normalized_variants = [_normalize(v, taal) for v in variants]

    correct = any(normalized_answer == v for v in normalized_variants) and bool(normalized_answer)

    # Prefer the first variant as the "canonical" expected string for
    # storage and future display.  If there are no variants at all
    # (should not happen for real items), fall back to an empty string.
    canonical_expected = normalized_variants[0] if normalized_variants else ""

    return GradingResult(
        correct=correct,
        normalized_answer=normalized_answer,
        normalized_expected=canonical_expected,
    )


def canonical_expected_answer(item: Item) -> str:
    """Return the first acceptable answer string, unnormalized.

    Handy for snapshotting ``item.antwoord`` onto an ItemResponse so
    later analysis doesn't depend on the item still existing in its
    current form.
    """
    variants = _expected_variants(item.antwoord)
    return variants[0] if variants else ""
