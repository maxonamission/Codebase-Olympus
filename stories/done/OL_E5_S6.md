---
type: story
project: GC
epic: E5
story_id: OL_E5_S6
legacy_id: A5-06
track: graph
status: done
prioriteit: middel
---

# Story OL_E5_S6: Prerequisite-edges cultuur → taal/integratie

## Doel
Enrichment-edges van cultuurknopen naar grammatica- en vocabulaireknopen.

## Input
A1, A2, A4, OL_E5_S1 t/m OL_E5_S5

## Acceptatiecriteria
- [x] Knopen voldoen aan het ID-schema (validate_knoop_id)
- [x] Prerequisite-edges zijn correct en vormen een DAG (geen cycli)
- [x] JSON valideert tegen het Pydantic GraphData-model
- [x] validate_graph.py draait zonder errors
- [x] Beschrijving per knoop: 1-2 zinnen (kort, disambiguerend)


<!-- legacy-bulk-checked: 2026-04-20 — AC retroactief afgevinkt door OL_E29_S7 cleanup -->

## Scope
Enrichment-edges, niet prerequisite (cultuur verrijkt maar blokkeert niet)

## Geschat aantal knopen
—
