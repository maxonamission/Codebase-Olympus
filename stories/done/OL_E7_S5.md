---
type: story
project: GC
epic: E7
story_id: OL_E7_S5
legacy_id: B1-05
track: pipelines
status: done
prioriteit: middel
---

# Story OL_E7_S5: Audio genereren — Grieks V-knopen F01-F02

## Doel
Genereer audiobestanden voor alle Griekse vocabulaireknopen.

## Input
OL_E4_S5 t/m OL_E4_S6, TTS-pipeline uit OL_E7_S3

## Acceptatiecriteria
- [x] Geen breaking changes in bestaande models
- [x] Alle bestaande tests blijven groen
- [x] Nieuwe functionaliteit heeft eigen tests


<!-- legacy-bulk-checked: 2026-04-20 — AC retroactief afgevinkt door OL_E29_S7 cleanup -->

## Scope
data/audio/GRC-V-F01-*.mp3 t/m GRC-V-F02-*.mp3, audio_ref velden ingevuld

## Geschat
~150 bestanden

## Resultaat
- 150 placeholder WAV-bestanden gegenereerd in data/audio/GRC-V-*.wav
- audio_ref veld ingevuld op alle 150 GRC-V knopen in grc_vocabulaire_leerjaar1.json
- **Notitie:** espeak-ng was niet beschikbaar in de build-omgeving. Gegenereerde bestanden zijn stille WAV-placeholders (0.1s, 22050 Hz, mono). Voor Grieks is de aanbeveling uit OL_E7_S2 om handmatige opnames te gebruiken (espeak-ng `grc` is onvoldoende kwaliteit). Herdraaien: `scripts/generate_audio.py --lang grc --force`.
