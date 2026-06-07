# Epics overzicht

## Statustabel

> Canoniek register (codebase-standards). Bron van waarheid = de story-bestanden in
> `stories/{backlog,doing,done}/` (front-matter `status:`). Tellingen worden
> geregenereerd met `scripts/regenerate_status.py` en gevalideerd in CI.
> Toekomstige epics zonder stories (E31/E32/E33/E34) staan onder hun sectie en
> verschijnen hier zodra ze stories krijgen.

| Epic | Naam | Status | Stories (done/total) |
|---|---|---|---|
| E1 | Grammatica Latijn | done | 15/15 |
| E2 | Grammatica Grieks | done | 11/11 |
| E3 | Grieks alfabet — onboarding-subgraph | done | 3/3 |
| E4 | Vocabulaire | done | 8/8 |
| E5 | Cultuur | done | 6/6 |
| E6 | Transfer-edges | done | 5/5 |
| E7 | TTS-pipeline en audio-generatie | done | 5/5 |
| E8 | Audio-oefentypen | done | 4/4 |
| E9 | STT-integratie | done | 4/4 |
| E10 | Pronunciation assessment (stretch goal) | backlog | 0/3 |
| E11 | Offline oefentypen en scheduling | done | 6/6 |
| E12 | OCR-pipeline | backlog | 0/5 |
| E13 | LLM-vertaalbeoordeling | backlog | 0/3 |
| E14 | Mentor-portfolio | backlog | 0/4 |
| E15 | Items genereren — Latijnse grammatica | done | 11/11 |
| E16 | Content schrijven — Latijnse grammatica | done | 5/5 |
| E17 | FastAPI backend | done | 8/8 |
| E18 | React frontend | done | 7/7 |
| E19 | Integratie en pilot-ready | done | 3/3 |
| E20 | Content-ontsluiting en kwaliteitsverbetering | actief | 14/15 |
| E21 | Mentor-dashboard | done | 4/4 |
| E22 | WKM-spiegeling — vertaalstrategie, misconcepties, bijspijkerroute | done | 4/4 |
| E23 | Meet- en experimenteer-infrastructuur | done | 3/3 |
| E24 | Learner model — receptief/productief, migreerbaar, individueel | done | 3/3 |
| E25 | Didactiek — worked examples, motivatie, equity | done | 3/3 |
| E26 | Pilot-ready — de eerste echte leerling | actief | 0/1 |
| E27 | Items en content voor Grieks + vocabulaire | done | 24/24 |
| E28 | Didactische routes — grammatica-eerst vs. context-eerst | done | 10/10 |
| E29 | Ontwikkelstraat fase 1 — Python-baseline | actief | 11/12 |
| E30 | Vernederlandste code-identifiers naar Engels | done | 6/6 |

**Totaal:** 30 epics, 201 stories (183 done, 1 doing, 0 todo, 17 backlog).

## Spoor A — Knowledge graph content

Leerjaar 1 gymnasium, beide talen. Doelomvang: ~850 knopen, ~1500-2000 edges.

## Uitvoervolgorde

1. **E3** (alfabet) — klein, zelfstandig, blokkeert niets
2. **E1** (grammatica Latijn) — bouwt voort op de 50 PoC-knopen
3. **E2** (grammatica Grieks) — structureel parallel aan E1
4. **E4** (vocabulaire) — heeft E1+E2+E3 nodig voor prerequisite-edges
5. **E5** (cultuur) — onafhankelijk van E1-E4 maar edges lopen ernaar
6. **E6** (transfer-edges) — heeft E1+E2+E3+E4+E5 nodig

---

## Epic E1: Grammatica Latijn

**Doel:** Methode-onafhankelijke grammaticale kern van klas 1, gebaseerd op de CvTE-minimumlijst gefilterd op wat alle methoden gemeen hebben.
**Geschat:** ~150 knopen
**Afhankelijkheden:** Geen (bouwt voort op bestaande PoC)
**Status:** done
**Bestand:** `data/graph/lat_grammatica_leerjaar1.json`

| Story | Titel | Knopen | Status |
|-------|-------|--------|--------|
| OL_E1_S1 | Conceptknopen en naamvalsysteem | 6 | done |
| OL_E1_S2 | 1e declinatie — alle naamvallen + paradigma | 4 | done |
| OL_E1_S3 | 2e declinatie — o-stammen masculinum + neutrum | 5 | done |
| OL_E1_S4 | 3e declinatie — consonantstammen + i-stammen basis | 10 | done |
| OL_E1_S5 | Adjectieven bonus-type en fortis-type | 7 | done |
| OL_E1_S6 | Werkwoord-concepten — conjugatie-intro, persoon, tempus, modus | 6 | done |
| OL_E1_S7 | Praesens indicativus actief — 4 conjugaties + esse | 5 | done |
| OL_E1_S8 | Imperfectum indicativus actief | 4 | done |
| OL_E1_S9 | Perfectum indicativus actief — inclusief stamtijdentypen | 12 | done |
| OL_E1_S10 | Plusquamperfectum indicativus actief | 5 | done |
| OL_E1_S11 | Imperativus + infinitivus praesens actief | 5 | done |
| OL_E1_S12 | Pronomina — persoonlijk, bezittelijk, aanwijzend begin | 11 | done |
| OL_E1_S13 | Voorzetsels met accusativus en ablativus | 6 | done |
| OL_E1_S14 | Basissyntaxis — woordvolgorde, congruentie, ontkenning, vraagzinnen | 7 | done |
| OL_E1_S15 | Review en prerequisite-edge validatie voor heel epic E1 | — | done |

---

## Epic E2: Grammatica Grieks

**Doel:** Griekse grammaticale kern van klas 1, gebaseerd op de GTC-minimumlijst gefilterd op klas 1 scope (Pallas les 1-14 / ARGO thema 1-4).
**Geschat:** ~100 knopen
**Afhankelijkheden:** E3 (alfabet moet af als prerequisite)
**Status:** done
**Bestand:** `data/graph/grc_grammatica_leerjaar1.json`

| Story | Titel | Knopen | Status |
|-------|-------|--------|--------|
| OL_E2_S1 | Conceptknopen Grieks — lidwoord, naamvalsysteem | 11 | done |
| OL_E2_S2 | 1e declinatie (α/η-stammen) | 10 | done |
| OL_E2_S3 | 2e declinatie (ο-stammen) | 10 | done |
| OL_E2_S4 | 3e declinatie introductie — via adjectieven πᾶς, σώφρων | 8 | done |
| OL_E2_S5 | Adjectieven α/ο-stam en medeklinkerstam | 8 | done |
| OL_E2_S6 | Praesens indicativus actief — thematisch + contracta + εἰμί | 12 | done |
| OL_E2_S7 | Imperfectum indicativus actief — augment | 8 | done |
| OL_E2_S8 | Aoristus introductie — sigmatisch + thematisch | 10 | done |
| OL_E2_S9 | Pronomina — persoonlijk, bezittelijk, aanwijzend | 10 | done |
| OL_E2_S10 | Voorzetsels + basissyntaxis | 8 | done |
| OL_E2_S11 | Review en prerequisite-edge validatie voor heel epic E2 | — | done |

