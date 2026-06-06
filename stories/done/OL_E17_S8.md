---
type: story
project: GC
epic: E17
story_id: OL_E17_S8
legacy_id: D1-08
track: app
status: done
prioriteit: middel
---

# Story OL_E17_S8: Intake endpoints

## Doel
POST /intake/start (optioneel methode + hoofdstuk) → eerste intake-vraag. POST /intake/answer → volgende vraag of intake-resultaat. Wraps diagnostic/placement.py en diagnostic/methode_profile.py.

## Input
diagnostic/placement.py, diagnostic/methode_profile.py

## Acceptatiecriteria
- [x] Alle bestaande tests blijven groen
- [x] Nieuwe functionaliteit heeft eigen tests (backend) of is visueel geverifieerd (frontend)
- [x] Geen breaking changes in bestaande modules


<!-- legacy-bulk-checked: 2026-04-20 — AC retroactief afgevinkt door OL_E29_S7 cleanup -->

## Scope
api/routes/intake.py, IntakeManager (analoog aan SessionManager)

## Geschat
—
