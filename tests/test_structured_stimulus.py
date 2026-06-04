"""Tests voor F1-03: structured-stimulus-adapter in _knoop_to_question.

De frontend leest platte velden op de Question (``question.item_type``,
``question.options``, ``question.instruction``, ``question.hint``,
``question.audio_ref``). De adapter promoot deze uit het eerste item van
een knoop zodat de frontend niet in ``question.items[0].stimulus`` hoeft
te graven.
"""

from __future__ import annotations

from gymnasium_classica.api.session_manager import (
    _knoop_to_question,
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
        knoop_ids=["LAT-V-F01-SUM"],
        type=ItemType.LUISTER_HERKENNING,
        richting=Direction.RECEPTIEF,
        moeilijkheid_initieel=0.0,
        discriminatie_initieel=1.0,
        verwachte_tijd_sec=15,
        stimulus={
            "instruction": "Luister naar het Latijnse woord en kies de juiste vertaling.",
            "audio_ref": "LAT-V-F01-SUM.wav",
            "options": ["zijn", "vaderland", "doden", "vragen, streven naar"],
        },
        antwoord="zijn",
        feedback="Correct: sum betekent 'zijn'.",
        bron=Source.HANDMATIG,
    )


def _text_item(item_id: str = "ITEM-LAT-V-F01-SUM-002") -> Item:
    """Een luister_productie-item met hint."""
    return Item(
        id=item_id,
        knoop_ids=["LAT-V-F01-SUM"],
        type=ItemType.LUISTER_PRODUCTIE,
        richting=Direction.PRODUCTIEF,
        moeilijkheid_initieel=0.2,
        discriminatie_initieel=1.0,
        verwachte_tijd_sec=20,
        stimulus={
            "instruction": "Luister naar het Latijnse woord en typ het in het Latijn.",
            "audio_ref": "LAT-V-F01-SUM.wav",
            "hint": "zijn",
        },
        antwoord="sum",
        feedback="Correct.",
        bron=Source.HANDMATIG,
    )


def _plain_item(item_id: str = "ITEM-LAT-G-DEMO-001") -> Item:
    """Een herkenning-item met een platte-string-stimulus (geen dict)."""
    return Item(
        id=item_id,
        knoop_ids=["LAT-G-MORF-NAAMVAL-INTRO"],
        type=ItemType.HERKENNING,
        richting=Direction.RECEPTIEF,
        moeilijkheid_initieel=-0.5,
        discriminatie_initieel=1.0,
        verwachte_tijd_sec=12,
        stimulus="Hoeveel naamvallen kent het Latijn?",
        antwoord="6",
        feedback="Zes.",
        bron=Source.HANDMATIG,
    )


def _vocab_knoop(items: list[Item]) -> Node:
    return Node(
        id="LAT-V-F01-SUM",
        type=NodeType.V,
        taal=Language.LAT,
        titel_nl="sum, esse — zijn",
        beschrijving="Het werkwoord 'zijn'.",
        bloom_niveau=BloomLevel.KENNIS,
        fase=Phase.ONDERBOUW_1,
        items=items,
    )


def _grammar_knoop(items: list[Item]) -> Node:
    return Node(
        id="LAT-G-MORF-NAAMVAL-INTRO",
        type=NodeType.G,
        taal=Language.LAT,
        titel_nl="Wat is een naamval?",
        beschrijving="Introductie van het concept naamval.",
        bloom_niveau=BloomLevel.KENNIS,
        fase=Phase.ONDERBOUW_1,
        items=items,
    )


