# Literatuuronderzoek: de leerbenadering van Gymnasium Classica

**Versie:** 0.1
**Datum:** 3 juni 2026
**Status:** Onderzoeksrapport — input voor `BRIEFING_GYMNASIUM_CLASSICA.md` en `ONTWERPKEUZES_GYMNASIUM_CLASSICA.md`
**Methode:** Gestructureerd literatuuronderzoek via een academische zoekmachine (Semantic Scholar / PubMed / Scopus / ArXiv, >200M papers) aangevuld met webbronnen. Vijf zoekhoeken, ~115 papers gescand, claims tegen elkaar afgewogen. Bronnen genummerd onderaan; betrouwbaarheidsniveau per claim aangegeven.

---

## 0. Kernoordeel in één alinea

De *componenten* van de Gymnasium Classica-benadering rusten elk op een solide tot zeer solide empirische basis — spaced repetition, het testing effect, expliciete grammatica-instructie en intelligent tutoring systems (ITS) behoren tot de best-gerepliceerde bevindingen uit de leerwetenschappen. De *combinatie* ervan in één adaptief systeem is plausibel maar niet als geheel getoetst, en vrijwel al het bewijs komt uit wiskunde/STEM en uit het moderne vreemde-talenonderwijs (vooral Engels), niet uit klassieke talen — waar de empirische basis aantoonbaar dun is. De zwakste schakel is de marketingclaim: **Bloom's "2 sigma" is nooit gerepliceerd**, en de "3x efficiëntiewinst" is een optimistische extrapolatie, geen gemeten resultaat. Aanbeveling: behoud de architectuur, maar formuleer de effectclaims conservatiever (realistisch: een substantiële maar geen spectaculaire winst) en bouw vanaf dag één meetinfrastructuur in om de eigen claim te kunnen toetsen.

---

## Deel A — De specifieke benadering, component voor component

### A1. Intelligent Tutoring Systems & mastery-based progression

Dit is het overkoepelende paradigma (MathAcademy-stijl: adaptief, mastery-gestuurd, één-op-één geëmuleerd). De evidence base is groot maar genuanceerd.

- De meest geciteerde review (VanLehn, 2011) ontkrachtte juist de mythische getallen. De gangbare aanname was: geen tutoring d=0, ITS d=1.0, menselijke tutor d=2.0. VanLehn vond menselijke tutoring op d≈0.79 en ITS op d≈0.76 — **ITS presteren bijna net zo goed als menselijke tutoren, en beide ver onder de "2 sigma"** [5].
- Meta-analyses bevestigen consistent positieve maar middelgrote effecten. Ma et al. (2014): ITS vs. klassikaal grootgroepsonderwijs g≈0.42, en **geen significant verschil** met één-op-één menselijke tutoring (g≈−0.11) of kleine groepen [2]. Kulik & Fletcher (2016): mediane winst van 0.66 SD (50e→75e percentiel) [6]. Steenbergen-Hu & Cooper: voor hbo/universiteit g≈0.32–0.37 [4], maar voor K-12 wiskunde slechts g≈0.01–0.09 [3].
- Recenter en kritischer: systematische reviews in reële schoolcontexten vinden positieve maar "afgezwakte" effecten zodra je vergelijkt met *niet-intelligente* software in plaats van met niets (Létourneau et al., 2025 [7]; Leite et al., 2025: g≈0.271 voor Amerikaanse K-12 [16]; Tlili et al., 2023: g≈0.36 in "social experiments" [17]).
- **Relevant voor dit project:** Tlili et al. (2023) vonden het *grootste* effect van ITS juist bij **taalkennis** ("huge effect" vs. andere domeinen) [17], en meerdere reviews noemen *worked examples* en interventieduur als belangrijkste moderatoren [11][16]. Steenbergen-Hu signaleerde een waarschuwing: ITS hielpen de gemiddelde leerling méér dan zwakke presteerders [3] — relevant voor de inclusiviteitsdoelen.

