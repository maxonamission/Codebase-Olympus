# TTS-evaluatie Latijn — Story B1-01

**Datum:** 2026-04-13
**Doel:** Evalueer beschikbare TTS-oplossingen voor klassiek Latijn met gerestaureerde uitspraak (niet kerklatijn). Selecteer de beste optie voor batch-generatie van ~300 vocabulaire-audiobestanden.

## Vereisten

- **Uitspraak:** gerestaureerde/klassieke uitspraak (c = /k/, v = /w/, diphthongen uitgesproken, ae = /ai/)
- **Macron-support:** cruciaal — macrons (ā, ē, ī, ō, ū) moeten klinkerlengte correct weergeven
- **Batch-generatie:** ~300 WAV/MP3-bestanden automatisch genereren
- **Licentie:** compatibel met educatief gebruik
- **Kwaliteit:** geschikt voor herhaald beluisteren door leerlingen

---

## Geëvalueerde opties

### 1. Poeta ex Machina

**Website:** [poetaexmachina.net](https://poetaexmachina.net/)
**Maker:** Lee Butterman (bachelorscriptie Brown University, Latijn + informatica)
**Technologie:** MBROLA met Italiaanse difoon-stem (Italiaans is fonetisch verwant aan Latijn)

| Criterium | Beoordeling |
|-----------|-------------|
| Uitspraakkwaliteit | Redelijk voor poëzie, klassieke uitspraak |
| Macron-support | **Nee** — leest geen gemacroniseerde tekst; doet interne macronisatie op basis van metrum |
| API/batch | Geen API; wel een GitHub-repo met bulk-MP3's (AGPL-3.0) |
| Licentie | Dataset: AGPL-3.0; webtool: onduidelijk |
| Kosten | Gratis |
| Onderhoud | Afgerond academisch project, geen actieve ontwikkeling |
| Bekende problemen | Geen /h/-klank, onjuiste /y/, geen onderscheid ph/p |

**Conclusie:** **Ongeschikt.** Kan geen gemacroniseerde input lezen — fataal voor vocabulaire-woorden waar klinkerlengte expliciet moet zijn. Ontworpen voor poëzie, niet voor losse woorden. Geen API.

---

### 2. Coqui TTS

**Repository:** [github.com/coqui-ai/TTS](https://github.com/coqui-ai/TTS)
**Status:** Bedrijf (Coqui AI) stopgezet eind 2023; project onderhouden door Idiap Research Institute en community. Release 0.27.3 (januari 2026).

| Criterium | Beoordeling |
|-----------|-------------|
| Latijn-support | **Nee** — Latijn niet in de 17 ondersteunde talen (XTTS-v2) |
| Custom training | Theoretisch mogelijk, maar: 10-30 uur Latijns audiomateriaal nodig; geen ingebouwde Latijnse fonemenizer; fine-tuning vanaf Italiaans riskeert "catastrophic forgetting" |
| Licentie | MPL 2.0 |
| Kosten | Gratis (open source) |
| Batch-generatie | Uitstekende CLI en Python-API zodra een model bestaat |
| Onderhoud | Actief (community-driven) |

**Conclusie:** **Niet haalbaar** zonder maandenlang werk. Er bestaat geen Latijns model en het opbouwen van een Latijns audiocorpus is een apart onderzoeksproject.

---

### 3. Piper TTS

**Repository:** [github.com/rhasspy/piper](https://github.com/rhasspy/piper)
**Technologie:** VITS-architectuur, gebruikt espeak-ng als fonemenizer

| Criterium | Beoordeling |
|-----------|-------------|
| Latijn-support | Geen voorgetraind model |
| Custom training | **Veelbelovend:** espeak-ng heeft al Latijnse fonemenregels (`la`), dus de grafeem-naar-foneem-pipeline bestaat. Training met klein dataset (1-3 uur opnames) is gedocumenteerd. Fine-tuning vanaf ander taalmodel mogelijk. |
| Licentie | MIT |
| Kosten | Gratis (open source) |
| Batch-generatie | Uitstekend — ontworpen voor snelle lokale inferentie |
| Onderhoud | Actief (Rhasspy-project) |

**Conclusie:** **Veelbelovend voor fase 2-3.** De espeak-ng fonemenizer handelt Latijn al correct af. Het knelpunt is het creëren van een trainingsdataset. Met 1-3 uur opnames van een classicus zou een bruikbaar Piper-model getraind kunnen worden.

---

### 4. eSpeak NG

**Repository:** [github.com/espeak-ng/espeak-ng](https://github.com/espeak-ng/espeak-ng)
**Technologie:** Formant-gebaseerde spraaksynthese, optioneel met MBROLA difoon-stemmen

| Criterium | Beoordeling |
|-----------|-------------|
| Latijn-support | **Ja** — taalcode `la`, klassieke uitspraakregels |
| Uitspraakkwaliteit | c = /k/, v = /w/, diphthongen correct, klassieke klemtoonregels |
| Macron-support | **Ja** — gemacroniseerde input wordt correct onderscheiden (lange vs. korte klinkers) |
| Audiokwaliteit | Slecht (robotachtig). Met MBROLA (`mb-la1`) iets beter, maar met bugs |
| MBROLA-bugs | Medeklinkerclusters laten klanken vallen; diftong "oe" verdwijnt soms; macron ā valt weg na s |
| API/batch | **Uitstekend:** `espeak-ng -v la -w output.wav "amīcus"` — triviale scripting |
| Licentie | GPL-3.0 (eSpeak NG); AGPL (MBROLA-stemmen) |
| Kosten | Gratis |
| Onderhoud | Actief, maar Latijn-specifieke bugs (issue #303) open sinds 2017 |

**Voorbeeld batch-generatie:**
```python
import subprocess

words = [("amīcus", "amicus"), ("bellum", "bellum"), ...]
for macronized, filename in words:
    subprocess.run(["espeak-ng", "-v", "la", "-s", "130",
                     "-w", f"data/audio/lat/{filename}.wav", macronized])
```

**Conclusie:** **Beste direct beschikbare optie.** Uitspraak is correct, macrons worden ondersteund, batch-generatie is triviaal. Audiokwaliteit is robotachtig maar functioneel. Geschikt als MVP-oplossing en als fonemenizer-frontend voor een neurale TTS-pipeline.

---

### 5. Overige onderzochte opties

| Optie | Beoordeling | Conclusie |
|-------|-------------|-----------|
| **ElevenLabs** | Claimt "Latin AI voices" in voice library, maar Latijn staat niet in de 32/74 officieel ondersteunde talen. Community-uploads zonder kwaliteitsgarantie. Geen macron-support. | Onbetrouwbaar — geen garantie op klassieke uitspraak |
| **Google Translate TTS** | Heeft een "Latijn"-optie, maar gebruikt de Italiaanse stem. Defectief Italianiserende uitspraak, geen klinkerlengte. | Onbruikbaar |
| **Google Cloud / Azure / Amazon Polly** | Geen Latijn-ondersteuning | Niet van toepassing |
| **Kveeky** | Claimt "advanced Latin TTS", maar geen bewijs van daadwerkelijk klassiek uitspraakmodel. Generieke marketing. | Vermoedelijk omverpakt generieke TTS |
| **Bark (Suno AI)** | Generatief audiomodel; Latijn niet ondersteund; geen fine-tuning-mechanisme | Niet van toepassing |
| **Kokoro / StyleTTS 2 / F5-TTS** | Nieuwste open-source modellen (2025-2026), hoge kwaliteit, maar geen Latijn-support | Niet van toepassing zonder significant onderzoek |
| **Handmatige opnames** | Hoogste kwaliteit; classicus inhuren via universiteit (Leiden, Amsterdam, Groningen). Kosten: EUR 500-1500 voor ~300 woorden. Niet schaalbaar. | Haalbaar alternatief voor v2 |

---

### 6. Hybride aanpak: eSpeak NG fonemenizer + neuraal TTS

Een veelbelovende aanpak die de sterke punten combineert:

1. **eSpeak NG** verzorgt de Latijnse grafeem-naar-foneem-conversie (handelt macrons en klassieke regels af)
2. **espeak-phonemizer** converteert eSpeak-output naar IPA geschikt voor neurale TTS-training
3. **Piper TTS** gebruikt deze fonemen voor synthese

Dit is de standaardaanpak voor het toevoegen van nieuwe talen aan Piper. Aangezien eSpeak NG al Latijnse foneemregels heeft, is de fonemenisatie-pipeline gereed. Het ontbrekende stuk is een Latijns audio-trainingsdataset.

---

## Samenvattingstabel

| Optie | Uitspraak | Audiokwaliteit | Macrons | Batch | Kosten | Inspanning | Aanbeveling |
|-------|-----------|----------------|---------|-------|--------|------------|-------------|
| **eSpeak NG `la`** | Uitstekend | Slecht (robotachtig) | Ja | Triviaal | Gratis | Minuten | **Gebruik nu (MVP)** |
| eSpeak NG `mb-la1` | Goed (enkele bugs) | Redelijk | Gedeeltelijk (bugs) | Triviaal | Gratis | Minuten | Testen, maar oppassen voor bugs |
| Poeta ex Machina | Goed (hiaten) | Redelijk | Nee (intern) | Geen API | Gratis | n.v.t. | Overslaan |
| **Piper (custom)** | Uitstekend (mits goed getraind) | Goed-uitstekend | Via eSpeak | Triviaal | Gratis + opnames | Weken | **Doel voor v2** |
| **Handmatige opnames** | Uitstekend | Uitstekend | n.v.t. | n.v.t. | EUR 500-1500 | Dagen | **Alternatief voor v2** |
| ElevenLabs | Onbekend | Hoog | Onbekend | API | $5+/mnd | Laag | Overslaan |
| Coqui TTS (custom) | Potentieel goed | Goed | Via fonemenizer | Ja | Gratis | Maanden | Te veel inspanning |
| Cloud TTS | n.v.t. | n.v.t. | n.v.t. | n.v.t. | n.v.t. | n.v.t. | Geen Latijn-support |

---

## Aanbeveling

### Fase 1 — MVP (nu)

**eSpeak NG met de standaard `la`-stem** is de enige tool die betrouwbaar aan alle eisen voldoet: klassieke uitspraak, macron-support en batch-generatie. De audiokwaliteit is robotachtig maar de uitspraak is correct. Implementatie is triviaal (zie voorbeeld hierboven). Dit produceert 300 WAV-bestanden in minder dan een minuut.

### Fase 2-3 — Verbeterde kwaliteit

**Pad A — Hybride pipeline (aanbevolen):**
1. Gebruik eSpeak NG als fonemenizer voor correcte Latijnse IPA uit gemacroniseerde tekst
2. Neem 1-2 uur op van een classicus die dezelfde 300 woorden leest
3. Train een Piper TTS-model met de eSpeak Latijnse fonemenizer + de opgenomen audio
4. Resultaat: natuurlijk klinkende stem met correcte klassieke uitspraak
5. Geschatte inspanning: 2-4 weken, kosten opnamesessie
6. Licenties: MIT (Piper) + GPL-3.0 (eSpeak NG fonemenizer)

**Pad B — Handmatige opnames:**
1. Vind een classicus (bijv. via een Nederlands universitair classica-departement)
2. Neem alle 300 woorden op met gemacroniseerde scripts
3. Post-process met Audacity (normaliseren, stilte trimmen)
4. Hoogste kwaliteit, meest authentiek
5. Geschatte inspanning: 1-2 dagen opname + 1 week bewerking
6. Kosten: EUR 500-1500
7. Niet schaalbaar als vocabulaire groeit

**Eindoordeel:** Begin met eSpeak NG voor de MVP. De uitspraak is correct, ook al klinkt de stem robotachtig. Voor een gepolijst product: investeer in een Piper custom model (schaalbaar, herbruikbaar) of handmatige opnames (hoogste kwaliteit maar niet schaalbaar). Het Piper-pad sluit beter aan bij de langetermijnbehoeften van het project, aangezien het vocabulaire voorbij 300 woorden zal groeien.

---

## Bronnen

- [Poeta ex Machina](https://poetaexmachina.net/)
- [Poeta ex Machina MP3 Recitations (GitHub)](https://github.com/lsb/poetaexmachina-mp3-recitations)
- [Lee Butterman — Tironiculum ASR for Latin](https://www.leebutterman.com/2022/03/01/automatic-speech-recognition-for-latin.html)
- [Coqui TTS (GitHub)](https://github.com/coqui-ai/TTS)
- [Piper TTS (GitHub)](https://github.com/rhasspy/piper)
- [Piper Training Documentation](https://github.com/rhasspy/piper/blob/master/TRAINING.md)
- [eSpeak NG (GitHub)](https://github.com/espeak-ng/espeak-ng)
- [eSpeak NG Latin issues (#303)](https://github.com/espeak-ng/espeak-ng/issues/303)
- [MBROLA Voices Repository](https://github.com/numediart/MBROLA-voices)
- [Classical Latin TTS (nesrad blog)](http://nesrad.blogspot.com/2017/09/classical-latin-text-to-speech-tts.html)
- [py-espeak-ng Python Wrapper](https://github.com/gooofy/py-espeak-ng)
- [espeak-phonemizer (PyPI)](https://pypi.org/project/espeak-phonemizer/)
- [ElevenLabs Supported Languages](https://help.elevenlabs.io/hc/en-us/articles/13313366263441-What-languages-do-you-support)
- [Open IPA Latin Transcription](https://www.openipa.org/transcription/latin)
- [Latin Text to Speech (Semantic Scholar)](https://www.semanticscholar.org/paper/Latin-Text-to-Speech-Leussen-Tromp/92feafc94b6b3361c5231c543f81bcfddd853b05)
