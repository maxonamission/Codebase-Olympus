"""Tests for the non-interference scheduling module."""

import pytest

from gymnasium_classica.models.graph import KennisKnoop
from gymnasium_classica.scheduling.non_interference import (
    NonInterferenceState,
    select_next,
)


def _vocab_knoop(id_suffix: str, cluster: str | None = None) -> KennisKnoop:
    """Helper: create a minimal vocabulary KennisKnoop."""
    return KennisKnoop(
        id=f"LAT-V-F01-{id_suffix.upper()}",
        type="V",
        taal="lat",
        titel_nl=f"Woord {id_suffix}",
        beschrijving=f"Vocabulaireknoop {id_suffix}.",
        bloom_niveau="kennis",
        fase="onderbouw_1",
        semantisch_cluster=cluster,
    )


def _grammar_knoop(id_suffix: str) -> KennisKnoop:
    """Helper: create a minimal grammar KennisKnoop (no cluster)."""
    return KennisKnoop(
        id=f"LAT-G-MORF-{id_suffix.upper()}",
        type="G",
        taal="lat",
        titel_nl=f"Grammatica {id_suffix}",
        beschrijving=f"Grammaticaknoop {id_suffix}.",
        bloom_niveau="kennis",
        fase="onderbouw_1",
    )


class TestNonInterferenceState:
    """Tests for NonInterferenceState penalty computation."""

    def test_no_penalty_when_empty(self):
        state = NonInterferenceState()
        knoop = _vocab_knoop("PATER", "familie")
        assert state.cluster_penalty(knoop) == 0.0

    def test_penalty_after_same_cluster(self):
        state = NonInterferenceState()
        pater = _vocab_knoop("PATER", "familie")
        mater = _vocab_knoop("MATER", "familie")

        state.record_selection(pater)
        penalty = state.cluster_penalty(mater)
        # Most recent match → penalty_weights[0] = 0.8
        assert penalty == pytest.approx(0.8)

    def test_no_penalty_different_cluster(self):
        state = NonInterferenceState()
        pater = _vocab_knoop("PATER", "familie")
        bellum = _vocab_knoop("BELLUM", "oorlog")

        state.record_selection(pater)
        assert state.cluster_penalty(bellum) == 0.0

    def test_penalty_decays_with_distance(self):
        state = NonInterferenceState()
        pater = _vocab_knoop("PATER", "familie")
        bellum = _vocab_knoop("BELLUM", "oorlog")
        terra = _vocab_knoop("TERRA", "natuur")
        mater = _vocab_knoop("MATER", "familie")

        state.record_selection(pater)  # 3 steps ago
        state.record_selection(bellum)  # 2 steps ago
        state.record_selection(terra)  # 1 step ago

        penalty = state.cluster_penalty(mater)
        # "familie" was 3 steps ago → penalty_weights[2] = 0.2
        assert penalty == pytest.approx(0.2)

    def test_penalty_zero_beyond_window(self):
        state = NonInterferenceState()
        pater = _vocab_knoop("PATER", "familie")
        filler_clusters = ["oorlog", "natuur", "emotie"]

        state.record_selection(pater)
        for i, cl in enumerate(filler_clusters):
            state.record_selection(_vocab_knoop(f"FILL{i}", cl))

        mater = _vocab_knoop("MATER", "familie")
        # pater is now 4 steps ago, beyond window_size=3
        assert state.cluster_penalty(mater) == 0.0

    def test_no_penalty_for_grammar_knoop(self):
        state = NonInterferenceState()
        pater = _vocab_knoop("PATER", "familie")
        nom = _grammar_knoop("NOM")

        state.record_selection(pater)
        assert state.cluster_penalty(nom) == 0.0

    def test_no_penalty_for_unclustered_vocab(self):
        state = NonInterferenceState()
        word_a = _vocab_knoop("WORDA", None)
        word_b = _vocab_knoop("WORDB", None)

        state.record_selection(word_a)
        assert state.cluster_penalty(word_b) == 0.0

    def test_apply_penalty_reduces_priority(self):
        state = NonInterferenceState()
        pater = _vocab_knoop("PATER", "familie")
        mater = _vocab_knoop("MATER", "familie")

        state.record_selection(pater)
        adjusted = state.apply_penalty(10.0, mater)
        # penalty=0.8 → adjusted = 10.0 * (1 - 0.8) = 2.0
        assert adjusted == pytest.approx(2.0)

    def test_apply_penalty_no_change_different_cluster(self):
        state = NonInterferenceState()
        pater = _vocab_knoop("PATER", "familie")
        bellum = _vocab_knoop("BELLUM", "oorlog")

        state.record_selection(pater)
        adjusted = state.apply_penalty(10.0, bellum)
        assert adjusted == pytest.approx(10.0)


class TestSelectNext:
    """Tests for the select_next() function."""

    def test_empty_candidates(self):
        state = NonInterferenceState()
        assert select_next([], state) is None

    def test_selects_highest_priority(self):
        state = NonInterferenceState()
        low = _vocab_knoop("LOW", "oorlog")
        high = _vocab_knoop("HIGH", "natuur")
        candidates = [(1.0, low), (5.0, high)]

        selected = select_next(candidates, state)
        assert selected.id == high.id

    def test_penalty_overrides_base_priority(self):
        state = NonInterferenceState()
        pater = _vocab_knoop("PATER", "familie")

        # Select pater first to set up the penalty
        state.record_selection(pater)

        # mater has higher base priority but same cluster
        mater = _vocab_knoop("MATER", "familie")
        bellum = _vocab_knoop("BELLUM", "oorlog")
        candidates = [(5.0, mater), (4.0, bellum)]

        selected = select_next(candidates, state)
        # mater: 5.0 * (1 - 0.8) = 1.0
        # bellum: 4.0 * (1 - 0.0) = 4.0
        assert selected.id == bellum.id

    def test_updates_state_after_selection(self):
        state = NonInterferenceState()
        knoop = _vocab_knoop("PATER", "familie")
        select_next([(1.0, knoop)], state)
        assert state.recent_clusters == ["familie"]

    def test_10_items_max_2_same_cluster(self):
        """The scheduler must never select more than 2 items from the same
        cluster in a sequence of 10 consecutive vocabulary items.

        Uses 5 clusters so the constraint is mathematically satisfiable
        (10 items / 5 clusters = 2 per cluster).
        """
        state = NonInterferenceState()

        # Build a candidate pool: 5 clusters, 4 words each, equal base priority
        clusters = ["familie", "oorlog", "natuur", "emotie", "politiek"]
        pool: list[tuple[float, KennisKnoop]] = []
        for cl in clusters:
            for i in range(4):
                suffix = f"{cl[:3].upper()}{i}"
                pool.append((1.0, _vocab_knoop(suffix, cl)))

        # Select 10 items
        selected: list[KennisKnoop] = []
        for _ in range(10):
            result = select_next(pool, state)
            assert result is not None
            selected.append(result)

        # The overall constraint: max 2 of the same cluster in the full 10
        clusters_selected = [k.semantisch_cluster for k in selected]
        from collections import Counter

        counts = Counter(clusters_selected)
        for cluster, count in counts.items():
            assert count <= 2, (
                f"Cluster {cluster!r} appeared {count} times in 10 selections. "
                f"Sequence: {clusters_selected}"
            )
