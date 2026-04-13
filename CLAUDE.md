# CLAUDE.md — Gymnasium Classica

## Project

Gymnasium Classica is een adaptief leersysteem voor Latijn en Grieks op VWO-gymnasiumniveau. Het combineert een knowledge graph met spaced repetition, Bayesian Knowledge Tracing en Item Response Theory. Doel: leerlingen voorbereiden op het staatsexamen LTC/GTC met 30 minuten per dag.

Lees voor de volledige context:
- `docs/BRIEFING_GYMNASIUM_CLASSICA.md` — projectvisie, architectuur, roadmap
- `docs/ONTWERPKEUZES_GYMNASIUM_CLASSICA.md` — vastgestelde ontwerpkeuzes met architecturale implicaties

## Tech stack en constraints

- **Python 3.11** (geen 3.13, geen conda)
- **uv** als package manager (`uv pip install`, `uv venv`)
- **FastAPI** backend, **SQLite** voor persistence (fase 0-3), migratie naar PostgreSQL later
- **NetworkX + JSON** voor de knowledge graph (in-memory, bestanden in `data/`)
- **React (JSX)** frontend (fase 4)
- Geen venvs in Obsidian vault of Synology-synced folders
- Encoding: UTF-8 without BOM voor alle bestanden
- Documentatie in het **Nederlands**, code (variabelen, docstrings, comments) in het **Engels**

## Werkwijze

- Schrijf geen code voordat de structuur besproken is. Begin met een plan in structured prose.
- Bij nieuwe componenten: beschrijf eerst het datamodel en de interfaces, dan de implementatie.
- Wees expliciet over wat je hebt gelezen vs. wat je aanneemt. Vlag onzekerheden.
- Gebruik type hints overal. Pydantic models voor data validation.
- Tests: pytest. Schrijf tests voor de knowledge graph (cycle detection, orphan detection, topologische sortering) en het learner model (BKT updates, SM-2 scheduling).
- Git commits: conventionele commits, Nederlands in commit messages.

## Output en sessie-management

De API heeft een idle timeout (~60s). Voorkom timeouts door:

- **Werk in kleine stappen.** Eén story per keer, niet meerdere stories in één response. Commit na elke afgeronde story.
- **Genereer grote JSON via scripts, niet inline.** Schrijf een Python-script dat de knopen genereert, valideert en opslaat. Toon de samenvatting (aantal knopen, edges, validatie-uitkomst), niet de volledige JSON.
- **Beperk tool-output.** Gebruik `| tail -N` of `| head -N` bij lange commando-output. Toon alleen relevante delen van testresultaten.
- **Splits grote bestanden.** Lees bestanden met `offset` en `limit`, niet in één keer als ze >150 regels zijn.
- **Geen volledige bestanden herhalen.** Bij edits: toon alleen wat er veranderd is, niet het hele bestand.
- **Commit vroeg en vaak.** Na elke story of logische eenheid. Niet wachten tot het einde van een sessie.

## Domeinkennis

- De CvTE-minimumlijsten (Latijn en Grieks) definiëren de scope van de grammatica.
- Kennisknopen zijn van type G (grammatica), V (vocabulaire), C (cultuur), I (integratie).
- Edges zijn `prerequisite` (hard), `enrichment` (soft), of `transfer` (cross-linguïstisch).
- Het examenprogramma kent domeinen A t/m E. Het CE toetst A1, B, C. Het college-examen (staatsexamen) toetst alle domeinen inclusief een mondeling deel.
- Het pensum wisselt jaarlijks per auteur — dit is een jaarlijks wisselende module bovenop de vaste graph.

## Projectstructuur

```
src/gymnasium_classica/
├── models/
│   ├── graph.py        # KennisKnoop, PrerequisiteEdge, Item, GraphData + enums
│   ├── user.py         # User, Subscription
│   └── learner.py      # LearnerModel, KnoopState, SessionRecord, ItemResponse
├── graph/
│   ├── loader.py       # JSON → NetworkX DiGraph (load_graph, graph_to_dict)
│   └── validation.py   # ValidationReport, cycle/orphan/connectivity checks
└── schemas/
    └── id_schema.py    # ID-validatie: validate_knoop_id(), parse_knoop_id()

data/
├── graph/                              # Knowledge graph JSON bestanden
│   ├── lat_grammatica_poc.json         # 50 Latijnse grammaticaknopen (smoke test)
│   ├── lat_grammatica_leerjaar1.json   # Extra Latijnse grammatica (~100 knopen)
│   ├── grc_alfabet.json                # Grieks alfabet onboarding (~40 knopen)
│   ├── grc_grammatica_leerjaar1.json   # Griekse grammatica (~100 knopen)
│   ├── lat_vocabulaire_leerjaar1.json  # Latijns vocabulaire (~300 knopen)
│   ├── grc_vocabulaire_leerjaar1.json  # Grieks vocabulaire (~200 knopen)
│   └── sha_cultuur_leerjaar1.json      # Gedeelde cultuurknopen (~70 knopen)
└── content/                            # Didactische markdown content per knoop
    └── {KNOOP_ID}.md                   # Bijv. LAT-G-MORF-DECL1-INTRO.md

scripts/
├── validate_graph.py   # CLI: laad graph, print ValidationReport
└── export_graph_stats.py  # CLI: knooptelling, diepte, statistieken

tests/                  # pytest tests voor alle modules
```

