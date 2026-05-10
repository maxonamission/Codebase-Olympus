# 05 — Bootstrap eerste maand + ontwerpkeuzes-template

Dit hoofdstuk geeft je twee dingen:
1. **Een ontwerpkeuzes-sjabloon** zodat je de fundamentele keuzes vóór de implementatie expliciet maakt.
2. **Een week-voor-week roadmap** voor je eerste maand, gebaseerd op wat in Olympus daadwerkelijk goed werkte.

## §1 — Het BRIEFING-document

Voor je begint te bouwen schrijf je een briefing. Deze leg je in `docs/BRIEFING_{PROJECT}.md`. Doel: vastleggen waar het project over gaat, voor wie, en hoe je succes meet — voordat technische beslissingen kleuren wat je wilt.

### Sjabloon

```markdown
# Project Briefing: {Naam}

**Versie:** 0.1
**Datum:** {datum}
**Auteur:** {wie}

## 1. Projectvisie

### 1.1 Kernidee
{1-2 alinea's: wat doet dit systeem, voor wie, wat lost het op?}

### 1.2 Doelgroepen
- **Primair:** {…}
- **Secundair:** {…}
- **Tertiair:** {…}

### 1.3 Ambitie en bewijs
{Waarom is je doelstelling realistisch? Onderbouw met concrete bronnen of duidelijk gemarkeerde aannames.}

## 2. Doelstellingen en eindtermen

### 2.1 Formeel kader
{Welke standaarden, eindtermen, certificaten, externe validatie?}

### 2.2 Concrete vaardigheids- of resultaatdoelen
{Wat moet de gebruiker uiteindelijk kunnen / weten / doen?}

### 2.3 Scope
{Wat valt erbinnen, wat erbuiten?}

## 3. Ontwerpkeuzes (voorlopig — definitief in ONTWERPKEUZES-document)

{Per fundamentele keuze: 2-3 alinea's analyse, en een voorlopige voorkeur.}

## 4. Architectuur (high-level)

{Welke onderdelen? Welke datalagen? Welke processen?}

## 5. Roadmap

| Fase | Doel | Tijd |
|------|------|------|
| 0 | Fundament | 1-2 weken |
| 1 | Knowledge graph MVP | 4-8 weken |
| 2 | … | … |

## 6. Open vragen

{Vragen die nog beslist moeten worden, met voorlopige meningen.}
```

Houd dit op 5-15 pagina's. Langer wordt niet gelezen.

## §2 — Het ONTWERPKEUZES-document

Vervolgens schrijf je `docs/ONTWERPKEUZES_{PROJECT}.md` waarin je per fundamentele keuze het volgende vastlegt:

### Sjabloon per keuze

```markdown
## Keuze {N}: {korte titel}

### Vraag
{Welke vraag staat hier centraal?}

### Beslissing
{Concreet: wat hebben we besloten? Eén alinea.}

### Onderbouwing
{Waarom deze keuze? Welk bewijs of welke afweging? 1-3 alinea's.}

### Architecturale implicaties

**A{N}.1** {Eerste concrete technische gevolg.}
**A{N}.2** {Tweede.}
**A{N}.3** {Etc.}
```

### Welke keuzes leg je minimaal vast?

Voor elk graph-gedreven project, beantwoord:

1. **Validatiepad / extern referentiekader.** Welk bestaand kader (eindterm, standaard, taxonomie) is leidend voor je content?
2. **Graph-vorm.** DAG / cyclisch / boom / bipartiet? Zie hoofdstuk 02 §A.
3. **Edge-typering.** Welke types, welke acyclisch?
4. **Scope.** Eerste-maand-scope, eerste-jaar-scope, einddoel.
5. **Onboarding-laag.** Heb je een verplichte instap-subgraph (zoals het Griekse alfabet)?
6. **Adaptief leren ja/nee.** Zo ja, welke combinatie van BKT/SM-2/IRT?
7. **Productieve / receptieve oefeningen** (alleen leerdomeinen).
8. **LLM-rol.** Generatie van items? Conversationele interface? Geen?
9. **Businessmodel.** Solo-tool, SaaS, open source, intern?
10. **Privacy en compliance.** Persoonlijke data? Minderjarigen? AVG-implicaties?
11. **Inputmethoden.** Hebben gebruikers iets bijzonders nodig (toetsenbord-extensies, audio-input)?
12. **Interfacetaal.** Welke taal voor de UI, welke voor terminologie?

