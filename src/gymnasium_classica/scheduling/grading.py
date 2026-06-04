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
from enum import StrEnum

from gymnasium_classica.models.graph import Item, Language

# --- Public types ---


class MismatchType(StrEnum):
    """Coarse classification of *why* a wrong answer is wrong (F2-04).

    Rule-based, no LLM. Feeds mentor diagnostics (F2-02/F2-03) with a
    hint instead of a raw character diff.
    """

    MACRON = "macron"  # only diacritics differ (Latin macron / Greek accent)
    NAAMVAL = "naamval"  # nominal: right stem, wrong case ending
    VERBUIGING = "verbuiging"  # verbal: right stem, wrong personal ending
    SPELLING = "spelling"  # small typo (Levenshtein <= 2), no stem/case story
    SYNONIEM = "synoniem"  # a real word, but a sibling in the same cluster
    ONBEKEND = "onbekend"  # none of the above heuristics matched


class InflectionKind(StrEnum):
    """Whether the item drills a nominal or a verbal paradigm.

    Used to choose between :attr:`MismatchType.NAAMVAL` and
    :attr:`MismatchType.VERBUIGING` for a wrong-ending answer. Inferred
    from the node-ID segments when not supplied by the caller.
    """

    NOMINAL = "nominal"
    VERBAL = "verbal"


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
    mismatch_type: MismatchType | None = None
    hint: str | None = None


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


def _normalize(raw: str, language: Language) -> str:
    """Normalize a piece of text for comparison.

    * trim + collapse internal whitespace
    * NFC-compose so visually-identical Greek strings compare equal
    * Latin: case-fold and strip macrons/breves
    * Greek: case-fold (diacritics preserved — they carry meaning)
    """
    text = unicodedata.normalize("NFC", raw).strip()
    text = " ".join(text.split())
    text = text.casefold()
    if language == Language.LAT:
        text = _strip_macrons(text)
    return text


def _expected_variants(answer: str | list[str]) -> list[str]:
    """Return the list of acceptable raw answers from an item."""
    if isinstance(answer, list):
        return [a for a in answer if isinstance(a, str)]
    return [answer]


# --- Error classification (F2-04) ---

# Node-ID segments that mark a verbal paradigm vs a nominal one. Derived
# from the actual leerjaar-1 grammar graphs (data/graph/*grammatica*.json).
_VERBAL_SEGMENTS = frozenset(
    {"PRAES", "PRES", "IMPF", "PERF", "PLQP", "FUT", "INF", "IMPV", "AOR", "CONJ"}
) | frozenset(f"C{i}" for i in range(1, 5))
_NOMINAL_SEGMENTS = frozenset({"DECL", "NOM", "ACC", "GEN", "DAT", "ABL", "VOC"}) | frozenset(
    f"D{i}" for i in range(1, 6)
)


def _strip_diacritics(text: str) -> str:
    """Remove *all* combining marks (Latin macrons, Greek accents/breathings)."""
    decomposed = unicodedata.normalize("NFD", text)
    stripped = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
    return unicodedata.normalize("NFC", stripped)


def _common_prefix_len(a: str, b: str) -> int:
    """Length of the shared leading substring of *a* and *b*."""
    n = 0
    for ca, cb in zip(a, b, strict=False):
        if ca != cb:
            break
        n += 1
    return n


def _levenshtein(a: str, b: str, max_distance: int = 2) -> int:
    """Levenshtein edit distance, capped at *max_distance* + 1.

    Returns ``max_distance + 1`` as soon as the true distance is known to
    exceed the cap, so callers can cheaply test ``<= max_distance``.
    """
    if a == b:
        return 0
    if abs(len(a) - len(b)) > max_distance:
        return max_distance + 1
    previous = list(range(len(b) + 1))
    for i, ca in enumerate(a, start=1):
        current = [i]
        row_min = i
        for j, cb in enumerate(b, start=1):
            cost = 0 if ca == cb else 1
            value = min(previous[j] + 1, current[j - 1] + 1, previous[j - 1] + cost)
            current.append(value)
            row_min = min(row_min, value)
        if row_min > max_distance:
            return max_distance + 1
        previous = current
    return previous[-1]


def infer_inflection(item: Item) -> InflectionKind | None:
    """Best-effort guess whether *item* drills a verbal or nominal paradigm.

    Scans the node-ID segments. Verbal markers win ties (a node tagged
    both would be unusual). Returns None when nothing matches — the
    caller then defaults to a nominal (case) reading.
    """
    segments: set[str] = set()
    for node_id in item.node_ids:
        segments.update(node_id.split("-"))
    if segments & _VERBAL_SEGMENTS:
        return InflectionKind.VERBAL
    if segments & _NOMINAL_SEGMENTS:
        return InflectionKind.NOMINAL
    return None


def _ending_hint(answer: str, expected: str, kind: MismatchType) -> str:
    if kind == MismatchType.VERBUIGING:
        return f"Juiste stam, verkeerde uitgang: je schreef '{answer}' i.p.v. '{expected}'."
    return f"Juiste stam, verkeerde naamval/uitgang: '{answer}' i.p.v. '{expected}'."


