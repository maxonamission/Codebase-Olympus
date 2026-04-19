# De ontwikkelstraat: kwaliteit zonder dat je er elke keer op hoeft te letten

## Waarvoor is dit document?

Als je software ontwikkelt met hulp van Claude Code, gaat het bouwen snel. Je bent in een middag verder dan je vroeger in een week kwam. Maar met die snelheid komt een nieuw probleem: **hoe houd je de kwaliteit op peil?** Je merkt het misschien zelf al. In het ene project staan nette tests, in het andere niet. Het ene project heeft duidelijke naamgeving, het volgende is een rommeltje. De regels die je vorige maand nog streng volgde, ben je deze week vergeten.

Dat is geen gebrek aan discipline. Dat is hoe mensen werken. Je hoofd zit vol met het probleem dat je aan het oplossen bent, niet met je eigen kwaliteitsregels.

De oplossing is een **ontwikkelstraat**: een reeks automatische controles die jouw regels afdwingen, ook als jij er even niet op let. In dit document leg ik uit wat dat is, waar het uit bestaat, en hoe je er zelf één bouwt.

Doelgroep: iemand die net begint met programmeren en al wél een paar projecten heeft lopen, maar nog nooit een echte "kwaliteitsstraat" heeft opgezet.

## Wat is een ontwikkelstraat?

Denk aan een fabriek waar auto's worden gemaakt. Aan het begin van de lijn ligt een stuk metaal. Aan het eind rolt een werkende auto van de band. Daartussen zitten tientallen controlepunten: past dit onderdeel wel? Zit die schroef goed vast? Lekt er geen olie? Elke controle vangt een ander soort fout op. En het belangrijke is: **die controles gebeuren automatisch, niet omdat iemand eraan denkt**.

Een ontwikkelstraat voor software werkt hetzelfde. Aan het begin staat jouw idee. Aan het eind staat werkende, geteste code die in productie kan. Daartussen zet je controlepunten neer. Elk punt vangt een bepaalde soort fout op. En ze werken automatisch: je kunt ze niet per ongeluk overslaan.

De Engelse term die je vaak tegenkomt is **pipeline** ("leiding" of "lopende band"). In dit document noem ik het een ontwikkelstraat, omdat dat beter uitdrukt waar het om gaat: een reeks stations die je achter elkaar doorloopt.

## Waarom is dit nodig?

Stel je werkt zonder ontwikkelstraat. Je schrijft code, je test het even met de hand, je pusht het naar GitHub. Wat kan er misgaan?

- **Je vergeet een test te schrijven.** Pas over drie weken merk je dat een functie niet meer werkt, omdat een andere wijziging hem stukmaakte.
- **Je gebruikt in project A andere naamgeving dan in project B.** Als je tussen projecten wisselt, moet je elke keer opnieuw nadenken over conventies.
- **Je vergeet een stap** die je eigenlijk altijd wilt doen: code formatteren, types checken, gevoelige sleutels eruit halen.
- **Onder tijdsdruk glippen er dingen door** die je normaal niet zou accepteren. "Ik fix het later wel." Later komt nooit.

Een ontwikkelstraat lost deze problemen op door de controle **uit jouw hoofd te halen en in het systeem te stoppen**. Je kunt een commit niet afronden als de tests niet draaien. Je kunt geen merge doen als de code niet geformatteerd is. Je kunt niet naar productie zonder dat de beveiligingscheck groen is.

Dat voelt in het begin beperkend. Na een week merk je dat het juist bevrijdend is: je hoeft er niet meer aan te denken.

## Waar bestaat het uit? De zes lagen

Een goede ontwikkelstraat heeft **meerdere lagen die elk iets anders afvangen**. Als één laag iets mist, vangt de volgende het op. Dit principe heet "defense in depth", verdediging in lagen.

De zes lagen die ik aanraad, van dicht bij jou (snel en lokaal) tot ver weg (traag maar streng):

1. **Projecttemplate** — het startpunt. Elke nieuwe app begint met dezelfde nette structuur, zodat je niet elke keer vanaf nul moet nadenken.
2. **Pre-commit hooks** — kleine controles die draaien voordat je een wijziging opslaat. Snel, lokaal, onmisbaar.
3. **Claude Code hooks** — controles die draaien terwijl Claude jouw code aan het schrijven is. Claude ziet de fouten meteen en lost ze op in dezelfde sessie.
4. **CI (Continuous Integration)** — controles op een server, nadat je je code hebt gepusht. Trager, maar streng: hier komt niemand zomaar langs.
5. **Geautomatiseerde review** — een tweede paar ogen dat jouw code nakijkt op patronen, beveiliging en stijl. Vaak ook door Claude zelf, in de vorm van "agents" of "skills".
6. **Gedeelde standaarden** — één centrale bron waarin staat wat jouw regels eigenlijk zijn. Zonder dit drijven je projecten langzaam uit elkaar.

In de volgende secties loop ik elke laag langs. Ik leg uit wat het doet, wat je ervoor nodig hebt, en wat je erin stopt.

