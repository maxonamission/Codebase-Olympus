# Project Briefing: Gymnasium Classica

## Een adaptief leersysteem voor Latijn en Grieks op VWO-gymnasiumniveau

**Versie:** 0.1 — Initiële briefing
**Datum:** 12 april 2026
**Auteur:** Max / Dream Team Dynamics
**Doel:** Projectbriefing voor Claude Code-implementatie

---

## 1. Projectvisie

### 1.1 Kernidee

Gymnasium Classica is een adaptief leersysteem dat leerlingen in staat stelt om — buiten school, met circa 30 minuten per dag — de eindtermen van het Nederlandse gymnasium te behalen voor Latijnse Taal en Cultuur (LTC) en Griekse Taal en Cultuur (GTC). Het systeem combineert een knowledge graph met spaced repetition, mastery-based progression en item response theory om een 3x efficiëntiewinst te realiseren ten opzichte van traditioneel klassikaal onderwijs.

### 1.2 Doelgroepen

**Primair:** VWO-leerlingen (atheneum) die Latijn en/of Grieks niet op school kunnen volgen maar zich op gymnasiumniveau willen ontwikkelen — bijvoorbeeld ter voorbereiding op een staatsexamen of als intellectuele verrijking.

**Secundair:** Gymnasiumleerlingen die bijles of extra ondersteuning nodig hebben. Het systeem kan fungeren als diagnostisch instrument (waar zit de lacune?) en als gerichte remediërende tool.

**Tertiair:** Volwassen autodidacten met interesse in de klassieke talen en cultuur.

### 1.3 Ambitie: waarom 3x realistisch is

De 3x-claim is geen marketingretoriek maar een conservatieve schatting op basis van drie convergerende lijnen uit de cognitieve psychologie:

**Bloom's 2-sigma probleem (1984).** Eén-op-één tutoring met mastery learning produceert een effect van twee standaarddeviaties boven klassikaal onderwijs. Dit is het verschil tussen de 50e en de 98e percentiel. De uitdaging die Bloom formuleerde — dit effect bereiken zonder een menselijke tutor per leerling — is precies wat een goed ontworpen adaptief systeem kan benaderen.

**Testing effect (Roediger & Karpicke, 2006).** Actieve retrieval is twee tot drie keer effectiever voor langetermijnretentie dan passieve studie. Een traditionele les bevat misschien 10-15% actieve retrieval; een goed ontworpen adaptief systeem kan dit naar 80%+ tillen.

**Spaced repetition (Cepeda et al., 2006; Pimsleur, 1967).** Het optimaal spreiden van herhalingen op basis van individueel vergeetgedrag verdubbelt tot verdrievoudigt de retentie per bestede minuut vergeleken met massed practice.

**De inefficiëntie van traditioneel klassikaal Latijn/Grieks.** Een gymnasiast besteedt typisch 760 studielasturen aan LTC of GTC over de volledige schoolloopbaan. Een groot deel daarvan gaat verloren aan klassikaal tempo (wachten op de langzaamste leerling), passief luisteren naar uitleg buiten de zone of proximal development, en herhaling die niet is afgestemd op individueel vergeetgedrag. Bij 30 minuten per dag over 4 jaar besteedt een Gymnasium Classica-leerling circa 730 uur — vergelijkbaar in volume, maar met een radicaal hogere effectiviteit per minuut.

---

## 2. Doelstellingen en eindtermen

### 2.1 Formeel kader

Het systeem bereidt voor op de officiële examenprogramma's LTC en GTC zoals vastgesteld door de minister en gespecificeerd in de syllabi van het College voor Toetsen en Examens (CvTE). De examenprogramma's kennen de volgende domeinen:

**Domein A** — Reflectie op klassieke teksten (subdomein 1) en antieke cultuur (subdomein 2)
**Domein B** — Reflectie op relaties tussen de antieke cultuur en de latere Europese cultuur
**Domein C** — Zelfstandige oordeelsvorming
**Domein D** — Oriëntatie op studie en beroep
**Domein E** — Informatievaardigheden

Het centraal examen (CE) toetst de domeinen A1, B en C. Het schoolexamen (SE) bestrijkt alle domeinen. Aangezien de leerling zich via een staatsexamen of extraneus-constructie moet kwalificeren, moet het systeem *alle* domeinen dekken.

### 2.2 Concrete vaardigheidsdoelen

**Taalvaardigheid (kern):**
- Zelfstandig vertalen van een ongeziene authentieke tekst (CE-niveau)
- Beheersing van de volledige grammatica volgens de CvTE-minimumlijst (per taal)
- Actieve beheersing van de hoogfrequente vocabulaire (Latijn: ~1500 woorden; Grieks: ~1200 woorden)
- Herkenning en analyse van stilistische, narratologische en argumentatieve middelen

**Leesvaardigheid (pensum):**
- Lezen en interpreteren van minimaal 30 pagina's (OCT) authentieke tekst per taal (SE)
- Lezen van minimaal 45 pagina's vertaalde klassieke tekst per taal (SE)
- Voorbereiding op het jaarlijks wisselende CE-pensum (specifieke auteur en genre)

