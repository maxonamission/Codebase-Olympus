"""Tests for the diagnostic intake system: method profile, adaptive
placement, and conditional completion (falling backwards).
"""

from pathlib import Path
from uuid import uuid4

import pytest

from gymnasium_classica.diagnostic.conditional_completion import apply_fallback
from gymnasium_classica.diagnostic.methode_profile import (
    PRIOR_TREATED,
    PRIOR_UNTREATED,
    apply_methode_profile,
    get_treated_knoop_ids,
    load_methode_mapping,
)
from gymnasium_classica.diagnostic.placement import (
    MASTERED_THRESHOLD,
    run_diagnostic,
)
from gymnasium_classica.graph.loader import load_graph
from gymnasium_classica.models.learner import LearnerModel, MasterySource


@pytest.fixture
def poc_graph(poc_graph_path):
    """Load the 50-node PoC graph."""
    if not poc_graph_path.exists():
        pytest.skip("PoC graph file not found")
    return load_graph(poc_graph_path)


@pytest.fixture
def methode_mapping():
    """Load the method mapping file."""
    path = Path(__file__).parent.parent / "data" / "methode_mapping.json"
    return load_methode_mapping(path)


@pytest.fixture
def fresh_learner():
    """A fresh learner model with no state."""
    return LearnerModel(user_id=uuid4())


# ============================================================
# Mechanism 1: School-method profile
# ============================================================


class TestMethodeProfile:
    """Tests for the school-method profile prior setting."""

    def test_fortuna_chapter_8_mapping_loads(self, methode_mapping):
        """The mapping file loads correctly and has the expected structure."""
        assert "fortuna" in methode_mapping["methoden"]
        fortuna = methode_mapping["methoden"]["fortuna"]
        assert fortuna["taal"] == "lat"
        assert "1" in fortuna["hoofdstukken"]

    def test_treated_knoop_ids_cumulative(self, methode_mapping):
        """Chapters are cumulative: chapter 3 includes 1, 2, and 3."""
        ch1_ids = get_treated_knoop_ids(methode_mapping, "fortuna", "1")
        ch3_ids = get_treated_knoop_ids(methode_mapping, "fortuna", "3")
        assert ch1_ids < ch3_ids  # strict subset

    def test_fortuna_chapter_5_covers_all_50_poc_nodes(self, methode_mapping, poc_graph):
        """Fortuna up to chapter 5 should cover all 50 PoC nodes."""
        treated = get_treated_knoop_ids(methode_mapping, "fortuna", "5")
        graph_ids = set(poc_graph.nodes)
        assert treated == graph_ids

    def test_apply_methode_profile_sets_priors(self, fresh_learner, poc_graph, methode_mapping):
        """After selecting 'fortuna hoofdstuk 2', all chapter 1+2 nodes get
        P(L₀) = 0.70 and the rest get P(L₀) = 0.10.
        """
        apply_methode_profile(fresh_learner, poc_graph, "fortuna", "2", mapping=methode_mapping)

        treated = get_treated_knoop_ids(methode_mapping, "fortuna", "2")

        for node_id in poc_graph.nodes:
            state = fresh_learner.knoop_states[node_id]
            if node_id in treated:
                assert state.posterior_mastery == pytest.approx(PRIOR_TREATED), (
                    f"Treated node {node_id} should have prior {PRIOR_TREATED}"
                )
            else:
                assert state.posterior_mastery == pytest.approx(PRIOR_UNTREATED), (
                    f"Untreated node {node_id} should have prior {PRIOR_UNTREATED}"
                )
            assert state.source == MasterySource.DIAGNOSTIC

    def test_apply_methode_profile_sets_intake_method(
        self, fresh_learner, poc_graph, methode_mapping
    ):
        apply_methode_profile(fresh_learner, poc_graph, "fortuna", "1", mapping=methode_mapping)
        assert fresh_learner.intake_method == "fortuna"

    def test_unknown_methode_raises(self, methode_mapping):
        with pytest.raises(ValueError, match="Unknown methode"):
            get_treated_knoop_ids(methode_mapping, "nonexistent", "1")


# ============================================================
# Mechanism 2: Adaptive diagnostic algorithm
# ============================================================


