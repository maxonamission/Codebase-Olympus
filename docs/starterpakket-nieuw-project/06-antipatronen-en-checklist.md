# 06 — Antipatronen en finale checklist

Dit hoofdstuk bevat de fouten die in Codebase-Olympus en aanverwante projecten (Graaf Zeppelin) achteraf zichtbaar zijn geworden. Sommige zijn gemaakt en gerepareerd; andere zijn vermeden door tijdig pas op de plaats te maken. Beide categorieën zijn even nuttig om vooraf te kennen.

## §A — Architectuur-antipatronen

### 1. Verkeerd archetype kiezen of niet kiezen

**Symptoom:** je begint te bouwen "een graph-systeem" zonder vooraf te bepalen of je archetype A (persoonlijke beheersing) of archetype B (domeinmodel voor hypothesevorming) volgt. Drie weken later merk je dat je BKT in elkaar aan het knippen bent voor een use case waar geen leerling bestaat — of je bent een simulatie-engine aan het bouwen voor een use case waar simpele beheersingstracking voldoende was.

**Olympus-voorbeeld:** geen — Olympus had archetype A vanaf de eerste alinea van de briefing helder.
**Zeppelin-voorbeeld:** Zeppelin's schema beloofde feedback-edges (archetype B-eigenschap) terwijl de simulatiecode globale acycliciteit afdwong (archetype A-aanname). Dat leverde een drie-weken-debat over "is dit nu een DAG of niet?" op.

**Vermijden:** in dag 1 van je BRIEFING één alinea: "dit is een archetype-X-project want …". Twijfel? Lees `README.md` §"Twee projectarchetypes" en maak een knoop door.

### 2. DAG-dogma op een causaal netwerk

**Symptoom:** je hebt een causaal of beleidsmodel waarin "meer X → meer Y → meer X" een legitieme dynamiek is, maar je validatie roept `nx.is_directed_acyclic_graph(graph)` aan over de hele graph en faalt op elke feedback-loop.

**Vermijden:** typeer je edges en filter de cyclus-check per type. Zie `graph-methodology.md` §5 en de Zeppelin-GZ-01-story als concrete uitwerking. Dit is **archetype B's** belangrijkste valkuil.

### 3. Dead-field anti-pattern

**Symptoom:** je schema bevat een veld (`time_lag`, `confidence`, `source`, …) dat je opslaat maar nergens gebruikt. Reviewers en toekomstige jezelf gaan ervan uit dat het veld iets doet; bij debugging blijkt dat niet zo.

**Vermijden:** ofwel activeer het veld in je code, ofwel schrap het uit het schema. Geen tussenweg. Bij elke nieuwe veld-toevoeging: schrijf eerst de test die het veld in werking ziet, daarna pas het schema-veld.

**Archetype B specifiek:** dit gebeurt vooral met dynamiek-velden (`time_lag`, `cycle_time`, `polarity`). Beslis vooraf of je domein dynamisch is. Zie `graph-methodology.md` Appendix.

### 4. Persistente JSON met rich text

**Symptoom:** je `data/graph/*.json` bevat markdown-snippets, escape-sequences, ingebedde HTML, of meerregelige uitleg. Diff's worden onleesbaar; loader-snelheid daalt; reviewers raken in de war over "is dit structuurdata of inhoud?".

**Vermijden:** strikt scheiden van structuur (JSON) en inhoud (markdown via `content_ref`). Zie `graph-methodology.md` §3 en hoofdstuk 02 §D in dit pakket.

### 5. Eén-bestand-met-alles

**Symptoom:** alle 800 knopen in één `data/graph/everything.json`. Reviewers willen niet meer mergen want elke conflict raakt het hele bestand. Editors openen het bestand traag.

**Vermijden:** loader die directories aankan + cross-file edges. Splits per coherent subdomein. Zie hoofdstuk 02 §D in dit pakket.

### 6. ID-schema migreren als datacorpus al groeit

**Symptoom:** je hebt 200 knopen met opake IDs (`N001`, `K042`) en realiseert je dat hiërarchische IDs leesbaarder waren. Migratie raakt elke `source`/`target`-referentie, elke externe documentatie, elke gedeelde rapportage.

