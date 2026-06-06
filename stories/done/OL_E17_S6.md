---
type: story
project: GC
epic: E17
story_id: OL_E17_S6
legacy_id: D1-06
track: app
status: done
prioriteit: middel
---

# Story OL_E17_S6: Session endpoint: summary

## Doel
GET /session/{id}/summary → sessie-samenvatting: items geoefend, mastery-veranderingen, nieuwe stof, review.

## Input
api/session_manager.py

## Acceptatiecriteria
- [x] Alle bestaande tests blijven groen
- [x] Nieuwe functionaliteit heeft eigen tests (backend) of is visueel geverifieerd (frontend)
- [x] Geen breaking changes in bestaande modules


<!-- legacy-bulk-checked: 2026-04-20 — AC retroactief afgevinkt door OL_E29_S7 cleanup -->

## Scope
api/routes/session.py uitbreiding, SessionSummaryResponse schema

## Geschat
—
