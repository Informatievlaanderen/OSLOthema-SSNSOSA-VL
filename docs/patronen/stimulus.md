# Stimulus

**De gebeurtenis die een sensor doet meten.** SOSA 2023 definieert een stimulus als "een
gebeurtenis in de echte wereld die een sensor activeert". Het studieobject blijft de plaats waar
het effect gemeten wordt. Zo blijven de *bron* en de *plaats van meting* gescheiden.

## Het patroon

```turtle
ex:geluidsevent-0123 a sosa:Stimulus , prov:Entity ;
    prov:wasGeneratedBy ex:vlucht-BCS6TP ;
    sosa:isDetectedBy ex:geluidsmeter-M072 .

ex:eventcollectie-0123 a sosa:ObservationCollection ;
    sosa:wasOriginatedBy ex:geluidsevent-0123 ;
    sosa:hasFeatureOfInterest ex:meetpost-M072 ;
    sosa:hasMember ex:laeq-0123 , ex:lamax-0123 , ex:sel-0123 , ex:duur-0123 .
```

- de stimulus wordt gedetecteerd door de sensor (`sosa:isDetectedBy`);
- de waarnemingen (of hun collectie) zijn veroorzaakt door de stimulus (`sosa:wasOriginatedBy`);
- het studieobject is de meetpost;
- de bron (de vlucht) genereert de stimulus.

## Waarom het samenhangt met de kernvocabularia

Het volgt de sensorketen van SOSA zelf: stimulus → sensor → waarneming. De stimulus is een
entiteit gegenereerd door een activiteit (de vlucht), dus de herkomst van een meetwaarde tot de
vlucht is opvraagbaar, zonder de plaats van meting op te geven als studieobject.

## Kiezen

**Kies het** wanneer de gebeurtenis een meting veroorzaakt op een vaste plaats, en de toestand van
die plaats de vraag is: hoeveel geluid krijgt deze meetpost, hoe vaak wordt een drempel
overschreden?

**Vergelijk** met [Emissie als studieobject](emissie.md): daar is de gebeurtenis zelf het
studieobject. In dit project bestaan beide lezingen van de geluidsdata naast elkaar.

## Gebruikt in

- [Geluidsmeetnet](../casussen/geluidsmeetnet.md) (hoofdmodel).

??? quote "Normatieve tekst (modelleergids, Engels)"

    --8<-- "kit/patroon-stimulus.md"
