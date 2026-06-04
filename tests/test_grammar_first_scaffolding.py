"""Tests voor F1-02: grammar-first scaffolding bij eerste introductie.

Scaffolding verschijnt alleen:
* tijdens NEW_MATERIAL
* bij de eerste keer dat de node voor deze leerling wordt opgeroepen
  (``NodeState.item_history`` is leeg of NodeState ontbreekt nog)
* context-first: na een passage (bestaand gedrag)
* grammar-first: alleen als ``User.show_grammar_scaffolding`` aan staat
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from uuid import uuid4

import networkx as nx

from gymnasium_classica.api.session_manager import (
    SessionManager,
    _should_scaffold,
)
from gymnasium_classica.models.graph import (
    BloomLevel,
    Direction,
    Item,
    ItemType,
    Language,
    Node,
    NodeType,
    Phase,
    Source,
)
from gymnasium_classica.models.learner import (
    ItemResponse,
    LearnerModel,
    NodeState,
)
from gymnasium_classica.models.user import LearningRoute, User
from gymnasium_classica.scheduling.session import SessionPhase

KNOOP_ID = "LAT-G-MORF-DECL1-INTRO"


def _node() -> Node:
    return Node(
        id=KNOOP_ID,
        type=NodeType.G,
        taal=Language.LAT,
        titel_nl="De eerste declinatie",
        beschrijving="Overzicht van de 1e declinatie (a-stammen).",
        bloom_niveau=BloomLevel.KENNIS,
        fase=Phase.ONDERBOUW_1,
        items=[
            Item(
                id=f"ITEM-{KNOOP_ID}-001",
                knoop_ids=[KNOOP_ID],
                type=ItemType.HERKENNING,
                richting=Direction.RECEPTIEF,
                moeilijkheid_initieel=0.0,
                discriminatie_initieel=1.0,
                verwachte_tijd_sec=10,
                stimulus="Wat is de nominativus van 'puella'?",
                antwoord="puella",
                feedback="Correct: puella.",
                bron=Source.HANDMATIG,
            )
        ],
    )


def _graph() -> nx.DiGraph:
    g = nx.DiGraph()
    k = _node()
    g.add_node(k.id, node=k)
    return g


def _content_dir_with_scaffolding(tmp_path: Path) -> Path:
    """Schrijf een markdown-bestand dat de loader voor KNOOP_ID kan vinden."""
    (tmp_path / f"{KNOOP_ID}.md").write_text(
        "# Paradigma\n\nPuella, puellae.",
        encoding="utf-8",
    )
    return tmp_path


# --- Unit tests op _should_scaffold ---


class TestShouldScaffoldPure:
    """Tests op de helper zelf — geen scheduler, geen echte sessie."""

    def _make_state(
        self,
        *,
        route: LearningRoute,
        show_grammar_scaffolding: bool = True,
        passage_presented: bool = False,
        item_history: list[ItemResponse] | None = None,
    ):
        from gymnasium_classica.api.session_manager import _SessionState

        learner = LearnerModel(user_id=uuid4())
        if item_history is not None:
            learner.node_states[KNOOP_ID] = NodeState(
                node_id=KNOOP_ID,
                item_history=item_history,
            )
        return _SessionState(
            session_id="t",
            user_id="u",
            learner=learner,
            graph=_graph(),
            started_at=datetime(2026, 4, 17, 10),
            learning_route=route,
            show_grammar_scaffolding=show_grammar_scaffolding,
            passage_presented=passage_presented,
        )

    def test_grammar_first_opt_in_first_introduction(self):
        state = self._make_state(route=LearningRoute.GRAMMAR_FIRST)
        assert _should_scaffold(state, _node(), SessionPhase.NEW_MATERIAL) is True

    def test_grammar_first_opt_out(self):
        state = self._make_state(
            route=LearningRoute.GRAMMAR_FIRST,
            show_grammar_scaffolding=False,
        )
        assert _should_scaffold(state, _node(), SessionPhase.NEW_MATERIAL) is False

    def test_grammar_first_second_time_no_scaffolding(self):
        """NodeState.item_history is niet leeg → al eens gezien."""
        prior = ItemResponse(
            timestamp=datetime(2026, 4, 10, 10),
            item_id=f"ITEM-{KNOOP_ID}-001",
            correct=True,
            response_time_ms=2000,
            node_id=KNOOP_ID,
            richting="receptief",
            mastery_before=0.0,
        )
        state = self._make_state(
            route=LearningRoute.GRAMMAR_FIRST,
            item_history=[prior],
        )
        assert _should_scaffold(state, _node(), SessionPhase.NEW_MATERIAL) is False

    def test_not_new_material_phase(self):
        state = self._make_state(route=LearningRoute.GRAMMAR_FIRST)
        assert _should_scaffold(state, _node(), SessionPhase.WARMUP) is False
        assert _should_scaffold(state, _node(), SessionPhase.DEEPENING) is False
        assert _should_scaffold(state, _node(), SessionPhase.COOLDOWN) is False

    def test_context_first_requires_passage_presented(self):
        not_yet = self._make_state(route=LearningRoute.CONTEXT_FIRST, passage_presented=False)
        assert _should_scaffold(not_yet, _node(), SessionPhase.NEW_MATERIAL) is False

        after = self._make_state(route=LearningRoute.CONTEXT_FIRST, passage_presented=True)
        assert _should_scaffold(after, _node(), SessionPhase.NEW_MATERIAL) is True

    def test_context_first_ignores_opt_out_flag(self):
        """Grammar-first flag mag niet context-first beïnvloeden."""
        state = self._make_state(
            route=LearningRoute.CONTEXT_FIRST,
            show_grammar_scaffolding=False,
            passage_presented=True,
        )
        assert _should_scaffold(state, _node(), SessionPhase.NEW_MATERIAL) is True


# --- Integratie-test via de echte SessionManager ---


class TestGrammarFirstSessionIntegration:
    def test_first_question_has_scaffolding_in_grammar_first(self, tmp_path):
        from gymnasium_classica.api import session_manager as sm_mod

        content_dir = _content_dir_with_scaffolding(tmp_path)
        original = sm_mod.CONTENT_DIR
        sm_mod.CONTENT_DIR = content_dir
        try:
            mgr = SessionManager()
            _, q = mgr.start_session(
                user_id=str(uuid4()),
                learner=LearnerModel(user_id=uuid4()),
                graph=_graph(),
                learning_route=LearningRoute.GRAMMAR_FIRST,
                show_grammar_scaffolding=True,
            )
        finally:
            sm_mod.CONTENT_DIR = original

        assert q is not None
        assert q.node_id == KNOOP_ID
        assert q.scaffolding_content is not None
        assert "Paradigma" in q.scaffolding_content

    def test_opt_out_suppresses_scaffolding_in_grammar_first(self, tmp_path):
        from gymnasium_classica.api import session_manager as sm_mod

        content_dir = _content_dir_with_scaffolding(tmp_path)
        original = sm_mod.CONTENT_DIR
        sm_mod.CONTENT_DIR = content_dir
        try:
            mgr = SessionManager()
            _, q = mgr.start_session(
                user_id=str(uuid4()),
                learner=LearnerModel(user_id=uuid4()),
                graph=_graph(),
                learning_route=LearningRoute.GRAMMAR_FIRST,
                show_grammar_scaffolding=False,
            )
        finally:
            sm_mod.CONTENT_DIR = original

        assert q is not None
        assert q.scaffolding_content is None

    def test_repeat_presentation_has_no_scaffolding(self, tmp_path):
        """Leerling die de node al eerder heeft gezien: geen scaffolding meer."""
        from gymnasium_classica.api import session_manager as sm_mod

        content_dir = _content_dir_with_scaffolding(tmp_path)
        original = sm_mod.CONTENT_DIR
        sm_mod.CONTENT_DIR = content_dir

        learner = LearnerModel(user_id=uuid4())
        # Seed een eerder item_history-entry om "tweede keer" te simuleren.
        learner.node_states[KNOOP_ID] = NodeState(
            node_id=KNOOP_ID,
            item_history=[
                ItemResponse(
                    timestamp=datetime(2026, 4, 10, 10),
                    item_id=f"ITEM-{KNOOP_ID}-001",
                    correct=True,
                    response_time_ms=2000,
                    node_id=KNOOP_ID,
                    richting="receptief",
                    mastery_before=0.0,
                )
            ],
        )
        try:
            mgr = SessionManager()
            _, q = mgr.start_session(
                user_id=str(uuid4()),
                learner=learner,
                graph=_graph(),
                learning_route=LearningRoute.GRAMMAR_FIRST,
                show_grammar_scaffolding=True,
            )
        finally:
            sm_mod.CONTENT_DIR = original

        assert q is not None
        assert q.scaffolding_content is None


class TestUserDefault:
    def test_new_user_has_flag_true(self):
        user = User(email="a@b.nl")
        assert user.show_grammar_scaffolding is True

    def test_existing_user_json_without_flag_defaults_to_true(self):
        """Migratie-pad: bestaande JSON zonder het veld krijgt True via Pydantic-default."""
        old_json = '{"email": "old@b.nl", "auth_provider": "local"}'
        user = User.model_validate_json(old_json)
        assert user.show_grammar_scaffolding is True
