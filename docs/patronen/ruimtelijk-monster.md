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

## Een monster van wat?

Het bemonsterde studieobject is het object waarvan het meetpunt de eigenschap schat, niet wat die
eigenschap veroorzaakt. Vraag je dus af of de gemeten eigenschap bij het grotere object hoort:

| Casus | Gemeten eigenschap | Monster van | Waarom |
|---|---|---|---|
| [verkeersmetingen](../casussen/verkeersmetingen.md) | fietsers per uur | de fietsroute | de intensiteit is een eigenschap van de route, ongeveer gelijk langs een stuk tussen twee kruispunten |
| [geluidsmeetnet](../casussen/geluidsmeetnet.md) | geluidsniveau van vliegtuigen | de omgeving van de luchthaven | het niveau is een eigenschap van de plaats, veroorzaakt door vluchten, niet van de startbaan |
| [ELF-meetnet](../casussen/elf.md) | magnetische fluxdichtheid | de omgeving van een hoogspanningsverbinding of -station | het veld hangt af van de afstand tot de geleiders en is geen eigenschap van de lijn |

Wordt de eigenschap veroorzaakt door een bron (immissie, blootstelling), dan is het meetpunt een
monster van de **omgeving** van die bron. De bron is dan een studieobject op zich, met eigen
eigenschappen. Voor een hoogspanningslijn is dat de stroombelasting, en die *is* wel gelijk langs een
stuk verbinding. Het veld langs de hele lijn is het werk van een rekenmodel; de metingen toetsen het
lokaal. De omgeving verwijst naar de bron, bv. met `prov:wasInfluencedBy`. Dat werkt voor een lijn
en voor een puntbron (een station) op dezelfde manier. Een meetcampagne (`sosa:Deployment`) noemt de
omgeving als `sosa:hasUltimateFeatureOfInterest`.

```turtle
ex:verbinding-… a sosa:FeatureOfInterest ;
    sosa:hasProperty ex:prop-stroombelasting .
ex:omgeving-verbinding-… a sosa:FeatureOfInterest ;
    prov:wasInfluencedBy ex:verbinding-… .
ex:meetlocatie-… a sosa:Platform , sosa:FeatureOfInterest , sosa:SpatialSample ;
    sosa:isSampleOf ex:omgeving-verbinding-… ;
    prov:atLocation ex:adres-… ;                 # zoals de registratie het geeft
    geo:hasGeometry ex:geom-… .                  # gegeocodeerd of gemeten, zie R11
```

**Adres en geometrie samen.** `prov:atLocation` naar het adres en `geo:hasGeometry` naar een punt
gaan samen ([R11](../regels/r11.md)). Wees voorzichtig met geocodering: de adrespositie is de positie
van het adres, niet van de sensor. Bij een waarde die sterk van de afstand afhangt, zoals een veld of
een geluidsniveau, vermeld je hoe het punt bepaald is. Een gemeten positie vervangt het zodra die er
is. Zet de CRS-IRI vooraan in de `geo:wktLiteral` als de coördinaten niet in CRS84 staan, bv.
`"<http://www.opengis.net/def/crs/EPSG/0/31370> POINT(81177 208128)"^^geo:wktLiteral` (Lambert 72).
Een meetlocatie bij iemand thuis is een persoonsgegeven: publiceer zo nodig een veralgemeende
geometrie.

## Varianten

- Een **rastercel** als ruimtelijk monster van een gewest ([PGD](../casussen/pgd.md)).
- Een **meetpost** voor de omgeving van een luchthaven ([geluidsmeetnet](../casussen/geluidsmeetnet.md)).
- Een **meetlocatie** voor de omgeving van een hoogspanningsverbinding of -station, met adres en
  geometrie ([ELF-meetnet](../casussen/elf.md)).
- Het meetpunt als **resultaat van een ruimtelijke bemonstering** (`sosa:Sampling`): de keuze van
  de plaats op de route ([verkeersmetingen](../casussen/verkeersmetingen.md)).

## Gebruikt in

[verkeersmetingen](../casussen/verkeersmetingen.md) · [waterkwaliteit](../casussen/waterkwaliteit.md)
(meetplaats oppervlaktewater) · [geluidsmeetnet](../casussen/geluidsmeetnet.md) ·
[PGD](../casussen/pgd.md) · [ELF-meetnet](../casussen/elf.md)

??? quote "Normatieve tekst (modelleergids, Engels)"

    --8<-- "kit/patroon-ruimtelijk-monster.md"
