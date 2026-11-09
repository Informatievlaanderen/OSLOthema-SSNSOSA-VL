# Bespreking — Omgevingsvergunning: de gewone procedure

## 1. Wat stelt dit voorbeeld voor?

De gewone vergunningsprocedure voor de omgevingsvergunning in eerste administratieve aanleg, voor
een project op de Vlaamse lijst (Omgevingsvergunningsdecreet, art. 18-36). Het voorbeeld legt de
procedure vast als **plan** met procedurestappen, substappen, volgorde, termijnen en rechtsgrond.
Het koppelt dat plan aan de **dienst** en het **product** uit de PDC van het Departement Omgeving
(`publicservice:D3-0098`, `output:P-0098`). Daarnaast toont het een **fictief dossier** dat de
procedure uitvoert, van de indiening op 2 februari 2026 tot de bekendmaking op 24 juni 2026.

De aanleiding is een vraag uit het beheer van codelijsten (VIZIER): hoe ga je om met een lijst van
procedurestappen waarin wettelijke stappen en andere toestanden (zoals "in voorbereiding") door
elkaar staan? Het antwoord van dit voorbeeld: procedurestappen zijn geen codelijst maar een plan.
De toestand van een dossier volgt uit de stappen die al uitgevoerd zijn.

## 2. Kleurlegenda

