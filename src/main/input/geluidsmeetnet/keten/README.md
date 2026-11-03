# Geluidsmeetnet — de keten emissie → immissie

## Intentie

Het hoofdmodel (`../geluidsmeetnet.ttl`) en het alternatief (`../alternatief/`) lezen het geluidsevent
verschillend. In het hoofdmodel is het een `sosa:Stimulus` en is de meetpost het studieobject. In
het alternatief is het een emissie en zelf het studieobject. Dit bestand toont dat beide lezingen
**schakels van één keten** zijn, volgens het patroon *Emissie en immissie* van de modelleergids:

```
vlucht ─generated→ geluidsemissie ─(voortplanting)→ geluidsevent bij een meetpost ─detected by→ geluidsmeter
                   (bronzijde)                      (immissie = sosa:Stimulus)
                                                          ▲ wasOriginatedBy
                                     eventcollectie ─hasFeatureOfInterest→ meetpost
```

- **De emissie** is het geluid van de vlucht aan de bron: één per vlucht, `prov:wasGeneratedBy` de
  vlucht. Ze is het studieobject van brongerichte waarnemingen, zoals het geluidsvermogen of het
  certificatieniveau. Die staan niet in de export.
- **De immissie** is het geluid zoals het een meetpost bereikt: het geluidsevent van het hoofdmodel,
  ongewijzigd een `sosa:Stimulus`, en nu ook `prov:wasDerivedFrom` de emissie. Eén emissie geeft
  hier vier immissies, op F041, F045, M071 en M072.
- **De verspreiding** (geluidsvoortplanting) is voor M072 uitgewerkt als activiteit met een
  *qualified derivation* (`prov:Derivation`, `prov:hadActivity`). Voor de andere drie events volstaat
  `prov:wasDerivedFrom`.
- **De meetpost** blijft het studieobject van de metingen: de vraag is wat de plaats te verduren
  krijgt.

Zo is het alternatief geen concurrent van het hoofdmodel meer. Elk beantwoordt een andere vraag:
wat stoot de vlucht uit, en wat krijgt de meetpost. In het alternatief is het geluid bij de meetpost
de emissie. In de keten is dat de immissie, en de emissie ligt bij de bron. Dat komt overeen met
*alternatief B* in `../alternatief/bespreking.md` §6.6 (één emissie per vlucht), maar zonder het
event als `sosa:Sample`: een immissie is geen monster van een emissie, maar is ervan afgeleid.

## Bronbestand

`../brondata/20260929_EBBR_NoiseEvents.csv`: de vier rijen van vertrek **TRA15N** (Mode S 4853D3,
B738, EBBR → LEAL, baan 25R, 29/09/2026 06:58), dezelfde als in `../alternatief/`. De
meetwaarden van M072 zijn die van het hoofdmodel.

## Transformatie

Handmatig opgesteld (geen script). IRI's onder `ex:` zijn die van het hoofdmodel: vlucht, events,
meetpost, observaties. De nieuwe resources van de keten (emissie, voortplanting, afleiding) staan
onder `keten:` (`https://example.org/geluidsmeetnet/keten/`).

## Bestanden

| Bestand | Inhoud |
|---|---|
| `geluidsmeetnet_keten.ttl` | De keten voor vlucht TRA15N: emissie, vier immissies, de metingen op M072 (≈145 triples). Door de bulkvalidatie gevalideerd. |
| `geluidsmeetnet_keten.mmd` | Diagram van de keten: bronzijde, verspreiding, ontvangerzijde |

## Wat niet in de export staat

- **Brongerichte waarnemingen** van de emissie (geluidsvermogen): de emissie heeft hier geen
  waarnemingen.
- **Berekende immissie.** Een geluidsmodel dat het niveau op een meetpost berekent uit de emissie,
  zou een afgeleide waarneming van de meetpost geven (R13), met `sosa:hasInputValue` naar de
  emissieresultaten en het model als `sosa:Sensor`. Aerovision meet enkel.
- **De positie van de meetposten**: de SHACL-warning van R11 (geen geometrie) blijft, zoals in het
  hoofdmodel.

## Validatie

`mcp__ld-vocab__validate_file` op `src/main/input/geluidsmeetnet/keten/geluidsmeetnet_keten.ttl`:
geen fouten, geen suspects in het vocabularium, geen disjunctiefouten. Er blijft één SHACL-warning
(R11, geometrie van meetpost M072), om dezelfde reden als in het hoofdmodel.
