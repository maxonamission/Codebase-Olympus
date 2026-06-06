---
type: story
project: GC
epic: E1
story_id: OL_E1_S14
legacy_id: A1-14
track: graph
status: done
prioriteit: middel
---

# Story OL_E1_S14: Basissyntaxis — woordvolgorde, congruentie, ontkenning, vraagzinnen

## Doel
Basisprincipes van Latijnse zinsbouw.

## Input
CvTE-minimumlijst, PoC-knopen

## Acceptatiecriteria
- [x] Knopen voldoen aan het ID-schema (validate_knoop_id)
- [x] Prerequisite-edges zijn correct en vormen een DAG (geen cycli)
- [x] JSON valideert tegen het Pydantic GraphData-model
- [x] validate_graph.py draait zonder errors
- [x] Beschrijving per knoop: 1-2 zinnen (kort, disambiguerend)


<!-- legacy-bulk-checked: 2026-04-20 — AC retroactief afgevinkt door OL_E29_S7 cleanup -->

## Scope
SOV-woordvolgorde, subject-predicaat congruentie, non/ne, num/nonne/-ne, AcI introductie

## Geschat aantal knopen
~12
