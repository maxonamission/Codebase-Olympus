---
type: story
project: GC
epic: E3
story_id: OL_E3_S2
legacy_id: A3-02
track: graph
status: done
prioriteit: middel
---

# Story OL_E3_S2: Diakritische tekens — spiritus, accenten, iota subscriptum

## Doel
Diakritische tekens in het polytonic Grieks.

## Input
Pallas, standaard grammatica's

## Acceptatiecriteria
- [x] Knopen voldoen aan het ID-schema (validate_knoop_id)
- [x] Prerequisite-edges zijn correct en vormen een DAG (geen cycli)
- [x] JSON valideert tegen het Pydantic GraphData-model
- [x] validate_graph.py draait zonder errors
- [x] Beschrijving per knoop: 1-2 zinnen (kort, disambiguerend)


<!-- legacy-bulk-checked: 2026-04-20 — AC retroactief afgevinkt door OL_E29_S7 cleanup -->

## Scope
Spiritus asper/lenis, acutus/gravis/circumflexus, iota subscriptum, coronis

## Geschat aantal knopen
~8
