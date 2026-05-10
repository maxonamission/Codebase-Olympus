# 01 — Werkwijze en projectprincipes

Voordat je over architectuur of inhoud nadenkt, leg je de werkwijze vast. Dit bespaart conflict later: de meeste discussies in een AI-geassisteerd project gaan niet over "wat doen we?" maar over "hoe leveren we het op?". Onderstaande zes principes zijn de stille fundering onder Codebase-Olympus en blijken in de praktijk goed transferbaar.

## Principe 1 — Klein leveren, vaak committen

**Regel.** Elke commit doet één ding. Eén story = één serie commits, niet één commit per story. Push na elke afgeronde story; wacht niet tot het einde van de sessie.

**Waarom.** AI-sessies hebben idle timeouts. Een sessie die crasht halverwege een grote ongecommitte wijziging is verloren werk. Bovendien lezen kleine commits beter terug — ze beschrijven wat er gebeurde, niet alleen wat er nu is.

**Concreet.**
- Maximaal ~150 regels per commit (richtlijn, geen wet).
- Eén logisch onderwerp per commit. "Refactor + bugfix + nieuwe feature" → drie commits.
- Conventionele commits met onderwerp in **de projecttaal** (zie principe 2). `feat: voeg cycle-check per edge-type toe`, niet `add cycle check by edge type`.

**Anti-patroon:** "ik commit pas als alles werkt." Resultaat: een commit van 3000 regels waarvan niemand meer weet welke wijziging welk effect had.

## Principe 2 — Eén taal voor documentatie, één taal voor code

**Regel.** Documentatie, story-titels, commit-messages: in **de domeintaal van het project** (Nederlands voor Olympus, kies bewust voor je eigen project). Code (variabelen, functies, klassen, docstrings, comments): **Engels**.

