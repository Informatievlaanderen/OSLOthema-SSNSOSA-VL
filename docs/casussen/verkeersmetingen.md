# Verkeersmetingen

*Uurtellingen van fietsers op een telpost, en de dagsom.*

| | |
|---|---|
| **Domein** | mobiliteit; fietstelposten (formaat van Provincie Antwerpen) |
| **Model** | plat, met een collectie per dag en een afgeleide waarneming |
| **Bron** | fictief illustratief voorbeeld; telpost FMN-021, Mercatorstraat, Antwerpen |
| **Bestanden** | [README](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/verkeersmetingen/README.md) · [bespreking](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/verkeersmetingen/bespreking.md) · [opdracht](../oefenen/verkeersmetingen.md) |

## De vraag

Hoeveel fietsers passeren er per uur, en per dag, op de fietsroute F1 ter hoogte van de
Mercatorstraat?

## De keuzes

- **Het telpunt is een ruimtelijk monster van de route.** Het is `sosa:Platform` (het herbergt de
  teller), `sosa:FeatureOfInterest` (het directe studieobject) en `sosa:SpatialSample` van de
  fietsroute F1, met een puntgeometrie. Het is het resultaat van een ruimtelijke bemonstering: de
  keuze van de plaats op de route ([R11](../regels/r11.md), [Ruimtelijk monster](../patronen/ruimtelijk-monster.md)).
- **Het studieobject van de collectie is het telpunt, niet de route.** De teller telt op één plaats.
- **Een collectie van 24 uurtellingen**, elk met een `time:Interval` van een uur, halfopen
  ([R12](../regels/r12.md)).
- **Benoemde resultaten** (`qudt:QuantityValue` met een IRI), omdat ze inputwaarde worden van de
  dagsom ([R3](../regels/r03.md)).
- **De dagsom is een afgeleide waarneming buiten de collectie**, met `sosa:hasInputValue` naar de
  24 uurresultaten en `sosa:relatedObservation` naar de collectie ([R13](../regels/r13.md)).
- **Plat, niet drielaags**: één teller, één eigenschap, geen meerstappenproces ([R4](../regels/r04.md)).

## Wat er rechtgezet werd

Tot 2026-10-01 verwees de dagsom met `sosa:hasInputValue` naar de **collectie**. De collectie
draagt `sosa:hasFeatureOfInterest` (⊂ `prov:used`, domein `prov:Activity`) en werd daardoor een
activiteit; als inputwaarde werd ze ook een entiteit. De validatie meldde de tegenspraak. Samen
met dezelfde fout in [paleo](paleo.md) leidde dit tot het voorstel om `sosa:hasInputValue ⊂
prov:used` in de W3C-module op te nemen ([SOSA en PROV-O](../kaart/sosa-prov.md#5-inputwaarde-en-resultaat-een-spiegel)).

## Diagram

```mermaid
--8<-- "src/main/input/verkeersmetingen/verkeersmetingen.mmd"
```

## Turtle

??? example "verkeersmetingen.ttl"

    ```turtle
    --8<-- "src/main/input/verkeersmetingen/verkeersmetingen.ttl"
    ```
