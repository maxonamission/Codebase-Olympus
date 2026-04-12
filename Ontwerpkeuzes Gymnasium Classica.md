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
