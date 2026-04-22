# Epics overzicht

## Spoor A — Knowledge graph content

Leerjaar 1 gymnasium, beide talen. Doelomvang: ~850 knopen, ~1500-2000 edges.

## Uitvoervolgorde

1. **A3** (alfabet) — klein, zelfstandig, blokkeert niets
2. **A1** (grammatica Latijn) — bouwt voort op de 50 PoC-knopen
3. **A2** (grammatica Grieks) — structureel parallel aan A1
4. **A4** (vocabulaire) — heeft A1+A2+A3 nodig voor prerequisite-edges
5. **A5** (cultuur) — onafhankelijk van A1-A4 maar edges lopen ernaar
6. **A6** (transfer-edges) — heeft A1+A2+A3+A4+A5 nodig

---

## Epic A1: Grammatica Latijn

**Doel:** Methode-onafhankelijke grammaticale kern van klas 1, gebaseerd op de CvTE-minimumlijst gefilterd op wat alle methoden gemeen hebben.
**Geschat:** ~150 knopen
**Afhankelijkheden:** Geen (bouwt voort op bestaande PoC)
**Status:** done
**Bestand:** `data/graph/lat_grammatica_leerjaar1.json`

| Story | Titel | Knopen | Status |
|-------|-------|--------|--------|
| A1-01 | Conceptknopen en naamvalsysteem | 6 | done |
| A1-02 | 1e declinatie — alle naamvallen + paradigma | 4 | done |
| A1-03 | 2e declinatie — o-stammen masculinum + neutrum | 5 | done |
| A1-04 | 3e declinatie — consonantstammen + i-stammen basis | 10 | done |
| A1-05 | Adjectieven bonus-type en fortis-type | 7 | done |
| A1-06 | Werkwoord-concepten — conjugatie-intro, persoon, tempus, modus | 6 | done |
| A1-07 | Praesens indicativus actief — 4 conjugaties + esse | 5 | done |
| A1-08 | Imperfectum indicativus actief | 4 | done |
| A1-09 | Perfectum indicativus actief — inclusief stamtijdentypen | 12 | done |
| A1-10 | Plusquamperfectum indicativus actief | 5 | done |
| A1-11 | Imperativus + infinitivus praesens actief | 5 | done |
| A1-12 | Pronomina — persoonlijk, bezittelijk, aanwijzend begin | 11 | done |
| A1-13 | Voorzetsels met accusativus en ablativus | 6 | done |
| A1-14 | Basissyntaxis — woordvolgorde, congruentie, ontkenning, vraagzinnen | 7 | done |
| A1-15 | Review en prerequisite-edge validatie voor heel epic A1 | — | done |

---

## Epic A2: Grammatica Grieks

**Doel:** Griekse grammaticale kern van klas 1, gebaseerd op de GTC-minimumlijst gefilterd op klas 1 scope (Pallas les 1-14 / ARGO thema 1-4).
**Geschat:** ~100 knopen
**Afhankelijkheden:** A3 (alfabet moet af als prerequisite)
**Status:** done
**Bestand:** `data/graph/grc_grammatica_leerjaar1.json`

| Story | Titel | Knopen | Status |
|-------|-------|--------|--------|
| A2-01 | Conceptknopen Grieks — lidwoord, naamvalsysteem | 11 | done |
| A2-02 | 1e declinatie (α/η-stammen) | 10 | done |
| A2-03 | 2e declinatie (ο-stammen) | 10 | done |
| A2-04 | 3e declinatie introductie — via adjectieven πᾶς, σώφρων | 8 | done |
| A2-05 | Adjectieven α/ο-stam en medeklinkerstam | 8 | done |
| A2-06 | Praesens indicativus actief — thematisch + contracta + εἰμί | 12 | done |
| A2-07 | Imperfectum indicativus actief — augment | 8 | done |
| A2-08 | Aoristus introductie — sigmatisch + thematisch | 10 | done |
| A2-09 | Pronomina — persoonlijk, bezittelijk, aanwijzend | 10 | done |
| A2-10 | Voorzetsels + basissyntaxis | 8 | done |
| A2-11 | Review en prerequisite-edge validatie voor heel epic A2 | — | done |

---

## Epic A3: Grieks alfabet — onboarding-subgraph

**Doel:** Grieks alfabet als onboarding-subgraph. Prerequisite voor alle GRC-grammaticaknopen.
**Geschat:** ~40 knopen
**Afhankelijkheden:** Geen
**Status:** done
**Bestand:** `data/graph/grc_alfabet.json`

| Story | Titel | Knopen | Status |
|-------|-------|--------|--------|
| A3-01 | Letters herkenning — 24 letters, majuskel + minuskel | 29 | done |
| A3-02 | Diakritische tekens — spiritus, accenten, iota subscriptum | 10 | done |
| A3-03 | Lettercombinaties en uitspraak — diphthongen, γγ=ng, speciale combinaties | 8 | done |

---

## Epic A4: Vocabulaire

**Doel:** Individuele woorden, frequentiegestuurd, met semantisch cluster.
**Geschat:** ~450 knopen
**Afhankelijkheden:** A1, A2, A3 (voor prerequisite-edges naar grammaticaknopen)
**Status:** done
**Bestanden:** `data/graph/lat_vocabulaire_leerjaar1.json`, `data/graph/grc_vocabulaire_leerjaar1.json`

