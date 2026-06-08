---
laatst-bijgewerkt: 2026-06-08
---
# Follow-ups — werkmap

Elke geparkeerde aanbeveling uit een review of audit leeft in deze map als **één
markdown-bestand**. Dat bestand is de enige plek waar de aanbeveling wordt
beschreven en bijgewerkt zolang ze wacht op de trigger. De PROJECTSTATUS-
bestanden houden alleen een korte index bij die naar deze formulieren verwijst.

> **Definitie.** Een follow-up is een bewust uitgestelde aanbeveling uit een
> review. Het is geen lopende beslissing — die staat in `review-acties/`. De
> aanbeveling komt pas weer in beeld als de **trigger** afgaat: een nieuwe
> toepassing, een geplande epic, beschikbaar komen van data, een review-uitkomst.

---

## Folderstructuur

```
follow-ups/
├── README.md          # dit bestand
├── open/              # actieve follow-ups (wachten op trigger)
└── afgehandeld/       # afgehandeld of vervallen (archief)
```

## Bestandsnaam-conventie

```
<PREFIX>__<korte-slug>.md
```

- `<PREFIX>` volgt de project-/story-prefix-conventie van deze repo (zie
  `CLAUDE.md`).
- `<korte-slug>` is lowercase met hyphens, geen spaties.
- Dubbele underscore (`__`) scheidt het project van de slug.

## Levenscyclus

1. **Aanmaken** — kopieer de follow-up-template (`FOLLOW_UP.template.md`) naar
   `open/<PREFIX>__<slug>.md`. Vul Situatie, Waarom geparkeerd, Trigger en
   Relevante documenten in.
2. **Indexeren** — voeg een korte rij toe aan de sectie `## Follow-ups uit
   reviews` in het PROJECTSTATUS-bestand: titel, trigger en link.
3. **Wachten** — niemand reageert tot de trigger afgaat. Tussentijdse
   observaties kunnen in *Status-aantekeningen* zonder de status te wijzigen.
4. **Afhandelen** — als de trigger afgaat: zet de aanbeveling om in een story (of
   verklaar haar vervallen). Zet `status: afgehandeld` + `afgehandeld:
   2026-06-08`, verplaats met `git mv` naar `afgehandeld/`, en verwijder de
   PROJECTSTATUS-rij.

## Verschil met review-acties

Review-acties zijn beslissingen die **nu** nodig zijn (projecteigenaar reageert
op korte termijn); follow-ups zijn aanbevelingen die **later** relevant worden
(wachten op een trigger). Zie de vergelijkingstabel in `review-acties/README.md`.

> Herkomst: gedeelde werkwijze uit `codebase-standards`
> (`docs/ways-of-working.md` §8). Wijzigingen aan het mechanisme lopen via die
> repo, niet hier.
