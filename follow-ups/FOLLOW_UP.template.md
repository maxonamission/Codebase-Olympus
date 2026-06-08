---
type: follow-up
project: "<PREFIX>"
status: open            # open | afgehandeld
aangemaakt: YYYY-MM-DD
afgehandeld: ""         # YYYY-MM-DD, leeg laten zolang status=open
bron: ""                # bv. "<PREFIX>_E13_S7 review §5"
trigger_categorie: ""   # bv. "nieuwe toepassing", "volgende ronde", "review-uitkomst"
---
# Follow-up — `<korte titel in een halve regel>`

> **Wat is dit?** Een aanbeveling uit een review of audit die bewust wordt
> geparkeerd. Pas wanneer de trigger hieronder afgaat, is dit formulier weer in
> beeld. Dit document is de enige plek waar het item leeft tot dat moment.

---

## Situatie

Twee tot vier zinnen over waar dit item over gaat en in welke review/audit het
voor het eerst is genoemd. B2-Nederlands; beperk jargon. Verwijs naar bronnen in
"Relevante documenten", niet hier.

## Waarom geparkeerd

Twee tot vier zinnen: waarom wordt dit nu niet opgepakt? Mist er data, kennis,
een casus, een validatie? Botst het met andere keuzes? Maak duidelijk dat het
bewust wachten is, niet vergeten.

## Trigger

Eén tot twee zinnen die beschrijven welke gebeurtenis dit item weer in beeld
brengt. Zo concreet mogelijk (een specifieke toepassing, een geplande epic,
beschikbaar komen van data, een review). Vage triggers ("ooit") geven het item
geen kans.

---

## Wat er moet gebeuren als de trigger afgaat

Korte beschrijving van de vervolgactie — genoeg richting zodat een opvolger de
strekking begrijpt, geen volledige uitwerking (die komt in een story).

- Onderdeel 1
- Onderdeel 2

---

## Relevante documenten

- [`pad/naar/bron-document.md`](https://github.com/maxonamission/Codebase-Olympus/blob/main/pad/naar/bron-document.md) — `<waarom relevant>`.

## Status-aantekeningen

Aantekeningen die kunnen worden toegevoegd zonder dat de status verandert
(tussentijdse observatie, datum waarop de trigger besproken maar niet afgegaan is).

- `YYYY-MM-DD` — `<aantekening>`

## Afhandeling

Invullen zodra de trigger afgaat of het item vervalt. Zet dan `status:
afgehandeld` + `afgehandeld: YYYY-MM-DD` in de frontmatter en verplaats het
bestand naar `follow-ups/afgehandeld/`.

- **Trigger afgegaan**: ja / nee
- **Vervolg**: `<verwijzing naar story, commit of besluit>`
- **Vervallen**: ja / nee, en waarom
