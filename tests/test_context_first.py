"""Tests for context-first scheduling (E7-05).

Tests cover:
- select_passage() logic
- _candidates_for_new_material_context_first()
- readiness_score with relaxed threshold
- run_session with learning_route=CONTEXT_FIRST
- SessionManager with learning_route=CONTEXT_FIRST
- Grammar-first route is unaffected
"""

from datetime import datetime
from uuid import uuid4

import networkx as nx
import pytest

from gymnasium_classica.api.session_manager import SessionManager
from gymnasium_classica.models.graph import (
    BloomNiveau,
    Fase,
    KennisKnoop,
    KnoopType,
    PrerequisiteEdge,
    Taal,
)
from gymnasium_classica.models.learner import (
    KnoopState,
    LearnerModel,
    ResponseType,
)
from gymnasium_classica.models.passage import Passage, WordAnnotation
from gymnasium_classica.models.user import LearningRoute
from gymnasium_classica.scheduling.priority import (
    PREREQ_READY_THRESHOLD,
    readiness_score,
)
from gymnasium_classica.scheduling.session import (
    CONTEXT_FIRST_PREREQ_THRESHOLD,
    _candidates_for_new_material,
    _candidates_for_new_material_context_first,
    run_session,
    select_passage,
)


def _make_knoop(knoop_id: str, taal: str = "lat") -> KennisKnoop:
    """Helper to create a minimal KennisKnoop."""
    return KennisKnoop(
        id=knoop_id,
        type=KnoopType.G,
        taal=taal,
        titel_nl=f"Knoop {knoop_id}",
        beschrijving=f"Test node {knoop_id}",
        bloom_niveau=BloomNiveau.KENNIS,
        fase=Fase.ONDERBOUW_1,
    )


def _build_test_graph() -> nx.DiGraph:
    """Build a small graph: ROOT -> A -> B, ROOT -> C.

    ROOT is a prereq for A and C; A is a prereq for B.
    """
    g = nx.DiGraph()
    for nid in ["LAT-G-MORF-ROOT", "LAT-G-MORF-CHILDA", "LAT-G-MORF-CHILDB", "LAT-G-MORF-CHILDC"]:
        g.add_node(nid, knoop=_make_knoop(nid))

    edges = [
        ("LAT-G-MORF-ROOT", "LAT-G-MORF-CHILDA"),
        ("LAT-G-MORF-CHILDA", "LAT-G-MORF-CHILDB"),
        ("LAT-G-MORF-ROOT", "LAT-G-MORF-CHILDC"),
    ]
    for src, tgt in edges:
        edge = PrerequisiteEdge(
            source_id=src, target_id=tgt, type="prerequisite", encompassing_weight=0.5
        )
        g.add_edge(src, tgt, edge=edge)

    return g


def _make_passage(
    passage_id: str = "LAT-P-T01",
    knoop_ids: list[str] | None = None,
    moeilijkheid: int = 1,
) -> Passage:
    if knoop_ids is None:
        knoop_ids = ["LAT-G-MORF-CHILDA", "LAT-G-MORF-CHILDC"]
    return Passage(
        id=passage_id,
        taal="lat",
        titel="Test passage",
        tekst="Puella cantat.",
        annotaties=[
            WordAnnotation(woord="Puella", lemma="puella", naamval="nom.sg", vertaling="het meisje"),
            WordAnnotation(woord="cantat", lemma="cantare", naamval="praes.ind.act.3sg", vertaling="zingt"),
        ],
        knoop_ids=knoop_ids,
        moeilijkheid=moeilijkheid,
    )


def _always_correct(knoop_id: str, knoop: KennisKnoop) -> tuple[ResponseType, int]:
    return (ResponseType.CORRECT, 2000)


# --- readiness_score with relaxed threshold ---


