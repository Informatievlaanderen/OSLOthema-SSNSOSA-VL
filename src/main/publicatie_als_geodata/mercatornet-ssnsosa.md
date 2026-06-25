# SSN/SOSA-observaties publiceren via MercatorNet

## Doel

MercatorNet publiceert geografische data als platte tabellen ("simple features"). SSN/SOSA biedt
een rijke semantische structuur voor observatiedata. Dit document beschrijft hoe je SSN/SOSA-data
zo modelleert dat het als platte tabel bij MercatorNet gepubliceerd kan worden — conform beide
standaarden tegelijk.

Basisprincipe: **GIS en LOD zijn complementair.** Het rijke semantische model leeft in een
triplestore of RDF-bestand. De platte projectie ervan wordt gepubliceerd via MercatorNet. Een
SPARQL SELECT-query is de brug tussen beide werelden.

> "A little semantics goes a long way." — Jim Hendler

Drie SSN/SOSA-toevoegingen volstaan al voor interoperabiliteit:
- `qudt:hasUnit` met QUDT URI → eenheden machineleesbaar
- `sosa:observedProperty` met URI → verwijzing naar codelijst
- `sosa:hasFeatureOfInterest` met URI → verwijzing naar masterdata

---

## Standaard kolomstructuur

Elke rij in de MercatorNet-tabel stelt één `sosa:Observation` voor.

| Kolomnaam | Postgres-type | Bron in SSN/SOSA | Opmerking |
|---|---|---|---|
| `obs_iri` | `TEXT` | IRI van `sosa:Observation` | identifier |
| `sensor_iri` | `TEXT` | `sosa:madeBySensor` | codelijst |
| `foi_iri` | `TEXT` | `sosa:hasFeatureOfInterest` | masterdata URI |
| `prop_iri` | `TEXT` | `sosa:observedProperty` | codelijst URI |
| `proc_iri` | `TEXT` | `sosa:usedProcedure` | codelijst URI |
| `begin_tijd` | `TIMESTAMP WITH TIME ZONE` | `time:hasBeginning / time:inXSDDateTimeStamp` | zie §Tijdsmodellering |
| `eind_tijd` | `TIMESTAMP WITH TIME ZONE` | `time:hasEnd / time:inXSDDateTimeStamp` | enkel bij periode-observatie |
| `result_tijd` | `TIMESTAMP WITH TIME ZONE` | `sosa:resultTime` | wanneer resultaat beschikbaar werd |
| `waarde` | `NUMERIC(p,s)` | `qudt:numericValue` of `sosa:hasSimpleResult` | precision en scale verplicht |
| `eenheid_iri` | `TEXT` | `qudt:hasUnit` | QUDT unit URI |
| `geom` | `GEOMETRY(Point, 3812)` | `geo:asWKT` omgezet naar Lambert 2008 | kolomnaam verplicht `geom` |

Kolomnamen in lowercase `[a-z,0-9,_]`, bij voorkeur ≤ 10 tekens (Shapefile-limiet).

---

## Laagnaamconventie

Pas het MercatorNet-patroon toe op SSN/SOSA-datasets:

```
<thema>_<observedProperty>_<schaal>_<jaar>
```

- **thema**: INSPIRE-afkorting. Gebruik `ef` (Environmental Monitoring Facilities) voor
  meetnetdata; `hy` voor hydrologische data; `lu` voor landgebruik.
- **observedProperty**: afkorting van de gemeten eigenschap (3–6 tekens), bijv. `gwpeil`,
  `verkint`, `sedvol`.
- **schaal**: nominale schaal als `1k`, `10k`, `1m`.
- **jaar**: publicatiejaar als `yyyy`.

Voorbeelden:

| Dataset | Laagnaam |
|---|---|
| Grondwaterpeilmetingen DOV | `ef_gwpeil_1k_2025` |
| Verkeersintensiteit fietsroutes | `ef_verkint_1k_2026` |
| Erosiesedimentvolume veldmeting | `ef_sedvol_1k_2024` |

---

