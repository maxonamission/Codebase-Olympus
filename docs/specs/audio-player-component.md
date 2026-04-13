# AudioPlayer Component — Specificatie

**Status:** Stub/specificatie (fase 4 — geen React-code in huidige fase)
**Story:** B2-02

## Doel

Een herbruikbare React-component voor het afspelen van audio in luister-oefeningen. Wordt gebruikt in `luister_herkenning` en `luister_productie` items.

---

## Props

| Prop | Type | Required | Default | Beschrijving |
|------|------|----------|---------|--------------|
| `src` | `string` | ja | — | Pad naar audiobestand, relatief aan `data/audio/`. Bijv. `"LAT-V-F01-SUM.wav"` |
| `autoPlay` | `boolean` | nee | `false` | Start afspelen zodra component mount |
| `playbackRate` | `number` | nee | `1.0` | Initiële afspeelsnelheid |
| `allowRateChange` | `boolean` | nee | `true` | Toon snelheidsregelaar |
| `maxPlays` | `number \| null` | nee | `null` | Maximum aantal keer afspelen per oefening. `null` = onbeperkt. |
| `showWaveform` | `boolean` | nee | `false` | Toon een visuele golfvorm (stretch goal) |
| `disabled` | `boolean` | nee | `false` | Schakel interactie uit (bijv. na beantwoording) |
| `className` | `string` | nee | `""` | Extra CSS-klasse voor styling |

## Events (callbacks)

| Callback | Signature | Beschrijving |
|----------|-----------|--------------|
| `onPlay` | `() => void` | Geactiveerd bij start afspelen |
| `onPause` | `() => void` | Geactiveerd bij pauzeren |
| `onEnded` | `() => void` | Geactiveerd wanneer audio klaar is |
| `onPlayCountChange` | `(count: number) => void` | Geactiveerd bij elke afspeling; `count` is het totale aantal keer afgespeeld |
| `onRateChange` | `(rate: number) => void` | Geactiveerd bij snelheidswijziging |
| `onError` | `(error: Error) => void` | Geactiveerd bij laadfout of afspeelfout |

## Snelheidsregeling

De component biedt drie vooringestelde snelheden:

| Label | Rate | Gebruik |
|-------|------|---------|
| Langzaam | `0.75` | Eerste kennismaking, moeilijke woorden |
| Normaal | `1.0` | Standaard afspeelsnelheid |
| Snel | `1.25` | Herhaling, gevorderde leerlingen |

De snelheidsknop cycled door de opties: 0.75 -> 1.0 -> 1.25 -> 0.75.

## Gebruik in oefentypen

### luister_herkenning (receptief)

```
Leerling hoort audio -> kiest juiste vertaling uit meerkeuze

+------------------------------------------+
|  [>]  ▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐  [1.0x]       |
|                                          |
|  Wat hoor je?                            |
|                                          |
|  [ ] kunnen       [ ] zijn               |
|  [ ] gaan         [ ] doen               |
+------------------------------------------+
```

### luister_productie (productief)

```
Leerling hoort audio -> typt het woord in de originele taal

+------------------------------------------+
|  [>]  ▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐  [0.75x]      |
|                                          |
|  Schrijf wat je hoort:                   |
|                                          |
|  [ __________________ ]                  |
|                                          |
|  [Controleer]                            |
+------------------------------------------+
```

## API-contract (REST)

De frontend haalt audiobestanden op via een statisch pad:

```
GET /api/audio/{filename}
```

Voorbeeld: `GET /api/audio/LAT-V-F01-SUM.wav`

Response: binary audio/wav (of audio/mpeg voor MP3).

De FastAPI-backend serveert bestanden uit `data/audio/` via `StaticFiles`:

```python
from fastapi.staticfiles import StaticFiles

app.mount("/api/audio", StaticFiles(directory="data/audio"), name="audio")
```

## Toegankelijkheid

- `aria-label` op de afspeelknop: `"Speel audio af voor {lemma}"`
- Keyboard: `Space` = play/pause, `ArrowUp`/`ArrowDown` = snelheid wijzigen
- Focus-indicator op de afspeelknop
- Visuele indicatie van afspeelstatus (icoonwissel play/pause)

## Gedrag bij maxPlays

Wanneer `maxPlays` is ingesteld:
1. Na bereiken van het maximum wordt de afspeelknop uitgeschakeld
2. De teller toont `"3/3 afgespeeld"` (voorbeeld)
3. De `onPlayCountChange` callback wordt na elke afspeling aangeroepen
4. De scheduling-engine kan `maxPlays` per oefentype configureren

## Voorbeeld JSX (fase 4)

```jsx
<AudioPlayer
  src="LAT-V-F01-SUM.wav"
  autoPlay={true}
  maxPlays={3}
  onEnded={() => setShowOptions(true)}
  onPlayCountChange={(count) => logPlayCount(count)}
/>
```

## Afhankelijkheden

- Geen externe audio-libraries nodig — `HTMLAudioElement` API volstaat
- Golfvorm-visualisatie (stretch): `Web Audio API` (`AnalyserNode`)
- Styling: past in het bestaande designsysteem (fase 4)

## Open vragen (fase 4)

- [ ] Preloading-strategie: laden bij mount of bij eerste play?
- [ ] Offline support: cachen van audiobestanden via Service Worker?
- [ ] Audio-formaat: WAV (groot, ongecomprimeerd) vs. MP3/OGG (kleiner)?
- [ ] Waveform: prioriteit of stretch goal?
