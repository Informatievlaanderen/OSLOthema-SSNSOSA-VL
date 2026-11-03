# Emissie en immissie

**Eén keten, twee vragen.** Een emissie bij een bron veroorzaakt een immissie op een plaats: wat
uitgestoten wordt, verspreidt zich (door lucht of water, als geluidsgolf) en komt elders aan.
[Emissie als studieobject](emissie.md) en [Stimulus](stimulus.md) zijn geen concurrerende lezingen,
maar twee schakels van die keten. Elk is het studieobject van een andere vraag.

```
bron ──generated──► emissie ──(verspreiding)──► immissie ──detected by──► sensor
(activiteit of       (prov:Entity; FOI van        (prov:Entity; bij een
 installatie)         brongerichte waarnemingen)   gebeurtenis ook sosa:Stimulus)
                                                         │ op
                                                         ▼
                                      plaats (Platform + FOI + SpatialSample
                                              van de omgeving van de bron)
```

## Het patroon

```turtle
keten:geluidsemissie-4853D3-… a prov:Entity , sosa:FeatureOfInterest ;
    prov:wasGeneratedBy ex:vlucht-4853D3-… .                  # bronzijde: één emissie per vlucht

ex:geluidsevent-M072-2-… a sosa:Stimulus , prov:Entity ;       # ontvangerzijde: de immissie
    prov:wasDerivedFrom keten:geluidsemissie-4853D3-… ;
    prov:qualifiedDerivation [ a prov:Derivation ;            # optioneel: de verspreiding
        prov:entity keten:geluidsemissie-4853D3-… ;
        prov:hadActivity keten:voortplanting-M072-2-… ] ;
    sosa:isDetectedBy ex:geluidsmeter-M072-2 ;
    prov:atLocation ex:meetpost-M072 .

ex:eventcollectie-M072-2-… sosa:wasOriginatedBy ex:geluidsevent-M072-2-… ;
    sosa:hasFeatureOfInterest ex:meetpost-M072 .               # de plaats blijft het studieobject
```

Drie soorten waarnemingen, elk met een eigen studieobject:

| Vraag | Studieobject | Verband met de emissie |
|---|---|---|
| wat stoot de bron uit? | de emissie | gegenereerd door de bronactiviteit |
| wat krijgt de plaats? (gemeten) | de plaats | `sosa:wasOriginatedBy` de immissie, die `prov:wasDerivedFrom` de emissie |
| wat krijgt de plaats? (berekend) | de plaats | afgeleide waarneming: `sosa:hasInputValue` naar de emissieresultaten, het model als sensor ([R13](../regels/r13.md)) |

## De regels

1. **De vraag bepaalt het studieobject.** Gaat de vraag over de bron (vrachten, uitstoot per vlucht
   of bedrijf), dan is het studieobject de emissie. Gaat ze over de plaats (blootstelling, hinder,
   toetsing aan een norm), dan is het de plaats. De immissie zelf is nooit het studieobject, ook niet
   als meer bronnen bijdragen.
2. **De immissie-entiteit is optioneel.** Neem ze enkel op als je ze nodig hebt: om een gemeten
   waarde toe te wijzen aan een bron, om bronnen uit elkaar te houden, of om gemeten en berekend per
   bron te vergelijken. Anders volstaan de plaats en haar eigenschap.
3. **Fysica tussen de dingen, afleiding tussen de data.** Tussen de entiteiten is de relatie
   `prov:wasDerivedFrom`. Tussen resultaten bestaat een afleiding enkel voor een *berekende* immissie.
   Een *gemeten* immissie heeft nooit `sosa:hasInputValue` naar emissieresultaten. En nooit
   `ex:plaats prov:wasDerivedFrom ex:emissie`: de plaats is niet afgeleid van de emissie.
4. **Meer bronnen, meer plaatsen.** Eén emissie kan meer immissies geven (één vlucht, vier
   meetposten), en één immissie kan van meer emissies afgeleid zijn. Een gemeten waarde is de som van
   de bijdragen. Een model geeft één afgeleide waarneming per bron, en hun som is zelf een afgeleide
   waarneming.
5. **De verspreiding** wordt enkel een activiteit (*qualified derivation*) als de omstandigheden
   ertoe doen: meteo, afstand, het gebruikte model.
6. **Een stimulus is een gebeurtenis.** De immissie is enkel een `sosa:Stimulus` als ze een
   afgebakend voorval is dat een sensor doet meten, zoals een geluidsevent. Een continue concentratie
   is dat niet.
7. **Niet voor een quasistatisch veld.** Het magnetische veld van een hoogspanningslijn reist niet:
   het bestaat zolang er stroom loopt ([ELF-meetnet](../casussen/elf.md)). Er is dan geen emissie- of
   immissie-entiteit. De omgeving is `prov:wasInfluencedBy` de bron
   ([Ruimtelijk monster](ruimtelijk-monster.md#een-monster-van-wat)). Een *berekend* veld blijft een
   afgeleide waarneming, uit de stroom. Ook een wiskundige relatie tussen grootheden (fluxdichtheid
   is flux per oppervlak) is geen afleiding: ze hoort bij de grootheden, niet tussen resources.

## Waarom het samenhangt met de kernvocabularia

- **PROV-O**: `prov:wasDerivedFrom` beschrijft precies de constructie van een nieuwe entiteit op
  basis van een bestaande, met een activiteit die de ene gebruikt en de andere genereert
  (`prov:qualifiedDerivation`, `prov:hadActivity`).
- **SOSA**: de stimulus is het einde van de keten, bij de sensor (stimulus → sensor → waarneming).
  De emissie en de plaats zijn elk een `sosa:FeatureOfInterest` van hun eigen waarnemingen.
- **R13**: een berekende immissie is een afgeleide waarneming zoals elke andere: `sosa:hasInputValue`
  naar de resultaten van de emissie.

## Kiezen

**Kies het** wanneer zowel de bron als de plaats ertoe doen, of wanneer gemeten en berekende
immissies per bron vergeleken worden: geluidskaarten tegenover meetposten, luchtkwaliteitsmodellen
tegenover meetstations, lozingen tegenover de kwaliteit van de ontvangende waterloop.

**Liever niet** wanneer enkel één van de twee vragen speelt: dan volstaat
[Emissie als studieobject](emissie.md) of de plaats met haar eigenschap, eventueel met een
[Stimulus](stimulus.md).

## Gebruikt in

- [Geluidsmeetnet, keten](../casussen/geluidsmeetnet.md#een-keten): vlucht TRA15N, één emissie, vier
  immissies op vier meetposten. De keten verbindt het hoofdmodel en het alternatief.
- [ELF-meetnet](../casussen/elf.md): als tegenvoorbeeld (regel 7).

??? quote "Normatieve tekst (modelleergids, Engels)"

    --8<-- "kit/patroon-emissie-immissie.md"
