# Bespreking — overstortsensoren van Aquafin (herziene versie)

Deze bespreking beschrijft `overstort_herzien.ttl`. Wat er aan het origineel veranderde en waarom,
staat in `README.md`, sectie *Verbeterpunten*.

## 1. Wat stelt dit voorbeeld voor?

Aquafin beheert ongeveer 1600 overstortmeters in Vlaanderen. Een overstort voert bij hevige
neerslag overtollig rioolwater uit de gemengde riolering af naar het oppervlaktewater. De meters
registreren per meetpunt periodes ("events") waarin een overstort in werking was, niet in werking
was, of waarin de werking onbekend was (verstoord signaal). Aquafin publiceert twee LDES-stromen:
`overstort-sensor` (toestelmetadata) en `overstort-event-cleansed` (events); zie
<https://informatievlaanderen.github.io/OSLO-mapping/water/Aquafin%20-%20Overstort%20In%20Vlaanderen/0_2_data_input>.
Het voorbeeld zet één sensorrecord en één eventrecord uit de LDES-output om.

## 2. Kleurlegenda

| Kleur | SOSA-concept | Betekenis in het domein |
|---|---|---|
| Blauw (#60c4e4) | `sosa:Platform` / `sosa:Sensor` / `sosa:Deployment` / `geo:Geometry` | meetpunt, overstortmeter, inzet, ligging |
| Oranje-rood (#fe7130) | `sosa:Property` | werking van de overstort |
| Roze (#e54b89) | `sosa:Observation` | overstortevent |
| Oranje (#f8b622) | resultaat / `time:Interval` / `time:Instant` | overstortstatus, periode, begin en einde |

## 3. Infrastructuur (blauwe nodes)

- **`meetpunt:P_000000599187`** — `sosa:Platform` en `sosa:FeatureOfInterest`. Het P-nummer komt uit
  de Rioolinventaris en duidt het overstortpunt aan. Het is platform omdat het de meter herbergt
  (`sosa:hosts`), en studieobject omdat de werking van de overstort op die plaats het geobserveerde
  kenmerk is. Het heeft twee geometrieën: WGS84 (`POINT(lon lat)`, de standaard-CRS van
  GeoSPARQL) en Lambert 72 (WKT met CRS-IRI EPSG:31370), beide uit het sensorrecord.
- **`sensor:738d3a70cbc10bee4be120f70e377bc0`** — `sosa:Sensor` (en expliciet `sosa:System`, voor
  SHACL). De overstortmeter, merk Ijinus, status Actief. De IRI is afgeleid uit de MD5 van het
  toestelnummer, dezelfde waarde die de eventstroom in `is_observed_with` levert.
- **`inzet:738d3a…-P_000000599187`** — `sosa:Deployment`: de meter (`sosa:deployedSystem`) op het
  meetpunt (`sosa:deployedOnPlatform`), gericht op dat meetpunt (`sosa:hasFeatureOfInterest`).
- **`meetpunt:P_000000350733`** en **`sensor:4c314f066bea53f212495cb8c1eaca0b`** — meetpunt en meter
  van het event. De bron levert van het event een ander toestel en meetpunt dan van het
  sensorrecord; hun beschrijving zou in de sensorstroom staan. Ze zijn hier enkel getypeerd.

<!-- TODO: is het P-nummer (bv. P_000000599187) het overstortpunt zelf in de Rioolinventaris, of een meetlocatie ernaast? Heeft de Rioolinventaris een persistente IRI per punt waarnaar het meetpunt kan verwijzen? -->
<!-- TODO: zijn de coördinaten in het sensorrecord die van het toestel of die van het P-punt in de Rioolinventaris? -->

## 4. Observatie/Actuatie-structuur (roze nodes)

| IRI | observedProperty | usedProcedure | hasResult | hasFeatureOfInterest |
|---|---|---|---|---|
| `event:4004f4ea-117d-4e01-9b7d-6b6af865ad52` | `kenmerk:Overstort` | — (niet in de bron) | `overstortstatus:NietInWerking` | `meetpunt:P_000000350733` |

Het event heeft verder `sosa:madeBySensor sensor:4c314f…`, `sosa:phenomenonTime` (interval
20:45–20:46 UTC op 18 februari 2024) en `dct:modified`. Er is geen `sosa:ObservationCollection`:
het voorbeeld bevat één event; in de volledige stroom kan een collectie per meetpunt de gedeelde
metadata (sensor, meetpunt, property) dragen.

## 5. Procedure en Property

- **Procedure**: de bron noemt er geen. De events zijn berekend ("telkens een berekening […] van de
  start- en eindtijd") uit het signaal van de meter, maar de methode is niet beschreven. Daarom
  blijft de R2-waarschuwing (`sosa:usedProcedure` sterk aanbevolen) staan.
  <!-- TODO: welke procedure berekent start en einde van een overstortevent uit het signaal van de meter (drempel op waterhoogte, minimale duur)? Heeft Aquafin er een procedure-IRI voor, zoals observatieproceduretype/OW19 in het doelmodel voor de overstorthoogte? -->
- **`kenmerk:Overstort`** (`sosa:Property`): de werking van de overstort. De waarden komen uit de
  codelijst `https://aquafin.be/id/concept/OverstortStatus/`: `InWerking` (overstort vastgesteld),
  `NietInWerking` (geen overstort), `WerkingOnbekend` (verstoord signaal) en `InWerkingDroogWeer`
  (door de mapping weggefilterd). De meters observeren het kenmerk (`sosa:observes`); de meetpunten
  hebben het (`sosa:hasProperty`).

## 6. Modelleer-keuzes toegelicht

**Waarom de periode als `sosa:phenomenonTime` en niet als start- en eindtijd op de observatie?**
Verworpen alternatief: twee eigen properties `aquafin:event_start_time` en `aquafin:event_end_time`
rechtstreeks op de observatie, zoals in de bron, "om het eindgebruikers makkelijker te maken"
(issue #1). Gekozen aanpak: `sosa:phenomenonTime → time:Interval` met `time:hasBeginning` en
`time:hasEnd`. Motivatie: R12; de eigen properties bestaan in geen vocabularium, zodat geen
SOSA-client of -query ze vindt, en een interval kan met OWL-Time-relaties (`time:intervalOverlaps`,
…) vergeleken worden. De eenvoud voor eindgebruikers hoort in een view of een JSON-LD-frame, niet in
het model. Een alternatief met bestaande termen, `prov:startedAtTime` / `prov:endedAtTime` (een
`sosa:Observation` is een `prov:Activity`), is mogelijk, maar beschrijft de uitvoering van de
observatie, niet de periode van het fenomeen.

**Waarom een `sosa:Deployment` tussen sensor en meetpunt?**
Verworpen alternatief: `sosa:hasFeatureOfInterest` rechtstreeks op de sensor (bron). Gekozen
aanpak: `sosa:hosts` op het meetpunt en een `sosa:Deployment` met `sosa:hasFeatureOfInterest`.
Motivatie: in SOSA 2023 loopt `sosa:hasFeatureOfInterest` van een Execution of een Deployment naar
haar doelwit; op een sensor maakt ze er een `prov:Activity` van. De inzet drukt precies uit wat de
bron bedoelt: dit toestel staat hier om dit meetpunt te observeren. Een begin- of einddatum van de
inzet geeft de bron niet: `valid_from`/`valid_to` gaan over de geldigheid van het record.
<!-- TODO: kent Aquafin de plaatsings- en verwijderdatum van een meter op een meetpunt? Die horen op de sosa:Deployment. -->

**Waarom het meetpunt en geen `sosa:SpatialSample`?**
Verworpen alternatief: het meetpunt als `sosa:SpatialSample` van een groter object (het
rioleringsstelsel of de ontvangende waterloop), zoals de meetpunten in `verkeersmetingen/` en
`waterkwaliteit/` (R11). Gekozen aanpak: het meetpunt is zelf het studieobject. Motivatie: de vraag
gaat over de werking van dit ene kunstwerk, niet over een eigenschap van een groter gebied waarvan
het meetpunt een steekproef is. Wie de overstort ziet als lozing in een waterloop, kiest het patroon
*Emissie als studieobject* (`patterns.md`), zoals de lozingen in `waterkwaliteit/`: dan is een
overstorting een `prov:Entity` en het meetpunt de plaats (`prov:atLocation`).

**Alternatief: de overstorting als emissie.** Die lezing is uitgewerkt in
[`alternatief/`](alternatief/README.md) (status: voorstel). Daar is een overstorting een
`wk:Emissie` en het studieobject van haar observaties (status, overstortduur), het resultaat van een
`sosa:Actuation` op het meetpunt. Een event zonder overstorting houdt er het meetpunt als
studieobject. De argumenten voor en tegen en de discussievragen staan in
[`alternatief/bespreking.md`](alternatief/bespreking.md) §6.

**Waarom `sosa:hasResult` naar een concept?**
De status is een codelijstwaarde, geen getal met eenheid; `sosa:hasSimpleResult` vraagt een literal.
`sosa:hasResult` naar de concept-IRI houdt de verwijzing naar de codelijst. Na inferentie is het
concept ook een resultaat van de observatie (`sosa:isResultOf`), en kan het resultaat van veel
events zijn. Wie per event een eigen resultaatobject wil, gebruikt een `sosa:Result` met een
verwijzing naar het concept.
<!-- TODO: welke codelijst is de referentie voor de overstortstatus: https://aquafin.be/id/concept/OverstortStatus/ (de mapping) of https://data.vlaanderen.be/id/concept/OverstortStatus/ (het doelmodel voor de overstorthoogte)? Is een van beide gepubliceerd? -->
<!-- TODO: waarom filtert de mapping events met status InWerkingDroogWeer weg? Een overstorting bij droog weer is net een belangrijke afwijking. -->

**Waarom geen eenheden?** Geen numerieke resultaten; R3 is niet van toepassing.

**Toesteleigenschappen.** Fabrikant met `saref:hasManufacturer`, status met `adms:status` naar een
concept (`toestelstatus:Actief`, een voorstel naar Aquafins eigen IRI-patroon; een codelijst van
toestelstatussen bestaat nog niet), het toesteltype als `rdfs:comment` (`dct:type` vraagt een
klasse). Niet overgenomen: eigenaar, leverancier, gehasht serienummer en kwaliteitslabel.
<!-- TODO: wat betekent quality_label (A00, A01, E00)? Is het een kwaliteitskenmerk van het toestel of van zijn metingen? -->
<!-- TODO: moeten eigenaar (Aquafin) en leverancier (ELSCOLAB) als organisatie-IRI (bv. KBO) mee in de data? -->

**Gelaten waarschuwing.** R2: geen `sosa:usedProcedure`, omdat de bron geen procedure noemt (§5).

## 7. Tijdsmodellering

Patroon: `sosa:phenomenonTime → time:Interval → time:hasBeginning / time:hasEnd → time:Instant →
time:inXSDDateTimeStamp` (R12). Het interval is halfopen: begin inbegrepen, einde niet. De bron geeft
de tijdzone (`Z`, UTC); die blijft behouden, er is geen aanname nodig. In Brusselse tijd liep het
event van 21:45 tot 21:46 (`+01:00`, winter).

`sosa:resultTime` is niet ingevuld: `modified_at` is het tijdstip waarop het record laatst
gewijzigd of verstuurd werd, niet noodzakelijk het tijdstip waarop het resultaat beschikbaar kwam.
Het staat als `dct:modified` op de observatie en dient als `ldes:timestampPath` van de stroom.
<!-- TODO: is modified_at het tijdstip waarop het event berekend werd (dan ook sosa:resultTime), of het tijdstip van de laatste wijziging van het record? -->

## 8. Prefixen en IRI-structuur

| Prefix | Basis-IRI | Tijdelijk of persistent |
|---|---|---|
| `sosa:` | `http://www.w3.org/ns/sosa/` | persistent (W3C) |
| `time:` | `http://www.w3.org/2006/time#` | persistent (W3C) |
| `geo:` | `http://www.opengis.net/ont/geosparql#` | persistent (OGC) |
| `dct:` | `http://purl.org/dc/terms/` | persistent (DCMI) |
| `adms:` | `http://www.w3.org/ns/adms#` | persistent (W3C) |
| `saref:` | `https://saref.etsi.org/core/` | persistent (ETSI) |
| `xsd:`, `rdfs:` | W3C | persistent |
| `sensor:` | `https://aquafin.be/id/sensor/` | productie-IRI van Aquafin; `{MD5(toestelnummer)}` |
| `event:` | `https://aquafin.be/id/event/` | productie-IRI van Aquafin; nu een UUID per run |
| `meetpunt:` | `https://aquafin.be/id/meetpunt/` | productie-IRI van Aquafin; `{P-nummer}` |
| `inzet:` | `https://aquafin.be/id/inzet/` | voorstel; `{MD5(toestelnummer)}-{P-nummer}` |
| `kenmerk:` | `https://aquafin.be/id/concept/Kenmerk/` | concept-IRI van Aquafin |
| `overstortstatus:` | `https://aquafin.be/id/concept/OverstortStatus/` | concept-IRI van Aquafin |
| `toestelstatus:` | `https://aquafin.be/id/concept/Toestelstatus/` | voorstel naar hetzelfde patroon |

Het interval, de instants en de geometrieën hebben skolem-IRI's afgeleid van het event of het
meetpunt (`…-interval`, `…-begin`, `…-einde`, `…-geometrie-wgs84`): de data komen uit een
pijplijn met veel events (R10).

De event-IRI's komen uit `STRUUID()` en veranderen dus bij elke run. Een stabiele IRI vraagt een
deterministische sleutel, bv. MD5(toestel + meetpunt + starttijd); de herziening houdt de UUID
omdat de bron de nodige velden niet ongehasht levert.
<!-- TODO: blijft een event bij een herberekening (cleansed) dezelfde identiteit houden, of kan de starttijd verschuiven? Dat bepaalt of de starttijd in de sleutel mag. -->

## 9. Inverse relaties

Opgenomen voor kortere querypaden:

- `sosa:hosts` ↔ `sosa:isHostedBy` (meetpunt ↔ meter);
- `sosa:deployedSystem` ↔ `sosa:systemDeployment`, `sosa:deployedOnPlatform` ↔ `sosa:inDeployment`;
- `sosa:hasFeatureOfInterest` ↔ `sosa:isFeatureOfInterestOf` (inzet ↔ meetpunt, event ↔ meetpunt);
- `sosa:madeBySensor` ↔ `sosa:madeObservation`;
- `sosa:observes` ↔ `sosa:isObservedBy`, `sosa:hasProperty` ↔ `sosa:isPropertyOf`.

In de LDES-stromen zelf volstaat telkens één richting: het event verwijst naar sensor en meetpunt,
de sensor naar het meetpunt.
