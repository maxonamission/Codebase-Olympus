#!/usr/bin/env python3
"""Generate printable A4 PDF worksheets per grammar knowledge node.

Produces:
- Empty paradigm tables (parsed from data/content/ markdown)
- Translation exercises with writing space (from node items)
- Greek writing practice lines (for GRC nodes)

Usage:
    python scripts/generate_worksheets.py [--knoop-id KNOOP_ID] [--output-dir DIR]

Without --knoop-id, generates worksheets for all grammar nodes that have content.
"""

import argparse
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from gymnasium_classica.graph.loader import load_graph
from gymnasium_classica.models.graph import KnoopType, Node

# --- Constants ---

PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN = 20 * mm
CONTENT_WIDTH = PAGE_WIDTH - 2 * MARGIN

# Font paths (DejaVu Sans supports Latin + Greek + diacritics)
# Search common locations across Linux, macOS, and Windows
_FONT_SEARCH_PATHS = [
    Path("/usr/share/fonts/truetype/dejavu"),  # Linux (Debian/Ubuntu)
    Path("/usr/share/fonts/dejavu-sans-fonts"),  # Linux (Fedora/RHEL)
    Path("/usr/share/fonts/TTF"),  # Linux (Arch)
    Path("/opt/homebrew/share/fonts/dejavu"),  # macOS (Homebrew ARM)
    Path("/usr/local/share/fonts/dejavu"),  # macOS (Homebrew Intel)
    Path("C:/Windows/Fonts"),  # Windows (system fonts)
]


def _find_font(name: str) -> Path | None:
    """Search for a font file across common system font directories."""
    for font_dir in _FONT_SEARCH_PATHS:
        candidate = font_dir / name
        if candidate.exists():
            return candidate
    return None


_FONT_REGULAR = _find_font("DejaVuSans.ttf")
_FONT_BOLD = _find_font("DejaVuSans-Bold.ttf")

FONT_NAME = "DejaVuSans"
FONT_NAME_BOLD = "DejaVuSans-Bold"
_USE_CUSTOM_FONT = _FONT_REGULAR is not None

# Greek writing practice: line height for ruled lines
WRITING_LINE_HEIGHT = 10 * mm
WRITING_LINES_PER_LETTER = 3


def _register_fonts() -> None:
    """Register DejaVu Sans (regular + bold) for Unicode support.

    Falls back to Helvetica (built-in, no Unicode) if DejaVu is not found.
    """
    global FONT_NAME, FONT_NAME_BOLD, _USE_CUSTOM_FONT
    if not _USE_CUSTOM_FONT:
        FONT_NAME = "Helvetica"
        FONT_NAME_BOLD = "Helvetica-Bold"
        return
    if FONT_NAME not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(TTFont(FONT_NAME, str(_FONT_REGULAR)))
    if _FONT_BOLD and FONT_NAME_BOLD not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(TTFont(FONT_NAME_BOLD, str(_FONT_BOLD)))


def _build_styles() -> dict[str, ParagraphStyle]:
    """Build paragraph styles using DejaVu Sans."""
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "WSTitle",
            parent=base["Title"],
            fontName=FONT_NAME_BOLD,
            fontSize=16,
            leading=20,
            spaceAfter=2 * mm,
        ),
        "subtitle": ParagraphStyle(
            "WSSubtitle",
            parent=base["Normal"],
            fontName=FONT_NAME,
            fontSize=9,
            textColor=colors.grey,
            spaceAfter=6 * mm,
        ),
        "heading": ParagraphStyle(
            "WSHeading",
            parent=base["Heading2"],
            fontName=FONT_NAME_BOLD,
            fontSize=12,
            leading=15,
            spaceBefore=6 * mm,
            spaceAfter=3 * mm,
        ),
        "body": ParagraphStyle(
            "WSBody",
            parent=base["Normal"],
            fontName=FONT_NAME,
            fontSize=10,
            leading=13,
        ),
        "exercise": ParagraphStyle(
            "WSExercise",
            parent=base["Normal"],
            fontName=FONT_NAME,
            fontSize=10,
            leading=13,
            spaceBefore=2 * mm,
        ),
        "footer": ParagraphStyle(
            "WSFooter",
            parent=base["Normal"],
            fontName=FONT_NAME,
            fontSize=7,
            textColor=colors.grey,
            alignment=1,  # center
        ),
    }


# --- Markdown parsing ---


def _strip_bold(text: str) -> str:
    """Remove markdown bold markers (**text**)."""
    return re.sub(r"\*\*(.+?)\*\*", r"\1", text)


