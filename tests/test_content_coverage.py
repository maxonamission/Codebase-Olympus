"""Tests voor scripts/content_coverage.py — dekkingsrapportage per node.

Doel: regressiecheck op de content-pipeline. Als LAT-G onder de drempel
zakt (bijv. doordat nieuwe knopen worden toegevoegd zonder items), faalt
deze test en blokkeert de CI.

Drempels zijn conservatief gekozen op basis van de huidige staat van de
graph (april 2026, ~800 knopen). Ze zijn bewust láger dan de feitelijke
dekking, zodat kleine schommelingen geen vals alarm geven maar echte
regressies wél zichtbaar worden.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

# scripts/ is not a package, so load content_coverage.py via importlib.
# Register in sys.modules so @dataclass can resolve the module during class
# construction (dataclasses looks up cls.__module__ in sys.modules).
_spec = importlib.util.spec_from_file_location(
    "content_coverage",
    Path(__file__).resolve().parent.parent / "scripts" / "content_coverage.py",
)
assert _spec is not None and _spec.loader is not None
_mod = importlib.util.module_from_spec(_spec)
sys.modules["content_coverage"] = _mod
_spec.loader.exec_module(_mod)

compute_coverage = _mod.compute_coverage
find_summary = _mod.find_summary
report_to_dict = _mod.report_to_dict
main = _mod.main

from gymnasium_classica.graph.loader import load_graph

REPO_ROOT = Path(__file__).resolve().parent.parent
GRAPH_DIR = REPO_ROOT / "data" / "graph"


@pytest.fixture(scope="module")
def coverage_report():
    """Bereken het dekkingsrapport één keer per module."""
    graph = load_graph(GRAPH_DIR)
    return compute_coverage(graph)


class TestPerKnoopFields:
    def test_every_node_has_four_flags(self, coverage_report):
        """Elke node krijgt has_items / has_content / has_audio / in_passage."""
        assert len(coverage_report.knopen) > 0
        for k in coverage_report.knopen:
            assert isinstance(k.has_items, bool)
            assert isinstance(k.has_content, bool)
            assert isinstance(k.has_audio, bool)
            assert isinstance(k.in_passage, bool)

    def test_audio_only_true_for_vocabulaire(self, coverage_report):
        """has_audio mag alleen True zijn voor V-knopen."""
        for k in coverage_report.knopen:
            if k.has_audio:
                assert k.type == "V", f"Niet-V node {k.id} heeft has_audio=True"


class TestSummaryBuckets:
    def test_summary_has_bucket_per_taal_type(self, coverage_report):
        """Er moet minimaal een LAT-G, LAT-V, GRC-G en GRC-V bucket zijn."""
        expected = {("lat", "G"), ("lat", "V"), ("grc", "G"), ("grc", "V")}
        actual = {(s.taal, s.type) for s in coverage_report.summaries}
        assert expected.issubset(actual)

    def test_totals_match_node_count(self, coverage_report):
        """Som van alle bucket-totalen gelijk aan aantal knopen."""
        total = sum(s.total for s in coverage_report.summaries)
        assert total == len(coverage_report.knopen)


class TestConservativeThresholds:
    """Regressie-drempels — falen als dekking onder conservatieve ondergrens zakt.

    Huidige staat (referentie):
        LAT-G: items 91.6%, content 25.2%, passage 32.2%
        LAT-V: items 100%, audio 100%
        GRC-G: items 16.9%, passage 29.6%
        GRC-V: items 100%, audio 100%
    """

    def test_lat_grammatica_items_above_threshold(self, coverage_report):
        s = find_summary(coverage_report, "lat", "G")
        assert s is not None
        assert s.items_pct >= 25.0, (
            f"LAT-G items-dekking {s.items_pct:.1f}% < 25% drempel "
            f"({s.items}/{s.total}). Voeg items toe of verlaag drempel expliciet."
        )

    def test_lat_vocabulaire_items_full(self, coverage_report):
        s = find_summary(coverage_report, "lat", "V")
        assert s is not None
        assert s.items_pct >= 90.0, f"LAT-V items-dekking {s.items_pct:.1f}% < 90% drempel."

    def test_lat_vocabulaire_audio_above_threshold(self, coverage_report):
        s = find_summary(coverage_report, "lat", "V")
        assert s is not None
        assert s.audio_pct >= 90.0, f"LAT-V audio-dekking {s.audio_pct:.1f}% < 90% drempel."

    def test_grc_vocabulaire_items_full(self, coverage_report):
        s = find_summary(coverage_report, "grc", "V")
        assert s is not None
        assert s.items_pct >= 90.0, f"GRC-V items-dekking {s.items_pct:.1f}% < 90% drempel."

    def test_grc_vocabulaire_audio_above_threshold(self, coverage_report):
        s = find_summary(coverage_report, "grc", "V")
        assert s is not None
        assert s.audio_pct >= 90.0, f"GRC-V audio-dekking {s.audio_pct:.1f}% < 90% drempel."


class TestJsonOutput:
    def test_report_to_dict_is_json_serialisable(self, coverage_report):
        d = report_to_dict(coverage_report)
        assert "knopen" in d and "summaries" in d
        dumped = json.dumps(d, ensure_ascii=False)
        loaded = json.loads(dumped)
        assert len(loaded["knopen"]) == len(coverage_report.knopen)
        assert len(loaded["summaries"]) == len(coverage_report.summaries)

    def test_cli_output_flag_writes_file(self, tmp_path):
        """Integratietest: `--output` schrijft een leesbaar JSON-bestand."""
        output = tmp_path / "coverage.json"
        exit_code = main(["--output", str(output)])
        assert exit_code == 0
        assert output.exists()
        payload = json.loads(output.read_text(encoding="utf-8"))
        assert payload["knopen"], "knopen-lijst is leeg"
        assert payload["summaries"], "summaries-lijst is leeg"
