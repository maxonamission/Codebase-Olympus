# 04 — Ontwikkelstraat en story-workflow

Dit hoofdstuk is een **uittreksel met praktijkrecepten** bij `docs/ontwikkelstraat-uitleg.md` (de long-read over de zes lagen) en codeert de story-workflow die in Olympus is gegroeid. Beide zijn direct overneembaar; pas alleen de specifieke regels aan op je eigen domein.

## §A — De zes lagen, samengevat

| Laag | Wat | Wanneer |
|------|-----|---------|
| 1. Projecttemplate | Skelet bij start | Nieuwe repo |
| 2. Pre-commit hooks | Lokale snelle checks | Bij elke commit |
| 3. Claude Code hooks | Tijdens AI-sessie | Bij elke file-edit + sessie-einde |
| 4. CI (GitHub Actions) | Server-zijde, hard | Bij elke push + PR |
| 5. Review-skills | Tweede paar ogen | Voor merge |
| 6. Gedeelde standaarden | Cross-project drift voorkomen | Continu |

Volg de lagen-volgorde bij invoer: laag 1-2 op dag één, laag 3-4 binnen de eerste sprint, laag 5 zodra je je eerste merge doet, laag 6 als je een tweede project hebt.

### Archief vanaf maand 6

Een lang-lopend project (>6 maanden) accumuleert versies van BRIEFING- en ONTWERPKEUZES-documenten, afgeronde closure-rapporten en gearchiveerde verkenningen. Zonder discipline raken die ofwel verloren of vervuilen ze de actieve werkruimte.

Werkwijze: een `archief/`-map met een `archief/INDEX.md` die per gearchiveerd document één regel geeft (titel, datum, reden van archivering). Zodra een document niet meer actief gebruikt wordt — een nieuwe versie is uit, een review-cyclus is afgesloten, een verkenning is gemerged of verworpen — verhuis je het naar `archief/` en voeg je een regel toe aan de index. **Wijzig nooit een document na archivering**, anders breekt de terugkijk-functie ("hoe stond het er destijds bij?"). Voor wijzigingen: maak een nieuw document in de actieve ruimte; verwijs eventueel terug.

Niet relevant in de eerste maanden; activeer zodra de tweede major versie van BRIEFING of ONTWERPKEUZES geschreven wordt.

## §B — Concreet: minimale starter-config

Hieronder de bestanden die je in je nieuwe repo zet. Je kunt ze grotendeels uit Olympus kopiëren en domein-specifiek aanpassen.

### `pyproject.toml` (essentie)

```toml
[project]
name = "your-project"
version = "0.1.0"
requires-python = ">=3.11,<3.13"
dependencies = [
    "pydantic[email]>=2.6,<3",
    "networkx>=3.2,<4",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-cov>=5.0",
    "ruff>=0.3",
    "mypy>=1.10",
    "pre-commit>=3.7",
]

[tool.ruff]
# Houd target-version op de laagste Python-versie uit requires-python (hier 3.11);
# dat dwingt ruff om geen syntax voor te stellen die op de oudste ondersteunde
# versie nog niet werkt. Vergeet niet bij te werken zodra je requires-python
# verhoogt.
target-version = "py311"
line-length = 99

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "SIM", "RUF"]
ignore = ["E501", "B008"]
# Voeg domein-specifieke ignores toe (bv. RUF001-003 als je niet-Latin alfabet gebruikt)

[tool.ruff.lint.per-file-ignores]
"tests/**" = ["B011", "E402"]
"scripts/**" = ["B008", "E402"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
line-ending = "lf"

[tool.mypy]
python_version = "3.11"
strict = true
plugins = ["pydantic.mypy"]
exclude = ["^tests/", "^scripts/", "^data/", "^docs/", "^stories/"]

[tool.pydantic-mypy]
init_forbid_extra = true
init_typed = true
warn_required_dynamic_aliases = true

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
```