---

## Epic E3: Grieks alfabet — onboarding-subgraph

**Doel:** Grieks alfabet als onboarding-subgraph. Prerequisite voor alle GRC-grammaticaknopen.
**Geschat:** ~40 knopen
**Afhankelijkheden:** Geen
**Status:** done
**Bestand:** `data/graph/grc_alfabet.json`

| Story | Titel | Knopen | Status |
|-------|-------|--------|--------|
| OL_E3_S1 | Letters herkenning — 24 letters, majuskel + minuskel | 29 | done |
| OL_E3_S2 | Diakritische tekens — spiritus, accenten, iota subscriptum | 10 | done |
| OL_E3_S3 | Lettercombinaties en uitspraak — diphthongen, γγ=ng, speciale combinaties | 8 | done |

---

## Epic E4: Vocabulaire

**Doel:** Individuele woorden, frequentiegestuurd, met semantisch cluster.
**Geschat:** ~450 knopen
**Afhankelijkheden:** E1, E2, E3 (voor prerequisite-edges naar grammaticaknopen)
**Status:** done
**Bestanden:** `data/graph/lat_vocabulaire_leerjaar1.json`, `data/graph/grc_vocabulaire_leerjaar1.json`

| Story | Titel | Knopen | Status |
|-------|-------|--------|--------|
| OL_E4_S1 | Strategie en bronnen — DCC Latin/Greek Core, cluster-definitie | — | done |
| OL_E4_S2 | Latijn frequentieband F01 — top-100 woorden | 100 | done |
| OL_E4_S3 | Latijn frequentieband F02 — woorden 101-200 | 100 | done |
| OL_E4_S4 | Latijn frequentieband F03 — woorden 201-300 | 100 | done |
| OL_E4_S5 | Grieks frequentieband F01 — top-75 woorden | 75 | done |
| OL_E4_S6 | Grieks frequentieband F02 — woorden 76-150 | 75 | done |
| OL_E4_S7 | Prerequisite-edges vocabulaire → grammatica | 21 edges | done |
| OL_E4_S8 | Enrichment-edges voor onverbuigbare vocabulaire (bijwoorden, voegwoorden, partikels) | 46 edges | done |

---

## Epic E5: Cultuur

**Doel:** Gedeelde (SHA-C-*) cultuurknopen voor leerjaar 1.
**Geschat:** ~70 knopen
**Afhankelijkheden:** Geen (maar enrichment-edges naar E1/E2/E4)
**Status:** done
**Bestand:** `data/graph/sha_cultuur_leerjaar1.json`

| Story | Titel | Knopen | Status |
|-------|-------|--------|--------|
| OL_E5_S1 | Mythologie — Olympische goden, helden, Troje, Odysseus | 20 | done |
| OL_E5_S2 | Romeins dagelijks leven — familia, domus, school, eten, slavernij | 15 | done |
| OL_E5_S3 | Geschiedenis basis — Romulus, Republiek, legioenen, forum | 15 | done |
| OL_E5_S4 | Grieks dagelijks leven — polis, agora, gymnasium, symposium | 10 | done |
| OL_E5_S5 | Taal en schrift — Latijns alfabet, Grieks alfabet, inscripties | 5 | done |
| OL_E5_S6 | Prerequisite-edges cultuur → taal/integratie | 11 edges | done |

---

## Epic E6: Transfer-edges

**Doel:** Cross-linguïstische verbindingen (type `transfer`) tussen Latijn en Grieks.
**Geschat:** ~100 edges
**Afhankelijkheden:** E1, E2, E3, E4, E5 (alle knopen moeten bestaan)
**Status:** done
**Bestand:** `data/graph/transfer_edges_leerjaar1.json`

| Story | Titel | Edges | Status |
|-------|-------|-------|--------|
| OL_E6_S1 | Naamvalsysteem — LAT ↔ GRC naamvallen | 30 | done |
| OL_E6_S2 | Werkwoordsmorfologie — praesens/imperfectum/aoristus parallellen | 30 | done |
| OL_E6_S3 | Cultuur — gedeelde mythologie en geschiedenis | 20 | done |
| OL_E6_S4 | Vocabulaire — cognaten en leenwoorden | 20 | done |
| OL_E6_S5 | Validatie transfer-edges — geen cycli, weights correct | — | done |

---

## Spoor B-audio — TTS en STT voor Latijn en Grieks

Audio-laag voor multi-modale taalverwerving. Gefaseerd: TTS in fase 3, STT in fase 5.

### Uitvoervolgorde

1. **E7** (TTS-pipeline) — evaluatie tools + audio genereren voor ~450 V-knopen
2. **E8** (audio-oefentypen) — nieuwe ItemTypes + frontend player
3. **E9** (STT-integratie) — spraakherkenning + mondelinge oefentypen
4. **E10** (pronunciation assessment) — foneem-scoring + feedback (stretch goal)

---

## Epic E7: TTS-pipeline en audio-generatie

**Doel:** Evalueer en bouw een TTS-pipeline voor klassiek Latijn (klassieke uitspraak) en Grieks (Erasmiaans). Genereer audio voor alle V-knopen.
**Geschat:** ~450 audiobestanden
**Afhankelijkheden:** E4 (vocabulaireknopen moeten bestaan)
**Status:** done (placeholder WAV; echte audio vereist espeak-ng of handmatige opnames)

| Story | Titel | Geschat | Status |
|-------|-------|---------|--------|
| OL_E7_S1 | TTS-evaluatie Latijn — Poeta ex Machina en alternatieven | — | done |
| OL_E7_S2 | TTS-evaluatie Grieks — Erasmiaans en alternatieven | — | done |
| OL_E7_S3 | TTS-pipeline bouwen — audio-generatiescript | — | done |
| OL_E7_S4 | Audio genereren — Latijn V-knopen F01-F03 | ~300 bestanden | done |
| OL_E7_S5 | Audio genereren — Grieks V-knopen F01-F02 | ~150 bestanden | done |

---

## Epic E8: Audio-oefentypen

**Doel:** Nieuwe oefentypen die audio gebruiken: luister-en-herken, luister-en-schrijf. Frontend audioplayer.
**Geschat:** ~400 items + frontend component
**Afhankelijkheden:** E7 (audio moet bestaan)
**Status:** done

| Story | Titel | Geschat | Status |
|-------|-------|---------|--------|
| OL_E8_S1 | ItemType uitbreiden — luister-oefentypen | — | done |
| OL_E8_S2 | Audio player component — frontend | — | done |
| OL_E8_S3 | Luister-en-herken oefeningen genereren | 450 items | done |
| OL_E8_S4 | Luister-en-schrijf oefeningen genereren | 450 items | done |

---