| Story | Titel | Knopen | Status |
|-------|-------|--------|--------|
| A4-01 | Strategie en bronnen — DCC Latin/Greek Core, cluster-definitie | — | done |
| A4-02 | Latijn frequentieband F01 — top-100 woorden | 100 | done |
| A4-03 | Latijn frequentieband F02 — woorden 101-200 | 100 | done |
| A4-04 | Latijn frequentieband F03 — woorden 201-300 | 100 | done |
| A4-05 | Grieks frequentieband F01 — top-75 woorden | 75 | done |
| A4-06 | Grieks frequentieband F02 — woorden 76-150 | 75 | done |
| A4-07 | Prerequisite-edges vocabulaire → grammatica | 21 edges | done |
| A4-08 | Enrichment-edges voor onverbuigbare vocabulaire (bijwoorden, voegwoorden, partikels) | 46 edges | done |

---

## Epic A5: Cultuur

**Doel:** Gedeelde (SHA-C-*) cultuurknopen voor leerjaar 1.
**Geschat:** ~70 knopen
**Afhankelijkheden:** Geen (maar enrichment-edges naar A1/A2/A4)
**Status:** done
**Bestand:** `data/graph/sha_cultuur_leerjaar1.json`

| Story | Titel | Knopen | Status |
|-------|-------|--------|--------|
| A5-01 | Mythologie — Olympische goden, helden, Troje, Odysseus | 20 | done |
| A5-02 | Romeins dagelijks leven — familia, domus, school, eten, slavernij | 15 | done |
| A5-03 | Geschiedenis basis — Romulus, Republiek, legioenen, forum | 15 | done |
| A5-04 | Grieks dagelijks leven — polis, agora, gymnasium, symposium | 10 | done |
| A5-05 | Taal en schrift — Latijns alfabet, Grieks alfabet, inscripties | 5 | done |
| A5-06 | Prerequisite-edges cultuur → taal/integratie | 11 edges | done |

---

## Epic A6: Transfer-edges

**Doel:** Cross-linguïstische verbindingen (type `transfer`) tussen Latijn en Grieks.
**Geschat:** ~100 edges
**Afhankelijkheden:** A1, A2, A3, A4, A5 (alle knopen moeten bestaan)
**Status:** done
**Bestand:** `data/graph/transfer_edges_leerjaar1.json`

| Story | Titel | Edges | Status |
|-------|-------|-------|--------|
| A6-01 | Naamvalsysteem — LAT ↔ GRC naamvallen | 30 | done |
| A6-02 | Werkwoordsmorfologie — praesens/imperfectum/aoristus parallellen | 30 | done |
| A6-03 | Cultuur — gedeelde mythologie en geschiedenis | 20 | done |
| A6-04 | Vocabulaire — cognaten en leenwoorden | 20 | done |
| A6-05 | Validatie transfer-edges — geen cycli, weights correct | — | done |

---

## Spoor B-audio — TTS en STT voor Latijn en Grieks

Audio-laag voor multi-modale taalverwerving. Gefaseerd: TTS in fase 3, STT in fase 5.

### Uitvoervolgorde

1. **B1** (TTS-pipeline) — evaluatie tools + audio genereren voor ~450 V-knopen
2. **B2** (audio-oefentypen) — nieuwe ItemTypes + frontend player
3. **B3** (STT-integratie) — spraakherkenning + mondelinge oefentypen
4. **B4** (pronunciation assessment) — foneem-scoring + feedback (stretch goal)

---

## Epic B1: TTS-pipeline en audio-generatie

**Doel:** Evalueer en bouw een TTS-pipeline voor klassiek Latijn (klassieke uitspraak) en Grieks (Erasmiaans). Genereer audio voor alle V-knopen.
**Geschat:** ~450 audiobestanden
**Afhankelijkheden:** A4 (vocabulaireknopen moeten bestaan)
**Status:** done (placeholder WAV; echte audio vereist espeak-ng of handmatige opnames)

| Story | Titel | Geschat | Status |
|-------|-------|---------|--------|
| B1-01 | TTS-evaluatie Latijn — Poeta ex Machina en alternatieven | — | done |
| B1-02 | TTS-evaluatie Grieks — Erasmiaans en alternatieven | — | done |
| B1-03 | TTS-pipeline bouwen — audio-generatiescript | — | done |
| B1-04 | Audio genereren — Latijn V-knopen F01-F03 | ~300 bestanden | done |
| B1-05 | Audio genereren — Grieks V-knopen F01-F02 | ~150 bestanden | done |

---

## Epic B2: Audio-oefentypen

**Doel:** Nieuwe oefentypen die audio gebruiken: luister-en-herken, luister-en-schrijf. Frontend audioplayer.
**Geschat:** ~400 items + frontend component
**Afhankelijkheden:** B1 (audio moet bestaan)
**Status:** done

| Story | Titel | Geschat | Status |
|-------|-------|---------|--------|
| B2-01 | ItemType uitbreiden — luister-oefentypen | — | done |
| B2-02 | Audio player component — frontend | — | done |
| B2-03 | Luister-en-herken oefeningen genereren | 450 items | done |
| B2-04 | Luister-en-schrijf oefeningen genereren | 450 items | done |

