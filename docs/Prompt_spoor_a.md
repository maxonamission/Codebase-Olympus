# Prompt: Spoor A — Knowledge Graph Content (Leerjaar 1, beide talen)

## Context

Spoor B (core learning loop) is in ontwikkeling. Dit is spoor A: het vullen van de knowledge graph naar ~800 knopen voor leerjaar 1 gymnasium, Latijn én Grieks.

Lees eerst deze bestanden in `docs/`:
- `BRIEFING_GYMNASIUM_CLASSICA.md` — projectvisie en architectuur
- `ONTWERPKEUZES_GYMNASIUM_CLASSICA.md` — vastgestelde keuzes, inclusief het KennisKnoop-schema
- `RESEARCH_LESSTOF_KLAS1.md` — research over exacte grammaticale scope per methode, vocabulaire-bronnen, en cultuurthema's
- `Grieks.pdf` — CvTE syllabus GTC 2026, bijlage 3 = minimumlijst Grieks (vormleer + syntaxis + literaire termen)
- `Latijn.pdf` — CvTE syllabus LTC 2026, bijlage 3 = minimumlijst Latijn (vormleer + syntaxis + literaire termen + appendix stamtijden)

Lees ook het bestaande ID-schema en Pydantic models in `src/gymnasium_classica/` en de PoC-knopen in `data/graph/lat_grammatica_poc.json` — de nieuwe knopen moeten consistent zijn met wat er al staat.

## Opdracht: stories-structuur opzetten en epic plannen

### Stap 1: Maak de volgende mappenstructuur aan

```
stories/
├── EPICS.md                    # Overzicht van alle epics met status
├── epic-a1-grammatica-latijn/
│   ├── todo/                   # Stories die nog uitgevoerd moeten worden
│   └── done/                   # Afgeronde stories (verplaatst uit todo/)
├── epic-a2-grammatica-grieks/
│   ├── todo/
│   └── done/
├── epic-a3-alfabet-grieks/
│   ├── todo/
│   └── done/
├── epic-a4-vocabulaire/
│   ├── todo/
│   └── done/
├── epic-a5-cultuur/
│   ├── todo/
│   └── done/
└── epic-a6-transfer-edges/
    ├── todo/
    └── done/
```

### Stap 2: Schrijf `stories/EPICS.md`

Dit document bevat per epic:
- Titel en doel
- Geschat aantal knopen/edges
- Afhankelijkheden (welke epics moeten eerst)
- Status: todo / in progress / done
- Lijst van stories (verwijzingen naar de md-bestanden)

### Stap 3: Schrijf de stories per epic

Elke story is een markdown-bestand in de `todo/` map van zijn epic. Formaat:

```markdown
# Story [EPIC]-[NR]: [titel]

## Doel
Wat deze story oplevert (specifiek: welke knopen, welke JSON-bestanden)

## Input
Welke bronbestanden worden gebruikt (syllabi, research, PoC-knopen)

## Acceptatiecriteria
- [ ] Knopen voldoen aan het ID-schema (validate_knoop_id)
- [ ] Prerequisite-edges zijn correct en vormen een DAG (geen cycli)
- [ ] JSON valideert tegen het Pydantic GraphData-model
- [ ] validate_graph.py draait zonder errors
- [ ] Beschrijving per knoop: 1-2 zinnen (kort, disambiguerend)

## Scope
Expliciete lijst van grammaticale verschijnselen / woorden / thema's

## Geschat aantal knopen
[N]
```

### De zes epics en hun stories

**Epic A1: Grammatica Latijn (~150 knopen)**
De methode-onafhankelijke grammaticale kern van klas 1, gebaseerd op de CvTE-minimumlijst gefilterd op wat alle methoden gemeen hebben (zie research):
- Story A1-01: Conceptknopen en naamvalsysteem (~15 knopen: naamval-intro, declinatie-intro, genus, numerus, casus-functies)
- Story A1-02: 1e declinatie — alle naamvallen + paradigma (~10 knopen)
- Story A1-03: 2e declinatie — o-stammen masculinum + neutrum (~12 knopen)
- Story A1-04: 3e declinatie — consonantstammen + i-stammen basis (~15 knopen)
- Story A1-05: Adjectieven bonus-type en fortis-type (~10 knopen)
- Story A1-06: Werkwoord-concepten — conjugatie-intro, persoon, numerus, tempus, modus (~10 knopen)
- Story A1-07: Praesens indicativus actief — 4 conjugaties + esse (~15 knopen)
- Story A1-08: Imperfectum indicativus actief (~8 knopen)
- Story A1-09: Perfectum indicativus actief — inclusief stamtijdentypen (~12 knopen)
- Story A1-10: Plusquamperfectum indicativus actief (~5 knopen)
- Story A1-11: Imperativus + infinitivus praesens actief (~6 knopen)
- Story A1-12: Pronomina — persoonlijk, bezittelijk, aanwijzend begin (~12 knopen)
- Story A1-13: Voorzetsels met accusativus en ablativus (~8 knopen)
- Story A1-14: Basissyntaxis — woordvolgorde, congruentie, ontkenning, vraagzinnen (~12 knopen)
- Story A1-15: Review en prerequisite-edge validatie voor heel epic A1

