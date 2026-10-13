# Bespreking — overstort, alternatief: de overstorting als emissie

Deze bespreking beschrijft `overstort_emissie.ttl`. Het hoofdmodel staat in
`../overstort_herzien.ttl` en `../bespreking.md`. Dit is geen herziening: beide lezingen zijn
verdedigbaar, en de werkgroep kiest.

## 1. Wat stelt dit voorbeeld voor?

Dezelfde overstortdata van Aquafin als het hoofdmodel, maar gelezen vanuit wat de overstort in het
oppervlaktewater brengt: een overstorting is een emissie van ongezuiverd rioolwater, net zoals een
lozing in `waterkwaliteit/`. Het voorbeeld bevat twee records. (a) is het LDES-event zonder
overstorting (NietInWerking). (b) is een overstorting van vier minuten op 27 juli 2024 uit Aquafins
doelmodel *Observaties Debiet & Overstortduur*
(<https://informatievlaanderen.github.io/OSLO-mapping/water/Aquafin%20-%20Overstort%20In%20Vlaanderen/>).

## 2. Kleurlegenda

| Kleur | SOSA-concept | Betekenis in het domein |
|---|---|---|
| Blauw (#60c4e4) | `sosa:Platform` / `sosa:Sensor` / `geo:Geometry` | meetpunt, overstortmeter, ligging |
| Paars (#c6a0f5) | `sosa:ActuatingProcedure` | het overstorten als werking van het kunstwerk |
| Oranje-rood (#fe7130) | `sosa:Property` | werking van de overstort, overstortduur |
| Roze (#e54b89) | `sosa:Actuation` / `sosa:Observation` / `sosa:ObservationCollection` | werking van de overstort, observaties |
| Oranje (#f8b622) | `wk:Emissie` / `qudt:QuantityValue` / `time:Interval` | de overstorting, resultaten, periode |

De emissie is oranje: in dit patroon is ze een entiteit, het resultaat van de actuatie.

## 3. Infrastructuur (blauwe nodes)

- **`meetpunt:P_000000217952`**: `sosa:Platform` dat de meter van record (b) herbergt, en
  `sosa:FeatureOfInterest` van de *actuatie*, niet van de observaties. Er zijn twee geometrieën:
  WGS84 en Lambert 72. De emissie verwijst naar dezelfde twee (`geo:hasGeometry`); de actuatie
  verwijst naar het meetpunt met `prov:atLocation`.
- **`sensor:2c2491f0e1234a7200b561c65718b9b5`**: de meter van record (b) (`isWaargenomenMet`
  418858). De IRI komt uit de MD5 van het toestelnummer, zoals in het hoofdmodel.
- **`meetpunt:P_000000350733`** en **`sensor:4c314f…`**: dezelfde als in het hoofdmodel, voor
  record (a).

<!-- TODO: hoort record (b) bij meetpunt P_000000217952? De coördinaten zijn gelijk, maar het record vermeldt geen meetpunt en een ander toestel (418858) dan het sensorvoorbeeld (P2050378). -->

## 4. Observatie/Actuatie-structuur (roze nodes)

| IRI | observedProperty / actsOnProperty | usedProcedure | hasResult | hasFeatureOfInterest |
|---|---|---|---|---|
| `alt:overstortwerking-P_000000217952-20240727T140000Z` (Actuation) | `kenmerk:Overstort` | `alt:procedure-overstorten` | `alt:overstorting-…` (de emissie) | `meetpunt:P_000000217952` |
| `alt:obs-…-status` | `kenmerk:Overstort` | — | `overstortstatus:InWerking` | `alt:overstorting-…` |
| `alt:obs-…-overstortduur` | `alt:prop-overstortduur` | — | 240 `unit:SEC` | `alt:overstorting-…` |
| `alt:obs-…-debiet` | `alt:prop-debiet` | — | 2.3 `unit:M3-PER-SEC` (aangenomen) | `alt:overstorting-…` |
| `event:4004f4ea-…` | `kenmerk:Overstort` | — | `overstortstatus:NietInWerking` | `meetpunt:P_000000350733` |

De collectie `alt:collectie-P_000000217952-20240727T140000Z` draagt wat de drie observaties van
de emissie delen: het studieobject, de sensor en de periode (`sosa:phenomenonTime`).

## 5. Procedure en Property

- **`alt:procedure-overstorten`** (`sosa:ActuatingProcedure`): het afvoeren van overtollig
  rioolwater naar het oppervlaktewater wanneer het peil de overstortdrempel overschrijdt. Het
  ontologiemodel van waterkwaliteit vraagt deze procedure: `wk:Emissie` is `prov:wasDerivedFrom`
  ten minste één `sosa:Procedure`. Er is geen `sosa:implementedBy`, omdat het kunstwerk een passieve
  drempel is en geen `sosa:Actuator`.
- **`kenmerk:Overstort`**: de werking van de overstort, zoals in het hoofdmodel. Ze is hier de
  property waarop de actuatie inwerkt (`sosa:actsOnProperty`). De statusobservatie gebruikt ze ook.
- **`alt:prop-overstortduur`**: de duur van de overstorting in seconden, een eigenschap van de
  emissie.
- **`alt:prop-debiet`**: het debiet van het overgestorte rioolwater over de periode van de
  overstorting, een eigenschap van de emissie.

Voor de observaties is er geen procedure, net als in het hoofdmodel: de R2-waarschuwing blijft.

## 6. Modelleer-keuzes toegelicht

**Waarom de overstorting als studieobject?**
Hoofdmodel: het meetpunt is het studieobject, een event observeert de werking van het kunstwerk.
Alternatief: de overstorting is een `wk:Emissie` en het studieobject van haar observaties. De
periode staat op `sosa:phenomenonTime`. De plaats is een geometrie op de emissie zelf
(`geo:hasGeometry`, R11 *Where a feature of interest is*), gedeeld met het meetpunt: de
coördinaten zijn bekend, dus een omweg via `prov:atLocation` is niet nodig. Dat maakt de emissie
een `geo:Feature`, ruimtelijk te bevragen zonder via het meetpunt te gaan. `prov:atLocation` zou
niet fout zijn, maar past beter als de plaats enkel als adres of omschrijving bekend is (zoals de
meetposten in `geluidsmeetnet/alternatief/`). Op de actuatie, een activiteit en geen feature,
blijft `prov:atLocation` naar het meetpunt.

*Voor het alternatief:*
- Het volgt het patroon van de lozing in `waterkwaliteit/` en van het geluidsevent in
  `geluidsmeetnet/alternatief/`. Een overstorting is een lozing van ongezuiverd rioolwater; met
  hetzelfde patroon zijn overstortingen en industriële lozingen samen bevraagbaar, bv. alle
  emissies in een waterloop.
- Overstortduur en debiet (Aquafins doelmodel) zijn eigenschappen van de overstorting, niet van het
  kunstwerk. Een vracht (debiet × duur × concentratie) heeft dan hetzelfde studieobject als in
  `waterkwaliteit/`.
- Elke overstorting heeft een eigen IRI. Een rapport per overstorting of een koppeling met een
  meting in de ontvangende waterloop verwijst daarnaar.

*Tegen het alternatief:*
- Niet elk event is een emissie. De stroom bevat ook NietInWerking en WerkingOnbekend. Die events
  houden het meetpunt als studieobject (record a), dus hangt het studieobject af van de status van
  het event. Een query naar "alle events op dit meetpunt" moet dan twee paden volgen.
- De status `InWerking` is op een emissie redundant: dat de emissie bestaat, zegt al dat er
  overstort was.
- Het model is zwaarder. `wk:Emissie` vraagt een `prov:Activity`, een `sosa:Actuation` en een
  `sosa:Procedure` (de restricties van `waterkwaliteit.ttl`). Dat zijn per overstorting drie
  resources meer dan in het hoofdmodel.
- De vraag van de LDES-stroom is "wanneer en waar stortte een overstort over?". Dat is een vraag
  naar de toestand van een plaats, waarvoor `patterns.md` het emissiepatroon afraadt.

*Tussenvorm:* het hoofdmodel blijft voor de eventstroom (meetpunt als studieobject, alle statussen
gelijk). Enkel waar Aquafin grootheden van de overstorting zelf publiceert (debiet, duur, later
vracht), wordt een `wk:Emissie` gemaakt. Die verwijst met `sosa:relatedObservation` naar het event
waaruit ze voortkomt. Zo heeft de eventstroom één vorm en krijgen de emissiegrootheden toch het
studieobject van `waterkwaliteit/`.

**Waarom een `sosa:Actuation` voor de werking van de overstort?**
`wk:Emissie` vraagt `sosa:isResultOf` een actuatie en `prov:wasGeneratedBy` een activiteit. Eén
resource vervult beide (`sosa:Actuation` ⊂ `sosa:Execution` ⊂ `prov:Activity`; `sosa:hasResult` ⊂
`prov:generated`). De actuatie werkt in op `kenmerk:Overstort` van het meetpunt. Zo is ze de
tegenhanger van de observatie in het hoofdmodel: het hoofdmodel observeert de werking, het
alternatief modelleert ze als handeling. Er is geen `sosa:madeByActuator`, omdat een overstortdrempel
niet aangestuurd wordt.
<!-- TODO: hebben sommige overstorten een aangestuurde klep of pomp? Dan is die de sosa:Actuator. -->

**Debiet met een aangenomen eenheid.**
Het doelmodel geeft `"debiet": "2.3"` zonder eenheid. Een getal zonder eenheid schendt R3, dus is
voor dit voorbeeld m³/s (`unit:M3-PER-SEC`) aangenomen. Die eenheid is verzonnen; het voorbeeld
toont enkel de structuur. Zo samen met de duur is een overgestort volume af te leiden
(2.3 m³/s × 240 s = 552 m³), als afgeleide observatie volgens R13.
<!-- TODO: in welke eenheid levert Aquafin het debiet (m³/s, l/s, m³/h)? Is het een gemiddeld of een piekdebiet over de overstorting? -->

**Waarom `wk:Emissie`? (R17)**
`wk:Emissie` komt uit de ontwerpversie van het waterkwaliteitsvocabularium in dit project
(`src/main/resources/be/vlaanderen/data/ns/waterkwaliteit/waterkwaliteit.ttl`). De doorslaggevende
reden is samenhang: hetzelfde begrip als de lozingen in `waterkwaliteit/`, binnen het lopende
OSLO-traject (voorkeursvolgorde 3). De toetsing aan de criteria van R17 brengt wel een zwak punt
aan het licht:

- *Dereferenceerbaar (1), versiebeheer (3):* het namespace `https://data.vlaanderen.be/ns/waterkwaliteit#`
  geeft Turtle, RDF/XML en JSON-LD terug, maar dat is de **gepubliceerde** versie (kandidaat-standaard
  2023). Daar is `wk:Emissie` een subklasse van `gfi:GFI_Feature` (ISO 19156), niet van
  `prov:Entity` en `sosa:FeatureOfInterest`. Wie de IRI opvraagt, krijgt dus een andere definitie
  dan die waarmee dit voorbeeld gevalideerd is. Het ontwerp heeft geen eigen `owl:versionIRI`.
- *Aansluiting (7) en uitlijning met de kern (8):* in het ontwerp goed (`⊂ prov:Entity`,
  `⊂ sosa:FeatureOfInterest`).
- *Verbintenis (9):* de restricties vragen per emissie een activiteit, een actuatie en een
  procedure. Zie hierboven: zwaar voor een passieve overstort.

Verworpen alternatieven:
- een eigen klasse onder `alt:`: dat zou de samenhang met `waterkwaliteit/` verbreken, precies wat
  dit alternatief wil tonen;
- enkel `prov:Entity` en `sosa:FeatureOfInterest`, zonder `wk:Emissie`: kern-only (voorkeur 1),
  maar dan is de emissie niet als emissie herkenbaar en niet samen met lozingen te bevragen. Dat
  is een volwaardige tussenvorm voor de werkgroep.
<!-- TODO: zolang het herziene waterkwaliteitsvocabularium niet gepubliceerd is, verdient het ontwerp een eigen owl:versionIRI (of een tijdelijk namespace), zodat dereferentie en validatie dezelfde definitie gebruiken. -->

**Eenheden:** QUDT (`unit:SEC`, `unit:M3-PER-SEC`), zoals de standaardkeuze van R3. De
overstortduur 240 komt overeen met de periode 14:00–14:04, dus de eenheid is seconden.

**Gelaten waarschuwingen:** R2 (`sosa:usedProcedure`) op de vier observaties. De bron noemt geen
meetprocedure.

**Discussievragen voor de werkgroep:**
1. Is de vraag achter de overstortdata de toestand van het kunstwerk ("stortte het over?") of de
   belasting van het oppervlaktewater ("hoeveel kwam erin?")? Het eerste pleit voor het
   hoofdmodel, het tweede voor het alternatief.
2. Mag het studieobject van een event afhangen van zijn status (emissie bij InWerking, meetpunt
   anders), of moet de eventstroom één vorm hebben (tussenvorm)?
3. Zijn de restricties van `wk:Emissie` (actuatie, procedure) voor een passieve overstort zinvol,
   of horen ze te versoepelen in `waterkwaliteit.ttl`?
4. Moeten overstortingen en industriële lozingen in dezelfde klasse vallen, zodat een query naar
   alle emissies in een waterloop beide vindt?

## 7. Tijdsmodellering

Zoals in het hoofdmodel: `sosa:phenomenonTime → time:Interval → time:hasBeginning / time:hasEnd
→ time:Instant → time:inXSDDateTimeStamp` (R12), met de tijdzone uit de bron (`Z`). Bij record (b)
staat het interval op de collectie, en de leden erven het (SOSA 2023). De emissie zelf is tijdloos,
zoals het patroon voorschrijft. De actuatie heeft geen eigen tijd, omdat die gelijk zou zijn aan het
interval. `modifiedAt` en `validatieStatus` ("raw") uit het doelmodel zijn niet overgenomen.
<!-- TODO: wat betekent validatieStatus "raw", en wordt een overstorting na validatie een nieuwe versie (dct:isVersionOf) of een nieuwe emissie? -->

## 8. Prefixen en IRI-structuur

| Prefix | Basis-IRI | Tijdelijk of persistent |
|---|---|---|
| `sosa:`, `prov:`, `time:` | W3C | persistent |
| `qudt:`, `unit:` | `http://qudt.org/schema/qudt/`, `http://qudt.org/vocab/unit/` | persistent |
| `geo:` | `http://www.opengis.net/ont/geosparql#` | persistent (OGC) |
| `dct:` | `http://purl.org/dc/terms/` | persistent (DCMI) |
| `wk:` | `https://data.vlaanderen.be/ns/waterkwaliteit#` | ontwerp (waterkwaliteit, dit project) |
| `xsd:`, `rdfs:` | W3C | persistent |
| `sensor:`, `event:`, `meetpunt:` | `https://aquafin.be/id/…/` | productie-IRI's van Aquafin, gedeeld met het hoofdmodel |
| `kenmerk:`, `overstortstatus:` | `https://aquafin.be/id/concept/…/` | concept-IRI's van Aquafin, gedeeld met het hoofdmodel |
| `alt:` | `https://example.org/overstort/alternatief/` | tijdelijk, enkel voor dit alternatief |

De emissie, de actuatie, de collectie, het interval en de resultaten hebben skolem-IRI's uit het
meetpunt en de starttijd (`…-P_000000217952-20240727T140000Z`, R10). Dat is meteen een
deterministische sleutel voor een overstorting, wat het hoofdmodel voor events nog mist (§8 daar).
Bij aanname zouden ze naar `https://aquafin.be/id/…` verhuizen.

## 9. Inverse relaties

- `sosa:hasResult` ↔ `sosa:isResultOf` (actuatie ↔ emissie); daarnaast `prov:wasGeneratedBy`
  vanaf de emissie;
- `sosa:hasFeatureOfInterest` ↔ `sosa:isFeatureOfInterestOf` (collectie ↔ emissie, actuatie ↔
  meetpunt, event ↔ meetpunt);
- `sosa:hasMember` ↔ `sosa:isMemberOf` (collectie ↔ observaties);
- `sosa:hosts` ↔ `sosa:isHostedBy`, `sosa:hasProperty` ↔ `sosa:isPropertyOf`,
  `sosa:madeBySensor` ↔ `sosa:madeObservation` (enkel bij record a, zoals in het hoofdmodel).
