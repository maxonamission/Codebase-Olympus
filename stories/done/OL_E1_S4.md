---
type: story
project: GC
epic: E1
story_id: OL_E1_S4
legacy_id: A1-04
track: graph
status: done
prioriteit: middel
---

# Story OL_E1_S4: 3e declinatie — consonantstammen + i-stammen basis

## Doel
Basis van de 3e declinatie: consonantstammen en i-stammen, alle naamvallen.

## Input
CvTE-minimumlijst

## Acceptatiecriteria
- [x] Knopen voldoen aan het ID-schema (validate_knoop_id)
- [x] Prerequisite-edges zijn correct en vormen een DAG (geen cycli)
- [x] JSON valideert tegen het Pydantic GraphData-model
- [x] validate_graph.py draait zonder errors
- [x] Beschrijving per knoop: 1-2 zinnen (kort, disambiguerend)


<!-- legacy-bulk-checked: 2026-04-20 — AC retroactief afgevinkt door OL_E29_S7 cleanup -->

## Scope
rex/corpus/mare-paradigma, consonantstam vs. i-stam, alle naamvallen sg+pl, decl3-intro

## Geschat aantal knopen
~15
