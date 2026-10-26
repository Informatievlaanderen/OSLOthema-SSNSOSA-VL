# Bespreking — BRDR: provenance van het heraligneren van een afbakening

## 1. Wat stelt dit voorbeeld voor?

De provenance van één heralignering: de afbakening van een aanduidingsobject van Onroerend Erfgoed
(hier een illustratief beschermd monument) wordt opnieuw gelegd op de administratieve percelen van
het GRB (ADP), nadat perceel 24504D0734/00M000 in de versie van 15 april 2024 gecorrigeerd is.
De Python-bibliotheek [brdr](https://github.com/OnroerendErfgoed/brdr) maakt per *relevante
afstand* een kandidaat, meet hoe elke kandidaat de percelen bedekt, vergelijkt dat met de
*formule* van de huidige afbakening, en een dossierbehandelaar kiest de kandidaat die de nieuwe
afbakening wordt. Het voorbeeld herziet de mapping in
[`gezever/BRDR`](https://github.com/gezever/BRDR) (zie de verbeterpunten in de README).

Het is een provenance-log, geen zuiver SOSA-model: SOSA beschrijft de waarnemingen en de wijziging
van de afbakening, PROV-O en P-PLAN de rest.

## 2. Kleurlegenda

| Kleur | SOSA-concept | Betekenis in het domein |
|---|---|---|
| Blauw (#60c4e4) | `sosa:Sensor`, `prov:Agent`, `sosa:FeatureOfInterest` | brdr, de dossierbehandelaar, Onroerend Erfgoed, het aanduidingsobject |
| Roze (#e54b89) | `sosa:Observation`, `sosa:ObservationCollection`, `sosa:Actuation`, `sosa:Deployment`, `p-plan:Activity` | aligneren, evalueren, vergelijken, selecteren; de heraligneringscampagne |
| Oranje (#f8b622) | `prov:Entity`, `geo:Geometry`, `qudt:QuantityValue` | geometrieën, referentielagen, parameters, bedekkingen, evaluatieklassen |
| Paars (#7f59ae) | `p-plan:Plan` / `p-plan:Step` | het plan *heraligneren* en zijn vier stappen |
| Oranjerood (#fe7130) | `sosa:Property` / `p-plan:Variable` | afbakening, bedekking, evaluatieklasse; de variabelen van het plan |

## 3. Infrastructuur (blauwe nodes)

- **`inst:brdr-0.9.0`** — `sosa:Sensor`, `sosa:System` en `prov:SoftwareAgent`. brdr is software
  die waarneemt: ze meet de bedekking van de percelen en vergelijkt die met de formule (R1, *agent
  die observaties maakt*). Ze `sosa:implements` de stappen evaluatie en vergelijking. Bij het
  aligneren is ze de agent (`prov:wasAssociatedWith`), zonder SOSA-rol: zie §6. Een `sosa:System` is
  in SSN/SOSA 2023 een `prov:Agent` of een `prov:Entity`; PROV-O verklaart `prov:Agent` en
  `prov:Entity` niet disjunct.
- **`inst:dossierbehandelaar`** — `prov:Person`: de persoon die de kandidaat kiest. Geen
  `sosa:Actuator` (§6).
- **`inst:onroerend-erfgoed`** — `prov:Organization`: voert de campagne uit volgens het plan
  (`prov:qualifiedAssociation` met `prov:hadPlan`).
- **`obj:aanduidingsobject-1`** — `geo:Feature` en `sosa:FeatureOfInterest`: het object waarvan de
  afbakening gewijzigd wordt. Het `geo:hasGeometry` de nieuwe afbakening.
- **`exec:heralignering-adp-2024-04-15`** — `sosa:Deployment`: de inzet van brdr voor de
  aanduidingsobjecten, aanleiding de nieuwe versie van ADP (`prov:used ent:adp-2024-04-15`).

Er is geen `sosa:Platform` en geen `sosa:hosts`: brdr draait niet op een plaats die voor de vraag
iets betekent.

## 4. Observatie/Actuatie-structuur (roze nodes)

**Formule en evaluatie** — drie `sosa:ObservationCollection`s met elk drie leden, één per perceel:

| IRI | observedProperty | usedProcedure | hasResult | hasFeatureOfInterest |
|---|---|---|---|---|
| `exec:formule-1-v1-0692`, `-0693`, `-0734` | `prop:bedekking-perceel` | `step:evaluatie` | 100 %, 100 %, 27,14 % | `ent:afbakening-1-v1` |
| `exec:evaluatie-1-rd1-0692`, `-0693`, `-0734` | `prop:bedekking-perceel` | `step:evaluatie` | 100 %, 100 %, 24,80 % | `ent:kandidaat-1-rd1` |
| `exec:evaluatie-1-rd2-0692`, `-0693`, `-0734` | `prop:bedekking-perceel` | `step:evaluatie` | 100 %, 100 %, 27,14 % | `ent:kandidaat-1-rd2` |

De collectie draagt de eigenschap, de procedure, de sensor, de feature of interest en (bij de
kandidaten) het resultaattijdstip. Elk lid heeft als `sosa:hasInputValue` de perceelgeometrie die
het meet: bij de formule de versie van 2018-12-01, bij de kandidaten die van 2024-04-15.

**Vergelijking** — afgeleide observaties (R13), geen lid van een collectie:

| IRI | observedProperty | usedProcedure | hasResult | hasFeatureOfInterest |
|---|---|---|---|---|
| `exec:vergelijking-1-rd1` | `prop:evaluatieklasse` | `step:vergelijking` | `cl:to_check_no_prediction` | `ent:kandidaat-1-rd1` |
| `exec:vergelijking-1-rd2` | `prop:evaluatieklasse` | `step:vergelijking` | `cl:equality_by_id` | `ent:kandidaat-1-rd2` |

Inputwaarden: de bedekking van perceel 0734 door de kandidaat en door de huidige afbakening;
`sosa:relatedObservation` naar de twee bronobservaties.

**Selectie** — de actuatie:

| IRI | actsOnProperty | usedProcedure | hasResult | hasFeatureOfInterest |
|---|---|---|---|---|
| `exec:selectie-1-2024-04-16` | `prop:afbakening` | `step:selectie` | `ent:afbakening-1-v2` | `obj:aanduidingsobject-1` |

Inputwaarden: de twee kandidaten en hun evaluatieklassen.

**Aligneren** — `exec:aligneren-1-rd1` en `-rd2` zijn `p-plan:Activity`'s zonder SOSA-type: ze
`prov:used` de huidige afbakening, de perceelgeometrieën en de parameters, en genereren elk één
kandidaat.

## 5. Procedure en Property

| Procedure | Klasse | Geïmplementeerd door | Gebruikt door |
|---|---|---|---|
| `plan:heraligneren` | `p-plan:Plan`, `sosa:Procedure` | — (plan van `inst:onroerend-erfgoed`) | `exec:heralignering-adp-2024-04-15` (`prov:hadPlan`) |
| `step:aligneren` | `p-plan:Step` | — | `exec:aligneren-1-rd1`, `-rd2` (`p-plan:correspondsToStep`) |
| `step:evaluatie` | `sosa:ObservingProcedure` | `inst:brdr-0.9.0` | de drie collecties |
| `step:vergelijking` | `sosa:ObservingProcedure` | `inst:brdr-0.9.0` | `exec:vergelijking-1-rd1`, `-rd2` |
| `step:selectie` | `sosa:ActuatingProcedure` | — | `exec:selectie-1-2024-04-16` |

| Property | Betekenis |
|---|---|
| `prop:afbakening` | de afbakening (geometrie) van een aanduidingsobject; de geometrie zelf is de waarde |
| `prop:bedekking-perceel` | het deel van een referentieperceel dat binnen een geometrie valt: oppervlakte van de doorsnede gedeeld door de oppervlakte van het perceel (brdr: `area_overlap_percentage`); 100 % is een volledig bedekt perceel (`full`) |
| `prop:evaluatieklasse` | hoe goed de bedekkingen van een kandidaat overeenkomen met de formule (brdr: `evaluation`) |

## 6. Modelleer-keuzes toegelicht

**Waarom is de selectie de actuatie, en het aligneren niet?**
Verworpen alternatief: elke alignering is een `sosa:Actuation` met de kandidaat als resultaat, zoals
in de bron en zoals brdr het zelf doet (`descriptor.py` maakt per relevante afstand een
`sosa:Actuation` met `ssn:hasInput brdr:relevant_distance`, `metadata.py` observaties per perceel).
Gekozen aanpak: aligneren is een `p-plan:Activity` die een voorstel genereert; de selectie is de
`sosa:Actuation` op `prop:afbakening` van het aanduidingsobject.
Motivatie: een actuatie verandert de toestand van haar feature of interest (SOSA 2023). Aligneren
laat het aanduidingsobject ongemoeid: van twee kandidaten wordt er één de afbakening, de andere
verandert niets. Een actuatie per kandidaat zou dus wijzigingen registreren die nooit gebeurden.
`sosa:Execution` als neutraal type kan niet: SOSA 2023 noemt die klasse abstract. brdr's eigen lezing
(een actuatie per kandidaat) is uitgewerkt als alternatieve mapping in
[`alternatief/`](alternatief/README.md), met de argumenten voor en tegen en discussievragen.
Status van beide: *voorstel*.

**Waarom is de kandidaat de feature of interest van de evaluatie, en niet het perceel?**
Verworpen alternatief: het perceel als feature of interest en de kandidaat als `prov:used`, zoals
brdr in `metadata.py` (`has_feature_of_interest: reference_id`, `used: result_id`). Gekozen
aanpak: de kandidaat is de feature of interest; de perceelgeometrie is een `sosa:hasInputValue`,
die overeenkomt met `sosa:hasInput var:referentiegeometrie` van de stap.
Motivatie: de vraag van de evaluatie gaat over de kandidaat (hoe verhoudt hij zich tot de
percelen?), en de vergelijking en de selectie werken per kandidaat. De eigenschap is een relatie
tussen twee geometrieën; met de kandidaat als feature of interest zitten alle waarnemingen over één
kandidaat in één collectie. Bij brdr's lezing is het perceel het studieobject en staat de kandidaat
in `prov:used`, dat buiten de procedure valt (R5). Ook die lezing staat in
[`alternatief/`](alternatief/README.md).

**Waarom een formule als aparte collectie?**
De vergelijking van brdr (`Evaluator`) zet de bedekkingen van een kandidaat naast die van de
huidige afbakening bij de vorige alignering, de *formule* (`brdr1.json`). Zonder die waarnemingen
is de evaluatieklasse niet te verklaren. `exec:formule-1-v1` heeft als feature of interest de oude
afbakening en als inputwaarden de perceelgeometrieën van ADP 2018-12-01.
<!-- TODO: wanneer en met welke brdr-versie is de formule van de huidige afbakening berekend? Het tijdstip ontbreekt in de bron; inst:brdr-0.9.0 als sensor van de formule is een aanname. -->

**Waarom zijn alleen de resultaten van perceel 0734 inputwaarden van de vergelijking?**
De twee andere percelen zijn bij de formule en bij beide kandidaten volledig bedekt (100 %); het
onderscheid zit in 0734. Een volledige afleiding zou alle zes resultaten noemen (R13); dat maakt
het voorbeeld langer zonder iets toe te voegen. In een gegenereerde dataset hoort het wel.

**Waarom een SKOS-codelijst voor de evaluatieklasse?**
De klassen van de brdr-enum `Evaluation` benoemen enkel een uitkomst; ze hebben geen eigen regels
(R18). Er is geen register voor; `cl:evaluatie` neemt de twaalf waarden van de enum letterlijk over,
met de waarde als `skos:notation`. Het resultaat van de vergelijking is een `prov:Entity` met
`rdf:value` naar het begrip, zoals de factorscores in `PGD_geschiktheidskaart/`.
<!-- TODO: moet cl:evaluatie een codelijst van Onroerend Erfgoed worden, met een eigen namespace? -->

**Waarom geen `sosa:madeByActuator` op de selectie?**
De keuze maakt een persoon (`prov:wasAssociatedWith inst:dossierbehandelaar`). Een persoon is geen
`sosa:System`. Welk systeem de nieuwe afbakening wegschrijft (de inventaris?), zegt de bron niet;
zoals bij de passieve bron in het patroon *Emissie als studieobject* blijft de actuator weg.
<!-- TODO: kiest altijd een persoon, of kiest brdr automatisch bij prediction_unique / equality_by_id? Dan is de selectie ook een stap van brdr. -->

**Waarom een nieuwe geometrie, en niet de kandidaat zelf als resultaat?**
In PROV-O heeft een entiteit één generatie. De kandidaat is gegenereerd door het aligneren; de
selectie genereert `ent:afbakening-1-v2`, met `prov:wasDerivedFrom` de kandidaat en
`prov:wasRevisionOf` de oude afbakening. De oude afbakening krijgt `prov:wasInvalidatedBy` de
selectie. Zo is de versieketen van de afbakening, en de reden van elke versie, op te vragen.

**De aanleiding als revisie.** De correctie van perceel 0734 is een `prov:wasRevisionOf` tussen
twee perceelgeometrieën, elk `dct:isPartOf` een versie van ADP. De inzet `prov:used` de nieuwe
versie. Zo kan je vragen welke afbakeningen door welke correctie veranderd zijn.

**Waarneming of record (R16)?** De waarnemingen zijn hier zelf de gepubliceerde resources
(oplossing A van R16): er staan geen recordeigenschappen (`prov:generatedAtTime`, …) op een
activiteit. `prov:generatedAtTime` staat enkel op de nieuwe afbakening, een entiteit.

**Drielaags of plat (R4)?** Drielaags: vier stappen met elk een eigen rol, een plan dat voor elk
aanduidingsobject opnieuw loopt, en herleidbaarheid van elke kandidaat naar zijn parameters.

**Eenheden (R3).** QUDT: `unit:PERCENT` voor bedekking en overlapdrempel, `unit:M` voor de
relevante afstand. Geen registereenheden.

**Vocabularia.** Enkel de kern (R17, niveau 1): SOSA/SSN 2023, PROV-O, P-PLAN, QUDT, GeoSPARQL 1.0,
SKOS, DCTERMS. Geen afweging buiten de kern nodig. `geo:hasMetricArea` (GeoSPARQL 1.1) is niet
geladen; de oppervlakte van de percelen is daarom niet overgenomen (README, punt 15).

**Feature of interest op de leden.** SOSA 2023 laat de leden van een collectie de feature of
interest erven, maar de SHACL die uit de ontologie gegenereerd wordt, ziet dat niet (de restrictie
staat op `sosa:Execution`). Daarom staat `sosa:hasFeatureOfInterest` ook op elk lid.

**Niet overgenomen uit brdr.** Het *open domein* (het deel van de afbakening buiten de percelen,
`reference_od`), de stabiliteit en de `prediction_score` van een kandidaat, en de oppervlaktes.
Elk kan als bijkomende waarneming in dezelfde collectie, met een eigen `sosa:Property`.

**Perceelgeometrieën zonder WKT.** De bron geeft geen coördinaten van de percelen; de geometrieën
zijn er als entiteiten, met hun versie, zonder `geo:asWKT`.

## 7. Tijdsmodellering

- **`sosa:resultTime "2024-04-16T00:00:12+00:00"^^xsd:dateTime`** op de evaluatiecollecties, de
  vergelijkingen en de selectie: het tijdstip uit de bron, met zijn tijdzone (UTC). Geen
  `sosa:phenomenonTime`: de bedekking is een eigenschap van twee geometrieën, niet van een
  verschijnsel in de tijd.
- **`prov:endedAtTime`** op de aligneringen: een `p-plan:Activity` is geen SOSA-uitvoering, dus
  geen `sosa:resultTime`.
- **`prov:generatedAtTime`** op de nieuwe afbakening: wanneer de versie ontstond.
- **`dct:issued "…"^^xsd:date`** op de versies van ADP: een datum zonder tijdstip.
- Alle tijdstippen uit de bron zijn gelijk (00:00:12 UTC). In werkelijkheid ligt de keuze van de
  dossierbehandelaar later dan de berekening. <!-- TODO: het werkelijke tijdstip van de selectie; is de vorige alignering (de formule) gedateerd? -->

## 8. Prefixen en IRI-structuur

| Prefix | Basis-IRI | Tijdelijk of persistent |
|---|---|---|
| `plan:` | `https://example.org/brdr/plan/` | tijdelijk (illustratief) |
| `step:` | `https://example.org/brdr/step/` | tijdelijk |
| `var:` | `https://example.org/brdr/var/` | tijdelijk |
| `exec:` | `https://example.org/brdr/exec/` | tijdelijk |
| `ent:` | `https://example.org/brdr/ent/` | tijdelijk |
| `inst:` | `https://example.org/brdr/inst/` | tijdelijk |
| `prop:` | `https://example.org/brdr/prop/` | tijdelijk |
| `obj:` | `https://example.org/brdr/object/` | tijdelijk; in productie `https://id.erfgoed.net/aanduidingsobjecten/{id}` |
| `cl:` | `https://example.org/brdr/concept/` | tijdelijk |
| `sosa:` | `http://www.w3.org/ns/sosa/` | persistent |
| `prov:` | `http://www.w3.org/ns/prov#` | persistent |
| `p-plan:` | `http://purl.org/net/p-plan#` | persistent |
| `qudt:` | `http://qudt.org/schema/qudt/` | persistent |
| `unit:` | `http://qudt.org/vocab/unit/` | persistent |
| `geo:` | `http://www.opengis.net/ont/geosparql#` | persistent |
| `skos:` | `http://www.w3.org/2004/02/skos/core#` | persistent |
| `dct:` | `http://purl.org/dc/terms/` | persistent |
| `xsd:`, `rdf:`, `rdfs:` | W3C | persistent |

De bron gebruikte `https://id.erfgoed.net/metadata/` voor alles (activiteiten, procedures,
geometrieën) en `https://data.vlaanderen.be/id/geometry/capakey/…` voor perceelgeometrieën. De
herziening gebruikt `example.org` voor alles wat illustratief is (R10) en verwijst naar het perceel
met `rdfs:seeAlso` naar de CAPAKEY-API, die geen identificator maar een document is. Een
pijplijn moet de IRI's van kandidaten en waarnemingen afleiden uit een vaste sleutel, bv.
object + versie van de referentielaag + relevante afstand, en niet uit een UUID per run, zoals
brdr nu doet (`uuid.uuid4()` in `descriptor.py` en `metadata.py`) (R10, *Stable IRIs in pipelines*).
<!-- TODO: welke basis-IRI voor geometrieën en provenance in productie (id.erfgoed.net/…)? Is er een persistente IRI voor een perceel (OSLO Perceel)? -->

Blanco knopen enkel voor de resultaten van volledig bedekte percelen (100 %), waar niemand naar
verwijst; de resultaten van perceel 0734 hebben een IRI omdat de vergelijking ze gebruikt.

## 9. Inverse relaties

Geen. De provenance wordt van de nieuwe afbakening terug naar de oorzaak gevolgd
(`prov:wasRevisionOf`, `prov:wasDerivedFrom`, `sosa:hasResult`, `prov:wasGeneratedBy`), en die richting
staat in de data. `sosa:isResultOf`, `sosa:isFeatureOfInterestOf` of `sosa:hasMember` in de andere
richting zijn niet toegevoegd; een toepassing die vaak van een object naar zijn wijzigingen zoekt,
kan `sosa:isFeatureOfInterestOf` toevoegen.
