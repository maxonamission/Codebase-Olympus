# 03 — De adaptieve laag (alleen bij leerdomeinen)

> **Sla dit hoofdstuk over** als je nieuwe project géén leerdomein is. Adaptief leren met BKT, SM-2 en IRT is een specifiek pakket dat alleen werkt als (a) je een individuele "leerling" hebt met persistente staat, (b) er objectief beoordeelbare oefeningen zijn, en (c) het doel beheersing van een corpus is. Een sportdeelname-beleidsmodel of vogelidentificatie-databank vraagt geen adaptieve laag.

Dit hoofdstuk vat de patronen samen die in Olympus zijn opgedaan. Het vervangt geen leerboek over educational data mining — het bespreekt **wanneer** je deze technieken kiest, **welke combinatie**, en **welke valkuilen** je vermijdt.

## §A — Wanneer is een adaptieve laag relevant?

Adaptief leren betekent: het systeem kiest het volgende item op basis van wat de leerling al kent. Dat is alleen zinvol als:

| Kenmerk | Adaptief loont? |
|---------|-----------------|
| Beheersings-gebaseerd doel ("je bent klaar als je X kunt") | Ja |
| Verkenningsdoel ("ik wil weten wat hier is") | Nee — gewone navigatie |
| Lange leerperiode (weken+) | Ja |
| Eenmalig assessment | Marginaal — alleen IRT voor item-selectie |
| Individuele variatie groot | Ja |
| Cohort-gebaseerd, iedereen tegelijk | Nee — gebruik gewone curriculum |
| Objectief beoordeelbaar (goed/fout, schaal 0-1) | Ja |
| Subjectief / open einde | Nee — probeer geen BKT op essays |

Stel jezelf de drie vragen:
1. Heeft een "leerling" een persistente staat die langer dan één sessie bestaat?
2. Kun je in <30 sec na een item bepalen of het correct was?
3. Is er een **eindcriterium** dat door beheersing wordt gehaald?

Drie keer ja → adaptieve laag heeft potentieel. Anders: simpeler systeem volstaat.

## §B — Drie technieken, één stack

Olympus combineert drie technieken die elk een ander deelprobleem oplossen.

### Bayesian Knowledge Tracing (BKT)

**Wat:** schat per leerling per knoop de kans dat de leerling de stof beheerst (`P(L)`, posterior mastery). Update na elke response.

**Wanneer relevant:** als je beheersing-per-onderdeel wilt bijhouden, niet alleen totaalscore.

**Vier parameters:**
- `p_init` — startkans dat de leerling het al kent
- `p_transit` — kans dat de leerling het leert van een oefening
- `p_slip` — kans dat een meester het toch fout doet
- `p_guess` — kans dat een novice het toch goed gokt

**Per knoop ofwel een set parameters,** of project-wide defaults met domein-specifieke uitzonderingen.

**Update-regel** (vereenvoudigd):
```
Na een response (correct/incorrect):
  Bayes-update P(L) gegeven slip/guess
  Vervolgens: P(L) ← P(L) + (1 - P(L)) * p_transit
```

**Beheersingsdrempel** typisch 0.85-0.95 (Olympus: 0.90).

**Olympus-implementatie:** `src/gymnasium_classica/scheduling/bkt.py`.

### SuperMemo SM-2 (spaced repetition)

**Wat:** plant wanneer een knoop opnieuw geoefend moet worden. Voorspelt vergeetkromme per leerling per knoop.

**Wanneer relevant:** als retentie over weken/maanden telt, niet alleen "kan ik het nu?"

**Per knoop bijhouden:**
- `easiness_factor` (EF) — hoe "makkelijk" deze knoop voor deze leerling is
- `interval_days` — huidige interval tot volgende review
- `repetitions` — aantal opeenvolgende correcte reviews
- `last_review` — datum

**Update-regel:**
```
Bij correct antwoord:
  repetitions += 1
  interval = berekend uit (repetitions, EF)
  EF = bijgewerkt op basis van zelf-rapportage of correctheid

Bij incorrect:
  repetitions = 0
  interval = 1
```