### `.pre-commit-config.yaml`

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.0
    hooks:
      - id: ruff
      - id: ruff-format

  - repo: local
    hooks:
      - id: mypy
        name: mypy
        entry: uv run mypy src/
        language: system
        pass_filenames: false

      - id: validate-graph
        name: validate-graph
        entry: uv run python scripts/validate_graph.py data/graph/ --mode=staged
        language: system
        pass_filenames: false
        files: ^data/graph/

      - id: story-status-check
        name: story-status-check
        entry: uv run python scripts/check_story_status.py --mode=staged
        language: system
        pass_filenames: false

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-toml
      - id: check-json
      - id: detect-private-key
      - id: check-added-large-files
        args: ['--maxkb=500']
```

### `.github/workflows/ci.yml`

```yaml
name: CI
on: [push, pull_request]

jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
      - run: uv venv --python 3.11
      - run: uv pip install -e ".[dev]"
      - run: uv run ruff check .
      - run: uv run ruff format --check .
      - run: uv run mypy src/
      - run: uv run python scripts/validate_graph.py data/graph/
      - run: uv run python scripts/check_story_status.py --mode=full
      - run: uv run pytest --cov
```

### `.claude/settings.json`

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "bash .claude/hooks/ruff_on_python.sh"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash .claude/hooks/pytest_on_stop.sh"
          }
        ]
      }
    ]
  }
}
```

Met scripts:

`.claude/hooks/ruff_on_python.sh`:
```bash
#!/usr/bin/env bash
set -e
echo "$CLAUDE_HOOK_INPUT" | jq -r '.tool_input.file_path' | while read -r FILE; do
  if [[ "$FILE" == *.py ]]; then
    uv run ruff check --fix "$FILE" || true
    uv run ruff format "$FILE" || true
  fi
done
```

`.claude/hooks/pytest_on_stop.sh`:
```bash
#!/usr/bin/env bash
set -e
uv run pytest -x --tb=short
```

Test eerst handmatig dat ze werken; commit pas daarna.

## §C — De story-workflow

De story-conventie is de manier om werk te verdelen in afgebakende, traceerbare eenheden — zowel voor jezelf als voor AI-assistentie. Olympus startte met drie statussen (`backlog/doing/done`); op basis van later opgedane ervaring is `todo/` als optionele vierde status toegevoegd voor projecten met een groeiende backlog. De aanbevolen structuur:

```
stories/
├── EPICS.md          # overzicht, status, doel per epic
├── backlog/          # ideeën die nog opgepakt moeten worden
│   ├── A1-01.md
│   └── A1-02.md
├── todo/             # OPTIONEEL: ingepland voor de eerstvolgende sessies
│   └── A1-03.md
├── doing/            # max 3 stories tegelijk; meer = onderbroken werk
│   └── A2-01.md
└── done/             # afgeronde stories; AC's afgevinkt
    ├── A0-01.md
    └── A0-02.md
```

### Vier statussen, met `todo/` als opt-in

| Status | Betekenis | WIP-richtlijn |
|---|---|---|
| `backlog` | Gedefinieerd, geen specifieke planning | Geen limiet |
| `todo` | Ingepland voor eerstvolgende sessies | Soft-cap 5–10 |
| `doing` | Actief in uitvoering | Max 3 |
| `done` | Afgerond en gereviewd | — |

`backlog → doing` mag direct — `todo` is opt-in. Voor solo-projecten met <15 stories in backlog is drie statussen prima. Activeer `todo/` zodra je merkt dat je elke sessie opnieuw moet kiezen "wat pak ik nu op?".

### Story-naamgeving

`{EPIC}-{NUMMER}.md`. Bijvoorbeeld `A1-03.md` = epic A1, story 3.

Epic-letters bewust kort: A, B, C, ... met getal voor sub-spoor. Voorbeeld uit Olympus:
- `A1`, `A2` — content (Latijnse grammatica, Griekse grammatica)
- `B1`, `B2` — graph-modules
- `OS-XX` — ontwikkelstraat-stories

