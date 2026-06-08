#!/usr/bin/env python3
"""Linkbeleid-validator: GitHub-native Markdown-links i.p.v. Obsidian-wikilinks.

Per Markdown-bestand (code-blocks gemaskeerd) controleert het script:

1. **Geen bare `[[wikilink]]`.** Obsidian-`[[..]]` degradeert tot platte tekst op
   GitHub (geen klik). Gebruik een relatieve Markdown-link.
2. **Dode relatieve `.md`-links.** Elke `[tekst](pad.md)` met een relatief pad moet
   naar een bestaand bestand wijzen.

`--fix` repareert beide, basename-gestuurd (story-/form-bestandsnamen zijn uniek):

- `[[X]]` / `[[X|alias]]` / `[[X#kop]]` → `[alias-of-X](relpad.md#kop-slug)` als
  `X.md` uniek in de repo resolvet.
- een dode `[tekst](oud/pad/X.md)` → herpunt naar het unieke `X.md` elders. Zo
  blijven links heel bij verplaatsingen (`backlog`→`done`, `open`→`afgehandeld`).

Niet-resolvebare (dode/ambigue) verwijzingen worden gerapporteerd, niet geraden.

Modi:
    --mode=report   Default. Print issues, exitcode 0 (warn-laag).
    --mode=strict   Exitcode 1 als er issues zijn (CI-gate na opschoning).
    --fix           Pas reparaties toe (met --mode bepaalt het de exitcode erna).
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path
from urllib.parse import quote, unquote

EXCLUDE_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", ".ruff_cache"}

WIKILINK_RE = re.compile(r"\[\[([^\[\]]+)\]\]")
MDLINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
FENCE_RE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`]*`")

Index = dict[str, list[Path]]


class Issue:
    __slots__ = ("kind", "message", "path")

    def __init__(self, path: Path, kind: str, message: str) -> None:
        self.kind = kind  # "wikilink" | "dead-link"
        self.message = message
        self.path = path

    def __str__(self) -> str:
        return f"  [{self.kind}] {self.path}: {self.message}"


def mask_code(text: str) -> str:
    """Vervang code-blocks/inline-code door spaties (lengte + posities behouden)."""

    def blank(m: re.Match[str]) -> str:
        return re.sub(r"\S", " ", m.group(0))

    text = FENCE_RE.sub(blank, text)
    return INLINE_CODE_RE.sub(blank, text)


def slugify_anchor(anchor: str) -> str:
    """GitHub-heading-slug: lowercase, spaties → '-', leestekens weg."""
    s = anchor.strip().lower()
    s = re.sub(r"[^\w\s-]", "", s)
    return re.sub(r"\s+", "-", s)


def find_md_files(root: Path) -> list[Path]:
    out: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for fn in filenames:
            if fn.endswith(".md"):
                out.append(Path(dirpath) / fn)
    return out


def basename_index(files: list[Path]) -> dict[str, list[Path]]:
    idx: dict[str, list[Path]] = {}
    for f in files:
        idx.setdefault(f.stem, []).append(f)
    return idx


def _rel(target: Path, from_file: Path) -> str:
    rel = os.path.relpath(target, start=from_file.parent).replace(os.sep, "/")
    return quote(rel, safe="/")  # spaties → %20 (mapnamen met spaties)


def _split_wikilink(body: str) -> tuple[str, str, str]:
    """`X#anchor|alias` → (target, anchor, display)."""
    alias = ""
    if "|" in body:
        body, alias = body.split("|", 1)
    anchor = ""
    if "#" in body:
        body, anchor = body.split("#", 1)
    target = body.strip().removesuffix(".md")
    display = alias.strip() if alias.strip() else (anchor.strip() or target)
    return target, anchor.strip(), display


def resolve_basename(name: str, idx: dict[str, list[Path]]) -> Path | None:
    hits = idx.get(Path(name).stem)
    return hits[0] if hits and len(hits) == 1 else None


def process_file(p: Path, idx: Index, fix: bool) -> tuple[list[Issue], str | None]:
    text = p.read_text(encoding="utf-8")
    masked = mask_code(text)
    issues: list[Issue] = []
    edits: list[tuple[int, int, str]] = []

    # 1. Wikilinks.
    for m in WIKILINK_RE.finditer(masked):
        target, anchor, display = _split_wikilink(m.group(1))
        hit = resolve_basename(target, idx)
        if hit is None:
            msg = f"[[{m.group(1)}]] (onresolvbaar — handmatig)"
            issues.append(Issue(p, "wikilink", msg))
            continue
        if fix:
            rel = _rel(hit, p)
            suffix = f"#{slugify_anchor(anchor)}" if anchor else ""
            edits.append((m.start(), m.end(), f"[{display}]({rel}{suffix})"))
        else:
            issues.append(Issue(p, "wikilink", f"[[{m.group(1)}]] → Markdown-link"))

    # 2. Dode relatieve .md-links.
    for m in MDLINK_RE.finditer(masked):
        url = m.group(2).strip()
        if "://" in url or url.startswith(("#", "mailto:")):
            continue
        path_part, _, frag = url.partition("#")
        if not path_part.endswith(".md"):
            continue
        decoded = unquote(path_part)  # %20 → spatie vóór de existence-check
        target = (p.parent / decoded).resolve()
        if target.exists():
            continue
        hit = resolve_basename(Path(decoded).name, idx)
        if hit is None:
            issues.append(Issue(p, "dead-link", f"{url} (geen uniek doel)"))
            continue
        if fix:
            rel = _rel(hit, p)
            newurl = f"{rel}#{frag}" if frag else rel
            edits.append((m.start(2), m.end(2), newurl))
        else:
            issues.append(Issue(p, "dead-link", f"{url} → {_rel(hit, p)}"))

    if fix and edits:
        for start, end, repl in sorted(edits, reverse=True):
            text = text[:start] + repl + text[end:]
        return issues, text
    return issues, None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--mode", choices=("report", "strict"), default="report")
    ap.add_argument(
        "--fix",
        action="store_true",
        help="pas reparaties toe (wikilink→md, herpunt dode links).",
    )
    args = ap.parse_args()

    root = Path(args.repo_root).resolve()
    files = find_md_files(root)
    idx = basename_index(files)

    all_issues: list[Issue] = []
    n_fixed = 0
    for p in sorted(files):
        issues, new_text = process_file(p, idx, args.fix)
        if new_text is not None:
            p.write_text(new_text, encoding="utf-8")
            n_fixed += 1
        all_issues.extend(issues)

    for i in all_issues:
        print(i)
    label = root.name
    n = len(all_issues)
    if args.fix:
        print(f"\nvalidate_links ({label}): {n_fixed} gefixt, {n} issues over.")
    else:
        print(f"\nvalidate_links ({label}): {n} issues / {len(files)} bestanden.")
    if args.mode == "strict" and all_issues:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