**Betrouwbaarheid: hoog.** ITS werken; ze zijn ongeveer zo goed als een gemiddelde menselijke tutor, niet beter dan een expert-tutor. Effectgroottes liggen typisch in de range 0.3–0.8 SD, niet 2.0.

### A2. Bloom's 2-sigma en de "3x"-claim

- De originele bevinding (Bloom, 1984): leerlingen met één-op-één mastery learning presteerden ~2 SD boven klassikaal onderwijs. **Dit specifieke resultaat is nooit gerepliceerd** [VanLehn 5; web: Education Next, Wikipedia]. Het kwam uit kortlopende studies (enkele weken) met door de onderzoekers ontworpen toetsen door promovendi van Bloom.
- De moderne consensus (o.a. Kraft) is dat realistische, goed opgezette interventies eerder in de orde van **0.2–0.5 SD** liggen, en dat het 2-sigma-frame onderzoekers misleidt en echte, repliceerbare effecten kleineert [web: 2-sigma kritiek].
- Genuanceerder tegengeluid (Nintil systematic review): hoogwaardige tutoren én hoogwaardige software *kunnen* richting 2 sigma komen, en mastery-based direct instruction levert grote effecten (>0.5 d); de methoden werken bovendien relatief beter voor zwakkere leerlingen [web: Nintil].
- MathAcademy zelf — het expliciete rolmodel — publiceert een doordachte pedagogische onderbouwing ("The Math Academy Way"), maar **geen peer-reviewed efficacy-studie** die de 2-sigma- of efficiëntieclaim hard maakt [web: mathacademy.com].

**Oordeel over de projectclaim:** De "3x efficiëntiewinst" en de impliciete 2-sigma-ambitie zijn **te sterk geformuleerd voor een onderbouwde claim.** De drie bouwstenen (tutoring/mastery, testing effect, spacing) zijn reëel, maar hun effecten stapelen niet lineair op tot 3x. Conservatief en verdedigbaar is: "aanzienlijk efficiënter per bestede minuut dan klassikaal onderwijs, met een effectgrootte die we zelf gaan meten." Behoud de visie als *ontwerpdoel*, niet als *bewezen resultaat*.

### A3. Spaced repetition (SM-2 / FSRS / half-life regression)

Dit is de sterkste pijler van alle.

- Het spacing-effect is een van de robuustste bevindingen in de psychologie. Cepeda et al. (2009): een optimale gap verhoogde uiteindelijke recall met **tot 150%**; het effect is niet-monotoon (een optimale tussenruimte, daarna afname) [12-spacing].
- Specifiek voor *taal*: de meta-analyse van Kim & Webb (2022, *Language Learning*; 98 effectgroottes, N≈3.411) vindt een **medium-tot-groot** effect van spaced practice op tweede-taalverwerving; langere spacing is beter voor uitgesteld (delayed) testen; gelijkmatige en expanderende schema's zijn statistisch gelijkwaardig [2-spacing]. Een lange reeks klassikale replicaties bevestigt dit voor woordenschat [1,3,8,11,16,18-spacing].
- Nuances die het ontwerp raken: spacing helpt vooral *expliciete* woordkennis (recall), terwijl voor *incidenteel/impliciet* leren massed practice soms gelijk of beter is [4,13-spacing]; bij jonge leerlingen en in ecologische klassencontexten zijn individuele verschillen vaak belangrijker dan het exacte spacing-interval [14-spacing].
- Algoritmekeuze: het FSRS-algoritme voorspelt vergeetgedrag aantoonbaar beter dan SM-2 op een zeer grote dataset (honderden miljoenen Anki-reviews), met ~25–30% minder reviews voor dezelfde retentie [web: FSRS-benchmark — *secundaire bronnen, middelhoge betrouwbaarheid*]. Duolingo's half-life regression (Settles & Meeder, 2016) reduceerde de voorspelfout met >45% t.o.v. baselines en verhoogde dagelijkse betrokkenheid met ~12% [web: Settles & Meeder / ACL 2016].

