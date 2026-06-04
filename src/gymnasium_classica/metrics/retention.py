"""Retentie- en voortgangsmetriek afgeleid uit het learner-model.

De functies hier reconstrueren retentie over tijd en aggregeren per
leerling, zodat de centrale projectclaim (efficiënter leren) testable
wordt. Alles is een *pure* functie over ``LearnerModel`` / ``NodeState``;
er wordt niets gemuteerd of opgeslagen.

De retentie-schatting is een bewuste eerste-orde heuristiek (exponentiële
vergeetcurve met het SM-2-interval als proxy voor geheugenstabiliteit).
Een gekalibreerd model (FSRS / half-life regression) kan dit later
vervangen zonder de aanroepende code te raken — zie het sprintplan.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import datetime

from gymnasium_classica.models.learner import LearnerModel, NodeState

# Drempels voor de mastery-verdeling. Bewust apart van de scheduler-drempel
# (priority.MASTERY_THRESHOLD = 0.75): dit is rapportage, geen planning.
NEW_MAX = 0.3  # posterior < NEW_MAX  -> nog niet begonnen / net gestart
MASTERED_MIN = 0.85  # posterior >= MASTERED_MIN -> beheerst
# Tussenin (NEW_MAX <= posterior < MASTERED_MIN) telt als "learning".

# Labels voor reviews per direction; "unknown" vangt self-assessment (geen item).
_DIRECTION_UNKNOWN = "unknown"


def estimated_retention(state: NodeState, now: datetime) -> float:
    """Schat de kans dat *state* op tijdstip *now* nog wordt herinnerd.

    Exponentiële vergeetcurve ``R = exp(-Δdagen / stabiliteit)`` met het
    SM-2-interval als stabiliteit: op het reviewmoment is ``R = 1.0`` en het
    daalt met een halfwaardetijd van ongeveer ``stabiliteit · ln2`` dagen.
    Een node die nog nooit gereviewd is, valt terug op de huidige
    posterior mastery (er is nog geen vergeetinformatie).

    De uitkomst ligt in [0.0, 1.0].
    """
    if state.last_review is None:
        return state.posterior_mastery
    days = (now - state.last_review).total_seconds() / 86400.0
    if days <= 0.0:
        return 1.0
    stability = max(state.interval_days, 1.0)
    return math.exp(-days / stability)


@dataclass(frozen=True)
class LearnerReport:
    """Samenvattende metriek voor één leerling op een tijdstip."""

    total_reviews: int
    """Aantal vastgelegde antwoorden over alle nodes heen."""
    total_study_seconds: float
    """Som van de duur van afgeronde sessies (ended_at - started_at)."""
    average_retention: float | None
    """Gemiddelde geschatte retentie over gereviewde nodes; None als er geen zijn."""
    mastery_distribution: dict[str, int]
    """Aantal nodes per bucket: 'new' / 'learning' / 'mastered'."""
    reviews_by_direction: dict[str, int]
    """Aantal antwoorden per direction: 'receptive' / 'productive' / 'unknown'."""


def _mastery_bucket(posterior: float) -> str:
    if posterior < NEW_MAX:
        return "new"
    if posterior >= MASTERED_MIN:
        return "mastered"
    return "learning"


def build_learner_report(learner: LearnerModel, now: datetime) -> LearnerReport:
    """Aggregeer het learner-model tot een :class:`LearnerReport` op *now*."""
    total_reviews = 0
    retentions: list[float] = []
    mastery_distribution = {"new": 0, "learning": 0, "mastered": 0}
    reviews_by_direction = {"receptive": 0, "productive": 0, _DIRECTION_UNKNOWN: 0}

    for state in learner.node_states.values():
        mastery_distribution[_mastery_bucket(state.posterior_mastery)] += 1
        if state.last_review is not None:
            retentions.append(estimated_retention(state, now))
        total_reviews += len(state.item_history)
        for response in state.item_history:
            key = response.direction if response.direction in ("receptive", "productive") else None
            reviews_by_direction[key or _DIRECTION_UNKNOWN] += 1

    total_study_seconds = sum(
        (session.ended_at - session.started_at).total_seconds()
        for session in learner.session_history
        if session.ended_at is not None
    )

    average_retention = sum(retentions) / len(retentions) if retentions else None

    return LearnerReport(
        total_reviews=total_reviews,
        total_study_seconds=total_study_seconds,
        average_retention=average_retention,
        mastery_distribution=mastery_distribution,
        reviews_by_direction=reviews_by_direction,
    )
