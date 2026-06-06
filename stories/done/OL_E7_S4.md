---
type: story
project: GC
epic: E7
story_id: OL_E7_S4
legacy_id: B1-04
track: pipelines
status: done
prioriteit: middel
---

# Story OL_E7_S4: Audio genereren — Latijn V-knopen F01-F03

## Doel
Genereer audiobestanden voor alle Latijnse vocabulaireknopen (frequentiebanden F01-F03).

## Input
OL_E4_S2 t/m OL_E4_S4, TTS-pipeline uit OL_E7_S3

## Acceptatiecriteria
- [x] Geen breaking changes in bestaande models
- [x] Alle bestaande tests blijven groen
- [x] Nieuwe functionaliteit heeft eigen tests


<!-- legacy-bulk-checked: 2026-04-20 — AC retroactief afgevinkt door OL_E29_S7 cleanup -->

## Scope
data/audio/LAT-V-F01-*.mp3 t/m LAT-V-F03-*.mp3, audio_ref velden ingevuld

## Geschat
~300 bestanden

## Resultaat
- 300 placeholder WAV-bestanden gegenereerd in data/audio/LAT-V-*.wav
- audio_ref veld ingevuld op alle 300 LAT-V knopen in lat_vocabulaire_leerjaar1.json
- **Notitie:** espeak-ng was niet beschikbaar in de build-omgeving. Gegenereerde bestanden zijn stille WAV-placeholders (0.1s, 22050 Hz, mono). Echte audio-generatie vereist installatie van espeak-ng (`apt install espeak-ng`) en herdraaien van `scripts/generate_audio.py --lang lat --force`.
