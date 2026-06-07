---
type: story
project: GC
epic: E28
story_id: OL_E28_S1
legacy_id: E7-01
track: didactiek
status: done
prioriteit: middel
---

# Story OL_E28_S1: Route-keuze model en User-uitbreiding

## Doel
Voeg een didactische route-voorkeur toe aan het User-model: enum (grammar_first, context_first). Default: grammar_first (huidige gedrag). De keuze wordt bij onboarding gevraagd en is op elk moment te wijzigen zonder dataverlies.

## Input
models/user.py, frontend onboarding flow

## Acceptatiecriteria
- [x] Geen breaking changes — bestaande grammar-first route blijft default
- [x] Alle bestaande tests blijven groen
- [x] Nieuwe functionaliteit heeft eigen tests


<!-- legacy-bulk-checked: 2026-04-20 — AC retroactief afgevinkt door OL_E29_S7 cleanup -->

## Scope
User.learning_route: enum, onboarding UI, settings-pagina om te wisselen

## Geschat
—
