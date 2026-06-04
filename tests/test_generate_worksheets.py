"""Tests for scripts/generate_worksheets.py — PDF worksheet generation."""

# Import the module under test (scripts/ is not a package, so use importlib)
import importlib.util
from pathlib import Path

import pytest

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
def sample_node() -> Node:
    """A minimal grammar node for testing."""
    return Node(
        id="LAT-G-MORF-DECL1-PARAD",
        type=NodeType.G,
        language=Language.LAT,
        title_nl="Paradigma 1e declinatie",
        description="De 1e declinatie met modelwoord puella.",
        bloom_level=BloomLevel.KENNIS,
        phase=Phase.ONDERBOUW_1,
        items=[
            Item(
                id="ITEM-LAT-G-MORF-DECL1-PARAD-001",
                node_ids=["LAT-G-MORF-DECL1-PARAD"],
                type=ItemType.HERKENNING,
                direction=Direction.RECEPTIEF,
                difficulty_initial=-0.5,
                discrimination_initial=1.0,
                expected_time_sec=15,
                stimulus="Geef de genitivus singularis van puella.",
                answer="puellae",
                feedback="De genitivus singularis van de 1e declinatie eindigt op -ae.",
                source=Source.HANDMATIG,
            ),
        ],
    )


@pytest.fixture
def greek_letter_node() -> Node:
    """A Greek alphabet node for testing writing lines."""
    return Node(
        id="GRC-G-FONL-ALFA-ALFA",
        type=NodeType.G,
        language=Language.GRC,
        title_nl="Α α — alfa",
        description="De letter alfa: Α (majuskel), α (minuskel). Klank: kort of lang /a/.",
        bloom_level=BloomLevel.KENNIS,
        phase=Phase.ONDERBOUW_1,
    )


@pytest.fixture
def node_no_content() -> Node:
    """A node with no content and no items."""
    return Node(
        id="LAT-G-MORF-GENUS-INTRO",
        type=NodeType.G,
        language=Language.LAT,
        title_nl="Grammaticaal geslacht",
        description="Introductie van het concept genus.",
        bloom_level=BloomLevel.KENNIS,
        phase=Phase.ONDERBOUW_1,
    )


