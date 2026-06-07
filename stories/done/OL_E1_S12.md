---
type: story
project: GC
epic: E1
story_id: OL_E1_S12
legacy_id: A1-12
track: graph
status: done
prioriteit: middel
---

# Story OL_E1_S12: Pronomina — persoonlijk, bezittelijk, aanwijzend begin

## Doel
Persoonlijke voornaamwoorden (ego, tu, is/ea/id), bezittelijke (meus, tuus, suus), aanwijzende (hic, ille).

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
ego/tu/nos/vos, is/ea/id, meus/tuus/suus/noster/vester, hic/ille

## Geschat aantal knopen
~12
