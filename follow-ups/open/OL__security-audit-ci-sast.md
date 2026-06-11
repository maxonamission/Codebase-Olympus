---
type: follow-up
project: "OL"
status: open
aangemaakt: 2026-06-11
afgehandeld: ""
bron: "interne audit gedeelde werkwijze (analyse 2026-06-05) — reconciliatie 2026-06-11"
trigger_categorie: "review-uitkomst / vóór pilot"
---
# Follow-up — `Security-laag in CI: SAST + secret-scan nog open (AVG + EU-AI-Act reeds gedekt)`

> **Wat is dit?** Een aanbeveling uit een audit die bewust wordt geparkeerd. Pas
> wanneer de trigger hieronder afgaat, is dit formulier weer in beeld. Dit document
> is de enige plek waar het item leeft tot dat moment.

---

## Situatie

Een interne audit van de gedeelde manier van werken (2026-06-05) vergeleek de
actieve repo's en noteerde voor Gymnasium Classica drie privacy-/security-punten:
(1) AVG-bescherming voor **minderjarigen**, (2) een **EU-AI-Act**-risico-inschatting
met trigger, en (3) een geautomatiseerde **SAST + secret-scan in CI**. Bij de
reconciliatie op 2026-06-11 blijken punten 1 en 2 al belegd in `docs/security/`
(zie Relevante documenten). Punt 3 staat nog open: de CI draait ruff, mypy en
pytest, maar heeft (nog) geen statische security-analyse (bandit/CodeQL) en geen
secret-scan (gitleaks).

## Waarom geparkeerd

Het project zit in fase 0/1 (pre-pilot): lokale SQLite, geen LLM-integratie, geen
externe API's en nog geen echte leerlinggegevens in de repo. De toevoeging is
laag-risico en goedkoop, maar hoort thuis in de bredere pre-pilot security-pass —
niet er los doorheen geschoven. Bewust wachten dus, niet vergeten.

## Trigger

Vóór de eerste pilot met echte leerlingen (epic **E26 — Pilot-ready**), of eerder
zodra user-input-endpoints SQLite-queries raken, of zodra een externe API / een
LLM-mentor wordt toegevoegd.

---

## Wat er moet gebeuren als de trigger afgaat

Uitwerking in een eigen story (`track: ontwikkelstraat`); hier alleen de richting:

- **SAST in CI.** Deze repo is **publiek**, dus **CodeQL** is gratis (GitHub
  Advanced Security voor public repos) — voorkeur. Anders **bandit** als lichte
  Python-SAST (zoals een zusterrepo koos toen CodeQL niet beschikbaar was).
- **Secret-scan** (gitleaks) als CI-workflow én pre-commit-hook, met een
  `.gitleaks.toml`.
- Optioneel de security-workflow conform de codebase-standards security-profiel-laag
  (secret-scan + SAST + dependency-audit in één `security.yml`).

## Relevante documenten

- [`docs/security/dpia.md`](https://github.com/maxonamission/Codebase-Olympus/blob/main/docs/security/dpia.md) — dekt AVG + minderjarigen (profilering, ouderlijke toestemming, dataminimalisatie).
- [`docs/security/eu-ai-act-risico.md`](https://github.com/maxonamission/Codebase-Olympus/blob/main/docs/security/eu-ai-act-risico.md) — dekt de Annex III hoog-risico-toets + trigger (LLM-mentor / formele beoordeling / externe hosting).
- [`.github/workflows/ci.yml`](https://github.com/maxonamission/Codebase-Olympus/blob/main/.github/workflows/ci.yml) — huidige CI zonder SAST/secret-scan.

## Status-aantekeningen

- `2026-06-11` — Reconciliatie van de audit. AVG-minderjarigen → reeds in `dpia.md`; EU-AI-Act Annex III + trigger → reeds in `eu-ai-act-risico.md` §4/§7. Alleen de SAST/secret-scan-laag ontbreekt nog in `ci.yml`. Geen juridisch advies; de classificatie-toets blijft een eigenaar-/juridische verantwoordelijkheid.

## Afhandeling

Invullen zodra de trigger afgaat of het item vervalt. Zet dan `status: afgehandeld`
+ `afgehandeld: YYYY-MM-DD` in de front-matter en verplaats het bestand naar
`follow-ups/afgehandeld/`.

- **Trigger afgegaan**: ja / nee
- **Vervolg**: `<verwijzing naar story, commit of besluit>`
- **Vervallen**: ja / nee, en waarom
