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

## Statistieken per periode

Minimum, maximum en gemiddelde per uur, dag of jaar vormen ook zo'n keten: uurindicatoren uit de
ruwe waarden, dagindicatoren uit de uurindicatoren ([ELF-meetnet](../casussen/elf.md)).

```turtle
ex:obs-ELF_C_0020-20251127-maximum a sosa:Observation ;
    sosa:usedProcedure ex:procedure-maximum ;
    sosa:observedProperty ex:prop-RMStotal ;
    sosa:phenomenonTime ex:interval-ELF_C_0020-20251127 ;          # de lokale dag
    sosa:hasInputValue ex:result-ELF_C_0020-20251127T00-maximum ,  # de 24 uurmaxima
        ex:result-ELF_C_0020-20251127T01-maximum ;                 # …
    sosa:relatedObservation ex:obs-ELF_C_0020-20251127T00-maximum ;
    sosa:hasResult ex:result-ELF_C_0020-20251127-maximum .
```

- **Minimum en maximum** gaan exact over: het maximum van de uurmaxima is het dagmaximum.
- **Een gemiddelde van uurgemiddelden** weegt elk uur even zwaar, ook als er ruwe waarden ontbreken
  binnen een uur: een tijdgewogen gemiddelde. Een gemiddelde over alle ruwe waarden van de dag doet dat
  niet. Zeg in de procedure welk van de twee het is.
- **De statistiek zit in de procedure, de periode in `sosa:phenomenonTime`.** De waargenomen
  eigenschap blijft dezelfde, zoals bij de dagsom van de [verkeersmetingen](../casussen/verkeersmetingen.md).
  Een eigen eigenschap krijgt een indicator pas wanneer een norm hem een eigen naam en definitie geeft
  (Lden).

## Waarom het samenhangt met de kernvocabularia

`sosa:hasInputValue ⊂ prov:used` en `sosa:hasResult ⊂ prov:generated`: de berekening is een
PROV-keten *activiteit genereert entiteit, die door de volgende activiteit gebruikt wordt*. Een
waarneming als inputwaarde zou een activiteit tot entiteit maken: inconsistent
([SOSA en PROV-O](../samenhang/sosa-prov.md)).

## Gebruikt in

- [Verkeersmetingen](../casussen/verkeersmetingen.md): dagsom uit 24 uurtellingen.
- [Geluidsmeetnet](../casussen/geluidsmeetnet.md): dagindicatoren uit events, Lden uit Ld, Le, Ln
  (nagerekend voor alle 13 campagnes).
- [ELF-meetnet](../casussen/elf.md): uurminimum, -maximum en -gemiddelde uit minuutwaarden,
  dagindicatoren uit de uurindicatoren.
- [Paleoklimaat](../casussen/paleo.md): CO₂-concentratie op een leeftijd, uit twee waarnemingen.
- [Waterkwaliteit](../casussen/waterkwaliteit.md): vrachten uit concentratie en debiet.
- [Geschiktheidskaart PGD](../casussen/pgd.md): kansrijkheid uit drie factorscores.

## Zie ook

[Hoe is het berekend?](../modelleren/afgeleid.md)

??? quote "Normatieve tekst (modelleergids, Engels)"

    --8<-- "kit/patroon-afgeleide-waarneming.md"
