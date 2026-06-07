---
type: story
project: GC
epic: E4
story_id: OL_E4_S1
legacy_id: A4-01
track: graph
status: done
prioriteit: middel
---

# Story OL_E4_S1: Strategie en bronnen — DCC Latin/Greek Core, cluster-definitie

## Doel
Definieer de vocabulaire-strategie: bronnen, frequentiecriteria, en update data/vocabulaire_clusters.json.

## Input
DCC Latin Core, DCC Greek Core, bestaande clusters

## Acceptatiecriteria
- [x] Knopen voldoen aan het ID-schema (validate_knoop_id)
- [x] Prerequisite-edges zijn correct en vormen een DAG (geen cycli)
- [x] JSON valideert tegen het Pydantic GraphData-model
- [x] validate_graph.py draait zonder errors
- [x] Beschrijving per knoop: 1-2 zinnen (kort, disambiguerend)


<!-- legacy-bulk-checked: 2026-04-20 — AC retroactief afgevinkt door OL_E29_S7 cleanup -->

## Scope
Bronkeuze, frequentiedrempels, mapping naar semantische clusters, selectiecriteria leerjaar 1

## Geschat aantal knopen
—
