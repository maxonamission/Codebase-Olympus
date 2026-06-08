#!/usr/bin/env python3
"""Optioneel doc-standaard-profiel: valideert het `diataxis:`-front-matter-veld.

Gefaseerde, opt-in adoptie van het documentatie-standaard-patroon (drie
levende-documentatie-artefacttypen + Diátaxis-modes). Generalisatie van Atlas'
`validate_doc_standard.py`; zie `profiles/diataxis/README.md` en
`docs/divergentie-cs-atlas.md` As 6.

Per gematcht document controleert het script:

1. **Aanwezigheid.** YAML-front-matter met een `diataxis:`-veld.
2. **Geldige waarde.** Eén van de toegestane modes (zie `VALID_MODES`).
3. **Pad↔type-consistentie.** Optioneel: bestandsnaam-patronen (bijv.
   `PROJECTSTATUS*` → `state`) moeten matchen met de gedeclareerde waarde.

Dependency-light (alleen stdlib). Default **warn-only** (`--gate=warn`,
exitcode 0): zo kan een repo per doc-type opt-in nemen zonder de CI te
breken, en pas op `--gate=error` zetten als de migratie voor dat type klaar is.

Gebruik:

    python check_diataxis.py --glob 'docs/**/*.md' --glob 'EPICS*.md'
    python check_diataxis.py --glob 'PROJECTSTATUS*.md' --gate=error --require-presence
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Toegestane waarden: de vier Diátaxis-modes + de operationele triade die
# CS/Atlas voor levende documentatie gebruiken (State/Log/Intent).
VALID_MODES = {
    "tutorial",
    "how-to",
    "howto",
    "reference",
    "explanation",
    "state",
    "log",
    "intent",
}

# Pad↔type-mapping (bestandsnaam-prefix → verwachte waarde). Conventie uit de
# documentatie-standaard; overschrijfbaar per repo via een eigen mapping.
DEFAULT_PATH_RULES: list[tuple[str, str]] = [
    ("PROJECTSTATUS", "state"),
    ("CHANGELOG", "log"),
    ("ROADMAP", "intent"),
    ("EPICS", "intent"),
    ("SPRINTPLAN", "intent"),
    ("ADR", "explanation"),
]

FM_RE = re.compile(r"^﻿?---\s*\n(.*?)\n---\s*\n", re.DOTALL)
FIELD_RE = re.compile(r"^diataxis:\s*(\S+)", re.MULTILINE)


class Issue:
    __slots__ = ("level", "message", "path")

    def __init__(self, path: Path, level: str, message: str) -> None:
        self.path = path
        self.level = level
        self.message = message

    def __str__(self) -> str:
        return f"  [{self.level}] {self.path}: {self.message}"


def read_diataxis(text: str) -> str | None:
    """Return de waarde van het `diataxis:`-veld, of None als front-matter/veld
    ontbreekt."""
    m = FM_RE.match(text)
    if not m:
        return None
    fm = m.group(1)
    fm_field = FIELD_RE.search(fm)
    if not fm_field:
        return None
    return fm_field.group(1).strip().strip("\"'").lower()


def expected_for_path(name: str, rules: list[tuple[str, str]]) -> str | None:
    for prefix, mode in rules:
        if name.startswith(prefix):
            return mode
    return None


def check_doc(p: Path, rules: list[tuple[str, str]]) -> list[Issue]:
    try:
        text = p.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:  # rapporteer leesfouten als issue
        return [Issue(p, "error", f"kan bestand niet lezen: {e}")]

    value = read_diataxis(text)
    if value is None:
        return [Issue(p, "warning", "geen `diataxis:`-veld in front-matter")]

    issues: list[Issue] = []
    if value not in VALID_MODES:
        issues.append(
            Issue(
                p,
                "error",
                f"ongeldige diataxis-waarde {value!r} (geldig: {sorted(VALID_MODES)})",
            )
        )
    expected = expected_for_path(p.name, rules)
    if expected and value != expected:
        issues.append(
            Issue(
                p,
                "warning",
                f"pad suggereert diataxis: {expected!r}, maar gedeclareerd is {value!r}",
            )
        )
    return issues


def collect(globs: list[str], root: Path) -> list[Path]:
    out: list[Path] = []
    seen: set[Path] = set()
    for g in globs:
        for p in sorted(root.glob(g)):
            if p.is_file() and p.suffix == ".md" and p not in seen:
                seen.add(p)
                out.append(p)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument(
        "--glob",
        action="append",
        default=[],
        help="glob t.o.v. --repo-root; herhaalbaar",
    )
    ap.add_argument("--repo-root", default=".")
    ap.add_argument(
        "--gate",
        choices=("warn", "error"),
        default="warn",
        help="warn: exitcode 0 ook bij issues (default); error: exitcode 1 bij errors.",
    )
    ap.add_argument(
        "--require-presence",
        action="store_true",
        help="behandel ontbrekend `diataxis:`-veld als error i.p.v. warning (alleen met --gate=error).",
    )
    args = ap.parse_args()

    root = Path(args.repo_root).resolve()
    globs = args.glob or ["**/*.md"]
    docs = collect(globs, root)
    if not docs:
        print("check_diataxis: geen documenten gematcht.")
        return 0

    n_err = n_warn = 0
    for p in docs:
        for issue in check_doc(p, DEFAULT_PATH_RULES):
            if (
                args.require_presence
                and issue.level == "warning"
                and "geen `diataxis:`-veld" in issue.message
            ):
                issue.level = "error"
            print(issue)
            if issue.level == "error":
                n_err += 1
            else:
                n_warn += 1

    print(
        f"\ncheck_diataxis: {len(docs)} documenten — {n_err} fouten, {n_warn} waarschuwingen."
    )
    if args.gate == "error" and n_err:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
