# 02 — Graph blueprint

Dit hoofdstuk is een **uittreksel met aanvullingen** op `docs/graph-methodology.md`. De methodologie zelf is direct overneembaar; lees dat document eerst, en gebruik dit hoofdstuk als praktische verlengstuk: keuzehulp, voorbeelden uit een ander domein, en verwijzingen naar concrete code in Olympus die je als sjabloon kunt gebruiken.

## §A — Welke graph-vorm past bij jouw domein?

Voordat je conventie 1-8 toepast, beantwoord je deze vraag. De vorm van je graph bepaalt of de hele methodologie past, of slechts deels.

| Domein-eigenschappen | Graph-vorm | Methodologie? |
|----------------------|------------|----------------|
| Voorwaardelijke kennis (X moet je kunnen voor Y), één afhankelijkheidsrichting | DAG (prerequisite-graph) | Volledig |
| Skill-tree, dependency-flow, certificering | DAG | Volledig |
| Causaal model met feedback-lussen ("meer X → meer Y → meer X") | Gemengde gerichte graph | Methodologie + appendix tijdsdimensie |
| Co-occurrence, sociaal netwerk, citaties, collaboraties | Ongerichte gewogen graph | Conventie 1, 2, 6, 7 + eigen invarianten |
| Taxonomie, classificatie, ouder-kind | Boom (subset DAG) | Methodologie minus cyclus-checks |
| Persoon ↔ object/instelling | Bipartiet | Conventie 1, 2, 6, 7 + matching-invarianten |
| Veranderend over tijd, versies of states | Eigen ontwerp | Buiten scope; zie graph-methodology.md "Afwijken" |

**Beslisregel.** Type je edges. Zelfs als je domein "gewoon" een DAG is, gun jezelf 2-3 edge-types: meestal vind je later toch dat sommige relaties zwakker zijn (`enrichment`, `recommendation`) of dwars staan op de hoofdrichting (`transfer`, `analogy`). Zie principe in `graph-methodology.md` §1 en §5.

## §B — Pydantic-typering: wat zet je minimaal op een knoop?

Olympus' `KennisKnoop` heeft 9 velden. Daarvan zijn er 5 die in **elk** graph-project aanwezig moeten zijn, ongeacht domein:

```python
class Node(BaseModel):
    """Minimal contract for a graph node — extend per project."""

    id: str  # see ID-schema, §C
    type: NodeType  # discriminator (StrEnum)
    title: str  # short, human-readable
    description: str  # 1-2 sentences, disambiguating
    content_ref: str | None = None  # path to full content, see chapter 03
```

Project-specifieke velden komen daar bovenop. Voorbeelden uit verschillende domeinen:

| Domein | Voorbeeld extra velden |
|--------|------------------------|
| Adaptief leren (Olympus) | `bloom_niveau`, `taal`, `fase`, `toetsbaar`, `pensum_jaren`, `items` |
| Causaal beleid (Zeppelin) | `domain`, `level`, `polarity`, `disciplines` |
| Sportdeelname-deelnemer | `leeftijdscategorie`, `niveau`, `regio` |
| Vogelidentificatie | `genus`, `family`, `habitat`, `seizoen`, `diagnostic_features` |
| Mediageletterdheid | `competentie`, `leeftijdscategorie`, `bloom_niveau`, `vakdomein` |

**Wel doen:** velden die structureel zijn (gebruikt in de scheduler, validator, of frontend-rendering).
**Niet doen:** velden die alleen voor documentatie zijn (die horen in `content_ref`).

## §C — ID-schema: hoe ontwerp je het?

Het ID-schema is een **eenmalige beslissing met blijvende impact**. Goed schema → diff-leesbaar, sortering werkt, debuggen makkelijk. Slecht schema → herwerkkosten als je migreert.

### Stap 1 — Verzamel je segment-vocabulaire

Loop door je verwachte 50-100 eerste knopen en noteer per knoop welke segmenten betekenisvol zijn. Voor Olympus: `{TAAL}-{TYPE}-{DOMEIN}-{SUBDOMEIN}-{SPECIFIEK}`. Voor een vogelidentificatie-project zou het kunnen worden: `{REGIO}-{ORDE}-{FAMILIE}-{GESLACHT}-{SOORT}`. Voor een huisartsenrichtlijn: `{HOOFDSTUK}-{KLACHT}-{TRAJECT}`.

### Stap 2 — Toets de breekpunten

