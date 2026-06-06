---
type: story
project: GC
epic: E19
story_id: OL_E19_S1
legacy_id: D3-01
track: app
status: done
prioriteit: middel
---

# Story OL_E19_S1: Dev server script + CORS + proxy

## Doel
scripts/run_dev.py dat zowel FastAPI (uvicorn) als Vite dev-server start. CORS-configuratie in FastAPI. Vite proxy /api → backend.

## Input
OL_E17_S1, OL_E18_S1

## Acceptatiecriteria
- [x] Alle bestaande tests blijven groen
- [x] Nieuwe functionaliteit heeft eigen tests (backend) of is visueel geverifieerd (frontend)
- [x] Geen breaking changes in bestaande modules


<!-- legacy-bulk-checked: 2026-04-20 — AC retroactief afgevinkt door OL_E29_S7 cleanup -->

## Scope
scripts/run_dev.py, CORS middleware in app.py, vite.config.js proxy

## Geschat
—
