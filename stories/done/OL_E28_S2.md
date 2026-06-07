---
type: story
project: GC
epic: E28
story_id: OL_E28_S2
legacy_id: E7-02
track: didactiek
status: done
prioriteit: middel
---

# Story OL_E28_S2: Leespassages als content-type

## Doel
Definieer leespassages als een nieuw content-type: korte Latijnse/Griekse teksten (2-5 zinnen) met per-woord annotatie (lemma, naamval, vertaling). Een passage is gekoppeld aan meerdere grammatica- en vocabulaireknopen die erin voorkomen.

## Input
models/graph.py, data/content/

## Acceptatiecriteria
- [x] Geen breaking changes — bestaande grammar-first route blijft default
- [x] Alle bestaande tests blijven groen
- [x] Nieuwe functionaliteit heeft eigen tests


<!-- legacy-bulk-checked: 2026-04-20 — AC retroactief afgevinkt door OL_E29_S7 cleanup -->

## Scope
PassageContent model: tekst, per-woord annotaties, gekoppelde knoop_ids. Opslag in data/passages/ of als nieuw veld op integratieknopen.

## Geschat
—