**Betrouwbaarheid: zeer hoog** voor het principe, **hoog** voor de taaltoepassing. **Implicatie:** de keuze in de briefing (start met SM-2, evalueer later FSRS/HLR) is verdedigbaar; FSRS is inmiddels de empirisch sterkere default en is de marginale extra complexiteit waard zodra er data is.

### A4. Het testing effect & desirable difficulties

- Retrieval practice (jezelf testen i.p.v. herlezen) is twee- tot drievoudig effectiever voor langetermijnretentie — de claim in de briefing (Roediger & Karpicke, 2006) is correct en breed gerepliceerd [web: Bjork-lab; Roediger & Karpicke].
- Bjork's "desirable difficulties"-raamwerk (spacing, interleaving, retrieval, generation, varied practice) heeft decennia bewijs; interleaving helpt discrimineren (Pan et al., 2019, d≈0.67) [web: Bjork]. Variabele retrieval-context versterkt het effect nog (Butowska-Buczyńska et al., 2024, PNAS) [17-spacing].
- **Belangrijke ontwerpwaarschuwing:** leerlingen *onderschatten* de effectiefste methoden systematisch ("metacognitieve illusie") — moeilijker voelende oefening voelt minder effectief maar leert beter [17-spacing]. Een systeem dat hierop stuurt, moet dus expliciet uitleggen waarom het moeilijk voelt, anders haken leerlingen af (raakt risico 7.4 "motivatie").

**Betrouwbaarheid: zeer hoog.** Dit is de best onderbouwde keuze in het hele ontwerp. De briefing-ambitie om actieve retrieval van ~10–15% naar 80%+ te tillen is precies het juiste mechanisme.

### A5. Bayesian Knowledge Tracing (BKT) & Item Response Theory (IRT)

Hier is de literatuur het meest *kritisch* op de specifieke modelkeuze.

- BKT is interpreteerbaar en breed gebruikt; een systematische review van 25 jaar BKT bevestigt de waarde maar ook de bekende zwaktes (Šarić-Grgić et al., 2024) [2-bkt]. Twee klassieke problemen: het **identifiability-probleem** (verschillende parameters passen even goed op dezelfde data) en **model degeneracy** (parameters die de betekenis omdraaien) — opgelost via contextuele slip/guess-schatting (Baker et al., 2008) [15-bkt] en geïndividualiseerde parameters (Yudelson et al., 2013) [20-bkt].
- Predictieve accuratesse: in eerlijke vergelijkingen presteren **logistische modellen (PFA) en — bij grote datasets — deep knowledge tracing vaak beter dan vanille-BKT** (Gervet et al., 2020: "Markov-methoden zoals BKT lopen achter") [6-bkt]. Tegelijk: bij weinig data per skill en voor *interpreteerbaarheid* blijft BKT competitief, en Bayesiaanse IRT-uitbreidingen verslaan zelfs neurale netwerken voor proficiency-schatting (Wilson et al., 2016) [19-bkt]. Verschillen tussen BKT en moderne modellen verdwijnen grotendeels al na de derde poging op een skill (Zhang et al., 2021) [10-bkt].
- Sterk relevant voor de **knowledge-graph-architectuur**: vanille-BKT modelleert skills *onafhankelijk* en mist daardoor transfer en prerequisite-structuur. Modellen die de graafstructuur expliciet meenemen (Dynamic Bayesian Networks, prerequisite-driven KT) presteren beter (Käser et al., 2014/2017 [3-bkt,17-bkt]; Chen et al., 2018 [9-bkt]). **Dat is precies de combinatie die dit project nastreeft** — graph + per-knoop-tracing — en die wordt door de literatuur ondersteund als kansrijker dan losse BKT.

**Betrouwbaarheid: hoog voor het principe, gemengd voor de modelkeuze.** BKT is een prima, interpreteerbare *start*, vooral met weinig data. Plan expliciet de optie in om naar PFA/logistische modellen of graph-aware varianten te migreren. IRT (2PL) voor itemselectie en kalibratie is goed onderbouwd en complementair.

---

## Deel B — Breder: effectieve methoden voor (klassieke) talen

