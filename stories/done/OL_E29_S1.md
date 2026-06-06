---
type: story
project: GC
epic: E29
story_id: OL_E29_S1
legacy_id: OS-00
track: ontwikkelstraat
status: done
prioriteit: middel
---

# Story OL_E29_S1: Storyconventie herstellen

## Doel
De storyconventie rechttrekken naar de standaard: één `stories/`-map met platte subfolders `backlog/`, `doing/`, `done/` en één `EPICS.md` als centraal overzicht. De bestaande Olympus-structuur met per-epic-submappen is een verkeerde interpretatie en moet weg, zodat de ontwikkelstraat-check (OL_E29_S7) op één consistente structuur kan bouwen.

## Input
- Bestaande `stories/epic-*/` submappen (29 epics, 164 storybestanden)
- Bestaande `stories/EPICS.md` als centrale index
- Losse `epic-f2-mentor-dashboard/EPIC.md` met uitgebreide epic-beschrijving
- Conflicterende `OL_E27_S16.md` (in zowel `todo/` als `done/` van epic-e3)

## Acceptatiecriteria
- [x] Eén `stories/`-map met `backlog/`, `doing/`, `done/` als directe subfolders
- [x] Alle storybestanden in precies één van de drie subfolders, zonder tussenliggende epic-map
- [x] Hernoeming van `todo/` naar `backlog/` doorgevoerd
- [x] `EPICS.md` is de centrale index met alle stories en hun status
- [x] Geen epic-submappen meer aanwezig (epic-a1/ t/m epic-f2/ allemaal verwijderd)
- [x] OL_E27_S16 conflict opgelost: `done/`-versie behouden, `todo/`-versie verwijderd
- [x] Epic F2: inhoud van losse `EPIC.md` gemerged in `EPICS.md` (Context, Afhankelijkheden, Verhouding tot track C, Niet-doel); losse `EPIC.md` verwijderd
- [x] Geen dangling paden in documentatie (grep `stories/epic-` geeft nul treffers)
- [x] Commit met `git mv` zodat history behouden blijft (niet als delete+add)

## Scope
Platslaan structuur + OL_E27_S16-conflict + F2-merge. Inhoud van storybestanden niet wijzigen.

## Niet in scope
- Inhoudelijke updates aan bestaande stories
- Validatie of AC van oude stories compleet zijn
- Scripts voor toekomstige conventie-handhaving — dat is OL_E29_S7

## Resultaat
- 163 storybestanden naar platte structuur (27 backlog, 1 doing, 135 done)
- 29 epic-submappen + 80 `.gitkeep`-bestanden verwijderd
- 1 duplicate (OL_E27_S16 todo) verwijderd
- 1 losse EPIC.md gemerged en verwijderd
- Commit `d103d91` op branch `claude/mobile-app-exploration-S1u5U`
