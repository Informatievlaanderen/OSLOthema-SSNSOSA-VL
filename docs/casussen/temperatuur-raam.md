# Temperatuur en raam

*Een thermometer en een raamopener: boven 20 °C gaat het raam open, onder 18 °C dicht.*

| | |
|---|---|
| **Domein** | gebouwbeheer |
| **Model** | drielaags (planning, inzet, uitvoering) |
| **Bron** | illustratief, een vereenvoudiging van [elektrisch raam](elektrisch-raam.md) |
| **Bestanden** | [README](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/temperatuur-raam/README.md) · [bespreking](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/temperatuur-raam/bespreking.md) · [opdracht](../oefenen/temperatuur-raam.md) |

## Waarom drielaags voor twee stappen?

Omdat er een **gegevensstroom** is: de gemeten temperatuur is de input van de beslissing om het
raam te openen of te sluiten. En omdat dezelfde werkwijze in **elk lokaal** kan draaien. Twee van
de drie criteria van [R4](../regels/r04.md).

## De keuzes

- **Een plan met twee stappen**: `step:temp-meting` (de waarneming) en `step:raam-actuatie` (de
  actuatie), met de temperatuur als variabele tussen beide ([Volgens welk plan?](../modelleren/plan.md)).
- **Elke stap is een procedure**: de thermometer implementeert de meetstap, de raamopener de
  actuatiestap (`p-plan:Step ⊂ sosa:Procedure`, [P-PLAN en SOSA](../kaart/pplan-sosa.md)).
- **Geen afgeleide waarneming**: de drempellogica (hysterese tussen 18 en 20 °C) zit in de
  procedure van de actuatie.
- **Benoemde resultaten** met `p-plan:correspondsToVariable`, zodat de actuatie naar de gemeten
  waarde kan verwijzen.
- **Type op de stap, waarde op de uitvoering**: `step:raam-actuatie` heeft `sosa:hasInput
  var:temperatuur`; de actuatie heeft `sosa:hasInputValue` naar het temperatuurresultaat, dat die
  variabele invult ([R5](../regels/r05.md), [R13](../regels/r13.md)).

## Diagram

```mermaid
--8<-- "src/main/input/temperatuur-raam/temperatuur-raam.mmd"
```

## Turtle

??? example "temperatuur-raam.ttl"

    ```turtle
    --8<-- "src/main/input/temperatuur-raam/temperatuur-raam.ttl"
    ```