### B1. Het centrale debat: expliciet vs. impliciet, GT vs. CI vs. PI

De meta-analytische literatuur is hier opvallend eenduidig — en gunstig voor de hybride keuze in de briefing.

- **Instructie helpt, en expliciete instructie helpt het meest.** Norris & Ortega (2000, 49 studies, 2300+ citaties): gerichte L2-instructie geeft grote, *duurzame* winst; expliciete typen zijn effectiever dan impliciete; en — verrassend — "Focus on Form" en "Focus on FormS" zijn even effectief [2-sla]. De update (Goo et al., 2015, 34 studies) bevestigt: **expliciet > impliciet** [1-sla].
- Spada & Tomita (2010): expliciete instructie wint voor zowel *eenvoudige* als *complexe* grammatica, en draagt bij aan spontaan gebruik, niet alleen gecontroleerde kennis [3-sla]. Li et al. (2023): expliciete instructie d≈0.81–1.07 [7-sla]. Kang et al. (2018, 35 jaar ISLA): totaal effect g≈1.06, met slechts een klein verschil expliciet/impliciet [16-sla].
- **Processing Instruction (VanPatten):** Shintani's meta-analyse (2015, 33 studies) nuanceert: PI is beter dan productiegerichte instructie voor *receptieve* kennis, maar productiegerichte instructie is even goed of beter voor *productieve* kennis — en met gelijke expliciete uitleg wint productie zelfs [12-sla]. Comprehension-based en production-based instructie zijn dus *complementair*.
- **Krashen / Comprehensible Input:** de input-hypothese (i+1) wordt in de toegepaste taalkunde gewaardeerd om de nadruk op begrijpelijke input, maar is wetenschappelijk omstreden: het concept i+1 is **niet precies gedefinieerd en moeilijk falsifieerbaar**, en input *alleen* leidt aantoonbaar niet tot productieve beheersing (cf. receptieve tweetaligen) [web: Krashen-kritiek; Frontiers 2025]. Voor een examen dat expliciete grammaticakennis toetst is puur CI ontoereikend.

**Conclusie Deel B1:** De aanbeveling in de briefing (§3.2.2) — **expliciete grammatica-instructie + contextueel lezen + processing-oefeningen + productieve consolidatie** — is precies wat de meta-analytische literatuur ondersteunt. Dit is geen eclecticisme maar de empirisch best verdedigbare mix. De ene aanscherping: voeg op grond van Shintani (2015) bewust *productiegerichte* oefening toe voor de vormen die actief beheerst moeten worden (vervoegen/verbuigen), niet alleen receptieve processing — wat ontwerpkeuze 5 (productieve oefeningen) al doet.

### B2. Woordenschat: frequentie + spacing + retrieval

- Frequentiegestuurd vocabulaire (de keuze in de briefing) sluit aan bij Nation's invloedrijke werk over high-frequency vocabulary en vocabulary size; de gescande L2-woordenschatstudies gebruiken consequent frequentie-gecontroleerde woordenlijsten en flashcard-/fill-in-the-blank-tools [3,6-spacing].
- De effectiefste woordenschatdidactiek combineert spacing + retrieval + corrective feedback [16-spacing], en fill-in-the-blank profiteert sterker van spacing dan kale flashcards [6-spacing] — een concreet argument om naast herkenning ook productieve invul-items te gebruiken.
- Let op de receptief/productief-asymmetrie: spacing en retrieval helpen receptieve kennis betrouwbaar, productieve kennis vergt meer en moeilijker oefening [19-spacing, 12-sla].

**Betrouwbaarheid: hoog.** De vocabulaire-aanpak (frequentiebanden, semantische clusters, SR, gemengde itemtypen) is goed onderbouwd.

### B3. Klassieke talen specifiek — waar de evidence dun wordt

Dit is de belangrijkste kanttekening van het hele rapport.

