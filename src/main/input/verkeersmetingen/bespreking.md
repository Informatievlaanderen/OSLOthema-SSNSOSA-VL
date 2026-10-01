# Bespreking — Verkeersmetingen (fietstelpost)

## 1. Wat stelt dit voorbeeld voor?

Dit voorbeeld modelleert de teldata van een vaste automatische fietstelpost op fietsroute F1
in Antwerpen, ter hoogte van het station Antwerpen-Centraal. De teller (meetpunt FMN-021,
naam Mercatorstraat, beheerder Provincie Antwerpen) registreert tweerichtingsverkeer van
lichte voertuigen: fietsen, steps en motorfietsen. Het voorbeeld toont een dagobservatie
(absolute dagsom) en 24 uurobservaties (absolute tellingen per uur, 00:00–23:00) voor
dinsdag 28 april 2026.

## 2. Kleurlegenda

| Kleur | SOSA-concept | Domeinbetekenis |
|---|---|---|
| Blauw (#60c4e4) | Platform / Sensor / FeatureOfInterest / SpatialSample | Meetpunt, automatische teller, fietsroute |
| Paars licht (#c6a0f5) | sosa:ObservingProcedure | Automatische telmethode |
| Oranje (#fe7130) | sosa:Property | Verkeersintensiteit |
| Roze (#e54b89) | Observation / ObservationCollection | Dagsom- en uurobservaties |
| Geel (#f8b622) | time:Interval / sosa:Result | Meetperiodes en telresultaten |

## 3. Infrastructuur (blauwe nodes)

**`ex:meetpunt-FMN-021` — `sosa:Platform`, `sosa:FeatureOfInterest`, `sosa:SpatialSample` (+ `sosa:Sample`)**
De fysieke locatie (hoek Mercatorstraat/Van Den Nestlei, lat 51.20910, lon 4.423123) die de
automatische teller herbergt. Drievoudige typering:
- `sosa:Platform`: het meetpunt draagt sensorapparatuur via `sosa:hosts`.
- `sosa:FeatureOfInterest`: het meetpunt is het directe studieobject van de observaties —
  de verkeersintensiteit wordt gemeten op precies dit punt.
- `sosa:SpatialSample`: het meetpunt is een ruimtelijk monster van de bredere
  `ex:fietsroute-F1-antwerpen` via `sosa:isSampleOf`. De geometrie is vastgelegd via
  `geo:hasGeometry` (GeoSPARQL WKT Point). `sosa:Sample` staat er expliciet bij: de SHACL-validatie
  gebeurt op het niet-afgeleide model en kent de superklasse anders niet.
- Het meetpunt is het resultaat (`sosa:isResultOf`) van een ruimtelijke bemonstering:
  `ex:sampling-meetpunt-FMN-021` (`sosa:Sampling`), de keuze van het meetpunt op de fietsroute
  (R8, R11). Zo is ook de fietsroute het FOI van een uitvoering, zoals SOSA vraagt.

**`ex:teller-FMN-021` — `sosa:Sensor` (+ `sosa:System`)**
De automatische teller die voertuigen detecteert en telt. Implementeert één
`sosa:ObservingProcedure` via `sosa:implements` en observeert `ex:property-verkeersintensiteit`.
`sosa:System` staat er expliciet bij, omdat een platform enkel platformen of systemen host
(`sosa:hosts`).

**`ex:fietsroute-F1-antwerpen` — `sosa:FeatureOfInterest`**
De bredere fietsroute is het ultimate FeatureOfInterest, bereikbaar via de sampling-keten
`meetpunt sosa:isSampleOf fietsroute`. Ze is het FOI van de ruimtelijke bemonstering
`ex:sampling-meetpunt-FMN-021` (`sosa:isFeatureOfInterestOf`, `sosa:hasSample`). Ze heeft `sosa:hasProperty ex:property-verkeersintensiteit`
expliciet gedeclareerd. Omdat het meetpunt een `sosa:SpatialSample` van de fietsroute is,
heeft het meetpunt die eigenschap ook — via de sampling-keten erft een monster de
eigenschappen van het bestudeerde object. In het diagram is `sosa:hasProperty` daarom
weergegeven op het meetpunt (I1), het concrete punt waar de meting plaatsvindt.

## 4. Observatie/Actuatie-structuur (roze nodes)

De `sosa:ObservationCollection` `ex:collectie-FMN-021-20260428` groepeert de **24
uurobservaties** van 28 april 2026. Op collectieniveau staan de gedeelde metadata: sensor,
procedure, feature of interest en observedProperty. De individuele uurobservaties voegen hun
specifieke tijdsinterval en resultaat toe. Ze herhalen ook het meetpunt als
`hasFeatureOfInterest`. SOSA 2023 laat dat toe (leden hebben dezelfde waarde als de collectie),
en de SHACL-validatie op het niet-afgeleide model kent geen collectie-erfenis.

| IRI | hasResult (waarde) | hasFeatureOfInterest | relatie tot collectie |
|---|---|---|---|
| `ex:obs-...-00u` | `ex:resultaat-...-00u` (15) | meetpunt | `sosa:isMemberOf` |
| `ex:obs-...-08u` | `ex:resultaat-...-08u` (291, ochtendspits) | meetpunt | `sosa:isMemberOf` |
| `ex:obs-...-17u` | `ex:resultaat-...-17u` (279, avondspits) | meetpunt | `sosa:isMemberOf` |
| `ex:obs-...-NNu` (×21) | `ex:resultaat-...-NNu` (variabel) | meetpunt | `sosa:isMemberOf` |

De **dagobservatie** `ex:obs-...-dag` is een afgeleide observatie en maakt **geen deel uit**
van de collectie. Ze is met de collectie verbonden via twee eigenschappen:

| Eigenschap | Richting | Betekenis |
|---|---|---|
| `sosa:relatedObservation` | dag → collectie | de bronobservaties: de 24 uurtellingen |
| `sosa:hasInputValue` | dag → de 24 uurresultaten | de waarden die opgeteld worden tot de dagsom (2541) |

De dagobservatie declareert `sosa:madeBySensor`, `sosa:usedProcedure`,
`sosa:hasFeatureOfInterest` en `sosa:observedProperty` expliciet op zichzelf.

## 5. Procedure en ObservableProperty

**`ex:procedure-automatisch-tellen` — `sosa:ObservingProcedure`**
Geïmplementeerd door `ex:teller-FMN-021` via `sosa:implements`.
Alle 25 observaties gebruiken deze procedure (gedeeld op collectieniveau via `sosa:usedProcedure`).
De procedure beschrijft geautomatiseerde detectie van passerende lichte voertuigen
(inductielus of radarsensor).

**`ex:property-verkeersintensiteit` — `sosa:Property`**
Absoluut aantal lichte voertuigen (fiets, step, motorfiets) dat het meetpunt passeert in de
gemeten periode. Voor uurobservaties: voertuigen/uur; voor de dagobservatie: voertuigen/dag.
Eigenschap van zowel `ex:meetpunt-FMN-021` (direct, via `sosa:hasProperty` op de
fietsroute) als bereikbaar via de sampling-keten.

## 6. Modelleer-keuzes toegelicht

### Waarom `sosa:SpatialSample` voor het meetpunt?

Verworpen alternatief: het meetpunt enkel als `sosa:Platform` modelleren, met de fietsroute
als directe FeatureOfInterest van de observaties.
Gekozen aanpak: het meetpunt is tegelijk `sosa:Platform`, `sosa:FeatureOfInterest` en
`sosa:SpatialSample`; de fietsroute is de ultimate FOI via `sosa:isSampleOf`.
Motivatie: een teller meet niet de volledige fietsroute maar één specifiek punt erop.
`sosa:SpatialSample` drukt precies uit dat het meetpunt een ruimtelijk deelmonster is van
de route. De geometrie (`geo:hasGeometry`) is dan een eigenschap van het monster, niet van
de volledige route.

### Waarom `sosa:hasFeatureOfInterest` op de collectie naar het meetpunt, niet naar de fietsroute?

Verworpen alternatief: `sosa:hasFeatureOfInterest ex:fietsroute-F1-antwerpen` op de collectie.
Gekozen aanpak: `sosa:hasFeatureOfInterest ex:meetpunt-FMN-021`.
Motivatie: de observaties meten de eigenschap op het meetpunt (het concrete studieobject),
niet op de volledige fietsroute. De fietsroute is bereikbaar als ultimate FOI via de
sampling-keten (`meetpunt isSampleOf fietsroute`), wat semantisch preciezer is dan de
route direct als FOI op te geven terwijl de meting slechts op één locatie plaatsvindt.

### Waarom `sosa:hasResult` met benoemde resultaten, en niet `sosa:hasSimpleResult`?

Verworpen alternatief: `sosa:hasSimpleResult "NNN"^^xsd:integer` voor alle 25 observaties.
Gekozen aanpak: elke observatie heeft `sosa:hasResult ex:resultaat-…` (`sosa:Result` met
`qudt:numericValue` en `qudt:hasUnit unit:NUM`).
Motivatie: de uurresultaten zijn de inputwaarden van de dagsom (`sosa:hasInputValue`). Een
inputwaarde is een entiteit (`sosa:hasInputValue` ⊂ `prov:used`, `pplan-sosa.ttl`), dus het
resultaat moet een eigen resource zijn waarnaar verwezen kan worden. Een literal via
`hasSimpleResult` kan dat niet. Dat is precies het geval waarvoor CLAUDE.md §5 de objectvorm
voorschrijft: provenance van het resultaat. De eenheid is `unit:NUM` (een aantal). "Voertuigen
per uur of per dag" volgt uit de property en de `phenomenonTime`. Ook de dagsom krijgt zo'n
resultaat, zodat de stijl niet gemengd wordt (R3).

### Waarom `sosa:ObservationCollection`?

Verworpen alternatief: 25 losse observaties zonder collectienode.
Gekozen aanpak: één `sosa:ObservationCollection` met gedeelde metadata.
Motivatie: sensor, procedure, feature of interest en observedProperty zijn identiek voor
alle 25 observaties. Door ze op collectieniveau te plaatsen wordt herhaling vermeden en is
de gemeenschappelijke context direct opvraagbaar (SOSA 2023 §4.3).

### Waarom `sosa:hasInputValue` naar de uurresultaten en `sosa:relatedObservation` naar de collectie?

Verworpen alternatieven: (a) de dagsom als gewoon `sosa:hasMember` opnemen in de collectie;
(b) `sosa:hasInputValue` naar de collectie.
Gekozen aanpak: de dagobservatie staat buiten de `hasMember`-lijst. Ze verwijst met
`sosa:hasInputValue` naar de 24 uurresultaten (de waarden) en met `sosa:relatedObservation`
naar de collectie (de bronobservaties).
Motivatie: de dagsom is geen directe registratie van de teller, maar een aggregatie van de
24 uurtellingen. Ze maakt dus geen deel uit van de collectie (R13). SOSA 2023 definieert
`sosa:hasInputValue` als "kent een waarde toe aan een input, gedefinieerd door de Procedure, die
gebruikt wordt in een Execution": een waarde, een `prov:Entity`. Een collectie van observaties
is geen waarde. Met `hasInputValue` ⊂ `prov:used` (`pplan-sosa.ttl`) zou ze een entiteit worden,
terwijl haar leden activiteiten zijn. De vorige versie van dit voorbeeld deed dat; de pipeline
meldde het als `[MODEL INVALID]` (rechtgezet 2026-10-01). De band met de bronobservaties is
`sosa:relatedObservation` ("relation from an Execution … to an Observation or
ObservationCollection"). Doordat de metadata
(sensor, procedure, FOI, property) niet via collectie-erfenis beschikbaar is, worden ze
expliciet herhaald op de dagobservatie.

### Waarom plat model en geen drielaags architectuur?

Verworpen alternatief: drielaags model met `p-plan:Plan`, Deployment en `prov:Activity`.
Gekozen aanpak: plat model.
Motivatie: er is één sensor op één locatie die één soort meting uitvoert. Er is geen
meerstaps-afleiding, geen herbruik van dezelfde procedure op meerdere datasets, en geen
vereiste traceerbaarheid naar een abstract plan. Het drielaags model is voorbehouden voor
meerstaps-processen.

## 7. Tijdsmodellering

Alle 25 observaties gebruiken `sosa:phenomenonTime → time:Interval` met
`time:hasBeginning` en `time:hasEnd` als anonieme `time:Instant`-nodes.

| Observatie | phenomenonTime (begin → end) | resultTime |
|---|---|---|
| dagsom | `2026-04-28T00:00:00 → 2026-04-29T00:00:00` | `2026-04-28T23:59:59` |
| uurobs NNu | `2026-04-28TNN:00:00 → 2026-04-28T(NN+1):00:00` | `2026-04-28TNN:59:59` |
| uurobs 23u | `2026-04-28T23:00:00 → 2026-04-29T00:00:00` | `2026-04-28T23:59:59` |

Onderscheid:
- `sosa:phenomenonTime` — de periode waarover het verkeer werd geteld (half-open interval,
  begin inclusief, end exclusief).
- `sosa:resultTime` — het moment waarop het telresultaat beschikbaar werd (einde van het
  meetinterval, als `xsd:dateTime`-literal).

`time:Interval` is hier correcter dan `time:Instant` omdat een telling inherent een periode
beslaat en geen puntmeting is.

## 8. Prefixen en IRI-structuur

| Prefix | Base URI | Tijdelijk of persistent |
|---|---|---|
| `ex:` | `https://example.org/verkeersmetingen/` | Tijdelijk (illustratief) |
| `sosa:` | `http://www.w3.org/ns/sosa/` | Persistent (W3C) |
| `time:` | `http://www.w3.org/2006/time#` | Persistent (W3C) |
| `geo:` | `http://www.opengis.net/ont/geosparql#` | Persistent (OGC) |
| `qudt:` | `http://qudt.org/schema/qudt/` | Persistent (QUDT) |
| `unit:` | `http://qudt.org/vocab/unit/` | Persistent (QUDT) |
| `xsd:` | `http://www.w3.org/2001/XMLSchema#` | Persistent (W3C) |
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
| `sosa:hasFeatureOfInterest` | `sosa:isFeatureOfInterestOf` | `ex:meetpunt-FMN-021 sosa:isFeatureOfInterestOf ex:collectie-FMN-021-20260428` |
| `sosa:hasMember` | `sosa:isMemberOf` | de 24 uurobservaties: `ex:obs-...-NNu sosa:isMemberOf ex:collectie-FMN-021-20260428` |
| `sosa:hasResult` | `sosa:isResultOf` | de 25 resultaten: `ex:resultaat-... sosa:isResultOf ex:obs-...`; het meetpunt: `sosa:isResultOf ex:sampling-meetpunt-FMN-021` |
| `sosa:hasSample` | `sosa:isSampleOf` | `ex:fietsroute-F1-antwerpen sosa:hasSample ex:meetpunt-FMN-021` |
| `sosa:hasFeatureOfInterest` | `sosa:isFeatureOfInterestOf` | ook `ex:fietsroute-F1-antwerpen sosa:isFeatureOfInterestOf ex:sampling-meetpunt-FMN-021` |

Vanuit de fietsroute zijn de observaties bereikbaar via de keten `fietsroute ← isSampleOf ← meetpunt ← isFeatureOfInterestOf ← collectie`.
