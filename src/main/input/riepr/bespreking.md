# Bespreking — RIE-IEPR, integraal milieujaarverslag 2021 van AGC Glass Mol

## 1. Wat stelt dit voorbeeld voor?

RIE-IEPR is de databank van het Departement Omgeving voor de rapportering over industriële
emissies (*Register Industriële Emissies — Integrated Environmental Permit Register*), met onder
meer het integraal milieujaarverslag (IMJV). Per exploitatie beschrijft ze de processen, de
installaties en punten die ze uitvoeren, en de waarden die de exploitant per rapporteringsjaar
aangeeft. Dit voorbeeld is een herziene subset van de export voor AGC Glass Europe, vestiging Mol
(exploitatie `https://data.imjv.omgeving.vlaanderen.be/id/exploitatie/01787986000160`), jaar 2021:
een procesketen naar de lucht (etslijn 2, gaswasser, emissiepunt 13005) en een naar het water
(vlakglas, lozingspunt LP01 2400006, met jaardebiet, concentratie en jaarvracht zink). De
ontologie `riepr.ttl` is mee herzien; de verbeterpunten staan in de README.

## 2. Kleurlegenda

| Kleur | SOSA-concept | Betekenis in het domein |
|---|---|---|
| Blauw (#60c4e4) | Platform / System / Deployment, Agent | exploitatielocatie, installaties, emissie-, lozings- en meetpunten, exploitatie, exploitant |
| Paars (#7f59ae) | `p-plan:Plan` / `p-plan:Step` | het proces 2021 en zijn stappen |
| Lichtpaars (#c6a0f5) | `sosa:ObservingProcedure` | de vrachtberekening |
| Oranje-rood (#fe7130) | `p-plan:Variable`, Property | procesvariabelen (rookgas, proceswater, afvalwater) |
| Roze (#e54b89) | Observation | aangegeven en berekende waarden |
| Oranje (#f8b622) | Result / `time:Interval` / Entity | resultaten, het jaar 2021, de lozing |

## 3. Infrastructuur (blauwe nodes)

| Node | Klassen | Waarom |
|---|---|---|
| `exploitant/0413638187` | `riepr:Exploitant`, `prov:Agent` | de exploitant als rol in RIE-IEPR; `prov:hadPrimarySource` naar de onderneming in de VKBO (`https://data.vlaanderen.be/id/onderneming/0413638187`, `org:Organization`) |
| `exploitatie/01787986000160` | `riepr:Exploitatielocatie`, `sosa:Platform` | de vestiging: de plaats die de systemen herbergt (R1), met een geometrie en een adres |
| `exploitatie/01787986000160/jaar/2021` | `riepr:Exploitatie`, `sosa:Deployment` | de inzet van de systemen op de locatie in rapporteringsjaar 2021 |
| `activiteit/19105`, `activiteit/323` | `riepr:Installatie`, `sosa:System` | productie-installaties (etslijn 2, vlakglas) |
| `zuiveringsapparaat/13179` | `riepr:Installatie`, `sosa:System` | de gaswasser, `dct:type installatie-type/luchtzuivering` |
| `emissiepunt/…/13005/jaar/2021` | `riepr:Emissiepunt`, `sosa:System`, `sosa:FeatureOfInterest` | het emissiepunt naar de lucht; ook studieobject van de observaties van zijn diameter en hoogte |
| `lozingspunt/…/2400006/jaar/2021` | `riepr:Emissiepunt`, `sosa:System` | lozingspunt LP01, `dct:type emissiepunt-type/lozingspunt` |
| `meetpunt/…/13005/…`, `meetpunt/…/2400006/…` | `riepr:Meetpunt`, `sosa:System` | de meetpunten bij het emissie- en het lozingspunt |

**Dubbele typering.** Elke RIE-IEPR-klasse krijgt ook haar SOSA-superklasse (`sosa:System`,
`sosa:Platform`, `sosa:Deployment`), zodat de data ook zonder de ontologie leesbaar blijft
(*Constrain your own subclasses*, `linked-data.md`). Het emissiepunt 13005 is daarnaast
`sosa:FeatureOfInterest`: een systeem kan zelf studieobject zijn.

**Hiërarchie.** De exploitatielocatie `sosa:hosts` de installaties en punten (en omgekeerd
`sosa:isHostedBy`). `sosa:hasSubSystem` volgt de bron: installatie → emissie- of lozingspunt →
meetpunt, en het emissiepunt 13005 bevat de gaswasser.
<!-- TODO: is de gaswasser 13179 een onderdeel van het emissiepunt 13005 (zoals de bron zegt), of van de installatie etslijn 2? De stroom rookgas → gaswasser → emissiepunt staat in het plan; hasSubSystem beschrijft de fysieke samenstelling. -->

**Typering uit de IRI.** De bron typeerde emissiepunten niet; `emissiepunt-type/emissiepunt_lucht`
en `emissiepunt-type/lozingspunt` zijn afgeleid uit het pad van de IRI (`/emissiepunt/`,
`/lozingspunt/`), `installatie-type/luchtzuivering` uit `riepr:ZuiveringsApparaat` en het label
*gaswasser*.

## 4. Observatie/Actuatie-structuur (roze nodes)

| IRI | observedProperty | usedProcedure | hasResult | hasFeatureOfInterest |
|---|---|---|---|---|
| `lozing/.well-known/genid/…/2400006/2021/debiet/bf7bed…` | `PAS_1838` debiet | `concept/debietmeting` | 336 735 m³/jaar (`E_50`) | lozing 2400006, 2021 |
| `observatie/…/2400006/…/HCHKCACWOHOZIP-UHFFFAOYSA-N/2021/concentratie` | `PAS_861` Zn t massaconcentratie | `concept/meetgegevens` | 0,00474 mg/L (`E_1`) | lozing 2400006, 2021 |
| `observatie/…/2400006/…/HCHKCACWOHOZIP-UHFFFAOYSA-N/2021` | `PAS_863` Zn t vracht per tijd | `concept/vrachtberekening` | 1,59612 kg/jaar (`E_12`) | lozing 2400006, 2021 |
| `emissiepunt/…/13005/jaar/2021/imjv#diameter` | `emissiepunt-eigenschappen/diameter` | — | 0,22 m (`E_59`) | emissiepunt 13005 |
| `emissiepunt/…/13005/jaar/2021/imjv#hoogte` | `emissiepunt-eigenschappen/hoogte` | — | 6,5 m (`E_59`) | emissiepunt 13005 |

De jaarvracht is een **afgeleide observatie** (R7, R13): `sosa:hasInputValue` naar de resultaten
van de concentratie en het jaardebiet, `sosa:relatedObservation` naar die twee observaties, en alle
verplichte eigenschappen expliciet.

Er is **geen `sosa:ObservationCollection`**. Het profiel eist het studieobject op elke
`riepr:Observatie` (minimum 1), dus een verzameling zou het niet weghalen; de observaties van de
lozing delen het jaar en de resultaattijd, maar verschillen in procedure; en de vracht mag geen
lid zijn van de verzameling van haar bronnen (R13). Het profiel kent wel
`riepr:ObservatieVerzameling`; voor een volledige aangifte per lozing is ze de plaats voor de
gedeelde metadata.

## 5. Procedure en Property

**Procedures van het plan** (`riepr:Proces`, via `dct:type`):

| Proces | dct:type | Uitgevoerd door (`sosa:implementedBy`) |
|---|---|---|
| `proces:…_activiteit_19105` | `riepr:verwerkingProcedure` | `activiteit/19105` |
| `proces:…_zuivering_13179` | `riepr:verwerkingProcedure` | `zuiveringsapparaat/13179` |
| `proces:…_uitstoot_13005` | `riepr:emissieProcedure` | `emissiepunt/…/13005/jaar/2021` |
| `proces:…_activiteit_323` | `riepr:verwerkingProcedure` | `activiteit/323` |
| `proces:…_lozing_2400006` | `riepr:emissieProcedure` | `lozingspunt/…/2400006/jaar/2021` |

De axioma's in de ontologie verbinden het type met de klasse van het systeem: een
verwerkingsprocedure wordt uitgevoerd door een installatie, een emissieprocedure door een
emissiepunt.

**Observatieprocedures:** `concept/debietmeting` en `concept/meetgegevens` (uit de bron) voor de
aangegeven waarden; `concept/vrachtberekening` voor de jaarvracht, met `sosa:hasInput` de
concentratie (`PAS_861`) en het debiet (`PAS_1838`), en `dct:type
operationeel-bepalingsmethode/berekend` uit de RIE-IEPR-codelijst.
<!-- TODO: horen meetgegevens en debietmeting bij de bepalingsmethode "gemeten" van de codelijst, en moet usedProcedure rechtstreeks naar de codelijst wijzen? -->

**Properties:**

| Property | Betekenis |
|---|---|
| `csor-parameteraspect:PAS_1838` | Q (standaard in water): debiet |
| `csor-parameteraspect:PAS_861` | Zn t (totaal in water): massaconcentratie |
| `csor-parameteraspect:PAS_863` | Zn t (totaal in water): vracht per tijd |
| `emissiepunt-eigenschappen/diameter` | diameter van de opening van het emissiepunt naar de lucht |
| `emissiepunt-eigenschappen/hoogte` | hoogte van het emissiepunt boven het maaiveld |

<!-- TODO: bedoelt IMJV met "Zink" het totaalgehalte (Zn t, PAS_861/863) of het gehalte zonder fractie (Zn, PAS_857/858)? De afvalwaterconcentraties in ../waterkwaliteit/ gebruiken PAS_861. -->

## 6. Modelleer-keuzes toegelicht

**Waarom drielaags?**
Verworpen alternatief: plat, met enkel de observaties. Gekozen aanpak: plan, inzet en uitvoering.
Motivatie: RIE-IEPR is opgebouwd als procesketen (activiteit → zuivering → uitstoot of lozing),
en de vraag is net welke emissie bij welk proces en welke installatie hoort (R4 b en c).

**Waarom stappen in volgorde in plaats van geneste stappen?**
Verworpen alternatief: zoals de bron, zuivering `isStepOfPlan` uitstoot `isStepOfPlan` activiteit.
Gekozen aanpak: alle stappen zijn stap van het plan 2021, geordend met `p-plan:isPrecededBy`, met
een eigen outputvariabele per stap. Motivatie: in P-PLAN maakt `isStepOfPlan` een stap lid van
een plan; een stroom van stoffen loopt via `hasOutputVar`/`hasInputVar`. Nesting vraagt deelplannen
(`p-plan:MultiStep`, `isDecomposedAsPlan`), wat de bron niet bedoelde.

**Waarom `prov:hadPlan` voor de exploitatie?**
Verworpen alternatief: `exploitatie sosa:implements proces` (de bron). Gekozen aanpak:
`prov:qualifiedAssociation [ prov:agent exploitant ; prov:hadPlan proces ]`. Motivatie: in
SSN/SOSA 2023 is `sosa:Deployment` een `prov:Activity`; `sosa:implements` gaat van een systeem
naar een procedure. PROV-O verbindt een activiteit met het plan dat een agent volgt via
`prov:hadPlan` (PROV-O §3.3, *Qualified terms*).

**Waarom de lozing als studieobject?**
Verworpen alternatief: het lozingspunt als studieobject. Gekozen aanpak: `riepr:Emissie` (een
`prov:Entity`), zoals in `../waterkwaliteit/` (patroon *Emissie als studieobject*). Motivatie: de
vraag gaat over wat geloosd werd, niet over de toestand van het punt; het punt is een systeem. De
lozing is aan het proces gekoppeld met `prov:wasDerivedFrom` naar de stap (wat het profiel eist)
en met `p-plan:correspondsToVariable` naar de outputvariabele van die stap.

`prov:wasDerivedFrom` naar het plan is een korte weg, geen nette afleidingsketen: de lozing is
niet uit een beschrijving afgeleid, maar door een activiteit gegenereerd. Het is niet fout, want
een `riepr:Proces` is een `p-plan:Plan` en dus een `prov:Entity`. De preciezere vorm is een
uitvoering van de stap (`p-plan:Activity`, `p-plan:correspondsToStep`) met
`prov:wasGeneratedBy`; de bron levert die activiteiten niet.

De lozing is per jaar een eigen resource (`lozing/…/2400006/2021`), terwijl het patroon een
tijdloze emissie voorstelt met de periode op de observatie. De bron volgt de IRI's van IMJV;
`../waterkwaliteit/` gebruikt een tijdloze `lozing-2400006`.
<!-- TODO: één tijdloze lozing per lozingspunt, of één per jaar? Afstemmen met waterkwaliteit (beslisdocument C4). -->

**Waarom de jaarvracht als afgeleide observatie?**
Verworpen alternatief: een gewone observatie met de procedure `meetgegevens` (de bron). Gekozen
aanpak: afgeleid (R7, R13). Motivatie: de vracht is concentratie × jaardebiet (README, punt 9).
Bij barium is de concentratie afgerond uit de vracht, wat erop wijst dat de richting van de
berekening per stof kan verschillen; zie de TODO in de README.

**Waarom kenmerken van punten als observaties?**
Verworpen alternatief: `riepr:Systeemeigenschap` (een `sosa:Property` met `rdfs:value` en
`qudt:hasUnit` rechtstreeks op het systeem). Gekozen aanpak: een observatie per kenmerk en per
rapporteringsjaar, met het punt als studieobject. Motivatie: de waarde is een aangifte voor een
jaar, en kan van jaar tot jaar veranderen (een hogere schouw); de observatie houdt de tijd en de
herkomst bij. Een systeemeigenschap past bij een vast gegeven uit een datasheet.

**Waarom geen sensor?**
De bron gaf elke observatie `sosa:madeBySensor agent:labo_mens_sensor_x`, een plaatshouder. Wie
de waarde bepaalde (de exploitant, een erkend labo, een meettoestel) staat niet in de export. De
R2-waarschuwing *madeBySensor strongly recommended* blijft daarom op de vijf observaties staan, en
*usedProcedure strongly recommended* op de twee kenmerken van het emissiepunt: de bron geeft daar
geen bepalingsmethode.
<!-- TODO: welk gegeven in IMJV zegt wie mat (labo, exploitant)? Dan kan madeBySensor naar een sosa:Sensor wijzen. -->

**Eenheden uit CSOR (R3).** Het register van het project. De CSOR-eenheden zijn in de data ook
`qudt:Unit`. Hun QUDT-mapping staat in CSOR, niet in de data:

| CSOR | Label | QUDT (`skos:exactMatch`) |
|---|---|---|
| `csor-eenheid:E_1` | milligram per liter | `unit:MilliGM-PER-L` |
| `csor-eenheid:E_12` | kilogram per jaar | `unit:KiloGM-PER-YR` |
| `csor-eenheid:E_50` | kubieke meter per jaar | `unit:M3-PER-YR` |
| `csor-eenheid:E_59` | meter | `unit:M` |

**Registers en codelijsten.** Eigenschappen van stoffen komen uit CSOR (parameteraspecten), zoals
in `../waterkwaliteit/`; statussen, installatie- en emissiepunttypes, de eigenschappen van
emissiepunten en de bepalingsmethode uit de RIE-IEPR-codelijst (geladen in `src/main/resources/`).
De data typeert de CSOR-parameteraspecten en de twee eigenschappen van emissiepunten als
`sosa:Property`, omdat CSOR niet geladen is en de codelijst ze enkel `skos:Concept` maakt.

**Waarom een eigen exploitant?**
Verworpen alternatief: de onderneming uit de VKBO zelf als `riepr:Exploitant` (de bron). Gekozen
aanpak: `exploitant/0413638187` met `prov:hadPrimarySource` naar de onderneming. Motivatie: het
profiel eist die bron, en de exploitant is een rol in RIE-IEPR met eigen gegevens (datums), die
niet in de namespace van de VKBO horen.

**Waarom de ontologie aanpassen?** Zonder die aanpassing eisen de shapes uit `riepr.ttl` termen
die niet bestaan (`ssn:deployedOnPlatform`, …). Elke wijziging staat in de README (O1–O12). Eén
ervan versoepelt een eis van het profiel (O8, `:inGebruikVanaf`), omdat de export het gegeven
niet bevat.

**Recordmetadata (R16).** De observaties dragen `dct:created` (eis van het profiel): oplossing A,
zonder PROV-recordeigenschappen. `qb:dataSet` is weggelaten. De systemen dragen
`prov:wasRevisionOf` naar hun versieloze IRI; systemen zijn `prov:Entity`, dus dat is consistent.

**Geen geometrie op de punten.** De bron gaf emissie- en lozingspunten een geometrie `"EMPTY"`;
er is geen locatie, dus geen geometrie (R11). Alleen de exploitatielocatie heeft een punt.

## 7. Tijdsmodellering

`sosa:phenomenonTime` is het rapporteringsjaar 2021, een `time:Interval` met begin
`2021-01-01T00:00:00+01:00` en einde `2022-01-01T00:00:00+01:00`, halfopen (R12). De bron gaf
geen tijdzone; aangenomen is `Europe/Brussels`, wintertijd (`+01:00`) op 1 januari.

`sosa:resultTime` is `2022-01-01T00:00:00+01:00`: dat is wat de bron geeft voor elke observatie,
en het lijkt een vaste waarde (het einde van het jaar) eerder dan de werkelijke datum van de
aangifte. `dct:created` (eis van het profiel) neemt dezelfde waarde over.
<!-- TODO: welke datum levert IMJV voor de indiening of goedkeuring van de aangifte? Die hoort in resultTime (en dct:created). -->

De datums op de systemen (`dct:created`, `dct:issued` 2010-01-01) komen ongewijzigd uit de bron.

## 8. Prefixen en IRI-structuur

| Prefix | Basis-IRI | Tijdelijk of persistent |
|---|---|---|
| (volledige IRI's) | `https://data.imjv.omgeving.vlaanderen.be/id/…` | persistent (IMJV), zoals ontvangen; voluit geschreven omdat de lokale namen `/` bevatten |
| `proces:` | `https://data.riepr.omgeving.vlaanderen.be/id/proces/` | persistent (RIE-IEPR) |
| `var:` | `https://data.riepr.omgeving.vlaanderen.be/id/variabele/` | persistent; twee nieuwe variabelen volgen het patroon |
| `riepr:` | `https://data.riepr.omgeving.vlaanderen.be/ns/riepr#` | ontologie |
| `riepr-status:`, `riepr-installatie:`, `riepr-emissie:`, `riepr-emissiepunt:`, `riepr-emissiepunt-eig:`, `riepr-bepalingsmethode:` | `https://data.omgeving.vlaanderen.be/id/concept/riepr/…/` | codelijst RIE-IEPR |
| `csor-eenheid:`, `csor-parameteraspect:`, `csor:` | `https://data.omgeving.vlaanderen.be/id/concept/csor/…/`, `…/ns/csor#` | register CSOR |
| `sosa:`, `prov:`, `p-plan:`, `qudt:`, `time:`, `geo:`, `locn:`, `adms:`, `org:`, `dct:`, `skos:`, `rdfs:`, `xsd:` | standaard | persistent |

Nieuwe IRI's in de herziening: `exploitant/0413638187`, `concept/vrachtberekening`,
`var:…_zuivering_13179_rookgas`, `var:…_lozing_2400006_afvalwater`. Ze volgen de patronen van de
bron en zijn voorstellen.

Op te volgen:

- **Drie domeinen.** De data gebruikt `data.imjv…` en `data.riepr…`; de `hydra:IriTemplate`s in
  de ontologie beschrijven `https://data.mjv.omgeving.vlaanderen.be/id/<klasse>/{uuid}/{issued}/{created}`.
  <!-- TODO: welk domein en welk sjabloon is het doel voor RIE-IEPR? -->
- **Versies in de IRI.** `…/jaar/2021` maakt een systeemversie per rapporteringsjaar, met
  `prov:wasRevisionOf` naar de versieloze IRI. De versieloze resources zelf staan niet in de
  export.
- **Skolem-IRI's.** De IRI van het jaardebiet bevat `.well-known/genid/…/bf7bed779f…`. Stabiel
  enkel als de hash uit vaste sleutels berekend wordt (R10).
  <!-- TODO: waaruit wordt de hash bf7bed779f6354cd1e1f2cd691b8ece3 berekend? -->
- **Hash-IRI's voor kenmerken.** `emissiepunt/…/jaar/2021/imjv#diameter` hangt de observatie aan
  het document van het emissiepunt. Dat werkt, maar een eigen pad (`observatie/…`) zoals bij de
  lozing is consistenter.

## 9. Inverse relaties

- `sosa:hosts` (locatie → systemen) en `sosa:isHostedBy` (systeem → locatie): beide, om vanuit de
  locatie en vanuit een systeem te kunnen zoeken.
- `sosa:deployedSystem` (exploitatie → systemen) en `sosa:hasDeployment` (systeem → exploitatie);
  `sosa:inDeployment` op de locatie, invers van `sosa:deployedOnPlatform`.
- `sosa:implementedBy` (stap → systeem) en `sosa:implements` (systeem → stap).
- `sosa:hasFeatureOfInterest` en `sosa:isFeatureOfInterestOf` op de lozing en het emissiepunt 13005,
  zoals de bron; het profiel vermeldt `sosa:isFeatureOfInterestOf` op `riepr:Emissie`.
- Niet opgenomen: `sosa:isResultOf` (de bron had het op de tussenknopen) en `p-plan:isOutputVarOf`.
