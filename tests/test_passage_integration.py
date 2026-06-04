"""Integration test: load and validate all passage files in data/passages/."""

from pathlib import Path

import pytest

from gymnasium_classica.models.passage import Passage
from gymnasium_classica.passages.loader import load_passages

PASSAGES_DIR = Path(__file__).parent.parent / "data" / "passages"


class TestPassageIntegration:
    """End-to-end validation of all passage files against the Passage model."""

    def test_all_passages_load(self):
        """All JSON files in data/passages/ must load without errors."""
        if not PASSAGES_DIR.is_dir():
            pytest.skip("data/passages/ not found")
        passages = load_passages(PASSAGES_DIR)
        assert len(passages) > 0, "Expected at least one passage"

    def test_all_passages_have_required_fields(self):
        """Every passage must have the canonical fields from the Passage model."""
        if not PASSAGES_DIR.is_dir():
            pytest.skip("data/passages/ not found")
        passages = load_passages(PASSAGES_DIR)
        for p in passages:
            assert isinstance(p, Passage)
            assert p.id, "Passage missing id"
            assert p.language in ("lat", "grc", "shared"), f"{p.id}: invalid language {p.language}"
            assert p.title, f"{p.id}: missing titel"
            assert p.text, f"{p.id}: missing tekst"
            assert len(p.annotations) > 0, f"{p.id}: no annotations"
            assert 1 <= p.difficulty <= 5, f"{p.id}: difficulty {p.difficulty} out of range"
            assert len(p.node_ids) > 0, f"{p.id}: no node_ids"

    def test_no_duplicate_passage_ids(self):
        """All passage IDs must be unique across all files."""
        if not PASSAGES_DIR.is_dir():
            pytest.skip("data/passages/ not found")
        passages = load_passages(PASSAGES_DIR)
        ids = [p.id for p in passages]
        assert len(ids) == len(set(ids)), f"Duplicate IDs: {[x for x in ids if ids.count(x) > 1]}"

    def test_annotations_have_valid_fields(self):
        """Every word annotation must have woord, lemma, and vertaling."""
        if not PASSAGES_DIR.is_dir():
            pytest.skip("data/passages/ not found")
        passages = load_passages(PASSAGES_DIR)
        for p in passages:
            for a in p.annotations:
                assert a.word, f"{p.id}: annotation missing woord"
                assert a.lemma, f"{p.id}: annotation missing lemma"
                assert a.translation, f"{p.id}: annotation missing vertaling"