class TestReadinessScoreRelaxed:
    """Test that readiness_score accepts a custom prereq_threshold."""

    def test_default_threshold_blocks(self):
        """With default threshold (0.75), a prereq at 0.50 blocks."""
        g = _build_test_graph()
        learner = LearnerModel(user_id=uuid4())
        learner.knoop_states["LAT-G-MORF-ROOT"] = KnoopState(
            knoop_id="LAT-G-MORF-ROOT", posterior_mastery=0.50
        )
        score = readiness_score("LAT-G-MORF-CHILDA", learner, g)
        assert score == 0.0

    def test_relaxed_threshold_allows(self):
        """With threshold 0.25, a prereq at 0.50 passes."""
        g = _build_test_graph()
        learner = LearnerModel(user_id=uuid4())
        learner.knoop_states["LAT-G-MORF-ROOT"] = KnoopState(
            knoop_id="LAT-G-MORF-ROOT", posterior_mastery=0.50
        )
        score = readiness_score(
            "LAT-G-MORF-CHILDA", learner, g,
            prereq_threshold=CONTEXT_FIRST_PREREQ_THRESHOLD,
        )
        assert score > 0.0

    def test_relaxed_threshold_still_blocks_very_low(self):
        """Even with 0.25, a prereq at 0.10 still blocks."""
        g = _build_test_graph()
        learner = LearnerModel(user_id=uuid4())
        learner.knoop_states["LAT-G-MORF-ROOT"] = KnoopState(
            knoop_id="LAT-G-MORF-ROOT", posterior_mastery=0.10
        )
        score = readiness_score(
            "LAT-G-MORF-CHILDA", learner, g,
            prereq_threshold=CONTEXT_FIRST_PREREQ_THRESHOLD,
        )
        assert score == 0.0

    def test_explicit_default_matches_implicit(self):
        """Passing threshold=None should match the default behavior."""
        g = _build_test_graph()
        learner = LearnerModel(user_id=uuid4())
        learner.knoop_states["LAT-G-MORF-ROOT"] = KnoopState(
            knoop_id="LAT-G-MORF-ROOT", posterior_mastery=0.80
        )
        score_default = readiness_score("LAT-G-MORF-CHILDA", learner, g)
        score_explicit = readiness_score(
            "LAT-G-MORF-CHILDA", learner, g, prereq_threshold=PREREQ_READY_THRESHOLD
        )
        assert score_default == score_explicit


# --- select_passage ---


class TestSelectPassage:
    def test_selects_passage_with_reachable_nodes(self):
        g = _build_test_graph()
        learner = LearnerModel(user_id=uuid4())
        # ROOT mastered so children are reachable with relaxed threshold
        learner.knoop_states["LAT-G-MORF-ROOT"] = KnoopState(
            knoop_id="LAT-G-MORF-ROOT", posterior_mastery=0.50
        )
        passages = [_make_passage()]
        result = select_passage(learner, g, passages)
        assert result is not None
        assert result.id == "LAT-P-T01"

    def test_returns_none_when_all_nodes_mastered(self):
        g = _build_test_graph()
        learner = LearnerModel(user_id=uuid4())
        for nid in ["LAT-G-MORF-ROOT", "LAT-G-MORF-CHILDA", "LAT-G-MORF-CHILDC"]:
            learner.knoop_states[nid] = KnoopState(
                knoop_id=nid, posterior_mastery=0.90
            )
        passages = [_make_passage()]
        result = select_passage(learner, g, passages)
        assert result is None

    def test_returns_none_when_no_passages(self):
        g = _build_test_graph()
        learner = LearnerModel(user_id=uuid4())
        result = select_passage(learner, g, [])
        assert result is None

    def test_prefers_lower_difficulty(self):
        g = _build_test_graph()
        learner = LearnerModel(user_id=uuid4())
        learner.knoop_states["LAT-G-MORF-ROOT"] = KnoopState(
            knoop_id="LAT-G-MORF-ROOT", posterior_mastery=0.50
        )
        p_easy = _make_passage("LAT-P-EASY", moeilijkheid=1)
        p_hard = _make_passage("LAT-P-HARD", moeilijkheid=5)
        result = select_passage(learner, g, [p_hard, p_easy])
        assert result is not None
        assert result.id == "LAT-P-EASY"

    def test_ignores_passage_with_unknown_nodes(self):
        g = _build_test_graph()
        learner = LearnerModel(user_id=uuid4())
        p = _make_passage(knoop_ids=["NONEXISTENT-NODE"])
        result = select_passage(learner, g, [p])
        assert result is None


# --- _candidates_for_new_material_context_first ---


class TestCandidatesContextFirst:
    def test_returns_candidates_from_passage(self):
        g = _build_test_graph()
        learner = LearnerModel(user_id=uuid4())
        learner.knoop_states["LAT-G-MORF-ROOT"] = KnoopState(
            knoop_id="LAT-G-MORF-ROOT", posterior_mastery=0.50
        )
        passages = [_make_passage()]
        candidates = _candidates_for_new_material_context_first(learner, g, passages)
        knoop_ids = [k.id for _, k in candidates]
        # CHILDA and CHILDC are in the passage and reachable (ROOT at 0.50 > 0.25)
        assert "LAT-G-MORF-CHILDA" in knoop_ids
        assert "LAT-G-MORF-CHILDC" in knoop_ids

    def test_grammar_first_would_not_find_these(self):
        """With standard threshold, same nodes are NOT candidates."""
        g = _build_test_graph()
        learner = LearnerModel(user_id=uuid4())
        learner.knoop_states["LAT-G-MORF-ROOT"] = KnoopState(
            knoop_id="LAT-G-MORF-ROOT", posterior_mastery=0.50
        )
        candidates = _candidates_for_new_material(learner, g)
        knoop_ids = [k.id for _, k in candidates]
        # Standard threshold (0.75) blocks: ROOT at 0.50 < 0.75
        assert "LAT-G-MORF-CHILDA" not in knoop_ids
        assert "LAT-G-MORF-CHILDC" not in knoop_ids

    def test_empty_when_no_passage_matches(self):
        g = _build_test_graph()
        learner = LearnerModel(user_id=uuid4())
        # All nodes mastered → no passage matches
        for nid in g.nodes:
            learner.knoop_states[nid] = KnoopState(
                knoop_id=nid, posterior_mastery=0.90
            )
        passages = [_make_passage()]
        candidates = _candidates_for_new_material_context_first(learner, g, passages)
        assert candidates == []


