# Overstort — overstortsensoren van Aquafin

Herziening van de SSN/SOSA-mapping die Aquafin maakte voor de overstortdata die het via LDES
publiceert ([issue #1](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/issues/1)).
Een overstort is een kunstwerk dat bij hevige neerslag overtollig rioolwater uit de gemengde
riolering naar het oppervlaktewater afvoert. Ongeveer 1600 overstortmeters registreren wanneer een
overstort in werking is.

## Bron

- Documentatie en mapping:
  [OSLO-mapping — Aquafin, Overstort in Vlaanderen](https://informatievlaanderen.github.io/OSLO-mapping/water/Aquafin%20-%20Overstort%20In%20Vlaanderen/0_2_data_input)
  (bron in [`Informatievlaanderen/OSLO-mapping`](https://github.com/Informatievlaanderen/OSLO-mapping),
  `docs/_water/Aquafin - Overstort In Vlaanderen/`).
- Twee LDES-stromen (niet publiek, toegang via info@aquafin.be):
  `overstort-sensor` (metadata per toestel) en `overstort-event-cleansed` (start- en eindtijd van
  overstortingen per toestel).

Ontvangen materiaal in `source/`, ongewijzigd:

| Bestand | Inhoud |
|---|---|
| `source/overstort-event.json` | voorbeeld van een eventbericht (JSON, zonder de commentaar uit de documentatie) |
| `source/overstort-sensor.json` | voorbeeld van een sensorbericht |
| `source/overstort-mapping.rq` | de twee SPARQL CONSTRUCT-mappings van de LDIO Workbench |
| `source/overstort.trig` | het eindresultaat op de LDES-server (één sensor, één event), Turtle als `.trig` |
| `source/overstort-input-voorbeelden.md` | voorbeeldrecords uit de documentatie (sensor P2050378 op meetpunt P_000000217952, event) |
| `source/overstort-debiet-overstortduur.json.txt` | Aquafins doelmodel voor observaties van debiet en overstortduur (geannoteerde JSON, geen geldige JSON) |

Het issue zelf staat in `github_issue1`.

## Transformatie

Bij Aquafin: JSON → LDIO Workbench (JSON-LD met `aquafin:`-context) → SPARQL CONSTRUCT → LDES-server
(versionering met `dct:isVersionOf` en `prov:generatedAtTime`). Hier: geen script; de herziene
versie is met de hand afgeleid uit `source/overstort.trig`.

## Mappingkeuzes

Plat model. Het meetpunt (P-nummer uit de Rioolinventaris) is `sosa:Platform` en
`sosa:FeatureOfInterest`; het herbergt de overstortmeter (`sosa:Sensor`) en is het doelwit van een
`sosa:Deployment`. Een overstortevent is een `sosa:Observation` van de property
`kenmerk:Overstort`, met de overstortstatus als resultaat en de periode als
`sosa:phenomenonTime → time:Interval`. Zie `bespreking.md`.

**Alternatief:** [`alternatief/`](alternatief/README.md) leest een overstorting als emissie
(`wk:Emissie` als studieobject, zoals de lozingen in `../waterkwaliteit/`), naast dit model, voor
de werkgroep.

## Diagram

- `overstort_herzien.mmd` — het herziene model.
- `overstort_vergelijking.mmd` — origineel en herziening naast elkaar.

## Outputbestanden

| Bestand | Inhoud |
|---|---|
| `overstort_herzien.ttl` | herziene versie (sensor, meetpunt, inzet, event) |
| `overstort_herzien.mmd` | diagram van de herziene versie |
| `overstort_vergelijking.mmd` | vergelijkingsdiagram |
| `bespreking.md` | bespreking in negen secties |

## Gebruik

```bash
riot --validate source/overstort.trig overstort_herzien.ttl
```

Valideren met `mcp__ld-vocab__validate_file` op `src/main/input/overstort/overstort_herzien.ttl`.

## Verbeterpunten

Diagnose van `source/overstort.trig` met `validate_file`: 16 `[VOCAB ERROR]`, 2 `[MODEL INVALID]`,
3 SHACL-schendingen en 1 waarschuwing. Elk punt: origineel → herzien → motivatie.

1. **Sensor als literal.** `sosa:madeBySensor "4c314f…"` (MD5 als tekst) → `sosa:madeBySensor
   sensor:4c314f066bea53f212495cb8c1eaca0b` → `sosa:madeBySensor` is een objectrelatie naar een
   `sosa:Sensor` (SHACL-schending). Met een literal is het event niet aan de sensorstroom te koppelen.

2. **Willekeurige IRI's.** Sensor- en event-IRI's uit `STRUUID()` → sensor-IRI uit de MD5 van het
   toestelnummer, `https://aquafin.be/id/sensor/{MD5(id)}` → een IRI die bij elke run verandert,
   kan niet als doel van een verwijzing dienen en breekt de versieketen (`dct:isVersionOf` wijst
   telkens naar een nieuwe basis-IRI) (R10). De eventstroom levert al dezelfde MD5
   (`is_observed_with`), dus de koppeling vraagt geen extra gegeven. Voor events is een
   deterministische sleutel nodig, bv. MD5(toestel + meetpunt + start); de bron geeft die niet,
   daarom houdt de herziening de bestaande UUID (zie bespreking, §8).

3. **Periode van het event.** `aquafin:event_start_time` / `aquafin:event_end_time` →
   `sosa:phenomenonTime → time:Interval → time:hasBeginning / time:hasEnd → time:Instant →
   time:inXSDDateTimeStamp` → R12: een event met een duur is een interval; de eigen properties
   bestaan in geen geladen vocabularium (`[VOCAB ERROR]`) en zijn voor geen enkele SOSA-client
   vindbaar. De vereenvoudiging voor eindgebruikers (issue #1) is besproken in `bespreking.md` §6
   en §7.

4. **Feature of interest op de sensor.** `sensor sosa:hasFeatureOfInterest meetpunt` →
   `meetpunt sosa:hosts sensor` plus een `sosa:Deployment` met `sosa:deployedSystem`,
   `sosa:deployedOnPlatform` en `sosa:hasFeatureOfInterest meetpunt` → in SOSA 2023 gaat
   `sosa:hasFeatureOfInterest` van een Execution of een Deployment naar haar doelwit; als
   deelproperty van `prov:used` maakt ze de sensor een `prov:Activity`, wat met
   `prov:generatedAtTime` (→ `prov:Entity`) het `[MODEL INVALID]` gaf.

5. **Ongetypeerde meetpunten en property.** `meetpunt:…` en `kenmerk:Overstort` zonder type →
   `sosa:Platform, sosa:FeatureOfInterest` respectievelijk `sosa:Property` → SHACL verwacht die
   klassen bij `hasFeatureOfInterest` en `observedProperty`; SHACL valideert de niet-afgeleide graaf.

6. **Coördinaten.** `geo:lat` / `geo:long` (W3C WGS84-vocabularium, niet geladen) en
   `aquafin:lat_Lambert72` / `long_Lambert72` op de sensor → twee `geo:Geometry` met `geo:asWKT` op
   het meetpunt: `POINT(lon lat)` in WGS84 en een WKT met de CRS-IRI van Lambert 72 (EPSG:31370) →
   R11 en het prefixgebruik uit `linked-data.md`: `geo:` is GeoSPARQL. In Lambert 72 is
   `long_Lambert72` de x en `lat_Lambert72` de y. De documentatie verwisselt ook *lengte* en
   *breedte* bij de WGS84-velden. De locatie hoort bij het meetpunt, het toestel staat daar.

7. **Dubbele en ongeldige toesteleigenschappen.**
   - `dct:identifier` en `environment:deviceId` (zelfde MD5) → enkel `dct:identifier`;
   - `dct:description` en `environment:deviceName` (zelfde naam) → `rdfs:label`;
   - `dct:type "Overstortmeter"` → `rdfs:comment`: het bereik van `dct:type` is `rdfs:Class`, geen
     tekst;
   - `environment:deviceModel "Ijinus"` → `saref:hasManufacturer "Ijinus"`: het is het merk
     (`brand`), niet het model;
   - `environment:deviceStatus "ACTIEF"` → `adms:status toestelstatus:Actief` (concept-IRI, voorstel
     naar het patroon van Aquafins eigen `…/id/concept/…`-IRI's);
   - de Smart Data Models-namespaces (`https://smartdatamodels.org/…`) zijn geen gepubliceerde
     RDF-vocabularia (`[VOCAB ERROR]`).

8. **Niet overgenomen** (geen bestaande term of betekenis onbekend; vragen in `bespreking.md`):
   `sdm:owner "AQUAFIN"`, `schema:seller "ELSCOLAB"`, `schema:serialNumber` (MD5 van het
   serienummer; stond niet in de LDES-output), `aquafin:quality_label`, `aquafin:valid_from`,
   `aquafin:valid_to`, `aquafin:is_deleted`.

9. **Versionering op de observatie.** `prov:generatedAtTime` op de versie van een
   `sosa:Observation` → enkel `dct:modified` (de wijzigingsdatum uit de bron) → `sosa:Observation`
   is een `prov:Activity`, `prov:generatedAtTime` maakt er een `prov:Entity` van; die klassen zijn
   disjunct (`[MODEL INVALID]`). Gebruik op de LDES-stroom `dct:modified` als `ldes:timestampPath`.
   `valid_from`/`valid_to` en `is_deleted` zijn eigenschappen van een *versie*, niet van het toestel
   of het event: de LDES-versieketen drukt ze al uit.

10. **Fouten in de mapping zelf** (`source/overstort-mapping.rq`): de prefix `purl:` is niet
    gedeclareerd (`purl:modified`); de JSON-LD-context gebruikt `https://qudt.org/…` in plaats van
    `http://qudt.org/…` (linked-data.md, `http` versus `https`), `"schema": "https://schema.org"`
    zonder afsluitende `/`, en `geo:` voor WGS84 naast `geosparql:`.
