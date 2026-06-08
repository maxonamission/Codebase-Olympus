#!/usr/bin/env python3
"""Auto-sync: verplaats story-bestanden naar de map die bij hun front-matter `status:` hoort.

Front-matter `status:` is de geautoriseerde bron; deze hook houdt de map
(`stories/{backlog,todo,doing,done}/`) daarmee in lijn. Bedoeld als pre-commit hook:
je bewerkt alleen het `status:`-veld, het bestand verhuist vanzelf.

  --check : verplaats niets, exit 1 als er een mismatch is (CI / dry-run).
  (default): verplaats mismatched stories via `git mv` en re-stage ze.

Alleen stdlib. Python 3.9+.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

STATUSES = ("backlog", "todo", "doing", "done", "cancelled")
FM = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def fm_status(text: str) -> str | None:
    m = FM.match(text)
    if not m:
        return None
    for line in m.group(1).splitlines():
        if line.strip().lower().startswith("status:"):
            return line.split(":", 1)[1].strip().strip("'\"").lower()
    return None


def story_roots(repo_root: Path) -> list[Path]:
    out = []
    for d in repo_root.rglob("stories"):
        if d.is_dir() and ".git" not in d.parts and any((d / s).is_dir() for s in STATUSES):
            out.append(d)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--repo-root", default=".")
    args = ap.parse_args()
    repo_root = Path(args.repo_root).resolve()
    mismatches: list[tuple[Path, str, str]] = []

    for root in story_roots(repo_root):
        for status in STATUSES:
            d = root / status
            if not d.is_dir():
                continue
            for story in d.glob("*.md"):
                if story.name.startswith("_"):
                    continue
                want = fm_status(story.read_text(encoding="utf-8", errors="replace"))
                if want in STATUSES and want != status:
                    mismatches.append((story, status, want))

    if not mismatches:
        print("alle stories staan in de juiste map.")
        return 0

    for story, cur, want in mismatches:
        rel = story.relative_to(repo_root)
        if args.check:
            print(f"MISMATCH: {rel} (map '{cur}', status '{want}')")
            continue
        target = story.parent.parent / want / story.name
        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            subprocess.run(["git", "mv", str(story), str(target)], cwd=repo_root, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            story.rename(target)  # fallback buiten git
        print(f"VERPLAATST: {rel} → {target.relative_to(repo_root)}")

    return 1 if args.check else 0


if __name__ == "__main__":
    sys.exit(main())
