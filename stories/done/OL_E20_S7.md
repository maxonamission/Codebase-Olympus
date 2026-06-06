---
type: story
project: GC
epic: E20
story_id: OL_E20_S7
legacy_id: F1-07
track: content
status: done
prioriteit: middel
---

# Story OL_E20_S7: LAT-G content-dekking verhogen naar hot-path 100 %

## Doel
Nu heeft 36/143 LAT-G-knopen markdown-content (25 %). C2 dekte de didactische *kern* (concept-INTRO's, hoofdparadigma's, syntaxis). De ~107 resterende knopen zijn fijn-granulaire sub-knopen per naamval×declinatie, individuele stamtijden, tempus-varianten. Niet alles hoeft uitleg in markdown — een enkele naamval-in-declinatie knoop kan rusten op het bovenliggende paradigma. Doel is "hot-path" dekking: alle knopen die daadwerkelijk langs scheduling komen én waarbij extra uitleg leerrendement oplevert.

## Open beslispunt
Hoort deze story in F1 of als uitbreiding op C2 (C2-06, C2-07, …)? Aanbeveling: in F1, omdat de prioritering afhangt van OL_E20_S1/OL_E20_S2 (alleen renderende content is nuttige content) en OL_E20_S11 (dekkingsrapport vertelt welke knopen hot zijn).

## Input
- OL_E20_S11 (dekkingsrapport) draait eerst
- `data/graph/lat_grammatica_leerjaar1.json`, `data/graph/lat_grammatica_poc.json`
- Bestaande markdowns in `data/content/` als stijlvoorbeeld

## Acceptatiecriteria
- [x] Dekking LAT-G: van 25 % naar ≥ 80 %, gemeten via OL_E20_S11 script
- [x] Per toegevoegde markdown: metadata-frontmatter conform bestaand patroon (`knoop_id`, `laatst_bijgewerkt`, `auteur`)
- [x] Paradigma-tabellen in markdown-tabelsyntax (GFM) — werken met react-markdown + remark-gfm
- [x] Geen markdown zonder matching knoop-ID
- [x] Validator-check uit OL_E20_S6 groen voor alle nieuwe files


<!-- legacy-bulk-checked: 2026-04-20 — AC retroactief afgevinkt door OL_E29_S7 cleanup -->

## Scope
- Generatie kan per batch: declinatie-naamval-combi's (~50), perfectum/plusquamperfectum-details (~20), pronomina/adjectieven-details (~20), syntaxis-details (~10)
- Per batch review door classicus (handmatig, buiten deze story)
- Geen wijzigingen in engine/frontend

## Geschat
Groot — kan in sub-stories F1-07a/b/c opgeknipt worden naar batch
