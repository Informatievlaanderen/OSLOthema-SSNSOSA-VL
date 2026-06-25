# R-factor erosiviteitsmetingen — SSN/SOSA datavoorbeeld

## Domeincontext

De R-factor (RUSLE rainfall erosivity factor) is een maat voor de erosieve kracht van neerslag.
Deze dataset bevat R-factorwaarden berekend voor 53 neerslagmeetstations in Vlaanderen,
beheerd door het KMI (Koninklijk Meteorologisch Instituut, 10 stations) en VMM
(Vlaams Milieumaatschappij, 43 stations). De data omvatten jaarlijkse, maandelijkse en
15-daagse aggregaties over meetperiodes van 1898 tot 2024.

Eenheid: MJ·mm/(ha·h·jaar) — de standaard RUSLE R-factor eenheid.

## Bronbestanden

| Bestand | Inhoud | Records |
|---|---|---|
| `stations_rfactor.csv` | Stationsmetadata (ID, beheerder, locatie, Lambert 72-coördinaten) | 53 |
| `view_rfactor.csv` | Samenvattingstabel per station (periode, gemiddelde, meest recente waarde) | 53 |
| `jaarlijkse_rfactor.csv` | Jaarlijkse R-factorwaarden per station | 941 |
| `maandelijkse_rfactor.csv` | Maandelijkse R-factorwaarden per station | 11.292 |
| `15-daagse_rfactor.csv` | 15-daagse R-factorwaarden per station (24 perioden/jaar) | 22.584 |
| `rfactor.gpkg` | GeoPackage met stationsgeometrie (OGC-formaat) | — |

## Transformatiepipeline (CSV → RDF)

```
stations_rfactor.csv  ─┐
view_rfactor.csv       ─┤
jaarlijkse_rfactor.csv ─┤  Rscript r/rfactor_to_rdf.R
maandelijkse_rfactor.csv─┤  (vanuit r-factor/ directory)
15-daagse_rfactor.csv  ─┘
        │
        ▼
   rfactor.jsonld    (JSON-LD intermediair, ~20 MB)
        │
        ▼ riot --output=turtle
   rfactor.ttl       (Turtle, ~34 MB)
```

### Stap voor stap

```bash
cd src/main/input/r-factor
Rscript r/rfactor_to_rdf.R
```

Vereisten: R ≥ 4.0 met pakketten `readr`, `dplyr`, `jsonlite`, `lubridate`;
Apache Jena `riot` op PATH.

## SSN/SOSA-modelleringspatroon

**Plat model** — drie temporele aggregatieniveaus, elk als `sosa:ObservationCollection`:

- **Jaarlijks**: `ex:collectie-{station}-jaarlijks` → leden per jaar
- **Maandelijks**: `ex:collectie-{station}-{jaar}-maandelijks` → 12 leden/jaar
- **15-daags**: `ex:collectie-{station}-{jaar}-15daags` → 24 leden/jaar

Elk station is `sosa:Platform + sosa:FeatureOfInterest + sosa:SpatialSample`
(ruimtelijk deelmonster van Vlaanderen) met Lambert 72-geometrie.

De gemiddelde jaarlijkse R-factor uit `view_rfactor.csv` is een **afgeleide observatie**
(`sosa:hasInputValue` → jaarlijkse collectie, conform R13).

## Gegenereerde output

| Bestand | Formaat | Grootte |
|---|---|---|
| `rfactor.jsonld` | JSON-LD | ~20 MB |
| `rfactor.ttl` | Turtle | ~34 MB |
