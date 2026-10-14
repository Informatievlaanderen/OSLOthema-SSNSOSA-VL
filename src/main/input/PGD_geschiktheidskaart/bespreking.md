# Bespreking: PGD_geschiktheidskaart

## 1. Wat stelt dit voorbeeld voor?

De geschiktheidskaart voor peilgestuurde drainage (PGD) van het VLAIO-project OP-PEIL (BDB, versie
augustus 2024) schat per rastercel van 100 m x 100 m in hoe kansrijk peilgestuurde drainage is in
het Vlaams Gewest. Drie factoren, elk gescoord van 0 (slecht) tot 3 (goed), worden met een
beslissingsmodel gecombineerd tot vier klassen, van *weinig kansrijk* tot *zeer kansrijk*. De
factoren komen uit andere kaartlagen: de Bodemkaart van België (bodemtextuur, drainageklasse), de
hellingskaart uit het DHMV II en, in de polders, TOPSOIL-kaartlagen. Dataset en QGIS-modellen:
<https://doi.org/10.5281/zenodo.17803699>.

Anders dan de andere voorbeelden meet hier geen toestel iets: elke waarde is afgeleid uit
bestaande kaarten. Het voorbeeld toont dat zo'n afgeleide kaart in SSN/SOSA past, met de
QGIS-modellen als `sosa:Sensor` en elke celwaarde als `sosa:Observation`. Het volgt één
illustratieve cel in Binnen-Vlaanderen door de vier stappen.

## 2. Kleurlegenda

