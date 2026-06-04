"""Tests for context-first scheduling (E7-05).

Tests cover:
- select_passage() logic
- _candidates_for_new_material_context_first()
- readiness_score with relaxed threshold
- run_session with learning_route=CONTEXT_FIRST
- SessionManager with learning_route=CONTEXT_FIRST
- Grammar-first route is unaffected
"""

from uuid import uuid4

import networkx as nx

from gymnasium_classica.api.session_manager import SessionManager
from gymnasium_classica.models.graph import (
    BloomLevel,
    Node,
    NodeType,
    Phase,
    PrerequisiteEdge,
)
from gymnasium_classica.models.learner import (
    LearnerModel,
    NodeState,
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


def _make_knoop(knoop_id: str, taal: str = "lat") -> Node:
    """Helper to create a minimal Node."""
    return Node(
        id=knoop_id,
        type=NodeType.G,
        taal=taal,
        titel_nl=f"Knoop {knoop_id}",
        beschrijving=f"Test node {knoop_id}",
        bloom_niveau=BloomLevel.KENNIS,
        fase=Phase.ONDERBOUW_1,
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
            WordAnnotation(
                woord="Puella", lemma="puella", naamval="nom.sg", vertaling="het meisje"
            ),
            WordAnnotation(
                woord="cantat", lemma="cantare", naamval="praes.ind.act.3sg", vertaling="zingt"
            ),
        ],
        knoop_ids=knoop_ids,
        moeilijkheid=moeilijkheid,
    )


def _always_correct(knoop_id: str, knoop: Node) -> tuple[ResponseType, int]:
    return (ResponseType.CORRECT, 2000)


# --- readiness_score with relaxed threshold ---