**Vermijden:** ID-schema vóór de eerste 50 knopen vastleggen. Twee dagen denken vooraf bespaart twee weken migreren later. Zie hoofdstuk 02 §C.

**Mitigatie als het al gebeurd is:** schrijf een idempotent migratiescript, lever een `old_to_new_ids.json` mee, voer pas door als alle externe consumenten ervan op de hoogte zijn.

**Patroon voor het migratiescript** (idempotent + zelf-validerend, naar het patroon `_scripts/check_*.py`):

```python
def migrate(data: dict) -> tuple[dict, dict[str, str]]:
    """Return (migrated_data, old_to_new_id_mapping). Idempotent."""
    mapping = build_mapping(data)              # bestaande IDs → nieuwe IDs
    if all(old == new for old, new in mapping.items()):
        return data, mapping                   # niets te doen, tweede run = no-op
    migrated = apply_mapping(data, mapping)
    validate_referential_integrity(migrated)   # geen dangling refs
    return migrated, mapping
```

Drie eigenschappen die het script altijd heeft: (1) idempotent (tweede run produceert geen wijzigingen), (2) referentiële integriteit gecheckt vóór wegschrijven, (3) mapping-bestand als audit-trail. Zonder een van de drie krijg je over zes maanden niemand meer die het durft te draaien.

## §B — Werkwijze-antipatronen

### 7. Bouwen-zonder-storying

**Symptoom:** je begint codewerk zonder een story. Tijdens het werk groeit de scope, breidt de tijd uit, en je herinnert je een week later niet meer wat je oorspronkelijk wilde.

**Vermijden:** elke wijziging die langer duurt dan 30 minuten begint met een story in `stories/doing/`. Zie hoofdstuk 04 §C.

### 8. Grote commits

**Symptoom:** je commit één keer per sessie van vier uur. Bij een conflict moet je dat hele blok terugdraaien of micro-mergen. Onmogelijk om "wanneer ging dit kapot?" te beantwoorden via `git bisect`.

**Vermijden:** principe 1 uit hoofdstuk 01 — klein leveren, vaak committen. Maximaal ~150 regels per commit als richtlijn.

### 9. Aannames niet markeren

**Symptoom:** in je BRIEFING staat: "leerlingen besteden gemiddeld 30 min per dag" alsof het feit is. Drie maanden later beslis je iets anders op basis van die "feit". Je weet niet meer of het cijfer kwam uit onderzoek, gebruikersinterviews, of buikgevoel.

**Vermijden:** principe 4 uit hoofdstuk 01 — bij elke claim ofwel een bron, ofwel `[aanname]`. In `ONTWERPKEUZES`: per beslissing een rationale-sectie met expliciete onzekerheden.

### 10. Te brede sessies

**Symptoom:** één Claude-sessie probeert "drie stories te doen". De context vult, hooks worden trager, idle timeouts beginnen te vallen, en de sessie crasht halverwege story 2.

**Vermijden:** één story per sessie. Commit en sluit af. Nieuwe sessie voor de volgende story. Zie principe 7 in hoofdstuk 01.

### 11. CI-falen negeren

**Symptoom:** je merge een PR ondanks rode CI met "fix het later wel". Een week later draaien er drie projecten met onbekende rode CI-staten.

**Vermijden:** `main` heeft branch protection. Geen merge zonder groene CI. Hard. Frictie in week 1 is rust in maand 3.

### 12. Voortijdige extractie naar template

**Symptoom:** na één succesvol project bouw je een `cookiecutter`- of `copier`-template. In je tweede project blijkt 60% van de template aanpassingen te vereisen omdat de aannames niet domein-onafhankelijk waren.

**Vermijden:** wacht tot na het tweede succesvolle project. Pas dan zie je welke patronen *echt* gedeeld zijn. Zie `ontwikkelstraat-uitleg.md` §"Valkuilen om te vermijden".

## §C — Domein-antipatronen

### 13. Graph-vóór-domein

