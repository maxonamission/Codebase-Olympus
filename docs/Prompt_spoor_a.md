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

### Kwaliteitseisen voor knopen

De volgende eisen gelden voor alle knopen in spoor A. Ze zijn het resultaat van een vergelijking tussen twee onafhankelijke sessies die dezelfde stories uitvoerden — de ene produceerde betere beschrijvingen, de andere een betere grafstructuur. Deze eisen combineren het beste van beide.

#### 1. Beschrijvingen: formaat en precisie

Elke `beschrijving` volgt een formaat dat disambigueert en vakinhoudelijk precies is. Het patroon verschilt per knooptype:

**Fonologie-knopen (FONL — letters, klanken, diakritiek):**
```
"De letter èta: Η (majuskel), η (minuskel). Klank: lang /ɛː/. Valse vriend: majuskel lijkt op Latijns H maar is een klinker."
```
Patroon: **Wat** (naam + vormen) → **Klank** (IPA-notatie) → **Disambiguatie**.
- Gebruik altijd IPA-notatie: `/a/`, `/tʰ/`, `/pʰ/`, `/kʰ/`, `/ɛː/`, `/ɔː/`, `/ŋ/`.
- Vermeld bij Griekse letters altijd majuskel én minuskel.
- Geef bij valse vrienden expliciet aan wat het verschil is.
- Bij Erasmiaanse uitspraak: geaspireerden (θ, φ, χ) met hoorbare aspiratie, niet als fricatieven.
- Bij accenten: geef een Grieks woordvoorbeeld (bv. λόγος, τοῦ, δῶρον).

