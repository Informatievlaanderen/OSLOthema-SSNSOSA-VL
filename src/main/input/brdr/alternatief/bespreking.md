# Bespreking — BRDR, alternatief: elke alignering als actuatie

## 1. Wat stelt dit voorbeeld voor?

Dezelfde heralignering als het hoofdmodel (`../bespreking.md`): de afbakening van een
aanduidingsobject van Onroerend Erfgoed wordt opnieuw gelegd op GRB-ADP na een correctie van
perceel 24504D0734/00M000. Het verschil zit in de lezing. Hier volgt het model de metadata die
[brdr](https://github.com/OnroerendErfgoed/brdr) zelf schrijft: elke alignering is een
`sosa:Actuation` die de afbakening van het object wijzigt, en de bedekking is een waarneming van
het referentieperceel. Status: *voorstel*, naast het hoofdmodel.

## 2. Kleurlegenda

| Kleur | SOSA-concept | Betekenis in het domein |
|---|---|---|
| Blauw (#60c4e4) | `sosa:Sensor`, `sosa:Actuator`, `prov:Agent`, `sosa:FeatureOfInterest` | brdr, zijn processor, de dossierbehandelaar, het aanduidingsobject |
| Roze (#e54b89) | `sosa:Actuation`, `sosa:Observation`, `sosa:Deployment`, `prov:Activity` | aligneren, evalueren, vergelijken, selecteren |
| Oranje (#f8b622) | `prov:Entity`, `geo:Geometry`, `qudt:QuantityValue` | geometrieën, parameters, bedekkingen, evaluatieklassen |
| Paars (#7f59ae) | `p-plan:Plan` / `p-plan:Step` | het plan en zijn stappen |
| Oranjerood (#fe7130) | `sosa:Property` / `p-plan:Variable` | afbakening, bedekking, volledig bedekt; variabelen |

## 3. Infrastructuur (blauwe nodes)

- **`inst:brdr-0.9.0`** — `sosa:Sensor`, zoals in het hoofdmodel. Het heeft een deelsysteem
  (`sosa:hasSubSystem`):
- **`alt:brdr-0.9.0-aligner`** — `sosa:Actuator`: de processor van brdr (`AlignerGeometryProcessor`,
  `2024:aligner2024a`), die `alt:step-aligneren` implementeert. brdr noemt de processor als
  `implementedBy` van de procedure.
- **`inst:dossierbehandelaar`**, **`inst:onroerend-erfgoed`**, **`obj:aanduidingsobject-1`** — zoals
  in het hoofdmodel. Het object `geo:hasGeometry` hier de gekozen kandidaat zelf.
- **`alt:heralignering-adp-2024-04-15`** — `sosa:Deployment` van beide systemen, met
  `prov:hadPlan alt:plan-heraligneren`.

## 4. Observatie/Actuatie-structuur (roze nodes)

**Actuaties:**

| IRI | actsOnProperty | usedProcedure | hasResult | hasFeatureOfInterest |
|---|---|---|---|---|
| `alt:aligneren-1-rd1` | `prop:afbakening` | `alt:step-aligneren` | `alt:kandidaat-1-rd1` | `obj:aanduidingsobject-1` |
| `alt:aligneren-1-rd2` | `prop:afbakening` | `alt:step-aligneren` | `alt:kandidaat-1-rd2` | `obj:aanduidingsobject-1` |

Inputwaarde: de relevante afstand. `prov:used`: de huidige afbakening, de perceelgeometrieën en de
instellingen van de processor (strategie open domein, overlapdrempel), die geen input van de
procedure zijn (R5, R13).

**Observaties:**

| IRI | observedProperty | usedProcedure | hasResult | hasFeatureOfInterest |
|---|---|---|---|---|
| `alt:formule-1-v1-0734` | `prop:bedekking-perceel` | `alt:step-evaluatie` | 27,14 % | `ent:perceel-24504D0734-00M000-2018-12-01` |
| `alt:evaluatie-1-rd1-0734` | `prop:bedekking-perceel` | `alt:step-evaluatie` | 24,80 % | `ent:perceel-24504D0734-00M000-2024-04-15` |
| `alt:evaluatie-1-rd2-0734` | `prop:bedekking-perceel` | `alt:step-evaluatie` | 27,14 % | `ent:perceel-24504D0734-00M000-2024-04-15` |
| `alt:volledig-1-rd1` | `alt:volledig-bedekt` | `alt:step-evaluatie` | `false` | `alt:kandidaat-1-rd1` |
| `alt:volledig-1-rd2` | `alt:volledig-bedekt` | `alt:step-evaluatie` | `false` | `alt:kandidaat-1-rd2` |
| `alt:vergelijking-1-rd1` | `prop:evaluatieklasse` | `alt:step-vergelijking` | `cl:to_check_no_prediction` | `alt:kandidaat-1-rd1` |
| `alt:vergelijking-1-rd2` | `prop:evaluatieklasse` | `alt:step-vergelijking` | `cl:equality_by_id` | `alt:kandidaat-1-rd2` |

Geen collecties: brdr schrijft losse observaties, en de bedekkingen van één kandidaat hebben hier
elk een ander studieobject (het perceel), dus is er niets gemeenschappelijks om op een collectie te
zetten behalve de kandidaat als inputwaarde, en die erft niet.

**Selectie:** `alt:selectie-1-2024-04-16`, een `prov:Activity`. Ze `prov:used` de kandidaten en
hun evaluatieklassen, en maakt de oude afbakening en kandidaat rd1 ongeldig.

## 5. Procedure en Property

| Procedure | Klasse | Geïmplementeerd door | Gebruikt door |
|---|---|---|---|
| `alt:step-aligneren` | `sosa:ActuatingProcedure` | `alt:brdr-0.9.0-aligner` | `alt:aligneren-1-rd1`, `-rd2` |
| `alt:step-evaluatie` | `sosa:ObservingProcedure` | `inst:brdr-0.9.0` | formule, evaluatie, volledig bedekt |
| `alt:step-vergelijking` | `sosa:ObservingProcedure` | `inst:brdr-0.9.0` | de twee vergelijkingen |
| `alt:step-selectie` | `p-plan:Step` | — | `alt:selectie-1-2024-04-16` |

brdr heeft een procedure per eigenschap (`brdr:observation_procedure_area_overlap_percentage`,
`…_area_overlap_full`); hier is dat één stap van het plan, met twee eigenschappen.

| Property | Betekenis |
|---|---|
| `prop:afbakening` | de afbakening van het object (gedeeld) |
| `prop:bedekking-perceel` | het deel van het perceel binnen de kandidaat (gedeeld); hier een eigenschap van het perceel |
| `alt:volledig-bedekt` | alle overlappende percelen volledig bedekt door de kandidaat (brdr: `area_overlap_full`) |
| `prop:evaluatieklasse` | overeenkomst met de formule (gedeeld) |

## 6. Modelleer-keuzes toegelicht

**Waarom elke alignering als actuatie?**
Hoofdmodel: aligneren berekent een voorstel; enkel de selectie wijzigt de afbakening.
Alternatief: elke alignering is een `sosa:Actuation` op `prop:afbakening` van het object, met de
kandidaat als resultaat, zoals brdr het schrijft (`"changes": "geo:hasGeometry"`).

*Voor het alternatief:*
- Het volgt de bron. brdr publiceert deze metadata al; de mapping is een kleine stap
  (README, *Transformatie*), en wat Onroerend Erfgoed bewaart, is wat brdr schreef. Het hoofdmodel
  vraagt een eigen omzetting die brdr's actuaties tot activiteiten herleidt.
- Elke kandidaat is herleidbaar tot een SOSA-procedure met haar inputwaarde
  (`sosa:hasInputValue` de relevante afstand); in het hoofdmodel valt het aligneren buiten SOSA en
  is de relevante afstand een gewone `prov:used`.
- De gekozen kandidaat is zelf de nieuwe afbakening; er is geen aparte versie
  (`ent:afbakening-1-v2`) die er een kopie van is. Minder resources, en de geometrie die het
  object krijgt is letterlijk die van de berekening.
- brdr's resultaat-IRI is een hash van de geometrie (`urn_from_geom`): gelijke geometrie, gelijke
  IRI. Daarmee is "dezelfde afbakening als vorig jaar" zonder extra werk te herkennen.

*Tegen het alternatief:*
- Een actuatie wijzigt de toestand van haar studieobject (SOSA 2023, *Actuation*: "changes the
  state of the world"). Hier wijzigen twee actuaties op hetzelfde moment dezelfde eigenschap van
  hetzelfde object, met een ander resultaat. Hoogstens één van beide is gebeurd; de data zegt het
  niet zonder de selectie erbij te halen. Een query "welke wijzigingen kreeg dit object?" telt elke
  kandidaat mee.
- De selectie, het moment waarop de afbakening werkelijk verandert en de verantwoordelijke, is een
  gewone `prov:Activity`. Wie naar de actuaties van een object vraagt, vindt de beslissing niet.
- Bij brdr's `predict` lopen tientallen relevante afstanden (standaard 0 tot 3 m per 0,1 m): dat
  zijn tientallen actuaties per object, waarvan er één geldt.
- Een niet gekozen kandidaat is het resultaat van een actuatie en meteen ongeldig
  (`prov:wasInvalidatedBy`). Dat is een omweg om "voorstel" te zeggen.

*Tussenvorm:* de alignering blijft een `sosa:Actuation`, zoals brdr het schrijft, maar de
actuaties van één heralignering worden gegroepeerd in een `sosa:ActuationCollection`, en de
gekozen actuatie wordt aangeduid met een status of met `prov:used` door de selectie. De
selectie blijft een PROV-activiteit. Zo blijft brdr's metadata ongewijzigd en is "de geldende
wijziging" één stap verder op te vragen. Een tweede tussenvorm is het omgekeerde: het hoofdmodel,
waarbij de omzetting van brdr's metadata de actuaties tot `p-plan:Activity` herleidt en enkel de
gekozen actuatie overneemt.

**Waarom het perceel als studieobject van de bedekking?**
Hoofdmodel: de kandidaat is het studieobject, het perceel een inputwaarde. Alternatief: de
perceelgeometrie is het studieobject en de kandidaat de inputwaarde, zoals brdr
(`has_feature_of_interest: reference_id`, `used: result_id`).

*Voor:* de eigenschap is gedefinieerd als een fractie van het perceel (doorsnede gedeeld door de
oppervlakte van het perceel); wie naar een perceel kijkt, ziet hoe elke kandidaat het bedekt. Het
sluit aan bij de vraag van een referentiebeheerder: welke afbakeningen raakt dit perceel?

*Tegen:* de waarnemingen over één kandidaat hebben drie studieobjecten, en `full` (volledig
bedekt) gaat dan weer over de kandidaat: binnen één evaluatie wisselt het studieobject. Zonder
collectie moeten procedure, sensor en tijdstip op elke observatie herhaald worden. De
vergelijking en de selectie werken per kandidaat; hun inputs komen van observaties van andere
objecten.

**Waarom de inputwaarde in plaats van `prov:used`?**
brdr schrijft `used` voor de kandidaat. Als inputwaarde van de procedure (`sosa:hasInput
var:kandidaatgeometrie`) is `sosa:hasInputValue` de SOSA-vorm; het is een deelproperty van
`prov:used` (R5, R13).

**Waarom de vergelijking zoals in het hoofdmodel?**
brdr schrijft de evaluatieklasse als eigenschap van het resultaat (`brdr_evaluation`), niet als
observatie. Ze hier anders modelleren zou een tweede verschil invoeren dat niets met de lezing van
de alignering te maken heeft.

**Eenheden, vocabularia, record of waarneming** — zoals in het hoofdmodel (QUDT, enkel de kern,
oplossing A van R16).

**Discussievragen voor de werkgroep:**
1. Is een berekend voorstel een wijziging van het object (actuatie), of pas de keuze ervan?
2. Moet de provenance van Onroerend Erfgoed de metadata van brdr letterlijk overnemen, of volstaat
   het dat ze ernaar te herleiden is?
3. Wie is het studieobject van een overlap: het perceel of de kandidaat? Hangt dat af van wie de
   data bevraagt (erfgoedbeheerder of referentiebeheerder)?
4. Worden alle kandidaten bewaard, of enkel de gekozen? Bij enkel de gekozen vervalt het
   belangrijkste bezwaar tegen het alternatief.
5. Kiest brdr soms zelf (bij `prediction_unique` of `equality_by_id`)? Dan is de selectie ook een
   handeling van een systeem, en komt de vraag terug welke resource de actuatie is.

## 7. Tijdsmodellering

Zoals in het hoofdmodel: `sosa:resultTime "2024-04-16T00:00:12+00:00"^^xsd:dateTime` op de actuaties
en observaties (brdr: `result_time`), `prov:endedAtTime` op de selectie, `dct:issued` op de versies
van ADP. De formule heeft geen tijdstip: de bron geeft het niet. De nieuwe afbakening heeft hier geen
`prov:generatedAtTime`: haar generatie is de actuatie, met haar resultaattijd.

## 8. Prefixen en IRI-structuur

| Prefix | Basis-IRI | Tijdelijk of persistent |
|---|---|---|
| `alt:` | `https://example.org/brdr/alternatief/` | tijdelijk; wat enkel in dit alternatief bestaat |
| `var:`, `ent:`, `inst:`, `prop:`, `obj:`, `cl:` | `https://example.org/brdr/…/` | tijdelijk; gedeeld met het hoofdmodel |
| `sosa:`, `prov:`, `p-plan:`, `qudt:`, `unit:`, `geo:`, `skos:`, `dct:`, `xsd:`, `rdf:`, `rdfs:` | zie `../bespreking.md` §8 | persistent |

`plan:`, `step:` en `exec:` van het hoofdmodel komen hier niet voor: plan, stappen en uitvoeringen
verschillen. brdr zelf geeft de actuatie, de sensor en elke observatie een willekeurige `urn:uuid`
(`uuid.uuid4()`), en het resultaat een `urn:uuid` uit de hash van de geometrie. De eerste zijn
niet stabiel (R10); de tweede wel, maar een `urn:uuid` is niet te dereferencen.
<!-- TODO: kan brdr een basis-IRI en een deterministische sleutel krijgen voor actuaties en observaties (bv. object + versie referentielaag + relevante afstand)? -->

## 9. Inverse relaties

Geen, zoals in het hoofdmodel.