Werk de keuzes uit waar ze relevant zijn voor jouw domein. In een vogelidentificatie-project zal "productieve oefeningen" geen rol spelen; in een huisartsenrichtlijn-project juist wel "scope" en "validatiepad".

Bij elke keuze noteer je expliciet de architecturale implicaties — dat is het stuk dat naar je code-implementatie doorklikt. Zie Olympus' `docs/ONTWERPKEUZES_GYMNASIUM_CLASSICA.md` voor 10 uitgewerkte voorbeelden.

## §3 — De eerste maand (week-voor-week roadmap)

Onderstaand een sequentie die in Olympus en Zeppelin als kritisch pad bleek. Pas aan op je domein, maar volg de **volgorde** — ze beschermt je tegen de duurste vergissingen.

### Week 1 — Fundament

**Doel einde week:** je kunt een lege project-skelet draaien, met alle kwaliteitscontroles in werking.

Dag 1
- [ ] Repo aanmaken, eerste commit met `pyproject.toml`, `.gitignore`, `README.md`-skelet, `CLAUDE.md`-skelet.
- [ ] Python 3.11, uv venv, `uv pip install -e ".[dev]"`.
- [ ] `pytest`, `ruff`, `mypy` allemaal eens handmatig draaien op leeg project.

Dag 2
- [ ] BRIEFING-document v0.1 (zie §1 hierboven).
- [ ] Beslissingen-vragen uit hoofdstuk 01 §"Vragen voor je nieuwe project" beantwoorden op papier.
- [ ] ONTWERPKEUZES-document v0.1 met minstens 5 belangrijkste keuzes (zie §2).

Dag 3
- [ ] `.pre-commit-config.yaml` met basis-hooks (ruff, mypy, eof, json/yaml/toml-check).
- [ ] `uv run pre-commit install`; één testcommit forceren tot het werkt.
- [ ] `.github/workflows/ci.yml` met ruff + mypy + pytest. Push, kijken of het groen draait.

Dag 4
- [ ] `.claude/settings.json` + hooks-scripts (PostToolUse + Stop). Testen.
- [ ] PR-template, issue-template als gewenst.
- [ ] `stories/`-structuur met `EPICS.md` v0.1.

Dag 5
- [ ] Eerste epic uitschrijven in `EPICS.md` met 3-5 stories in `backlog/`.
- [ ] CLAUDE.md afmaken (kopieer uit Olympus, vul jouw projectinfo in).
- [ ] Status: leeg project met ontwikkelstraat erin, klaar om te bouwen.

### Week 2 — Graph-laag MVP

**Doel einde week:** je kunt 50 echte knopen laden, valideren en visualiseren.

Dag 6
- [ ] Story `B0-01: Pydantic-modellen voor Node, Edge, GraphData`. Schrijf models, geen logic.
- [ ] StrEnums voor types vastleggen.
- [ ] Tests: model-validatie van Pydantic.

Dag 7
- [ ] Story `B0-02: ID-schema`. Zie hoofdstuk 02 §C.
- [ ] `validate_id`, `parse_id` + tests.
- [ ] `docs/id-schema.md` invullen.

Dag 8
- [ ] Story `B0-03: Loader (single-file)`. Lees JSON, parse via Pydantic, bouw `nx.DiGraph`.
- [ ] Smoke-tests: empty file, malformed JSON, duplicate ID, dangling edge.

Dag 9
- [ ] Story `B0-04: PoC-data`. Vul met de hand 30-50 knopen + 50-80 edges in een JSON-bestand. Géén script, met de hand. Dit is je echte sanity-test op je eigen ID-schema en types.
- [ ] Loader op je PoC-data. Eerste plotje (Graphviz `dot`-export).

Dag 10
- [ ] Story `B0-05: Validatie-catalogus`. Cycle-detectie per edge-type, orphan, connectivity, edge-weight, ID-format.
- [ ] `scripts/validate_graph.py`.
- [ ] Hoek de validatie aan in pre-commit + CI.

### Week 3 — Eerste content + uitbreiding

**Doel einde week:** je hebt 100-200 knopen, content-markdowns voor de helft, en een werkende `data/`-pipeline.

