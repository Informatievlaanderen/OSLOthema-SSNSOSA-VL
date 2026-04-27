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

Plat SSN/SOSA-model met `sosa:ObservationCollection`:

- Het **meetpunt** (vaste locatie) is een `sosa:Platform` dat de automatische teller herbergt.
- De **automatische teller** is een `sosa:Sensor` die twee observeerbare eigenschappen meet:
  absolute verkeersintensiteit (dagsom in aantal voertuigen) en een relatieve verkeersindex
  per uur (dimensieloze factor t.o.v. het piekuur).
- De **fietsroute F1** is het `sosa:FeatureOfInterest`.
- Een `sosa:ObservationCollection` groepeert alle observaties van 29 april 2026.
- Twee `sosa:ObservableProperty`-instanties onderscheiden dagsom- van uurprofielmetingen.

## Grafische voorstelling

Zie `verkeersmetingen.mmd` voor het Mermaid-diagram.

## Outputbestanden

Na uitvoering van de pipeline:

- `src/main/output/verkeersmetingen/verkeersmetingen.ttl` — Turtle na inferentie
- `src/main/output/verkeersmetingen/verkeersmetingen.jsonld` — JSON-LD na framing

## Gebruik

```bash
mvn compile exec:java
```