- **Empirisch onderzoek naar het leren/onderwijzen van Latijn en Grieks is schaars.** Het lezen van Latijn is "pas recent" object van empirisch onderzoek; veel literatuur bestaat uit ervaringsverslagen en didactische suggesties, niet uit gecontroleerde studies [web: *Journal of Latin Linguistics* 2019, "Latin learning and instruction as a research field"].
- De traditionele grammatica-vertaalmethode vertoont volgens dit onderzoek "aanzienlijke zwaktes" in het ontwikkelen van basale *leesvaardigheid* (het richt zich op decoderen en hercoderen naar de L1, niet op vlot lezen) [web: Cogent Education 2024, corpus-based fluency tool].
- Opkomende, psycholinguïstisch geïnformeerde benaderingen (eye-tracking, think-aloud, corpus-based fluency-tools) zijn veelbelovend maar klein van schaal [web: De Gruyter / *JoLL* 2018].
- Het debat in de klassieke-talenwereld kent drie stromingen — Grammar-Translation, Comprehensible Input, en "Reading Methods" — vergelijkbaar met B1, maar **vrijwel zonder de gecontroleerde effectstudies** die het moderne vreemde-talenonderwijs wel heeft [web: Memoria Press; TCL/CAMWS]. LLPSI (Ørberg) is invloedrijk maar wordt didactisch vaak *misverstaan* als puur-CI: het introduceert grammaticale features juist stap voor stap en verwacht expliciet begrip — dus dichter bij de hybride dan bij Krashen [web: The Patrologist].

**Implicatie:** De generalisatie van STEM/EFL-bewijs naar Latijn/Grieks is een **redelijke maar onbewezen aanname**. Het project doet er goed aan dit expliciet te erkennen (zoals de briefing met externe validatie en het staatsexamen als objectieve toets ook al doet) en zelf data te genereren — er is hier een reëel gat in de literatuur dat het project zou kunnen helpen vullen.

---

## Deel C — Beoordeling van de projectclaims

| Claim uit de briefing | Oordeel | Onderbouwing |
|---|---|---|
| Spaced repetition verdubbelt/verdrievoudigt retentie per minuut | **Ondersteund** | Cepeda tot +150%; Kim & Webb medium-groot voor L2 [12-spacing, 2-spacing] |
| Testing effect 2–3x effectiever dan passief | **Ondersteund** | Roediger & Karpicke; Bjork-raamwerk [web] |
| Expliciete grammatica + contextueel lezen + PI (hybride) | **Sterk ondersteund** | Norris & Ortega, Goo, Spada & Tomita, Shintani [1,2,3,12-sla] |
| Knowledge graph + per-knoop tracing | **Ondersteund (kansrijk)** | Graph-aware KT > vanille-BKT [3,9,17-bkt] |
| BKT als learner model | **Deels** — interpreteerbaar maar niet de sterkste voorspeller | Gervet, Wilson, identifiability [6,19-bkt,15-bkt] |
| ITS ≈ effectief als één-op-één tutoring | **Ondersteund** | VanLehn d≈0.76 vs 0.79; Ma g≈−0.11 [5,2] |
| Bloom 2-sigma als richtpunt | **Niet gerepliceerd** — als ambitie ok, als claim te sterk | VanLehn; Education Next; Kraft [5, web] |
| "3x efficiëntiewinst" t.o.v. klassikaal | **Te sterk** — plausibel als doel, niet bewezen | Effecten stapelen niet lineair; realistisch 0.2–0.8 SD [5,6, web] |
| Generalisatie naar Latijn/Grieks | **Aanname** — evidence base dun | JoLL 2019; empirisch onderzoek schaars [web] |

---

## Deel D — Concrete aanbevelingen

