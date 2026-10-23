# Energiemanagement

*Drie scenario's uit energiebeheer in gebouwen en industrie, elk ontvangen als eerste versie en
herzien naar het drielaagse patroon.*

| Scenario | Wat | Bestanden |
|---|---|---|
| **Isolatieadvies** | een warmteverliesklasse van een gebouw, afgeleid uit het gemiddelde nachtelijke warmteverlies | [README](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/EnergieManagementSystem/DatavoorbeeldIsolatieadvies/README.md) |
| **Voorverwarming HVAC** | een machinaal-leermodel voorspelt wanneer de warmtepomp moet starten; een actuatie start ze | [README](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/EnergieManagementSystem/DatavoorbeeldPreHeatingHvac/README.md) |
| **Stillegging productielijn** | een productielijn in Kortrijk stopt wanneer de elektriciteitsprijs een drempel overschrijdt, met minimale en maximale stilleggingstijd | [README](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/EnergieManagementSystem/DatavoorbeeldStilleggingProductielijn/README.md) |

## Waarom deze casus

Drie herzieningen van modellen die met de beste bedoelingen gemaakt werden, maar planning,
inzet en uitvoering door elkaar haalden. De verbeterpunten zijn een catalogus van wat er gebeurt
zonder die scheiding.

## Wat er in de ontvangen versies misliep

- **Planning en uitvoering door elkaar**: een procedure die zowel abstracte variabelen als
  concrete waarnemingen bevat; concrete waarden (100 EUR drempel, 8 uur maximum) rechtstreeks in de
  procedure.
- **`sosa:hasInput` voor concrete waarden**, op uitvoeringsniveau ([R5](../regels/r05.md)).
- **Waarneming en actuatie vermengd** in één geneste structuur met blanco knopen.

## De keuzes van de herzieningen

- **Drielaags**, met de drempelwaarden als variabelen op planniveau en hun concrete waarden als
  entiteiten op uitvoeringsniveau ([R4](../regels/r04.md), [Volgens welk plan?](../modelleren/plan.md)).
- **`sosa:hasInputValue` voor de waarden die een inputvariabele invullen** (sinds 2026-10-01; daarvoor
  `prov:used`).
- **Het ML-model is een artefact**: een `it6:MachineLearningModel` en `prov:Entity`, gegenereerd
  door een training; de voorspelling gebruikt het met `prov:used`; de voorspeller is de sensor
  ([R6](../regels/r06.md)).
- **De warmtepomp is systeem en studieobject**: de actuatie werkt erop in.
- **MultiSteps**: in Isolatieadvies en Stillegging gebruikt een uitvoering het definitieplan van
  haar stap ([P-PLAN en SOSA](../samenhang/pplan-sosa.md#3-welke-procedure-de-stap-of-het-definitieplan)).

!!! note "Overgenomen bronmodellen"
    De ontvangen versies staan ongewijzigd in `source/` van elk scenario. Ze zijn niet normatief;
    enkel de `_herzien`-versies volgen de regels.

## Diagram: voorverwarming (herzien)

```mermaid
--8<-- "src/main/input/EnergieManagementSystem/DatavoorbeeldPreHeatingHvac/DatavoorbeeldPreHeatingHvac_herzien.mmd"
```

## Diagram: stillegging, vóór en na

```mermaid
--8<-- "src/main/input/EnergieManagementSystem/DatavoorbeeldStilleggingProductielijn/DatavoorbeeldStilleggingProductielijn_vergelijking.mmd"
```

## Turtle

??? example "DatavoorbeeldPreHeatingHvac_herzien.ttl"

    ```turtle
    --8<-- "src/main/input/EnergieManagementSystem/DatavoorbeeldPreHeatingHvac/DatavoorbeeldPreHeatingHvac_herzien.ttl"
    ```
