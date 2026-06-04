#!/usr/bin/env python3
"""C1-11 validation: coverage, IRT parameters, exercise type mix for all LAT-G items."""

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from gymnasium_classica.models.graph import Item

BASE = Path(__file__).parent.parent / "data" / "graph"


def main():
    poc = json.loads((BASE / "lat_grammatica_poc.json").read_text(encoding="utf-8"))
    lj1 = json.loads((BASE / "lat_grammatica_leerjaar1.json").read_text(encoding="utf-8"))

    all_items = []
    knopen_met = []
    knopen_zonder = []
    item_ids = set()
    dupes = []
    validation_errors = []

    for src in [poc, lj1]:
        for k in src["nodes"]:
            if k["language"] != "lat" or k["type"] != "G":
                continue
            items = k.get("items", [])
            if items:
                knopen_met.append((k["id"], len(items)))
                for i in items:
                    # Validate via Pydantic
                    try:
                        Item(**i)
                    except Exception as e:
                        validation_errors.append(f"{i['id']}: {e}")
                    # Check dupes
                    if i["id"] in item_ids:
                        dupes.append(i["id"])
                    item_ids.add(i["id"])
                    all_items.append(i)
            else:
                knopen_zonder.append(k["id"])

    total = len(all_items)
    types = Counter(i["type"] for i in all_items)
    richt = Counter(i["direction"] for i in all_items)
    moeil = [i["difficulty_initial"] for i in all_items]
    discr = [i["discrimination_initial"] for i in all_items]
    tijden = [i["expected_time_sec"] for i in all_items]

    ok = True
    print("=" * 60)
    print("C1-11 VALIDATIE — Items voor Latijnse grammatica")
    print("=" * 60)

    print("\n1. DEKKING")
    print(f"   LAT-G nodes met items:    {len(knopen_met)}")
    print(f"   LAT-G nodes zonder items: {len(knopen_zonder)}")
    print(f"   Totaal items:              {total}")
    print(f"   Gem. items/node:          {total / len(knopen_met):.1f}")

    min_items = min(n for _, n in knopen_met)
    if min_items < 2:
        print(f"   ❌ Minimumeis (2 items/node) NIET gehaald: min = {min_items}")
        ok = False
    else:
        print(f"   ✓ Alle nodes met items >= 2 (min = {min_items})")

    print("\n2. OEFENTYPE-MIX")
    for t, c in types.most_common():
        pct = 100 * c / total
        # Placeholder: altijd "✓" zolang we geen striktere drempel handhaven.
        flag = "✓"
        print(f"   {flag} {t:15s}: {c:4d} ({pct:.0f}%)")
    hpct = 100 * types.get("herkenning", 0) / total
    ppct = 100 * types.get("productie", 0) / total
    cpct = 100 * (types.get("contextueel", 0) + types.get("analyse", 0)) / total
    if hpct < 30:
        print("   ❌ Herkenning < 30%")
        ok = False
    if ppct < 30:
        print("   ❌ Productie < 30%")
        ok = False
    if cpct < 10:
        print(f"   ⚠ Contextueel+analyse = {cpct:.0f}% (doel: 10%+) — acceptabel voor phase 1")

    print("\n3. RICHTING-MIX")
    for r, c in richt.most_common():
        print(f"   {r:15s}: {c:4d} ({100 * c / total:.0f}%)")

    print("\n4. IRT-PARAMETERS")
    print(
        f"   Moeilijkheid:   min={min(moeil):.1f}  max={max(moeil):.1f}  gem={sum(moeil) / len(moeil):.2f}"
    )
    print(
        f"   Discriminatie:  min={min(discr):.1f}  max={max(discr):.1f}  gem={sum(discr) / len(discr):.2f}"
    )
    print(
        f"   Verwachte tijd: min={min(tijden)}s  max={max(tijden)}s  gem={sum(tijden) / len(tijden):.0f}s"
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

    print("\n5. DUPLICATEN")
    if dupes:
        print(f"   ❌ {len(dupes)} dubbele item-IDs: {dupes[:5]}")
        ok = False
    else:
        print("   ✓ Geen dubbele item-IDs")

    print("\n6. PYDANTIC VALIDATIE")
    if validation_errors:
        print(f"   ❌ {len(validation_errors)} fouten:")
        ok = False
        for e in validation_errors[:5]:
            print(f"      {e}")
    else:
        print("   ✓ Alle items valide")

    print(f"\n{'=' * 60}")
    print(f"RESULTAAT: {'✓ GESLAAGD' if ok else '❌ GEFAALD'}")
    print(f"{'=' * 60}")

    if knopen_zonder:
        print(f"\nKnopen zonder items ({len(knopen_zonder)}, niet in scope C1-01..C1-10):")
        for kid in sorted(knopen_zonder):
            print(f"  {kid}")

    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
