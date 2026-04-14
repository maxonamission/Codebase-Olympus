# Gymnasium Classica

Adaptief leersysteem voor Latijn en Grieks op VWO-gymnasiumniveau. Bereidt leerlingen voor op het staatsexamen LTC/GTC met 30 minuten per dag.

## Wat het doet

Het systeem combineert een knowledge graph met spaced repetition (SM-2), Bayesian Knowledge Tracing en Item Response Theory om een gepersonaliseerd leerpad te bieden. De kern: elke leerling krijgt exact de stof die hij nodig heeft, op het moment dat hij er klaar voor is.

**Huidige staat:** MVP in ontwikkeling. De engine en knowledge graph zijn compleet, de webapplicatie is in aanbouw.

## Projectstructuur

```
src/gymnasium_classica/
├── models/           # Pydantic models (KennisKnoop, User, LearnerModel)
├── graph/            # Knowledge graph loader + validatie (NetworkX)
├── schemas/          # ID-schema validatie
├── scheduling/       # BKT, SM-2, priority queue, sessie-orkestratie
├── diagnostic/       # Adaptieve intake (placement test)
└── api/              # FastAPI backend (in ontwikkeling)

data/
├── graph/            # Knowledge graph: 800 knopen, 1280 edges
├── content/          # Didactische markdown content per knoop
├── audio/            # Audio (TTS placeholder bestanden)
└── methode_mapping.json  # Schoolmethode → knoop-ID mapping

frontend/             # React (Vite) frontend (in ontwikkeling)
scripts/              # CLI tools: validatie, sessie, audio, werkbladen
tests/                # pytest (300+ tests)
stories/              # Epic/story tracking (todo/doing/done)
docs/                 # Briefing, ontwerpkeuzes, syllabi, prompts
```

## Knowledge Graph

800 kennisknopen over Latijn en Grieks (leerjaar 1 gymnasium):

| Component | Knopen |
|-----------|--------|
| Latijnse grammatica | ~150 |
| Griekse grammatica | ~100 |
| Grieks alfabet (onboarding) | ~47 |
| Latijns vocabulaire (F01-F03) | ~300 |
| Grieks vocabulaire (F01-F02) | ~150 |
| Gedeelde cultuurknopen | ~65 |
| Transfer-edges LAT↔GRC | ~200 |

Elke knoop heeft een type (G/V/C/I), prerequisite-edges met encompassing weights, en optioneel oefeningen (items) met IRT-parameters.

## Adaptieve engine

- **BKT** (Bayesian Knowledge Tracing): posterior mastery per knoop per leerling
- **SM-2** (SuperMemo 2): spaced repetition scheduling
- **Prioriteitswachtrij**: urgency scores op basis van vergeet-urgentie, readiness, pedagogische waarde, domeinbalans
- **Non-interference**: semantische clustering voorkomt dat verwante vocabulaire direct na elkaar wordt geoefend
- **Sessie-orkestratie**: 30-minuten sessies in 4 fasen (warmup → nieuwe stof → verdieping → cooldown)
- **Diagnostische intake**: adaptief placement test via topologische graph-traversal

## Quickstart

```bash
# Vereisten: Python 3.11
uv venv .venv --python 3.11
source .venv/bin/activate
uv pip install -e ".[dev]"

# Valideer de knowledge graph
python scripts/validate_graph.py data/graph/

# Draai een gesimuleerde sessie via CLI
python scripts/run_session.py data/graph/lat_grammatica_poc.json --simulate

# Met diagnostische intake
python scripts/run_session.py data/graph/ --simulate --intake fortuna 3

# Tests
pytest tests/ -q
```

## Tech stack

- **Python 3.11**, **uv** als package manager
- **Pydantic** voor datavalidatie
- **NetworkX** voor de knowledge graph (in-memory)
- **FastAPI** + **SQLite** voor de backend
- **React** (Vite) voor de frontend
- **pytest** (300+ tests)

## Documentatie

| Document | Inhoud |
|----------|--------|
| `docs/BRIEFING_GYMNASIUM_CLASSICA.md` | Projectvisie, architectuur, roadmap |
| `docs/ONTWERPKEUZES_GYMNASIUM_CLASSICA.md` | Vastgestelde ontwerpkeuzes |
| `docs/A_Lesstof_Latijn_Grieks.md` | Research lesstof klas 1 |
| `docs/syllabus-latijn/` | CvTE syllabus LTC 2026 (markdown) |
| `docs/syllabus-grieks/` | CvTE syllabus GTC 2026 (markdown) |
| `CLAUDE.md` | Instructies voor Claude Code sessies |

## Licentie

Nog niet vastgesteld. De CvTE-minimumlijsten zijn overheidspublicaties. Alle oefeningen en teksten zijn nieuw gecreëerd.
