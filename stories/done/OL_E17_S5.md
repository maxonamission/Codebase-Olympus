---
type: story
project: GC
epic: E17
story_id: OL_E17_S5
legacy_id: D1-05
track: app
status: done
prioriteit: middel
---

# Story OL_E17_S5: Session endpoints: start + answer

## Doel
POST /session/start → session_id + eerste vraag. POST /session/answer (session_id + response) → feedback + volgende vraag of sessie-einde.

## Input
api/session_manager.py, api/schemas.py

## Acceptatiecriteria
- [x] Alle bestaande tests blijven groen
- [x] Nieuwe functionaliteit heeft eigen tests (backend) of is visueel geverifieerd (frontend)
- [x] Geen breaking changes in bestaande modules


<!-- legacy-bulk-checked: 2026-04-20 — AC retroactief afgevinkt door OL_E29_S7 cleanup -->

## Scope
api/routes/session.py, request/response Pydantic schemas

## Geschat
—
