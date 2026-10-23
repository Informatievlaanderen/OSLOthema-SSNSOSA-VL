# SOSA en SAREF

**Wanneer gebouwen, toestellen en energie in beeld komen.** SAREF (*Smart Applications REFerence
ontology*, ETSI) is de Europese norm voor slimme toestellen, met uitbreidingen voor gebouwen,
energie en systemen. SSN/SOSA 2023 publiceert een uitlijning met SAREF. Ze is een goed voorbeeld
van waarom je een alignment moet zoeken waar je ze niet verwacht.

| | |
|---|---|
| **Module** | `sosa-saref` (`http://www.w3.org/ns/sosa/saref`), versie 2023 |
| **Uitgever** | W3C/OGC, onderdeel van SSN/SOSA 2023 (niet van SAREF) |
| **Lijnt uit met** | SAREF core v4.1.1 en SAREF4SYST v1.1.2 |
| **Specificatie** | <https://www.w3.org/TR/vocab-ssn-2023/#SAREF-alignment> |
| **Bestand in dit project** | [`src/main/resources/org/w3/www/ns/sosa/alignments/sosa-saref.ttl`](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/resources/org/w3/www/ns/sosa/alignments/sosa-saref.ttl) |

## 1. Wat de module zegt (selectie)

| SOSA | | SAREF | Gevolg |
|---|---|---|---|
| `sosa:Observation`, `sosa:Actuation` | ≡ | `saref:Observation`, `saref:Actuation` | dezelfde klassen |
| `sosa:Execution` | ≡ | `saref:ProcedureExecution` | SAREF nam het begrip over uit de *Procedure Execution ontology*; SOSA hernoemde het naar `sosa:Execution` |
| `sosa:hasResult`, `sosa:phenomenonTime`, `sosa:resultTime` | ≡ | `saref:hasResult`, `saref:hasPhenomenonTime`, `saref:hasResultTime` | dezelfde eigenschappen |
| `sosa:madeBySystem` | ≡ | `saref:madeBy` | |
| `sosa:usedProcedure` | ≡ | `saref:isExecutionOf` | |
| `saref:Device` | ⊂ | `sosa:System` | een SAREF-toestel is een systeem; omgekeerd niet, want een SOSA-systeem kan ook een mens of software zijn |
| `saref:Sensor` | ⊂ | `sosa:Sensor` | idem: een SAREF-sensor is tastbaar, een SOSA-sensor niet noodzakelijk |
| `saref:Property`, `saref:PropertyOfInterest`, `saref:State`, `saref:StateOfInterest` | ⊂ | `sosa:Property` | ook een toestand (open, dicht) is een SOSA-eigenschap |
| `sosa:Asset` | ⊂ | `saref:FeatureOfInterest`, `s4syst:System` | elk systeem en platform is een SAREF-studieobject |
| `sosa:FeatureOfInterest`, `sosa:Sample` | ⊂ | `saref:FeatureOfInterest` | |

Wat SAREF niet heeft: collecties, platformen, inzet, stimulus, `sosa:hasSimpleResult`,
`sosa:relatedObservation`.

## 2. Waarom dit hoofdstuk ertoe doet

**De alignment staat in geen van beide vocabularia waar je ze zoekt.** SAREF verwijst niet naar
de module, de namespace van SOSA ook niet, en het register van Linked Open Vocabularies kent ze
niet. Wie enkel in SAREF kijkt, besluit dat er geen alignment is. Daarom bestaat er een
zoekvolgorde ([Een alignment vinden en beoordelen](alignment-vinden.md)) en een register van
gekende alignments.

**Een term lenen is een verbintenis aangaan.** De herziening van de
[overstort](../casussen/overstort.md)-mapping zocht een eigenschap voor de fabrikant van een
toestel en koos `saref:hasManufacturer`. Het domein daarvan maakt het onderwerp een
`saref:FeatureOfInterest`. Dat is geen probleem: de module maakt elk `sosa:System` al een
`saref:FeatureOfInterest` (via `sosa:Asset`). Maar het moest nagekeken worden. Regel
[R17](../regels/r17.md), criterium 9, vraagt precies dat: wat voegen het domein, het bereik en de
afleidingen van die ene term toe, samen gelezen met de alignment?

## Casussen

- [Energiemanagement](../casussen/ems.md): HVAC-scenario's met SAREF-begrippen.
- [Overstort](../casussen/overstort.md): `saref:hasManufacturer` na een vergelijking volgens R17.
