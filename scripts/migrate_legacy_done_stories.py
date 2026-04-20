"""Eenmalige migratie: vink AC-checkboxes af in legacy done-stories.

Achtergrond: vóór OS-06 was het afvinken van acceptatiecriteria geen
discipline. Stories werden naar ``done/`` verplaatst zonder dat ``- [ ]``
naar ``- [x]`` was omgezet. Dit script doet die afronding eenmalig en
markeert elk gemigreerd bestand met een HTML-comment, zodat de bulk-actie
auditbaar is.

Het script:

* itereert over ``stories/done/*.md``
* skipt bestanden met de marker (idempotent)
* skipt bestanden zonder openstaande AC (geen wijziging nodig)
* vervangt in de ``## Acceptatiecriteria``-sectie alle ``- [ ]`` door
  ``- [x]`` en voegt direct na die sectie de marker toe
* rapporteert een samenvatting

Run::

    python scripts/migrate_legacy_done_stories.py            # apply
    python scripts/migrate_legacy_done_stories.py --dry-run  # alleen tonen
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DONE_DIR = REPO_ROOT / "stories" / "done"

MARKER_PREFIX = "<!-- legacy-bulk-checked:"
MARKER_TEMPLATE = f"{MARKER_PREFIX} {{date}} — AC retroactief afgevinkt door OS-06 cleanup -->"

AC_HEADER_RE = re.compile(r"^##\s+Acceptatiecriteria\b", re.IGNORECASE)
ANY_HEADER_RE = re.compile(r"^##\s+\S")
UNCHECKED_RE = re.compile(r"^(\s*-\s*)\[\s\](\s+)")


def migrate_file(path: Path, today: str) -> tuple[bool, int]:
    """Migreer één bestand. Returns (changed, n_checked).

    Wijzigt het bestand in-place. Idempotent: als marker al aanwezig is
    of er geen openstaande AC zijn, wordt niets veranderd.
    """
    text = path.read_text(encoding="utf-8")

    if MARKER_PREFIX in text:
        return False, 0

    lines = text.splitlines()
    in_ac = False
    n_checked = 0
    new_lines: list[str] = []
    marker_inserted = False

    for line in lines:
        if AC_HEADER_RE.match(line):
            in_ac = True
            new_lines.append(line)
            continue
        if in_ac and ANY_HEADER_RE.match(line):
            # AC-sectie eindigt hier; voeg marker in vóór deze nieuwe header.
            if n_checked > 0 and not marker_inserted:
                new_lines.append("")
                new_lines.append(MARKER_TEMPLATE.format(date=today))
                new_lines.append("")
                marker_inserted = True
            in_ac = False
            new_lines.append(line)
            continue
        if in_ac:
            replaced, count = UNCHECKED_RE.subn(r"\1[x]\2", line, count=1)
            if count:
                n_checked += 1
            new_lines.append(replaced)
            continue
        new_lines.append(line)

    # Als AC-sectie tot het einde van het bestand liep en marker nog niet ingevoegd:
    if in_ac and n_checked > 0 and not marker_inserted:
        new_lines.append("")
        new_lines.append(MARKER_TEMPLATE.format(date=today))

    if n_checked == 0:
        return False, 0

    # Behoud trailing newline van origineel.
    new_text = "\n".join(new_lines)
    if text.endswith("\n"):
        new_text += "\n"

    path.write_text(new_text, encoding="utf-8")
    return True, n_checked


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not DONE_DIR.is_dir():
        print(f"Map niet gevonden: {DONE_DIR}", file=sys.stderr)
        return 2

    today = date.today().isoformat()
    files = sorted(DONE_DIR.glob("*.md"))
    print(f"Doorloop {len(files)} done-stories…")

    total_changed = 0
    total_acs = 0
    skipped_marker = 0
    skipped_no_ac = 0
    changes: list[tuple[Path, int]] = []

    for path in files:
        if args.dry_run:
            text = path.read_text(encoding="utf-8")
            if MARKER_PREFIX in text:
                skipped_marker += 1
                continue
            unchecked = sum(1 for line in text.splitlines() if UNCHECKED_RE.match(line))
            if unchecked == 0:
                skipped_no_ac += 1
                continue
            changes.append((path, unchecked))
            total_changed += 1
            total_acs += unchecked
            continue

        changed, n = migrate_file(path, today)
        if changed:
            total_changed += 1
            total_acs += n
            changes.append((path, n))
        elif MARKER_PREFIX in path.read_text(encoding="utf-8"):
            skipped_marker += 1
        else:
            skipped_no_ac += 1

    mode_label = "Zou wijzigen" if args.dry_run else "Gewijzigd"
    print("\n=== Samenvatting ===")
    print(f"{mode_label}: {total_changed} bestanden, {total_acs} AC-items afgevinkt")
    print(f"Skip (marker al aanwezig): {skipped_marker}")
    print(f"Skip (geen openstaande AC): {skipped_no_ac}")

    if changes and args.dry_run:
        print("\nDetails (eerste 10):")
        for path, n in changes[:10]:
            print(f"  {path.relative_to(REPO_ROOT)}: {n} AC")
        if len(changes) > 10:
            print(f"  … en nog {len(changes) - 10}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
