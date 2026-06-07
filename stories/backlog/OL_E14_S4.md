---
type: story
project: GC
epic: E14
story_id: OL_E14_S4
legacy_id:
track: mentor
status: backlog
prioriteit: middel
---

# Story OL_E14_S4: Leerling-opt-in voor mentor-deling (consent-record + intrekken)

## Doel

Maak het delen van het leerprofiel met een mentor **leerling-geïnitieerd en expliciet**,
conform ADR-0001 (Optie 2). Vandaag bestaan de koppel-tabel (`mentor_assignments`) en de
afscherming (`require_mentor_of` → 403) al, maar er is geen endpoint dat een koppeling
aanmaakt en geen vastgelegde toestemming van de leerling. Deze story sluit dat gat: geen
mentor ziet voortgang zonder dat de leerling daar bewust en intrekbaar mee instemde.

## Input / afhankelijkheden

- Bestaand: `mentor_assignments`, `create_mentor_assignment`, `is_mentor_of`,
  `require_mentor_of` (`api/database.py`, `api/auth.py`).
- Bestaand: ouderlijke-toestemming-/AVG-flow voor minderjarigen (OL_E9_S4, A7.6).
- ADR-0001 (`docs/decisions/ADR-0001-leerprofiel-opslag-en-mentor-opt-in.md`).

## Acceptatiecriteria

- [ ] Een koppeling mentor↔leerling kan **alleen** ontstaan na een expliciete
      leerling-actie (leerling nodigt mentor uit óf keurt een mentorverzoek goed).
- [ ] Bij een leerling **< 16 jaar** is bovendien ouderlijke toestemming vereist vóór de
      koppeling actief wordt (hergebruik de bestaande toestemmingsflow).
- [ ] Er wordt een **consent-record** vastgelegd: wie, wanneer, scope (welke gegevens),
      en de grondslag/toestemmingsbron.
- [ ] De leerling kan de deling **intrekken**; intrekken verwijdert de koppeling en de
      mentor krijgt direct weer 403 (`require_mentor_of`).
- [ ] `create_mentor_assignment` wordt nooit aangeroepen zonder geldige consent (gate ervoor).
- [ ] Geen breaking changes in bestaande models; bestaande tests blijven groen.
- [ ] Nieuwe functionaliteit heeft eigen tests (opt-in happy path, weigeren/geen-consent →
      403, intrekken → 403, <16 zonder ouderlijke toestemming → geen koppeling).

## Scope

Consent-gate + leerling-gestuurde endpoints (uitnodigen/goedkeuren/intrekken) + consent-record
bovenop de bestaande afscherming. **Buiten scope:** de client-held/edge-opslagvariant
(ADR-0001 Optie 3) — aparte afweging/story als die richting gekozen wordt. Frontend-UI mag
deels een vervolgstory zijn (fase 4+), mits de API de opt-in afdwingt.

## Geschat

—
