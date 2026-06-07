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

## Ontwikkelstraat

Kwaliteit wordt automatisch afgedwongen in zes lagen. Achtergrond: `docs/ontwikkelstraat-uitleg.md`.

### Laag 1 — Lint & types

- **Lint/format**: `uv run ruff check .` + `uv run ruff format --check .`. Regelkeuze in `pyproject.toml`. `RUF001-003` op ignore: Griekse tekens zijn kernfunctionaliteit, niet ambigu.
- **Type-checking**: `uv run mypy src/`. `strict = true` op `src/`; `tests/` en `scripts/` uitgezonderd. Pydantic-plugin actief. Nieuwe code moet mypy-groen zijn.

### Laag 2 — Pre-commit

- Eenmalig per checkout: `uv run pre-commit install`. Daarna draait elke commit automatisch door ruff-check + format, mypy, whitespace/EOF, yaml/toml/json-validatie, private-key-detector, large-file-check en de story-status-check (zie Laag 6).
- Handmatig over de hele repo: `uv run pre-commit run --all-files`.
- Bij faling: hooks auto-fixen waar mogelijk; anders fouten lezen, fixen, opnieuw stagen.

### Laag 3 — Claude Code hooks

- `.claude/settings.json` definieert twee hooks die vanuit elke sessie draaien:
  - **PostToolUse** (`Edit`/`Write` op `.py`) → `.claude/hooks/ruff_on_python.sh` (ruff fix + format op het gewijzigde bestand).
  - **Stop** → `.claude/hooks/pytest_on_stop.sh` (`pytest -x --tb=short`; blokkeert de Stop bij rode tests).
- Persoonlijke overrides in `.claude/settings.local.json` (gitignored).

### Laag 4 — CI (GitHub Actions)

- Workflow `.github/workflows/ci.yml` draait op elke push en PR: dezelfde checks als pre-commit (ruff, mypy, story-status) plus `pytest --cov`. Pre-commit kun je lokaal overslaan; CI niet.
- Status-badge in `README.md`; branch protection op `main` hoort CI verplicht te maken (handmatige GitHub-instelling).

### Laag 5 — Review-skills

- `/review` draaien vóór elke PR-merge en commentaar verwerken.
- `/security-review` **verplicht** bij wijzigingen in: auth/token-afhandeling, sqlite-queries, user-input-endpoints, externe API-calls, dependency-upgrades. Optioneel bij de rest.
- PR-template (`.github/pull_request_template.md`) bevat de volledige checklist.

### Laag 6 — Story-workflow

Zie `## Story-workflow` hieronder. Handhaving via de gevendorde codebase-standards-scripts (`sync_story_folders.py` + `regenerate_status.py` + `check_story_status.py --ac-gate=warn`), geïntegreerd in pre-commit en CI.

## Story-workflow

Stories staan onder `stories/` met subfolders `backlog/`, `doing/`, `done/` + centrale `stories/EPICS.md`. Sinds de codebase-standards-adoptie (OS-11) is de **front-matter `status:`** van een story de bron van waarheid; de map wordt daar automatisch op gehouden. Elke story heeft een front-matter-blok:

```
---
type: story
project: GC
epic: E1
story_id: OL_E1_S1
legacy_id: A1-01
track: graph
status: backlog        # backlog | doing | done
prioriteit: middel
---
```

> Sinds E2_S3 (codebase-standards) dragen story-ids het canonieke `OL_E#_S#`-format en epics een doorlopend `E#` (statustabel-volgorde; oude spoor-labels A–F/OS/E1/E3/E7 → `E1..E30`, story-loze roadmap-placeholders → `E31..E34`). Het oude vakinhoudelijke id (`A1-01`, `B4-02`) staat in front-matter `legacy_id:`; het `track:`-veld (`graph`/`pipelines`/`mentor`/`content`/`app`/`didactiek`/`learner`/`ontwikkelstraat`) vervangt de oude spoor-letter als werkstroom-as. De gedeelde validator blijft ID-schema-agnostisch.

**Bij oppakken / afronden van een story:**

1. Pas het `status:`-veld in de front-matter aan (`backlog` → `doing` → `done`). De pre-commit-hook `sync-story-folders` verplaatst het bestand via `git mv` naar de juiste map.
2. Bij afronden: vink alle `- [ ]` in `## Acceptatiecriteria` om naar `- [x]`. Een `done`-story met openstaande AC **blokkeert de CI** (de AC-gate staat sinds juni 2026 hard op `error`; legacy-opruiming is afgerond). Voeg eventueel een resultaat-blok toe.
3. De pre-commit-hook `regenerate-status` werkt de tellingen in `stories/EPICS.md` (Statustabel) en `PROJECTSTATUS.md` automatisch bij — counts hoef je nooit met de hand te tellen.
4. Draai lokaal `uv run python scripts/check_story_status.py --mode=full --ac-gate=error --format-gate=error` — moet groen zijn (gelijk aan de CI-gate).
5. Commit en push; pre-commit en CI valideren dezelfde regels.

**De check blokkeert (CI) als:** map ≠ front-matter `status:`, EPICS/PROJECTSTATUS-tellingen ≠ filesystem, een `done`-epic nog open stories heeft, **of een `done`-story openstaande AC heeft** (`--ac-gate=error`). Orphans/dead-refs blijven waarschuwingen.

