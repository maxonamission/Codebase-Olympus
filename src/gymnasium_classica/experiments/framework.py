"""Lichtgewicht, deterministisch A/B-experiment- en variant-framework (L1-03).

Maakt leerstrategie-parameters controleerbaar variabel per leerling, zodat
ontwerpkeuzes meetbaar getoetst kunnen worden in plaats van aangenomen.

Ontwerp:
- ``StrategyParams`` bundelt tunebare parameters; de defaults reproduceren
  exact het huidige gedrag (geen regressie zonder actief experiment).
- Een ``Experiment`` wijst een leerling **deterministisch** (SHA-256 over
  ``naam:user_id``) en gebalanceerd aan een ``ExperimentArm`` toe.
- ``ACTIVE_EXPERIMENTS`` is in productie leeg → ``strategy_params_for``
  geeft altijd de defaults terug. Een experiment activeer je door het aan
  die lijst toe te voegen (test/onderzoek).

De toewijzing wordt op ``LearnerModel.experiment_arms`` vastgelegd, zodat de
meetlaag (L1-01/L1-02) uitkomsten per variant kan uitsplitsen.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, fields, replace
from typing import TYPE_CHECKING
from uuid import UUID

if TYPE_CHECKING:
    from gymnasium_classica.models.learner import LearnerModel


@dataclass(frozen=True)
class StrategyParams:
    """Tunebare strategie-parameters. Defaults == huidig productiegedrag."""

    spacing_multiplier: float = 1.0
    """Schaalt de SM-2-review-intervallen. 1.0 = ongewijzigd."""
    motivation_enabled: bool = True
    """Of de motivatie-uitlegmomenten actief zijn (L3-02). Variant-baar."""


DEFAULT_PARAMS = StrategyParams()


@dataclass(frozen=True)
class ExperimentArm:
    """Eén variant binnen een experiment, met de bijbehorende parameters."""

    name: str
    params: StrategyParams = DEFAULT_PARAMS


@dataclass(frozen=True)
class Experiment:
    """Een experiment dat leerlingen deterministisch over armen verdeelt."""

    name: str
    arms: tuple[ExperimentArm, ...]

    def __post_init__(self) -> None:
        if len(self.arms) < 2:
            raise ValueError(f"Experiment {self.name!r} needs at least 2 arms.")
        if len({a.name for a in self.arms}) != len(self.arms):
            raise ValueError(f"Experiment {self.name!r} has duplicate arm names.")

    def assign(self, user_id: UUID | str) -> ExperimentArm:
        """Deterministische, gebalanceerde toewijzing op basis van user-id."""
        digest = hashlib.sha256(f"{self.name}:{user_id}".encode()).hexdigest()
        return self.arms[int(digest, 16) % len(self.arms)]


# Productie: leeg → default gedrag. Vul aan om een experiment te activeren.
ACTIVE_EXPERIMENTS: list[Experiment] = []


def assign_variants(user_id: UUID | str) -> dict[str, str]:
    """Wijs *user_id* aan een arm toe per actief experiment: {exp: arm}."""
    return {exp.name: exp.assign(user_id).name for exp in ACTIVE_EXPERIMENTS}


def _merge(base: StrategyParams, override: StrategyParams) -> StrategyParams:
    """Overlay niet-default velden van *override* op *base* (veld-voor-veld)."""
    changes = {
        f.name: getattr(override, f.name)
        for f in fields(StrategyParams)
        if getattr(override, f.name) != getattr(DEFAULT_PARAMS, f.name)
    }
    return replace(base, **changes)


def resolve_params(arms: dict[str, str]) -> StrategyParams:
    """Bouw de effectieve parameters uit vastgelegde arm-toewijzingen."""
    params = DEFAULT_PARAMS
    for exp in ACTIVE_EXPERIMENTS:
        arm_name = arms.get(exp.name)
        if arm_name is None:
            continue
        arm = next((a for a in exp.arms if a.name == arm_name), None)
        if arm is not None:
            params = _merge(params, arm.params)
    return params


def strategy_params_for(learner: LearnerModel) -> StrategyParams:
    """Effectieve strategie-parameters voor *learner*.

    Wijst (en registreert) de leerling lazily toe aan actieve experimenten.
    Zonder actieve experimenten een no-op: levert ``DEFAULT_PARAMS``.
    """
    if ACTIVE_EXPERIMENTS and not learner.experiment_arms:
        learner.experiment_arms = assign_variants(learner.user_id)
    return resolve_params(learner.experiment_arms)
