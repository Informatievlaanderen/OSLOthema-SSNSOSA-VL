# Register en QUDT

**Wanneer QUDT de eenheid niet kent.** "Milligram fosfor per liter" is geen QUDT-eenheid: QUDT
kent milligram per liter, maar niet gebonden aan een stof. Het Vlaamse omgevingsdomein heeft daarom
een eigen eenhedenregister, CSOR, dat waar mogelijk naar QUDT verwijst. De alignment tussen beide
staat in het register, niet in de data.

| | |
|---|---|
| **Soort** | SKOS-mapping tussen begrippen, in het register zelf |
| **Register** | CSOR-eenheden, `https://data.omgeving.vlaanderen.be/id/conceptscheme/csor/eenheid` |
| **Waar vastgelegd** | regel [R3](../regels/r03.md); casus [waterkwaliteit](../casussen/waterkwaliteit.md), beslispunt A2 |

## 1. Hoe het register naar QUDT verwijst

```turtle
csor-eenheid:E_1 a skos:Concept , csor:Eenheid ;
    skos:prefLabel "milligram per liter"@nl ;
    csor:symbool "mg/L" ;
    skos:exactMatch unit:MilliGM-PER-L .

csor-eenheid:E_131 a skos:Concept , csor:Eenheid ;
    skos:prefLabel "milligram fosfor per liter"@nl ;
    csor:symbool "mgP/L" ;
    skos:broader csor-eenheid:E_1 ;
    skos:broadMatch unit:MilliGM-PER-L .
```

- **`skos:exactMatch`**: de register-eenheid is dezelfde als de QUDT-eenheid (mg/L).
- **`skos:broadMatch`**: de QUDT-eenheid is ruimer; de register-eenheid voegt iets toe (de stof
  waarop de massa slaat). Een waarde in mgP/L is óók een waarde in mg/L, maar niet omgekeerd.
- Binnen het register ordent `skos:broader` de eenheden: mgP/L is een soort mg/L.

Van de 360 CSOR-eenheden in dit project hebben er 163 een QUDT-mapping: 50 exact, 113 ruimer.

Dit is precies waarvoor SKOS-mappings bedoeld zijn: relaties tussen **begrippen** in codelijsten.
Tussen **klassen** horen ze niet ([R15](../regels/r15.md)).

## 2. Wat de data doet

```turtle
ex:resultaat-1 a qudt:QuantityValue ;
    qudt:numericValue 0.42 ;
    qudt:hasUnit csor-eenheid:E_131 .
```

De data verwijst naar de register-eenheid. Ze herhaalt de mapping niet en voegt er geen toe.

!!! regel "Mappings horen in het register"
    Een SKOS-mapping is een uitspraak over een begrip van het register, in de namespace van het
    register. Zet ze niet in de data. Ontbreekt een mapping, of klopt er een niet, dan is dat een
    punt voor de beheerder van het register (in een beslisdocument: deel C).

Wie de waarde in QUDT-termen wil, volgt de mapping in een query:

```sparql
SELECT ?waarde ?qudtEenheid WHERE {
  ?r qudt:numericValue ?waarde ; qudt:hasUnit ?eenheid .
  ?eenheid skos:exactMatch|skos:broadMatch ?qudtEenheid .
}
```

## 3. De twee klassen van een register-eenheid

`qudt:hasUnit` verwacht een `qudt:Unit` (het bereik). Een redeneerder leidt dat type af, maar een
validatie met SHACL ziet enkel wat er staat. Daarom:

- wanneer de data een register-eenheid **beschrijft** (ze typeert met de klasse van het register),
  typeert ze haar ook `qudt:Unit`: `csor-eenheid:E_131 a csor:Eenheid , qudt:Unit`;
- een eenheid waar de data **enkel naar verwijst**, heeft geen typering nodig.

QUDT vraagt van elke `qudt:Unit` een grootheidssoort (`qudt:hasQuantityKind`) en een
dimensievector (`qudt:hasDimensionVector`). Een register-eenheid heeft die meestal niet. Ze horen
niet in de data (wel in het register). Het toepassingsprofiel versoepelt die eis met
`owl:minCardinality 0` op `qudt:Unit` voor beide eigenschappen. Dat is de enige plaats waar een
profiel een hergebruikte klasse mag aanraken: een versoepeling, geen beperking
([Ontologie en toepassingsprofiel](../werkwijze/ontologie.md)).

## 4. QUDT of register: één keuze per voorbeeld

| | QUDT | Register |
|---|---|---|
| wanneer | de eenheid bestaat in QUDT en het domein heeft geen eigen register | stofgebonden eenheden, domeineigen eenheden, of een domein met een gangbaar register |
| voordeel | internationaal, met dimensies en omrekening | sluit aan op de bron, dekt alle eenheden van het domein |
| nadeel | dekt niet alles | omrekening en dimensie via de mapping, voor zover die bestaat |

Meng beide niet binnen één voorbeeld: een query die op `qudt:hasUnit` filtert, moet niet twee
soorten eenheden naast elkaar verwachten. Vermeld de keuze, en bij een register de mapping naar
QUDT, in de bespreking.

## Casussen

- [Waterkwaliteit](../casussen/waterkwaliteit.md): CSOR-eenheden voor concentraties, vrachten en
  debieten.
- [R-factor](../casussen/r-factor.md): een eigen eenheid (MJ·mm/(ha·h·jaar)) die in QUDT
  ontbreekt.