**Cultuur (geïntegreerd):**
- Kennis van de cultuurhistorische context van gelezen teksten
- Reflectie op relaties tussen antieke en latere Europese cultuur (receptie, doorwerking)
- Zelfstandige oordeelsvorming over antieke thema's en dilemma's

### 2.3 Scope: Latijn én Grieks als geïntegreerd systeem

Het systeem behandelt Latijn en Grieks als twee parallelle maar verweven leerpaden binnen één knowledge graph. De rationale hiervoor:

- De cultuurhistorische laag (domein A2, B) is grotendeels gedeeld: Griekse filosofie, mythologie, geschiedenis en kunst zijn prerequisite-kennis voor zowel GTC als LTC
- Grammaticale concepten zijn structureel isomorf: het naamvallensysteem, werkwoordsmorfologie, syntactische constructies — de abstracte structuur is vergelijkbaar, alleen de concrete vormen verschillen
- Filosofie en geschiedenis fungeren als verbindend weefsel dat het leren van taal en cultuur versterkt en contextualiseert
- Het eindexamen LTC veronderstelt kennis van Griekse filosofie (Socrates, Plato, Aristoteles, Stoa, Epicurisme) en vice versa

De graph bevat daarom drie lagen:
1. **Taal-Latijn** en **Taal-Grieks** — grotendeels parallelle DAGs met taalspecifieke knopen
2. **Cultuur** — een gedeeld netwerk van cultuurhistorische knopen, verbonden met beide taallagen
3. **Interdisciplinair** — knopen die raken aan filosofie, geschiedenis, kunst en literatuurwetenschap, als verrijking en contextgevers

---

## 3. Ontwerpkeuzes

### 3.1 Methodische positionering: aansluiten bij of afwijken van schoolmethoden?

Dit is de meest fundamentele ontwerpkeuze. Hieronder een analyse van de opties.

#### 3.1.1 Het Nederlandse methodenlandschap

**Latijn — onderbouw:**
- **Fortuna** — geleidelijke opbouw via cultuurhistorisch-chronologische verhaallijn
- **SPQR** — steile leercurve, grammatica in overkoepelende thema's
- **Minerva** — innovatief, korte teksten, snel naar authentiek
- **Via Latina** — geïntegreerde taal-en-cultuurroute
- **Caesar** — grammatica in logische volgorde, eenvoudig en beeldend
- **Disco** — aandacht voor vertaaldidactiek en zelfstandig werken
- **LLPSI (Ørberg)** — natural method, geheel in het Latijn

**Grieks — onderbouw:**
- **Pallas** — marktleider, uitdagende teksten, versneld tempo in editie 2016
- **Olympos** — logisch, helder, overzichtelijk, één grammaticaonderwerp per hoofdstuk
- **Kosmos** — nieuwere methode

**Bovenbouw (beide talen):** Examenbundels en eigen lesmateriaal van docenten, gebaseerd op de jaarlijks wisselende syllabi.

#### 3.1.2 Analyse: sterke en zwakke punten van bestaande methoden

**Sterktes om over te nemen:**
- De grammaticale sequencing is doorgaans goed doordacht (decennia ervaring)
- De cultuurhistorische verhaallijn (Fortuna, Pallas) verhoogt motivatie
- De integratie van taal en cultuur (sinds 2014) is pedagogisch waardevol

**Zwaktes die het systeem moet adresseren:**
- Lineaire progressie: alle leerlingen doorlopen dezelfde sequentie in hetzelfde tempo
- Onvoldoende actieve retrieval: veel passief lezen en luisteren
- Geen adaptieve spacing: herhaling is kalendergestuurd, niet geheugengestuurd
- Te weinig diagnostiek: lacunes worden pas bij toetsen ontdekt, niet proactief gedetecteerd
- Overbelaste docenten die moeten kiezen tussen vertaalvaardigheid en cultuur

#### 3.1.3 Aanbeveling: hybride benadering

**Volg de schoolmethoden voor:**
- De *scope* van de grammatica en vocabulaire (de CvTE-minimumlijsten zijn leidend)
- De globale volgorde van grammaticale introductie (bewezen effectief over decennia)
- De cultuurhistorische thema's en auteurs
- De eindtermen als toetssteen

**Wijk af van de schoolmethoden voor:**
- De *granulariteit*: breek elke les op in atomaire kennisknopen (MathAcademy-stijl)
- De *sequencing*: gebruik de knowledge graph voor optimale volgorde, niet het lineaire boek
- De *repetitie*: vervang kalendergestuurde herhaling door algoritmische spaced repetition
- De *diagnostiek*: continue Bayesian Knowledge Tracing in plaats van periodieke toetsen
- De *didactiek*: hybride van deductieve grammatica-uitleg en inductief lezen (niet puur het een of het ander)

### 3.2 Didactische benadering: Grammar-Translation vs. Comprehensible Input vs. Hybride

#### 3.2.1 De benaderingen

**Grammar-Translation (GT):** De traditionele Nederlandse aanpak. Expliciete grammatica-instructie, rijtjes leren, ontleedoefeningen, vertalen van/naar het Nederlands. Sterk in analytisch begrip, zwak in leesvloeiendheid.

