# Waarneming of record?

Een vraag die pas opduikt wanneer data gepubliceerd wordt, maar dan meteen: **is wat je
publiceert de waarneming zelf, of een record over de waarneming?** Een LDES-member, een versie, een
rij in een database: ze hebben een aanmaakdatum, een wijzigingsdatum, een versieketen, soms een
verwijdervlag. De waarneming heeft dat niet. Zij is het meten, tijdens haar fenomeentijd.

## Waarom het ertoe doet

Een waarneming is een `prov:Activity` ([SOSA en PROV-O](../kaart/sosa-prov.md)). Een record is een
ding dat door een pipeline gegenereerd werd: een `prov:Entity`. Wie de eigenschappen van het record
op de waarneming zet, maakt ze tot entiteit.

```turtle
# fout: één resource voor beide
ex:event-4004f4ea a sosa:Observation ;
    sosa:phenomenonTime ex:interval-event ;     # het meten: 18 februari 2024, 20:45–20:46
    prov:generatedAtTime "2025-08-26T08:49:13Z"^^xsd:dateTime ;   # het record: 26 augustus 2025
    dct:isVersionOf ex:event-basis .
```

Het domein van `prov:generatedAtTime` is `prov:Entity`; de waarneming wordt zo tegelijk activiteit
en entiteit, wat PROV-O uitsluit. Dat is wat de [overstort](../casussen/overstort.md)-mapping van
Aquafin deed.

## Twee oplossingen

| | **A. De waarneming is de gepubliceerde resource** | **B. Een apart record** |
|---|---|---|
| wat | enkel eigenschappen zonder PROV-domein op de waarneming: `dct:modified` (als tijdstempel van de stroom), `dct:isVersionOf` (versieketen); geen `prov:generatedAtTime` | de gepubliceerde resource is een `prov:Entity` met de recordeigenschappen, die naar de waarneming verwijst (bv. `foaf:primaryTopic`) |
| voor | consistent; een client die versies materialiseert, krijgt waarnemingen; weinig wijziging | elke eigenschap staat op het juiste object; de herkomst van het record is expliciet |
| tegen | record en waarneming vallen nog samen; `dct:modified` op een activiteit is strikt genomen even fout, alleen merkt geen redeneerder het | versiematerialisatie levert records op, geen waarnemingen; een stap meer navigeren; een extra resource per waarneming |

```turtle
# B: het record verwijst naar de waarneming
ex:record-4004f4ea-v3 a prov:Entity ;
    prov:generatedAtTime "2025-08-26T08:49:13Z"^^xsd:dateTime ;
    dct:isVersionOf ex:record-4004f4ea ;
    foaf:primaryTopic ex:event-4004f4ea .
ex:event-4004f4ea a sosa:Observation ;
    sosa:phenomenonTime ex:interval-event .
```

Niet `prov:wasDerivedFrom` van record naar waarneming: het bereik daarvan is `prov:Entity`, en dat
brengt dezelfde botsing terug.

!!! regel "Kies bewust"
    Beide oplossingen zijn verdedigbaar. Kies er een, en zeg in de bespreking welke en waarom
    ([R16](../regels/r16.md), fout 1). De overstortherziening volgt voorlopig A; de keuze ligt voor
    bij de databeheerder en de werkgroep.

## Ook voor systemen

Een sensorrecord met `valid_from`, `valid_to`, `is_deleted` en `modified_at` beschrijft de versie
van het record, niet het toestel. Daar geeft het geen tegenspraak (een sensor is ook een entiteit),
maar de verwarring is dezelfde: wanneer was het toestel actief, en wanneer werd het record
gewijzigd? Houd die twee uit elkaar.

## Stabiele IRI's

Een versieketen werkt enkel met stabiele IRI's. Een pipeline die per run een willekeurige IRI
maakt (`STRUUID()`), breekt de keten: `dct:isVersionOf` wijst telkens naar een nieuwe basis-IRI
([IRI's](iris.md)).
