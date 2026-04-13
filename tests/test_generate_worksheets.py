"""Tests for scripts/generate_worksheets.py — PDF worksheet generation."""

import re
from pathlib import Path

import pytest

from gymnasium_classica.models.graph import (
    BloomNiveau,
    Bron,
    Fase,
    Item,
    ItemType,
    KennisKnoop,
    KnoopType,
    Richting,
    Taal,
)

# Import the module under test (scripts/ is not a package, so use importlib)
import importlib.util

_spec = importlib.util.spec_from_file_location(
    "generate_worksheets",
    Path(__file__).resolve().parent.parent / "scripts" / "generate_worksheets.py",
)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

parse_markdown_tables = _mod.parse_markdown_tables
generate_worksheet = _mod.generate_worksheet
_strip_bold = _mod._strip_bold
_make_empty_paradigm_table = _mod._make_empty_paradigm_table
_build_exercise_elements = _mod._build_exercise_elements
_build_greek_writing_lines = _mod._build_greek_writing_lines
_build_styles = _mod._build_styles
_register_fonts = _mod._register_fonts


# --- Fixtures ---


@pytest.fixture
def sample_knoop() -> KennisKnoop:
    """A minimal grammar knoop for testing."""
    return KennisKnoop(
        id="LAT-G-MORF-DECL1-PARAD",
        type=KnoopType.G,
        taal=Taal.LAT,
        titel_nl="Paradigma 1e declinatie",
        beschrijving="De 1e declinatie met modelwoord puella.",
        bloom_niveau=BloomNiveau.KENNIS,
        fase=Fase.ONDERBOUW_1,
        items=[
            Item(
                id="ITEM-LAT-G-MORF-DECL1-PARAD-001",
                knoop_ids=["LAT-G-MORF-DECL1-PARAD"],
                type=ItemType.HERKENNING,
                richting=Richting.RECEPTIEF,
                moeilijkheid_initieel=-0.5,
                discriminatie_initieel=1.0,
                verwachte_tijd_sec=15,
                stimulus="Geef de genitivus singularis van puella.",
                antwoord="puellae",
                feedback="De genitivus singularis van de 1e declinatie eindigt op -ae.",
                bron=Bron.HANDMATIG,
            ),
        ],
    )


@pytest.fixture
def greek_letter_knoop() -> KennisKnoop:
    """A Greek alphabet knoop for testing writing lines."""
    return KennisKnoop(
        id="GRC-G-FONL-ALFA-ALFA",
        type=KnoopType.G,
        taal=Taal.GRC,
        titel_nl="Α α — alfa",
        beschrijving="De letter alfa: Α (majuskel), α (minuskel). Klank: kort of lang /a/.",
        bloom_niveau=BloomNiveau.KENNIS,
        fase=Fase.ONDERBOUW_1,
    )


@pytest.fixture
def knoop_no_content() -> KennisKnoop:
    """A knoop with no content and no items."""
    return KennisKnoop(
        id="LAT-G-MORF-GENUS-INTRO",
        type=KnoopType.G,
        taal=Taal.LAT,
        titel_nl="Grammaticaal geslacht",
        beschrijving="Introductie van het concept genus.",
        bloom_niveau=BloomNiveau.KENNIS,
        fase=Fase.ONDERBOUW_1,
    )


SAMPLE_MARKDOWN = """\
---
knoop_id: LAT-G-MORF-DECL1-PARAD
---

# Paradigma 1e declinatie

## Paradigma

| Naamval      | Enkelvoud     | Meervoud       |
|-------------|--------------|---------------|
| Nominativus | puell-**a**    | puell-**ae**    |
| Genitivus   | puell-**ae**   | puell-**ārum**  |
| Dativus     | puell-**ae**   | puell-**īs**    |

## Herkenningstips

Blah blah.
"""


# --- Tests: _strip_bold ---


class TestStripBold:
    def test_removes_double_asterisks(self):
        assert _strip_bold("puell-**a**") == "puell-a"

    def test_handles_multiple_bold(self):
        assert _strip_bold("**foo** and **bar**") == "foo and bar"

    def test_no_bold(self):
        assert _strip_bold("no bold here") == "no bold here"

    def test_empty_string(self):
        assert _strip_bold("") == ""


# --- Tests: parse_markdown_tables ---


