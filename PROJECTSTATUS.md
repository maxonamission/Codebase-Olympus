---
diataxis: state
project: GC
laatst-bijgewerkt: 2026-06-05
---

# PROJECTSTATUS — Gymnasium Classica

## Status-samenvatting

Fase 0/1: knowledge graph + sessie-engine + FastAPI-backend grotendeels af. Story-administratie nu op het canonieke codebase-standards-format gebracht (front-matter leidend, gedeelde drift-validator in pre-commit + CI). IDs ongewijzigd (vakinhoudelijk schema A1-01 etc.); eventuele hernummering is een aparte story.

## Dashboard

`v0.1 · 183/200 done · → B5/B6 offline-spoor · ⚠ —`

## Epic-status

| Epic | Naam | Status | Stories | Volgende stap |
|---|---|---|---|---|
| A1 | Grammatica Latijn | done | 15/15 | — |
| A2 | Grammatica Grieks | done | 11/11 | — |
| A3 | Grieks alfabet — onboarding-subgraph | done | 3/3 | — |
| A4 | Vocabulaire | done | 8/8 | — |
| A5 | Cultuur | done | 6/6 | — |
| A6 | Transfer-edges | done | 5/5 | — |
| B1 | TTS-pipeline en audio-generatie | done | 5/5 | — |
| B2 | Audio-oefentypen | done | 4/4 | — |
| B3 | STT-integratie | done | 4/4 | — |
| B4 | Pronunciation assessment (stretch goal) | backlog | 0/3 | — |
| B5 | Offline oefentypen en scheduling | done | 6/6 | — |
| B6 | OCR-pipeline | backlog | 0/5 | — |
| B7 | LLM-vertaalbeoordeling | backlog | 0/3 | — |
| B8 | Mentor-portfolio | backlog | 0/3 | — |
| C1 | Items genereren — Latijnse grammatica | done | 11/11 | — |
| C2 | Content schrijven — Latijnse grammatica | done | 5/5 | — |
| D1 | FastAPI backend | done | 8/8 | — |
| D2 | React frontend | done | 7/7 | — |
| D3 | Integratie en pilot-ready | done | 3/3 | — |
| F1 | Content-ontsluiting en kwaliteitsverbetering | actief | 14/15 | — |
| F2 | Mentor-dashboard | done | 4/4 | — |
| M1 | WKM-spiegeling — vertaalstrategie, misconcepties, bijspijkerroute | done | 4/4 | — |
| L1 | Meet- en experimenteer-infrastructuur | done | 3/3 | — |
| L2 | Learner model — receptief/productief, migreerbaar, individueel | done | 3/3 | — |
| L3 | Didactiek — worked examples, motivatie, equity | done | 3/3 | — |
| E1 | Pilot-ready — de eerste echte leerling | actief | 0/1 | — |
| E3 | Items en content voor Grieks + vocabulaire | done | 24/24 | — |
| E7 | Didactische routes — grammatica-eerst vs. context-eerst | done | 10/10 | — |
| OS | Ontwikkelstraat fase 1 — Python-baseline | actief | 11/12 | — |
| N1 | Vernederlandste code-identifiers naar Engels | done | 6/6 | — |

## Aanbevolen volgende acties

1. Offline-spoor (B5/B6) oppakken.
2. Legacy-AC opschonen zodat `--ac-gate` van warn naar error kan.