**Comprehensible Input (CI) / Natural Method:** De aanpak van Ørberg (LLPSI) en de bredere CI-beweging (Krashen). Leren door veel begrijpelijke input te verwerken, grammatica wordt impliciet verworven. Sterk in leesvloeiendheid, maar de evidence base voor klassieke talen is beperkt en het Nederlandse eindexamen toetst expliciet grammaticakennis.

**Processing Instruction (PI, VanPatten):** Een middenweg. Leerlingen verwerken input, maar worden expliciet gestuurd naar het verwerken van specifieke grammaticale features. Heeft een sterkere evidence base dan puur CI voor instructed settings.

#### 3.2.2 Aanbeveling: expliciete instructie + contextueel lezen

Het systeem moet de leerling voorbereiden op een examen dat *expliciete* grammaticakennis en vertaalvaardigheid toetst. Puur CI is daarvoor onvoldoende. De aanbeveling is:

1. **Expliciete grammatica-instructie** op het niveau van individuele kennisatomen, met directe oefening (GT-element)
2. **Contextueel lezen** van passages die de zojuist geleerde grammatica in context tonen (CI-element)
3. **Processing-oefeningen** die de leerling dwingen om op specifieke grammaticale features te letten (PI-element)
4. **Productieve oefeningen** (vormen invullen, zinnen vertalen) voor consolidatie

Dit is geen eclecticisme maar een weloverwogen combinatie: de expliciete instructie bouwt de analytische vaardigheid op die het examen vereist, het contextueel lezen bouwt leesvloeiendheid en woordenschat op, en de processing-oefeningen overbruggen de kloof.

### 3.3 Granulariteit van kennisknopen

#### 3.3.1 Het MathAcademy-model

MathAcademy werkt met circa 2500 *topics*, elk met 3-4 *knowledge points*. Elke knowledge point heeft prerequisite-relaties met *encompassing weights* die aangeven welk percentage van de prerequisite wordt geoefend bij het toepassen van de post-requisite. De totale graph heeft duizenden edges.

#### 3.3.2 Vertaling naar klassieke talen

De kennisatomen in Gymnasium Classica zijn van drie typen:

**Type G (Grammatica):** Minimaal toetsbare grammaticale eenheden.
Voorbeelden: "nominativus enkelvoud 1e declinatie", "presens indicativus actief 1e conjugatie", "AcI herkennen", "genitivus absolutus vertalen".
Geschat aantal: 400-600 per taal (Latijn iets meer door rijkere morfologie bij werkwoorden, Grieks door complexer accentensysteem en augment/reduplicatie).

**Type V (Vocabulaire):** Woorden gegroepeerd op frequentie in authentieke teksten.
De CvTE-minimumlijst is het vertrekpunt. Woorden worden niet alfabetisch maar op frequentie geordend en in semantische clusters aangeboden (lichaamsdelen, oorlogsvoering, politiek, filosofie).
Geschat aantal: 1500 Latijn, 1200 Grieks.

**Type C (Cultuur):** Cultuurhistorische kenniseenheden.
Voorbeelden: "de Atheense democratie", "de Stoïsche filosofie", "Vergilius' Aeneas als Romeinse held", "receptie van Ovidius in de Renaissance".
Geschat aantal: 200-300 (gedeeld tussen Latijn en Grieks, met taalspecifieke uitbreidingen).

**Type I (Integratie):** Vaardigheden die meerdere atomen combineren.
Voorbeelden: "een relatieve bijzin met conjunctivus in een Cicero-tekst vertalen", "een passage uit Homerus scanderen en het metrum herkennen".
Geschat aantal: 150-250 per taal.

**Totaal geschat:** 3000-5000 kennisknopen over beide talen heen, met 10.000-20.000 edges.

### 3.4 Relaties met filosofie en geschiedenis

Het systeem behandelt filosofie en geschiedenis niet als aparte vakken maar als *contextuele versterkers* van het taal- en cultuuronderwijs. Concreet:

**Filosofie** wordt geïntroduceerd wanneer de grammatica en vocabulaire het toelaten om filosofische teksten (in vertaling of origineel) te lezen. De kennisknopen zijn:
- Pre-Socratische natuurfilosofie (context voor vroege Griekse teksten)
- Socrates, Plato, Aristoteles (kernstof GTC én LTC)
- Hellenistische filosofie: Stoa, Epicurisme, Scepticisme (essentieel voor Seneca, Cicero)
- Ethiek en politieke filosofie (doorwerking naar Europese cultuur, domein B)

**Geschiedenis** wordt verweven als achtergrond bij de gelezen teksten:
- Griekse polis en Atheense democratie
- Perzische oorlogen en Peloponnesische oorlog
- Alexander de Grote en het Hellenisme
- Romeinse Republiek en Keizerrijk
- Overgang oudheid → middeleeuwen (receptie, domein B)

De implementatie: filosofische en historische knopen zijn prerequisite-knopen voor de integratieve vertaal- en interpretatieknopen die ze contextualiseren. Voorbeeld: de knoop "Stoïsche ethiek: kernbegrippen" is een prerequisite voor "Seneca, Epistulae Morales: vertaling en interpretatie".

### 3.5 Leerpadvolgorde: wanneer Latijn, wanneer Grieks?

#### Optie A: Latijn eerst (traditioneel Nederlands gymnasium)
De meeste Nederlandse gymnasia starten met Latijn in klas 1, Grieks in klas 2. Rationale: het Latijnse alfabet is vertrouwd, en basiskennis van het naamvallensysteem transfer naar Grieks.