class TestParseMarkdownTables:
    def test_extracts_single_table(self):
        tables = parse_markdown_tables(SAMPLE_MARKDOWN)
        assert len(tables) == 1

    def test_table_has_heading(self):
        tables = parse_markdown_tables(SAMPLE_MARKDOWN)
        assert tables[0]["heading"] == "Paradigma"

    def test_table_rows_count(self):
        tables = parse_markdown_tables(SAMPLE_MARKDOWN)
        # Header + 3 data rows (separator skipped)
        assert len(tables[0]["rows"]) == 4

    def test_header_row(self):
        tables = parse_markdown_tables(SAMPLE_MARKDOWN)
        header = tables[0]["rows"][0]
        assert "Naamval" in header
        assert "Enkelvoud" in header
        assert "Meervoud" in header

    def test_bold_stripped_from_cells(self):
        tables = parse_markdown_tables(SAMPLE_MARKDOWN)
        # Second row (Nominativus): bold markers should be removed
        nom_row = tables[0]["rows"][1]
        assert "**" not in nom_row[1]
        assert "puell-a" in nom_row[1]

    def test_no_tables(self):
        tables = parse_markdown_tables("Just some text\nno tables here")
        assert tables == []

    def test_multiple_tables(self):
        content = """\
## Table A

| Col1 | Col2 |
|------|------|
| a    | b    |

## Table B

| X | Y |
|---|---|
| 1 | 2 |
"""
        tables = parse_markdown_tables(content)
        assert len(tables) == 2
        assert tables[0]["heading"] == "Table A"
        assert tables[1]["heading"] == "Table B"


# --- Tests: generate_worksheet ---


class TestGenerateWorksheet:
    def test_generates_pdf_with_content(self, sample_knoop, tmp_path):
        """Worksheet with markdown content produces a valid PDF."""
        content_dir = tmp_path / "content"
        content_dir.mkdir()
        (content_dir / "LAT-G-MORF-DECL1-PARAD.md").write_text(
            SAMPLE_MARKDOWN, encoding="utf-8"
        )

        output = tmp_path / "worksheets" / "LAT-G-MORF-DECL1-PARAD.pdf"
        result = generate_worksheet(sample_knoop, content_dir, output)

        assert result is True
        assert output.exists()
        # Check valid PDF header
        with open(output, "rb") as f:
            assert f.read(5) == b"%PDF-"

    def test_generates_pdf_with_items_only(self, tmp_path):
        """Knoop with items but no content file still produces a PDF."""
        knoop = KennisKnoop(
            id="LAT-G-SYNT-WRDVLG",
            type=KnoopType.G,
            taal=Taal.LAT,
            titel_nl="Woordvolgorde",
            beschrijving="Latijnse woordvolgorde is vrij.",
            bloom_niveau=BloomNiveau.BEGRIP,
            fase=Fase.ONDERBOUW_1,
            items=[
                Item(
                    id="ITEM-LAT-G-SYNT-WRDVLG-001",
                    knoop_ids=["LAT-G-SYNT-WRDVLG"],
                    type=ItemType.PRODUCTIE,
                    richting=Richting.PRODUCTIEF,
                    moeilijkheid_initieel=0.0,
                    discriminatie_initieel=1.0,
                    verwachte_tijd_sec=30,
                    stimulus="Vertaal: Het meisje ziet de heer.",
                    antwoord="Puella dominum videt.",
                    feedback="SOV is de gangbare volgorde.",
                    bron=Bron.HANDMATIG,
                ),
            ],
        )
        content_dir = tmp_path / "content"
        content_dir.mkdir()
        output = tmp_path / "out" / "LAT-G-SYNT-WRDVLG.pdf"
        result = generate_worksheet(knoop, content_dir, output)

        assert result is True
        assert output.exists()

    def test_skips_knoop_without_content_or_items(self, knoop_no_content, tmp_path):
        """Knoop with no content and no items is skipped."""
        content_dir = tmp_path / "content"
        content_dir.mkdir()
        output = tmp_path / "out" / "test.pdf"
        result = generate_worksheet(knoop_no_content, content_dir, output)

        assert result is False
        assert not output.exists()

    def test_greek_writing_lines(self, greek_letter_knoop, tmp_path):
        """Greek alphabet knoop produces a PDF with writing practice."""
        content_dir = tmp_path / "content"
        content_dir.mkdir()
        output = tmp_path / "worksheets" / "GRC-G-FONL-ALFA-ALFA.pdf"
        result = generate_worksheet(greek_letter_knoop, content_dir, output)

        assert result is True
        assert output.exists()
        # File should be a valid PDF of reasonable size
        size = output.stat().st_size
        assert size > 1000  # non-trivial PDF

    def test_output_dir_created(self, sample_knoop, tmp_path):
        """Output directory is created automatically if it doesn't exist."""
        content_dir = tmp_path / "content"
        content_dir.mkdir()
        (content_dir / "LAT-G-MORF-DECL1-PARAD.md").write_text(
            SAMPLE_MARKDOWN, encoding="utf-8"
        )

        output = tmp_path / "deep" / "nested" / "dir" / "test.pdf"
        result = generate_worksheet(sample_knoop, content_dir, output)

        assert result is True
        assert output.exists()

    def test_content_ref_used(self, tmp_path):
        """When knoop has content_ref, that file is loaded."""
        knoop = KennisKnoop(
            id="LAT-G-MORF-DECL1-PARAD",
            type=KnoopType.G,
            taal=Taal.LAT,
            titel_nl="1e declinatie paradigma",
            beschrijving="Paradigma.",
            bloom_niveau=BloomNiveau.KENNIS,
            fase=Fase.ONDERBOUW_1,
            content_ref="LAT-G-MORF-DECL1-PARAD.md",
        )

        content_dir = tmp_path / "content"
        content_dir.mkdir()
        (content_dir / "LAT-G-MORF-DECL1-PARAD.md").write_text(
            SAMPLE_MARKDOWN, encoding="utf-8"
        )

        output = tmp_path / "out" / "test.pdf"
        result = generate_worksheet(knoop, content_dir, output)
        assert result is True
        assert output.exists()


