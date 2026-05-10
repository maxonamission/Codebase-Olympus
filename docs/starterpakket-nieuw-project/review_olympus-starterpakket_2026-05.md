# Review — Olympus starterpakket-nieuw-project (versie 1.0, mei 2026)

**Bron:** [`maxonamission/Codebase-Olympus`](https://github.com/maxonamission/Codebase-Olympus/tree/main/docs/starterpakket-nieuw-project) — `docs/starterpakket-nieuw-project/`, versie 1.0, mei 2026.

**Reviewdatum:** 2026-05-10. **Reviewer:** Claude (op basis van Atlas' geleerde lessen tot mei 2026).

**Doel van deze review.** Het Olympus-team heeft een starterpakket gebundeld waarmee een nieuw graph-gedreven project opgezet kan worden zonder elke architectuurvraag opnieuw uit te vechten. Het pakket put expliciet uit Olympus (archetype A — adaptief leren) en verwijst naar Graaf Zeppelin (archetype B — causaal beleidsmodel). Atlas heeft op multi-model-coördinatie veel geleerd dat een latente verrijking voor dit pakket kan zijn. Deze review benoemt waar Atlas-ervaring concrete aanvullingen oplevert, en welke Atlas-conventies bewust **niet** in het pakket horen omdat ze single-project-scope overstijgen.

---

## Inhoudsopgave

1. [Algemene indruk](#1-algemene-indruk)
2. [Aanbevelingen, geordend op impact (H1–H8)](#2-aanbevelingen-geordend-op-impact)
3. [Kleinere correcties (S1–S8)](#3-kleinere-correcties)
4. [Bewust niet overnemen uit Atlas](#4-bewust-niet-overnemen-uit-atlas)
5. [Atlas-bron-mapping per aanbeveling](#5-atlas-bron-mapping-per-aanbeveling)

---

## 1. Algemene indruk

Sterk pakket. Wat goed werkt:

- **Archetype A vs B als opening van de README.** Dat onderscheid is precies de vraag die Atlas zelf pas laat heeft expliciet gemaakt (de route A/B/C/D-typering in `docs/routes.md` werd pas in een latere epic toegevoegd). Vooraan in de README zetten is een echte verbetering ten opzichte van Atlas' eigen ontstaansvolgorde.
- **Hoofdstukstructuur 01 → 06** loopt mooi van werkwijze naar checklist. De *vragen voor je nieuwe project* aan het eind van elk hoofdstuk dwingt een lezer om antwoorden op papier te zetten in plaats van door te scrollen.
- **Hoofdstuk 06 antipatronen-en-checklist** is goud: 25 concrete antipatronen mét voorbeelden uit Olympus en Zeppelin. Atlas heeft zoiets zelf niet als gebundeld document.
- **Bootstrap §3 (week-voor-week)** is ambitieus maar realistisch geschat (10 maanden tot pilot-MVP voor Olympus is consistent met Atlas' eigen tempo).
- **Hoofdstuk 03 "wanneer NIET adaptief"** is uitstekend opgesteld als skip-signaal. Dat kan een hoop tijdverlies besparen voor projecten waar BKT/SM-2/IRT overkill is.

**Eerlijke kanttekening.** Atlas is een multi-model repo, het Olympus-pakket adresseert single-project. Veel onderstaande aanbevelingen komen uit hick-ups bij meervoudige modellen of lang-lopende coördinatie en zijn dus pas relevant op een later moment van het project. Per aanbeveling is dat aangegeven.

---

## 2. Aanbevelingen, geordend op impact

### H1 — Story-workflow: voeg `todo/` toe als optionele grooming-tussenstap

**Locatie in pakket:** hoofdstuk 04 §C, en de mappenstructuur in §C.

**Atlas-bevinding (CA_E3, april 2026).** Het drie-statusmodel (`backlog/doing/done`) bleek te grofkorrelig zodra de backlog opliep. Voor stories die op korte termijn aan de beurt kwamen ontbrak een groomings-trap; alles in `backlog/` was gelijk-gewicht. Toevoeging van `todo/` als wachtkamer-voor-eerstvolgende-sessie loste dat op zonder de WIP-discipline te ondergraven.

**Aanbeveling.** Vier statussen, met `todo/` als **vrijwillige** tussenstap:

| Status | Betekenis | WIP-richtlijn |
|---|---|---|
| `backlog` | Gedefinieerd, geen specifieke planning | Geen limiet |
| `todo` | Ingepland voor eerstvolgende sessie | Soft-cap 5–10 |
| `doing` | Actief in uitvoering | Max 3 |
| `done` | Afgerond en gereviewd | — |

Expliciet vermelden dat `backlog → doing` direct mag — `todo` is opt-in. Dat houdt het simpel voor solo-projecten en geeft ruimte zodra de backlog groter wordt.

**Wanneer relevant.** Vanaf het moment dat de backlog meer dan ~15 stories bevat. Daaronder is drie statussen prima.

---

### H2 — Cross-branch epic-collision-protocol

**Locatie in pakket:** hoofdstuk 04 §C, na "Workflow".

**Atlas-bevinding (PR#43, mei 2026).** Zodra twee feature-branches gelijktijdig leven, claimen ze allebei het volgende `E#`. Resolution-patroon (`C1_E20` → `C1_E21`) bleek niet-triviaal omdat zowel folder-naam, story-IDs als kruisverwijzingen mee moeten.

**Aanbeveling.** Korte sectie toevoegen:

```markdown
### Nieuwe epic openen (als je met meerdere branches werkt)

1. `git fetch origin main` vóór epic-creatie.
2. Pak het hoogste E# op origin/main + 1 — niet op je eigen branch.
3. Bij collision: tweede merger hernoemt. Documenteer het patroon
   nu, niet als het probleem ontstaat.
```

Geen volledig collision-script; één paragraaf volstaat. Voor solo-één-branch-projecten irrelevant maar niet schadelijk.

**Wanneer relevant.** Vanaf de eerste keer dat je een feature-branch naast een andere actieve branch hebt staan.

---

### H3 — Review-acties + follow-ups als gestold spoor

**Locatie in pakket:** nieuw blokje in hoofdstuk 04, of in hoofdstuk 05 §6 ("stop-momenten").

**Atlas-bevinding.** Acceptatiecriteria in stories vangen niet alle uitkomsten van werk. Reviews leveren twee verschillende soorten residu op:

1. **Review-acties voor de projecteigenaar** — concrete actie die de mens moet doen (lezen-en-akkoord, expert-consult, scope-beslissing). Verdwijnt na afhandeling.
2. **Follow-ups uit reviews** — geparkeerde overwegingen die op de roadmap blijven staan tot een trigger ze activeert (bv. "model raakt actief gebruikt door externe instantie").

Beide worden in Atlas in `PROJECTSTATUS_<X>.md` als aparte tabellen bijgehouden. Zonder die scheiding kruipen geparkeerde dingen óf de backlog in (als drukgevoelig werk dat niet klaar is) óf verdwijnen ze.

**Aanbeveling.** Toevoegen aan het PROJECTSTATUS-template (impliciet aanwezig als `EPICS.md`-overzicht) of als losse sectie:

```markdown
## Review-acties voor de projecteigenaar

| Actie | Document | Toelichting |
|---|---|---|

## Follow-ups uit reviews

| Item | Bron | Plek (signaalstory of doc-sectie) | Trigger |
|---|---|---|---|
```

Tweede tabel pas aanmaken zodra er minstens één levende follow-up is — leeg toevoegen is overbodig.

**Wanneer relevant.** Vanaf de eerste externe review-sessie of het eerste expert-consult.

---

### H4 — Evidence-traceability: `ref_id` en literatuurregister

**Locatie in pakket:** hoofdstuk 02 (graph-blueprint) §B en §F, hoofdstuk 06 §E (archetype B-checklist).

**Atlas-bevinding.** Voor archetype-B-modellen (causaal/beleid) rotten claims zonder bron snel. Atlas hanteert sinds vroege epics: elke A/B/C-evidence-claim heeft een `ref_id` dat naar een gedeeld literatuurregister verwijst, en `audit_literatuur_schemas.py` valideert dat. Het is een van de "Niet-doen"-regels in Atlas' CLAUDE.md.

Het Olympus-pakket noemt "literatuur-onderbouwing voor de defaults" bij sliders (06 §E-23) maar definieert geen registratie-mechanisme.

**Aanbeveling.**

In hoofdstuk 02 §F validatie-catalogus toevoegen als **conditioneel** invariant ("alleen als je archetype B en/of evidence-claims hebt"):

> **9. Reference-integrity** — als een knoop, edge, of slider een `ref_id`-veld heeft, bestaat die ID in `data/literatuur.json` (of equivalent register).

In hoofdstuk 06 §E checklist (archetype B) toevoegen:

- [ ] Sliders en evidence-claims hebben `ref_id` naar gedeeld literatuurregister.
- [ ] Literatuur-audit-script in CI.

**Wanneer relevant.** Direct vanaf de eerste evidence-claim. Voor archetype A weegt het minder, maar item-bronnen (authentieke teksten, vraag-bronnen) kennen vergelijkbare rot-risico's.

---

### H5 — Soft-fail / strict modes voor validators

**Locatie in pakket:** hoofdstuk 04 §B (`.pre-commit-config.yaml`) en §C (`scripts/check_story_status.py`).

**Atlas-bevinding.** Een hard-fail validator op pre-commit voor *cross-document consistency* (epic-tellingen, story-status, wikilinks) blokkeert lokaal werk dat eigenlijk op een lopende epic legitiem inconsistent is. Twee modes lossen dat op: `--mode=staged` (soft-fail, drift-rapport) lokaal/pre-commit, `--mode=full` (hard) in CI.

Olympus' `check_story_status.py` lijkt single-mode.

**Aanbeveling.** Toevoegen aan de beschrijving van `scripts/check_story_status.py`:

> Twee modes:
>
> - `--mode=staged` (default lokaal): rapporteert drift, exit 0 — niet-blokkerend.
> - `--mode=full` (CI): hard, exit 1 bij elk probleem.
>
> Lokaal mag drift bestaan tijdens werk-in-uitvoering; CI is de gate.

**Wanneer relevant.** Direct, zodra je een cross-document-consistency-validator inzet.

---

### H6 — "Niet-doen"-lijst in CLAUDE.md-template

**Locatie in pakket:** hoofdstuk 04 §F (CLAUDE.md handover-template).

**Atlas-bevinding.** Een aparte "Niet-doen"-sectie in CLAUDE.md (5 regels in Atlas) is veel effectiever dan dezelfde regels verstopt in een antipatronen-catalogus. De AI leest CLAUDE.md elke sessie; de antipatronen-catalogus alleen als iemand er expliciet naar verwijst.

**Aanbeveling.** Voeg expliciet een "Niet doen"-sectie toe aan het handover-template, met instructie om de drie tot zes domein-specifieke valkuilen daar te plakken (gedestilleerd uit hoofdstuk 06 antipatronen). Voorbeeld voor archetype B:

```markdown
## Niet doen

1. Geen globale DAG-cyclus-check op een netwerk met feedback-edges.
2. Geen edge-velden invoeren die niet door code gebruikt worden.
3. Geen sliders zonder eenheid + literatuur-onderbouwing.
4. Geen statische pad-analyse als antwoord op dynamische vragen.
```

Korter en harder dan het antipatronen-hoofdstuk; AI ziet het direct in elke sessie.

**Wanneer relevant.** Direct in het CLAUDE.md-template.

---

### H7 — Archief-conventie

**Locatie in pakket:** hoofdstuk 04 §A (zes lagen) of als nieuwe paragraaf in hoofdstuk 01.

**Atlas-bevinding.** Historische staat onder `archief/` is bewust read-only. Wijzigingen daar breken de archief-functie (terugkijken naar wat er was). Atlas heeft hier een expliciete "niet-doen"-regel én een `archief/INDEX.md` die context geeft.

Het Olympus-pakket heeft geen archief-concept. Voor een lang-lopend project (>6 maanden) wordt dat zinvol — anders raken oude versies van briefing/ontwerpkeuzes/closure-rapporten ofwel verloren of vervuilen ze het actieve werk.

**Aanbeveling.** Eén alinea in hoofdstuk 04 §A toevoegen:

> Vanaf maand 6: een `archief/`-map met een `INDEX.md`. Versies van BRIEFING/ONTWERPKEUZES, afgeronde closure-rapporten, gearchiveerde verkenningen — daar landen ze zodra ze niet meer actief zijn. **Niet wijzigen na archivering** — anders breekt de terugkijk-functie.

**Wanneer relevant.** Vanaf maand 6 of zodra de tweede major versie van BRIEFING/ONTWERPKEUZES geschreven wordt.

---

### H8 — Quick-lookup-tabel onderaan CLAUDE.md

**Locatie in pakket:** hoofdstuk 04 §F (handover-template).

**Atlas-bevinding.** §10 in Atlas' CLAUDE.md ("Waar vind ik wat?") is in de praktijk de meest geraadpleegde sectie. Sneller dan zoeken, scheelt veel mis-zoekend van de AI.

**Aanbeveling.** Voeg aan het CLAUDE.md-template een laatste sectie toe:

```markdown
## Waar vind ik wat?

| Vraag | Locatie |
|---|---|
| Projectvisie en scope | `docs/BRIEFING_*.md` |
| Vastgestelde ontwerpkeuzes | `docs/ONTWERPKEUZES_*.md` |
| Edge- en node-types | `src/<pkg>/schemas/` |
| ID-schema | `docs/id-schema.md` |
| Validatie-catalogus | `src/<pkg>/graph/validation.py` |
| Stories-overzicht | `stories/EPICS.md` |
| ... | ... |
```

Klein, krachtig, scheelt zoek-rondes voor mens én AI.

**Wanneer relevant.** Direct in het CLAUDE.md-template; tabel groeit organisch mee.

---

## 3. Kleinere correcties

| Nr. | Pakket-locatie | Voorstel |
|---|---|---|
| **S1** | Hoofdstuk 01 principe 7 punt 4 | Atlas-ervaring: bestand-splitsing aan de bron oplossen (max ~200 knopen per JSON, max ~800 regels per markdown) is sneller dan reactief in tool-input splitsen. Voeg een vooraf-regel toe naast de reactieve. |
| **S2** | Hoofdstuk 02 §J Sprint 1 stap 6 | `scripts/validate_graph.py` zou ook `--mode=staged\|full` moeten meenemen (zie H5). |
| **S3** | Hoofdstuk 04 §B `pyproject.toml` | `target-version = "py311"` ligt vast terwijl `requires-python` `>=3.11,<3.13` toelaat. Maak deze consistent (kies één Python-versie als baseline, of laat ruff `target-version` op de laagste staan). |
| **S4** | Hoofdstuk 04 §F CLAUDE.md-template | Voeg "Onomkeerbare acties bevestigen" als zelfstandige kop toe. Principe 9 uit hoofdstuk 01 staat nu wel ergens vermeld maar niet als zelfstandige sectie. AI's lezen CLAUDE.md selectief op kop-niveau. |
| **S5** | Hoofdstuk 05 §3 dag 14 | "Buffer / refactor / bugjes." → expliciet stop-criterium toevoegen ("als de loader nog niet stabiel is, ga niet door naar week 3"). Zonder criterium glijdt buffer-tijd onbedoeld in scope-uitbreiding. |
| **S6** | Hoofdstuk 06 §A.6 ID-schema-migratie | Voeg een verwijzing toe naar het patroon van een idempotent migratie-validator-script (Atlas: `_scripts/check_*.py`-stijl). Olympus zegt nu "schrijf een idempotent migratiescript" zonder dat te onderbouwen. |
| **S7** | Hoofdstuk 06 §F finale checklist | Voeg een top-level "Heb je een externe-blik-sessie ingepland (review door iemand die niet meegebouwd heeft)?" toe — antipatroon §H punt 2 noemt het maar het zit nu niet in de checklist. |
| **S8** | README "Pad C — overdracht" | Voeg toe dat de overnemer ook een eigen pass over `06-antipatronen` doet. Antipatronen herkennen is de meest waardevolle vaardigheid voor een overnemer. |

---

## 4. Bewust niet overnemen uit Atlas

Sommige Atlas-conventies zijn waardevol voor Atlas zelf maar overengineered voor een starterpakket. Niet toevoegen:

- **Multi-model prefix-systeem** (`MI`, `ME`, `MA`, `D1`, `C1`, `KNSBMESO`, ...). Atlas heeft dat omdat het een meta-architectuur over zes coexisterende modellen voert. Een nieuw single-project-team zou er onnodig in vastlopen. Olympus' simpele `A1`/`B1`-conventie is correct voor een starter.
- **Meta-architectuur-check verplicht per epic.** In Atlas zinvol omdat er een gedeeld vocabulaire over modellen bewaakt moet worden. In een single-project komt het neer op "check je eigen ONTWERPKEUZES" — dat is impliciet al in elke epic-rationale.
- **Werkconcept-vs-norm-onderscheid (`A_/`-rol).** Atlas-specifiek; in een starter overbodig.
- **Cross-project dashboard (`PROJECTSTATUS_Modelbouw.md`).** Pas relevant bij ≥2 actieve modellen.
- **Slider-naam-stabiliteit cross-model.** Idem.
- **Wikilink-validator.** Atlas gebruikt veel `[[wikilinks]]` tussen modellen; voor een single-project doc-set is een gewone broken-link-checker (bijv. `markdown-link-check`) genoeg.
- **Disambiguator-suffixen op story-prefixen** (`KNSBMESO`/`KNSBMACRO`). Pure multi-tree-symptoom.

Deze allemaal noemen in het pakket zou de leescurve kelderen zonder concrete winst voor een nieuw enkel-project.

---

## 5. Atlas-bron-mapping per aanbeveling

Voor verifieerbaarheid: per aanbeveling de Atlas-bron(nen) waar de bevinding op steunt.

| Aanbeveling | Atlas-bron |
|---|---|
| H1 (`todo`-status) | CLAUDE.md §4 (vier statussen sinds CA_E3, april 2026) |
| H2 (epic-collision) | CLAUDE.md §4 ("Nieuwe epic openen"), `_scripts/check_epic_collisions.py`, PR#43 (mei 2026) |
| H3 (review-acties / follow-ups) | CLAUDE.md §4 stappen 7-8, format in elk `PROJECTSTATUS_<X>.md` |
| H4 (`ref_id` + literatuurregister) | CLAUDE.md §7 punt 4 ("Geen evidence-claims zonder `ref_id`"), `_scripts/audit_literatuur_schemas.py`, `archief/E18_review_eindstand_literatuurregisters.md` |
| H5 (soft/strict modes) | CLAUDE.md §4 ("Lokaal kun je `--mode=staged` draaien"), `docs/ontwikkelstraat.md` |
| H6 ("Niet-doen"-sectie in CLAUDE.md) | CLAUDE.md §7 (vijf scherp geformuleerde regels) |
| H7 (archief-conventie) | CLAUDE.md §7 punt 3, `archief/INDEX.md` |
| H8 (quick-lookup-tabel) | CLAUDE.md §10 |
| S2 / H5 mode-flags | `_scripts/validate_epics_consistency.py`, `_scripts/check_story_status.py` |
| S6 (idempotent migratie-validator) | Atlas-patroon `_scripts/check_*.py` |
| S7 (externe-blik-sessie) | CLAUDE.md §8 ("werkhouding"), Atlas review-cyclus |

---

## Slot

Dit is een snapshot-review van Olympus-starterpakket v1.0 (mei 2026) tegen Atlas-staat mei 2026. De acht hoofdaanbevelingen (H1–H8) zijn elk gefundeerd op concrete Atlas-bevindingen (zie §5). De acht kleinere correcties (S1–S8) zijn lokale verbeteringen die geen architectuur-impact hebben. Sectie 4 ("bewust niet overnemen") is even belangrijk: het filteren van Atlas-idiosyncrasieën voorkomt dat het pakket dichtslibt met multi-model-coördinatie die in een eerste project alleen ruis is.

Latere versies van het Olympus-pakket of vervolg-reviews kunnen dit document als baseline nemen.
