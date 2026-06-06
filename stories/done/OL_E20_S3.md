---
type: story
project: GC
epic: E20
story_id: OL_E20_S3
legacy_id: F1-03
track: content
status: done
prioriteit: middel
---

# Story OL_E20_S3: Frontend rendert structured stimulus (instruction / hint / options)

## Doel
De frontend leest nu `question.item_type` en `question.options` uit een veld dat de API niet zo verstuurt (`api/session_manager.py:199-244` stuurt `items: [...]` en `stimulus: {instruction, options, audio_ref, hint}`). Gevolg: multiple-choice items renderen niet als MC maar vallen terug op "Toon antwoord"-zelfbeoordeling. Fix zodat de structured stimulus daadwerkelijk zichtbaar wordt.

## Input
- `src/gymnasium_classica/api/session_manager.py:199-244`
- `frontend/src/components/QuestionCard.jsx:10-17`
- `frontend/src/components/AnswerInput.jsx:7-51`

## Acceptatiecriteria
- [x] Voor een vocabulaire-knoop (V-type, eerste item) worden de MC-opties uit `stimulus.options` op het scherm getoond en selecteerbaar
- [x] `stimulus.instruction` wordt als prompt getoond boven de input/opties
- [x] `stimulus.hint` (bij `luister_productie`) wordt zichtbaar als Nederlandse hint
- [x] Self-assess fallback blijft werken voor items zonder `options` en zonder `hint`
- [x] Bestaande tests groen; nieuwe frontend-smoketest voor MC-flow


<!-- legacy-bulk-checked: 2026-04-20 — AC retroactief afgevinkt door OL_E29_S7 cleanup -->

## Scope
- Ofwel: eerste item in de `items`-lijst promoveren naar top-level velden (`item_type`, `options`, `hint`) in de API-response, zodat de frontend-verwachting klopt (kleine backend-shim, geen modelverandering)
- Ofwel: frontend aanpassen om direct uit `question.items[0].stimulus` te lezen
- Aanbevolen: de eerste optie — minder wijziging in frontend-componenten, simpeler typing contract

## Geschat
Klein-medium (contract-keuze + backend-adapter of frontend-refactor, beide ~½ dag)
