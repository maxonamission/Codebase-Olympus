# Prompt: Spoor C — Items genereren en content schrijven

## Context

Spoor A vult de knowledge graph met ~850 knopen. Spoor B heeft de learning loop gebouwd (BKT, SM-2, scheduling, sessie-orkestratie). Dit is spoor C: het genereren van oefeningen (Items) en didactische content voor de bestaande knopen, zodat het systeem bruikbaar wordt voor een pilot.

**Doel:** een Latijn leerjaar 1-leerling kan een volledige 30-minuten sessie draaien met echte oefeningen en uitleg.

Lees eerst:
- `CLAUDE.md` — projectoverzicht, ID-schema, content-architectuur
- `src/gymnasium_classica/models/graph.py` — het Item-model en alle enums
- `data/graph/lat_grammatica_poc.json` — de 50 PoC-knopen (referentie)
- `data/graph/lat_grammatica_leerjaar1.json` — de nieuwere A1-knopen
- `data/content/LAT-G-MORF-DECL1-INTRO.md` — voorbeeld content-bestand

## Twee deelsporen

### Deelspoor C1: Items genereren voor Latijnse grammaticaknopen

Elke kennisknoop heeft een veld `items: list[Item]`. In fase 0/1 is dit leeg. Nu vullen.

**Het Item-model:**
```python
class Item(BaseModel):
    id: str                          # Uniek, bijv. "ITEM-LAT-G-MORF-NOM-D1-001"
    knoop_ids: list[str]             # Welke knopen dit item toetst
    type: ItemType                   # herkenning, productie, analyse, synthese, contextueel, offline_schrijven
    richting: Richting               # receptief, productief
    moeilijkheid_initieel: float     # IRT b-parameter (-3 tot +3, 0 = gemiddeld)
    discriminatie_initieel: float    # IRT a-parameter (> 0, typisch 0.5-2.0)
    verwachte_tijd_sec: int          # Verwachte antwoordtijd in seconden
    stimulus: str | dict             # De opgave
    antwoord: str | list[str]        # Correct antwoord(en)
    feedback: str                    # Uitleg bij fout antwoord
    bron: Bron                       # handmatig, llm_gegenereerd, authentiek
    audio_ref: Optional[str]         # Pad naar audiobestand (fase 3)
    verificatie_methode: Optional[..] # Voor offline_schrijven items
    verwacht_resultaat: Optional[str] # Voor offline_schrijven items
```

**Item-ID schema:** `ITEM-{KNOOP_ID}-{NR}` (3-cijferig volgnummer)
Voorbeeld: `ITEM-LAT-G-MORF-NOM-D1-001`

**Oefentypen per knooptype:**

| Knooptype | Oefentype | Richting | Voorbeeld |
|-----------|-----------|----------|-----------|
| MORF INTRO | herkenning | receptief | "Hoeveel declinaties kent het Latijn?" → "5" |
| MORF paradigma | herkenning | receptief | "Welke naamval is 'puellae' (1e decl.)?" → "genitivus sg. of nominativus pl." |
| MORF paradigma | productie | productief | "Geef de accusativus meervoud van 'puella'." → "puellas" |
| MORF paradigma | analyse | receptief | "Ontleed 'puellarum' volledig." → "genitivus pluralis, 1e declinatie" |
| SYNT functie | herkenning | receptief | "Welke naamval gebruik je voor het lijdend voorwerp?" → "accusativus" |
| SYNT functie | contextueel | receptief | "Welke functie heeft 'puellam' in: 'Dominus puellam videt'?" → "lijdend voorwerp" |
| CONJ paradigma | productie | productief | "Vervoeg 'amare' in de 3e persoon enkelvoud presens." → "amat" |
| CONJ paradigma | herkenning | receptief | "Welke persoon en getal is 'amabamus'?" → "1e persoon meervoud imperfectum" |

**IRT-parameters richtlijnen:**
- `moeilijkheid_initieel`: herkenning = -1.0 tot 0.0, productie = 0.0 tot 1.5, analyse = 0.5 tot 2.0
- `discriminatie_initieel`: 1.0 als default, 1.5 voor scherp discriminerende items, 0.7 voor brede items
- `verwachte_tijd_sec`: herkenning = 10-15s, productie = 20-30s, analyse = 30-45s, contextueel = 30-60s

**Minimumaantal items per knoop:**
- INTRO-knopen: 2-3 items (kennis-check)
- Paradigmaknopen: 4-6 items (mix herkenning + productie)
- Functie-/syntaxisknopen: 3-5 items (mix herkenning + contextueel)

**Feedback-kwaliteit:**
Elke `feedback` string moet:
- De correcte regel benoemen ("De genitivus enkelvoud van de 1e declinatie eindigt op -ae")
- Het specifieke foutpatroon adresseren waar mogelijk ("Let op: -as is de accusativus meervoud, niet de genitivus")
- Maximaal 2 zinnen

### Deelspoor C2: Content schrijven voor kernknopen

Elke knoop kan een `content_ref` hebben dat verwijst naar `data/content/{KNOOP_ID}.md`.

**Format (zie bestaand voorbeeld `LAT-G-MORF-DECL1-INTRO.md`):**

