"""N1 Tier 3 — migreer Dutch JSON-*keys* naar Engels (waarden onveranderd).

Eenmalige, idempotente datamigratie over de drie JSON-schema's die door
Pydantic-modellen worden geladen:

- ``data/graph/*.json``         -> Node / Item / GraphData (models/graph.py)
- ``data/passages/*.json``      -> Passage / WordAnnotation (models/passage.py)
- ``data/methode_mapping.json`` -> dict-access (diagnostic/methode_profile.py)

Alleen dict-*keys* worden hernoemd (exacte match), nooit waarden -- zo blijft
alle Nederlandstalige content (vertalingen, feedback, beschrijvingen) intact.
De methode-eigen config-keys (``methoden``, ``hoofdstukken``) vallen buiten
scope en blijven ongemoeid.

Gebruik: ``python scripts/migrate_n1_tier3_keys.py [--check]``
``--check`` rapporteert alleen (geen schrijfacties).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

# Nederlandse JSON-key -> Engelse key. Exacte-match rename (geen substring).
# NB: de waarden links zijn opzettelijk Nederlands; pas deze module niet aan
# met een blinde identifier-rename.
KEY_MAP: dict[str, str] = {
    # GraphData / gedeeld
    "knopen": "nodes",
    "knoop_ids": "node_ids",
    "taal": "language",
    # Node
    "titel_nl": "title_nl",
    "titel_terminologie": "title_terminology",
    "beschrijving": "description",
    "bloom_niveau": "bloom_level",
    "fase": "phase",
    "toetsbaar": "testable",
    "pensum_jaren": "pensum_years",
    "cevte_referentie": "cevte_reference",
    "semantisch_cluster": "semantic_cluster",
    # Item
    "richting": "direction",
    "moeilijkheid_initieel": "difficulty_initial",
    "discriminatie_initieel": "discrimination_initial",
    "verwachte_tijd_sec": "expected_time_sec",
    "antwoord": "answer",
    "bron": "source",
    "verificatie_methode": "verification_method",
    "verwacht_resultaat": "expected_result",
    # Passage / WordAnnotation
    "titel": "title",
    "tekst": "text",
    "annotaties": "annotations",
    "moeilijkheid": "difficulty",
    "woord": "word",
    "naamval": "case",
    "vertaling": "translation",
}

TARGETS = [
    "data/graph",
    "data/passages",
    "data/methode_mapping.json",
]


def _rename_keys(obj: Any, counter: dict[str, int]) -> Any:
    """Recursively rename dict keys per KEY_MAP; values untouched."""
    if isinstance(obj, dict):
        new: dict[str, Any] = {}
        for key, value in obj.items():
            new_key = KEY_MAP.get(key, key)
            if new_key != key:
                counter[key] = counter.get(key, 0) + 1
            new[new_key] = _rename_keys(value, counter)
        return new
    if isinstance(obj, list):
        return [_rename_keys(item, counter) for item in obj]
    return obj


def _json_files(target: Path) -> list[Path]:
    if target.is_dir():
        return sorted(target.glob("*.json"))
    return [target] if target.exists() else []


def main() -> int:
    check_only = "--check" in sys.argv
    root = Path(__file__).resolve().parent.parent
    total_counter: dict[str, int] = {}
    files_changed = 0

    for target_rel in TARGETS:
        for path in _json_files(root / target_rel):
            original = json.loads(path.read_text(encoding="utf-8"))
            counter: dict[str, int] = {}
            migrated = _rename_keys(original, counter)
            if counter:
                files_changed += 1
                for k, n in counter.items():
                    total_counter[k] = total_counter.get(k, 0) + n
                if not check_only:
                    path.write_text(
                        json.dumps(migrated, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8",
                    )
                rel = path.relative_to(root)
                print(f"  {rel}: {sum(counter.values())} keys ({', '.join(sorted(counter))})")

    print(
        f"\n{'[check] ' if check_only else ''}{files_changed} bestanden, "
        f"{sum(total_counter.values())} key-occurrences hernoemd."
    )
    if total_counter:
        print("Per key:")
        for k in sorted(total_counter):
            print(f"  {k} -> {KEY_MAP[k]}: {total_counter[k]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
