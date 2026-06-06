---
type: story
project: GC
epic: E17
story_id: OL_E17_S1
legacy_id: D1-01
track: app
status: done
prioriteit: middel
---

# Story OL_E17_S1: Project setup: FastAPI + uvicorn + SQLite

## Doel
FastAPI app scaffolding: api/ package, app.py met graph-laden bij startup, database.py met SQLite schema (users + learner_models tabellen), pyproject.toml dependencies toevoegen.

## Input
pyproject.toml, src/gymnasium_classica/graph/loader.py

## Acceptatiecriteria
- [x] Alle bestaande tests blijven groen
- [x] Nieuwe functionaliteit heeft eigen tests (backend) of is visueel geverifieerd (frontend)
- [x] Geen breaking changes in bestaande modules


<!-- legacy-bulk-checked: 2026-04-20 — AC retroactief afgevinkt door OL_E29_S7 cleanup -->

## Scope
api/__init__.py, api/app.py, api/database.py, SQLite schema, uvicorn start

## Geschat
—
