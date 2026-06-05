#!/usr/bin/env python3
"""Drift-/staleness-check voor adopterende repo's (codebase-standards).

Twee signalen:
  1. STALENESS — de geadopteerde versie (`.codebase-standards-version`) loopt achter op
     de upstream `VERSION`.
  2. DRIFT — een lokaal gevendord bestand wijkt af van de manifest-hash. Vereist een
     sync-map die lokale paden koppelt aan upstream-bronpaden.

Sync-map (`.codebase-standards-sync.json`), optioneel:
    { "<lokaal pad>": "<upstream pad in manifest>", ... }
    bv. { ".github/pull_request_template.md": "templates/PR_TEMPLATE.md" }

Bewuste lokale afwijkingen whitelist je met --allow <lokaal pad> (herhaalbaar).

Standaard warn-only (exit 0). --strict laat drift falen (exit 1). Alleen stdlib.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


def parse_semver(s: str) -> tuple[int, int, int]:
    parts = (s.strip().lstrip("v").split(".") + ["0", "0", "0"])[:3]
    try:
        return tuple(int(p) for p in parts)  # type: ignore[return-value]
    except ValueError:
        return (0, 0, 0)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--version-file", default=".codebase-standards-version")
    ap.add_argument("--upstream-version", help="pad naar upstream VERSION (voor staleness)")
    ap.add_argument("--manifest", default=".codebase-standards-manifest.json")
    ap.add_argument("--sync-map", default=".codebase-standards-sync.json")
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--allow", action="append", default=[], help="lokaal pad dat mag afwijken")
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()

    root = Path(args.repo_root).resolve()
    warnings: list[str] = []
    drifts: list[str] = []

    # 1. Staleness
    vf = root / args.version_file
    if vf.is_file():
        adopted = vf.read_text(encoding="utf-8").strip()
        if args.upstream_version:
            up = Path(args.upstream_version).read_text(encoding="utf-8").strip()
            if parse_semver(adopted) < parse_semver(up):
                warnings.append(f"staleness: geadopteerd v{adopted} < upstream v{up} — overweeg upgrade")
        print(f"geadopteerde standaard: v{adopted}")
    else:
        warnings.append(f"geen {args.version_file} gevonden — repo heeft de standaard nog niet geadopteerd")

    # 2. Drift (vereist manifest + sync-map)
    man = root / args.manifest
    smap = root / args.sync_map
    if man.is_file() and smap.is_file():
        manifest = json.loads(man.read_text(encoding="utf-8"))
        sync = json.loads(smap.read_text(encoding="utf-8"))
        for local_path, source_path in sync.items():
            if local_path in args.allow:
                continue
            lp = root / local_path
            expected = manifest.get(source_path)
            if expected is None:
                warnings.append(f"sync-map verwijst naar onbekend manifest-pad: {source_path}")
                continue
            if not lp.is_file():
                drifts.append(f"{local_path}: ontbreekt (verwacht kopie van {source_path})")
            elif sha256(lp) != expected:
                drifts.append(f"{local_path}: wijkt af van {source_path} (lokaal gewijzigd of verouderd)")
    else:
        print("drift-check overgeslagen (manifest of sync-map ontbreekt).")

    for w in warnings:
        print(f"WAARSCHUWING: {w}")
    for d in drifts:
        print(f"DRIFT: {d}")

    print(f"\n{len(drifts)} drift(s) · {len(warnings)} waarschuwing(en)")
    if args.strict and drifts:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
