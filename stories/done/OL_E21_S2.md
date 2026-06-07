---
type: story
project: GC
epic: E21
story_id: OL_E21_S2
legacy_id: F2-02
track: mentor
status: done
prioriteit: middel
---

# Story OL_E21_S2: Laatste foute antwoorden per leerling per knoop

## Doel
Een mentor opent de view van een leerling, ziet per struikel-knoop de
laatste N foute antwoorden (letterlijk), met correct-answer-snapshot en
tijdstip.  Dit maakt concrete coaching mogelijk: *"je typte `puellae`
in plaats van `puellam` — dat is genitivus, niet accusativus"*.

## Input
- `KnoopState.item_history` (gevuld door OL_E20_S12)
- `data/graph/*.json` voor knoop-titel
- `src/gymnasium_classica/api/routes/progress.py` — bestaande
  knoop-progress-endpoint ter referentie

## Acceptatiecriteria
- [x] Endpoint `GET /mentor/{user_id}/knoop/{knoop_id}/attempts?limit=10`
      — beschermd door OL_E21_S1-guard
- [x] Response bevat per attempt: timestamp, answer_text, correct_answer,
      correct (bool), response_time_ms, item_type
- [x] `null`-attempts (self-assess zonder literal answer) worden
      uitgefilterd of als zodanig gemarkeerd
- [x] Frontend-component `MentorAttemptList` toont de lijst met
      visuele diff (goed vs. ingevuld)
- [x] Pytest + component-smoketest

## Scope
- Eén leerling per keer, één knoop per keer (aggregatie komt in OL_E21_S3)
- Geen bewerkingsmogelijkheid; alleen lezen

## Geschat
Klein-medium

## Resultaat

**Backend:**
- `GET /mentor/{user_id}/knoop/{knoop_id}/attempts?limit=10` in
  `api/routes/mentor.py`, beschermd door `require_mentor_of` (OL_E21_S1).
- Schemas `MentorAttempt` / `MentorAttemptsResponse` in `api/schemas.py`.
- Filtert self-assess-pogingen (`answer_text is None`) eruit; sorteert
  nieuwste eerst; `limit` 1–100 (default 10). Onbekende knoop → 404.
  Knoop-titel uit de graph; lege lijst als er nog geen state/history is.
- 8 pytest-tests in `tests/test_api_mentor_attempts.py` (volgorde, null-
  filter, limit, metadata, leeg, 404, 403 niet-gekoppeld, 403 leerling).

**Frontend:**
- `components/MentorAttemptList.jsx` — presentational, toont per poging een
  ✓/✗-badge, het ingevulde antwoord met **char-diff** (`<mark>` op het
  afwijkende midden) t.o.v. het juiste antwoord, en het tijdstip.
- Diff-logica losgetrokken naar `components/mentorDiff.js` (react-refresh-
  lintregel: component-bestand exporteert alleen de component).
- `api.getMentorAttempts(userId, knoopId, limit)` + `getMentees()`.
- Diff-stijlen in `styles/main.css`.
- 9 vitest-tests (`MentorAttemptList.test.jsx`): diffParts-eenheid +
  component-smoketests (leeg, titel, highlight, correct-antwoord, geen
  diff bij goed).

**Buiten scope (bewust):** data-fetch/pagina-wiring van de component, en
het meesturen van de OL_E21_S4-`mismatch_type` (telemetrie slaat die nog niet
op — vervolgstap). Suites: backend 719 groen, frontend 35 groen, mypy +
ruff + eslint (eigen bestanden) schoon.
