"""Meetlaag (L1-01): afgeleide retentie- en effectgrootte-metriek.

Deze module berekent metriek *uit* het bestaande learner-model; ze slaat
zelf niets op. Zie ``docs/ONTWERPKEUZES_GYMNASIUM_CLASSICA.md`` keuze 12.
"""

from gymnasium_classica.metrics.effect_size import (
    CohortReport,
    LearnerProgress,
    capture_baseline,
    cohort_report,
    learner_progress,
)
from gymnasium_classica.metrics.retention import (
    LearnerReport,
    build_learner_report,
    estimated_retention,
)

__all__ = [
    "CohortReport",
    "LearnerProgress",
    "LearnerReport",
    "build_learner_report",
    "capture_baseline",
    "cohort_report",
    "estimated_retention",
    "learner_progress",
]
