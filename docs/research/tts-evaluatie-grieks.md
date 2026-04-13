# TTS-evaluatie Grieks — Story B1-02

**Datum:** 2026-04-13
**Doel:** Evalueer beschikbare TTS-oplossingen voor klassiek/oud-Grieks met Erasmiaanse uitspraak, zoals onderwezen op het Nederlandse gymnasium. Selecteer de beste optie voor batch-generatie van ~150 vocabulaire-audiobestanden.

## Vereisten

- **Uitspraak:** Erasmiaans (zoals in het Nederlandse gymnasiumonderwijs), niet Modern Grieks
- **Kernverschillen met Modern Grieks:** onderscheiden klinkers (η ≠ ι ≠ ει ≠ οι), uitgesproken spiritus asper/lenis, diphthongen als diphthongen, geen iotacisme
- **Polytoon Grieks:** volledige ondersteuning voor polytone diakritische tekens (ἀ, ἁ, ά, ᾶ, ᾳ, etc.)
- **Batch-generatie:** ~150 WAV/MP3-bestanden automatisch genereren
- **Licentie:** compatibel met educatief gebruik
- **Kwaliteit:** geschikt voor herhaald beluisteren door leerlingen

---

## Geëvalueerde opties

### 1. Poeta ex Machina

**Website:** [poetaexmachina.net](https://poetaexmachina.net/)
**Maker:** Lee Butterman (Brown University)

| Criterium | Beoordeling |
|-----------|-------------|
| Grieks-support | Primair een Latijns poëzie-tool; beperkte/onduidelijke Griekse ondersteuning |
| Uitspraaksysteem | Klassiek (gereconstrueerd) voor Latijn, niet expliciet Erasmiaans Grieks |
| Polytone ondersteuning | Niet bevestigd; de tool richt zich op Latijnse metrische tekst |
| Erasmiaanse nauwkeurigheid | Slecht — geen /h/-klank (cruciaal: geen spiritus asper), geen onderscheid ph/p, onjuiste /y/ |
| API/batch | Geen — alleen webinterface |
| Kosten | Gratis |
| Onderhoud | Beperkt onderhouden, smal gefocust op Latijnse poëzie |

**Conclusie:** **Ongeschikt.** Fundamentele uitspraakhiaten maken het onbruikbaar voor Erasmiaans Grieks. Geen spiritus asper, geen ph/p-onderscheid — dit zijn diskwalificerende tekortkomingen.

---

### 2. Google Cloud TTS met SSML

**Documentatie:** [Google Cloud TTS](https://cloud.google.com/text-to-speech)

| Criterium | Beoordeling |
|-----------|-------------|
| Grieks-support | Alleen Modern Grieks (el-GR) — geen oud-Grieks taalcode |
| Stemmen | Meerdere Modern Griekse stemmen: Standard, WaveNet, Neural2, Chirp 3 HD |
| SSML `<phoneme>` tags | Grieks (el-GR) staat **niet** in de lijst van talen met foneemtag-ondersteuning. Alleen Engels, Mandarijn, Kantonees en Japans worden ondersteund. |
| Erasmiaanse haalbaarheid | Zeer slecht — zonder foneemtags kan Modern Griekse uitspraak niet overschreven worden. Zelfs met tags: het stemmodel heeft Modern Griekse prosodie ingebakken. |
| Polytone input | Zou polytone diakritische tekens waarschijnlijk strippen/negeren |
| Batch-generatie | Uitstekende API, eenvoudig te automatiseren |
| Kosten | Standard: $4/1M tekens; WaveNet: $16/1M tekens. Gratis tier: 1M WaveNet tekens/mnd. Voor ~150 woorden verwaarloosbaar. |
| Audiokwaliteit | Uitstekend voor Modern Grieks — volledig onbruikbaar voor Erasmiaans |

**Conclusie:** **Ongeschikt.** Modern Griekse uitspraak is fundamenteel onverenigbaar met Erasmiaans. Het kernprobleem is iotacisme: in Modern Grieks klinken η, ι, ει, οι allemaal als /i/ — precies het onderscheid dat Erasmiaans wél maakt. Zelfs met SSML-manipulatie zou je tegen het volledige fonologische systeem van het stemmodel invechten.

---

### 3. eSpeak NG (Oud-Grieks)

**Repository:** [github.com/espeak-ng/espeak-ng](https://github.com/espeak-ng/espeak-ng)

| Criterium | Beoordeling |
|-----------|-------------|
| Oud-Grieks support | **Ja** — taalcode `grc`. Een van de weinige TTS-engines met expliciete oud-Griekse ondersteuning. |
| Uitspraaksysteem | Gereconstrueerd klassiek Grieks — overlapt sterk met Erasmiaans (beide pre-iotacisme) |
| Polytone ondersteuning | Verwerkt Unicode polytoon Grieks (diakritische tekens, spiritus) |
| Erasmiaanse nauwkeurigheid | Matig — uitspraakregels zijn gebaseerd op gereconstrueerd oud-Grieks, wat grotendeels overeenkomt met Erasmiaans |
| Audiokwaliteit | **Zeer slecht** — beschreven als "naïeve initiële implementatie" en "bijna onverstaanbaar". Formant-synthese, robotachtig. |
| API/batch | Uitstekend: `espeak-ng -v grc -w output.wav "λόγος"` |
| Licentie | GPL-3.0 |
| Kosten | Gratis |
| Onderhoud | Project actief, maar de oud-Griekse stem heeft minimale aandacht gekregen |

**Conclusie:** **Functioneel maar kwaliteit is diskwalificerend voor een educatief product.** De robotachtige, nauwelijks verstaanbare klank zou leerlingen frustreren. Kan dienen als technisch prototype of placeholder, maar niet als primaire audiobron.

---

### 4. Handmatige opnames

| Criterium | Beoordeling |
|-----------|-------------|
| Scope | ~150 woorden. Bij ~3-5 seconden per woord: ca. 8-12 minuten totale audio. |
| Tijdsinschatting | Opname: 2-4 uur (incl. setup, retakes, verificatie). Post-processing: 2-4 uur (normalisatie, stilte trimmen, bestandsnaamgeving). Totaal: ~1 dag werk. |
| Kosteninschatting | Optie A: Classica-docent inhuren — EUR 200-500 voor een halve dag. Optie B: Freelancer via Fiverr/Upwork met classica-achtergrond — $50-200. Optie C: Nederlandse gymnasiumdocent of universitair docent — potentieel gratis of nominale vergoeding. |
| Waar sprekers te vinden | Nederlandse universiteiten met GLTC-programma's (Leiden, UvA/VU Amsterdam, Groningen, Nijmegen, Utrecht). Nederlandse gymnasiumdocenten (opgeleid in Erasmiaans). |
| Bestaand Erasmiaans audiomateriaal | [Forvo](https://forvo.com/languages/grc/) — enkele oud-Griekse woorden, maar dekking is schaars en uitspraaksysteem varieert. Athenaze-leerboek audio — gereconstrueerde uitspraak (dicht bij Erasmiaans). [Austrian Academy of Sciences](https://www.oeaw.ac.at/kal/agp/) — klassieke uitspraaksamples, maar passage-niveau, niet woordniveau. |
| Kwaliteitscontrole | Te verifiëren: (1) correcte Erasmiaanse klinkeronderscheidingen, (2) spiritus uitgesproken, (3) consistent accentplaatsing, (4) schone audio zonder achtergrondgeluid. Tweede classicus voor review. |
| Erasmiaanse nauwkeurigheid | Hoogst mogelijke — je controleert de sprekerselectie. Een Nederlands-opgeleide classicus gebruikt exact de Erasmiaanse variant die op Nederlandse scholen onderwezen wordt. |
| Licentie | Volledig eigendom bij opdrachtwerk (work-for-hire contract aanbevolen) |

**Conclusie:** **Meest betrouwbare optie voor kwaliteit en nauwkeurigheid.** De scope (~150 woorden) is klein genoeg om praktisch te zijn. Kosten zijn bescheiden. De uitdaging is het vinden en plannen van een geschikte spreker, maar Nederlandse universiteiten en gymnasia bieden een natuurlijke pool.

---

### 5. Overige onderzochte opties

#### 5a. Cartesia Sonic TTS (met IPA-uitspraakoverride)

**Website:** [cartesia.ai](https://cartesia.ai/sonic)
**Technologie:** Sonic-2 model ondersteunt aangepaste uitspraak via MFA-stijl IPA voor alle talen, inclusief Modern Grieks.

| Criterium | Beoordeling |
|-----------|-------------|
| Haalbaarheid | Theoretisch mogelijk: Modern Griekse stem met per-woord IPA-overrides naar Erasmiaanse foneemwaarden |
| Benodigde inspanning | Matig: IPA-lookup-tabel voor 150 woorden aanmaken (2-4 uur voor classicus met IPA-kennis) |
| Kwaliteit | Onderliggende stem is Modern Grieks (neuraal, natuurlijk). Met IPA-overrides zouden individuele fonemen correct zijn, maar prosodie blijft Modern Grieks. |
| Risico | De MFA-foneemset voor Grieks bevat mogelijk niet alle benodigde Erasmiaanse fonemen (bijv. /ɛː/ voor eta, /ɔː/ voor omega, geaspireerde stops). Ongetest voor dit gebruik. |
| Kosten | $0,03/minuut audio. Voor ~150 woorden (~10 min): ca. $0,30. |
| API | Ja, REST API met Python SDK |

**Conclusie:** **Veelbelovend maar onbewezen.** Een proof-of-concept met 5-10 woorden is raadzaam voordat je committeert. De IPA-override-aanpak is creatief maar de resultaten zijn onvoorspelbaar.

#### 5b. Microsoft Azure TTS

Modern Griekse neurale stem (`el-GR-AthinaNeural`). Grieks staat **niet** in de lijst van talen die SSML-foneemtags (IPA) ondersteunen. Zelfde fundamentele probleem als Google Cloud TTS.

**Conclusie:** Ongeschikt.

#### 5c. Amazon Polly

Ondersteunt **geen Grieks** — el-GR staat niet in de ondersteunde talenlijst.

**Conclusie:** Niet beschikbaar.

#### 5d. ElevenLabs

IPA-foneemtags werken alleen met Engelse modellen. Voor andere talen is alleen "alias"-substitutie beschikbaar. Voice cloning vereist opnames (kip-en-ei-probleem).

**Conclusie:** Ongeschikt voor direct gebruik.

#### 5e. ancientgreekspeak (GitHub)

**Repository:** [github.com/ryanfb/ancientgreekspeak](https://github.com/ryanfb/ancientgreekspeak)
Ruby-tool die polytoon Grieks translitereert naar Apple-fonemen, gepijpt naar macOS `say`. MIT-licentie. Laatste update 2019.

**Conclusie:** Platformgebonden aan macOS, niet productiekwaliteit, verlaten project.

#### 5f. Piper TTS / Coqui TTS

Beide hebben Modern Grieks maar geen oud-Grieks. Geen aanpasbaar uitspraakmechanisme. Custom training vereist een audiocorpus dat niet bestaat.

**Conclusie:** Niet geschikt zonder enorme inspanning.

---

## Samenvattingstabel

| Optie | Audiokwaliteit | Erasmiaanse nauwkeurigheid | Polytoon | API/Batch | Kosten | Inspanning | Aanbeveling |
|-------|----------------|---------------------------|----------|-----------|--------|------------|-------------|
| **Handmatige opnames** | Uitstekend | Uitstekend | n.v.t. | Nee | EUR 200-500 | Laag (1 dag) | **AANBEVOLEN** |
| **Cartesia Sonic + IPA** | Goed (neuraal) | Onzeker | Via IPA | Ja | ~$1 | Matig (IPA-mapping) | Testen waard |
| eSpeak-ng (`grc`) | Zeer slecht | Matig | Ja | Ja | Gratis | Laag | Alleen prototype/placeholder |
| Poeta ex Machina | n.v.t. voor Grieks | Slecht | Nee | Nee | Gratis | Laag | Ongeschikt |
| Google Cloud TTS | n.v.t. (Modern) | Geen | Nee | Ja | Verwaarloosbaar | n.v.t. | Ongeschikt |
| Azure TTS | n.v.t. (Modern) | Geen | Nee | Ja | Verwaarloosbaar | n.v.t. | Ongeschikt |
| ElevenLabs | n.v.t. | Geen | Nee | Ja | $99/mnd | n.v.t. | Ongeschikt |
| Piper / Coqui (custom) | n.v.t. (geen model) | n.v.t. | n.v.t. | Ja | Gratis | Maanden | Te veel inspanning |

---

## Aanbeveling

### Primaire aanpak: handmatige opnames door een Nederlands-opgeleide classicus

**Rationale:**
- **150 woorden is een kleine, beheersbare scope.** Dit is een halve dag opnamesessie, geen grote productie.
- **Erasmiaanse uitspraak zoals onderwezen op Nederlandse scholen is de eis.** Geen enkele TTS-engine implementeert dit. Een Nederlandse gymnasiumdocent of GLTC-universitair docent is de enige bron die de exacte uitspraakvariant garandeert.
- **Kosten zijn laag.** EUR 200-500 voor opdrachtopnames, potentieel minder bij een universiteitscontact.
- **Kwaliteit is het hoogst.** Neurale TTS-stemmen voor Modern Grieks klinken natuurlijk maar spreken alles verkeerd uit voor Erasmiaans. Een menselijke spreker klinkt natuurlijk EN spreekt correct uit.
- **Volledig IE-eigendom.** Work-for-hire geeft volledige controle over de audiobestanden.
- **Toekomstbestendig.** Audiobestanden kunnen onbeperkt hergebruikt worden. Bij uitbreiding van de woordenlijst zijn extra opnamesessies eenvoudig.

### Secundaire/experimentele aanpak: Cartesia Sonic met IPA-overrides

Een proof-of-concept met 5-10 woorden is raadzaam:
1. Maak een Erasmiaanse IPA-transcriptie voor elk testwoord
2. Gebruik Cartesia Sonic-2's `<< >>`-syntax om uitspraak te specificeren
3. Evalueer of het Modern Griekse stemmodel acceptabele resultaten produceert met Erasmiaanse fonemen

Als dit goed werkt, kan het dienen als schaalbare aanvulling voor toekomstige vocabulaire-uitbreiding voorbij de initiële 150 woorden (bijv. leerjaar 2-3). De kosten zijn verwaarloosbaar en de batch-verwerkingscapaciteit via API is uitstekend.

### Prototype/placeholder: eSpeak-ng

Houd eSpeak-ng (`espeak-ng -v grc`) in de gereedschapskist als:
- Ontwikkelingsplaceholder terwijl opnames worden geregeld
- Toegankelijkheids-fallback voor screenreaders
- Gratis, open-source optie die fonemen tenminste bij benadering correct weergeeft

### Voorgestelde workflow

1. Bouw de Cartesia Sonic proof-of-concept nu (1-2 uur, vrijwel geen kosten)
2. Neem contact op met een Nederlands classica-departement of gymnasiumdocent voor opnameplanning
3. Gebruik eSpeak-ng als placeholder-audio tijdens ontwikkeling
4. Vervang door professionele opnames wanneer beschikbaar
5. Sla audiobestanden op in `data/content/audio/{KNOOP_ID}.mp3`

### Verschil met Latijn-evaluatie

De situatie voor Grieks is fundamenteel anders dan voor Latijn:
- **Latijn:** eSpeak NG (`la`) levert bruikbare uitspraak met correcte macron-support — geschikt als MVP
- **Grieks:** eSpeak NG (`grc`) is te slecht voor productiegebruik — handmatige opnames zijn de primaire aanbeveling
- **Reden:** de Latijnse stem in eSpeak is beter ontwikkeld en verstaanbaarder dan de oud-Griekse

---

## Bronnen

- [Poeta ex Machina](https://poetaexmachina.net/)
- [Linguae — Latin & Ancient Greek Speech Engines](https://linguae.weebly.com/latin--ancient-greek-speech-engines.html)
- [eSpeak-ng (GitHub)](https://github.com/espeak-ng/espeak-ng)
- [eSpeak-ng Languages](https://github.com/espeak-ng/espeak-ng/blob/master/docs/languages.md)
- [Google Cloud TTS Pricing](https://cloud.google.com/text-to-speech/pricing)
- [Google Cloud TTS Phonemes](https://docs.cloud.google.com/text-to-speech/docs/phonemes)
- [Azure Speech Service](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support)
- [Cartesia Custom Pronunciations](https://docs.cartesia.ai/2025-04-16/build-with-cartesia/capability-guides/specify-custom-pronunciations)
- [ancientgreekspeak (GitHub)](https://github.com/ryanfb/ancientgreekspeak)
- [Forvo — Ancient Greek](https://forvo.com/languages/grc/)
- [Austrian Academy — Sound of Ancient Greek](https://www.oeaw.ac.at/kal/agp/)
- [Wikipedia — Pronunciation of Ancient Greek in Teaching](https://en.wikipedia.org/wiki/Pronunciation_of_Ancient_Greek_in_teaching)
- [Piper TTS (GitHub)](https://github.com/rhasspy/piper)
- [ElevenLabs Supported Languages](https://help.elevenlabs.io/hc/en-us/articles/13313366263441-What-languages-do-you-support)
- [Fiverr Ancient Greek Experts](https://www.fiverr.com/hire/ancient-greek)
