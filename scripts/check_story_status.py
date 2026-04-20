"""Validatie van story-status en acceptatiecriteria.

Controleert dat de stories/-map intern consistent is en dat acceptatiecriteria
in done-stories afgevinkt zijn. Draait in twee modi:

* ``--mode=staged`` — alleen wijzigingen in de staged-set; gebruikt door
  pre-commit. Soft mode: rapporteert problemen maar blokkeert alleen
  duidelijke fouten.
* ``--mode=full`` — hele ``stories/``-map + cross-check tegen
  ``EPICS.md``. Gebruikt door CI. Strict: elke fout blokkeert.

Returncodes:

* 0 — alles ok
* 1 — waarschuwingen (alleen staged-mode)
* 2 — harde fouten

Zie ``stories/done/OS-06.md`` voor de zes checks die dit script implementeert.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
STORIES_DIR = REPO_ROOT / "stories"
EPICS_PATH = STORIES_DIR / "EPICS.md"

VALID_STATUSES = {"backlog", "doing", "done"}
# In EPICS.md tolereren we aliassen voor backlog (legacy / synoniemen).
EPICS_ALIASES = {"draft": "backlog", "todo": "backlog"}

# Regex voor de titel-regel van een storybestand.
# ID-patroon: zelfde als EPICS_ROW_RE — letters + optioneel cijfer + dash + cijfers
# + optionele kleine letter (bv. E3-18a).
TITLE_RE = re.compile(r"^#\s+Story\s+([A-Z]+\d?-\d{1,2}[a-z]?):\s*(.+?)\s*$")

# Regex voor checkbox-items in de AC-sectie.
CHECKBOX_RE = re.compile(r"^\s*-\s*\[([ xX])\]\s+")

# Regex voor de Doel-sectie-header.
DOEL_RE = re.compile(r"^##\s+Doel\b", re.IGNORECASE)
AC_RE = re.compile(r"^##\s+Acceptatiecriteria\b", re.IGNORECASE)

# Regex voor story-rijen in EPICS.md tabellen.
# Voorbeelden: | OS-01 | titel | 1 | — | done |   en   | A1-01 | titel | 6 | done |
# Het ID-patroon ondersteunt twee vormen:
#   - Letter(s) + cijfer + dash + cijfer(s) + optionele letter   (A1-01, E3-18a, F1-19)
#   - Letter(s) + dash + cijfer(s) + optionele letter            (OS-01, OS-18a)
EPICS_ROW_RE = re.compile(
    r"^\|\s*([A-Z]+\d?-\d{1,2}[a-z]?)\s*\|"
    r"\s*([^|]+?)\s*\|"
    r"(?:[^|]*\|){0,3}"
    r"\s*(backlog|doing|done|draft|todo)\s*\|",
    re.IGNORECASE,
)


@dataclass
class Story:
    """Een storybestand op disk."""

    id: str
    title: str
    path: Path
    status_from_location: str  # backlog/doing/done
    has_doel: bool
    ac_total: int
    ac_checked: int

    @property
    def ac_open(self) -> int:
        return self.ac_total - self.ac_checked


@dataclass
class EpicEntry:
    """Een story-rij in EPICS.md."""

    story_id: str
    title: str
    status: str  # backlog/doing/done (na alias-resolutie)
    line_number: int


@dataclass
class CheckResult:
    """Resultaat van één check-functie."""

    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def _display_path(path: Path) -> str:
    """Pad relatief tot REPO_ROOT, of absoluut als dat niet kan (bv. in tests)."""
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


# --- Parsers ---


def parse_story(path: Path) -> Story | None:
    """Parse één storybestand. Returns None bij onleesbaar bestand."""
    if not path.is_file() or path.suffix != ".md":
        return None

    status_from_location = path.parent.name
    if status_from_location not in VALID_STATUSES:
        return None  # bestand zit niet in een status-map

    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    title_match = TITLE_RE.match(lines[0]) if lines else None
    if title_match is None:
        # Kan niet parsen zonder titel; gebruik filename als fallback.
        story_id = path.stem
        title = ""
    else:
        story_id = title_match.group(1)
        title = title_match.group(2)

    # Loop door secties: Doel, Acceptatiecriteria.
    has_doel = False
    in_ac_section = False
    ac_total = 0
    ac_checked = 0

    for line in lines:
        if DOEL_RE.match(line):
            has_doel = True
            in_ac_section = False
            continue
        if AC_RE.match(line):
            in_ac_section = True
            continue
        # Een nieuwe ##-header sluit de AC-sectie.
        if in_ac_section and line.startswith("## "):
            in_ac_section = False
            continue
        if in_ac_section:
            cb = CHECKBOX_RE.match(line)
            if cb:
                ac_total += 1
                if cb.group(1).lower() == "x":
                    ac_checked += 1

    return Story(
        id=story_id,
        title=title,
        path=path,
        status_from_location=status_from_location,
        has_doel=has_doel,
        ac_total=ac_total,
        ac_checked=ac_checked,
    )


def parse_epics(path: Path) -> dict[str, EpicEntry]:
    """Parse EPICS.md. Returns dict story_id -> EpicEntry."""
    entries: dict[str, EpicEntry] = {}
    if not path.is_file():
        return entries

    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        match = EPICS_ROW_RE.match(line)
        if not match:
            continue
        story_id = match.group(1).upper()
        title = match.group(2).strip()
        status = match.group(3).lower()
        status = EPICS_ALIASES.get(status, status)
        entries[story_id] = EpicEntry(
            story_id=story_id,
            title=title,
            status=status,
            line_number=line_no,
        )
    return entries


def discover_stories(root: Path) -> list[Story]:
    """Scan stories/{backlog,doing,done}/*.md en parse alles."""
    found: list[Story] = []
    for status in VALID_STATUSES:
        folder = root / status
        if not folder.is_dir():
            continue
        for md_path in sorted(folder.glob("*.md")):
            story = parse_story(md_path)
            if story is not None:
                found.append(story)
    return found


def staged_story_paths() -> list[Path]:
    """Vraag git om de gestageerde storybestanden onder stories/."""
    try:
        result = subprocess.run(
            # ACMR = Added, Copied, Modified, Renamed.
            # Met name R is belangrijk: een story van backlog/ naar done/
            # verplaatsen telt git als rename, niet als modify.
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
            capture_output=True,
            text=True,
            check=True,
            cwd=REPO_ROOT,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []

    paths: list[Path] = []
    for raw in result.stdout.splitlines():
        path = REPO_ROOT / raw
        try:
            path.relative_to(STORIES_DIR)
        except ValueError:
            continue
        if path.suffix == ".md" and path.name != "EPICS.md":
            paths.append(path)
    return paths


# --- Checks ---


def check_structure(story: Story) -> CheckResult:
    """Check 1: titel + Doel + AC-sectie met >= 1 item."""
    result = CheckResult()
    rel = _display_path(story.path)

    if not story.title:
        result.errors.append(
            f"{rel}: titel-regel ontbreekt of matcht niet '# Story <ID>: <titel>'"
        )

    if story.title and story.id.upper() != story.path.stem.upper():
        result.errors.append(
            f"{rel}: titel-ID '{story.id}' matcht niet bestandsnaam '{story.path.stem}'"
        )

    if not story.has_doel:
        result.errors.append(f"{rel}: '## Doel'-sectie ontbreekt")

    if story.ac_total == 0:
        result.errors.append(
            f"{rel}: '## Acceptatiecriteria'-sectie ontbreekt of bevat geen checkboxes"
        )

    return result


def check_done_ac(story: Story) -> CheckResult:
    """Check 3: een story in done/ heeft alle AC afgevinkt."""
    result = CheckResult()
    if story.status_from_location != "done":
        return result
    if story.ac_open > 0:
        rel = _display_path(story.path)
        result.errors.append(
            f"{rel}: staat in done/ maar heeft {story.ac_open} openstaand(e) "
            f"acceptatiecriterium/criteria (van {story.ac_total} totaal)"
        )
    return result


def check_status_location(story: Story, epics: dict[str, EpicEntry]) -> CheckResult:
    """Check 2: locatie van bestand komt overeen met status in EPICS.md."""
    result = CheckResult()
    rel = _display_path(story.path)
    epic_entry = epics.get(story.id.upper())
    if epic_entry is None:
        # Zit aparte check voor: orphans. Hier alleen de match-check.
        return result
    if epic_entry.status != story.status_from_location:
        result.errors.append(
            f"{rel}: locatie zegt '{story.status_from_location}', "
            f"EPICS.md regel {epic_entry.line_number} zegt '{epic_entry.status}'"
        )
    return result


def check_orphan(story: Story, epics: dict[str, EpicEntry]) -> CheckResult:
    """Check 5: elke story op disk staat in EPICS.md."""
    result = CheckResult()
    if story.id.upper() not in epics:
        rel = _display_path(story.path)
        result.warnings.append(f"{rel}: story-ID '{story.id}' niet gevonden in EPICS.md (orphan)")
    return result


def check_dead_refs(epics: dict[str, EpicEntry], story_ids: set[str]) -> CheckResult:
    """Check 6: elke story-rij in EPICS.md heeft een bestand op disk."""
    result = CheckResult()
    for entry in epics.values():
        if entry.story_id.upper() not in story_ids:
            result.warnings.append(
                f"EPICS.md regel {entry.line_number}: story '{entry.story_id}' "
                f"heeft geen bestand in stories/{{backlog,doing,done}}/"
            )
    return result


# --- Mode dispatchers ---


def run_full(root: Path) -> CheckResult:
    """Volledige check: alle stories + cross-references."""
    combined = CheckResult()
    epics = parse_epics(EPICS_PATH)
    stories = discover_stories(root)
    story_ids = {s.id.upper() for s in stories}

    for story in stories:
        for check in (check_structure, check_done_ac):
            r = check(story)
            combined.errors.extend(r.errors)
            combined.warnings.extend(r.warnings)
        for cross in (check_status_location, check_orphan):
            r = cross(story, epics)
            combined.errors.extend(r.errors)
            combined.warnings.extend(r.warnings)

    dead = check_dead_refs(epics, story_ids)
    combined.errors.extend(dead.errors)
    combined.warnings.extend(dead.warnings)

    return combined


def run_staged() -> CheckResult:
    """Alleen gestageerde storybestanden + lichte cross-check."""
    combined = CheckResult()
    epics = parse_epics(EPICS_PATH)
    paths = staged_story_paths()
    if not paths:
        return combined

    for path in paths:
        story = parse_story(path)
        if story is None:
            continue
        for check in (check_structure, check_done_ac):
            r = check(story)
            combined.errors.extend(r.errors)
            combined.warnings.extend(r.warnings)
        cross = check_status_location(story, epics)
        combined.errors.extend(cross.errors)
        combined.warnings.extend(cross.warnings)

    return combined


# --- CLI ---


def _print_report(result: CheckResult, label: str) -> None:
    if not result.errors and not result.warnings:
        print(f"✓ {label}: geen problemen.")
        return
    if result.errors:
        print(f"✗ {label}: {len(result.errors)} fout(en):")
        for err in result.errors:
            print(f"  - {err}")
    if result.warnings:
        print(f"! {label}: {len(result.warnings)} waarschuwing(en):")
        for warn in result.warnings:
            print(f"  - {warn}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mode",
        choices=("staged", "full"),
        default="full",
        help="staged: alleen gestageerde wijzigingen (pre-commit). full: hele stories/-map (CI).",
    )
    args = parser.parse_args()

    if args.mode == "staged":
        result = run_staged()
        _print_report(result, "stories (staged)")
        if result.errors:
            return 1
        return 0

    result = run_full(STORIES_DIR)
    _print_report(result, "stories (full)")
    if result.errors:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