1. **Herformuleer de effectclaims conservatiever.** Vervang "3x efficiëntiewinst" en de impliciete 2-sigma-belofte in de briefing door een falsifieerbare, meetbare ambitie (bijv. "doel: staatsexamen halen in vergelijkbaar urenvolume met aantoonbaar hogere retentie; effectgrootte wordt intern gemeten"). Dit beschermt de geloofwaardigheid bij externe validatie.
2. **Bouw meet-infrastructuur vanaf fase 0.** Het grootste gat in de literatuur is klassieke talen zelf. Leg per leerling retentie-, tijd- en masterydata vast zodat het project zijn *eigen* effectgrootte kan rapporteren (pilot tegen staatsexamen = objectieve externe toets). Dit maakt van een zwakte een onderscheidende sterkte.
3. **Behoud de hybride didactiek — die is empirisch het best onderbouwd.** Voeg op grond van Shintani (2015) bewust productiegerichte oefening toe voor actief te beheersen morfologie, naast receptieve processing-oefeningen.
4. **Prioriteer spaced repetition en retrieval practice; overweeg FSRS eerder dan "later".** Dit zijn de twee sterkste, goedkoopste hefbomen. SM-2 als start is prima; FSRS is de empirisch betere default zodra er data is.
5. **Plan de learner-modelmigratie expliciet in.** Start met BKT (interpreteerbaar, werkt met weinig data), maar ontwerp de interface zo dat PFA/logistische of graph-aware modellen later inplugbaar zijn. Modelleer prerequisite-/transfer-structuur in het learner model, niet alleen in de graph — dat is juist waar graph-aware tracing wint.
6. **Adresseer de metacognitieve illusie in de UX.** Omdat effectieve (moeilijke) oefening minder effectief *voelt*, is expliciete uitleg + voortgangsvisualisatie (de groen kleurende heat map) geen luxe maar een retentie-instrument. Sluit aan bij risico 7.4.
7. **Erken de generalisatie-aanname in de documentatie.** Vermeld dat vrijwel al het onderliggende bewijs uit STEM/EFL komt en dat klassieke talen een dunne evidence base hebben — dit is intellectueel eerlijk en stuurt de externe validatie (klassieke-taleninstituut).

---

## Bronnen

### Academische papers — Intelligent Tutoring Systems & mastery
- [2] Ma, W. et al. (2014). *Intelligent tutoring systems and learning outcomes: A meta-analysis.* Journal of Educational Psychology. https://consensus.app/papers/details/15bad3825a355ae8b71876954042805f/
- [3] Steenbergen-Hu, S. & Cooper, H. (2013). *Meta-analysis of ITS on K–12 mathematics.* J. Educ. Psychol. https://consensus.app/papers/details/ed8d0ba8b3ba520496342d1cfc274a1b/
- [4] Steenbergen-Hu, S. & Cooper, H. (2013). *Meta-analysis of ITS on college students' learning.* J. Educ. Psychol. https://consensus.app/papers/details/8b54bacc97ca534980906b3ca6c978a1/
- [5] VanLehn, K. (2011). *The Relative Effectiveness of Human Tutoring, ITS, and Other Tutoring Systems.* Educational Psychologist. https://consensus.app/papers/details/63ed22c148a959538c81a9f2409dfc89/
- [6] Kulik, J. & Fletcher, J. (2016). *Effectiveness of Intelligent Tutoring Systems.* Review of Educational Research. https://consensus.app/papers/details/782be0b9909252ea98683faacc402245/
- [7] Létourneau, A. et al. (2025). *Systematic review of AI-driven ITS in K-12.* npj Science of Learning. https://consensus.app/papers/details/1e4d48effd3154c180864cb6b75eeb01/
- [11] Huang, X. et al. (2025). *Effects of ITS on Educational Outcomes.* Int. J. Distance Educ. Technol. https://consensus.app/papers/details/77056234a2a2572a90d1ab5851566760/
- [16] Leite, W. et al. (2025). *Do ITS benefit K-12 students? Heterogeneity of treatment effects in the U.S.* ArXiv. https://consensus.app/papers/details/b7b17f52df4f561eb573f743ddc9dfaf/
- [17] Tlili, A. et al. (2023). *ITS Examined in Social Experiments — Is the Magic Gone? A Meta-Analysis.* IEEE ICALT. https://consensus.app/papers/details/09f94399e28d52ca802608374820ef85/

