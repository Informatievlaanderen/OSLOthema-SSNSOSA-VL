# Bespreking — Verkeersmetingen (fietstelpost)

## 1. Wat stelt dit voorbeeld voor?

Dit voorbeeld modelleert de teldata van een vaste automatische fietstelpost op fietsroute F1
in Antwerpen, ter hoogte van het station Antwerpen-Centraal. De teller (meetpunt FMN-021,
naam Mercatorstraat, beheerder Provincie Antwerpen) registreert tweerichtingsverkeer van
lichte voertuigen: fietsen, steps en motorfietsen. Het voorbeeld toont zowel een dagobservatie
(absolute dagsom) als twee uurobservaties (ochtend- en avondspits via een relatieve
verkeersindex) op woensdag 29 april 2026.

## 2. Kleurlegenda

| Kleur | SOSA-concept | Domeinbetekenis |
|---|---|---|
| Blauw (#60c4e4) | Platform / Sensor / FeatureOfInterest | Meetpunt, automatische teller, fietsroute |
| Paars licht (#c6a0f5) | sosa:ObservingProcedure | Automatische telmethode |
| Oranje (#fe7130) | sosa:Property | Verkeersintensiteit en verkeersindex |
| Roze (#e54b89) | Observation / ObservationCollection | Dagsom- en uurobservaties |
| Geel (#f8b622) | time:Instant / hasSimpleResult | Tijdstippen en telresultaten |

## 3. Infrastructuur (blauwe nodes)

**`ex:meetpunt-FMN-021` — `sosa:Platform`**
De fysieke locatie (hoek Mercatorstraat/Van Den Nestlei) die de automatische teller herbergt.
Een Platform is hier de juiste klasse omdat het een vaste locatie is die sensorapparatuur
draagt (`sosa:hosts`). Het meetpunt is niet zelf een sensor: het maakt geen observaties.

**`ex:teller-FMN-021` — `sosa:Sensor`**
De automatische teller die de voertuigen detecteert en telt. Een Sensor is hier gepast omdat
het een agent is die observaties uitvoert (`sosa:madeBySensor`). De teller implementeert één
ObservingProcedure en observeert twee ObservableProperties.

**`ex:fietsroute-F1-antwerpen` — `sosa:FeatureOfInterest`**
De fietsroute zelf is het ding waarvan een eigenschap wordt bestudeerd (verkeersintensiteit).
Een FeatureOfInterest is de juiste klasse omdat het geen sensor of platform is, maar het
studieobject. Er is geen samplingketen nodig: de teller observeert de route direct.

## 4. Observatie/Actuatie-structuur (roze nodes)

De `sosa:ObservationCollection` `ex:collectie-FMN-021-20260429` groepeert de drie
observaties van 29 april 2026. Op collectieniveau staan de gedeelde metadata: sensor,
procedure en feature of interest. De individuele observaties voegen enkel hun specifieke
observedProperty, tijdstip en resultaat toe.

| IRI | observedProperty | usedProcedure | hasSimpleResult | hasFeatureOfInterest |
|---|---|---|---|---|
| `ex:obs-...-dag` | `ex:property-verkeersintensiteit` | `ex:procedure-automatisch-tellen` | `"2395"^^xsd:integer` | `ex:fietsroute-F1-antwerpen` |
| `ex:obs-...-08u` | `ex:property-verkeersindex` | `ex:procedure-automatisch-tellen` | `"0.86"^^xsd:decimal` | `ex:fietsroute-F1-antwerpen` |
| `ex:obs-...-17u` | `ex:property-verkeersindex` | `ex:procedure-automatisch-tellen` | `"0.79"^^xsd:decimal` | `ex:fietsroute-F1-antwerpen` |

## 5. Procedure en ObservableProperty

**`ex:procedure-automatisch-tellen` — `sosa:ObservingProcedure`**
Geïmplementeerd door `ex:teller-FMN-021` via `ssn:implements`.
Alle drie observaties gebruiken deze procedure via `sosa:usedProcedure`.
De procedure beschrijft de meetmethode: geautomatiseerde detectie van passerende lichte
voertuigen (inductielus of radarsensor).

**`ex:property-verkeersintensiteit` — `sosa:Property`**
Absolute dagsom van passerende voertuigen (fiets, step, motorfiets) als integer (dimensieloos
aantal). Eigenschap van `ex:fietsroute-F1-antwerpen` via `ssn:hasProperty`.

**`ex:property-verkeersindex` — `sosa:Property`**
Relatieve verkeersintensiteitsindex per uur, uitgedrukt als decimale factor t.o.v. het
historische piekuur (dinsdag 08:00 = 1,00). Dimensieloos. Eigenschap van de fietsroute.
Geobserveerd door de uurobservaties in de collectie.

## 6. Modelleer-keuzes toegelicht

### Waarom twee ObservableProperties in plaats van één?

**Verworpen alternatief:** Alle resultaten (dagsom en uurindex) modelleren als dezelfde
ObservableProperty `verkeersintensiteit`, met het eenheidsverschil uitgedrukt in `qudt:hasUnit`.

**Gekozen aanpak:** Twee aparte ObservableProperties: `verkeersintensiteit` (absoluut,
xsd:integer) en `verkeersindex` (relatief, xsd:decimal).

**Motivatie:** De dagsom en de uurindex zijn conceptueel verschillende grootheden: de ene
is een absolute telling (N voertuigen/dag), de andere is een dimensieloze ratio t.o.v. een
referentieperiode. Verschillende ObservableProperties maken SPARQL-queries duidelijker en
voorkomen dat afnemers de twee begrippen moeten onderscheiden op basis van het datatype
van `hasSimpleResult`.

### Waarom `sosa:hasSimpleResult` en niet `qudt:QuantityValue`?

**Verworpen alternatief:** Elk resultaat als een apart `qudt:QuantityValue`-object met
`qudt:numericValue` en `qudt:hasUnit`.

**Gekozen aanpak:** `sosa:hasSimpleResult` met gelitypeerde waarden (`xsd:integer`,
`xsd:decimal`).

**Motivatie:** De resultaten hoeven niet extern gerefereerd te worden als zelfstandige
entiteiten. Er is geen onzekerheid of provenance op resultaatniveau. De SOSA-spec zegt
expliciet dat `hasSimpleResult` gepast is wanneer geen apart resultaatobject nodig is
(SOSA §3.2). Mixen van de twee stijlen binnen één voorbeeld is verboden (R3 CLAUDE.md).

### Waarom `sosa:ObservationCollection`?

**Verworpen alternatief:** Losse observaties zonder collectienode.

**Gekozen aanpak:** ObservationCollection groepeert alle observaties van de meetdag.

**Motivatie:** Sensor, procedure en FeatureOfInterest zijn identiek voor alle observaties.
Door ze op collectieniveau te plaatsen wordt herhaling vermeden en is de gemeenschappelijke
context direct opvraagbaar. Dit volgt de SOSA 2023-aanbeveling voor gedeelde metadata
(§4.3 SSN/SOSA 2023 spec).

### Waarom plat model en geen drielaags architectuur?

**Verworpen alternatief:** Drielaags model met p-plan:Plan, Deployment en prov:Activity.

**Gekozen aanpak:** Plat model.

**Motivatie:** Er is één sensor op één locatie die één soort meting uitvoert. Er is geen
meerstaps-afleiding, geen herbruik van dezelfde procedure op meerdere datasets, en geen
vereiste traceerbaarheid naar een abstract plan. R4 (CLAUDE.md) reserveert het drielaags
model voor meerstaps-processen (zie EnergieManagementSystem of paleo).

## 7. Tijdsmodellering

| Observatie | phenomenonTime | resultTime | Patroon |
|---|---|---|---|
| dagsom | `time:Instant → time:inXSDDate "2026-04-29"` | `"2026-04-29T23:59:59"^^xsd:dateTime` | Standaard kalenderdatum |
| 08u uurindex | `time:Instant → time:inXSDDateTime "2026-04-29T08:00:00"` | `"2026-04-29T08:59:59"^^xsd:dateTime` | Standaard kalender met uur |
| 17u uurindex | `time:Instant → time:inXSDDateTime "2026-04-29T17:00:00"` | `"2026-04-29T17:59:59"^^xsd:dateTime` | Standaard kalender met uur |

- `sosa:phenomenonTime`: het tijdstip of de periode waarop het verkeer werd gemeten.
- `sosa:resultTime`: het tijdstip waarop het telresultaat beschikbaar werd (einde van
  het meetinterval).
- Voor de dagobservatie wordt `time:inXSDDate` gebruikt (geen uur nodig); voor de
  uurobservaties `time:inXSDDateTime` om het startuur van het meetinterval vast te leggen.

## 8. Prefixen en IRI-structuur

| Prefix | Base URI | Tijdelijk of persistent |
|---|---|---|
| `ex:` | `https://example.org/verkeersmetingen/` | Tijdelijk (illustratief) |
| `sosa:` | `http://www.w3.org/ns/sosa/` | Persistent (W3C) |
| `ssn:` | `http://www.w3.org/ns/ssn/` | Persistent (W3C) |
| `time:` | `http://www.w3.org/2006/time#` | Persistent (W3C) |
| `xsd:` | `http://www.w3.org/2001/XMLSchema#` | Persistent (W3C) |
| `rdf:` | `http://www.w3.org/1999/02/22-rdf-syntax-ns#` | Persistent (W3C) |
| `rdfs:` | `http://www.w3.org/2000/01/rdf-schema#` | Persistent (W3C) |

In een productieomgeving zouden de meetpunt-IRI's gebaseerd zijn op de gezaghebbende URI
van het telpostenbeheerssysteem (bijv. `https://data.provincie-antwerpen.be/telpost/FMN-021`).
De ObservableProperty- en Procedure-IRI's zouden idealiter verwijzen naar een gedeelde
concepten-thesaurus voor verkeer (bijv. een OSLO-verkeersvocabulaire).

<!-- TODO: Is er een officiële URI-structuur voor Vlaamse verkeerstellingsdata? Zo ja, vervang de ex:-IRI's door productie-URIs. -->

## 9. Inverse relaties

| Eigenschap | Inverse | Opgenomen op |
|---|---|---|
| `sosa:hosts` | `sosa:isHostedBy` | `ex:teller-FMN-021 sosa:isHostedBy ex:meetpunt-FMN-021` |
| `sosa:hasFeatureOfInterest` | `sosa:isFeatureOfInterestOf` | `ex:fietsroute-F1-antwerpen sosa:isFeatureOfInterestOf <collectie/obs>` |
| `sosa:hasMember` | `sosa:isMemberOf` | `ex:obs-... sosa:isMemberOf ex:collectie-...` |

De inverse `sosa:isHostedBy` ondersteunt query-paden die vertrekken vanuit de sensor
("geef het platform waarop deze sensor is gemonteerd"). De inverse
`sosa:isFeatureOfInterestOf` laat toe om vanuit de fietsroute alle observaties op te
vragen. `sosa:isMemberOf` maakt het mogelijk een observatie op te vragen en onmiddellijk
zijn collectie te kennen.
