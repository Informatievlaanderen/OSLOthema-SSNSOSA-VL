# Elektrisch raam

*De automatische raambesturing van zaal 01.16 in het Herman Teirlinckgebouw: vier sensoren, een
afgeleide waarneming en een actuatie.*

| | |
|---|---|
| **Domein** | gebouwbeheer, Herman Teirlinckgebouw (Brussel) |
| **Model** | drielaags |
| **Bron** | illustratief, op basis van de beschrijving van de raamautomatisering |
| **Bestanden** | [README](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/elektrisch-raam/README.md) · [bespreking](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/elektrisch-raam/bespreking.md) |

## Het proces

1. Vier stappen meten: temperatuur, windsnelheid (aan de gevel), lichtintensiteit, regen.
2. Een afgeleide waarneming berekent de afwijking van de temperatuur tegenover 20 °C.
3. Een actuatie bepaalt de raamstand uit de afwijking en de andere drie metingen.

## De keuzes

- **Drielaags**: vijf procedures met een gegevensstroom, herbruikbaar in andere zalen
  ([R4](../regels/r04.md)).
- **Elke sensor implementeert één stap**, die tegelijk `p-plan:Step` en `sosa:Procedure` is.
- **De besturingseenheid is een sensor** voor de afgeleide waarneming: ze bepaalt een waarde
  (de afwijking) uit andere waarden.
- **Benoemde resultaten** met `p-plan:correspondsToVariable`, zodat ze extern aanspreekbaar zijn
  en de volgende stap ernaar kan verwijzen ([R3](../regels/r03.md)).
- **Het regenresultaat zonder QUDT**: een ja/nee-waarde heeft geen eenheid.
- **Gedeelde infrastructuur** krijgt een eigen prefix: `htg:` voor het Herman Teirlinckgebouw.
- **Inputwaarden**: de afgeleide waarneming en de actuatie verwijzen met `sosa:hasInputValue` naar
  de resultaten die hun inputvariabelen invullen; de stappen declareren die variabelen met
  `sosa:hasInput` ([R13](../regels/r13.md)).

## Diagram

```mermaid
--8<-- "src/main/input/elektrisch-raam/elektrisch-raam.mmd"
```

## Turtle

??? example "elektrisch-raam.ttl"

    ```turtle
    --8<-- "src/main/input/elektrisch-raam/elektrisch-raam.ttl"
    ```
