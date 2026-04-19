"""Tests for the priority queue / urgency scoring module."""

from datetime import datetime, timedelta
from uuid import uuid4

import pytest

from gymnasium_classica.graph.loader import load_graph, load_graph_from_dict
from gymnasium_classica.models.learner import KnoopState, LearnerModel, MasterySource
from gymnasium_classica.scheduling.priority import (
    compute_urgency_scores,
    estimate_retention,
    forget_urgency,
    pedagogical_value,
    readiness_score,
)


class TestEstimateRetention:
    def test_never_reviewed_unmastered(self):
        state = KnoopState(knoop_id="X", posterior_mastery=0.10)
        assert estimate_retention(state) == 0.0

    def test_never_reviewed_mastered_diagnostic(self):
        state = KnoopState(knoop_id="X", posterior_mastery=0.80, source=MasterySource.DIAGNOSTIC)
        assert estimate_retention(state) == pytest.approx(0.5)

    def test_just_reviewed(self):
        now = datetime(2026, 4, 12, 10, 0)
        state = KnoopState(
            knoop_id="X",
            posterior_mastery=0.90,
            interval_days=6.0,
            easiness_factor=2.5,
            last_review=now,
        )
        retention = estimate_retention(state, now=now)
        assert retention == pytest.approx(1.0, abs=0.01)

    def test_decay_over_time(self):
        base = datetime(2026, 4, 1)
        state = KnoopState(
            knoop_id="X",
            posterior_mastery=0.90,
            interval_days=6.0,
            easiness_factor=2.5,
            last_review=base,
        )
        r_3d = estimate_retention(state, now=base + timedelta(days=3))
        r_10d = estimate_retention(state, now=base + timedelta(days=10))
        assert r_3d > r_10d  # More decay after more time

    def test_higher_ef_slower_decay(self):
        base = datetime(2026, 4, 1)
        now = base + timedelta(days=5)

        low_ef = KnoopState(
            knoop_id="X",
            posterior_mastery=0.90,
            interval_days=6.0,
            easiness_factor=1.5,
            last_review=base,
        )
        high_ef = KnoopState(
            knoop_id="X",
            posterior_mastery=0.90,
            interval_days=6.0,
            easiness_factor=3.0,
            last_review=base,
        )
        assert estimate_retention(high_ef, now) > estimate_retention(low_ef, now)


class TestForgetUrgency:
    def test_unreviewed_unmastered_max_urgency(self):
        state = KnoopState(knoop_id="X", posterior_mastery=0.10)
        assert forget_urgency(state) == pytest.approx(1.0)

    def test_just_reviewed_low_urgency(self):
        now = datetime(2026, 4, 12)
        state = KnoopState(
            knoop_id="X",
            posterior_mastery=0.90,
            interval_days=6.0,
            easiness_factor=2.5,
            last_review=now,
        )
        assert forget_urgency(state, now) < 0.1


class TestReadinessScore:
    def test_root_node_always_ready(self, sample_graph_data):
        graph = load_graph_from_dict(sample_graph_data)
        learner = LearnerModel(user_id=uuid4())
        # Root node has no prerequisites
        score = readiness_score("LAT-G-MORF-NAAMVAL-INTRO", learner, graph)
        assert score == 1.0

    def test_prerequisites_not_met(self, sample_graph_data):
        graph = load_graph_from_dict(sample_graph_data)
        learner = LearnerModel(user_id=uuid4())
        # NOM-D1 requires DECL1-INTRO (not in learner states → posterior 0.0)
        score = readiness_score("LAT-G-MORF-NOM-D1", learner, graph)
        assert score == 0.0

    def test_prerequisites_met(self, sample_graph_data):
        graph = load_graph_from_dict(sample_graph_data)
        learner = LearnerModel(user_id=uuid4())
        # Set all prerequisites of NOM-D1 to mastered
        for pred in graph.predecessors("LAT-G-MORF-NOM-D1"):
            learner.knoop_states[pred] = KnoopState(knoop_id=pred, posterior_mastery=0.85)
        score = readiness_score("LAT-G-MORF-NOM-D1", learner, graph)
        assert score > 0.0

    def test_mastered_node_returns_zero(self, sample_graph_data):
        graph = load_graph_from_dict(sample_graph_data)
        learner = LearnerModel(user_id=uuid4())
        learner.knoop_states["LAT-G-MORF-NOM-D1"] = KnoopState(
            knoop_id="LAT-G-MORF-NOM-D1", posterior_mastery=0.90
        )
        score = readiness_score("LAT-G-MORF-NOM-D1", learner, graph)
        assert score == 0.0


class TestPedagogicalValue:
    def test_root_high_value(self, sample_graph_data):
        graph = load_graph_from_dict(sample_graph_data)
        max_deg = max(graph.out_degree(n) for n in graph.nodes)
        # NAAMVAL-INTRO has out-degree 1 (→ DECL-INTRO)
        val = pedagogical_value("LAT-G-MORF-NAAMVAL-INTRO", graph, max_deg)
        assert val > 0.0

    def test_leaf_zero_value(self, sample_graph_data):
        graph = load_graph_from_dict(sample_graph_data)
        max_deg = max(graph.out_degree(n) for n in graph.nodes)
        # NOM-D1 is a leaf (out-degree 0)
        val = pedagogical_value("LAT-G-MORF-NOM-D1", graph, max_deg)
        assert val == 0.0


class TestComputeUrgencyScores:
    def test_poc_graph_produces_valid_scores(self, poc_graph_path):
        if not poc_graph_path.exists():
            pytest.skip("PoC graph not found")
        graph = load_graph(poc_graph_path)
        learner = LearnerModel(user_id=uuid4())

        scores = compute_urgency_scores(learner, graph)
        # Should produce results for root nodes (no prereqs needed)
        assert len(scores) > 0
        # All urgencies should be non-negative
        for urgency, knoop in scores:
            assert urgency >= 0.0

    def test_unmet_prerequisites_excluded(self, sample_graph_data):
        graph = load_graph_from_dict(sample_graph_data)
        learner = LearnerModel(user_id=uuid4())
        # No states → only root nodes should appear
        scores = compute_urgency_scores(learner, graph)
        node_ids = {knoop.id for _, knoop in scores}
        assert "LAT-G-MORF-NAAMVAL-INTRO" in node_ids  # root
        assert "LAT-G-MORF-NOM-D1" not in node_ids  # prereqs not met

    def test_mastered_review_due_included(self, sample_graph_data):
        graph = load_graph_from_dict(sample_graph_data)
        learner = LearnerModel(user_id=uuid4())
        # Master a node with old review
        learner.knoop_states["LAT-G-MORF-NOM-D1"] = KnoopState(
            knoop_id="LAT-G-MORF-NOM-D1",
            posterior_mastery=0.90,
            interval_days=6.0,
            last_review=datetime(2026, 3, 1),
        )
        scores = compute_urgency_scores(learner, graph, now=datetime(2026, 4, 12))
        node_ids = {knoop.id for _, knoop in scores}
        assert "LAT-G-MORF-NOM-D1" in node_ids  # review due

    def test_sorted_descending(self, sample_graph_data):
        graph = load_graph_from_dict(sample_graph_data)
        learner = LearnerModel(user_id=uuid4())
        scores = compute_urgency_scores(learner, graph)
        urgencies = [u for u, _ in scores]
        assert urgencies == sorted(urgencies, reverse=True)
