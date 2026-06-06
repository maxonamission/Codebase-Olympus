---
type: story
project: GC
epic: E2
story_id: OL_E2_S11
legacy_id: A2-11
track: graph
status: done
prioriteit: middel
---

# Story OL_E2_S11: Review en prerequisite-edge validatie voor heel epic A2

## Doel
Cross-check van alle A2-knopen.

## Input
Alle A2-stories, validate_graph.py

## Acceptatiecriteria
- [x] Knopen voldoen aan het ID-schema (validate_knoop_id)
- [x] Prerequisite-edges zijn correct en vormen een DAG (geen cycli)
- [x] JSON valideert tegen het Pydantic GraphData-model
- [x] validate_graph.py draait zonder errors
- [x] Beschrijving per knoop: 1-2 zinnen (kort, disambiguerend)


<!-- legacy-bulk-checked: 2026-04-20 — AC retroactief afgevinkt door OL_E29_S7 cleanup -->

## Scope
DAG-validatie, edge-weight review, prerequisite naar A3 (alfabet)

## Geschat aantal knopen
—
