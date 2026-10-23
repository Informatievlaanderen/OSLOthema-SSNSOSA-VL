# Ontologie en toepassingsprofiel

Wanneer een domein eigen klassen, eigenschappen of verplichtingen nodig heeft, komt er een
ontologie, en meestal een toepassingsprofiel dat zegt wat een dataset moet bevatten. Het
uitgewerkte voorbeeld is `waterkwaliteit.ttl`
([casus waterkwaliteit](../casussen/waterkwaliteit.md), beslispunten A14–A15).

## Principes

**Eén bron.** Schrijf de ontologie en de beperkingen van het profiel in één OWL-bestand, en
genereer de SHACL uit de OWL-restricties. Geen handmatig onderhouden SHACL ernaast: twee bronnen
lopen uit elkaar.

**Hergebruiken, dan specialiseren.** Hergebruik SOSA, PROV-O, QUDT, OWL-Time, GeoSPARQL en de
registers. Definieer een eigen klasse enkel waar het domein eigen beperkingen of betekenis nodig
heeft, als **subklasse** van de hergebruikte klasse:

```turtle
wk:WaterkwaliteitObservatie rdfs:subClassOf sosa:Observation ;
    rdfs:subClassOf [ a owl:Restriction ;
        owl:onProperty sosa:observedProperty ;
        owl:someValuesFrom csor:ParameterAspect ] .
wk:Meetresultaat rdfs:subClassOf qudt:QuantityValue .
```

**Beperk je eigen subklassen, nooit hergebruikte klassen.** Een restrictie op
`sosa:Observation` zou gelden voor elke SOSA-dataset en elk ander profiel dat SOSA hergebruikt.
De data typeert de eigen subklasse én de hergebruikte superklasse expliciet, zodat ze ook geldig
blijft voor een SHACL-validator die geen klassehiërarchie kent.

De enige uitzondering is een **versoepeling**: een `owl:minCardinality 0` die een ondergrens van
een hergebruikt vocabularium opheft (QUDT's `qudt:hasQuantityKind` op `qudt:Unit`, voor
register-eenheden). Die moet op de hergebruikte klasse, want op een subklasse heft ze niets op.
Ze voegt geen beperking toe, maar versoepelt wel de vormen voor alles wat met deze ontologie
gevalideerd wordt; zeg dat in het commentaar en de bespreking.

**Uitlijnen met subklassen en OWL**, niet met SKOS ([R15](../regels/r15.md)).

## Van OWL naar SHACL

| OWL-restrictie | Betekenis in het profiel |
|---|---|
| `owl:someValuesFrom C` | minstens één waarde is een C (verplicht, met type) |
| `owl:allValuesFrom C` | elke waarde is een C (niet verplicht) |
| `owl:cardinality`, `minCardinality`, `maxCardinality n` | aantal waarden |
| gekwalificeerde kardinaliteit (`owl:onClass`) | aantal waarden van een type |
| `owl:hasValue v` | deze waarde moet er zijn |
| `owl:unionOf (A B)` als waarde | een A of een B |
| `owl:minCardinality 0` | heft elke ondergrens op dezelfde klasse en eigenschap op (conventie van de generator) |

De generator leest de restricties als eisen aan de data: een profiellezing. OWL zelf maakt een
ontbrekende waarde nooit een fout.

**Wat de generator niet uitdrukt:** een keuze tussen eigenschappen ("`numericValue` of
`upperBound`"), samenhang tussen een collectie en haar leden, labels van eigenschappen in de
context van het profiel. Documenteer die apart.

!!! valkuil "Kardinaliteit op `sosa:usedProcedure`"
    `owl:maxCardinality 1` op `sosa:usedProcedure` lijkt onschuldig, maar de eigenschap heeft een
    keten van eigenschappen (in `sosa-prov`), en in OWL 2 DL mag zo'n eigenschap niet in een
    kardinaliteitsrestrictie. Wil een profiel één procedure, dan met SHACL op de gegeven data
    ([P-PLAN en SOSA](../samenhang/pplan-sosa.md#4-wat-de-ketens-nog-niet-doen)).

## Stappen

1. **Verzamel de eisen** uit de datavoorbeelden: welke klassen ze typeren, welke eigenschappen ze
   gebruiken, met welke kardinaliteit.
2. **Schrijf klassen en restricties.**
3. **Zoek elke term op**: bestaat hij, is hij niet verouderd, passen domein en bereik?
4. **Toets de voorbeelden** tegen de gegenereerde vormen: elke fout wijst op een fout in een
   voorbeeld, of op een restrictie die te streng is.
5. **Toets de ontologie zelf** (ook R15 geldt voor ontologiebestanden).
6. **Genereer het UML-diagram** uit de ontologie, in plaats van het te tekenen.
7. **Map het oude profiel**, als er een is: een tabel *oud → nieuw*, met wat verdwijnt en wat open
   ligt.

## Wat het oplevert

De ontologie (in de map met geladen ontologieën), het gegenereerde UML-diagram, de
mappingtabel van het oude profiel, en de beslispunten.
