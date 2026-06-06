#!/usr/bin/env python3
"""Cross-branch detectie van epic-/story-id-collisions (codebase-standards).

Beantwoordt: "claimt een andere actieve `claude/*`-branch hetzelfde `E#`-nummer
voor een ander epic dan ik — of werkt die parallel aan dezelfde story?"

Achtergrond: epic-nummers worden uitgedeeld vanuit `origin/main`. Twee branches
die parallel een nieuwe epic openen of dezelfde story oppakken claimen onafhankelijk
hetzelfde nummer — pas zichtbaar bij merge (precedent: de OS-11/E2_S3-merge-conflict
op Olympus, jun 2026). Dit script geeft een vroeg signaal vóór PR.

**ID-schema-agnostisch.** Gepromoveerd uit Atlas (`_scripts/check_epic_collisions.py`)
en generiek gemaakt: EPICS-bestanden en story-prefixen worden automatisch ontdekt, dus
het werkt voor elke `<PREFIX>_E#_S#`-repo (MH/VX/OL/CS, …) zonder per-repo-config.

**Geen CI-gate.** Exit altijd 0; output is markdown, bedoeld als handmatige preflight
bij sessiestart en vóór epic-creatie/oppakken van een story. Reden: het vergt alle
remote-branches (`--fetch`) en de juiste resolutie (hernoemen vs. mergen) is een
menselijke afweging, geen mechanische blokkade.

Gebruik:
    python scripts/check_epic_collisions.py --fetch            # epic-collisions
    python scripts/check_epic_collisions.py --fetch --stories  # + story-collisions

Alleen stdlib. Python 3.9+.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MAIN_REF = "origin/main"
BRANCH_PREFIX = "claude/"
SKIP_DIR_PARTS = {"templates", "archief", "archive", "_archief", "node_modules", ".git"}

# Epic-rij in een statustabel: `| E20 | naam | ... |`.
RE_EPIC_ROW = re.compile(r"^\|\s*(E\d+[a-z]?)\s*\|\s*([^|]+?)\s*\|")
# Story-bestandsnaam: <PREFIX>_E#_S#[suffix].md. Suffix vrij: `_slug`, ` - Titel`,
# of niets — dekt OL_E1_S1.md, VX_E3_S1_slug.md, MH_E10_S8 - Titel.md, CS_E2_S7_slug.md.
RE_STORY_FILE = re.compile(
    r"^(?P<prefix>[A-Z]{2,})_E(?P<epic>\d+)_S(?P<story>\d+)(?:[ _-].*)?\.md$"
)
RE_STORY_STATUS_DIR = re.compile(r"(?:^|/)stories/(?P<status>doing|done)/[^/]+$")
RE_EPICS_FILE = re.compile(r"(?:^|/)EPICS[^/]*\.md$")


def run(args: list[str]) -> str:
    """Run git, return stdout ('' on non-zero exit)."""
    res = subprocess.run(args, cwd=REPO_ROOT, capture_output=True, text=True)
    return res.stdout if res.returncode == 0 else ""


def list_branches() -> list[str]:
    out = run(["git", "for-each-ref", "--format=%(refname:short)", "refs/remotes/origin/"])
    refs = [b.strip() for b in out.splitlines() if b.strip()]
    return sorted(r for r in refs if r == MAIN_REF or r.startswith(f"origin/{BRANCH_PREFIX}"))


def epics_files_at_ref(branch: str) -> list[str]:
    """Alle EPICS*.md-paden op een branch (skip templates/archief)."""
    out = run(["git", "ls-tree", "-r", "--name-only", branch])
    files = []
    for line in out.splitlines():
        p = line.strip()
        if RE_EPICS_FILE.search(p) and not SKIP_DIR_PARTS.intersection(Path(p).parts):
            files.append(p)
    return files


def parse_epics_at_ref(branch: str, file_path: str) -> dict[str, str]:
    """`{epic_id: epic_name}` uit de statustabel van `<branch>:<file_path>`."""
    blob = run(["git", "show", f"{branch}:{file_path}"])
    if not blob:
        return {}
    epics: dict[str, str] = {}
    in_table = False
    for line in blob.splitlines():
        s = line.strip()
        if not in_table:
            if s.startswith("|") and "Epic" in s and "Status" in s and "Stories" in s:
                in_table = True
            continue
        if not s.startswith("|"):
            break
        if set(s) <= {"|", "-", " ", ":"}:
            continue
        m = RE_EPIC_ROW.match(s)
        if m:
            epics[m.group(1)] = m.group(2).strip()
    return epics


def collect_all_epics(branches: list[str]) -> dict[tuple[str, str], dict[str, str]]:
    """`{(epics_path, epic_id): {branch: epic_name}}` over alle branches."""
    result: dict[tuple[str, str], dict[str, str]] = defaultdict(dict)
    for branch in branches:
        for path in epics_files_at_ref(branch):
            for epic_id, name in parse_epics_at_ref(branch, path).items():
                result[(path, epic_id)][branch] = name
    return result


def find_epic_collisions(
    all_epics: dict[tuple[str, str], dict[str, str]],
) -> list[tuple[str, str, dict[str, str]]]:
    """Collision = zelfde `(epics_path, epic_id)` met >1 unieke epic-naam over branches."""
    out = []
    for (path, epic_id), branch_to_name in all_epics.items():
        if len({n.casefold() for n in branch_to_name.values()}) > 1:
            out.append((path, epic_id, branch_to_name))
    return sorted(out)


def parse_stories_at_ref(branch: str) -> dict[tuple[str, str, str], str]:
    """`{(prefix, E#, S#): status}` voor stories in `stories/{doing,done}/`."""
    out = run(["git", "ls-tree", "-r", "--name-only", branch])
    found: dict[tuple[str, str, str], str] = {}
    for line in out.splitlines():
        path = line.strip()
        sm = RE_STORY_STATUS_DIR.search(path)
        if not sm:
            continue
        fm = RE_STORY_FILE.match(path.rsplit("/", 1)[-1])
        if not fm:
            continue
        key = (fm["prefix"], f"E{fm['epic']}", f"S{fm['story']}")
        if found.get(key) != "done":  # done = sterkste signaal
            found[key] = sm["status"]
    return found


def collect_all_stories(branches: list[str]) -> dict[tuple[str, str, str], dict[str, str]]:
    result: dict[tuple[str, str, str], dict[str, str]] = defaultdict(dict)
    for branch in branches:
        for key, status in parse_stories_at_ref(branch).items():
            result[key][branch] = status
    return result


def find_story_collisions(
    all_stories: dict[tuple[str, str, str], dict[str, str]],
) -> list[tuple[str, str, str, dict[str, str]]]:
    """Collision = zelfde story op >1 `claude/*`-branch in doing/done, en op main
    nog niet `done` (anders gedeelde baseline)."""
    out = []
    for (prefix, epic, story), b2s in all_stories.items():
        if b2s.get(MAIN_REF) == "done":
            continue
        claude = {b: s for b, s in b2s.items() if b != MAIN_REF}
        if len(claude) > 1:
            out.append((prefix, epic, story, claude))
    return sorted(out)


def render(branches, epic_collisions, story_collisions=None) -> str:
    L = ["# Epic-collision-rapport (cross-branch)", "",
         f"**Branches gescand:** {len(branches)} (`origin/main` + `origin/claude/*`)", ""]
    if not epic_collisions:
        L.append("**Geen epic-collisions.** Elk `E#` is over alle branches consistent gebruikt.")
    else:
        L.append(f"**{len(epic_collisions)} epic-collision(s)** — zelfde `E#` claimt "
                 "verschillende namen op verschillende branches:")
        L.append("")
        for path, epic_id, b2n in epic_collisions:
            L += [f"## `{epic_id}` in `{path}`", "", "| Branch | Epic-naam |", "|---|---|"]
            L += [f"| `{b}` | {b2n[b]} |" for b in sorted(b2n)] + [""]
        L += ["**Resolution:** de tweede-mergende branch hernoemt naar het volgende vrije "
              "`E#` op `origin/main` (met erratum-blok + cross-references).", ""]
    if story_collisions is not None:
        L += ["", "---", "", "## Story-collisions", ""]
        if not story_collisions:
            L.append("**Geen story-collisions.** Geen `<PREFIX>_E#_S#` op >1 `claude/*`-branch "
                     "tegelijk in `doing/`/`done/`.")
        else:
            L.append(f"**{len(story_collisions)} story-collision(s)** — mogelijk parallel-werk; "
                     "check vóór verdere mutatie:")
            L.append("")
            for prefix, epic, story, b2s in story_collisions:
                L += [f"### `{prefix}_{epic}_{story}`", "", "| Branch | Status |", "|---|---|"]
                L += [f"| `{b}` | `{b2s[b]}` |" for b in sorted(b2s)] + [""]
    return "\n".join(L) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--fetch", action="store_true", help="Eerst `git fetch --all --prune`.")
    ap.add_argument("--stories", action="store_true", help="Tevens story-collisions rapporteren.")
    args = ap.parse_args()
    if args.fetch:
        run(["git", "fetch", "--all", "--prune"])
    branches = list_branches()
    if not branches:
        print("Geen origin/-branches gevonden. Draai eerst `git fetch --all` of gebruik --fetch.",
              file=sys.stderr)
        return 0
    epic_collisions = find_epic_collisions(collect_all_epics(branches))
    story_collisions = find_story_collisions(collect_all_stories(branches)) if args.stories else None
    print(render(branches, epic_collisions, story_collisions), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
