---
type: story
project: GC
epic: E22
story_id: OL_E22_S1
legacy_id: M1-01
track: didactiek
status: done
prioriteit: middel
---

# Story OL_E22_S1: Knoop-type P (Procedure) + POLMO-stappen-DAG

## Doel
Voeg een vijfde knoop-type **P (Procedure/Strategie)** toe aan het
KennisKnoop-model en modelleer de canonieke vertaalstrategie **POLMO**
als eerste procedure-DAG, voor zowel Latijn als Grieks. Dit maakt het
mogelijk om de *vertaalprocedure zelf* als leerbare en diagnoseerbare
eenheid te behandelen, naast de declaratieve grammatica- en
woordkennis.

## Achtergrond

Wijkunnenmeer (Reijgwart) noemt vier problemen bij intuïtieve
("Lego-")vertalers:

1. te kleine woordenschat
2. onvoldoende grammaticakennis
3. niet kunnen ontleden
4. **geen systematische vertaalmethode**

De eerste drie matchen op Olympus' types V (vocabulaire), G
(grammatica) en I (integratie/ontleden). Het vierde — de
**procedurele stappenvolgorde** zelf — heeft op dit moment geen plek
in het model. Een leerling kan alle naamvallen kennen en alle woorden
beheersen en tóch steevast verkeerd vertalen, omdat hij geen
strategie toepast.

