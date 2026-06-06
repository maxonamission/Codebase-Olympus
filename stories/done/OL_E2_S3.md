---
type: story
project: GC
epic: E2
story_id: OL_E2_S3
legacy_id: A2-03
track: graph
status: done
prioriteit: middel
---

# Story OL_E2_S3: 2e declinatie (ο-stammen)

## Doel
Griekse 2e declinatie: o-stammen masculinum en neutrum.

## Input
CvTE-minimumlijst Grieks

## Acceptatiecriteria
- [x] Knopen voldoen aan het ID-schema (validate_knoop_id)
- [x] Prerequisite-edges zijn correct en vormen een DAG (geen cycli)
- [x] JSON valideert tegen het Pydantic GraphData-model
- [x] validate_graph.py draait zonder errors
- [x] Beschrijving per knoop: 1-2 zinnen (kort, disambiguerend)


<!-- legacy-bulk-checked: 2026-04-20 — AC retroactief afgevinkt door OL_E29_S7 cleanup -->

## Scope
λόγος-paradigma, ἔργον-paradigma, alle naamvallen sg+pl

## Geschat aantal knopen
~10
