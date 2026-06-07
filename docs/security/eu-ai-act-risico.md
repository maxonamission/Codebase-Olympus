---
repo: Codebase-Olympus
artefact: eu-ai-act-risico
diataxis: explanation
status: concept
standaard-versie: 0.5.0
laatst-bijgewerkt: 2026-06-07
eigenaar: <CODEOWNERS-handle>
---

# EU AI Act — risico-inschatting (concept) — Gymnasium Classica

> **Concept** — gevendord uit codebase-standards `security/eu-ai-act-risico-template.md`
> (v0.5.0), ingevuld met de bekende feiten. Geen juridisch advies; input voor de
> projecteigenaar + een juridische toets. **Aandachtspunt:** het systeem combineert
> **minderjarigen** met het **onderwijsdomein** — twee factoren die de AI Act zwaar weegt.

## 1. Systeembeschrijving

Gymnasium Classica is een adaptief leersysteem voor Latijn en Grieks (VWO-gymnasium). Het
personaliseert oefenstof via een knowledge graph + **Bayesian Knowledge Tracing (BKT)**,
**Item Response Theory (IRT)** en **SM-2 spaced repetition**. In fase 0–3 is er **geen
LLM/generatieve AI**; de "AI" bestaat uit eigen statistische/algoritmische modellen. Een
LLM-mentor staat pas op de roadmap voor latere fasen.

De repo treedt op als **aanbieder (provider)** *en* **gebruiksverantwoordelijke (deployer)**
— het systeem wordt in eigen huis gebouwd én ingezet.

## 2. Rolbepaling (AI Act)

| Rol | Van toepassing? | Toelichting |
|---|---|---|
| Aanbieder (provider) van een AI-systeem | **ja** | eigen adaptief leersysteem onder eigen naam |
| Gebruiksverantwoordelijke (deployer) | **ja** | zet het systeem in voor leerlingen |
| GPAI-aanbieder | nee (nu) | geen general-purpose model; BKT/IRT zijn bespoke. Wijzigt als een LLM-mentor wordt toegevoegd (dan is de LLM-leverancier de GPAI-aanbieder) |

## 3. Risicoclassificatie

| Categorie | Inschatting | Onderbouwing |
|---|---|---|
| **Verboden praktijken** (Art. 5) | **toetsen — vermoedelijk n.v.t.** | Art. 5 verbiedt o.a. het uitbuiten van kwetsbaarheden van minderjarigen. Een ondersteunend leerinstrument is dat niet — **mits** geen manipulatieve/verslavende ("dark pattern") gamification op minderjarigen wordt ingezet. Bewust ontwerpen tegen die grens. |
| **Hoog-risico** (Annex III) | **toetsen — reëel mogelijk** | Annex III rekent o.a. AI voor *het evalueren van leerresultaten* en *het sturen van het leerproces/toegang tot onderwijs* tot hoog-risico. Het systeem schat mastery en stuurt de leerroute. Zolang dit een **oefen-/planningshulp** is en niet (mede)bepalend voor formele beoordeling, toelating of examenuitslag, is de hoog-risico-status discutabel. **Wordt de output besluitvormend** (cijfers, examen-go/no-go, plaatsing), dan gelden de hoog-risico-verplichtingen (risicomanagement, logging, menselijk toezicht, transparantie, conformiteitsbeoordeling). |
| **Transparantieverplichting** (Art. 50) | **deels nu, volledig bij LLM** | Nu geen generatieve output → Art. 50 (AI-content markeren) nog niet aan de orde. Wel: leerling + ouder helder informeren dát de personalisatie algoritmisch gebeurt. Zodra een **LLM-mentor** content genereert: expliciet melden dat output AI-gegenereerd is. |
| **Minimaal/laag risico** | restcategorie | Indicatief leunt het huidige systeem richting laag risico, **maar** de combinatie onderwijs + minderjarigen maakt het hoog-risico-vraagstuk (Annex III) een bewuste toets, geen automatische "laag". |

## 4. Voorlopige conclusie

Indicatief valt het huidige systeem (fase 0–3, geen LLM) waarschijnlijk **buiten hoog-risico**,
als *oefen- en planningshulp met de docent/mentor in de lus*. De classificatie **kantelt naar
hoog-risico** zodra de output (mede)bepalend wordt voor beoordeling, toelating of
examen-readiness, of zodra een LLM individuele begeleiding genereert. Gezien minderjarigen +
onderwijs is een **juridische toets vóór de pilot** sterk aanbevolen.

## 5. Verplichtingen / maatregelen (checklist)

- [ ] **Transparantie naar gebruiker** — leerling + ouder informeren over algoritmische
      personalisatie; bij latere LLM: zichtbaar melden dat output AI-gegenereerd is.
- [ ] **Menselijke controle** — mentor/docent in de lus; adaptieve route is advies, geen
      bindend oordeel.
- [ ] **Data-governance** — minimaliseer leer-/antwoorddata; zie [`dpia.md`](dpia.md).
- [ ] **Logging/traceerbaarheid** — herleidbaarheid van mastery-schatting → onderbouwing.
- [ ] **Robuustheid/veiligheid** — geen verslavende/manipulatieve mechanismen richting
      minderjarigen; bij LLM: prompt-injection-/misbruik-mitigatie.
- [ ] **Bewaar leverancier-documentatie** — n.v.t. tot een GPAI/LLM wordt toegevoegd.

## 6. GPAI-leveranciers

Nu geen general-purpose AI in gebruik. Bij toevoeging van een LLM-mentor wordt de
LLM-leverancier de GPAI-aanbieder; de repo blijft deployer. Bewaar dan de
model-/transparantiedocumentatie van de leverancier en sluit een verwerkersovereenkomst
(zie de codebase-standards `verwerkersovereenkomst-checklist`).

## 7. Opvolging

Projecteigenaar bevestigt de classificatie met een juridische toets (prioriteit, gezien
minderjarigen + onderwijs) en besluit over transparantie-UI, ouderlijke toestemming en
logging vóór de pilot. Heroverweeg bij: invoeren LLM-mentor, koppeling aan formele
beoordeling, of externe hosting. Wijzigingen loggen in `CHANGELOG`/ADR.
