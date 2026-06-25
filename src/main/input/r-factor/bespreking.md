# Bespreking: R-factor erosiviteitsmetingen

## 1. Wat stelt dit voorbeeld voor?

De R-factor (RUSLE Rainfall Erosivity Factor) is een maat voor de erosieve kracht van neerslag:
hoe intenser de regen, hoe hoger de R-factor en hoe meer bodemerosie er optreedt.
Dit voorbeeld modelleert de historische R-factormetingen van 53 neerslagstations in Vlaanderen,
beheerd door het KMI (10 stations, pluviografennetwerk) en VMM (43 stations, hydrologisch netwerk).
De meetreeksen bestrijken perioden van 4 tot 126 jaar (KMI-station Ukkel: 1898–2024).
De data zijn beschikbaar op drie temporele aggregatieniveaus: jaarlijks, maandelijks en
15-daags (24 perioden per jaar).

Bron: Vlaams Erosiemeetnet via KMI en VMM (geen publieke Linked Data-URI beschikbaar).

---

## 2. Kleurlegenda

| Kleur | SOSA-concept | Domeinbetekenis |
|---|---|---|
| Blauw (#60c4e4) | Platform / SpatialSample / FeatureOfInterest / Sensor | Neerslagmeetstation + -sensor |
| Oranje (#fe7130) | Property / ObservingProcedure | Erosiviteitseigenschap + meetprocedure |
| Roze (#e54b89) | ObservationCollection / Observation | Erosiviteitsmeting of -collectie |
| Geel (#f8b622) | qudt:QuantityValue / time:Interval | Meetresultaat en tijdsperiode |
| Goudgeel (#f8e1ad) | Afgeleide observatie | Berekend gemiddelde (R13) |

---

## 3. Infrastructuur (blauwe nodes)

### `ex:vlaanderen` — `sosa:FeatureOfInterest`
Het bredere studiegebied waarvan alle meetpunten ruimtelijke deelmonsters zijn.

### `ex:{station-id}` — `sosa:Platform + sosa:FeatureOfInterest + sosa:SpatialSample`
Elke van de 53 neerslagstations is drievoudig getypeerd (zie R1, R11):
- `sosa:Platform`: herbergt de neerslagsensor
- `sosa:FeatureOfInterest`: is zelf studieobject (erosiviteit op deze locatie)
- `sosa:SpatialSample`: ruimtelijk punt- of vlakmonster dat representatief is voor
  een groter Vlaams gebied (erosiviteitszone)

Geometrie: Lambert 72-coördinaten (`SRID=31370;POINT(x y)^^geo:wktLiteral`).
Koppeling: `sosa:isSampleOf ex:vlaanderen`.

### `ex:sensor-{station-id}` — `sosa:Sensor`
Één sensor per station (pluviograaf of hydrometrisch instrument). Elke sensor:
- `sosa:isHostedBy` → het bijbehorende Platform
- `sosa:implements` → `ex:procedure-rfactor-kmi` of `ex:procedure-rfactor-vmm`
- `sosa:observes` → `ex:property-erosiviteit`

Twee sensorfamilies (KMI vs VMM) reflect het feit dat de twee netwerken verschillende
instrumenttypes en kalibratiemethoden gebruiken.

---

## 4. Observatie/Actuatie-structuur (roze nodes)

### Observatiecollecties (drie niveaus)

| Collectie-IRI | Groepeert | Gedeelde metadata |
|---|---|---|
| `ex:collectie-{station}-jaarlijks` | alle jaarlijkse obs voor een station | sensor, procedure, FOI, property |
| `ex:collectie-{station}-{jaar}-maandelijks` | 12 maandelijkse obs per station-jaar | idem |
| `ex:collectie-{station}-{jaar}-15daags` | 24 15-daagse obs per station-jaar | idem |

### Individuele observaties

| Type | IRI-patroon | observedProperty | usedProcedure | hasResult | hasFeatureOfInterest |
|---|---|---|---|---|---|
| Jaarlijks | `ex:obs-{st}-{jaar}` | ex:property-erosiviteit | ex:procedure-rfactor-{kmi\|vmm} | qudt:QuantityValue (xsd:decimal) | ex:{station} |
| Maandelijks | `ex:obs-{st}-{jaar}-m{mm}` | idem | idem | idem | idem |
| 15-daags | `ex:obs-{st}-{jaar}-p{pp}` | idem | idem | idem | idem |
| Gemiddelde | `ex:obs-{st}-gemiddelde` | idem | idem | idem | idem |

Elke observatie draagt ook `sosa:madeBySensor` en `sosa:isMemberOf` voor de bijbehorende collectie.

---

## 5. Procedure en ObservableProperty

### Procedures

| IRI | Klasse | Geïmplementeerd door |
|---|---|---|
| `ex:procedure-rfactor-kmi` | `sosa:ObservingProcedure` | alle KMI-sensoren (10 stations) |
| `ex:procedure-rfactor-vmm` | `sosa:ObservingProcedure` | alle VMM-sensoren (43 stations) |

Beide procedures berekenen de RUSLE R-factor maar via verschillende meetinstrumenten:
KMI gebruikt klassieke pluviografen, VMM telemetrische hydrometrie.

### ObservableProperty

`ex:property-erosiviteit` — `sosa:Property`
De erosieve kracht van neerslag, uitgedrukt in MJ·mm/(ha·h·jaar).
Dit is de temporele R-factor zoals gedefinieerd in de RUSLE-methodiek
(Renard et al. 1997; Panagos et al. 2015 voor de Europese parameterisatie).

---

## 6. Modelleer-keuzes toegelicht

### Waarom één sensor per station in plaats van één per beheerder?

Verworpen alternatief: twee globale sensoren (`ex:sensor-kmi`, `ex:sensor-vmm`), elk gedeeld
door alle stations van die beheerder. Dit is semantisch onjuist: `sosa:isHostedBy` impliceert
een 1-op-1 fysieke host-relatie. Een sensor kan niet tegelijk door 10 verschillende platforms
worden geherbergd (één meetinstrument staat op één locatie). Gekozen aanpak: één sensor per
station. De twee procedures (`ex:procedure-rfactor-kmi` en `ex:procedure-rfactor-vmm`)
modelleren het verschil in meetmethode per beheerder.

### Waarom `sosa:ObservationCollection` per aggregatieniveau?

De drie temporele niveaus (jaarlijks, maandelijks, 15-daags) zijn onafhankelijke
aggregaties van hetzelfde onderliggende meetproces, niet hiërarchisch genest.
`sosa:hasMember` is gereserveerd voor observaties die tot dezelfde collectie behoren.
Een jaarlijkse collectie is de logische container voor alle jaarmetingen van één station;
maandelijkse en 15-daagse collecties zijn per station×jaar gegroepeerd omdat de jaargrens
de meest logische aggregatiegrens is. Gedeelde metadata (sensor, procedure, FOI, property)
staan op de collectie; individuele observaties erven via `sosa:isMemberOf` (R4).

### Waarom `time:Interval` en niet `time:Instant` voor alle niveaus?

De R-factor is altijd een aggregaat over een periode (R12). Een jaarlijkse waarde
beschrijft het erosiviteitsklimaat van een volledig jaar; een maandelijkse waarde beslaat
een kalendermaand; een 15-daagse waarde een vaste 15-daagse periode. Zelfs de jaarlijkse
meting is geen puntmeting maar een integraal over 365 dagen. `time:Instant` zou semantisch
onjuist zijn. Half-open intervallen conform CLAUDE.md-conventie: [begin, einde).

### Waarom `gemiddelde_waarde` als afgeleide observatie en `meest_recente_waarde` niet?

`view_rfactor.csv` bevat twee statistische samenvattingen per station:
- `meest_recente_waarde` = de waarde van het laatste jaar in `jaarlijkse_rfactor.csv`
  (geverifieerd: KMI_6408/2005 → 1102.318 ≈ 1102.32). Dit is geen nieuwe meting maar
  gewoon de laatste jaarlijkse observatie — die al aanwezig is in het model. Geen apart
  resource nodig.
- `gemiddelde_waarde` = gemiddelde over alle gevalideerde jaren. Dit is wél een nieuwe
  observatie die niet in `jaarlijkse_rfactor.csv` staat. Conform R13 wordt ze gemodelleerd
  als afgeleide observatie met `sosa:hasInputValue` → jaarlijkse collectie.
  Ze staat bewust NIET als `sosa:hasMember` in de jaarlijkse collectie (R13: afgeleide
  observaties zijn geen directe leden van de broncollectie).

### Waarom `sosa:SpatialSample` voor elk meetstation?

Een neerslagmeetstation is een puntlocatie die representatief is voor een ruimer
erosiviteitsgebied in de omgeving (analoog aan een grondwaterfilter dat representatief
is voor een hydrogeologische laag). De station-IRI is het directe `sosa:hasFeatureOfInterest`
van de observaties; via `sosa:isSampleOf ex:vlaanderen` is het overkoepelende studieobject
bereikbaar. Lambert 72-geometrie (`SRID=31370;POINT(...)^^geo:wktLiteral`) geeft de
exacte stationslocatie mee (R11).

### Waarom skolem-IRIs voor `time:Interval`, `time:Instant`, `qudt:QuantityValue` en `geo:Geometry`?

Verworpen alternatief: blank nodes voor de geneste structuren (zoals in andere eenvoudigere
voorbeelden). Bij een dataset met 34.000+ observaties zijn blank nodes onpraktisch: ze kunnen
niet van buiten gerefereerd worden, ze kunnen niet worden hergebruikt in joins over grafen,
en SPARQL property-path-queries op blank nodes zijn minder efficiënt. Gekozen aanpak: elke
geneste resource krijgt een deterministische IRI op basis van de bovenliggende observatie-ID
— bijv. `ex:interval-KMI-6408-jaar-2002`, `ex:instant-KMI-6408-jaar-2002-begin`,
`ex:result-KMI-6408-jaar-2002`. Geometrieën worden gedeeld per station: `ex:geom-KMI-6408`.
Het resultaat is een volledig blank-node-vrij graaf (R10: geen blank nodes voor extern
refereerbare resources).

### Waarom een lokale `ex:unit-rfactor` en geen standaard QUDT-eenheid?

De RUSLE R-factor eenheid MJ·mm/(ha·h·jaar) heeft geen equivalent in het QUDT-
eenheidenvocabulaire (`http://qudt.org/vocab/unit/`). Een lokale `qudt:Unit`-instantie
wordt gedefinieerd met `rdfs:label` en `rdfs:comment`. Dit is een pragmatische keuze;
een toepassingsprofiel kan later een eigen eenheden-namespace introduceren.

---

## 7. Tijdsmodellering

Alle observaties gebruiken `sosa:phenomenonTime → time:Interval` (R12) omdat de R-factor
altijd een aggregaat over een periode is:

| Aggregatieniveau | Patroon | Voorbeeld |
|---|---|---|
| Jaarlijks | `time:Interval` [1 jan, 1 jan volgend jaar) | 2002-01-01 – 2003-01-01 |
| Maandelijks | `time:Interval` [1e dag maand, 1e dag volgende maand) | 2002-08-01 – 2002-09-01 |
| 15-daags (oneven p) | `time:Interval` [dag 1, dag 16 van maand) | 2002-08-01 – 2002-08-16 |
| 15-daags (even p) | `time:Interval` [dag 16, 1e dag volgende maand) | 2002-08-16 – 2002-09-01 |
| Gemiddelde | `time:Interval` over de volledige meetperiode | 2002-01-01 – 2006-01-01 |

Periode-mapping: 24 perioden per jaar, 2 per kalendermaand. Periode 2k−1 = eerste helft
van maand k (dag 1–15); periode 2k = tweede helft van maand k (dag 16–einde). Berekend
in R via `lubridate::make_date()` en `%m+% months(1)`.

Elk `time:Interval` bevat:
- `time:hasBeginning → time:Instant → time:inXSDDate "YYYY-MM-DD"^^xsd:date`
- `time:hasEnd → time:Instant → time:inXSDDate "YYYY-MM-DD"^^xsd:date`

---

## 8. Prefixen en IRI-structuur

| Prefix | Base URI | Tijdelijk of persistent |
|---|---|---|
| `sosa:` | `http://www.w3.org/ns/sosa/` | Persistent (W3C-standaard) |
| `time:` | `http://www.w3.org/2006/time#` | Persistent (W3C-standaard) |
| `qudt:` | `http://qudt.org/schema/qudt/` | Persistent |
| `geo:` | `http://www.opengis.net/ont/geosparql#` | Persistent (OGC) |
| `rdfs:` | `http://www.w3.org/2000/01/rdf-schema#` | Persistent (W3C) |
| `xsd:` | `http://www.w3.org/2001/XMLSchema#` | Persistent (W3C) |
| `ex:` | `https://example.org/rfactor/` | Tijdelijk (illustratief) |

Regels:
- Stations: `ex:{KMI-6408}` (underscores → koppeltekens voor IRI-leesbaarheid)
- Sensoren: `ex:sensor-{station-id}`
- Collecties: `ex:collectie-{station-id}-jaarlijks`, `-{jaar}-maandelijks`, `-{jaar}-15daags`
- Observaties: `ex:obs-{station-id}-{jaar}`, `-{jaar}-m{mm}`, `-{jaar}-p{pp}`, `-gemiddelde`
- Geen blank nodes voor stations, sensoren of collecties (extern refereerbaar, R10)

---

## 9. Inverse relaties

| Directe relatie | Inverse relatie | Aanwezig |
|---|---|---|
| `sosa:hosts` (Platform → Sensor) | `sosa:isHostedBy` (Sensor → Platform) | Ja, op sensor |
| `sosa:implements` (Sensor → Procedure) | — | Niet nodig |
| `sosa:hasMember` (Collectie → Obs) | `sosa:isMemberOf` (Obs → Collectie) | Ja, op elke observatie |
| `sosa:hasFeatureOfInterest` (Obs → FOI) | `sosa:isFeatureOfInterestOf` (FOI → Obs) | Ja, Platform → jaarlijkse collectie |
| `sosa:isSampleOf` (Station → Vlaanderen) | — | Eenrichtings (geen inverse in SSN/SOSA 2023) |
