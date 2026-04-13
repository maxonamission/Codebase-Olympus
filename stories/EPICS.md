# Spoor A — Epics overzicht

Knowledge graph content voor leerjaar 1 gymnasium, beide talen.
Doelomvang: ~850 knopen, ~1500-2000 edges.

## Uitvoervolgorde

1. **A3** (alfabet) — klein, zelfstandig, blokkeert niets
2. **A1** (grammatica Latijn) — bouwt voort op de 50 PoC-knopen
3. **A2** (grammatica Grieks) — structureel parallel aan A1
4. **A4** (vocabulaire) — heeft A1+A2+A3 nodig voor prerequisite-edges
5. **A5** (cultuur) — onafhankelijk van A1-A4 maar edges lopen ernaar
6. **A6** (transfer-edges) — heeft A1+A2+A3+A4+A5 nodig

---

## Epic A1: Grammatica Latijn

**Doel:** Methode-onafhankelijke grammaticale kern van klas 1, gebaseerd op de CvTE-minimumlijst gefilterd op wat alle methoden gemeen hebben.
**Geschat:** ~150 knopen
**Afhankelijkheden:** Geen (bouwt voort op bestaande PoC)
**Status:** todo
**Bestand:** `data/graph/lat_grammatica_leerjaar1.json`

| Story | Titel | Knopen | Status |
|-------|-------|--------|--------|
| A1-01 | Conceptknopen en naamvalsysteem | ~15 | todo |
| A1-02 | 1e declinatie — alle naamvallen + paradigma | ~10 | todo |
| A1-03 | 2e declinatie — o-stammen masculinum + neutrum | ~12 | todo |
| A1-04 | 3e declinatie — consonantstammen + i-stammen basis | ~15 | todo |
| A1-05 | Adjectieven bonus-type en fortis-type | ~10 | todo |
| A1-06 | Werkwoord-concepten — conjugatie-intro, persoon, tempus, modus | ~10 | todo |
| A1-07 | Praesens indicativus actief — 4 conjugaties + esse | ~15 | todo |
| A1-08 | Imperfectum indicativus actief | ~8 | todo |
| A1-09 | Perfectum indicativus actief — inclusief stamtijdentypen | ~12 | todo |
| A1-10 | Plusquamperfectum indicativus actief | ~5 | todo |
| A1-11 | Imperativus + infinitivus praesens actief | ~6 | todo |
| A1-12 | Pronomina — persoonlijk, bezittelijk, aanwijzend begin | ~12 | todo |
| A1-13 | Voorzetsels met accusativus en ablativus | ~8 | todo |
| A1-14 | Basissyntaxis — woordvolgorde, congruentie, ontkenning, vraagzinnen | ~12 | todo |
| A1-15 | Review en prerequisite-edge validatie voor heel epic A1 | — | todo |

---

## Epic A2: Grammatica Grieks

**Doel:** Griekse grammaticale kern van klas 1, gebaseerd op de GTC-minimumlijst gefilterd op klas 1 scope (Pallas les 1-14 / ARGO thema 1-4).
**Geschat:** ~100 knopen
**Afhankelijkheden:** A3 (alfabet moet af als prerequisite)
**Status:** todo
**Bestand:** `data/graph/grc_grammatica_leerjaar1.json`

| Story | Titel | Knopen | Status |
|-------|-------|--------|--------|
| A2-01 | Conceptknopen Grieks — lidwoord, naamvalsysteem | ~10 | todo |
| A2-02 | 1e declinatie (α/η-stammen) | ~10 | todo |
| A2-03 | 2e declinatie (ο-stammen) | ~10 | todo |
| A2-04 | 3e declinatie introductie — via adjectieven πᾶς, σώφρων | ~8 | todo |
| A2-05 | Adjectieven α/ο-stam en medeklinkerstam | ~8 | todo |
| A2-06 | Praesens indicativus actief — thematisch + contracta + εἰμί | ~12 | todo |
| A2-07 | Imperfectum indicativus actief — augment | ~8 | todo |
| A2-08 | Aoristus introductie — sigmatisch + thematisch | ~10 | todo |
| A2-09 | Pronomina — persoonlijk, bezittelijk, aanwijzend | ~10 | todo |
| A2-10 | Voorzetsels + basissyntaxis | ~8 | todo |
| A2-11 | Review en prerequisite-edge validatie voor heel epic A2 | — | todo |

