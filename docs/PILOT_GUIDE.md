# Pilot Guide — Gymnasium Classica MVP

Handleiding voor het lokaal draaien en testen van de Gymnasium Classica webapplicatie.

## Vereisten

- Python 3.11 (geen 3.13)
- Node.js 18+ en npm
- uv als Python package manager

## Installatie

### 1. Backend dependencies

```bash
uv venv
uv pip install -e ".[dev]"
```

### 2. Frontend dependencies

```bash
cd frontend
npm install
cd ..
```

### 3. Seed database (optioneel)

Maak een demo-gebruiker aan met vooringevulde voortgang:

```bash
python scripts/seed_dev.py
```

Dit maakt:
- **Gebruiker:** demo@gymnasium.nl / wachtwoord123
- **Profiel:** Fortuna hoofdstuk 3 intake, 20 knopen beheerst, 3-daagse streak

## Opstarten

Start backend en frontend tegelijk:

```bash
python scripts/run_dev.py
```

Of apart:

```bash
# Terminal 1: Backend (FastAPI op :8000)
PYTHONPATH=src uvicorn gymnasium_classica.api.app:app --reload --port 8000

# Terminal 2: Frontend (Vite op :5173)
cd frontend && npm run dev
```

Open de browser op **http://localhost:5173**.

## Walkthrough: registreer → login → sessie → dashboard

### Stap 1: Registreren

1. Open http://localhost:5173 — je komt op het inlogscherm
2. Klik op **"Registreren"** onderaan
3. Vul in:
   - E-mailadres: bijv. `leerling@test.nl`
   - Wachtwoord: minimaal 8 tekens
4. Klik **Registreren**
5. Bij succes: automatisch doorgestuurd naar het dashboard

Of gebruik het seeded account: `demo@gymnasium.nl` / `wachtwoord123`.

### Stap 2: Dashboard bekijken

Na inloggen zie je het dashboard met:
- **Statistieken:** percentage beheerst, aantal knopen, streak
- **Voortgang per domein:** progress bars voor Grammatica, Vocabulaire, Cultuur, Integratie
- **Start sessie** knop

### Stap 3: Sessie starten

1. Klik **Start sessie** op het dashboard
2. Je ziet:
   - **Fase-indicator** bovenaan (Opwarming → Nieuwe stof → Verdieping → Afkoeling)
   - **Voortgangsbalk** met vraagnummer
   - **Vraagkaart** met titel, beschrijving en stimulus

### Stap 4: Vragen beantwoorden

Per vraag zijn er drie invoermodi, afhankelijk van het vraagtype:

- **Multiple choice** (herkenning): klik op het juiste antwoord
- **Tekstveld** (productie): typ je antwoord en klik Controleer
- **Zelfbeoordeling** (fallback): kies Goed / Te langzaam / Fout

Na elk antwoord verschijnt een **feedbackkaart**:
- Groen accent = correct, rood = incorrect
- Toont het juiste antwoord bij een fout
- Toont de beheersingsverandering (bijv. 30% → 55%)
- Klik **Volgende** voor de volgende vraag

### Stap 5: Sessie-samenvatting

Na de laatste vraag verschijnt het samenvattingsscherm:
- Aantal vragen beantwoord
- Nieuwe knopen geïntroduceerd
- Knopen herhaald
- Beheersingsveranderingen per knoop (before → after)
- **Terug naar dashboard** knop

### Stap 6: Dashboard controleren

Terug op het dashboard zou je de bijgewerkte voortgang moeten zien:
- Aangepaste percentages per domein
- Bijgewerkt totaal
- Streak-teller

## Architectuur overzicht

```
Browser (:5173)  →  Vite proxy /api  →  FastAPI (:8000)  →  SQLite
     │                                       │
     └── React SPA                           ├── Knowledge graph (in-memory)
         ├── Login.jsx                       ├── BKT + SM-2 engine
         ├── Session.jsx                     └── Session manager
         └── Dashboard.jsx
```

- **Frontend:** Vite + React, plain CSS, React Router
- **Backend:** FastAPI, SQLite (JSON blobs), in-memory knowledge graph
- **Proxy:** Vite proxied `/api/*` naar `localhost:8000` (strip /api prefix)
- **Auth:** Bearer token in localStorage, meegezonden in Authorization header

## Bekende beperkingen (MVP)

- Sessie-state leeft in-memory — verdwijnt bij server restart
- Geen OAuth, alleen email/wachtwoord
- Geen real-time timer (sessiefases zijn servergestuurd)
- Seed-data is vereist voor een zinvolle demo met de seeded gebruiker
