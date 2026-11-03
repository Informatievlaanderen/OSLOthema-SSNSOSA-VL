# Bespreking — ELF-meetnet

## 1. Wat stelt dit voorbeeld voor?

Een meetnet van ELF-nodes: draagbare meters die het laagfrequente magnetische veld (*extremely low
frequency*, typisch van elektrische installaties en hoogspanningslijnen) langs drie assen meten en
de waarden ongeveer elke minuut naar een ThingsBoard-platform sturen. Elke meetcampagne (een sensor
op een adres, voor een periode) is geregistreerd als Jira-ticket in het project SENS. Het voorbeeld
mapt de registratie van de 15 campagnes en de telemetrie van één campagne: ELF_C_0020 op
Obscurionweg 91 in Duisterwijk (SENS-269), van 26/11/2025 tot 26/01/2026. De bron is een interne
export (`source/`); er is nog geen publieke IRI.

<!-- TODO: wie beheert het ELF-meetnet (welke dienst), en met welk doel worden de campagnes uitgevoerd (blootstelling in woningen, opvolging van een klacht, een installatie)? -->

## 2. Kleurlegenda

| Kleur | SOSA-begrip | Betekenis in het domein |
|---|---|---|
| Blauw (#60c4e4) | `sosa:Sensor`, `sosa:Platform` / `sosa:FeatureOfInterest`, `prov:Location` | ELF-node, conversiescript, meetlocatie, adres |
| Paars (#c6a0f5) | `sosa:ObservingProcedure` | de meting door de node, de berekening van het uurgemiddelde |
| Oranje (#fe7130) | `sosa:Property` | RMStotal en de zes aswaarden |
| Roze (#e54b89) | `sosa:Deployment`, `sosa:ObservationCollection`, `sosa:Observation` | meetcampagne, uur- en minuutcollectie, observaties, uurgemiddelde |
| Geel (#f8b622) | `qudt:QuantityValue`, `time:Interval` | meetwaarden in µT, het uur van het uurgemiddelde |

## 3. Infrastructuur (blauwe nodes)

**`ex:sensor-ELF_C_0020`, `ex:sensor-ELF_C_0025`, …: `sosa:Sensor`.** Een ELF-node is een
apparaat dat waarneemt (R1). Het ID uit de registratie (`ELF_C_0020`) staat als `dcterms:identifier`.
De sensor `sosa:implements` de meetprocedure en `sosa:observes` de zeven eigenschappen. Er is geen
`sosa:hosts`: een sensor verhuist (zie §6).

<!-- TODO: wat onderscheidt een ELF_C-node van een ELF_L-node (bv. continu en laboratorium, of een ander type sonde)? Als het type eigen regels heeft, wordt het een subklasse; anders een begrip met dct:type (R18). -->

**`ex:meetlocatie-6839-obscurionweg-91`: `sosa:Platform` en `sosa:FeatureOfInterest`.**
Platform omdat de meter er opgesteld staat (`sosa:deployedOnPlatform` in de campagne);
studieobject omdat de waarnemingen het magnetische veld *op die plaats* beschrijven. De IRI volgt uit
postcode, straat en huisnummer, zodat twee campagnes op hetzelfde adres dezelfde meetlocatie delen
(SENS-269 en SENS-270 in Duisterwijk, SENS-96 en SENS-97 in Grimoorwoud).

<!-- TODO: staan ELF_C_0020 en ELF_C_0025 in Duisterwijk op dezelfde plek (dubbele meting, vergelijking van toestellen) of op verschillende plekken in het gebouw (binnen en buiten, verschillende verdiepingen)? In het laatste geval krijgt elke plek een eigen meetlocatie. -->

**`ex:adres-6839-obscurionweg-91`: `prov:Location`.** Het adres zoals de registratie het geeft,
met `prov:atLocation` vanaf de meetlocatie. De bron heeft geen coördinaten (zie §6).

**`ex:conversiescript`: `sosa:Sensor`.** Software die het uurgemiddelde berekent. Een softwareagent
die waarnemingen maakt is een `sosa:Sensor` (R1), zoals de Aerovision-rekenmodule in
`geluidsmeetnet/`.

**`ex:meetcampagne-SENS-269`: `sosa:Deployment`.** Eén Jira-ticket is één inzet van één sensor op één
meetlocatie, met `sosa:deployedSystem`, `sosa:deployedOnPlatform`, `sosa:hasFeatureOfInterest`,
`prov:startedAtTime` en `prov:endedAtTime`. `sosa:Deployment` is in SSN/SOSA 2023 een
`prov:Activity`, dus de PROV-tijden passen (R16). De Jira-sleutel staat als `dcterms:identifier`.

## 4. Observatie/Actuatie-structuur (roze nodes)

Drie niveaus:

1. **Uurcollectie** `ex:collectie-ELF_C_0020-20251127T10` (`sosa:ObservationCollection`): sensor,
   procedure en studieobject, met de minuutcollecties van dat lokale uur als leden.
2. **Minuutcollectie** `ex:meting-ELF_C_0020-20251127T090049427Z`: één ThingsBoard-bericht, met het
   `sosa:resultTime` en zeven observaties als leden.
3. **Observatie** `ex:obs-…-RMStotal`: eigenschap, studieobject en resultaat.

| IRI | observedProperty | usedProcedure | hasResult | hasFeatureOfInterest |
|---|---|---|---|---|
| `ex:obs-ELF_C_0020-20251127T090049427Z-RMStotal` | `ex:prop-RMStotal` | `ex:procedure-elf-meting` (uurcollectie) | `ex:result-…-RMStotal`: 0.68249 `unit:MicroT` | `ex:meetlocatie-6839-obscurionweg-91` |
| `ex:obs-ELF_C_0020-20251127T090049427Z-Xpeak_low` (en de vijf andere aswaarden) | `ex:prop-Xpeak_low` … | idem | `ex:result-…-Xpeak_low` … | idem |
| `ex:obs-ELF_C_0020-20251127T10-uurgemiddelde` | `ex:prop-RMStotal` | `ex:procedure-uurgemiddelde` | `ex:result-…-uurgemiddelde`: 0.67729 `unit:MicroT` | idem |

**Wat op de collecties staat.** SOSA 2023 laat leden de eigenschappen van een
`sosa:ExecutionCollection` erven, ook over geneste collecties. Op de uurcollectie: wat voor alle
leden gelijk is (sensor, procedure, studieobject). Op de minuutcollectie: wat zeven observaties
delen (het resultaattijdstip). Op de observatie: wat verschilt (eigenschap en resultaat).
`sosa:hasFeatureOfInterest` staat toch ook op elke observatie (zie §6).

**Het uurgemiddelde** is een afgeleide waarneming (R13): niet in een collectie, met alle verplichte
eigenschappen expliciet, `sosa:hasInputValue` naar de 60 RMStotal-*resultaten*,
`sosa:relatedObservation` naar de 60 RMStotal-*observaties* (R7) en een eigen `sosa:phenomenonTime`.

## 5. Procedure en Property

**`ex:procedure-elf-meting`**: de driedimensionale meting door de ELF-node; `sosa:implements` door
elke ELF-sensor, gebruikt door alle uurcollecties. `sosa:hasOutput` de zeven eigenschappen.

**`ex:procedure-uurgemiddelde`**: het rekenkundige gemiddelde van de RMStotal-waarden waarvan het
resultaattijdstip in het lokale uur [hh:00, hh+1:00) valt; `sosa:hasInput` en `sosa:hasOutput`
`ex:prop-RMStotal`. Geïmplementeerd door `ex:conversiescript`.

| Property | Betekenis |
|---|---|
| `ex:prop-RMStotal` | effectieve waarde (RMS) van de grootte van de magnetische fluxdichtheid over de drie assen |
| `ex:prop-Xpeak_low`, `ex:prop-Ypeak_low`, `ex:prop-Zpeak_low` | component per as, kanaal *low* (altijd positief in de data) |
| `ex:prop-Xpeak_high`, `ex:prop-Ypeak_high`, `ex:prop-Zpeak_high` | component per as, kanaal *high* (ook negatieve waarden) |

Alle zeven hebben `qudt:hasQuantityKind quantitykind:MagneticFluxDensity` en `skos:notation` met de
sleutel uit ThingsBoard.

**Een verband in de data.** Voor alle 82 748 meetmomenten geldt
`RMStotal = 1,2374 × √(Xpeak_low² + Ypeak_low² + Zpeak_low²)` (spreiding van de factor < 0,00002).
RMStotal is dus de grootte van de *low*-vector, geschaald met een vaste factor; het apparaat berekent
die zelf.

<!-- TODO: wat betekenen 'low' en 'high' (frequentieband, bv. 5 Hz–2 kHz en 2–400 kHz; of minimum en maximum binnen het meetvenster)? Waarom zijn de 'high'-waarden vaak negatief? En waar komt de factor 1,2374 vandaan (kalibratie, piek-naar-RMS)? -->

## 6. Modelleer-keuzes toegelicht

**Waarom een `sosa:Deployment` per meetcampagne, en geen `sosa:hosts`?**
Verworpen alternatief: `ex:meetlocatie-… sosa:hosts ex:sensor-…`. Gekozen: een `sosa:Deployment`
per Jira-ticket. Motivering: `sosa:hosts` is tijdloos, maar een ELF-node verhuist (ELF_C_0025:
Bloedhoven van april tot september 2025, daarna Duisterwijk). Met `sosa:hosts` zou ELF_C_0025 op twee plaatsen
tegelijk staan. De campagne geeft de periode en verbindt sensor, platform en studieobject (SOSA 2023:
*arrangement of assets … with respect to designated features of interest*).

**Waarom de meetlocatie als studieobject, en geen `sosa:SpatialSample`?**
Verworpen alternatief: de meetlocatie als ruimtelijk monster (R11) van een groter gebied, zoals de
omgeving van een hoogspanningslijn. Gekozen: `sosa:Platform` en `sosa:FeatureOfInterest`, zonder
sampling-keten. Motivering: de bron noemt geen groter studieobject. Een `sosa:isSampleOf` naar een
verzonnen gebied zou informatie toevoegen die er niet is. Zodra het doel van de campagnes gekend is
(§1), kan de meetlocatie een `sosa:SpatialSample` worden van de woning, het perceel of de installatie.

**Waarom een adres als `prov:Location` en geen geometrie?**
Verworpen alternatief: geocoderen naar `geo:hasGeometry` met een punt, of `locn:Address` met
afzonderlijke velden. Gekozen: `prov:atLocation` naar een `prov:Location` met het adres als label.
Motivering: de bron geeft enkel een adres. R11 (*Where a feature of interest is*) kiest
`prov:atLocation` wanneer de plaats door een adres gegeven is. Geocoderen zou een positie verzinnen.
`locn:Address` is geladen, maar valt buiten de kern (R17, niveau 3). Een label volstaat voor een
voorbeeld; in productie verwijst de meetlocatie naar de IRI van het adres in het Adressenregister.
Er blijft geen SHACL-warning over de geometrie: de regel geldt voor een `sosa:SpatialSample`, en dat is
de meetlocatie hier niet.

<!-- TODO: kan de registratie de ID van het Adressenregister meegeven (https://data.vlaanderen.be/id/adres/…), en voor 'Bahaalweg z/n, Grafsteenzele' een perceel of coördinaten? -->

**Waarom microtesla, en waarom een `qudt:QuantityValue`?**
Gekozen: `sosa:hasResult` naar een `qudt:QuantityValue` met `qudt:numericValue` en
`qudt:hasUnit unit:MicroT` (R3). Verworpen: `sosa:hasSimpleResult` met een kaal getal, waarbij de
eenheid verloren gaat, en het uurgemiddelde heeft benoemde resultaten nodig als inputwaarde. De
eenheid is een **aanname**: de bron vermeldt ze niet. Het bereik van RMStotal (0,20–1,72) past bij
µT voor een binnenomgeving bij elektrische installaties, en niet bij nT of mT. QUDT volstaat; er is
geen registereenheid nodig.

<!-- TODO: bevestiging door de beheerder van het meetnet: zijn alle zeven waarden in µT? -->

**Waarom zeven eigenschappen, en niet één vectoreigenschap?**
Verworpen alternatief: één eigenschap *magnetische fluxdichtheid* met een vectorresultaat, of
`RMStotal` als afgeleide waarneming uit de drie *low*-componenten. Gekozen: zeven `sosa:Property`'s,
één per ThingsBoard-sleutel, elk met `quantitykind:MagneticFluxDensity`. Motivering: de betekenis van
*low* en *high* is niet gedocumenteerd (§5). Elke sleutel apart houdt de data getrouw aan de bron
zonder een interpretatie op te leggen. RMStotal is weliswaar berekend (§5), maar door het apparaat
zelf, in hetzelfde bericht. Het hoort bij de output van de meetprocedure, niet bij een aparte afleiding
achteraf. Een alternatieve mapping kan RMStotal wél als afgeleide waarneming modelleren
(`sosa:hasInputValue` naar de drie *low*-resultaten), zodra de factor 1,2374 verklaard is.

**Waarom geneste collecties?**
Gekozen: een uurcollectie met minuutcollecties, elk met zeven observaties. Verworpen: losse
observaties met sensor, procedure en resultaattijd op elk van de zeven herhaald, of één collectie per
campagne (82 748 leden, onhandig in een bestand per dag). Het lokale uur is ook de eenheid van het
uurgemiddelde.

**Waarom `sosa:hasFeatureOfInterest` toch op elke observatie?**
SOSA 2023 laat de leden het studieobject van de collectie erven. De SHACL die ld-mcp uit de
OWL-restrictie op `sosa:Execution` (`someValuesFrom sosa:FeatureOfInterest`) genereert, ziet die
overerving echter niet. Daarom staat het studieobject op elk lid, zoals in `brdr/` en
`geluidsmeetnet/`.

**Waarom een uurgemiddelde dat niet in de bron staat?**
Het uurgemiddelde illustreert een afgeleide waarneming (R13), zoals de dagsom in
`verkeersmetingen/`. Het script berekent het, dus is het script de sensor, en niet de ELF-node: de
herkomst blijft zichtbaar. De eigenschap is dezelfde als die van de inputwaarden (`ex:prop-RMStotal`).
De aggregatie zit in de procedure en het interval in de `sosa:phenomenonTime`, zoals in
`verkeersmetingen/`. Uren met ontbrekende minuten (bv. 34 van de 60 op 27/11 tussen 7 en 8 uur)
krijgen het gemiddelde over de beschikbare waarden; het aantal staat in `rdfs:comment`.

<!-- TODO: welk aggregaat gebruikt de beheerder voor blootstelling (rekenkundig gemiddelde van RMS, kwadratisch gemiddelde, mediaan, percentiel), en over welke periode (uur, nacht, campagne)? -->

**Waarom de apparaatstatus niet mappen?**
`lastConnectTime`, `lastActivityTime`, `lastDisconnectTime`, `lastInactivityAlarmTime`,
`inactivityTimeout` en `active` beschrijven de verbinding van het apparaat met ThingsBoard, niet het
magnetische veld. Als observaties van de meetlocatie zouden ze een verkeerd studieobject krijgen. Als
eigenschappen van de sensor horen ze bij het beheer van het platform, niet bij de waarnemingsdata
(R16, in de geest: gegevens over het record of het apparaat zijn geen waarneming). De perioden waarin
`active` onwaar is, verklaren de gaten in de reeks (de grootste duurt ruim 11 uur).

**Waarom geen persoonsgegevens?**
De registratie bevat e-mailadressen, namen en voornamen van contactpersonen, en soms de naam van een
bedrijf of een site. Die worden niet overgenomen: ze zijn niet nodig voor de waarnemingen. De
bronbestanden zelf zijn bovendien gepseudonimiseerd met namen uit De Rode Ridder
(`scripts/anonimiseer.py`, zie README). Gemeenten, straten, postcodes, personen en e-mailadressen zijn
fictief, en dus ook de adressen en de IRI's van de meetlocaties in dit voorbeeld
(`ex:meetlocatie-6839-obscurionweg-91`). Meetwaarden, datums, sensor-ID's en Jira-sleutels zijn echt.

**Waarom geen `prov:endedAtTime` voor SENS-320?**
Het einde (31/12/2026) ligt na de peildatum van de export (`PEILDATUM` in het script). Een gepland
einde is geen afgelopen activiteit; het staat als commentaar.

**Patronen.** *Afgeleide waarneming* gevolgd (het uurgemiddelde). *Ruimtelijk monster* overwogen en
niet gevolgd (zie hoger). *Emissie* en *stimulus* passen niet: de vraag gaat over het veld op een
plaats, niet over een bron of een gebeurtenis.

**Vocabularia.** Enkel de kern (R17, niveau 1): SOSA/SSN 2023, PROV-O, QUDT, OWL-Time, DCTERMS,
SKOS, RDFS. Geen afweging buiten de kern nodig.

**Validatie.** `elf.ttl` en `elf.trig`: geen fouten, geen suspects, geen SHACL-warnings.

## 7. Tijdsmodellering

- **Resultaattijd van een meetmoment:** `sosa:resultTime` op de minuutcollectie, als
  `xsd:dateTimeStamp` in UTC met milliseconden, zoals ThingsBoard de tijdstempel geeft (R12: een
  gegeven tijdzone blijft behouden). Het is het tijdstip waarop het resultaat beschikbaar werd.
- **Fenomeentijd van een meetmoment:** niet opgenomen. RMS- en piekwaarden gelden over een
  meetvenster, dus een `time:Instant` zou fout zijn (R12), en de duur van het venster is niet gekend.

  <!-- TODO: over welk venster berekent de node RMStotal en de piekwaarden (de minuut vóór de tijdstempel, enkele seconden)? Dan krijgt elke minuutcollectie een time:Interval als sosa:phenomenonTime. -->

- **Uurgemiddelde:** `sosa:phenomenonTime` naar een `time:Interval` van één lokaal uur, halfopen,
  met `time:Instant`s in `time:inXSDDateTimeStamp` (`2025-11-27T10:00:00+01:00` →
  `2025-11-27T11:00:00+01:00`). Lokale tijd, omdat uurwaarden zo gelezen worden; skolem-IRI's (R10).
  Een minuut hoort bij het uur van haar resultaattijd: `09:00:49Z` is 10:00:49 lokale tijd.
- **Meetcampagne:** `prov:startedAtTime` en `prov:endedAtTime` (`xsd:dateTime`) op middernacht
  lokale tijd. De registratie geeft enkel datums (`26/nov/25 12:00 AM`). Aanname: de datums zijn in
  `Europe/Brussels`, met `+01:00` in de winter en `+02:00` tijdens de zomertijd.
  De ThingsBoard-export voor SENS-269 begint om 09:00 UTC. Dat is het venster van de export, geen
  begin van de campagne; de eerste meting volgt om 09:07 UTC.

## 8. Prefixen en IRI-structuur

| Prefix | Basis-IRI | Tijdelijk of persistent |
|---|---|---|
| `sosa:` | `http://www.w3.org/ns/sosa/` | persistent (W3C) |
| `prov:` | `http://www.w3.org/ns/prov#` | persistent (W3C) |
| `time:` | `http://www.w3.org/2006/time#` | persistent (W3C) |
| `qudt:` | `http://qudt.org/schema/qudt/` | persistent |
| `unit:` | `http://qudt.org/vocab/unit/` | persistent |
| `quantitykind:` | `http://qudt.org/vocab/quantitykind/` | persistent |
| `dcterms:` | `http://purl.org/dc/terms/` | persistent |
| `skos:` | `http://www.w3.org/2004/02/skos/core#` | persistent (W3C) |
| `rdfs:` | `http://www.w3.org/2000/01/rdf-schema#` | persistent (W3C) |
| `xsd:` | `http://www.w3.org/2001/XMLSchema#` | persistent (W3C) |
| `ex:` | `https://example.org/elf/` | tijdelijk (illustratief) |

IRI-patronen onder `ex:`, allemaal deterministisch (R10, *stabiele IRI's in pijplijnen*):

| Resource | Patroon | Sleutel |
|---|---|---|
| sensor | `sensor-{ID}` | titel van het ticket |
| meetlocatie, adres | `meetlocatie-{postcode}-{straat}-{nr}`, `adres-…` | adresvelden |
| meetcampagne | `meetcampagne-{ticket}` | Jira-sleutel |
| uurcollectie | `collectie-{ID}-{jjjjmmdd}T{uu}` | sensor en lokaal uur |
| minuutcollectie, observatie, resultaat | `meting-{ID}-{UTC-tijdstempel met ms}`, `obs-…-{sleutel}`, `result-…-{sleutel}` | sensor, tijdstip, sleutel |
| uurgemiddelde, interval, instants | `obs-{ID}-{uur}-uurgemiddelde`, `interval-…`, `instant-…-begin` / `-einde` | sensor en lokaal uur |

Geen blanke knopen: het is een grote, gescripte dataset (R10).

<!-- TODO: welke persistente basis-IRI krijgt het meetnet in productie (bv. https://data.omgeving.vlaanderen.be/id/…)? -->

## 9. Inverse relaties

- `sosa:hasDeployment` (sensor → campagne) en `sosa:inDeployment` (meetlocatie → campagne): opgenomen.
  Zo vind je vanuit een sensor of een adres snel alle campagnes, en dat is de vraag die de registratie
  beantwoordt.
- `sosa:isMemberOf`, `sosa:isResultOf` en `sosa:isFeatureOfInterestOf`: **niet** opgenomen. Op
  minuutniveau zouden ze per meetmoment 22 triples toevoegen (8 `isMemberOf`, 7 `isResultOf`, 7 `isFeatureOfInterestOf`). Een SPARQL-endpoint met inferentie
  of een omgekeerd pad (`^sosa:hasMember`) bereikt hetzelfde.
