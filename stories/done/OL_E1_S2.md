---
type: story
project: GC
epic: E1
story_id: OL_E1_S2
legacy_id: A1-02
track: graph
status: done
prioriteit: middel
---

# Story OL_E1_S2: 1e declinatie — alle naamvallen + paradigma

## Doel
Alle naamvalvormen van de 1e declinatie (a-stammen), enkelvoud en meervoud.

## Input
CvTE-minimumlijst, Fortuna/SPQR volgorde

## Acceptatiecriteria
- [x] Knopen voldoen aan het ID-schema (validate_knoop_id)
- [x] Prerequisite-edges zijn correct en vormen een DAG (geen cycli)
- [x] JSON valideert tegen het Pydantic GraphData-model
- [x] validate_graph.py draait zonder errors
- [x] Beschrijving per knoop: 1-2 zinnen (kort, disambiguerend)


<!-- legacy-bulk-checked: 2026-04-20 — AC retroactief afgevinkt door OL_E29_S7 cleanup -->

## Scope
puella-paradigma: nom/gen/dat/acc/abl/voc sg+pl, decl1-intro

## Geschat aantal knopen
~10
