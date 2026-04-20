#!/usr/bin/env python3
"""E3-12 validation: coverage, IRT parameters, exercise type mix for GRC items.

Covers two graph files — grc_alfabet.json (FONL) and
grc_grammatica_leerjaar1.json (MORF + SYNT). Reports per knoop-type.
Analoog aan scripts/validate_items_c1_11.py voor Latijn.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from gymnasium_classica.models.graph import Item

BASE = Path(__file__).parent.parent / "data" / "graph"


def _subcategory(knoop_id: str) -> str:
    """Return MORF, SYNT or FONL based on knoop-id segments."""
    parts = knoop_id.split("-")
    if len(parts) >= 3:
        return parts[2]
    return "OTHER"


def main() -> None:
    alfa = json.loads((BASE / "grc_alfabet.json").read_text(encoding="utf-8"))
    gram = json.loads((BASE / "grc_grammatica_leerjaar1.json").read_text(encoding="utf-8"))

    all_items: list[dict] = []
    knopen_met: list[tuple[str, int]] = []
    knopen_zonder: list[str] = []
    item_ids: set[str] = set()
    dupes: list[str] = []
    validation_errors: list[str] = []
    per_subcat_items: dict[str, int] = Counter()
    per_subcat_knopen: dict[str, int] = Counter()

    for src in (alfa, gram):
        for k in src["knopen"]:
            if k["taal"] != "grc" or k["type"] != "G":
                continue
            subcat = _subcategory(k["id"])
            per_subcat_knopen[subcat] += 1
            items = k.get("items", []) or []
            if items:
                knopen_met.append((k["id"], len(items)))
                per_subcat_items[subcat] += len(items)
                for item in items:
                    try:
                        Item(**item)
                    except Exception as exc:
                        validation_errors.append(f'{item["id"]}: {exc}')
                    if item["id"] in item_ids:
                        dupes.append(item["id"])
                    item_ids.add(item["id"])
                    all_items.append(item)
            else:
                knopen_zonder.append(k["id"])

    total = len(all_items)
    types = Counter(i["type"] for i in all_items)
    richt = Counter(i["richting"] for i in all_items)
    moeil = [i["moeilijkheid_initieel"] for i in all_items]
    discr = [i["discriminatie_initieel"] for i in all_items]
    tijden = [i["verwachte_tijd_sec"] for i in all_items]

    ok = True
    print("=" * 60)
    print("E3-12 VALIDATIE — Items voor Griekse grammatica + alfabet")
    print("=" * 60)

    print("\n1. DEKKING")
    print(f"   GRC-G knopen met items:    {len(knopen_met)}")
    print(f"   GRC-G knopen zonder items: {len(knopen_zonder)}")
    print(f"   Totaal items:              {total}")
    if knopen_met:
        print(f"   Gem. items/knoop:          {total / len(knopen_met):.1f}")
        # Alfabet-letter-knopen hebben bij ontwerp 1 offline-schrijven item.
        def _is_letter_drill(kid: str) -> bool:
            return (
                kid.startswith("GRC-G-FONL-ALFA-")
                and kid.split("-")[-1] not in {"INTRO", "GRP1", "GRP2", "GRP3", "GRP4"}
            )

        under_two = [
            (kid, n) for kid, n in knopen_met if n < 2 and not _is_letter_drill(kid)
        ]
        if under_two:
            print(f"   ⚠ {len(under_two)} niet-letter-knopen met < 2 items:")
            for kid, n in under_two[:5]:
                print(f"      {kid} ({n})")
        else:
            print(
                "   ✓ Alle niet-letter-knopen >= 2 items "
                "(alfabet-letters hebben bij ontwerp 1 schrijf-drill item)"
            )

    if knopen_zonder:
        print(f"   ❌ Knopen zonder items ({len(knopen_zonder)}):")
        for kid in sorted(knopen_zonder):
            print(f"      {kid}")
        ok = False
    else:
        print("   ✓ Alle GRC-G-knopen hebben items")

    print("\n2. DEKKING PER SUBCATEGORIE (MORF / SYNT / FONL)")
    for sub in sorted(per_subcat_knopen):
        k_total = per_subcat_knopen[sub]
        k_with = sum(
            1 for kid, _ in knopen_met if _subcategory(kid) == sub
        )
        i_total = per_subcat_items[sub]
        pct = 100 * k_with / k_total if k_total else 0
        print(
            f"   {sub:6s}: {k_with:3d}/{k_total:3d} knopen "
            f"({pct:5.1f}%) · {i_total} items"
        )

    print("\n3. OEFENTYPE-MIX")
    for t, c in types.most_common():
        pct = 100 * c / total
        print(f"   {t:20s}: {c:4d} ({pct:.1f}%)")
    hpct = 100 * types.get("herkenning", 0) / total
    ppct = 100 * types.get("productie", 0) / total
    cpct = 100 * (types.get("contextueel", 0) + types.get("analyse", 0)) / total
    if hpct < 20:
        print(f"   ⚠ Herkenning lager dan gewenst: {hpct:.0f}% (doel: 30%+)")
    if ppct < 20:
        print(f"   ⚠ Productie lager dan gewenst: {ppct:.0f}% (doel: 30%+)")
    if cpct < 10:
        print(f"   ⚠ Contextueel+analyse: {cpct:.0f}% (doel: 10%+)")

    print("\n4. RICHTING-MIX")
    for r, c in richt.most_common():
        print(f"   {r:15s}: {c:4d} ({100 * c / total:.1f}%)")

    print("\n5. IRT-PARAMETERS")
    print(
        f"   Moeilijkheid:   min={min(moeil):.2f}  max={max(moeil):.2f}  "
        f"gem={sum(moeil) / len(moeil):.2f}"
    )
    print(
        f"   Discriminatie:  min={min(discr):.2f}  max={max(discr):.2f}  "
        f"gem={sum(discr) / len(discr):.2f}"
    )
    print(
        f"   Verwachte tijd: min={min(tijden)}s  max={max(tijden)}s  "
        f"gem={sum(tijden) / len(tijden):.0f}s"
    )
    if min(discr) <= 0:
        print("   ❌ Discriminatie <= 0 gevonden")
        ok = False
    else:
        print("   ✓ Alle discriminatie > 0")
    if min(moeil) < -3 or max(moeil) > 3:
        print("   ❌ Moeilijkheid buiten [-3, 3]")
        ok = False
    else:
        print("   ✓ Moeilijkheid binnen [-3, 3]")

    print("\n6. DUPLICATEN")
    if dupes:
        print(f"   ❌ {len(dupes)} dubbele item-IDs: {dupes[:5]}")
        ok = False
    else:
        print("   ✓ Geen dubbele item-IDs")

    print("\n7. PYDANTIC VALIDATIE")
    if validation_errors:
        print(f"   ❌ {len(validation_errors)} fouten:")
        for e in validation_errors[:5]:
            print(f"      {e}")
        ok = False
    else:
        print("   ✓ Alle items valide")

    print()
    print("=" * 60)
    print(f"RESULTAAT: {'✓ GESLAAGD' if ok else '❌ GEFAALD'}")
    print("=" * 60)

    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