---

## Epic B3: STT-integratie

**Doel:** Spraakherkenning voor mondelinge oefeningen en examensimulatie. AVG-conforme verwerking.
**Geschat:** STT-pipeline + mondelinge oefentypen
**Afhankelijkheden:** B1 (referentie-audio), fase 5
**Status:** done (stub-implementatie; echte STT niet haalbaar voor klassieke talen in huidige fase)

| Story | Titel | Geschat | Status |
|-------|-------|---------|--------|
| B3-01 | STT-evaluatie — Whisper vs. Voxtral | — | done |
| B3-02 | STT-pipeline bouwen — transcriptie-module | — | done |
| B3-03 | Mondelinge oefentypen — spreek-na en beantwoord mondeling | — | done |
| B3-04 | Privacy-implementatie — spraakdata AVG-conform | — | done |

---

## Epic B4: Pronunciation assessment (stretch goal)

**Doel:** Foneem-niveau uitspraakbeoordeling met MFA. Per-foneem feedback.
**Geschat:** Scoring model + feedback-integratie
**Afhankelijkheden:** B3 (STT moet werken)
**Status:** geparkeerd (STT voor klassieke talen onvoldoende betrouwbaar)

| Story | Titel | Geschat | Status |
|-------|-------|---------|--------|
| B4-01 | Montreal Forced Aligner evaluatie en integratie | — | todo |
| B4-02 | Pronunciation scoring model | — | todo |
| B4-03 | Pronunciation feedback integratie in oefentypen | — | todo |

---

## Spoor B-offline — Schrijfoefeningen, OCR en mentor-portfolio

Offline schrijven als volwaardige oefenvorm met OCR-verificatie en mentor-portfolio.

### Uitvoervolgorde

1. **B5** (offline oefentypen) — datamodel, self-report, PDF-werkbladen, scheduling
2. **B6** (OCR-pipeline) — camera-capture, Grieks alfabet, paradigma's, vertalingen
3. **B7** (LLM-vertaalbeoordeling) — OCR + LLM-feedback op vertalingen
4. **B8** (mentor-portfolio) — selectie, PDF-generatie, Addisco-integratie

---

## Epic B5: Offline oefentypen en scheduling

**Doel:** Offline schrijfoefeningen als gepland onderdeel van de learning loop. Self-report flow, printbare werkbladen, scheduling aan einde sessie.
**Geschat:** ~100 items + scheduling-logica + PDF-generatie
**Afhankelijkheden:** A1, A2, A3 (grammaticaknopen moeten bestaan)
**Status:** todo

| Story | Titel | Geschat | Status |
|-------|-------|---------|--------|
| B5-01 | Offline oefentype en scheduling-integratie | — | done |
| B5-02 | Self-report flow en BKT-integratie met verlaagde confidence | — | done |
| B5-03 | Printbare PDF-werkbladen genereren | — | done |
| B5-04 | Paradigma-schrijfoefeningen genereren | ~50 items | done |
| B5-05 | Vertaal-op-papier oefeningen genereren | ~30 items | done |
| B5-06 | Grieks alfabet schrijfoefeningen | ~24 items | done |

---

## Epic B6: OCR-pipeline

**Doel:** OCR-verificatie voor offline schrijfwerk waar dat beslissend is voor progressie: Grieks alfabet (blokkerend), paradigmatabellen (progressie-kritisch), vertalingen (feedback-kritisch).
**Geschat:** OCR-pipeline + BKT-integratie
**Afhankelijkheden:** B5 (offline items moeten bestaan), fase 5
**Status:** todo

| Story | Titel | Geschat | Status |
|-------|-------|---------|--------|
| B6-01 | Camera-capture component — frontend | — | todo |
| B6-02 | OCR Grieks alfabet — letterherkenning | — | todo |
| B6-03 | OCR paradigmatabellen — gestructureerde herkenning | — | todo |
| B6-04 | OCR Nederlandse vertalingen — handschriftherkenning | — | todo |
| B6-05 | BKT-integratie OCR — confidence-mapping | — | todo |

---

## Epic B7: LLM-vertaalbeoordeling

**Doel:** Na OCR-transcriptie van een vertaling: LLM vergelijkt met modelantwoord en genereert inhoudelijke feedback per foutcategorie.
**Geschat:** LLM-pipeline + foutcategorisatie
**Afhankelijkheden:** B6 (OCR moet werken), Claude API
**Status:** todo

| Story | Titel | Geschat | Status |
|-------|-------|---------|--------|
| B7-01 | LLM-vergelijking met modelantwoord | — | todo |
| B7-02 | Foutcategorisatie en feedback-generatie | — | todo |
| B7-03 | Integratie met BKT en conditional completion | — | todo |

---

## Epic B8: Mentor-portfolio

**Doel:** Maandelijks portfolio met selectie van meest informatieve offline werk. PDF-export, optionele Addisco-integratie.
**Geschat:** Selectie-algoritme + PDF-generatie
**Afhankelijkheden:** B5, B6 (offline werk en OCR-resultaten)
**Status:** todo

