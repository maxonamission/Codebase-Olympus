---
type: story
project: GC
epic: E1
story_id: OL_E1_S6
legacy_id: A1-06
track: graph
status: done
prioriteit: middel
---

# Story OL_E1_S6: Werkwoord-concepten — conjugatie-intro, persoon, tempus, modus

## Doel
Conceptknopen voor het Latijnse werkwoordssysteem.

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
Conjugatie-intro, 4 conjugatie-intro's, persoon-intro, tempus-intro, modus-intro, activum/passivum-intro

## Geschat aantal knopen
~10
