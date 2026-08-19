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
   rfactor.jsonld        (JSON-LD intermediair, ~34 MB)
        │
        ├─► rfactor.trig (volledige dataset, ~42 MB — uitgesloten van mvn-validatie)
        │
        └─► rfactor.ttl  (validatie-subset: station KMI_6408, ~185 KB)
```

### Stap voor stap

```bash
cd src/main/input/r-factor
Rscript r/rfactor_to_rdf.R
```

Vereisten: R ≥ 4.0 met pakketten `readr`, `dplyr`, `jsonlite`, `lubridate`;
Apache Jena `riot` op PATH.

Het script genereert twee Turtle-bestanden:
- **`rfactor.trig`** — volledige dataset (alle 53 stations, alle jaren). De `.trig`-extensie
  zorgt ervoor dat dit bestand niet meegenomen wordt in `mvn compile exec:java`
  (de pipeline verwerkt alleen `.ttl`-bestanden).
- **`rfactor.ttl`** — validatie-subset met één station (KMI_6408, jaren 2002–2005),
  alle drie aggregatieniveaus en de gemiddelde observatie. Dit bestand wordt wél
  gevalideerd door de pipeline.

Om een ander station als validatie-subset te kiezen, pas `VALIDATIE_STATION` aan in
`r/rfactor_to_rdf.R`.

## SSN/SOSA-modelleringspatroon

**Plat model** — drie temporele aggregatieniveaus, elk als `sosa:ObservationCollection`:

- **Jaarlijks**: `ex:collectie-{station}-jaarlijks` → leden per jaar
- **Maandelijks**: `ex:collectie-{station}-{jaar}-maandelijks` → 12 leden/jaar
- **15-daags**: `ex:collectie-{station}-{jaar}-15daags` → 24 leden/jaar

Elk station is `sosa:Platform + sosa:FeatureOfInterest + sosa:SpatialSample`
(ruimtelijk deelmonster van Vlaanderen) met Lambert 72-geometrie.

De R-factor wordt niet lokaal per station berekend, maar centraal door Departement Omgeving.
Alle observaties/collecties dragen daarom `sosa:madeBySensor` naar één gedeelde
`ex:sensor-rfactor` (gehost door `ex:departement-omgeving`), terwijl `sosa:usedProcedure`
wel gedifferentieerd blijft naar KMI/VMM omdat de brondataverwerking per meetnet verschilt.

De gemiddelde jaarlijkse R-factor uit `view_rfactor.csv` is een **afgeleide observatie**
(`sosa:hasInputValue` → jaarlijkse collectie, conform R13).

Alle geneste resources (`time:Interval`, `time:Instant`, `qudt:QuantityValue`,
`geo:Geometry`) krijgen deterministische skolem-IRIs — het model bevat geen blank nodes.

## Gegenereerde output

| Bestand | Formaat | Grootte | Opmerking |
|---|---|---|---|
| `rfactor.jsonld` | JSON-LD | ~34 MB | Intermediair, volledig |
| `rfactor.trig` | Turtle (TriG-extensie) | ~42 MB | Volledige dataset, niet gevalideerd door pipeline |
| `rfactor.ttl` | Turtle | ~185 KB | Validatie-subset (1 station), wél gevalideerd |
