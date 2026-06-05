#!/usr/bin/env python3
"""Gedeelde story-status-validator (codebase-standards, canoniek format).

Bron van waarheid = de front-matter `status:` van elke story. De map
(`stories/{backlog,todo,doing,done}/`) wordt daar door `sync_story_folders.py`
op gehouden. Deze validator toetst de consistentie:

  C1  map == front-matter `status:`                       (per story)
  C2  `status: done` ⇒ alle acceptatiecriteria afgevinkt   (per story; bewijs-gedekt)
  C3  elke story heeft een EPICS-rij; elke EPICS-storyrij heeft een bestand
  C4  EPICS-statustabel: per-epic `done/total` == filesystem; status-enum geldig;
      een `done`-epic heeft geen open (niet-done) stories; totaalregel klopt
  C5  PROJECTSTATUS epic-tabel: per-epic `done/total` == EPICS == filesystem

**ID-schema-agnostisch.** De epic- en story-ids komen uit de front-matter
(`epic:` / `story_id:`); tabelrijen in EPICS/PROJECTSTATUS worden daartegen
geclassificeerd (lidmaatschap), niet via een vast `E#_S#`-patroon. Zo werkt de
validator zowel voor het canonieke `E#_S#`-schema als voor repo-lokale schema's
(bv. Olympus' `A1-01`, `B4-02`). Een tabel-eerste-cel die eruitziet als een
story-id maar geen bestand heeft, wordt als dead-ref gemeld.

Modi:
  --mode=staged : soft — print issues, exit 0 (pre-commit).
  --mode=full   : strict — exit 1 bij errors (CI).

Alleen stdlib. Python 3.9+.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

STATUSES = ("backlog", "todo", "doing", "done")
EPIC_STATUSES = STATUSES + ("actief",)
AC_HEADERS = ("acceptatiecriteria", "acceptance criteria")
UNCHECKED = re.compile(r"^\s*[-*]\s*\[\s\]", re.MULTILINE)
HEADER = re.compile(r"^#{1,6}\s*(.+?)\s*$", re.MULTILINE)
FM = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
COUNT = re.compile(r"(\d+)\s*/\s*(\d+)")
# Een eerste-cel die eruitziet als een story-id: eindigt op scheidingsteken +
# (optioneel S) + nummer — bv. "E1_S1", "E01-S01", "A1-01", "OS-06".
STORY_SHAPE = re.compile(r"[-_]S?\d+$")
SKIP_PARTS = {".git", "templates", "archief", "archive", "_archief", "node_modules"}


def _skip(path: Path) -> bool:
    return bool(SKIP_PARTS.intersection(path.parts)) or path.name.endswith(".template.md")


def parse_frontmatter(text: str) -> dict[str, str]:
    m = FM.match(text)
    out: dict[str, str] = {}
    if not m:
        return out
    for line in m.group(1).splitlines():
        if ":" in line and not line.lstrip().startswith("#"):
            k, _, v = line.partition(":")
            out[k.strip()] = v.strip().strip("'\"")
    return out


def ac_section(text: str) -> str | None:
    matches = list(HEADER.finditer(text))
    for i, m in enumerate(matches):
        if m.group(1).strip().lower() in AC_HEADERS:
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            return text[m.end():end]
    return None


def find_story_roots(repo_root: Path) -> list[Path]:
    roots: set[Path] = set()
    for d in repo_root.rglob("stories"):
        if d.is_dir() and not _skip(d) and any((d / s).is_dir() for s in STATUSES):
            roots.add(d)
    return sorted(roots)


def table_rows(text: str):
    """Yield gestripte cel-lijsten voor elke markdown-tabelregel."""
    for line in text.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells:
            yield cells


def clean_id(cell: str) -> str:
    """Haal een id-token uit de eerste tabelcel.

    Ondersteunt bare ids ("E1_S1", "A1-01"), Obsidian-wikilinks
    ("[[E01-S01 - Titel]]") en "id + naam"-cellen ("E01 Projectnaam"):
    strip brackets, knip op " - "/" — "-scheiding, neem het eerste woord.
    """
    c = cell.strip().strip("[]").strip()
    c = re.split(r"\s+[-–—]\s+", c)[0].strip()
    parts = c.split()
    return parts[0] if parts else c


def collect_epics(repo_root: Path, epic_ids: set[str], story_ids: set[str]):
    """Parse EPICS*.md data-driven tegen bekende epic-/story-ids.

    Returns (epics, referenced_story_ids, dead_refs) waarbij
    epics[eid] = {status, done, total}.
    """
    epics: dict[str, dict] = {eid: {"status": None, "done": None, "total": None} for eid in epic_ids}
    referenced: set[str] = set()
    dead_refs: set[str] = set()
    for path in repo_root.rglob("EPICS*.md"):
        if _skip(path):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for cells in table_rows(text):
            fid = clean_id(cells[0])
            if fid in epic_ids:
                status = next((c.lower() for c in cells if c.lower() in EPIC_STATUSES), None)
                cnt = next((COUNT.search(c) for c in cells if COUNT.search(c)), None)
                e = epics.setdefault(fid, {"status": None, "done": None, "total": None})
                if status:
                    e["status"] = status
                if cnt:
                    e["done"], e["total"] = int(cnt.group(1)), int(cnt.group(2))
            elif fid in story_ids:
                referenced.add(fid)
            elif STORY_SHAPE.search(fid):
                dead_refs.add(fid)
    return epics, referenced, dead_refs


def collect_projectstatus(repo_root: Path, epic_ids: set[str]) -> dict[str, tuple[int, int]]:
    """PROJECTSTATUS*.md epic-tabel → {epic_id: (done,total)}."""
    out: dict[str, tuple[int, int]] = {}
    for ps in repo_root.rglob("PROJECTSTATUS*.md"):
        if _skip(ps):
            continue
        text = ps.read_text(encoding="utf-8", errors="replace")
        for cells in table_rows(text):
            fid = clean_id(cells[0])
            if fid not in epic_ids:
                continue
            cnt = next((COUNT.search(c) for c in cells if COUNT.search(c)), None)
            if cnt:
                out[fid] = (int(cnt.group(1)), int(cnt.group(2)))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--mode", choices=("staged", "full"), default="full")
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--ac-gate", choices=("error", "warn"), default="error",
                    help="C2 (done⇒AC afgevinkt): hard (error) of zacht (warn) tijdens legacy-opruiming")
    args = ap.parse_args()
    repo_root = Path(args.repo_root).resolve()
    errors: list[str] = []
    warnings: list[str] = []

    roots = find_story_roots(repo_root)
    if not roots:
        print("geen stories/-structuur gevonden — niets te controleren.")
        return 0

    # --- per-story checks (C1, C2) + filesystem-tellingen per epic ---
    fs_counts: dict[str, dict[str, int]] = {}   # epic -> status -> n
    story_ids: set[str] = set()
    epic_ids: set[str] = set()
    for root in roots:
        for status in STATUSES:
            d = root / status
            if not d.is_dir():
                continue
            for story in sorted(d.glob("*.md")):
                if story.name.startswith("_"):
                    continue
                rel = story.relative_to(repo_root)
                text = story.read_text(encoding="utf-8", errors="replace")
                fm = parse_frontmatter(text)
                fm_status = fm.get("status", "").lower()
                sid = fm.get("story_id", story.stem)
                epic = fm.get("epic", "")
                story_ids.add(sid)
                if epic:
                    epic_ids.add(epic)
                # C1: map == front-matter
                if fm_status != status:
                    errors.append(f"{rel}: front-matter status '{fm_status or '—'}' ≠ map '{status}'")
                # C2: done ⇒ alle AC afgevinkt
                if fm_status == "done" or status == "done":
                    sec = ac_section(text)
                    if sec is None:
                        warnings.append(f"{rel}: done zonder acceptatiecriteria-sectie")
                    elif UNCHECKED.search(sec):
                        n = len(UNCHECKED.findall(sec))
                        msg = f"{rel}: done met {n} openstaande acceptatiecriteria"
                        (warnings if args.ac_gate == "warn" else errors).append(msg)
                # tellingen op basis van de bron (front-matter status, anders map)
                eff = fm_status if fm_status in STATUSES else status
                if epic:
                    fs_counts.setdefault(epic, {s: 0 for s in STATUSES})[eff] += 1

    epics, referenced, dead_refs = collect_epics(repo_root, epic_ids, story_ids)
    ps = collect_projectstatus(repo_root, epic_ids)

    # --- C3: orphans / dead-refs ---
    for sid in story_ids:
        if sid not in referenced:
            warnings.append(f"story '{sid}' niet gevonden in een EPICS-tabel")
    for sid in dead_refs:
        warnings.append(f"EPICS noemt story '{sid}' maar er is geen bestand")

    # --- C4: EPICS done/total per epic == filesystem; done-epic geen open stories ---
    for eid, e in sorted(epics.items()):
        fs = fs_counts.get(eid)
        if fs is None:
            continue
        fs_done, fs_total = fs["done"], sum(fs.values())
        if e["done"] is not None and (e["done"], e["total"]) != (fs_done, fs_total):
            errors.append(f"{eid}: EPICS zegt {e['done']}/{e['total']}, filesystem {fs_done}/{fs_total}")
        if e["status"] == "done" and (fs["backlog"] or fs["todo"] or fs["doing"]):
            open_n = fs["backlog"] + fs["todo"] + fs["doing"]
            errors.append(f"{eid}: status 'done' maar {open_n} story('s) nog niet done")
        if e["status"] and e["status"] not in EPIC_STATUSES:
            errors.append(f"{eid}: ongeldige status '{e['status']}'")

    # --- C5: PROJECTSTATUS == EPICS == filesystem ---
    for eid, (psd, pst) in ps.items():
        fs = fs_counts.get(eid)
        if fs is not None:
            fs_done, fs_total = fs["done"], sum(fs.values())
            if (psd, pst) != (fs_done, fs_total):
                errors.append(f"{eid}: PROJECTSTATUS zegt {psd}/{pst}, filesystem {fs_done}/{fs_total}")

    for w in warnings:
        print(f"WAARSCHUWING: {w}")
    for e in errors:
        print(f"FOUT: {e}")
    print(f"\n{len(story_ids)} stories · {len(epics)} epics · {len(errors)} fout(en) · {len(warnings)} waarschuwing(en)")

    return 1 if (args.mode == "full" and errors) else 0


if __name__ == "__main__":
    sys.exit(main())
