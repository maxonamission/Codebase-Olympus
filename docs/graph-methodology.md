# Graph-methodologie

## Waarom dit document?

Projecten met kennis- of netwerkgrafen delen geen inhoud maar wel een werkwijze. Dit document legt acht conventies vast die zijn ontstaan tijdens Gymnasium Classica en waarvan we verwachten dat ze zich lenen voor andere graph-projecten — ook als die inhoudelijk totaal iets anders doen (sportdeelname, persoonlijke vermogens, affectief vitale verenigingen, ...).

Het is bewust **geen library** en bewust **geen generieke basisklasse**. Het is een gedeelde taal: overnemen vraagt handwerk, maar voorkomt dat elk nieuw project dezelfde architectuurvragen opnieuw stelt.

**Doelgroep:** ontwikkelaars die een project starten met een typed graph als kernmodel. Eén- of tweepersoons-teams, Python 3.11+, NetworkX als in-memory type, JSON als persistence. Grotere graph-projecten (>10⁵ knopen, echte graph-database) vallen buiten scope — die hebben andere afwegingen.

## Acht conventies

### 1. Pydantic-getypeerde nodes en edges

**Regel.** Elke knoop en elke edge is een Pydantic `BaseModel` met expliciete velden, validators en — waar mogelijk — `frozen=True`. Subtypen via discriminated unions of `StrEnum`-velden, niet via losse klassen.

**Rationale.** Runtime-validatie vangt garbage-in aan de rand van het systeem; type hints maken IDE-autocomplete en mypy-strict bruikbaar; de Pydantic-mypy-plugin dwingt consistente velden af.

**Olympus-voorbeeld:** `KennisKnoop(id, type: KnoopType, titel_nl, bloom_niveau, beschrijving)` en `PrerequisiteEdge(source_id, target_id, weight, type: EdgeType)`.

**Vrij invulbaar:** welke velden en welke subtypen. Vaste kern: iedere knoop heeft minstens een `id`, een `type`, en een korte beschrijving (1-2 zinnen).

### 2. ID-schema als contract

**Regel.** Elke knoop heeft een menselijk leesbare, hiërarchische ID volgens patroon `{DOMEIN}-{TYPE}-{SEGMENT}[-{SEGMENT}]...`. Uppercase ASCII, `-` als separator, max 8 tekens per segment.

**Rationale.** IDs lezen als adressen. Je ziet aan `LAT-G-MORF-NOM-D1` waar een knoop thuishoort zonder de database te openen. Diffs in JSON worden daardoor leesbaar; sorteren op ID geeft automatisch een zinvolle volgorde.

**Verplicht in het project:** `validate_xxx_id(id: str) -> bool` én `parse_xxx_id(id: str) -> ParsedId` in `schemas/id_schema.py`, met unit-tests op geldige en ongeldige voorbeelden.

**Vrij invulbaar:** de segmenten en hun volgorde. Een sportdeelname-project kan bijvoorbeeld `NL-V-SPORT-VOETBAL-P18` gebruiken (Nederland, vereniging, sport, discipline, leeftijd), een affectieve-vereniging-project `REGIO-TYPE-AARD-FASE`.

### 3. Persistence: lean JSON + separate content

**Regel.** `data/graph/*.json` bevat structuurdata (IDs, types, velden, edges). Uitgebreide teksten, beschrijvingen, voorbeelden en media staan apart in `data/content/{ID}.md` (of `/media/{ID}.png`), gereferenced via een `content_ref`-veld op de knoop.

**Rationale.** De graph moet snel in-memory laadbaar blijven. Content groeit onafhankelijk en is vaak door een andere persoon geschreven dan de structuur. Reviewers kunnen content apart beoordelen. In-JSON markdown wordt een escape-hel.

**Vrij invulbaar:** welke content-typen je ondersteunt (alleen markdown, of ook audio/SVG), en of je per ID één bestand hebt of een bundel.

**Niet van afwijken:** JSON blijft structured (veldnamen, geen rich text), markdown blijft buiten de JSON.

### 4. Directory-mode loader met cross-file edges

**Regel.** Je `load_graph(path)`-functie accepteert zowel een enkel JSON-bestand als een directory met `*.json`-bestanden. In directory-mode: alle bestanden laden, edges die naar een ID in een ander bestand verwijzen correct resolven, dangling references → `ValueError` met locatie.

**Rationale.** Elke serieuze graph groeit uit één bestand. Per subdomein opdelen (Latijnse grammatica, Griekse grammatica, Cultuur, ...) houdt bestanden reviewbaar, maar je wilt edges tussen subgraphs kunnen leggen zonder kunstmatige shims.

**Vrij invulbaar:** hoe je de splitting kiest (per taal, per taxonomie-niveau, per versie). Wat vast is: de loader ontzorgt het samenvoegen; de rest van de code krijgt één `nx.DiGraph`.

### 5. Invarianten-catalogus

**Regel.** Elk project heeft `graph/validation.py` die een `ValidationReport` produceert. Minstens deze checks:

- cycle-detectie op "harde" edges
- orphan-detectie (isolated nodes)
- duplicate-ID-detectie
- dangling edge-references (al in de loader)

Optioneel, afhankelijk van het domein: topologische sortering, connectivity-analyse, diameter, clustering.

**Rationale.** Deze checks vangen 80 % van de dataset-fouten die anders pas aan het oppervlak komen in productie. Wat "hard" betekent verschilt per domein — in Olympus is `prerequisite` hard en `enrichment` soft. Daarom definieert elk project zelf welk edge-type deel is van de invariant.

