# Sprintplan Gymnasium Classica

**Versie:** 0.1
**Datum:** 3 juni 2026
**Doel:** Een samenhangend, dependency-respecterend pad door alle open stories, zodat het werk gestructureerd naar een werkend en *meetbaar* resultaat loopt in plaats van ad hoc.

---

## Hoe dit plan te gebruiken

- **Eén sprint tegelijk, één story tegelijk.** Volg de story-workflow uit `CLAUDE.md`: `git mv` naar `doing/`, status in `EPICS.md` bijwerken, commit, afronden, `git mv` naar `done/`.
- **Sprints zijn thematisch, niet strikt even groot.** De volgorde respecteert afhankelijkheden; binnen een sprint staat de aanbevolen volgorde aangegeven.
- **De volgorde is een advies, geen wet.** Sprints 5 (mentor) en 6 (methodologie) zijn onderling verwisselbaar; sprint 7 (offline-loop) is bewust achteraan omdat het de grootste en minst pilot-kritische brok is.
- Dit plan is afgeleid van `stories/EPICS.md` (bron van waarheid voor status) en `docs/LITERATUURONDERZOEK_LEERBENADERING.md` (prioritering).

## Leidende uitgangspunten (uit het literatuuronderzoek)

1. **Meet vanaf dag één.** Zonder eigen meting blijft "efficiënter leren" een aanname (ontwerpkeuze 12). Daarom staat de meetlaag (L1) vóór de bredere uitbouw.
2. **Eerst de inner loop vergrendelen.** De ontwikkelstraat afmaken (OS) voorkomt ad-hoc werken — precies de gestelde valkuil.
3. **Sterkste hefbomen eerst:** spaced repetition + retrieval zijn al gebouwd; de grootste resterende winst zit in meten, het learner model en didactische kwaliteit, niet in nieuwe modaliteiten.
4. **Niet vroeg over-optimaliseren:** SR-algoritme (SM-2 volstaat), geavanceerde/neurale knowledge tracing en uitspraakbeoordeling blijven geparkeerd tot er data of noodzaak is.

---

## Overzicht

| Sprint | Thema | Stories | Hoofddoel |
|--------|-------|---------|-----------|
| **1** | Ontwikkelstraat vergrendelen | OS-07, OS-08, OS-09 | Kwaliteitspipeline af; minder ad-hoc |
| **2** | Meten + pilot live | L1-01, L1-02, E1-01 | Eerste echte leerling die meetbare data genereert |
| **3** | Leren van data + learner-model kern | L1-03, L2-01, L2-02 | Experimenteerbaar; receptief/productief; graph-aware |
| **4** | Didactische kwaliteit + motivatie/equity | L2-03, L3-01, L3-02, L3-03 | Worked examples, motivatie- en equity-laag |
| **5** | Mentor-inzicht (online diagnostiek) | F2-01, F1-13, F2-02, F2-03, F2-04 | Mentor ziet wáár én hóe een leerling struikelt |
| **6** | Methodologie: vertaalstrategie & bijspijkeren | M1-01, M1-02, M1-03 | POLMO, misconcepties, tweede gebruikersmodus |
| **7** | Offline-loop: OCR → LLM → portfolio | B6-01..05, B7-01..03, B8-01..03 | Offline schrijfwerk verifiëren, beoordelen, bundelen |
| **Parkeer** | Stretch (geblokkeerd) | B4-01, B4-02, B4-03 | Uitspraakbeoordeling — wacht op betrouwbare STT |

35 open stories: 3 in `doing`, 32 in `backlog`.

---

## Sprint 1 — Ontwikkelstraat vergrendelen

**Doel:** De zesde laag van de ontwikkelstraat afmaken zodat kwaliteit automatisch wordt afgedwongen en je daarna met vertrouwen kunt bouwen. Dit pakt direct de gestelde valkuil (ad-hoc werken) aan.

| Story | Titel | Status | Volgorde |
|-------|-------|--------|----------|
| OS-07 | Review-skills inbedden in workflow | doing | 1 |
| OS-08 | CLAUDE.md bijwerken met ontwikkelstraat-sectie | doing | 2 (na OS-07) |
| OS-09 | validation.py generiek per edge-type maken | backlog | parallel |

**Afhankelijkheden:** OS-08 documenteert OS-07; OS-09 is zelfstandig.
**Definition of done:** alle zes lagen actief, CI groen op `main`, ontwikkelstraat-werkwijze gedocumenteerd, break-test geblokkeerd op ≥2 lagen.
**Waarom nu:** in-flight werk afronden en de inner loop vastzetten is de goedkoopste manier om gestructureerd te blijven werken.

