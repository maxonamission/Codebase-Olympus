---
type: story
project: GC
epic: E6
story_id: OL_E6_S5
legacy_id: A6-05
track: graph
status: done
prioriteit: middel
---

# Story OL_E6_S5: Validatie transfer-edges — geen cycli, weights correct

## Doel
Validatie van alle transfer-edges: geen cycli, weights in [0.0, 1.0], correct type.

## Input
Alle A6-stories, validate_graph.py

## Acceptatiecriteria
- [x] Knopen voldoen aan het ID-schema (validate_knoop_id)
- [x] Prerequisite-edges zijn correct en vormen een DAG (geen cycli)
- [x] JSON valideert tegen het Pydantic GraphData-model
- [x] validate_graph.py draait zonder errors
- [x] Beschrijving per knoop: 1-2 zinnen (kort, disambiguerend)


<!-- legacy-bulk-checked: 2026-04-20 — AC retroactief afgevinkt door OL_E29_S7 cleanup -->

## Scope
Volledige DAG-validatie na toevoeging transfer-edges

## Geschat aantal knopen
—
