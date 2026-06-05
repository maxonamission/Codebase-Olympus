# Ontwerpkeuzes Gymnasium Classica

**Versie:** 0.1
**Datum:** 12 april 2026
**Status:** Vastgesteld — complement bij BRIEFING_GYMNASIUM_CLASSICA.md

---

## Leeswijzer

Dit document legt de ontwerpkeuzes vast die volgen uit de open vragen in de projectbriefing (sectie 9). Per keuze wordt de vraag herhaald, de beslissing genoteerd, de onderbouwing gegeven, en de architecturale implicaties benoemd. Het document dient als referentie voor de Claude Code-implementatie: elke keuze vertaalt zich in concrete technische requirements.

---

## Keuze 1: Validatiepad — Staatsexamen

### Vraag
Hoe verhoudt het staatsexamen zich tot het reguliere eindexamen, en welke consequenties heeft dit voor het curriculum?

### Beslissing
Het systeem bereidt primair voor op het **staatsexamen VWO** in LTC en/of GTC. Het staatsexamen is het formele validatiepad voor leerlingen die buiten het reguliere gymnasium om examen willen doen.

### Onderbouwing
Het staatsexamen is volledig gelijkwaardig aan het reguliere eindexamen. Het centraal examen (CE) is identiek — dezelfde opgaven, op hetzelfde moment. Het verschil zit uitsluitend in het schoolexamen, dat bij het staatsexamen wordt vervangen door een *college-examen*. Dit college-examen kent twee componenten:

1. **Schriftelijk deel:** vergelijkbaar met het SE, toetst de domeinen A t/m E aan de hand van gelezen teksten (pensum) en cultuurkennis.
2. **Mondeling deel:** de kandidaat wordt mondeling geëxamineerd over de gelezen teksten en de cultuurhistorische context. Dit is het cruciale verschil met het reguliere onderwijs.

Voor de primaire doelgroep (atheneumleerlingen die een vak erbij willen doen) geldt dat zij zich als extraneus kunnen aanmelden bij DUO wanneer hun school het vak niet aanbiedt. Zij ontvangen dan een deelcertificaat dat meetelt voor hun diploma.

### Architecturale implicaties

**A1.1** Het curriculum moet alle vijf domeinen (A t/m E) dekken, niet alleen het CE-deel.

**A1.2** Het systeem moet een **pensum-module** bevatten: een begeleid leestraject door de jaarlijks wisselende auteur en teksten. Het CE-pensum wordt ruim van tevoren bekendgemaakt (auteurs staan al vast tot 2030), dus het systeem kan vooruit plannen.

**A1.3** Het systeem moet een **mondelinge examenmodule** bevatten (zie keuze 6).

**A1.4** De planning-engine moet rekening houden met de examendatum: het systeem moet het leerpad zo timen dat de leerling op de examendatum klaar is, inclusief het pensum van dat specifieke jaar.

---

## Keuze 2: Omvang van de culturele laag

### Vraag
Hoeveel van domein B (receptie, doorwerking) moet het systeem zelfstandig dekken?

### Beslissing
Het systeem dekt **alle cultuurkennis die expliciet in de CvTE-syllabi wordt vereist**, aangevuld met een **contextuele verrijkingslaag** die niet wordt getoetst maar het leren versterkt.

### Onderbouwing
De syllabi zijn verrassend specifiek over welke cultuurkennis wordt verwacht. De syllabus LTC 2026 (Seneca/Cicero) bevat bijvoorbeeld een uitgebreide behandeling van de Stoïsche en Epicurische filosofie, het begrip vriendschap bij Aristoteles, en de brieftraditie in de oudheid. Deze kennis is *geen optionele verrijking* — het wordt direct getoetst op het CE via interpretatievragen bij het pensum.

