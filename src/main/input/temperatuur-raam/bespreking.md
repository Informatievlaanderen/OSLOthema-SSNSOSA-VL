# Bespreking: temperatuur-raam

## 1. Wat stelt dit voorbeeld voor?

Dit voorbeeld modelleert een minimale temperatuurgestuurde raambesturing voor zaal 01.16
(Rik Wouters) in het Herman Teirlinck gebouw te Brussel. Een enkele thermometer meet de
binnentemperatuur. Op basis van twee drempelwaarden beslist de elektrische raamopener
automatisch: boven 20 °C gaat het raam open, onder 18 °C gaat het raam dicht (hysterese).
Het voorbeeld is een vereenvoudigde variant van `elektrisch-raam` en dient als
instapscenario voor het drielaags SSN/SOSA + p-plan-model met één sensor en één actuator.

## 2. Kleurlegenda

| Kleur | SOSA-concept | Domeinbetekenis |
|---|---|---|
| Blauw (#60c4e4) | Platform / Sensor / Actuator | Gebouw, zaal, thermometer en raamopener |
| Roze (#e54b89) | Observation / Actuation | Temperatuurmeting en raamstandinstelling |
| Oranje (#f8b622) | Result / p-plan:Variable | Gemeten temperatuur en raamstand-percentage |
| Paars (#7f59ae) | p-plan:Plan / p-plan:Step | Abstract raambesturingsplan en zijn twee stappen |

## 3. Infrastructuur (blauwe nodes)

| Node | SOSA-klasse(n) | Motivatie |
|---|---|---|
| `htg:gebouw-herman-teirlinck` | `sosa:Platform` | Het gebouw herbergt de zaal en alle apparatuur. |
| `htg:zaal-0116` | `sosa:Platform`, `sosa:FeatureOfInterest` | De zaal is infrastructuur (host voor thermometer en raamopener) én het ding waarvan de temperatuur gemeten wordt. Dubbele typering conform R1. |
| `inst:thermometer-01` | `sosa:Sensor`, `sosa:System` | Meet de binnentemperatuur; implementeert `step:temp-meting`. |
| `inst:raam-opener-01` | `sosa:Actuator`, `sosa:System` | Stuurt de elektrische raamopener aan op basis van de drempellogica; implementeert `step:raam-actuatie`. |

`sosa:hosts`-hiërarchie:
- `htg:gebouw-herman-teirlinck` → `htg:zaal-0116`
- `htg:zaal-0116` → `inst:thermometer-01`, `inst:raam-opener-01`

`htg:raam-zaal-0116` is een `sosa:FeatureOfInterest` zonder Platform-rol: het raam is
het ding dat geactueerd wordt, maar herbergt zelf geen sensoren.

## 4. Observatie/Actuatie-structuur (roze nodes)

| IRI | observedProperty / actsOnProperty | usedProcedure | hasResult | hasFeatureOfInterest |
|---|---|---|---|---|
| `exec:temp-obs-20250427` | `prop:binnentemperatuur` | `step:temp-meting` | `ent:result-temp-20250427` (22.3 °C) | `htg:zaal-0116` |
| `exec:raam-actuatie-20250427` | `prop:raam-stand` | `step:raam-actuatie` | `ent:result-raam-stand-20250427` (100 %) | `htg:raam-zaal-0116` |
| `exec:temp-obs-20250427T1000` | `prop:binnentemperatuur` | `step:temp-meting` | `ent:result-temp-20250427T1000` (17.5 °C) | `htg:zaal-0116` |
| `exec:raam-actuatie-20250427T1005` | `prop:raam-stand` | `step:raam-actuatie` | `ent:result-raam-stand-20250427T1005` (0 %) | `htg:raam-zaal-0116` |

Alle vier uitvoeringen zijn verbonden met hun abstracte stap via `p-plan:correspondsToStep`.
Elke actuatie verwijst via `prov:used` naar het bijhorende temperatuurresultaat om de
data-afhankelijkheid per meetmoment aantoonbaar te maken. Beide actuaties implementeren
dezelfde `step:raam-actuatie`-procedure, wat de herbruikbaarheid van het abstracte plan illustreert.

## 5. Procedure en ObservableProperty

Elke stap (`p-plan:Step`) is tegelijk getypeerd als `sosa:Procedure` (en specifieker als
`sosa:ObservingProcedure` of `sosa:ActuatingProcedure`) zodat `sosa:implements` geldig is.

| Stap / Procedure | Type | Sensor/Actuator | Uitvoeringen |
|---|---|---|---|
| `step:temp-meting` | `sosa:ObservingProcedure` | `inst:thermometer-01` | `exec:temp-obs-20250427` |
| `step:raam-actuatie` | `sosa:ActuatingProcedure` | `inst:raam-opener-01` | `exec:raam-actuatie-20250427` |

Observeerbare/actueerbare eigenschappen (`sosa:Property`):

| IRI | Betekenis |
|---|---|
| `prop:binnentemperatuur` | Luchttemperatuur in de zaal (°C) |
| `prop:raam-stand` | Actueerbare eigenschap: percentage raamopening (0 = dicht, 100 = volledig open) |

## 6. Modelleer-keuzes toegelicht

### Waarom drielaags architectuur voor slechts twee stappen?

Verworpen alternatief: plat model met `sosa:ObservationCollection` en directe `prov:used`
van de actuatie naar de observatie.
Gekozen aanpak: Planning / Deployment / Execution met p-plan.
Motivatie: ook al zijn er maar twee stappen, de dataflow (temp-meting output → raam-actuatie
input) is expliciet via `p-plan:isPrecededBy` en `p-plan:isInputVarOf` te lezen. Dezelfde
`step:raam-actuatie`-procedure is herbruikbaar op andere kamers (R4b). Het drielaags model
maakt de afstand tussen het abstracte plan en de concrete uitvoering aantoonbaar, wat de
kernboodschap van dit voorbeeld is.

### Waarom geen afgeleide observatie?

Verworpen alternatief: een tussenstap die berekent of de drempel overschreden is (zoals
`step:afwijking-berekening` in `elektrisch-raam`).
Gekozen aanpak: de drempellogica (> 20 °C of < 18 °C) is opgenomen in de procedure
`step:raam-actuatie` zelf; de actuatie gebruikt direct het temperatuurresultaat via
`prov:used`.
Motivatie: bij een enkelvoudige drempelconditie voegt een extra afgeleide observatie
alleen complexiteit toe zonder extra informatiewaarde. De data-afhankelijkheid is via
`prov:used` reeds volledig traceerbaar.

### Waarom `sosa:hasResult` (IRI-entiteiten) en niet `sosa:hasSimpleResult`?

Verworpen alternatief: `sosa:hasSimpleResult "22.3"^^xsd:decimal` op de observatie.
Gekozen aanpak: benoemde `qudt:QuantityValue, prov:Entity`-entiteiten met eigen IRI.
Motivatie: het temperatuurresultaat wordt extern gerefereerd via `prov:used` door de
actuatie. Een blank node of `sosa:hasSimpleResult` laat geen externe referentie toe (R3).
Het raamstandresultaat volgt dezelfde stijl voor consistentie binnen het voorbeeld.

### Waarom `prov:used` en niet `sosa:hasInput` voor de actuatie?

Verworpen alternatief: `sosa:hasInput ent:result-temp-20250427` op de actuatie.
Gekozen aanpak: `prov:used ent:result-temp-20250427` op `exec:raam-actuatie-20250427`.
Motivatie: regel R5 verbiedt `sosa:hasInput` op execution-niveau. `sosa:hasInput` beschrijft
abstracte inputtypes op procedure-nodes; `prov:used` verwijst op execution-niveau naar
concrete entiteiten (PROV-O spec).

## 7. Tijdsmodellering

Patroon: `sosa:phenomenonTime → time:Instant → time:inXSDDateTimeStamp`.

Beide uitvoeringen delen hetzelfde `time:Instant` (`exec:instant-20250427T0900`) voor het
fenomeentijdstip, want de temperatuurmeting en de raambeweging slaan beide op het moment
09:00:00Z.

| Uitvoering | `sosa:resultTime` | `sosa:phenomenonTime` | Drempel |
|---|---|---|---|
| `exec:temp-obs-20250427` | 09:00:00Z | `exec:instant-20250427T0900` | 22.3 °C > 20 °C → open |
| `exec:raam-actuatie-20250427` | 09:00:05Z | `exec:instant-20250427T0900` | → 100 % |
| `exec:temp-obs-20250427T1000` | 10:00:00Z | `exec:instant-20250427T1000` | 17.5 °C < 18 °C → dicht |
| `exec:raam-actuatie-20250427T1005` | 10:00:05Z | `exec:instant-20250427T1000` | → 0 % |

Onderscheid:
- `sosa:phenomenonTime` — wanneer het fenomeen of de raambeweging fysiek plaatsvond
- `sosa:resultTime` — wanneer het resultaat beschikbaar werd (steeds 5 s na de meting voor actuaties)

De twee `time:Instant`-resources (`exec:instant-20250427T0900` en `exec:instant-20250427T1000`)
zijn aparte instanties omdat ze verschillende tijdstippen vertegenwoordigen.

## 8. Prefixen en IRI-structuur

| Prefix | Base URI | Tijdelijk of persistent |
|---|---|---|
| `plan:` | `https://example.org/temperatuur-raam/plan/` | Illustratief |
| `step:` | `https://example.org/temperatuur-raam/step/` | Illustratief |
| `var:` | `https://example.org/temperatuur-raam/var/` | Illustratief |
| `exec:` | `https://example.org/temperatuur-raam/exec/` | Illustratief |
| `ent:` | `https://example.org/temperatuur-raam/ent/` | Illustratief |
| `inst:` | `https://example.org/temperatuur-raam/inst/` | Illustratief |
| `htg:` | `https://example.org/herman-teirlinck/` | Illustratief (gedeeld met `elektrisch-raam`) |
| `prop:` | `https://example.org/temperatuur-raam/prop/` | Illustratief |
| `sosa:` | `http://www.w3.org/ns/sosa/` | Persistent (W3C) |
| `prov:` | `http://www.w3.org/ns/prov#` | Persistent (W3C) |
| `p-plan:` | `http://purl.org/net/p-plan#` | Persistent (purl.org) |
| `time:` | `http://www.w3.org/2006/time#` | Persistent (W3C) |
| `qudt:` | `http://qudt.org/schema/qudt/` | Persistent (QUDT) |
| `unit:` | `http://qudt.org/vocab/unit/` | Persistent (QUDT) |

Geen blank nodes voor extern gerefereerde resources (R10). De prefix `htg:` is gedeeld
met het `elektrisch-raam`-voorbeeld zodat `htg:gebouw-herman-teirlinck` en `htg:zaal-0116`
als dezelfde IRIs herkend worden bij gecombineerde bevragingen.

## 9. Inverse relaties

| Inverse paar | Reden |
|---|---|
| `sosa:hosts` ↔ `sosa:isHostedBy` | Zowel top-down (gebouw → zaal → sensor) als bottom-up navigeerbaar |
| `sosa:hasFeatureOfInterest` ↔ `sosa:isFeatureOfInterestOf` | Vanuit de zaal of het raam direct de bijhorende observaties en actuaties opvragen |
| `sosa:hasResult` ↔ `sosa:isResultOf` | Vanuit een resultaat-entiteit terug naar de observatie of actuatie navigeren |

`sosa:hasProperty` ↔ `sosa:isPropertyOf` is niet expliciet opgenomen; de eigenschappen
zijn via `sosa:hasProperty` op de FeatureOfInterest-nodes te navigeren.
