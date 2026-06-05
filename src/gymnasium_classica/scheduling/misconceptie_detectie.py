"""Detection of systematic misconceptions from BKT aggregates (M1-02).

The first misconception is the "Lego-vertaler": a learner who knows the
vocabulary but stacks word meanings without parsing the sentence. Two
learners with identical BKT scores can differ in whether they actually
parse; this rule-based heuristic separates them by comparing mastery
*across* node categories (vocabulary vs. morphology vs. translation).

The thresholds live in a single :class:`LegoDetectorConfig` so they can be
recalibrated on pilot data without touching the detection logic.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING

from gymnasium_classica.models.learner import LearnerModel
from gymnasium_classica.models.misconception_flag import MisconceptionFlag

if TYPE_CHECKING:
    import networkx as nx

    from gymnasium_classica.models.graph import Node

LEGO_CODE = "LEGO_VERTALEN"

LEGO_SESSION_MESSAGE = (
    "Je vertalingen lopen vooruit op je grammatica. We oefenen daarom "
    "even extra met ontleden voordat we verder gaan met vertalen."
)


@dataclass(frozen=True)
class LegoDetectorConfig:
    """Tunable thresholds for the Lego-vertaler heuristic.

    Frozen so a shared default cannot be mutated by accident; pass a custom
    instance to recalibrate after a pilot.
    """

    min_avg_v: float = 0.70
    """Vocabulary (F01-F02) mastery must be at least this high."""
    max_avg_g_morf: float = 0.50
    """Morphology-concept mastery must be below this."""
    max_avg_i_vert: float = 0.40
    """Translation-integration mastery must be below this."""
    min_nodes_per_category: int = 1
    """Minimum observed nodes per category before the rule may fire."""
    boost_factor: float = 1.75
    """Urgency multiplier (1.5-2.0) applied to remediation/diagnostic nodes."""


DEFAULT_LEGO_CONFIG = LegoDetectorConfig()


def _segments(node_id: str) -> list[str]:
    return node_id.split("-")


def _is_vocab_f01_f02(node_id: str) -> bool:
    parts = _segments(node_id)
    return len(parts) >= 3 and parts[1] == "V" and parts[2] in {"F01", "F02"}


def _is_morphology(node_id: str) -> bool:
    parts = _segments(node_id)
    return len(parts) >= 3 and parts[1] == "G" and parts[2] == "MORF"


def _is_translation(node_id: str) -> bool:
    parts = _segments(node_id)
    return len(parts) >= 3 and parts[1] == "I" and parts[2] == "VERT"


def _category_average(
    learner: LearnerModel, predicate: Callable[[str], bool]
) -> tuple[float | None, int]:
    """Mean posterior mastery over node states whose ID matches ``predicate``.

    Returns ``(None, 0)`` when the learner has no observed nodes in the
    category, so callers can distinguish "weak" from "never practised".
    """
    values = [
        state.posterior_mastery
        for node_id, state in learner.node_states.items()
        if predicate(node_id)
    ]
    if not values:
        return None, 0
    return sum(values) / len(values), len(values)


def evaluate_lego_translator(
    learner: LearnerModel, config: LegoDetectorConfig = DEFAULT_LEGO_CONFIG
) -> MisconceptionFlag:
    """Evaluate the Lego-vertaler profile and return a detailed flag.

    The flag is active when all three conditions hold:
      - vocabulary (F01-F02) mastery is high (``avg_v >= min_avg_v``),
      - morphology-concept mastery is low (``avg_g_morf < max_avg_g_morf``),
      - translation-integration mastery is low (``avg_i_vert < max_avg_i_vert``).

    If any category lacks enough observed nodes the flag is inactive with a
    reason saying so — absence of translation practice is not the same as a
    misconception.
    """
    avg_v, n_v = _category_average(learner, _is_vocab_f01_f02)
    avg_g, n_g = _category_average(learner, _is_morphology)
    avg_i, n_i = _category_average(learner, _is_translation)

    min_n = config.min_nodes_per_category
    insufficient = [
        label
        for label, count in (("V", n_v), ("G-morfologie", n_g), ("I-vertalen", n_i))
        if count < min_n
    ]
    if insufficient or avg_v is None or avg_g is None or avg_i is None:
        return MisconceptionFlag(
            code=LEGO_CODE,
            active=False,
            avg_v=avg_v,
            avg_g_morf=avg_g,
            avg_i_vert=avg_i,
            reason=(
                "Onvoldoende waarnemingen om het profiel te bepalen "
                f"(te weinig data in: {', '.join(insufficient) or 'onbekend'})."
            ),
        )

    cond_v = avg_v >= config.min_avg_v
    cond_g = avg_g < config.max_avg_g_morf
    cond_i = avg_i < config.max_avg_i_vert
    active = cond_v and cond_g and cond_i

    if active:
        reason = (
            f"Woordenschat sterk (V={avg_v:.2f}) maar morfologie zwak "
            f"(G={avg_g:.2f}) en vertalen zwak (I={avg_i:.2f}): "
            "profiel Lego-vertaler actief."
        )
    else:
        misses = []
        if not cond_v:
            misses.append(f"woordenschat nog niet sterk genoeg (V={avg_v:.2f})")
        if not cond_g:
            misses.append(f"morfologie niet zwak genoeg (G={avg_g:.2f})")
        if not cond_i:
            misses.append(f"vertalen niet zwak genoeg (I={avg_i:.2f})")
        reason = "Profiel niet actief: " + "; ".join(misses) + "."

    return MisconceptionFlag(
        code=LEGO_CODE,
        active=active,
        avg_v=avg_v,
        avg_g_morf=avg_g,
        avg_i_vert=avg_i,
        reason=reason,
    )


def detect_lego_translator(
    learner: LearnerModel, config: LegoDetectorConfig = DEFAULT_LEGO_CONFIG
) -> bool:
    """Boolean shorthand for :func:`evaluate_lego_translator`."""
    return evaluate_lego_translator(learner, config).active


def lego_boost_targets(graph: nx.DiGraph) -> set[str]:
    """Node IDs that the Lego-vertaler remediation should prioritise.

    Collected from every ``LEGO_VERTALEN`` misconception in the graph: its
    ``remediation_nodes`` (POLMO steps + morphology concepts) plus the nodes
    that host its ``diagnostic_items`` (used as a peilstok/probe).
    """
    targets: set[str] = set()
    diagnostic_items: set[str] = set()
    for node_id in graph.nodes:
        node = graph.nodes[node_id].get("node")
        if node is None:
            continue
        for misc in node.known_misconceptions:
            if misc.code == LEGO_CODE:
                targets.update(misc.remediation_nodes)
                diagnostic_items.update(misc.diagnostic_items)

    if diagnostic_items:
        for node_id in graph.nodes:
            node = graph.nodes[node_id].get("node")
            if node is None:
                continue
            if any(item.id in diagnostic_items for item in node.items):
                targets.add(node_id)
    return targets


def apply_lego_boost(
    scored_nodes: list[tuple[float, Node]],
    learner: LearnerModel,
    graph: nx.DiGraph,
    config: LegoDetectorConfig = DEFAULT_LEGO_CONFIG,
) -> tuple[list[tuple[float, Node]], MisconceptionFlag]:
    """Re-rank urgency scores when the Lego-vertaler profile is active.

    Multiplies (never overrides) the urgency of remediation and diagnostic
    nodes by ``config.boost_factor``, so other urgencies stay respected. When
    the profile is inactive the scores are returned unchanged.

    Returns the (possibly re-ranked) scores and the :class:`MisconceptionFlag`
    so the caller can surface the reason.
    """
    flag = evaluate_lego_translator(learner, config)
    if not flag.active:
        return scored_nodes, flag

    targets = lego_boost_targets(graph)
    boosted = [
        (urgency * config.boost_factor if node.id in targets else urgency, node)
        for urgency, node in scored_nodes
    ]
    boosted.sort(key=lambda pair: pair[0], reverse=True)
    return boosted, flag


def lego_session_message(flag: MisconceptionFlag) -> str | None:
    """Learner-facing session message, or None when no profile is active.

    Deliberately jargon-free: the learner never sees the technical label
    "Lego-vertaler".
    """
    if flag.active and flag.code == LEGO_CODE:
        return LEGO_SESSION_MESSAGE
    return None
