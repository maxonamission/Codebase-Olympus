"""N1 Tier 3 (deel 2) — migreer Nederlandstalige enum-*waarden* naar Engels.

Veld-*gericht* over ``data/graph/*.json`` zodat alleen echte enum-waarden
worden vertaald en Nederlandstalige content (beschrijvingen, betekenissen)
ongemoeid blijft:

- ``node.bloom_level``  (BloomLevel)
- ``item.type``         (ItemType — NIET node.type/NodeType: G/V/C/I blijft)
- ``item.direction``    (Direction)
- ``item.source``       (Source)

Buiten scope (keuze juni 2026): ``Phase`` (onderbouw/bovenbouw = NL-
onderwijstermen) en ``Language`` (lat/grc/shared = taalcodes) blijven.
Idempotent: onbekende/al-Engelse waarden blijven ongewijzigd.

Gebruik: ``python scripts/migrate_n1_enum_values.py [--check]``
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

BLOOM = {
    "kennis": "knowledge",
    "begrip": "comprehension",
    "toepassing": "application",
    "analyse": "analysis",
    "synthese": "synthesis",
}
DIRECTION = {"receptief": "receptive", "productief": "productive"}
SOURCE = {
    "handmatig": "manual",
    "llm_gegenereerd": "llm_generated",
    "authentiek": "authentic",
}
ITEMTYPE = {
    "herkenning": "recognition",
    "productie": "production",
    "analyse": "analysis",
    "synthese": "synthesis",
    "contextueel": "contextual",
    "offline_schrijven": "offline_writing",
    "luister_herkenning": "listening_recognition",
    "luister_productie": "listening_production",
}


def _migrate_graph(data: dict[str, Any], counter: dict[str, int]) -> None:
    def bump(field: str) -> None:
        counter[field] = counter.get(field, 0) + 1

    for node in data.get("nodes", []):
        if (v := node.get("bloom_level")) in BLOOM:
            node["bloom_level"] = BLOOM[v]
            bump("bloom_level")
        for item in node.get("items", []):
            if (v := item.get("type")) in ITEMTYPE:
                item["type"] = ITEMTYPE[v]
                bump("type")
            if (v := item.get("direction")) in DIRECTION:
                item["direction"] = DIRECTION[v]
                bump("direction")
            if (v := item.get("source")) in SOURCE:
                item["source"] = SOURCE[v]
                bump("source")


def main() -> int:
    check_only = "--check" in sys.argv
    root = Path(__file__).resolve().parent.parent
    total: dict[str, int] = {}
    files_changed = 0

    for path in sorted((root / "data" / "graph").glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        counter: dict[str, int] = {}
        _migrate_graph(data, counter)
        if counter:
            files_changed += 1
            for k, n in counter.items():
                total[k] = total.get(k, 0) + n
            if not check_only:
                path.write_text(
                    json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )
            print(f"  {path.relative_to(root)}: {sum(counter.values())} waarden")

    print(
        f"\n{'[check] ' if check_only else ''}{files_changed} bestanden, "
        f"{sum(total.values())} enum-waarden vertaald."
    )
    for k in sorted(total):
        print(f"  {k}: {total[k]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
