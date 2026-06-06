---
type: story
project: GC
epic: E11
story_id: OL_E11_S1
legacy_id: B5-01
track: pipelines
status: done
prioriteit: middel
---

# Story OL_E11_S1: Offline oefentype en scheduling-integratie

## Doel
Integreer offline_schrijven items in de sessie-orkestratie: inplannen aan einde van sessie, self-report opvolgflow aan begin volgende sessie.

## Input
scheduling/session.py, models/graph.py (ItemType, VerificatieMethode)

## Acceptatiecriteria
- [x] Geen breaking changes in bestaande models
- [x] Alle bestaande tests blijven groen
- [x] Nieuwe functionaliteit heeft eigen tests


<!-- legacy-bulk-checked: 2026-04-20 — AC retroactief afgevinkt door OL_E29_S7 cleanup -->

## Scope
Scheduling-logica: offline items aan einde sessie, opvolgvraag volgende sessie, self-report met verlaagde BKT-confidence

## Geschat
—
