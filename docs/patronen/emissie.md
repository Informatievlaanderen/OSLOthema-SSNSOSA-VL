# Emissie als studieobject

**De uitstoot zelf is het studieobject**: een lozing, een geluidsemissie, een overstorting. Ze is
een `prov:Entity`, gegenereerd door een activiteit (een bedrijfsproces, een vlucht, een
overloop), en waar ze gemeten werd, is niet het studieobject maar haar plaats.

## Het patroon

```turtle
ex:lozing-2400006 a prov:Entity , sosa:FeatureOfInterest ;
    prov:wasGeneratedBy ex:bedrijfsactiviteit ;      # of een vlucht, een productierun …
    geo:hasGeometry ex:geometrie-meetput-2400006 ;   # of prov:atLocation, zie onder
    dct:type matrix:afvalwater .                     # de matrix is een eigenschap van de emissie

ex:waarneming-jaardebiet sosa:hasFeatureOfInterest ex:lozing-2400006 ;
    sosa:phenomenonTime ex:periode-2023 .
```

- De emissie is **tijdloos**: de periode staat op de fenomeentijd van de waarneming.
- De **matrix** (afvalwater, oppervlaktewater) is een kenmerk van het studieobject.
- Een **plaats**: `geo:hasGeometry` wanneer coördinaten gekend zijn (ze mag de geometrie van het
  meetpunt delen); `prov:atLocation` naar het meetpunt is niet fout, en is de keuze wanneer de
  plaats enkel met een adres of als resource zonder coördinaten gekend is.
- Een monster van de emissie (een staal) is `sosa:isSampleOf` de emissie
  ([Monster en uiteindelijk studieobject](monster.md)).
- Beschrijft de bron de veroorzakende activiteit niet, maar wel wie verantwoordelijk is, dan kan
  de emissie ook toegeschreven worden aan een agent: in de waterkwaliteitsdata is de lozing
  `prov:wasAttributedTo` de exploitatie uit RIE-IEPR.

## Waarom het past in de kaart

De emissie is een entiteit, de activiteit die haar veroorzaakt een activiteit, en
`prov:wasGeneratedBy` verbindt ze, precies zoals PROV-O het bedoelt. Een herkomstquery vindt van
een meetwaarde de lozing, en van de lozing het bedrijfsproces.

## Passieve bron

Wanneer niets gestuurd wordt (een overstort die bij hevige regen over een drempel loopt), kan de
activiteit die de emissie genereert een `sosa:Actuation` op het kunstwerk zijn, met de emissie als
resultaat, een `sosa:ActuatingProcedure`, en zonder `sosa:madeByActuator`. Eén resource dient dan
als `prov:wasGeneratedBy` én als `sosa:isResultOf` (want `sosa:Actuation ⊂ prov:Activity` en
`sosa:hasResult ⊂ prov:generated`).

```turtle
ex:overstorting-0218 a wk:Emissie , sosa:FeatureOfInterest , prov:Entity ;
    sosa:isResultOf ex:overloop-0218 .
ex:overloop-0218 a sosa:Actuation ;
    sosa:hasFeatureOfInterest ex:overstort-P217952 ;
    sosa:usedProcedure ex:overloop-bij-hoge-waterstand ;
    sosa:hasResult ex:overstorting-0218 .
```

## Kiezen

**Kies het** wanneer de vraag over de bron en haar uitstoot gaat: vrachten per bedrijf, emissies
per vlucht, overstortvolumes per kunstwerk.

**Liever niet** wanneer de vraag over de toestand van een plaats gaat (hoeveel geluid krijgt deze
wijk?); dan past de [stimulus](stimulus.md) beter.

**Gebeurtenissen zonder emissie.** Een gegevensstroom meldt soms ook periodes *zonder* emissie
(geen overstorting, signaal gestoord). Die hebben geen emissie die het studieobject kan zijn; ze
blijven waarnemingen van de plaats. Het studieobject hangt dan af van de status van het event, wat
een argument tegen dit patroon is voor zulke stromen (overstort, alternatief, bespreking §6).

## Gebruikt in

- [Waterkwaliteit](../casussen/waterkwaliteit.md): de lozing als studieobject van debieten en
  vrachten, en als uiteindelijk studieobject van stalen.
- [Geluidsmeetnet, alternatief](../casussen/geluidsmeetnet.md#twee-lezingen): het geluidsevent als
  emissie van de vlucht.
- [Overstort, alternatief](../casussen/overstort.md#twee-lezingen): de overstorting als emissie,
  resultaat van een actuatie.

??? quote "Normatieve tekst (modelleergids, Engels)"

    --8<-- "kit/patroon-emissie.md"
