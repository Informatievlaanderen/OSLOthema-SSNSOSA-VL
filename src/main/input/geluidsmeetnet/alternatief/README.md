# Geluidsmeetnet — alternatief: het geluidsevent als emissie

## Intentie

Discussievoorstel naast het hoofdmodel (`../geluidsmeetnet.ttl`). In het hoofdmodel is het
geluidsevent een `sosa:Stimulus` en is de **meetpost** het FeatureOfInterest. Hier is het
geluidsevent een **emissie**: `wk:Emissie`, `prov:Entity` en `sosa:FeatureOfInterest`,
`prov:wasGeneratedBy` de vlucht (`prov:Activity`). Dat is hetzelfde patroon als de lozing in
`../../waterkwaliteit/` (beslisdocument A5, A14).

Het voorbeeld is geen herziening: beide lezingen staan naast elkaar om in de werkgroep te
bespreken. De argumenten voor en tegen, een tussenvorm (alternatief B: één emissie per vlucht,
het event als `sosa:Sample`) en de discussievragen staan in `bespreking.md` §6.

## Bronbestand

`../brondata/20260929_EBBR_NoiseEvents.csv`: de vier rijen van vertrek **TRA15N** (Mode S
4853D3, B738, EBBR → LEAL, baan 25R, 29/09/2026 06:58), die op meetposten F041, F045, M071 en
M072 een event gaf. Vluchtgegevens zoals in `../geluidsmeetnet.ttl`.

## Transformatie

Handmatig opgesteld uit de vier CSV-rijen (geen script): de selectie (één vlucht, vier meetposten)
wijkt af van de subset van het hoofdmodel (één meetpost, 58 events), en het doel is vergelijken,
niet volledigheid. Wordt het alternatief aangenomen, dan volstaat een kleine aanpassing van
`../scripts/geluidsmeetnet_to_rdf.py` (FOI en typering van het event).

## Bestanden

| Bestand | Inhoud |
|---|---|
| `geluidsmeetnet_emissie.ttl` | Alternatief A: vlucht TRA15N, 4 emissies, 4 eventcollecties, 16 observaties (≈450 triples). Door de pipeline gevalideerd. |
| `geluidsmeetnet_emissie.mmd` | Diagram van alternatief A, uitgewerkt voor het event op M072 |
| `geluidsmeetnet_vergelijking.mmd` | Hoofdmodel, alternatief A en alternatief B naast elkaar, toegespitst op het FOI |
| `bespreking.md` | De negen secties, met de argumenten in §6 |

## Verschillen met het hoofdmodel

| Aspect | Hoofdmodel | Alternatief A |
|---|---|---|
| Geluidsevent | `sosa:Stimulus`, `prov:Entity` | `wk:Emissie`, `prov:Entity`, `sosa:FeatureOfInterest` |
| FOI van LAeq, LAmax, SEL, duur | meetpost | geluidsevent (emissie) |
| Koppeling collectie → event | `sosa:wasOriginatedBy` | `sosa:hasFeatureOfInterest` |
| Koppeling collectie → meetpost | `sosa:hasFeatureOfInterest` | `prov:atLocation` |
| FOI van de dagindicatoren | meetpost | meetpost (ongewijzigd) |
| Vlucht → events | `prov:wasGeneratedBy` | idem, plus inverse `prov:generated` |
| IRI's | `ex:` | `ex:` voor gedeelde resources, `alt:` voor collecties, observaties en resultaten |

## Gebruik

```bash
mvn compile exec:java      # vanuit de root; valideert ook alternatief/geluidsmeetnet_emissie.ttl
```
