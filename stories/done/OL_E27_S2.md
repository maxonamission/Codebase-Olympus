---
type: story
project: GC
epic: E27
story_id: OL_E27_S2
legacy_id: E3-02
track: content
status: done
prioriteit: middel
---

# Story OL_E27_S2: Items voor GRC-conceptknopen

## Doel
Items voor de Griekse INTRO-knopen: naamval, numerus, genus, declinatie, conjugatie, tempus, persoon, thematische vocaal, woordstam, uitgang, lidwoord. Doel: activeren van achtergrondconcepten voordat paradigma's aan bod komen.

## Input
`data/graph/grc_grammatica_leerjaar1.json` — alle `GRC-G-MORF-*-INTRO` knopen + lidwoord-knopen (2 stuks).

## Acceptatiecriteria
- [x] Geen breaking changes in bestaande models
- [x] Alle bestaande tests blijven groen
- [x] Elke INTRO-knoop heeft minstens 2 items (herkenning + self_assess of productie)
- [x] Items voldoen aan kwaliteitseisen uit `docs/Prompt_spoor_c.md`
- [x] Geen overlap met LAT-conceptknopen — Grieks-specifieke voorbeelden (ἄνθρωπος, λόγος, γράφω)


<!-- legacy-bulk-checked: 2026-04-20 — AC retroactief afgevinkt door OL_E29_S7 cleanup -->

## Scope
~12 knopen, ~25 items.

## Geschat
~25 items
