---
type: story
project: GC
epic: E28
story_id: OL_E28_S7
legacy_id: E7-07
track: didactiek
status: done
prioriteit: middel
---

# Story OL_E28_S7: Frontend: passage-lezer component

## Doel
React component voor het tonen van een leespassage: Latijnse/Griekse tekst met per-woord hover-annotaties (lemma, naamval, vertaling). Woorden waarvan de grammatica onbekend is worden gemarkeerd. Klik op een onbekend woord → grammatica-uitleg verschijnt.

## Input
frontend/src/components/, OL_E28_S2 passage-model

## Acceptatiecriteria
- [x] Geen breaking changes — bestaande grammar-first route blijft default
- [x] Alle bestaande tests blijven groen
- [x] Nieuwe functionaliteit heeft eigen tests


<!-- legacy-bulk-checked: 2026-04-20 — AC retroactief afgevinkt door OL_E29_S7 cleanup -->

## Scope
PassageReader component: tekst met interactieve woord-annotaties, kleurcodering per beheersingsgraad, grammatica-popup bij klik

## Geschat
—