```markdown
---
knoop_id: LAT-G-MORF-DECL1-INTRO
laatst_bijgewerkt: 2026-04-13
auteur: handmatig
---

# [Titel]

## Overzicht
[1-2 alinea's: wat is dit concept, waarom is het belangrijk]

## Paradigma
[Tabel met volledige verbuiging/vervoeging]

## Herkenningstips
[Hoe herken je deze vorm in een tekst]

## Let op
[Veelgemaakte fouten, valse vrienden, uitzonderingen]
```

**Prioriteit:** schrijf content voor knopen die het meest impact hebben op de learning loop:
1. INTRO-knopen (de leerling leest dit als eerste bij nieuwe stof)
2. Paradigmaknopen met onregelmatigheden (esse, 3e declinatie)
3. Syntaxisknopen (woordvolgorde, AcI — conceptueel moeilijker)

**Omvang:** 50-150 woorden per bestand. Beknopt maar compleet.

## Epics en stories

### Epic C1: Items genereren

| Story | Titel | Scope | Geschat |
|-------|-------|-------|---------|
| C1-01 | Items voor conceptknopen (INTRO) | A1-01 knopen: naamval, declinatie, genus, numerus, persoon, tempus | ~20 items |
| C1-02 | Items voor 1e declinatie | A1-02 knopen: alle naamvallen | ~30 items |
| C1-03 | Items voor 2e declinatie | A1-03 knopen: alle naamvallen incl. neutrum | ~35 items |
| C1-04 | Items voor 3e declinatie | A1-04 knopen | ~40 items |
| C1-05 | Items voor adjectieven | A1-05 knopen | ~25 items |
| C1-06 | Items voor presens indicativus | A1-06 + A1-07 knopen: 4 conjugaties + esse | ~50 items |
| C1-07 | Items voor imperfectum + perfectum | A1-08 + A1-09 knopen | ~40 items |
| C1-08 | Items voor overige werkwoordsvormen | A1-10 + A1-11 knopen: plqpf, imperativus, infinitivus | ~25 items |
| C1-09 | Items voor pronomina | A1-12 knopen | ~30 items |
| C1-10 | Items voor voorzetsels + syntaxis | A1-13 + A1-14 knopen | ~35 items |
| C1-11 | Validatie: alle items laden, IRT-parameters check, dekking per knoop | — | — |

### Epic C2: Content schrijven

| Story | Titel | Scope | Geschat |
|-------|-------|-------|---------|
| C2-01 | Content voor concept-INTRO knopen | naamval, declinatie, conjugatie, tempus, genus | ~8 bestanden |
| C2-02 | Content voor declinatie-paradigma's | 1e, 2e, 3e declinatie met volledige tabellen | ~6 bestanden |
| C2-03 | Content voor werkwoord-paradigma's | presens, imperfectum, perfectum, esse | ~8 bestanden |
| C2-04 | Content voor syntaxis | woordvolgorde, congruentie, voorzetsels, AcI | ~6 bestanden |
| C2-05 | Content voor pronomina + adjectieven | persoonlijk, bezittelijk, aanwijzend, bonus/fortis-type | ~6 bestanden |

## Afhankelijkheden

- **C1 (items)** hangt af van de A1-knopen die al bestaan. Stories kunnen starten zodra de corresponderende A1-story done is. C1-01 en C1-02 kunnen nu al (A1-01 en A1-02 zijn done).
- **C2 (content)** is onafhankelijk van C1 — content en items zijn parallelle werkstromen.
- **C1 en C2 zijn onafhankelijk van spoor B.**

## Timeout-preventie

- **Eén story per keer.** Niet meerdere stories combineren.
- **Genereer items via een Python-script.** Definieer items als dicts, valideer via `Item(**data)`, voeg toe aan het JSON-bestand, toon alleen de samenvatting.
- **Content-bestanden zijn klein** (~50-150 woorden) en kunnen direct geschreven worden.
- **Commit na elke story.**

## Werkwijze per C1-story (items)

1. Lees de relevante knopen uit `data/graph/` (welke knoop-IDs, welke beschrijvingen)
2. Schrijf een Python-script dat:
   - Per knoop 3-6 items definieert (mix oefentypen)
   - Items valideert via `Item(**data)`
   - Laadt het bestaande JSON-bestand, voegt items toe aan de knopen, schrijft terug
   - Print: aantal items per knoop, totaal, oefentype-verdeling
3. Run het script
4. Run `python scripts/validate_graph.py data/graph/` — moet groen zijn
5. Commit: `feat(items): [story-id] — [korte beschrijving]`

## Werkwijze per C2-story (content)

1. Lees de knoop-beschrijving uit `data/graph/`
2. Schrijf het markdown-bestand in `data/content/{KNOOP_ID}.md` met het vaste format
3. Update `content_ref` op de knoop in het JSON-bestand (optioneel, kan later in bulk)
4. Commit: `feat(content): [story-id] — [korte beschrijving]`

## Kwaliteitscheck

Na alle C1-stories:
- Elke LAT-G knoop heeft minimaal 2 items
- Mix van oefentypen: minimaal 30% herkenning, 30% productie, 10% contextueel
- IRT-parameters zijn ingevuld en realistisch
- Feedback is specifiek en benoemt de regel

Na alle C2-stories:
- Elke INTRO-knoop en elke paradigma-knoop heeft een content-bestand
- Paradigmatabellen zijn compleet (geen ontbrekende naamvallen/personen)
- Beknopt maar volledig (~50-150 woorden)
