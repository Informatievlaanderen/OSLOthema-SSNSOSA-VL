# Waar?

Het hoofdstuk [SOSA en GeoSPARQL](../kaart/sosa-geosparql.md) beschrijft het model; deze pagina
geeft de beslissingen.

## 1. Wat heeft een plaats?

Een plaats hoort bij een **ding**, niet bij een waarneming: het studieobject (een meetpunt, een
erosiepoel, een rastercel) of het platform. Een waarneming vindt plaats *aan* een studieobject; haar
plaats volgt uit dat van het studieobject.

## 2. Ken je coördinaten?

| Je kent … | Gebruik |
|---|---|
| coördinaten (punt, lijn, vlak) | `geo:hasGeometry` naar een `geo:Geometry` met `geo:asWKT` |
| een adres of beschrijving | `prov:atLocation` naar een `prov:Location`, of een OSLO-adres |
| een andere resource die zelf een plaats is (een waterloop, een gemeente) | een relatie naar die resource; bij een monster `sosa:isSampleOf` |
| niets | niets; zeg het in de bespreking, verzin geen plaats |

```turtle
ex:meetpunt geo:hasGeometry ex:geometrie-meetpunt .
ex:geometrie-meetpunt a geo:Geometry ;
    geo:asWKT "POINT(4.423123 51.20910)"^^geo:wktLiteral .
```

- WKT in WGS84: **lengte eerst**.
- Een ander referentiestelsel als IRI vóór de vorm:
  `"<http://www.opengis.net/def/crs/EPSG/0/31370> POINT(x y)"^^geo:wktLiteral` (Lambert 72).
- Twee resources op dezelfde plaats mogen één geometrie delen; een geometrie mag per station
  gedeeld worden in grote datasets.

## 3. Staat het meetpunt voor een groter gebied?

Dan is het een **ruimtelijk monster**: type `sosa:Platform`, `sosa:FeatureOfInterest` en
`sosa:SpatialSample`, met `sosa:isSampleOf` het grotere gebied en een geometrie. Het studieobject
van de waarnemingen is het meetpunt; het gebied is het uiteindelijke studieobject
([R11](../regels/r11.md), [Ruimtelijk monster](../patronen/ruimtelijk-monster.md)).

## 4. Valkuilen

- `geo:asWKT` rechtstreeks op het studieobject: het domein is `geo:Geometry`, disjunct met
  `geo:Feature`.
- `geo:lat` en `geo:long` (WGS84 Basic Geo) onder het prefix `geo:` dat conventioneel GeoSPARQL
  is.
- lengte en breedte omgewisseld; in Lambert 72 x en y.
