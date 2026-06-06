---
type: story
project: GC
epic: E23
story_id: OL_E23_S1
legacy_id: L1-01
track: learner
status: done
prioriteit: middel
---

# Story OL_E23_S1: Retentie- en sessiemetriek-logging

## Doel
Leg per leerling voldoende data vast om **retentie over tijd** en
**effectgrootte** te kunnen berekenen, zodat de centrale projectclaim
("efficiënter leren per bestede minuut") toetsbaar wordt. Dit is de
fundamentele meetlaag onder Spoor L (zie ontwerpkeuze 12).

## Achtergrond
Bloom's "2 sigma" is nooit gerepliceerd en realistische effecten
liggen rond 0,2–0,8 SD (zie `docs/LITERATUURONDERZOEK_LEERBENADERING.md`,
deel C en aanbeveling D2). Zonder eigen meting blijft elke
efficiëntieclaim een aanname. Bovendien is er nauwelijks empirisch
onderzoek naar klassieke talen — dit project kan die evidence zelf
genereren.

## Input
- `src/gymnasium_classica/models/learner.py` — `ItemResponse`,
  `KnoopState`, `SessionRecord`, `LearnerModel`
- bestaande telemetrie-basis (OL_E20_S12, done) als referentie
- `tests/test_answer_capture.py`, `tests/test_session.py`

## Acceptatiecriteria
- [x] Elke `ItemResponse` legt genoeg vast om retentie te reconstrueren:
      tijdstip, knoop (`knoop_id`), richting (receptief/productief),
      correctheid, responstijd, en het mastery-niveau vóór de poging
      (`mastery_before`)
- [x] Een afleidbare metriek-functie berekent per knoop de geschatte
      retentie als functie van tijd sinds laatste review
      (`metrics.estimated_retention`)
- [x] Een rapportagefunctie levert per leerling: totale leertijd,
      aantal reviews, gemiddelde retentie en mastery-verdeling
      (`metrics.build_learner_report` → `LearnerReport`)
- [x] De metriek-functies hebben eigen unit-tests met vaste fixtures
      (`tests/test_metrics_retention.py`)
- [x] **Bewuste breaking change** (gekozen i.p.v. additief, juni 2026):
      `knoop_id`, `richting` en `mastery_before` zijn verplichte velden op
      `ItemResponse`. Alle constructie-sites bijgewerkt; alle tests groen
      (587). Geen gecommitte DB/seed-data in git, dus alleen lokale
      dev-DB's moeten opnieuw geseed worden (`scripts/seed_dev.py`).
- [x] Privacy: de meetlaag bevat geen extra persoonsgegevens buiten wat
      al wordt opgeslagen (conform AVG-uitgangspunt keuze 7)

## Scope
Alleen het vastleggen en afleiden van metriek. Geen dashboards
(frontend), geen A/B-logica (OL_E23_S3), geen intake-baseline (OL_E23_S2).

## Afhankelijkheden
Geen harde — bouwt op het bestaande learner-model.

## Geschat
Medium — vooral modeluitbreiding + afgeleide metriek + tests.

## Resultaat
- `ItemResponse` uitgebreid met drie verplichte velden: `knoop_id`,
  `richting` (str-snapshot, consistent met `item_type`), `mastery_before`
  (BKT-posterior vóór de poging). Bewuste breaking change (gekozen door
  de gebruiker boven de additieve variant).
- `api/session_manager.py`: de enige productie-funnel (`_build_item_response`
  / `_grade_and_record`) geeft de drie velden door; `mastery_before` komt
  uit `SessionState.current_before` (de posterior vóór de BKT-update).
- Nieuwe `gymnasium_classica.metrics`-module: `estimated_retention`
  (exponentiële vergeetcurve met SM-2-interval als stabiliteit) en
  `build_learner_report` → `LearnerReport` (totale leertijd, aantal
  reviews, gemiddelde retentie, mastery-verdeling, reviews per richting).
- Tests: `tests/test_metrics_retention.py` (+ uitgebreide ItemResponse-tests);
  bestaande constructie-sites bijgewerkt. **587 passed**, mypy + ruff groen.
- Geen gecommitte learner-data in git; lokale dev-DB's opnieuw seeden via
  `scripts/seed_dev.py`.
