---
type: story
project: GC
epic: E20
story_id: OL_E20_S4
legacy_id: F1-04
track: content
status: done
prioriteit: middel
---

# Story OL_E20_S4: AudioPlayer component + afspelen van audio_ref in luister-items

## Doel
De 450 WAV-bestanden in `data/audio/` worden nergens afgespeeld. `audio_ref` staat in de item-stimulus én als top-level veld op items (`models/graph.py:97-100`), maar noch de API serveert ze, noch de frontend speelt ze af. Zonder audio-playback zijn `luister_herkenning` en `luister_productie` items functioneel identiek aan gewone MC/text-items.

## Input
- `data/audio/*.wav` (450 placeholders, 4454 B elk — echte audio volgt in Epic E2)
- `src/gymnasium_classica/api/app.py` — backend moet `/audio/{filename}` serveren (StaticFiles)
- `frontend/src/components/AnswerInput.jsx`
- Item-types: `luister_herkenning`, `luister_productie`

## Acceptatiecriteria
- [x] FastAPI serveert `data/audio/` op pad `/audio/{filename}` als static files (read-only)
- [x] Nieuwe component `frontend/src/components/AudioPlayer.jsx` met play/stop en replay-knop
- [x] Voor items met `stimulus.audio_ref` wordt de player getoond boven de opties/input
- [x] Geen autoplay (WCAG/UX); leerling drukt zelf op play
- [x] Werkt met zowel placeholder-stubs als echte audio (zodra E2 geleverd is)
- [x] Backend-test: audio-endpoint retourneert 200 + correct content-type; 404 bij onbekend bestand


<!-- legacy-bulk-checked: 2026-04-20 — AC retroactief afgevinkt door OL_E29_S7 cleanup -->

## Scope
- `app.py`: `app.mount("/audio", StaticFiles(directory=AUDIO_DIR))` (met veiligheidscheck: alleen `.wav`/`.mp3`)
- Nieuwe React component
- Integratie in `AnswerInput` of apart boven `QuestionCard`
- Eén regressie-test per kant (backend + frontend smoketest)

## Geschat
Medium (backend static-mount + 1 component + tests)