**Waarom.** Documentatie en stories worden gelezen door domeinexperts (in Olympus' geval: classici); zij denken niet in het Engels. Code wordt gelezen door ontwikkelaars en hun tooling; zij dénken in het Engels en de meeste libraries zijn dat ook. Mengen doet beide kanten kwaad.

**Implementatie.**
- CLAUDE.md vermeldt dit expliciet zodat de AI niet onbewust hertaalt.
- Type-hints zijn onderdeel van de code → Engels (`KennisKnoop` is een grijs gebied; in Olympus bewust gehouden omdat de term diepste betekenis heeft in het Nederlands).
- Tests die domeinkennis controleren mogen Nederlandse stringliterals bevatten (zoals `assert vertaling == "vader"`).

**Voor je nieuwe project:**
- Beslis in dag één in welke taal documentatie wordt geschreven.
- Beslis voor de paar grijze gevallen (modelnaam, enum-waardes, story-IDs) wat je doet — en houd je eraan.

## Principe 3 — Schrijf eerst de structuur, dan de code

**Regel.** Geen implementatie voordat het datamodel en de interfaces beschreven zijn. Voor nieuwe componenten: eerst Pydantic-modellen + functie-signatures, dan de body.

**Waarom.** Een verkeerde signature is in een AI-sessie binnen seconden door je hele codebase gepropageerd. Een verkeerde implementatie is lokaal en oplosbaar. Tijd-investering aan de voorkant betaalt zich tienvoudig terug.

**Concrete werkwijze.**
1. Beschrijf in twee alinea's wat het component doet en wat de in/output is.
2. Schrijf de Pydantic-modellen (zonder methods).
3. Schrijf de publieke functie-signatures met docstrings, body = `raise NotImplementedError`.
4. Schrijf één of twee tests die de signature gebruiken.
5. Implementeer de bodies.

Stap 1-4 is meestal 20-30% van de totale tijd; stap 5 voelt daarna bijna mechanisch. Sla je 1-4 over, dan groeit stap 5 explosief.

## Principe 4 — Wees expliciet over kennis vs. aanname

**Regel.** Bij elke beslissing markeer je: "dit volgt uit X" (waar X concreet bewijs is) versus "dit is mijn beste gok". Onzekerheden vlag je expliciet.

**Waarom.** AI-assistenten neigen naar gladde, plausibele antwoorden. Zonder expliciete markering raken aannames vermomd als kennis. Drie weken later weet je niet meer wat onderzocht en wat verzonnen is.

**Praktisch.**
- In `BRIEFING.md`: per claim een bron of expliciet "[aanname]".
- In `ONTWERPKEUZES.md`: elke beslissing heeft een rationale-sectie waarin onzekerheden benoemd worden.
- In stories: `## Open vragen`-sectie waar dingen die nog niet beslist zijn parkeren.
- Zelf in code-comments: "we gaan ervan uit dat …" alleen als de aanname niet uit de types blijkt.

## Principe 5 — Story-eerst, niet code-eerst

**Regel.** Voordat je iets bouwt, schrijf je een story. Een story heeft minstens: doel, input, acceptatiecriteria, scope, geschatte omvang. Stories leven in `stories/backlog/`, `stories/doing/` en `stories/done/`. Zie `04-ontwikkelstraat-en-stories.md` voor de complete conventie.

**Waarom.** Een story dwingt je het werk áf te bakenen voor je begint. Je merkt veel ambiguïteit pas bij het schrijven; oplossen-tijdens-coderen is duurder dan oplossen-tijdens-storying.

**Anti-patroon:** "Eerst even snel een loader bouwen, daarna de story schrijven." Garantie dat de loader achteraf niet meer past op de uiteindelijke story.

## Principe 6 — Type-hints overal, validatie aan de rand

**Regel.** Elke functie, elke klasse, elke return: type-hints. Validatie van data (Pydantic) gebeurt waar data het systeem binnenkomt: JSON laden, API-input, CLI-argumenten. Daarna vertrouw je op types.

**Waarom.** mypy `strict` werkt alleen als je het overal aanzet. Halve dekking is erger dan geen dekking — je krijgt false confidence. En als je validatie pas bij gebruik doet (i.p.v. bij binnenkomst), heb je de fout al door tien lagen heen gevoerd.

**Implementatie:**
- `pyproject.toml` heeft `[tool.mypy] strict = true` op `src/` en `pydantic.mypy`-plugin.
- Tests en scripts mogen losser (anders worden mocks onmogelijk).
- Pydantic-modellen aan de buitenkant; daarbinnen reken je op de types.

## Principe 7 — Output- en sessiediscipline

**Regel.** Vier specifieke gedragingen die context-gebrek voorkomen in lange AI-sessies:

1. **Werk in kleine stappen.** Eén story per response, niet meerdere.
2. **Genereer grote data via scripts**, niet inline. Toon de samenvatting (knopen-aantal, validatie-uitkomst), niet de hele JSON.
3. **Beperk tool-output.** Pijp lange commando-uitvoer door `head -N` of `tail -N`. Toon alleen relevante delen van testresultaten.
4. **Splits grote bestanden.** Lees met `offset` en `limit` als bestanden >150 regels zijn.

Dit klinkt micromanagement; in de praktijk redt het je een uur per dag aan crashende sessies en context-overload.

## Principe 8 — Doe domeinwerk niet in code

**Regel.** Inhoudelijke beslissingen (welke knopen, welke prerequisite-relaties, welke voorbeelden) horen niet in commit-messages of code-comments. Ze horen in:
- `docs/` — projectvisie en ontwerpkeuzes
- `stories/` — afgebakende deelvragen
- domeinspecifieke researchdocumenten

**Waarom.** Code-comments verouderen mee met code; documentatie verouderd mee met inzicht. Als je domeinkennis vermengt met implementatie-keuzes, krijg je twee soorten rot tegelijk.

**Voorbeeld.** "Deze prerequisite is omdat in alle methoden de nominativus voor de genitivus komt" → hoort in een story of in `RESEARCH_LESSTOF.md`, niet als comment in een seed-script.

## Principe 9 — Onomkeerbare acties bevestigen

**Regel.** Reversibele lokale acties (file edits, tests, refactors) doe je gewoon. Onomkeerbare of breed-zichtbare acties (force-push, branch verwijderen, package upgrade in lockfile, PR mergen, externe API-call met effect) bevestigt de AI of doe je zelf.

**Waarom.** Een AI is goed in vooruit-denken op één lijn; minder goed in voorzien wat een onomkeerbare actie elders breekt. Vijf seconden bevestigingsvraag bespaart drie uur reparatie.

In CLAUDE.md staat dit principe expliciet voor sessies. Voor je nieuwe project: neem het over.

## Vragen voor je nieuwe project

Voordat je begint, beantwoord deze tien vragen op papier:

1. Welke taal voor documentatie? Welke voor code? (zie principe 2)
2. Welke commit-conventie volg je? Voorbeeld: `<type>: <kort> in projecttaal`.
3. Wie is de domeinexpert die domeinkennis valideert? (jij zelf of iemand anders?)
4. Welke vorm heeft je graph (DAG, cyclisch causaal netwerk, bipartiet, taxonomie)? Zie `02-graph-blueprint.md`.
5. Heeft het domein een tijdsdimensie? Zie `02-graph-blueprint.md` §"Wanneer dynamisch".
6. Heb je een per-gebruiker-staat (leerlingmodel, profiel) of is alles read-only voor de eindgebruiker?
7. Welke schaal verwacht je (10², 10³, 10⁴ knopen)? Bij >10⁴: zie afwijkingen in `graph-methodology.md`.
8. Zijn de knopen door één team beheerd of komen ze van eindgebruikers? Bij user-generated: ID-schema-aanpak verandert.
9. Wat is je eerste-maand-doel? Concreet en meetbaar (zie `05-bootstrap-en-ontwerpkeuzes.md`).
10. Wat is je eerste-jaar-doel? Niet de droom, het minimale levensvatbare product.

Tien antwoorden op papier = je werkwijze is grotendeels vastgesteld. Vermijd om vraag 4-9 in code te beantwoorden voordat je het op papier hebt. Vraag 1-3 mag eerst opportunistisch — je kunt altijd bijdraaien.
