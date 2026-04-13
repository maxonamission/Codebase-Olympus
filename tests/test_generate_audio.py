"""Tests for scripts/generate_audio.py — TTS audio generation pipeline."""

import struct
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

# Make the scripts directory importable
_SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(_SCRIPTS_DIR))

from generate_audio import (
    GenerationSummary,
    VocabEntry,
    collect_vocab_nodes,
    extract_lemma,
    generate_all,
    generate_placeholder,
)


# ---------------------------------------------------------------------------
# extract_lemma
# ---------------------------------------------------------------------------


class TestExtractLemma:
    """Tests for extract_lemma()."""

    def test_latin_verb(self):
        assert extract_lemma("sum, esse — zijn") == "sum, esse"

    def test_latin_pronoun(self):
        assert extract_lemma("qui, quae, quod — die, dat; wie, wat") == "qui, quae, quod"

    def test_latin_preposition_with_parentheses(self):
        assert extract_lemma("in (+acc/abl) — in, naar; in, op") == "in (+acc/abl)"

    def test_greek_verb(self):
        assert extract_lemma("εἰμί, εἶναι — zijn") == "εἰμί, εἶναι"

    def test_greek_particle(self):
        assert extract_lemma("καί (part.) — en, ook") == "καί (part.)"

    def test_greek_article(self):
        assert extract_lemma("ὁ, ἡ, τό — de, het (lidwoord)") == "ὁ, ἡ, τό"

    def test_no_dash_returns_full(self):
        assert extract_lemma("puella") == "puella"

    def test_strips_whitespace(self):
        assert extract_lemma("  amicus  ") == "amicus"

    def test_only_first_dash_used(self):
        # Edge case: multiple em-dashes — only split on the first
        assert extract_lemma("a — b — c") == "a"


# ---------------------------------------------------------------------------
# generate_placeholder
# ---------------------------------------------------------------------------


class TestGeneratePlaceholder:
    """Tests for generate_placeholder()."""

    def test_creates_valid_wav(self, tmp_path: Path):
        out = tmp_path / "test.wav"
        generate_placeholder(out)
        assert out.exists()
        assert out.stat().st_size > 44  # WAV header is 44 bytes

    def test_wav_header_valid(self, tmp_path: Path):
        out = tmp_path / "test.wav"
        generate_placeholder(out)

        with open(out, "rb") as f:
            riff = f.read(4)
            assert riff == b"RIFF"
            _file_size = struct.unpack("<I", f.read(4))[0]
            wave = f.read(4)
            assert wave == b"WAVE"
            fmt_tag = f.read(4)
            assert fmt_tag == b"fmt "
            chunk_size = struct.unpack("<I", f.read(4))[0]
            assert chunk_size == 16  # PCM
            audio_format = struct.unpack("<H", f.read(2))[0]
            assert audio_format == 1  # PCM
            num_channels = struct.unpack("<H", f.read(2))[0]
            assert num_channels == 1  # mono
            sample_rate = struct.unpack("<I", f.read(4))[0]
            assert sample_rate == 22050

    def test_wav_is_silent(self, tmp_path: Path):
        out = tmp_path / "test.wav"
        generate_placeholder(out)

        with open(out, "rb") as f:
            f.seek(44)  # skip header
            data = f.read()
            assert all(b == 0 for b in data)


# ---------------------------------------------------------------------------
# collect_vocab_nodes
# ---------------------------------------------------------------------------


class TestCollectVocabNodes:
    """Tests for collect_vocab_nodes() using the real graph data."""

    @pytest.fixture
    def graph_dir(self) -> Path:
        return Path(__file__).resolve().parent.parent / "data" / "graph"

    def test_loads_all_vocab(self, graph_dir: Path):
        entries = collect_vocab_nodes(graph_dir)
        assert len(entries) == 450  # 300 LAT + 150 GRC

    def test_filter_lat(self, graph_dir: Path):
        entries = collect_vocab_nodes(graph_dir, lang="lat")
        assert len(entries) == 300
        assert all(e.taal == "lat" for e in entries)

    def test_filter_grc(self, graph_dir: Path):
        entries = collect_vocab_nodes(graph_dir, lang="grc")
        assert len(entries) == 150
        assert all(e.taal == "grc" for e in entries)

    def test_entries_sorted_by_id(self, graph_dir: Path):
        entries = collect_vocab_nodes(graph_dir)
        ids = [e.knoop_id for e in entries]
        assert ids == sorted(ids)

    def test_all_entries_have_lemma(self, graph_dir: Path):
        entries = collect_vocab_nodes(graph_dir)
        for entry in entries:
            assert entry.lemma, f"Empty lemma for {entry.knoop_id}"


