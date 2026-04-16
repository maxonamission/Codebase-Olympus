# scripts/

CLI-scripts voor onderhoud, validatie en generatie rondom de knowledge graph
en de bijbehorende content (items, markdown, audio, passages).

Alle scripts draaien vanuit de repo-root en verwachten dat het pakket
`gymnasium_classica` geïnstalleerd is (bijv. `uv pip install -e .[dev]`).

## Overzicht

| Script | Doel |
|--------|------|
| `validate_graph.py` | Laadt een graph-bestand/directory en print een `ValidationReport` (cycles, orphans, dangling edges). |
| `export_graph_stats.py` | Print samenvattende statistieken: knopen per type, Bloom-niveau, topologische diepte. |
| `content_coverage.py` | Rapporteert per knoop welke content-artefacten aanwezig zijn (items, markdown, audio, passage) en aggregeert per (taal, type). |

De `generate_*.py`-scripts genereren items, vocabulaire, audio en passages —
zie de docstring bovenin elk bestand voor scope en invoer.

## content_coverage.py

Structureel zicht op content-kwaliteit per knoop. Het script controleert vier
dimensies en aggregeert het resultaat per `(taal, type)`-bucket:

| Vlag | Definitie |
|------|-----------|
| `has_items` | De knoop heeft ten minste één `Item` in de graph-JSON. |
| `has_content` | `data/content/{id}.md` bestaat **óf** `content_ref` wijst naar een bestaand bestand. |
| `has_audio` | Alleen voor V-knopen: `data/audio/{id}.wav` bestaat én is > 1 KB. |
| `in_passage` | De knoop-ID komt voor in de `knoop_ids` van een passage in `data/passages/*.json`. |

### Gebruik

```bash
# Samenvatting op stdout
python scripts/content_coverage.py

# Volledige rapport + JSON-export voor historische vergelijking
python scripts/content_coverage.py --output data/content_coverage.json
```

Optionele flags (voor tests en experimenten):

- `--graph-dir PATH` — alternatieve graph-directory (default: `data/graph`)
- `--content-dir PATH` — alternatieve content-directory
- `--audio-dir PATH` — alternatieve audio-directory
- `--passages-dir PATH` — alternatieve passages-directory

### Voorbeelduitvoer

```
=== Content-dekking (800 knopen) ===
taal   type total             items          content            audio          passage
--------------------------------------------------------------------------------------
grc    G      142    24/142 (16.9%)     0/142 (0.0%)           n.v.t.   42/142 (29.6%)
grc    V      150  150/150 (100.0%)     0/150 (0.0%) 150/150 (100.0%)   36/150 (24.0%)
lat    G      143   131/143 (91.6%)   36/143 (25.2%)           n.v.t.   46/143 (32.2%)
lat    V      300  300/300 (100.0%)     0/300 (0.0%) 300/300 (100.0%)   49/300 (16.3%)
shared C       65       0/65 (0.0%)      0/65 (0.0%)           n.v.t.      0/65 (0.0%)
```

### CI-regressiecheck

`tests/test_content_coverage.py` laadt de echte `data/graph/` en faalt als de
dekking onder een conservatieve drempel zakt (o.a. LAT-G items ≥ 25 %, LAT-V
en GRC-V items/audio ≥ 90 %). De drempels liggen ruim onder de huidige staat:
ze vangen regressies op (bijv. nieuwe knopen zonder items) zonder vals alarm
bij normale schommelingen.

Drempels verhogen mag alleen expliciet en onderbouwd — verhoog pas als een
nieuwe baseline stabiel is.
