# BRDR

*Een herziening van de provenance van het heraligneren van afbakeningen van aanduidingsobjecten
op een gecorrigeerde perceellaag, met de bibliotheek brdr.*

| | |
|---|---|
| **Domein** | onroerend erfgoed, referentiedata; afbakeningen van Onroerend Erfgoed op GRB-ADP |
| **Model** | drielaags |
| **Bron** | provenance-voorbeelden in [`gezever/BRDR`](https://github.com/gezever/BRDR); de bibliotheek [brdr](https://github.com/OnroerendErfgoed/brdr) (Onroerend Erfgoed en Athumi) |
| **Bestanden** | [README met verbeterpunten](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/brdr/README.md) · [bespreking](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/brdr/bespreking.md) · [alternatief](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/brdr/alternatief/README.md) |

## Waarom deze casus

Een provenance-log waarin SOSA maar een deel van het verhaal is. De casus toont waar SOSA past (de
waarnemingen van een algoritme, de wijziging van een afbakening) en waar PROV-O en P-PLAN volstaan
(een voorstel berekenen, versies van geometrieën en referentielagen). Ze toont ook de fout die in
provenance het vaakst voorkomt: een activiteit gebruiken alsof ze een entiteit is
([R16](../regels/r16.md)).

## De verbeterpunten

| # | Ontvangen | Herzien | Regel |
|---|---|---|---|
| 1 | de selectie `prov:used` de observaties | `sosa:hasInputValue` naar de resultaten van de vergelijking | [R7](../regels/r07.md), [R16](../regels/r16.md) |
| 2 | `prov:generatedAtTime` op de selectie (een activiteit) | op de nieuwe afbakening | [R16](../regels/r16.md) |
| 3 | de alignering is een `sosa:Actuation` op een geometrie | aligneren is een `p-plan:Activity`; de selectie is de actuatie op de afbakening van het object | [R1](../regels/r01.md) |
| 4 | één actuatie voor drie identieke kandidaten | een alignering per relevante afstand, met haar parameters | [R5](../regels/r05.md) |
| 5 | de gekozen kandidaat twee keer gegenereerd | een nieuwe versie, `prov:wasRevisionOf` de oude | — |
| 6 | enkel kandidaat *a* geëvalueerd, *b* gekozen | een collectie per kandidaat, plus de formule van de huidige afbakening | — |
| 7 | geen vergelijking | afgeleide observaties met de evaluatieklasse van brdr | [R13](../regels/r13.md) |
| 8 | percentage als `hasSimpleResult` | `qudt:QuantityValue` met `unit:PERCENT` | [R3](../regels/r03.md) |
| 9 | `ssn:implements`, `ssn:hasInput`, `ssn:Property` | `sosa:`-termen, `p-plan:Variable` | [R14](../regels/r14.md) |
| 10 | WKT in Lambert 72 zonder CRS | CRS-IRI van EPSG:31370 in de literal | [R11](../regels/r11.md) |
| 11 | versiedatum en capakey op een perceelgeometrie | versies van ADP en van de perceelgeometrieën; het perceel met zijn IRI uit het Perceelregister | [R10](../regels/r10.md) |

De validatie van het origineel gaf 7 inconsistenties (punten 1 en 2) en 34 schendingen van de
gegenereerde shapes.

## De keuzes van de herziening

- **Enkel de keuze verandert het object.** Aligneren berekent voorstellen; de selectie is de
  `sosa:Actuation` op de afbakening van het aanduidingsobject.
- **De kandidaat is het studieobject van de evaluatie**, het perceel een inputwaarde.
- **De formule** (de bedekkingen door de huidige afbakening) is een eigen collectie, zodat de
  vergelijking haar inputwaarden heeft.
- **De formule draagt haar herkomst**: de bedekkingen van de huidige afbakening komen uit
  `brdr1.json` (brdr 0.9.0, 2025-03-31), met per perceel de versiedatum.
- **De aanleiding is een revisie**: de geometrie van perceel 0734 van 2025-09-03
  `prov:wasRevisionOf` die van 2018-12-01, en de inzet gebruikt de nieuwe versie van ADP.
- **Bestaande IRI's** voor de percelen, uit het Perceelregister
  (`https://data.vlaanderen.be/id/perceel/…`).
- **Eenheden uit QUDT**: procent en meter.

## Twee lezingen

Het alternatief volgt de metadata die **brdr zelf** schrijft: elke alignering is een
`sosa:Actuation` op de afbakening, met de kandidaat als resultaat en de relevante afstand als
inputwaarde, en het referentieperceel is het studieobject van de bedekking. De gekozen kandidaat is
dan zelf de nieuwe afbakening, en de mapping ligt dicht bij wat brdr al publiceert. Een argument
tegen: twee actuaties wijzigen op hetzelfde moment dezelfde eigenschap van hetzelfde object, en
enkel de selectie, een gewone PROV-activiteit, zegt welke wijziging gebeurd is. Status: beide
*voorstel*.

```mermaid
--8<-- "src/main/input/brdr/alternatief/brdr_vergelijking.mmd"
```

## Diagram: vóór en na

```mermaid
--8<-- "src/main/input/brdr/brdr_vergelijking.mmd"
```

## Diagram: de herziening

```mermaid
--8<-- "src/main/input/brdr/brdr_herzien.mmd"
```

## Turtle

??? example "brdr_herzien.ttl"

    ```turtle
    --8<-- "src/main/input/brdr/brdr_herzien.ttl"
    ```

??? example "alternatief/brdr_actuatie.ttl"

    ```turtle
    --8<-- "src/main/input/brdr/alternatief/brdr_actuatie.ttl"
    ```
