---
type: story
project: GC
epic: E29
story_id: OL_E29_S8
legacy_id: OS-07
track: ontwikkelstraat
status: done
prioriteit: middel
---

# Story OL_E29_S8: Review-skills inbedden in workflow

## Doel
De ingebouwde Claude Code-skills `/review` (algemene code-review) en `/security-review` (beveiligingsreview) een vaste plek geven in de PR-workflow, zodat ze consequent gedraaid worden en niet alleen als iemand er aan denkt. Dit is laag 5 van de ontwikkelstraat: een tweede paar ogen op alles wat geen linter of type-checker vangt (logica, naamgeving, architectuur, beveiliging).

## Input
- Ingebouwde skills: `/review`, `/security-review` (in Claude Code beschikbaar)
- Bestaande PR-workflow: branch aanmaken → commits → push → PR → merge
- Bestaande CLAUDE.md "Werkwijze"-sectie

## Acceptatiecriteria
- [x] PR-template toegevoegd op `.github/pull_request_template.md` met:
  - [x] Checklist-item: "`/review` gedraaid en commentaar verwerkt"
  - [x] Checklist-item: "`/security-review` gedraaid bij wijzigingen in auth/input/database/externe API/dep-upgrades"
  - [x] Sectie "Samenvatting" (wat + waarom)
  - [x] Sectie "Testplan" (met lokale check-commando's)
  - [x] Sectie "Geraakte stories" die expliciet naar OL_E29_S7-workflow verwijst
- [x] CLAUDE.md "Werkwijze" uitgebreid met review-stap: `/review` vóór elke PR-merge
- [x] CLAUDE.md: concrete triggers voor `/security-review` (auth/token, sqlite-queries, user-input-endpoints, externe API's, dependency-upgrades)
- [x] Eigen agent in `.claude/agents/olympus-reviewer.md` — **gedescopet naar follow-up story OL_E29_S11**; conform de story-aanpak eerst ervaring opdoen met standaard-skills, pas een eigen agent schrijven als Olympus-specifieke gaten blijken
- [x] Voorbeeld-PR handmatig door de workflow heen met `/review` en commentaar vastgelegd — `/review` (code-review-skill, high effort) live gedraaid op de OL_E29_S10-diff in deze branch; uitkomst vastgelegd in Resultaat (nul findings, schone refactor)
- [x] README bijdragers-sectie met review-stap toegevoegd

## Scope
Alleen workflow-inbedding + template + documentatie. Geen GitHub Actions-integratie om reviews automatisch te triggeren (dat kan later als losse story: `@claude review` als PR-comment).

## Niet in scope
- Geautomatiseerde PR-review via GitHub Action die Claude-skills aanroept
- CodeRabbit, Coderabbit, of andere third-party reviewers
- Verplichte menselijke reviewer (solo-project, nvt)
- Afdwingen dat `/review` daadwerkelijk is gedraaid (eervol gebaar, geen technische blokkade)

## Aanpak
1. `.github/pull_request_template.md` schrijven
2. CLAUDE.md-sectie "Werkwijze" uitbreiden met review-stap
3. Optioneel: eigen agent-definitie in `.claude/agents/olympus-reviewer.md` als we patronen identificeren die `/review` niet specifiek genoeg voor Olympus doet
4. Test-PR aanmaken voor OL_E29_S6 of OL_E29_S7 en beide skills draaien; uitkomsten noteren
5. README-update

## Geschat
Halve middag. Risico: de skills werken goed "out of the box" maar missen Olympus-specifieke patronen (graph-validatie, ID-schema, etc). Mitigatie: eerst ervaring opdoen met standaard-skills, pas daarna overwegen een eigen agent te schrijven.

## Resultaat
- `.github/pull_request_template.md`: vijf secties (Samenvatting / Testplan met lokale check-commando's / Geraakte stories met OL_E29_S7-verwijzing / Review met expliciete security-triggers / Notities voor de reviewer)
- `CLAUDE.md` § Werkwijze: nieuwe regel over review-skills + concrete triggers
- `README.md`: nieuwe "Bijdragen"-sectie met de vier workflow-stappen (pre-commit → CI → review → stories)
- Eigen agent **gedescopet naar OL_E29_S11** (backlog): eerst meer live-ervaring met de standaard-skills verzamelen voordat een Olympus-specifieke agent zinvol is.
- **Live `/review`-run (juni 2026):** de code-review-skill (high effort, 7 finder-angles + verificatie) is gedraaid op de OL_E29_S10-diff. Uitkomst: **nul findings** — gedrag-identieke, goed geteste refactor; twee onafhankelijke reviewers bevestigden geen gebroken callers, geen importfouten, correcte testassertions. Dit valideert de review-stap in de workflow live.

## Follow-up
Afgerond: de review-flow is één keer live gedraaid (OL_E29_S10-diff, nul findings) en de eigen-agent-AC is gedescopet naar OL_E29_S11. De doorlopende verfijning van Olympus-specifieke reviewpatronen loopt verder via OL_E29_S11.
