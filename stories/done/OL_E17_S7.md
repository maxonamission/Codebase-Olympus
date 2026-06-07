---
type: story
project: GC
epic: E17
story_id: OL_E17_S7
legacy_id: D1-07
track: app
status: done
prioriteit: middel
---

# Story OL_E17_S7: Progress endpoints

## Doel
GET /progress/overview → knopen per status (beheerst/in-progress/onbekend), per domein (G/V/C/I), streak. GET /progress/knoop/{id} → detail per knoop.

## Input
models/learner.py, api/database.py

## Acceptatiecriteria
- [x] Alle bestaande tests blijven groen
- [x] Nieuwe functionaliteit heeft eigen tests (backend) of is visueel geverifieerd (frontend)
- [x] Geen breaking changes in bestaande modules


<!-- legacy-bulk-checked: 2026-04-20 — AC retroactief afgevinkt door OL_E29_S7 cleanup -->

## Scope
api/routes/progress.py, ProgressOverview/KnoopDetail response schemas

## Geschat
—
