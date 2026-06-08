#!/usr/bin/env python3
"""Regenerator: leid story-tellingen af uit het filesystem en werk de
auto-afgeleide cellen in EPICS*.md + PROJECTSTATUS*.md bij.

Analoog aan Atlas' `regenerate_project_status.py`, maar voor het canonieke
markdown-format van codebase-standards (geen centrale status-YAML — de
tellingen leven in de tabellen zelf).

Auto-afgeleid (overschreven):
  - EPICS-statustabel: de `Stories (done/total)`-cel per epic-rij.
  - EPICS-totaalregel: `**Totaal:** E epic(s), S story/stories
    (D done, I doing, T todo, B backlog).`
  - PROJECTSTATUS epic-tabel: de `done/total`-cel per epic-rij.
  - PROJECTSTATUS-dashboard: het `N/T done`-segment.

Narratieve velden (epic-naam, prio, status, toelichting, samenvatting) blijven
handmatig — die raakt de regenerator niet aan.

Bron van waarheid voor de tellingen = de story-bestanden (front-matter `status:`,
fallback de map), identiek aan `check_story_status.py`. De regenerator beslist
géén status; hij telt alleen en schrijft die tellingen terug.

Modi:
  (default) : schrijf de bijgewerkte bestanden.
  --check   : schrijf niets; exit 1 als regeneratie drift toont (CI/pre-commit).

Alleen stdlib. Python 3.9+.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Hergebruik de parsers/constanten uit de bestaande validator: één bron voor
# "wat is een story-root" en "hoe lees ik front-matter".
sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_story_status import (  # noqa: E402
    ALL_STATUSES,
    CANCELLED,
    STATUSES,
    _skip,
    clean_id,
    find_story_roots,
    parse_frontmatter,
)

# Een tabel-cel die volledig een telling is, bv. "3/8".
COUNT_CELL = re.compile(r"^\d+\s*/\s*\d+$")
TOTAAL_LINE = re.compile(r"^\*\*Totaal:\*\*.*$", re.MULTILINE)
# Het "N/T done"-segment in de dashboard-cel.
DASH_DONE = re.compile(r"\d+\s*/\s*\d+\s+done")


def collect_fs_counts(repo_root: Path) -> tuple[dict[str, dict[str, int]], dict[str, int]]:
    """Tel stories per epic en globaal, op basis van front-matter status (fallback map).

    Returns (per_epic, totals) waarbij per_epic[epic][status] = n en
    totals[status] = n over alle stories.
    """
    per_epic: dict[str, dict[str, int]] = {}
    totals: dict[str, int] = {s: 0 for s in ALL_STATUSES}
    for root in find_story_roots(repo_root):
        for status in ALL_STATUSES:
            d = root / status
            if not d.is_dir():
                continue
            for story in sorted(d.glob("*.md")):
                if story.name.startswith("_"):
                    continue
                fm = parse_frontmatter(story.read_text(encoding="utf-8", errors="replace"))
                fm_status = fm.get("status", "").lower()
                eff = fm_status if fm_status in ALL_STATUSES else status
                epic = fm.get("epic", "")
                if epic:
                    per_epic.setdefault(epic, {s: 0 for s in ALL_STATUSES})[eff] += 1
                totals[eff] += 1
    return per_epic, totals


def _replace_count_cell(line: str, new_cell: str) -> str:
    """Vervang in een tabel-regel de eerste cel die een telling is door new_cell.

    Behoudt de oorspronkelijke spatiëring (in-place substitutie binnen de pipes),
    zodat de diff minimaal blijft.
    """
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    for c in cells:
        if COUNT_CELL.match(c) and c != new_cell:
            return re.sub(
                r"(\|\s*)" + re.escape(c) + r"(\s*\|)",
                lambda m: m.group(1) + new_cell + m.group(2),
                line,
                count=1,
            )
    return line


def _make_totaal(n_epics: int, totals: dict[str, int]) -> str:
    total = sum(totals[s] for s in STATUSES)  # cancelled telt niet mee in het totaal
    epic_w = "epic" if n_epics == 1 else "epics"
    story_w = "story" if total == 1 else "stories"
    canc = f" + {totals[CANCELLED]} cancelled" if totals.get(CANCELLED) else ""
    return (
        f"**Totaal:** {n_epics} {epic_w}, {total} {story_w} "
        f"({totals['done']} done, {totals['doing']} doing, "
        f"{totals['todo']} todo, {totals['backlog']} backlog){canc}."
    )


def _epic_id(line: str, epic_ids: set[str]) -> str | None:
    """Eerste-cel-id van een tabelrij als die een bekende epic-id is (data-driven)."""
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if not (cells and line.lstrip().startswith("|")):
        return None
    fid = clean_id(cells[0])
    return fid if fid in epic_ids else None


def regenerate_epics(text: str, per_epic: dict[str, dict[str, int]], totals: dict[str, int]) -> str:
    """Werk een EPICS*.md-tekst bij: per-epic count-cellen + totaalregel."""
    epic_ids = set(per_epic)
    lines = text.splitlines(keepends=True)
    n_epics = sum(1 for line in lines if _epic_id(line, epic_ids) is not None)
    out: list[str] = []
    for line in lines:
        eol = "\n" if line.endswith("\n") else ""
        body = line[: -len(eol)] if eol else line
        eid = _epic_id(body, epic_ids)
        if eid is not None and eid in per_epic:
            fs = per_epic[eid]
            body = _replace_count_cell(body, f"{fs['done']}/{sum(fs[s] for s in STATUSES)}")
        out.append(body + eol)
    new = "".join(out)
    if n_epics:
        new = TOTAAL_LINE.sub(lambda m: _make_totaal(n_epics, totals), new, count=1)
    return new


def regenerate_projectstatus(
    text: str, per_epic: dict[str, dict[str, int]], totals: dict[str, int]
) -> str:
    """Werk een PROJECTSTATUS*.md-tekst bij: epic-tabel count-cellen + dashboard."""
    epic_ids = set(per_epic)
    lines = text.splitlines(keepends=True)
    out: list[str] = []
    for line in lines:
        eol = "\n" if line.endswith("\n") else ""
        body = line[: -len(eol)] if eol else line
        eid = _epic_id(body, epic_ids)
        if eid is not None and eid in per_epic:
            fs = per_epic[eid]
            body = _replace_count_cell(body, f"{fs['done']}/{sum(fs[s] for s in STATUSES)}")
        out.append(body + eol)
    new = "".join(out)
    done, total = totals["done"], sum(totals[s] for s in STATUSES)
    new = DASH_DONE.sub(f"{done}/{total} done", new, count=1)
    return new


def process(repo_root: Path, check: bool) -> tuple[bool, list[str]]:
    """Regenereer alle EPICS/PROJECTSTATUS-bestanden. Returns (drift, gewijzigde paden)."""
    per_epic, totals = collect_fs_counts(repo_root)
    changed: list[str] = []

    targets: list[tuple[Path, str]] = []
    for path in repo_root.rglob("EPICS*.md"):
        if not _skip(path):
            targets.append((path, "epics"))
    for path in repo_root.rglob("PROJECTSTATUS*.md"):
        if not _skip(path):
            targets.append((path, "ps"))

    for path, kind in sorted(targets):
        text = path.read_text(encoding="utf-8", errors="replace")
        new = (
            regenerate_epics(text, per_epic, totals)
            if kind == "epics"
            else regenerate_projectstatus(text, per_epic, totals)
        )
        if new != text:
            changed.append(str(path.relative_to(repo_root)))
            if not check:
                path.write_text(new, encoding="utf-8")
    return bool(changed), changed


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="schrijf niets; exit 1 bij drift (CI/pre-commit)")
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()
    repo_root = Path(args.repo_root).resolve()

    drift, changed = process(repo_root, check=args.check)

    if args.check:
        if drift:
            sys.stderr.write("regenerate_status: drift gedetecteerd in:\n")
            for c in changed:
                sys.stderr.write(f"  - {c}\n")
            sys.stderr.write("Draai `python scripts/regenerate_status.py` om bij te werken.\n")
            return 1
        if not args.quiet:
            print("regenerate_status: geen drift.")
        return 0

    if changed:
        for c in changed:
            print(f"regenerate_status: bijgewerkt {c}")
    elif not args.quiet:
        print("regenerate_status: geen wijzigingen.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
