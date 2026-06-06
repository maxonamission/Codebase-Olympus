---
type: story
project: GC
epic: E9
story_id: OL_E9_S2
legacy_id: B3-02
track: pipelines
status: done
prioriteit: middel
---

# Story OL_E9_S2: STT-pipeline bouwen — transcriptie-module

## Doel
Bouw een transcriptiemodule die audio-input omzet naar tekst en vergelijkt met verwacht antwoord.

## Input
Gekozen STT-tool uit OL_E9_S1

## Acceptatiecriteria
- [x] Geen breaking changes in bestaande models
- [x] Alle bestaande tests blijven groen
- [x] Nieuwe functionaliteit heeft eigen tests


<!-- legacy-bulk-checked: 2026-04-20 — AC retroactief afgevinkt door OL_E29_S7 cleanup -->

## Scope
scheduling/stt.py met transcribe() en compare_transcription() functies

## Geschat
—
