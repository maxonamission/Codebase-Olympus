---
type: story
project: GC
epic: E30
story_id: OL_E30_S2
legacy_id: N1-02
track: ontwikkelstraat
status: done
prioriteit: middel
---

# Story OL_E30_S2: KennisKnoop → Node

## Doel
Hernoem de klasse `KennisKnoop` naar `Node` in de hele codebase,
conform de Engels-in-code-conventie. Niet-breaking voor opgeslagen data.
(Eén soort node-object in de graph, dus de korte naam `Node` is eenduidig;
paart met `NodeState` en `PrerequisiteEdge`.)

## Achtergrond
Grootste vernederlandste klassenaam (~133 refs in ~24 bestanden). Hangt
samen met OL_E30_S1 (NodeState) — samen vormen ze de kern van de
graph-/learner-modellen. Velden (`titel_nl`, `beschrijving`, …) blijven in
deze story ongewijzigd; die horen bij Tier 3 (zie epic N1).

## Input
- `src/gymnasium_classica/models/graph.py` (definitie)
- alle imports/refs in `src/`, `tests/`, `scripts/`
- `graph/loader.py` (construeert KennisKnoop uit JSON — veldnamen blijven)

## Acceptatiecriteria
- [x] Klasse `KennisKnoop` hernoemd naar `Node` op de definitie
- [x] Alle imports en referenties bijgewerkt
- [x] Geen veldnamen of JSON-keys gewijzigd (Tier 3)
- [x] `ruff check .`, `mypy src/` en de volledige pytest-suite groen
- [x] Loader laadt alle bestaande graph-JSON ongewijzigd in

## Scope
Alleen de naam `KennisKnoop` → `Node`.

## Geschat
Medium — breedste rename; zorgvuldig + tests.

## Resultaat
- `KennisKnoop` → `Node` (definitie in `models/graph.py`) plus alle 134
  referenties; test-klasse `TestKennisKnoop`→`TestNode`.
- Geen veldnamen/JSON-keys of attribuut-keys gewijzigd (de graph-attribuutkey
  `"knoop"` is een string-literal, blijft → Tier 3). Geen string-literals
  geraakt.
- AC-verificatie: `scripts/validate_graph.py data/graph/` laadt alle
  bestaande graph-JSON ongewijzigd in (alleen bekende no-items-warnings).
- `ruff check .` (+ format), `mypy src/` (42), pytest (**599**) groen.
