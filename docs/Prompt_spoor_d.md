# Prompt: Spoor D — Werkende MVP-applicatie (FastAPI + React)

## Context

De engine is compleet: knowledge graph (800 knopen, 1080 edges), sessie-orkestratie (BKT, SM-2, priority queue, non-interference), diagnostische intake, en ~310 items voor Latijnse grammatica. De CLI (`scripts/run_session.py`) draait sessies. Wat ontbreekt is een webapplicatie waar een leerling in de browser een sessie kan doorlopen.

**Doel:** een werkend MVP dat je in de browser kunt demonstreren. Een leerling kan inloggen, een sessie starten, vragen beantwoorden, feedback zien, en zijn voortgang bekijken. Geen productie-deploy — een lokale dev-server volstaat.

Lees eerst:
- `CLAUDE.md` — tech stack (FastAPI, SQLite, React), projectstructuur
- `src/gymnasium_classica/scheduling/session.py` — de `run_session()` functie en `AnswerFn` callback
- `src/gymnasium_classica/models/user.py` — User en Subscription models
- `src/gymnasium_classica/models/learner.py` — LearnerModel, KnoopState, OfflineAssignment
- `scripts/run_session.py` — de bestaande CLI die als referentie dient

## Architectuurbeslissingen

### Backend: FastAPI + SQLite

De sessie-engine (`run_session`) werkt nu synchroon met een `answer_fn` callback. Voor een web-API moet dit omgebouwd worden naar een **stapsgewijs protocol**:

1. Client vraagt een sessie aan → server berekent de eerste vraag
2. Server stuurt de vraag (knoop_id, titel, beschrijving, stimulus, fase)
3. Client stuurt het antwoord (response_type, response_time_ms)
4. Server verwerkt (BKT + SM-2), berekent de volgende vraag
5. Herhaal tot sessie afgelopen → server stuurt samenvatting

Dit is een **stateful sessie**. De state (welke fase, welke knopen al gezien, non-interference state, tijdbudget) moet server-side leven. Twee opties:

- **Optie A: In-memory sessie-state** met een session-ID. Simpel, maar verdwijnt bij server restart. Goed genoeg voor MVP.
- **Optie B: SQLite-persisted sessie-state.** Robuuster maar complexer.

**Keuze: Optie A voor MVP.** Sessie-state in een dict, geïndexeerd op session_id. Learner-state wordt per mutatie naar SQLite geschreven.

### Persistence: SQLite

De Pydantic models (User, LearnerModel) worden opgeslagen als JSON-blobs in SQLite. Geen ORM — dat is over-engineering voor deze fase.

```sql
CREATE TABLE users (
    id TEXT PRIMARY KEY,          -- UUID
    email TEXT UNIQUE NOT NULL,
    data TEXT NOT NULL             -- JSON: volledige User model
);

CREATE TABLE learner_models (
    user_id TEXT PRIMARY KEY,
    data TEXT NOT NULL             -- JSON: volledige LearnerModel
);
```

De knowledge graph wordt bij server start in-memory geladen via `load_graph()` — dat verandert niet.

### Frontend: React (Vite)

Minimale React-app met Vite. Geen component-library — plain CSS of Tailwind. Drie schermen:

1. **Login/Registratie** — email + wachtwoord (lokaal, geen OAuth in MVP)
2. **Sessie** — de 30-minuten leerervaring: vraag, antwoordinvoer, feedback, fase-indicator, timer
3. **Dashboard** — voortgangsoverzicht: hoeveel knopen beheerst, per domein, streak

## Drie epics

### Epic D1: FastAPI backend

**Doel:** REST API die de sessie-engine exposed. SQLite persistence voor users en learner models.

**Bestanden:**
```
src/gymnasium_classica/
├── api/
│   ├── __init__.py
│   ├── app.py              # FastAPI app, CORS, startup (graph laden)
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py          # POST /auth/register, POST /auth/login
│   │   ├── session.py       # POST /session/start, POST /session/answer, GET /session/summary
│   │   └── progress.py      # GET /progress/overview, GET /progress/knoop/{id}
│   ├── schemas.py           # Pydantic request/response models voor de API
│   ├── database.py          # SQLite connection, CRUD voor users en learner_models
│   └── session_manager.py   # In-memory sessie-state, bridge tussen API en run_session
```

