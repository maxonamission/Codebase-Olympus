---
type: story
project: GC
epic: E12
story_id: OL_E12_S5
legacy_id: B6-05
track: pipelines
status: backlog
prioriteit: middel
---

# Story OL_E12_S5: BKT-integratie OCR — confidence-mapping

## Doel
Map OCR-resultaten naar BKT-parameters: OCR-geverifieerd = normale confidence, lage OCR-confidence = fallback naar self-report + mentor-review.

## Input
OL_E12_S2 t/m OL_E12_S4, scheduling/bkt.py

## Acceptatiecriteria
- [ ] Geen breaking changes in bestaande models
- [ ] Alle bestaande tests blijven groen
- [ ] Nieuwe functionaliteit heeft eigen tests

## Scope
OCR confidence ≥ 0.7 → normale P(G)/P(S), < 0.7 → self-report + markeer voor mentor

## Geschat
—
