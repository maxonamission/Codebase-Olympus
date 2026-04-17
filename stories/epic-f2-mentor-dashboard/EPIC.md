# Epic F2 — Mentor-dashboard

## Doel
Mentoren en docenten in staat stellen om leerlingen op concreet niveau
te helpen.  Niet alleen *dat* een leerling struikelt op een knoop, maar
*hoe*: welke letterlijke antwoorden gaven ze, welke MC-distractors
kozen ze, zitten er patronen in (systematische naamvalsfout,
synoniem-verwarring, macron-vergeten, ...).

## Context
F1-12 heeft de datavoorraad neergelegd (`ItemResponse.answer_text`,
`correct_answer`-snapshot, `item_type` per poging in
`KnoopState.item_history`).  Dit epic bouwt de ontsluiting daarop:
rol-gebaseerde UI + aggregatie + optionele fout-classificatie.

## Afhankelijkheden
- F1-12 (done) — answer_text + item_history wiring.  Zonder deze story
  is er geen data om te tonen.
- E7-08-ish — user-rollen bestaan in het user-model (nu alleen "learner").
  Een "mentor"/"docent"-rol met relatie tot leerlingen moet erbij.

## Verhouding tot B8
`epic-b8-mentor-portfolio` richt zich op offline werk (portfolio-selectie,
OCR-confidence).  F2 is specifiek over **online** oefen-telemetrie en
foutdiagnostiek — de twee zijn complementair en kunnen later dezelfde
mentor-UI delen.

## Verhouding tot track C (fout-classificatie)
De grading-module (`scheduling/grading.py`) en `GradingResult` zijn
ontworpen zodat een fout-classificator (spelling vs naamval vs
synoniem) als uitbreiding kan worden toegevoegd.  F2-04 trekt die brug.

## Stories

| Story | Titel | Afhankelijk |
|-------|-------|-------------|
| F2-01 | Mentor-rol + leerling-koppeling in user-model | geen |
| F2-02 | Endpoint + UI: laatste N foute antwoorden per leerling per knoop | F2-01, F1-12 |
| F2-03 | Aggregatie-view: struikelpunten over een klas | F2-01 |
| F2-04 | Fout-classificatie: spelling / naamval / synoniem / macron (track C-kern) | F1-12 |

## Niet-doel
- Portfolio-selectie offline werk → B8.
- LLM-gestuurde vrije-vorm-feedback → aparte story.
- Cijferrapportage / toetsdossier → out-of-scope.

## Status
draft — nog geen stories in uitvoering, alleen skeletten.