class TestReadinessScoreRelaxed:
    """Test that readiness_score accepts a custom prereq_threshold."""

    def test_default_threshold_blocks(self):
        """With default threshold (0.75), a prereq at 0.50 blocks."""
        g = _build_test_graph()
        learner = LearnerModel(user_id=uuid4())
        learner.knoop_states["LAT-G-MORF-ROOT"] = NodeState(
            knoop_id="LAT-G-MORF-ROOT", posterior_mastery=0.50
        )
        score = readiness_score("LAT-G-MORF-CHILDA", learner, g)
        assert score == 0.0

    def test_relaxed_threshold_allows(self):
        """With threshold 0.25, a prereq at 0.50 passes."""
        g = _build_test_graph()
        learner = LearnerModel(user_id=uuid4())
        learner.knoop_states["LAT-G-MORF-ROOT"] = NodeState(
            knoop_id="LAT-G-MORF-ROOT", posterior_mastery=0.50
        )
        score = readiness_score(
            "LAT-G-MORF-CHILDA",
            learner,
            g,
            prereq_threshold=CONTEXT_FIRST_PREREQ_THRESHOLD,
        )
        assert score > 0.0

    def test_relaxed_threshold_still_blocks_very_low(self):
        """Even with 0.25, a prereq at 0.10 still blocks."""
        g = _build_test_graph()
        learner = LearnerModel(user_id=uuid4())
        learner.knoop_states["LAT-G-MORF-ROOT"] = NodeState(
            knoop_id="LAT-G-MORF-ROOT", posterior_mastery=0.10
        )
        score = readiness_score(
            "LAT-G-MORF-CHILDA",
            learner,
            g,
            prereq_threshold=CONTEXT_FIRST_PREREQ_THRESHOLD,
        )
        assert score == 0.0

    def test_explicit_default_matches_implicit(self):
        """Passing threshold=None should match the default behavior."""
        g = _build_test_graph()
        learner = LearnerModel(user_id=uuid4())
        learner.knoop_states["LAT-G-MORF-ROOT"] = NodeState(
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
        learner.knoop_states["LAT-G-MORF-ROOT"] = NodeState(
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
            learner.knoop_states[nid] = NodeState(knoop_id=nid, posterior_mastery=0.90)
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
        learner.knoop_states["LAT-G-MORF-ROOT"] = NodeState(
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
        learner.knoop_states["LAT-G-MORF-ROOT"] = NodeState(
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
        learner.knoop_states["LAT-G-MORF-ROOT"] = NodeState(
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
            learner.knoop_states[nid] = NodeState(knoop_id=nid, posterior_mastery=0.90)
        passages = [_make_passage()]
        candidates = _candidates_for_new_material_context_first(learner, g, passages)
        assert candidates == []


# --- run_session with context-first ---


class TestRunSessionContextFirst:
    def test_context_first_produces_items(self):
        g = _build_test_graph()
        learner = LearnerModel(user_id=uuid4())
        learner.knoop_states["LAT-G-MORF-ROOT"] = NodeState(
            knoop_id="LAT-G-MORF-ROOT", posterior_mastery=0.50
        )
        passages = [_make_passage()]
        result = run_session(
            learner,
            g,
            _always_correct,
            learning_route=LearningRoute.CONTEXT_FIRST,
            passages=passages,
        )
        assert len(result.items) > 0

    def test_grammar_first_default_unaffected(self):
        """Default run_session (grammar_first) still works exactly as before."""
        g = _build_test_graph()
        learner = LearnerModel(user_id=uuid4())
        # ROOT fully mastered for grammar-first to find children
        learner.knoop_states["LAT-G-MORF-ROOT"] = NodeState(
            knoop_id="LAT-G-MORF-ROOT", posterior_mastery=0.90
        )
        result = run_session(learner, g, _always_correct)
        # Should still work without passages
        assert result.session_id != ""

    def test_context_first_without_passages_falls_back(self):
        """Context-first without passages falls back to grammar-first behavior."""
        g = _build_test_graph()
        learner = LearnerModel(user_id=uuid4())
        learner.knoop_states["LAT-G-MORF-ROOT"] = NodeState(
            knoop_id="LAT-G-MORF-ROOT", posterior_mastery=0.90
        )
        result = run_session(
            learner,
            g,
            _always_correct,
            learning_route=LearningRoute.CONTEXT_FIRST,
            passages=[],
        )
        assert result.session_id != ""


# --- SessionManager with context-first ---


class TestSessionManagerContextFirst:
    def test_start_with_context_first_presents_passage(self):
        """Context-first session starts with a passage question."""
        g = _build_test_graph()
        learner = LearnerModel(user_id=uuid4())
        learner.knoop_states["LAT-G-MORF-ROOT"] = NodeState(
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
        assert question is not None
        # First question should be the passage itself
        assert question.knoop_id == "LAT-P-T01"
        assert isinstance(question.stimulus, dict)
        assert question.stimulus["type"] == "passage"
        assert question.stimulus["tekst"] == "Puella cantat."

    def test_start_grammar_first_default(self):
        """Default (grammar_first) SessionManager still works."""
        g = _build_test_graph()
        learner = LearnerModel(user_id=uuid4())
        learner.knoop_states["LAT-G-MORF-ROOT"] = NodeState(
            knoop_id="LAT-G-MORF-ROOT", posterior_mastery=0.90
        )
        mgr = SessionManager()
        session_id, _question = mgr.start_session(
            user_id=str(uuid4()),
            learner=learner,
            graph=g,
        )
        assert session_id is not None

    def test_passage_then_grammar_scaffolding(self):
        """After answering the passage, grammar nodes from it are presented."""
        g = _build_test_graph()
        learner = LearnerModel(user_id=uuid4())
        learner.knoop_states["LAT-G-MORF-ROOT"] = NodeState(
            knoop_id="LAT-G-MORF-ROOT", posterior_mastery=0.50
        )
        passages = [_make_passage()]
        mgr = SessionManager()
        session_id, q1 = mgr.start_session(
            user_id=str(uuid4()),
            learner=learner,
            graph=g,
            learning_route=LearningRoute.CONTEXT_FIRST,
            passages=passages,
        )
        assert q1 is not None
        assert q1.knoop_id == "LAT-P-T01"  # passage first

        # Answer the passage question
        result = mgr.submit_answer(session_id, ResponseType.CORRECT, 3000)
        assert result.feedback.response_type == "passage_read"

        # Next question should be a grammar node from the passage
        q2 = result.next_question
        if q2 is not None:
            assert q2.knoop_id in ["LAT-G-MORF-CHILDA", "LAT-G-MORF-CHILDC"]
            assert isinstance(q2.stimulus, str)  # not a dict (normal knoop question)

    def test_bkt_not_applied_to_passage(self):
        """BKT updates should NOT happen on the passage ID."""
        g = _build_test_graph()
        learner = LearnerModel(user_id=uuid4())
        learner.knoop_states["LAT-G-MORF-ROOT"] = NodeState(
            knoop_id="LAT-G-MORF-ROOT", posterior_mastery=0.50
        )
        passages = [_make_passage()]
        mgr = SessionManager()
        session_id, _q1 = mgr.start_session(
            user_id=str(uuid4()),
            learner=learner,
            graph=g,
            learning_route=LearningRoute.CONTEXT_FIRST,
            passages=passages,
        )
        # Answer the passage
        mgr.submit_answer(session_id, ResponseType.CORRECT, 2000)

        # Passage ID should NOT appear in learner's knoop_states
        assert "LAT-P-T01" not in learner.knoop_states

    def test_bkt_applied_to_grammar_nodes(self):
        """BKT updates DO happen on the grammar nodes after passage."""
        g = _build_test_graph()
        learner = LearnerModel(user_id=uuid4())
        learner.knoop_states["LAT-G-MORF-ROOT"] = NodeState(
            knoop_id="LAT-G-MORF-ROOT", posterior_mastery=0.50
        )
        passages = [_make_passage()]
        mgr = SessionManager()
        session_id, _q1 = mgr.start_session(
            user_id=str(uuid4()),
            learner=learner,
            graph=g,
            learning_route=LearningRoute.CONTEXT_FIRST,
            passages=passages,
        )
        # Answer passage
        result1 = mgr.submit_answer(session_id, ResponseType.CORRECT, 2000)
        if result1.next_question is not None:
            grammar_id = result1.next_question.knoop_id
            before = learner.knoop_states.get(grammar_id)
            before_val = before.posterior_mastery if before else 0.10

            # Answer the grammar node correctly
            mgr.submit_answer(session_id, ResponseType.CORRECT, 2000)
            after_val = learner.knoop_states[grammar_id].posterior_mastery

            # Mastery should have increased (BKT applied)
            assert after_val > before_val

    def test_submit_answer_passage_then_complete(self):
        """Full flow: passage → grammar nodes → session completes."""
        g = _build_test_graph()
        learner = LearnerModel(user_id=uuid4())
        learner.knoop_states["LAT-G-MORF-ROOT"] = NodeState(
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
        # Walk through all questions until session finishes
        steps = 0
        while question is not None and steps < 50:
            result = mgr.submit_answer(session_id, ResponseType.CORRECT, 2000)
            question = result.next_question
            steps += 1
            if result.session_finished:
                break

        summary = mgr.get_summary(session_id)
        assert summary.total_items >= 1  # at least the passage was presented
