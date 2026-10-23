# Afgeleide waarneming

**Berekend uit de resultaten van andere waarnemingen.** `sosa:hasInputValue` naar de
bron*resultaten*, `sosa:relatedObservation` naar de bron*waarnemingen*; geen lid van de collectie
van de bronnen; alle verplichte eigenschappen expliciet ([R7](../regels/r07.md),
[R13](../regels/r13.md)). Ketens zijn toegelaten.

## Het patroon

```turtle
ex:lden a sosa:Observation ;
    sosa:hasFeatureOfInterest ex:meetpost-M072 ;
    sosa:observedProperty ex:Lden ;
    sosa:madeBySensor ex:aerovision-rekenmodule ;
    sosa:usedProcedure ex:procedure-Lden ;
    sosa:hasInputValue ex:resultaat-Ld , ex:resultaat-Le , ex:resultaat-Ln ;
    sosa:relatedObservation ex:Ld , ex:Le , ex:Ln ;
    sosa:hasResult ex:resultaat-Lden .
```

Lden is hier een afgeleide van afgeleiden: Ld, Le en Ln zijn zelf berekend uit de events van de
dag.

## Waarom het past in de kaart

`sosa:hasInputValue ⊂ prov:used` en `sosa:hasResult ⊂ prov:generated`: de berekening is een
PROV-keten *activiteit genereert entiteit, die door de volgende activiteit gebruikt wordt*. Een
waarneming als inputwaarde zou een activiteit tot entiteit maken: inconsistent
([SOSA en PROV-O](../kaart/sosa-prov.md)).

## Gebruikt in

- [Verkeersmetingen](../casussen/verkeersmetingen.md): dagsom uit 24 uurtellingen.
- [Geluidsmeetnet](../casussen/geluidsmeetnet.md): dagindicatoren uit events, Lden uit Ld, Le, Ln
  (nagerekend voor alle 13 campagnes).
- [Paleoklimaat](../casussen/paleo.md): CO₂-concentratie op een leeftijd, uit twee waarnemingen.
- [Waterkwaliteit](../casussen/waterkwaliteit.md): vrachten uit concentratie en debiet.
- [Geschiktheidskaart PGD](../casussen/pgd.md): kansrijkheid uit drie factorscores.

## Zie ook

[Hoe is het berekend?](../modelleren/afgeleid.md)

??? quote "Normatieve tekst (modelleergids, Engels)"

    --8<-- "kit/patroon-afgeleide-waarneming.md"
