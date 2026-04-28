# Bespreking — Erosiepoel (modellering)

## 1. Wat stelt dit voorbeeld voor?

Een veldwaarnemer (Waarnemer X) voert 's ochtends een controle uit op een erosiepoel
beheerd door Stad Mechelen. Na een nachtelijke regenbui schat hij het volume neergeslagen
sediment op 245.000 liter — bijna de volledige capaciteit van 250.000 liter. De meting
ondersteunt besluitvorming over ruimingsbeheer om bodemerosie te beperken.

## 2. Kleurlegenda

| Kleur | SOSA-concept | Domeinbetekenis |
|---|---|---|
| Blauw (#60c4e4) | Platform / FeatureOfInterest | Erosiepoel (locatie én onderwerp) en veldwaarnemer |
| Paars (#c6a0f5) | sosa:ObservingProcedure | Visuele veldmeetprocedure |
| Oranje (#fe7130) | sosa:Property | Sedimentvolume |
| Roze (#e54b89) | ObservationCollection / Observation | Ochtendcontrole en de concrete volumemeting |
| Geel (#f8b622) | qudt:QuantityValue / time:Instant | Meetresultaat (245.000 L) en tijdstip |

## 3. Infrastructuur (blauwe nodes)

**`ex:Erosiepoel_Mechelen`** — `sosa:Platform + sosa:FeatureOfInterest`

De erosiepoel heeft een dubbele typering:
- Als `sosa:Platform` herbergt ze de veldwaarnemer via `sosa:hosts`. Zonder deze rol is
  de `sosa:hosts`-relatie niet valide en ontbreekt de infrastructuurlaag volledig.
- Als `sosa:FeatureOfInterest` is de erosiepoel het bestudeerde object: het sedimentvolume
  wordt aan en in de poel bepaald. De poel is dus tegelijk locatie en fenomeen.

Deze dubbele typering is een standaardpatroon voor monitoringinfrastructuur die ook het
te bestuderen fenomeen draagt (zie ook grondwaterpeilmetingen-voorbeeld).

`sosa:hosts` ↔ `sosa:isHostedBy` verbindt Platform en Sensor.

**`ex:Waarnemer_X`** — `sosa:Sensor`

Een menselijke veldwaarnemer. De SSN/SOSA-definitie van `sosa:Sensor` omvat uitdrukkelijk
personen: "een agent (persoon, apparaat of software) die observaties maakt". `prov:Agent`
(het origineel) is te generiek en mist de observatiecapaciteit die `ssn:implements` vereist.

## 4. Observatie/Actuatie-structuur (roze nodes)

`sosa:ObservationCollection` groepeert de ochtendcontrole. Gedeelde metadata staat op
collection-niveau en wordt niet herhaald op de individuele observatie.

| IRI | observedProperty | usedProcedure | hasResult | hasFeatureOfInterest |
|---|---|---|---|---|
| `ex:Obs_SedimentVolume_EM_20240901` | `ex:SedimentVolume` | `ex:VeldmeetProcedure` (via collection) | `ex:Result_SedimentVolume_EM_20240901` (245.000 L) | `ex:Erosiepoel_Mechelen` |

De `sosa:ObservationCollection` `ex:ObsCollection_EM_20240901` heeft als gedeelde metadata:
`sosa:hasFeatureOfInterest`, `sosa:madeBySensor`, `sosa:usedProcedure`, `sosa:phenomenonTime`,
`sosa:resultTime`. Bij uitbreiding naar meerdere metingen per bezoek (bijv. ook troebelheid
of waterstand) hoeven deze properties enkel op de collection te staan.

## 5. Procedure en ObservableProperty

**`ex:VeldmeetProcedure`** — `sosa:ObservingProcedure`

- Geïmplementeerd door `ex:Waarnemer_X` via `sosa:implements`.
- Gebruikt door `ex:ObsCollection_EM_20240901` via `sosa:usedProcedure`.
- Beschrijft een manuele visuele schatting ter plaatse na een neerslagepisode.

**`ex:SedimentVolume`** — `sosa:Property`

Fysieke betekenis: het volume neergeslagen erosiemateriaal (slib, modder) in de
retentiepoel, uitgedrukt in liter. Dit is een directe indicator voor de vullingsgraad
en daarmee voor de urgentie van een ruimingsoperatie.

## 6. Modelleer-keuzes toegelicht

### Waarom `sosa:Platform + sosa:FeatureOfInterest` dubbele typering?

Verworpen alternatief: erosiepoel enkel als `sosa:FeatureOfInterest`, waarnemer als
los element zonder infrastructuurkoppeling. Gekozen aanpak: dubbele typering zodat
`sosa:hosts` / `sosa:isHostedBy` geldig is. Motivatie: de erosiepoel is de fysieke
locatie van de meting én het bestudeerde object; SSN/SOSA 2023 voorziet expliciet in
deze combinatie voor meetinfrastructuur die het fenomeen draagt.

### Waarom `sosa:ObservationCollection` i.p.v. losse observaties?

Verworpen alternatief: één losstaande `sosa:Observation` zonder collection (originele aanpak).
Gekozen aanpak: `sosa:ObservationCollection` met gedeelde metadata. Motivatie: sensor,
procedure en tijdstip zijn identiek voor alle metingen van een veldbezoek. Door ze op
collection-niveau te plaatsen vermijdt men redundantie en maakt men de collectieve context
explicieter. Tevens vergemakkelijkt dit uitbreiding naar extra observabele eigenschappen
(troebelheid, waterstand) zonder refactoring van bestaande tripels.

### Waarom `sosa:hasResult` met `qudt:QuantityValue` i.p.v. `sosa:hasSimpleResult`?

Verworpen alternatief: `sosa:hasSimpleResult "245000"^^xsd:decimal` (originele aanpak) —
eenheid ontbreekt, getal is ambigu (liter? m³? mm?). Gekozen aanpak: `sosa:hasResult`
verwijzend naar `ex:Result_SedimentVolume_EM_20240901` met `qudt:hasUnit unit:L`. Motivatie:
Het object-resultaat-patroon is vereist wanneer een eenheid, onzekerheid of provenance nodig is;
het resultaat heeft een persistente IRI en kan extern gerefereerd worden.

### Waarom `sosa:Sensor` voor een menselijke waarnemer?

Verworpen alternatief: `prov:Agent` (originele aanpak). Gekozen aanpak: `sosa:Sensor`.
Motivatie: SSN/SOSA definieert `sosa:Sensor` als "een agent die observaties maakt via
een procedure"; dit omvat personen. `prov:Agent` mist `ssn:implements` en legt de
observatierelatie niet formeel vast.

## 7. Tijdsmodellering

Gebruikt patroon: `sosa:phenomenonTime → time:Instant → time:inXSDDateTime`

De ochtendcontrole heeft een concreet uurstijdstip (09:00). `time:inXSDDateTime` is
gekozen boven `time:inXSDDate` omdat het tijdstip van de dag relevant is: de observatie
vindt 's ochtends plaats, direct na een nachtelijke regenbui, en het uur kan diagnostisch
zijn bij vergelijking met regenmeetdata.

| Property | Waarde | Betekenis |
|---|---|---|
| `sosa:phenomenonTime` | `ex:Instant_20240901_09u` | Moment van de observatie ter plaatse |
| `sosa:resultTime` | `"2024-09-01T09:00:00"^^xsd:dateTime` | Moment waarop het resultaat beschikbaar werd (hier gelijk aan phenomenonTime) |

## 8. Prefixen en IRI-structuur

| Prefix | Base URI | Tijdelijk of persistent |
|---|---|---|
| `sosa:` | `http://www.w3.org/ns/sosa/` | Persistent |
| `ssn:` | `http://www.w3.org/ns/ssn/` | Persistent |
| `time:` | `http://www.w3.org/2006/time#` | Persistent |
| `qudt:` | `http://qudt.org/schema/qudt/` | Persistent |
| `unit:` | `http://qudt.org/vocab/unit/` | Persistent |
| `xsd:` | `http://www.w3.org/2001/XMLSchema#` | Persistent |
| `rdf:` | `http://www.w3.org/1999/02/22-rdf-syntax-ns#` | Persistent |
| `rdfs:` | `http://www.w3.org/2000/01/rdf-schema#` | Persistent |
| `ex:` | `https://example.org/erosiepoel/` | Tijdelijk (illustratief) |

In productie zou `ex:` vervangen worden door een gezaghebbende URI van Stad Mechelen
of het Departement Omgeving (bijv. `https://data.mechelen.be/erosiepoel/`).

## 9. Inverse relaties

Volgende inverse paren zijn opgenomen voor query-efficiëntie:

| Richting | Property | Inverse |
|---|---|---|
| Platform → Sensor | `sosa:hosts` | `sosa:isHostedBy` |
| Observation/Collection → FOI | `sosa:hasFeatureOfInterest` | `sosa:isFeatureOfInterestOf` |

`ex:Erosiepoel_Mechelen sosa:isFeatureOfInterestOf ex:ObsCollection_EM_20240901` is
expliciet opgenomen zodat SPARQL-queries die starten vanuit de erosiepoel direct naar
alle gerelateerde observatiecollecties navigeren zonder reverse-path (`^`).

`ex:Waarnemer_X sosa:isHostedBy ex:Erosiepoel_Mechelen` legt de hosting-relatie vast
vanuit het perspectief van de sensor.