### Story-template

```markdown
# Story {ID}: {korte titel}

## Doel
{1-2 zinnen wat deze story bereikt}

## Input
{Welke documenten, code, data je nodig hebt}

## Acceptatiecriteria
- [ ] {AC 1, concreet en falsifieerbaar}
- [ ] {AC 2}
- [ ] {AC 3}

## Scope
{Wat valt erbinnen, wat erbuiten}

## Geschat aantal {knopen / regels code / uren}
{schatting}

## Aanpak
{Optioneel: stappenplan in 3-7 punten}

## Risico's
{Optioneel: bekende valkuilen}
```

### Workflow

**Bij oppakken:**
1. `git mv stories/{backlog,todo}/XX-NN.md stories/doing/`
2. Werk de status-kolom in `EPICS.md` bij naar `doing`
3. Commit deze verplaatsing apart van inhoudelijk werk

**Bij afronden:**
1. Vink alle `- [ ]` AC's om naar `- [x]`
2. Eventueel een korte resultaat-blok toevoegen
3. `git mv stories/doing/XX-NN.md stories/done/`
4. Werk status in `EPICS.md` bij naar `done`
5. Lokaal: `python scripts/check_story_status.py --mode=full` moet groen zijn
6. Commit en push

**Pre-commit hook** valideert: stories in `done/` hebben geen openstaande AC's, locatie en `EPICS.md`-status matchen.

### Nieuwe epic openen (bij meerdere actieve branches)

Zodra je tegelijk aan twee feature-branches werkt — ook in solo-context — claimen ze allebei het volgende epic-nummer als je niet uitkijkt. Resolution achteraf is niet-triviaal: niet alleen folder- en story-IDs moeten hernoemd, ook elke kruisverwijzing in docs en `EPICS.md`.

```markdown
1. `git fetch origin main` vóór je een epic-folder aanmaakt.
2. Pak het hoogste E# op origin/main + 1 — niet op je eigen branch.
3. Bij collision: tweede merger hernoemt. Documenteer het patroon
   nu, niet als het probleem ontstaat.
```

Voor één-branch-projecten meestal overbodig; opnemen in CLAUDE.md zodra je voor het eerst twee actieve branches naast elkaar hebt.

### `EPICS.md` opbouw

```markdown
# Epics overzicht

## Epic A1: {korte titel}

**Doel:** {één zin}
**Geschat:** {aantal knopen / regels / dagen}
**Afhankelijkheden:** {andere epics}
**Status:** done | doing | backlog

| Story | Titel | Eenheid | Status |
|-------|-------|---------|--------|
| A1-01 | … | 6 knopen | done |
| A1-02 | … | 4 knopen | done |
```

### Review-acties en follow-ups in `EPICS.md`

Acceptatiecriteria in stories vangen niet alle uitkomsten van werk. Reviews leveren twee soorten residu op die in stories niet thuishoren maar wel zichtbaar moeten blijven:

1. **Review-acties voor de projecteigenaar** — concrete handelingen die de mens (niet de AI) moet doen: lezen-en-akkoord, expert-consult, scope-beslissing. Verdwijnen na afhandeling.
2. **Follow-ups uit reviews** — geparkeerde overwegingen die op de roadmap blijven staan tot een trigger ze activeert (bv. "model raakt actief gebruikt door externe instantie").

Houd beide bij in `EPICS.md` als losse secties onderaan, niet als verkapte stories in `backlog/`. Dat scheidt **werk dat alleen jij kunt doen** van **werk dat in een story past**, en het maakt het later veel makkelijker om eerder werk weer op te pakken: één blik op `EPICS.md` toont én de status van alle epics én wat er nog op jou wacht.

```markdown
## Review-acties voor de projecteigenaar

| Actie | Document | Toelichting |
|---|---|---|
| {…} | {…} | {…} |

## Follow-ups uit reviews

| Item | Bron | Plek (signaalstory of doc-sectie) | Trigger |
|---|---|---|---|
| {…} | {…} | {…} | {…} |
```