POLMO is de Nederlandse standaard-vertaalstappenplan ("vrijwel altijd
werkt", "bestaat al heel lang"). De afkorting staat voor de volgorde
waarin een leerling zinsdelen identificeert:

- **P**ersoonsvorm
- **O**nderwerp
- **L**ijdend voorwerp
- **M**eewerkend voorwerp
- **O**verige (bijwoordelijke bepalingen, bijzinnen, congruentie)

Door deze stappen als knopen te modelleren met een eigen prerequisite-
keten, kan:

- **diagnostiek per stap** plaatsvinden ("leerling vindt persoonsvorm
  wel maar onderwerp niet")
- **scheduling per stap** ("leerling moet eerst stap 2 inslijten
  voordat stap 3 zin heeft")
- **misconceptie-detectie** (OL_E22_S2) terugslaan op een specifieke stap

## Input

- `src/gymnasium_classica/models/graph.py` — `KnoopType`-enum,
  `KennisKnoop`, `EdgeType`-enum, `PrerequisiteEdge`
- `src/gymnasium_classica/schemas/id_schema.py` — ID-validatie (P moet
  worden toegevoegd als geldig type-segment)
- `src/gymnasium_classica/graph/loader.py` — directory-loading van
  graph-JSONs
- `src/gymnasium_classica/graph/validation.py` — cycle/orphan checks
- `data/graph/lat_grammatica_leerjaar1.json` als referentie voor schema
- `docs/externe-bronnen/wkm-problemen-latijn-grieks.md` — brontekst

## Acceptatiecriteria

- [x] `KnoopType` uitgebreid met waarde `P` ("Procedure/Strategie")
- [x] `id_schema.validate_knoop_id()` accepteert `P` als geldig
      type-segment (bijv. `LAT-P-VERTAAL-POLMO-PV`)
- [x] `EdgeType` uitgebreid met waarde `procedure_step` — een
      *volgordelijke* edge die zegt "deze stap volgt op die stap",
      onderscheiden van `prerequisite` (dat zegt "deze knoop moet
      beheerst zijn voordat je deze andere kunt leren")
- [x] Validator: voor elke procedure (groep knopen verbonden via
      `procedure_step`) geldt: het is een lineair pad (geen
      vertakkingen), exact één knoop heeft geen inkomende
      `procedure_step`-edge (de start), exact één knoop heeft geen
      uitgaande (het einde)
- [x] Nieuwe graph-JSON `data/graph/sha_strategie_polmo.json` met:
  - 1 conceptknoop `SHA-P-VERTAAL-POLMO-INTRO` ("Wat is POLMO en
    wanneer pas je het toe?")
  - 5 stap-knopen voor de canonieke volgorde: `SHA-P-VERTAAL-POLMO-PV`
    (persoonsvorm), `-OND` (onderwerp), `-LV` (lijdend voorwerp),
    `-MV` (meewerkend voorwerp), `-OV` (overig)
  - `procedure_step`-edges PV → OND → LV → MV → OV
  - Reguliere `prerequisite`-edges van elke stap naar de relevante
    G-knopen (PV → werkwoordsmorfologie-conceptknoop; OND → nominativus;
    LV → accusativus; MV → datief/dativus; OV → ablativus + voorzetsels +
    bijzinnen)
- [x] Taal van de POLMO-knopen is `shared` (de strategie geldt voor
      Latijn én Grieks). Eventuele taalspecifieke verfijningen krijgen
      eigen LAT-P- of GRC-P-knopen in een latere story
- [x] Tests in `tests/test_graph_validation.py`:
  - graph laadt succesvol met de nieuwe knopen en edges
  - cycle-detection ziet de POLMO-keten niet als cycle (procedure_step
    is acyclisch)
  - validator detecteert een geconstrueerde malformed POLMO
    (vertakking, dubbele start) als fout
- [x] Geen regressie: alle 165+ bestaande tests blijven groen
- [x] Korte uitbreiding van `docs/ONTWERPKEUZES_GYMNASIUM_CLASSICA.md`
      met "Keuze 11: Procedurele knopen" — onderbouwing en
      architecturale implicaties (analoog aan de bestaande
      keuzes-structuur)
- [x] Markdown-content `data/content/SHA-P-VERTAAL-POLMO-INTRO.md` met
      uitleg van de strategie en wanneer toe te passen (1 bestand —
      verdere content per stap volgt in een latere story)

## Resultaat

- `models/graph.py`: `NodeType.P` + `EdgeType.PROCEDURE_STEP` toegevoegd.
- `schemas/id_schema.py`: `P` geldig in regex + `TYPE_VALUES` + `PROCEDURE_DOMAINS` (`VERTAAL`). Functie heet `validate_node_id` (Engels in code).
- `graph/validation.py`: `procedure_step` opgenomen in `ACYCLIC_EDGE_TYPES`; nieuwe `validate_procedures()` (lineair-pad-check: geen vertakking, exact één start/eind), gewired als stap 10 in `validate_graph`.
- `data/graph/sha_strategie_polmo.json`: 6 `shared` P-knopen (INTRO + PV/OND/LV/MV/OV), `procedure_step`-keten PV→OND→LV→MV→OV, en `prerequisite`-edges van de Latijnse grammatica-ankers (`MORF-PERSOON-INTRO`, `SYNT-{NOM,ACC,DAT,ABL}-FUNCTIE`, `SYNT-PREP-INTRO`, `SYNT-BIJW-BEP`) naar de stappen. Volledige graph valideert groen (806 knopen, 1 component, 0 cycles).
- `data/content/SHA-P-VERTAAL-POLMO-INTRO.md`: didactische uitleg + Begrippen-sectie.
- `docs/ONTWERPKEUZES_…`: "Keuze 11: Procedurele knopen" ingevuld (de slot was expliciet gereserveerd).
- `tests/test_graph_validation.py`: 8 nieuwe tests (lineaire keten valide, branching/dubbele-start afgewezen, procedure_step-cyclus gedetecteerd, integratietest op de echte graph). Bestaande policy-set-test bijgewerkt.

**Bewuste keuze:** POLMO is `shared`, maar de grammatica-ankers zijn nu Latijnse `SYNT-FUNCTIE`-knopen (Latijn = instaptaal). Griekse verankering + per-taal verfijning (`LAT-P-`/`GRC-P-`-ketens) zijn uitgesteld naar een vervolgstory — vastgelegd in keuze 11 (A11.3) en conform story-scope.

**Status:** 733 pytest groen (geen regressie), ruff + mypy strict schoon.

## Scope

- Alleen het datamodel + de POLMO-DAG zelf
- Geen items/oefeningen voor de stap-knopen (komt in een vervolgstory)
- Geen scheduler-uitbreidingen (komt in OL_E22_S2 en OL_E22_S3)
- Geen frontend-aanpassingen
- Eén procedure (POLMO); andere procedures (zinsontleden Grieks
  specifiek, scanderen, etc.) zijn aparte latere stories

## Niet-doel

- Geen herstructurering van bestaande I-knopen — die blijven
  uitkomst-knopen ("vertaal deze AcI-zin"). De P-knopen leven daarnaast
  en worden via prerequisite-edges aan de I-knopen gekoppeld in OL_E22_S2
- Geen automatische foutclassificatie op basis van POLMO-stap (dat is
  een uitbreiding van OL_E21_S4 die in een latere story landt)

## Afhankelijkheden

- Geen harde afhankelijkheden — bouwt op het bestaande graph-model
- Wenselijk parallel met **OL_E22_S2** (misconcepties) zodat de
  Lego-vertaler-detectie meteen kan terugslaan op POLMO-stappen
- **OL_E20_S1** (ScaffoldingPanel rendert markdown) is al done, dus de
  POLMO-INTRO-content is direct zichtbaar in de huidige frontend

## Geschat

Medium — modelaanpassing is klein, maar er zijn aanpassingen op zes
plekken (model, schema, loader, validator, data, content) plus tests
en een ontwerpkeuze-document.