## Epic E9: STT-integratie

**Doel:** Spraakherkenning voor mondelinge oefeningen en examensimulatie. AVG-conforme verwerking.
**Geschat:** STT-pipeline + mondelinge oefentypen
**Afhankelijkheden:** E7 (referentie-audio), fase 5
**Status:** done (stub-implementatie; echte STT niet haalbaar voor klassieke talen in huidige fase)

| Story | Titel | Geschat | Status |
|-------|-------|---------|--------|
| OL_E9_S1 | STT-evaluatie — Whisper vs. Voxtral | — | done |
| OL_E9_S2 | STT-pipeline bouwen — transcriptie-module | — | done |
| OL_E9_S3 | Mondelinge oefentypen — spreek-na en beantwoord mondeling | — | done |
| OL_E9_S4 | Privacy-implementatie — spraakdata AVG-conform | — | done |

---

## Epic E10: Pronunciation assessment (stretch goal)

**Doel:** Foneem-niveau uitspraakbeoordeling met MFA. Per-foneem feedback.
**Geschat:** Scoring model + feedback-integratie
**Afhankelijkheden:** E9 (STT moet werken)
**Status:** geparkeerd (STT voor klassieke talen onvoldoende betrouwbaar)

| Story | Titel | Geschat | Status |
|-------|-------|---------|--------|
| OL_E10_S1 | Montreal Forced Aligner evaluatie en integratie | — | todo |
| OL_E10_S2 | Pronunciation scoring model | — | todo |
| OL_E10_S3 | Pronunciation feedback integratie in oefentypen | — | todo |

---

## Spoor B-offline — Schrijfoefeningen, OCR en mentor-portfolio

Offline schrijven als volwaardige oefenvorm met OCR-verificatie en mentor-portfolio.

### Uitvoervolgorde

1. **E11** (offline oefentypen) — datamodel, self-report, PDF-werkbladen, scheduling
2. **E12** (OCR-pipeline) — camera-capture, Grieks alfabet, paradigma's, vertalingen
3. **E13** (LLM-vertaalbeoordeling) — OCR + LLM-feedback op vertalingen
4. **E14** (mentor-portfolio) — selectie, PDF-generatie, Addisco-integratie

---

## Epic E11: Offline oefentypen en scheduling

**Doel:** Offline schrijfoefeningen als gepland onderdeel van de learning loop. Self-report flow, printbare werkbladen, scheduling aan einde sessie.
**Geschat:** ~100 items + scheduling-logica + PDF-generatie
**Afhankelijkheden:** E1, E2, E3 (grammaticaknopen moeten bestaan)
**Status:** todo

| Story | Titel | Geschat | Status |
|-------|-------|---------|--------|
| OL_E11_S1 | Offline oefentype en scheduling-integratie | — | done |
| OL_E11_S2 | Self-report flow en BKT-integratie met verlaagde confidence | — | done |
| OL_E11_S3 | Printbare PDF-werkbladen genereren | — | done |
| OL_E11_S4 | Paradigma-schrijfoefeningen genereren | ~50 items | done |
| OL_E11_S5 | Vertaal-op-papier oefeningen genereren | ~30 items | done |
| OL_E11_S6 | Grieks alfabet schrijfoefeningen | ~24 items | done |

---

## Epic E12: OCR-pipeline

**Doel:** OCR-verificatie voor offline schrijfwerk waar dat beslissend is voor progressie: Grieks alfabet (blokkerend), paradigmatabellen (progressie-kritisch), vertalingen (feedback-kritisch).
**Geschat:** OCR-pipeline + BKT-integratie
**Afhankelijkheden:** E11 (offline items moeten bestaan), fase 5
**Status:** todo

| Story | Titel | Geschat | Status |
|-------|-------|---------|--------|
| OL_E12_S1 | Camera-capture component — frontend | — | todo |
| OL_E12_S2 | OCR Grieks alfabet — letterherkenning | — | todo |
| OL_E12_S3 | OCR paradigmatabellen — gestructureerde herkenning | — | todo |
| OL_E12_S4 | OCR Nederlandse vertalingen — handschriftherkenning | — | todo |
| OL_E12_S5 | BKT-integratie OCR — confidence-mapping | — | todo |

---

## Epic E13: LLM-vertaalbeoordeling

**Doel:** Na OCR-transcriptie van een vertaling: LLM vergelijkt met modelantwoord en genereert inhoudelijke feedback per foutcategorie.
**Geschat:** LLM-pipeline + foutcategorisatie
**Afhankelijkheden:** E12 (OCR moet werken), Claude API
**Status:** todo

| Story | Titel | Geschat | Status |
|-------|-------|---------|--------|
| OL_E13_S1 | LLM-vergelijking met modelantwoord | — | todo |
| OL_E13_S2 | Foutcategorisatie en feedback-generatie | — | todo |
| OL_E13_S3 | Integratie met BKT en conditional completion | — | todo |

---

## Epic E14: Mentor-portfolio

**Doel:** Maandelijks portfolio met selectie van meest informatieve offline werk. PDF-export, optionele Addisco-integratie.
**Geschat:** Selectie-algoritme + PDF-generatie
**Afhankelijkheden:** E11, E12 (offline werk en OCR-resultaten)
**Status:** todo

| Story | Titel | Geschat | Status |
|-------|-------|---------|--------|
| OL_E14_S1 | Portfolio-selectie-algoritme | — | todo |
| OL_E14_S2 | Portfolio PDF-generatie | — | todo |
| OL_E14_S3 | Mentor-dashboard en Addisco-integratie | — | todo |
| OL_E14_S4 | Leerling-opt-in voor mentor-deling (consent + intrekken) | — | backlog |

---

## Spoor C — Items en content voor Latijnse grammatica

Items (oefeningen) en didactische content voor de LAT-G knopen, richting pilot.
Zie `docs/Prompt_spoor_c.md` voor de volledige prompt.

### Uitvoervolgorde

- **E15** en **E16** zijn onderling onafhankelijk en kunnen parallel
- E15-stories hangen af van de corresponderende E1-story (knopen moeten bestaan)
- E16-stories hangen af van dezelfde E1-knopen maar niet van E15

---

## Epic E15: Items genereren — Latijnse grammatica

**Doel:** Oefeningen genereren voor alle LAT-G knopen. Mix van herkenning, productie, analyse, contextueel.
**Geschat:** ~330 items
**Afhankelijkheden:** E1 (per story: corresponderende E1-story moet done zijn)
**Status:** done