def parse_markdown_tables(content: str) -> list[dict]:
    """Parse markdown content and extract tables with their preceding heading.

    Returns a list of dicts:
        {"heading": str | None, "rows": list[list[str]]}
    Each row is a list of cell strings (bold markers stripped).
    """
    lines = content.split("\n")
    tables: list[dict] = []
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        # Detect table start: line begins with '|'
        if line.startswith("|") and "|" in line[1:]:
            # Look back for a heading
            heading = None
            for back in range(i - 1, max(i - 5, -1), -1):
                prev = lines[back].strip()
                if prev.startswith("#"):
                    heading = re.sub(r"^#+\s*", "", prev)
                    break
                if prev and not prev.startswith("|"):
                    break

            rows: list[list[str]] = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                row_line = lines[i].strip()
                # Skip separator lines (|---|---|)
                if re.match(r"^\|[\s\-:|]+\|$", row_line):
                    i += 1
                    continue
                cells = [
                    _strip_bold(c.strip())
                    for c in row_line.split("|")[1:-1]  # skip empty first/last
                ]
                rows.append(cells)
                i += 1

            if rows:
                tables.append({"heading": heading, "rows": rows})
        else:
            i += 1

    return tables


def _make_empty_paradigm_table(table_data: dict, styles: dict[str, ParagraphStyle]) -> list:
    """Build a reportlab Table from parsed markdown table data.

    The first row (header) is kept; all other cells are emptied
    so students can fill them in.
    """
    rows = table_data["rows"]
    if not rows:
        return []

    header = rows[0]
    num_cols = len(header)

    # Build table data: header + empty rows (keep first column as row label)
    pdf_rows = [[Paragraph(cell, styles["body"]) for cell in header]]
    for row in rows[1:]:
        pdf_row = []
        for col_idx, cell in enumerate(row):
            if col_idx == 0:
                # Keep row labels (e.g. case names, person numbers)
                pdf_row.append(Paragraph(cell, styles["body"]))
            else:
                # Empty cell for student to fill in
                pdf_row.append("")
        # Pad if row is shorter than header
        while len(pdf_row) < num_cols:
            pdf_row.append("")
        pdf_rows.append(pdf_row)

    # Calculate column widths
    available = CONTENT_WIDTH
    col_width = available / num_cols

    table = Table(pdf_rows, colWidths=[col_width] * num_cols, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, 0), FONT_NAME_BOLD),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("BACKGROUND", (0, 0), (-1, 0), colors.Color(0.9, 0.9, 0.9)),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                # Minimum row height for writing space
                ("ROWHEIGHT", (0, 1), (-1, -1), 10 * mm),
            ]
        )
    )
    return table


def _build_exercise_elements(knoop: Node, styles: dict[str, ParagraphStyle]) -> list:
    """Build exercise elements from the knoop's items."""
    elements = []
    # Filter for suitable exercise items (production, analyse, synthese, offline)
    exercise_items = [
        item
        for item in knoop.items
        if item.type.value
        in ("productie", "analyse", "synthese", "offline_schrijven", "herkenning")
    ]

    if not exercise_items:
        return elements

    elements.append(Paragraph("Oefeningen", styles["heading"]))

    for idx, item in enumerate(exercise_items, 1):
        stimulus = item.stimulus if isinstance(item.stimulus, str) else str(item.stimulus)
        elements.append(Paragraph(f"{idx}. {stimulus}", styles["exercise"]))
        # Add ruled writing lines
        line_table = Table(
            [[""] for _ in range(2)],
            colWidths=[CONTENT_WIDTH],
            rowHeights=[8 * mm] * 2,
        )
        line_table.setStyle(
            TableStyle(
                [
                    ("LINEBELOW", (0, 0), (-1, -1), 0.3, colors.Color(0.7, 0.7, 0.7)),
                    ("TOPPADDING", (0, 0), (-1, -1), 0),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                ]
            )
        )
        elements.append(line_table)
        elements.append(Spacer(1, 2 * mm))

    return elements


def _build_greek_writing_lines(knoop: Node, styles: dict[str, ParagraphStyle]) -> list:
    """Build Greek letter writing practice lines for GRC alphabet nodes."""
    elements = []

    # Only for Greek alphabet nodes (GRC-G-FONL-ALFA-*)
    if not knoop.id.startswith("GRC-G-FONL-ALFA-"):
        return elements

    # Extract the letter info from the description
    beschrijving = knoop.beschrijving
    # Try to extract majuskel/minuskel from description
    # Pattern: "Α (majuskel), α (minuskel)" or similar
    letter_match = re.search(
        r"([Α-Ωα-ω\u0370-\u03FF])\s*\(majuskel\).*?([Α-Ωα-ω\u0370-\u03FF])\s*\(minuskel\)",
        beschrijving,
    )

    if not letter_match:
        return elements

    majuskel = letter_match.group(1)
    minuskel = letter_match.group(2)

    elements.append(Paragraph("Schrijfoefening", styles["heading"]))
    elements.append(
        Paragraph(
            f"Oefen het schrijven van de letter: {majuskel} (hoofdletter) en "
            f"{minuskel} (kleine letter)",
            styles["body"],
        )
    )
    elements.append(Spacer(1, 3 * mm))

    # Generate ruled lines with the letter as example at the start
    for letter, label in [(majuskel, "hoofdletter"), (minuskel, "kleine letter")]:
        elements.append(Paragraph(f"{label}: {letter}", styles["body"]))
        # Create practice rows: first cell has the example, rest is blank
        practice_rows = []
        for _ in range(WRITING_LINES_PER_LETTER):
            practice_rows.append([letter, "", "", "", "", "", "", "", "", ""])

        col_w = CONTENT_WIDTH / 10
        line_table = Table(
            practice_rows,
            colWidths=[col_w] * 10,
            rowHeights=[WRITING_LINE_HEIGHT] * WRITING_LINES_PER_LETTER,
        )
        line_table.setStyle(
            TableStyle(
                [
                    ("FONTNAME", (0, 0), (-1, -1), FONT_NAME),
                    ("FONTSIZE", (0, 0), (-1, -1), 14),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("GRID", (0, 0), (-1, -1), 0.3, colors.Color(0.7, 0.7, 0.7)),
                    ("TEXTCOLOR", (0, 0), (0, -1), colors.Color(0.6, 0.6, 0.6)),
                ]
            )
        )
        elements.append(line_table)
        elements.append(Spacer(1, 3 * mm))

    return elements


