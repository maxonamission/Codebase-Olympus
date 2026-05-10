# Starterpakket — een nieuw graph-gedreven project opzetten

## Wat is dit?

Dit pakket bundelt de geleerde lessen uit Codebase-Olympus (Gymnasium Classica) tot een set documenten waarmee je een **nieuw project op een totaal ander onderwerp** kunt opstarten zonder elke architectuurvraag opnieuw uit te vechten. Het is geschreven voor één- of tweepersoonsteams die met Claude Code (of vergelijkbare AI-assistent) bouwen.

Het uitgangspunt: je hebt een onderwerp waar een **typed graph** een centrale rol in speelt. Of dat onderwerp nu sportdeelname-beleid is, persoonlijke vermogens, vogelidentificatie, mediageletterdheid of huisartsenrichtlijnen — de werkwijze is grotendeels gelijk; alleen de inhoud verschilt.

## Twee projectarchetypes

Een belangrijk onderscheid vooraf: niet elk graph-gedreven project heeft hetzelfde doel. In de praktijk zien we (minstens) twee archetypes terug, en je kiest **expliciet** welk type je bouwt voor je begint. De methodologie en de ontwikkelstraat zijn voor beide identiek; de bovenliggende lagen verschillen.

### Archetype A — Graph als skelet voor persoonlijke beheersing

**Voorbeeld:** Codebase-Olympus / Gymnasium Classica.

**Doel:** een individuele gebruiker (leerling, professional, kandidaat) helpt het corpus onder de knie krijgen. De graph beschrijft *wat er te leren valt*; per gebruiker hou je *wat is al beheerst* bij.

**Bovenop de graph komt:** een leerlingmodel (per-gebruiker-staat), BKT/SM-2/IRT-achtige technieken, oefenitems met antwoorden, een scheduler die het volgende item kiest, sessies, voortgangsrapportage.

**Edges domineren:** prerequisites, enrichment, transfer (cross-domain analogie). Vrijwel altijd acyclisch in de hoofdas.

**Hoofdstuk in dit pakket:** §03 (adaptieve laag) is voor jou kern. §02 graph-blueprint past volledig.

### Archetype B — Graph als model van een domein voor hypothesevorming en interventie-simulatie

**Voorbeeld:** Graaf Zeppelin / sportdeelname-beleidsmodel.

**Doel:** een ontwerper of beleidsmaker krijgt grip op hoe een domein werkt. De graph is een *causaal of structureel model van het domein zelf*; eindgebruikers verkennen, vragen "wat als ik X verander?" en formuleren hypothesen op basis van context en cases. Er is geen "leerling" en geen mastery-tracking.

**Bovenop de graph komt:** een propagatie- of simulatie-engine, sliders/parameters voor interventies, scenario's, vergelijkingen, eventueel onzekerheidsranges en literatuurverwijzingen op edges.

**Edges domineren:** structureel, mediërend, social-regulatory, feedback, moderator. **Feedback-lussen zijn essentieel** — de graph is dus niet globaal acyclisch.

**Hoofdstuk in dit pakket:** §02 graph-blueprint past volledig (zie vooral §A "graph-vorm" en §I "tijdsdimensie"). §03 adaptieve laag **sla je over**. In §05 bootstrap volg je het Zeppelin-pad in week 4.

### Combinatie en variatie

- Sommige projecten zijn **mengvormen** (bv. een coachings-tool waarin én een domeinmodel én individuele voortgang zit). Bouw beide lagen apart en koppel ze pas in een overlay; meng ze niet in één model.
- Sommige projecten zijn **geen van beide** — bv. een puur descriptief netwerk (citatiekaart, organisatiekaart). Daar past §02 maar niet §03 of §05's leerling-week. De methodologie (`graph-methodology.md`) is je belangrijkste anker.

Bepaal in dag 1 welk archetype je bouwt; documenteer het in je BRIEFING. Latere migratie van archetype A naar B (of andersom) is duur omdat je leerlingmodel óf je simulatie-engine moet weggooien.

## Wat zit erbij?

| Bestand | Onderwerp |
|---------|-----------|
| `README.md` | Deze leeswijzer |
| `01-werkwijze-en-principes.md` | Hoe je werkt: kleine stappen, taalconventies, story-driven |
| `02-graph-blueprint.md` | Knowledge graph: typering, ID-schema, persistence, validatie |
| `03-adaptieve-laag.md` | *Alleen bij leerdomeinen:* wanneer BKT, SM-2, IRT zin hebben |
| `04-ontwikkelstraat-en-stories.md` | Zes-lagen kwaliteitsstraat + story-workflow als blauwdruk |
| `05-bootstrap-en-ontwerpkeuzes.md` | Eerste maand stap-voor-stap + sjabloon voor ontwerpkeuzes |
| `06-antipatronen-en-checklist.md` | Concrete misstappen + finale checklist |