## QUDT-eenheden

Gebruik `qudt:hasUnit` met de volledige QUDT URI in het RDF-model. In de MercatorNet-tabel
wordt die URI als tekst opgeslagen in de kolom `eenheid_iri`.

```turtle
sosa:hasResult [
    a qudt:QuantityValue ;
    qudt:numericValue "7.53"^^xsd:decimal ;
    qudt:hasUnit unit:Meter
] .
```

→ `waarde = 7.53`, `eenheid_iri = 'http://qudt.org/vocab/unit/Meter'`

Voordeel: afnemers kunnen eenheden automatisch omzetten zonder vrije-tekst parsing.
Gebruik `sosa:hasSimpleResult` enkel voor dimensieloze telwaarden (aantallen, categorieën).

Twee resultaatpatronen zijn toegestaan — meng ze niet binnen één dataset:
- **Expliciete resource**: `[ a qudt:QuantityValue ; qudt:numericValue … ; qudt:hasUnit … ]` — gebruik wanneer het resultaat extern gerefereerd moet worden.
- **Blank node**: `[ a sosa:Result ; qudt:numericValue … ; qudt:hasUnit … ]` — gebruik voor lokale resultaten zonder externe verwijzing.

---

## Codelijsten en masterdata

**`prop_iri`** — URI van `sosa:ObservableProperty`. Publiceer de eigenschap als OSLO-codelijst
en verwijs ernaar. Zolang een codelijst ontbreekt, gebruik `https://example.org/`-URIs als
tijdelijke placeholder.

**`foi_iri`** — URI van `sosa:FeatureOfInterest`. Verwijs naar gezaghebbende masterdata:

| Domein | URI-patroon |
|---|---|
| DOV grondwaterfilters | `https://www.dov.vlaanderen.be/data/filter/{id}` |
| DOV grondwaterputten | `https://www.dov.vlaanderen.be/data/put/{id}` |
| Gebouwen | `https://data.vlaanderen.be/id/gebouw/{id}` |
| Ondernemingen | `https://data.vlaanderen.be/id/onderneming/{kvk}` |
| Organisaties (OVO) | `https://data.vlaanderen.be/id/organisatie/{ovo}` |

Wanneer een meetpunt een ruimtelijk deelmonster is van een groter studieobject (fietsroute,
waterlichaam, gemeente), gebruik dan de typering `sosa:SpatialSample` en koppel via
`sosa:isSampleOf` aan het bredere FeatureOfInterest. Zet `sosa:hasFeatureOfInterest` op de
observatie naar **het meetpunt** (het directe studieobject), niet naar het bredere gebied.
Het bredere gebied is bereikbaar via de sampling-keten (`sosa:isSampleOf`).

---

## Geometrie

In het RDF-model:

```turtle
ex:meetpunt a sosa:Platform, sosa:FeatureOfInterest, sosa:SpatialSample ;
    geo:hasGeometry [
        a geo:Geometry ;
        geo:asWKT "Point(4.423123 51.20910)"^^geo:wktLiteral
    ] .
```

GeoSPARQL WKT gebruikt WGS84 (lon lat). MercatorNet vereist Lambert 2008 (epsg:3812).
Omzetten via PostGIS bij het inladen:

```sql
ST_Transform(ST_GeomFromText('POINT(4.423123 51.20910)', 4326), 3812)
```

Regels:
- Kolomnaam MOET `geom` zijn.
- Geen Z-waarden tenzij hoogte betekenisvol is.
- Nauwkeurigheid beperken tot 3 decimalen (millimeter).
- Gebruik het specifieke geometrietype (`POINT`, `LINESTRING`, `POLYGON`) — nooit generiek `GEOMETRY`.

---

## Tijdsmodellering

### Puntmeting

Wanneer het fenomeen geen duur heeft:

```turtle
sosa:phenomenonTime [ a time:Instant ; time:inXSDDateTimeStamp "2024-09-01T09:00:00Z"^^xsd:dateTimeStamp ] ;
sosa:resultTime "2024-09-01T09:00:00Z"^^xsd:dateTime .
```

