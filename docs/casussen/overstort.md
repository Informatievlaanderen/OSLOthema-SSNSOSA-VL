# Overstort

*Een herziening van Aquafins LDES-mapping van overstortmeters en overstortevents, met een
alternatieve lezing.*

| | |
|---|---|
| **Domein** | riolering, oppervlaktewater; ~1600 overstortmeters van Aquafin |
| **Model** | plat |
| **Bron** | twee LDES-stromen (`overstort-sensor`, `overstort-event-cleansed`), de LDIO-mapping (SPARQL CONSTRUCT) en het resultaat op de LDES-server; [issue #1](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/issues/1) |
| **Bestanden** | [README met verbeterpunten](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/overstort/README.md) · [bespreking](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/overstort/bespreking.md) · [alternatief](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/overstort/alternatief/README.md) |

## Waarom deze casus

Een echte mapping van een echte publicatie, door een organisatie die het goed wilde doen. Ze
bevat de fouten die in productiemappings het vaakst voorkomen, en die enkel zichtbaar worden met
de [alignment van SOSA met PROV-O](../kaart/sosa-prov.md): record en waarneming door elkaar, en
uitvoeringseigenschappen op een sensor. Ze toont ook hoe je vocabularia kiest
([R17](../regels/r17.md)).

## De verbeterpunten

| # | Ontvangen | Herzien | Regel |
|---|---|---|---|
| 1 | de LDES-member (een recordversie van 26/08/2025) is getypeerd als de waarneming (18/02/2024, 20:45–20:46), met `prov:generatedAtTime` | voorlopig oplossing A: geen PROV-recordeigenschappen op de waarneming; B (een apart record) ligt voor | [R16](../regels/r16.md), [Waarneming of record?](../modelleren/record.md) |
| 2 | `sosa:madeBySensor "4c314f…"` (een literal) | een sensor-IRI | [R1](../regels/r01.md) |
| 3 | IRI's uit `STRUUID()` | sensor-IRI uit de MD5 van het toestelnummer | [R10](../regels/r10.md) |
| 4 | `aquafin:event_start_time`, `event_end_time` | `sosa:phenomenonTime` → `time:Interval` | [R12](../regels/r12.md) |
| 5 | `sensor sosa:hasFeatureOfInterest meetpunt` | `meetpunt sosa:hosts sensor` + een `sosa:Deployment` | [R16](../regels/r16.md) |
| 6 | meetpunt en eigenschap zonder type | `sosa:Platform`, `sosa:FeatureOfInterest`; `sosa:Property` | [R1](../regels/r01.md) |
| 7 | `geo:lat`/`geo:long` (WGS84 Basic Geo) en Lambert-velden op de sensor | twee `geo:Geometry` met WKT op het meetpunt, in WGS84 en Lambert 72 | [R11](../regels/r11.md) |
| 8 | Smart Data Models-termen zonder RDF-definitie | `rdfs:label`, `saref:hasManufacturer`, `adms:status`, na vergelijking | [R17](../regels/r17.md) |
| 9 | eigenaar, leverancier, gehasht serienummer, kwaliteitslabel | niet overgenomen; vragen aan Aquafin | — |

De validatie van het origineel gaf 16 onbekende termen, 2 inconsistenties (punten 1 en 5) en 3
schendingen van de regels.

## De keuzes van de herziening

- **Het meetpunt is platform en studieobject**, geen ruimtelijk monster: de vraag gaat over de
  werking van dit ene kunstwerk, niet over een eigenschap van het rioleringsstelsel of de
  ontvangende waterloop waarvan het meetpunt een steekproef zou zijn.
- **Een inzet** verbindt sensor, meetpunt en studieobject.
- **Het event is een waarneming** van de eigenschap *overstort*, met de status als resultaat (een
  begrip) en de periode als interval.
- **Geen eenheden**: er zijn geen numerieke resultaten.

## Twee lezingen

Het alternatief leest een overstorting als **emissie**: een `wk:Emissie` als studieobject, het
resultaat van een `sosa:Actuation` op de overstort (een passieve bron, zonder actuator), zoals de
lozingen in [waterkwaliteit](waterkwaliteit.md) ([Emissie als studieobject](../patronen/emissie.md#passieve-bron)).
Een argument tegen: de stroom meldt ook periodes *zonder* overstorting, die geen emissie hebben
als studieobject. Status: beide *voorstel*.

## Diagram: vóór en na

```mermaid
--8<-- "src/main/input/overstort/overstort_vergelijking.mmd"
```

## Diagram: de herziening

```mermaid
--8<-- "src/main/input/overstort/overstort_herzien.mmd"
```

## Turtle

??? example "overstort_herzien.ttl"

    ```turtle
    --8<-- "src/main/input/overstort/overstort_herzien.ttl"
    ```

??? example "alternatief/overstort_emissie.ttl"

    ```turtle
    --8<-- "src/main/input/overstort/alternatief/overstort_emissie.ttl"
    ```