---

## Sprint 2 — Meten vanaf dag één + pilot live

**Doel:** De eerste echte leerling laten draaien, maar zó dat er vanaf het begin meetbare data ontstaat (retentie, tijd, mastery) met een baseline als nulpunt.

| Story | Titel | Status | Volgorde |
|-------|-------|--------|----------|
| L1-01 | Retentie- en sessiemetriek-logging | done | 1 |
| L1-02 | Baseline-intakemeting en effectgrootte-rapportage | done | 2 (na L1-01) |
| E1-01 | Pilot-ready milestone — eerste echte leerling | doing | 3 (met L1 op zijn plek) |

**Afhankelijkheden:** L1-02 → L1-01. E1-01 leunt op de al-done F1-pipeline (scaffolding, structured stimulus, audio); meetlaag erbij maakt de pilot pas evalueerbaar.
**Definition of done:** een echte leerling doorloopt dagelijkse sessies; baseline vastgelegd; retentie en effectgrootte zijn uit de data af te leiden.
**Waarom nu:** ontwerpkeuze 12 — meten vanaf het begin verandert de grootste zwakte (geen evidence voor klassieke talen) in een sterkte. Een pilot zonder meting verspilt de waardevolste databron.

---

## Sprint 3 — Leren van data + learner-model kern

**Doel:** Van data naar verbetering kunnen komen (controleerbare varianten) en het learner model versterken op de twee punten waar de literatuur de meeste winst ziet.

| Story | Titel | Status | Volgorde |
|-------|-------|--------|----------|
| L1-03 | A/B-experiment- en variant-framework | done | 1 |
| L2-01 | Receptieve en productieve mastery apart tracken | done | 2 |
| L2-02 | Learner-model-strategie-interface + graph-aware tracing | done | 3 (na L2-01) |

**Afhankelijkheden:** L1-03 → L1-01/02; L2-02 → L2-01.
**Definition of done:** leerstrategie-parameters zijn controleerbaar te variëren en per variant te meten; het model onderscheidt receptieve van productieve beheersing en kan de graph-structuur benutten; BKT zit achter een migreerbare interface.
**Waarom nu:** met de pilotdata uit sprint 2 kun je nu écht itereren in plaats van gokken.

---

## Sprint 4 — Didactische kwaliteit + motivatie/equity

**Doel:** Didactische patronen toevoegen die de literatuur ondersteunt, en de retentie-/motivatie-risico's afdekken.

| Story | Titel | Status | Volgorde |
|-------|-------|--------|----------|
| L2-03 | Learner-niveau parameters (individuele leersnelheid) | backlog | 1 |
| L3-01 | Worked-example oefentype met faded scaffolding | backlog | parallel |
| L3-02 | Motivatielaag tegen de metacognitieve illusie | backlog | na L1-01 |
| L3-03 | Equity-waarborgen voor zwakkere leerlingen | backlog | na L1-01/02 |

**Afhankelijkheden:** L2-03 → L2-02; L3-02/03 leunen op de meetlaag (L1).
**Definition of done:** worked examples beschikbaar als oefentype; motivatielaag legt uit waarom oefening zwaar voelt; equity-waarborg remt automatisch af bij lage-mastery-trajecten; individuele leersnelheid in het model.
**Waarom nu:** dit zijn de kwaliteits- en retentie-verbeteringen die het meest renderen zodra de kern-loop meet en itereert.

---

## Sprint 5 — Mentor-inzicht (online diagnostiek)

**Doel:** De data die F1-12 al verzamelt ontsluiten voor mentoren/docenten — cruciaal voor de secundaire doelgroep (bijles/remediatie).

| Story | Titel | Status | Volgorde |
|-------|-------|--------|----------|
| F2-01 | Mentor-rol + leerling-koppeling in user-model | backlog | 1 |
| F1-13 | Frontend mentor-view (placeholder) | backlog | 2 |
| F2-02 | Laatste foute antwoorden per leerling per knoop | backlog | 3 (na F2-01, F1-12) |
| F2-03 | Struikelpunten-overzicht per leerling | backlog | 4 (na F2-01) |
| F2-04 | Fout-classificatie (spelling/naamval/synoniem/macron) | backlog | parallel (na F1-12) |

**Afhankelijkheden:** F2-01 levert de user-rollen waar de rest op leunt; F1-12 (done) is de databron.
**Definition of done:** een mentor kan inloggen, leerlingen koppelen en per leerling per knoop zien wáár en hóe het misgaat, met eerste fout-classificatie.
**Waarom nu:** activeert waarde die sinds april 2026 al wordt verzameld, en bedient de bijles-doelgroep zodra de pilot draait.