# --- Tests: _build_exercise_elements ---


class TestBuildExerciseElements:
    def test_returns_elements_for_items(self, sample_knoop):
        _register_fonts()
        styles = _build_styles()
        elements = _build_exercise_elements(sample_knoop, styles)
        # Should contain heading + exercise + line table + spacer
        assert len(elements) >= 3

    def test_empty_for_no_items(self, knoop_no_content):
        _register_fonts()
        styles = _build_styles()
        elements = _build_exercise_elements(knoop_no_content, styles)
        assert elements == []


# --- Tests: _build_greek_writing_lines ---


class TestBuildGreekWritingLines:
    def test_returns_elements_for_greek_letter(self, greek_letter_knoop):
        _register_fonts()
        styles = _build_styles()
        elements = _build_greek_writing_lines(greek_letter_knoop, styles)
        # Should have heading + instructions + spacer + label + table + spacer (x2 for maj/min)
        assert len(elements) >= 5

    def test_empty_for_non_greek_knoop(self, sample_knoop):
        _register_fonts()
        styles = _build_styles()
        elements = _build_greek_writing_lines(sample_knoop, styles)
        assert elements == []

    def test_empty_for_non_letter_greek_knoop(self):
        """Greek group nodes (not individual letters) should not get writing lines."""
        _register_fonts()
        styles = _build_styles()
        knoop = KennisKnoop(
            id="GRC-G-FONL-ALFA-GRP1",
            type=KnoopType.G,
            taal=Taal.GRC,
            titel_nl="Groep 1: identieke letters",
            beschrijving="Letters die identiek zijn aan het Latijnse alfabet.",
            bloom_niveau=BloomNiveau.KENNIS,
            fase=Fase.ONDERBOUW_1,
        )
        elements = _build_greek_writing_lines(knoop, styles)
        assert elements == []


# --- Tests: _make_empty_paradigm_table ---


class TestMakeEmptyParadigmTable:
    def test_returns_table(self):
        _register_fonts()
        styles = _build_styles()
        table_data = {
            "heading": "Test",
            "rows": [
                ["Naamval", "Enkelvoud", "Meervoud"],
                ["Nominativus", "puella", "puellae"],
                ["Genitivus", "puellae", "puellarum"],
            ],
        }
        result = _make_empty_paradigm_table(table_data, styles)
        # Should return a Table object
        from reportlab.platypus import Table

        assert isinstance(result, Table)

    def test_empty_rows_returns_empty(self):
        _register_fonts()
        styles = _build_styles()
        table_data = {"heading": "Empty", "rows": []}
        result = _make_empty_paradigm_table(table_data, styles)
        assert result == []
