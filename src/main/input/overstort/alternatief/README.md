# Overstort — alternatief: de overstorting als emissie

## Intentie

Een discussievoorstel naast het hoofdmodel (`../overstort_herzien.ttl`), geen herziening. In het
hoofdmodel is het **meetpunt** (het overstortpunt) het studieobject: een event is een observatie
van de werking van de overstort op die plaats. Hier is een overstorting een **emissie**:
`wk:Emissie`, `prov:Entity` en `sosa:FeatureOfInterest`, het resultaat van de werking van de
overstort (`sosa:Actuation`), op het meetpunt (`prov:atLocation`). Dat is hetzelfde patroon als
de lozing in `../../waterkwaliteit/` (beslisdocument A5, A14) en het geluidsevent in
`../../geluidsmeetnet/alternatief/` (oslo-ld-kit, `patterns.md`: *Emission as feature of
interest*).

Beide lezingen staan naast elkaar om in de werkgroep te bespreken. De argumenten voor en tegen,
een tussenvorm en de discussievragen staan in `bespreking.md` §6.

**Status:** voorstel (12 oktober 2026). Hoofdmodel: voorstel.

## Bron en selectie

| Record | Bron | Waarom |
|---|---|---|
| (a) event `4004f4ea-…`, status NietInWerking, meetpunt P_000000350733 | `../source/overstort.trig` (LDES-output) | het enige event in de LDES-output; toont wat er gebeurt met een event zonder overstorting |
| (b) overstorting 27 juli 2024 14:00–14:04 UTC, status InWerking, overstortduur 240, debiet 2.3 | `../source/overstort-debiet-overstortduur.json.txt` (doelmodel van Aquafin) | een event mét overstorting, met de grootheden die een emissie typeren |

Het meetpunt van (b) staat niet in het record. De coördinaten zijn gelijk aan die van meetpunt
P_000000217952 in `../source/overstort-input-voorbeelden.md`; die koppeling is een aanname. De bron
geeft het debiet (2.3) zonder eenheid; voor dit voorbeeld is m³/s (`unit:M3-PER-SEC`) aangenomen.
Die eenheid is verzonnen, niet bevestigd door Aquafin.

## Transformatie

Met de hand opgesteld (geen script), zoals het hoofdmodel. Wordt het alternatief gekozen, dan
moet de CONSTRUCT voor de eventstroom (`../source/overstort-mapping.rq`) per status een andere
vorm maken: bij `InWerking` een emissie, een actuatie en een observatiecollectie (status, overstortduur, debiet); bij de andere
statussen een observatie op het meetpunt, zoals in het hoofdmodel.

## Bestanden

| Bestand | Inhoud |
|---|---|
| `overstort_emissie.ttl` | alternatief: records (a) en (b) (124 triples) |
| `overstort_emissie.mmd` | diagram van het alternatief |
| `overstort_vergelijking.mmd` | hoofdmodel en alternatief naast elkaar voor record (b), toegespitst op het studieobject |
| `bespreking.md` | de negen secties, met de argumenten in §6 |

## Verschillen met het hoofdmodel

| Aspect | Hoofdmodel | Alternatief |
|---|---|---|
| Studieobject van een event met overstorting | meetpunt (`sosa:Platform`, `sosa:FeatureOfInterest`) | overstorting (`wk:Emissie`, `prov:Entity`, `sosa:FeatureOfInterest`) |
| Studieobject van een event zonder overstorting | meetpunt | meetpunt (ongewijzigd) |
| Meetpunt → event met overstorting | `sosa:hasFeatureOfInterest` | `prov:atLocation` (van de emissie) |
| Werking van de overstort | geobserveerde property (`kenmerk:Overstort`) | ook een `sosa:Actuation` op het meetpunt met de emissie als resultaat |
| Status `InWerking` | informatief resultaat | redundant: een emissie bestaat enkel bij een overstorting |
| Overstortduur, debiet | observaties van het meetpunt | observaties van de emissie |
| Procedure | geen | `alt:procedure-overstorten` (`sosa:ActuatingProcedure`), vereist door `wk:Emissie` |
| IRI's | `sensor:`, `event:`, `meetpunt:`, … | dezelfde voor gedeelde resources; `alt:` voor emissie, actuatie, collectie, observaties en resultaten |

## Gebruik

Valideren met `mcp__ld-vocab__validate_file` op
`src/main/input/overstort/alternatief/overstort_emissie.ttl`.