class TestAdaptivePlacement:
    """Tests for the adaptive diagnostic placement algorithm."""

    def test_converges_for_fully_mastered_learner(self, fresh_learner, poc_graph):
        """A learner who answers everything correctly converges quickly."""

        def always_correct(knoop_id: str) -> bool:
            return True

        result = run_diagnostic(fresh_learner, poc_graph, always_correct)
        assert result.converged is True
        assert result.questions_asked <= 30

    def test_converges_for_fully_unmastered_learner(self, fresh_learner, poc_graph):
        """A learner who answers everything incorrectly converges quickly."""

        def always_incorrect(knoop_id: str) -> bool:
            return False

        result = run_diagnostic(fresh_learner, poc_graph, always_incorrect)
        assert result.converged is True
        # Should converge fast: a few wrong answers push everything below threshold
        assert result.questions_asked <= 15

    def test_converges_within_15_questions_for_decl2_learner(
        self, fresh_learner, poc_graph, methode_mapping
    ):
        """A learner who has mastered everything through declension 2 (fortuna
        chapter 3): the diagnostic should find the frontier in ≤ 15 questions.
        """
        # Set up priors: chapters 1-3 treated (decl 1+2 + presens 1-2 + esse)
        apply_methode_profile(fresh_learner, poc_graph, "fortuna", "3", mapping=methode_mapping)

        treated = get_treated_knoop_ids(methode_mapping, "fortuna", "3")

        def simulated_learner(knoop_id: str) -> bool:
            return knoop_id in treated

        result = run_diagnostic(fresh_learner, poc_graph, simulated_learner)

        assert result.questions_asked <= 15, (
            f"Expected ≤ 15 questions, got {result.questions_asked}. "
            f"Tested: {result.knoop_ids_tested}"
        )
        assert fresh_learner.intake_completed is True

    def test_frontier_correctly_identified(self, fresh_learner, poc_graph, methode_mapping):
        """After diagnostic, nodes the learner knows should have high posteriors
        and nodes they don't know should have low posteriors.
        """
        apply_methode_profile(fresh_learner, poc_graph, "fortuna", "2", mapping=methode_mapping)

        treated = get_treated_knoop_ids(methode_mapping, "fortuna", "2")

        def simulated_learner(knoop_id: str) -> bool:
            return knoop_id in treated

        run_diagnostic(fresh_learner, poc_graph, simulated_learner)

        # Treated nodes should be at or above the mastered threshold
        for node_id in treated:
            state = fresh_learner.knoop_states[node_id]
            assert state.posterior_mastery >= MASTERED_THRESHOLD * 0.8, (
                f"Treated node {node_id} posterior {state.posterior_mastery:.2f} is too low"
            )

    def test_no_profile_starts_from_beginning(self, fresh_learner, poc_graph):
        """Without a method profile, the learner starts with P(L₀) = 0.10
        everywhere and the diagnostic starts from the first unresolved node.
        """

        def knows_basics(knoop_id: str) -> bool:
            # Only knows the very first concept nodes
            return knoop_id in {
                "LAT-G-MORF-NAAMVAL-INTRO",
                "LAT-G-MORF-NUMERUS-INTRO",
                "LAT-G-MORF-GENUS-INTRO",
            }

        result = run_diagnostic(fresh_learner, poc_graph, knows_basics)
        assert result.questions_asked <= 30
        assert fresh_learner.intake_completed is True


# ============================================================
# Mechanism 3: Conditional completion (falling backwards)
# ============================================================


class TestConditionalCompletion:
    """Tests for the conditional completion / fallback mechanism."""

    def test_fallback_reduces_prerequisite_posteriors(
        self, fresh_learner, poc_graph, methode_mapping
    ):
        """When a learner fails on a post-requisite after diagnostic intake,
        the posteriors of its prerequisites should decrease.
        """
        # Set up: learner completed intake via fortuna ch3
        apply_methode_profile(fresh_learner, poc_graph, "fortuna", "3", mapping=methode_mapping)

        # Record initial posteriors of the prerequisites of NOM-D1
        pred_ids = list(poc_graph.predecessors("LAT-G-MORF-NOM-D1"))
        initial_posteriors = {}
        for pred_id in pred_ids:
            initial_posteriors[pred_id] = fresh_learner.knoop_states[pred_id].posterior_mastery

        # Learner fails on NOM-D1 → prerequisites should be penalised
        affected = apply_fallback(fresh_learner, poc_graph, "LAT-G-MORF-NOM-D1")

        # At least one prerequisite should be affected
        assert len(affected) > 0

        # Affected prerequisites should have lower posteriors
        for pred_id in affected:
            state = fresh_learner.knoop_states[pred_id]
            assert state.posterior_mastery < initial_posteriors[pred_id], (
                f"Prerequisite {pred_id} posterior should have decreased"
            )
            assert state.source == MasterySource.REVIEW

    def test_fallback_only_affects_diagnostic_nodes(
        self, fresh_learner, poc_graph, methode_mapping
    ):
        """Nodes that were established through practice (not diagnostic)
        should NOT be penalised by the fallback.
        """
        apply_methode_profile(fresh_learner, poc_graph, "fortuna", "3", mapping=methode_mapping)

        # Manually mark one prerequisite as practice-verified
        pred_id = "LAT-G-MORF-DECL1-INTRO"
        fresh_learner.knoop_states[pred_id].source = MasterySource.PRACTICE
        original = fresh_learner.knoop_states[pred_id].posterior_mastery

        apply_fallback(fresh_learner, poc_graph, "LAT-G-MORF-NOM-D1")

        # The practice-verified node should be unchanged
        assert fresh_learner.knoop_states[pred_id].posterior_mastery == original
        assert fresh_learner.knoop_states[pred_id].source == MasterySource.PRACTICE

    def test_fallback_returns_affected_ids_for_review_queue(
        self, fresh_learner, poc_graph, methode_mapping
    ):
        """The affected IDs returned by apply_fallback should be usable
        as elevated-priority entries in the review queue.
        """
        apply_methode_profile(fresh_learner, poc_graph, "fortuna", "3", mapping=methode_mapping)

        affected = apply_fallback(fresh_learner, poc_graph, "LAT-G-MORF-NOM-D1")

        # All affected IDs should exist in the graph
        for node_id in affected:
            assert node_id in poc_graph.nodes

        # All affected IDs should now have source=REVIEW
        for node_id in affected:
            assert fresh_learner.knoop_states[node_id].source == MasterySource.REVIEW