#### Optie B: Parallel, maar Latijn met voorsprong
Start Latijn direct, introduceer het Griekse alfabet na circa 2 maanden, en laat Grieks vervolgens parallel maar met een fase-offset lopen.

#### Optie C: Vrije keuze
Laat de leerling (of ouder) kiezen. Het systeem ondersteunt beide talen onafhankelijk, maar benut transfer waar mogelijk.

**Aanbeveling:** Optie B als default, met mogelijkheid voor de leerling om via optie C te kiezen. Het systeem detecteert automatisch transfer-mogelijkheden (als de leerling de Latijnse ablativus kent, kan de introductie van de Griekse datief hierop voortbouwen).

### 3.6 Authenticiteit van teksten

#### Het spanningsveld
Het eindexamen vereist het vertalen van authentieke (ongeziene) teksten. Maar beginners kunnen geen authentieke teksten lezen. Er zijn twee strategieën:

**Aangepaste teksten (adaptationes):** Vereenvoudigde versies van authentieke teksten die geleidelijk complexer worden. Dit is de aanpak van Ørberg en de meeste schoolmethoden.

**Authentiek van begin af aan, maar met scaffolding:** De tekst is authentiek, maar het systeem biedt hulp (glosses, grammaticale annotaties, stap-voor-stap ontleedondersteuning).

**Aanbeveling:** Fase 1 (onderbouw-equivalent) werkt met aangepaste teksten en korte authentieke fragmenten. Fase 2 (bovenbouw-equivalent) introduceert langere authentieke teksten met afnemende scaffolding. Het systeem tracked de mate van scaffolding die de leerling nodig heeft als indicator van beheersing.

### 3.7 De rol van LLMs in het systeem

#### Waar LLMs waardevol zijn:
- **Oefeningen genereren:** Gegeven de constraints van de knowledge graph (welke grammatica en vocabulaire zijn beschikbaar), kan een LLM nieuwe oefenzinnen produceren die precies de juiste knopen activeren
- **Feedback formuleren:** Bij een foutieve vertaling kan een LLM uitleggen *waarom* het fout is en welke grammaticaregel van toepassing is
- **Culturele context verrijken:** Bij het lezen van een tekst kan een LLM aanvullende context bieden over de historische setting
- **Adaptieve uitleg:** De grammatica-uitleg aanpassen aan het begripsniveau van de leerling

#### Waar LLMs *niet* de kern vormen:
- **De knowledge graph** is handmatig opgebouwd door domeinexperts (cf. MathAcademy)
- **De scheduling engine** is algoritmisch, niet LLM-gestuurd
- **Het learner model** is gebaseerd op IRT/BKT, niet op LLM-inferentie
- **De beoordeling van vertalingen** vereist een rubric-gestuurd systeem, niet open-ended LLM-evaluatie (te onbetrouwbaar voor high-stakes assessment)

---

## 4. Systeemarchitectuur

### 4.1 Overzicht: vier lagen

```
┌─────────────────────────────────────────────┐
│           Laag 4: Presentation              │
│     React frontend · dagelijkse sessie      │
│     30 min · progress dashboard             │
├─────────────────────────────────────────────┤
│           Laag 3: Scheduling Engine         │
│     Task selection · spaced repetition      │
│     priority queue · session orchestration  │
├─────────────────────────────────────────────┤
│           Laag 2: Learner Model             │
│     BKT per knoop · IRT kalibratie          │
│     knowledge frontier · heat map           │
├─────────────────────────────────────────────┤
│           Laag 1: Knowledge Graph           │
│     kennisatomen · prerequisite edges       │
│     encompassing weights · oefeningen       │
│     culturele knopen · interdisciplinair    │
└─────────────────────────────────────────────┘
```

### 4.2 Laag 1: Knowledge Graph

#### 4.2.1 Datamodel

Elke **knoop** (kennisatoom) bevat:
- `id`: unieke identifier (bijv. `LAT-G-NOM-1D-SG` voor "Latijn, Grammatica, Nominativus, 1e declinatie, enkelvoud")
- `type`: G (grammatica), V (vocabulaire), C (cultuur), I (integratie)
- `taal`: `lat`, `grc`, `shared` (voor cultuurknopen)
- `titel_nl`: Nederlandse titel voor weergave
- `beschrijving`: Uitleg van het concept
- `bloom_niveau`: kennis, begrip, toepassing, analyse, synthese
- `fase`: onderbouw (1-3), bovenbouw (4-6)
- `bron_methode`: referentie naar schoolmethode(n) waar dit concept behandeld wordt
- `cevte_referentie`: verwijzing naar exameneenheid in het officiële examenprogramma

Elke **edge** (prerequisite-relatie) bevat:
- `source`: prerequisite-knoop
- `target`: post-requisite-knoop
- `type`: `prerequisite` (hard: moet beheerst zijn), `enrichment` (soft: helpt maar is niet strikt nodig), `transfer` (cross-linguïstisch: kennis in de ene taal faciliteert de andere)
- `encompassing_weight`: float 0-1, welk percentage van de prerequisite wordt mee-geoefend bij het oefenen van de post-requisite (cf. MathAcademy)

