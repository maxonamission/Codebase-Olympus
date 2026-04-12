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

## Projectstructuur

```
src/gymnasium_classica/
├── models/
│   ├── graph.py        # KennisKnoop, PrerequisiteEdge, Item, GraphData + enums
│   ├── user.py         # User, Subscription
│   └── learner.py      # LearnerModel, KnoopState, SessionRecord, ItemResponse
├── graph/
│   ├── loader.py       # JSON → NetworkX DiGraph (load_graph, graph_to_dict)
│   └── validation.py   # ValidationReport, cycle/orphan/connectivity checks
└── schemas/
    └── id_schema.py    # ID-validatie: validate_knoop_id(), parse_knoop_id()

data/
├── graph/              # Knowledge graph JSON bestanden
│   └── lat_grammatica_poc.json  # 50 Latijnse grammaticaknopen (PoC)
└── content/            # Didactische markdown content per knoop
    └── {KNOOP_ID}.md   # Bijv. LAT-G-MORF-DECL1-INTRO.md

scripts/
├── validate_graph.py   # CLI: laad graph, print ValidationReport
└── export_graph_stats.py  # CLI: knooptelling, diepte, statistieken

tests/                  # pytest tests voor alle modules
```

## ID-schema voor kennisknopen

Formaat: `{TAAL}-{TYPE}-{SEGMENT}[-{SEGMENT}]...` (3-6 segmenten, uppercase ASCII)

- **Taal:** `LAT`, `GRC`, `SHA` (shared)
- **Type:** `G` (grammatica), `V` (vocabulaire), `C` (cultuur), `I` (integratie)
- **Segmenten:** typespecifiek, max 8 chars per segment
- Conceptknopen eindigen op `-INTRO`

Voorbeelden: `LAT-G-MORF-NOM-D1`, `LAT-V-F01-ESSE`, `SHA-C-FIL-STOA`

## Content-architectuur

- **`data/graph/*.json`** — structuurdata: IDs, types, titels, Bloom-niveaus, prerequisites, IRT-params, korte beschrijving (1-2 zinnen)
- **`data/content/{KNOOP_ID}.md`** — didactische inhoud: paradigma's, uitleg, voorbeeldzinnen, veelgemaakte fouten
- `content_ref` veld in KennisKnoop verwijst naar het markdown-bestand
- **Rationale:** graph blijft lean voor in-memory laden, content evolueert onafhankelijk

## Huidige fase: Fase 0 — Fundament

Status: **compleet**. Alle deliverables zijn geïmplementeerd:
1. ✅ Projectstructuur met src/, data/, tests/, docs/, scripts/
2. ✅ Pydantic models voor KennisKnoop, PrerequisiteEdge, Item, User, Subscription, LearnerModel
3. ✅ NetworkX graph loader met validatie (cycle detection, connectivity, orphan detection, topo sort)
4. ✅ 50 Latijnse grammaticaknopen als PoC (`data/graph/lat_grammatica_poc.json`)
5. ✅ 109 tests (alle groen)

Volgende fase: **Fase 1 — Knowledge Graph uitbreiden**

## Niet doen

- Geen frontend werk in fase 0-2
- Geen LLM-integratie in fase 0-2
- Geen deployment/hosting configuratie in fase 0
- Geen over-engineering: SQLite, geen Docker, geen microservices
