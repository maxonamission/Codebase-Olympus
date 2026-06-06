---
type: story
project: GC
epic: E28
story_id: OL_E28_S6
legacy_id: E7-06
track: didactiek
status: done
prioriteit: middel
---

# Story OL_E28_S6: Sessie-orkestratie met passages

## Doel
Pas de sessie-orkestratie aan voor de context-first route. De 'nieuwe stof' fase begint met een leespassage. De leerling leest, probeert te begrijpen. Het systeem toont daarna de grammatica-uitleg voor de woorden/constructies die de leerling nog niet beheerst.

## Input
scheduling/session.py, api/session_manager.py

## Acceptatiecriteria
- [x] Geen breaking changes — bestaande grammar-first route blijft default
- [x] Alle bestaande tests blijven groen
- [x] Nieuwe functionaliteit heeft eigen tests


<!-- legacy-bulk-checked: 2026-04-20 — AC retroactief afgevinkt door OL_E29_S7 cleanup -->

## Scope
Context-first sessie-flow: passage → begrip-check → grammatica-scaffolding → oefening op de getoonde grammatica → herhaling passage. De warmup/cooldown fasen blijven hetzelfde.

## Geschat
—
