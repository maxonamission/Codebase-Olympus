"""Equity-waarborgen voor zwakkere leerlingen (L3-03, ontwerpkeuze 16b).

ITS-systemen helpen de gemiddelde leerling vaak méér dan zwakke presteerders
(Steenbergen-Hu & Cooper, 2013), terwijl remediatie juist een doelgroep van
dit project is. Deze laag verhoogt voor structureel-onderpresterende leerlingen
de prerequisite-drempel vóór nieuw materiaal: meer consolidatie, minder nieuw.

Het signaal hergebruikt de individuele leersnelheid (L2-03): een leerling die
structureel onder de modelverwachting blijft heeft ``learning_rate < 1.0``.
De aanpassing is **gradueel** (schaalt met hoe ver de rate onder 1.0 ligt),
**gecapt**, en **zelfherstellend** (zodra de rate weer richting 1.0 kruipt,
verdwijnt de boost vanzelf). Leerlingen op koers (rate >= 1.0) houden het
ongewijzigde gedrag.
"""

from __future__ import annotations

from gymnasium_classica.models.learner import LearnerModel
from gymnasium_classica.scheduling.priority import PREREQ_READY_THRESHOLD

EQUITY_RATE_FLOOR = 1.0
"""Op/boven deze leersnelheid is er geen aanpassing (leerling op koers)."""
EQUITY_SENSITIVITY = 0.3
"""Hoeveel de drempel stijgt per eenheid leersnelheid onder de floor."""
EQUITY_MAX_BOOST = 0.15
"""Maximale verhoging van de prerequisite-drempel (cap)."""


def is_low_mastery_trajectory(learner: LearnerModel) -> bool:
    """Of de leerling structureel onder de verwachte voortgang blijft (L1/L2)."""
    return learner.learning_rate < EQUITY_RATE_FLOOR


def equity_prereq_threshold(learner: LearnerModel, base: float | None = None) -> float:
    """Prerequisite-drempel voor nieuw materiaal, equity-gecorrigeerd.

    Op-koers-leerlingen krijgen *base* (default ``PREREQ_READY_THRESHOLD``);
    zwakkere leerlingen een gradueel hogere, gecapte drempel.
    """
    threshold = PREREQ_READY_THRESHOLD if base is None else base
    rate = learner.learning_rate
    if rate >= EQUITY_RATE_FLOOR:
        return threshold
    boost = min(EQUITY_MAX_BOOST, EQUITY_SENSITIVITY * (EQUITY_RATE_FLOOR - rate))
    return min(0.99, threshold + boost)