- **Hoeveel segmenten?** 3-6 is werkbaar. Minder = te ondiep, meer = onleesbaar.
- **Hoe lang per segment?** Max 8 tekens (Olympus' regel). `MORF` is goed; `MORFOLOGIE` te lang.
- **Uppercase ASCII met dash?** Ja, als regel. Diakritische tekens, lowercase, of underscore in IDs zijn een bron van bugs.
- **Afkortingen consistent?** Beter `D1`, `D2`, `D3` dan `EERSTE`, `TWEEDE`, `DERDE`. Beter `INTRO` dan `BASIS`/`OVERZICHT`/`UITLEG` willekeurig door elkaar.

### Stap 3 — Schrijf validate + parse

```python
ID_PATTERN = re.compile(r"^([A-Z]{1,3})-(N|E|...)(-[A-Z0-9]{1,8}){1,4}$")

def validate_id(node_id: str) -> bool:
    return bool(ID_PATTERN.match(node_id))

def parse_id(node_id: str) -> ParsedId:
    if not validate_id(node_id):
        raise ValueError(f"Invalid ID: {node_id!r}")
    parts = node_id.split("-")
    return {"region": parts[0], "type": parts[1], "segments": parts[2:]}
```

Plus tests met geldige + ongeldige voorbeelden. Zie `src/gymnasium_classica/schemas/id_schema.py` als sjabloon.

### Stap 4 — Reserveer ruimte voor groei

Voorbeeld-anti-patroon: je gebruikt `001`..`099` als laatste segment en hebt na half jaar `099` aangetikt. Reserveer ten minste twee orden van grootte: `001`..`999`. Als je later vermoedt dat je verder groeit, gebruik vier cijfers.

### Stap 5 — Documenteer in `docs/id-schema.md`

Niet alleen de regex, maar ook: voorbeelden, segmenten met hun toegestane waardes, regels voor concept- vs. detail-knopen (Olympus heeft `-INTRO` voor concepten), reserveringen voor toekomst.

## §D — Persistence: lean JSON + content separation

Zie `graph-methodology.md` §3 voor de volledige rationale. Hier de praktische uitwerking.

### Mappenstructuur

```
data/
├── graph/                                # Structuur (JSON)
│   ├── {domein1}_{scope}.json           # Bijv. lat_grammatica_leerjaar1.json
│   ├── {domein2}_{scope}.json
│   └── shared_{thema}.json              # Cross-domein knopen
└── content/                              # Inhoud (markdown)
    └── {NODE_ID}.md                     # Één markdown per knoop
```

Niet plat in `data/` gooien. Sub-directories werken — de loader hoort `data/graph/` als root te zien en alle `.json` daaronder te ontdekken.

### Bestandssplitsing

Olympus heeft 8 JSON-bestanden voor 800 knopen. Vuistregel: **150-200 knopen per bestand**, gegroepeerd per coherent subdomein. Als je een bestand opent en je scrollt langer dan 30 seconden voor je het overzicht hebt, het bestand is te groot.

### Cross-file edges

Edges mogen verwijzen naar knopen in een ander bestand. De loader plakt eerst alle nodes samen, daarna alle edges. Dangling edge → `ValueError` met locatie. Zie Olympus `src/gymnasium_classica/graph/loader.py`.

### Wat hoort in `data/content/{ID}.md`?

Markdown met de uitleg, voorbeelden, paradigma's, beelden, audio-refs. Niet de structurele velden (titel, beschrijving) — die staan al in de JSON.

```
# {Titel — uit JSON}

## Korte uitleg
{1-3 alinea's}

## Voorbeelden
- {voorbeeld 1}
- {voorbeeld 2}

## Veelgemaakte fouten
{...}

## Verwijzingen
{...}
```

Geen rich-text in de JSON. Geen structured data in de markdown. Strikt gescheiden.

## §E — De loader

```python
def load_graph(path: Path) -> nx.DiGraph:
    """Load a graph from a single JSON file or a directory of JSONs.

    - Single file: read and parse one GraphData document.
    - Directory: read all *.json under it, concatenate nodes and edges.
    - Validate IDs unique across all files.
    - Validate edge source/target references existing nodes (after merging).
    - Return an nx.DiGraph with each Pydantic model attached as node/edge data.
    """
```

Implementatieblauwdruk uit `src/gymnasium_classica/graph/loader.py`:

1. Resolve path; collect alle te laden JSON-paden.
2. Per bestand: laad raw, valideer met `GraphData.model_validate(raw)`, voeg toe aan combined-list.
3. Check: alle node-IDs uniek over bestanden? Anders `ValueError("Duplicate ID … in files A en B")`.
4. Check: elke edge-source en -target bestaat als node? Anders `ValueError("Dangling edge … in file X")`.
5. Bouw `nx.DiGraph`, attach Pydantic-objecten als `data["knoop"]` en `data["edge"]`.
6. Return.

Geen lazy loading, geen streaming. Voor < 10⁴ knopen werkt dit prima.

## §F — Validatie-catalogus

Verplicht in elk graph-project, zie `graph-methodology.md` §5:

1. **Cycle-detectie per edge-type**, geen globale.
2. **Orphan-detectie** (knopen zonder edges).
3. **Duplicate-ID-detectie** (al in loader voor cross-file).
4. **Dangling-edge-detectie** (al in loader).
5. **Edge-weight-validatie** (waardes in [0, 1] of in toegestane enum).
6. **Node-ID-format-validatie** (matcht ID-schema).
7. **Connectivity-analyse** (waarschuw bij meerdere disconnected components).
8. **Topologische sortering** (alleen als de graph-vorm een sortering toelaat).

Implementeer in `src/<package>/graph/validation.py` met een `ValidationReport`-dataclass. Zie Olympus' implementatie als sjabloon (250 regels).

CLI in `scripts/validate_graph.py`:

```bash
python scripts/validate_graph.py data/graph/
```

Exit non-zero bij errors. Hangt aan in pre-commit en CI (zie hoofdstuk 04).

## §G — Visualisatie

Zie `graph-methodology.md` §7 voor de keuze. Praktische start:

- **DAG?** Graphviz `dot`, layout `dot`. Output: SVG of PNG. Eén regel: `nx.nx_agraph.write_dot(graph, "out.dot")`.
- **Causaal netwerk?** Graphviz `neato` of `circo` voor circular layout. Of D3 met force-directed layout in een eenvoudige HTML.
- **Klein netwerk?** Mermaid in markdown — kan inline in je documentatie.

Bouw geen interactieve viz voordat je een use-case hebt. Begin met statische export.

## §H — Tests

Drie soorten, allemaal verplicht. Zie `graph-methodology.md` §8.

1. **Smoke** (`tests/test_graph_loader.py`): empty, duplicate, dangling, cyclus.
2. **Round-trip** (`tests/test_graph_roundtrip.py`): `load(serialize(g)) == g`.
3. **Invariant-based** (`tests/test_graph_invariants.py`): de **echte** dataset (niet een fixture) voldoet aan alle checks.

Het derde type is het belangrijkst — die test breekt zodra iemand een rotte commit aan data/ wil pushen.

## §I — Wanneer dynamisch (tijdsdimensie)

Zie `graph-methodology.md` Appendix.

Drie signalen dat je in dynamisch domein zit:
- Edges hebben een `time_lag`, `delay`, `polarity` of `cycle_time`-veld.
- Je wilt "wat als ik X verander?"-vragen kunnen beantwoorden, niet alleen "hoe hangt X met Y samen?".
- Feedback-lussen zijn essentieel.

Drie valkuilen om te vermijden:
1. Velden opslaan en niet gebruiken (dead-field anti-pattern).
2. Globale DAG-acycliciteit forceren op een netwerk dat feedback heeft.
3. Statische pad-analyse gebruiken voor dynamische interventie-vragen.

In je nieuwe project: beslis vóóraf of je structureel of dynamisch werkt. Mengvorm is mogelijk maar dan documenteer je expliciet welke laag wat doet.

## §J — Stappen om je eigen graph-laag op te zetten

Sprint 1 (1-2 dagen):
1. ID-schema vastleggen + tests.
2. Pydantic-modellen voor Node, Edge, GraphData.
3. Eén handmatig PoC-JSON met 30-50 knopen.
4. Loader (single-file + directory).
5. Eerste twee invariant-checks (cycle + duplicate).
6. `scripts/validate_graph.py`.
7. Tests groen.

Sprint 2 (1 dag):
1. Verbreed invariant-catalogus naar volledige set.
2. Round-trip-tests.
3. Stats-script (`scripts/export_graph_stats.py`).
4. Eerste `dot`-export.

Daarna: groei door inhoud invoeren in nieuwe JSON-bestanden, edges leggen, content-markdowns schrijven. De graph-laag zelf is dan stabiel.

## Vragen voor je nieuwe project

1. Welke graph-vorm? (zie §A)
2. Welke kernvelden op een knoop? Welke per-domein-uitbreidingen? (zie §B)
3. Welk ID-schema? Schrijf vier voorbeelden uit. (zie §C)
4. Hoe split je je JSON? Hoeveel bestanden voor de eerste 100 knopen? (zie §D)
5. Welke edge-types, en welke daarvan moeten acyclisch zijn? (zie §F)
6. Welke visualisatie als default? (zie §G)
7. Statisch of dynamisch domein? (zie §I)

Antwoorden op papier vóór je een regel code schrijft.