**Dependencies toe te voegen aan pyproject.toml:**
```toml
"fastapi>=0.110",
"uvicorn[standard]>=0.29",
```

**API endpoints:**

| Method | Path | Beschrijving |
|--------|------|-------------|
| POST | `/auth/register` | Registreer user (email, wachtwoord) → user_id + token |
| POST | `/auth/login` | Login → token |
| POST | `/session/start` | Start een sessie → session_id + eerste vraag |
| POST | `/session/answer` | Beantwoord huidige vraag → feedback + volgende vraag (of sessie-einde) |
| GET | `/session/{id}/summary` | Sessie-samenvatting |
| GET | `/progress/overview` | Voortgangsoverzicht: knopen per status, domeinen, streak |
| GET | `/progress/knoop/{knoop_id}` | Detail per knoop: posterior, history, items |
| POST | `/intake/start` | Start diagnostische intake |
| POST | `/intake/answer` | Beantwoord intake-vraag |

**SessionManager (de cruciale bridge):**

`run_session()` verwacht een synchrone `answer_fn` callback — die werkt niet met een request/response API. De SessionManager vervangt dit:

```python
class SessionManager:
    """Manages active sessions as a step-by-step protocol."""
    
    def start_session(self, user_id, graph) -> tuple[str, Question]:
        """Start a new session, return session_id and first question."""
    
    def submit_answer(self, session_id, response, time_ms) -> AnswerResult:
        """Process answer, return feedback + next question (or session end)."""
    
    def get_summary(self, session_id) -> SessionSummary:
        """Return session summary after completion."""
```

Intern gebruikt de SessionManager dezelfde BKT, SM-2, priority queue en non-interference logica als `run_session()`, maar stap-voor-stap in plaats van in een loop.

### Epic D2: React frontend

**Doel:** Minimale maar functionele UI voor de leerervaring.

**Structuur:**
```
frontend/
├── package.json
├── vite.config.js
├── index.html
├── src/
│   ├── main.jsx
│   ├── App.jsx
│   ├── api.js              # Fetch wrapper voor backend calls
│   ├── pages/
│   │   ├── Login.jsx
│   │   ├── Session.jsx      # De kern: vraag + antwoord + feedback
│   │   └── Dashboard.jsx    # Voortgangsoverzicht
│   ├── components/
│   │   ├── QuestionCard.jsx  # Toont stimulus, antwoordopties
│   │   ├── FeedbackCard.jsx  # Toont feedback na antwoord
│   │   ├── PhaseIndicator.jsx # Warmup/Nieuw/Verdieping/Cooldown
│   │   ├── ProgressBar.jsx   # Sessie-voortgang
│   │   └── MasteryHeatmap.jsx # Simpele visualisatie per domein
│   └── styles/
│       └── main.css
```

**Drie pagina's:**

**Login.jsx:**
- Email + wachtwoord invoer
- Registratie of login
- Na succes: redirect naar Session of Dashboard

**Session.jsx (de kern):**
- Toont de huidige vraag: knoop-titel, beschrijving, stimulus
- Fase-indicator bovenaan (warmup → nieuw → verdieping → cooldown)
- Timer (optioneel, voor tijdsdruk-gevoel)
- Antwoordinvoer:
  - Voor herkenning: multiple choice (4 opties)
  - Voor productie: tekstveld
  - Voor alle types: correct/slow/incorrect self-assessment als fallback
- Na antwoord: feedback-kaart met uitleg
- "Volgende" knop → volgende vraag
- Aan het einde: sessie-samenvatting (knopen geoefend, mastery-veranderingen)

**Dashboard.jsx:**
- Voortgang per domein (G/V/C/I): percentage beheerst
- Totaal knopen beheerst / totaal
- Streak (dagen achtereen geoefend)
- "Start sessie" knop

### Epic D3: Integratie en pilot-ready

**Doel:** Alles draait samen als één applicatie.

- `scripts/run_dev.py` — start zowel de FastAPI backend als de Vite dev-server
- Dev-configuratie: CORS correct, API proxy in Vite config
- Smoke test: registreer, login, start sessie, beantwoord 5 vragen, bekijk dashboard
- Seed-script: `scripts/seed_dev.py` — maak een test-user met intake-profiel aan

## Stories per epic

### Epic D1: FastAPI backend (8 stories)