---

## Epic A3: Grieks alfabet — onboarding-subgraph

**Doel:** Grieks alfabet als onboarding-subgraph. Prerequisite voor alle GRC-grammaticaknopen.
**Geschat:** ~40 knopen
**Afhankelijkheden:** Geen
**Status:** todo
**Bestand:** `data/graph/grc_alfabet.json`

| Story | Titel | Knopen | Status |
|-------|-------|--------|--------|
| A3-01 | Letters herkenning — 24 letters, majuskel + minuskel | ~24 | todo |
| A3-02 | Diakritische tekens — spiritus, accenten, iota subscriptum | ~8 | todo |
| A3-03 | Lettercombinaties en uitspraak — diphthongen, γγ=ng, speciale combinaties | ~8 | todo |

---

## Epic A4: Vocabulaire

**Doel:** Individuele woorden, frequentiegestuurd, met semantisch cluster.
**Geschat:** ~450 knopen
**Afhankelijkheden:** A1, A2, A3 (voor prerequisite-edges naar grammaticaknopen)
**Status:** todo
**Bestanden:** `data/graph/lat_vocabulaire_leerjaar1.json`, `data/graph/grc_vocabulaire_leerjaar1.json`

| Story | Titel | Knopen | Status |
|-------|-------|--------|--------|
| A4-01 | Strategie en bronnen — DCC Latin/Greek Core, cluster-definitie | — | todo |
| A4-02 | Latijn frequentieband F01 — top-100 woorden | ~100 | todo |
| A4-03 | Latijn frequentieband F02 — woorden 101-200 | ~100 | todo |
| A4-04 | Latijn frequentieband F03 — woorden 201-300 | ~100 | todo |
| A4-05 | Grieks frequentieband F01 — top-75 woorden | ~75 | todo |
| A4-06 | Grieks frequentieband F02 — woorden 76-150 | ~75 | todo |
| A4-07 | Prerequisite-edges vocabulaire → grammatica | — | todo |

---

## Epic A5: Cultuur

**Doel:** Gedeelde (SHA-C-*) cultuurknopen voor leerjaar 1.
**Geschat:** ~70 knopen
**Afhankelijkheden:** Geen (maar enrichment-edges naar A1/A2/A4)
**Status:** todo
**Bestand:** `data/graph/sha_cultuur_leerjaar1.json`

| Story | Titel | Knopen | Status |
|-------|-------|--------|--------|
| A5-01 | Mythologie — Olympische goden, helden, Troje, Odysseus | ~20 | todo |
| A5-02 | Romeins dagelijks leven — familia, domus, school, eten, slavernij | ~15 | todo |
| A5-03 | Geschiedenis basis — Romulus, Republiek, legioenen, forum | ~15 | todo |
| A5-04 | Grieks dagelijks leven — polis, agora, gymnasium, symposium | ~10 | todo |
| A5-05 | Taal en schrift — Latijns alfabet, Grieks alfabet, inscripties | ~5 | todo |
| A5-06 | Prerequisite-edges cultuur → taal/integratie | — | todo |

---

## Epic A6: Transfer-edges

**Doel:** Cross-linguïstische verbindingen (type `transfer`) tussen Latijn en Grieks.
**Geschat:** ~100 edges
**Afhankelijkheden:** A1, A2, A3, A4, A5 (alle knopen moeten bestaan)
**Status:** todo

| Story | Titel | Edges | Status |
|-------|-------|-------|--------|
| A6-01 | Naamvalsysteem — LAT ↔ GRC naamvallen | ~30 | todo |
| A6-02 | Werkwoordsmorfologie — praesens/imperfectum/aoristus parallellen | ~30 | todo |
| A6-03 | Cultuur — gedeelde mythologie en geschiedenis | ~20 | todo |
| A6-04 | Vocabulaire — cognaten en leenwoorden | ~20 | todo |
| A6-05 | Validatie transfer-edges — geen cycli, weights correct | — | todo |
