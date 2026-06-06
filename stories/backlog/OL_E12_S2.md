---
type: story
project: GC
epic: E12
story_id: OL_E12_S2
legacy_id: B6-02
track: pipelines
status: backlog
prioriteit: middel
---

# Story OL_E12_S2: OCR Grieks alfabet — letterherkenning

## Doel
OCR-pipeline specifiek voor Griekse lettervormen. Hoogste prioriteit: blokkeert progressie.

## Input
OL_E11_S6 (schrijfoefeningen alfabet), Transkribus of Vision API

## Acceptatiecriteria
- [ ] Geen breaking changes in bestaande models
- [ ] Alle bestaande tests blijven groen
- [ ] Nieuwe functionaliteit heeft eigen tests

## Scope
Per-letter confidence score, feedback bij verkeerde vorm, fallback naar self-report bij confidence < 0.7

## Geschat
—