| Story | Titel | Scope |
|-------|-------|-------|
| D1-01 | Project setup: FastAPI + uvicorn + SQLite | pyproject.toml deps, api/ package, database.py met schema, app.py met startup |
| D1-02 | Auth endpoints: register + login | /auth/register, /auth/login, simpele token (JWT of UUID), password hashing |
| D1-03 | Database CRUD: users + learner_models | save/load User en LearnerModel als JSON in SQLite |
| D1-04 | SessionManager: stapsgewijs sessie-protocol | De bridge tussen API en sessie-engine, in-memory state |
| D1-05 | Session endpoints: start + answer | /session/start, /session/answer met SessionManager |
| D1-06 | Session endpoint: summary | /session/{id}/summary |
| D1-07 | Progress endpoints | /progress/overview, /progress/knoop/{id} |
| D1-08 | Intake endpoints | /intake/start, /intake/answer (wraps diagnostic/placement.py) |

### Epic D2: React frontend (7 stories)

| Story | Titel | Scope |
|-------|-------|-------|
| D2-01 | Project setup: Vite + React + routing | frontend/ dir, package.json, vite.config.js, React Router, api.js fetch wrapper |
| D2-02 | Login pagina | Email/wachtwoord form, register/login toggle, token opslaan in localStorage |
| D2-03 | Session pagina: vraag tonen | QuestionCard component, fase-indicator, timer |
| D2-04 | Session pagina: antwoord + feedback | Antwoordinvoer (MC + tekstveld + self-assess), FeedbackCard, volgende-knop |
| D2-05 | Session pagina: samenvatting | Einde-scherm met mastery-veranderingen, "terug naar dashboard" |
| D2-06 | Dashboard pagina | Voortgang per domein, totaal beheerst, streak, "start sessie" knop |
| D2-07 | Polytonic Greek input | Tekstveld met ondersteuning voor Griekse diakritische tekens (soft keyboard of input helper) |

### Epic D3: Integratie (3 stories)

| Story | Titel | Scope |
|-------|-------|-------|
| D3-01 | Dev server script + CORS + proxy | scripts/run_dev.py, Vite proxy config, CORS in FastAPI |
| D3-02 | Seed script: test-user met intake | scripts/seed_dev.py, Fortuna profiel, 20 knopen mastered |
| D3-03 | End-to-end smoke test | Registreer → login → start sessie → beantwoord → dashboard. Documenteer in docs/PILOT_GUIDE.md |

## Afhankelijkheden

```
D1-01 → D1-02 → D1-03 → D1-04 → D1-05 → D1-06 → D1-07 → D1-08
                                     ↓
D2-01 → D2-02 ─────────────────→ D2-03 → D2-04 → D2-05
                                                      ↓
                                  D2-06 ←─────────────┘
                                  D2-07 (onafhankelijk)

D3-01 (na D1-01 + D2-01)
D3-02 (na D1-03)
D3-03 (na D1-08 + D2-06)
```

**Parallel mogelijk:**
- D1 en D2-01+02 kunnen parallel (backend en frontend setup + login)
- D2-03+ heeft D1-05 nodig (session endpoints)
- D2-07 (Greek input) is onafhankelijk, kan altijd

## Timeout-preventie

- **Eén story per keer.** D1-stories zijn compact (één endpoint per story).
- **Frontend: geen grote JSX-blokken inline.** Schrijf components als aparte bestanden.
- **Test na elke story.** Backend: `pytest`. Frontend: dev-server start, pagina laadt.
- **Commit na elke story.**

## Werkwijze per D1-story (backend)

1. Lees de story-beschrijving
2. Implementeer het endpoint / de module
3. Schrijf tests in `tests/test_api_*.py` (gebruik FastAPI TestClient)
4. Run `pytest tests/ -q` — moet groen
5. Commit: `feat(api): [story-id] — [korte beschrijving]`

## Werkwijze per D2-story (frontend)

1. Lees de story-beschrijving
2. Implementeer de component/pagina
3. Start dev-server (`npm run dev`), verifieer visueel
4. Commit: `feat(frontend): [story-id] — [korte beschrijving]`

## Kwaliteitseisen

- Backend: alle endpoints retourneren Pydantic-gevalideerde responses
- Frontend: responsive (desktop + tablet), clean layout, Nederlands UI-tekst
- Geen hardcoded data — alles komt uit de API
- Error handling: backend retourneert duidelijke HTTP errors, frontend toont ze
- Geen over-engineering: geen Redux, geen component library, geen Docker
