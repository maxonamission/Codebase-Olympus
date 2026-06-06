---
type: story
project: GC
epic: E30
story_id: OL_E30_S4
legacy_id: N1-04
track: ontwikkelstraat
status: done
prioriteit: middel
---

# Story OL_E30_S4: knoop-veldnamen + attribuutkey → node (Tier 2)

## Doel
Hernoem de resterende `knoop`-gewortelde code-identifiers naar `node`,
conform CLAUDE.md ("code in het Engels"). Dit is de veld-/variabele-laag
ná de klasse-renames van Tier 1.

## Achtergrond
Tier 2 van epic N1. Betreft ~1800 voorkomens: model-veldnamen
(`knoop_id`, `knoop_states`), lokale variabelen/parameters (`knoop`,
`knoop_ids`, `knoop_state`, …) en de in-memory NetworkX-attribuutkey
`"knoop"` (`graph.nodes[id]["knoop"]`).

**Breaking, maar geen data-bestand-migratie:** `knoop_id`/`knoop_states`
staan in 0 graph-JSON-bestanden (geverifieerd) en er is geen gecommitte
learner-data → re-seed lost serialisatie op (zoals OL_E23_S1). De
graph-JSON-keys (`titel_nl`, `moeilijkheid_initieel`, `richting`, …) en
enum-*waarden* blijven hier ongemoeid — die horen bij Tier 3.

## Aanpak
Whole-word rename `\bknoop` → `node` (boundary aan de start van de
identifier), zodat geprefixte Dutch compounds (`Grammaticaknoop`,
`Vocabulaireknoop`) onaangeroerd blijven.

## Input
- `src/gymnasium_classica/models/learner.py` (velddefinities)
- alle imports/refs/vars in `src/`, `tests/`, `scripts/`
- de `"knoop"`-attribuutkey in `graph/loader.py` + alle lezers

## Acceptatiecriteria
- [x] Model-veldnamen `knoop_id` → `node_id`, `knoop_states` → `node_states`
- [x] Lokale variabelen/parameters `knoop*` → `node*`
- [x] NetworkX-attribuutkey `"knoop"` → `"node"` (consistent schrijf+lees)
- [x] Geprefixte Dutch compounds (`Grammaticaknoop` e.d.) ongewijzigd
- [x] Geen graph-JSON-keys of enum-waarden gewijzigd (Tier 3)
- [x] `ruff check .`, `mypy src/` en de volledige pytest-suite groen
- [x] `scripts/validate_graph.py data/graph/` laadt de graph ongewijzigd
- [x] `scripts/seed_dev.py` draait foutloos (re-seed)

## Scope
Alleen `knoop`-gewortelde code-identifiers + de attribuutkey. Geen
graph-JSON-schema-keys, geen enum-waarden.

## Geschat
Medium-groot — mechanisch maar zeer breed; gate + graph/seed-verificatie.

## Resultaat
- `\bknoop → node` (start-boundary) + `_knoop → _node` (snake_case-infix)
  over alle .py: model-velden `knoop_id`→`node_id`, `knoop_states`→
  `node_states`, lokale vars/params, private methods (`_knoop_to_question`
  →`_node_to_question`), helpers (`validate_knoop_id`→`validate_node_id`),
  en de NetworkX-attribuutkey `"knoop"`→`"node"`.
- **Scope-correctie:** `knoop_ids` (meervoud) bleek een graph-JSON-key
  (2732× in data/graph) — die is teruggedraaid en doorgeschoven naar
  **Tier 3** (datamigratie samen met `titel_nl` c.s. + enum-waarden).
  Enkelvoud `knoop_id` stond in 0 graph-bestanden en is wél hernoemd.
- Geprefixte Dutch compounds (`Grammaticaknoop`, `Vocabulaireknoop`) in
  test-fixture-strings/comment bewust ongemoeid.
- Verificatie: `ruff`+`mypy`(42)+pytest (**599**) groen;
  `validate_graph data/graph/` → 800 nodes, Valid: True;
  `seed_dev.py` re-seedt foutloos.
