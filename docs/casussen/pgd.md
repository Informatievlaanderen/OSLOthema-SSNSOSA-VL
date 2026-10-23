# Geschiktheidskaart PGD

*Een geschiktheidskaart voor peilgestuurde drainage (OP-PEIL), afgeleid uit andere kaartlagen:
per rastercel van 100 m drie factorscores en een kansrijkheid.*

| | |
|---|---|
| **Domein** | landbouw, water; Bodemkundige Dienst van België, VLAIO-project OP-PEIL (augustus 2024) |
| **Model** | drielaags |
| **Bron** | technische fiche en dataset op Zenodo ([10.5281/zenodo.17803699](https://doi.org/10.5281/zenodo.17803699)); kaart op [waterradar.be](https://waterradar.be/map) |
| **Bestanden** | [README](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/PGD_geschiktheidskaart/README.md) · [bespreking](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/PGD_geschiktheidskaart/bespreking.md) |

## Waarom deze casus

Een kaartlaag is ook een verzameling waarnemingen: per cel een waarde van een eigenschap, bepaald
volgens een werkwijze. Deze casus toont dat met een berekende kaart, waar de "sensor" een
QGIS-model is en de "metingen" andere kaartlagen.

## De keuzes

- **Drielaags**: drie factorscores uit drie kaartlagen en een beslissingsmodel dat ze combineert
  (meerdere stappen); twee QGIS-modellen (Binnen-Vlaanderen en polders) die stappen delen
  (hergebruik); en de herkomst van elke cel moet tot het plan te herleiden zijn
  ([R4](../regels/r04.md)).
- **Twee plannen**, één per QGIS-model, met hun stappen en variabelen; **de QGIS-modellen zijn
  sensoren**; de uitvoering voor Binnen-Vlaanderen is een inzet, met de gebruikte kaartlagen en
  het outputraster als PROV-entiteiten.
- **Een berekende score is een waarneming**: de waarde van een eigenschap (waterdoorlaatbaarheid,
  grondwateraanvoer, helling) van een studieobject (de rastercel), bepaald volgens een procedure.
- **De rastercel is een ruimtelijk monster** van Binnen-Vlaanderen, geen platform: er staat niets
  op ([R11](../regels/r11.md)).
- **De kansrijkheid is een afgeleide waarneming** met de drie scores als inputwaarde
  ([R13](../regels/r13.md)).
- **Scores en kansrijkheid uit twee kleine SKOS-codelijsten**; de helling als
  `qudt:QuantityValue` met een QUDT-eenheid.
- **Een stap in twee plannen** levert via de ketens van [P-PLAN en SOSA](../samenhang/pplan-sosa.md)
  twee procedures op; daarom staat `sosa:usedProcedure` expliciet op de stap.

## Diagram

```mermaid
--8<-- "src/main/input/PGD_geschiktheidskaart/pgd-geschiktheidskaart.mmd"
```

## Turtle

??? example "pgd-geschiktheidskaart.ttl"

    ```turtle
    --8<-- "src/main/input/PGD_geschiktheidskaart/pgd-geschiktheidskaart.ttl"
    ```