**Herkomst:** deze werkwijze komt uit [`codebase-standards`](https://github.com/maxonamission/codebase-standards) (v0.6.0; gevendord in `scripts/`, versie-stempel `.codebase-standards-version`, drift bewaakt via `.codebase-standards-manifest.json`). Wijzigingen aan de gedeelde werkwijze lopen via die repo, niet hier.

## Output en sessie-management

De API heeft een idle timeout (~60s). Voorkom timeouts door:

- **Werk in kleine stappen.** Eén story per keer, niet meerdere stories in één response. Commit na elke afgeronde story.
- **Genereer grote JSON via scripts, niet inline.** Schrijf een Python-script dat de knopen genereert, valideert en opslaat. Toon de samenvatting (aantal knopen, edges, validatie-uitkomst), niet de volledige JSON.
- **Beperk tool-output.** Gebruik `| tail -N` of `| head -N` bij lange commando-output. Toon alleen relevante delen van testresultaten.
- **Splits grote bestanden.** Lees bestanden met `offset` en `limit`, niet in één keer als ze >150 regels zijn.
- **Geen volledige bestanden herhalen.** Bij edits: toon alleen wat er veranderd is, niet het hele bestand.
- **Commit vroeg en vaak.** Na elke story of logische eenheid. Niet wachten tot het einde van een sessie.
- **Stop-hook draait `pytest`.** De Claude Code Stop-hook blokkeert de sessie-afronding bij rode tests. Plan commits dus vóór het einde van een sessie, en verwacht bij een rood testresultaat een extra iteratie — niet het einde van de turn.

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
├── graph/                              # Knowledge graph JSON bestanden
│   ├── lat_grammatica_poc.json         # 50 Latijnse grammaticaknopen (smoke test)
│   ├── lat_grammatica_leerjaar1.json   # Extra Latijnse grammatica (~100 knopen)
│   ├── grc_alfabet.json                # Grieks alfabet onboarding (~40 knopen)
│   ├── grc_grammatica_leerjaar1.json   # Griekse grammatica (~100 knopen)
│   ├── lat_vocabulaire_leerjaar1.json  # Latijns vocabulaire (~300 knopen)
│   ├── grc_vocabulaire_leerjaar1.json  # Grieks vocabulaire (~200 knopen)
│   └── sha_cultuur_leerjaar1.json      # Gedeelde cultuurknopen (~70 knopen)
└── content/                            # Didactische markdown content per knoop
    └── {KNOOP_ID}.md                   # Bijv. LAT-G-MORF-DECL1-INTRO.md

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

## Huidige fase: Fase 0/1 — Fundament + Knowledge Graph MVP

### Fase 0 — Fundament (compleet)
1. ✅ Projectstructuur met src/, data/, tests/, docs/, scripts/
2. ✅ Pydantic models voor KennisKnoop, PrerequisiteEdge, Item, User, Subscription, LearnerModel
3. ✅ NetworkX graph loader met validatie + directory-loading (meerdere JSON bestanden)
4. ✅ 50 Latijnse grammaticaknopen als smoke test (`data/graph/lat_grammatica_poc.json`)
5. ✅ 113 tests (alle groen)

### Fase 1 — MVP Knowledge Graph (in uitvoering)

**Scope: leerjaar 1 gymnasium, beide talen.** Model: scholen als het Vossius die Latijn én Grieks vanaf dag 1 aanbieden. Externe validatie door een klassieke-taleninstituut.

**Doelomvang: ~850 knopen, ~1500-2000 edges**

| Component | Knopen | Status |
|-----------|--------|--------|
| Latijnse grammatica (decl. 1-5, conj. 1-4, perf., passief, syntax) | ~150 | 50 PoC ✅, ~100 uit te breiden |
| Grieks alfabet onboarding-subgraph | ~40 | Te bouwen |
| Griekse grammatica (o-/a-/3e decl., presens/impf., medium, syntax) | ~100 | Te bouwen |
| Latijns vocabulaire (frequentiegestuurd, individuele woorden) | ~300 | Te bouwen |
| Grieks vocabulaire (frequentiegestuurd, individuele woorden) | ~200 | Te bouwen |
| Gedeelde cultuurknopen (SHA-C-*, mythologie/geschiedenis/maatschappij) | ~70 | Te bouwen |
| Transfer-edges (LAT↔GRC isomorfe concepten) | ~100 edges | Te bouwen |

**Graph-bestanden:** `data/graph/` bevat meerdere JSON-bestanden per domein. De loader combineert ze automatisch (`load_graph(directory_path)`). Cross-file edges (bijv. transfer-edges naar knopen in andere bestanden) worden correct opgelost.

**Grieks alfabet:** subgraph `GRC-G-FONL-ALFA-*`, prerequisite voor alle GRC-grammaticaknopen. Drie fasen: letterherkenning → fonologie/diakritiek → leesvaardigheid. Blokkeert alle Griekse stof tot volledige beheersing.

## Niet doen

- Geen frontend werk in fase 0-2
- Geen LLM-integratie in fase 0-2
- Geen deployment/hosting configuratie in fase 0
- Geen over-engineering: SQLite, geen Docker, geen microservices
