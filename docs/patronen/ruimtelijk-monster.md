# Ruimtelijk monster

**Een meetpunt dat voor een groter gebied staat**, is een `sosa:Platform`,
`sosa:FeatureOfInterest` en `sosa:SpatialSample`, `sosa:isSampleOf` het gebied, met een geometrie.
Het studieobject van de collectie is het meetpunt, niet het gebied ([R11](../regels/r11.md)).

## Het patroon

```turtle
ex:meetplaats-OW12000 a sosa:Platform , sosa:FeatureOfInterest , sosa:SpatialSample ;
    sosa:isSampleOf ex:waterloop-VHA-6030069 ;
    geo:hasGeometry ex:geometrie-OW12000 .

ex:collectie-staal-0128 a sosa:ObservationCollection ;
    sosa:hasFeatureOfInterest ex:meetplaats-OW12000 ;
    sosa:hasUltimateFeatureOfInterest ex:waterloop-VHA-6030069 .
```

## Waarom het samenhangt met de kernvocabularia

- **SOSA** heeft er een eigen klasse voor: een deelverzameling van een studieobject, gedefinieerd
  door haar plaats en vorm.
- **GeoSPARQL**: de geometrie maakt het meetpunt een `geo:Feature`, ruimtelijk bevraagbaar
  ([SOSA en GeoSPARQL](../samenhang/sosa-geosparql.md)).
- **PROV-O**: `sosa:isSampleOf ⊂ prov:wasDerivedFrom`.
- Het **uiteindelijke studieobject** (de route, de waterloop) is vaak een resource uit een register
  (de VHA), waarnaar de data verwijst zonder ze te beschrijven.

## Varianten

- Een **rastercel** als ruimtelijk monster van een gewest ([PGD](../casussen/pgd.md)).
- Een **meetpost** voor de omgeving van een luchthaven ([geluidsmeetnet](../casussen/geluidsmeetnet.md)).
- Het meetpunt als **resultaat van een ruimtelijke bemonstering** (`sosa:Sampling`): de keuze van
  de plaats op de route ([verkeersmetingen](../casussen/verkeersmetingen.md)).

## Gebruikt in

[verkeersmetingen](../casussen/verkeersmetingen.md) · [waterkwaliteit](../casussen/waterkwaliteit.md)
(meetplaats oppervlaktewater) · [geluidsmeetnet](../casussen/geluidsmeetnet.md) ·
[PGD](../casussen/pgd.md)

??? quote "Normatieve tekst (modelleergids, Engels)"

    --8<-- "kit/patroon-ruimtelijk-monster.md"