def classify_mismatch(
    answer: str,
    expected: str,
    *,
    language: Language,
    inflection: InflectionKind | None = None,
    synonym_pool: frozenset[str] | None = None,
) -> tuple[MismatchType, str | None]:
    """Classify a *wrong* answer against the expected string.

    All inputs are assumed already normalized by :func:`_normalize`.
    The caller guarantees ``answer != expected``. ``synonym_pool`` holds
    normalized accepted answers of *other* items in the same semantic
    cluster; a match there means the learner produced a real word from
    the wrong slot.

    Returns ``(mismatch_type, hint)``. ``hint`` is Dutch, mentor-facing,
    and may be ``None`` for :attr:`MismatchType.ONBEKEND`.
    """
    if not answer:
        return MismatchType.ONBEKEND, None

    # 1. Synonym: an exact hit on a sibling-cluster answer is the
    #    strongest signal, even if it happens to share a stem.
    if synonym_pool and answer in synonym_pool:
        return (
            MismatchType.SYNONIEM,
            f"'{answer}' bestaat, maar hoort bij een ander woord — gevraagd was '{expected}'.",
        )

    # 2. Diacritics only: same letters, different marks.
    if _strip_diacritics(answer) == _strip_diacritics(expected):
        if language == Language.GRC:
            hint = f"Let op de accenten/spiritus: '{answer}' i.p.v. '{expected}'."
        else:
            hint = f"Let op de lengtetekens (macron): '{answer}' i.p.v. '{expected}'."
        return MismatchType.MACRON, hint

    # 3. Shared stem, different ending → wrong case / wrong conjugation.
    prefix = _common_prefix_len(answer, expected)
    shorter = min(len(answer), len(expected))
    answer_ending = answer[prefix:]
    expected_ending = expected[prefix:]
    if (
        prefix >= 2
        and prefix * 2 >= shorter
        and len(answer_ending) <= 4
        and len(expected_ending) <= 4
    ):
        kind = (
            MismatchType.VERBUIGING
            if inflection == InflectionKind.VERBAL
            else MismatchType.NAAMVAL
        )
        return kind, _ending_hint(answer, expected, kind)

    # 4. Small typo.
    if _levenshtein(answer, expected, max_distance=2) <= 2:
        return (
            MismatchType.SPELLING,
            f"Spelling: '{answer}' ligt dicht bij '{expected}' — controleer de letters.",
        )

    # 5. Nothing matched.
    return MismatchType.ONBEKEND, None


# --- Public API ---


def grade_answer(
    raw_answer: str,
    item: Item,
    language: Language,
    *,
    synonym_pool: frozenset[str] | None = None,
) -> GradingResult:
    """Compare a learner's answer against the item's expected answer.

    Args:
        raw_answer: Exactly what the learner typed (or the MC-option
            they selected).  Leading/trailing whitespace is tolerated.
        item: The Item being graded.  ``item.answer`` may be a single
            string or a list of acceptable strings.
        language: The language of the node, used to pick normalization
            rules (macron-tolerant for Latin).
        synonym_pool: Optional raw accepted answers of *other* items in
            the same semantic cluster.  When the learner's wrong answer
            matches one, the mismatch is classified as ``SYNONIEM``.
            Defaults to None so existing callers are unaffected.

    Returns:
        A :class:`GradingResult` with the boolean, the normalized strings
        that were compared, and — for wrong answers — a
        :class:`MismatchType` plus a Dutch mentor-facing ``hint``.  The
        raw answer is intentionally not echoed back — callers store it
        separately.
    """
    normalized_answer = _normalize(raw_answer, language)
    variants = _expected_variants(item.answer)
    normalized_variants = [_normalize(v, language) for v in variants]

    correct = any(normalized_answer == v for v in normalized_variants) and bool(normalized_answer)

    # Prefer the first variant as the "canonical" expected string for
    # storage and future display.  If there are no variants at all
    # (should not happen for real items), fall back to an empty string.
    canonical_expected = normalized_variants[0] if normalized_variants else ""

    mismatch_type: MismatchType | None = None
    hint: str | None = None
    if not correct and normalized_answer and normalized_variants:
        # Diagnose against the closest acceptable variant, not blindly the
        # first — matters for list-answers where the learner aimed at a
        # later synonym.
        closest = min(
            normalized_variants,
            key=lambda v: _levenshtein(
                normalized_answer, v, max_distance=len(v) + len(normalized_answer)
            ),
        )
        pool = (
            frozenset(_normalize(s, language) for s in synonym_pool)
            if synonym_pool is not None
            else None
        )
        mismatch_type, hint = classify_mismatch(
            normalized_answer,
            closest,
            language=language,
            inflection=infer_inflection(item),
            synonym_pool=pool,
        )

    return GradingResult(
        correct=correct,
        normalized_answer=normalized_answer,
        normalized_expected=canonical_expected,
        mismatch_type=mismatch_type,
        hint=hint,
    )


def canonical_expected_answer(item: Item) -> str:
    """Return the first acceptable answer string, unnormalized.

    Handy for snapshotting ``item.answer`` onto an ItemResponse so
    later analysis doesn't depend on the item still existing in its
    current form.
    """
    variants = _expected_variants(item.answer)
    return variants[0] if variants else ""
