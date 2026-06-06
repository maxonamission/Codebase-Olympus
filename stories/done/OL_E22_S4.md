---
type: story
project: GC
epic: E22
story_id: OL_E22_S4
legacy_id: M1-04
track: didactiek
status: done
prioriteit: middel
---

# Story OL_E22_S4: Vertaal-integratielaag — eerste I-VERT-knopen

> Enabler-story, afgesplitst tijdens OL_E22_S2 (Sprint 6). OL_E22_S2 nam aan dat
> er I-knopen voor vertaling bestonden; die waren er niet. Deze story
> bouwt de eerste vertaal-integratieknopen zodat OL_E22_S2 daarna exact
> uitvoerbaar is (de `LEGO_VERTALEN`-misconceptie koppelt aan deze
> knopen en hun items).

## Doel
De eerste knopen van type **I (Integratie)** voor het domein **VERT
(vertalen)** toevoegen aan de graph, voor Latijn én Grieks. Deze knopen
maken de vertaalvaardigheid zelf — het ontleden van een zin naar
zinsdelen en die omzetten naar correct Nederlands — een leerbare,
diagnoseerbare eenheid. Ze sluiten de POLMO-procedure (OL_E22_S1) aan op een
concrete uitkomst-knoop en vormen de `avg_I_vert`-basis voor de
Lego-vertaler-detectie (OL_E22_S2).

## Achtergrond
Type `I` en domein `VERT` zijn al gedefinieerd in het model
(`NodeType.I`) en het ID-schema (`INTEGRATION_DOMAINS` bevat `VERT`),
maar er bestond nog geen enkele I-knoop in de graph. De grammatica- en
vocabulaire-lagen (epics A1–A4) en de POLMO-procedurelaag (OL_E22_S1) zijn
er wel. De integratielaag is de ontbrekende schakel: waar de leerling
losse kennis samenbrengt tot een vertaling.

Juist hier faalt het "Lego-vertalen": een leerling die de woorden kent
maar de naamval negeert, vertaalt "Servus dominum videt" net zo vaak
verkeerd ("De meester ziet de slaaf") als goed, omdat hij op
woordvolgorde gokt in plaats van op de uitgang te letten.

## Input
- `src/gymnasium_classica/schemas/id_schema.py` — `INTEGRATION_DOMAINS`
  (bevat al `VERT`), geen wijziging nodig
- `data/graph/` — bestaande grammatica-/POLMO-knopen als edge-targets
- `data/graph/sha_strategie_polmo.json` (OL_E22_S1) — de POLMO-keten
- Item-vorm zoals in bestaande graph-JSONs (recognition-items met
  `stimulus.instruction` + `options`)

## Acceptatiecriteria

### Knopen en data
- [x] Nieuw graph-bestand `data/graph/lat_integratie_leerjaar1.json` met
      3 Latijnse I-VERT-knopen:
  - `LAT-I-VERT-INTRO` — "Van ontleden naar vertalen" (conceptknoop)
  - `LAT-I-VERT-NAAMVAL` — "Naamval bepaalt de functie" (onderwerp vs.
    lijdend voorwerp; hosts de diagnostische items)
  - `LAT-I-VERT-POLMO` — "Een zin vertalen met POLMO"
- [x] Nieuw graph-bestand `data/graph/grc_integratie_leerjaar1.json` met
      de 3 Griekse equivalenten (`GRC-I-VERT-INTRO`, `-NAAMVAL`, `-POLMO`)
- [x] `prerequisite`-edges die de integratielaag verankeren:
  - morfologie-/syntaxis-concepten → `…-I-VERT-NAAMVAL`
  - `SHA-P-VERTAAL-POLMO-OV` (eind POLMO-procedure) → `…-I-VERT-POLMO`
  - `…-I-VERT-INTRO` → `…-I-VERT-NAAMVAL` → `…-I-VERT-POLMO` (interne keten)
- [x] Elke `…-I-VERT-NAAMVAL`-knoop heeft ≥3 vertaalitems waar de
      naamval-uitgang het verschil maakt tussen onderwerp en lijdend
      voorwerp (geschikt als latere `diagnose_items` voor OL_E22_S2)

### Inhoud en validatie
- [x] Markdown-content voor elke INTRO-knoop
      (`data/content/LAT-I-VERT-INTRO.md`, `data/content/GRC-I-VERT-INTRO.md`)
      met Begrippen-sectie
- [x] Volledige graph blijft valide (`validate_graph` groen): geen
      cycles, alle edge-targets resolven, ID's geldig
- [x] Geen weesknopen: de I-VERT-knopen hangen via prerequisites aan de
      bestaande graph

### Tests
- [x] Test die bevestigt dat de 6 I-VERT-knopen laden en de graph valide
      blijft (`tests/test_graph_validation.py` of nieuw bestand)
- [x] Test die bevestigt dat POLMO → I-VERT-POLMO-edge bestaat (de
      OL_E22_S1 → integratie-koppeling)
- [x] Geen regressie op bestaande tests

## Resultaat

- `data/graph/lat_integratie_leerjaar1.json` + `grc_integratie_leerjaar1.json`: elk 3 I-VERT-knopen (INTRO/NAAMVAL/POLMO), type `I`, met prerequisite-verankering aan grammatica- en POLMO-knopen. De NAAMVAL-knopen hosten elk 3 vertaalitems waar de naamval-uitgang subject/object bepaalt (incl. woordvolgorde-variant); klaar als `diagnose_items` voor OL_E22_S2.
- Koppeling OL_E22_S1 → integratie: `SHA-P-VERTAAL-POLMO-OV` is prerequisite van beide `…-I-VERT-POLMO`-knopen.
- Content: `LAT-I-VERT-INTRO.md` + `GRC-I-VERT-INTRO.md` (met Begrippen-sectie).
- Geen modelwijziging nodig — type `I` en domein `VERT` bestonden al.
- Tests: `tests/test_integratielaag.py` (5 tests: 6 knopen laden, type I, graph valide, POLMO-koppeling, ≥3 diagnostische items).

**Status:** volledige graph valideert groen (812 knopen, 1306 edges, 0 cycles); 738 pytest groen (geen regressie); ruff schoon.

## Scope
- Eerste, kleine integratielaag (6 knopen) — genoeg om OL_E22_S2 te enablen
- Geen herstructurering van bestaande knopen
- Geen volledige vertaal-curriculum (proza/poëzie, scanderen, interpretatie
  — dat zijn latere I-domeinen SCAN/INTERP/ONTL en eigen stories)

## Niet-doel
- Geen misconceptie-logica (dat is OL_E22_S2)
- Geen scheduler-wijziging
- Geen frontend-werk

## Afhankelijkheden
- **OL_E22_S1 (POLMO-DAG)** — done; `…-I-VERT-POLMO` verankert aan
  `SHA-P-VERTAAL-POLMO-OV`
- Blokkeert **OL_E22_S2** (Lego-vertaler-detectie)

## Geschat
Medium — pure data/content/tests, geen modelwijziging.