| Story | Titel | Geschat | Status |
|-------|-------|---------|--------|
| B8-01 | Portfolio-selectie-algoritme | — | todo |
| B8-02 | Portfolio PDF-generatie | — | todo |
| B8-03 | Mentor-dashboard en Addisco-integratie | — | todo |

---

## Spoor C — Items en content voor Latijnse grammatica

Items (oefeningen) en didactische content voor de LAT-G knopen, richting pilot.
Zie `docs/Prompt_spoor_c.md` voor de volledige prompt.

### Uitvoervolgorde

- **C1** en **C2** zijn onderling onafhankelijk en kunnen parallel
- C1-stories hangen af van de corresponderende A1-story (knopen moeten bestaan)
- C2-stories hangen af van dezelfde A1-knopen maar niet van C1

---

## Epic C1: Items genereren — Latijnse grammatica

**Doel:** Oefeningen genereren voor alle LAT-G knopen. Mix van herkenning, productie, analyse, contextueel.
**Geschat:** ~330 items
**Afhankelijkheden:** A1 (per story: corresponderende A1-story moet done zijn)
**Status:** done

| Story | Titel | Geschat | Status |
|-------|-------|---------|--------|
| C1-01 | Items voor conceptknopen (INTRO) | 24 items | done |
| C1-02 | Items voor 1e declinatie | 30 items | done |
| C1-03 | Items voor 2e declinatie | 39 items | done |
| C1-04 | Items voor 3e declinatie | 37 items | done |
| C1-05 | Items voor adjectieven | 25 items | done |
| C1-06 | Items voor presens indicativus | 38 items | done |
| C1-07 | Items voor imperfectum + perfectum | 39 items | done |
| C1-08 | Items voor plqpf + imperativus + infinitivus | 22 items | done |
| C1-09 | Items voor pronomina | 24 items | done |
| C1-10 | Items voor voorzetsels + syntaxis | 32 items | done |
| C1-11 | Validatie: dekking, IRT-parameters, oefentype-mix | — | done |

---

## Epic C2: Content schrijven — Latijnse grammatica

**Doel:** Didactische markdown content voor de kernknopen: paradigmatabellen, uitleg, herkenningstips.
**Geschat:** ~34 bestanden
**Afhankelijkheden:** A1 (knopen moeten bestaan)
**Status:** done

| Story | Titel | Geschat | Status |
|-------|-------|---------|--------|
| C2-01 | Content voor concept-INTRO knopen | 8 bestanden | done |
| C2-02 | Content voor declinatie-paradigma's | 6 bestanden | done |
| C2-03 | Content voor werkwoord-paradigma's | 8 bestanden | done |
| C2-04 | Content voor syntaxis | 6 bestanden | done |
| C2-05 | Content voor pronomina + adjectieven | 6 bestanden | done |

---

## Spoor D — Werkende MVP-applicatie (FastAPI + React)

De engine naar een webapplicatie brengen. Zie `docs/Prompt_spoor_d.md` voor de volledige prompt.

### Uitvoervolgorde

1. **D1** (backend) en **D2-01+02** (frontend setup + login) kunnen parallel
2. **D2-03+** heeft D1-05 nodig (session endpoints)
3. **D3** na D1+D2 compleet

---

## Epic D1: FastAPI backend

**Doel:** REST API die de sessie-engine wraps. SQLite persistence. Auth.
**Geschat:** 8 stories
**Afhankelijkheden:** Geen (bouwt op bestaande engine)
**Status:** done

| Story | Titel | Status |
|-------|-------|--------|
| D1-01 | Project setup: FastAPI + uvicorn + SQLite | done |
| D1-02 | Auth endpoints: register + login | done |
| D1-03 | Database CRUD: users + learner_models | done |
| D1-04 | SessionManager: stapsgewijs sessie-protocol | done |
| D1-05 | Session endpoints: start + answer | done |
| D1-06 | Session endpoint: summary | done |
| D1-07 | Progress endpoints | done |
| D1-08 | Intake endpoints | done |

---

## Epic D2: React frontend

**Doel:** Minimale maar functionele UI: login, sessie-interface, dashboard.
**Geschat:** 7 stories
**Afhankelijkheden:** D1-02 (auth), D1-05 (session), D1-07 (progress)
**Status:** todo

| Story | Titel | Status |
|-------|-------|--------|
| D2-01 | Project setup: Vite + React + routing | done |
| D2-02 | Login pagina | done |
| D2-03 | Session pagina: vraag tonen | done |
| D2-04 | Session pagina: antwoord + feedback | done |
| D2-05 | Session pagina: samenvatting | done |
| D2-06 | Dashboard pagina | done |
| D2-07 | Polytonic Greek input | done |

---

## Epic D3: Integratie en pilot-ready

**Doel:** Alles draait samen. Dev server, seed data, end-to-end test.
**Geschat:** 3 stories
**Afhankelijkheden:** D1 + D2 compleet
**Status:** done

| Story | Titel | Status |
|-------|-------|--------|
| D3-01 | Dev server script + CORS + proxy | done |
| D3-02 | Seed script: test-user met intake | done |
| D3-03 | End-to-end smoke test + pilot guide | done |

---

## Spoor F — Content-ontsluiting en kwaliteitsverbetering

