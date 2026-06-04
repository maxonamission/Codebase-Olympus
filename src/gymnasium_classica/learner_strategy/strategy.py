"""Learner-model-strategie-interface (L2-02, ontwerpkeuze 14).

Abstraheert het learner model achter een ``LearnerModelStrategy`` zodat het
interpreteerbare BKT later vervangbaar is door PFA/logistische of graph-aware
modellen — zonder de aanroepende code (scheduler/sessie) te wijzigen.

- ``BKTStrategy``: de default; delegeert naar de bestaande BKT-functies en
  reproduceert het huidige gedrag exact (pariteit).
- ``GraphAwareBKTStrategy``: stelt de prior van een knoop bij op basis van de
  mastery van prerequisite-/transfer-buren (gewogen met ``encompassing_weight``)
  vóór de BKT-update — prerequisite-driven knowledge tracing.

De actieve strategie is module-globaal (``get_strategy``/``set_strategy``);
default = ``BKTStrategy`` → geen gedragsregressie.

Buiten scope: neurale/deep knowledge tracing.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

import networkx as nx

from gymnasium_classica.models.graph import Direction, EdgeType, PrerequisiteEdge
from gymnasium_classica.models.learner import LearnerModel, NodeState, ResponseType
from gymnasium_classica.scheduling.bkt import (
    POSTERIOR_MAX,
    POSTERIOR_MIN,
    BKTParams,
    _get_or_create_state,
    propagate_practice_correct,
    update_node_state,
)

# Buurtypes die het graph-signaal voeden (inkomende edges).
_NEIGHBOUR_EDGE_TYPES = (EdgeType.PREREQUISITE, EdgeType.TRANSFER)

_CORRECT_RESPONSES = (ResponseType.CORRECT, ResponseType.SLOW_CORRECT)
_DEFAULT_PRIOR = 0.10


class LearnerModelStrategy(ABC):
    """Interface voor mastery-predictie en -update per knoop."""

    @abstractmethod
    def predict(
        self, learner: LearnerModel, node_id: str, *, direction: Direction | None = None
    ) -> float:
        """Voorspelde mastery (kans op correct) voor een knoop/richting."""

    @abstractmethod
    def update(
        self,
        learner: LearnerModel,
        graph: nx.DiGraph,
        node_id: str,
        response: ResponseType,
        *,
        direction: Direction | None = None,
        params: BKTParams | None = None,
    ) -> NodeState:
        """Werk de state van een knoop bij na een respons en return die state."""


class BKTStrategy(LearnerModelStrategy):
    """Default: standaard-BKT + praktijk-propagatie (huidige gedrag)."""

    def predict(
        self, learner: LearnerModel, node_id: str, *, direction: Direction | None = None
    ) -> float:
        state = learner.node_states.get(node_id)
        return state.mastery_for(direction) if state is not None else _DEFAULT_PRIOR

    def update(
        self,
        learner: LearnerModel,
        graph: nx.DiGraph,
        node_id: str,
        response: ResponseType,
        *,
        direction: Direction | None = None,
        params: BKTParams | None = None,
    ) -> NodeState:
        state = update_node_state(learner, node_id, response, params, direction)
        if response in _CORRECT_RESPONSES:
            propagate_practice_correct(learner, graph, node_id)
        return state


class GraphAwareBKTStrategy(BKTStrategy):
    """Graph-aware BKT: stelt de prior bij op basis van buren-mastery.

    Vóór de BKT-update wordt de prior van de knoop geblend richting een
    gewogen gemiddelde van de mastery van zijn prerequisite-/transfer-buren
    (gewogen met ``encompassing_weight``). Zonder relevante buren is het
    identiek aan ``BKTStrategy``.
    """

    def __init__(self, graph_influence: float = 0.3) -> None:
        if not 0.0 <= graph_influence <= 1.0:
            raise ValueError("graph_influence must be in [0.0, 1.0].")
        self.graph_influence = graph_influence

    def _neighbour_signal(
        self,
        learner: LearnerModel,
        graph: nx.DiGraph,
        node_id: str,
        direction: Direction | None,
    ) -> float | None:
        """Gewogen gemiddelde buren-mastery, of None als er geen buren zijn."""
        weighted_sum = 0.0
        total_weight = 0.0
        for pred in graph.predecessors(node_id):
            edge = graph.edges[pred, node_id].get("edge")
            if not isinstance(edge, PrerequisiteEdge) or edge.type not in _NEIGHBOUR_EDGE_TYPES:
                continue
            neighbour = learner.node_states.get(pred)
            mastery = neighbour.mastery_for(direction) if neighbour is not None else 0.0
            weighted_sum += edge.encompassing_weight * mastery
            total_weight += edge.encompassing_weight
        if total_weight == 0.0:
            return None
        return weighted_sum / total_weight

    def _blend_prior(self, prior: float, signal: float) -> float:
        blended = (1.0 - self.graph_influence) * prior + self.graph_influence * signal
        return max(POSTERIOR_MIN, min(POSTERIOR_MAX, blended))

    def update(
        self,
        learner: LearnerModel,
        graph: nx.DiGraph,
        node_id: str,
        response: ResponseType,
        *,
        direction: Direction | None = None,
        params: BKTParams | None = None,
    ) -> NodeState:
        signal = self._neighbour_signal(learner, graph, node_id, direction)
        if signal is not None:
            state = _get_or_create_state(learner, node_id)
            # Stel de prior(s) bij die de BKT-update vervolgens gebruikt.
            state.posterior_mastery = self._blend_prior(state.posterior_mastery, signal)
            if direction == Direction.RECEPTIVE:
                state.receptive_mastery = self._blend_prior(state.receptive_mastery, signal)
            elif direction == Direction.PRODUCTIVE:
                state.productive_mastery = self._blend_prior(state.productive_mastery, signal)
        return super().update(
            learner, graph, node_id, response, direction=direction, params=params
        )


_active_strategy: LearnerModelStrategy = BKTStrategy()


def get_strategy() -> LearnerModelStrategy:
    """De actieve learner-model-strategie (default: BKT)."""
    return _active_strategy


def set_strategy(strategy: LearnerModelStrategy) -> None:
    """Wissel de actieve strategie (config/experiment), zonder callers te raken."""
    global _active_strategy
    _active_strategy = strategy
