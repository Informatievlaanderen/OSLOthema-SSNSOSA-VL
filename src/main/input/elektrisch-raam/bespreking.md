# Bespreking: elektrisch-raam

## 1. Wat stelt dit voorbeeld voor?

Dit voorbeeld modelleert een geautomatiseerd raambesturingssysteem voor zaal 01.16 (Rik Wouters)
in het Herman Teirlinck gebouw te Brussel. Het systeem leest continu vier omgevingssensoren
(binnentemperatuur, windsnelheid, lichtintensiteit, regen) en berekent op basis daarvan de
optimale raamstand. De elektrische raamopener (spindel- of kettingaandrijving) voert de berekende
stand uit. Het scenario illustreert hoe SSN/SOSA + p-plan een meerstaps besturingsproces
modelleert waarbij meetwaarden via een afgeleide observatie doorstromen naar een actuatie.

## 2. Kleurlegenda

| Kleur | SOSA-concept | Domeinbetekenis |
|---|---|---|
| Blauw (#60c4e4) | Platform / Sensor / Actuator | Gebouw, zaal, gevel en meetapparaten |
| Roze (#e54b89) | Observation / Actuation | Temperatuur-, wind-, licht- en regenmetingen; raamstandinstelling |
| Oranje (#f8b622) | Result / p-plan:Variable | Meetwaarden, afgeleide afwijking, raamstand-percentage |
| Paars (#7f59ae) | p-plan:Plan / p-plan:Step | Abstract raambesturingsplan en zijn stappen |

## 3. Infrastructuur (blauwe nodes)

| Node | SOSA-klasse(n) | Motivatie |
|---|---|---|
| `htg:gebouw-herman-teirlinck` | `sosa:Platform` | Het gebouw herbergt alle sub-platforms en sensoren. |
| `htg:zaal-0116` | `sosa:Platform`, `sosa:FeatureOfInterest` | De zaal is zowel infrastructuur (host voor thermometer en raamopener) als het ding waarvan de temperatuur gemeten wordt. Dubbele typering conform R1. |
| `htg:gevel` | `sosa:Platform` | De gevel herbergt de buitensensoren (wind, licht, regen). |
| `inst:thermometer-01` | `sosa:Sensor`, `sosa:System` | Meet binnentemperatuur; implementeert `step:temp-meting`. |
| `inst:windmeter-01` | `sosa:Sensor`, `sosa:System` | Meet windsnelheid; implementeert `step:wind-meting`. |
| `inst:lichtmeter-01` | `sosa:Sensor`, `sosa:System` | Meet lichtintensiteit; implementeert `step:licht-meting`. |
| `inst:regensensor-01` | `sosa:Sensor`, `sosa:System` | Detecteert neerslag; implementeert `step:regen-detectie`. |
| `inst:besturings-eenheid` | `sosa:Sensor`, `sosa:System` | Berekent de temperatuursafwijking (afgeleide observatie); implementeert `step:afwijking-berekening`. |
| `inst:raam-opener-01` | `sosa:Actuator`, `sosa:System` | Stuurt de elektrische raamopener aan; implementeert `step:raam-stand-bepaling`. |

`sosa:hosts`-hiërarchie:
- `htg:gebouw-herman-teirlinck` → `htg:zaal-0116`, `htg:gevel`
- `htg:zaal-0116` → `inst:thermometer-01`, `inst:raam-opener-01`
- `htg:gevel` → `inst:windmeter-01`, `inst:lichtmeter-01`, `inst:regensensor-01`

## 4. Observatie/Actuatie-structuur (roze nodes)

| IRI | observedProperty / actsOnProperty | usedProcedure | hasResult | hasFeatureOfInterest |
|---|---|---|---|---|
| `exec:temp-obs-20250427` | `prop:binnentemperatuur` | `step:temp-meting` | `ent:result-temp-20250427` (22.3 °C) | `htg:zaal-0116` |
| `exec:wind-obs-20250427` | `prop:windsnelheid` | `step:wind-meting` | `ent:result-wind-20250427` (3.5 m/s) | `htg:buitenomgeving` |
| `exec:licht-obs-20250427` | `prop:lichtintensiteit` | `step:licht-meting` | `ent:result-licht-20250427` (450 lux) | `htg:buitenomgeving` |
| `exec:regen-obs-20250427` | `prop:regen-aanwezigheid` | `step:regen-detectie` | `ent:result-regen-20250427` (false) | `htg:buitenomgeving` |
| `exec:afwijking-obs-20250427` | `prop:temp-afwijking` | `step:afwijking-berekening` | `ent:result-afwijking-20250427` (+2.3 °C) | `htg:zaal-0116` |
| `exec:raam-actuatie-20250427` | `prop:raam-stand` | `step:raam-stand-bepaling` | `ent:result-raam-stand-20250427` (45 %) | `htg:raam-zaal-0116` |

Alle zes uitvoeringen zijn verbonden met hun abstracte stap via `p-plan:correspondsToStep`.
Er is geen `sosa:ObservationCollection` gebruikt; de p-plan-laag legt de groepering al
structureel vast via het plan.

## 5. Procedure en ObservableProperty

Elke stap (`p-plan:Step`) is tegelijk getypeerd als `sosa:Procedure` (en specifieker als
`sosa:ObservingProcedure` of `sosa:ActuatingProcedure`) zodat `sosa:implements` geldig is.

| Stap / Procedure | Type | Sensor/Actuator | Observaties die de stap gebruiken |
|---|---|---|---|
| `step:temp-meting` | `sosa:ObservingProcedure` | `inst:thermometer-01` | `exec:temp-obs-20250427` |
| `step:wind-meting` | `sosa:ObservingProcedure` | `inst:windmeter-01` | `exec:wind-obs-20250427` |
| `step:licht-meting` | `sosa:ObservingProcedure` | `inst:lichtmeter-01` | `exec:licht-obs-20250427` |
| `step:regen-detectie` | `sosa:ObservingProcedure` | `inst:regensensor-01` | `exec:regen-obs-20250427` |
| `step:afwijking-berekening` | `sosa:ObservingProcedure` | `inst:besturings-eenheid` | `exec:afwijking-obs-20250427` |
| `step:raam-stand-bepaling` | `sosa:ActuatingProcedure` | `inst:raam-opener-01` | `exec:raam-actuatie-20250427` |

Observeerbare/actueerbare eigenschappen (`sosa:Property`):

| IRI | Betekenis |
|---|---|
| `prop:binnentemperatuur` | Luchttemperatuur in de zaal (°C) |
| `prop:windsnelheid` | Windsnelheid aan de buitengevel (m/s) |
| `prop:lichtintensiteit` | Zonlichtintensiteit (lux) |
| `prop:regen-aanwezigheid` | Boolean: is er neerslag? |
| `prop:temp-afwijking` | Berekende afwijking t.o.v. 20°C (positief = te warm) |
| `prop:raam-stand` | Actueerbare eigenschap: percentage raamopening |

## 6. Modelleer-keuzes toegelicht

### Waarom drielaags architectuur?

Verworpen alternatief: plat model met één `sosa:ObservationCollection`.
Gekozen aanpak: Planning / Deployment / Execution met p-plan.
Motivatie: het scenario heeft 5 procedures met expliciete gegevensstroom (output van stap 1
is input van stap 5a; output van stappen 1–4 zijn input van stap 5b). Dezelfde stappen
kunnen herbruikt worden op andere gebouwen of kamers. Traceerbaarheid naar het abstracte
besturingsplan is vereist. Dit voldoet aan de drie criteria van R4.

### Waarom `sosa:hasResult` (IRI-entiteiten) en niet `sosa:hasSimpleResult`?

Verworpen alternatief: `sosa:hasSimpleResult "22.3"^^xsd:decimal` op de observatie.
Gekozen aanpak: benoemde `qudt:QuantityValue, prov:Entity`-entiteiten met eigen IRI.
Motivatie: de resultaten moeten extern gerefereerd worden via `p-plan:correspondsToVariable`
en via `prov:used` vanuit de afgeleide observatie en de actuatie. Blank nodes of
`sosa:hasSimpleResult` laten geen externe referentie toe (R3).

### Waarom `inst:besturings-eenheid` als `sosa:Sensor`?

Verworpen alternatief: modelleren als `prov:SoftwareAgent` of `prov:Agent`.
Gekozen aanpak: `sosa:Sensor, sosa:System`.
Motivatie: de besturings-eenheid maakt een afgeleide observatie (`exec:afwijking-obs-20250427`)
op basis van berekening. In SSN/SOSA is elk systeem dat observaties produceert een `sosa:Sensor`,
ook als de waarde berekend is (R1). De `sosa:Sensor`-typering laat `sosa:madeBySensor` en
`sosa:implements` toe op correcte wijze.

### Waarom `prov:used` en niet `sosa:hasInput` voor de afgeleide observatie?

Verworpen alternatief: `sosa:hasInput ent:result-temp-20250427` op de observatie.
Gekozen aanpak: `prov:used ent:result-temp-20250427` op `exec:afwijking-obs-20250427`.
Motivatie: regel R5 verbiedt `sosa:hasInput` op execution-niveau. `sosa:hasInput` beschrijft
abstracte inputtypes op procedure-nodes. De concrete entiteits-referentie hoort op
`prov:used` (PROV-O spec).

### Waarom het regenresultaat als `prov:Entity, sosa:Result` zonder QUDT?

Verworpen alternatief: `sosa:hasSimpleResult false` op de observatie.
Gekozen aanpak: benoemd IRI-entiteit `ent:result-regen-20250427` met `rdf:value "false"^^xsd:boolean`.
Motivatie: ook het regenresultaat moet gerefereerd worden via `prov:used` door de actuatie
(`exec:raam-actuatie-20250427`). Een benoemd entiteit is daarvoor noodzakelijk. QUDT is
niet van toepassing op booleaanse waarden; `rdf:value` is hier de correcte modellering.

## 7. Tijdsmodellering

Patroon: `sosa:phenomenonTime → time:Instant → time:inXSDDateTimeStamp`.

Alle vier directe observaties delen hetzelfde `time:Instant` (`exec:instant-20250427T0900`),
want ze vinden alle op hetzelfde tijdstip plaats (09:00:00Z).

| Uitvoering | `sosa:resultTime` | `sosa:phenomenonTime` |
|---|---|---|
| `exec:temp-obs-20250427` | 09:00:00Z | `exec:instant-20250427T0900` |
| `exec:wind-obs-20250427` | 09:00:00Z | `exec:instant-20250427T0900` |
| `exec:licht-obs-20250427` | 09:00:00Z | `exec:instant-20250427T0900` |
| `exec:regen-obs-20250427` | 09:00:00Z | `exec:instant-20250427T0900` |
| `exec:afwijking-obs-20250427` | 09:00:05Z | — (resultaat beschikbaar 5 s na meting) |
| `exec:raam-actuatie-20250427` | 09:00:10Z | `exec:instant-20250427T0900` (moment van raambeweging) |

Onderscheid:
- `sosa:phenomenonTime` — wanneer het fenomeen of de actuatie fysiek plaatsvond
- `sosa:resultTime` — wanneer het resultaat (inclusief berekening) beschikbaar werd

## 8. Prefixen en IRI-structuur

| Prefix | Base URI | Tijdelijk of persistent |
|---|---|---|
| `plan:` | `https://example.org/elektrisch-raam/plan/` | Illustratief |
| `step:` | `https://example.org/elektrisch-raam/step/` | Illustratief |
| `var:` | `https://example.org/elektrisch-raam/var/` | Illustratief |
| `exec:` | `https://example.org/elektrisch-raam/exec/` | Illustratief |
| `ent:` | `https://example.org/elektrisch-raam/ent/` | Illustratief |
| `inst:` | `https://example.org/elektrisch-raam/inst/` | Illustratief |
| `htg:` | `https://example.org/herman-teirlinck/` | Illustratief (zou persistent kunnen zijn voor Herman Teirlinck-data) |
| `prop:` | `https://example.org/elektrisch-raam/prop/` | Illustratief |
| `sosa:` | `http://www.w3.org/ns/sosa/` | Persistent (W3C) |
| `prov:` | `http://www.w3.org/ns/prov#` | Persistent (W3C) |
| `p-plan:` | `http://purl.org/net/p-plan#` | Persistent (purl.org) |
| `time:` | `http://www.w3.org/2006/time#` | Persistent (W3C) |
| `qudt:` | `http://qudt.org/schema/qudt/` | Persistent (QUDT) |
| `unit:` | `http://qudt.org/vocab/unit/` | Persistent (QUDT) |

Geen blank nodes voor extern gerefereerde resources (R10). Het regenresultaat
(`ent:result-regen-20250427`) heeft een IRI ondanks de eenvoudige booleaanse waarde,
omdat het via `prov:used` gerefereerd moet worden.

## 9. Inverse relaties

| Inverse paar | Reden |
|---|---|
| `sosa:hosts` ↔ `sosa:isHostedBy` | Zowel top-down (platform naar sensor) als bottom-up (sensor naar platform) navigeerbaar |
| `sosa:hasFeatureOfInterest` ↔ `sosa:isFeatureOfInterestOf` | Vanuit een zaal of buitenomgeving direct de bijhorende observaties opvragen |

`sosa:hasProperty` ↔ `sosa:isPropertyOf` is niet expliciet opgenomen; eigenschappen zijn
vanuit de FeatureOfInterest-nodes te navigeren via `sosa:hasProperty`.
