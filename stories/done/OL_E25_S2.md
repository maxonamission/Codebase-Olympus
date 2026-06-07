---
type: story
project: GC
epic: E25
story_id: OL_E25_S2
legacy_id: L3-02
track: didactiek
status: done
prioriteit: middel
---

# Story OL_E25_S2: Motivatielaag tegen de metacognitieve illusie

## Doel
Geef het systeem een laag die expliciet uitlegt **waarom effectieve
oefening zwaar voelt**, gekoppeld aan voortgangsvisualisatie, om
afhaken te voorkomen.

## Achtergrond
Ontwerpkeuze 16a. Effectieve, "desirable difficult" oefening (spacing,
retrieval, interleaving) wordt door leerlingen systematisch onderschat —
een reëel afhaakrisico (briefing-risico 7.4). De groen kleurende
knowledge-graph-heatmap is een krachtig tegenwicht, mits gekoppeld aan
uitleg op de juiste momenten.

## Input
- `src/gymnasium_classica/models/learner.py` — mastery/voortgang als
  databron voor visualisatie en triggers
- bestaande progress-/heatmap-logica en frontend-componenten
- OL_E23_S1 (metriek) voor het detecteren van "zware maar productieve" momenten

## Acceptatiecriteria
- [x] Een mechanisme dat bepaalt wanneer een uitlegmoment relevant is
      (bijv. na een reeks moeilijke maar leerzame items, of bij een
      retrieval-dip die normaal en gewenst is)
- [x] Een set korte, herbruikbare uitlegteksten ("dit voelt zwaar omdat
      het werkt") gekoppeld aan deze momenten — in het Nederlands
- [x] Voortgangssignaal: de mastery-toename wordt zichtbaar gekoppeld aan
      de inspanning, zodat de leerling het effect ziet
- [x] De triggers zijn instelbaar/uitschakelbaar (geen opdringerigheid)
      en deelbaar als variant via OL_E23_S3
- [x] Unit-tests voor de trigger-logica met fixtures
- [x] Geen breaking changes; bestaande tests blijven groen

## Scope
Trigger-logica + tekstcontent + koppeling aan voortgangsdata. Volledige
visuele uitwerking in de frontend mag deels een vervolgstory zijn.

## Afhankelijkheden
- OL_E23_S1 (metriek) wenselijk om zinvolle triggers te bepalen.

## Geschat
Medium.

## Resultaat
- Nieuw pakket `gymnasium_classica.motivation`: `evaluate_motivation(learner,
  config)` levert een `MotivationCue` op datagedreven momenten —
  retrieval-dip (geruststelling) → desirable difficulty (uitleg) →
  voortgangswinst (bevestiging), of None.
- `MESSAGES`: korte Nederlandse uitlegteksten ("dit voelt zwaar omdat het
  werkt") per moment. `MotivationCue.mastery_gain` koppelt de winst aan de
  inspanning (voortgangssignaal).
- `MotivationConfig` met instelbare drempels en een `enabled`-toggle (geen
  opdringerigheid). Variant-baar via OL_E23_S3: `StrategyParams.motivation_enabled`
  + `motivation_config_for(learner)` neemt de experiment-toewijzing mee.
- Triggers gebaseerd op de OL_E23_S1-meetdata (`ItemResponse.mastery_before` +
  uitkomst). Volledige visuele uitwerking = frontend-vervolg.
- Tests: elk moment, disabled/no-history → None, Nederlandse tekst,
  variant-uitschakeling. **658 tests groen**, geen regressie.