**Script:** `scripts/validate_graph.py` draait de hele catalogus en exit non-zero bij fouten. Staat in CI als aparte stap, zodat een kapotte data-commit niet naar `main` gaat.

### 6. Naamgevingsconventies

**Mappen.** `data/graph/` voor JSON-bestanden. `data/content/` voor markdown-content. `data/<assets>/` voor alles erbuiten.

**Bestanden.** Patroon `{domein}_{subdomein}_{scope}.json` — bijv. `lat_vocabulaire_leerjaar1.json`, `persoonlijke_vermogens_basis.json`, `verenigingen_regio_noord.json`. Underscore als separator in bestandsnamen, dash in IDs.

**Scripts.** `validate_graph.py` en `export_graph_stats.py` zijn standaardnamen. Geen varianten als `check_graph.py` of `graph_lint.py` — dezelfde naam in elk project.

**Modules.** `src/<package>/models/graph.py` (Pydantic), `graph/loader.py`, `graph/validation.py`, `schemas/id_schema.py`. Consistent over projecten heen zodat je als ontwikkelaar niet hoeft te zoeken.

### 7. Layout- en visualisatie-defaults

De gekozen graph-vorm dicteert de default-visualisatie:

- **DAG:** hiërarchisch (Sugiyama-layout) via Graphviz `dot`. Goed voor prerequisite-graphs, skill-trees, dependency-flows.
- **Dicht ongerichte graph:** force-directed (Fruchterman-Reingold, spring-layout). Goed voor sociale netwerken, co-occurrence-graphs.
- **Boom:** layered top-down. Goed voor taxonomieën.
- **Bipartite:** kolomlayout met één kant links, andere rechts. Goed voor "persoon ↔ vereniging"-achtige modellen.

**Export-formaten die minimaal ondersteund worden:** `.dot` (Graphviz, printvast), Cytoscape-JSON (interactief web), Mermaid (inline in markdown-docs).

**Node size ∝ belangrijkheid.** Voor DAGs: out-degree is vaak een goede proxy ("hoeveel andere knopen hangen van deze af"). Voor sociale: betweenness- of eigenvector-centraliteit. Voor bipartite: aantal connecties in een kant.

### 8. Test-patronen

Drie soorten tests die in elk graph-project thuishoren:

**Smoke-tests** (`tests/test_graph_loader.py`): empty directory → specifieke error, duplicate ID → ValueError, dangling edge → ValueError, cyclus in hard-edges → ValueError (via validation).

**Round-trip** (`tests/test_graph_roundtrip.py`): `load_graph_from_dict(graph_to_dict(g))` produceert een equivalente graph. Vangt serializer-bugs vroeg.

**Invariant-based** (`tests/test_graph_invariants.py`): de echte project-graph (niet een fixture) voldoet aan alle checks uit de catalogus. Dit is de test die in CI de actuele dataset bewaakt.

## Wat NIET in deze methodologie hoort

- Concrete knoop-typen (G/V/C/I bij Olympus, of `Persoon`/`Vereniging` elders)
- Concrete edge-typen (prerequisite vs. influences vs. membership)
- Domein-vocabulaire, gebruikersflow, UI-copy
- Backend- of framework-keuzes buiten graph-modellering
- Frontend-visualisatie-implementaties (wél de default-keuze voor welk algoritme, niet de component-code)
- Versiebeheer van de graph zelf (migrations, schema-evolutie) — dat verdient een eigen document

## Wanneer afwijken?

Deze methodologie past bij ~10² tot ~10⁴ knopen, read-mostly, door één team beheerd. Afwijken is legitiem bij:

- **Grootte > 10⁵ knopen:** JSON + NetworkX schaalt niet; overweeg Neo4j of een native graph-database. Conventies 3-5 vervallen; 1, 2, 6, 7 blijven geldig.
- **User-generated knopen:** hiërarchisch menselijk ID-schema werkt niet als gebruikers zelf knopen aanmaken. Gebruik UUIDs + metadata-velden, en behoud conventie 1, 3-8.
- **Sterk evoluerend schema:** als knoop-typen vaak veranderen, wordt Pydantic's strictheid een rem. Overweeg losse dicts met JSON-schema-validatie, maar **documenteer waarom** je conventie 1 loslaat.

## Toepassingschecklist

Loop langs bij het opstarten van een nieuw graph-project:

- [ ] Python 3.11+, NetworkX, JSON, team ≤3 → methodologie is toepasbaar
- [ ] Knoop- en edge-typen als Pydantic-modellen gedefinieerd (§1)
- [ ] ID-schema ontworpen vóór data ingevoerd; `validate_xxx_id` + `parse_xxx_id` met tests (§2)
- [ ] Structuur-JSON en content-markdown gesplitst; `content_ref`-veld aanwezig (§3)
- [ ] Loader werkt op directory + resolve cross-file edges (§4)
- [ ] `graph/validation.py` met minstens 3 invariant-checks + `scripts/validate_graph.py` (§5)
- [ ] Naamgeving volgt de conventie (§6)
- [ ] Default-visualisatie gekozen op basis van graph-vorm (§7)
- [ ] Smoke + round-trip + invariant-based tests aanwezig (§8)

Acht "ja" = je volgt de methodologie. Minder is geen ramp, mits je per afwijking een eenregelige rationale in je project-CLAUDE.md noteert.
