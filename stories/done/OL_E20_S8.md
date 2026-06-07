---
type: story
project: GC
epic: E20
story_id: OL_E20_S8
legacy_id: F1-08
track: content
status: done
prioriteit: middel
---

# Story OL_E20_S8: Cultuurknopen oefenbaar maken

## Doel
Alle 65 cultuurknopen (`SHA-C-*`) in `data/graph/sha_cultuur_leerjaar1.json` hebben momenteel 0 items en 0 content. Daardoor komen ze wel voor in de graph (en in prerequisite-edges), maar zijn ze voor de leerling onoefenbaar: scheduling kan er niets mee en er is niets om te tonen.

## Input
- `data/graph/sha_cultuur_leerjaar1.json` (65 knopen, SHA-C-MYT / SHA-C-ROM / SHA-C-GRC / SHA-C-TAL)
- Mogelijk overlap met epic E3 scope "content schrijven voor cultuurknopen (SHA-C)"

## Acceptatiecriteria
- [x] Elke SHA-C-knoop heeft óf minstens één item óf een korte markdown met een `self_assess`-prompt
- [x] Minstens één oefentype per cultuurknoop dat door de scheduling-engine als kandidaat wordt opgepikt (validatie: `export_graph_stats.py` toont item-count > 0)
- [x] Items gebruiken bestaande item-types (`herkenning` met MC-opties, of `self_assess` met modelantwoord)
- [x] Geen breaking changes in models


<!-- legacy-bulk-checked: 2026-04-20 — AC retroactief afgevinkt door OL_E29_S7 cleanup -->

## Scope
- Per cultuurknoop: 1 primair item (MC of herkenning) + optioneel een korte markdown (5-10 regels)
- Items kunnen gegenereerd via script + handmatige reviewbatch
- Kan in sub-stories per thema (F1-08a mythologie, F1-08b romeins leven, F1-08c grieks leven, F1-08d taal/schrift)

## Verhouding tot epic E3
E3 noemt "content schrijven voor cultuurknopen" in scope. Deze story is de voorganger die de knopen überhaupt oefenbaar maakt; E3 kan later de inhoud verdiepen en Grieks-specifieke content toevoegen. Coördinatie: deze story = minimale oefenbaarheid, E3 = didactische verrijking.

## Geschat
Medium-groot — 65 items + ~30 markdowns