**Symptoom:** je bouwt loader, validatie, scheduling en visualisatie volledig uit voor je 50 echte knopen hebt. Dan blijken je aannames over de structuur niet te kloppen tegen echte inhoud.

**Vermijden:** week 1-2 van de bootstrap-roadmap (hoofdstuk 05) — bouw eerst de minimale graph-laag, voer met de hand 30-50 knopen in, dan pas de uitgebreide validatie.

### 14. Edge-typen bedenken na het feit

**Symptoom:** je begint met één type edge ("dit hangt samen met dat"). Halverwege ontdek je dat sommige relaties asymmetrisch zijn (X is voorwaarde voor Y) en andere symmetrisch (X verwijst naar Y). Te laat om alle edges te hertypen.

**Vermijden:** in dag 1 minstens drie edge-types definiëren, ook als sommigen leeg blijven. Zie `graph-methodology.md` §1 voor de discriminated-union-conventie.

### 15. Onboarding-laag vergeten

**Symptoom:** je systeem werkt prima voor mensen die al wat van het domein weten, maar nieuwe gebruikers stuiten op een muur van prerequisites die nergens is uitgelegd.

**Vermijden:** in je ONTWERPKEUZES vraag 5 "is er een verplichte instap-subgraph?" expliciet beantwoorden. Zo ja: bouw die als eerste epic. Olympus' Grieks-alfabet-subgraph (40 knopen) is het schoolvoorbeeld.

**Archetype B specifiek:** ook causale beleidsmodellen hebben een "context-onboarding"-stap nodig — een kleine demo of tutorial-scenario dat de gebruiker laat zien hoe het model werkt voor ze het op echte cases inzetten.

### 16. Pensum / contextlaag verwarren met kerncorpus

**Symptoom:** je mengt jaarlijks wisselende inhoud (Olympus' pensum, Zeppelin's actuele cases) met je vaste graph. Bij update raken inhoud en structuur beide.

**Vermijden:** modelleer wisselende inhoud als **overlay** — een aparte set bestanden in `data/{thema}/{jaar}/` die de vaste graph aanvult, niet vervangt. Zie Olympus-keuze "Pensum als jaarlijks wisselende module".

## §D — Antipatronen specifiek voor archetype A (persoonlijke beheersing)

### 17. BKT zonder beheersingsdrempel

**Symptoom:** je BKT-update werkt, maar je hebt geen expliciete drempel waarboven een knoop "beheerst" heet. Resultaat: leerlingen oefenen oneindig door, of geven op omdat het systeem nooit een afsluiting biedt.

**Vermijden:** in ONTWERPKEUZES vastleggen wat de drempel is (Olympus: 0.90 posterior). Zichtbaar maken in de UI.

### 18. SM-2 zonder kalibratie

**Symptoom:** je gebruikt SuperMemo's originele EF-update-formules zonder ze tegen je domein te toetsen. Voor een domein met snel verval (volledige paradigma's) zijn de defaults te ruim; voor langzaam verval (cultuurkennis) te krap.

**Vermijden:** start met defaults, log alle reviews en self-assessments, kalibreer na 1000 datapunten. Zonder kalibratie heb je een gevoel van adaptiviteit zonder de winst.

### 19. Items zonder feedback

**Symptoom:** items hebben een stimulus en een correct antwoord, maar geen uitleg. Leerlingen die het fout doen weten niet waarom.

**Vermijden:** elk item heeft een verplicht `feedback`-veld in het Pydantic-model. Validatie blokkeert items zonder feedback bij data-loading. Zie hoofdstuk 03 §F.

### 20. Producent zonder receptief eerst

**Symptoom:** je vraagt productieve oefeningen ("vertaal deze zin naar Latijn") aan leerlingen die de receptieve vaardigheid ("herken Latijnse vorm") nog niet beheersen. Frustratie en demotivatie.

**Vermijden:** productieve items komen pas in de scheduler beschikbaar als de gerelateerde receptieve knoop boven de drempel zit. Zie Olympus-keuze 5.

## §E — Antipatronen specifiek voor archetype B (domeinmodel)

### 21. Globale DAG-acycliciteit forceren

Zie antipatroon 2 hierboven — het is voor archetype B het *enkele meest voorkomende* probleem.