SAMPLE_MARKDOWN = """\
---
node_id: LAT-G-MORF-DECL1-PARAD
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
    def test_generates_pdf_with_content(self, sample_node, tmp_path):
        """Worksheet with markdown content produces a valid PDF."""
        content_dir = tmp_path / "content"
        content_dir.mkdir()
        (content_dir / "LAT-G-MORF-DECL1-PARAD.md").write_text(SAMPLE_MARKDOWN, encoding="utf-8")

        output = tmp_path / "worksheets" / "LAT-G-MORF-DECL1-PARAD.pdf"
        result = generate_worksheet(sample_node, content_dir, output)

        assert result is True
        assert output.exists()
        # Check valid PDF header
        with open(output, "rb") as f:
            assert f.read(5) == b"%PDF-"

    def test_generates_pdf_with_items_only(self, tmp_path):
        """Knoop with items but no content file still produces a PDF."""
        node = Node(
            id="LAT-G-SYNT-WRDVLG",
            type=NodeType.G,
            language=Language.LAT,
            title_nl="Woordvolgorde",
            description="Latijnse woordvolgorde is vrij.",
            bloom_level=BloomLevel.BEGRIP,
            phase=Phase.ONDERBOUW_1,
            items=[
                Item(
                    id="ITEM-LAT-G-SYNT-WRDVLG-001",
                    node_ids=["LAT-G-SYNT-WRDVLG"],
                    type=ItemType.PRODUCTIE,
                    direction=Direction.PRODUCTIEF,
                    difficulty_initial=0.0,
                    discrimination_initial=1.0,
                    expected_time_sec=30,
                    stimulus="Vertaal: Het meisje ziet de heer.",
                    answer="Puella dominum videt.",
                    feedback="SOV is de gangbare volgorde.",
                    source=Source.HANDMATIG,
                ),
            ],
        )
        content_dir = tmp_path / "content"
        content_dir.mkdir()
        output = tmp_path / "out" / "LAT-G-SYNT-WRDVLG.pdf"
        result = generate_worksheet(node, content_dir, output)

        assert result is True
        assert output.exists()

    def test_skips_node_without_content_or_items(self, node_no_content, tmp_path):
        """Knoop with no content and no items is skipped."""
        content_dir = tmp_path / "content"
        content_dir.mkdir()
        output = tmp_path / "out" / "test.pdf"
        result = generate_worksheet(node_no_content, content_dir, output)

        assert result is False
        assert not output.exists()

    def test_greek_writing_lines(self, greek_letter_node, tmp_path):
        """Greek alphabet node produces a PDF with writing practice."""
        content_dir = tmp_path / "content"
        content_dir.mkdir()
        output = tmp_path / "worksheets" / "GRC-G-FONL-ALFA-ALFA.pdf"
        result = generate_worksheet(greek_letter_node, content_dir, output)

        assert result is True
        assert output.exists()
        # File should be a valid PDF of reasonable size
        size = output.stat().st_size
        assert size > 1000  # non-trivial PDF

    def test_output_dir_created(self, sample_node, tmp_path):
        """Output directory is created automatically if it doesn't exist."""
        content_dir = tmp_path / "content"
        content_dir.mkdir()
        (content_dir / "LAT-G-MORF-DECL1-PARAD.md").write_text(SAMPLE_MARKDOWN, encoding="utf-8")

        output = tmp_path / "deep" / "nested" / "dir" / "test.pdf"
        result = generate_worksheet(sample_node, content_dir, output)

        assert result is True
        assert output.exists()

    def test_content_ref_used(self, tmp_path):
        """When node has content_ref, that file is loaded."""
        node = Node(
            id="LAT-G-MORF-DECL1-PARAD",
            type=NodeType.G,
            language=Language.LAT,
            title_nl="1e declinatie paradigma",
            description="Paradigma.",
            bloom_level=BloomLevel.KENNIS,
            phase=Phase.ONDERBOUW_1,
            content_ref="LAT-G-MORF-DECL1-PARAD.md",
        )

        content_dir = tmp_path / "content"
        content_dir.mkdir()
        (content_dir / "LAT-G-MORF-DECL1-PARAD.md").write_text(SAMPLE_MARKDOWN, encoding="utf-8")

        output = tmp_path / "out" / "test.pdf"
        result = generate_worksheet(node, content_dir, output)
        assert result is True
        assert output.exists()


# --- Tests: _build_exercise_elements ---


class TestBuildExerciseElements:
    def test_returns_elements_for_items(self, sample_node):
        _register_fonts()
        styles = _build_styles()
        elements = _build_exercise_elements(sample_node, styles)
        # Should contain heading + exercise + line table + spacer
        assert len(elements) >= 3

    def test_empty_for_no_items(self, node_no_content):
        _register_fonts()
        styles = _build_styles()
        elements = _build_exercise_elements(node_no_content, styles)
        assert elements == []


# --- Tests: _build_greek_writing_lines ---


class TestBuildGreekWritingLines:
    def test_returns_elements_for_greek_letter(self, greek_letter_node):
        _register_fonts()
        styles = _build_styles()
        elements = _build_greek_writing_lines(greek_letter_node, styles)
        # Should have heading + instructions + spacer + label + table + spacer (x2 for maj/min)
        assert len(elements) >= 5

    def test_empty_for_non_greek_node(self, sample_node):
        _register_fonts()
        styles = _build_styles()
        elements = _build_greek_writing_lines(sample_node, styles)
        assert elements == []

    def test_empty_for_non_letter_greek_node(self):
        """Greek group nodes (not individual letters) should not get writing lines."""
        _register_fonts()
        styles = _build_styles()
        node = Node(
            id="GRC-G-FONL-ALFA-GRP1",
            type=NodeType.G,
            language=Language.GRC,
            title_nl="Groep 1: identieke letters",
            description="Letters die identiek zijn aan het Latijnse alfabet.",
            bloom_level=BloomLevel.KENNIS,
            phase=Phase.ONDERBOUW_1,
        )
        elements = _build_greek_writing_lines(node, styles)
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