# --- run_session with context-first ---


class TestRunSessionContextFirst:
    def test_context_first_produces_items(self):
        g = _build_test_graph()
        learner = LearnerModel(user_id=uuid4())
        learner.knoop_states["LAT-G-MORF-ROOT"] = KnoopState(
            knoop_id="LAT-G-MORF-ROOT", posterior_mastery=0.50
        )
        passages = [_make_passage()]
        result = run_session(
            learner, g, _always_correct,
            learning_route=LearningRoute.CONTEXT_FIRST,
            passages=passages,
        )
        assert len(result.items) > 0

    def test_grammar_first_default_unaffected(self):
        """Default run_session (grammar_first) still works exactly as before."""
        g = _build_test_graph()
        learner = LearnerModel(user_id=uuid4())
        # ROOT fully mastered for grammar-first to find children
        learner.knoop_states["LAT-G-MORF-ROOT"] = KnoopState(
            knoop_id="LAT-G-MORF-ROOT", posterior_mastery=0.90
        )
        result = run_session(learner, g, _always_correct)
        # Should still work without passages
        assert result.session_id != ""

    def test_context_first_without_passages_falls_back(self):
        """Context-first without passages falls back to grammar-first behavior."""
        g = _build_test_graph()
        learner = LearnerModel(user_id=uuid4())
        learner.knoop_states["LAT-G-MORF-ROOT"] = KnoopState(
            knoop_id="LAT-G-MORF-ROOT", posterior_mastery=0.90
        )
        result = run_session(
            learner, g, _always_correct,
            learning_route=LearningRoute.CONTEXT_FIRST,
            passages=[],
        )
        assert result.session_id != ""


# --- SessionManager with context-first ---


class TestSessionManagerContextFirst:
    def test_start_with_context_first(self):
        g = _build_test_graph()
        learner = LearnerModel(user_id=uuid4())
        learner.knoop_states["LAT-G-MORF-ROOT"] = KnoopState(
            knoop_id="LAT-G-MORF-ROOT", posterior_mastery=0.50
        )
        passages = [_make_passage()]
        mgr = SessionManager()
        session_id, question = mgr.start_session(
            user_id=str(uuid4()),
            learner=learner,
            graph=g,
            learning_route=LearningRoute.CONTEXT_FIRST,
            passages=passages,
        )
        assert session_id is not None
        # Question should come from passage-linked nodes
        if question is not None:
            assert question.knoop_id in [
                "LAT-G-MORF-CHILDA", "LAT-G-MORF-CHILDC",
                "LAT-G-MORF-ROOT", "LAT-G-MORF-CHILDB",
            ]

    def test_start_grammar_first_default(self):
        """Default (grammar_first) SessionManager still works."""
        g = _build_test_graph()
        learner = LearnerModel(user_id=uuid4())
        learner.knoop_states["LAT-G-MORF-ROOT"] = KnoopState(
            knoop_id="LAT-G-MORF-ROOT", posterior_mastery=0.90
        )
        mgr = SessionManager()
        session_id, question = mgr.start_session(
            user_id=str(uuid4()),
            learner=learner,
            graph=g,
        )
        assert session_id is not None

    def test_submit_answer_context_first(self):
        g = _build_test_graph()
        learner = LearnerModel(user_id=uuid4())
        learner.knoop_states["LAT-G-MORF-ROOT"] = KnoopState(
            knoop_id="LAT-G-MORF-ROOT", posterior_mastery=0.50
        )
        passages = [_make_passage()]
        mgr = SessionManager()
        session_id, question = mgr.start_session(
            user_id=str(uuid4()),
            learner=learner,
            graph=g,
            learning_route=LearningRoute.CONTEXT_FIRST,
            passages=passages,
        )
        if question is not None:
            result = mgr.submit_answer(
                session_id, ResponseType.CORRECT, 2000
            )
            assert result.feedback.correct is True
