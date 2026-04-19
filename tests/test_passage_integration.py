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
            assert p.taal in ("lat", "grc", "shared"), f"{p.id}: invalid taal {p.taal}"
            assert p.titel, f"{p.id}: missing titel"
            assert p.tekst, f"{p.id}: missing tekst"
            assert len(p.annotaties) > 0, f"{p.id}: no annotaties"
            assert 1 <= p.moeilijkheid <= 5, f"{p.id}: moeilijkheid {p.moeilijkheid} out of range"
            assert len(p.knoop_ids) > 0, f"{p.id}: no knoop_ids"

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
            for a in p.annotaties:
                assert a.woord, f"{p.id}: annotation missing woord"
                assert a.lemma, f"{p.id}: annotation missing lemma"
                assert a.vertaling, f"{p.id}: annotation missing vertaling"