| Kleur | Concept | Betekenis in het domein |
|---|---|---|
| Paars (#7f59ae) | `p-plan:Plan` / `p-plan:Step` (ook `ov:Procedure` / `ov:Procedurestap`) | de procedure, haar stappen en het deelplan |
| Lichtpaars (#c6a0f5) | `cpsv:PublicService` | de dienst uit de PDC |
| Oranje-rood (#fe7130) | `p-plan:Variable` (ook `cv:Output`) | wat een stap nodig heeft of oplevert, met het product |
| Blauw (#60c4e4) | `sosa:System` / `sosa:Sensor` / `sosa:Actuator`, `cv:PublicOrganisation` | de actoren |
| Roze (#e54b89) | `sosa:Observation` / `sosa:Actuation` / `p-plan:Activity`, `dbo:Case` | de zaak en haar zaakhandelingen |
| Oranje (#f8b622) | `prov:Entity`, `sosa:FeatureOfInterest` | documenten, adviezen, de vergunde toestand, het project |

Het diagram heeft de drie lagen PLANNING, INFRASTRUCTUUR en EXECUTION. Op de plaats van DEPLOYMENT
staat INFRASTRUCTUUR, omdat het model geen `sosa:Deployment` heeft (§6). In EXECUTION groepeert
DERIVATION (lichtgeel, #f8e1ad) het GOVC-advies en de beslissing: de waarnemingen en actuaties die
van eerdere resultaten afgeleid zijn (R13).

## 3. Infrastructuur (blauwe nodes)

| Node | Klasse | Waarom |
|---|---|---|
| `inst:gewestelijke-omgevingsambtenaar` | `sosa:System`, `prov:Agent` | het ambt dat het dossier behandelt; handelt namens de Vlaamse Regering (`prov:actedOnBehalfOf`) |
| `inst:goa-ontvankelijkheid` | `sosa:Sensor` | deelsysteem: onderzoekt of de aanvraag ontvankelijk en volledig is (R1: een agent die waarneemt) |
| `inst:goa-beslissing` | `sosa:Actuator` | deelsysteem: beslist, en verandert zo de rechtstoestand (R1: een agent die de wereld verandert) |
| `inst:govc` | `sosa:Sensor` | geeft een geïntegreerd advies |
| `inst:adviesinstantie` | `sosa:Sensor`, `prov:Organization` | geeft een advies (fictief) |
| `inst:vlaamse-regering` | `cv:PublicOrganisation`, `prov:Organization` | bevoegde overheid voor projecten op de Vlaamse lijst (OVD art. 15) |
| `inst:rvvb` | `ov:Rechtscollege`, `cv:PublicOrganisation` | bevoegd voor het beroep |
| `inst:gemeente` | `cv:PublicOrganisation`, `prov:Organization` | stelt het openbaar onderzoek in, in opdracht van het bevoegde bestuur (OVB art. 67, §1) (fictief); geen SOSA-rol |
| `inst:aanvrager` | `prov:Organization` | dient de aanvraag in (fictief); geen SOSA-rol |

**Twee deelsystemen voor één ambt.** De omgevingsambtenaar onderzoekt (waarneming) én beslist
(actuatie). SOSA 2023 laat dat niet toe in één resource: een `sosa:Sensor` implementeert enkel
`sosa:ObservingProcedure`s en een `sosa:Actuator` enkel `sosa:ActuatingProcedure`s
(`allValuesFrom` op `sosa:implements`). De validatie gaf daarvoor twee schendingen. Het ambt is
daarom een `sosa:System` met twee deelsystemen (`sosa:hasSubSystem`), één per rol. De
uitvoeringen verwijzen naar de rol, niet naar het ambt.

## 4. Observatie/Actuatie-structuur (roze nodes)

| IRI | observedProperty / actsOnProperty | usedProcedure | hasResult | hasFeatureOfInterest |
|---|---|---|---|---|
| `exec:onderzoek-ontvankelijkheid-1` | `prop:ontvankelijk-en-volledig` | `step:onderzoek-ontvankelijkheid` | `hasSimpleResult true` | `ent:aanvraag-1` |
| `exec:advies-1` | `prop:verenigbaarheid` | `step:advies-adviesinstanties` | `ent:advies-1` (voorwaardelijk gunstig) | `obj:project-1` |
| `exec:advies-govc-1` | `prop:verenigbaarheid` | `step:advies-govc` | `ent:advies-govc-1` (voorwaardelijk gunstig) | `obj:project-1` |
| `exec:beslissing-1` | `prop:vergunde-toestand` | `step:beslissing` | `ent:vergunde-toestand-1` | `obj:project-1` |

De andere zaakhandelingen (indiening, mededeling, openbaar onderzoek, bekendmaking) zijn
`p-plan:Activity`'s zonder SOSA-rol: ze nemen niets waar en veranderen de rechtstoestand niet.

Het GOVC-advies is een **afgeleide waarneming** (R7, R13): `sosa:hasInputValue` naar het advies
(het resultaat) en de bundel bezwaren, `sosa:relatedObservation` naar de adviesobservatie. De
beslissing heeft het GOVC-advies als inputwaarde, op dezelfde manier.

De **zaak** (`exec:zaak-1`, `dbo:Case`, `prov:Activity`) is de uitvoering van het plan
(`prov:hadPlan`, `ov:procedure`) en bundelt de zaakhandelingen met `ov:zaakhandeling`. Ze is geen
`sosa:ObservationCollection`: haar leden zijn van verschillende soorten en delen geen eigenschap of
procedure. Waarom ze een activiteit is en geen "eenheid van werk" zoals in het AP Dossier, staat in
§6.

De **uitvoering van de MultiStep** (`exec:ontvankelijkheid-1`) is een `p-plan:Activity` die met
`step:ontvankelijkheid` overeenkomt en het deelplan volgt (`prov:hadPlan
plan:ontvankelijkheidsonderzoek`). Het onderzoek en de mededeling zijn haar delen (`dct:hasPart`),
zoals de substappen delen zijn van het deelplan. De m.e.r.-screening heeft geen uitvoering: er zat
geen screeningsnota bij de aanvraag.

## 5. Procedure en Property

| Procedure | Soort | Geïmplementeerd door | Gebruikt door |
|---|---|---|---|
| `plan:gewone-procedure` | `p-plan:Plan`, `sosa:Procedure`, `ov:Procedure`, `cpsv:Rule` | — (de zaak heeft het plan, `prov:hadPlan`) | `exec:zaak-1` (`ov:procedure`) |
| `step:onderzoek-ontvankelijkheid` | `sosa:ObservingProcedure` | `inst:goa-ontvankelijkheid` | `exec:onderzoek-ontvankelijkheid-1` |
| `step:advies-adviesinstanties` | `sosa:ObservingProcedure` | `inst:adviesinstantie` | `exec:advies-1` |
| `step:advies-govc` | `sosa:ObservingProcedure` | `inst:govc` | `exec:advies-govc-1` |
| `step:beslissing` | `sosa:ActuatingProcedure` | `inst:goa-beslissing` | `exec:beslissing-1` |

De overige stappen zijn enkel `p-plan:Step` (en via `pplan-sosa.ttl` een `sosa:Procedure`).

De stappen, in volgorde, met termijn en rechtsgrond:

| Stap | Voorafgegaan door | Termijn | Rechtsgrond (`dct:source`) |
|---|---|---|---|
| `step:indienen` | — | — | OVD art. 18 |
| `step:ontvankelijkheid` (MultiStep) | indienen | — | OVD art. 19-21 |
| ↳ `step:onderzoek-ontvankelijkheid` | — | — | OVD art. 19 |
| ↳ `step:mer-screening` (enkel met screeningsnota) | — | — | OVD art. 20 |
| ↳ `step:mededeling-resultaat` | onderzoek, mer-screening | 30 dagen | OVD art. 21 |
| `step:openbaar-onderzoek` | ontvankelijkheid | 30 dagen, begin binnen 10 dagen | OVD art. 23, OVB art. 16, 67 |
| `step:advies-adviesinstanties` | ontvankelijkheid | 50 dagen (afdelingen RO en Milieu: 60) | OVD art. 24-26, OVB art. 67 |
| `step:advies-govc` | openbaar onderzoek, adviezen | 90 dagen | OVD art. 25, 27, OVB art. 67 |
| `step:beslissing` | advies GOVC | 120 dagen (+60) | OVD art. 32-33 |
| `step:bekendmaking` | beslissing | aanplakking binnen 10 dagen | OVD art. 35-36, OVB art. 56, 59 |
| `step:beroep-rvvb` (Beroepsmogelijkheid) | bekendmaking | 45 dagen | OVD art. 52, 105, DBRC-decreet |

De termijnen komen uit de geconsolideerde teksten in de Vlaamse Codex (OVD en OVB, geraadpleegd
op 9 november 2026):

- **Openbaar onderzoek** (OVB art. 16, 67): het bevoegde bestuur geeft de gemeente waar het project
  ligt de opdracht het openbaar onderzoek in te stellen, op de dag van de ontvankelijk- en
  volledigverklaring. Het onderzoek duurt dertig dagen en begint binnen tien dagen na die
  verklaring. `exec:openbaar-onderzoek-1` heeft daarom `prov:wasAssociatedWith inst:gemeente`.
- **Adviezen** (OVB art. 67): met een GOVC vraagt de GOVC de adviesinstanties en het college om
  advies, binnen tien dagen na haar eigen adviesvraag. Vervaltermijn in een eerste adviesronde:
  zestig dagen voor de afdelingen RO en Milieu van het Departement Omgeving, vijftig dagen voor de
  andere adviesinstanties en het college. De dertig dagen gelden enkel voor andere adviezen
  (bv. een tweede adviesronde). De GOVC bezorgt haar geïntegreerd advies binnen negentig dagen.
  `ov:termijn` van `step:advies-adviesinstanties` geeft de vijftig dagen van de meeste
  adviesinstanties; de zestig dagen staan in het commentaar.
- **Bekendmaking** (OVB art. 56, 59, 60, 63): aanplakking, publicatie op de website van de gemeente
  en terinzagelegging, elk uiterlijk tien dagen na de beslissing (of na de ontvangst ervan) en
  gedurende dertig dagen.
- **Beroep** (OVD art. 52, 105): administratief beroep bestaat enkel tegen beslissingen van het
  college en de deputatie. Een beslissing van de Vlaamse Regering of de gewestelijke
  omgevingsambtenaar is dus genomen in laatste administratieve aanleg en gaat rechtstreeks naar de
  RvVb. De vervaltermijn van 45 dagen staat in het OVD zelf (art. 105, §3), niet in het
  DBRC-decreet: vanaf de dag na de betekening voor wie de beslissing betekend krijgt, vanaf de dag
  na de eerste dag van de aanplakking voor de anderen. Het DBRC-decreet regelt de rechtspleging.

<!-- TODO: art. 23 en 28 OVD gelden in de Codex "tot 31/05/2029": welke wijziging treedt dan in werking, en raakt ze de stappen van dit plan? -->

**Properties:**

| Property | Betekenis |
|---|---|
| `prop:ontvankelijk-en-volledig` | of een aanvraag ontvankelijk en volledig is; eigenschap van de aanvraag |
| `prop:verenigbaarheid` | of het project verenigbaar is met de regelgeving en de goede ruimtelijke ordening, volgens wie adviseert |
| `prop:vergunde-toestand` | de rechten en plichten die op het project van toepassing zijn (AP: Vergunde Toestand) |

## 6. Modelleer-keuzes toegelicht

### Waarom procedurestappen als plan, en niet als codelijst?

**Verworpen alternatief:** een SKOS-codelijst van procedurestappen, eventueel met collecties voor
wettelijke en niet-wettelijke stappen. **Gekozen aanpak:** de procedure is een `p-plan:Plan`, elke
stap een `p-plan:Step`. **Motivering:** een stap heeft regels van zichzelf (volgorde, termijn,
rechtsgrond, in- en uitvoer, bevoegde overheid). Volgens R18 maakt dat haar tot een resource met
eigenschappen, niet tot een concept dat enkel benoemt. Het AP Omgevingsvergunning maakt dezelfde
keuze: Procedure en Procedurestap zijn klassen. Een keuzelijst voor een applicatie blijft mogelijk
door de stappen van een plan op te vragen, of door ze daarnaast als `skos:Concept` te publiceren.

### Waarom één IRI voor procedure, plan, SOSA-procedure en regel?

**Verworpen alternatief:** vier resources (een `ov:Procedure`, een `p-plan:Plan`, een
`cpsv:Rule`-document, een `sosa:Procedure`) met verwijzingen ertussen. **Gekozen aanpak:**
`plan:gewone-procedure` is alle vier. **Motivering:** het is één ding, door vier modellen
beschreven. `p-plan:Plan ⊂ sosa:Procedure ⊂ prov:Plan` (pplan-sosa, sosa-prov). `ov:Procedure` en
`cpsv:Rule` hebben geen axioma's die botsen. Eén kanttekening: CPSV-AP noemt een Rule een
FRBR-expressie, een document. Een plan is abstracter. Wie dat onderscheid strikt wil houden, maakt
een apart document met `cpsv:follows` en laat het naar het plan verwijzen; CPSV-AP heeft daar
geen eigenschap voor.

### Waarom de rechtsgrond per stap in `dct:source`?

**Verworpen alternatief:** `ov:rechtsgrond` op elke stap. **Gekozen aanpak:** `ov:rechtsgrond` en
`cpsv:implements` op de procedure, `dct:source` naar het artikel op elke stap. **Motivering:**
`ov:rechtsgrond` heeft als domein `ov:Procedure`. Op een stap zou de inferentie de stap een
Procedure maken. `dct:source` ("a related resource from which the described resource is derived")
heeft geen domein. Dit is verbeterpunt 1 voor het AP (README).

### Waarom substappen als `p-plan:MultiStep`?

**Verworpen alternatief:** substappen als gewone stappen van het hoofdplan, of een eigen eigenschap
"heeft substap". **Gekozen aanpak:** `step:ontvankelijkheid` is een `p-plan:MultiStep` met een
deelplan (`p-plan:isDecomposedAsPlan`). **Motivering:** zo blijft het hoofdplan leesbaar, en het
deelplan kan in een andere procedure (de vereenvoudigde) hergebruikt worden. Een `p-plan:MultiStep`
is volgens P-PLAN zowel `p-plan:Step` als `p-plan:Plan`; beide types staan expliciet in de data
voor SHACL-engines zonder klassehiërarchie. In het dossier krijgt de MultiStep een eigen uitvoering,
`exec:ontvankelijkheid-1`, met `p-plan:correspondsToStep` naar de MultiStep en `prov:hadPlan` naar
het deelplan; de zaakhandelingen van de substappen zijn haar delen. Zo komt elke stap van het
hoofdplan overeen met één zaakhandeling, en hoeft `stand-van-de-zaak.rq` geen substappen te
doorzoeken.

### Waarom een advies als waarneming en de beslissing als actuatie?

**Verworpen alternatief:** alle zaakhandelingen als `p-plan:Activity`, zonder SOSA. **Gekozen
aanpak:** adviezen en het ontvankelijkheidsonderzoek zijn `sosa:Observation`, de beslissing een
`sosa:Actuation`. **Motivering:** een advies is een oordeel over een eigenschap van het project
(de verenigbaarheid) en verandert niets: een waarneming. De beslissing verandert de rechtstoestand
van het project: SOSA 2023 definieert een actuatie als het veranderen van de waarde van een
eigenschap van een feature of interest. Het resultaat is de nieuwe waarde, een
`ov:VergundeToestand`. Het besluit zelf is een document (`prov:generated`, `ov:document`). Dit
volgt het patroon van `brdr/`, waar de selectie de actuatie op de afbakening is.

### Waarom de zaakhandeling als activiteit, en het besluit als apart document?

**Verworpen alternatief:** het besluit als `ov:Vergunning` (een Juridisch Werk) en tegelijk als
resultaat van de actuatie. **Gekozen aanpak:** `exec:beslissing-1` is `ov:Vergunning`,
`ov:Zaakhandeling` en `sosa:Actuation`; het besluit is `ent:besluit-1`, een `foaf:Document`.
**Motivering:** in het AP is `ov:Vergunning` zowel Zaakhandeling (een handeling) als, via
Rechtshandeling, Juridisch Werk (een werk). PROV-O scheidt activiteit en entiteit (R16). Het AP
legt geen verband met PROV, dus de validatie meldt geen disjunctie, maar het onderscheid blijft
belangrijk. De definitie van Rechtshandeling ("handeling met beoogde rechtsgevolgen") wijst op de
handeling, dus dat is de lezing hier. Verbeterpunten 3 en 4 voor het AP (README).

### Waarom komt de zaak overeen met een plan, en is ze geen eenheid van werk?

Een uitvoering wordt getypeerd door de blauwdruk die ze uitvoert, op elk niveau:

| Uitvoering | Blauwdruk | P-PLAN / PROV | AP Omgevingsvergunning | AP Dossier |
|---|---|---|---|---|
| zaak | procedure (plan) | `prov:qualifiedAssociation` met `prov:hadPlan` | `ov:procedure` → `ov:Procedure` | `dbo:procedure`, een string |
| zaakhandeling | procedurestap | `p-plan:correspondsToStep` | `ov:procedurestap` → `ov:Procedurestap` | geen |
| document | variabele | `p-plan:correspondsToVariable` | geen | geen |

**Verworpen alternatief:** de zaak zoals het [AP Dossier](https://data.vlaanderen.be/doc/applicatieprofiel/dossier/)
haar ziet. Daar is een Zaak een *Eenheid van werk* (`dbo:UnitOfWork`), die "verschilt van
Activiteit in die zin dat het een duidelijk einde heeft en gemeten wordt". Die Activiteit is in het
AP Dossier `prov:Activity`. Een activiteit "vindt plaats tijdens" een eenheid van werk
(`dossier:vindtPlaatsTijdens`), een zaak "doorloopt" procedurestappen, en de procedure is een
string: "de naam die verwijst naar de formele definitie van een verzameling stappen".
**Gekozen aanpak:** de zaak is een `prov:Activity` met `prov:hadPlan` naar het plan, en
`ov:procedure` naar hetzelfde plan.

**Motivering.** Het criterium van het AP Dossier onderscheidt niets: ook zijn Activiteit heeft een
verplichte einddatum. Het echte onderscheid is structureel. Een eenheid van werk is het geheel
waarbinnen activiteiten plaatsvinden. Dat gaat in tegen wat een zaak moet kunnen: overeenkomen met
de blauwdruk die ze uitvoert. De enige eigenschap in de kern die een uitvoering als geheel aan een
plan bindt, is `prov:hadPlan`, en die vraagt een `prov:Activity`. P-PLAN heeft geen eigenschap van
een uitvoering naar een plan. `p-plan:Bundle` beschrijft "de herkomst van de uitvoering van een
plan", maar is een entiteit en wijst niet naar het plan. Wie de zaak geen activiteit laat zijn,
verliest dus de koppeling met de blauwdruk. Een procedure als string maakt die koppeling sowieso
onmogelijk: zonder resource zijn er geen stappen, volgorde of termijnen om mee te vergelijken.

`sosa:ExecutionCollection` lijkt een uitweg: het AP Dossier leest zich als een collectie
(`vindt plaats tijdens` als omgekeerde van `sosa:hasMember`, `behandelt` als
`sosa:hasFeatureOfInterest`, de openings- en sluitingsdatum als samenvatting van de leden). Maar een
SOSA-collectie bevat enkel `sosa:Execution`s, uitgevoerd door een systeem op een studieobject. De
indiening, het openbaar onderzoek en de bekendmaking zijn dat niet. En een `sosa:usedProcedure` op
de collectie moet volgens de samenvattingsregels gelden voor elk lid, terwijl elk lid een andere
stap uitvoert.

**Twee betekenissen van "Procedurestap".**

| | AP Omgevingsvergunning (`ov:Procedurestap`) | AP Dossier (`dossier:Procedurestap`) |
|---|---|---|
| Definitie | "een voorgeschreven handeling binnen een Procedure" | "het geheel aan werk gedaan binnen een specifiek chronologisch, logisch, organisatorisch of wettelijk bepaald onderdeel van een procedure" |
| Superklasse | geen (in de alignering `p-plan:Step`) | `dbo:UnitOfWork` |
| Eigenschappen | termijn, rechtsgrond, procedure | naam, startdatum, einddatum (verplicht) |
| Niveau | blauwdruk | uitvoering in één dossier |

Het AP Omgevingsvergunning gebruikt beide samen (`ov:dossier` heeft als bereik
`dossier:Dossier`), dus één label staat voor twee niveaus. Wat het AP Dossier een procedurestap
noemt, is in P-PLAN een activiteit die met een stap overeenkomt. Voor een stap met substappen is
dat `exec:ontvankelijkheid-1`: één activiteit die het deelplan volgt, met de handelingen van de
substappen als delen. Het AP Dossier mist daarbij de link naar de voorgeschreven stap.

**Voorstel: de blauwdruk in de kern, het domein als subklasse.** Het AP Dossier is generiek en
verwijst dus niet naar een klasse van één domein, maar naar P-PLAN:

| Laag | Blauwdruk | Uitvoering → blauwdruk |
|---|---|---|
| kern | `p-plan:Plan`, `p-plan:Step` (via pplan-sosa en sosa-prov ook `sosa:Procedure` en `prov:Plan`) | zaak: `prov:hadPlan`; handeling: `p-plan:correspondsToStep` |
| AP Dossier | bereik `p-plan:Plan` en `p-plan:Step` | Zaak → plan; Activiteit `p-plan:correspondsToStep` |
| AP Omgevingsvergunning | `ov:Procedure ⊂ p-plan:Plan`, `ov:Procedurestap ⊂ p-plan:Step` | `ov:procedure` en `ov:procedurestap` als subproperty van die van het AP Dossier |

`p-plan:Plan` en `p-plan:Step` zijn het juiste bereik. `prov:Plan` zegt niets over stappen.
`sosa:Procedure` is te ruim (ook de werkwijze van een sensor) en onderscheidt plan en stap niet.
Via pplan-sosa en sosa-prov volgen de SOSA- en PROV-klassen vanzelf. Dit zijn verbeterpunten 10 tot
12 (README).

<!-- TODO: neemt de werkgroep van het AP Dossier een eigenschap van Zaak naar p-plan:Plan op (in plaats van dbo:procedure als string), en wordt Zaak dan een prov:Activity? -->
<!-- TODO: blijft dossier:Procedurestap bestaan (dan met een link naar de voorgeschreven stap en een ander label), of wordt het een Activiteit met p-plan:correspondsToStep? -->

### Waarom het product als variabele van de procedure?

**Verworpen alternatief:** een eigen `var:vergunningsbeslissing` naast `output:P-0098`, met
`rdfs:seeAlso` ertussen. **Gekozen aanpak:** `output:P-0098` is `cv:Output` én `p-plan:Variable`,
uitvoer van `step:beslissing`; het concrete besluit `p-plan:correspondsToVariable` het product.
**Motivering:** beide beschrijven hetzelfde op typeniveau: wat de dienst oplevert. Zo leidt een
pad van dienst via product en stap naar elk besluit, zonder extra koppeleigenschap. De typering
`p-plan:Variable` is een uitspraak over een resource van de PDC en hoort daar thuis (verbeterpunt
7). Hier staat ze ter illustratie.

### Hoe verbindt het voorbeeld P-PLAN met de PDC?

De PDC beschrijft de dienstverlening met CPSV-AP en P-PLAN beschrijft de procedure. Beide werken
op **typeniveau**: een dienst, een product en een stap zijn beschrijvingen van wat telkens gebeurt,
niet van één dossier. Het dossier staat op **uitvoeringsniveau**. Zes links verbinden de drie lagen:

| Van | Eigenschap | Naar | Niveau |
|---|---|---|---|
| `publicservice:D3-0098` | `cpsv:produces` | `output:P-0098` | dienst (overgenomen uit de PDC) |
| `publicservice:D3-0098` | `cpsv:follows` | `plan:gewone-procedure` | dienst (voorstel voor de PDC) |
| `publicservice:D3-0098` | `cv:hasLegalResource` | `wet:ovd` | dienst (voorstel voor de PDC) |
| `step:beslissing` | `sosa:hasOutput` | `output:P-0098` | plan |
| `output:P-0098` | `p-plan:isOutputVarOf` / `p-plan:isInputVarOf` | `step:beslissing` / `step:bekendmaking`, `step:beroep-rvvb` | plan |
| `ent:besluit-1` | `p-plan:correspondsToVariable` | `output:P-0098` | dossier |

**Twee bruggen.** De eerste brug is één resource met twee rollen. `output:P-0098` is in CPSV-AP
het product van de dienst (`cv:Output`) en in P-PLAN de uitvoervariabele van de beslissing
(`p-plan:Variable`). Dat werkt omdat beide klassen op hetzelfde niveau staan. Een `cv:Output`
zegt wat een dienst oplevert, niet welk exemplaar. Een `p-plan:Variable` is de plaatshouder voor
wat een stap oplevert, die elke uitvoering met een eigen entiteit invult. De tweede brug is
`cpsv:follows`. Daarmee volgt de dienst de procedure als regel (`cpsv:Rule`), en die regel is
dezelfde IRI als het plan (zie *Waarom één IRI*). `cv:hasLegalResource` hoort niet bij een brug:
het geeft de rechtsgrond van de dienst als geheel, terwijl de stappen elk hun eigen artikel krijgen
(`dct:source`).

**Van het dossier naar de PDC.** P-PLAN verbindt de uitvoering met het plan:
`p-plan:correspondsToStep` voor een handeling en `p-plan:correspondsToVariable` voor een entiteit.
Via de bruggen bereikt een dossier zo de dienst langs twee wegen:

```sparql
# langs het product: van het besluit naar de dienst die het product levert
ent:besluit-1 p-plan:correspondsToVariable ?product .
?dienst cpsv:produces ?product .

# langs de procedure: van de zaak naar de dienst die de procedure volgt
exec:zaak-1 ov:procedure ?plan .
?dienst cpsv:follows ?plan .
```

Beide wegen geven hier `publicservice:D3-0098`. Ze zeggen niet hetzelfde. De weg langs het product
vertrekt pas bij een besluit, dus niet bij een zaak die nog loopt of zonder beslissing eindigt. De
weg langs de procedure werkt vanaf de indiening, maar enkel zolang één dienst de procedure volgt.

**Samenhang tussen dienst en plan.** De dienst levert een product (`cpsv:produces`) en volgt een
plan (`cpsv:follows`). Dat product moet dan ook de uitvoer van een stap van dat plan zijn
(`sosa:hasOutput`). Geen van beide vocabularia legt die samenhang op. Een SPARQL-controle kan het
wel:

```sparql
?dienst cpsv:produces ?product ; cpsv:follows ?plan .
FILTER NOT EXISTS { ?stap p-plan:isStepOfPlan ?plan ; sosa:hasOutput ?product }
```

In dit voorbeeld geeft die controle geen resultaat: het product is uitvoer van `step:beslissing`.

**De invoerkant is niet gekoppeld.** De aanvraag is een variabele van het plan (`var:aanvraag`),
en het aanvraagdossier zegt `p-plan:correspondsToVariable` die variabele. CPSV-AP kan de invoer
van een dienst beschrijven als `cv:hasInput`, een `cv:Evidence`. De PDC doet dat nu niet. Zou ze
het wel doen, dan kan `var:aanvraag` dezelfde dubbele rol krijgen als het product: `cv:Evidence` en
`p-plan:Variable`. Dan is de dienst langs zijn invoer en zijn uitvoer aan het plan gekoppeld.

**Wat ontbreekt: de link van een zaak naar de dienst.** Beide wegen hierboven zijn omwegen. De
enige rechtstreekse link van het dossier naar de PDC loopt van het besluit naar het product. Volgen
meerdere diensten dezelfde procedure, dan valt voor een zaak zonder besluit niet meer af te leiden
welke dienst ze levert. Verworpen: `dct:relation` (geen betekenis), een gekwalificeerde associatie met de dienst
als `prov:hadPlan` (een dienst is geen plan), en `ent:besluit-1` typeren als `cv:Output` (dat
vermengt het product op typeniveau met elk exemplaar ervan). CPSV-AP en het AP hebben geen
eigenschap van een zaak naar een dienst; dit is verbeterpunt 9 (README).

<!-- TODO: welke eigenschap van Zaak naar cpsv:PublicService wil de werkgroep van het AP Omgevingsvergunning, en beschrijft de PDC het aanvraagdossier als cv:hasInput (cv:Evidence) van de dienst? -->

### Waarom geen deploymentlaag?

**Verworpen alternatief:** de zaak als `sosa:Deployment` van de actoren. **Gekozen aanpak:** geen
deployment; de zaak is een `prov:Activity` met `prov:hadPlan` naar de procedure. **Motivering:**
een deployment zet systemen in voor een doel. Hier wijst de regelgeving de actoren aan, en een zaak
brengt geen systemen in stelling. De zaak draagt het plan, zoals de inzet in `brdr/` en de
exploitatie in `riepr/` dat doen.

### Waarom geen status "in voorbereiding"?

**Verworpen alternatief:** een codelijst van dossierstatussen naast of in de procedurestappen.
**Gekozen aanpak:** geen status in de data; [`stand-van-de-zaak.rq`](stand-van-de-zaak.rq) leidt
af welke stappen aan de beurt zijn. **Motivering:** een procedurestap is volgens het AP een
"voorgeschreven handeling". "In voorbereiding" is geen handeling maar een toestand van het dossier.
Een afgeleide stand kan niet in tegenspraak zijn met de zaakhandelingen; een bijgehouden status
wel. Heeft een applicatie toch een weergavestatus nodig, dan hoort die in een eigen lijst van
statussen, los van de procedure.

### Waarom een eigen codelijst voor de strekking van een advies?

**Gekozen aanpak:** `cl:adviesstrekking` (gunstig, voorwaardelijk gunstig, ongunstig), met de
strekking als `rdf:value` van het adviesdocument, zoals de evaluatieklasse in `brdr/`.
**Motivering:** geen bestaande lijst gevonden.

<!-- TODO: heeft het omgevingsloket een codelijst voor de strekking van een advies (en voor de soort beslissing)? Dan vervangt die cl:adviesstrekking. -->

### Waarom deze vocabularia?

**AP Omgevingsvergunning (`ov:`).** Kandidaten voor procedure en procedurestap: P-PLAN (in de
kern), CPSV-AP (`cpsv:Rule`), CMMN (CasePlanModel, PlanItem) en het AP Omgevingsvergunning.
Doorslaggevend: het AP is de Vlaamse standaard voor dit domein (criterium 13) met de begrippen die
de vraag stelt: Procedure, Procedurestap, Beroepsmogelijkheid, Zaak, Zaakhandeling, Vergunde
Toestand (7). P-PLAN blijft nodig voor wat het AP niet uitdrukt. CMMN heeft geen RDF-vocabularium
(1). Zwakke punten van het AP: geen versie (`dc:issued "TODO"`, 3), geen alignering met PROV of
SOSA (8), en het zet een Nederlands label op `prov:atLocation`, een term van een ander vocabularium
(5). Geladen via content negotiation (1: dereferencieerbaar als Turtle).

**CPSV-AP 3.2.0 (`cpsv:`, `cv:`).** De PDC gebruikt het al (13); SEMIC publiceert het met versie
en wijzigingslog (2, 3, 11, 12). Er zijn geen domeinen en bereiken, dus geen ongewenste inferenties
(9). Het herdeclareert wel DCTERMS-termen met eigen commentaar (5), zonder axioma's.
`cpsv:follows` is de enige CPSV-AP-eigenschap van een dienst naar de regels die hij volgt.

**DBpedia (`dbo:Case`).** Gebruikt omdat het AP de Zaak zo definieert; al geladen.

**`foaf:Document`.** Het bereik van `ov:document`; het AP-vocabularium declareert de klasse, FOAF
zelf is niet geladen.

**Aligneringen.** Gezocht in `oslo-ld-kit/registers/alignments.ttl` (geen vermelding van `ov:` of
`cpsv:`), in beide vocabularia (geen verwijzing naar PROV, SOSA of P-PLAN) en in
`w3c/sdw-sosa-ssn` (geen module voor CPSV of OSLO). Geen alignering gevonden. Dit project voegt er
daarom zelf een toe, als voorstel voor het AP (volgende subsectie).

### Waarom een alignering van het AP met P-PLAN en PROV-O?

**Verworpen alternatief:** geen alignering, en in de data elke resource met zowel de AP-klasse als
de P-PLAN-, SOSA- en PROV-klasse typeren (zoals nu). **Gekozen aanpak:** een uitlijningsmodule
[`ov-pplan-prov.ttl`](../../resources/be/vlaanderen/data/ns/omgevingsvergunning/alignments/ov-pplan-prov.ttl)
in `src/main/resources/`, naast `pplan-sosa.ttl`:

| Axioma | Gevolg |
|---|---|
| `ov:Procedure ⊂ p-plan:Plan` | een procedure is ook `sosa:Procedure` (pplan-sosa) en `prov:Plan` |
| `ov:Procedurestap ⊂ p-plan:Step` | volgorde (`p-plan:isPrecededBy`) en substappen (`p-plan:MultiStep`) zonder nieuwe AP-termen; ook `ov:Beroepsmogelijkheid` is een stap |
| `ov:Zaakhandeling ⊂ prov:Activity` | een zaakhandeling is een activiteit; R16 is nu controleerbaar |
| `ov:VergundeToestand ⊂ prov:Entity` | de vergunde toestand is een entiteit, het resultaat van de actuatie |
| `ov:procedurestap ⊑ p-plan:correspondsToStep` | een zaakhandeling met een stap is een `p-plan:Activity` die met die stap overeenkomt |

**Motivering:** het AP heeft geen enkele link naar PROV, SOSA of P-PLAN (R17, criterium 8). Zonder
alignering is de koppeling enkel een afspraak in de data, en ziet de validatie niet dat een
`ov:Vergunning` die ook als `prov:Entity` gebruikt wordt, R16 schendt. Met de module meldt
`[DISJOINTNESS]` dat wel (getest). Ze lost verbeterpunt 2 (volgorde en substappen) op zonder het AP te
wijzigen. Voor `p-plan:correspondsToStep` geldt: het is functioneel, wat klopt met de definitie in
het AP ("een procedurestap" per zaakhandeling).

**Bewust niet gealigneerd:** `ov:JuridischWerk`, `ov:Rechtshandeling` en hun subklassen.
`ov:Vergunning`, `ov:Aanvraag` en `ov:InstellingBeroep` zijn in het AP zowel Zaakhandeling als, via
Rechtshandeling, Juridisch Werk. `ov:JuridischWerk ⊂ prov:Entity` zou ze inconsistent maken. Om
dezelfde reden blijft `ov:document` los van `prov:generated`: het domein `ov:Rechtshandeling` zou
dan een activiteit worden. Dat hangt af van de keuze in verbeterpunt 3. Ook `ov:procedure` (zaak
naar procedure) blijft los: de PROV-tegenhanger is een gekwalificeerde associatie met
`prov:hadPlan`, geen enkele eigenschap.

De data typeert de P-PLAN-, SOSA- en PROV-klassen nog altijd expliciet, voor SHACL-engines zonder
klassehiërarchie. Met de module zijn die types afleidbaar; de validatie van alle voorbeelden blijft
ongewijzigd foutloos.

**In het AP, niet als aparte module.** Rust het AP Dossier op P-PLAN (zie *Waarom komt de zaak
overeen met een plan*), dan hangen `ov:Procedure` en `ov:Procedurestap` daaronder als subklassen.
De axioma's horen dan in het AP Omgevingsvergunning zelf.

<!-- TODO: neemt de werkgroep van het AP Omgevingsvergunning de axioma's over, samen met ov:procedure en ov:procedurestap als subproperty van de eigenschappen van het AP Dossier? -->

### Validatie

`[VOCAB] ok`, `[DISJOINTNESS] ok`, `[SHACL] conforms` (22 van 203 shapes toegepast op 39
focusnodes). De bulkvalidatie van alle voorbeelden geeft na het laden van de twee vocabularia
en de uitlijningsmodule geen fouten.

## 7. Tijdsmodellering

- **Termijnen** zijn `time:Duration`s met `time:numericDuration` en `time:unitType time:unitDay`,
  als waarde van `ov:termijn` (bereik `time:TemporalDuration`). Het OVD telt kalenderdagen "vanaf
  de dag na" een gebeurtenis; dat staat in het commentaar van elke stap, niet in de duur.
- **Zaakhandelingen met een duur** (het openbaar onderzoek) hebben `prov:startedAtTime` en
  `prov:endedAtTime`, half-open: 5 maart 2026 00:00 tot 4 april 2026 00:00, dus dertig dagen tot en
  met 3 april. Het onderzoek begint binnen tien dagen na de ontvankelijk- en volledigverklaring van
  25 februari (OVB art. 16). De zomertijd begint op 29 maart, vandaar `+01:00` en `+02:00`.
- **De uitvoering van de MultiStep** loopt van 3 februari 2026 00:00 (de dag na de indiening, waarop
  de termijn van dertig dagen begint, OVD art. 21) tot de mededeling op 25 februari.
- **Momenten** zijn `prov:endedAtTime` (indiening, mededeling) of `sosa:resultTime` (adviezen,
  beslissing); de bekendmaking heeft enkel `prov:startedAtTime`, de eerste dag van de aanplakking.
- **Termijnen in het dossier**, uitgerekend: ontvankelijk en volledig verklaard op 25 februari
  2026, dus de beslissingstermijn van 120 dagen loopt van 26 februari tot en met 25 juni 2026. De
  beslissing op 18 juni valt erbinnen. De beroepstermijn van 45 dagen loopt van 25 juni tot en met
  8 augustus 2026.
- **Tijdzone:** het dossier is fictief; alle tijden in `Europe/Brussels`.

## 8. Prefixen en IRI-structuur

| Prefix | Basis-IRI | Tijdelijk of persistent |
|---|---|---|
| `plan:` | `https://example.org/omgevingsvergunning/plan/` | tijdelijk (voorbeeld) |
| `step:` | `https://example.org/omgevingsvergunning/step/` | tijdelijk |
| `var:` | `https://example.org/omgevingsvergunning/var/` | tijdelijk |
| `exec:` | `https://example.org/omgevingsvergunning/exec/` | tijdelijk |
| `ent:` | `https://example.org/omgevingsvergunning/ent/` | tijdelijk |
| `inst:` | `https://example.org/omgevingsvergunning/inst/` | tijdelijk |
| `prop:` | `https://example.org/omgevingsvergunning/prop/` | tijdelijk |
| `obj:` | `https://example.org/omgevingsvergunning/object/` | tijdelijk |
| `cl:` | `https://example.org/omgevingsvergunning/concept/` | tijdelijk |
| `wet:` | `https://example.org/omgevingsvergunning/wet/` | tijdelijk, zie hieronder |
| `publicservice:` | `https://data.omgeving.vlaanderen.be/id/publicservice/producten_en_diensten/` | persistent (PDC) |
| `output:` | `https://data.omgeving.vlaanderen.be/id/output/producten_en_diensten/` | persistent (PDC) |
| `pd:` | `https://data.omgeving.vlaanderen.be/id/concept/producten_en_diensten/` | persistent (PDC) |
| `ovo:` | `http://data.vlaanderen.be/id/organisatie/` | persistent (Wegwijs) |
| `ov:` | `https://data.vlaanderen.be/ns/omgevingsvergunning#` | vocabularium |
| `cpsv:`, `cv:` | `http://purl.org/vocab/cpsv#`, `http://data.europa.eu/m8g/` | vocabularium |
| `dbo:`, `foaf:` | `http://dbpedia.org/ontology/`, `http://xmlns.com/foaf/0.1/` | vocabularium |
| `sosa:`, `prov:`, `p-plan:`, `time:`, `skos:`, `dct:`, `xsd:`, `rdf:`, `rdfs:` | standaard | vocabularium |

**In productie** krijgen de procedure en haar stappen persistente IRI's in de namespace van wie
ze beheert, bijvoorbeeld `https://data.omgeving.vlaanderen.be/id/procedure/…`. De dienst, het
product, VIZIER en de dossiers verwijzen ernaar. De juridische werken krijgen een ELI.
`wet:ovd` en `wet:ovb` verwijzen al met `rdfs:seeAlso` naar een ELI van het Belgisch Staatsblad
(R10: IRI's die nog niet vaststaan).

De ELI's van het OVD (NUMAC 2014036510) en het OVB (NUMAC 2016035143) zijn nagekeken: ze geven
op Justel het decreet van 25 april 2014 en het besluit van 27 november 2015.

<!-- TODO: heeft de Vlaamse Codex (of Justel) een persistente IRI per artikel om wet:ovd-art-* en wet:ovb-art-* te vervangen? -->
<!-- TODO: wie beheert de procedures in productie (Departement Omgeving, team omgevingsloket?), en in welke namespace? -->

## 9. Inverse relaties

| Paar | Hier | Waarom |
|---|---|---|
| `dct:hasPart` (procedure → stap) ↔ `p-plan:isStepOfPlan` (stap → plan) | beide | het AP vraagt `dct:hasPart`, P-PLAN `isStepOfPlan`; zo werken queries van beide kanten |
| `ov:zaakhandeling` (zaak → handeling) ↔ `ov:zaak` (handeling → zaak) | beide | het AP heeft beide; de query voor de stand van een zaak gebruikt `ov:zaak` |
| `ov:procedurestap` ↔ `p-plan:correspondsToStep` | beide (geen inverse, wel dezelfde betekenis) | het AP en P-PLAN, elk met hun eigen term |
| `sosa:hasOutput` (stap → variabele) ↔ `p-plan:isOutputVarOf` (variabele → stap) | beide | zoals in `brdr/`: SOSA op de procedure, P-PLAN op de variabele |
| `sosa:implements` ↔ `sosa:implementedBy` | enkel `implements` | |
| `prov:generated` ↔ `prov:wasGeneratedBy` | enkel `generated` | |
| `cpsv:follows` | enkel van dienst naar procedure | CPSV-AP heeft geen inverse |
