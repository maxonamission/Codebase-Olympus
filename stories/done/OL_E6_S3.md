---
type: story
project: GC
epic: E6
story_id: OL_E6_S3
legacy_id: A6-03
track: graph
status: done
prioriteit: middel
---

# Story OL_E6_S3: Cultuur — gedeelde mythologie en geschiedenis

## Doel
Transfer-edges tussen cultuurknopen en taalspecifieke knopen.

## Input
A1, A2, A5

## Acceptatiecriteria
- [x] Knopen voldoen aan het ID-schema (validate_knoop_id)
- [x] Prerequisite-edges zijn correct en vormen een DAG (geen cycli)
- [x] JSON valideert tegen het Pydantic GraphData-model
- [x] validate_graph.py draait zonder errors
- [x] Beschrijving per knoop: 1-2 zinnen (kort, disambiguerend)


<!-- legacy-bulk-checked: 2026-04-20 — AC retroactief afgevinkt door OL_E29_S7 cleanup -->

## Scope
Mythologie → LAT/GRC vocabulaire, geschiedenis → LAT/GRC context

## Geschat aantal knopen
~20 edges