| Story | Titel | Geschat | Status |
|-------|-------|---------|--------|
| OL_E15_S1 | Items voor conceptknopen (INTRO) | 24 items | done |
| OL_E15_S2 | Items voor 1e declinatie | 30 items | done |
| OL_E15_S3 | Items voor 2e declinatie | 39 items | done |
| OL_E15_S4 | Items voor 3e declinatie | 37 items | done |
| OL_E15_S5 | Items voor adjectieven | 25 items | done |
| OL_E15_S6 | Items voor presens indicativus | 38 items | done |
| OL_E15_S7 | Items voor imperfectum + perfectum | 39 items | done |
| OL_E15_S8 | Items voor plqpf + imperativus + infinitivus | 22 items | done |
| OL_E15_S9 | Items voor pronomina | 24 items | done |
| OL_E15_S10 | Items voor voorzetsels + syntaxis | 32 items | done |
| OL_E15_S11 | Validatie: dekking, IRT-parameters, oefentype-mix | — | done |

---

## Epic E16: Content schrijven — Latijnse grammatica

**Doel:** Didactische markdown content voor de kernknopen: paradigmatabellen, uitleg, herkenningstips.
**Geschat:** ~34 bestanden
**Afhankelijkheden:** E1 (knopen moeten bestaan)
**Status:** done

| Story | Titel | Geschat | Status |
|-------|-------|---------|--------|
| OL_E16_S1 | Content voor concept-INTRO knopen | 8 bestanden | done |
| OL_E16_S2 | Content voor declinatie-paradigma's | 6 bestanden | done |
| OL_E16_S3 | Content voor werkwoord-paradigma's | 8 bestanden | done |
| OL_E16_S4 | Content voor syntaxis | 6 bestanden | done |
| OL_E16_S5 | Content voor pronomina + adjectieven | 6 bestanden | done |

---

## Spoor D — Werkende MVP-applicatie (FastAPI + React)

De engine naar een webapplicatie brengen. Zie `docs/Prompt_spoor_d.md` voor de volledige prompt.

### Uitvoervolgorde

1. **E17** (backend) en **OL_E18_S1+02** (frontend setup + login) kunnen parallel
2. **OL_E18_S3+** heeft OL_E17_S5 nodig (session endpoints)
3. **E19** na E17+E18 compleet

---

## Epic E17: FastAPI backend

**Doel:** REST API die de sessie-engine wraps. SQLite persistence. Auth.
**Geschat:** 8 stories
**Afhankelijkheden:** Geen (bouwt op bestaande engine)
**Status:** done

| Story | Titel | Status |
|-------|-------|--------|
| OL_E17_S1 | Project setup: FastAPI + uvicorn + SQLite | done |
| OL_E17_S2 | Auth endpoints: register + login | done |
| OL_E17_S3 | Database CRUD: users + learner_models | done |
| OL_E17_S4 | SessionManager: stapsgewijs sessie-protocol | done |
| OL_E17_S5 | Session endpoints: start + answer | done |
| OL_E17_S6 | Session endpoint: summary | done |
| OL_E17_S7 | Progress endpoints | done |
| OL_E17_S8 | Intake endpoints | done |

---

## Epic E18: React frontend

**Doel:** Minimale maar functionele UI: login, sessie-interface, dashboard.
**Geschat:** 7 stories
**Afhankelijkheden:** OL_E17_S2 (auth), OL_E17_S5 (session), OL_E17_S7 (progress)
**Status:** todo

| Story | Titel | Status |
|-------|-------|--------|
| OL_E18_S1 | Project setup: Vite + React + routing | done |
| OL_E18_S2 | Login pagina | done |
| OL_E18_S3 | Session pagina: vraag tonen | done |
| OL_E18_S4 | Session pagina: antwoord + feedback | done |
| OL_E18_S5 | Session pagina: samenvatting | done |
| OL_E18_S6 | Dashboard pagina | done |
| OL_E18_S7 | Polytonic Greek input | done |

---

## Epic E19: Integratie en pilot-ready

**Doel:** Alles draait samen. Dev server, seed data, end-to-end test.
**Geschat:** 3 stories
**Afhankelijkheden:** E17 + E18 compleet
**Status:** done

| Story | Titel | Status |
|-------|-------|--------|
| OL_E19_S1 | Dev server script + CORS + proxy | done |
| OL_E19_S2 | Seed script: test-user met intake | done |
| OL_E19_S3 | End-to-end smoke test + pilot guide | done |

---

## Spoor F — Content-ontsluiting en kwaliteitsverbetering

Bestaand materiaal (markdowns, audio, MC-opties, vocab-metadata) daadwerkelijk naar de leerling krijgen, en dekkingsgaten dichten waar dat leerrendement oplevert. Focus op wat al in `data/` staat maar niet bereikt wordt.

### Uitvoervolgorde

1. **OL_E20_S11** eerst — dekkingsrapport geeft baseline
2. **OL_E20_S1** en **OL_E20_S3** — frontend-pipeline werkend (scaffolding + structured stimulus); blokkerend voor rest
3. **OL_E20_S4** — audio pipeline
4. **OL_E20_S2**, **OL_E20_S5**, **OL_E20_S6** — parallel, bouwen voort op 01/03
5. **OL_E20_S7**, **OL_E20_S8** — content-uitbreiding, na pipeline
6. **OL_E20_S9**, **OL_E20_S10** — opschoning, kan altijd

---

## Epic E20: Content-ontsluiting en kwaliteitsverbetering

**Doel:** Het gat dichten tussen aanwezig materiaal en wat de leerling daadwerkelijk ziet. Frontend-pipeline voor `scaffolding_content`, structured stimulus (MC-opties, hints) en audio-playback; vocab-metadata ontsluiten; content-dekking van LAT-G opschalen; cultuurknopen oefenbaar maken; dode data opruimen; permanente monitoring via dekkingsrapport.
**Geschat:** 11 stories
**Afhankelijkheden:** E17 + E18 compleet (engine en frontend draaien)
**Status:** todo

| Story | Titel | Status |
|-------|-------|--------|
| OL_E20_S1 | Frontend ScaffoldingPanel — render `scaffolding_content` als markdown | done |
| OL_E20_S2 | Scaffolding ook in grammar-first (opt-in) bij eerste introductie | done |
| OL_E20_S3 | Frontend rendert structured stimulus (instruction / hint / options) | done |
| OL_E20_S4 | AudioPlayer component + afspelen van `audio_ref` in luister-items | done |
| OL_E20_S5 | Woordkaart — toon structured vocab-metadata uit vocab_sources | done |
| OL_E20_S6 | `content_ref` expliciet zetten in alle graph-JSONs + validator | done |
| OL_E20_S7 | LAT-G content-dekking verhogen naar hot-path ≥ 80 % | done |
| OL_E20_S8 | Cultuurknopen oefenbaar maken (items + korte markdown) | done |
| OL_E20_S9 | Ontsluit of verwijder `vocabulaire_clusters.json` | done |
| OL_E20_S10 | Opschonen passages — merge `lat_passages_leerjaar1.json` | done |
| OL_E20_S11 | Content-dekkingsrapport — script + CI-check | done |
| OL_E20_S12 | Telemetrie-uitbreiding — `answer_text` + `item_history` wiring | done |
| OL_E20_S13 | Mentor-view pagina (capstone Sprint 5) | done |
| OL_E20_S14 | Diverse content-opschoning ronde 2 | done |
| OL_E20_S15 | Mouseover-tooltips voor vaktermen in content (afgesplitst van OL_E20_S13) | backlog |

