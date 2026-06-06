---
type: story
project: GC
epic: E28
story_id: OL_E28_S5
legacy_id: E7-05
track: didactiek
status: done
prioriteit: middel
---

# Story OL_E28_S5: Context-first scheduling strategie

## Doel
Implementeer een alternatieve scheduling strategie voor de context-first route. In plaats van topologische knoop-selectie: selecteer een passage op basis van de knowledge frontier, presenteer de passage, en introduceer de grammatica die de leerling nodig heeft om de passage te begrijpen.

## Input
scheduling/session.py, scheduling/priority.py

## Acceptatiecriteria
- [x] Geen breaking changes — bestaande grammar-first route blijft default
- [x] Alle bestaande tests blijven groen
- [x] Nieuwe functionaliteit heeft eigen tests


<!-- legacy-bulk-checked: 2026-04-20 — AC retroactief afgevinkt door OL_E29_S7 cleanup -->

## Scope
ContextFirstStrategy class met: select_passage(learner, graph) → passage + bijbehorende grammaticaknopen. Relaxed prerequisite-gate: grammatica-prereqs hoeven niet ≥0.75 te zijn als ze via een passage worden aangeboden.

## Geschat
—
