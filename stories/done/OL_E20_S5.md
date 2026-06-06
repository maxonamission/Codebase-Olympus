---
type: story
project: GC
epic: E20
story_id: OL_E20_S5
legacy_id: F1-05
track: content
status: done
prioriteit: middel
---

# Story OL_E20_S5: Woordkaart — toon structured vocab-metadata uit vocab_sources

## Doel
De JSONs in `data/vocab_sources/` bevatten structured data per lemma (`pos`, `conj`, `gen`, `mean`, `cl` = semantisch cluster, en voor werkwoorden de stamtijden in `gen`) die nu alleen in generate-scripts wordt gebruikt. Bij een V-knoop krijgt de leerling daardoor alleen de minimale graph-beschrijving te zien. Met een woordkaart-component zichtbaar maken bij elk V-item: stamtijden, genitief, geslacht, cluster.

## Input
- `data/vocab_sources/{lat_f01,lat_f02,lat_f03,grc_f01,grc_f02}_words.json`
- V-knopen in `data/graph/lat_vocabulaire_leerjaar1.json` en `data/graph/grc_vocabulaire_leerjaar1.json`
- Koppeling: V-knoop-ID (bijv. `LAT-V-F01-SUM`) → vocab_source-entry met `id: "SUM"` in `lat_f01_words.json`

## Acceptatiecriteria
- [x] Backend laadt vocab_sources bij startup en verrijkt V-knopen met `metadata: {pos, gen, conj, cl}` in de question-response (niet in de graph-JSONs zelf; runtime join)
- [x] Frontend-component `WoordKaart.jsx` toont deze metadata compact onder/naast een V-item
- [x] Eerste V-item ("herkenning" MC-type) toont metadata *pas* na antwoord-feedback (anders verklapt het het antwoord)
- [x] Productie-item toont metadata als hint/ondersteuning na foutieve poging
- [x] Unit-test: lookup werkt voor alle 450 V-knopen (geen missing lemma's)


<!-- legacy-bulk-checked: 2026-04-20 — AC retroactief afgevinkt door OL_E29_S7 cleanup -->

## Scope
- Nieuwe loader `src/gymnasium_classica/vocab/loader.py` (analoog aan passages/loader.py)
- API-wijziging: `Question.vocab_metadata` optioneel veld
- Frontend-component
- Tests

## Geschat
Medium
