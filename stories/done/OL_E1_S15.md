---
type: story
project: GC
epic: E1
story_id: OL_E1_S15
legacy_id: A1-15
track: graph
status: done
prioriteit: middel
---

# Story OL_E1_S15: Review en prerequisite-edge validatie voor heel epic A1

## Doel
Cross-check van alle A1-knopen: edges consistent, geen cycli, topologische orde klopt.

## Input
Alle A1-stories, validate_graph.py

## Acceptatiecriteria
- [x] Knopen voldoen aan het ID-schema (validate_knoop_id)
- [x] Prerequisite-edges zijn correct en vormen een DAG (geen cycli)
- [x] JSON valideert tegen het Pydantic GraphData-model
- [x] validate_graph.py draait zonder errors
- [x] Beschrijving per knoop: 1-2 zinnen (kort, disambiguerend)


<!-- legacy-bulk-checked: 2026-04-20 — AC retroactief afgevinkt door OL_E29_S7 cleanup -->

## Scope
Volledige DAG-validatie, edge-weight review, cross-referentie met PoC-knopen

## Geschat aantal knopen
—
