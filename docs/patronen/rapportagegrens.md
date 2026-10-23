# Rapportagegrens

**"< X" is een interval, geen waarde.** Een resultaat onder de rapportagegrens heeft geen
`qudt:numericValue`: een waarde gelijk aan de grens zou een meting suggereren die niet bestaat.
Geef het interval dat het labo rapporteert.

## Het patroon

```turtle
# "< 0,0125 µg/L"
ex:resultaat-pfos a qudt:QuantityValue ;
    qudt:lowerBound 0.0 ;
    qudt:upperBound 0.0125 ;
    qudt:hasUnit unit:MicroGM-PER-L .

# "= 0,42 mg P/L"
ex:resultaat-ptot a qudt:QuantityValue ;
    qudt:numericValue 0.42 ;
    qudt:hasUnit csor-eenheid:E_131 .
```

- `[0, X]` voor "< X";
- het **teken volgt uit de vorm**: een `numericValue` voor een gemeten waarde, enkel grenzen voor
  "kleiner dan". Een aparte codelijst voor het teken is niet nodig.

## Waarom

Een resultaat "< 0,0125" invullen als 0,0125, of als 0, of als de helft van de grens, is een
interpretatie die de bron niet maakt. Statistiek over zulke waarden (gemiddelden, trends) vraagt
een methode die de grens kent. Het interval bewaart wat het labo zei, en laat de interpretatie aan
de gebruiker.

## Open

De detectie- en kwantificeringsgrenzen zelf (welke grens gold voor deze analyse?) zijn een aparte
vraag. Kandidaat: `ssn-system:DetectionLimit`. Status: *open*.

## Gebruikt in

- [Waterkwaliteit](../casussen/waterkwaliteit.md): in de oppervlaktewaterdata 834 van de 999
  resultaten onder de grens.

??? quote "Normatieve tekst (modelleergids, Engels)"

    --8<-- "kit/patroon-rapportagegrens.md"
