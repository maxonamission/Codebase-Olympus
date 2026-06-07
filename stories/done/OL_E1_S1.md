---
type: story
project: GC
epic: E1
story_id: OL_E1_S1
legacy_id: A1-01
track: graph
status: done
prioriteit: middel
---

# Story OL_E1_S1: Conceptknopen en naamvalsysteem

## Doel
Conceptknopen die het Latijnse naamvalsysteem introduceren: naamval-intro, declinatie-intro, genus, numerus, casus-functies.

## Input
CvTE-minimumlijst Latijn (docs/Latijn.pdf), RESEARCH_LESSTOF_KLAS1.md, PoC-knopen

## Acceptatiecriteria
- [x] Knopen voldoen aan het ID-schema (validate_knoop_id)
- [x] Prerequisite-edges zijn correct en vormen een DAG (geen cycli)
- [x] JSON valideert tegen het Pydantic GraphData-model
- [x] validate_graph.py draait zonder errors
- [x] Beschrijving per knoop: 1-2 zinnen (kort, disambiguerend)


<!-- legacy-bulk-checked: 2026-04-20 — AC retroactief afgevinkt door OL_E29_S7 cleanup -->

## Scope
Naamval-intro, declinatie-intro, genus-intro, numerus-intro, persoon-intro, de 5 naamvalfuncties (nom/gen/dat/acc/abl), zinsdeel-intro

## Geschat aantal knopen
~15