#### 4.2.2 Oefeningen-database

Elke knoop heeft een verzameling **items** (oefeningen):
- `knoop_ids`: lijst van kennisknopen die dit item activeert
- `type`: herkenning (MC), productie (invullen), analyse (ontleden), synthese (vertalen), contextueel (passage-gebaseerd)
- `moeilijkheid`: IRT-parameter (initieel geschat, later gekalibreerd)
- `discriminatie`: IRT-parameter (hoe goed onderscheidt dit item tussen beheersers en niet-beheersers)
- `verwachte_tijd`: in seconden (voor time-weighted scoring)
- `stimulus`: de opgave (tekst, afbeelding, audio)
- `antwoord`: correct antwoord + acceptabele varianten
- `feedback`: uitleg bij fout antwoord
- `bron`: handmatig, gegenereerd (LLM), of afgeleid van authentieke tekst

### 4.3 Laag 2: Learner Model

#### 4.3.1 Bayesian Knowledge Tracing (BKT)

Per knoop per leerling worden vier parameters bijgehouden:
- `P(L₀)`: kans dat de knoop al beheerst is vóór de eerste oefening (prior)
- `P(T)`: kans dat de knoop geleerd wordt bij een oefening (transitie)
- `P(G)`: kans op een correct antwoord bij niet-beheersing (raden)
- `P(S)`: kans op een fout antwoord bij wel-beheersing (vergissing)

Na elke oefening wordt de posterior `P(Lₙ)` bijgewerkt via Bayes' regel.

#### 4.3.2 Item Response Theory (IRT)

Een 2PL-model (Two-Parameter Logistic):
```
P(correct | θ, a, b) = 1 / (1 + exp(-a(θ - b)))
```
- `θ`: leerlingvaardigheid (geschat per domein/cluster)
- `a`: discriminatieparameter per item
- `b`: moeilijkheidsparameter per item

IRT wordt gebruikt voor:
- Selectie van items op het juiste niveau (niet te makkelijk, niet te moeilijk: de zone of proximal development)
- Kalibratie van nieuwe items op basis van leerlingreacties
- Efficiënte diagnostiek bij intake (adaptive testing)

#### 4.3.3 Vergeetcurve (Ebbinghaus / SM-2+)

Per beheerste knoop wordt bijgehouden:
- `laatste_review`: timestamp
- `interval`: huidige review-interval
- `easiness_factor`: hoe makkelijk de leerling deze knoop onthoudt
- `repetitions`: aantal succesvolle reviews
- `geschatte_retentie`: functie van tijd sinds laatste review en het individuele vergeettempo

### 4.4 Laag 3: Scheduling Engine

#### 4.4.1 Het optimalisatieprobleem

Gegeven een sessie van 30 minuten, selecteer een sequentie van taken die de verwachte leerwinst maximaliseert, waarbij:
- Knopen die dreigen te worden vergeten (retentie < drempel) worden herhaald
- Nieuwe knopen worden geïntroduceerd waarvoor alle prerequisites groen zijn (≥ 0.85 beheersing)
- Integratieve taken worden ingezet die meerdere knopen tegelijk versterken
- Non-interference wordt nagestreefd: opeenvolgende taken variëren in type en onderwerp

#### 4.4.2 Prioriteitswachtrij

Elke knoop krijgt een **urgentiescore** die wordt berekend als gewogen combinatie van:

1. **Vergeet-urgentie:** `1 - geschatte_retentie` (hoe lager de retentie, hoe urgenter)
2. **Readiness:** voor nieuwe knopen: gemiddelde beheersing van prerequisites (hoe hoger, hoe klaar)
3. **Pedagogische waarde:** knopen met veel post-requisites (hoog out-degree in de graph) zijn waardevoller om vroeg te beheersen
4. **Encompassing-bonus:** integratieknopen die meerdere prerequisites tegelijk versterken
5. **Domein-balans:** het systeem zorgt dat grammatica, vocabulaire en cultuur evenwichtig aan bod komen

#### 4.4.3 Sessie-orkestratie

Een sessie van 30 minuten wordt opgedeeld in blokken:

- **Warming-up (5 min):** Snelle retrieval van vocabulaire en basisgrammatica (flashcard-achtig)
- **Nieuwe stof (10 min):** Introductie van 1-2 nieuwe kennisknopen met uitleg + oefening
- **Verdieping (10 min):** Contextueel lezen of vertaaloefening die nieuwe en bekende stof combineert
- **Cool-down (5 min):** Spaced repetition review van eerder geleerde stof

De verhoudingen zijn adaptief: als veel stof dreigt weg te zakken, verschuift het accent naar herhaling; als de leerling sterk presteert, wordt meer nieuwe stof aangeboden.

### 4.5 Laag 4: Presentation

#### 4.5.1 Frontend

React-applicatie met:
- **Sessie-interface:** de dagelijkse 30-minuten-ervaring
- **Progress dashboard:** knowledge graph visualisatie (heat map), voortgang per domein, spaced repetition statistieken
- **Pensum-lezer:** voor het lezen van langere authentieke teksten met annotaties
- **Cultureel portfolio:** verzameling van culturele kennis, gelinkt aan de graph

#### 4.5.2 Backend