Bestaand materiaal (markdowns, audio, MC-opties, vocab-metadata) daadwerkelijk naar de leerling krijgen, en dekkingsgaten dichten waar dat leerrendement oplevert. Focus op wat al in `data/` staat maar niet bereikt wordt.

### Uitvoervolgorde

1. **F1-11** eerst — dekkingsrapport geeft baseline
2. **F1-01** en **F1-03** — frontend-pipeline werkend (scaffolding + structured stimulus); blokkerend voor rest
3. **F1-04** — audio pipeline
4. **F1-02**, **F1-05**, **F1-06** — parallel, bouwen voort op 01/03
5. **F1-07**, **F1-08** — content-uitbreiding, na pipeline
6. **F1-09**, **F1-10** — opschoning, kan altijd

---

## Epic F1: Content-ontsluiting en kwaliteitsverbetering

**Doel:** Het gat dichten tussen aanwezig materiaal en wat de leerling daadwerkelijk ziet. Frontend-pipeline voor `scaffolding_content`, structured stimulus (MC-opties, hints) en audio-playback; vocab-metadata ontsluiten; content-dekking van LAT-G opschalen; cultuurknopen oefenbaar maken; dode data opruimen; permanente monitoring via dekkingsrapport.
**Geschat:** 11 stories
**Afhankelijkheden:** D1 + D2 compleet (engine en frontend draaien)
**Status:** todo

| Story | Titel | Status |
|-------|-------|--------|
| F1-01 | Frontend ScaffoldingPanel — render `scaffolding_content` als markdown | done |
| F1-02 | Scaffolding ook in grammar-first (opt-in) bij eerste introductie | done |
| F1-03 | Frontend rendert structured stimulus (instruction / hint / options) | done |
| F1-04 | AudioPlayer component + afspelen van `audio_ref` in luister-items | done |
| F1-05 | Woordkaart — toon structured vocab-metadata uit vocab_sources | done |
| F1-06 | `content_ref` expliciet zetten in alle graph-JSONs + validator | done |
| F1-07 | LAT-G content-dekking verhogen naar hot-path ≥ 80 % | done |
| F1-08 | Cultuurknopen oefenbaar maken (items + korte markdown) | done |
| F1-09 | Ontsluit of verwijder `vocabulaire_clusters.json` | done |
| F1-10 | Opschonen passages — merge `lat_passages_leerjaar1.json` | done |
| F1-11 | Content-dekkingsrapport — script + CI-check | done |
| F1-12 | Telemetrie-uitbreiding — `answer_text` + `item_history` wiring | done |
| F1-13 | Frontend mentor-view (placeholder) | backlog |
| F1-19 | Diverse content-opschoning ronde 2 | done |

**Verhouding tot andere epics:**
- F1 overlapt niet met **A-spoor** (graph-structuur) — die is af.
- F1-04 vult de frontend-kant aan die B2 voorondersteld had; echte audio komt later via **E2**.
- F1-07/F1-08 raken aan **C2** (LAT-G-content) en **E3** (GRC-G + SHA-C items/content). F1 levert eerst de pipeline en basis-oefenbaarheid; E3 kan verdiepend Grieks-materiaal toevoegen.
- F1 is pilot-kritisch: zonder F1-01, F1-03 en F1-04 blijft veel van het gegenereerde materiaal onzichtbaar voor de leerling en is een **E1**-pilot minder waardevol.

---

## Epic F2: Mentor-dashboard

**Doel:** Mentoren en docenten in staat stellen om leerlingen op concreet niveau te helpen. Niet alleen *dat* een leerling struikelt op een knoop, maar *hoe*: welke letterlijke antwoorden gaven ze, welke MC-distractors kozen ze, zitten er patronen in (systematische naamvalsfout, synoniem-verwarring, macron-vergeten, ...).

**Geschat:** 4 stories (uitbreidbaar)
**Status:** draft — skeletten in `stories/backlog/`

**Context:** F1-12 heeft de datavoorraad neergelegd (`ItemResponse.answer_text`, `correct_answer`-snapshot, `item_type` per poging in `KnoopState.item_history`). Dit epic bouwt de ontsluiting daarop: rol-gebaseerde UI + aggregatie + optionele fout-classificatie.

**Afhankelijkheden:**
- **F1-12** (done) — `answer_text` + `item_history` wiring. Zonder deze story is er geen data om te tonen.
- **E7-08-ish** — user-rollen bestaan in het user-model (nu alleen "learner"). Een "mentor"/"docent"-rol met relatie tot leerlingen moet erbij.

| Story | Titel | Afhankelijk | Status |
|-------|-------|-------------|--------|
| F2-01 | Mentor-rol + leerling-koppeling in user-model | — | draft |
| F2-02 | Laatste foute antwoorden per leerling per knoop | F2-01, F1-12 | draft |
| F2-03 | Struikelpunten-overzicht per leerling | F2-01 | draft |
| F2-04 | Fout-classificatie (spelling / naamval / synoniem / macron) — track C kern | F1-12 | draft |

**Verhouding tot B8:**
`epic-b8-mentor-portfolio` richt zich op offline werk (portfolio-selectie, OCR-confidence). F2 is specifiek over **online** oefen-telemetrie en foutdiagnostiek — de twee zijn complementair en kunnen later dezelfde mentor-UI delen.

