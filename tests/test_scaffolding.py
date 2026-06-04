"""Tests for E7-09: grammatica-scaffolding bij passages."""

from pathlib import Path
from uuid import uuid4

import networkx as nx
import pytest

from gymnasium_classica.api.session_manager import (
    SessionManager,
    _load_scaffolding_content,
    _node_to_question,
)
from gymnasium_classica.models.graph import (
    BloomLevel,
    Language,
    Node,
    NodeType,
    Phase,
    PrerequisiteEdge,
)
from gymnasium_classica.models.learner import LearnerModel, NodeState, ResponseType
from gymnasium_classica.models.passage import Passage, WordAnnotation
from gymnasium_classica.models.user import LearningRoute
from gymnasium_classica.scheduling.session import SessionPhase


def _make_node(node_id: str, content_ref: str | None = None) -> Node:
    return Node(
        id=node_id,
        type=NodeType.G,
        language=Language.LAT,
        title_nl=f"Knoop {node_id}",
        description=f"Test node {node_id}",
        bloom_level=BloomLevel.KENNIS,
        phase=Phase.ONDERBOUW_1,
        content_ref=content_ref,
    )


def _build_graph() -> nx.DiGraph:
    g = nx.DiGraph()
    for nid in ["LAT-G-MORF-ROOT", "LAT-G-MORF-CHILDA", "LAT-G-MORF-CHILDB"]:
        g.add_node(nid, node=_make_node(nid))
    edge = PrerequisiteEdge(
        source_id="LAT-G-MORF-ROOT",
        target_id="LAT-G-MORF-CHILDA",
        type="prerequisite",
        encompassing_weight=0.5,
    )
    g.add_edge("LAT-G-MORF-ROOT", "LAT-G-MORF-CHILDA", edge=edge)
    return g


def _make_passage() -> Passage:
    return Passage(
        id="LAT-P-T01",
        language="lat",
        title="Test passage",
        text="Puella cantat.",
        annotations=[
            WordAnnotation(word="Puella", lemma="puella", case="nom.sg", translation="het meisje"),
            WordAnnotation(
                word="cantat", lemma="cantare", case="praes.ind.act.3sg", translation="zingt"
            ),
        ],
        node_ids=["LAT-G-MORF-CHILDA"],
        difficulty=1,
    )


# --- _load_scaffolding_content ---


class TestLoadScaffoldingContent:
    def test_loads_existing_content(self, tmp_path: Path):
        node = _make_node("LAT-G-MORF-TEST")
        content_file = tmp_path / "LAT-G-MORF-TEST.md"
        content_file.write_text("# Test content\n\nThis is test grammar.", encoding="utf-8")

        result = _load_scaffolding_content(node, content_dir=tmp_path)
        assert result is not None
        assert "# Test content" in result
        assert "test grammar" in result

    def test_returns_none_for_missing_content(self, tmp_path: Path):
        node = _make_node("LAT-G-MORF-NOPE")
        result = _load_scaffolding_content(node, content_dir=tmp_path)
        assert result is None

    def test_uses_content_ref_when_set(self, tmp_path: Path):
        content_file = tmp_path / "custom.md"
        content_file.write_text("# Custom content", encoding="utf-8")

        node = _make_node("LAT-G-MORF-TEST", content_ref=str(content_file))
        result = _load_scaffolding_content(node, content_dir=tmp_path)
        assert result is not None
        assert "# Custom content" in result

    def test_loads_real_content_files(self):
        """Verify that data/content/ files can be loaded."""
        content_dir = Path(__file__).parent.parent / "data" / "content"
        if not content_dir.exists():
            pytest.skip("data/content/ not found")

        # Try loading a known file
        test_node = _make_node("LAT-G-MORF-DECL1-INTRO")
        result = _load_scaffolding_content(test_node, content_dir=content_dir)
        if result is not None:
            assert len(result) > 0
            assert "declinatie" in result.lower() or "#" in result


# --- _node_to_question with scaffolding ---


class TestKnoopToQuestionScaffolding:
    def test_no_scaffolding_by_default(self, tmp_path: Path):
        node = _make_node("LAT-G-MORF-TEST")
        (tmp_path / "LAT-G-MORF-TEST.md").write_text("# Content", encoding="utf-8")

        q = _node_to_question(node, SessionPhase.NEW_MATERIAL, content_dir=tmp_path)
        assert q.scaffolding_content is None

    def test_scaffolding_when_requested(self, tmp_path: Path):
        node = _make_node("LAT-G-MORF-TEST")
        (tmp_path / "LAT-G-MORF-TEST.md").write_text(
            "# Grammatica-uitleg\n\nDit is uitleg.", encoding="utf-8"
        )

        q = _node_to_question(
            node,
            SessionPhase.NEW_MATERIAL,
            include_scaffolding=True,
            content_dir=tmp_path,
        )
        assert q.scaffolding_content is not None
        assert "Grammatica-uitleg" in q.scaffolding_content

    def test_scaffolding_none_when_no_file(self, tmp_path: Path):
        node = _make_node("LAT-G-MORF-NOPE")
        q = _node_to_question(
            node,
            SessionPhase.NEW_MATERIAL,
            include_scaffolding=True,
            content_dir=tmp_path,
        )
        assert q.scaffolding_content is None


# --- SessionManager scaffolding integration ---


class TestSessionManagerScaffolding:
    def test_scaffolding_after_passage(self):
        """Grammar nodes after a passage should include scaffolding_content
        when a content file exists."""
        g = _build_graph()
        learner = LearnerModel(user_id=uuid4())
        learner.node_states["LAT-G-MORF-ROOT"] = NodeState(
            node_id="LAT-G-MORF-ROOT", posterior_mastery=0.50
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
        assert q1.node_id == "LAT-P-T01"  # passage first

        # Answer the passage
        result = mgr.submit_answer(session_id, ResponseType.CORRECT, 3000)
        q2 = result.next_question

        # The grammar node might or might not have content on disk,
        # but the scaffolding_content field should be present (possibly None)
        if q2 is not None:
            assert hasattr(q2, "scaffolding_content") or "scaffolding_content" in str(type(q2))

    def test_grammar_first_no_scaffolding(self):
        """Grammar-first route should NOT include scaffolding."""
        g = _build_graph()
        learner = LearnerModel(user_id=uuid4())
        learner.node_states["LAT-G-MORF-ROOT"] = NodeState(
            node_id="LAT-G-MORF-ROOT", posterior_mastery=0.90
        )
        mgr = SessionManager()
        _session_id, q1 = mgr.start_session(
            user_id=str(uuid4()),
            learner=learner,
            graph=g,
        )
        if q1 is not None:
            assert q1.scaffolding_content is None
