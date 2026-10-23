# Woordenlijst

De Nederlandse benamingen zijn de labels van de Nederlandse vertaling van SOSA, PROV-O, P-PLAN en
GeoSPARQL die in dit project geladen is
([`ssn-sosa-fullprov-o-p-plan-geosparql-dbo.ttl`](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/resources/ontologies/ssn-sosa-fullprov-o-p-plan-geosparql-dbo.ttl)).
Dezelfde woorden voor dezelfde begrippen, in elk team: dat is de helft van de samenhang.

## SOSA — klassen

| Term | Engels | Nederlands | Kern |
|---|---|---|---|
| `sosa:Execution` | Execution of a Procedure | uitvoering | abstract: waarneming, actuatie of bemonstering |
| `sosa:Observation` | Observation | waarneming | de waarde van een eigenschap bepalen (ook: observatie) |
| `sosa:Actuation` | Actuation | actuatie | de toestand van iets wijzigen |
| `sosa:Sampling` | Sampling | bemonstering | een monster nemen |
| `sosa:ObservationCollection` | Observation Collection | waarnemingscollectie | waarnemingen met gedeelde context |
| `sosa:FeatureOfInterest` | Feature Of Interest | studieobject | waarover de uitvoering gaat |
| `sosa:Sample` | Sample | monster | een representatief deel van een studieobject (ook: staal) |
| `sosa:MaterialSample` | Material Sample | materieel monster | een fysiek deel |
| `sosa:SpatialSample` | Spatial Sample | ruimtelijk monster | een plaats binnen een groter gebied |
| `sosa:Property` | Property | eigenschap | wat waargenomen of gewijzigd wordt |
| `sosa:Procedure` | Procedure | procedure | de herbruikbare werkwijze |
| `sosa:ObservingProcedure` | Observing Procedure | observerende procedure | werkwijze van een waarneming |
| `sosa:ActuatingProcedure` | Actuating Procedure | actuerende procedure | werkwijze van een actuatie |
| `sosa:SamplingProcedure` | Sampling Procedure | bemonsteringsprocedure | werkwijze van een bemonstering |
| `sosa:System` | System | systeem | abstract: sensor, actuator of bemonsteraar |
| `sosa:Sensor` | Sensor or Observer | sensor of waarnemer | wie of wat waarneemt; ook een mens of software |
| `sosa:Actuator` | Actuator | actuator | wie of wat handelt |
| `sosa:Sampler` | Sampler | bemonsteraar | wie of wat bemonstert |
| `sosa:Platform` | Platform or Host | platform of gastheer | wat systemen herbergt |
| `sosa:Deployment` | Deployment | inzet | de opstelling van systemen voor een doel |
| `sosa:Stimulus` | Stimulus | stimulus | de gebeurtenis die een sensor activeert |

## SOSA — eigenschappen

| Term | Engels | Nederlands |
|---|---|---|
| `sosa:hasFeatureOfInterest` | has feature of interest | heeft studieobject |
| `sosa:hasUltimateFeatureOfInterest` | has ultimate feature of interest | heeft uiteindelijk studieobject |
| `sosa:observedProperty` | observed property | geobserveerde eigenschap |
| `sosa:actsOnProperty` | acts on property | werkt in op eigenschap |
| `sosa:hasResult` | has result | heeft resultaat |
| `sosa:hasSimpleResult` | has simple result | heeft eenvoudig resultaat |
| `sosa:hasInput` / `sosa:hasOutput` | has input / has output | heeft input / heeft output |
| `sosa:hasInputValue` | has input value | heeft inputwaarde |
| `sosa:usedProcedure` | used procedure | gebruikte procedure |
| `sosa:madeBySensor` | made by sensor or observer | gemaakt door sensor of waarnemer |
| `sosa:madeByActuator` | made by actuator | gemaakt door actuator |
| `sosa:madeBySampler` | made by sampler | gemaakt door bemonsteraar |
| `sosa:phenomenonTime` | phenomenon time | fenomeentijd |
| `sosa:resultTime` | result time | resultaattijd |
| `sosa:startTime` / `sosa:endTime` | start time / end time | starttijd / eindtijd |
| `sosa:isSampleOf` | is sample of | is monster van |
| `sosa:hosts` | hosts | herbergt |
| `sosa:hasSubSystem` | has subsystem | heeft subsysteem |
| `sosa:implements` | implements | implementeert |
| `sosa:observes` | observes | observeert |
| `sosa:actsOn` | acts on | werkt in op |
| `sosa:relatedObservation` | related observation | gerelateerde waarneming |
| `sosa:hasMember` | has member | heeft lid van collectie |
| `sosa:wasOriginatedBy` | was originated by | werd veroorzaakt door |
| `sosa:isDetectedBy` | is detected by | wordt gedetecteerd door |
| `sosa:deployedSystem` | deployed system | ingezet systeem |
| `sosa:deployedOnPlatform` | deployed on platform | ingezet op platform |

