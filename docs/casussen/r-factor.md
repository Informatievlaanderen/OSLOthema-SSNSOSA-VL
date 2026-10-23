# R-factor

*De erosiviteit van neerslag (RUSLE R-factor) voor 53 neerslagstations van KMI en VMM: jaar-,
maand- en 15-daagse waarden, 1898–2024.*

| | |
|---|---|
| **Domein** | bodemerosie, neerslag |
| **Model** | plat, drie collecties per aggregatieniveau, een afgeleide waarneming |
| **Bron** | CSV-bestanden en een GeoPackage (53 stations, ~35 000 waarden) |
| **Transformatie** | R-script → JSON-LD → `riot` → `.trig` (volledig, 42 MB) en `.ttl` (één station) |
| **Bestanden** | [README](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/r-factor/README.md) · [bespreking](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/r-factor/bespreking.md) · [script](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/r-factor/r/rfactor_to_rdf.R) |

## Waarom deze casus

Het toont hoe een grote, gescripte dataset eruitziet: volledige data en een toetsdeel, gekozen met
één variabele in het script; deterministische IRI's voor alles; geen enkele blanco knoop.

## De keuzes

- **Elk station is een ruimtelijk monster van Vlaanderen**: `sosa:Platform`,
  `sosa:FeatureOfInterest` en `sosa:SpatialSample`, met een geometrie in Lambert 72, en het
  resultaat van een ruimtelijke bemonstering ([R11](../regels/r11.md)).
- **Eén centrale sensor**: de R-factor wordt niet per station berekend, maar centraal door het
  Departement Omgeving. Alle waarnemingen hebben dezelfde sensor en procedure, ongeacht of de
  brondata van KMI of VMM komt.
- **Een collectie per aggregatieniveau**: jaarlijks, maandelijks, 15-daags; elke waarde met een
  `time:Interval` ([R12](../regels/r12.md)).
- **Het gemiddelde is een afgeleide waarneming** met `sosa:hasInputValue` naar de jaarresultaten
  ([R13](../regels/r13.md)); de meest recente waarde niet, want die is gewoon een van de leden.
- **Skolem-IRI's** voor intervallen, tijdstippen, resultaten en geometrieën ([R10](../regels/r10.md)).
- **Een lokale eenheid** `ex:unit-rfactor` (MJ·mm/(ha·h·jaar)): QUDT heeft ze niet, en er is geen
  register dat ze dekt. Een kandidaat voor een register.

## Diagram

```mermaid
--8<-- "src/main/input/r-factor/rfactor.mmd"
```

## Turtle

Het toetsdeel (`rfactor.ttl`, één station, 185 KB) is te groot om hier in te voegen:
[op GitHub bekijken](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/r-factor/rfactor.ttl).