**Variant:** SM-2 hangt origineel aan zelf-rapportage (0-5). Je kunt EF afleiden uit response time + correctheid (Olympus' aanpak).

**Olympus-implementatie:** `src/gymnasium_classica/scheduling/sm2.py`.

### Item Response Theory (IRT)

**Wat:** schat per item hoe moeilijk en hoe discriminerend het is, zodat je items kiest die op de juiste moeilijkheid zitten voor deze leerling.

**Wanneer relevant:** als je een grote item-pool hebt (>10× je gemiddelde sessielengte) en je items niet uniform moeilijk zijn.

**Twee-parameter logistisch model:**
- `b` — moeilijkheid (waar zit het 50%-punt op de leerling-vaardigheidsschaal)
- `a` — discriminatie (hoe scherp onderscheidt dit item beheersers van niet-beheersers)

**Voor een nieuw project:** schat initiële parameters per hand of via een paar pilot-runs. Update later op basis van data.

**Wel doen:** IRT voor **item-selectie** binnen een knoop ("welk item bied ik nu aan?"). 
**Niet doen:** IRT als vervanging van BKT voor mastery-tracking; dat zijn twee verschillende modellen.

## §C — De combinatie: wie regeert wat?

In Olympus:
- **BKT** beheert mastery-state per knoop.
- **SM-2** beheert wanneer een knoop opnieuw geoefend moet worden.
- **IRT** beheert welk item binnen een knoop wordt aangeboden.
- **Een prioriteitswachtrij** weegt over alle knopen heen wat het meest urgente is om nu te oefenen.

```
Leerling start sessie van 30 minuten:
  loop tot de tijd op is:
    knoop = priority_queue.pop()  # wat is nu het meest waardevol om te doen?
    item = irt.select_item(knoop, leerling.skill_level)
    response = stel_item_voor(item)
    bkt.update(leerling, knoop, response)
    sm2.update(leerling, knoop, response)
    priority_queue.recompute(leerling)  # mastery is veranderd → herrekening
```

Laat de scheduler **niet** ad hoc beslissen. Bouw een expliciete `priority_queue` met benoembare urgency-componenten:
- vergeet-urgentie (SM-2: hoe ver is `now > last_review + interval`?)
- readiness (zijn de prerequisites beheerst?)
- pedagogische waarde (Bloom-niveau, blokkeert dit andere knopen?)
- domein-balans (niet drie naamval-items achter elkaar)

**Olympus-implementatie:** `src/gymnasium_classica/scheduling/priority.py`.

## §D — Datamodel voor de leerling

Minimale set entiteiten:

```python
class LearnerModel(BaseModel):
    user_id: UUID
    knoop_states: dict[str, KnoopState]
    session_history: list[SessionRecord]

class KnoopState(BaseModel):
    knoop_id: str
    posterior_mastery: float  # uit BKT
    easiness_factor: float    # uit SM-2
    interval_days: float
    repetitions: int
    last_review: datetime | None
    item_history: list[ItemResponse]

class ItemResponse(BaseModel):
    item_id: str
    timestamp: datetime
    correct: bool
    response_time_sec: float
    self_assessment: int | None  # SM-2 0-5, optioneel
```

Sla op in SQLite (fase 0-3) met een eenvoudig schema. Migratie naar PostgreSQL als je klanten hebt en multi-tenancy actief wordt. Niet eerder.

## §E — Diagnostische intake / placement

Een nieuwe leerling heeft geen BKT-state. Twee paden:

**Pad 1 — Cold start.** Begin met `p_init` als prior; eerste sessie traint zichzelf. Werkt prima als de eerste knopen instap-niveau zijn.

**Pad 2 — Adaptieve placement.** Voor leerlingen met voorkennis: doorloop een korte test (15-20 items) die door de graph propageert. Topologische strategie: vraag iets midden in de graph, propageer beheersing/niet-beheersing vooruit en achteruit, kies volgende item op informatiewinst.

Olympus heeft beide; pad 2 is `src/gymnasium_classica/diagnostic/placement.py`. Voor nieuwe projecten: start met cold start. Bouw placement pas als gebruikers klagen dat ze "begin van het begin" moeten doen.

## §F — Oefeningen (items)

Vijf oefentypen die in Olympus voldoende blijken:

1. **Herkenning** — herkennen van vorm/concept ("welke naamval is dit?")
2. **Productie** — produceren van vorm ("vervoeg dit werkwoord")
3. **Analyse** — ontleden ("ontleed deze zin")
4. **Synthese** — combineren ("vertaal deze zin")
5. **Contextueel** — toepassing in passage

**Per item minimaal:**

```python
class Item(BaseModel):
    id: str
    knoop_ids: list[str]            # over welke knopen gaat dit
    type: ItemType                  # zie boven
    moeilijkheid_initieel: float    # IRT b
    discriminatie_initieel: float   # IRT a
    verwachte_tijd_sec: int
    stimulus: str | dict            # tekst, of structured (audio, image)
    antwoord: str | list[str]       # exact match of lijst van varianten
    feedback: str
    bron: ItemSource                # handmatig, llm-gegenereerd, authentiek
```

**Zes-aandachtspunten:**
1. Items koppelen aan **één primaire knoop** plus zwakke koppelingen aan medeknopen.
2. Antwoord-matching: exact, normalized (lowercase, trim), of regex-tolerant. Beslis vooraf.
3. Feedback **altijd**: niet alleen "fout", maar uitleg waarom.
4. `verwachte_tijd_sec` voor scheduling van 30-min-sessies.
5. `bron` voor auditbaarheid, vooral bij LLM-gegenereerde items.
6. Items in JSON onder de knoop, of in losse `data/items/`-bestanden bij hoge volumes.

## §G — Niet-interferentie en sessie-opbouw

Twee technieken die in Olympus achteraf onmisbaar bleken:

### Non-interference

Twee knopen die semantisch dicht bij elkaar liggen (bv. twee declinaties met overlappende uitgangen) **niet** direct na elkaar oefenen. Werkt verwarring in de hand. Implementatie: clusterlabels op knopen, scheduler kiest niet twee uit hetzelfde cluster binnen N items.

`src/gymnasium_classica/scheduling/non_interference.py`.

### Sessie-fasering

30-minuten-sessie in 4 fasen:
1. **Warmup** (3-5 min): bekende, lichte items. Activeert geheugen.
2. **Nieuwe stof** (10-15 min): introductie van knopen die net beschikbaar zijn (prerequisites groen).
3. **Verdieping** (8-10 min): herhaling van nog-niet-beheerste knopen, hogere moeilijkheid.
4. **Cooldown** (2-3 min): items met hoge succeskans, gevoel van afsluiting.

Niet een hard schema; weight op urgency-componenten verandert per fase.

## §H — Wanneer je dit alles **niet** wilt

Drie domeinen waar adaptief leren met BKT/SM-2/IRT overkill is:

- **Verkenningstool / encyclopedie.** Geen progressie-doel. Gebruik gewone navigatie + eventueel bookmarks.
- **Eenmalige toets.** Niet langdurig. Gewone IRT-gebaseerde computer-adaptive testing zonder BKT/SM-2.
- **Coaching met menselijke begeleiding.** Trainer beslist; systeem is alleen tracking.

In zulke gevallen: skip dit hoofdstuk, en behoud alleen de graph-laag uit hoofdstuk 02.

## §I — Stappen om de adaptieve laag op te zetten

Sprint 1 (1 dag): datamodel.
- Pydantic `LearnerModel`, `KnoopState`, `ItemResponse`, `SessionRecord`.
- SQLite-schema + repository-functies.
- Tests: round-trip, persistence.

Sprint 2 (1 dag): BKT.
- `bkt.py` met update-functie + tests met handgerekende voorbeelden.
- Defaults: `p_init=0.1, p_transit=0.15, p_slip=0.1, p_guess=0.2` als startwaardes.

Sprint 3 (1 dag): SM-2.
- `sm2.py` met update-functie + tests.
- Defaults: SuperMemo's originele waardes.

Sprint 4 (1-2 dagen): scheduler.
- `priority.py` met urgency-berekening per knoop.
- `session.py` met sessie-fasering.
- End-to-end test: simuleer een leerling met scripted antwoorden, controleer dat de scheduler aanbiedt wat verwacht.

Sprint 5 (later): IRT-item-selectie binnen een knoop.

Sprint 6 (later): non-interference, placement, fijnafstemming.

Bouw eerst sprint 1-4 en gebruik het op een speelgoeddataset. Pas als dat werkt: sprint 5+.

## Vragen voor je nieuwe project

1. Heeft het echt een individuele leerling met persistente staat? (zo nee → skip dit hoofdstuk)
2. Wat is de eindcriterium-definitie? Wanneer is een leerling "klaar"?
3. Welke BKT-defaults heb je intuïtief? (begin daarmee, kalibreer later)
4. Heb je een grote item-pool (>1000 items, >10x sessielengte)? Zo nee, IRT eventueel uitstellen.
5. Is response-time betekenisvol in je domein? (Olympus: ja, voor SM-2 EF. Andere domeinen: niet altijd.)
6. Hoe groot is je verwachte sessieduur? Welke fase-verdeling past?
7. Heb je non-interference nodig (zijn er semantisch dichtbij liggende knopen)?

Beantwoord, en plan op basis daarvan welke sprints je daadwerkelijk doet. Niet elke sprint hoeft als de eerdere nog rendement opleveren.