→ `begin_tijd = '2024-09-01 09:00:00+00'`, geen `eind_tijd`.

### Periode-observatie (R12)

Wanneer de meting een tijdspanne beslaat (uurtelling, dagsom):

```turtle
sosa:phenomenonTime [
    a time:Interval ;
    time:hasBeginning [ a time:Instant ; time:inXSDDateTime "2026-04-28T08:00:00"^^xsd:dateTime ] ;
    time:hasEnd       [ a time:Instant ; time:inXSDDateTime "2026-04-28T09:00:00"^^xsd:dateTime ]
] .
```

→ `begin_tijd = '2026-04-28 08:00:00'`, `eind_tijd = '2026-04-28 09:00:00'` (half-open interval:
begin inclusief, einde exclusief).

Gebruik altijd `TIMESTAMP WITH TIME ZONE` in Postgres, nooit bare `TIMESTAMP`.

---

## SPARQL-materializatiequery

De query hieronder extraheert een platte tabel uit een SSN/SOSA-graph. Ze is gebaseerd op het
[verkeersmetingen-voorbeeld](../input/verkeersmetingen/verkeersmetingen.ttl) en volgt het
patroon waarbij gedeelde metadata op de `sosa:ObservationCollection` staat en individuele
observaties via `sosa:isMemberOf` eraan gekoppeld zijn.

```sparql
PREFIX sosa: <http://www.w3.org/ns/sosa/>
PREFIX time: <http://www.w3.org/2006/time#>
PREFIX qudt: <http://qudt.org/schema/qudt/>
PREFIX geo:  <http://www.opengis.net/ont/geosparql#>
PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>

SELECT
  ?obs_iri
  ?sensor_iri
  ?foi_iri
  ?prop_iri
  ?proc_iri
  ?begin_tijd
  ?eind_tijd
  ?result_tijd
  ?waarde
  ?eenheid_iri
  ?wkt           # vervolgens via PostGIS omzetten naar Lambert 2008
WHERE {
  ?obs_iri a sosa:Observation .

  # Sensor, FOI, property, procedure: direct op de observatie OF geërfd van de collectie
  { ?obs_iri sosa:madeBySensor ?sensor_iri }
  UNION
  { ?obs_iri sosa:isMemberOf/sosa:madeBySensor ?sensor_iri }

  { ?obs_iri sosa:hasFeatureOfInterest ?foi_iri }
  UNION
  { ?obs_iri sosa:isMemberOf/sosa:hasFeatureOfInterest ?foi_iri }

  { ?obs_iri sosa:observedProperty ?prop_iri }
  UNION
  { ?obs_iri sosa:isMemberOf/sosa:observedProperty ?prop_iri }

  { ?obs_iri sosa:usedProcedure ?proc_iri }
  UNION
  { ?obs_iri sosa:isMemberOf/sosa:usedProcedure ?proc_iri }

  # Tijdsmodellering: Interval of Instant
  OPTIONAL {
    ?obs_iri sosa:phenomenonTime/time:hasBeginning/time:inXSDDateTime ?begin_tijd .
    ?obs_iri sosa:phenomenonTime/time:hasEnd/time:inXSDDateTime       ?eind_tijd .
  }
  OPTIONAL {
    ?obs_iri sosa:phenomenonTime/time:inXSDDateTime ?begin_tijd .
    FILTER NOT EXISTS { ?obs_iri sosa:phenomenonTime/time:hasBeginning ?_ }
  }

  OPTIONAL { ?obs_iri sosa:resultTime ?result_tijd }

  # Meetwaarde: QuantityValue of hasSimpleResult
  OPTIONAL {
    ?obs_iri sosa:hasResult ?res .
    ?res qudt:numericValue ?waarde ;
         qudt:hasUnit      ?eenheid_iri .
  }
  OPTIONAL {
    ?obs_iri sosa:hasSimpleResult ?waarde .
    FILTER NOT EXISTS { ?obs_iri sosa:hasResult ?_ }
  }

  # Geometrie via het FeatureOfInterest
  OPTIONAL {
    ?foi_iri geo:hasGeometry/geo:asWKT ?wkt .
  }
}
ORDER BY ?foi_iri ?begin_tijd
```

