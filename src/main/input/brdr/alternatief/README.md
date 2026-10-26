# BRDR — alternatief: elke alignering als actuatie (de lezing van brdr)

## Intentie

Een discussievoorstel naast het hoofdmodel (`../brdr_herzien.ttl`), geen herziening. In het
hoofdmodel berekent het aligneren enkel voorstellen (`p-plan:Activity`), en is de **selectie** de
`sosa:Actuation` die de afbakening van het aanduidingsobject wijzigt. Hier is **elke alignering**
een `sosa:Actuation` op de afbakening, met de kandidaat als resultaat, zoals de bibliotheek brdr
het zelf in haar metadata schrijft (`OnroerendErfgoed/brdr`, `brdr/descriptor.py` en
`brdr/metadata.py`). De evaluatie volgt brdr ook: het referentieperceel is het studieobject, de
kandidaat de inputwaarde.

Beide lezingen staan naast elkaar om in de werkgroep te bespreken. De argumenten voor en tegen,
een tussenvorm en de discussievragen staan in `bespreking.md` §6.

**Status:** voorstel (26 oktober 2026). Hoofdmodel: voorstel.

## Bron en selectie

Dezelfde bron als het hoofdmodel (`../source/`), plus de broncode van brdr als bron voor de
vorm van de metadata:

| Element | Bron in brdr | Hier |
|---|---|---|
| actuatie per relevante afstand | `descriptor.py`: `"type": "sosa:Actuation"`, `"sosa:hasFeatureOfInterest"` (het thematische object), `"changes": "geo:hasGeometry"`, `"result"`, `"result_time"` | `alt:aligneren-1-rd1`, `-rd2` |
| procedure met input | `descriptor.py`: `"procedure"` met `"ssn:hasInput"` `brdr:relevant_distance` en een `input_value`; `implementedBy` de processor | `alt:step-aligneren`, `sosa:hasInputValue ent:relevante-afstand-…`, `alt:brdr-0.9.0-aligner` |
| resultaat-IRI | `utils.py`: `urn_from_geom`, een `urn:uuid` uit de SHA-256 van de geometrie | leesbare IRI `alt:kandidaat-1-rd…` (§8) |
| bedekking per perceel | `metadata.py`: `has_feature_of_interest` de referentiegeometrie, `used` het resultaat, `brdr:area_overlap_percentage` | `alt:evaluatie-1-rd…-0734`, `alt:formule-1-v1-0734` |
| volledig bedekt | `metadata.py`: `brdr:area_overlap_full` met het resultaat als studieobject | `alt:volledig-1-rd1`, `-rd2` |
| vergelijking, selectie | niet als RDF (de Evaluator schrijft eigenschappen; geen selectie) | vergelijking zoals in het hoofdmodel; selectie als `prov:Activity` |

Selectie: dezelfde twee kandidaten en dezelfde illustratieve waarden als het hoofdmodel. Van de
bedekkingen is enkel perceel 0734 uitgeschreven; 0692 en 0693 (100 %) volgen hetzelfde patroon.

## Transformatie

Met de hand opgesteld. Wordt dit alternatief gekozen, dan ligt de mapping dicht bij wat brdr al
schrijft: de JSON van `process_result["metadata"]` (met `log_metadata` en `add_observations`)
kan met een JSON-LD-context of een SPARQL CONSTRUCT naar deze vorm. Drie aanpassingen zijn nodig:
`ssn:hasInput` → `sosa:hasInput` (R14), de willekeurige `urn:uuid` van sensor, actuatie en
observaties vervangen door een deterministische sleutel (R10), en de selectie toevoegen, die brdr
niet schrijft.

## Bestanden

| Bestand | Inhoud |
|---|---|
| `brdr_actuatie.ttl` | alternatief, zelfstandig te valideren (302 triples) |
| `brdr_actuatie.mmd` | diagram van het alternatief (drielaags) |
| `brdr_vergelijking.mmd` | hoofdmodel en alternatief naast elkaar voor kandidaat rd2 |
| `bespreking.md` | de negen secties, met de argumenten in §6 |

## Verschillen met het hoofdmodel

| Aspect | Hoofdmodel | Alternatief |
|---|---|---|
| Aligneren | `p-plan:Activity`, geen SOSA; `prov:wasAssociatedWith` brdr | `sosa:Actuation` op `prop:afbakening` van het object, `sosa:madeByActuator` de processor |
| Stap aligneren | `p-plan:Step` | `sosa:ActuatingProcedure` met `sosa:hasInput var:relevante-afstand` |
| Relevante afstand | `prov:used` | `sosa:hasInputValue` |
| Selectie | `sosa:Actuation` op de afbakening, met een nieuwe geometrie als resultaat | `prov:Activity` die de gekozen kandidaat geldig maakt en de rest ongeldig (`prov:wasInvalidatedBy`) |
| Nieuwe afbakening | `ent:afbakening-1-v2`, `prov:wasDerivedFrom` de kandidaat | de gekozen kandidaat zelf (`alt:kandidaat-1-rd2`), `prov:wasRevisionOf` de oude |
| Niet gekozen kandidaat | gewoon een voorstel | resultaat van een actuatie, daarna ongeldig verklaard |
| Studieobject van de bedekking | de kandidaat; het perceel als `sosa:hasInputValue` | de perceelgeometrie; de kandidaat als `sosa:hasInputValue` |
| Volledig bedekt (`full`) | niet overgenomen (= 100 %) | observatie met de kandidaat als studieobject |
| Formule | `sosa:ObservationCollection` met de oude afbakening als studieobject | losse observaties met de perceelgeometrieën in ADP 2025-03-31 als studieobject |
| brdr | `sosa:Sensor` | `sosa:Sensor` met een `sosa:Actuator` als deelsysteem (de processor) |
| IRI's | `exec:`, `ent:`, `step:`, `plan:` | dezelfde voor gedeelde resources (`var:`, `ent:`, `inst:`, `prop:`, `obj:`, `cl:`); `alt:` voor plan, stappen, uitvoeringen, kandidaten en resultaten |

Samen geladen zijn beide bestanden consistent (validatie van de samenvoeging: geen fouten). Het
object heeft dan twee geometrieën, een per lezing.

## Gebruik

```bash
riot --validate brdr_actuatie.ttl
```

Valideren met `mcp__ld-vocab__validate_file` op
`src/main/input/brdr/alternatief/brdr_actuatie.ttl`.
