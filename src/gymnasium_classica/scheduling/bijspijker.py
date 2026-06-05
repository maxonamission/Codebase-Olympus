"""Catch-up planner for bijspijker mode (M1-03).

Where the staatsexamen scheduler optimises long-horizon mastery of the
exam end-terms, the :class:`BijspijkerPlanner` optimises a short-horizon
goal: getting a learner *bij* (up to speed) with a school method and
chapter as fast as possible. It replicates Wijkunnenmeer's "overhoren"
practice — diagnose what is missing up to the class's chapter, catch up
quickly, and close each session with a translation from that chapter.

The planner is pure: given a learner and one or more method/chapter
targets it returns a :class:`BijspijkerPlan`. Turning that plan into a
session is the scheduler's job (the cool-down nodes and intro tempo feed
``run_session``).
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

import networkx as nx

from gymnasium_classica.diagnostic.methode_profile import (
    MethodeMapping,
    get_treated_node_ids,
    load_methode_mapping,
)
from gymnasium_classica.graph.validation import acyclic_subgraph, topological_sort

if TYPE_CHECKING:
    from gymnasium_classica.models.learner import LearnerModel


@dataclass(frozen=True)
class BijspijkerConfig:
    """Tunable parameters for the catch-up planner."""

    mastery_threshold: float = 0.70
    """A node counts as mastered (bij) at or above this posterior."""
    intro_per_sessie: int = 4
    """New nodes introduced per session — catch-up tempo (3-5), vs. 1-2 staatsexamen."""


DEFAULT_BIJSPIJKER_CONFIG = BijspijkerConfig()


@dataclass(frozen=True)
class BijspijkerTarget:
    """One language's catch-up goal: a method up to a chapter."""

    methode: str
    hoofdstuk: int


@dataclass
class BijspijkerPlan:
    """Result of planning a catch-up route."""

    doelset: list[str] = field(default_factory=list)
    diagnose: list[str] = field(default_factory=list)
    cooldown_node_ids: list[str] = field(default_factory=list)
    fractie_bij: float = 0.0
    is_bij: bool = False
    suggest_chapter_bump: bool = False
    intro_per_sessie: int = 0
    eta_dagen: int = 0


class BijspijkerPlanner:
    """Plans an accelerated catch-up route towards a method/chapter goal."""

    def __init__(
        self,
        graph: nx.DiGraph,
        mapping: MethodeMapping | None = None,
        config: BijspijkerConfig = DEFAULT_BIJSPIJKER_CONFIG,
    ) -> None:
        self.graph = graph
        self.mapping = mapping if mapping is not None else load_methode_mapping()
        self.config = config
        # Prerequisite-only subgraph for transitive closure (no transfer edges).
        self._prereq_graph = acyclic_subgraph(graph, include_edge_types={"prerequisite"})
        topo = topological_sort(graph)
        self._topo_index = {node_id: i for i, node_id in enumerate(topo or [])}

    def _target_node_ids(self, target: BijspijkerTarget) -> set[str]:
        """Nodes treated up to the target chapter, plus their prerequisites."""
        treated = get_treated_node_ids(self.mapping, target.methode, str(target.hoofdstuk))
        closure: set[str] = set(treated)
        for node_id in treated:
            if node_id in self._prereq_graph:
                closure.update(nx.ancestors(self._prereq_graph, node_id))
        return closure

    def _chapter_node_ids(self, target: BijspijkerTarget) -> list[str]:
        """Node IDs of exactly the target chapter (used as cool-down context)."""
        methode_data = self.mapping["methoden"].get(target.methode, {})
        chapter = methode_data.get("hoofdstukken", {}).get(str(target.hoofdstuk), {})
        return list(chapter.get("node_ids", []))

    def _mastery(self, learner: LearnerModel, node_id: str) -> float:
        state = learner.node_states.get(node_id)
        return state.posterior_mastery if state else 0.0

    def _has_practised(self, learner: LearnerModel, node_id: str) -> bool:
        state = learner.node_states.get(node_id)
        return bool(state and state.item_history)

    def plan(self, learner: LearnerModel, targets: list[BijspijkerTarget]) -> BijspijkerPlan:
        """Build a catch-up plan for the given per-language targets."""
        doelset: set[str] = set()
        cooldown: list[str] = []
        for target in targets:
            doelset.update(self._target_node_ids(target))
            cooldown.extend(self._chapter_node_ids(target))

        threshold = self.config.mastery_threshold
        # Diagnose: unmastered OR not yet verified by any practice (story step 2).
        diagnose = [
            node_id
            for node_id in doelset
            if self._mastery(learner, node_id) < threshold
            or not self._has_practised(learner, node_id)
        ]
        # Sequencing: topological order so prerequisites are introduced first.
        diagnose.sort(key=lambda nid: self._topo_index.get(nid, len(self._topo_index)))

        mastered = sum(1 for nid in doelset if self._mastery(learner, nid) >= threshold)
        fractie_bij = mastered / len(doelset) if doelset else 0.0
        is_bij = len(diagnose) == 0

        intro = self.config.intro_per_sessie
        eta_dagen = math.ceil(len(diagnose) / intro) if intro > 0 else 0

        return BijspijkerPlan(
            doelset=sorted(doelset),
            diagnose=diagnose,
            cooldown_node_ids=cooldown,
            fractie_bij=fractie_bij,
            is_bij=is_bij,
            suggest_chapter_bump=is_bij,
            intro_per_sessie=intro,
            eta_dagen=eta_dagen,
        )
