"""Tests voor F1-03: structured-stimulus-adapter in _node_to_question.

De frontend leest platte velden op de Question (``question.item_type``,
``question.options``, ``question.instruction``, ``question.hint``,
``question.audio_ref``). De adapter promoot deze uit het eerste item van
een node zodat de frontend niet in ``question.items[0].stimulus`` hoeft
te graven.
"""

from __future__ import annotations

from gymnasium_classica.api.session_manager import (
    _node_to_question,
    _promote_first_item,
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
from gymnasium_classica.scheduling.session import SessionPhase


def _mc_item(item_id: str = "ITEM-LAT-V-F01-SUM-001") -> Item:
    """Een luister_herkenning-item zoals de vocab-generator ze produceert."""
    return Item(
        id=item_id,
        node_ids=["LAT-V-F01-SUM"],
        type=ItemType.LISTENING_RECOGNITION,
        direction=Direction.RECEPTIVE,
        difficulty_initial=0.0,
        discrimination_initial=1.0,
        expected_time_sec=15,
        stimulus={
            "instruction": "Luister naar het Latijnse woord en kies de juiste vertaling.",
            "audio_ref": "LAT-V-F01-SUM.wav",
            "options": ["zijn", "vaderland", "doden", "vragen, streven naar"],
        },
        answer="zijn",
        feedback="Correct: sum betekent 'zijn'.",
        source=Source.MANUAL,
    )


def _text_item(item_id: str = "ITEM-LAT-V-F01-SUM-002") -> Item:
    """Een luister_productie-item met hint."""
    return Item(
        id=item_id,
        node_ids=["LAT-V-F01-SUM"],
        type=ItemType.LISTENING_PRODUCTION,
        direction=Direction.PRODUCTIVE,
        difficulty_initial=0.2,
        discrimination_initial=1.0,
        expected_time_sec=20,
        stimulus={
            "instruction": "Luister naar het Latijnse woord en typ het in het Latijn.",
            "audio_ref": "LAT-V-F01-SUM.wav",
            "hint": "zijn",
        },
        answer="sum",
        feedback="Correct.",
        source=Source.MANUAL,
    )


def _plain_item(item_id: str = "ITEM-LAT-G-DEMO-001") -> Item:
    """Een herkenning-item met een platte-string-stimulus (geen dict)."""
    return Item(
        id=item_id,
        node_ids=["LAT-G-MORF-NAAMVAL-INTRO"],
        type=ItemType.RECOGNITION,
        direction=Direction.RECEPTIVE,
        difficulty_initial=-0.5,
        discrimination_initial=1.0,
        expected_time_sec=12,
        stimulus="Hoeveel naamvallen kent het Latijn?",
        answer="6",
        feedback="Zes.",
        source=Source.MANUAL,
    )


def _vocab_node(items: list[Item]) -> Node:
    return Node(
        id="LAT-V-F01-SUM",
        type=NodeType.V,
        language=Language.LAT,
        title_nl="sum, esse — zijn",
        description="Het werkwoord 'zijn'.",
        bloom_level=BloomLevel.KNOWLEDGE,
        phase=Phase.ONDERBOUW_1,
        items=items,
    )


def _grammar_node(items: list[Item]) -> Node:
    return Node(
        id="LAT-G-MORF-NAAMVAL-INTRO",
        type=NodeType.G,
        language=Language.LAT,
        title_nl="Wat is een naamval?",
        description="Introductie van het concept naamval.",
        bloom_level=BloomLevel.KNOWLEDGE,
        phase=Phase.ONDERBOUW_1,
        items=items,
    )


class TestPromoteFirstItem:
    def test_luister_herkenning_promotes_options_and_instruction(self):
        node = _vocab_node([_mc_item()])
        item_type, instruction, options, hint, audio_ref = _promote_first_item(node)

        assert item_type == "listening_recognition"
        assert instruction == ("Luister naar het Latijnse woord en kies de juiste vertaling.")
        assert options == ["zijn", "vaderland", "doden", "vragen, streven naar"]
        assert hint is None
        assert audio_ref == "LAT-V-F01-SUM.wav"

    def test_luister_productie_promotes_hint(self):
        node = _vocab_node([_text_item()])
        item_type, _instruction, options, hint, audio_ref = _promote_first_item(node)

        assert item_type == "listening_production"
        assert hint == "zijn"
        assert options is None
        assert audio_ref == "LAT-V-F01-SUM.wav"

    def test_plain_string_stimulus_leaves_optional_fields_none(self):
        node = _grammar_node([_plain_item()])
        item_type, instruction, options, hint, audio_ref = _promote_first_item(node)

        assert item_type == "recognition"
        assert instruction is None
        assert options is None
        assert hint is None
        assert audio_ref is None

    def test_node_without_items_returns_all_none(self):
        node = _grammar_node([])
        assert _promote_first_item(node) == (None, None, None, None, None)

    def test_only_first_item_is_promoted(self):
        """Een node met MC én text-item promoot alleen het eerste (MC)."""
        node = _vocab_node([_mc_item(), _text_item()])
        item_type, _instruction, options, hint, _audio_ref = _promote_first_item(node)

        assert item_type == "listening_recognition"
        assert options is not None
        # hint hoort bij item[1] en mag niet lekken
        assert hint is None


class TestKnoopToQuestionFlatShape:
    """De volledige _node_to_question-adapter — top-level Question-velden."""

    def test_mc_vocab_node_exposes_options_at_top_level(self, tmp_path):
        q = _node_to_question(
            _vocab_node([_mc_item()]),
            SessionPhase.NEW_MATERIAL,
            content_dir=tmp_path,
        )

        assert q.item_type == "listening_recognition"
        assert q.options == ["zijn", "vaderland", "doden", "vragen, streven naar"]
        assert q.instruction is not None
        assert q.audio_ref == "LAT-V-F01-SUM.wav"
        assert q.hint is None
        # items-lijst blijft intact voor achterwaartse compatibiliteit
        assert len(q.items) == 1
        assert q.items[0]["type"] == "listening_recognition"

    def test_text_vocab_node_exposes_hint(self, tmp_path):
        q = _node_to_question(
            _vocab_node([_text_item()]),
            SessionPhase.NEW_MATERIAL,
            content_dir=tmp_path,
        )

        assert q.item_type == "listening_production"
        assert q.hint == "zijn"
        assert q.options is None

    def test_self_assess_fallback_leaves_flat_fields_none(self, tmp_path):
        """Een node zonder items → zelfbeoordeling; geen MC-/hint-velden."""
        node = _grammar_node([])
        q = _node_to_question(node, SessionPhase.NEW_MATERIAL, content_dir=tmp_path)

        assert q.item_type is None
        assert q.options is None
        assert q.hint is None
        assert q.instruction is None
        # stimulus valt terug op de self-assess prompt (string)
        assert isinstance(q.stimulus, str)

    def test_plain_string_item_does_not_set_options(self, tmp_path):
        """Grammatica-node met platte-string stimulus: wél item_type, geen opties."""
        q = _node_to_question(
            _grammar_node([_plain_item()]),
            SessionPhase.NEW_MATERIAL,
            content_dir=tmp_path,
        )

        assert q.item_type == "recognition"
        assert q.options is None
        assert q.instruction is None
        assert q.hint is None


class TestQuestionResponseSerialization:
    """Sanity-check: de adapter in routes/session.py geeft de platte velden door."""

    def test_promoted_fields_round_trip_through_response(self, tmp_path):
        from gymnasium_classica.api.routes.session import _question_to_response

        q = _node_to_question(
            _vocab_node([_mc_item()]),
            SessionPhase.NEW_MATERIAL,
            content_dir=tmp_path,
        )
        resp = _question_to_response(q)
        assert resp is not None
        payload = resp.model_dump()

        assert payload["item_type"] == "listening_recognition"
        assert payload["options"] == ["zijn", "vaderland", "doden", "vragen, streven naar"]
        assert payload["instruction"].startswith("Luister")
        assert payload["audio_ref"] == "LAT-V-F01-SUM.wav"
        assert payload["hint"] is None

    def test_none_response(self):
        from gymnasium_classica.api.routes.session import _question_to_response

        assert _question_to_response(None) is None