Python-backend (FastAPI) met:
- Knowledge graph opgeslagen in een geschikt formaat (zie sectie 5)
- Learner model per gebruiker
- Scheduling engine
- API voor oefeningen-generatie (optioneel: LLM-integratie)
- Authenticatie en progress-opslag

---

## 5. Technische ontwerpkeuzes

### 5.1 Dataopslag voor de knowledge graph

**Optie A: Neo4j (graph database)**
Voordelen: native graph queries, Cypher querytaal, visualisatie-tools.
Nadelen: extra infra, overhead voor een applicatie van deze schaal.

**Optie B: NetworkX + JSON/YAML-bestanden**
Voordelen: geen externe dependencies, volledige controle, goed te versiebeheren in Git, makkelijk te bewerken in Obsidian.
Nadelen: geen persistente graph database, queries zijn minder expressief.

**Optie C: SQLite + adjacency list**
Voordelen: enkelvoudig bestand, SQL-queries, goed genoeg voor de schaal.
Nadelen: minder elegant voor graph-traversal.

**Aanbeveling:** Start met optie B (NetworkX + JSON) voor de modellerings- en prototypefase. De graph past ruim in geheugen (5000 knopen, 20.000 edges). Migreer naar Neo4j of SQLite als de applicatie in productie gaat en meerdere gebruikers bedient.

### 5.2 Opslag van de knowledge graph in Obsidian

Tijdens de modelleeringsfase kan de knowledge graph in Obsidian worden opgebouwd:
- Elke knoop als een note met YAML frontmatter (type, taal, fase, prerequisites, etc.)
- Links tussen notes als prerequisite-relaties
- Tags voor clustering (grammatica, vocabulaire, cultuur)
- Obsidian Graph View als visuele controle op structuur en connectiviteit

Een export-script converteert de Obsidian vault naar het formaat dat de applicatie gebruikt.

### 5.3 Spaced repetition algoritme

**Optie A: SM-2 (SuperMemo)**
Het klassieke algoritme. Eenvoudig, goed begrepen, breed gebruikt (Anki).
Nadelen: geen adaptatie op basis van item-kenmerken, geen optimalisatie voor verwachte retentie.

**Optie B: FSRS (Free Spaced Repetition Scheduler)**
Modernier algoritme (Anki v23+). Betere voorspelling van vergeetgedrag op basis van machine learning.

**Optie C: Half-Life Regression (Settles & Meeder, 2016, Duolingo)**
Schat de half-life van elk feit per leerling op basis van features (woord-moeilijkheid, herhalingsgeschiedenis, etc.).

**Aanbeveling:** Start met SM-2 voor eenvoud. Evalueer na voldoende data of FSRS of HLR een significante verbetering oplevert. Het verschil wordt pas meetbaar bij honderden leerlingen met maanden aan data.

### 5.4 Tech stack samenvatting

| Component | Technologie | Rationale |
|---|---|---|
| Knowledge graph (modellering) | Obsidian + YAML frontmatter | Max' bestaande tooling, visuele graph view |
| Knowledge graph (runtime) | NetworkX + JSON | In-memory, snel, geen extra infra |
| Learner model | Python (numpy/scipy) | BKT en IRT zijn matrixoperaties |
| Scheduling engine | Python | Prioriteitswachtrij, graph-traversal |
| Backend API | FastAPI | Async, type-safe, snel te prototypen |
| Frontend | React (JSX) | Interactieve sessie-interface |
| Database (users/progress) | SQLite → PostgreSQL | Start simpel, schaal later |
| LLM-integratie (optioneel) | Claude API (Anthropic) | Oefeningen genereren, feedback, uitleg |
| Package management | uv | Max' standaard |

---

## 6. Roadmap

### Fase 0: Fundament (weken 1-4) ✅

- [x] Projectstructuur opzetten (Python project met uv, Git repo)
- [x] Taxonomie van kennisatoom-types formaliseren (Pydantic models + ID-schema)
- [x] Eerste 50 grammaticaknopen Latijn modelleren met prerequisite-relaties (smoke test)
- [x] Graph loader met directory-loading en validatie (cycle detection, connectivity, topo sort)
- [x] 113 tests (alle groen)

### Fase 1: Knowledge Graph — MVP leerjaar 1 (weken 5-16)

**MVP-scope: leerjaar 1 gymnasium, beide talen (~850 knopen).** Model: scholen als het Vossius die Latijn én Grieks vanaf dag 1 aanbieden. Externe validatie door een klassieke-taleninstituut.

**1a. Latijnse grammatica (~150 knopen)**
- [x] 50 Latijnse grammaticaknopen als smoke test (decl. 1-2, presens, imperfectum, basissyntaxis)
- [ ] Declinatie 3 compleet (alle naamvallen sg/pl, m/f vs. neutrum, i-stammen)
- [ ] Declinaties 4 en 5 (basis)
- [ ] Pronomina (persoonlijk, bezittelijk, aanwijzend, vragend)
- [ ] Adjectieven 3e declinatie, trappen van vergelijking (basis)
- [ ] Perfectum systeem (ind. act., 4 conjugaties + esse)
- [ ] Passief presens (ind., 4 conjugaties)
- [ ] Imperativus, deelwoorden (PPP/PPA herkenning)
- [ ] Syntaxis: AcI, relatieve bijzin, bijwoordelijke bepalingen, voegwoorden