Daarnaast verwijs je gewoon door naar de oorspronkelijke documenten, die al generiek genoeg zijn om mee te nemen:

| Brondocument in Olympus | Status |
|-------------------------|--------|
| `docs/graph-methodology.md` | **Direct overneembaar** — acht conventies + appendix tijdsdimensie. Het hart van de methodologie. |
| `docs/ontwikkelstraat-uitleg.md` | **Direct overneembaar** — long-read over de zes lagen kwaliteitsstraat. |
| `docs/voor-graaf-zeppelin/actieplan.md` | **Voorbeeld archetype B** — laat zien hoe je de methodologie + ontwikkelstraat post-hoc toepast op een Zeppelin-achtig domeinmodel. Lees als demo, niet als template. Bevat ook concrete lessen over `time_lag`-velden, per-edge-type-cycle-checks en migratie-paden die voor archetype B kernrelevant zijn. |

## Hoe gebruik je dit pakket?

### Pad A — je hebt al een idee

1. Lees `01-werkwijze-en-principes.md` (10 min) voor de mentale modus.
2. Schrijf je eigen `BRIEFING.md` op basis van het sjabloon in `05-bootstrap-en-ontwerpkeuzes.md` §1.
3. Schrijf je `ONTWERPKEUZES.md` met het sjabloon in `05-bootstrap-en-ontwerpkeuzes.md` §2.
4. Beslis op basis van `02-graph-blueprint.md` welke conventies je overneemt en welke je aanpast.
5. Volg de bootstrap-volgorde in `05-bootstrap-en-ontwerpkeuzes.md` §3 voor de eerste maand.
6. Loop af en toe `06-antipatronen-en-checklist.md` langs als sanity-check.

### Pad B — je verkent of het idee überhaupt past

1. Lees alleen `02-graph-blueprint.md` (graph-vorm) en `03-adaptieve-laag.md` (alleen als leerdomein).
2. Beantwoord de vragen onderaan elk hoofdstuk.
3. Als de antwoorden "ja, ja, ja" zijn → ga naar Pad A. Anders: noteer welke conventie níét past en waarom — dat scheelt je later twijfel.

### Pad C — overdracht naar iemand anders

1. Geef deze hele map plus de drie brondocumenten aan de overnemer.
2. Voeg een eigen `00-context.md` toe met: wat het onderwerp is, waarom dit project, wie de doelgroep is, en wat de huidige status is.
3. Laat overnemer eerst Pad B doorlopen voordat hij/zij begint te bouwen.

## Wat dit pakket bewust **niet** doet

- **Geen template-repo of cookiecutter.** Olympus is geen template; dit pakket is een gedeelde taal. Een copier-template is een aparte stap die je *na* twee succesvolle projecten zet, niet ervoor (zie anti-patroon "voortijdige extractie" in `06-antipatronen-en-checklist.md`).
- **Geen library of basisklasse.** Overnemen vraagt handwerk per project. Dat is een feature: het dwingt je elk project tegen je eigen onderwerp te toetsen.
- **Geen UI- of frontend-keuzes.** Frontend is domein-afhankelijk en valt buiten de gedeelde methodologie.
- **Geen LLM-architectuur.** Een LLM-laag is een aparte discipline; deze starterpakket gaat over het datafundament eronder.
- **Geen domeininhoud.** Dit pakket bevat geen voorbeeld-knopen, geen voorbeeld-vocabulaire, geen voorbeeld-cultuurnetwerk. Die maak je zelf.

## Mentale waarschuwingen vooraf

Drie dingen waar nieuwe projecten op stuk lopen, terwijl ze met deze methodologie te voorkomen zijn:

1. **Bouwen voor de schaal van morgen.** Bij 50 knopen heb je geen graphdatabase nodig, geen distributed systeem, geen microservices. Begin met SQLite + JSON + in-memory NetworkX. Schaal komt pas als probleem wanneer het écht een probleem is.
2. **Graph-vóór-domein.** Verleidelijk: eerst de loader perfect maken, dan inhoud invoeren. Beter: 50 knopen met de hand intikken in een proof-of-concept JSON, daarna de loader er omheen bouwen. Inhoud botst op aannames die je in een leeg systeem nooit zou tegenkomen.
3. **Geen edge-typering.** Eén soort relatie ("X hangt samen met Y") lijkt eenvoudig, maar zodra je een tweede semantiek nodig hebt — bv. "X versterkt Y" naast "X is voorwaarde voor Y" — moet je terug naar de tekentafel. Type je edges vanaf knoop 1.

Lees `06-antipatronen-en-checklist.md` voor de volledige lijst.

## Versie

Versie 1.0 — opgesteld door Codebase-Olympus, mei 2026. Pakket is een momentopname; nieuwe lessen die opdoemen in vervolgprojecten kunnen terug landen in de brondocumenten (`graph-methodology.md` en `ontwikkelstraat-uitleg.md`) zonder dit pakket te wijzigen.
