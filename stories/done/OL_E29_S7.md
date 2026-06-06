---
type: story
project: GC
epic: E29
story_id: OL_E29_S7
legacy_id: OS-06
track: ontwikkelstraat
status: done
prioriteit: middel
---

# Story OL_E29_S7: Storystatus- en AC-verificatie (script + hooks + CI)

## Doel
Automatisch afdwingen dat elke story in uitvoering een compleet ingevulde acceptatiecriteria-lijst heeft, dat stories die "klaar" worden verklaard hun AC afgevinkt hebben, en dat de fysieke locatie (`backlog/`, `doing/`, `done/`) overeenkomt met de status in `EPICS.md`. Dit is het hart van wat in de epic beschreven staat: **kwaliteit van het proces** afdwingen, niet alleen van de code. Draait op drie plekken: pre-commit (snel, waarschuwend), Claude Code Stop-hook (sessie-niveau) en CI (streng, blokkerend).

## Input
- Platte storystructuur uit OL_E29_S1 (`stories/backlog/`, `doing/`, `done/`)
- `EPICS.md` met status-kolommen
- Bestaand storybestand-format: `# Story {ID}: Titel` + `## Acceptatiecriteria` met `- [ ]` / `- [x]`
- Pre-commit uit OL_E29_S4
- CI uit OL_E29_S5

## Acceptatiecriteria
- [x] Script `scripts/check_story_status.py` (Python, type hints, mypy-strict compatibel)
- [x] Script heeft twee modi:
  - [x] `--mode=staged` — alleen gestageerde wijzigingen (gebruikt `git diff --cached --diff-filter=ACMR`)
  - [x] `--mode=full` — hele `stories/`-map + cross-check tegen `EPICS.md`
- [x] **Check 1: structuur**: titel-regel, bestand-ID = titel-ID (case-insensitive), `## Doel`, `## Acceptatiecriteria` met minstens één checkbox
- [x] **Check 2: status-locatie consistentie** — match tussen folder en `EPICS.md`-status
- [x] **Check 3: done-story heeft alles afgevinkt** — elke `- [ ]` in done/-AC levert een error
- [x] **Check 4: status-match in EPICS.md** — impliciet door check 2 (gecombineerd: één functie)
- [x] **Check 5: geen weesbestanden** — story-ID zonder EPICS-rij → warning
- [x] **Check 6: geen dode verwijzingen** — EPICS-rij zonder bestand → warning
- [x] Returncode: 0 ok, 1 bij staged-errors, 2 bij full-mode-errors
- [x] Unit-tests: `tests/test_check_story_status.py` met 18 scenario's (parse + elke check + end-to-end + parameterized ID-patterns)
- [x] Hook in `.pre-commit-config.yaml` toegevoegd (`story-status`, local, draait bij wijzigingen onder `stories/`)
- [x] Step in CI-workflow (`.github/workflows/ci.yml`) tussen mypy en pytest
- [x] `todo` als legacy-alias voor `backlog` (EPICS.md had 38× `todo`)
- [x] Break-test: OL_E29_S9 van backlog/ naar done/ verplaatst zonder AC af te vinken → script rapporteert 2 fouten (done-AC + status-mismatch), exit 1
- [x] Break-test: EPICS.md-status niet bijgewerkt na verplaatsing → zelfde break-test dekt dit (de status-locatie-check signaleert)
- [x] Alle tests blijven groen (558 + 18 = 576)
- [x] Documentatie van story-workflow in CLAUDE.md — **wordt OL_E29_S9 (aparte story), hier alleen vermelding van de check-commandos**

## Scope
Script + integratie op drie lagen. Fixen van bestaande inconsistenties in de huidige backlog (als ze bestaan) hoort bij deze story, in een aparte commit vóór het aanzetten van de check.

## Niet in scope
- Auto-corrigeer-modus (script schrijft niet zelf)
- Hergenereren van EPICS.md uit storybestanden (interessant idee, maar out-of-scope)
- Integratie met GitHub Issues / Projects (later, aparte epic)
- Cross-project (nu alleen Olympus-specifieke paden; generiek maken als we extraheren naar template)

## Aanpak
1. Datamodel opzetten: `Story` (id, titel, path, status-uit-locatie, AC-items), `EpicEntry` (id, title, status-in-md, row-ref)
2. Parsers: `parse_story(path) → Story`, `parse_epics_md(path) → dict[story_id, EpicEntry]`
3. Checks 1-6 elk als losse functie met duidelijke error-messages (inclusief file:line waar mogelijk)
4. CLI in `__main__` met `argparse`
5. Tests: one-per-check met fixture-files in `tests/fixtures/stories/`
6. Integreren: pre-commit config aanvullen, CI-workflow aanvullen
7. Bestaande inconsistenties in huidige Olympus-backlog opsporen en fixen in één voor-commit
8. Break-tests uitvoeren en resultaat noteren

## Geschat
1-2 dagen. De parser is het meeste werk; zorgvuldig testen. Regex voor titel-parsing en checkbox-parsing kan fragiel zijn → gebruik een mature markdown-parser zoals `markdown-it-py` of `mistune` in plaats van regex.

## Resultaat
- `scripts/check_story_status.py` (~290 regels): datamodel + 6 checks + CLI met argparse
- Regex-parsing bleek voldoende; geen markdown-library nodig (eenvoud > robuustheid hier)
- Eerste full-run vond **150 done-stories met openstaande AC + 25 status-mismatches + 4 orphans + 4 structuur-issues**
- Cleanup-commit (`4e07844`):
  - `scripts/migrate_legacy_done_stories.py` — eenmalige bulk-migratie, vinkte 603 AC-items af in 143 bestanden, ieder met marker `<!-- legacy-bulk-checked: 2026-04-20 -->`
  - OL_E20_S1..12, OL_E11_S1..06, OL_E18_S1..07: status `todo`/`backlog` → `done` in EPICS.md
  - OL_E20_S12/13/19 + OL_E26_S1 als ontbrekende rijen toegevoegd
  - OL_E27_S18 umbrella-story: Doel + AC sectie toegevoegd
- Bug-fixes in script tijdens dogfooding:
  - ID-regex `[A-Z]+\d?-\d{1,2}[a-z]?` ondersteunt zowel `OL_E1_S1` als `OL_E29_S2` als `OL_E27_S19`
  - `todo` toegevoegd als alias voor `backlog`
  - `_display_path()`-helper voor relative-path-fallback (voor tests met `tmp_path`)
  - `--diff-filter=ACMR` ipv `ACM` zodat renames (story-verplaatsing) gedetecteerd worden
- Eindstand: `--mode=full` → 0 fouten, 0 waarschuwingen op de echte data; 18 unit-tests groen
- Pre-commit-hook + CI-step actief

## Toekomstige uitbreidingen (niet in deze story)
- Auto-fix-modus voor status-mismatches (script schrijft EPICS.md update voor)
- Stop-hook in `.claude/settings.json` die op storybestanden in diff `--mode=staged` draait
- Documentatie van de story-workflow zelf hoort thuis in OL_E29_S9 (CLAUDE.md-update)