### Academische papers — Spacing, retrieval & vocabulaire (L2)
- [2-spacing] Kim, S.K. & Webb, S. (2022). *The Effects of Spaced Practice on Second Language Learning: A Meta-Analysis.* Language Learning. https://consensus.app/papers/details/8bf5cae9a33f5c18b7b789b71111bb05/
- [12-spacing] Cepeda, N. et al. (2009). *Optimizing distributed practice.* Experimental Psychology. https://consensus.app/papers/details/1aee86902085592caf5b7717c70d361e/
- [4-spacing] Nakata, T. & Suzuki, Y. (2020). *Effects of spacing on contextual vocabulary learning.* Second Language Research. https://consensus.app/papers/details/3f0a97527ee652e49b5fef1f8595e895/
- [6-spacing] Kim, S.K. & Webb, S. (2023). *Spaced practice: fill-in-the-blanks vs. flashcards.* Modern Language Journal. https://consensus.app/papers/details/043fef7f3eb85c0e8320d1755c25b1a9/
- [14-spacing] Kasprowicz, R. et al. (2019). *Distribution of practice for FL verb morphology (young learners).* Modern Language Journal. https://consensus.app/papers/details/75e05a3a98e45d358a752e8f0ded7393/
- [16-spacing] Lotfolahi, A. et al. (2017). *Spacing effects in vocabulary learning: young EFL learners.* Cogent Education. https://consensus.app/papers/details/b3c6618bbe8d51809ac7884dee0f8f9d/
- [17-spacing] Butowska-Buczyńska, E. et al. (2024). *The role of variable retrieval in effective learning.* PNAS. https://consensus.app/papers/details/c8371a0a1d1c5af9a35662cd0566e1be/
- [19-spacing] Serfaty, J. & Serrano, R. (2024). *Lag effects for FL vocabulary through Quizlet.* Language Learning & Technology. https://consensus.app/papers/details/c68825dadbfe53fca72365978285406b/

### Academische papers — SLA: expliciet/impliciet & Processing Instruction
- [1-sla] Goo, J. et al. (2015). *Implicit and explicit instruction in L2 learning: Norris & Ortega revisited.* https://consensus.app/papers/details/cae0777e40695f38a5571d97dcd9e7cd/
- [2-sla] Norris, J. & Ortega, L. (2000). *Effectiveness of L2 Instruction: A Research Synthesis and Quantitative Meta-analysis.* Language Learning. https://consensus.app/papers/details/cb9eb78b6d62595fb89f1d94d04b3337/
- [3-sla] Spada, N. & Tomita, Y. (2010). *Interactions between Type of Instruction and Type of Language Feature: A Meta-Analysis.* Language Learning. https://consensus.app/papers/details/b8f1693688875fca86f91a40f5ff766f/
- [7-sla] Li, F. et al. (2023). *Effects of different forms of explicit instruction on L2 development: A meta-analysis.* Foreign Language Annals. https://consensus.app/papers/details/843033a4e3fa577390714a4383eab02c/
- [12-sla] Shintani, N. (2015). *The Effectiveness of Processing Instruction and Production-based Instruction on L2 Grammar Acquisition: A Meta-Analysis.* Applied Linguistics. https://consensus.app/papers/details/3861c5fc81405c41b81f9182140bcff0/
- [16-sla] Kang, E. et al. (2018). *Thirty-five years of ISLA on form-focused instruction: A meta-analysis.* Language Teaching Research. https://consensus.app/papers/details/0df14a2dd8fc5a4986aa4a16054cbaf2/

