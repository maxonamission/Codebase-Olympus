"""Tests voor scripts/check_story_status.py.

Per check één scenario; helpers schrijven story-bestanden in een
``tmp_path``-tree zodat tests volledig hermetisch zijn.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Maak het script importeerbaar.
_SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(_SCRIPTS_DIR))

from check_story_status import (
    check_dead_refs,
    check_done_ac,
    check_orphan,
    check_status_location,
    check_structure,
    parse_epics,
    parse_story,
)


def _write_story(folder: Path, story_id: str, *, ac_lines: list[str], doel: bool = True) -> Path:
    """Schrijf een minimale story-md."""
    folder.mkdir(parents=True, exist_ok=True)
    parts = [f"# Story {story_id}: Test"]
    if doel:
        parts.extend(["", "## Doel", "Iets doen."])
    parts.extend(["", "## Acceptatiecriteria", *ac_lines, ""])
    path = folder / f"{story_id}.md"
    path.write_text("\n".join(parts), encoding="utf-8")
    return path


def _write_epics(root: Path, rows: list[tuple[str, str, str]]) -> Path:
    """Schrijf een EPICS.md met één tabel.

    rows = [(id, titel, status), ...]
    """
    lines = ["# Epics", "", "| Story | Titel | Status |", "|---|---|---|"]
    for sid, title, status in rows:
        lines.append(f"| {sid} | {title} | {status} |")
    path = root / "EPICS.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


# --- parse_story ---


def test_parse_story_extracts_id_title_and_ac(tmp_path: Path) -> None:
    p = _write_story(tmp_path / "done", "OS-99", ac_lines=["- [x] een", "- [ ] twee"])
    story = parse_story(p)
    assert story is not None
    assert story.id == "OS-99"
    assert story.title == "Test"
    assert story.status_from_location == "done"
    assert story.has_doel is True
    assert story.ac_total == 2
    assert story.ac_checked == 1
    assert story.ac_open == 1


def test_parse_story_returns_none_outside_status_folder(tmp_path: Path) -> None:
    p = tmp_path / "scratch" / "X1-01.md"
    p.parent.mkdir()
    p.write_text("# Story X1-01: Test\n## Doel\nx\n## Acceptatiecriteria\n- [ ] x\n")
    assert parse_story(p) is None


# --- parse_epics ---


def test_parse_epics_resolves_aliases(tmp_path: Path) -> None:
    path = _write_epics(
        tmp_path,
        [("OS-01", "Lint", "done"), ("F1-01", "Frontend", "todo"), ("X1-01", "X", "draft")],
    )
    entries = parse_epics(path)
    assert entries["OS-01"].status == "done"
    assert entries["F1-01"].status == "backlog"  # todo alias
    assert entries["X1-01"].status == "backlog"  # draft alias


# --- check 1: structure ---


def test_check_structure_flags_missing_doel_and_ac(tmp_path: Path) -> None:
    p = _write_story(tmp_path / "doing", "OS-99", ac_lines=[], doel=False)
    story = parse_story(p)
    assert story is not None
    result = check_structure(story)
    assert any("Doel" in e for e in result.errors)
    assert any("Acceptatiecriteria" in e for e in result.errors)


def test_check_structure_passes_on_valid_story(tmp_path: Path) -> None:
    p = _write_story(tmp_path / "doing", "OS-99", ac_lines=["- [ ] a"])
    story = parse_story(p)
    assert story is not None
    assert check_structure(story).errors == []


# --- check 2: status-location consistency ---


def test_check_status_location_flags_mismatch(tmp_path: Path) -> None:
    p = _write_story(tmp_path / "done", "OS-99", ac_lines=["- [x] a"])
    story = parse_story(p)
    epics = parse_epics(_write_epics(tmp_path, [("OS-99", "X", "backlog")]))
    assert story is not None
    result = check_status_location(story, epics)
    assert len(result.errors) == 1
    assert "done" in result.errors[0] and "backlog" in result.errors[0]


def test_check_status_location_passes_on_match(tmp_path: Path) -> None:
    p = _write_story(tmp_path / "done", "OS-99", ac_lines=["- [x] a"])
    story = parse_story(p)
    epics = parse_epics(_write_epics(tmp_path, [("OS-99", "X", "done")]))
    assert story is not None
    assert check_status_location(story, epics).errors == []


# --- check 3: done-AC ---


def test_check_done_ac_flags_open_in_done(tmp_path: Path) -> None:
    p = _write_story(tmp_path / "done", "OS-99", ac_lines=["- [x] a", "- [ ] b"])
    story = parse_story(p)
    assert story is not None
    result = check_done_ac(story)
    assert len(result.errors) == 1
    assert "openstaand" in result.errors[0]


def test_check_done_ac_passes_in_backlog(tmp_path: Path) -> None:
    p = _write_story(tmp_path / "backlog", "OS-99", ac_lines=["- [ ] a"])
    story = parse_story(p)
    assert story is not None
    assert check_done_ac(story).errors == []


# --- check 5 + 6: orphan and dead-ref ---


def test_check_orphan_warns_when_no_epics_row(tmp_path: Path) -> None:
    p = _write_story(tmp_path / "doing", "OS-99", ac_lines=["- [ ] a"])
    story = parse_story(p)
    assert story is not None
    result = check_orphan(story, epics={})
    assert len(result.warnings) == 1


def test_check_dead_refs_warns_when_no_file(tmp_path: Path) -> None:
    epics = parse_epics(_write_epics(tmp_path, [("OS-77", "Ghost", "backlog")]))
    result = check_dead_refs(epics, story_ids=set())
    assert len(result.warnings) == 1
    assert "OS-77" in result.warnings[0]


# --- end-to-end ---


def test_run_full_clean_repo(tmp_path: Path) -> None:
    """Een volledig consistent stories/-tree → geen problemen."""
    _write_story(tmp_path / "backlog", "OS-99", ac_lines=["- [ ] a"])
    _write_story(tmp_path / "done", "OS-98", ac_lines=["- [x] a"])
    _write_epics(tmp_path, [("OS-99", "x", "backlog"), ("OS-98", "y", "done")])

    # run_full leest EPICS_PATH; monkeypatch via env-var of monkeypatch is overkill,
    # dus we patchen via module-attributen.
    import check_story_status as mod

    orig_dir, orig_path = mod.STORIES_DIR, mod.EPICS_PATH
    try:
        mod.STORIES_DIR = tmp_path
        mod.EPICS_PATH = tmp_path / "EPICS.md"
        result = mod.run_full(tmp_path)
    finally:
        mod.STORIES_DIR = orig_dir
        mod.EPICS_PATH = orig_path

    assert result.errors == []
    assert result.warnings == []


def test_run_full_catches_done_with_open_ac(tmp_path: Path) -> None:
    _write_story(tmp_path / "done", "OS-99", ac_lines=["- [x] a", "- [ ] b"])
    _write_epics(tmp_path, [("OS-99", "x", "done")])

    import check_story_status as mod

    orig_dir, orig_path = mod.STORIES_DIR, mod.EPICS_PATH
    try:
        mod.STORIES_DIR = tmp_path
        mod.EPICS_PATH = tmp_path / "EPICS.md"
        result = mod.run_full(tmp_path)
    finally:
        mod.STORIES_DIR = orig_dir
        mod.EPICS_PATH = orig_path

    assert any("openstaand" in e for e in result.errors)


@pytest.mark.parametrize(
    "story_id",
    ["OS-01", "A1-01", "E3-18a", "F1-19", "OS-08"],
)
def test_id_pattern_accepts_known_forms(tmp_path: Path, story_id: str) -> None:
    p = _write_story(tmp_path / "done", story_id, ac_lines=["- [x] a"])
    story = parse_story(p)
    assert story is not None
    assert story.id == story_id
