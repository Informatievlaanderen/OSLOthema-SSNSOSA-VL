# Wanneer?

Het hoofdstuk [SOSA en OWL-Time](../samenhang/sosa-time.md) beschrijft het model; deze pagina geeft
de beslissingen in volgorde.

## 1. Welke tijd geeft de bron?

| De bron zegt … | Dat is | Eigenschap |
|---|---|---|
| wanneer het verschijnsel plaatsvond (meetmoment, telperiode, datum van de staalname) | de fenomeentijd | `sosa:phenomenonTime` |
| wanneer het resultaat beschikbaar was (rapportdatum, verzendtijd) | de resultaattijd | `sosa:resultTime` |
| wanneer het toestel startte en stopte | begin en einde van de uitvoering | `sosa:startTime`, `sosa:endTime` |
| wanneer het record aangemaakt of gewijzigd werd | een eigenschap van het **record**, niet van de waarneming | zie [Waarneming of record?](record.md) |

Een bron met één tijdstip geeft meestal de fenomeentijd. Zeg in de bespreking hoe je dat las.

## 2. Tijdstip of interval?

- **Interval** (`time:Interval` met `time:hasBeginning` en `time:hasEnd`) als de waarde een
  periode dekt: uurtelling, daggemiddelde, jaarvracht, event van een minuut tot een uur.
- **Tijdstip** (`time:Instant`) enkel voor een puntmeting zonder duur.
- Intervallen zijn **halfopen**: begin inbegrepen, einde niet.

!!! valkuil "Eigen velden voor begin en einde"
    `ex:event_start_time` en `ex:event_end_time` zijn voor geen enkele SOSA-toepassing vindbaar,
    en bestaan in geen vocabularium. Een periode is een `time:Interval` op de fenomeentijd
    ([casus overstort](../casussen/overstort.md), verbeterpunt 4).

## 3. Welke waarde?

| Precisie | Eigenschap op het `time:Instant` | Datatype |
|---|---|---|
| datum en uur | `time:inXSDDateTimeStamp` | `xsd:dateTimeStamp` (tijdzone verplicht) |
| datum | `time:inXSDDate` | `xsd:date` |
| jaar | `time:inXSDgYear` | `xsd:gYear` |
| niet-kalender (jaren BP, geologische tijd) | `time:inTimePosition` met `time:hasTRS` | ([R9](../regels/r09.md)) |

Gebruik **nooit** `time:inXSDDateTime`: OWL-Time verklaart het verouderd.

## 4. Welke tijdzone?

- De bron geeft een tijdzone (`Z`, `+00:00`, `+02:00`): behouden.
- De bron geeft er geen: `Europe/Brussels` aannemen, `+01:00` in de winter en `+02:00` tijdens
  de zomertijd (van de laatste zondag van maart tot de laatste zondag van oktober), en die aanname
  in de bespreking vermelden.
- Gemengde bronnen: normaliseren. In het [geluidsmeetnet](../casussen/geluidsmeetnet.md) stonden
  sommige kolommen in lokale tijd met offset en andere zonder offset in UTC; alles werd omgezet
  naar lokale tijd met offset.

## 5. Blanco knoop of IRI?

In een klein voorbeeld een blanco knoop; in een grote, gescripte dataset een deterministische IRI
afgeleid van de waarneming (`ex:interval-{id}`, `ex:tijdstip-{id}-begin`) ([R10](../regels/r10.md)).

## Samengevat

```turtle
ex:uurtelling-08 sosa:phenomenonTime [
        a time:Interval ;
        time:hasBeginning [ a time:Instant ; time:inXSDDateTimeStamp "2026-04-28T08:00:00+02:00"^^xsd:dateTimeStamp ] ;
        time:hasEnd       [ a time:Instant ; time:inXSDDateTimeStamp "2026-04-28T09:00:00+02:00"^^xsd:dateTimeStamp ]
    ] ;
    sosa:resultTime "2026-04-28T09:00:05+02:00"^^xsd:dateTime .
```
