# Brownies

*Brownies bakken volgens het recept van Nigella Lawson, als demonstratie van het volledige
drielaagse patroon: het recept als plan, de inzet van het keukengerei, één concrete uitvoering met
de herkomst van elk tussenproduct.*

| | |
|---|---|
| **Domein** | bewust alledaags: een recept |
| **Model** | drielaags, met deelplannen |
| **Bestanden** | [README](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/Nigella-Lawson-Brownies/README.md) · [bespreking](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/Nigella-Lawson-Brownies/bespreking.md) |

## Waarom een recept

Het domein is alledaags, zodat de aandacht naar het patroon gaat en niet naar de vakkennis. Het
patroon is hetzelfde als bij een laboratoriumanalyse of een productieproces: stappen, variabelen,
systemen die stappen uitvoeren, en een afleidingsketen van grondstof tot eindproduct.

## De keuzes

- **Drie lagen**: het recept is een plan met stappen (smelten, hakken, mengen, bakken), het
  keukengerei wordt ingezet in één keuken, en één uitvoering (10 februari 2026) is gedocumenteerd
  ([R4](../regels/r04.md)).
- **Een plan is ook een procedure** (`p-plan:Plan ⊂ sosa:Procedure`, [P-PLAN en SOSA](../samenhang/pplan-sosa.md)).
- **Een stap én een deelplan**: elke stap (`step:melting`) is uitgewerkt in een eigen plan
  (`plan:melting`), verbonden met `p-plan:isDecomposedAsPlan`. Bewust twee resources en geen
  `p-plan:MultiStep` in één: zo blijft het onderscheid tussen de plaats in het recept en de
  uitgewerkte instructies zichtbaar. De uitvoering gebruikt het deelplan, de herbruikbare definitie
  ([Welke procedure?](../samenhang/pplan-sosa.md#3-welke-procedure-de-stap-of-het-definitieplan)).
- **Het keukengerei als systeem dat handelt**: elk stuk gerei implementeert een stap, is de agent
  van zijn deelactiviteit (`prov:wasAssociatedWith`) en handelt namens de kok
  (`prov:actedOnBehalfOf`). Verworpen: de kok als enige agent en het gerei als gebruikte entiteit.
  Gevolg: `prov:used` en `sosa:hasResult` bevatten enkel wat omgevormd wordt, zodat de herkomst
  van de brownies uit die twee relaties alleen te reconstrueren is.
- **Een collectie als studieobject**: smelten en mengen werken in op een verzameling ingrediënten
  (`prov:Collection`).
- **De kleurcontrole is een waarneming met een mens als sensor**.

## Diagram

```mermaid
--8<-- "src/main/input/Nigella-Lawson-Brownies/Nigella-Lawson-brownies.mmd"
```

## Turtle

??? example "Nigella-Lawson-Brownies.ttl"

    ```turtle
    --8<-- "src/main/input/Nigella-Lawson-Brownies/Nigella-Lawson-Brownies.ttl"
    ```
