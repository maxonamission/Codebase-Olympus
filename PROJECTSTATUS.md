---
diataxis: state
project: GC
laatst-bijgewerkt: 2026-06-11
---

# PROJECTSTATUS — Gymnasium Classica

## Status-samenvatting

Fase 0/1: knowledge graph + sessie-engine + FastAPI-backend grotendeels af. Story-administratie nu op het canonieke codebase-standards-format gebracht (front-matter leidend, gedeelde drift-validator in pre-commit + CI). Story-ids gemigreerd naar het canonieke `OL_E#_S#`-format (E2_S3); epics doorlopend `E1..E30` (+ roadmap-placeholders `E31..E34`). Oude vakinhoudelijke ids (`A1-01` etc.) bewaard in front-matter `legacy_id:`, plus een `track:`-veld per story.

## Dashboard

`v0.1 · 183/201 done · → E11/E12 offline-spoor · ⚠ —`

## Epic-status

| Epic | Naam | Status | Stories | Volgende stap |
|---|---|---|---|---|
| E1 | Grammatica Latijn | done | 15/15 | — |
| E2 | Grammatica Grieks | done | 11/11 | — |
| E3 | Grieks alfabet — onboarding-subgraph | done | 3/3 | — |
| E4 | Vocabulaire | done | 8/8 | — |
| E5 | Cultuur | done | 6/6 | — |
| E6 | Transfer-edges | done | 5/5 | — |
| E7 | TTS-pipeline en audio-generatie | done | 5/5 | — |
| E8 | Audio-oefentypen | done | 4/4 | — |
| E9 | STT-integratie | done | 4/4 | — |
| E10 | Pronunciation assessment (stretch goal) | backlog | 0/3 | — |
| E11 | Offline oefentypen en scheduling | done | 6/6 | — |
| E12 | OCR-pipeline | backlog | 0/5 | — |
| E13 | LLM-vertaalbeoordeling | backlog | 0/3 | — |
| E14 | Mentor-portfolio | backlog | 0/4 | — |
| E15 | Items genereren — Latijnse grammatica | done | 11/11 | — |
| E16 | Content schrijven — Latijnse grammatica | done | 5/5 | — |
| E17 | FastAPI backend | done | 8/8 | — |
| E18 | React frontend | done | 7/7 | — |
| E19 | Integratie en pilot-ready | done | 3/3 | — |
| E20 | Content-ontsluiting en kwaliteitsverbetering | actief | 14/15 | — |
| E21 | Mentor-dashboard | done | 4/4 | — |
| E22 | WKM-spiegeling — vertaalstrategie, misconcepties, bijspijkerroute | done | 4/4 | — |
| E23 | Meet- en experimenteer-infrastructuur | done | 3/3 | — |
| E24 | Learner model — receptief/productief, migreerbaar, individueel | done | 3/3 | — |
| E25 | Didactiek — worked examples, motivatie, equity | done | 3/3 | — |
| E26 | Pilot-ready — de eerste echte leerling | actief | 0/1 | — |
| E27 | Items en content voor Grieks + vocabulaire | done | 24/24 | — |
| E28 | Didactische routes — grammatica-eerst vs. context-eerst | done | 10/10 | — |
| E29 | Ontwikkelstraat fase 1 — Python-baseline | actief | 11/12 | — |
| E30 | Vernederlandste code-identifiers naar Engels | done | 6/6 | — |

## Aanbevolen volgende acties

1. Offline-spoor (E11/E12) oppakken.
2. Legacy-AC opschonen zodat `--ac-gate` van warn naar error kan.
3. Vóór de pilot (E26): SAST + secret-scan in CI toevoegen — zie follow-up `OL__security-audit-ci-sast`.

## Follow-ups uit reviews

| Titel | Trigger | Link |
|---|---|---|
| Security-laag in CI: SAST + secret-scan (AVG + EU-AI-Act reeds gedekt) | Vóór pilot (E26) / externe API / LLM-mentor | [`OL__security-audit-ci-sast`](follow-ups/open/OL__security-audit-ci-sast.md) |
