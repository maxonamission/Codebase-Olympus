---
type: story
project: GC
epic: E3
story_id: OL_E3_S1
legacy_id: A3-01
track: graph
status: done
prioriteit: middel
---

# Story OL_E3_S1: Letters herkenning — 24 letters, majuskel + minuskel

## Doel
De 24 letters van het Griekse alfabet als individuele of gegroepeerde knopen.

## Input
Standaard Grieks alfabet, Pallas les 1

## Acceptatiecriteria
- [x] Knopen voldoen aan het ID-schema (validate_knoop_id)
- [x] Prerequisite-edges zijn correct en vormen een DAG (geen cycli)
- [x] JSON valideert tegen het Pydantic GraphData-model
- [x] validate_graph.py draait zonder errors
- [x] Beschrijving per knoop: 1-2 zinnen (kort, disambiguerend)


<!-- legacy-bulk-checked: 2026-04-20 — AC retroactief afgevinkt door OL_E29_S7 cleanup -->

## Scope
α-ω, majuskel+minuskel, naam+klank, gegroepeerd naar visuele gelijkenis met Latijn

## Geschat aantal knopen
~24