De tweede tabel maak je pas aan zodra er minstens één levende follow-up is — leeg toevoegen is overbodig.

### `scripts/check_story_status.py`

Eenvoudige Python-CLI die:
1. Door `stories/done/` loopt en controleert dat geen `- [ ]` meer in `## Acceptatiecriteria` staat.
2. Door `stories/doing/` loopt en alleen waarschuwt bij meer dan 3 actieve stories.
3. Verifieert dat elke story-naam ook in `EPICS.md` voorkomt.
4. Verifieert dat de status in `EPICS.md` overeenkomt met de fysieke locatie.

**Twee modes** (geldt ook voor `validate_graph.py` en andere cross-document-validators):

- `--mode=staged` (default lokaal, voor pre-commit): rapporteert drift, exit 0 — niet-blokkerend. Lokaal mag drift bestaan tijdens werk-in-uitvoering: een story zit halverwege een refactor, EPICS.md is nog niet bijgewerkt, een ref_id is nog niet uitgevuld. Soft-fail voorkomt dat zulke tijdelijke inconsistentie de commit blokkeert.
- `--mode=full` (CI): hard, exit 1 bij elk probleem. CI is de gate die `main` schoonhoudt.

Zonder dit onderscheid wordt de pre-commit hook ofwel zo streng dat hij vaak omzeild wordt (`--no-verify`), ofwel zo lakse dat hij in CI alsnog dingen toelaat die niet hadden gemoeten.

Implementatieblauwdruk in Olympus' `scripts/check_story_status.py`. ~150 regels.

## §D — Het PR-template

`.github/pull_request_template.md`:

```markdown
## Wat verandert er?

{Korte samenvatting in 1-3 zinnen}

## Welke stories?

- {ID en titel}

## Checklist

- [ ] Lokale tests groen (`uv run pytest`)
- [ ] Ruff + mypy groen (`uv run pre-commit run --all-files`)
- [ ] Story-status correct (verplaatst naar done/, AC's afgevinkt, EPICS.md bijgewerkt)
- [ ] Documentatie bijgewerkt waar relevant
- [ ] `/review` gedraaid in Claude Code
- [ ] **Bij security-trigger:** `/security-review` gedraaid
  - Triggers: auth-flow, user-input-endpoint, externe API-call, dependency-upgrade, queries naar persistente storage

## Open punten

{Eventuele zaken die nog niet af zijn maar bewust gemerged worden}
```

## §E — Wat je in een nieuw project minder makkelijk kunt overslaan

Drie lagen hebben in Olympus achteraf het meeste waarde geleverd:

1. **Pre-commit story-status-check.** Zonder deze hook glijdt regelmatig een story met openstaande AC's naar `done/`. Hook kost een halve dag bouwen, voorkomt elke week een vergissing.
2. **Claude Code Stop-hook met pytest.** Voorkomt dat een sessie afgesloten wordt met rode tests. Eén regel `pytest -x` in een hook bespaart elke week minstens één "vergat ik de tests te draaien"-incident.
3. **CI op `main` als hard gate.** Branch protection actief, geen merge zonder groene CI. In de eerste week voelt het frictie; daarna voelt het rust.

Drie lagen die in Olympus uitgesteld zijn zonder schade:

1. **Visualisatie-tooling** — bouw pas als je echt een viz nodig hebt.
2. **Custom review-skills** — `/review` en `/security-review` zoals ze zijn werken al goed.
3. **Code coverage drempel** — alleen handhaven als je merkt dat tests sluipenderwijs vergeten worden.

## §F — De handover-template

Voor je nieuwe project, kopieer en vul in:

```markdown
# CLAUDE.md — {Projectnaam}

## Project

{1-3 zinnen wat het project is, wat het doel is.}

Lees voor de volledige context:
- `docs/BRIEFING_{PROJECT}.md` — projectvisie, architectuur, roadmap
- `docs/ONTWERPKEUZES_{PROJECT}.md` — vastgestelde ontwerpkeuzes

## Tech stack en constraints

- **Python 3.11**
- **uv** als package manager
- **{andere keuzes: FastAPI? SQLite? React?}**
- Documentatie in {taal}, code in **Engels**

## Werkwijze

{kopieer principes uit hoofdstuk 01 van het starterpakket}

## Ontwikkelstraat

{kopieer beschrijving uit §A van dit hoofdstuk + verwijs naar `docs/ontwikkelstraat-uitleg.md`}

## Story-workflow

{kopieer §C van dit hoofdstuk}

## Output en sessie-management

{kopieer principes uit hoofdstuk 01 §7}

## Domeinkennis

{Domein-specifiek: relevante terminologie, scope, edge-types, etc.}

## Projectstructuur

{Mapboom, zoals in Olympus' CLAUDE.md}

## ID-schema voor knopen

{Specifiek voor jouw schema, met voorbeelden}

## Onomkeerbare acties bevestigen

{Reversibele lokale acties (file-edits, tests, refactors) gewoon doen.
Onomkeerbare of breed-zichtbare acties (force-push, branch verwijderen,
package upgrade in lockfile, PR mergen, externe API-call met effect)
expliciet bevestigen. Vijf seconden bevestigingsvraag bespaart drie
uur reparatie.}

## Niet doen

{Drie tot zes scherp geformuleerde regels — gedestilleerd uit hoofdstuk 06
antipatronen, domein-specifiek gemaakt. Voorbeeld voor archetype B:}

1. Geen globale DAG-cyclus-check op een netwerk met feedback-edges.
2. Geen edge-velden invoeren die niet door code gebruikt worden.
3. Geen sliders zonder eenheid + literatuur-onderbouwing (`ref_id`).
4. Geen statische pad-analyse als antwoord op dynamische vragen.

{De "Niet-doen"-sectie staat hier omdat de AI CLAUDE.md elke sessie leest;
het antipatronen-hoofdstuk alleen als iemand er expliciet naar verwijst.
Korter en harder dan §6 — zet hier alleen wat al gefaald heeft of
gegarandeerd zal falen.}

## Waar vind ik wat?

| Vraag | Locatie |
|---|---|
| Projectvisie en scope | `docs/BRIEFING_*.md` |
| Vastgestelde ontwerpkeuzes | `docs/ONTWERPKEUZES_*.md` |
| Edge- en node-types | `src/<pkg>/schemas/` |
| ID-schema | `docs/id-schema.md` |
| Validatie-catalogus | `src/<pkg>/graph/validation.py` |
| Stories-overzicht | `stories/EPICS.md` |
| Review-acties + follow-ups | `stories/EPICS.md` (onderaan) |
| Literatuurregister | `data/literatuur.json` |
| Archief van oude versies | `archief/INDEX.md` |
| ... | ... |
```

Voor Olympus is dit bestand 11 KB. Voor een nieuw project mag je beginnen met de helft daarvan en geleidelijk uitbreiden. De "Waar vind ik wat?"-tabel is in de praktijk de meest geraadpleegde sectie — laat hem organisch meegroeien met je repo.

## Vragen voor je nieuwe project

1. Welke pre-commit hooks zet je actief vanaf dag 1? (advies: ruff + mypy + format minimaal)
2. Welke CI-stappen? (advies: minstens ruff + mypy + pytest)
3. Welke Claude Code hooks? (advies: PostToolUse `Edit|Write` op je primaire taal + Stop met pytest)
4. Welke story-naamgeving (epics A/B/C of zinniger labels voor je domein)?
5. Wie verzorgt de security-review-trigger als je geen security-relevante code hebt? (in dat geval mag je hem uit de PR-template halen)
6. Hoe vaak push je naar `main`? Direct of via feature-branches met PR? (advies: PR's, ook al ben je solo — dan dwing je je eigen review)
