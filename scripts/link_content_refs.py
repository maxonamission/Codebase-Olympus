#!/usr/bin/env python3
"""Link knowledge-graph knopen to their markdown content files.

For every knoop that has a matching ``data/content/{ID}.md`` file this
script ensures the knoop's ``content_ref`` points at that file.  The
reference is stored as a POSIX-style repo-relative path so the JSON
blijft platform-onafhankelijk:

    "content_ref": "data/content/LAT-G-MORF-NOM-D1.md"

The script is idempotent: knopen that already have the correct
``content_ref`` are left untouched.  Use ``--dry-run`` to preview
changes without writing to disk.

Usage::

    python scripts/link_content_refs.py --dry-run
    python scripts/link_content_refs.py
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_GRAPH_DIR = REPO_ROOT / "data" / "graph"
DEFAULT_CONTENT_DIR = REPO_ROOT / "data" / "content"


# Canonical key order for a knoop. Existing JSON files omit content_ref, so we
# insert it in the position dictated by the Pydantic model (after
# cevte_referentie, before pronunciation). Keys not listed here keep their
# original order.
_KNOOP_KEY_ORDER = [
    "id",
    "type",
    "taal",
    "titel_nl",
    "titel_terminologie",
    "beschrijving",
    "bloom_niveau",
    "fase",
    "toetsbaar",
    "pensum_jaren",
    "cevte_referentie",
    "content_ref",
    "pronunciation",
    "semantisch_cluster",
    "items",
]


@dataclass
class LinkResult:
    """Summary of what the script did (or would do, with --dry-run)."""

    scanned_files: int = 0
    scanned_knopen: int = 0
    content_files_found: int = 0
    refs_added: list[tuple[str, str]] = field(default_factory=list)
    refs_updated: list[tuple[str, str, str]] = field(default_factory=list)
    refs_unchanged: int = 0
    files_written: list[str] = field(default_factory=list)


def expected_content_ref(knoop_id: str) -> str:
    """Canonical repo-relative path for the markdown content of a knoop."""
    return f"data/content/{knoop_id}.md"


def _reorder_knoop_keys(knoop: dict) -> dict:
    """Return *knoop* with keys in the canonical order defined above."""
    ordered: dict = {}
    for key in _KNOOP_KEY_ORDER:
        if key in knoop:
            ordered[key] = knoop[key]
    # Preserve any keys we didn't anticipate, at the end.
    for key, value in knoop.items():
        if key not in ordered:
            ordered[key] = value
    return ordered


def link_content_refs(
    graph_dir: Path = DEFAULT_GRAPH_DIR,
    content_dir: Path = DEFAULT_CONTENT_DIR,
    *,
    dry_run: bool = False,
) -> LinkResult:
    """Set ``content_ref`` on every knoop with a matching markdown file.

    Only updates knopen where ``{content_dir}/{knoop_id}.md`` exists.  The
    JSON is re-written with ``indent=2`` and ``ensure_ascii=False`` to match
    the existing style.
    """
    result = LinkResult()
    content_ids: set[str] = {p.stem for p in content_dir.glob("*.md")}
    result.content_files_found = len(content_ids)

    for json_path in sorted(graph_dir.glob("*.json")):
        result.scanned_files += 1
        with open(json_path, encoding="utf-8") as f:
            data = json.load(f)

        file_changed = False
        knopen = data.get("knopen", [])
        for idx, knoop in enumerate(knopen):
            result.scanned_knopen += 1
            knoop_id = knoop.get("id")
            if not knoop_id or knoop_id not in content_ids:
                continue

            expected = expected_content_ref(knoop_id)
            current = knoop.get("content_ref")
            if current == expected:
                result.refs_unchanged += 1
                continue

            if current is None:
                result.refs_added.append((json_path.name, knoop_id))
            else:
                result.refs_updated.append((json_path.name, knoop_id, current))

            knoop["content_ref"] = expected
            knopen[idx] = _reorder_knoop_keys(knoop)
            file_changed = True

        if file_changed and not dry_run:
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                f.write("\n")
            result.files_written.append(json_path.name)
        elif file_changed and dry_run:
            result.files_written.append(json_path.name)

    return result


def _print_summary(result: LinkResult, *, dry_run: bool) -> None:
    verb_future = "zou" if dry_run else "heeft"
    print(f"=== link_content_refs ({'DRY-RUN' if dry_run else 'APPLY'}) ===")
    print(f"Graph-bestanden gescand:    {result.scanned_files}")
    print(f"Knopen gescand:             {result.scanned_knopen}")
    print(f"Content-bestanden gevonden: {result.content_files_found}")
    print(f"Nieuwe content_refs:        {len(result.refs_added)}")
    print(f"Bijgewerkte content_refs:   {len(result.refs_updated)}")
    print(f"Al correct (onveranderd):   {result.refs_unchanged}")
    print(f"Bestanden {verb_future} geschreven:   {len(result.files_written)}")

    if result.refs_added:
        print("\nNieuwe koppelingen:")
        for filename, knoop_id in result.refs_added:
            print(f"  + {knoop_id}  ({filename})")
    if result.refs_updated:
        print("\nBijgewerkte koppelingen:")
        for filename, knoop_id, old in result.refs_updated:
            print(f"  ~ {knoop_id}: {old!r} -> {expected_content_ref(knoop_id)!r}  ({filename})")


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Zet content_ref op elke knoop waarvoor een matching markdown-bestand bestaat.",
    )
    parser.add_argument(
        "--graph-dir",
        type=Path,
        default=DEFAULT_GRAPH_DIR,
        help="Map met graph-JSON-bestanden (default: data/graph).",
    )
    parser.add_argument(
        "--content-dir",
        type=Path,
        default=DEFAULT_CONTENT_DIR,
        help="Map met markdown-content (default: data/content).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Rapporteer wat er zou gebeuren zonder bestanden te schrijven.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    result = link_content_refs(
        graph_dir=args.graph_dir,
        content_dir=args.content_dir,
        dry_run=args.dry_run,
    )
    _print_summary(result, dry_run=args.dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main())
