---
type: story
project: GC
epic: E28
story_id: OL_E28_S9
legacy_id: E7-09
track: didactiek
status: done
prioriteit: middel
---

# Story OL_E28_S9: Grammatica-scaffolding bij passages

## Doel
Wanneer een passage grammatica bevat die de leerling niet beheerst: toon een inline grammatica-uitleg (uit data/content/) met een korte oefening. De BKT-update gebeurt op de grammaticaknoop, niet op de passage.

## Input
api/session_manager.py, data/content/

## Acceptatiecriteria
- [x] Geen breaking changes — bestaande grammar-first route blijft default
- [x] Alle bestaande tests blijven groen
- [x] Nieuwe functionaliteit heeft eigen tests


<!-- legacy-bulk-checked: 2026-04-20 — AC retroactief afgevinkt door OL_E29_S7 cleanup -->

## Scope
Scaffolding-mechanisme: detecteer onbeheerste grammatica in passage → toon content_ref uitleg → mini-oefening → BKT update op grammaticaknoop

## Geschat
—