**Verhouding tot andere epics:**
- E20 overlapt niet met **A-spoor** (graph-structuur) — die is af.
- OL_E20_S4 vult de frontend-kant aan die E8 voorondersteld had; echte audio komt later via **E31**.
- OL_E20_S7/OL_E20_S8 raken aan **E16** (LAT-G-content) en **E27** (GRC-G + SHA-C items/content). E20 levert eerst de pipeline en basis-oefenbaarheid; E27 kan verdiepend Grieks-materiaal toevoegen.
- E20 is pilot-kritisch: zonder OL_E20_S1, OL_E20_S3 en OL_E20_S4 blijft veel van het gegenereerde materiaal onzichtbaar voor de leerling en is een **E26**-pilot minder waardevol.

---

## Epic E21: Mentor-dashboard

**Doel:** Mentoren en docenten in staat stellen om leerlingen op concreet niveau te helpen. Niet alleen *dat* een leerling struikelt op een knoop, maar *hoe*: welke letterlijke antwoorden gaven ze, welke MC-distractors kozen ze, zitten er patronen in (systematische naamvalsfout, synoniem-verwarring, macron-vergeten, ...).

**Geschat:** 4 stories (uitbreidbaar)
**Status:** draft — skeletten in `stories/backlog/`

**Context:** OL_E20_S12 heeft de datavoorraad neergelegd (`ItemResponse.answer_text`, `correct_answer`-snapshot, `item_type` per poging in `KnoopState.item_history`). Dit epic bouwt de ontsluiting daarop: rol-gebaseerde UI + aggregatie + optionele fout-classificatie.

**Afhankelijkheden:**
- **OL_E20_S12** (done) — `answer_text` + `item_history` wiring. Zonder deze story is er geen data om te tonen.
- **OL_E28_S8-ish** — user-rollen bestaan in het user-model (nu alleen "learner"). Een "mentor"/"docent"-rol met relatie tot leerlingen moet erbij.

| Story | Titel | Afhankelijk | Status |
|-------|-------|-------------|--------|
| OL_E21_S1 | Mentor-rol + leerling-koppeling in user-model | — | done |
| OL_E21_S2 | Laatste foute antwoorden per leerling per knoop | OL_E21_S1, OL_E20_S12 | done |
| OL_E21_S3 | Struikelpunten-overzicht per leerling | OL_E21_S1 | done |
| OL_E21_S4 | Fout-classificatie (spelling / naamval / synoniem / macron) — track C kern | OL_E20_S12 | done |

**Verhouding tot E14:**
`epic-b8-mentor-portfolio` richt zich op offline werk (portfolio-selectie, OCR-confidence). E21 is specifiek over **online** oefen-telemetrie en foutdiagnostiek — de twee zijn complementair en kunnen later dezelfde mentor-UI delen.

**Verhouding tot track C (fout-classificatie):**
De grading-module (`scheduling/grading.py`) en `GradingResult` zijn ontworpen zodat een fout-classificator (spelling vs naamval vs synoniem) als uitbreiding kan worden toegevoegd. OL_E21_S4 trekt die brug. Dit is de reguliere instap voor track C en breidt `scheduling/grading.py` uit zonder bestaande callers te raken.

**Niet-doel:**
- Portfolio-selectie offline werk → E14
- LLM-gestuurde vrije-vorm-feedback → aparte story
- Cijferrapportage / toetsdossier → out-of-scope

Blokkeert niet, maar activeert waarde die OL_E20_S12 sinds april 2026 al verzamelt.

---

## Spoor M — Methodologie en doelgroep-uitbreiding

Spiegeling van Olympus' aanpak aan externe didactische praktijk
(Wijkunnenmeer / Reijgwart). Drie sporen: vertaalstrategie als
first-class object in de graph, misconceptie-diagnostiek, en een
tweede gebruikersmodus voor de gymnasiast die op school al vastloopt.

Bron: `docs/externe-bronnen/wkm-problemen-latijn-grieks.md`.

### Uitvoervolgorde

1. **OL_E22_S1** (Knoop-type P + POLMO) — modelaanpassing, blokkeert OL_E22_S2
2. **OL_E22_S2** (Misconcepties + Lego-vertaler-detectie) — bouwt op OL_E22_S1
3. **OL_E22_S3** (Bijspijkerroute) — onafhankelijk maar profiteert van OL_E22_S1/02

---

## Epic E22: WKM-spiegeling — vertaalstrategie, misconcepties, bijspijkerroute

**Doel:** Drie inzichten uit Wijkunnenmeer's praktijk inbouwen in
Olympus: (1) de vertaalstrategie POLMO als procedurele DAG naast de
declaratieve grammatica; (2) misconcepties als first-class object met
een eerste detector voor "Lego-vertalen"; (3) een tweede
gebruikersmodus die de grotere doelgroep — gymnasiasten die op school
dreigen te zakken — als primaire doelgroep ondersteunt.

**Geschat:** 3 stories (uitbreidbaar — vervolgstories voor extra
procedures, extra misconcepties en extra schoolmethodes liggen voor
de hand)

**Afhankelijkheden:**
- E1, E2, E3 done (graph bestaat)
- OL_E20_S12 done (telemetrie-basis voor OL_E22_S2)
- E26 in uitvoering (methode-mapping voor OL_E22_S3)

**Status:** in uitvoering — OL_E22_S1 opgepakt (Sprint 6, juni 2026).

| Story | Titel | Afhankelijk | Status |
|-------|-------|-------------|--------|
| OL_E22_S1 | Knoop-type P (Procedure) + POLMO-stappen-DAG | — | done |
| OL_E22_S2 | Misconceptie-attribuut + Lego-vertaler-detectie | OL_E22_S1, OL_E22_S4 | done |
| OL_E22_S3 | Bijspijkerroute — methode-en-hoofdstuk-gestuurde catch-up | E26 | done |
| OL_E22_S4 | Vertaal-integratielaag — eerste I-VERT-knopen (enabler OL_E22_S2) | OL_E22_S1 | done |

**Verhouding tot andere epics:**
- **E26** is begonnen aan methode-mapping (Fortuna, SPQR); OL_E22_S3
  formaliseert dat tot een tweede planner-modus
- **E28** (didactische routes) is route-loodrecht op E22: bijspijker- en
  staatsexamen-modus werken beide op grammar-first én context-first
- **E21** (mentor-dashboard) wordt waardevoller wanneer OL_E22_S2 actief
  is — een misconceptie-flag is precies het soort signaal dat een
  mentor wil zien
- **E15/E16/E27** (items en content) — POLMO-stappen krijgen later eigen
  items en content via vervolgstories

**Niet-scope voor E22:**
- Volledige Bug Library (meerdere misconcepties) — alleen Lego-vertalen
- Studievaardigheden als parallelle skill-tree (executieve functies,
  encoding-strategieën) — eigen toekomstige epic