**Verhouding tot track C (fout-classificatie):**
De grading-module (`scheduling/grading.py`) en `GradingResult` zijn ontworpen zodat een fout-classificator (spelling vs naamval vs synoniem) als uitbreiding kan worden toegevoegd. F2-04 trekt die brug. Dit is de reguliere instap voor track C en breidt `scheduling/grading.py` uit zonder bestaande callers te raken.

**Niet-doel:**
- Portfolio-selectie offline werk → B8
- LLM-gestuurde vrije-vorm-feedback → aparte story
- Cijferrapportage / toetsdossier → out-of-scope

Blokkeert niet, maar activeert waarde die F1-12 sinds april 2026 al verzamelt.

---
---

## Roadmap — toekomstige epics

Uitwerking in stories volgt per epic wanneer deze opgepakt wordt.

---

## Epic E1: Pilot-ready — de eerste echte leerling

**Doel:** Het systeem klaar maken zodat een echte leerling (niet de ontwikkelaar) er dagelijks mee kan werken. Bugs vinden, UX valideren, eerste learner data verzamelen.
**Afhankelijkheden:** D compleet (MVP draait)
**Status:** todo

Scope:
- End-to-end walkthrough met een testleerling (niet de developer)
- Methode-mapping completeren: Fortuna volledig (alle hoofdstukken), SPQR uitbreiden
- Bugfixes uit eerste gebruikerstest
- UX-verbeteringen op basis van observatie (waar haakt de leerling af?)
- Monitoring: logging van sessie-data voor analyse
- Feedbackformulier integreren (simpel: Google Form of in-app)

| Story | Titel | Status |
|-------|-------|--------|
| E1-01 | Pilot-ready milestone — eerste echte leerling | doing |

---

## Epic E2: Echte TTS-audio

**Doel:** Placeholder audio vervangen door echte uitspraak. Klassiek Latijn en Erasmiaans Grieks.
**Afhankelijkheden:** B1 done (pipeline staat), E1 (prioriteit op basis van pilot-feedback)
**Status:** todo

Scope:
- espeak-ng configureren voor klassiek Latijn (of alternatief uit B1-01 evaluatie)
- Erasmiaans Grieks: handmatige opnames overwegen (samenwerking Addisco-docenten?)
- Audio genereren voor alle 450 V-knopen
- Kwaliteitscheck: steekproef door classicus
- audio_ref velden updaten van placeholder naar definitief

Bronnen en leads:
- **espeak-ng** — <https://github.com/espeak-ng/espeak-ng> — open-source formant-synth met ingebouwde Latijnse stem (`la`) en Oud-Grieks (`grc`). GPLv3. Command-line en libary. Macron-support voor lange klinkers via IPA of via [[lengte]]-markers werkt voor klassieke uitspraak; kwaliteit is robotisch maar goed genoeg voor woord-niveau drill.
- Overwegen ná B1-01 evaluatie: Piper (neural, hogere kwaliteit, geen Latijnse stem out-of-the-box), Coqui TTS (fine-tune vereist), Poeta ex Machina (klassiek-specifiek maar beperkte API).

---

## Epic E3: Items en content voor Grieks + vocabulaire

**Doel:** C1/C2 dekken alleen Latijnse grammatica. Grieks en vocabulaire hebben ook items en content nodig voor een volwaardige ervaring. Parallelstructuur met C1 (items) en C2 (content) voor Latijn.
**Geschat:** 19 stories, ~400 GRC-G-items, ~900 extra V-items, ~40 GRC-markdowns, ~60 SHA-C-markdowns
**Afhankelijkheden:** A2, A3 done (Griekse knopen bestaan); F1-01 + F1-03 wenselijk (rendering werkt); F1-08 voor cultuur (items-basis)
**Status:** done

### Items — GRC grammatica (analoog aan C1)

