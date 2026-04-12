# CLAUDE.md — Gymnasium Classica

## Project

Gymnasium Classica is een adaptief leersysteem voor Latijn en Grieks op VWO-gymnasiumniveau. Het combineert een knowledge graph met spaced repetition, Bayesian Knowledge Tracing en Item Response Theory. Doel: leerlingen voorbereiden op het staatsexamen LTC/GTC met 30 minuten per dag.

Lees voor de volledige context:
- `docs/BRIEFING_GYMNASIUM_CLASSICA.md` — projectvisie, architectuur, roadmap
- `docs/ONTWERPKEUZES_GYMNASIUM_CLASSICA.md` — vastgestelde ontwerpkeuzes met architecturale implicaties

## Tech stack en constraints

- **Python 3.11** (geen 3.13, geen conda)
- **uv** als package manager (`uv pip install`, `uv venv`)
- **FastAPI** backend, **SQLite** voor persistence (fase 0-3), migratie naar PostgreSQL later
- **NetworkX + JSON** voor de knowledge graph (in-memory, bestanden in `data/`)
- **React (JSX)** frontend (fase 4)
- Geen venvs in Obsidian vault of Synology-synced folders
- Encoding: UTF-8 without BOM voor alle bestanden
- Documentatie in het **Nederlands**, code (variabelen, docstrings, comments) in het **Engels**

## Werkwijze

- Schrijf geen code voordat de structuur besproken is. Begin met een plan in structured prose.
- Bij nieuwe componenten: beschrijf eerst het datamodel en de interfaces, dan de implementatie.
- Wees expliciet over wat je hebt gelezen vs. wat je aanneemt. Vlag onzekerheden.
- Gebruik type hints overal. Pydantic models voor data validation.
- Tests: pytest. Schrijf tests voor de knowledge graph (cycle detection, orphan detection, topologische sortering) en het learner model (BKT updates, SM-2 scheduling).
- Git commits: conventionele commits, Nederlands in commit messages.

## Domeinkennis

- De CvTE-minimumlijsten (Latijn en Grieks) definiëren de scope van de grammatica.
- Kennisknopen zijn van type G (grammatica), V (vocabulaire), C (cultuur), I (integratie).
- Edges zijn `prerequisite` (hard), `enrichment` (soft), of `transfer` (cross-linguïstisch).
- Het examenprogramma kent domeinen A t/m E. Het CE toetst A1, B, C. Het college-examen (staatsexamen) toetst alle domeinen inclusief een mondeling deel.
- Het pensum wisselt jaarlijks per auteur — dit is een jaarlijks wisselende module bovenop de vaste graph.

## Huidige fase: Fase 0 — Fundament

Focus:
1. Projectstructuur opzetten (src/, data/, tests/, docs/)
2. JSON schema's voor KennisKnoop, PrerequisiteEdge, Item (zie ONTWERPKEUZES sectie "Knowledge Graph schema")
3. Pydantic models die de schema's implementeren
4. NetworkX-gebaseerde graph loader met validatie (cycle detection, connectivity checks)
5. Eerste 50 Latijnse grammaticaknopen als proof of concept (`data/graph/lat_grammatica_poc.json`)

## Niet doen

- Geen frontend werk in fase 0-2
- Geen LLM-integratie in fase 0-2
- Geen deployment/hosting configuratie in fase 0
- Geen over-engineering: SQLite, geen Docker, geen microservices
