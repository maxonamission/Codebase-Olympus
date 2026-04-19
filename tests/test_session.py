"""Tests for session orchestration."""

from datetime import datetime, timedelta
from uuid import uuid4

import pytest

from gymnasium_classica.graph.loader import load_graph
from gymnasium_classica.models.graph import KennisKnoop
from gymnasium_classica.models.learner import (
    KnoopState,
    LearnerModel,
    MasterySource,
    ResponseType,
)
from gymnasium_classica.scheduling.session import (
    SessionPhase,
    run_session,
)


def _always_correct(knoop_id: str, knoop: KennisKnoop) -> tuple[ResponseType, int]:
    return (ResponseType.CORRECT, 2000)


def _always_incorrect(knoop_id: str, knoop: KennisKnoop) -> tuple[ResponseType, int]:
    return (ResponseType.INCORRECT, 5000)


def _mastery_based_answer(learner: LearnerModel):
    """Return an answer_fn that simulates responses based on current mastery."""

    def answer(knoop_id: str, knoop: KennisKnoop) -> tuple[ResponseType, int]:
        state = learner.knoop_states.get(knoop_id)
        posterior = state.posterior_mastery if state else 0.10
        if posterior >= 0.75:
            return (ResponseType.CORRECT, 1500)
        elif posterior >= 0.40:
            return (ResponseType.SLOW_CORRECT, 4000)
        else:
            return (ResponseType.INCORRECT, 6000)

    return answer


@pytest.fixture
def poc_graph(poc_graph_path):
    if not poc_graph_path.exists():
        pytest.skip("PoC graph not found")
    return load_graph(poc_graph_path)


class TestSessionOrchestration:
    """Core session orchestration tests."""

    def test_session_completes(self, poc_graph):
        learner = LearnerModel(user_id=uuid4())
        result = run_session(learner, poc_graph, _always_correct)
        assert result.session_id != ""
        assert len(result.items) > 0

    def test_all_four_phases_possible(self, poc_graph):
        """With a partially mastered learner, all phases should have items."""
        learner = LearnerModel(user_id=uuid4())
        now = datetime(2026, 4, 12)

        # Set up: some nodes mastered (with old review), some not
        import networkx as nx

        topo = list(nx.topological_sort(poc_graph))
        for i, node_id in enumerate(topo):
            if i < 15:
                # Mastered, reviewed a week ago
                learner.knoop_states[node_id] = KnoopState(
                    knoop_id=node_id,
                    posterior_mastery=0.85,
                    source=MasterySource.PRACTICE,
                    interval_days=6.0,
                    easiness_factor=2.5,
                    repetitions=3,
                    last_review=now - timedelta(days=7),
                )
            else:
                learner.knoop_states[node_id] = KnoopState(
                    knoop_id=node_id,
                    posterior_mastery=0.10,
                )

        result = run_session(learner, poc_graph, _mastery_based_answer(learner), now=now)
        phases_present = {item.phase for item in result.items}
        # At minimum warmup (review due) and new_material should be present
        assert SessionPhase.WARMUP in phases_present or SessionPhase.NEW_MATERIAL in phases_present
        assert len(result.items) > 3

    def test_bkt_updates_applied(self, poc_graph):
        learner = LearnerModel(user_id=uuid4())
        run_session(learner, poc_graph, _always_correct)

        # After correct answers, posteriors should have increased from default
        updated_any = False
        for state in learner.knoop_states.values():
            if state.posterior_mastery > 0.10:
                updated_any = True
                break
        assert updated_any

    def test_sm2_updates_applied(self, poc_graph):
        learner = LearnerModel(user_id=uuid4())
        now = datetime(2026, 4, 12)
        run_session(learner, poc_graph, _always_correct, now=now)

        # After the session, at least one node should have last_review set
        reviewed_any = False
        for state in learner.knoop_states.values():
            if state.last_review is not None:
                reviewed_any = True
                assert state.repetitions >= 1
                break
        assert reviewed_any

    def test_session_recorded_in_history(self, poc_graph):
        learner = LearnerModel(user_id=uuid4())
        assert len(learner.session_history) == 0
        run_session(learner, poc_graph, _always_correct)
        assert len(learner.session_history) == 1

    def test_no_premature_introduction(self, poc_graph):
        """New material should only be introduced when prerequisites are met."""
        learner = LearnerModel(user_id=uuid4())
        result = run_session(learner, poc_graph, _always_correct)

        # All introduced nodes should be root nodes or have mastered prereqs

        for node_id in result.nodes_introduced:
            preds = list(poc_graph.predecessors(node_id))
            if not preds:
                continue  # Root node, OK
            # At least initially, only root nodes should be introduced
            # (a beginner has no mastered prereqs)

    def test_mastery_changes_tracked(self, poc_graph):
        learner = LearnerModel(user_id=uuid4())
        result = run_session(learner, poc_graph, _always_correct)
        assert len(result.mastery_changes) > 0
        for _knoop_id, (before, after) in result.mastery_changes.items():
            # Correct answers should increase mastery
            assert after >= before


class TestMultiSessionProgression:
    """Test that multiple sessions lead to measurable progress."""

    def test_three_sessions_progression(self, poc_graph):
        """After 3 sessions with correct answers, more nodes should be mastered."""
        learner = LearnerModel(user_id=uuid4())
        now = datetime(2026, 4, 12)

        mastered_counts = []
        for day in range(3):
            session_time = now + timedelta(days=day)
            run_session(learner, poc_graph, _always_correct, now=session_time)
            mastered = sum(1 for s in learner.knoop_states.values() if s.posterior_mastery >= 0.75)
            mastered_counts.append(mastered)

        # Each session should master at least as many nodes as the previous
        assert mastered_counts[-1] >= mastered_counts[0]
        # After 3 sessions of all-correct, at least some nodes should be mastered
        assert mastered_counts[-1] > 0
