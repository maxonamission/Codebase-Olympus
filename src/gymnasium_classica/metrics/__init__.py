"""Meetlaag (L1-01): afgeleide retentie- en effectgrootte-metriek.

Deze module berekent metriek *uit* het bestaande learner-model; ze slaat
zelf niets op. Zie ``docs/ONTWERPKEUZES_GYMNASIUM_CLASSICA.md`` keuze 12.
"""

from gymnasium_classica.metrics.retention import (
    LearnerReport,
    build_learner_report,
    estimated_retention,
)

__all__ = ["LearnerReport", "build_learner_report", "estimated_retention"]
