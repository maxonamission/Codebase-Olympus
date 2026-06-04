"""Motivatielaag tegen de metacognitieve illusie (L3-02, ontwerpkeuze 16a).

Effectieve "desirable difficult" oefening (spacing, retrieval, interleaving)
voelt zwaar en wordt door leerlingen systematisch onderschat — een reëel
afhaakrisico. Deze laag bepaalt op datagedreven momenten of een korte uitleg
relevant is ("dit voelt zwaar omdat het werkt") en koppelt mastery-winst aan
de geleverde inspanning.

Backend-triggerlogica + content; de visuele uitwerking is frontend (vervolg).
De toggle is variant-baar via L1-03 (``StrategyParams.motivation_enabled``).
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import StrEnum

from gymnasium_classica.experiments import strategy_params_for
from gymnasium_classica.models.learner import ItemResponse, LearnerModel


class MotivationMoment(StrEnum):
    """Soorten uitlegmomenten."""

    DESIRABLE_DIFFICULTY = "desirable_difficulty"
    RETRIEVAL_DIP = "retrieval_dip"
    PROGRESS_GAIN = "progress_gain"


# Korte, herbruikbare uitlegteksten in het Nederlands.
MESSAGES: dict[MotivationMoment, str] = {
    MotivationMoment.DESIRABLE_DIFFICULTY: (
        "Dit voelt zwaar — en dat is precies waarom het werkt. Moeite doen om "
        "iets terug te halen versterkt je geheugen sterker dan vlot herlezen."
    ),
    MotivationMoment.RETRIEVAL_DIP: (
        "Even kwijt en dan terughalen hoort erbij: juist dat ophalen ná een dip "
        "verankert de stof langdurig. Dit is normaal en gewenst."
    ),
    MotivationMoment.PROGRESS_GAIN: (
        "Je beheersing is merkbaar gestegen door deze inspanning — de zwaarte "
        "zet zich om in blijvende kennis."
    ),
}


@dataclass(frozen=True)
class MotivationConfig:
    """Instelbare, uitschakelbare trigger-drempels (geen opdringerigheid)."""

    enabled: bool = True
    min_hard_items: int = 3
    """Aantal opeenvolgende moeilijk-maar-correcte items voor 'desirable difficulty'."""
    hard_mastery_ceiling: float = 0.5
    """mastery_before <= dit telt als 'moeilijk' (geworsteld maar goed)."""
    dip_mastery_floor: float = 0.75
    """Een fout op een knoop die hierboven beheerst was = een (gewenste) dip."""
    progress_gain_threshold: float = 0.15
    """Gemiddelde mastery-winst boven dit niveau toont een voortgangssignaal."""


DEFAULT_MOTIVATION_CONFIG = MotivationConfig()


@dataclass(frozen=True)
class MotivationCue:
    """Een uitlegmoment met de bijbehorende tekst en (voor voortgang) de winst."""

    moment: MotivationMoment
    message: str
    mastery_gain: float = 0.0


def _recent_responses(learner: LearnerModel, limit: int) -> list[ItemResponse]:
    responses = [r for state in learner.node_states.values() for r in state.item_history]
    responses.sort(key=lambda r: r.timestamp)
    return responses[-limit:] if limit > 0 else responses


def _mean_recent_gain(learner: LearnerModel, limit: int) -> float:
    """Gemiddelde (huidige mastery - mastery_before) over recente antwoorden."""
    gains: list[float] = []
    for response in _recent_responses(learner, limit):
        state = learner.node_states.get(response.node_id)
        if state is not None:
            gains.append(state.posterior_mastery - response.mastery_before)
    return sum(gains) / len(gains) if gains else 0.0


def motivation_config_for(
    learner: LearnerModel, base: MotivationConfig = DEFAULT_MOTIVATION_CONFIG
) -> MotivationConfig:
    """Config voor een leerling, met de L1-03-variant-toggle meegenomen."""
    params = strategy_params_for(learner)
    return replace(base, enabled=base.enabled and params.motivation_enabled)


def evaluate_motivation(
    learner: LearnerModel, config: MotivationConfig = DEFAULT_MOTIVATION_CONFIG
) -> MotivationCue | None:
    """Bepaal of er nu een uitlegmoment relevant is; anders None.

    Prioriteit: retrieval-dip (geruststelling) → desirable difficulty (uitleg)
    → voortgangswinst (bevestiging). Levert None als de laag uitstaat of er
    onvoldoende observaties zijn.
    """
    if not config.enabled:
        return None

    recent = _recent_responses(learner, config.min_hard_items)
    if not recent:
        return None

    # 1. Retrieval-dip: het laatste antwoord is fout op een eerder-beheerste knoop.
    last = recent[-1]
    if not last.correct and last.mastery_before >= config.dip_mastery_floor:
        return MotivationCue(
            MotivationMoment.RETRIEVAL_DIP, MESSAGES[MotivationMoment.RETRIEVAL_DIP]
        )

    # 2. Desirable difficulty: een reeks moeilijke-maar-correcte items.
    if len(recent) >= config.min_hard_items and all(
        r.correct and r.mastery_before <= config.hard_mastery_ceiling for r in recent
    ):
        return MotivationCue(
            MotivationMoment.DESIRABLE_DIFFICULTY,
            MESSAGES[MotivationMoment.DESIRABLE_DIFFICULTY],
        )

    # 3. Voortgangssignaal: merkbare mastery-winst gekoppeld aan de inspanning.
    gain = _mean_recent_gain(learner, config.min_hard_items)
    if gain >= config.progress_gain_threshold:
        return MotivationCue(
            MotivationMoment.PROGRESS_GAIN,
            MESSAGES[MotivationMoment.PROGRESS_GAIN],
            mastery_gain=gain,
        )

    return None