**1b. Grieks alfabet — onboarding-subgraph (~40 knopen)**
- [ ] Letterherkenning (groepen naar visuele/fonetische gelijkenis)
- [ ] Fonologie: klinkers, medeklinkers, diftongen
- [ ] Diakritiek: spiritus asper/lenis, accenttekens, iota subscriptum
- [ ] Leesvaardigheid: syllaben → woorden → korte zinnen
- [ ] Prerequisite-gate: blokkeert alle GRC-grammaticaknopen

**1c. Griekse grammatica (~100 knopen)**
- [ ] O-declinatie (2e) en a-declinatie (1e), incl. subtypes
- [ ] 3e declinatie basis (consonantstammen)
- [ ] Lidwoord (ὁ, ἡ, τό) — prominent in Grieks
- [ ] Presens ind. act. (thematische -ω verba + εἰμί)
- [ ] Imperfectum (augment + persoonsuitgangen)
- [ ] Medium-passief presens (typisch Grieks)
- [ ] Pronomina, adjectieven, imperativus, infinitief, participia intro
- [ ] Syntaxis: woordvolgorde, ontkenning, voorzetsels

**1d. Vocabulaire (~500 knopen, individueel per woord)**
- [ ] Latijns vocabulaire (~300 woorden, frequentiebanden F01-F06)
- [ ] Grieks vocabulaire (~200 woorden, frequentiebanden F01-F04)
- [ ] Prerequisite-edges naar relevante grammaticaknopen (declinatie/conjugatie)

**1e. Gedeelde cultuurknopen (~70 knopen, SHA-C-\*)**
- [ ] Mythologie (~15): Olympische goden, Trojaanse oorlog, Odysseus, Herakles
- [ ] Geschiedenis (~15): stichting Rome, poleis, Atheense democratie, Perzische oorlogen
- [ ] Maatschappij (~12): dagelijks leven, slavernij, onderwijs, familia Romana
- [ ] Kunst, literatuur, religie, filosofie intro (~25)

**1f. Transfer-edges (~100 edges)**
- [ ] LAT→GRC transfer-edges tussen isomorfe concepten (naamvallen, werkwoordstijden, syntaxis)
- [ ] Encompassing weights 0.2-0.4 (transfer faciliteert, vereist niet)

**1g. Kwaliteitscontrole**
- [ ] Encompassing weights instellen per edge
- [ ] Graph-kwaliteitscontrole: cycle detection, orphan detection, topologische analyse
- [ ] Externe validatie door klassieke-taleninstituut

### Fase 2: Learner Model + Scheduling (weken 17-24)
- [ ] BKT-implementatie per knoop
- [ ] SM-2 spaced repetition implementatie
- [ ] Prioriteitswachtrij met urgentiescores
- [ ] Sessie-orkestratie (30 min, verdeling warming-up / nieuw / verdieping / cool-down)
- [ ] Diagnostische intake (adaptive placement test)
- [ ] CLI-interface voor testen (geen frontend nodig in deze fase)

### Fase 3: Oefeningen-engine (weken 25-32)
- [ ] Oefentypen per knoop-type ontwerpen
- [ ] Handmatige oefeningen voor de eerste 200 knopen
- [ ] LLM-gebaseerde oefeningen-generatie (gegeven constraints uit de graph)
- [ ] Feedback-engine (uitleg bij foute antwoorden)
- [ ] IRT-kalibratie framework (initiële parameterschattingen)

### Fase 4: Frontend + MVP (weken 33-40)
- [ ] React frontend: sessie-interface
- [ ] Progress dashboard met graph-visualisatie
- [ ] User authenticatie en progress-opslag
- [ ] Eerste pilot met 5-10 leerlingen

### Fase 5: Iteratie en uitbreiding (week 41+)
- [ ] IRT-parameters kalibreren op basis van pilot-data
- [ ] Vocabulaire-knopen uitbreiden naar volledige CvTE-minimumlijst
- [ ] Cultuurknopen uitbreiden
- [ ] Pensum-lezer voor authentieke teksten
- [ ] Examensimulatie (proef-CE)

---

## 7. Risico's en mitigatie

### 7.1 De knowledge graph bouwen is arbeidsintensief

MathAcademy rapporteert dat het instellen van encompassing weights een maand full-time werk kostte voor één persoon. Voor klassieke talen is de graph kleiner (3000-5000 vs. 2500 topics bij MathAcademy, maar MathAcademy-topics zijn grover), maar het vereist domeinexpertise.

**Mitigatie:** Begin met een *minimal viable graph* (Latijn onderbouw, 200 knopen) en valideer de architectuur voordat je de volledige graph bouwt. Gebruik de grammaticale sequencing van bestaande methoden als startpunt, niet als slavische kopie.

### 7.2 Auteursrecht op lesmateriaal

De inhoud van methoden als Pallas, Fortuna en SPQR is auteursrechtelijk beschermd. Het systeem kan niet simpelweg teksten en oefeningen overnemen.