De verrijkingslaag dient twee doelen: motivatie (de leerling begrijpt *waarom* deze teksten en thema's belangrijk zijn) en transfer (filosofische en historische context helpt bij het interpreteren van ongeziene teksten).

### Architecturale implicaties

**A2.1** Cultuurknopen in de knowledge graph krijgen een attribuut `toetsbaar: boolean`. Toetsbare knopen zijn gekoppeld aan specifieke exameneenheden; verrijkingsknopen zijn dat niet.

**A2.2** De scheduling engine behandelt toetsbare cultuurknopen als verplichte stof (moeten groen zijn voor examengereedheid); verrijkingsknopen worden aangeboden wanneer er ruimte is in de sessie of als de leerling extra tijd besteedt.

**A2.3** Per examenjaar wordt een **syllabus-overlay** gedefinieerd: een set cultuurknopen die specifiek is voor de auteur en het thema van dat jaar. Dit is een jaarlijks onderhoudstaak.

**A2.4** De interdisciplinaire knopen (filosofie, geschiedenis) worden gemodelleerd als *gedeelde knopen* met edges naar zowel Latijnse als Griekse taal- en integratieknopen. Een knoop als "Stoïsche ethiek: kernbegrippen" is prerequisite voor zowel Seneca-interpretatie (LTC) als Epictetus-context (GTC).

---

## Keuze 3: Grieks alfabet — onboarding-module

### Vraag
Moet het systeem een aparte module bieden voor het Griekse alfabet?

### Beslissing
**Ja.** Het Griekse alfabet wordt gemodelleerd als een **onboarding-subgraph** die prerequisite is voor alle Griekse grammatica- en vocabulaireknopen.

### Onderbouwing
Het Griekse alfabet is de meest voorspelbare bottleneck voor beginners. Het omvat 24 letters, majuskel- en minuskelvormen, en het systeem van diakritische tekens (spiritus asper/lenis, accenttekens). Voor een Nederlandse leerling is dit in 2-3 weken te leren bij dagelijks oefenen.

De subgraph is klein (circa 30-40 knopen: individuele letters, lettergroepen, diakritische tekens, leesoefeningen) maar kritisch: zonder beheersing van het alfabet is elke andere Griekse oefening onmogelijk.

### Architecturale implicaties

**A3.1** De onboarding-subgraph is een DAG met drie fasen: letterherkenning (Grieks→naam), letterschrijven (naam→Grieks), en woorden lezen (combinaties van letters in eenvoudige woorden).

**A3.2** De scheduling engine blokkeert alle Griekse grammaticaknopen zolang de alfabet-subgraph niet beheerst is (≥ 0.90 posterior op alle knopen).

**A3.3** Oefentypen voor het alfabet zijn specifiek: visuele herkenning, audio-herkenning (uitspraak), en productie (het typen van Griekse letters). Dit vereist een Grieks toetsenbord-input in het frontend.

**A3.4** Het alfabet wordt aangeboden zodra de leerling Grieks activeert. Bij de aanbevolen volgorde (optie B: Latijn met voorsprong) wordt de alfabet-module gestart na circa 2 maanden Latijn.

---

## Keuze 4: Metriek en prosodie

### Vraag
In hoeverre moet het systeem metriek behandelen?

### Beslissing
**Volledig opnemen als subgraph**, beperkt tot de metrische vormen die op het CE aan bod komen: dactylisch hexameter (Latijn en Grieks) en elegisch distichon (Latijn).

### Onderbouwing
Scanderen wordt actief getoetst op het CE wanneer het pensum poëzie betreft (Vergilius, Ovidius, Homerus). De cyclus van CE-auteurs is voorspelbaar — poëzie komt gemiddeld om het jaar voor. Een leerling die het CE maakt in een poëziejaar *moet* kunnen scanderen.

Metriek is bovendien een domein dat zich uitstekend leent voor algoritmische oefening: het is regelgestuurd (lang/kort regels, elisieregeIs, caesuurregels) en de correctheid van een scansie is objectief vast te stellen.

### Architecturale implicaties

**A4.1** De metriek-subgraph bevat circa 15-20 knopen: prosodie (lettergreeplengte), positieregeIs, dactylus/spondee, hexameter-schema, caesuren, elisie, en scan-oefeningen van toenemende complexiteit.

**A4.2** Prerequisite-edges vanuit metriek lopen naar de integratieknopen voor poëzie-auteurs (Vergilius, Ovidius, Homerus).

**A4.3** De scheduling engine activeert metriek-knopen op basis van het gekozen examenjaar: als het pensum proza is (Cicero, Livius, Seneca), krijgen metriek-knopen een lagere prioriteit maar worden ze niet overgeslagen (ze zijn nodig voor het SE-pensum dat ook poëzie kan bevatten).

---

## Keuze 5: Productieve oefeningen (Nederlands→Latijn/Grieks)

### Vraag
Moet het systeem productieve taalvaardigheid (actief Latijn/Grieks) nastreven?

### Beslissing
**Ja, als trainingsmiddel.** Productieve oefeningen worden opgenomen in de oefeningen-engine als een oefentype naast receptieve oefeningen. Ze zijn geen einddoel en worden niet apart getoetst.

### Onderbouwing
De evidence is helder: bidirectioneel oefenen versterkt de retentie van morfologie significant. Bjork (1994) noemt dit *desirable difficulty*: een oefenvorm die op het moment van oefenen moeilijker voelt, maar op langere termijn tot betere retentie leidt.

Concreet gaat het om oefenvormen als:
- **Vormen invullen:** "Vul de juiste vorm in: puer _____ (amare, 3e pers. sing. imperfectum)" → *amabat*
- **Zinnen aanvullen:** Gegeven een Nederlandse zin en een Latijns/Grieks sjabloon, vul de ontbrekende woorden in de juiste vorm in
- **Paradigma-drill:** Vervoeg/verbuig een woord in alle gevraagde vormen

Dit zijn *gesloten* oefenvormen (er is één correct antwoord of een beperkte set correcte antwoorden), geen vrije compositie. Dat maakt automatische beoordeling betrouwbaar.

### Architecturale implicaties

**A5.1** Het oefentype `productie` wordt toegevoegd aan de oefeningen-taxonomie, naast `herkenning`, `analyse` en `synthese`.

**A5.2** Productieve items worden gekoppeld aan dezelfde kennisknopen als receptieve items, maar met een hogere moeilijkheidsparameter in het IRT-model (ze zijn inherent moeilijker).

**A5.3** De scheduling engine weegt productieve oefeningen als *versterking*: ze worden ingezet wanneer een knoop net de beheersingsdrempel heeft bereikt, als consolidatie-strategie. Ze worden niet gebruikt als introductie van nieuw materiaal.

**A5.4** Het frontend moet Latijnse en Griekse tekst-input ondersteunen, inclusief diakritische tekens voor Grieks. Dit vereist een polytonic Greek keyboard-component of een input-helper.

---

## Keuze 6: Mondelinge examensimulatie

### Vraag
Wil je LLM-gestuurde mondelinge examensimulatie opnemen?

### Beslissing
**Ja, als aparte module in de roadmap** (fase 5 of later). Dit is een onderscheidende feature die geen bestaand systeem biedt.

### Onderbouwing
Het college-examen van het staatsexamen bevat een mondeling deel waarin de kandidaat wordt ondervraagd over de gelezen teksten en de cultuurhistorische context. Dit is een vaardigheid die fundamenteel verschilt van schriftelijke toetsing: de leerling moet in real-time antwoorden formuleren, doorvragen beantwoorden, en een interpretatie verdedigen.

Een LLM is bij uitstek geschikt om dit te simuleren: het kan de rol van examinator spelen, contextueel relevante vragen stellen over het gelezen pensum, doorvragen bij onduidelijke antwoorden, en feedback geven op de kwaliteit van de argumentatie.

De kwalificatie "als aparte module in de roadmap" is bewust: dit vereist voice-interface (STT/TTS), een gespecialiseerde prompt-architectuur, en kalibratie tegen echte examenstandaarden. Het is technisch haalbaar maar niet noodzakelijk voor de MVP.

### Architecturale implicaties

**A6.1** De mondelinge module wordt gemodelleerd als een apart systeem dat *bovenop* de knowledge graph en het learner model functioneert, niet als onderdeel ervan.

**A6.2** De module gebruikt het pensum dat de leerling heeft gelezen (uit de pensum-module) als context voor de LLM-examinator.

**A6.3** Technische vereisten: spraak-naar-tekst (STT), tekst-naar-spraak (TTS), een conversationele LLM-interface met domeinspecifieke system prompts, en een rubric-gebaseerd beoordelingsmodel.

**A6.4** Privacy-overweging: spraakdata van minderjarigen vereist expliciete toestemming en verwerking conform AVG. Bij de keuze voor een LLM-provider geldt de bestaande voorkeur voor EU data residency (Mistral/Voxtral voor STT, Claude voor de conversatie).

**A6.5** Roadmap-positie: na de MVP (fase 5+). De module kan als standalone feature worden ontwikkeld zodra het pensum-leessysteem en de cultuurknopen functioneel zijn.

---

## Keuze 7: Businessmodel en architectuur

### Vraag
Welk businessmodel, en wat zijn de architecturale consequenties?

### Beslissing
**Architectuur geschikt maken voor betaald abonnement**, ook al is de prijs in beginsel laag of €0. Het systeem wordt ontworpen als een SaaS-applicatie met multi-tenant architectuur.

### Onderbouwing
Deze keuze is strategisch: door van begin af aan de juiste architecturale patronen te implementeren (user management, subscription state, data isolation), voorkom je een kostbare refactor later. De prijs kan flexibel zijn — gratis gedurende de pilotfase, symbolisch laag gedurende beta, marktconform bij volwassenheid — maar de technische basis moet vanaf dag één kloppen.

Een betaald model heeft ook een pedagogisch voordeel: het creëert een licht commitment-effect (*sunk cost*) dat de kans op doorzetten vergroot. Een abonnement van zelfs €5/maand verhoogt de retentie significant ten opzichte van volledig gratis (Gneezy & Rustichini, 2000: het verschil tussen "gratis" en "bijna gratis" is groter dan tussen "bijna gratis" en "duurder").

### Architecturale implicaties

**A7.1 Multi-tenant datamodel.** Elke leerling heeft een geïsoleerd learner model. De knowledge graph is gedeeld (read-only voor de applicatie), het learner model is per-user.

**A7.2 Authenticatie.** OAuth 2.0 / OpenID Connect. Geen eigen wachtwoord-opslag. Overweeg inloggen via school-account (Entree Federatie / SURFconext) voor de primaire doelgroep.

**A7.3 Subscription state.** Een `subscription` entity per user met: plan (free/basic/premium), status (active/trial/expired), examenjaar (bepaalt welk pensum actief is), en startdatum.

**A7.4 Data residency.** Alle learner data wordt opgeslagen binnen de EU (AVG). De knowledge graph bevat geen persoonsgegevens.

**A7.5 Hosting.** Start met een single-server deployment (VPS, bijv. Hetzner EU). De architectuur moet schaalbaar zijn naar container-based deployment (Docker Compose → Kubernetes) maar hoeft dat niet vanaf dag één te zijn.

**A7.6 Privacy by design.** Leerling-accounts voor minderjarigen vereisen ouderlijke toestemming. De data-export en verwijderfunctionaliteit (AVG recht op vergetelheid) wordt van begin af aan ingebouwd.

---

## Samenvatting: beslissingsmatrix

| # | Vraag | Beslissing | Prioriteit |
|---|---|---|---|
| 1 | Validatiepad | Staatsexamen (CE + college-examen) | Fundamenteel — bepaalt scope |
| 2 | Culturele laag | Volledig conform syllabi + verrijking | Fase 1 (graph) |
| 3 | Grieks alfabet | Aparte onboarding-subgraph | Fase 1 (graph) |
| 4 | Metriek | Volledig als subgraph | Fase 1 (graph) |
| 5 | Productieve oefeningen | Ja, als trainingsmiddel | Fase 3 (oefeningen) |
| 6 | Mondelinge simulatie | Ja, als aparte module | Fase 5+ |
| 7 | Businessmodel | SaaS-ready, multi-tenant | Fase 0 (fundament) |

---

## Aanvullende keuzes die uit de discussie volgen

### Keuze 8: Pensum als jaarlijks wisselende module

Het CE-pensum wisselt jaarlijks van auteur. De cyclus is voorspelbaar en wordt jaren vooruit bekendgemaakt:

**Grieks:** Homerus (Odyssee) 2026 → Herodotus 2027 → Plato 2028 → Euripides (Helena) 2029 → Homerus (Ilias) 2030

**Latijn:** Filosofie (Seneca/Cicero) 2026 → Cicero retor 2027 → Ovidius 2028 → Seneca/Cicero/Erasmus 2029 → Vergilius 2030

**Beslissing:** Het pensum wordt gemodelleerd als een **jaarlijks te activeren module** bovenop de vaste graph. De leerling selecteert bij inschrijving het beoogde examenjaar, en het systeem activeert de bijbehorende pensum-module met auteurspecifieke cultuurknopen en het leesprogramma.

**Implicatie A8.1:** De pensum-module is een apart datamodel dat per examenjaar wordt onderhouden. Dit is de voornaamste jaarlijkse onderhoudslast.

### Keuze 9: Inputmethode voor Griekse en Latijnse tekst

**Beslissing:** Het frontend biedt een **gecombineerde oplossing**: een soft keyboard voor polytonic Grieks (met visuele toetsen voor spiritus, accenten, iota subscriptum) plus support voor fysieke keyboard-input via standaard Unicode-methoden. Voor Latijn volstaat het standaard toetsenbord met eventueel macron-ondersteuning voor lange klinkers (niet strikt nodig voor het examen, maar nuttig als leerhulp).

**Implicatie A9.1:** De frontend-component voor tekst-input wordt een herbruikbare React-module die in alle oefentypen wordt ingezet.

### Keuze 10: Taal van de interface

**Beslissing:** De interface is **volledig in het Nederlands**. Grammaticale terminologie wordt in het Nederlands aangeboden (naamval, werkwoordstijd, etc.) met de Latijnse/Griekse term als tooltip/annotatie. Dit sluit aan bij hoe het op Nederlandse scholen wordt onderwezen en hoe het CE-correctiemodel is opgesteld.

**Implicatie A10.1:** De knowledge graph bevat per knoop zowel `titel_nl` als `titel_lat`/`titel_grc` voor de grammaticale terminologie.

---

### Keuze 11: Procedurele knopen (type P) en de POLMO-strategie

**Vraag:** Wijkunnenmeer (Reijgwart) noemt vier oorzaken van slecht vertalen; drie ervan — woordenschat, grammaticakennis, kunnen ontleden — vallen onder de bestaande knoop-types V, G en I. De vierde, het ontbreken van een *systematische vertaalmethode*, heeft geen plek in het model. Hoe modelleren we de vertaalprocedure zélf als leerbare en diagnoseerbare eenheid?

**Beslissing:** Een vijfde knoop-type **P (Procedure/Strategie)** naast G/V/C/I, plus een nieuw edge-type **`procedure_step`** dat een *volgordelijke* stap binnen een procedure uitdrukt — onderscheiden van `prerequisite`, dat "moet beheerst zijn vóór" betekent. De canonieke vertaalstrategie **POLMO** (Persoonsvorm → Onderwerp → Lijdend voorwerp → Meewerkend voorwerp → Overige) is de eerste procedure-DAG: zes `shared` knopen (één INTRO plus vijf stappen), met `procedure_step`-edges voor de volgorde en reguliere `prerequisite`-edges van de relevante grammatica-knopen naar elke stap.

**Onderbouwing:** Een leerling kan alle naamvallen kennen en tóch structureel verkeerd vertalen door zonder strategie te werken ("Lego-vertalen"). Door de stappen als knopen te modelleren ontstaat (1) diagnostiek per stap, (2) scheduling per stap, en (3) een aangrijppunt voor misconceptie-detectie (M1-02), die kan terugslaan op een specifieke POLMO-stap.

**Architecturale implicaties:**
- **A11.1** `NodeType` krijgt waarde `P`; `procedure_step` wordt opgenomen in `ACYCLIC_EDGE_TYPES` (een procedure is per definitie acyclisch) en in de ID-schema-validatie (`SHA-P-VERTAAL-POLMO-PV`, etc.).
- **A11.2** Een procedure-validator eist dat elke `procedure_step`-component een *lineair pad* is: geen vertakking, exact één start, exact één eind. Een malformed procedure (vertakking, dubbele start) is een harde validatiefout.
- **A11.3** POLMO is `shared` (geldt voor Latijn én Grieks). De grammatica-ankers verwijzen voorlopig naar de Latijnse `SYNT-FUNCTIE`-knopen (Latijn = instaptaal). Per-taal verfijning — eigen `LAT-P-`/`GRC-P-`-ketens en Griekse ankers — is bewust uitgesteld naar een vervolgstory.
- **A11.4** Stap-knopen krijgen vooralsnog geen eigen items; didactische content bestaat enkel voor de INTRO-knoop. Items per stap en automatische POLMO-stap-foutclassificatie (uitbreiding van F2-04) volgen in latere stories.

---

## Evidence-based keuzes (uit het literatuuronderzoek, juni 2026)

> Keuzes 12 t/m 16 vloeien voort uit `docs/LITERATUURONDERZOEK_LEERBENADERING.md`. Implementatie loopt via **Spoor L** in `stories/EPICS.md`. (Keuze 11 — "Procedurele knopen" uit epic M1 — staat hierboven, los van deze evidence-based cluster.)

### Evidence-based uitgangspunten (prioritering)

De literatuur geeft niet alleen aan *wat* werkt, maar ook waar je energie wél en niet in moet steken. Deze uitgangspunten zijn leidend bij planning en review:

- **Méér prioriteit:** spaced repetition en retrieval practice (de twee best-gerepliceerde, goedkoopste hefbomen); meetbaarheid van de eigen effectgrootte; het onderscheid receptief/productief; het benutten van de graph-structuur in het learner model.
- **Minder prioriteit (niet vroeg over-optimaliseren):** de exacte keuze van het SR-algoritme (SM-2 volstaat tot er data is; FSRS als latere upgrade — het verschil wordt pas meetbaar bij honderden leerlingen); geavanceerde BKT-varianten (vanille-BKT is een prima, interpreteerbare start).
- **Geen prioriteit (parkeren/schrappen):** pure Comprehensible Input/Krashen als methode (omstreden én misaligned met het examen — hybride blijft leidend); deep/neurale knowledge tracing (voortijdig, vereist big data, levert interpreteerbaarheid in).

### Keuze 12: Meetbaarheid en effectgrootte als first-class uitgangspunt

**Vraag:** Hoe toetst het project zijn eigen centrale claim (efficiënter leren) en het gat in de literatuur (geen evidence voor klassieke talen)?

**Beslissing:** Het systeem legt vanaf de vroegste fase retentie-, tijd- en mastery-data per leerling vast, met een baseline-meting bij intake en de mogelijkheid tot A/B-vergelijking van leerstrategieën. De pilot tegen het staatsexamen is de objectieve externe toets.

**Onderbouwing:** Bloom's "2 sigma" is nooit gerepliceerd en realistische effecten liggen rond 0,2–0,8 SD; zonder eigen meting blijft "efficiënter" een aanname. Door dit te meten verandert de grootste zwakte (dunne evidence voor Latijn/Grieks) in een onderscheidende sterkte: het project genereert die evidence zelf.

**Architecturale implicaties:**
- **A12.1** Een meetlaag die per `ItemResponse`/`SessionRecord` voldoende vastlegt om retentie over tijd en effectgrootte te berekenen (zie story L1-01).
- **A12.2** Een baseline-/intakemeting die als nulpunt dient voor voortgangsrapportage (L1-02).
- **A12.3** Een experiment-/variant-framework zodat leerstrategie-parameters (bijv. spacing-schema, scaffolding-drempel) controleerbaar gevarieerd kunnen worden (L1-03).

### Keuze 13: Receptieve en productieve beheersing apart modelleren

**Vraag:** Volstaat één masterygetal per knoop?

**Beslissing:** Nee. Receptieve en productieve beheersing worden apart bijgehouden per knoop.

**Onderbouwing:** Spacing en retrieval leveren receptieve kennis betrouwbaar op, maar productieve beheersing (actief vervoegen/verbuigen) vereist meer en moeilijker oefening (Shintani, 2015). `Item` heeft al een `richting`-veld (receptief/productief), maar `KnoopState.posterior_mastery` is één float — die asymmetrie kan het systeem nu niet zien.

**Architecturale implicaties:**
- **A13.1** `KnoopState` krijgt gescheiden receptieve en productieve mastery; de BKT-update routeert op `Item.richting` (L2-01).
- **A13.2** De scheduler en readiness-gates kunnen per richting drempels hanteren; productieve oefening wordt als consolidatie ingezet zodra receptieve beheersing er is (sluit aan op keuze 5).

### Keuze 14: Learner model als migreerbare laag met individuele parameters

**Vraag:** Is BKT de definitieve keuze voor het learner model?

**Beslissing:** BKT is de *start* (interpreteerbaar, werkt met weinig data), maar de learner-model-laag wordt achter een interface geabstraheerd zodat migratie naar PFA/logistische of graph-aware modellen mogelijk is. De graph-structuur (prerequisite/transfer-edges) wordt actief benut, en er komen learner-niveau parameters naast skill-niveau parameters.

**Onderbouwing:** In eerlijke vergelijkingen presteren PFA en — bij grote datasets — graph-aware modellen vaak beter dan vanille-BKT, dat skills onafhankelijk modelleert en transfer mist. Juist de combinatie graph + per-knoop-tracing is waar de literatuur winst ziet (prerequisite-driven KT). Bij (jonge) taalleerders wegen individuele verschillen vaak zwaarder dan het exacte interval (Kasprowicz, 2019; geïndividualiseerde BKT, Yudelson, 2013).

**Architecturale implicaties:**
- **A14.1** Een `LearnerModelStrategy`-interface met BKT als eerste implementatie; predictiemodel inplugbaar (L2-02).
- **A14.2** De BKT-update mag prior/transitie bijstellen op basis van mastery van prerequisite-/transfer-buren in de graph (L2-02).
- **A14.3** Learner-niveau parameters (bijv. individuele leersnelheid) naast de skill-parameters (L2-03).

### Keuze 15: Worked examples en faded scaffolding als oefentype

**Vraag:** Dekken de huidige oefentypen de effectiefste didactische patronen?

**Beslissing:** Voeg een uitgewerkt-voorbeeld-oefentype met afnemende steun (faded scaffolding) toe aan de oefeningen-taxonomie.

**Onderbouwing:** Meerdere ITS-meta-analyses noemen *worked examples* als belangrijkste moderator van effectiviteit. De huidige `ItemType`-waarden (herkenning/productie/analyse/synthese/contextueel) bevatten geen uitgewerkt voorbeeld met geleidelijk wegvallende steun. Dit sluit naadloos aan op de scaffolding-aanpak voor teksten (keuze in briefing §3.6).

**Architecturale implicaties:**
- **A15.1** `ItemType` uitgebreid met een `worked_example`-variant; een item kan een reeks stappen met instelbaar steunniveau bevatten (L3-01).
- **A15.2** De scheduler zet worked examples in bij de introductie van een knoop en faseert ze uit naarmate de mastery stijgt.

### Keuze 16: Motivatie- (metacognitieve illusie) en equity-laag

**Vraag:** Hoe voorkomen we afhaken en averechtse effecten voor zwakkere leerlingen?

**Beslissing:** Het systeem krijgt (a) een motivatielaag die expliciet uitlegt waarom effectieve oefening zwaar voelt, gekoppeld aan voortgangsvisualisatie, en (b) expliciete equity-waarborgen voor zwakkere presteerders.

**Onderbouwing:** Effectieve, "desirable difficult" oefening wordt door leerlingen systematisch onderschat (metacognitieve illusie) — een reëel afhaakrisico (briefing-risico 7.4). Daarnaast waarschuwt onderzoek dat ITS de gemiddelde leerling méér helpen dan zwakke presteerders, terwijl bijles/remediatie juist de secundaire doelgroep is.

**Architecturale implicaties:**
- **A16.1** Een UX-laag met "waarom dit werkt"-uitleg en de groen kleurende heat map als tegenwicht (L3-02).
- **A16.2** Equity-waarborgen: extra scaffolding-drempels en langzamere readiness-gates voor leerlingen met lage mastery-trajecten, zodat het systeem niet versnelt waar het zou moeten consolideren (L3-03).

---

### Keuze 17: Misconcepties als first-class object (Bug Library)

> Hoort bij **Spoor M1** (verlengstuk van Keuze 11 — POLMO), niet bij de evidence-based cluster 12–16. Numeriek volgt het op Keuze 16.

**Vraag:** De graph kent alleen *positieve* kennis (wat een leerling moet weten). Maar twee leerlingen met identieke BKT-scores kunnen verschillen in of ze daadwerkelijk *ontleden* dan wel "Lego-vertalen" (woorden op elkaar stapelen zonder de zinsbouw te lezen). Op makkelijke stof levert dat dezelfde uitkomst; op moeilijke stof loopt de Lego-vertaler exponentieel sneller stuk. Hoe maken we zo'n systematisch *fout* patroon expliciet, diagnoseerbaar en aanpakbaar?

**Beslissing:** Een **`Misconception`-model** als first-class attribuut op `Node` (`known_misconceptions: list[Misconception]`), volgens het **Bug Library**-patroon uit de intelligent-tutoring-literatuur: naast "wat moet de leerling kennen" ook "welke fouten maken leerlingen systematisch, en hoe diagnosticeer je ze". Elke misconceptie heeft een `code`, mensleesbare naam/beschrijving, `diagnostic_items` (item-IDs die de fout blootleggen) en `remediation_nodes` (knopen die geactiveerd worden bij detectie). De eerste misconceptie is **`LEGO_VERTALEN`**, gekoppeld aan de vertaal-integratieknopen (I-VERT, LAT+GRC), met de POLMO-DAG (Keuze 11) en de morfologie-conceptknopen als remediatie.

**Onderbouwing:** Wijkunnenmeer's praktijk laat zien dat veel struikelgevallen niet door kennis-*tekort* komen maar door een fout patroon dat de leerling consequent toepast. Een misconceptie-laag scheidt deze twee oorzaken — en geeft de scheduler een gericht aangrijppunt (terugslaan op ontleden vóór vertalen) in plaats van generiek "meer oefenen".

**Detectie (regelgebaseerd, uitlegbaar):** `detect_lego_translator()` vergelijkt mastery *over knoop-categorieën* heen, afgeleid uit node-ID-patronen: woordenschat F01–F02 sterk (`avg_V ≥ 0.70`), morfologie zwak (`avg_G_morf < 0.50`), vertalen zwak (`avg_I_vert < 0.40`). Alle drie waar → profiel actief. Drempels staan in één `LegoDetectorConfig` (frozen dataclass), zodat ze op pilot-data herkalibreerd worden zónder codewijziging. Bij onvoldoende waarnemingen per categorie vuurt de regel niet (geen vals-positief bij "nog nooit vertaald").

**Architecturale implicaties:**
- **A17.1** `Misconception` met `code`-validator (uppercase ASCII + underscore). Cross-references (`diagnostic_items`, `remediation_nodes`) worden in `validate_graph` (stap 11, `validate_misconceptions`) gecontroleerd op bestaan — cross-file via de loader-resolutie.
- **A17.2** Detectie levert een `MisconceptionFlag` (drie scores + reden), niet enkel een `bool`, zodat een mentor-dashboard of sessie-summary het kan tonen.
- **A17.3** Scheduler-integratie is een *vermenigvuldiging* op de bestaande urgentiescore (`apply_lego_boost`, factor 1.5–2.0, default 1.75), géén harde override — andere urgenties blijven gerespecteerd. Doelknopen: POLMO-stappen, morfologie-concepten en de diagnose-item-knopen.
- **A17.4** Leerling-feedback is jargonvrij: de sessie-summary toont "Je vertalingen lopen vooruit op je grammatica…", nooit het technische label "Lego-vertaler".

**Nieuwe misconcepties toevoegen (proces):** (1) definieer een `Misconception` met unieke `code` en koppel hem aan de knopen waar de fout zich manifesteert; (2) voeg `diagnostic_items` toe die de fout voorspelbaar blootleggen, en `remediation_nodes` die hem corrigeren; (3) `validate_graph` borgt dat alle verwijzingen resolven; (4) schrijf een detector-functie die op BKT-aggregaten werkt, met drempels in een eigen config-object; (5) kalibreer die drempels op pilot-data. Een volledige Bug Library (bijv. "alleen werkwoord uit de zin pikken", "tijd negeren") is bewust uitgesteld — `LEGO_VERTALEN` is het startpunt (M1-02).

---

### Keuze 18: Bijspijker- vs. staatsexamen-modus

> Hoort bij **Spoor M1**. Numeriek volgt het op Keuze 17. (De story vroeg
> om "Keuze 13", maar dat nummer is al bezet door receptief/productief.)

**Vraag:** De briefing positioneerde als primaire doelgroep VWO-leerlingen
die de klassieke talen *niet* op school kunnen volgen, met het
staatsexamen als doel. Wijkunnenmeer's praktijk laat een grotere, urgentere
doelgroep zien: gymnasiasten die de talen *wél* volgen maar dreigen te
zakken. Hun doel is niet een examen over jaren, maar **bij blijven met de
klas** — een fundamenteel andere optimalisatiefunctie. Hoe bedienen we beide?

**Beslissing:** Twee gebruikersmodi met aparte planners.

| Aspect | Staatsexamen | Bijspijker |
|---|---|---|
| Tijdshorizon | jaren | weken |
| Doel | beheersing eindtermen | bij met de schoolmethode |
| Sequencing | graph + examenjaar | methode + hoofdstuk |
| "Klaar" | examen gehaald | doelset ≥ drempel |
| Cool-down | lange-termijn SR | vertaling uit huidig hoofdstuk |

`User.modus` (`STAATSEXAMEN | BIJSPIJKER`) plus per taal
`huidige_methode_*` + `huidige_hoofdstuk_*`. De `BijspijkerPlanner`
repliceert WKM's "overhoren": doelset = methode-hoofdstuk-knopen +
prerequisite-closure; diagnose = wat nog niet beheerst/geverifieerd is;
versneld tempo (3-5 nieuwe knopen/sessie) en elke sessie afgesloten met
een vertaling uit het huidige hoofdstuk.

**Onderbouwing:** Voor een leerling die dreigt te zakken is
lange-termijnretentie secundair aan *nu* het cijfer omhoog krijgen. De
optimalisatie maximaliseert de fractie van de doelset die snel groen
wordt; retentie mag in deze modus iets lager zijn. Dit opent het systeem
voor de doelgroep met de hoogste urgentie en betalingsbereidheid.

**Architecturale implicaties:**
- **A18.1** `Modus`-default is `STAATSEXAMEN` (technische backward-compat:
  vóór M1-03 opgeslagen accounts deserialiseren ongewijzigd). De
  product-intentie "nieuwe accounts zijn bijspijker" leeft in de
  onboarding-flow, die modus + methode + hoofdstuk samen zet — zo is de
  model-validator (BIJSPIJKER vereist methode+hoofdstuk voor ≥1 taal)
  altijd vervulbaar. Geen apart migratiescript nodig.
- **A18.2** De methode-mapping blijft in het bestaande
  `data/methode_mapping.json` (niet de per-methode-directory uit de
  story), zodat de werkende intake-route niet breekt.
  `validate_methode_mapping` borgt knoop-bestaan, geen duplicaten en
  opeenvolgende hoofdstukken.
- **A18.3** Twee endpoints: `POST /intake/bijspijker` (zet modus + plan,
  `reset_priors=False` voor een hoofdstuk-bump zonder voortgangsverlies)
  en `GET /progress/bijspijker`. Sessie-endpoints blijven ongewijzigd; de
  planner wordt op `User.modus` geselecteerd.
- **A18.4** De `BijspijkerPlanner` is puur (geeft een plan terug); de
  scheduler vertaalt intro-tempo en cool-down-knopen naar een sessie.

---

## Edge-type-beleid

De graph kent drie edge-types (`prerequisite`, `enrichment`, `transfer`). Voor de acycliciteitseis geldt één regel:

- **`prerequisite` en `enrichment` moeten samen acyclisch zijn** — zij leggen een leervolgorde op; een cyclus zou betekenen dat een knoop (indirect) zijn eigen voorwaarde is.
- **`transfer` mag cyclisch zijn** — transfer-edges zijn bidirectionele, cross-linguïstische verbanden (LAT ↔ GRC) die geen volgorde opleggen.

Dit beleid staat op één plek in de code: de constante `ACYCLIC_EDGE_TYPES` in `graph/validation.py`. Cycle-detectie en topologische sortering filteren de graph via `acyclic_subgraph(...)` op precies die set. Een vierde edge-type toevoegen kost daardoor één regel: opnemen in of weglaten uit `ACYCLIC_EDGE_TYPES`. (Afgeleid uit de graph-methodologie-reflectie; geïmplementeerd in story OS-09.)

---

## Architectuurconsequenties — samenvatting voor Claude Code

De volgende technische requirements vloeien direct voort uit de bovenstaande keuzes en moeten vanaf fase 0 worden meegenomen:

### Datamodel (fase 0)

```
User
├── id: UUID
├── email: str
├── auth_provider: str (OAuth)
├── subscription: Subscription
├── examenjaar_ltc: Optional[int]
├── examenjaar_gtc: Optional[int]
├── created_at: datetime
└── learner_model: LearnerModel

Subscription
├── plan: enum (free, basic, premium)
├── status: enum (trial, active, expired)
├── started_at: datetime
└── expires_at: Optional[datetime]

LearnerModel
├── user_id: UUID
├── knoop_states: dict[knoop_id → KnoopState]
└── session_history: list[SessionRecord]

KnoopState
├── knoop_id: str
├── posterior_mastery: float  # P(L) uit BKT
├── easiness_factor: float   # SM-2
├── interval_days: float     # SM-2
├── repetitions: int
├── last_review: Optional[datetime]
├── last_response: enum (correct, incorrect, slow_correct)
└── item_history: list[ItemResponse]
```

### Knowledge Graph schema (fase 0-1)

```
KennisKnoop
├── id: str              # bijv. "LAT-G-NOM-1D-SG"
├── type: enum (G, V, C, I)
├── taal: enum (lat, grc, shared)
├── titel_nl: str
├── titel_terminologie: Optional[str]  # Latijnse/Griekse term
├── beschrijving: str
├── bloom_niveau: enum (kennis, begrip, toepassing, analyse, synthese)
├── fase: enum (onderbouw_1, onderbouw_2, onderbouw_3, bovenbouw_4, bovenbouw_5, bovenbouw_6)
├── toetsbaar: bool       # verschil CE/SE-stof vs. verrijking
├── pensum_jaren: list[int]  # in welke examenjaren is dit relevant
├── cevte_referentie: Optional[str]
└── items: list[Item]

PrerequisiteEdge
├── source_id: str
├── target_id: str
├── type: enum (prerequisite, enrichment, transfer)
└── encompassing_weight: float  # 0.0 – 1.0

Item
├── id: str
├── knoop_ids: list[str]
├── type: enum (herkenning, productie, analyse, synthese, contextueel)
├── richting: enum (receptief, productief)  # nieuw: keuze 5
├── moeilijkheid_initieel: float  # IRT b-parameter
├── discriminatie_initieel: float # IRT a-parameter
├── verwachte_tijd_sec: int
├── stimulus: str | dict         # tekst, of structured (audio, afbeelding)
├── antwoord: str | list[str]    # correct antwoord(en)
├── feedback: str
└── bron: enum (handmatig, llm_gegenereerd, authentiek)
```

### Frontend requirements (fase 4)

- Polytonic Greek keyboard component (React)
- Macron-input voor Latijn (optioneel, als leerhulp)
- Timer-gebaseerde sessie-interface (30 min default, configureerbaar)
- Progress heat map (graph visualisatie met kleurcodering per beheersingsgraad)
- Pensum-lezer met annotatie-ondersteuning
- Responsive design (desktop + tablet; mobiel is secondary)

### Privacy en compliance (doorlopend)

- AVG-conforme dataverwerking, opslag binnen EU
- Ouderlijke toestemming voor accounts < 16 jaar
- Data-export (JSON) en volledige verwijdering op verzoek
- Geen tracking van gedrag buiten de leercontext
- LLM-calls (oefeningen-generatie, mondelinge module) via EU-residency providers waar mogelijk

---

*Dit document wordt bijgewerkt bij nieuwe ontwerpkeuzes. Versiebeheer via Git.*
