# Vocabulairestrategie — Gymnasium Classica leerjaar 1

## Bronnen

| Bron | Taal | Omvang | Licentie | Rol |
|------|------|--------|----------|-----|
| DCC Latin Core Vocabulary | Latijn | 1.000 lemma's, ~70% tekstdekking | CC BY-SA 3.0 | Primaire frequentiebron |
| DCC Ancient Greek Core Vocabulary | Grieks | 500 lemma's, ~65% tekstdekking | CC BY-SA 3.0 | Primaire frequentiebron |
| CvTE-minimumlijst Latijn (LTC 2026) | Latijn | Vormleer + syntaxis | Publiek | Cross-referentie grammatica |
| CvTE-minimumlijst Grieks (GTC 2026) | Grieks | Vormleer + syntaxis | Publiek | Cross-referentie grammatica |

**Keuze DCC als primaire bron:** De CvTE-minimumlijst bevat geen vocabulaire. De DCC-frequentielijsten zijn de beste methode-onafhankelijke bron: de eerste ~300 Latijnse en ~200 Griekse woorden corresponderen goed met het klas 1-vocabulaire ongeacht de gebruikte methode (SPQR, Fortuna, Pallas, ARGO).

## Frequentiebanden

| Band | Latijn | Grieks |
|------|--------|--------|
| F01 | woorden 1-100 | woorden 1-75 |
| F02 | woorden 101-200 | woorden 76-150 |
| F03 | woorden 201-300 | — |

**Totaal:** ~300 Latijnse knopen + ~150 Griekse knopen = ~450 vocabulaireknopen.

## Semantische clusters

De 13 clusters in `data/vocabulaire_clusters.json` dekken het vocabulairedomein van leerjaar 1:

| Cluster | Scope |
|---------|-------|
| `familie` | Familierelaties, huishouden |
| `oorlog` | Oorlog, militaire zaken |
| `lichaam` | Lichaamsdelen, fysieke eigenschappen |
| `politiek` | Politiek, bestuur, recht |
| `religie` | Religie, goden, ritueel |
| `natuur` | Natuur, landschap, weer |
| `emotie` | Emoties, mentale toestanden |
| `beweging` | Beweging, richting, reizen |
| `communicatie` | Communicatie, spreken, schrijven |
| `tijd` | Tijd, duur, leeftijd |
| `gebouwen` | Gebouwen, ruimte, stad |
| `voedsel` | Voedsel, drinken, maaltijd |
| `onderwijs` | Onderwijs, kennis, kunst |

**Onverbuigbare woorden** (voorzetsels, conjuncties, bijwoorden, partikels) krijgen `semantisch_cluster: null`. Ze veroorzaken geen semantische interferentie en hoeven niet gespreid te worden door de scheduling engine.

## Knoopconventies

### ID-formaat
`{TAAL}-V-{BAND}-{LEMMA}` — voorbeeld: `LAT-V-F01-TERRA`
- LEMMA: uppercase, max 8 tekens, eerste hoofddeel (nominatief voor substantieven, 1e persoon sg. voor werkwoorden)

### titel_nl
- Substantieven: `terra, -ae (v.) — aarde, land`
- Werkwoorden: `dare, dedi, datum (1) — geven`
- Adjectieven: `magnus, -a, -um — groot`
- Onverbuigbaar: `sed (conj.) — maar`

### beschrijving
- Substantieven: `Het zelfstandig naamwoord terra, -ae (v.): aarde, land. 1e declinatie. Frequentieband F01.`
- Werkwoorden: `Het werkwoord dare (geven): regelmatig. 1e conjugatie. Frequentieband F01.`
- Onregelmatig: `Het werkwoord esse (zijn): onregelmatig, alle vormen suppletief. Frequentieband F01.`
- Adjectieven: `Het bijvoeglijk naamwoord magnus, -a, -um: groot. 1e/2e declinatie. Frequentieband F01.`
- Onverbuigbaar: `Het voorzetsel in (+acc/abl): in, naar (binnen). Onverbuigbaar. Frequentieband F01.`

### Overige velden
- `bloom_niveau`: `kennis` (herkennen van betekenis)
- `fase`: `onderbouw_1`
- `toetsbaar`: `true`

## Edge-strategie

Elk vocabulairewoord krijgt maximaal 1 prerequisite-edge naar de relevante grammatica-INTRO-knoop:

| Woordsoort | Target | Weight |
|------------|--------|--------|
| 1e decl. substantief | `LAT-G-MORF-DECL1-INTRO` | 0.3 |
| 2e decl. substantief | `LAT-G-MORF-DECL2-INTRO` | 0.3 |
| 3e decl. substantief | `LAT-G-MORF-DECL3-INTRO` | 0.3 |
| 4e/5e decl. substantief | Geen (buiten scope leerjaar 1) | — |
| Werkwoord 1e-4e conj. | `LAT-G-MORF-CONJ{N}-INTRO` | 0.3 |
| Werkwoord 3e-io conj. | `LAT-G-MORF-CONJ3B-INTRO` | 0.3 |
| Onregelmatig werkwoord | `LAT-G-MORF-PRAES-INTRO` | 0.3 |
| Bijvoeglijk naamwoord | `LAT-G-MORF-ADJ-INTRO` | 0.3 |
| Voornaamwoord | `LAT-G-MORF-PRON-INTRO` | 0.3 |
| Voorzetsel | `LAT-G-SYNT-PREP-INTRO` | 0.3 |
| Voegwoord/bijwoord/partikel | Geen (leaf node) | — |

## Groepknopen

Geen groepknopen per frequentieband. Bij ~100 woorden over 13 clusters is het gemiddelde ~6 per cluster — onder de drempel van 10 voor groepering.
