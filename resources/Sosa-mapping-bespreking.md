# Bespreking: `Sosa mapping.xlsx` (Digitaal Vlaanderen)

Dit document bespreekt de inhoud van `resources/Sosa mapping.xlsx`, aangeleverd door de
collega's van Digitaal Vlaanderen, en toetst de feitelijke SSN/SOSA-beweringen erin af tegen
de ontologieën die in dit project effectief geladen worden —
`src/main/resources/org/w3/www/ns/sosa/ssn-sosa_2023.ttl` (§3) en, in een tweede controleronde,
`src/main/resources/ontologies/ssn-sosa-fullprov-o-p-plan-geosparql-dbo.ttl` +
`src/main/resources/org/purl/net/p-plan/p-plan.ttl` +
`src/main/resources/ontologies/pplan-sosa.ttl` (§4) — en tegen de modelleringsregels in
`CLAUDE.md`. Een volledig gecorrigeerde en aangevulde versie is gepubliceerd als
`resources/Sosa mapping (gecorrigeerd).xlsx`; alle bevindingen hieronder zijn daarin verwerkt
(zie het tabblad **Wijzigingslog** in dat bestand voor de rij-per-rij traceerbaarheid).

---

## 1. Structuur van het bestand

Het werkboek bevat 10 tabbladen, met een kleurcode die op tabblad "Legenda tabbladen" wordt
toegelicht:

| Kleur | Betekenis | Tabbladen |
|---|---|---|
| Groen | Tijdelijke, projectmatige tabbladen | Legenda tabbladen, Lessons_to_receptenboek, Actiepunten |
| Blauw | Informatie/elementen bestemd voor de publicatie | Context toelichting, **Begrippen v2**, Regels, Keuzes, Beslisboom, Receptenboek |
| Rood | Oude, gearchiveerde bladen | **Begrippen** (v1) |

Dit is bevestigd via de `tabColor`-attributen in de xlsx zelf (niet enkel de tekstuele legenda):
`Begrippen` (10 tabbladen terug, 128 rijen) staat op `FFC00000` (rood/gearchiveerd) en is
vervangen door **Begrippen v2** (101 rijen, `FFDCEAF7`, blauw). Voor de inhoudelijke bespreking
hieronder is dus **Begrippen v2** het leidende tabblad — Begrippen v1 wordt enkel gebruikt als
extra context waar v2 een detail lijkt te missen.

**Kanttekening** *(tabblad: Begrippen v2, vergeleken met Begrippen v1)*: rij B080 in Begrippen v2
(`FeatureOfInterest | Relatie | featureH | ...`) is onafgewerkt — de kolommen Ontologie Term,
Definitie en Range zijn leeg, terwijl het corresponderende begrip in Begrippen v1 (rij 92,
`sosa:featureHasUltimateSample`) wel volledig is uitgewerkt. Dit lijkt een kopieerfout bij de
migratie v1 → v2.

---

## 2. Inhoud per tabblad

- **Legenda tabbladen** — kleurcode-uitleg (zie boven).
- **Lessons_to_receptenboek** — 14 "geleerde lessen" uit het traject (SOSA, PROV-O), met
  koppeling naar wat er al verwerkt is. Grotendeels nog open (status 0).
- **Actiepunten** — 10 actiepunten (A01–A10), o.a. I-ADOPT-afstemming, FOI-kardinaliteit,
  tijdreeksen/collections/rapporten, W3C-template-evaluatie. Eigenaars: Geert, Pieter, PM.
- **Context toelichting** — wanneer PROV-O naast SOSA gebruiken (herkomst, derivatieketens,
  auditability), met kernprincipe "SOSA beschrijft observaties, PROV-O beschrijft hoe ze
  tot stand kwamen" en link naar de officiële SOSA-PROV-alignment.
- **Begrippen v2** — 100 begrippen (B001–B100): kernwoordenlijst van SSN/SOSA-2023- en
  PROV-O-termen, per architectuurlaag (Planning/Deployment/Execution/Cross-cutting/Provenance),
  telkens met ontologieterm, definitie, brownie-voorbeeld, gebruiksregels en -fouten.
- **Regels** — 5 modelleringsregels (RG01–RG05): Planning≠Execution, FOI enkelvoudig,
  pragmatisch modelleren, scheiding lifecycle-lagen, gebruik actuele 2023-terminologie
  (`sosa:Property` i.p.v. deprecated `ObservableProperty`/`ActuatableProperty`).
