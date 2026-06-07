---
type: story
project: GC
epic: E6
story_id: OL_E6_S1
legacy_id: A6-01
track: graph
status: done
prioriteit: middel
---

# Story OL_E6_S1: Naamvalsysteem — LAT ↔ GRC naamvallen

## Doel
Transfer-edges tussen isomorfe naamvalconcepten Latijn ↔ Grieks.

## Input
A1, A2

## Acceptatiecriteria
- [x] Knopen voldoen aan het ID-schema (validate_knoop_id)
- [x] Prerequisite-edges zijn correct en vormen een DAG (geen cycli)
- [x] JSON valideert tegen het Pydantic GraphData-model
- [x] validate_graph.py draait zonder errors
- [x] Beschrijving per knoop: 1-2 zinnen (kort, disambiguerend)


<!-- legacy-bulk-checked: 2026-04-20 — AC retroactief afgevinkt door OL_E29_S7 cleanup -->

## Scope
LAT nom/gen/dat/acc/abl ↔ GRC nom/gen/dat/acc, declinatie-concepten, functie-knopen

## Geschat aantal knopen
~30 edges