def generate_worksheet(
    knoop: Node,
    content_dir: Path,
    output_path: Path,
) -> bool:
    """Generate a single PDF worksheet for a knowledge node.

    Returns True if a PDF was generated, False if skipped (no content).
    """
    _register_fonts()
    styles = _build_styles()

    # Load content markdown if available
    content_text = None
    if knoop.content_ref:
        content_path = content_dir / knoop.content_ref
        if content_path.exists():
            content_text = content_path.read_text(encoding="utf-8")
    else:
        # Try conventional path
        content_path = content_dir / f"{knoop.id}.md"
        if content_path.exists():
            content_text = content_path.read_text(encoding="utf-8")

    # Need either content (for tables) or items (for exercises)
    # or be a Greek alphabet node (for writing lines)
    has_tables = content_text and "|" in content_text
    has_items = bool(knoop.items)
    is_greek_letter = knoop.id.startswith("GRC-G-FONL-ALFA-") and re.search(
        r"\(majuskel\)", knoop.beschrijving or ""
    )

    if not has_tables and not has_items and not is_greek_letter:
        return False

    # Build document
    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN,
        bottomMargin=MARGIN,
        title=f"Werkblad — {knoop.titel_nl}",
        author="Gymnasium Classica",
    )

    elements: list = []

    # Title block
    elements.append(Paragraph(knoop.titel_nl, styles["title"]))
    elements.append(Paragraph(f"Knoop: {knoop.id}", styles["subtitle"]))

    # Description
    if knoop.beschrijving:
        elements.append(Paragraph(knoop.beschrijving, styles["body"]))
        elements.append(Spacer(1, 4 * mm))

    # Paradigm tables (empty for filling in)
    if has_tables:
        tables = parse_markdown_tables(content_text)
        for table_data in tables:
            if table_data["heading"]:
                heading = table_data["heading"]
                # Prefix with "Vul in:" if it's a paradigm table
                if "paradigma" in heading.lower() or len(table_data["rows"]) > 2:
                    heading = f"Vul in: {heading}"
                elements.append(Paragraph(heading, styles["heading"]))
            else:
                elements.append(Paragraph("Vul het paradigma in", styles["heading"]))

            pdf_table = _make_empty_paradigm_table(table_data, styles)
            if pdf_table:
                elements.append(pdf_table)
                elements.append(Spacer(1, 4 * mm))

    # Exercises from items
    elements.extend(_build_exercise_elements(knoop, styles))

    # Greek writing practice
    elements.extend(_build_greek_writing_lines(knoop, styles))

    # Footer
    elements.append(Spacer(1, 6 * mm))
    elements.append(Paragraph("Gymnasium Classica — Werkblad", styles["footer"]))

    doc.build(elements)
    return True


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate printable PDF worksheets for grammar knowledge nodes."
    )
    parser.add_argument(
        "--graph-dir",
        type=Path,
        default=Path("data/graph"),
        help="Directory containing graph JSON files (default: data/graph)",
    )
    parser.add_argument(
        "--content-dir",
        type=Path,
        default=Path("data/content"),
        help="Directory containing content markdown files (default: data/content)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/worksheets"),
        help="Output directory for PDF files (default: data/worksheets)",
    )
    parser.add_argument(
        "--knoop-id",
        type=str,
        default=None,
        help="Generate worksheet for a single knoop ID only",
    )
    args = parser.parse_args()

    # Load graph
    graph = load_graph(args.graph_dir)
    print(f"Loaded graph: {graph.number_of_nodes()} nodes")

    # Select target nodes
    generated = 0
    skipped = 0

    for node_id in sorted(graph.nodes):
        knoop: Node = graph.nodes[node_id]["knoop"]

        # Filter: only grammar nodes
        if knoop.type != KnoopType.G:
            continue

        # Filter: specific knoop if requested
        if args.knoop_id and knoop.id != args.knoop_id:
            continue

        output_path = args.output_dir / f"{knoop.id}.pdf"

        if generate_worksheet(knoop, args.content_dir, output_path):
            generated += 1
            print(f"  [OK] {knoop.id}")
        else:
            skipped += 1

    print(f"\nDone: {generated} worksheets generated, {skipped} skipped (no content).")


if __name__ == "__main__":
    main()