## Laag 1: Het projecttemplate

Een template is een **voorbeeldproject** dat je elke keer kopieert als je iets nieuws begint. Niet handmatig ("oh, kopieer die map van vorige keer") maar met een gereedschap zoals `copier` of `cookiecutter`. Je typt één commando en er komt een compleet skelet uit, klaar om in te vullen.

Wat zet je erin?

- De **mapstructuur** die je altijd gebruikt: `src/`, `tests/`, `docs/`, `scripts/`.
- De **configuratiebestanden** voor de gereedschappen die je toch altijd aanzet (formatters, type-checkers, test-runners).
- Een **leeg CLAUDE.md** met je basisregels, zodat Claude in elk project dezelfde conventies gebruikt.
- Een **voorbeeldtest**, zodat de testsuite al draait voordat je ook maar één regel echte code hebt geschreven.
- Een **README-skelet** met de secties die je normaal gesproken invult.

Wat bereik je hiermee? Je **begin-kwaliteit is altijd hoog**. Een nieuw project heeft op dag één al tests, formatters en een duidelijke structuur. Je hebt geen excuus meer om "dat later nog toe te voegen".

Belangrijk: een template mag best klein zijn. Liever een template van tien bestanden die je écht gebruikt, dan een template van honderd bestanden waarvan je er negentig negeert.

## Laag 2: Pre-commit hooks

Een **commit** is een opgeslagen wijziging in je versiebeheer (git). Elke keer dat je iets afrondt, commit je het. Een **hook** is een stukje code dat automatisch afgaat op een bepaald moment. Een **pre-commit hook** draait dus vlak voordat je commit klaar is.

Dit is je eerste vangnet. Een pre-commit hook kan bijvoorbeeld:

- Je code formatteren (zorgen dat spaties en regels netjes zijn).
- Controleren of de types kloppen (in Python: `mypy`, in TypeScript: `tsc`).
- Zoeken naar veelgemaakte fouten met een **linter** (een gereedschap dat naar code-patronen zoekt, zoals `ruff` of `eslint`).
- Blokkeren dat er wachtwoorden of API-sleutels in je code staan.

Als een hook faalt, gaat de commit **niet door**. Je moet het probleem eerst oplossen. Dat klinkt vervelend, maar in de praktijk duurt zo'n check één of twee seconden, en hij vangt fouten op die je anders pas veel later had gemerkt.

Het Python-pakket `pre-commit` (naam van het gereedschap én van het concept) regelt dit voor je. Je zet één bestand (`.pre-commit-config.yaml`) in je repo, en iedereen die meewerkt krijgt dezelfde checks.

## Laag 3: Claude Code hooks

Claude Code, de AI-assistent waar je mee werkt, kan ook hooks draaien. Dit is een **ander soort hook** dan hierboven. Claude-hooks zitten in een bestand dat `.claude/settings.json` heet, en ze gaan af op momenten binnen je chatgesprek met Claude.

De twee die het meest nuttig zijn:

- **PostToolUse** — draait nadat Claude een bestand heeft bewerkt. Je laat hem bijvoorbeeld de linter draaien op dat bestand. Als er een fout staat, ziet Claude dat meteen en repareert hij hem in dezelfde sessie. Zonder deze hook schrijft Claude iets, beweert dat het klaar is, en merk jij pas later dat de code niet compileert.
- **Stop** — draait voordat Claude een sessie afrondt. Hier laat je typisch de hele testsuite draaien. Zo weet je zeker dat Claude niet "klaar" is terwijl je tests stuk zijn.

Waarom is dit waardevol? Omdat de reparatie **binnen de context** gebeurt. Claude weet nog precies wat hij aan het doen was. Als je de fout pas een dag later ziet, moet je opnieuw uitleggen wat er moest gebeuren.

De skill `update-config` in Claude Code helpt je deze hooks goed te configureren.

## Laag 4: CI — Continuous Integration

CI betekent letterlijk "doorlopend integreren". In de praktijk: **elke keer dat iemand code pusht naar GitHub, draait er op een server automatisch een reeks checks**. Dezelfde linters, dezelfde tests, plus dingen die lokaal te traag zijn (tests op meerdere besturingssystemen, tests die een database nodig hebben, beveiligingsscans).

Waarom doe je dit, als je al pre-commit hooks hebt? Drie redenen:

1. **Pre-commit kun je overslaan** met een vlaggetje (`--no-verify`). CI kun je niet overslaan.
2. **Niet iedereen heeft pre-commit goed geïnstalleerd.** CI draait altijd.
3. **Sommige checks zijn te traag voor lokaal.** In CI mogen ze twee minuten duren; lokaal niet.

CI is je **harde poort**. Geen code mag naar de hoofdbranch zonder groene CI. GitHub Actions is hiervoor de meest gebruikte dienst: je zet een bestand in `.github/workflows/` en het draait automatisch.

## Laag 5: Geautomatiseerde review

