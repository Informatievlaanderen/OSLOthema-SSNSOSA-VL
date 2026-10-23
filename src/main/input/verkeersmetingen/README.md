# Verkeersmetingen — fietstelpost Mercatorstraat

## Bronbestand

Fictief illustratief voorbeeld gebaseerd op het dataformaat van automatische fietstelposten
beheerd door Provincie Antwerpen. Meetpunt-ID: **FMN-021**, naam: **Mercatorstraat**,
locatie: Hoek Mercatorstraat met Van Den Nestlei, Antwerpen (lat 51.20910 / lon 4.423123).

## Transformatieproces

Geen formele transformatie — het Turtle-bestand is rechtstreeks aangemaakt op basis van de
meetpuntbeschrijving en teldata. In een productiesituatie zou de brondata (CSV of JSON via een
verkeerstellings-API) omgezet worden via:

1. **CSV → RDF**: `riot --output=TURTLE` na een SPARQL-CONSTRUCT of YARRRML-mapping.
2. **Geocoding**: coördinaten worden gemapt op een `sosa:Platform`-node.
3. **Tijdreeksverwerking**: uurwaarden per dag worden omgezet naar individuele `sosa:Observation`-instances.

## Mapping-keuzes

Plat SSN/SOSA-model met `sosa:ObservationCollection` (details in `bespreking.md`):

- Het **meetpunt** FMN-021 is tegelijk `sosa:Platform` (het herbergt de teller),
  `sosa:FeatureOfInterest` (het directe studieobject) en `sosa:SpatialSample` van de fietsroute
  (R11). Het is het resultaat van een ruimtelijke bemonstering (`sosa:Sampling`): de keuze van het
  meetpunt op de route.
- De **automatische teller** is een `sosa:Sensor` die één eigenschap meet:
  `ex:property-verkeersintensiteit` (aantal passerende lichte voertuigen in de gemeten periode).
- De **fietsroute F1** is het ultieme `sosa:FeatureOfInterest`, bereikbaar via `sosa:isSampleOf`.
- Een `sosa:ObservationCollection` groepeert de 24 uurtellingen van dinsdag 28 april 2026, elk
  met een `time:Interval` (R12) en een benoemde `qudt:QuantityValue`.
- De **dagsom** (2541) is een afgeleide observatie buiten de collectie (R13): `sosa:hasInputValue`
  naar de 24 uurresultaten, `sosa:relatedObservation` naar de collectie.

## Grafische voorstelling

Zie `verkeersmetingen.mmd` voor het Mermaid-diagram.

## Gebruik

Valideren: `mcp__ld-vocab__validate_file` op `src/main/input/verkeersmetingen/verkeersmetingen.ttl`, of alle voorbeelden
samen met het commando in de README van de repository.