**Mitigatie:** Gebruik de methoden als *referentie voor scope en volgorde*, niet als bron van content. Alle oefeningen en teksten worden nieuw gecreëerd of afgeleid van public domain bronnen (authentieke klassieke teksten zijn vrij van auteursrecht). De CvTE-minimumlijsten zijn overheidspublicaties en vrij te gebruiken.

### 7.3 Validatie zonder schoolcontext

Zonder een school als institutionele partner is het moeilijk om het systeem te valideren met voldoende leerlingen.

**Mitigatie:** Start met een kleine pilot (5-10 leerlingen) via persoonlijk netwerk. Het staatsexamen biedt een objectieve externe toets: als leerlingen na x maanden gebruik een staatsexamen LTC of GTC halen, is dat harde validatie.

### 7.4 Motivatie bij zelfstudie

30 minuten per dag volhouden zonder externe dwang (school, docent, klasgenoten) is een uitdaging, vooral voor tieners.

**Mitigatie:** Gamification elementen (XP, streaks, niveaus — cf. MathAcademy), maar ook intrinsieke motivatie via fascinerende culturele content. De cultuurlaag is niet alleen examenstof maar ook het "waarom zou ik dit willen leren"-antwoord. Daarnaast: progress visibility (de heat map van de knowledge graph die langzaam groen kleurt) is een krachtige motivator.

---

## 8. Referenties

### Cognitieve psychologie en leerwetenschappen
- Bloom, B. S. (1984). The 2 Sigma Problem: The Search for Methods of Group Instruction as Effective as One-to-One Tutoring. *Educational Researcher, 13*(6), 4-16.
- Cepeda, N. J., et al. (2006). Distributed practice in verbal recall tasks: A review and quantitative synthesis. *Psychological Bulletin, 132*(3), 354-380.
- Corbett, A. T., & Anderson, J. R. (1995). Knowledge tracing: Modeling the acquisition of procedural knowledge. *User Modeling and User-Adapted Interaction, 4*(4), 253-278.
- Doignon, J.-P., & Falmagne, J.-C. (1999). *Knowledge Spaces*. Springer.
- Pimsleur, P. (1967). A Memory Schedule. *The Modern Language Journal, 51*(2), 73-75.
- Roediger, H. L., & Karpicke, J. D. (2006). Test-Enhanced Learning: Taking Memory Tests Improves Long-Term Retention. *Psychological Science, 17*(3), 249-255.
- Settles, B., & Meeder, B. (2016). A Trainable Spaced Repetition Model for Language Learning. *Proceedings of ACL 2016*.

### Adaptief leren en knowledge graphs
- MathAcademy (2024). How Our AI Works. https://mathacademy.com/how-our-ai-works
- Skycak, J. (2024). How Math Academy Creates its Knowledge Graph. https://www.justinmath.com/how-math-academy-creates-its-knowledge-graph/
- VanLehn, K. (2006). The behavior of tutoring systems. *International Journal of Artificial Intelligence in Education, 16*(3), 227-265.

### Klassieke talen didactiek
- Ørberg, H. H. (2011). *Lingua Latina per se Illustrata, Pars I: Familia Romana*. Focus Publishing.
- VanPatten, B. (2004). *Processing Instruction: Theory, Research, and Commentary*. Lawrence Erlbaum.
- Krashen, S. D. (1982). *Principles and Practice in Second Language Acquisition*. Pergamon.

### Nederlands examenkader
- CvTE. Syllabus Centraal Examen LTC VWO. https://www.examenblad.nl
- CvTE. Syllabus Centraal Examen GTC VWO. https://www.examenblad.nl
- SLO. Leerplan in Beeld: Klassieke Talen. https://www.slo.nl/thema/vakspecifieke-thema/klassieke-talen/
- VCN (2014). Een Gouden Standaard voor de gymnasiumopleiding.
- SLO (2023). Startnotitie Actualisatie Examenprogramma's Klassieke Talen.

---

## 9. Open vragen voor vervolgdiscussie

1. **Staatsexamen als validatiepad:** Hoe verhoudt het staatsexamen zich exact tot het reguliere eindexamen? Zijn er verschillen in pensum of toetsvorm die het curriculum beïnvloeden?

2. **Omvang van de culturele laag:** Hoeveel van domein B (receptie, doorwerking) moet het systeem zelfstandig afdekken, en hoeveel kan worden overgelaten aan aanvullend leeswerk?

3. **Grieks alfabet als bottleneck:** Het Griekse alfabet is voor veel leerlingen een drempel. Moet het systeem hier een aparte module voor bieden (voorafgaand aan de reguliere graph)?

4. **Metriek en prosodie:** In hoeverre moet het systeem metriek behandelen (hexameter scanderen, etc.)? Dit is een specifieke vaardigheid die op het CE aan bod kan komen.

5. **Actief Latijn/Grieks:** Moet het systeem enige vorm van productieve taalvaardigheid nastreven (zinnen schrijven in het Latijn/Grieks), of is puur receptieve beheersing (vertalen naar het Nederlands) voldoende voor het examen?

6. **Businessmodel:** Is dit een open-source-project, een freemium SaaS, of een eenmalig-licentiemodel? Dit beïnvloedt architectuurbeslissingen (multi-tenancy, privacy, hosting).

---

*Dit document is een levend document. Het wordt bijgewerkt naarmate ontwerpkeuzes worden gemaakt en het project vordert.*