| Kleur | SOSA-concept | Domeinbetekenis |
|---|---|---|
| Blauw (#60c4e4) | Sensor / FeatureOfInterest / SpatialSample | QGIS-modellen, Vlaams Gewest, Binnen-Vlaanderen, rastercel |
| Roze (#e54b89) | Observation / Deployment | factorscores en kansrijkheid van de cel; uitvoering van het QGIS-model |
| Oranje (#f8b622) | Result / prov:Entity | inputwaarden en scores van de cel; kaartlagen en het outputraster |
| Paars (#7f59ae) | p-plan:Plan / p-plan:Step | de twee QGIS-modellen en hun stappen |
| Oranjerood (#fe7130) | sosa:Property / p-plan:Variable | beoordeelde eigenschappen en variabelen van het plan |

## 3. Infrastructuur (blauwe nodes)

| Node | SOSA-klasse(n) | Motivatie |
|---|---|---|
| `inst:qgis-model-pgd-binvla` | `sosa:Sensor`, `sosa:System` | Het QGIS-model `PGDv082024_binVla.model3` maakt de observaties voor Binnen-Vlaanderen. Software die observaties maakt is een `sosa:Sensor` (R1). Implementeert het plan en zijn vier stappen. |
| `inst:qgis-model-pgd-polders` | `sosa:Sensor`, `sosa:System` | Het QGIS-model voor de poldergebieden; enkel op planniveau uitgewerkt, zonder observaties. |
| `geb:vlaams-gewest` | `sosa:FeatureOfInterest` | Het uiteindelijke studieobject (`sosa:hasUltimateFeatureOfInterest`). |
| `geb:binnen-vlaanderen` | `sosa:SpatialSample`, `sosa:Sample`, `sosa:FeatureOfInterest` | De zone waarop het model voor Binnen-Vlaanderen loopt (`Zone_BinVlaanderen2.shp`): een ruimtelijk deel van het Gewest (R11). Feature of interest van de inzet. |
| `geb:cel-200000-210000` | `sosa:SpatialSample`, `sosa:Sample`, `sosa:FeatureOfInterest` | Eén rastercel van 100 m; de directe feature of interest van alle observaties. Draagt haar geometrie (polygoon in Lambert 72). |

Er is geen `sosa:Platform`: niets wordt fysiek opgesteld, en de cel *draagt* geen sensor. R11
noemt het meetpunt ook een platform omdat er doorgaans een toestel staat; voor een rastercel geldt
dat niet.

Bemonsteringsketen (R8): `geb:cel-200000-210000` `sosa:isSampleOf` `geb:binnen-vlaanderen`
`sosa:isSampleOf` `geb:vlaams-gewest`.

## 4. Observatie/Actuatie-structuur (roze nodes)

| IRI | observedProperty | usedProcedure | hasResult | hasFeatureOfInterest |
|---|---|---|---|---|
| `exec:obs-waterdoorlaatbaarheid-cel-200000-210000` | `prop:score-waterdoorlaatbaarheid` | `step:score-waterdoorlaatbaarheid-binvla` | `ent:score-waterdoorlaatbaarheid-…` (goed, 3) | `geb:cel-200000-210000` |
| `exec:obs-grondwateraanvoer-cel-200000-210000` | `prop:score-grondwateraanvoer` | `step:score-grondwateraanvoer-binvla` | `ent:score-grondwateraanvoer-…` (voldoende, 2) | `geb:cel-200000-210000` |
| `exec:obs-helling-cel-200000-210000` | `prop:score-helling` | `step:score-helling` | `ent:score-helling-…` (goed, 3) | `geb:cel-200000-210000` |
| `exec:obs-kansrijkheid-cel-200000-210000` | `prop:pgd-kansrijkheid` | `step:samengestelde-score` | `ent:kansrijkheid-…` (kansrijk, 3) | `geb:cel-200000-210000` |

De drie factorobservaties hebben als `sosa:hasInputValue` de waarde uit de kaartlaag voor de cel:
bodemtextuur `S` (lemig zand), drainageklasse `d` (matig nat) en helling 0,3 %. De
kansrijkheid is een afgeleide observatie (R7, R13): `sosa:hasInputValue` naar de drie
*resultaten*, `sosa:relatedObservation` naar de drie factorobservaties, en alle verplichte
eigenschappen expliciet. De regel die geldt: twee factoren goed en één voldoende geeft *kansrijk*.

Er is geen `sosa:ObservationCollection`: de observaties zijn allemaal afgeleid, en het plan
groepeert ze al via `p-plan:correspondsToStep`.

`exec:inzet-pgd-binvla-v082024` is een `sosa:Deployment` (een `prov:Activity`): de inzet van het
model op Binnen-Vlaanderen, met de gebruikte kaartlagen (`prov:used`) en het gegenereerde
raster (`prov:wasGeneratedBy`).

## 5. Procedure en Property

| Stap / Procedure | Plan(nen) | `sosa:hasInput` → `sosa:hasOutput` | Geïmplementeerd door | Gebruikt door |
|---|---|---|---|---|
| `step:score-waterdoorlaatbaarheid-binvla` | Binnen-Vlaanderen | `var:bodemtextuur` → `var:score-waterdoorlaatbaarheid` | `inst:qgis-model-pgd-binvla` | `exec:obs-waterdoorlaatbaarheid-…` |
| `step:score-grondwateraanvoer-binvla` | Binnen-Vlaanderen | `var:drainageklasse` → `var:score-grondwateraanvoer` | `inst:qgis-model-pgd-binvla` | `exec:obs-grondwateraanvoer-…` |
| `step:score-waterdoorlaatbaarheid-polders` | polders | `var:topsoil-2a1`, `var:topsoil-2b` → `var:score-waterdoorlaatbaarheid` | `inst:qgis-model-pgd-polders` | — |
| `step:score-grondwateraanvoer-polders` | polders | `var:topsoil-2d` → `var:score-grondwateraanvoer` | `inst:qgis-model-pgd-polders` | — |
| `step:score-helling` | beide | `var:helling` → `var:score-helling` | beide modellen | `exec:obs-helling-…` |
| `step:samengestelde-score` | beide | drie factorscores → `var:kansrijkheid` | beide modellen | `exec:obs-kansrijkheid-…` |

De beoordelingstabellen van de technische fiche staan als `rdfs:comment` bij elke stap. De twee
plannen zijn ook `sosa:ObservingProcedure`, omdat een `sosa:Sensor` enkel observatieprocedures
implementeert (gegenereerde shape uit de OWL-restrictie op `sosa:Sensor`).

| Property | Betekenis |
|---|---|
| `prop:score-waterdoorlaatbaarheid` | Hoe goed de bovenste bodemlagen water doorlaten; lichte textuur scoort beter. |
| `prop:score-grondwateraanvoer` | Natuurlijke aanvoer van grondwater (kwel); nattere gronden scoren beter. |
| `prop:score-helling` | Vlakheid van het terrein; met één regelput beheer je in vlak land een grotere oppervlakte. |
| `prop:pgd-kansrijkheid` | Samengestelde geschiktheid voor peilgestuurde drainage, in vier klassen. |

## 6. Modelleer-keuzes toegelicht

### Waarom een drielaags model?

Verworpen alternatief: een plat model met een `sosa:ObservationCollection` per cel.
Gekozen aanpak: Planning / Deployment / Execution met P-PLAN.
Motivatie: alle drie criteria van R4 gelden. Er zijn meerdere stappen (drie factoren, dan het
beslissingsmodel); twee QGIS-modellen delen de stappen voor helling en samengestelde score, maar
leiden de andere factoren uit andere kaartlagen af; en de herkomst van een celwaarde moet tot de
beoordelingsregel te herleiden zijn. De gedeelde variabelen (`var:score-…`) maken zichtbaar dat
de polders en Binnen-Vlaanderen op dezelfde schaal uitkomen, wat de samenvoeging tot één kaart
mogelijk maakt.

### Waarom een berekende score als `sosa:Observation`?

Verworpen alternatief: de scores enkel als `prov:Entity`, afgeleid (`prov:wasDerivedFrom`) uit
de kaartlagen, zonder SOSA.
Gekozen aanpak: elke celwaarde is een `sosa:Observation` van de cel, gemaakt door het QGIS-model.
Motivatie: SOSA 2023 laat een observatie toe die een waarde *schat* met een procedure, ook zonder
fysieke meting; een sensor kan software zijn (R1). Zo krijgt de kaartwaarde dezelfde structuur
(eigenschap, feature of interest, procedure, resultaat) als een gemeten waarde, en is ze met
andere observatiedata te bevragen. Hetzelfde patroon staat in `r-factor/` en `paleo/`.

### Waarom de rastercel als `sosa:SpatialSample`?

Verworpen alternatief: het Vlaams Gewest of Binnen-Vlaanderen als feature of interest van elke
observatie.
Gekozen aanpak: de rastercel is de directe feature of interest, een `sosa:SpatialSample` van
Binnen-Vlaanderen, dat zelf een ruimtelijk deel van het Gewest is (R11, patroon *Spatial
sample*).
Motivatie: de waarde geldt voor de cel, niet voor het gebied; SOSA gebruikt een SpatialSample
precies wanneer een eigenschap binnen een feature varieert. `sosa:hasUltimateFeatureOfInterest`
geeft een korte zoekweg naar het Gewest (R8).

### Waarom geen `sosa:Platform`?

Verworpen alternatief: de cel ook als `sosa:Platform` typeren, zoals R11 voor een meetpunt doet.
Gekozen aanpak: geen platform.
Motivatie: een platform herbergt een toestel; hier staat niets in het veld. Het QGIS-model wordt
niet *op* de cel opgesteld. De `sosa:Deployment` heeft daarom geen `sosa:deployedOnPlatform`.

### Waarom de kaartwaarden als inputwaarde en niet als observatie?

Verworpen alternatief: de bodemtextuur, drainageklasse en helling van de cel als eigen
observaties (de bodemkartering, de hellingsberekening uit het DTM), met de factorobservaties als
afgeleide observaties daarvan.
Gekozen aanpak: de celwaarden zijn `prov:Entity`'s, `prov:wasDerivedFrom` de kaartlaag, met
`p-plan:correspondsToVariable` naar de inputvariabele, en `sosa:hasInputValue` vanuit de
factorobservatie (R13).
Motivatie: het QGIS-model krijgt de kaartlagen als input; hoe die tot stand kwamen (kartering
1947-1974, DHMV II) valt buiten het proces van de fiche. Wie die herkomst wil, kan de
`prov:Entity` later als resultaat van een observatie beschrijven, zonder iets aan dit voorbeeld te
veranderen.
<!-- TODO: bestaan er IRI's voor de bodemtextuur- en drainageklassen van de Bodemkaart (DOV-codelijsten), zodat rdf:value "S" en "d" door een concept-IRI vervangen kunnen worden? -->

### Waarom twee kleine SKOS-codelijsten voor de scores en de kansrijkheid?

Verworpen alternatief: `sosa:hasSimpleResult 3` (een geheel getal) per observatie.
Gekozen aanpak: het resultaat is een `prov:Entity` per cel met `rdf:value` naar een concept uit
`cl:factorscore` (goed, voldoende, matig, slecht) of `cl:kansrijkheid` (zeer kansrijk tot weinig
kansrijk), met de score als `skos:notation`.
Motivatie: de scores zijn ordinaal, geen hoeveelheden met een eenheid; de fiche geeft ze een
naam, en het beslissingsmodel redeneert in die namen. Het resultaat moet een eigen IRI hebben,
omdat de samengestelde score ernaar verwijst met `sosa:hasInputValue`. Het concept zelf is geen
resultaat: `sosa:hasResult` is een subproperty van `prov:generated`, en een gedeeld concept zou
door elke cel "gegenereerd" worden (R16). Geen bestaand register dekt deze klassen; ze staan
daarom in het voorbeeld zelf, onder `https://example.org/`.
<!-- TODO: beheert BDB of OP-PEIL een vaste legende (PGDv082024_style.qml) die als codelijst gepubliceerd kan worden? -->

### Waarom de helling als `qudt:QuantityValue` met QUDT-eenheid?

De helling is de enige echte hoeveelheid in het voorbeeld: 0,3 %, `qudt:numericValue` met
`qudt:hasUnit unit:PERCENT` (R3, QUDT als bron van eenheden). De fiche drukt de helling uit in
procent (hoogteverschil per horizontale afstand), niet in graden.

### Waarom de inzet en het outputraster als PROV?

Verworpen alternatief: enkel de observaties, zonder dataset.
Gekozen aanpak: `exec:inzet-pgd-binvla-v082024` (`sosa:Deployment`) gebruikt de kaartlagen en
genereert `ent:pgd-stack-binvla-v082024`; elk celresultaat is `dct:isPartOf` dat raster (band 1
tot 4), dat zelf deel is van de Zenodo-dataset.
Motivatie: wie de kaart gebruikt, werkt met het raster, niet met losse observaties. De koppeling
maakt de weg van celwaarde naar gepubliceerd bestand en DOI expliciet. `dct:isPartOf` (DCTERMS,
kern volgens R17) heeft geen domein dat met `prov:Entity` botst.

### Wat valt buiten dit voorbeeld?

- De poldergebieden zijn enkel op planniveau uitgewerkt; een cel in de polders volgt hetzelfde
  patroon met de TOPSOIL-waarden als inputwaarde.
- De samenvoeging van beide rasters tot `PGDv082024_stack.tif` voor het hele Gewest is niet
  gemodelleerd; ze verandert geen celwaarde.
- Gebieden met antropogene bodems vallen buiten de kaart; daar is geen observatie.
- De cel is illustratief: haar ligging en waarden zijn niet uit het raster gelezen.
<!-- TODO: welke echte cel (coördinaten in Lambert 72) uit PGDv082024_stack_binVla.tif kan het voorbeeld vervangen, met haar vier bandwaarden? -->

### Bewust behouden SHACL-warning

`R11: give a sosa:SpatialSample a geometry` voor `geb:binnen-vlaanderen`: de zone is afgebakend
door `Zone_BinVlaanderen2.shp` in de Zenodo-dataset; de polygoon wordt niet in het voorbeeld
overgenomen. De rastercel heeft wel een geometrie.

### Alternatieve lezing

Een geschiktheidskaart kan ook gelezen worden als een *beoordeling* van een gebied tegen criteria
(een conformiteits- of geschiktheidsbeoordeling) eerder dan als een observatie. Dat sluit aan bij
de latere fase van `waterkwaliteit/` (normen en beoordelingen). Dit voorbeeld kiest de
observatielezing omdat elke stap een eigenschap van de cel schat; een alternatieve mapping kan de
andere lezing uitwerken.

## 7. Tijdsmodellering

De observaties hebben geen `sosa:phenomenonTime` en geen `sosa:resultTime`. De bron geeft geen
datum per waarde, alleen de versie van de kaart: augustus 2024, op het outputraster als
`dct:issued "2024-08"^^xsd:gYearMonth`. Een `sosa:resultTime` vraagt een volledige
`xsd:dateTime`, die de bron niet geeft; er is daarom geen tijdzone-aanname nodig.

De kaart beschrijft een toestand die als stabiel wordt beschouwd. De inputlagen hebben elk hun
eigen referentieperiode: de Bodemkaart (kartering 1947-1974, digitale versie 2017, aangepaste
attributentabel april 2024) en het DHMV II (2014).
<!-- TODO: geldt de kaart voor een bepaalde periode (phenomenonTime), bv. die van het DHMV II, of is ze tijdloos tot een nieuwe versie verschijnt? -->

## 8. Prefixen en IRI-structuur

| Prefix | Base IRI | Tijdelijk of persistent |
|---|---|---|
| `plan:` | `https://example.org/pgd-geschiktheidskaart/plan/` | Illustratief |
| `step:` | `https://example.org/pgd-geschiktheidskaart/step/` | Illustratief |
| `var:` | `https://example.org/pgd-geschiktheidskaart/var/` | Illustratief |
| `exec:` | `https://example.org/pgd-geschiktheidskaart/exec/` | Illustratief |
| `ent:` | `https://example.org/pgd-geschiktheidskaart/ent/` | Illustratief |
| `inst:` | `https://example.org/pgd-geschiktheidskaart/inst/` | Illustratief |
| `prop:` | `https://example.org/pgd-geschiktheidskaart/prop/` | Illustratief |
| `geb:` | `https://example.org/pgd-geschiktheidskaart/gebied/` | Illustratief |
| `cl:` | `https://example.org/pgd-geschiktheidskaart/concept/` | Illustratief |
| `sosa:` | `http://www.w3.org/ns/sosa/` | Persistent (W3C) |
| `prov:` | `http://www.w3.org/ns/prov#` | Persistent (W3C) |
| `p-plan:` | `http://purl.org/net/p-plan#` | Persistent (purl.org) |
| `qudt:` | `http://qudt.org/schema/qudt/` | Persistent (QUDT) |
| `unit:` | `http://qudt.org/vocab/unit/` | Persistent (QUDT) |
| `geo:` | `http://www.opengis.net/ont/geosparql#` | Persistent (OGC) |
| `skos:` | `http://www.w3.org/2004/02/skos/core#` | Persistent (W3C) |
| `dct:` | `http://purl.org/dc/terms/` | Persistent (DCMI) |

De Zenodo-dataset krijgt geen eigen IRI: het voorbeeld hergebruikt de DOI,
`https://doi.org/10.5281/zenodo.17803699`. De rastercel heet naar haar linkeronderhoek in Lambert
72 (`cel-{X}-{Y}`); bij een volledige omzetting van het raster levert dat deterministische IRI's
op (R10), net als de afgeleide IRI's van de inputwaarden en resultaten (`ent:score-…-cel-{X}-{Y}`).
Geen blank nodes: elke waarde wordt van elders gerefereerd.
<!-- TODO: welke persistente basis-IRI (BDB, OP-PEIL, DOV, Waterradar) is bevoegd voor de cellen en resultaten van de kaart? -->

## 9. Inverse relaties

| Inverse paar | Reden |
|---|---|
| `sosa:hasFeatureOfInterest` ↔ `sosa:isFeatureOfInterestOf` | Vanuit de cel meteen haar vier observaties opvragen. |
| `sosa:hasResult` ↔ `sosa:isResultOf` | Vanuit een score de observatie terugvinden, bv. bij een bevraging van het raster. |
| `sosa:isSampleOf` ↔ `sosa:hasSample` | Vanuit het Gewest en Binnen-Vlaanderen naar de onderliggende zones en cellen navigeren. |

`sosa:implements` ↔ `sosa:implementedBy` en `sosa:hasProperty` ↔ `sosa:isPropertyOf` zijn niet
expliciet opgenomen; de richting vanuit sensor en cel volstaat.
