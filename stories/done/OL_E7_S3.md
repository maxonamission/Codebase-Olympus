---
type: story
project: GC
epic: E7
story_id: OL_E7_S3
legacy_id: B1-03
track: pipelines
status: done
prioriteit: middel
---

# Story OL_E7_S3: TTS-pipeline bouwen — audio-generatiescript

## Doel
Bouw een script dat gegeven een lijst lemma's en taal/uitspraakkeuze audiobestanden genereert en opslaat in data/audio/.

## Input
Gekozen TTS-tool uit OL_E7_S1/OL_E7_S2

## Acceptatiecriteria
- [x] Geen breaking changes in bestaande models
- [x] Alle bestaande tests blijven groen
- [x] Nieuwe functionaliteit heeft eigen tests


<!-- legacy-bulk-checked: 2026-04-20 — AC retroactief afgevinkt door OL_E29_S7 cleanup -->

## Scope
scripts/generate_audio.py, input: lemma-lijst, output: data/audio/{knoop_id}.mp3

## Geschat
—
