---
type: story
project: GC
epic: E13
story_id: OL_E13_S3
legacy_id: B7-03
track: pipelines
status: backlog
prioriteit: middel
---

# Story OL_E13_S3: Integratie met BKT en conditional completion

## Doel
LLM-beoordeling van vertaling koppelen aan BKT-updates: fout in vertaling → identificeer welke grammaticaknoop de oorzaak is.

## Input
OL_E13_S2, scheduling/bkt.py, diagnostic/conditional_completion.py

## Acceptatiecriteria
- [ ] Geen breaking changes in bestaande models
- [ ] Alle bestaande tests blijven groen
- [ ] Nieuwe functionaliteit heeft eigen tests

## Scope
LLM detecteert foutbron → conditional completion op de relevante knoop

## Geschat
—
