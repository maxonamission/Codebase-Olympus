# ADR-0001 — Opslag van het leerprofiel en mentor-deling via opt-in

- **Status:** Voorgesteld (2026-06-07) — ter besluitvorming door de projecteigenaar
- **Context-trigger:** privacy-by-design-vraag bij de concept-DPIA (`docs/security/dpia.md`)
  en EU AI Act-inschatting (`docs/security/eu-ai-act-risico.md`)
- **Relateert aan:** ontwerpkeuzes A7.1 (multi-tenant, geïsoleerd learner model) en A7.6
  (privacy by design) in `docs/ONTWERPKEUZES_GYMNASIUM_CLASSICA.md`
- **Implementatie:** story `OL_E14_S4`

> Eerste ADR in deze repo; introduceert tegelijk de ADR-conventie (`docs/decisions/`).

## Context

Het systeem verwerkt gegevens van **minderjarigen**. Relevante feiten uit de codebase:

- **Het leerprofiel is al pseudoniem.** `LearnerModel` (`models/learner.py`) bevat alleen
  `user_id` (UUID) + voortgang (`node_states`/mastery, sessie-historie, baseline,
  `learning_rate`). **Geen** naam/e-mail/geboortedatum — identiteit staat uitsluitend in de
  aparte `users`-tabel.
- **De knowledge graph heeft geen persoonsgegevens nodig** — die is statische didactische
  data (read-only); de enige per-leerling-laag is de voortgangs-overlay.
- **Schone laad/opslag-grens.** De engine doet `load_learner_model(user_id)` bij sessiestart
  en `save_learner_model(model)` op het eind; het hele model gaat als één JSON-blob in/uit
  (`api/database.py`). Tussentijds is het profiel alleen *tijdens* een sessie nodig.
- **Mentor-toegang is al afgeschermd maar nog niet opt-in.** `require_mentor_of` geeft 403
  zonder koppeling (`api/auth.py`), maar `create_mentor_assignment` wordt door **geen
  endpoint** aangeroepen en controleert alleen de mentor-rol — **niet of de leerling
  toestemde**. De koppel-/consent-flow is dus nog niet ontworpen.

Belangrijke nuance: pseudonieme voortgang blijft **persoonsgegeven** (herleidbaar via
`user_id`), en zegt bij minderjarigen iets over leervermogen. Scheiding van identiteit is
waardevol maar maakt voortgang niet "niet-persoonlijk".

## Beslissing (voorgesteld)

**Optie 2 — server-side pseudoniem + expliciete leerling-opt-in voor mentor-deling.**

1. Houd de voortgang server-side maar **pseudoniem** (identiteit gescheiden in `users`,
   zoals nu al). Overweeg versleuteling-at-rest van de `learner_models`-blob.
2. Maak mentor-deling **leerling-geïnitieerd en expliciet**: de leerling nodigt een mentor
   uit of keurt een mentorverzoek goed. Pas dán wordt een koppeling aangemaakt.
3. Leg een **consent-record** vast (tijdstip, scope, en bij <16 jaar ouderlijke toestemming),
   en maak het **intrekbaar** (intrekken = koppeling weg, toegang stopt direct).
4. `require_mentor_of` blijft de afdwinging; de opt-in-gate komt vóór
   `create_mentor_assignment`.

## Overwogen alternatieven

- **Optie 1 — status quo (verworpen):** mentor-koppeling zonder expliciete consent-gate.
  Onvoldoende privacy-by-design voor minderjarigen; bovendien is de flow tóch nog niet
  gebouwd, dus er is geen reden het zónder opt-in te bouwen.
- **Optie 3 — client-held / storage-on-the-edge (geparkeerd, niet nu):** de client houdt de
  pseudonieme voortgangs-blob, stuurt 'm bij sessiestart op, de server rekent in-memory en
  bewaart niets server-side; delen = de leerling pusht bewust een kopie. **Sterkste**
  minimalisatie (kleinst breach-oppervlak) en sluit naadloos aan op opt-in-deling.
  **Trade-offs** die het nu te zwaar maken: multi-device-continuïteit, backup/herstel bij
  apparaatverlies, spaced-repetition-herinneringen tussen sessies, en integriteit
  (client-manipulatie van mastery). Geschikt als latere evolutie of voor zeer gevoelige
  contexten.

## Gevolgen

- **Positief:** sluit aan op de bestaande `mentor_assignments`/`require_mentor_of`-laag
  (afgebakende uitbreiding, geen engine-herbouw); concrete invulling van A7.6; expliciet
  bewijs van toestemming voor de DPIA.
- **Kosten/werk:** consent-record + datamodel, leerling-gestuurde endpoints
  (uitnodigen/goedkeuren/intrekken), ouderlijke-toestemming-koppeling voor <16,
  UI-bevestiging. Zie `OL_E14_S4`.
- **Heroverweging → Optie 3** als: maximale dataminimalisatie vereist wordt, multi-device
  niet kritiek is, of een toezichthouder/DPO daarom vraagt.