- Ouder/mentor-dashboard met misconceptie-overzicht — E21-uitbreiding
- LLM-feedback bij misconceptie — buiten scope, regelgebaseerde
  detectie volstaat

---
---

## Spoor L — Evidence-based leerontwerp

Vertaling van `docs/LITERATUURONDERZOEK_LEERBENADERING.md` naar de
aanpak: meetbaarheid, een beter learner model, en didactische
patronen die de literatuur ondersteunt. Onderbouwing in
`docs/ONTWERPKEUZES_GYMNASIUM_CLASSICA.md`, keuzes 12–16, plus de
evidence-based uitgangspunten (prioritering méér/minder/geen).

### Uitvoervolgorde

1. **E23** (meetlaag) — fundament: zonder meten geen toetsbare claim
2. **E24** (learner model) — bouwt deels op E23 voor evaluatie
3. **E25** (didactiek/UX) — gebruikt E23-metriek voor triggers en equity

---

## Epic E23: Meet- en experimenteer-infrastructuur

**Doel:** De centrale claim ("efficiënter leren per minuut") toetsbaar
maken en het gat in de literatuur (geen evidence voor klassieke talen)
zelf vullen. Retentie-/tijd-/masterymetriek, een baseline, en een licht
A/B-framework.
**Geschat:** 3 stories
**Afhankelijkheden:** Bestaand learner-model + telemetrie (OL_E20_S12 done)
**Status:** done — alle drie de tiers afgerond (juni 2026).

| Story | Titel | Afhankelijk | Status |
|-------|-------|-------------|--------|
| OL_E23_S1 | Retentie- en sessiemetriek-logging | — | done |
| OL_E23_S2 | Baseline-intakemeting en effectgrootte-rapportage | OL_E23_S1 | done |
| OL_E23_S3 | A/B-experiment- en variant-framework | OL_E23_S1, OL_E23_S2 | done |

---

## Epic E24: Learner model — receptief/productief, migreerbaar, individueel

**Doel:** Het learner model versterken conform de literatuur: receptieve
en productieve beheersing apart, BKT achter een migreerbare interface
met graph-aware tracing, en learner-niveau parameters.
**Geschat:** 3 stories
**Afhankelijkheden:** Bestaand BKT/SM-2 learner-model
**Status:** done — alle drie de tiers afgerond (juni 2026).

| Story | Titel | Afhankelijk | Status |
|-------|-------|-------------|--------|
| OL_E24_S1 | Receptieve en productieve mastery apart tracken | — | done |
| OL_E24_S2 | Learner-model-strategie-interface + graph-aware tracing | OL_E24_S1 | done |
| OL_E24_S3 | Learner-niveau parameters (individuele leersnelheid) | OL_E24_S2 | done |

---

## Epic E25: Didactiek — worked examples, motivatie, equity

**Doel:** Didactische patronen toevoegen die de literatuur ondersteunt:
worked examples met faded scaffolding, een motivatielaag tegen de
metacognitieve illusie, en equity-waarborgen voor zwakkere leerlingen.
**Geschat:** 3 stories
**Afhankelijkheden:** E23 (metriek voor triggers en equity-detectie)
**Status:** done — alle drie de tiers afgerond (juni 2026).

| Story | Titel | Afhankelijk | Status |
|-------|-------|-------------|--------|
| OL_E25_S1 | Worked-example oefentype met faded scaffolding | — | done |
| OL_E25_S2 | Motivatielaag tegen de metacognitieve illusie | OL_E23_S1 | done |
| OL_E25_S3 | Equity-waarborgen voor zwakkere leerlingen | OL_E23_S1, OL_E23_S2 | done |

---
---

## Roadmap — toekomstige epics

Uitwerking in stories volgt per epic wanneer deze opgepakt wordt.

---

## Epic E26: Pilot-ready — de eerste echte leerling

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
| OL_E26_S1 | Pilot-ready milestone — eerste echte leerling | doing |

---

## Epic E31: Echte TTS-audio

**Doel:** Placeholder audio vervangen door echte uitspraak. Klassiek Latijn en Erasmiaans Grieks.
**Afhankelijkheden:** E7 done (pipeline staat), E26 (prioriteit op basis van pilot-feedback)
**Status:** todo

Scope:
- espeak-ng configureren voor klassiek Latijn (of alternatief uit OL_E7_S1 evaluatie)
- Erasmiaans Grieks: handmatige opnames overwegen (samenwerking Addisco-docenten?)
- Audio genereren voor alle 450 V-knopen
- Kwaliteitscheck: steekproef door classicus
- audio_ref velden updaten van placeholder naar definitief

Bronnen en leads:
- **espeak-ng** — <https://github.com/espeak-ng/espeak-ng> — open-source formant-synth met ingebouwde Latijnse stem (`la`) en Oud-Grieks (`grc`). GPLv3. Command-line en libary. Macron-support voor lange klinkers via IPA of via [[lengte]]-markers werkt voor klassieke uitspraak; kwaliteit is robotisch maar goed genoeg voor woord-niveau drill.
- Overwegen ná OL_E7_S1 evaluatie: Piper (neural, hogere kwaliteit, geen Latijnse stem out-of-the-box), Coqui TTS (fine-tune vereist), Poeta ex Machina (klassiek-specifiek maar beperkte API).

---

## Epic E27: Items en content voor Grieks + vocabulaire

**Doel:** E15/E16 dekken alleen Latijnse grammatica. Grieks en vocabulaire hebben ook items en content nodig voor een volwaardige ervaring. Parallelstructuur met E15 (items) en E16 (content) voor Latijn.
**Geschat:** 19 stories, ~400 GRC-G-items, ~900 extra V-items, ~40 GRC-markdowns, ~60 SHA-C-markdowns
**Afhankelijkheden:** E2, E3 done (Griekse knopen bestaan); OL_E20_S1 + OL_E20_S3 wenselijk (rendering werkt); OL_E20_S8 voor cultuur (items-basis)
**Status:** done

### Items — GRC grammatica (analoog aan E15)