**Morfologie-knopen (MORF — declinaties, conjugaties, paradigma's):**

Conceptknopen (INTRO):
```
"Introductie van het imperfectum: vorming (stam + ba + persoonsuitgang) en gebruik (duurhandeling in het verleden)."
```
Patroon: **Wat** (naam concept) → **Vorming** (hoe herkenbaar) → **Gebruik** (functie).

Naamvalsknopen (per declinatie):
```
"De genitivus sg. (-ae) en pl. (-arum) van de 1e declinatie."
```
Patroon: **Naamval** → **Uitgangen** sg. en pl. → **Declinatie**.

Werkwoordstijdknopen (per conjugatie):
```
"Alle zes persoonsvormen van het presens ind. act. van de 1e conjugatie: amo, amas, amat, amamus, amatis, amant."
```
Patroon: **Bereik** (6 vormen) → **Tijd/modus/diathese** → **Conjugatie** → **Modelparadigma**.

Paradigma-intro-knopen (per declinatie):
```
"Overzicht van de 1e declinatie (a-stammen). Modelwoord: puella, -ae (v.)."
```
Patroon: **Naam** → **Stamtype** → **Modelwoord met genitief en genus**.

**Syntaxis-knopen (SYNT — zinsbouw, functies):**
```
"De nominativus als naamval van het onderwerp en het naamwoordelijk deel van het gezegde."
```
Patroon: **Vorm** → **Syntactische functie(s)**. Geen paradigma, wél functieomschrijving.

```
"Veelvoorkomende voorzetsels die de accusativus vereisen: in (+acc), ad, per, ante, post, etc."
```
Patroon: **Regel** → **Voorbeelden** (3-5 representatieve items).

**Vocabulaire-knopen (type V):**
```
"Het werkwoord εἰμί (zijn): onregelmatig, alle vormen suppletief. Frequentieband F01."
```
Patroon: **Lemma** (origineel schrift + vertaling) → **Bijzonderheid** → **Frequentieband**.

```
"Het zelfstandig naamwoord terra, -ae (v.): aarde, land. 1e declinatie. Frequentieband F01."
```
Patroon: **Lemma** met stamtijden/genitief → **Vertaling** → **Declinatie/conjugatie** → **Frequentieband**.

**Cultuur-knopen (type C):**
```
"Zeus/Jupiter: oppergod, heerser over hemel en bliksem. Verschijnt in vrijwel alle mythologische verhalen."
```
Patroon: **Grieks/Latijns equivalent** → **Kernidentificatie** → **Belang/context**.

**Universele regels:**
- Max 2 zinnen. Geen opsommingen van 3+ items in de beschrijving — dat hoort in een groepsknoop.
- Volg bestaande beschrijvingen in `data/graph/` als referentie voor stijl en diepte.

#### 2. ID-naamgeving: consistente afkortingen

- Segmenten max **5-6 tekens** per stuk (niet het schema-maximum van 8). Dit houdt IDs leesbaar.
- Gebruik **consequent dezelfde afkortingsstrategie**: EPSIL (niet EPSLN), LAMBD (niet LAMBDA), OMIKR (niet OMIKRN), UPSIL (niet UPSLN).
- Segmentnamen in het **Nederlands of Latijn**, consistent met bestaande patronen: MORF, SYNT, FONL, KOMBI, DIAK, ALFA. Niet: COMB, PHON, ALPHA.
- Raadpleeg altijd `data/graph/` om bestaande naamconventies te volgen.

#### 3. Didactische groepering

Waar een story >10 individuele knopen bevat op hetzelfde niveau, maak **groeperingsknopen** die de leerling door de stof leiden:

```
INTRO → GRP1 → GRP2 → GRP3 → individuele knopen per groep
```

Groepeer op didactisch relevante criteria per epic:
- **Alfabet (A3):** visuele gelijkenis met Latijn (identiek / afwijkende vorm / valse vrienden / uniek)
- **Declinaties (A1/A2):** NIET groeperen — 6 naamvallen per declinatie is al een beheerbaar aantal; gebruik de DECL-INTRO als groeperingsknoop
- **Conjugaties (A1/A2):** per tempus een INTRO-knoop, dan per conjugatie (C1-C4) de paradigma-knopen
- **Vocabulaire (A4):** groepeer per semantisch cluster binnen een frequentieband als een cluster >10 woorden bevat
- **Cultuur (A5):** groepeer per thema (mythologie, dagelijks leven, geschiedenis)

Voordeel: de DAG blijft beheersbaar (4 kinderen i.p.v. 24 vanuit INTRO) en het leerpad is expliciet.

**Wanneer NIET groeperen:** declinatie-naamvallen (max 6 per decl.), pronomina-types (max 4-5), diakritische subcategorieën (max 3 accenten). Groepsknopen voor <6 items zijn overhead.

#### 4. Edge-gebruik: prerequisite vs. enrichment

- **prerequisite**: de target-knoop is niet leerbaar zonder de source. Gebruik voor de hoofdstructuur van het leerpad.
- **enrichment**: de source verrijkt het begrip van de target, maar is niet strikt nodig. Gebruik voor:
  - Cross-section verbindingen (bv. diakritiek-knopen → leesvaardigheid)
  - Verwante concepten die elkaars begrip versterken (bv. acutus → gravis, gamma → nasaal-gamma)
  - Verbindingen tussen subsecties (bv. iota subscriptum → oneigenlijke diftongen)

**Enrichment-edges die vaak vergeten worden:**
- Diakritiek → leesvaardigheid (je moet spiritus en accenten kennen om te kunnen lezen)
- Individuele letters → lettercombinaties die ze bevatten (gamma → nasaal-gamma)
- Accenttypen onderling (acutus → gravis, want gravis vervangt acutus op de ultima)

#### 5. Integratiepunten per subgraph

Elke subgraph moet uitmonden in een **toetsbare integratie-knoop** (bloom_niveau: `toepassing`). Voorbeelden:
- **Alfabet:** `KOMBI-LEESV` — Griekse woorden hardop lezen
- **Declinatie:** een knoop die alle naamvallen van die declinatie combineert in een herkenningstaak (bv. `LAT-G-MORF-DECL1-HERK`)
- **Werkwoord:** een knoop die persoonsvorm-herkenning over conjugaties heen toetst per tempus
- **Vocabulaire:** niet per woord, maar per frequentieband: een knoop die de ~100 woorden van F01 combineert in contextherkenning

Deze integratie-knoop krijgt prerequisite-edges vanuit alle relevante deelknopen.

#### 6. Bloom-niveaus: richtlijnen per knooptype

De PoC gebruikt drie niveaus met een duidelijk patroon. Volg dit:

| Knooptype | bloom_niveau | Wanneer |
|-----------|-------------|---------|
| INTRO / conceptknoop | `kennis` | Definitie, overzicht, geen actieve toepassing |
| Functie-/gebruiksknoop (SYNT) | `begrip` | Leerling begrijpt de rol van een vorm in de zin |
| Paradigma-/vormknoop (uitgangen, vormen) | `toepassing` | Leerling kan de vorm herkennen én produceren |
| Integratie-/herkenningsknoop | `toepassing` | Leerling past kennis toe op onbekende voorbeelden |

Gebruik `analyse` pas in bovenbouw of bij complexe syntaxis (AcI, ablativus absolutus — buiten scope klas 1).

#### 7. Encompassing_weight: richtlijnen

De PoC gebruikt weights tussen 0.2 en 0.5 met dit patroon:

| Weight | Betekenis | Voorbeeld |
|--------|-----------|-----------|
| **0.2** | Zwakke prerequisite — helpt maar is niet essentieel | enrichment-edge, optionele context |
| **0.3** | Standaard prerequisite — normaal vereiste voorkennis | naamval-intro → declinatie-intro |
| **0.4** | Sterke prerequisite — direct noodzakelijk | declinatie-intro → paradigmaknopen |
| **0.5** | Kritieke prerequisite — knoop is niet leerbaar zonder source | overzichtsknoop → specifieke deelvormen |

Gebruik **0.3 als default**. Verhoog naar 0.4-0.5 alleen als de target echt onbegrijpelijk is zonder de source.

#### 8. Grieks-specifieke aandachtspunten

- **Alle GRC-G-knopen** (behalve alfabet/fonologie) krijgen een prerequisite-edge vanuit `GRC-G-FONL-KOMBI-LEESV`. Een leerling moet het alfabet beheersen vóór grammatica.
- **Augment** (imperfectum, aoristus): beschrijf altijd het type (syllabisch ἐ- vs. temporaal) en de positie (voor de stam).
- **Contracta** (ποιέω-type): vermeld welke klinker contraheert en het resultaat.
- **Lidwoord** ὁ, ἡ, τό: dit is een zelfstandige knoop, geen onderdeel van de declinatie. Het Griekse lidwoord bestaat niet in het Latijn en is een cruciale marker.
- **Medium/passivum, conjunctivus, optativus**: buiten scope klas 1, niet modelleren.

#### 9. Latijn-specifieke aandachtspunten

- **Bestaande PoC-knopen** (50 stuks in `lat_grammatica_poc.json`): nieuwe A1-knopen moeten hierop aansluiten, niet dupliceren. Check altijd of een knoop al bestaat.
- **Stamtijden**: bij perfectum-knopen altijd het type noemen (v-perfectum, u-perfectum, reduplicatie, stamwisseling).
- **esse/posse**: onregelmatig, altijd apart modelleren met volledige paradigma's in de beschrijving.
- **Naamvalsfuncties** (SYNT-knopen): de PoC heeft al functie-knopen voor nom/acc/gen/dat/abl. A1-stories moeten hier edges naartoe leggen, niet nieuwe functie-knopen aanmaken.

#### 10. Vocabulaire-specifieke aandachtspunten (A4)

- **`semantisch_cluster`-veld** invullen: lowercase, max 20 chars. Bv. `goden`, `familie`, `oorlog`, `natuur`, `basiswerkwoord`.
- **Prerequisite-edge naar grammatica**: elk vocabulairewoord krijgt een edge naar de relevante declinatie- of conjugatie-INTRO-knoop (bv. `terra` → `LAT-G-MORF-DECL1-INTRO`).
- **Lemma-formaat** in `titel_nl`: Latijn: "terra, -ae (v.) — aarde", Grieks: "λόγος, -ου (m.) — woord, rede".
- **Frequentieband** in ID: F01 (top 100), F02 (101-200), F03 (201-300).

#### 11. Taalgebruik

- `beschrijving`: Nederlands, met Griekse/Latijnse voorbeelden in origineel schrift.
- `titel_nl`: Nederlands, mag Grieks/Latijns schrift bevatten (bv. "Α α — alfa", "Praesens indicativus actief — 1e conjugatie").
- Segmentnamen in IDs: Latijns/Nederlands (MORF, FONL, KOMBI, DIAK, PRAES, IMPF, PERF), niet Engels (COMB, PHON, PRES).
- Gebruik "polytoon" (niet "polytonic"), "diftong" (niet "diphthong"), "nasaal" (niet "nasal") in beschrijvingen.
- Naamvallen in IDs: NOM, GEN, DAT, ACC, ABL, VOC (Latijnse afkortingen, consistent met PoC).

### Werkwijze per story

1. Lees de relevante sectie uit de CvTE-minimumlijst (syllabi in docs/)
2. Cross-refereer met de klas 1-afbakening in `docs/A_Lesstof_Latijn_Grieks.md`
3. Lees **bestaande knopen** in `data/graph/` om naamconventies, beschrijvingsstijl en edge-patronen te volgen
4. Genereer de knopen als JSON conform het GraphData-schema, met de kwaliteitseisen hierboven
5. Voeg prerequisite-edges toe voor het leerpad, plus enrichment-edges voor cross-section verbindingen
6. Voeg de nieuwe knopen toe aan het bestaande JSON-bestand of maak een nieuw bestand per epic
7. Run `python scripts/validate_graph.py data/graph/` — moet groen zijn (zowel individueel bestand als hele directory)
8. Verplaats de story van `todo/` naar `done/`
9. Commit: `feat(graph): [story-id] — [korte beschrijving]`

### Begin nu met:
1. De mappenstructuur aanmaken
2. EPICS.md schrijven
3. Alle story-bestanden aanmaken in de juiste `todo/` mappen
4. Wacht op mijn akkoord voordat je begint met de eerste story (A3-01)
