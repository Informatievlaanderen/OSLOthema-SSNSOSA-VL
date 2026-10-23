# III. Modelleren per vraag

Een modelleerder vertrekt niet van een vocabularium, maar van een dataset en een paar vragen. Dit
hoofdstuk volgt die vragen. Elke pagina geeft het antwoord van de kernvocabularia, de keuzes die
verdedigbaar zijn, en hoe je kiest.

## De vragen

| Vraag | Begrippen | Pagina |
|---|---|---|
| **Wat bestudeer ik?** Waarover gaat de waarde? | studieobject, monster, uiteindelijk studieobject, eigenschap | [Wat bestudeer ik?](studieobject.md) |
| **Wie of wat meet of handelt?** | sensor, actuator, bemonsteraar, platform, inzet | [Wie of wat meet of handelt?](systemen.md) |
| **Wat is het resultaat?** | grootheidswaarde, eenheid, eenvoudig resultaat, rapportagegrens | [Wat is het resultaat?](resultaat.md) |
| **Wanneer?** | fenomeentijd, resultaattijd, tijdstip, interval | [Wanneer?](tijd.md) |
| **Waar?** | geometrie, ruimtelijk monster, locatie | [Waar?](plaats.md) |
| **Hoe is het berekend?** | afgeleide waarneming, inputwaarde, gerelateerde waarneming | [Hoe is het berekend?](afgeleid.md) |
| **Volgens welk plan?** | procedure, plan, stap, variabele; plat of drielaags | [Volgens welk plan?](plan.md) |
| **Publiceer ik de waarneming of een record erover?** | waarneming, record, versie | [Waarneming of record?](record.md) |
| **Welke waarden komen uit een lijst?** | codelijst, register, SKOS | [Codelijsten en registers](codelijsten.md) |
| **Hoe noem ik de dingen?** | IRI, blanco knoop, skolem-IRI | [IRI's](iris.md) |

## Het skelet van elke waarneming

Wat de vragen ook opleveren, het skelet blijft hetzelfde:

```turtle
ex:waarneming a sosa:Observation ;
    sosa:hasFeatureOfInterest ex:studieobject ;   # waarover        (verplicht)
    sosa:observedProperty     ex:eigenschap ;     # wat             (verplicht)
    sosa:hasResult            ex:resultaat ;      # de waarde       (verplicht: dit of hasSimpleResult)
    sosa:madeBySensor         ex:sensor ;         # door wie        (sterk aanbevolen)
    sosa:usedProcedure        ex:procedure ;      # volgens welke werkwijze (sterk aanbevolen)
    sosa:phenomenonTime       ex:periode ;        # wanneer
    sosa:resultTime           "2026-04-28T09:00:05+02:00"^^xsd:dateTime . # wanneer beschikbaar
```

De eerste drie zijn verplicht ([R2](../regels/r02.md)); sensor en procedure zijn sterk aanbevolen,
want zonder kan niemand de waarde beoordelen. Een actuatie (`sosa:Actuation`) en een bemonstering
(`sosa:Sampling`) hebben hetzelfde skelet, met `sosa:actsOnProperty` en `sosa:madeByActuator`,
respectievelijk een monster als resultaat en `sosa:madeBySampler`.

## Collecties

Komen veel waarnemingen met dezelfde context (dezelfde sensor, hetzelfde studieobject, dezelfde
eigenschap), zet die context dan op een `sosa:ObservationCollection`. SOSA 2023 bepaalt dat de
leden de enkelvoudige waarden van de collectie erven:

```turtle
ex:dagcollectie a sosa:ObservationCollection ;
    sosa:hasFeatureOfInterest ex:meetpunt ;
    sosa:observedProperty ex:verkeersintensiteit ;
    sosa:madeBySensor ex:teller ;
    sosa:usedProcedure ex:telprocedure ;
    sosa:hasMember ex:uurtelling-00 , ex:uurtelling-01 , ex:uurtelling-02 .   # …

ex:uurtelling-08 a sosa:Observation ;
    sosa:phenomenonTime ex:interval-08 ;
    sosa:hasResult ex:resultaat-08 .
```

Een collectie loont van zodra er gedeelde context is, ook bij één waarneming die later kan
aangroeien. Een afgeleide waarneming (een dagsom) hoort **niet** in de collectie van haar bronnen
([Hoe is het berekend?](afgeleid.md)).

## Plat of drielaags

De meeste datasets passen in het **platte model**: infrastructuur, procedure en waarneming. Het
**drielaagse model** (planning, inzet, uitvoering) is er voor processen in meerdere stappen, voor
een werkwijze die op meerdere plaatsen draait, of wanneer traceerbaarheid naar een plan vereist
is ([Volgens welk plan?](plan.md)).
