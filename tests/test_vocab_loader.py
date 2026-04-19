"""Tests voor F1-05: vocab/loader.py — structured metadata per lemma."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from gymnasium_classica.graph.loader import load_graph
from gymnasium_classica.models.graph import KnoopType
from gymnasium_classica.vocab.loader import (
    VocabEntry,
    knoop_id_from_file_and_entry,
    load_vocab_metadata,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
VOCAB_DIR = REPO_ROOT / "data" / "vocab_sources"
GRAPH_DIR = REPO_ROOT / "data" / "graph"


class TestKnoopIdComposition:
    def test_lat_f01(self):
        assert knoop_id_from_file_and_entry("lat_f01_words.json", "SUM") == ("LAT-V-F01-SUM")

    def test_grc_f02(self):
        assert knoop_id_from_file_and_entry("grc_f02_words.json", "LOGOS") == ("GRC-V-F02-LOGOS")


class TestLoadFromFile:
    def test_single_file_returns_keyed_dict(self, tmp_path):
        path = tmp_path / "lat_f99_words.json"
        path.write_text(
            json.dumps(
                [
                    {
                        "lemma": "foo",
                        "id": "FOO",
                        "pos": "noun",
                        "conj": "1",
                        "gen": "foo",
                        "mean": "foo-betekenis",
                        "cl": "test",
                    }
                ]
            ),
            encoding="utf-8",
        )
        result = load_vocab_metadata(path)
        assert set(result.keys()) == {"LAT-V-F99-FOO"}
        entry = result["LAT-V-F99-FOO"]
        assert isinstance(entry, VocabEntry)
        assert entry.lemma == "foo"
        assert entry.pos == "noun"
        assert entry.cl == "test"

    def test_rejects_non_list(self, tmp_path):
        path = tmp_path / "lat_f99_words.json"
        path.write_text('{"not": "a list"}', encoding="utf-8")
        with pytest.raises(ValueError, match="JSON list"):
            load_vocab_metadata(path)


class TestLoadFromDirectory:
    def test_empty_directory_raises(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            load_vocab_metadata(tmp_path)

    def test_duplicate_entry_in_same_file_rejected(self, tmp_path):
        path = tmp_path / "lat_f01_words.json"
        path.write_text(
            json.dumps(
                [
                    {"lemma": "x", "id": "X", "pos": "noun", "mean": "m1"},
                    {"lemma": "x2", "id": "X", "pos": "noun", "mean": "m2"},
                ]
            ),
            encoding="utf-8",
        )
        with pytest.raises(ValueError, match="Duplicate"):
            load_vocab_metadata(path)


class TestRealVocabSources:
    """Echte data/vocab_sources tegen data/graph/*.json — geen mocks."""

    @pytest.fixture(scope="class")
    def lookup(self) -> dict[str, VocabEntry]:
        return load_vocab_metadata(VOCAB_DIR)

    def test_lookup_has_450_entries(self, lookup):
        assert len(lookup) == 450

    def test_every_v_knoop_has_metadata(self, lookup):
        """Alle V-knopen in de productie-graph moeten matchen."""
        graph = load_graph(GRAPH_DIR)
        v_ids = [n for n in graph.nodes if graph.nodes[n]["knoop"].type == KnoopType.V]
        missing = [kid for kid in v_ids if kid not in lookup]
        assert missing == [], f"V-knopen zonder vocab_source-entry: {missing[:5]}"

    def test_sample_entries_have_expected_shape(self, lookup):
        sum_entry = lookup["LAT-V-F01-SUM"]
        assert sum_entry.lemma == "sum"
        assert sum_entry.pos == "verb"
        assert "zijn" in sum_entry.mean

    def test_cluster_labels_where_present(self, lookup):
        clusters = {e.cl for e in lookup.values() if e.cl is not None}
        assert "communicatie" in clusters
        assert "beweging" in clusters