### Resultaat voor verkeersmetingen (uittreksel)

| obs\_iri | sensor\_iri | foi\_iri | prop\_iri | begin\_tijd | eind\_tijd | waarde | eenheid\_iri | wkt |
|---|---|---|---|---|---|---|---|---|
| …/obs-FMN-021-20260428-08u | …/teller-FMN-021 | …/meetpunt-FMN-021 | …/property-verkeersintensiteit | 2026-04-28T08:00 | 2026-04-28T09:00 | 291 | _(geen)_ | Point(4.423… 51.209…) |
| …/obs-FMN-021-20260428-dag | …/teller-FMN-021 | …/meetpunt-FMN-021 | …/property-verkeersintensiteit | 2026-04-28T00:00 | 2026-04-29T00:00 | 2541 | _(geen)_ | Point(4.423… 51.209…) |

---

## Checklist voor databeheerders

Gebruik deze lijst om een SSN/SOSA-laag MercatorNet-klaar te maken:

- [ ] Kolomnamen in lowercase `[a-z,0-9,_]`, geen hoofdletters, geen speciale tekens
- [ ] Kolomnamen bij voorkeur ≤ 10 tekens (Shapefile-compatibiliteit)
- [ ] Geometriekolom heet exact `geom`
- [ ] Geometrietype specifiek: `POINT`, `LINESTRING` of `POLYGON` — niet generiek `GEOMETRY`
- [ ] Coördinaten in Lambert 2008 (epsg:3812) of Lambert 72 (epsg:31370)
- [ ] Geen Z-waarden tenzij hoogte betekenisvol is
- [ ] Tijdskolommen van type `TIMESTAMP WITH TIME ZONE`, nooit bare `TIMESTAMP`
- [ ] Meetwaarden van type `NUMERIC(precision, scale)` — precision en scale expliciet vermeld
- [ ] Kolom `eenheid_iri` met QUDT URI — geen vrije tekst voor eenheden
- [ ] Kolom `prop_iri` met URI van `sosa:ObservableProperty` — bij voorkeur OSLO-codelijst
- [ ] Kolom `foi_iri` met URI van `sosa:FeatureOfInterest` — bij voorkeur gezaghebbende masterdata

---

## Referentiedatavoorbeelden

| Voorbeeld | Model | Toepasbaar voor |
|---|---|---|
| [verkeersmetingen](../input/verkeersmetingen/) | Plat, SpatialSample, time:Interval | Tellers, meetstations met periodedata |
| [grondwaterpeilmetingen](../input/grondwaterpeilmetingen/) | Plat, ObservationCollection, QUDT-resultaten | Meerdere eigenschappen per meetronde |
| [erosiepoel](../input/erosiepoel/) | Plat, enkelvoudige meting, QuantityValue | Veldmetingen, eenmalige opnames |

Aanvullende SSN/SOSA-regels relevant voor MercatorNet-publicatie:
- **Verplichte properties per observatie**: elke `sosa:Observation` heeft minimaal `sosa:observedProperty`, `sosa:hasFeatureOfInterest`, en `sosa:hasResult` of `sosa:hasSimpleResult`. `sosa:madeBySensor` en `sosa:usedProcedure` zijn sterk aanbevolen (mogen op de collectie staan).
- **Periode vs. punt**: gebruik `time:Interval` met `time:hasBeginning` / `time:hasEnd` wanneer de meting een tijdspanne beslaat (uurtelling, dagsom); gebruik `time:Instant` voor puntmetingen zonder duur.
- **Afgeleide observaties**: dagsom, aggregaat of andere berekende waarden staan als aparte rijen in de MercatorNet-tabel — niet als lid van de bronobservatie-collectie. Koppel via `sosa:hasInputValue` aan de bronobservaties of -collectie.