**Epic A2: Grammatica Grieks (~100 knopen)**
Idem, voor Grieks. Gebaseerd op de GTC-minimumlijst gefilterd op klas 1 scope (Pallas les 1-14 / ARGO thema 1-4):
- Story A2-01: Conceptknopen Grieks — lidwoord, naamvalsysteem (~10 knopen)
- Story A2-02: 1e declinatie (α/η-stammen) (~10 knopen)
- Story A2-03: 2e declinatie (ο-stammen) (~10 knopen)
- Story A2-04: 3e declinatie introductie — via adjectieven πᾶς, σώφρων (~8 knopen)
- Story A2-05: Adjectieven α/ο-stam en medeklinkerstam (~8 knopen)
- Story A2-06: Praesens indicativus actief — thematisch + contracta + εἰμί (~12 knopen)
- Story A2-07: Imperfectum indicativus actief — augment (~8 knopen)
- Story A2-08: Aoristus introductie — sigmatisch + thematisch (~10 knopen)
- Story A2-09: Pronomina — persoonlijk, bezittelijk, aanwijzend (~10 knopen)
- Story A2-10: Voorzetsels + basissyntaxis (~8 knopen)
- Story A2-11: Review en prerequisite-edge validatie voor heel epic A2

**Epic A3: Grieks alfabet — onboarding-subgraph (~40 knopen)**
Prerequisite voor alle GRC-knopen:
- Story A3-01: Letters herkenning — 24 letters, majuskel + minuskel (~24 knopen, of gegroepeerd)
- Story A3-02: Diakritische tekens — spiritus, accenten, iota subscriptum (~8 knopen)
- Story A3-03: Lettercombinaties en uitspraak — diphthongen, γγ=ng, speciale combinaties (~8 knopen)

**Epic A4: Vocabulaire (~400 knopen)**
Individuele woorden, frequentiegestuurd, met semantisch cluster:
- Story A4-01: Strategie en bronnen — DCC Latin Core top-300 mappen op klas 1, DCC Greek Core top-150, semantische clusters definiëren → `data/vocabulaire_clusters.json`
- Story A4-02: Latijn frequentieband F01 — top-100 woorden (~100 knopen)
- Story A4-03: Latijn frequentieband F02 — woorden 101-200 (~100 knopen)
- Story A4-04: Latijn frequentieband F03 — woorden 201-300 (~100 knopen)
- Story A4-05: Grieks frequentieband F01 — top-75 woorden (~75 knopen)
- Story A4-06: Grieks frequentieband F02 — woorden 76-150 (~75 knopen)
- Story A4-07: Prerequisite-edges vocabulaire → grammatica (elk woord linken aan zijn declinatie/conjugatie-knoop)

**Epic A5: Cultuur (~70 knopen)**
Gedeelde (SHA-C-*) cultuurknopen:
- Story A5-01: Mythologie — Olympische goden, helden, Troje, Odysseus (~20 knopen)
- Story A5-02: Romeins dagelijks leven — familia, domus, school, eten, slavernij (~15 knopen)
- Story A5-03: Geschiedenis basis — Romulus, Republiek, legioenen, forum (~15 knopen)
- Story A5-04: Grieks dagelijks leven — polis, agora, gymnasium, symposium (~10 knopen)
- Story A5-05: Taal en schrift — Latijns alfabet, Grieks alfabet, inscripties (~5 knopen)
- Story A5-06: Prerequisite-edges cultuur → taal/integratie

**Epic A6: Transfer-edges (~100 edges)**
Cross-linguïstische verbindingen, type `transfer`:
- Story A6-01: Naamvalsysteem — LAT nominativus ↔ GRC nominativus etc. (~30 edges)
- Story A6-02: Werkwoordsmorfologie — praesens/imperfectum/aoristus parallellen (~30 edges)
- Story A6-03: Cultuur — gedeelde mythologie en geschiedenis (~20 edges)
- Story A6-04: Vocabulaire — cognaten en leenwoorden (~20 edges)
- Story A6-05: Validatie transfer-edges — geen cycli, weights correct

### Uitvoervolgorde

1. **A3** (alfabet) — klein, zelfstandig, blokkeert niets
2. **A1** (grammatica Latijn) — bouwt voort op de PoC-knopen die er al zijn
3. **A2** (grammatica Grieks) — structureel parallel aan A1
4. **A4** (vocabulaire) — heeft A1+A2+A3 nodig voor prerequisite-edges
5. **A5** (cultuur) — onafhankelijk van A1-A4 maar edges lopen ernaar
6. **A6** (transfer-edges) — heeft A1+A2+A3+A4+A5 nodig

### Werkwijze per story

1. Lees de relevante sectie uit de CvTE-minimumlijst (syllabi in docs/)
2. Cross-refereer met de klas 1-afbakening in RESEARCH_LESSTOF_KLAS1.md
3. Genereer de knopen als JSON conform het GraphData-schema
4. Voeg prerequisite-edges toe
5. Voeg de nieuwe knopen toe aan het bestaande JSON-bestand of maak een nieuw bestand per epic
6. Run `python scripts/validate_graph.py` — moet groen zijn
7. Verplaats de story van `todo/` naar `done/`
8. Commit: `feat(graph): [story-id] — [korte beschrijving]`

### Begin nu met:
1. De mappenstructuur aanmaken
2. EPICS.md schrijven
3. Alle story-bestanden aanmaken in de juiste `todo/` mappen
4. Wacht op mijn akkoord voordat je begint met de eerste story (A3-01)
