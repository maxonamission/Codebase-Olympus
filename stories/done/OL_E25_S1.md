---
type: story
project: GC
epic: E25
story_id: OL_E25_S1
legacy_id: L3-01
track: didactiek
status: done
prioriteit: middel
---

# Story OL_E25_S1: Worked-example oefentype met faded scaffolding

## Doel
Voeg een **uitgewerkt-voorbeeld**-oefentype toe waarbij de steun
geleidelijk wegvalt (faded scaffolding), als aanvulling op de bestaande
oefentypen.

## Achtergrond
Ontwerpkeuze 15. Meerdere ITS-meta-analyses noemen *worked examples*
als belangrijkste moderator van effectiviteit. De huidige
`ItemType`-waarden (herkenning, productie, analyse, synthese,
contextueel) bevatten geen uitgewerkt voorbeeld met afnemende steun.
Dit sluit aan op de scaffolding-aanpak voor teksten (briefing §3.6) en
op de bestaande `ScaffoldingPanel` in de frontend (OL_E20_S1, done).

## Input
- `src/gymnasium_classica/models/graph.py` — `ItemType`, `Item`
- bestaande oefentypen en hun validatie/serialisatie
- `tests/test_structured_stimulus.py`, item-gerelateerde tests

## Acceptatiecriteria
- [x] `ItemType` uitgebreid met een `worked_example`-variant
- [x] Een worked-example-item kan een geordende reeks stappen bevatten,
      elk met een instelbaar steunniveau (volledig uitgewerkt →
      gedeeltelijk → zelf invullen)
- [x] Validatie: stappen zijn geordend en het steunniveau neemt monotoon
      af (geen "terug naar meer steun" binnen één item)
- [x] Minstens één concreet voorbeeld-item in de data (bijv. een
      stap-voor-stap ontlede/vertaalde zin) met bijbehorende content
- [x] De scheduler kan worked examples markeren als introductie-oefening
      (interface/markering aanwezig; volledige uitfasering mag later)
- [x] Unit-tests: model accepteert geldige worked examples en weigert
      malformede (ongeordende of oplopende steun)
- [x] Geen breaking changes; bestaande tests blijven groen

## Scope
Datamodel + validatie + één voorbeelditem. Volledige
scheduler-uitfasering en frontend-rendering mogen vervolgstories zijn.

## Afhankelijkheden
Geen harde.

## Geschat
Medium.

## Resultaat
- `ItemType.WORKED_EXAMPLE` toegevoegd; `WorkedStep`-model (order,
  support_level 0-1, content) + `Item.worked_steps` (optioneel).
- Validatie via `model_validator`: worked_example vereist niet-lege,
  uniek-geordende stappen met monotoon niet-stijgend steunniveau; stappen
  alleen toegestaan op worked_example-items.
- Markering: `Item.is_worked_example` + scheduler-helper
  `is_introduction_item(item)`.
- Voorbeelditem in `data/graph/lat_grammatica_poc.json`
  (`...NAAMVAL-INTRO-WE01`): stap-voor-stap naamval-analyse met steun
  1.0 → 0.5 → 0.0. Graph valideert (800 nodes), migratie-scripts idempotent.
- Tests: geldige/malformede worked examples (ongeordend/oplopende steun/
  dubbele order/steps-op-verkeerd-type), markering, en het data-voorbeeld.
  **649 tests groen**, geen regressie.