Dag 11-12
- [ ] Story `A1-01: Eerste echte content-blok`. Bijvoorbeeld 20 knopen rond één centraal thema.
- [ ] Loader naar directory-mode (multiple JSON files).
- [ ] Cross-file edges valideren.

Dag 13
- [ ] Story `B0-06: content_ref`. Velden in Pydantic, content-validatie in catalogus, `data/content/{ID}.md` bestanden voor de eerste 20 knopen.

Dag 14
- [ ] Story `B0-07: Stats- en export-script`. `scripts/export_graph_stats.py` met knooptelling, edge-typeverdeling, topologische diepte. Geeft je grip op groei.

Dag 15
- [ ] Buffer / refactor / bugjes. Belangrijk: gebruik dag 15 níet om aan een tweede onderwerp te beginnen. Stabiliseer wat er is.
- [ ] **Stop-criterium expliciet:** als de loader, de invariant-catalogus, of de PoC-data nog niet stabiel zijn, ga níet door naar week 3. Buffer-tijd glijdt anders ongemerkt in scope-uitbreiding. Liever een dag uitloop op week 2 dan een wankel fundament onder weken aan content.

### Week 4 — Eerste bovenliggende laag (kies je archetype)

Vanaf hier verschilt de roadmap per archetype (zie README §"Twee projectarchetypes"). Kies vóór week 4 expliciet welk pad je volgt.

#### Pad A — Archetype "persoonlijke beheersing" (Olympus-stijl)

Dag 16-17
- [ ] Story `LM-01: Datamodel learner`. SQLite-schema + Pydantic-modellen. Round-trip-tests.
- [ ] Eenvoudige CLI om een mock-leerling te creëren en items te tonen.

Dag 18
- [ ] Story `LM-02: BKT update`. Implementeer + handgerekende tests.

Dag 19
- [ ] Story `LM-03: SM-2 update`. Implementeer + tests.

Dag 20
- [ ] Story `LM-04: Eerste minimal-scheduler`. Topologische volgorde + readiness-check. Geen IRT, geen non-interference, geen fasen — alleen "wat is de eerstvolgende knoop met groene prerequisites?"
- [ ] End-to-end: leerling start, krijgt 10 items aangeboden, BKT en SM-2 updaten meebewegend.

#### Pad B — Archetype "domeinmodel voor hypothesevorming" (Zeppelin-stijl)

Dag 16-17
- [ ] Story `SIM-01: Edge-velden voor causale propagatie`. Voeg op je edge-model de domein-relevante velden toe: `polarity` (versterkend/dempend), `strength`, en — *alleen als je domein dynamisch is en je dat ook gaat gebruiken* — `time_lag` of `cycle_time`.
- [ ] **Belangrijke discipline:** voer geen velden in die je code niet gebruikt. Het "dead-field anti-pattern" (zie `voor-graaf-zeppelin/actieplan.md` GZ-03) is bij dit archetype de grootste valkuil.
- [ ] Pas je validatie-catalogus aan zodat cycle-detectie alleen draait op edge-types die acyclisch *moeten* zijn. Globale DAG-check is hier fout.

Dag 18
- [ ] Story `SIM-02: Eerste propagatie-functie`. Gegeven een knoop en een interventie-waarde, propageer naar verbonden knopen via je edge-curve (lineair, dempend, omgekeerd-U — wat je domein vraagt). Niet eerst tijd-iteratief — eerst één-staps.
- [ ] Tests: triviale lineaire keten geeft verwachte uitkomsten; kruising van versterkend en dempend werkt.

Dag 19
- [ ] Story `SIM-03: Scenario-laag`. Een scenario is: "verander knoop X met waarde V; toon impact op alle andere knopen". Implementeer als pure functie; geen UI nodig.
- [ ] Eerste case: documenteer drie cases uit jouw domein die je vooraf weet (expert-intuïtie) en check of je propagatie ze reproduceert.

Dag 20
- [ ] Story `SIM-04: Tijd-iteratie ja/nee`. Op basis van wat je in dag 18 hebt geleerd: beslis of je `time_lag`-iteratie inbouwt of niet. Beide zijn legitiem — onbeslist laten is dat niet (zie ook GZ-03 in het Zeppelin-actieplan voor pad A vs. B).
- [ ] End-to-end: een gebruiker geeft een interventie op, krijgt een scenario-uitvoer terug. CLI is genoeg; geen frontend.