class TestPromoteFirstItem:
    def test_luister_herkenning_promotes_options_and_instruction(self):
        knoop = _vocab_knoop([_mc_item()])
        item_type, instruction, options, hint, audio_ref = _promote_first_item(knoop)

        assert item_type == "luister_herkenning"
        assert instruction == ("Luister naar het Latijnse woord en kies de juiste vertaling.")
        assert options == ["zijn", "vaderland", "doden", "vragen, streven naar"]
        assert hint is None
        assert audio_ref == "LAT-V-F01-SUM.wav"

    def test_luister_productie_promotes_hint(self):
        knoop = _vocab_knoop([_text_item()])
        item_type, _instruction, options, hint, audio_ref = _promote_first_item(knoop)

        assert item_type == "luister_productie"
        assert hint == "zijn"
        assert options is None
        assert audio_ref == "LAT-V-F01-SUM.wav"

    def test_plain_string_stimulus_leaves_optional_fields_none(self):
        knoop = _grammar_knoop([_plain_item()])
        item_type, instruction, options, hint, audio_ref = _promote_first_item(knoop)

        assert item_type == "herkenning"
        assert instruction is None
        assert options is None
        assert hint is None
        assert audio_ref is None

    def test_knoop_without_items_returns_all_none(self):
        knoop = _grammar_knoop([])
        assert _promote_first_item(knoop) == (None, None, None, None, None)

    def test_only_first_item_is_promoted(self):
        """Een knoop met MC én text-item promoot alleen het eerste (MC)."""
        knoop = _vocab_knoop([_mc_item(), _text_item()])
        item_type, _instruction, options, hint, _audio_ref = _promote_first_item(knoop)

        assert item_type == "luister_herkenning"
        assert options is not None
        # hint hoort bij item[1] en mag niet lekken
        assert hint is None


class TestKnoopToQuestionFlatShape:
    """De volledige _knoop_to_question-adapter — top-level Question-velden."""

    def test_mc_vocab_knoop_exposes_options_at_top_level(self, tmp_path):
        q = _knoop_to_question(
            _vocab_knoop([_mc_item()]),
            SessionPhase.NEW_MATERIAL,
            content_dir=tmp_path,
        )

        assert q.item_type == "luister_herkenning"
        assert q.options == ["zijn", "vaderland", "doden", "vragen, streven naar"]
        assert q.instruction is not None
        assert q.audio_ref == "LAT-V-F01-SUM.wav"
        assert q.hint is None
        # items-lijst blijft intact voor achterwaartse compatibiliteit
        assert len(q.items) == 1
        assert q.items[0]["type"] == "luister_herkenning"

    def test_text_vocab_knoop_exposes_hint(self, tmp_path):
        q = _knoop_to_question(
            _vocab_knoop([_text_item()]),
            SessionPhase.NEW_MATERIAL,
            content_dir=tmp_path,
        )

        assert q.item_type == "luister_productie"
        assert q.hint == "zijn"
        assert q.options is None

    def test_self_assess_fallback_leaves_flat_fields_none(self, tmp_path):
        """Een knoop zonder items → zelfbeoordeling; geen MC-/hint-velden."""
        knoop = _grammar_knoop([])
        q = _knoop_to_question(knoop, SessionPhase.NEW_MATERIAL, content_dir=tmp_path)

        assert q.item_type is None
        assert q.options is None
        assert q.hint is None
        assert q.instruction is None
        # stimulus valt terug op de self-assess prompt (string)
        assert isinstance(q.stimulus, str)

    def test_plain_string_item_does_not_set_options(self, tmp_path):
        """Grammatica-knoop met platte-string stimulus: wél item_type, geen opties."""
        q = _knoop_to_question(
            _grammar_knoop([_plain_item()]),
            SessionPhase.NEW_MATERIAL,
            content_dir=tmp_path,
        )

        assert q.item_type == "herkenning"
        assert q.options is None
        assert q.instruction is None
        assert q.hint is None


class TestQuestionResponseSerialization:
    """Sanity-check: de adapter in routes/session.py geeft de platte velden door."""

    def test_promoted_fields_round_trip_through_response(self, tmp_path):
        from gymnasium_classica.api.routes.session import _question_to_response

        q = _knoop_to_question(
            _vocab_knoop([_mc_item()]),
            SessionPhase.NEW_MATERIAL,
            content_dir=tmp_path,
        )
        resp = _question_to_response(q)
        assert resp is not None
        payload = resp.model_dump()

        assert payload["item_type"] == "luister_herkenning"
        assert payload["options"] == ["zijn", "vaderland", "doden", "vragen, streven naar"]
        assert payload["instruction"].startswith("Luister")
        assert payload["audio_ref"] == "LAT-V-F01-SUM.wav"
        assert payload["hint"] is None

    def test_none_response(self):
        from gymnasium_classica.api.routes.session import _question_to_response

        assert _question_to_response(None) is None
