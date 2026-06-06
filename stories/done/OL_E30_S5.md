---
type: story
project: GC
epic: E30
story_id: OL_E30_S5
legacy_id: N1-05
track: ontwikkelstraat
status: done
prioriteit: middel
---

# Story OL_E30_S5: JSON-schema-keys naar Engels (Tier 3, deel 1)

## Doel
Hernoem de Nederlandstalige JSON-*keys* van de datamodellen naar Engels,
inclusief de bijbehorende Pydantic-veldnamen en alle code-refs. Enum-*waarden*
blijven hier ongewijzigd (die horen bij OL_E30_S6).

## Achtergrond
Eerste deel van Tier 3. Raakt drie JSON-schema's die door modellen worden
geladen: graph (`Node`/`Item`/`GraphData`), passages (`Passage`/
`WordAnnotation`) en `methode_mapping.json` (dict-access). De gedeelde keys
(`taal`/`knoop_ids`/`beschrijving`) dwingen een gecombineerde migratie af.

## Aanpak
- `scripts/migrate_n1_tier3_keys.py`: idempotente, exacte-match key-rename
  over `data/graph/`, `data/passages/`, `data/methode_mapping.json`. **Alleen
  keys, nooit waarden** — Nederlandstalige content blijft intact.
- Pydantic-velden + code-refs hernoemd; content-strings beschermd via
  positie-gerichte patronen (`.veld`, `veld=`, `["veld"]`, `"veld":`).

## Acceptatiecriteria
- [x] Alle Nederlandstalige JSON-schema-keys hernoemd naar Engels
      (`knopen→nodes`, `knoop_ids→node_ids`, `taal→language`, `titel_nl→
      title_nl`, `beschrijving→description`, `bloom_niveau→bloom_level`,
      `fase→phase`, `toetsbaar→testable`, `pensum_jaren→pensum_years`,
      `cevte_referentie→cevte_reference`, `semantisch_cluster→
      semantic_cluster`, `richting→direction`, `moeilijkheid_initieel→
      difficulty_initial`, `discriminatie_initieel→discrimination_initial`,
      `verwachte_tijd_sec→expected_time_sec`, `antwoord→answer`,
      `bron→source`, `verificatie_methode→verification_method`,
      `verwacht_resultaat→expected_result`; passage: `titel→title`,
      `tekst→text`, `annotaties→annotations`, `moeilijkheid→difficulty`,
      `woord→word`, `naamval→case`, `vertaling→translation`)
- [x] Pydantic-velden (graph.py, passage.py, schemas.py, learner.py) +
      alle code-refs bijgewerkt
- [x] Enum-*waarden* ongewijzigd (Nederlands; OL_E30_S6)
- [x] Nederlandstalige content (vertalingen, feedback, descriptions) intact
- [x] Migratiescript idempotent; `ruff`, `mypy src/`, pytest (**599**) groen
- [x] `validate_graph data/graph/` → 800 nodes, Valid: True; `seed_dev.py` OK

## Scope
JSON-schema-keys + veldnamen + code-refs. Enum-waarden (OL_E30_S6) en
methode-eigen config-keys (`methoden`/`hoofdstukken`) buiten scope.

## Resultaat
27637 key-occurrences over 11 databestanden gemigreerd. Drie schema's +
API-schemas + learner-model consistent op Engelse veldnamen. Geen
data-verlies (idempotente re-run = 0). 599 tests groen.