#### Pad C — Archetype "descriptief netwerk" (geen leerling, geen simulatie)

Bij projecten zoals citatiekaart, organisatieoverzicht, bibliografie of glossarium-met-relaties: gebruik week 4 om je content-pipeline op te schalen — meer JSON-bestanden, meer content-markdowns, meer cross-file edges. Bouw een eerste exportscript dat je netwerk in een formaat zet dat anderen kunnen lezen (Cytoscape-JSON, GEXF, of statisch SVG via Graphviz).

### Voorbij maand 1

Vanaf hier is je projectarchitectuur in werking; het werk wordt **inhoud** in plaats van **infrastructuur**. Splits het in epics:
- Content-epic per coherent subdomein (bv. per hoofdstuk, per regio, per thema)
- Engine-epic per geavanceerde scheduler-feature (IRT, non-interference, sessie-fasering)
- API-epic zodra je een frontend gaat bouwen
- Frontend-epic als laatste

Vermijd in maand 2-3 om te beginnen aan visualisatie-componenten, LLM-integratie of multi-tenant infrastructuur. Die komen na een proof-of-life van het basismodel.

## §4 — Hoeveel tijd neem je?

Realistische tijdsschattingen per fase, aangenomen ~3 uur Claude-Code-werk per dag:

| Fase | Tijd |
|------|------|
| Maand 1 — fundament + graph-MVP + eerste content | 4 weken |
| Maand 2-3 — uitbreiding content tot scope-doel | 6-12 weken |
| Maand 4-5 — engine + diagnostische intake (alleen leerdomein) | 6-8 weken |
| Maand 6-8 — frontend en gebruikerservaring | 8-12 weken |
| Maand 9+ — pilot, kalibratie, productie | doorlopend |

Olympus is in 10 maanden van leeg naar pilot-MVP gegaan. Reken voor jezelf op 8-14 maanden tot een echte gebruiker je systeem in gebruik neemt — afhankelijk van inhoud-volume.

## §5 — Welke beslissingen vooruit schuiven?

Drie beslissingen die in Olympus tot fase 3-4 uitgesteld zijn zonder problemen:

1. **PostgreSQL-migratie.** SQLite werkt prima tot je echte concurrent users hebt.
2. **Frontend-framework.** Tot je content er is, hoeft de UI niet meer dan een CLI te zijn.
3. **Multi-tenant authenticatie.** Eén lokale gebruiker is genoeg voor de eerste 100 testsessies.

Drie beslissingen die je vroeg moet nemen:

1. **ID-schema.** Migreren is duur. Beter twee dagen denken vooraf dan twee weken migreren later.
2. **Edge-types.** Toevoegen kan; semantiek wijzigen niet.
3. **Welke taal voor wat.** Documentatietaal halverwege wisselen is een nachtmerrie voor zoekbaarheid.

## §6 — Stop-momenten in je roadmap

Plan expliciete review-momenten:

- **Einde week 1:** "kan ik een leeg project draaien met groene CI?" — zo nee, repareren voor week 2 begint.
- **Einde week 2:** "kan ik 50 knopen laden, valideren en visualiseren?" — zo nee, geen content schrijven.
- **Einde week 4:** "is mijn architectuur stabiel of voel ik nog dagelijks frictie?" — bij frictie: refactoren voor je opschaalt naar honderden knopen.
- **Maand 3:** retrospectief — wat van de oorspronkelijke briefing klopt nog? Update BRIEFING en ONTWERPKEUZES.
- **Maand 6:** is het einddoel haalbaar in maand 12, of moet de scope kleiner?

Stop-momenten zijn geen vrijwillige luxe; ze zijn de plekken waar de aanname-versus-kennis-verhouding (principe 4 in hoofdstuk 01) wordt herijkt.

## Vragen voor je nieuwe project

1. Heb je je BRIEFING en ONTWERPKEUZES op papier vóór je dag 1 begint?
2. Welke vijf keuzes uit §2 zijn voor jou domein-relevant en welke zijn niet van toepassing?
3. Welke ene story uit week 2 zou je het meeste zorgen baren als die langer duurt? — bouw extra buffer.
4. Heb je een buffer-dag per week ingepland voor onverwachte refactors?
5. Welke stop-momenten zet je in je agenda?
