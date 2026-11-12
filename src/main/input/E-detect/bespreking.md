# Bespreking — E-Detect

## 1. Wat stelt dit voorbeeld voor?

Eén geurepisode in de industriële pilootzone van E-Detect (EFRO-project 2330, Provincie
West-Vlaanderen), op 5 november 2026 tussen 22:10 en 22:20. Er zijn drie bronnen van gegevens:

- een geursensor (e-nose) op meetpunt G01;
- een windmeter op weerstation W01;
- een omwonende die een geurmelding doet.

Het dataplatform leidt daaruit drie dingen af: een geschatte geurconcentratie in ouE/m³, een alarm,
en de waarschijnlijkheid dat bedrijf A de bron is. Alle data is fictief. De bron van het voorbeeld is
de checklist interoperabiliteit van het project, samengevat in de [README](README.md).

## 2. Kleurlegenda

| Kleur | SOSA-concept | Betekenis in het domein |
|---|---|---|
| Blauw (#60c4e4) | Platform / Sensor / FeatureOfInterest / Organization | meetpunt, weerstation, sensoren, melder, software, bedrijf, omgeving |
| Paars (#c6a0f5) | sosa:ObservingProcedure | meting, melding, kalibratie, drempel, bronanalyse |
| Oranje (#fe7130) | sosa:Property | sensorrespons, wind, kenmerken van een melding, geurconcentratie, alarm, waarschijnlijkheid |
| Roze (#e54b89) | Observation / ObservationCollection / prov:Activity | waarnemingen, collecties, productie |
| Geel (#f8b622) | qudt:QuantityValue / prov:Entity / skos:Concept | resultaten, de geuremissie |
| Lichtgeel (subgraph) | DERIVATION | afgeleide waarnemingen |

## 3. Infrastructuur (blauwe nodes)

- **`ex:meetpunt-G01`** is `sosa:Platform`, `sosa:FeatureOfInterest` en `sosa:SpatialSample`. Het is
  de paal waarop de e-nose staat (platform), de plaats waarvan de luchtsamenstelling bestudeerd
  wordt (studieobject), en een ruimtelijk monster van `ex:omgeving-industriezone` (R11). Het heeft
  een fictieve geometrie in Lambert 72.
- **`ex:geursensor-G01`** is een `sosa:Sensor` (e-nose). Ze meet een sensorrespons, geen
  geurconcentratie en geen geurbeleving. Dat onderscheid maakt de checklist zelf (vragen 12 en 15).
- **`ex:weerstation-W01`** is een `sosa:Platform` met **`ex:windsensor-W01`** erop. Het studieobject
  van de windmeting is de omgeving, niet het weerstation: de wind geldt voor de hele zone.
- **`ex:melder-M0042`** is een mens als sensor (R1, zoals de veldwaarnemer in `erosiepoel/`), en
  gepseudonimiseerd.
- **`ex:meldplaats-M0042`** is `sosa:FeatureOfInterest` en `sosa:SpatialSample` van de omgeving. Het is
  geen platform, want er staat niets. De geometrie is veralgemeend tot een vak van 100 m.
- **`ex:kalibratiemodel`** en **`ex:bronanalysemodel`** zijn software van het dataplatform, als
  `sosa:Sensor` van de afgeleide waarnemingen (zoals het conversiescript in `elf/`).
- **`ex:omgeving-industriezone`** is het gebied waarvan meetpunten en meldplaatsen monsters zijn
  (`sosa:hasSample`). Het staat onder invloed van de geuremissie (`prov:wasInfluencedBy`), zoals in
  `elf/`.
- **`ex:geuremissie-bedrijf-A`** is een `prov:Entity` en `sosa:FeatureOfInterest`, voortgebracht door
  `ex:productie-bedrijf-A` (een `prov:Activity` van `ex:bedrijf-A`, een `prov:Organization`). De
  emissie heeft de geometrie van de schouw.

Hiërarchie: `meetpunt-G01 sosa:hosts geursensor-G01`, `weerstation-W01 sosa:hosts windsensor-W01`.

## 4. Observatie/Actuatie-structuur (roze nodes)

| IRI | observedProperty | usedProcedure | resultaat | hasFeatureOfInterest |
|---|---|---|---|---|
| `ex:obs-G01-20261105T2214` (…`2215`, `2216`) | `ex:prop-sensorrespons` | `ex:procedure-enose` | `ex:result-G01-…` (0,41 · 0,58 · 0,52 `unit:UNITLESS`) | `ex:meetpunt-G01` |
| `ex:obs-W01-20261105T2210-richting` | `ex:prop-windrichting` | `ex:procedure-wind` | 247 `unit:DEG` | `ex:omgeving-industriezone` |
| `ex:obs-W01-20261105T2210-snelheid` | `ex:prop-windsnelheid` | `ex:procedure-wind` | 3,2 `unit:M-PER-SEC` | `ex:omgeving-industriezone` |
| `ex:obs-M0042-20261105-1-soort` | `ex:prop-geursoort` | `ex:procedure-geurmelding` (collectie) | `ex:geursoort-voeding` | `ex:meldplaats-M0042` |
| `ex:obs-M0042-20261105-1-intensiteit` | `ex:prop-geurintensiteit` | idem | `ex:geurintensiteit-4` | `ex:meldplaats-M0042` |
| `ex:obs-M0042-20261105-1-toon` | `ex:prop-hedonische-toon` | idem | `ex:hedonische-toon-min3` | `ex:meldplaats-M0042` |
| `ex:obs-G01-20261105T2214-geurconcentratie` | `ex:prop-geurconcentratie` | `ex:procedure-kalibratie` | 7,4 `eenheid:ouE-PER-M3` | `ex:meetpunt-G01` |
| `ex:obs-G01-20261105T2214-alarm` | `ex:prop-drempeloverschrijding` | `ex:procedure-drempel` | `true` (enkelvoudig) | `ex:meetpunt-G01` |
| `ex:obs-bedrijf-A-20261105T2210-bron` | `ex:prop-waarschijnlijkheid-bron` | `ex:procedure-bronanalyse` | 0,82 (enkelvoudig) | `ex:geuremissie-bedrijf-A` |

**Collecties.**
- `ex:collectie-G01-20261105T22`: sensor, procedure, eigenschap en studieobject van de minuutwaarden.
- `ex:collectie-W01-20261105T2210`: sensor, procedure, studieobject en de tijd van de twee
  windwaarnemingen.
- `ex:melding-M0042-20261105-1`: één melding met melder, procedure, meldplaats, het tijdstip van de
  waarneming en de resultaattijd. De leden erven die van de collectie (SOSA 2023, R2). Het
  studieobject staat er toch ook expliciet op, omdat de uit de OWL-restricties gegenereerde shape het
  per waarneming vereist.

De drie afgeleide waarnemingen zijn geen lid van een broncollectie (R13).

## 5. Procedure en Property

| Procedure | Geïmplementeerd door | Input → output |
|---|---|---|
| `ex:procedure-enose` | `ex:geursensor-G01` | → sensorrespons (minuutgemiddelde) |
| `ex:procedure-wind` | `ex:windsensor-W01` | → windrichting, windsnelheid (10-minutengemiddelde) |
| `ex:procedure-geurmelding` | `ex:melder-M0042` | → soort, intensiteit (VDI 3882-1), hedonische toon (VDI 3882-2) |
| `ex:procedure-kalibratie` | `ex:kalibratiemodel` | sensorrespons → geurconcentratie (gekalibreerd tegen olfactometrie, EN 13725:2022) |
| `ex:procedure-drempel` | `ex:kalibratiemodel` | geurconcentratie → overschrijding van 5 ouE/m³ (fictieve drempel) |
| `ex:procedure-bronanalyse` | `ex:bronanalysemodel` | geurconcentratie, wind, soort en intensiteit van de melding → waarschijnlijkheid per bron |

Eigenschappen:
- **sensorrespons**: een genormaliseerd signaal van de gassensoren, zonder fysische betekenis buiten
  de kalibratie;
- **geurconcentratie**: geurmengsel in ouE/m³, de verdunning tot de detectiedrempel van een panel
  (EN 13725:2022);
- **geurintensiteit en hedonische toon**: de beleving van een mens, op de schalen van VDI 3882;
- **waarschijnlijkheid als oorzaak**: 0 tot 1, een eigenschap van de emissie in een periode.

## 6. Modelleer-keuzes toegelicht

### Waarom een tijdelijke eenheid voor ouE/m³?

**Verworpen alternatieven:**
- `unit:NUM-PER-M3`, een aantal per kubieke meter, voor tellingen van deeltjes of organismen;
- `quantitykind:OlfactoryThreshold` met een massaconcentratie. Dat is de geurdrempel van één stof,
  geen concentratie van een mengsel.

**Gekozen aanpak:** `eenheid:ouE-PER-M3` in een eigen `example.org`-namespace, getypeerd als
`qudt:Unit` en `skos:Concept`, met de definitie uit EN 13725:2022.

**Rationale:** QUDT 3.5.2 en CSOR hebben geen eenheid voor de Europese geureenheid. Gezocht met
`search_terms` op `odour`, `odor`, `smell`, `olfact`, `ouE`, `dilution` en op de eenheden
`…PER-M3`. Een ouE/m³ is operationeel gedefinieerd: verdunning tot de detectiedrempel van een panel,
met 1 ouE ≙ 123 µg n-butanol als referentie. Die equivalentie geldt alleen voor n-butanol; een
`skos:exactMatch` naar een massa-eenheid zou dus fout zijn (R3).

Validatie: geen warning op de ontbrekende `qudt:hasQuantityKind` en `qudt:hasDimensionVector`,
dankzij de relaxatie `owl:minCardinality 0` op `qudt:Unit` uit de geladen ontologieën.

<!-- TODO: de eenheid aanvragen bij de beheerders van CSOR (beslisdocument C1); daarna de IRI vervangen. -->

### Waarom de ruwe e-nose-respons als eigen waarneming, en de geurconcentratie als afgeleide?

**Verworpen alternatief:** de e-nose rechtstreeks een geurconcentratie laten "meten".

**Gekozen aanpak:** de sensor meet een dimensieloze respons, en een kalibratiemodel leidt er de
geurconcentratie uit af (R7, R13): `sosa:hasInputValue` naar de drie resultaten,
`sosa:relatedObservation` naar de drie waarnemingen.

**Rationale:** een e-nose meet geen ouE/m³; de checklist zegt het zelf (vragen 12 en 15). Een
geschatte concentratie hangt af van een kalibratie, en het bestek vraagt die transparant te maken
(vraag 16). De respons heeft een resultaatobject (`unit:UNITLESS`) en geen
`sosa:hasSimpleResult`, omdat een afgeleide waarneming naar het resultaat moet kunnen verwijzen.

### Waarom de geuremissie als studieobject van de bronaanwijzing, en de plaats als studieobject van de metingen?

**Verworpen alternatieven:**
- het meetpunt als studieobject van de bronaanwijzing. De vraag "welke bron?" gaat over de bron,
  niet over de plaats;
- een immissie-entiteit (`prov:wasDerivedFrom` de emissie) als studieobject. Volgens het patroon is
  een immissie nooit het studieobject.

**Gekozen aanpak:** het patroon *Emissie en immissie*. Metingen en meldingen gaan over de plaats
(meetpunt, meldplaats). De bronaanwijzing gaat over de emissie.

**Rationale:** de vraag bepaalt het studieobject (`patterns.md`, *Emission and immission*, punt 1).

De immissie-entiteit is weggelaten. Ze is optioneel (punt 2) en voegt hier niets toe zolang er maar
één kandidaat-bron is. Bij meerdere bronnen, of om gemeten en berekende geur per bron te vergelijken,
krijgt ze wel een plaats.

### Waarom geen sosa:Stimulus?

**Verworpen alternatief:** de geurpiek als `sosa:Stimulus`, zoals een geluidsevent in
`geluidsmeetnet/`.

**Gekozen aanpak:** de e-nose meet continu, elke minuut. Geen gebeurtenis zet een meting in gang.

**Rationale:** patroon *Emissie en immissie*, punt 6. Een continue concentratie is geen stimulus.
Een geurmelding wordt wel door een voorval uitgelokt; als de werkgroep dat wil uitdrukken, is dat
een alternatieve lezing.

### Waarom een waarschijnlijkheid als eigenschap van de emissie?

**Gekozen aanpak:** `ex:prop-waarschijnlijkheid-bron`, een dimensieloos getal tussen 0 en 1, als
`sosa:hasSimpleResult`.

**Rationale:** dit is het einde van de keten; niets verwijst naar dit resultaat.

Een bronanalysemodel kan in de plaats daarvan een *bijdrage* aan de concentratie op het meetpunt
geven (in ouE/m³). Dat is dan een afgeleide waarneming van de plaats per bron (punt 4 van het
patroon). Welke uitvoer het platform geeft, beslist de leverancier.

<!-- TODO: geeft het bronanalysemodel van de leverancier een waarschijnlijkheid, een bijdrage of een rangorde van bronnen? -->

### Waarom een mens als sensor, en een veralgemeende meldplaats?

**Gekozen aanpak:** de melder is een `sosa:Sensor` (R1), gepseudonimiseerd. De meldplaats is een
vak van 100 m.

**Rationale:** een geurmelding is een menselijke waarneming. De locatie van een melding kan iemands
woning zijn, en dus persoonsgegevens (AVG, checklist vraag 27). Daarom wordt de geometrie
veralgemeend (R11).

<!-- TODO: welke veralgemening is nodig en volstaat (vak, buurt), en wie houdt de exacte locatie bij? -->

### Waarom eigen codelijsten voor de melding?

**Gekozen aanpak:** drie kleine SKOS-schema's onder `ex:`, met enkel de gebruikte waarden.

**Rationale:** er is geen register gevonden voor de schalen van VDI 3882 of voor soorten geur. De
data verwijst naar concepten en kopieert geen register.

<!-- TODO: bestaat er een Vlaams of Europees register voor geurintensiteit, hedonische toon of soorten geur (bv. bij VMM of in de geurnormering van VLAREM)? -->

### Waarom de alarmdrempel in de procedure?

**Gekozen aanpak:** het alarm is een afgeleide waarneming met een booleaans resultaat. De drempel
staat in de procedure, niet in de eigenschap.

**Rationale:** dezelfde eigenschap (overschrijding) kan met andere drempels berekend worden.
Wijzigt de drempel, dan krijgt het alarm een andere procedure.

### Woordenschat

Geen termen buiten de kern (SOSA, PROV-O, QUDT, OWL-Time, GeoSPARQL, SKOS, DCTERMS). R17 is niet van
toepassing.

### Meldingen van de validatie

Geen. `[VOCAB]`, `[DISJOINTNESS]` en `[SHACL]` zijn in orde; 30 van de 203 shapes zijn op de data
toegepast.

## 7. Tijdsmodellering

- **Minuutwaarden e-nose:** `sosa:phenomenonTime` → `time:Interval` van één minuut, half open
  (22:14–22:15 …). De respons is een gemiddelde over de minuut, dus geen `time:Instant` (R12).
- **Wind:** één interval van tien minuten op de collectie en op de waarnemingen.
- **Geschatte geurconcentratie en alarm:** het interval 22:14–22:17 van de drie inputwaarden.
- **Bronaanwijzing:** de episode 22:10–22:20.
- **Melding:** `sosa:phenomenonTime` is het tijdstip waarop de geur werd waargenomen (22:18, een
  `time:Instant`). `sosa:resultTime` is het moment waarop de melding werd verstuurd (22:19:37).

Tijdzone: `+01:00` (Europe/Brussels, wintertijd), want de data is fictief. Bij echte data: de
tijdzone van het platform overnemen, of `+01:00`/`+02:00` aannemen en dat hier vermelden.

## 8. Prefixen en IRI-structuur

| Prefix | Basis-IRI | Tijdelijk of persistent |
|---|---|---|
| `sosa:` | `http://www.w3.org/ns/sosa/` | persistent |
| `prov:` | `http://www.w3.org/ns/prov#` | persistent |
| `time:` | `http://www.w3.org/2006/time#` | persistent |
| `qudt:` | `http://qudt.org/schema/qudt/` | persistent |
| `unit:` | `http://qudt.org/vocab/unit/` | persistent |
| `geo:` | `http://www.opengis.net/ont/geosparql#` | persistent |
| `skos:` | `http://www.w3.org/2004/02/skos/core#` | persistent |
| `dcterms:` | `http://purl.org/dc/terms/` | persistent |
| `xsd:`, `rdfs:` | W3C | persistent |
| `ex:` | `https://example.org/e-detect/` | tijdelijk (fictieve data) |
| `eenheid:` | `https://example.org/e-detect/eenheid/` | tijdelijk, tot de eenheid in CSOR staat |

IRI's van resultaten, intervallen en geometrieën zijn skolem-IRI's, afgeleid van de waarneming of
het meetpunt (R10). Een echte pipeline leidt ze af van de sensor-ID van de leverancier en het
tijdstip, nooit van een willekeurige UUID.

## 9. Inverse relaties

- `sosa:hosts` ↔ `sosa:isHostedBy`: beide opgenomen voor de sensoren, zodat je zowel vanaf het
  platform als vanaf de sensor kan zoeken.
- `sosa:isSampleOf` ↔ `sosa:hasSample`: beide opgenomen, zodat de omgeving haar meetpunten en
  meldplaatsen kent.
- `sosa:hasFeatureOfInterest` ↔ `sosa:isFeatureOfInterestOf`: enkel de eerste. De inverse volgt bij
  het bevragen.