## PROV-O

| Term | Nederlands | Kern |
|---|---|---|
| `prov:Activity` | activiteit | iets wat over een tijd plaatsvindt |
| `prov:Entity` | entiteit | een ding met vaste kenmerken; **disjunct met activiteit** |
| `prov:Agent` | agent | wie verantwoordelijk is |
| `prov:Plan` | plan | wat een agent volgt |
| `prov:Collection` | collectie | een entiteit die uit entiteiten bestaat |
| `prov:Location` | locatie | een plaats |
| `prov:SoftwareAgent` | software-agent | software als agent |
| `prov:used` | gebruikte | activiteit → entiteit die ze gebruikte |
| `prov:generated` / `prov:wasGeneratedBy` | gegenereerd / wasGegenereerdDoor | activiteit ↔ entiteit die ze voortbracht |
| `prov:wasDerivedFrom` | wasAfgeleidVan | entiteit → entiteit waarvan ze afgeleid is |
| `prov:wasAssociatedWith` | wasGeassocieerdMet | activiteit → verantwoordelijke agent |
| `prov:wasAttributedTo` | wasToegeschrevenAan | entiteit → verantwoordelijke agent |
| `prov:atLocation` | opLocatie | iets → zijn locatie |

## P-PLAN

| Term | Nederlands | Kern |
|---|---|---|
| `p-plan:Plan` | plan | een plan uit stappen en variabelen |
| `p-plan:Step` | stap | een geplande activiteit binnen een plan |
| `p-plan:MultiStep` | meerstaps-stap | een stap die zelf als plan uitgewerkt is |
| `p-plan:Variable` | variabele | input of output van een stap |
| `p-plan:Activity` / `p-plan:Entity` | activiteit / entiteit | de uitvoering van een stap / de waarde van een variabele |
| `p-plan:isStepOfPlan` | isStapVanPlan | |
| `p-plan:isPrecededBy` | wordtVoorafgegaanDoor | volgorde van stappen |
| `p-plan:isDecomposedAsPlan` | isOntledenAlsPlan | stap → het plan dat hem uitwerkt |
| `p-plan:isInputVarOf` / `p-plan:isOutputVarOf` | isInputVariabeleVan / isOutputVariabeleVan | |
| `p-plan:correspondsToStep` | komtOvereenMetStap | uitvoering → stap |
| `p-plan:correspondsToVariable` | komtOvereenMetVariabele | entiteit → variabele |

## GeoSPARQL, QUDT, OWL-Time

| Term | Nederlands | Kern |
|---|---|---|
| `geo:Feature` | feature | een ding met een plaats |
| `geo:Geometry` | geometrie | de vorm; **disjunct met feature** |
| `geo:hasGeometry` | heeft geometrie | |
| `geo:asWKT` | als WKT | de vorm als WKT-literal |
| `qudt:QuantityValue` | grootheidswaarde | getal met eenheid |
| `qudt:numericValue` | numerieke waarde | het getal |
| `qudt:hasUnit` | heeft eenheid | |
| `qudt:lowerBound` / `qudt:upperBound` | ondergrens / bovengrens | voor een interval (rapportagegrens) |
| `time:Instant` | tijdstip | |
| `time:Interval` | interval | met begin en einde |
| `time:TRS` | tijdreferentiesysteem | een tijdschaal (kalender of niet) |

## Begrippen van dit werk

| Begrip | Betekenis |
|---|---|
| **alignment** | een uitspraak (OWL-axioma, SKOS-mapping) die begrippen van twee vocabularia verbindt |
| **afgeleide waarneming** | een waarneming berekend uit de resultaten van andere ([R13](../regels/r13.md)) |
| **drielaags model** | planning, inzet en uitvoering, met P-PLAN ([R4](../regels/r04.md)) |
| **plat model** | infrastructuur, procedure en waarneming, zonder planlaag |
| **kern** | SOSA/SSN, PROV-O, QUDT, OWL-Time, GeoSPARQL, SKOS, DCTERMS, RDFS ([R17](../regels/r17.md)) |
| **register** | een beheerde codelijst van een autoriteit (CSOR, VHA, …) |
| **skolem-IRI** | een deterministische IRI in plaats van een blanco knoop ([R10](../regels/r10.md)) |
| **toetsdeel** | een klein, representatief deel van een grote dataset dat gevalideerd wordt |
| **record** | een gepubliceerd dataobject over iets, niet het ding zelf ([Waarneming of record?](../modelleren/record.md)) |
| **uiteindelijk studieobject** | wat een monster vertegenwoordigt |
