"""Tests voor het worked-example-oefentype met faded scaffolding (L3-01)."""

import json
from itertools import pairwise
from pathlib import Path

import pytest
from pydantic import ValidationError

from gymnasium_classica.models.graph import (
    Direction,
    Item,
    ItemType,
    Source,
    WorkedStep,
)
from gymnasium_classica.scheduling.session import is_introduction_item


def _item(**overrides) -> Item:
    base = dict(
        id="ITEM-LAT-G-X-001",
        node_ids=["LAT-G-X"],
        type=ItemType.RECOGNITION,
        direction=Direction.RECEPTIVE,
        difficulty_initial=0.0,
        discrimination_initial=1.0,
        expected_time_sec=10,
        stimulus="?",
        answer="a",
        feedback="fb",
        source=Source.MANUAL,
    )
    base.update(overrides)
    return Item(**base)


def _steps(*levels: float) -> list[WorkedStep]:
    return [
        WorkedStep(order=i, support_level=lvl, content=f"step {i}") for i, lvl in enumerate(levels)
    ]


class TestWorkedExampleValidation:
    def test_valid_faded_scaffolding_accepted(self):
        item = _item(type=ItemType.WORKED_EXAMPLE, worked_steps=_steps(1.0, 0.5, 0.0))
        assert item.is_worked_example
        assert len(item.worked_steps) == 3

    def test_requires_steps(self):
        with pytest.raises(ValidationError, match="non-empty worked_steps"):
            _item(type=ItemType.WORKED_EXAMPLE)

    def test_rejects_increasing_support(self):
        with pytest.raises(ValidationError, match="must not increase"):
            _item(type=ItemType.WORKED_EXAMPLE, worked_steps=_steps(0.5, 0.8))

    def test_allows_equal_support_non_increasing(self):
        # Gelijk steunniveau is toegestaan (monotoon niet-stijgend).
        item = _item(type=ItemType.WORKED_EXAMPLE, worked_steps=_steps(0.5, 0.5, 0.2))
        assert item.is_worked_example

    def test_rejects_duplicate_orders(self):
        steps = [
            WorkedStep(order=1, support_level=1.0, content="a"),
            WorkedStep(order=1, support_level=0.5, content="b"),
        ]
        with pytest.raises(ValidationError, match="unique order"):
            _item(type=ItemType.WORKED_EXAMPLE, worked_steps=steps)

    def test_rejects_steps_on_non_worked_example(self):
        with pytest.raises(ValidationError, match="only allowed on worked_example"):
            _item(type=ItemType.RECOGNITION, worked_steps=_steps(1.0, 0.0))

    def test_unordered_input_is_sorted_for_validation(self):
        # In willekeurige volgorde aangeleverd, maar op order gesorteerd niet-stijgend.
        steps = [
            WorkedStep(order=2, support_level=0.0, content="c"),
            WorkedStep(order=0, support_level=1.0, content="a"),
            WorkedStep(order=1, support_level=0.5, content="b"),
        ]
        item = _item(type=ItemType.WORKED_EXAMPLE, worked_steps=steps)
        assert item.is_worked_example


class TestIntroductionMarking:
    def test_worked_example_is_introduction(self):
        item = _item(type=ItemType.WORKED_EXAMPLE, worked_steps=_steps(1.0, 0.0))
        assert is_introduction_item(item) is True

    def test_other_types_are_not_introduction(self):
        assert is_introduction_item(_item(type=ItemType.RECOGNITION)) is False


class TestExampleItemInData:
    def test_poc_graph_contains_valid_worked_example(self):
        path = Path("data/graph/lat_grammatica_poc.json")
        data = json.loads(path.read_text(encoding="utf-8"))
        worked = [
            item
            for node in data["nodes"]
            for item in node.get("items", [])
            if item.get("type") == "worked_example"
        ]
        assert worked, "verwacht minstens één worked_example-item in de PoC-graph"
        # Valideert tegen het model (inclusief faded-scaffolding-regel).
        parsed = Item.model_validate(worked[0])
        assert parsed.is_worked_example
        levels = [s.support_level for s in sorted(parsed.worked_steps, key=lambda s: s.order)]
        assert all(b <= a for a, b in pairwise(levels))
