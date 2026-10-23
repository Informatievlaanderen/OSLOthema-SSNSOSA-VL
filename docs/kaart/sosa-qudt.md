# SOSA en QUDT

**Een getal zonder eenheid is geen meetwaarde.** SOSA zegt dat een waarneming een resultaat
heeft, maar niet hoe dat resultaat eruitziet. QUDT levert het model voor een grootheidswaarde:
een getal en een eenheid, met de eenheid uit een register dat dimensies en omrekeningen kent.

| | |
|---|---|
| **Soort** | afspraak (geen OWL-module) |
| **Waar vastgelegd** | regel [R3](../regels/r03.md) |
| **QUDT-versie in dit project** | 3.5.2 (schema en eenheden) |

## 1. Het patroon

```turtle
ex:waarneming-1 a sosa:Observation ;
    sosa:observedProperty ex:sedimentvolume ;
    sosa:hasFeatureOfInterest ex:erosiepoel ;
    sosa:hasResult [
        a qudt:QuantityValue ;
        qudt:numericValue 2.4 ;
        qudt:hasUnit unit:M3
    ] .
```

- Het resultaat is een **`qudt:QuantityValue`** met **`qudt:numericValue`** (het getal) en
  **`qudt:hasUnit`** (de eenheid).
- In een klein voorbeeld volstaat een blanco knoop; wanneer het resultaat van buitenaf
  aanspreekbaar moet zijn, of in grote datasets, krijgt het een IRI
  ([R10](../regels/r10.md)), bv. `ex:resultaat-{waarneming}`.

## 2. Waarom het past

Het past omdat [SOSA en PROV-O](sosa-prov.md) het resultaat al een `prov:Entity` maken
(`sosa:hasResult ⊂ prov:generated`), en een grootheidswaarde is precies dat: een ding met vaste
kenmerken, gegenereerd door de waarneming. QUDT voegt geen tegenstrijdige types toe:
`qudt:QuantityValue` is geen activiteit.

Het resultaat als eigen resource heeft drie voordelen boven een literal:

1. **De eenheid hoort bij de waarde.** Twee waarnemingen van dezelfde eigenschap kunnen een
   verschillende eenheid hebben; met `qudt:hasUnit` op het resultaat blijft elke waarde
   ondubbelzinnig.
2. **Het resultaat kan inputwaarde zijn.** Een afgeleide waarneming verwijst met
   `sosa:hasInputValue` naar de resultaten van haar bronnen ([R7](../regels/r07.md)). Een
   literal kan geen object van een objecteigenschap zijn; een resource wel.
3. **Er is plaats voor meer.** Een onzekerheid, een rapportagegrens (`qudt:lowerBound`,
   `qudt:upperBound`), een kwaliteitsoordeel: ze horen bij het resultaat.

## 3. Wat er niet in hoort

!!! valkuil "`qudt:value` bestaat, maar is het niet"
    `qudt:value` is een bestaande QUDT-eigenschap, dus geen controle op onbekende termen vindt ze
    verdacht. Het patroon voor een numerieke meting is toch `qudt:numericValue`. Bestaan bewijst
    geen juistheid.

!!! valkuil "`sosa:Result` is verouderd"
    SSN/SOSA 2023 verklaart `sosa:Result` `owl:deprecated`
    ([w3c/sdw-sosa-ssn#113](https://github.com/w3c/sdw-sosa-ssn/issues/113)). Het voegt niets toe:
    elk resultaat is via `sosa:hasResult ⊂ prov:generated` al een `prov:Entity`. Een profiel dat
    een eigen klasse voor zijn resultaten nodig heeft, maakt ze subklasse van `qudt:QuantityValue`
    (zoals `wk:Meetresultaat` in [waterkwaliteit](../casussen/waterkwaliteit.md)).

- **Geen `qudt:unit`.** Die eigenschap bestaat niet in QUDT 3; het is `qudt:hasUnit`.
- **Geen eenheid als datatype.** `"2.4"^^unit:M3` maakt van een eenheid een datatype; een
  eenheid is een resource.
- **Geen eenheid op de eigenschap.** "Temperatuur in °C" is geen eigenschap; temperatuur is de
  eigenschap, °C de eenheid van één resultaat.

## 4. Wanneer `sosa:hasSimpleResult` volstaat

`sosa:hasSimpleResult` geeft het resultaat als literal, zonder eenheid. Dat is verdedigbaar voor
een waarde die geen grootheid is: een tekst, een code, een booleaanse waarde, een telling zonder
eenheid. Zodra er een eenheid, een onzekerheid of een herkomst bij hoort, of zodra het resultaat
inputwaarde van een afgeleide waarneming kan worden, gebruik je `sosa:hasResult` met een
`qudt:QuantityValue`. In twijfel: het resultaat als resource. Het kost één knoop en sluit niets
uit.

## 5. Waar de eenheid vandaan komt

Eén keuze per voorbeeld:

| Bron | Wanneer | Voorbeeld |
|---|---|---|
| **QUDT** (standaard) | de eenheid bestaat in QUDT | `unit:M`, `unit:MilliGM-PER-L`, `unit:DeciB_A` |
| **een domeinregister** | QUDT kan de eenheid niet uitdrukken (gebonden aan een stof: "mg P/L"; `/100mL`; `meq/L`), of het domein heeft een eigen register | CSOR in het Vlaamse omgevingsdomein |

Het tweede geval is een eigen alignment, tussen het register en QUDT:
[Register en QUDT](register-qudt.md).

!!! hulpmiddel "Een QUDT-eenheid vinden"
    QUDT-namen zijn niet te raden: de meter is `unit:M`, niet `unit:Meter`; euro is
    `unit:CCY_EUR`. Zoek op label of symbool in het eenhedenregister van QUDT
    (<https://qudt.org/vocab/unit/>), of met het zoekhulpmiddel van de
    [validatieserver](../bijlagen/hulpmiddelen.md).

## Casussen

- [Erosiepoel](../casussen/erosiepoel.md): `qudt:unit` → `qudt:hasUnit`.
- [Verkeersmetingen](../casussen/verkeersmetingen.md): benoemde resultaten als inputwaarde van een
  dagsom.
- [Waterkwaliteit](../casussen/waterkwaliteit.md): CSOR-eenheden en de rapportagegrens.
- [VLAREM-rubrieken](../casussen/vlarem.md): `qudt:QuantityValue` buiten SOSA, voor een norm.