### 22. Statische analyse voor dynamische vragen

**Symptoom:** een gebruiker vraagt "wat als ik investering in groep A verdrievoudig — hoe ziet groep B er over vijf jaar uit?". Je systeem antwoordt met pad-analyse ("groep A en groep B hangen samen via knopen X, Y, Z"). Dat is een ander soort antwoord.

**Vermijden:** scheid structurele analyse (welke factoren hangen samen?) van dynamische simulatie (hoe verandert factor X over tijd?). Bouw beide als aparte componenten of beslis bewust dat je alleen statisch werkt. Zie `graph-methodology.md` Appendix.

### 23. Sliders zonder rationale

**Symptoom:** je beleidsmodel heeft acht sliders. Geen enkele is gedocumenteerd qua eenheid, range, of literatuur-onderbouwing. Gebruikers zetten ze willekeurig en interpreteren de uitkomst als "wat het model zegt".

**Vermijden:** elke slider heeft een toelichting (eenheid, betekenisvolle minimale en maximale waardes, literatuur-onderbouwing voor de defaults). Onzekerheidsbereik tonen in plaats van puntwaardes waar mogelijk.

### 24. Casuïstiek niet meegeleverd

**Symptoom:** je hebt een rijk model, maar geen documenteerde voorbeeldcases ("zo werkt het voor scenario X"). Eerste gebruikers staan voor een leeg model en weten niet hoe ze moeten beginnen.

**Vermijden:** lever bij elke release minstens drie scenarios mee — beschrijving, ingestelde waardes, expert-verwachte uitkomst, daadwerkelijke modeluitkomst, interpretatie-discussie. Dit hoort in `docs/scenarios/`.

### 25. Validation zonder externe expertise

**Symptoom:** je model "werkt" omdat de uitkomst plausibel is voor jou. Een domeinexpert die het model voor het eerst ziet, vindt drie ernstige inconsistenties.

**Vermijden:** plan minstens één externe-expertise-sessie vóórdat je het model uitrolt. Documenteer de feedback in een review-blok in je `BRIEFING`.

## §F — Finale checklist

Loop deze door **vóór je je eerste echte gebruiker (of pilotgroep) toelaat**. Acht "ja's" is goed; minder dan zes is een rode vlag.

### Werkwijze (hoofdstuk 01)

- [ ] BRIEFING-document geschreven en up-to-date
- [ ] ONTWERPKEUZES-document met minstens 5 keuzes uitgewerkt (vraag, beslissing, rationale, implicaties)
- [ ] Documentatietaal en codetaal expliciet vastgelegd
- [ ] Stories worden geschreven vóór codework
- [ ] Aannames worden gemarkeerd in alle docs

### Graph-laag (hoofdstuk 02)

- [ ] Archetype expliciet gekozen (A, B, of mengvorm) en in BRIEFING genoemd
- [ ] Pydantic-modellen voor Node, Edge, GraphData met `frozen=True` waar zinvol
- [ ] ID-schema vastgelegd en `validate_id` + `parse_id` met tests
- [ ] Lean JSON + content-markdown gescheiden via `content_ref`
- [ ] Loader werkt op directory + cross-file edges
- [ ] Validatie-catalogus met minstens cyclus, orphan, duplicate, dangling, edge-weight, ID-format
- [ ] Cyclus-detectie per edge-type (geen globale)
- [ ] Smoke + round-trip + invariant-based tests

### Adaptieve laag (hoofdstuk 03 — alleen archetype A)

- [ ] Datamodel learner gepersisteerd (SQLite of equivalent)
- [ ] BKT geïmplementeerd met handgerekende tests
- [ ] SM-2 geïmplementeerd met handgerekende tests
- [ ] Scheduler met benoemde urgency-componenten
- [ ] Beheersingsdrempel expliciet vastgelegd
- [ ] Items hebben verplichte feedback-velden

### Domeinmodel-laag (hoofdstuk 02 §I + Zeppelin-actieplan — alleen archetype B)

