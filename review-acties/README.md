---
laatst-bijgewerkt: 2026-06-08
---
# Review-acties — werkmap

Elke review-actie voor de projecteigenaar leeft in deze map als **één
markdown-bestand**. Dat bestand is de enige plek waar de actie wordt beschreven,
gelezen en beantwoord. De PROJECTSTATUS-bestanden houden alleen een korte index
bij die naar deze formulieren verwijst.

> **Definitie.** Een review-actie is een beslismoment voor de projecteigenaar
> dat een lopende keuze blokkeert: lezen + akkoord, kiezen tussen opties, of een
> open vraag beantwoorden. Het is geen geparkeerde aanbeveling — die staat in
> `follow-ups/`.

---

## Folderstructuur

```
review-acties/
├── README.md          # dit bestand
├── open/              # actieve review-acties (wachten op antwoord)
└── afgehandeld/       # afgehandelde review-acties (archief)
```

## Bestandsnaam-conventie

```
<PREFIX>__<korte-slug>.md
```

- `<PREFIX>` volgt de project-/story-prefix-conventie van deze repo (zie
  `CLAUDE.md`).
- `<korte-slug>` is lowercase met hyphens, geen spaties.
- Dubbele underscore (`__`) scheidt het project van de slug zodat ze visueel uit
  elkaar staan in één lange bestandslijst.

## Levenscyclus

1. **Aanmaken** — kopieer de review-actie-template (`REVIEW_ACTIE.template.md`)
   naar `open/<PREFIX>__<slug>.md`. Vul Situatie, Complicatie, Gevraagde
   beslissing en Relevante documenten in.
2. **Indexeren** — voeg een rij toe aan de tabel `## Review-acties voor
   projecteigenaar` in het PROJECTSTATUS-bestand van het project. Eén regel:
   titel + link naar het formulier.
3. **Beantwoorden** — de projecteigenaar vult de sectie *Antwoord
   projecteigenaar* in het formulier zelf in.
4. **Afhandelen** — zet `status: afgehandeld` + `afgehandeld: 2026-06-08` in de
   frontmatter, voer de vervolgactie uit, en verplaats het bestand met `git mv`
   naar `afgehandeld/`. Verwijder daarna de rij uit de PROJECTSTATUS-index.

## Verschil met follow-ups

| | Review-actie | Follow-up |
|---|---|---|
| **Doel** | Beslissing die nu nodig is | Aanbeveling die later relevant wordt |
| **Wie reageert** | Projecteigenaar | Niemand, tot de trigger afgaat |
| **Wachttijd** | Kort (dagen tot weken) | Lang (maanden) |
| **Resultaat** | Antwoord → `afgehandeld/` | Trigger gaat af → story of vervallen |
| **Folder** | `review-acties/` | `follow-ups/` |

> Herkomst: gedeelde werkwijze uit `codebase-standards`
> (`docs/ways-of-working.md` §8). Wijzigingen aan het mechanisme lopen via die
> repo, niet hier.
