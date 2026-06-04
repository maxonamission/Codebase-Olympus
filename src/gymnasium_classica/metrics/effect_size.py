"""Baseline-vastlegging en effectgrootte-rapportage (L1-02).

Bouwt voort op de meetlaag uit L1-01. De baseline is het mastery-nulpunt
op het moment van intake-afronding; voortgang en effectgrootte worden
hiertegen afgezet.

Belangrijk voorbehoud (zie ``docs/LITERATUURONDERZOEK_LEERBENADERING.md``):
de cohort-``cohen_d`` hier is een *within-cohort gestandaardiseerde winst*
(een one-sample d t.o.v. nul winst), GEEN gecontroleerde-trial-effectgrootte
— er is geen controlegroep. Het staatsexamen is de objectieve externe toets.
"""

from __future__ import annotations

import statistics
from dataclasses import dataclass
from datetime import datetime

from gymnasium_classica.models.learner import BaselineSnapshot, LearnerModel


def capture_baseline(learner: LearnerModel, captured_at: datetime) -> BaselineSnapshot:
    """Snapshot de huidige posterior mastery per node als baseline-nulpunt."""
    return BaselineSnapshot(
        captured_at=captured_at,
        mastery={kid: state.posterior_mastery for kid, state in learner.node_states.items()},
    )


@dataclass(frozen=True)
class LearnerProgress:
    """Voortgang van één leerling t.o.v. de eigen baseline."""

    baseline_mean: float
    current_mean: float
    mean_delta: float
    """current_mean - baseline_mean (ruwe mastery-winst)."""
    standardized_gain: float | None
    """mean_delta / baseline-SD over nodes; None als de baseline-SD 0 is."""
    n_nodes: int
    """Aantal baseline-nodes dat nog in het learner-model bestaat."""


def learner_progress(learner: LearnerModel) -> LearnerProgress | None:
    """Bereken voortgang t.o.v. de baseline. None als er geen baseline is."""
    if learner.baseline is None or not learner.baseline.mastery:
        return None

    baseline_values: list[float] = []
    current_values: list[float] = []
    for node_id, baseline_mastery in learner.baseline.mastery.items():
        state = learner.node_states.get(node_id)
        if state is None:
            continue
        baseline_values.append(baseline_mastery)
        current_values.append(state.posterior_mastery)

    if not baseline_values:
        return None

    baseline_mean = statistics.fmean(baseline_values)
    current_mean = statistics.fmean(current_values)
    mean_delta = current_mean - baseline_mean
    baseline_sd = statistics.pstdev(baseline_values) if len(baseline_values) > 1 else 0.0
    standardized_gain = mean_delta / baseline_sd if baseline_sd > 0 else None

    return LearnerProgress(
        baseline_mean=baseline_mean,
        current_mean=current_mean,
        mean_delta=mean_delta,
        standardized_gain=standardized_gain,
        n_nodes=len(baseline_values),
    )


@dataclass(frozen=True)
class CohortReport:
    """Geaggregeerde voortgang over een cohort leerlingen."""

    n_learners: int
    """Aantal leerlingen met een baseline (en dus voortgang)."""
    mean_delta: float | None
    """Gemiddelde van de per-leerling mean_delta; None als n_learners == 0."""
    sd_delta: float | None
    """Steekproef-SD van de per-leerling mean_delta; None als n_learners < 2."""
    cohen_d: float | None
    """Within-cohort gestandaardiseerde winst (mean_delta / sd_delta). GEEN
    gecontroleerde effectgrootte — zie module-docstring. None als n < 2 of SD 0."""


def cohort_report(learners: list[LearnerModel]) -> CohortReport:
    """Aggregeer de effectgrootte over meerdere leerlingen."""
    deltas = [
        progress.mean_delta
        for learner in learners
        if (progress := learner_progress(learner)) is not None
    ]
    n = len(deltas)
    if n == 0:
        return CohortReport(n_learners=0, mean_delta=None, sd_delta=None, cohen_d=None)

    mean_delta = statistics.fmean(deltas)
    if n < 2:
        return CohortReport(n_learners=n, mean_delta=mean_delta, sd_delta=None, cohen_d=None)

    sd_delta = statistics.stdev(deltas)
    cohen_d = mean_delta / sd_delta if sd_delta > 0 else None
    return CohortReport(n_learners=n, mean_delta=mean_delta, sd_delta=sd_delta, cohen_d=cohen_d)