## ID-schema voor kennisknopen

Formaat: `{TAAL}-{TYPE}-{SEGMENT}[-{SEGMENT}]...` (3-6 segmenten, uppercase ASCII)

- **Taal:** `LAT`, `GRC`, `SHA` (shared)
- **Type:** `G` (grammatica), `V` (vocabulaire), `C` (cultuur), `I` (integratie)
- **Segmenten:** typespecifiek, max 8 chars per segment
- Conceptknopen eindigen op `-INTRO`

Voorbeelden: `LAT-G-MORF-NOM-D1`, `LAT-V-F01-ESSE`, `SHA-C-FIL-STOA`

## Content-architectuur

- **`data/graph/*.json`** — structuurdata: IDs, types, titels, Bloom-niveaus, prerequisites, IRT-params, korte beschrijving (1-2 zinnen)
- **`data/content/{KNOOP_ID}.md`** — didactische inhoud: paradigma's, uitleg, voorbeeldzinnen, veelgemaakte fouten
- `content_ref` veld in KennisKnoop verwijst naar het markdown-bestand
- **Rationale:** graph blijft lean voor in-memory laden, content evolueert onafhankelijk

## Huidige fase: Fase 0/1 — Fundament + Knowledge Graph MVP

### Fase 0 — Fundament (compleet)
1. ✅ Projectstructuur met src/, data/, tests/, docs/, scripts/
2. ✅ Pydantic models voor KennisKnoop, PrerequisiteEdge, Item, User, Subscription, LearnerModel
3. ✅ NetworkX graph loader met validatie + directory-loading (meerdere JSON bestanden)
4. ✅ 50 Latijnse grammaticaknopen als smoke test (`data/graph/lat_grammatica_poc.json`)
5. ✅ 113 tests (alle groen)

### Fase 1 — MVP Knowledge Graph (in uitvoering)

**Scope: leerjaar 1 gymnasium, beide talen.** Model: scholen als het Vossius die Latijn én Grieks vanaf dag 1 aanbieden. Externe validatie door een klassieke-taleninstituut.

**Doelomvang: ~850 knopen, ~1500-2000 edges**

| Component | Knopen | Status |
|-----------|--------|--------|
| Latijnse grammatica (decl. 1-5, conj. 1-4, perf., passief, syntax) | ~150 | 50 PoC ✅, ~100 uit te breiden |
| Grieks alfabet onboarding-subgraph | ~40 | Te bouwen |
| Griekse grammatica (o-/a-/3e decl., presens/impf., medium, syntax) | ~100 | Te bouwen |
| Latijns vocabulaire (frequentiegestuurd, individuele woorden) | ~300 | Te bouwen |
| Grieks vocabulaire (frequentiegestuurd, individuele woorden) | ~200 | Te bouwen |
| Gedeelde cultuurknopen (SHA-C-*, mythologie/geschiedenis/maatschappij) | ~70 | Te bouwen |
| Transfer-edges (LAT↔GRC isomorfe concepten) | ~100 edges | Te bouwen |

**Graph-bestanden:** `data/graph/` bevat meerdere JSON-bestanden per domein. De loader combineert ze automatisch (`load_graph(directory_path)`). Cross-file edges (bijv. transfer-edges naar knopen in andere bestanden) worden correct opgelost.

**Grieks alfabet:** subgraph `GRC-G-FONL-ALFA-*`, prerequisite voor alle GRC-grammaticaknopen. Drie fasen: letterherkenning → fonologie/diakritiek → leesvaardigheid. Blokkeert alle Griekse stof tot volledige beheersing.

## Niet doen

- Geen frontend werk in fase 0-2
- Geen LLM-integratie in fase 0-2
- Geen deployment/hosting configuratie in fase 0
- Geen over-engineering: SQLite, geen Docker, geen microservices