Tot hier hebben we vooral gekeken naar **mechanische** checks: formatteren, types, tests. Maar kwaliteit is meer dan dat. Is de code logisch opgebouwd? Zijn de namen duidelijk? Zit er geen beveiligingslek in?

Daar kun je een **tweede paar ogen** voor gebruiken, in de vorm van Claude zelf. In Claude Code bestaan er **skills** zoals `/review` (algemene code-review) en `/security-review` (specifiek op beveiliging). Je draait ze op elke pull request. Ze lezen je wijzigingen en geven commentaar.

Je kunt ook **eigen agents** maken voor patronen die specifiek zijn voor jouw werk. Bijvoorbeeld: "controleer of elk API-eindpunt een Pydantic-model gebruikt", of "controleer of elke databasequery een index kan gebruiken".

Wat bereik je hiermee? Claude vangt dingen die linters niet kunnen vinden. En het gebeurt consequent, niet alleen op de dagen dat je zelf goed uitgeslapen bent.

## Laag 6: Gedeelde standaarden

Dit is de minst zichtbare laag, maar de belangrijkste voor de lange termijn. Als je werkt zonder gedeelde standaarden, gebeurt er het volgende: **elk project drijft langzaam zijn eigen kant op**. Na een jaar heb je vijf projecten die elk net iets anders zijn ingericht. Als je van het ene naar het andere springt, kost dat energie.

De oplossing is **één centrale plek waar je regels staan**. Bijvoorbeeld:

- Een persoonlijk `~/.claude/CLAUDE.md` met regels die voor álle projecten gelden (type hints altijd, nooit `print` in productiecode, commit-berichten in het Nederlands).
- Een aparte repo `ci-templates` met herbruikbare GitHub Actions-workflows.
- Een `standards`-map die je via een git-submodule of `copier update` in elk project binnenhaalt.

Zodra je iets verandert aan die centrale regels, kun je ze **één keer updaten** en naar alle projecten doorsijpelen. Zonder deze laag verdampt het effect van je ontwikkelstraat na een paar maanden.

## Hoe begin je?

De verleiding is groot om alle zes de lagen tegelijk op te zetten. Dat is een valkuil. Je bouwt dan een systeem bovenop iets wat nog niet stabiel is, en je raakt de weg kwijt zodra iets niet werkt.

Veel beter: **begin bij één bestaand project en werk van binnen naar buiten**.

1. **Kies je beste lopende project.** Dat wordt je "voorbeeldproject".
2. **Zet formatter, linter en tests op orde.** Zorg dat de testsuite draait en groen is.
3. **Voeg pre-commit hooks toe.** Dit is vaak een middag werk. Meet het resultaat: hoeveel fouten vangt het op in de eerste week?
4. **Voeg CI toe.** Eén GitHub Actions-workflow die dezelfde checks draait als pre-commit, plus de tests.
5. **Pas nu** ga je extraheren naar een template. Pak wat in het voorbeeldproject werkt en zet het in een aparte template-repo.
6. **Daarna** komt de Claude Code-hooklaag. Start klein: alleen `PostToolUse` op je hoofdtaal (Python of TypeScript).
7. **Tot slot** de gedeelde standaarden en de review-skills.

Tussen elke stap: **gebruik het echt een week of twee**. Als een controle te traag of te vervelend is, pas hem aan. Pas als een laag werkelijk zonder frictie draait, voeg je de volgende toe.

## Valkuilen om te vermijden

- **Te veel abstractie te vroeg.** Drie projecten met duplicatie is geen probleem. Pas als je de vijfde bent begonnen en merkt dat je dingen overtypt, is het tijd om te extraheren.
- **Trage hooks.** Als een pre-commit hook vijftien seconden duurt, ga je hem omzeilen. Houd hem onder de drie seconden. Zware checks horen in CI.
- **Templates die "alles" proberen.** Een template van tien goed-werkende bestanden is beter dan een template van honderd bestanden waarvan je er negentig verwijdert. Voeg pas iets toe als je het in twee projecten écht gebruikt.
- **Drift accepteren.** Als je merkt dat projecten uit elkaar groeien, pak dat meteen aan. Zet bijvoorbeeld een maandelijkse "template-sync"-sessie in waarin je `copier update` draait op al je projecten.
- **Regels waar niemand meer naar kijkt.** Een ontwikkelstraat werkt alleen als falingen ook écht blokkeren. Als iedereen de checks op "waarschuwing" zet, net zo goed kunnen ze weg.

## Afsluiting

Een ontwikkelstraat is geen sprint-project. Het is een investering van misschien tien tot twintig uur, verspreid over een paar weken. Na die investering haal je die tijd **iedere maand** terug, omdat je minder bugs, minder rework en minder context-switches hebt.

Het echte voordeel zit niet in de techniek, maar in je hoofd: je hoeft niet meer op te letten. Je kunt je volle aandacht bij het eigenlijke probleem houden — de applicatie die je aan het bouwen bent — in plaats van bij de regels waaraan je wilt voldoen. De regels zorgen voor zichzelf.

En dat is precies wat automatisering zou moeten doen: **niet meer werk voor jou, maar minder**.