- [ ] Edge-typering met expliciete acyclische set
- [ ] Edge-velden alleen aanwezig als ze door code gebruikt worden (geen dead fields)
- [ ] Propagatie- of simulatie-functie met tests
- [ ] Statische vs. dynamische analyse expliciet gescheiden
- [ ] Sliders/parameters met eenheden en literatuur-onderbouwing
- [ ] Minstens drie voorbeeldscenario's gedocumenteerd

### Evidence-traceability (alle archetypes met literatuur- of bronclaims)

- [ ] Sliders, evidence-claims en bron-velden hebben een `ref_id` naar een gedeeld literatuurregister (`data/literatuur.json` of equivalent)
- [ ] Reference-integrity-invariant draait in `validation.py` (zie hoofdstuk 02 §F invariant 9)
- [ ] Literatuur-audit-script in CI; rotte refs blokkeren de merge

### Ontwikkelstraat (hoofdstuk 04)

- [ ] Pre-commit hooks actief en groen
- [ ] CI groen op `main`; branch protection ingesteld
- [ ] Claude Code hooks (PostToolUse + Stop) ingericht
- [ ] PR-template in repo
- [ ] Story-status-check draait in pre-commit en CI

### Stories en epics (hoofdstuk 04 §C)

- [ ] `stories/`-structuur met `backlog/`, `doing/`, `done/` + `EPICS.md`
- [ ] Maximaal 3 stories tegelijk in `doing/`
- [ ] Stories in `done/` hebben alle AC's afgevinkt

### Domeinvalidatie

- [ ] Externe expertise-sessie heeft plaatsgevonden vóór pilot (of expliciete reden geboekt waarom niet)
- [ ] Onboarding-laag aanwezig en getest
- [ ] Pensum/scenario-overlay (jaarlijks of cases-gestuurd) gescheiden van vaste graph
- [ ] Privacy-implicaties (AVG, minderjarigen) afgewogen indien van toepassing

## §G — Symptomen die een mid-project review rechtvaardigen

Als je een van deze tegenkomt, plan een dag voor reflectie + eventueel refactor in:

- Je laatste tien commits zijn meer dan 50% bug-fixes op recent gewijzigde code → ontwerp staat onder druk.
- Je AI-sessies crashen vaker dan eens per week op idle timeout → te brede stories of te veel tool-output.
- Je `data/graph/` heeft een bestand dat door meerdere stories tegelijk wordt gewijzigd → splitsing nodig.
- Je merkt dat je BRIEFING niet meer klopt met wat je bouwt → BRIEFING bijwerken (niet de bouw veranderen).
- Je hebt voor de derde keer hetzelfde soort bug — patroon zit diep, refactor nu.

## §H — Lessen die in deze checklist niet passen

Drie meta-lessen die niet als checkpunt te formuleren zijn maar wel cruciaal:

1. **Wachten met optimaliseren.** Performance-tuning is bijna nooit nodig in de eerste 12 maanden van een graph-project op deze schaal. Sla 1000 sessies op, kijk dan pas of iets traag is.
2. **Extern bekijken.** Iemand die het project niet heeft gebouwd kan in twee uur drie problemen zien die jij in twee maanden niet hebt gemerkt. Plan dat.
3. **Stoppen met polijsten.** Op een gegeven moment is het systeem af genoeg om gebruikers ermee te laten werken. Polijsten zonder gebruikers betekent polijsten op aannames.

## Slot

Een nieuw project starten met deze methodologie kost je naar schatting drie weken extra werk in maand 1 vergeleken met "gewoon beginnen en zien". Die drie weken haal je terug in maand 4-6 omdat je dan geen weeklange refactors hoeft te doen op fundamentele beslissingen. Het is geen zekerheid; het is een gunstige weddenschap.

De grootste winst zit níét in techniek of architectuur. Hij zit in **structurele zelfdiscipline**: je dwingt jezelf om vóór je bouwt na te denken, en je bouwt het systeem zo dat ook je toekomstige zelf (of een opvolger) gedwongen wordt na te denken vóór ingrijpen. Dat is wat al deze conventies bij elkaar opleveren — niet de losse regels, maar het patroon erachter.

Tot zover het pakket. Veel succes.
