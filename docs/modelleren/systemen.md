# Wie of wat meet of handelt?

## Systemen

SOSA noemt wie of wat een uitvoering doet een **systeem** (`sosa:System`), met drie concrete
soorten:

| Klasse | Doet | Voorbeelden |
|---|---|---|
| `sosa:Sensor` | waarnemen: de waarde van een eigenschap bepalen | een drukopnemer, een fietsteller, een laboranalist, een rekenmodel, een veldwaarnemer |
| `sosa:Actuator` | handelen: de toestand van iets wijzigen | een raamopener, een klep, een stuurprogramma |
| `sosa:Sampler` | bemonsteren: een monster nemen | een staalnemer, een boortoestel |

Een sensor is **niet noodzakelijk een toestel**. SOSA definieert hem als een agent die een
waarnemingsprocedure uitvoert: "een toestel, een stuk infrastructuur, een agent (ook een mens) of
een softwaresysteem, ook voor simulaties". In de voorbeelden is een sensor:

- een veldwaarnemer van de stad ([erosiepoel](../casussen/erosiepoel.md));
- de rekenmodule van Aerovision die dagindicatoren berekent ([geluidsmeetnet](../casussen/geluidsmeetnet.md));
- een QGIS-model dat een geschiktheidskaart maakt ([PGD](../casussen/pgd.md)).

`sosa:System` zelf is abstract: type een concreet systeem als sensor, actuator of bemonsteraar.

Een systeem kan uit delen bestaan (`sosa:hasSubSystem`), en implementeert een procedure
(`sosa:implements`). Wat het waarneemt of waarop het inwerkt, zeg je met `sosa:observes`
(sensor), `sosa:actsOn` (actuator) of het algemene `sosa:forProperty`.

## Platformen

Een **platform** (`sosa:Platform`) draagt of herbergt systemen: een meetpost, een paal, een
gebouw, een boei, een satelliet, een erosiepoel waar een waarnemer staat.

```turtle
ex:meetpost-M072 a sosa:Platform ;
    sosa:hosts ex:geluidsmeter-M072 .
ex:geluidsmeter-M072 a sosa:Sensor ;
    sosa:isHostedBy ex:meetpost-M072 ;
    sosa:observes ex:geluidsdrukniveau .
```

Platformen kunnen genest zijn: een gebouw herbergt een lokaal, dat een sensor herbergt.

## Inzet

Een **inzet** (`sosa:Deployment`) is de opstelling van systemen op een platform, voor een doel,
gedurende een periode. Het is de plaats om te zeggen waarop een systeem gericht is:

```turtle
ex:campagne-M072-2 a sosa:Deployment ;
    sosa:deployedSystem ex:geluidsmeter-M072 ;
    sosa:deployedOnPlatform ex:meetpost-M072 ;
    sosa:hasFeatureOfInterest ex:meetpost-M072 .
```

Een inzet is een `prov:Activity` ([SOSA en PROV-O](../samenhang/sosa-prov.md)): ze loopt over een
periode. Een meetcampagne is daar een goed voorbeeld van.

## Wat niet op een systeem hoort

!!! valkuil "Uitvoeringseigenschappen op een sensor"
    `ex:sensor sosa:hasFeatureOfInterest ex:meetpunt` lijkt logisch (de sensor meet het meetpunt),
    maar `sosa:hasFeatureOfInterest` is een subproperty van `prov:used`, met als domein
    `prov:Activity`. De sensor wordt zo een activiteit, terwijl hij als systeem een entiteit is:
    een tegenspraak. Hetzelfde geldt voor `sosa:usedProcedure`, `sosa:hasResult`,
    `prov:startedAtTime` op een sensor of platform.

Wat je wilde zeggen, heeft een eigen plaats:

| Je wil zeggen | Gebruik |
|---|---|
| welke eigenschap de sensor waarneemt | `sosa:observes` (of `sosa:forProperty`) |
| waarop de actuator inwerkt | `sosa:actsOn` |
| waarop het systeem gericht is | een `sosa:Deployment` met `sosa:hasFeatureOfInterest` |
| waar het systeem staat | `sosa:isHostedBy` het platform |
| welke werkwijze het volgt | `sosa:implements` de procedure |

`sosa:observedProperty` op een sensor geeft geen tegenspraak (die eigenschap heeft geen
PROV-domein), maar is tegen de definitie: ze hoort op de waarneming ([R16](../regels/r16.md)).

## Een getraind model

Een machinaal-leermodel is geen sensor. Het is een **artefact**, een `prov:Entity` gegenereerd door
een trainingsactiviteit. De software die het model gebruikt om voorspellingen te maken, is de
sensor; elke voorspelling (een waarneming) **gebruikt** het model ([R6](../regels/r06.md)):

```turtle
ex:voorspellingsmodel a it6:MachineLearningModel , prov:Entity ;
    prov:wasGeneratedBy [ a prov:Activity ; prov:used ex:trainingsdata ] .

ex:voorspeller a sosa:Sensor ;
    sosa:implements ex:voorspellingsprocedure .

ex:voorspelling-1 a sosa:Observation ;
    sosa:madeBySensor ex:voorspeller ;
    prov:used ex:voorspellingsmodel ;
    sosa:hasInputValue ex:historische-data ;
    sosa:hasResult ex:voorspeld-tijdstip .
```

`prov:used` en niet `sosa:hasInputValue`, omdat het model geen waarde is voor een input die de
procedure definieert, maar een hulpmiddel van de uitvoering. De casus
[energiemanagement](../casussen/ems.md) (voorverwarming) werkt het uit.