- **Keuzes** — 8 modelleerkeuzes (K01–K08) met optie A/B en toelichting (System-as-Agent,
  drielaags of niet, Samples of niet, ObservationCollection of niet, foutieve observaties
  behouden of niet, p-plan+PROV-O vs. enkel sosa:Procedure, provenance-detailniveau,
  derivatieketens expliciet of niet).
- **Beslisboom** — 6 ja/nee-vragen (B01–B06) die naar de Keuzes-tab verwijzen; praktisch
  hulpmiddel om snel tot een modelleerbeslissing te komen.
- **Receptenboek** — 9 geplande voorbeelden (V01–V09), waarvan enkel het Brownie-voorbeeld
  (V01, W3C PR#442) klaar is; de rest is "nog te maken" of "verder uit te werken".
- **Begrippen (v1, gearchiveerd)** — voorloper van Begrippen v2, met vergelijkbare inhoud maar
  andere kolomstructuur (ID 0–37) en enkele extra begrippen die niet expliciet in v2 terugkomen
  (System Capabilities, Location/Geometry-patroon, UoM-patroon, Domain types-patroon).

---

## 3. Juistheidscontrole tegen de geladen ontologie

*Betreft uitsluitend het tabblad **Begrippen v2** (en, ter vergelijking, het gearchiveerde
**Begrippen** v1) — de andere tabbladen (Regels, Keuzes, Beslisboom, Context toelichting,
Receptenboek, …) bevatten geen verifieerbare ontologie-technische beweringen (domain/range/inverse)
en zijn hier niet aan getoetst.*

Ik heb de circa 100 rijen in Begrippen v2 (en waar nodig v1) rij per rij afgezet tegen
`ssn-sosa_2023.ttl`. Het overgrote deel — domains, ranges, inverse relaties van
`hosts`/`isHostedBy`, `implements`/`implementedBy`, `usedProcedure`/`usedForExecution`,
`hasProperty`/`isPropertyOf`, `hasSample`/`isSampleOf`, `hasSubSystem`/`isSubSystemOf`,
`hasInputValue`, `hasProcedure`, `featureHasUltimateSample`/`isSampleOfUltimateFOI`,
`hasOriginalSample`/`isOriginalSampleOf`, en de PROV-alignments `Procedure ⊑ prov:Plan`,
`Execution ⊑ prov:Activity`, `System ⊑ prov:Agent, prov:Entity`, `FeatureOfInterest ⊑ prov:Entity`
— klopt woordelijk met wat in de ontologie gedefinieerd staat. Ook Regel 5 ("gebruik
`sosa:Property`, niet de deprecated `ObservableProperty`/`ActuatableProperty`") is correct:
die laatste twee termen komen letterlijk niet meer voor in `ssn-sosa_2023.ttl`.

Een paar punten verdienen echter aandacht:

### 3.1 Fout: `actsOn` / `actsOnProperty` / `isActedOnBy` / `wasActedOnBy` door elkaar gehaald

**Tabblad(en):** Begrippen v2 (rijen B063–B065) én, identiek, het gearchiveerde tabblad
Begrippen v1 (rijen 76–78) — de fout is dus al bij de eerste versie ontstaan en ongewijzigd
overgenomen in v2.

| Rij | Claim in Excel | Werkelijkheid in `ssn-sosa_2023.ttl` |
|---|---|---|
| `actsOnProperty` | Inverse: `sosa:isActedOnBy` | Inverse is **`sosa:wasActedOnBy`** (domain `Actuation`/`ActuationCollection`, range `Property`) |
| `actsOn` | Range = `FeatureOfInterest`; "Directe actie op FOI (niet enkel op de Property)" | `sosa:actsOn` heeft domain **`Actuator`** en range **`Property`** (`rdfs:subPropertyOf sosa:forProperty`) — het is het Deployment-niveau-equivalent van `sosa:observes`, net als bij Sensors. Er is geen relatie "Actuation acteert rechtstreeks op FOI" in deze ontologie. |
| `wasActedOnBy` | "Inverse van `actsOn`"; range `Actuation`/`ActuationCollection` | Domain is `Property`, range is `Actuation`/`ActuationCollection`, maar de inverse is **`actsOnProperty`**, niet `actsOn` |

Samengevat: `actsOn` zit op het **Deployment**-niveau (Actuator → Property, analoog aan
`sosa:observes`), niet op het **Execution**-niveau (Actuation). De Excel plaatst `actsOn` echter
onder "Execution / Actuation" en kent er een FOI-relatie aan toe die niet bestaat. Dit is de
enige inhoudelijk foute bewering die ik in het bestand gevonden heb, en ze staat zowel in het
gearchiveerde begrippenblad als (ongewijzigd) in de nieuwe v2-versie — dus geen tijdelijke typfout
maar een aanhoudend misverstand dat best gecorrigeerd wordt vóór publicatie.

### 3.2 Twijfelachtig: `sosa:Asset` als klasse

**Tabblad:** Begrippen v2, rij B043 (`Asset | Klasse | sosa:Asset | Abstracte superklasse van
Platform en System`). Ook aanwezig in het gearchiveerde Begrippen v1, rij 117 (ID 26), met
dezelfde bewering.

In de geladen `ssn-sosa_2023.ttl` bestaat **geen** `owl:Class sosa:Asset`, en dat is opnieuw
bevestigd in `ssn-sosa-fullprov-o-p-plan-geosparql-dbo.ttl` (§4). Wat wél bestaat is de
eigenschap `sosa:deployedAsset` (domain `Deployment`, `schema:rangeIncludes` de unie van
`{Actuator, Platform, System, Sensor, Sampler}`) en het woord "asset" duikt alleen op in
`skos:definition`-teksten ("relation from an asset (System or Platform) …") als informele
verzamelnaam. Er is dus geen formele klasse waar `Platform`/`System` een `rdfs:subClassOf` van
zijn.

**In `Sosa mapping (gecorrigeerd).xlsx` is rij B043 daarom volledig verwijderd**, niet enkel
geannoteerd — een eerdere tussenversie liet de rij nog staan met `Rijtype = "Patroon (informeel)"`
maar behield `Naam = "Asset"` en `Ontologie Term = "sosa:Asset"`, wat bij het scannen van de
kolom nog steeds de indruk wekte dat het een geldige term was. Diezelfde onderliggende fout stond
trouwens ook op **rij B026** (`sosa:deployedAsset`, "Generaliseert deployedSystem naar Asset",
Range = `Asset`) — ook daar is de Range gecorrigeerd naar `Platform/System (unie)`. Het
gearchiveerde Begrippen v1 (rij 117, ID 26) blijft ongewijzigd, ter documentatie van de
oorspronkelijke fout.

### 3.3 Nuance: "Exact 1" voor `hasFeatureOfInterest`

**Tabbladen:** Begrippen v2, rij B051 (en het gelijkaardige rij B056 met "Regel 2"); de
bijbehorende regel staat ook op tabblad **Regels** (RG02, "FeatureOfInterest enkelvoudig") en
het openstaande vraagpunt op tabblad **Actiepunten** (A02, "FOI-kardinaliteit").

Begrippen v2, rij B051 stelt `hasFeatureOfInterest` op `Execution` verplicht met kardinaliteit
"Exact 1 (verplicht)". In de OWL-encodering zelf is dit enkel een `owl:someValuesFrom`-restrictie
(minstens 1), er staat geen `owl:cardinality`/`owl:maxQualifiedCardinality` van 1 op. "Exact 1" is
dus een projectconventie/interpretatie van de spec-tekst, niet iets wat de ontologie zelf
technisch afdwingt. Dat is verdedigbaar (het is ook zo genoteerd als "Regel 2", met een open vraag
over kardinaliteit — actiepunt A02), maar de formulering "verplicht" mag niet gelezen worden als
"OWL-gevalideerd"; SHACL-validatie in dit project zou zelf een `sh:maxCount 1` moeten opleggen als
die garantie gewenst is.

### 3.4 Ontbrekend: `sosa:hasInput` (Procedure-niveau) wordt nergens gedocumenteerd

**Tabbladen:** ontbreekt op Begrippen v2 én op het gearchiveerde Begrippen v1 — nergens in het
hele werkboek wordt `sosa:hasInput` vermeld (enkel `hasInputValue` op Begrippen v2, rij B053).

De Excel documenteert `sosa:hasInputValue` (Execution-niveau, concrete waarde) correct, maar
vermeldt nergens `sosa:hasInput` (Procedure-niveau, abstract inputtype — wél aanwezig in
`ssn-sosa_2023.ttl`, regel 2194). Dat is precies het onderscheid dat `CLAUDE.md` §7 **R5**
normatief maakt ("`sosa:hasInput` hoort uitsluitend op `sosa:Procedure`-nodes"). Zonder dat begrip
in het Receptenboek/Begrippen-blad is er een reëel risico dat toekomstige voorbeelden
`hasInputValue` en `hasInput` door elkaar gebruiken.

---

## 4. Tweede controleronde: `ssn-sosa-fullprov-o-p-plan-geosparql-dbo.ttl` + p-plan

*Betreft het tabblad **Begrippen v2**.* Deze tweede ontologie is rijker dan `ssn-sosa_2023.ttl`
alleen: ze bevat ook de volledige PROV-O- en p-plan-modules, en — uniek voor dit bestand —
**Nederlandstalige `@nl`-labels en -definities** naast de Engelse. Ik heb elke `Ontologie Term`
uit Begrippen v2 (105 stuks) opnieuw opgezocht, ditmaal met `rdflib` (domain/domainIncludes,
range/rangeIncludes, `owl:inverseOf`, `owl:Restriction`s), plus de losse p-plan-bestanden erbij
gehaald omdat p-plan daar preciezer in staat. Dit leverde, naast een volledige bevestiging van
§3, drie nieuwe bevindingen op.

### 4.1 Fout: `ssn:` in plaats van `sosa:` voor Stimulus/detects/isProxyFor/wasOriginatedBy

**Rijen:** B032 (`detects`), B040 (`Stimulus`), B041 (`isProxyFor`), B042 (`wasOriginatedBy`) —
identiek fout in het gearchiveerde Begrippen v1.

In **beide** geladen ontologiebestanden bestaan deze vier termen uitsluitend onder het
`sosa:`-namespace (`sosa:Stimulus`, `sosa:detects`, `sosa:isProxyFor`, `sosa:wasOriginatedBy`).
Het `ssn:`-prefix zelf komt in `ssn-sosa-fullprov-o-p-plan-geosparql-dbo.ttl` enkel voor als een
kale `owl:Ontology`-declaratie, zonder één eigen klasse of property — exact hetzelfde patroon als
Regel 5 al beschrijft voor `sosa:Property` (verplaatst van `ssn:`/deprecated naar `sosa:` sinds
de 2023-editie), maar dan voor deze vier termen, die de Excel nog met het oude `ssn:`-prefix
noteert.

**Reëel gevolg:** deze exacte fout (`ssn:Stimulus`, `ssn:wasOriginatedBy`, `ssn:isProxyFor`) komt
ook voor in al gepubliceerde datavoorbeelden — `Nigella-Lawson-Brownies/Nigella-Lawson-Brownies-simple.ttl`,
`EnergieManagementSystem/DatavoorbeeldStilleggingProductielijn/DatavoorbeeldStilleggingProductielijn_herzien.ttl`
en `EnergieManagementSystem/DatavoorbeeldIsolatieadvies/DatavoorbeeldIsolatieadvies_herzien.ttl`.
Deze `.ttl`-bestanden riskeren een `[VOCAB ERROR]` bij de eerstvolgende `mvn compile exec:java`,
omdat `ssn:wasOriginatedBy`/`ssn:Stimulus`/`ssn:isProxyFor` niet in `completeOntology` bestaan.
**Dit valt buiten de scope van de Excel-correctie** en wordt hier enkel gesignaleerd — een
herziening van die datavoorbeelden volgt de workflow in `CLAUDE.md` §8 en is aparte actie.

### 4.2 Ontbrekend: `sosa:Property`, `hasProcedure`/`isProcedureFor`, p-plan-relaties en `hasOutput`

Bij het doorlopen van de p-plan- en Cross-cutting-secties bleek Begrippen v2 systematisch meer
te hebben laten vallen bij de migratie van v1 dan enkel de Sample-keten (§3.4):

- **`sosa:Property` zelf heeft geen klasse-rij** in Begrippen v2 — terwijl Regel 5 nu net over
  deze klasse gaat ("gebruik `sosa:Property`, niet de deprecated `ObservableProperty`/
  `ActuatableProperty`"). Wel aanwezig in Begrippen v1 (rijen 93–97).
- **`sosa:hasProcedure`/`sosa:isProcedureFor`** (Property ↔ Procedure) — aanwezig in v1 (rij 95),
  ontbrak in v2.
- **`sosa:hasOutput`/`sosa:outputFor`** — het officiële SOSA 2023-tegenhangerpaar van
  `sosa:hasInput`/`sosa:inputFor` (zie §3.4); ontbrak in zowel v1 als v2.
- **P-plan-relaties** `isStepOfPlan`, `isSubPlanOfPlan`, `isVariableOfPlan`, `correspondsToStep`,
  `correspondsToVariable` — aanwezig in v1 (rijen 6, 10, 11, 16, 17), ontbraken volledig in v2,
  terwijl ze actief gebruikt worden in `Nigella-Lawson-Brownies`, `elektrisch-raam`,
  `temperatuur-raam`, `paleo` en `EnergieManagementSystem`, en `CLAUDE.md` §7 R7 er expliciet
  naar verwijst ("p-plan:correspondsToVariable en p-plan:correspondsToStep voor
  abstractie-naar-concreet").

**Bijkomende correctie binnen deze aanvulling:** de officiële p-plan-ontologie
(`org/purl/net/p-plan/p-plan.ttl`, v1.3) definieert **geen** `p-plan:hasStep` — enkel de inverse
`p-plan:isStepOfPlan` (Step → Plan) bestaat formeel. `p-plan:hasStep` komt wel voor in
`EnergieManagementSystem/DatavoorbeeldPreHeatingHvac/README.md`; ook dat is een prozavoorbeeld,
geen gevalideerd `.ttl`-bestand, maar goed om te weten mocht het ooit naar Turtle overgezet
worden.

### 4.3 Nieuwe vondst: project-specifieke brug tussen p-plan en `sosa:Procedure`

`src/main/resources/ontologies/pplan-sosa.ttl` — een apart, klein (39 regels) bestand dat wél
mee geladen wordt door de pipeline maar nergens in de Excel, in `CLAUDE.md`, of in Begrippen v1
vermeld stond — legt een formele alignment vast:

- `p-plan:Plan rdfs:subClassOf sosa:Procedure` en `p-plan:Step rdfs:subClassOf sosa:Procedure`.
- Drie `owl:propertyChainAxiom`'s die `sosa:usedProcedure` automatisch afleiden uit de
  p-plan-structuur: via `correspondsToStep ∘ isDecomposedAsPlan`, via
  `hasResult ∘ correspondsToVariable ∘ outputFor`, en via
  `hasFeatureOfInterest ∘ correspondsToVariable ∘ inputFor`.

Dit is inhoudelijk relevant voor Keuze K06 ("p-plan+PROV-O vs. enkel sosa:Procedure") — het
toont dat de twee aanpakken in dít project formeel geen alternatieven zijn maar elkaar aanvullen:
een `p-plan:Plan`/`p-plan:Step` **is tegelijk** een `sosa:Procedure`, en de p-plan-laag voedt
`sosa:usedProcedure` automatisch via inferentie. Toegevoegd als nieuw patroon-rij (B125) en als
aanvulling op de Plan/Step-klasserijen (B002, B003).

---

## 5. Verhouding tot de modelleringsregels in `CLAUDE.md`

*Betreft de tabbladen **Regels**, **Keuzes** en **Actiepunten**.*

De Regels-tab (RG01–RG05) dekt een deelverzameling van wat inmiddels in `CLAUDE.md` §7 staat:

| Excel-regel | Komt overeen met CLAUDE.md |
|---|---|
| RG01 Planning ≠ Execution | — (geen expliciete R-regel, wel impliciet in de laag-scheiding) |
| RG02 FOI enkelvoudig | — |
| RG03 Pragmatisch modelleren | — |
| RG04 Scheiding lifecycle-lagen | R4 (wanneer drielaags) |
| RG05 Actuele 2023-terminologie | (toegepast, geen genummerde regel) |

Regels **R5–R13** uit `CLAUDE.md` — `hasInput` vs. `prov:used`, ML-model als artefact,
`SpatialSample`+GeoSPARQL, `time:Interval` voor periode-observaties, afgeleide/geaggregeerde
observaties via `hasInputValue` (niet als `hasMember`) — hebben **geen tegenhanger** in de
Excel-tabbladen Regels/Keuzes/Begrippen v2. Dat is geen fout, maar wijst erop dat dit project
(via de voorbeelden `verkeersmetingen`, `paleo`, `erosiepoel`, …) inmiddels verder staat dan wat
Digitaal Vlaanderen in dit bestand had vastgelegd. Omgekeerd bevat het Excel-bestand (Keuzes K01,
K06–K08; Actiepunt A01 I-ADOPT-afstemming) een aantal open vragen die nog niet in `CLAUDE.md`
beantwoord zijn — met name de I-ADOPT-alignment (A01) en de kardinaliteit van
`hasFeatureOfInterest` (A02, zie 3.3 hierboven) zijn relevant voor dit project en verdienen een
plek in `CLAUDE.md` zodra ze beslist zijn.

---

## 6. Samenvatting en aanbevelingen

| # | Aanbeveling | Tabblad(en) |
|---|---|---|
| 1 | **Corrigeer de `actsOn`/`actsOnProperty`-verwarring** (§3.1) vóór dit blad als referentie dient voor nieuwe voorbeelden — dit is de enige harde fout en ze is er al twee versies lang. | Begrippen v2 (B063–B065) + Begrippen v1 (76–78) |
| 2 | **Schrap `sosa:Asset` als klasse** (§3.2) — rij volledig verwijderd (niet enkel geannoteerd), en de foutieve Range "Asset" op `deployedAsset` (B026) gecorrigeerd naar de werkelijke unie Platform/System. | Begrippen v2 (B043 verwijderd, B026 gecorrigeerd) |
| 3 | **Voeg `sosa:hasInput` toe** naast `hasInputValue`, in lijn met R5. | Begrippen v2 (ontbreekt naast B053) |
| 4 | **Werk rij B080 (`featureHasUltimateSample`) af** — de gegevens staan al volledig in het gearchiveerde blad en kunnen 1-op-1 overgenomen worden. | Begrippen v2 (B080) ← over te nemen uit Begrippen v1 (rij 92) |
| 5 | **Volg actiepunten A01 (I-ADOPT) en A02 (FOI-kardinaliteit) op** en neem de uitkomst op in `CLAUDE.md` §7. | Actiepunten (A01, A02) + Regels (RG02) |
| 6 | Herbevestig bij Digitaal Vlaanderen welke kardinaliteit voor `hasFeatureOfInterest` bedoeld is ("Exact 1" vs. "minstens 1"). | Begrippen v2 (B051, B056) + Regels (RG02) |
| 7 | **Corrigeer `ssn:` → `sosa:`** voor `Stimulus`/`detects`/`isProxyFor`/`wasOriginatedBy` (§4.1). | Begrippen v2 (B032, B040–B042) + Begrippen v1 |
| 8 | **Vul `sosa:Property`, `hasProcedure`/`isProcedureFor`, `hasOutput`/`outputFor` en de p-plan-relaties (`isStepOfPlan` e.a.) aan** (§4.2) — actief gebruikt in datavoorbeelden, nergens gedefinieerd. | Begrippen v2 (ontbreekt) |
| 9 | **Herzie afzonderlijk** de `.ttl`-datavoorbeelden die `ssn:Stimulus`/`ssn:wasOriginatedBy`/`ssn:isProxyFor` gebruiken (§4.1) — buiten scope van deze Excel-correctie, apart traject via `CLAUDE.md` §8. | `Nigella-Lawson-Brownies-simple.ttl`, `EnergieManagementSystem/*_herzien.ttl` |
| 10 | **Documenteer de p-plan/sosa:Procedure-brug** (`ontologies/pplan-sosa.ttl`, §4.3) — relevant voor Keuze K06. | Begrippen v2 (B002, B003, B125) |

Alle 10 punten hierboven zijn al doorgevoerd in `resources/Sosa mapping (gecorrigeerd).xlsx`
(tabblad Wijzigingslog), met uitzondering van punt 9, dat bewust buiten de Excel-correctie valt.

Voor het overige is de inhoud **inhoudelijk betrouwbaar**: op tabblad Begrippen v2 komt de
overgrote meerderheid van de oorspronkelijke ~100 begrippen, hun domains/ranges en inverse
relaties letterlijk overeen met beide geladen SSN/SOSA-2023-ontologiebestanden. De overige
tabbladen (Context toelichting, Keuzes, Beslisboom, Receptenboek) bevatten geen
ontologie-technische beweringen en zijn dus niet aan deze juistheidscontrole onderworpen — die
zijn eerder proces-/afsprakendocumenten, samengevat in §2 en §5.
