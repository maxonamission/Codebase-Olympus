# DPIA / data-flow — Gymnasium Classica

> **Concept** — gevendord uit codebase-standards `security/DPIA-template.md` (v0.5.0),
> ingevuld met de bekende feiten. Geen juridisch advies; dwingt de juiste vragen af.
> **Let op:** dit systeem verwerkt gegevens van **minderjarigen** (VWO-gymnasiumleerlingen).
> Dat is op zichzelf een verhoogd-risico-signaal → een **volledige DPIA + afstemming met
> DPO/jurist** is aanbevolen vóór een pilot met echte leerlingen. Velden met `<…>` moeten
> door de projecteigenaar/school worden ingevuld.

## 1. Verwerkingen

| Verwerking | Welke persoonsgegevens | Categorie | Doel | Grondslag (AVG art. 6) |
|---|---|---|---|---|
| Accountbeheer | account-id (UUID), rol (learner/mentor), plan/abonnementsstatus, `<naam/e-mail bij login — bevestigen>` | gewoon | toegang + facturatie | `<contract / toestemming (ouder) — invullen>` |
| Leer-/voortgangsmodel | item-responses (juist/fout, antwoordtekst, responstijd), mastery-schattingen (BKT), SM-2-planning, sessie-records | gewoon, **profilering van een minderjarige** | adaptief plannen + voortgang | `<toestemming ouder/school of gerechtvaardigd belang — invullen>` |
| Modus/onboarding | leerdoel (staatsexamen/bijspijker), methode + hoofdstuk | gewoon | personalisatie | `<invullen>` |

> Leerprestatie-data kan **leerproblemen** zichtbaar maken. Geen bijzondere categorie in de
> zin van art. 9, maar wel gevoelig bij minderjarigen — behandel met extra terughoudendheid.

## 2. Betrokkenen

- **Leerlingen — minderjarigen** (gymnasium, ca. 12–18 jaar). Toestemming/▸ouderlijke
  toestemming en de rol van de school (verwerkersverantwoordelijke vs. verwerker) moeten
  expliciet belegd worden. `<bevestigen>`
- Mentoren/docenten (mentor-rol, dashboard).

## 3. Data-flow

```
browser (leerling/mentor) → FastAPI-backend → SQLite (lokaal, fase 0-3)
   → learner model (BKT/IRT/SM-2, in-memory + persistente staat)
```

- **Externe (sub)verwerkers:** in fase 0–3 **geen** — geen LLM-integratie, geen externe
  API's (zie `CLAUDE.md` "Niet doen"). Bij latere hosting (PostgreSQL) of een LLM-mentor
  (fase 4+) ontstaat een (sub)verwerker → dan verwerkersovereenkomst + heroverweging.
- Data buiten de EU? Bij lokale/EU-hosting: nee. `<bevestigen bij hosting-keuze>`

## 4. Bewaartermijn & minimalisatie

- Bewaartermijn leer-/sessiedata: `<invullen — zo kort als didactisch nodig; recht op
  verwijdering bij uitschrijving>`.
- Dataminimalisatie: sla geen vrije antwoordteksten langer op dan nodig voor feedback;
  overweeg pseudonimisering van het leermodel t.o.v. de accountidentiteit.
- **Geen persoonsgegevens in de git-repo of CI-logs** (graph-/contentdata is didactisch,
  geen PII).

## 5. Beveiliging

- Authenticatie/autorisatie: rol-gebaseerd (learner/mentor). `<sterkte, sessiebeheer — invullen>`
- Opslag versleuteld in rust/transport: `<invullen — afhankelijk van hosting>`.
- Toegang beperkt tot: `<wie — school/beheerder>`.

## 6. Risico's & maatregelen

| Risico | Kans/impact | Maatregel |
|---|---|---|
| Profilering van minderjarigen | midden/hoog | dataminimalisatie, transparantie naar leerling+ouder, mentor-in-the-loop |
| Leerproblemen herleidbaar | midden | toegangsbeperking, korte bewaartermijn, geen externe deling |
| Latere LLM-mentor lekt leerdata naar externe API | hoog (toekomstig) | verwerkersovereenkomst + DPIA-herziening vóór ingebruikname |

## 7. EU AI Act

Adaptief leren raakt het onderwijsdomein (Annex III). Aparte inschatting:
zie [`eu-ai-act-risico.md`](eu-ai-act-risico.md).
