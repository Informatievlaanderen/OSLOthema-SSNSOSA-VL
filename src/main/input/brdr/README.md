# BRDR — provenance van het heraligneren van afbakeningen

Herziening van de provenance-voorbeelden in [`gezever/BRDR`](https://github.com/gezever/BRDR).
De afbakening (geometrie) van een aanduidingsobject van Onroerend Erfgoed, zoals een beschermd
monument, volgt de grenzen van de onderliggende percelen. Wordt een referentielaag zoals GRB-ADP
(de administratieve percelen) gecorrigeerd, dan moet de afbakening opnieuw gealigneerd worden. De
Python-bibliotheek [brdr](https://github.com/OnroerendErfgoed/brdr) (Onroerend Erfgoed en Athumi)
stelt daarvoor kandidaten voor. Van dat proces willen we de volledige provenance vastleggen:

1. aligneren en kandidaten voorstellen, één per *relevante afstand*;
2. elke kandidaat evalueren op zijn overlap met de percelen;
3. de resultaten vergelijken met de *formule* van de huidige afbakening;
4. één kandidaat kiezen als nieuwe afbakening.

Het voorbeeld is een provenance-log: niet alles is in SOSA uitgedrukt. Waar SOSA past
(waarnemingen van bedekking, de wijziging van de afbakening), wordt het gebruikt. De rest is
PROV-O en P-PLAN.

## Bron

Ontvangen materiaal in `source/`, ongewijzigd (commit `77f589a` van `gezever/BRDR`):

| Bestand | Inhoud |
|---|---|
| `source/features-geometries.trig` | het object, zijn geometrie en drie perceelgeometrieën (`src/examples/features-geometries.ttl`) |
| `source/alignment.trig` | de alignering als `sosa:Actuation` met een `prov:Collection` van drie kandidaten |
| `source/evaluatie.trig` | zes observaties van de overlap van kandidaat *a* met de percelen |
| `source/selectie.trig` | de keuze van kandidaat *b* als `prov:Activity` |
| `source/ssn_properties.trig` | de twee eigenschappen (`ssn:Property`) |
| `source/ontology.trig` | kopieën van de gebruikte SOSA-, PROV- en GeoSPARQL-termen, plus `erfgoed:full` en `erfgoed:percentage` |
| `source/brdr1.json` | voorbeeld van een brdr-formule (JSON): bedekking per perceel, open domein, versiedatums |
| `source/BRDR-Readme.md` | de README van `gezever/BRDR` met de vier stappen |

De Turtle is als `.trig` opgeslagen, zodat de bulkvalidatie hem overslaat (CLAUDE.md §4).

Achtergrond over brdr zelf: de broncode van `OnroerendErfgoed/brdr` (`brdr/enums.py` voor de
evaluatieklassen, `brdr/aligner.py` voor de formule, `brdr/descriptor.py` en `brdr/metadata.py`
voor brdr's eigen SOSA-metadata).

## Transformatie

Geen. Bij BRDR werden de Turtle-voorbeelden met de hand geschreven en met `src/frame_from_ttl.js`
naar JSON-LD geframed. Hier is de herziene versie met de hand afgeleid uit de bron. De
afbakening is de originele geometrie; de twee kandidaten en hun bedekkingspercentages zijn
illustratief.

## Mappingkeuzes

Drielaags (R4): een proces met vier stappen, dat voor elk aanduidingsobject opnieuw loopt, met
herleidbaarheid naar het plan als doel.

- **Planning:** `plan:heraligneren` met de stappen aligneren, evaluatie, vergelijking en selectie,
  en hun variabelen (relevante afstand, kandidaat, bedekking, evaluatieklasse, afbakening).
- **Deployment:** de heralignering op ADP 2025-09-15 als `sosa:Deployment` van brdr 0.9.0, met
  `prov:hadPlan`.
- **Execution:** aligneren is een `p-plan:Activity` (geen SOSA). Evaluatie en vergelijking zijn
  `sosa:Observation`s door brdr als `sosa:Sensor`. De selectie is de `sosa:Actuation` die de
  afbakening van het object wijzigt. Nieuwe en oude afbakening zijn verbonden met
  `prov:wasRevisionOf`.

Zie `bespreking.md`.

**Alternatief:** [`alternatief/`](alternatief/README.md) volgt de lezing van brdr zelf: elke
alignering is een `sosa:Actuation` op de afbakening, en het referentieperceel is het studieobject
van de bedekking. Naast dit model, voor de werkgroep.

## Diagram

- `brdr_herzien.mmd` — het herziene model (drielaags).
- `brdr_vergelijking.mmd` — origineel en herziening naast elkaar.

## Outputbestanden

| Bestand | Inhoud |
|---|---|
| `brdr_herzien.ttl` | herziene versie: plan, inzet, referentiedata, twee kandidaten, evaluatie, vergelijking, selectie |
| `brdr_herzien.mmd` | diagram van de herziene versie |
| `brdr_vergelijking.mmd` | vergelijkingsdiagram |
| `bespreking.md` | bespreking in negen secties |

## Gebruik

```bash
riot --validate source/*.trig brdr_herzien.ttl
```

Valideren met `mcp__ld-vocab__validate_file` op `src/main/input/brdr/brdr_herzien.ttl`.

## Verbeterpunten

Diagnose van de vijf databestanden in `source/`, samengevoegd, met `validate_file`: 1 `[error]`
en 3 `[suspect]` onder `[VOCAB]`, 4 `[hint]`s voor `ssn:`-termen, 7 `[DISJOINTNESS]`-schendingen
en 34 SHACL-schendingen. Elk punt: origineel → herzien → motivatie.

1. **Observaties als gebruikte entiteit.** `erfgoed:selectie prov:used erfgoed:alignment_evaluatie1aa, …`
   → `exec:selectie-1-2025-09-15 sosa:hasInputValue ent:evaluatieklasse-1-rd1, ent:evaluatieklasse-1-rd2`
   (de resultaten van de vergelijking) → het bereik van `prov:used` is `prov:Entity`, en een
   `sosa:Observation` is een `prov:Activity`. PROV-O verklaart die twee klassen disjunct, dus
   leveren de zes observaties zes `[DISJOINTNESS]`-schendingen op (R7, R16). Een activiteit gebruikt
   de *resultaten* van een andere activiteit, niet de activiteit zelf.

2. **`prov:generatedAtTime` op een activiteit.** `erfgoed:selectie prov:generatedAtTime …` →
   `ent:afbakening-1-v2 prov:generatedAtTime …` en `sosa:resultTime` op de selectie →
   `prov:generatedAtTime` heeft als domein `prov:Entity`. Op een activiteit geeft dat de zevende
   schending (R16). Het tijdstip waarop de nieuwe geometrie ontstaat, hoort bij die geometrie.

3. **Wat de alignering verandert.** `erfgoed:aligning1 a sosa:Actuation` met als feature of
   interest de geometrie en als resultaat een `prov:Collection` van drie kandidaten → aligneren
   als `p-plan:Activity` die per relevante afstand één kandidaat genereert; de *selectie* is de
   `sosa:Actuation`, met als feature of interest het aanduidingsobject en
   `sosa:actsOnProperty prop:afbakening` → een actuatie verandert de toestand van haar feature of
   interest (SOSA 2023). Aligneren stelt enkel kandidaten voor; pas de keuze wijzigt de
   afbakening van het object. De geometrie is de *waarde* van die eigenschap, niet het
   studieobject (SHACL: `erfgoed:geometry1` is geen `sosa:FeatureOfInterest`). brdr leest het zelf
   anders; die lezing staat als alternatief in [`alternatief/`](alternatief/README.md).

4. **Eén actuatie voor alle kandidaten, zonder inputwaarden.** `erfgoed:aligning1` met één
   `ssn:hasInput erfgoed:parameters_xyz` op de procedure → een `p-plan:Activity` per relevante
   afstand (`exec:aligneren-1-rd1`, `-rd2`), elk met `prov:used` naar haar eigen waarde
   (`ent:relevante-afstand-1m`, `-2m`, als `qudt:QuantityValue`), de strategie voor het open domein
   en de overlapdrempel → elke kandidaat moet terug te voeren zijn op de parameters die hem
   opleverden (R5). In het origineel hebben de drie kandidaten dezelfde WKT en is niet te zien
   waarin ze verschillen.

5. **Dubbele generatie.** `erfgoed:alignment1b` is resultaat van `erfgoed:aligning1`
   (`sosa:hasResult ⊂ prov:generated`) en wordt nog eens `prov:generated` door `erfgoed:selectie`
   → de selectie genereert een nieuwe entiteit, `ent:afbakening-1-v2`, met
   `prov:wasDerivedFrom ent:kandidaat-1-rd2` en `prov:wasRevisionOf ent:afbakening-1-v1`; de oude
   afbakening krijgt `prov:wasInvalidatedBy` de selectie → in PROV-O heeft een entiteit één
   generatie. De versieketen van de afbakening, de kern van een provenance-log, ontbrak.

6. **Evaluatie van één kandidaat.** De zes observaties hebben allemaal `erfgoed:alignment1a` als
   feature of interest; kandidaat *b*, die gekozen wordt, is niet geëvalueerd → een
   `sosa:ObservationCollection` per kandidaat, plus de *formule* van de huidige afbakening
   (`exec:formule-1-v1`) → zonder evaluatie van elke kandidaat en zonder de formule is de keuze
   niet te verantwoorden.

7. **Stap 3 ontbrak.** Het vergelijken van de resultaten (README van BRDR) had geen activiteit →
   `exec:vergelijking-1-rd1`, `-rd2` als afgeleide observaties, met de bedekkingen als
   `sosa:hasInputValue`, de bronobservaties als `sosa:relatedObservation` en de evaluatieklasse van
   brdr (`cl:equality_by_id`, `cl:to_check_no_prediction`) als resultaat (R7, R13). De klassen
   komen uit de enum `Evaluation` van brdr en staan als SKOS-codelijst `cl:evaluatie` in de data.

8. **Perceel als gebruikte entiteit.** `prov:used <…/24504D0692/00B000>` op een observatie →
   `sosa:hasInputValue` naar de perceelgeometrie, die overeenkomt met `sosa:hasInput
   var:referentiegeometrie` van `step:evaluatie` (R5, R13).

9. **Percentage zonder eenheid.** `sosa:hasSimpleResult 100.0` voor de bedekking →
   `sosa:hasResult [ a qudt:QuantityValue ; qudt:numericValue 100.0 ; qudt:hasUnit unit:PERCENT ]`
   (R3). De observaties van `coverage_boolean` (`full`) zijn niet overgenomen: `full` is
   `percentage = 100`, en brdr leidt het zelf zo af (`metadata.py`).

10. **SSN-termen.** `ssn:implements`, `ssn:hasInput`, `ssn:Input`, `ssn:Property` → `sosa:implements`,
    `sosa:hasInput`, `p-plan:Variable`, `sosa:Property` (R14).

11. **`ssn:implements` op een agent.** `erfgoed:agent1 a prov:Agent ; ssn:implements
    erfgoed:selectie_procedure` → `inst:dossierbehandelaar a prov:Person` via
    `prov:wasAssociatedWith` op de selectie → `sosa:implements` heeft als domein `sosa:System`; een
    persoon die een keuze maakt is geen systeem (R1, R16).

12. **WKT zonder CRS.** `geo:asWKT "POLYGON ((173091.23 174049.97, …))"` →
    `"<http://www.opengis.net/def/crs/EPSG/0/31370> POLYGON (…)"` → zonder CRS-IRI is een WKT-literal
    in CRS84 (lengte, breedte in graden; GeoSPARQL 1.0, `geo:wktLiteral`). De coördinaten zijn
    Lambert 72.

13. **Versiedatum van de referentielaag.** `erfgoed:version_date "2024-04-15"^^xsd:date` op elke
    perceelgeometrie → twee datums, zoals brdr ze zelf onderscheidt (`brdr1.json`): de versie van
    de laag (`reference_source.version_date`) als `ent:adp-…`, een `prov:Entity` met `dct:issued`,
    en de versie van elke perceelgeometrie (`version_date`) als `dct:issued` op die geometrie, met
    `dct:isPartOf` de laag en `prov:wasRevisionOf` tussen de versies van perceel 0734 → de
    correctie, de aanleiding van de heralignering, wordt zo een expliciete revisie, en de inzet
    gebruikt de nieuwe laag (`prov:used`). `erfgoed:version_date` bestond in geen vocabularium
    (`[suspect]`).

14. **Capakey als notatie van een geometrie.** `skos:notation "24504D0692/00B000"^^perceel:capakey`
    op een `geo:Geometry`, met IRI `https://data.vlaanderen.be/id/geometry/capakey/…` →
    het perceel met zijn persistente IRI uit het Perceelregister
    (`https://data.vlaanderen.be/id/perceel/24504D0692-00B000`), een `geo:Feature` met
    `dct:identifier "24504D0692/00B000"` en `geo:hasGeometry` naar de geometrie per versie → de
    capakey identificeert het perceel, niet een versie van zijn geometrie, en het perceel heeft al
    een IRI (R10; `linked-data.md`: bestaande IRI's van externe datasets hergebruiken; bespreking §8). Het datatype `perceel:capakey` bestaat niet
    (`[suspect]`), en de IRI's in `data.vlaanderen.be/id/geometry/` zijn niet uitgegeven door de
    beheerder van dat domein (R10). Het voorbeeld met `adms:Identifier` en een datatype in
    `example.com` is niet overgenomen.

15. **`geo:hasMetricArea`.** De oppervlakte van de percelen → niet overgenomen → de term is
    GeoSPARQL 1.1; in dit project is GeoSPARQL 1.0 geladen (`[error]` Unknown property). De
    oppervlakte speelt geen rol in de stappen. <!-- TODO: GeoSPARQL 1.1 laden (R17, alle voorbeelden opnieuw valideren) en de oppervlakte terugzetten? -->

16. **Inconsistenties in de brondata.** In `features-geometries.ttl` is 0692 130,44 m² en 0693
    147,8 m²; in `brdr1.json` en `src/test/test.ttl` is het omgekeerd. In `brdr1.json` heeft
    perceel 0734 versiedatum 2018-12-01, in de Turtle 2024-04-15, en de Turtle dateert alles op
    2024-04-16, een jaar vóór de formule van `brdr1.json` (2025-03-31). De herziening volgt
    `brdr1.json` als formule, en het Perceelregister voor de correctie: perceel 0734 heeft daar
    een versie van 2025-09-03. De heralignering (ADP 2025-09-15) en de keuze (2025-09-17) zijn
    illustratief.

17. **Prefixen en ontologie.** `sdo:` en `schema:` voor dezelfde namespace, en ongebruikte
    prefixen (`owl:`, `vann:`, `qb:`, `parcel:`, `geometry:`, …) → enkel de gebruikte prefixen.
    `ontology.ttl` herhaalt termen uit SOSA, PROV-O en GeoSPARQL, en voegt
    `erfgoed:full`/`erfgoed:percentage` met `qb:concept` toe, die de data niet gebruikt → niet
    overgenomen; de vocabularia worden geladen, niet gekopieerd (R17, criterium 5).
