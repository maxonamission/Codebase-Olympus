"""Tests voor receptieve/productieve mastery-splitsing (L2-01)."""

from uuid import uuid4

import networkx as nx

from gymnasium_classica.models.graph import Direction, EdgeType, PrerequisiteEdge
from gymnasium_classica.models.learner import LearnerModel, NodeState, ResponseType
from gymnasium_classica.scheduling.bkt import update_node_state
from gymnasium_classica.scheduling.priority import readiness_score


class TestMasteryFor:
    def test_routes_per_direction(self):
        state = NodeState(
            node_id="LAT-G-X",
            posterior_mastery=0.5,
            receptive_mastery=0.3,
            productive_mastery=0.7,
        )
        assert state.mastery_for(None) == 0.5
        assert state.mastery_for(Direction.RECEPTIVE) == 0.3
        assert state.mastery_for(Direction.PRODUCTIVE) == 0.7

    def test_combined_is_min_of_both(self):
        state = NodeState(node_id="LAT-G-X", receptive_mastery=0.6, productive_mastery=0.2)
        assert state.combined_mastery == 0.2


class TestBktRouting:
    def test_receptive_item_moves_only_receptive(self):
        learner = LearnerModel(user_id=uuid4())
        update_node_state(learner, "LAT-G-X", ResponseType.CORRECT, direction=Direction.RECEPTIVE)
        state = learner.node_states["LAT-G-X"]
        assert state.receptive_mastery > 0.0
        assert state.productive_mastery == 0.0  # niet bewogen
        assert state.posterior_mastery > 0.10  # overall wel bijgewerkt

    def test_productive_item_moves_only_productive(self):
        learner = LearnerModel(user_id=uuid4())
        update_node_state(learner, "LAT-G-Y", ResponseType.CORRECT, direction=Direction.PRODUCTIVE)
        state = learner.node_states["LAT-G-Y"]
        assert state.productive_mastery > 0.0
        assert state.receptive_mastery == 0.0

    def test_no_direction_leaves_split_untouched(self):
        """Default (geen richting) reproduceert het oorspronkelijke gedrag."""
        learner = LearnerModel(user_id=uuid4())
        update_node_state(learner, "LAT-G-Z", ResponseType.CORRECT)
        state = learner.node_states["LAT-G-Z"]
        assert state.posterior_mastery > 0.10  # overall bijgewerkt zoals voorheen
        assert state.receptive_mastery == 0.0
        assert state.productive_mastery == 0.0

    def test_incorrect_receptive_does_not_touch_productive(self):
        learner = LearnerModel(user_id=uuid4())
        learner.node_states["LAT-G-X"] = NodeState(node_id="LAT-G-X", productive_mastery=0.6)
        update_node_state(
            learner, "LAT-G-X", ResponseType.INCORRECT, direction=Direction.RECEPTIVE
        )
        assert learner.node_states["LAT-G-X"].productive_mastery == 0.6


class TestReadinessPerDirection:
    def _graph(self) -> nx.DiGraph:
        g = nx.DiGraph()
        g.add_node("LAT-G-A")
        g.add_node("LAT-G-B")
        g.add_edge(
            "LAT-G-A",
            "LAT-G-B",
            edge=PrerequisiteEdge(
                source_id="LAT-G-A",
                target_id="LAT-G-B",
                type=EdgeType.PREREQUISITE,
                encompassing_weight=1.0,
            ),
        )
        return g

    def _learner_split_prereq(self) -> LearnerModel:
        # Prerequisite: receptief beheerst (0.8), productief nog niet (0.2).
        learner = LearnerModel(user_id=uuid4())
        learner.node_states["LAT-G-A"] = NodeState(
            node_id="LAT-G-A",
            posterior_mastery=0.8,
            receptive_mastery=0.8,
            productive_mastery=0.2,
        )
        return learner

    def test_default_uses_overall_posterior(self):
        g, learner = self._graph(), self._learner_split_prereq()
        # Overall 0.8 >= drempel → klaar (huidig gedrag, ongewijzigd).
        assert readiness_score("LAT-G-B", learner, g) > 0.0

    def test_productive_direction_gates_on_productive_mastery(self):
        g, learner = self._graph(), self._learner_split_prereq()
        # Productief 0.2 < drempel → gate dicht.
        assert readiness_score("LAT-G-B", learner, g, direction=Direction.PRODUCTIVE) == 0.0

    def test_receptive_direction_passes(self):
        g, learner = self._graph(), self._learner_split_prereq()
        assert readiness_score("LAT-G-B", learner, g, direction=Direction.RECEPTIVE) > 0.0