# ---------------------------------------------------------------------------
# generate_all — dry-run
# ---------------------------------------------------------------------------


class TestGenerateAllDryRun:
    """Tests for generate_all() in dry-run mode."""

    def _make_entries(self) -> list[VocabEntry]:
        return [
            VocabEntry(knoop_id="LAT-V-F01-SUM", lemma="sum, esse", taal="lat"),
            VocabEntry(knoop_id="LAT-V-F01-DO", lemma="do, dare", taal="lat"),
            VocabEntry(knoop_id="GRC-V-F01-EIMI", lemma="εἰμί, εἶναι", taal="grc"),
        ]

    def test_dry_run_creates_no_files(self, tmp_path: Path):
        entries = self._make_entries()
        summary = generate_all(entries, tmp_path / "audio", dry_run=True)
        assert not (tmp_path / "audio").exists()
        assert summary.generated == 3
        assert summary.total == 3

    def test_dry_run_reports_skips(self, tmp_path: Path):
        out_dir = tmp_path / "audio"
        out_dir.mkdir()
        # Pre-create one file
        (out_dir / "LAT-V-F01-SUM.wav").touch()

        entries = self._make_entries()
        summary = generate_all(entries, out_dir, dry_run=True)
        assert summary.skipped == 1
        assert summary.generated == 2


# ---------------------------------------------------------------------------
# generate_all — real generation (placeholder backend)
# ---------------------------------------------------------------------------


class TestGenerateAllPlaceholder:
    """Tests for generate_all() with placeholder backend."""

    def _make_entries(self) -> list[VocabEntry]:
        return [
            VocabEntry(knoop_id="LAT-V-F01-SUM", lemma="sum, esse", taal="lat"),
            VocabEntry(knoop_id="GRC-V-F01-EIMI", lemma="εἰμί, εἶναι", taal="grc"),
        ]

    @patch("generate_audio._espeak_available", return_value=False)
    def test_generates_placeholder_files(self, _mock, tmp_path: Path):
        entries = self._make_entries()
        out_dir = tmp_path / "audio"

        summary = generate_all(entries, out_dir)

        assert summary.generated == 2
        assert summary.errors == 0
        assert summary.backend == "placeholder (silent WAV)"
        assert (out_dir / "LAT-V-F01-SUM.wav").exists()
        assert (out_dir / "GRC-V-F01-EIMI.wav").exists()

    @patch("generate_audio._espeak_available", return_value=False)
    def test_skips_existing_without_force(self, _mock, tmp_path: Path):
        entries = self._make_entries()
        out_dir = tmp_path / "audio"
        out_dir.mkdir()
        (out_dir / "LAT-V-F01-SUM.wav").write_bytes(b"existing")

        summary = generate_all(entries, out_dir)

        assert summary.skipped == 1
        assert summary.generated == 1
        # The existing file should not be overwritten
        assert (out_dir / "LAT-V-F01-SUM.wav").read_bytes() == b"existing"

    @patch("generate_audio._espeak_available", return_value=False)
    def test_force_overwrites_existing(self, _mock, tmp_path: Path):
        entries = self._make_entries()
        out_dir = tmp_path / "audio"
        out_dir.mkdir()
        (out_dir / "LAT-V-F01-SUM.wav").write_bytes(b"existing")

        summary = generate_all(entries, out_dir, force=True)

        assert summary.skipped == 0
        assert summary.generated == 2
        # The file should now be a valid WAV, not the old content
        content = (out_dir / "LAT-V-F01-SUM.wav").read_bytes()
        assert content[:4] == b"RIFF"

    @patch("generate_audio._espeak_available", return_value=False)
    def test_creates_output_dir(self, _mock, tmp_path: Path):
        entries = self._make_entries()
        out_dir = tmp_path / "nested" / "audio"

        generate_all(entries, out_dir)

        assert out_dir.exists()
        assert out_dir.is_dir()


# ---------------------------------------------------------------------------
# GenerationSummary
# ---------------------------------------------------------------------------


class TestGenerationSummary:
    def test_print_report(self, capsys):
        summary = GenerationSummary(
            generated=10,
            skipped=2,
            errors=1,
            total=13,
            backend="espeak-ng",
            dry_run=False,
        )
        summary.print_report()
        captured = capsys.readouterr()
        assert "Total:       13" in captured.out
        assert "Generated:   10" in captured.out
        assert "Skipped:     2" in captured.out
        assert "Errors:      1" in captured.out
        assert "espeak-ng" in captured.out

    def test_print_report_dry_run(self, capsys):
        summary = GenerationSummary(dry_run=True, backend="placeholder (silent WAV)")
        summary.print_report()
        captured = capsys.readouterr()
        assert "(dry-run)" in captured.out
