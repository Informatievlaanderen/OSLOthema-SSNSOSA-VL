# VLAREM-rubrieken

*Hoeveelheden in de criteria van een VLAREM-rubriek: "meer dan 50 l of 50 kg". Geen
SSN/SOSA-mapping: een criterium is een norm, geen waarneming.*

| | |
|---|---|
| **Domein** | milieuvergunningen, VLAREM-indelingslijst |
| **Model** | geen SOSA; QUDT en SKOS, met een ontwerpvocabularium `vlarem:` |
| **Bron** | het register van de VLAREM-rubrieken (rubriek 17.4) en twee ontvangen varianten |
| **Bestanden** | [README](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/vlarem_rubrieken/README.md) · [bespreking](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/vlarem_rubrieken/bespreking.md) · [alternatief](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/vlarem_rubrieken/alternatief/README.md) |

## Waarom deze casus in een werk over SOSA

Omdat de eerste reflex ook betekent: **weten wanneer SOSA niet past**. Een criterium in een rubriek
("een opslag van meer dan 50 liter") gaat niet over een waarde die iemand bepaalde, maar over een
grens die een regel stelt. Er is geen studieobject, geen sensor, geen fenomeentijd. Wat wel blijft:
een hoeveelheid met een eenheid is een `qudt:QuantityValue`, en een lijst van waarden is een
SKOS-begrippenschema.

## De keuzes

- **Geen SSN/SOSA**: een norm is geen waarneming.
- **Het criterium hangt aan de versie van de rubriek**, niet aan de rubriek: criteria veranderen
  met de regelgeving.
- **Een grens met een operator en alternatieve waarden**: een ondergrens (`vlarem:hasMin`) en een
  bovengrens (`vlarem:hasMax`), elk met een vergelijkingsoperator (een begrip uit een nieuwe
  SKOS-lijst) en per alternatieve eenheid één `qudt:QuantityValue`.
- **QUDT-eenheden**, geen register: liter en kilogram bestaan in QUDT ([R3](../regels/r03.md)).
- **De grootheid volgt uit de eenheid**; geen aparte onderwerpcode.
- **Een eigen ontwerpvocabularium** `vlarem:` voor wat geen bestaand vocabularium dekt, na
  vergelijking ([R17](../regels/r17.md)); geladen als ontologie, zodat de data gecontroleerd wordt.
- **De rubriek zelf staat niet in de data**: ze is een begrip van het register
  ([Codelijsten en registers](../modelleren/codelijsten.md)).

## Herziening en alternatief

Twee ontvangen varianten (een tussenlaag met grootheid en waarde, of grootheden en waarden op de
grens zelf) zijn herzien tot één model. Het alternatief groepeert per eenheid: één bereik per
eenheid, met `qudt:minExclusive` en `qudt:maxExclusive`.

## Diagram

```mermaid
--8<-- "src/main/input/vlarem_rubrieken/vlarem_rubrieken.mmd"
```

## Vergelijking met het alternatief

```mermaid
--8<-- "src/main/input/vlarem_rubrieken/alternatief/vlarem_rubrieken_vergelijking.mmd"
```

## Turtle

??? example "vlarem_rubrieken.ttl"

    ```turtle
    --8<-- "src/main/input/vlarem_rubrieken/vlarem_rubrieken.ttl"
    ```

??? example "alternatief/vlarem_rubrieken_bereik.ttl"

    ```turtle
    --8<-- "src/main/input/vlarem_rubrieken/alternatief/vlarem_rubrieken_bereik.ttl"
    ```