| Story | Titel | Geschat | Status |
|-------|-------|---------|--------|
| E3-01 | Items voor GRC alfabet — restknopen (INTRO, groepen, diakritiek, combinaties) | ~60 items | done |
| E3-02 | Items voor GRC-conceptknopen (naamval/genus/declinatie/tempus-INTRO's) | ~25 items | done |
| E3-03 | Items voor GRC 1e declinatie (α/η-stammen) | ~30 items | done |
| E3-04 | Items voor GRC 2e declinatie (ο-stammen m/n) | ~30 items | done |
| E3-05 | Items voor GRC 3e declinatie (πᾶς, σώφρων) | ~25 items | done |
| E3-06 | Items voor GRC adjectieven (α/ο-stam + medeklinkerstam) | ~25 items | done |
| E3-07 | Items voor GRC praesens actief (thematisch + contracta + εἰμί) | ~40 items | done |
| E3-08 | Items voor GRC imperfectum + augment | ~30 items | done |
| E3-09 | Items voor GRC aoristus (sigmatisch + thematisch) | ~30 items | done |
| E3-10 | Items voor GRC pronomina (persoonlijk, bezittelijk, aanwijzend) | ~30 items | done |
| E3-11 | Items voor GRC voorzetsels + basissyntaxis | ~30 items | done |
| E3-12 | Validatie — dekking, IRT-params, oefentype-mix (GRC) | — | done |

### Content — GRC grammatica (analoog aan C2)

| Story | Titel | Geschat | Status |
|-------|-------|---------|--------|
| E3-13 | Content voor GRC concept-INTRO knopen | ~10 bestanden | done |
| E3-14 | Content voor GRC declinatie-paradigma's | ~8 bestanden | done |
| E3-15 | Content voor GRC werkwoord-paradigma's | ~10 bestanden | done |
| E3-16 | Content voor GRC syntaxis | ~6 bestanden | done |
| E3-17 | Content voor GRC pronomina + adjectieven | ~6 bestanden | done |

### Cultuur en vocabulaire

E3-18 is opgesplitst in 5 thematische sub-stories voor parallel werk; samen 65 SHA-C-markdowns.

| Story | Titel | Geschat | Status |
|-------|-------|---------|--------|
| E3-18 | Content voor cultuurknopen (SHA-C) — umbrella | ~65 bestanden | done |
| E3-18a | SHA-C mythologie | 20 bestanden | done |
| E3-18b | SHA-C Romeins dagelijks leven | 15 bestanden | done |
| E3-18c | SHA-C Grieks dagelijks leven | 10 bestanden | done |
| E3-18d | SHA-C geschiedenis + staatsinrichting | 15 bestanden | done |
| E3-18e | SHA-C taal, schrift, literatuur | 5 bestanden | done |
| E3-19 | Vocabulaire — stamtijd-items voor werkwoorden (NL↔lemma was al gerealiseerd) | 94 items | done |

### Resultaat

- **GRC-G-items: 100 % dekking** (142/142 knopen, 389 items) — gemeten via `scripts/validate_items_e3_12.py`
- **GRC-G-content: 45 markdowns** voor concept-INTRO's, declinaties, werkwoorden, syntaxis, pronomina/adjectieven
- **SHA-C-content: 100 % dekking** (65/65 cultuurknopen)
- **V-items: 5 per werkwoord-knoop** (4 basis + 1 stamtijd voor 94 verbs); rest 4 per knoop

**Verhouding tot andere epics:**
- **F1-01 en F1-03** moeten draaien voordat GRC-items en -markdowns nut hebben op het scherm.
- **F1-08** levert minimum-oefenbaarheid voor cultuurknopen; E3-18 voegt didactische verdieping toe.
- **F1-11** dekkingsrapport geeft tussentijds voortgangsmeetpunt; E3-12 gebruikt ditzelfde script.
- **E2** (echte TTS) is nodig voor audio-items: GRC-stem van espeak-ng is de lead.

---

## Epic E4: Productie-deployment

**Doel:** Van localhost naar een publiek toegankelijke applicatie. Single-server deployment, geen over-engineering.
**Afhankelijkheden:** E1 done (pilot-bugs gefixt)
**Status:** todo

Scope:
- VPS provisioning (Hetzner EU, conform AVG)
- Docker Compose: backend + frontend + SQLite (of PostgreSQL migratie)
- HTTPS via Let's Encrypt
- CI/CD: GitHub Actions voor tests + deploy
- Backup-strategie voor learner data
- Domein + DNS
- OAuth / SURFconext voor schoolaccounts (of uitstellen naar E5)

---

## Epic E5: Pensum-module — jaarlijks wisselende auteurs

**Doel:** Het CE-pensum wisselt jaarlijks van auteur. Het systeem moet een jaarlijks te activeren module ondersteunen bovenop de vaste graph.
**Afhankelijkheden:** E1 done, externe validatie door domeinpartner
**Status:** todo

Scope:
- Pensum-datamodel: per examenjaar een set auteurspecifieke cultuurknopen + leesteksten
- Pensum 2026 LTC: Seneca/Cicero (filosofie) — cultuurknopen + integratieknopen
- Pensum 2026 GTC: Homerus (Odyssee) — cultuurknopen + leespassages
- Pensum-selectie bij onboarding (User.examenjaar_ltc/gtc)
- Scheduling engine: pensum-knopen activeren op basis van examenjaar
- Syllabus-overlay: welke cultuurknopen zijn toetsbaar per examenjaar

---

## Epic E6: Leerjaar 2+ content uitbreiden

**Doel:** De knowledge graph uitbreiden voorbij leerjaar 1 richting het volledige eindexamenprogramma.
**Afhankelijkheden:** E1 + E5 done, IRT-kalibratie op pilot-data
**Status:** todo

Scope:
- Latijnse grammatica leerjaar 2-3: passivum volledig, conjunctivus, participia, gerundium/gerundivum, AcI/NcI verdieping
- Griekse grammatica leerjaar 2-3: medium volledig, aoristus passief, conjunctivus, optativus, participia
- Latijnse grammatica bovenbouw: ablativus absolutus, indirecte rede, opeenvolging van tijden
- Griekse grammatica bovenbouw: mi-verba, onregelmatige aoristus, indirecte rede
- Vocabulaire uitbreiden: volledige CvTE-minimumlijst (~1500 LAT, ~1200 GRC)
- Cultuur bovenbouw: filosofie (Stoa, Epicurisme), receptie en doorwerking
- Metriek-subgraph: hexameter, elegisch distichon (cf. ontwerpkeuze 4)
- Geschatte omvang: 2000-3000 extra knopen

---

## Epic E7: Didactische routes — grammatica-eerst vs. context-eerst

**Doel:** De leerling kan kiezen tussen twee didactische routes: de traditionele grammatica-eerst aanpak (huidig) of een context-eerst aanpak (Addisco-stijl) waarbij lezen centraal staat en grammatica wordt aangeboden wanneer het nodig is voor begrip.

Beide routes leiden tot mastery op dezelfde knopen — het verschil is de volgorde en de presentatievorm. SM-2 en BKT werken per knoop en zijn route-onafhankelijk. Wisselen tussen routes verstoort de scheduling niet.

**Afhankelijkheden:** E1 (pilot-feedback), A1+A2 (grammaticaknopen bestaan)
**Status:** done

**Belangrijke ontwerpbeslissing:** de context-first route relaxt de prerequisite-gate. In grammar-first moet een leerling de 1e declinatie beheersen voordat voorzetsels aan bod komen. In context-first kan een passage met voorzetsels worden aangeboden terwijl de declinatie nog niet volledig beheerst is — de passage IS de introductie, met scaffolding.

| Story | Titel | Status |
|-------|-------|--------|
| E7-01 | Route-keuze model en User-uitbreiding | done |
| E7-02 | Leespassages als content-type | done |
| E7-03 | Eerste set leespassages — Latijn onderbouw (~20 passages) | done |
| E7-04 | Eerste set leespassages — Grieks onderbouw (~15 passages) | done |
| E7-05 | Context-first scheduling strategie | done |
| E7-06 | Sessie-orkestratie met passages | done |
| E7-07 | Frontend: passage-lezer component | done |
| E7-08 | Frontend: route-selectie en onboarding | done |
| E7-09 | Grammatica-scaffolding bij passages | done |
| E7-10 | Validatie: vergelijk leeruitkomsten beide routes | done |

---

## Epic OS: Ontwikkelstraat fase 1 — Python-baseline

**Doel:** Een werkende, laaggewijze ontwikkelstraat die code-kwaliteit, teststatus en storystatus automatisch bewaakt, zodat dit niet meer afhangt van oplettendheid per sessie. Zes lagen: projecttemplate (buiten scope), pre-commit, Claude Code hooks, CI, geautomatiseerde review, gedeelde standaarden.

**Scope:** Alleen Codebase-Olympus. Templatisering naar andere projecten (`my-templates/`) is een latere epic.

**Afhankelijkheden:** Geen. Bouwt voort op bestaande `pyproject.toml`, `ruff`-config en pytest-suite (165 tests).

**Status:** in uitvoering — OS-00/01/02/03/05/06 done; OS-04, OS-07, OS-08 in doing (wachten op externe verificatie); OS-09 in backlog (volgde uit graph-methodologie-reflectie)

**Epic-brede acceptatiecriteria:**
- [ ] Alle vijf actieve lagen van de ontwikkelstraat hebben ten minste één werkende check
- [ ] CI is groen op `main` na alle stories
- [ ] Een "break-test" (opzettelijk falende code) wordt geblokkeerd op minstens twee lagen
- [ ] Nieuwe story kan niet naar `done/` zonder dat AC afgevinkt zijn — geautomatiseerd
- [ ] Ontwikkelstraat-werkwijze gedocumenteerd in `CLAUDE.md`

| Story | Titel | Laag | Afhankelijk | Status |
|-------|-------|------|-------------|--------|
| OS-00 | Storyconventie herstellen (platte backlog/doing/done) | — | — | done |
| OS-01 | Lint- en formatbasis afmaken (ruff strict) | 1 | — | done |
| OS-02 | Type-checking toevoegen (mypy) | 1 | — | done |
| OS-03 | Pre-commit hooks | 2 | OS-01, OS-02 | done |
| OS-04 | CI baseline (GitHub Actions) | 4 | OS-01, OS-02 | doing |
| OS-05 | Claude Code hooks (PostToolUse + Stop) | 3 | OS-01 | done |
| OS-06 | Storystatus- en AC-verificatie (script + hooks + CI) | 2 + 4 | OS-03, OS-04 | done |
| OS-07 | Review-skills inbedden in workflow | 5 | — | doing |
| OS-08 | CLAUDE.md bijwerken met ontwikkelstraat-sectie | 6 | alle voorgaande | doing |
| OS-09 | validation.py generiek per edge-type maken | 5 | — | backlog |

**Volgorde-advies:** OS-01 en OS-02 parallel (beide linter-achtig). OS-03 en OS-04 daarna; OS-06 bouwt op beide. OS-05 (Claude-hooks) kan vroeg, zodra OS-01 klaar is, omdat het de inner loop versnelt. OS-07 en OS-08 als laatste: eerst moet er iets zijn om te documenteren.

**Niet-scope voor deze epic:**
- Uitrol naar andere repos (voxtral-transcribe, toekomstige apps)
- Template-repo `my-templates/` opzetten
- `mypy --strict` op de hele bestaande codebase (baseline-aanpak volstaat)
- Coverage-thresholds optrekken (wel rapporteren, niet blokkeren)
