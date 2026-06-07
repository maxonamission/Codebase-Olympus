---
type: story
project: GC
epic: E4
story_id: OL_E4_S7
legacy_id: A4-07
track: graph
status: done
prioriteit: middel
---

# Story OL_E4_S7: Prerequisite-edges vocabulaire → grammatica

## Doel
Elk vocabulairewoord koppelen aan de juiste declinatie/conjugatie-knoop.

## Input
A1, A2, A3, OL_E4_S2 t/m OL_E4_S6

## Acceptatiecriteria
- [x] Knopen voldoen aan het ID-schema (validate_knoop_id)
- [x] Prerequisite-edges zijn correct en vormen een DAG (geen cycli)
- [x] JSON valideert tegen het Pydantic GraphData-model
- [x] validate_graph.py draait zonder errors
- [x] Beschrijving per knoop: 1-2 zinnen (kort, disambiguerend)


<!-- legacy-bulk-checked: 2026-04-20 — AC retroactief afgevinkt door OL_E29_S7 cleanup -->

## Scope
Zelfstandige naamwoorden → declinatie, werkwoorden → conjugatie, edges type prerequisite

## Geschat aantal knopen
—