### Academische papers — Knowledge Tracing / IRT
- [2-bkt] Šarić-Grgić, I. et al. (2024). *Twenty-five years of Bayesian knowledge tracing: a systematic review.* UMUAI. https://consensus.app/papers/details/364b478d4a065957a54b0a25a8b1a223/
- [3-bkt] Käser, T. et al. (2017). *Dynamic Bayesian Networks for Student Modeling.* IEEE TLT. https://consensus.app/papers/details/88feee569dea562895553d045b31e5f1/
- [6-bkt] Gervet, T. et al. (2020). *When is Deep Learning the Best Approach to Knowledge Tracing?* https://consensus.app/papers/details/1307ddb6dc305842858d965713149af4/
- [9-bkt] Chen, P. et al. (2018). *Prerequisite-Driven Deep Knowledge Tracing.* IEEE ICDM. https://consensus.app/papers/details/c6c1fe52ab1357e1b16098cd9e8ab122/
- [10-bkt] Zhang, J. et al. (2021). *Knowledge Tracing Models' Predictive Performance when a Student Starts a Skill.* https://consensus.app/papers/details/a87ce7ebe8ca51268af73000e797f0e3/
- [15-bkt] Baker, R. et al. (2008). *Contextual Estimation of Slip and Guess Probabilities in BKT.* https://consensus.app/papers/details/fe491454eee45993a40e08e4920e7ad0/
- [17-bkt] Käser, T. et al. (2014). *Beyond Knowledge Tracing: Modeling Skill Topologies with Bayesian Networks.* https://consensus.app/papers/details/2300e95db53a52ac93b253a0838ef083/
- [19-bkt] Wilson, K. et al. (2016). *Back to the basics: Bayesian extensions of IRT outperform neural networks for proficiency estimation.* https://consensus.app/papers/details/ed68e04414d854558724e50c5149aed9/
- [20-bkt] Yudelson, M. et al. (2013). *Individualized Bayesian Knowledge Tracing Models.* https://consensus.app/papers/details/0a2bb6757fe858d8be9267d68f9b2a67/

### Webbronnen
- Bloom's 2-sigma — kritiek & replicatie: Education Next, *Two-Sigma Tutoring: Separating Science Fiction from Science Fact* (https://www.educationnext.org/two-sigma-tutoring-separating-science-fiction-from-science-fact/); Nintil, *On Bloom's two sigma problem* (https://nintil.com/bloom-sigma/); Wikipedia (https://en.wikipedia.org/wiki/Bloom's_2_sigma_problem)
- MathAcademy pedagogiek: https://www.mathacademy.com/how-our-ai-works ; *The Math Academy Way* (https://www.justinmath.com/files/the-math-academy-way.pdf)
- Spaced repetition algoritmen: Settles, B. & Meeder, B. (2016), *A Trainable Spaced Repetition Model for Language Learning*, ACL (https://aclanthology.org/P16-1174/ ; dataset https://github.com/duolingo/halflife-regression); FSRS-benchmark (open-spaced-repetition, secundair: https://deepwiki.com/open-spaced-repetition/fsrs-optimizer/7.3-comparison-with-sm-2)
- Desirable difficulties / retrieval: Bjork & Bjork (2011), *Creating Desirable Difficulties to Enhance Learning* (https://bjorklab.psych.ucla.edu/wp-content/uploads/sites/13/2016/04/EBjork_RBjork_2011.pdf)
- Krashen-kritiek: *Beyond comprehensible input: a neuro-ecological critique* (Frontiers in Psychology, 2025; https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2025.1636777/full); *A Critical Review of Krashen's Input Hypothesis* (http://jehd.thebrpi.org/journals/jehd/Vol_4_No_4_December_2015/16.pdf)
- Klassieke talen didactiek: *Latin learning and instruction as a research field*, Journal of Latin Linguistics 2019 (https://www.degruyterbrill.com/document/doi/10.1515/joll-2019-0001/html); *Reading Latin and the need for empirical research* (https://www.degruyterbrill.com/document/doi/10.1515/joll-2018-0013/html); *Development of basic reading skills in Latin: a corpus-based tool* (Cogent Education 2024, https://www.tandfonline.com/doi/full/10.1080/2331186X.2024.2416819); LLPSI/Ørberg & CI: The Patrologist (https://thepatrologist.com/2020/08/15/misunderstanding-ci-krashen-and-orberg/)

---

*Dit rapport is een momentopname. De academische bronnen zijn via een geaggregeerde zoekmachine geselecteerd; voor citatie in formele publicaties wordt aangeraden de originele DOI's te verifiëren.*
