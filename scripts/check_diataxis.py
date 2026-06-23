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
4. **Doc-staleness (opt-in, `--check-review-date`).** Waarschuwt voor verouderde
   documentatie op basis van een expliciete `volgende-review:`-datum en/of de
   ouderdom van `laatst-bijgewerkt:`. Bewust **altijd warn-level** (ook onder
   `--gate=error`): een verouderd document is een signaal, geen kapotte build.

Dependency-light (alleen stdlib). Default **warn-only** (`--gate=warn`,
exitcode 0): zo kan een repo per doc-type opt-in nemen zonder de CI te
breken, en pas op `--gate=error` zetten als de migratie voor dat type klaar is.

Gebruik:

    python check_diataxis.py --glob 'docs/**/*.md' --glob 'EPICS*.md'
    python check_diataxis.py --glob 'PROJECTSTATUS*.md' --gate=error --require-presence
    # Staleness-signaal (warn): verlopen volgende-review of >180 dagen oud
    python check_diataxis.py --glob '**/*.md' --check-review-date --max-age-days 180
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
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
DATE_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})$")


def front_matter(text: str) -> str | None:
    """Return de ruwe YAML-front-matter-tekst, of None als die ontbreekt."""
    m = FM_RE.match(text)
    return m.group(1) if m else None


def read_field(fm: str, field: str) -> str | None:
    """Lees een scalair front-matter-veld (zonder YAML-dependency)."""
    field_re = re.compile(rf"^{re.escape(field)}:\s*(\S+)", re.MULTILINE)
    m = field_re.search(fm)
    return m.group(1).strip().strip("\"'") if m else None


def parse_iso_date(value: str) -> date | None:
    """Parse een strikte ISO-datum (YYYY-MM-DD); None bij ongeldig formaat."""
    m = DATE_RE.match(value)
    if not m:
        return None
    try:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return None


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


def check_review_date(
    p: Path,
    text: str,
    *,
    review_field: str,
    updated_field: str,
    max_age_days: int | None,
    require_review_date: bool,
    today: date,
) -> list[Issue]:
    """Opt-in staleness-signaal. Altijd warn-level: een verouderd document is
    een signaal, geen build-breker.

    Twee onafhankelijke triggers (beide warn):
    - `volgende-review:` ligt in het verleden → review verlopen.
    - `--max-age-days N` gezet én `laatst-bijgewerkt:` is ouder dan N dagen.
    """
    fm = front_matter(text)
    if fm is None:
        # Geen front-matter: de presence-check (check_doc) vlagt dit al.
        return []

    issues: list[Issue] = []

    review_raw = read_field(fm, review_field)
    if review_raw is None:
        if require_review_date:
            issues.append(
                Issue(p, "warning", f"geen `{review_field}:`-datum in front-matter")
            )
    else:
        review_date = parse_iso_date(review_raw)
        if review_date is None:
            issues.append(
                Issue(p, "warning", f"ongeldige `{review_field}`-datum {review_raw!r} (verwacht YYYY-MM-DD)")
            )
        elif review_date < today:
            overdue = (today - review_date).days
            issues.append(
                Issue(
                    p,
                    "warning",
                    f"review verlopen: {review_field} {review_date.isoformat()} ({overdue} dagen geleden)",
                )
            )

    if max_age_days is not None:
        updated_raw = read_field(fm, updated_field)
        if updated_raw is not None:
            updated_date = parse_iso_date(updated_raw)
            if updated_date is None:
                issues.append(
                    Issue(p, "warning", f"ongeldige `{updated_field}`-datum {updated_raw!r} (verwacht YYYY-MM-DD)")
                )
            else:
                age = (today - updated_date).days
                if age > max_age_days:
                    issues.append(
                        Issue(
                            p,
                            "warning",
                            f"verouderd: {updated_field} {updated_date.isoformat()} is {age} dagen oud (> {max_age_days})",
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
    # --- Opt-in staleness-signaal (altijd warn-level) ---
    ap.add_argument(
        "--check-review-date",
        action="store_true",
        help="schakel het doc-staleness-signaal in (verlopen `volgende-review` / oude `laatst-bijgewerkt`).",
    )
    ap.add_argument(
        "--review-field",
        default="volgende-review",
        help="front-matter-veld met de volgende-review-datum (default: volgende-review).",
    )
    ap.add_argument(
        "--updated-field",
        default="laatst-bijgewerkt",
        help="front-matter-veld met de laatste-bijwerk-datum (default: laatst-bijgewerkt).",
    )
    ap.add_argument(
        "--max-age-days",
        type=int,
        default=None,
        help="waarschuw als `laatst-bijgewerkt` ouder is dan N dagen (alleen met --check-review-date).",
    )
    ap.add_argument(
        "--require-review-date",
        action="store_true",
        help="waarschuw als een document geen `volgende-review`-datum draagt (alleen met --check-review-date).",
    )
    ap.add_argument(
        "--today",
        default=None,
        help="override de referentiedatum (YYYY-MM-DD) voor deterministische CI/tests.",
    )
    args = ap.parse_args()

    today = date.today()
    if args.today is not None:
        parsed = parse_iso_date(args.today)
        if parsed is None:
            print(f"check_diataxis: ongeldige --today {args.today!r} (verwacht YYYY-MM-DD).")
            return 2
        today = parsed

    root = Path(args.repo_root).resolve()
    globs = args.glob or ["**/*.md"]
    docs = collect(globs, root)
    if not docs:
        print("check_diataxis: geen documenten gematcht.")
        return 0

    n_err = n_warn = 0
    for p in docs:
        issues = check_doc(p, DEFAULT_PATH_RULES)
        if args.check_review_date:
            try:
                text = p.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                text = None
            if text is not None:
                issues = issues + check_review_date(
                    p,
                    text,
                    review_field=args.review_field,
                    updated_field=args.updated_field,
                    max_age_days=args.max_age_days,
                    require_review_date=args.require_review_date,
                    today=today,
                )
        for issue in issues:
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

    print(f"\ncheck_diataxis: {len(docs)} documenten — {n_err} fouten, {n_warn} waarschuwingen.")
    if args.gate == "error" and n_err:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