| Story | Titel | Geschat | Status |
|-------|-------|---------|--------|
| OL_E27_S1 | Items voor GRC alfabet — restknopen (INTRO, groepen, diakritiek, combinaties) | ~60 items | done |
| OL_E27_S2 | Items voor GRC-conceptknopen (naamval/genus/declinatie/tempus-INTRO's) | ~25 items | done |
| OL_E27_S3 | Items voor GRC 1e declinatie (α/η-stammen) | ~30 items | done |
| OL_E27_S4 | Items voor GRC 2e declinatie (ο-stammen m/n) | ~30 items | done |
| OL_E27_S5 | Items voor GRC 3e declinatie (πᾶς, σώφρων) | ~25 items | done |
| OL_E27_S6 | Items voor GRC adjectieven (α/ο-stam + medeklinkerstam) | ~25 items | done |
| OL_E27_S7 | Items voor GRC praesens actief (thematisch + contracta + εἰμί) | ~40 items | done |
| OL_E27_S8 | Items voor GRC imperfectum + augment | ~30 items | done |
| OL_E27_S9 | Items voor GRC aoristus (sigmatisch + thematisch) | ~30 items | done |
| OL_E27_S10 | Items voor GRC pronomina (persoonlijk, bezittelijk, aanwijzend) | ~30 items | done |
| OL_E27_S11 | Items voor GRC voorzetsels + basissyntaxis | ~30 items | done |
| OL_E27_S12 | Validatie — dekking, IRT-params, oefentype-mix (GRC) | — | done |

### Content — GRC grammatica (analoog aan E16)

| Story | Titel | Geschat | Status |
|-------|-------|---------|--------|
| OL_E27_S13 | Content voor GRC concept-INTRO knopen | ~10 bestanden | done |
| OL_E27_S14 | Content voor GRC declinatie-paradigma's | ~8 bestanden | done |
| OL_E27_S15 | Content voor GRC werkwoord-paradigma's | ~10 bestanden | done |
| OL_E27_S16 | Content voor GRC syntaxis | ~6 bestanden | done |
| OL_E27_S17 | Content voor GRC pronomina + adjectieven | ~6 bestanden | done |

### Cultuur en vocabulaire

OL_E27_S18 is opgesplitst in 5 thematische sub-stories voor parallel werk; samen 65 SHA-C-markdowns.

| Story | Titel | Geschat | Status |
|-------|-------|---------|--------|
| OL_E27_S18 | Content voor cultuurknopen (SHA-C) — umbrella | ~65 bestanden | done |
| OL_E27_S19 | SHA-C mythologie | 20 bestanden | done |
| OL_E27_S20 | SHA-C Romeins dagelijks leven | 15 bestanden | done |
| OL_E27_S21 | SHA-C Grieks dagelijks leven | 10 bestanden | done |
| OL_E27_S22 | SHA-C geschiedenis + staatsinrichting | 15 bestanden | done |
| OL_E27_S23 | SHA-C taal, schrift, literatuur | 5 bestanden | done |
| OL_E27_S24 | Vocabulaire — stamtijd-items voor werkwoorden (NL↔lemma was al gerealiseerd) | 94 items | done |

### Resultaat

- **GRC-G-items: 100 % dekking** (142/142 knopen, 389 items) — gemeten via `scripts/validate_items_e3_12.py`
- **GRC-G-content: 45 markdowns** voor concept-INTRO's, declinaties, werkwoorden, syntaxis, pronomina/adjectieven
- **SHA-C-content: 100 % dekking** (65/65 cultuurknopen)
- **V-items: 5 per werkwoord-knoop** (4 basis + 1 stamtijd voor 94 verbs); rest 4 per knoop

**Verhouding tot andere epics:**
- **OL_E20_S1 en OL_E20_S3** moeten draaien voordat GRC-items en -markdowns nut hebben op het scherm.
- **OL_E20_S8** levert minimum-oefenbaarheid voor cultuurknopen; OL_E27_S18 voegt didactische verdieping toe.
- **OL_E20_S11** dekkingsrapport geeft tussentijds voortgangsmeetpunt; OL_E27_S12 gebruikt ditzelfde script.
- **E31** (echte TTS) is nodig voor audio-items: GRC-stem van espeak-ng is de lead.

---

## Epic E32: Productie-deployment

**Doel:** Van localhost naar een publiek toegankelijke applicatie. Single-server deployment, geen over-engineering.
**Afhankelijkheden:** E26 done (pilot-bugs gefixt)
**Status:** todo

Scope:
- VPS provisioning (Hetzner EU, conform AVG)
- Docker Compose: backend + frontend + SQLite (of PostgreSQL migratie)
- HTTPS via Let's Encrypt
- CI/CD: GitHub Actions voor tests + deploy
- Backup-strategie voor learner data
- Domein + DNS
- OAuth / SURFconext voor schoolaccounts (of uitstellen naar E33)

---

## Epic E33: Pensum-module — jaarlijks wisselende auteurs

**Doel:** Het CE-pensum wisselt jaarlijks van auteur. Het systeem moet een jaarlijks te activeren module ondersteunen bovenop de vaste graph.
**Afhankelijkheden:** E26 done, externe validatie door domeinpartner
**Status:** todo

Scope:
- Pensum-datamodel: per examenjaar een set auteurspecifieke cultuurknopen + leesteksten
- Pensum 2026 LTC: Seneca/Cicero (filosofie) — cultuurknopen + integratieknopen
- Pensum 2026 GTC: Homerus (Odyssee) — cultuurknopen + leespassages
- Pensum-selectie bij onboarding (User.examenjaar_ltc/gtc)
- Scheduling engine: pensum-knopen activeren op basis van examenjaar
- Syllabus-overlay: welke cultuurknopen zijn toetsbaar per examenjaar

---

## Epic E34: Leerjaar 2+ content uitbreiden

**Doel:** De knowledge graph uitbreiden voorbij leerjaar 1 richting het volledige eindexamenprogramma.
**Afhankelijkheden:** E26 + E33 done, IRT-kalibratie op pilot-data
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

## Epic E28: Didactische routes — grammatica-eerst vs. context-eerst

**Doel:** De leerling kan kiezen tussen twee didactische routes: de traditionele grammatica-eerst aanpak (huidig) of een context-eerst aanpak (Addisco-stijl) waarbij lezen centraal staat en grammatica wordt aangeboden wanneer het nodig is voor begrip.

Beide routes leiden tot mastery op dezelfde knopen — het verschil is de volgorde en de presentatievorm. SM-2 en BKT werken per knoop en zijn route-onafhankelijk. Wisselen tussen routes verstoort de scheduling niet.

**Afhankelijkheden:** E26 (pilot-feedback), E1+E2 (grammaticaknopen bestaan)
**Status:** done

**Belangrijke ontwerpbeslissing:** de context-first route relaxt de prerequisite-gate. In grammar-first moet een leerling de 1e declinatie beheersen voordat voorzetsels aan bod komen. In context-first kan een passage met voorzetsels worden aangeboden terwijl de declinatie nog niet volledig beheerst is — de passage IS de introductie, met scaffolding.

| Story | Titel | Status |
|-------|-------|--------|
| OL_E28_S1 | Route-keuze model en User-uitbreiding | done |
| OL_E28_S2 | Leespassages als content-type | done |
| OL_E28_S3 | Eerste set leespassages — Latijn onderbouw (~20 passages) | done |
| OL_E28_S4 | Eerste set leespassages — Grieks onderbouw (~15 passages) | done |
| OL_E28_S5 | Context-first scheduling strategie | done |
| OL_E28_S6 | Sessie-orkestratie met passages | done |
| OL_E28_S7 | Frontend: passage-lezer component | done |
| OL_E28_S8 | Frontend: route-selectie en onboarding | done |
| OL_E28_S9 | Grammatica-scaffolding bij passages | done |
| OL_E28_S10 | Validatie: vergelijk leeruitkomsten beide routes | done |

---

## Epic E29: Ontwikkelstraat fase 1 — Python-baseline

**Doel:** Een werkende, laaggewijze ontwikkelstraat die code-kwaliteit, teststatus en storystatus automatisch bewaakt, zodat dit niet meer afhangt van oplettendheid per sessie. Zes lagen: projecttemplate (buiten scope), pre-commit, Claude Code hooks, CI, geautomatiseerde review, gedeelde standaarden.

**Scope:** Alleen Codebase-Olympus. Templatisering naar andere projecten (`my-templates/`) is een latere epic.

**Afhankelijkheden:** Geen. Bouwt voort op bestaande `pyproject.toml`, `ruff`-config en pytest-suite (165 tests).

**Status:** afgerond voor de oorspronkelijke scope — OL_E29_S1 t/m OL_E29_S10 done (Sprint 1, juni 2026). OL_E29_S11 (Olympus-specifieke reviewer-agent) is als follow-up in backlog gezet (gedescopet uit OL_E29_S8).

**Epic-brede acceptatiecriteria:**
- [ ] Alle vijf actieve lagen van de ontwikkelstraat hebben ten minste één werkende check
- [ ] CI is groen op `main` na alle stories
- [ ] Een "break-test" (opzettelijk falende code) wordt geblokkeerd op minstens twee lagen
- [ ] Nieuwe story kan niet naar `done/` zonder dat AC afgevinkt zijn — geautomatiseerd
- [ ] Ontwikkelstraat-werkwijze gedocumenteerd in `CLAUDE.md`

| Story | Titel | Laag | Afhankelijk | Status |
|-------|-------|------|-------------|--------|
| OL_E29_S1 | Storyconventie herstellen (platte backlog/doing/done) | — | — | done |
| OL_E29_S2 | Lint- en formatbasis afmaken (ruff strict) | 1 | — | done |
| OL_E29_S3 | Type-checking toevoegen (mypy) | 1 | — | done |
| OL_E29_S4 | Pre-commit hooks | 2 | OL_E29_S2, OL_E29_S3 | done |
| OL_E29_S5 | CI baseline (GitHub Actions) | 4 | OL_E29_S2, OL_E29_S3 | done |
| OL_E29_S6 | Claude Code hooks (PostToolUse + Stop) | 3 | OL_E29_S2 | done |
| OL_E29_S7 | Storystatus- en AC-verificatie (script + hooks + CI) | 2 + 4 | OL_E29_S4, OL_E29_S5 | done |
| OL_E29_S8 | Review-skills inbedden in workflow | 5 | — | done |
| OL_E29_S9 | CLAUDE.md bijwerken met ontwikkelstraat-sectie | 6 | alle voorgaande | done |
| OL_E29_S10 | validation.py generiek per edge-type maken | 5 | — | done |
| OL_E29_S11 | Olympus-specifieke reviewer-agent | 5 | OL_E29_S8 | backlog |
| OL_E29_S12 | Adopteer codebase-standards canoniek format + drift-validator | 6 | OL_E29_S7 | done |

**Volgorde-advies:** OL_E29_S2 en OL_E29_S3 parallel (beide linter-achtig). OL_E29_S4 en OL_E29_S5 daarna; OL_E29_S7 bouwt op beide. OL_E29_S6 (Claude-hooks) kan vroeg, zodra OL_E29_S2 klaar is, omdat het de inner loop versnelt. OL_E29_S8 en OL_E29_S9 als laatste: eerst moet er iets zijn om te documenteren.

**Niet-scope voor deze epic:**
- Uitrol naar andere repos (voxtral-transcribe, toekomstige apps)
- Template-repo `my-templates/` opzetten
- `mypy --strict` op de hele bestaande codebase (baseline-aanpak volstaat)
- Coverage-thresholds optrekken (wel rapporteren, niet blokkeren)

---

## Spoor N — Naamgeving & consistentie (Engelse code-identifiers)

CLAUDE.md schrijft voor: documentatie in het Nederlands, **code in het
Engels**. De codebase bevat nog vernederlandste identifiers. Dit spoor
brengt code-identifiers naar Engels, gefaseerd op risico (afgeleid uit een
inventarisatie, juni 2026).

**Tiers:**
- **Tier 1 (veilig, niet-breaking):** klasse-/enum-*namen*. Pydantic
  serialiseert veldnamen, niet klassenamen → geen data-impact. = OL_E30_S1..03.
- **Tier 2 (breaking, geen data-bestand-migratie):** learner-model
  *veldnamen* (`knoop_id` → `node_id`, …). Breekt opgeslagen learner-data,
  maar staat in 0 graph-databestanden → re-seed lost het op (zoals OL_E23_S1).
- **Tier 3 (breaking + data-migratie):** graph-JSON *schema-keys*
  (`titel_nl`, `beschrijving`, `antwoord`, `moeilijkheid_initieel`,
  `verwachte_tijd_sec`, `bloom_niveau`, `toetsbaar`, `pensum_jaren`,
  `knoop_ids`) en
  enum-*waarden* (`receptief`/`productief`, bloom-/fase-waarden). Vereist
  migratie van ~7-9 graph-databestanden + loader + veel tests. **Besloten (juni 2026): volledige Tier 3 wordt uitgevoerd** — "pijnlijk
  maar anders blijven we ermee zitten". Stories worden uitgewerkt zodra E30
  start (na de Sprint-2-merge).

**Uitvoervolgorde:** OL_E30_S1 → OL_E30_S2 → OL_E30_S3 (elk eigen, kleine PR; per
rename de volledige suite groen). Tier 2/3 daarna, alleen na expliciet
akkoord over de scope.

**Afhankelijkheden:** raakt `models/graph.py` en `models/learner.py` —
plannen ná merge van lopend werk dat diezelfde bestanden aanpast
(Sprint 2 / E23), om merge-conflicten te vermijden.

**Status:** done — alle drie de tiers afgerond (juni 2026).

## Epic E30: Vernederlandste code-identifiers naar Engels

| Story | Titel | Tier | Status |
|-------|-------|------|--------|
| OL_E30_S1 | KnoopState → NodeState | 1 | done |
| OL_E30_S2 | KennisKnoop → Node | 1 | done |
| OL_E30_S3 | Enum-klassen naar Engels | 1 | done |
| OL_E30_S4 | knoop-veldnamen + attribuutkey → node | 2 | done |
| OL_E30_S5 | JSON-schema-keys → Engels | 3 | done |
| OL_E30_S6 | Enum-waarden → Engels | 3 | done |

**Scope besloten: t/m Tier 3** (volledig). Tier 2- en Tier 3-stories
(veldnamen, JSON-keys, enum-waarden + datamigratie) worden uitgewerkt zodra
E30 daadwerkelijk start, ná de Sprint-2-merge.
