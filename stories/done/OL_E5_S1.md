---
type: story
project: GC
epic: E5
story_id: OL_E5_S1
legacy_id: A5-01
track: graph
status: done
prioriteit: middel
---

# Story OL_E5_S1: Mythologie — Olympische goden, helden, Troje, Odysseus

## Doel
Mythologische cultuurknopen (SHA-C-MYT-*).

## Input
Standaard mythologie, schoolmethoden, CvTE cultuurlijst

## Acceptatiecriteria
- [x] Knopen voldoen aan het ID-schema (validate_knoop_id)
- [x] Prerequisite-edges zijn correct en vormen een DAG (geen cycli)
- [x] JSON valideert tegen het Pydantic GraphData-model
- [x] validate_graph.py draait zonder errors
- [x] Beschrijving per knoop: 1-2 zinnen (kort, disambiguerend)


<!-- legacy-bulk-checked: 2026-04-20 — AC retroactief afgevinkt door OL_E29_S7 cleanup -->

## Scope
Zeus/Jupiter, Athena/Minerva, Apollo, Troje, Odysseus, Herakles, Theseus, scheppingsmythen

## Geschat aantal knopen
~20
