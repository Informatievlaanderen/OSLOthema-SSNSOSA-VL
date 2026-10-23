# Erosiepoel

*Een veldwaarneming van het sedimentvolume in een erosiepoel na een nachtelijke regenbui.*

| | |
|---|---|
| **Domein** | erosiebeheer, Stad Mechelen |
| **Model** | plat, met een `sosa:ObservationCollection` |
| **Bron** | een aangeleverd scenario met een eerste Turtle-versie (geen externe databron) |
| **Bestanden** | [README](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/erosiepoel/README.md) · [bespreking](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/erosiepoel/bespreking.md) · [opdracht](../oefenen/erosiepoel.md) |

## Waarom deze casus eerst

Ze bevat het hele skelet van een waarneming (studieobject, eigenschap, resultaat met eenheid,
sensor, procedure, tijd) in één kleine graaf, en ze toont zeven fouten die in een eerste versie
typisch voorkomen.

## De keuzes

- **De poel is platform én studieobject.** Ze herbergt de veldwaarnemer (`sosa:Platform`) en is
  het ding waarvan het sedimentvolume bepaald wordt (`sosa:FeatureOfInterest`) ([R1](../regels/r01.md)).
- **Een mens is een sensor.** SOSA definieert een sensor als agent die een waarnemingsprocedure
  uitvoert; een veldwaarnemer van de stad is dat ([Wie of wat meet?](../modelleren/systemen.md)).
- **Een collectie, ook voor één waarneming.** Sensor, procedure en tijdstip staan op de collectie;
  een tweede meting kan erbij zonder iets te herhalen ([R2](../regels/r02.md)).
- **Het resultaat als `qudt:QuantityValue`** met kubieke meter, niet als literal ([R3](../regels/r03.md)).

## Wat er verbeterd werd

| Ontvangen | Herzien | Waarom |
|---|---|---|
| `ep:Erosiepoel` (enkel domeinklasse) | `sosa:Platform`, `sosa:FeatureOfInterest` | de SOSA-rol moet expliciet zijn ([R1](../regels/r01.md)) |
| `sosa:ObservableProperty` | `sosa:Property` | term van SSN/SOSA 2023 ([R14](../regels/r14.md)) |
| `qudt:unit` | `qudt:hasUnit` | `qudt:unit` bestaat niet ([R3](../regels/r03.md)) |
| `prov:startedAtTime`/`prov:endedAtTime` | `sosa:phenomenonTime`, `sosa:resultTime` | PROV-tijden zeggen wanneer de activiteit liep, niet wanneer het verschijnsel plaatsvond ([SOSA en OWL-Time](../samenhang/sosa-time.md)) |
| geen sensor | `ex:Waarnemer_X a sosa:Sensor` | nodig voor `sosa:madeBySensor` en `sosa:implements` |
| geen collectie | `sosa:ObservationCollection` | gedeelde context, uitbreidbaar |
| geen procedure | `ex:VeldmeetProcedure a sosa:ObservingProcedure` | sterk aanbevolen, voor reproduceerbaarheid |

## Diagram

```mermaid
--8<-- "src/main/input/erosiepoel/erosiepoel.mmd"
```

## Turtle

??? example "erosiepoel.ttl"

    ```turtle
    --8<-- "src/main/input/erosiepoel/erosiepoel.ttl"
    ```
