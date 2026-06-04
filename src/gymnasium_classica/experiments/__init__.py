"""Experiments subpackage: deterministic A/B variant assignment (L1-03)."""

from gymnasium_classica.experiments.framework import (
    ACTIVE_EXPERIMENTS,
    DEFAULT_PARAMS,
    Experiment,
    ExperimentArm,
    StrategyParams,
    assign_variants,
    resolve_params,
    strategy_params_for,
)

__all__ = [
    "ACTIVE_EXPERIMENTS",
    "DEFAULT_PARAMS",
    "Experiment",
    "ExperimentArm",
    "StrategyParams",
    "assign_variants",
    "resolve_params",
    "strategy_params_for",
]