---

## Sprint 6 — Methodologie: vertaalstrategie & bijspijkerroute

**Doel:** De WKM-spiegeling: vertaalstrategie als first-class object, misconceptie-diagnostiek en een tweede gebruikersmodus voor de gymnasiast die op school vastloopt.

| Story | Titel | Status | Volgorde |
|-------|-------|--------|----------|
| M1-01 | Knoop-type P (Procedure) + POLMO-stappen-DAG | backlog | 1 |
| M1-02 | Misconceptie-attribuut + Lego-vertaler-detectie | backlog | 2 (na M1-01) |
| M1-03 | Bijspijkerroute — methode-en-hoofdstuk-gestuurde catch-up | backlog | 3 |

**Afhankelijkheden:** M1-02 → M1-01; M1-03 leunt op E1 (pilot, sprint 2) en profiteert van M1-01/02. M1-01 introduceert ontwerpkeuze 11.
**Definition of done:** POLMO is gemodelleerd en oefenbaar; eerste misconceptie-detector werkt; bijspijkermodus beschikbaar als tweede planner-modus.
**Waarom nu:** verbreedt de doelgroep en de didactische diepgang; profiteert van de mentor-diagnostiek uit sprint 5 (misconceptie-flags zijn precies wat een mentor wil zien).

---

## Sprint 7 — Offline-loop: OCR → LLM-feedback → portfolio

**Doel:** Offline schrijfwerk (al gebouwd in B5) sluiten met verificatie, inhoudelijke beoordeling en een mentor-portfolio. Grote brok; loop deze als drie deelblokken.

**7a — OCR-pipeline**

| Story | Titel | Status |
|-------|-------|--------|
| B6-01 | Camera-capture component — frontend | backlog |
| B6-02 | OCR Grieks alfabet — letterherkenning | backlog |
| B6-03 | OCR paradigmatabellen — gestructureerde herkenning | backlog |
| B6-04 | OCR Nederlandse vertalingen — handschriftherkenning | backlog |
| B6-05 | BKT-integratie OCR — confidence-mapping | backlog |

**7b — LLM-vertaalbeoordeling** (na 7a)

| Story | Titel | Status |
|-------|-------|--------|
| B7-01 | LLM-vergelijking met modelantwoord | backlog |
| B7-02 | Foutcategorisatie en feedback-generatie | backlog |
| B7-03 | Integratie met BKT en conditional completion | backlog |

**7c — Mentor-portfolio** (na 7a; deelt UI met sprint 5)

| Story | Titel | Status |
|-------|-------|--------|
| B8-01 | Portfolio-selectie-algoritme | backlog |
| B8-02 | Portfolio PDF-generatie | backlog |
| B8-03 | Mentor-dashboard en Addisco-integratie | backlog |

**Afhankelijkheden:** B6 → B5 (done); B7 → B6 + Claude API; B8 → B5 + B6.
**Definition of done:** een leerling fotografeert schrijfwerk, OCR + LLM geven feedback, en de mentor krijgt een maandelijks portfolio.
**Waarom achteraan:** grootste omvang, minst pilot-kritisch, en bouwt op de mentor-UI uit sprint 5.

---

## Parkeer-bucket — stretch / geblokkeerd

| Story | Titel | Reden |
|-------|-------|-------|
| B4-01 | Montreal Forced Aligner evaluatie en integratie | STT voor klassieke talen onvoldoende betrouwbaar |
| B4-02 | Pronunciation scoring model | idem; wacht op B3-betrouwbaarheid |
| B4-03 | Pronunciation feedback integratie in oefentypen | idem |

Niet inplannen tot STT-betrouwbaarheid voor Latijn/Grieks aantoonbaar verbetert.

---

## Kritisch pad (samenvatting)

```
OS-07/08/09  →  L1-01 → L1-02 → E1-01 (pilot)  →  L1-03
                                          ↘ L2-01 → L2-02 → L2-03
                                                         ↘ L3-01/02/03
E1-01 ──────────────────────────────────────────────→ M1-03
F1-12 (done) ─→ F2-01 → F2-02/03/04 ; F1-13
M1-01 → M1-02
B5 (done) → B6-* → B7-* ; B6-* → B8-*
```

De enige harde "must-finish-first" voor de pilot is de meetlaag (L1-01/02). Al het overige bouwt incrementeel verder op een draaiende, gemeten pilot.

---

*Levend document. Bij elke afgeronde sprint: status bijwerken in `stories/EPICS.md` en zo nodig de volgorde van de resterende sprints herijken op basis van pilot-bevindingen.*
