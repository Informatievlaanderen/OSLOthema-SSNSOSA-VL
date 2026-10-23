# SOSA en OWL-Time

**Wanneer gebeurde het, en wanneer was het resultaat er?** SOSA onderscheidt die twee vragen;
OWL-Time drukt het antwoord op de eerste uit. De koppeling zit in de definitie van SOSA zelf: de
fenomeentijd "kan een interval, een tijdstip, of een andere samengestelde temporele entiteit zijn
(OWL-Time)".

| | |
|---|---|
| **Soort** | definitie in SOSA, aangevuld met een afspraak |
| **Waar vastgelegd** | regels [R12](../regels/r12.md) en [R9](../regels/r09.md) |

## 1. Drie tijden

| Eigenschap | Wat | Waarde |
|---|---|---|
| `sosa:phenomenonTime` | wanneer het verschijnsel plaatsvond waarop het resultaat slaat | een OWL-Time-entiteit: `time:Instant` of `time:Interval` |
| `sosa:resultTime` | wanneer het resultaat beschikbaar werd | een literal (`xsd:dateTime`, …) |
| `sosa:startTime`, `sosa:endTime` | wanneer de uitvoering zelf begon en eindigde | een literal; ⊂ `prov:startedAtTime`, `prov:endedAtTime` |

De drie vallen vaak samen, maar niet altijd:

- bij een **voorspelling** ligt de fenomeentijd ná de resultaattijd;
- bij **paleoklimaat** ligt de fenomeentijd duizenden jaren terug, de resultaattijd vandaag;
- bij een **labo-analyse** is de fenomeentijd het moment van de staalname, de resultaattijd de
  datum van het analyserapport;
- bij een **uurtelling** is de fenomeentijd het uur, de resultaattijd het moment waarop de teller
  het aantal doorstuurde.

!!! valkuil "PROV-tijden voor het verschijnsel"
    `prov:startedAtTime` en `prov:endedAtTime` zeggen wanneer de *activiteit* liep, niet wanneer
    het *verschijnsel* plaatsvond. Een herziene mapping van de [erosiepoel](../casussen/erosiepoel.md)
    gebruikte ze voor de regenbui; ze zijn vervangen door `sosa:phenomenonTime` en
    `sosa:resultTime`.

## 2. Tijdstip of interval

```turtle
# een puntmeting: het verschijnsel heeft geen duur
ex:peilmeting sosa:phenomenonTime [
    a time:Instant ;
    time:inXSDDateTimeStamp "2026-04-28T08:15:00+02:00"^^xsd:dateTimeStamp
] .

# een periode: uurtelling, dagsom, jaarvracht
ex:uurtelling-08 sosa:phenomenonTime [
    a time:Interval ;
    time:hasBeginning [ a time:Instant ;
        time:inXSDDateTimeStamp "2026-04-28T08:00:00+02:00"^^xsd:dateTimeStamp ] ;
    time:hasEnd [ a time:Instant ;
        time:inXSDDateTimeStamp "2026-04-28T09:00:00+02:00"^^xsd:dateTimeStamp ]
] .
```

- Een **interval** wanneer de waarde een periode dekt: een telling per uur, een daggemiddelde, een
  jaardebiet, een overstortevent.
- Een **tijdstip** enkel voor een puntmeting.
- Intervallen zijn **halfopen**: het begin hoort erbij, het einde niet. 08:00–09:00 is uur 08.

## 3. Altijd een tijdzone

`time:inXSDDateTime` is in OWL-Time **verouderd**, omdat `xsd:dateTime` geen tijdzone vereist.
`time:inXSDDateTimeStamp` met `xsd:dateTimeStamp` maakt de tijdzone verplicht. Geeft de bron geen
tijdzone, dan neem je die van Vlaanderen aan (`Europe/Brussels`: `+01:00` in de winter, `+02:00`
tijdens de zomertijd, van de laatste zondag van maart tot de laatste zondag van oktober), en vermeld
je die aanname in de bespreking. Geeft de bron er wel een (`Z`, `+00:00`), dan behoud je ze.

Een datum zonder uur: `time:inXSDDate`. Enkel een jaar: `time:inXSDgYear`.

## 4. Tijd die geen kalender is

Een C14-leeftijd van een luchtbel in een ijskern wordt niet in kalenderjaren uitgedrukt, maar in
jaren *Before Present*. OWL-Time laat elke tijdschaal toe via een tijdreferentiesysteem:

```turtle
ex:co2-waarneming sosa:phenomenonTime [
    a time:Instant ;
    time:inTimePosition [
        a time:TimePosition ;
        time:numericPosition 7530 ;
        time:hasTRS ex:BP
    ]
] .
ex:BP a time:TRS ;
    skos:prefLabel "Before Present"@en ;
    skos:definition "Jaren vóór 1950, de referentie van radiokoolstofdatering."@nl .
```

Regel [R9](../regels/r09.md): een benoemd `time:TRS`, beschreven met `skos:prefLabel` en
`skos:definition`. De casus [paleoklimaat](../casussen/paleo.md) gebruikt het.

## 5. Tijd op een collectie

Een `sosa:ObservationCollection` mag een fenomeentijd hebben. SOSA 2023 legt de betekenis vast:
heeft de collectie één waarde of een interval, dan moet de fenomeentijd van elk lid daarmee
overeenkomen of erbinnen vallen. Een dagcollectie met het interval van de dag kan dus 24 leden
met elk een uurinterval bevatten.

## 6. In grote datasets

Een blanco knoop voor elk tijdstip en interval is handig in een klein voorbeeld, maar moeilijk te
bevragen en samen te voegen in een grote dataset. Daar krijgen intervallen en tijdstippen een
deterministische IRI, afgeleid van de waarneming: `ex:interval-{waarneming}`,
`ex:tijdstip-{waarneming}-begin` ([R10](../regels/r10.md)). De casus
[R-factor](../casussen/r-factor.md) doet dat.

## Casussen

- [Verkeersmetingen](../casussen/verkeersmetingen.md): uurintervallen en een dagsom.
- [Overstort](../casussen/overstort.md): een event als interval in plaats van eigen start- en
  eindvelden.
- [Paleoklimaat](../casussen/paleo.md): jaren *Before Present*.
- [Geluidsmeetnet](../casussen/geluidsmeetnet.md): tijdstempels zonder tijdzone in de bron.
