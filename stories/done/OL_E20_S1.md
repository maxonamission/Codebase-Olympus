---
type: story
project: GC
epic: E20
story_id: OL_E20_S1
legacy_id: F1-01
track: content
status: done
prioriteit: middel
---

# Story OL_E20_S1: Frontend ScaffoldingPanel — render scaffolding_content als markdown

## Doel
De `scaffolding_content` die de backend al meestuurt (`Question.scaffolding_content`, gevuld in `session_manager._knoop_to_question`) daadwerkelijk op het scherm van de leerling krijgen. Rendering gebeurt als markdown (paradigma-tabellen en herkenningstips zijn essentieel).

## Input
- `src/gymnasium_classica/api/session_manager.py:199-244` — `_knoop_to_question` vult reeds `scaffolding_content`
- `data/content/*.md` — 36 bestaande markdowns (LAT-G)
- `frontend/src/components/QuestionCard.jsx`, `frontend/src/pages/Session.jsx:158-190`

## Acceptatiecriteria
- [x] Geen breaking changes in bestaande models/API
- [x] Alle bestaande tests blijven groen
- [x] Nieuwe component (`ScaffoldingPanel.jsx`) heeft eigen component-smoke-test
- [x] Markdown wordt als markdown gerenderd (tabellen, headings, fett/cursief), niet als platte tekst
- [x] Panel wordt alleen getoond wanneer `scaffolding_content` aanwezig is


<!-- legacy-bulk-checked: 2026-04-20 — AC retroactief afgevinkt door OL_E29_S7 cleanup -->

## Scope
- Kies/installeer een lightweight markdown-renderer (bijv. `react-markdown` + `remark-gfm` voor tabellen)
- Nieuwe component `frontend/src/components/ScaffoldingPanel.jsx`
- Inlijven in `Session.jsx` boven `QuestionCard` wanneer `question.scaffolding_content` aanwezig is
- Styling-basis in bestaande styles-folder (tabellen leesbaar, geen scroll-traps)

## Geschat
Klein (1 component + 1 dependency + 1 integratie)
