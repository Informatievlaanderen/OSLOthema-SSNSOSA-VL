# Bespreking — Geluidsmeetnet Brussels Airport

## 1. Wat stelt dit voorbeeld voor?

Dit voorbeeld modelleert één meetdag (29 september 2026, 07:00 → 30 september 07:00) van het
geluidsmeetnet rond Brussels Airport (EBBR), zoals geëxporteerd uit het verwerkingsplatform
Aerovision (`brondata/voorbeeld_aerovision_data_20260929.zip`). Geluidsmeters op 13
meetcampagnes registreren **geluidsevents**. Aerovision koppelt elk event aan de **vlucht** die
het veroorzaakte (via radargegevens) en berekent per meetpost **dagindicatoren voor
vliegtuiggeluid**: L24, Ld, Le, Ln, Lden, LAeq, LAmax en SEL. De gevalideerde subset
(`geluidsmeetnet.ttl`) bevat campagne M072-2 met 58 events. De volledige dataset staat in
`geluidsmeetnet.trig` (1 818 events, 13 campagnes).

## 2. Kleurlegenda

| Kleur | SOSA-concept | Domeinbetekenis |
|---|---|---|
| Blauw (#60c4e4) | Platform / System / Sensor / Deployment / FeatureOfInterest | Meetpost, meetcampagne, geluidsmeter, meetnet, Aerovision-rekenmodule, omgeving van de luchthaven |
| Paars licht (#c6a0f5) | sosa:ObservingProcedure | Eventmeting en de rekenregels voor de dagindicatoren |
| Oranje (#fe7130) | sosa:Property | Akoestische grootheden (LAeq, LAmax, SEL, duur, Ld, Le, Ln, Lden, …) |
| Roze (#e54b89) | Observation / ObservationCollection / Sampling / prov:Activity | Eventmetingen, dagindicatoren, keuze van de meetpost, vlucht |
| Geel (#f8b622) | sosa:Result / time:Interval / time:Instant / sosa:Stimulus / prov:Entity | Meetwaarden, tijden, het geluidsevent, het luchtvaartuig |
| Lichtgeel (#f8e1ad, subgraaf) | DERIVATION | Afgeleide dagindicatoren |

## 3. Infrastructuur (blauwe nodes)

**`ex:meetpost-M072` — `sosa:Platform`, `sosa:FeatureOfInterest`, `sosa:SpatialSample` (+ `sosa:Sample`)**
Drievoudige typering, zoals in `verkeersmetingen` (R11):
- `sosa:Platform`: de meetpost draagt de geluidsmeter (`sosa:hosts`).
- `sosa:FeatureOfInterest`: het geluidsniveau wordt op precies deze plek bepaald. Wat een meter
  meet, is het geluidsveld *op de meetpost*, niet de vlucht en niet het hele gebied.
- `sosa:SpatialSample` van `ex:omgeving-EBBR` (`sosa:isSampleOf`): de meetpost is een
  puntmonster van het geluidsbelaste gebied rond de luchthaven. Ze is het resultaat van een
  ruimtelijke bemonstering `ex:sampling-meetpost-M072` (`sosa:Sampling`).

<!-- TODO: Wat zijn de coördinaten (en eventueel de hoogte boven maaiveld) van de meetposten? De Aerovision-export bevat ze niet; zodra ze bekend zijn: geo:hasGeometry [ geo:asWKT "Point(lon lat)" ] toevoegen (R11). -->

**`ex:campagne-M072-2` — `sosa:Deployment`**
De kolom `Campaigns` bevat codes zoals `F040-2` en `M072-2`. In dit voorbeeld lezen we die als
*meetpost* (`M072`) + *volgnummer van de inzet* (`-2`). De campagne is dan de inzet
(`sosa:deployedSystem`) van een geluidsmeter op een meetpost (`sosa:inDeployment`). Zo blijft de
meetpost hetzelfde FOI over opeenvolgende campagnes heen, ook als de meter vervangen of
verplaatst wordt.

<!-- TODO: Klopt de interpretatie van de campagnecode (prefix F = vaste meetpost, M = mobiele meetpost? suffix = volgnummer van de inzet)? Zo niet, dan valt sosa:Deployment weg en wordt de volledige code de meetpost-ID. -->

**`ex:geluidsmeter-M072-2` — `sosa:Sensor` (+ `sosa:System`)**
De geluidsmeter detecteert events (het event verwijst ernaar met `sosa:isDetectedBy`), implementeert
`ex:procedure-eventmeting` en observeert LAeq, LAmax, SEL en duur. `sosa:System` staat er
expliciet bij, omdat `sosa:hosts`, `sosa:hasSubSystem` en `sosa:deployedSystem` een systeem
verwachten en de SHACL-validatie op het niet-afgeleide model gebeurt.

**`ex:aerovision-rekenmodule` — `sosa:Sensor` (+ `sosa:System`)**
De software die de dagindicatoren berekent. Een softwareagent die observaties maakt, is volgens
R1 een `sosa:Sensor`. Ze implementeert de vier rekenprocedures.

**`ex:geluidsmeetnet-EBBR` — `sosa:System`**
Het meetnet als geheel, met `sosa:hasSubSystem` naar alle geluidsmeters en de rekenmodule.

**`ex:omgeving-EBBR` — `sosa:FeatureOfInterest`**
Het ultieme FOI: het gebied rond Brussels Airport. Het is het FOI van de bemonstering en het
doel van de campagnes (`sosa:hasUltimateFeatureOfInterest` op de Deployment).

## 4. Observatie/Actuatie-structuur (roze nodes)

De observaties zitten in **twee niveaus van collecties**:

1. **Dagcollectie** `ex:collectie-M072-2-20260929`: alle eventcollecties van de campagne op de
   meetdag. Gedeelde metadata: `madeBySensor` (de geluidsmeter), `usedProcedure`
   (eventmeting), `hasFeatureOfInterest` (de meetpost), `phenomenonTime` (het etmaal).
2. **Eventcollectie** `ex:eventcollectie-M072-2-<startUTC>`: de vier metingen van één event.
   Ze deelt het tijdsinterval van het event en verwijst met `sosa:wasOriginatedBy` naar de
   stimulus (het geluidsevent).

Observaties van het voorbeeld-event (vertrek BCS6TP, 30/09 01:22:39–01:23:58):

| IRI | observedProperty | usedProcedure | hasResult | hasFeatureOfInterest |
|---|---|---|---|---|
| `ex:obs-M072-2-20260929T232239Z-LAeq` | `ex:prop-LAeq` | (collectie) `ex:procedure-eventmeting` | 57.392307 dB(A) | `ex:meetpost-M072` |
| `ex:obs-M072-2-20260929T232239Z-LAmax` | `ex:prop-LAmax` | (collectie) | 62.97 dB(A) | `ex:meetpost-M072` |
| `ex:obs-M072-2-20260929T232239Z-SEL` | `ex:prop-SEL` | (collectie) | 76.368576 dB(A) | `ex:meetpost-M072` |
| `ex:obs-M072-2-20260929T232239Z-duur` | `ex:prop-duur` | (collectie) | 79 s | `ex:meetpost-M072` |

Afgeleide dagindicatoren (buiten de collecties, `madeBySensor ex:aerovision-rekenmodule`):

| IRI | observedProperty | usedProcedure | hasResult | hasInputValue |
|---|---|---|---|---|
| `ex:obs-M072-2-20260929-L24` | `ex:prop-L24` | energetische-sommatie | 40.45 | SEL van alle 58 events |
| `ex:obs-M072-2-20260929-Ld` | `ex:prop-Ld` | energetische-sommatie | 42.31 | SEL van de 40 D-events |
| `ex:obs-M072-2-20260929-Le` | `ex:prop-Le` | energetische-sommatie | 39.33 | SEL van de 13 E-events |
| `ex:obs-M072-2-20260929-Ln` | `ex:prop-Ln` | energetische-sommatie | 35.39 | SEL van de 5 N-events |
| `ex:obs-M072-2-20260929-SEL` | `ex:prop-SEL` | energetische-sommatie | 89.81 | SEL van alle events |
| `ex:obs-M072-2-20260929-LAmax` | `ex:prop-LAmax` | maximum | 65.28 | LAmax van alle events |
| `ex:obs-M072-2-20260929-LAeq-vliegtuiggeluid` | `ex:prop-LAeq-vliegtuiggeluid` | energetisch-gemiddelde-eventduur | 53.74 | SEL + duur van alle events |
| `ex:obs-M072-2-20260929-Lden` | `ex:prop-Lden` | lden | 43.9 | resultaten Ld, Le, Ln |

Alle indicatoren hebben FOI `ex:meetpost-M072` en eenheid `unit:DeciB_A`.

## 5. Procedure en ObservableProperty

| Procedure | Geïmplementeerd door | Gebruikt door | hasInput → hasOutput |
|---|---|---|---|
| `ex:procedure-eventmeting` | geluidsmeters | alle event- en dagcollecties | — → LAeq, LAmax, SEL, duur |
| `ex:procedure-energetische-sommatie` | rekenmodule | L24, Ld, Le, Ln, SEL (dag) | SEL → L24, Ld, Le, Ln, SEL |
| `ex:procedure-maximum` | rekenmodule | LAmax (dag) | LAmax → LAmax |
| `ex:procedure-energetisch-gemiddelde-eventduur` | rekenmodule | LAeq (dag) | SEL, duur → LAeq-vliegtuiggeluid |
| `ex:procedure-lden` | rekenmodule | Lden | Ld, Le, Ln → Lden |

`sosa:hasInput` verwijst naar de *eigenschap* waarvan de waarden de invoer vormen. Zo is elke
`sosa:hasInputValue` op een observatie (een resultaat van die eigenschap) consistent met een
`sosa:hasInput` van de procedure, zoals SOSA 2023 vraagt.

<!-- TODO: Hoe definieert Aerovision een geluidsevent (drempelniveau in dB(A), minimale duur, eventueel een dynamische drempel boven het achtergrondniveau)? Die parameters horen als rdfs:comment of als sosa:hasInput bij ex:procedure-eventmeting. -->

Eigenschappen (`sosa:Property`):

| Property | Betekenis |
|---|---|
| `ex:prop-LAeq` | Equivalent continu A-gewogen geluidsdrukniveau over de duur van het event |
| `ex:prop-LAmax` | Maximaal A-gewogen niveau binnen de phenomenonTime (event of dag) |
| `ex:prop-SEL` | Sound Exposure Level (LAE): het niveau van 1 s met dezelfde energie als het event of de som van de events |
| `ex:prop-duur` | Duur van het event |
| `ex:prop-L24`, `ex:prop-Ld`, `ex:prop-Le`, `ex:prop-Ln` | LAeq van vliegtuiggeluid over etmaal / dag (07–19) / avond (19–23) / nacht (23–07) |
| `ex:prop-Lden` | Dag-avond-nachtniveau, avond +5 dB, nacht +10 dB (Richtlijn 2002/49/EG) |
| `ex:prop-LAeq-vliegtuiggeluid` | LAeq over de cumulatieve duur van de vliegtuiggeluidevents (Aerovision-indicator "LAeq") |

## 6. Modelleer-keuzes toegelicht

### Waarom een plat model en geen drielaags architectuur?

> **Verworpen alternatief:** Planning (Plan met stappen *eventdetectie → vluchtcorrelatie →
> dagaggregatie*), Deployment, Execution met `p-plan:correspondsToStep`.
> **Gekozen aanpak:** plat model met geneste collecties en afgeleide observaties.
> **Motivatie:** R4 vraagt drielaags bij meerstapsprocessen *waarvan de stappen beschreven
> kunnen worden*. De export bevat enkel de uitkomsten. Over de stappen zelf (drempels,
> correlatievenster, uitsluitingen, kalibratie) staat er niets in, dus de Planning-laag zou
> volledig verzonnen zijn. Wat wél expliciet en controleerbaar is, is de afleiding van de
> dagindicatoren uit de events. Die is nagerekend: voor 11 van de 13 campagnes geeft
> 10·log10(Σ10^(SEL/10)/T) exact de geleverde L24, Ld, Le en Ln, en het maximum van de event-LAmax
> geeft exact de dag-LAmax. Die afleiding vangt R13 volledig op zonder drielaags model. Levert
> Aerovision later de verwerkingsparameters, dan is drielaags een logische volgende stap.

### Waarom het geluidsevent als `sosa:Stimulus`?

> **Verworpen alternatieven:** (a) het event als `sosa:FeatureOfInterest`; (b) de vlucht als FOI
> van de geluidsmetingen.
> **Gekozen aanpak:** `ex:geluidsevent-…` is een `sosa:Stimulus`. De eventcollectie verwijst er
> naar met `sosa:wasOriginatedBy`, en het event zelf met `sosa:isDetectedBy` naar de geluidsmeter.
> **Motivatie:** SOSA 2023 definieert een Stimulus als het reële voorval dat een sensor
> aanzet tot observeren. Een geluidsevent is precies dat: een drempeloverschrijding die een
> meting start. Het FOI blijft de meetpost, want daar wordt het geluidsniveau bepaald. Met de
> vlucht als FOI zou de *bron* verward worden met de *plaats waar het effect gemeten wordt*.

### Waarom de vlucht als `prov:Activity` en het event via `prov:wasGeneratedBy`?

> **Verworpen alternatief:** de vlucht als `sosa:FeatureOfInterest` met eigen
> radarobservaties (positie, afstand).
> **Gekozen aanpak:** `ex:vlucht-<ModeS>-<eersteplotUTC>` is een `prov:Activity` die een
> `ex:luchtvaartuig-<ModeS>` (`prov:Entity`) gebruikt (`prov:used`). Het geluidsevent is
> `prov:wasGeneratedBy` de vlucht.
> **Motivatie:** een vlucht is een activiteit in de tijd, en het geluid is iets wat die
> activiteit voortbrengt. PROV-O drukt die herkomst rechtstreeks uit. Het Mode S-adres (ICAO
> 24-bit) is de stabiele identificatie van het toestel. Callsign, herkomst/bestemming, baan en
> route staan in `dcterms:identifier` en `rdfs:comment`, omdat de geladen vocabularia daar geen
> eigen termen voor hebben.

<!-- TODO: De koppeling event → vlucht is zelf een resultaat van de Aerovision-correlatie (radarspoor ↔ geluidsevent). Moet die toewijzing als eigen observatie met procedure en betrouwbaarheid gemodelleerd worden, en welke regels gebruikt Aerovision (tijdvenster, maximale afstand)? -->

<!-- TODO: Moeten positie (X, Y, Z) en afstand van het toestel tot de meetpost op het moment van het event mee opgenomen worden? Dat zijn radarobservaties met als FOI het luchtvaartuig, niet de meetpost, dus ze passen niet in de eventcollectie. -->

### Waarom geneste `sosa:ObservationCollection`s?

> **Verworpen alternatief:** één collectie per dag met losse observaties, of per event vier
> losse observaties zonder collectie.
> **Gekozen aanpak:** dagcollectie ⊃ eventcollectie ⊃ 4 observaties.
> **Motivatie:** de vier waarden van een event delen interval, stimulus, sensor, procedure en
> FOI. De eventcollectie legt die één keer vast en maakt het event als eenheid opvraagbaar.
> De dagcollectie geeft de afgeleide indicatoren één `sosa:relatedObservation`-doel. SOSA 2023
> laat een collectie toe als lid van een collectie (`sosa:hasMember` range).

### Waarom `sosa:hasResult` met benoemde resultaten, en niet `sosa:hasSimpleResult`?

> **Verworpen alternatief:** `sosa:hasSimpleResult "62.97"^^xsd:decimal`.
> **Gekozen aanpak:** `sosa:Result` met `qudt:numericValue` en `qudt:hasUnit unit:DeciB_A`
> (of `unit:SEC`), met skolem-IRI `ex:resultaat-<obs-id>`.
> **Motivatie:** de eenheid moet expliciet zijn, en vooral: `sosa:hasInputValue` van de
> dagindicatoren moet naar de *waarde* van een event verwijzen. Dat kan enkel als die waarde een
> eigen IRI heeft (R3, R13).

### Waarom `sosa:hasInputValue` naar de event-resultaten en `sosa:relatedObservation` naar de dagcollectie?

> **Verworpen alternatief:** de dagindicatoren als `sosa:hasMember` in de dagcollectie, of
> `sosa:hasInputValue` naar de observaties.
> **Gekozen aanpak:** elke indicator verwijst met `sosa:hasInputValue` naar precies de
> resultaten die in de berekening zitten (bv. Ln → de SEL-resultaten van de 5 nachtevents) en
> met `sosa:relatedObservation` naar de dagcollectie. Lden verwijst naar de resultaten en
> observaties van Ld, Le en Ln.
> **Motivatie:** R7/R13. Een observatie is een activiteit, geen waarde, en een afgeleide
> indicator is geen lid van de bronreeks. Omdat de afleiding expliciet is, kan een afnemer ze
> met SPARQL narekenen.

**Afwijkingen bij de controle:** voor F041-1 en F045-1 wijken L24/Ld met 0,04–0,05 dB af en is
de geleverde aeronautische duur iets korter dan de som van de eventduren (8 042 s tegen 8 091 s,
7 257 s tegen 7 271 s). Dat wijst op events die gedeeltelijk buiten het etmaal vallen en daar
afgekapt worden. De `hasInputValue`-lijst bevat voor die campagnes het volledige event.

<!-- TODO: Bevestigen bij Aerovision dat events die de grens van 07:00 overschrijden pro rata worden meegeteld (verklaart de afwijking bij F041-1 en F045-1). -->

### Waarom aparte properties voor Ld, Le, Ln en L24?

> **Verworpen alternatief:** één `ex:prop-LAeq` voor alle indicatoren, met de referentieperiode
> enkel via `sosa:phenomenonTime` (L24 = LAeq over 24 u, Ld = LAeq over 07–19 u, …).
> **Gekozen aanpak:** een eigen `sosa:Property` per benoemde indicator. LAmax en SEL gebruiken
> wel dezelfde property op event- en dagniveau.
> **Motivatie:** Ld, Le, Ln en Lden zijn wettelijk gedefinieerde indicatoren (Richtlijn
> 2002/49/EG) waarop gebruikers rechtstreeks willen filteren. Lden en de Aerovision-"LAeq"
> (gemiddelde over de eventduur, geen aaneengesloten interval) zijn bovendien niet als gewone
> LAeq over een interval uit te drukken. Bij LAmax en SEL verandert de betekenis niet met de
> tijdsspanne, dus daar volstaat één property.

### Waarom `sosa:SpatialSample` voor de meetpost?

> **Verworpen alternatief:** de meetpost enkel als `sosa:Platform` en het gebied als FOI.
> **Gekozen aanpak:** drievoudige typering met `sosa:isSampleOf ex:omgeving-EBBR` (R11).
> **Motivatie:** geluid varieert sterk binnen het gebied. Een meting zegt iets over het punt,
> en via de bemonstering over het gebied. `sosa:hasFeatureOfInterest` wijst daarom naar de
> meetpost, niet naar het gebied.

### Waarom een `.ttl`-subset naast een `.trig`?

> **Verworpen alternatief:** alle 13 campagnes in één `.ttl`.
> **Gekozen aanpak:** `geluidsmeetnet.trig` (≈145 000 triples, uitgesloten van de pipeline) en
> `geluidsmeetnet.ttl` (campagne M072-2, de kleinste met 58 events) als gevalideerde subset.
> **Motivatie:** de volledige set maakt de OWL- en SHACL-validatie onwerkbaar traag. Beide
> bestanden komen uit hetzelfde script, dus de subset is representatief voor de structuur.

## 7. Tijdsmodellering

| Element | Patroon |
|---|---|
| Event (LAeq, SEL, duur, eventcollectie) | `sosa:phenomenonTime → time:Interval → hasBeginning/hasEnd → time:Instant → time:inXSDDateTimeStamp` |
| LAmax van een event | `sosa:phenomenonTime → time:Instant` (kolom *Maximum*: het moment van het maximum) |
| Dagindicatoren | gedeelde intervallen `ex:interval-20260929-{dag,D,E,N}` |

- **`time:inXSDDateTimeStamp`**: de bron bevat tijden met expliciete offset (`+02:00`), en de
  radarplots in UTC. Een tijdstempel met verplichte tijdzone voorkomt verwarring tussen beide.
- **Aerovision-etmaal**: het etmaal loopt van 07:00 tot 07:00 lokale tijd, niet van middernacht
  tot middernacht. Dag = 07–19, avond = 19–23, nacht = 23–07 (halfopen intervallen, R12).
- **LAmax op een Instant**: het maximum is een waarde *op* een tijdstip binnen het event. Het
  verschilt daarmee van het interval op de eventcollectie; de andere drie leden erven het
  interval.
- **`sosa:resultTime`** is niet opgenomen: de export zegt niet wanneer Aerovision de events en
  indicatoren beschikbaar maakte.
- **Instants** hebben skolem-IRI's op basis van het UTC-tijdstip (`ex:instant-20260929T232312Z`)
  en worden gedeeld wanneer twee events hetzelfde tijdstip raken.

<!-- TODO: Wanneer worden de event- en dagresultaten in Aerovision beschikbaar (real-time, na validatie, dag+1)? Dat bepaalt de sosa:resultTime. -->

## 8. Prefixen en IRI-structuur

| Prefix | Base URI | Tijdelijk of persistent |
|---|---|---|
| `sosa:` | `http://www.w3.org/ns/sosa/` | Persistent (W3C) |
| `prov:` | `http://www.w3.org/ns/prov#` | Persistent (W3C) |
| `time:` | `http://www.w3.org/2006/time#` | Persistent (W3C) |
| `qudt:` | `http://qudt.org/schema/qudt/` | Persistent (QUDT) |
| `unit:` | `http://qudt.org/vocab/unit/` | Persistent (QUDT) |
| `dcterms:` | `http://purl.org/dc/terms/` | Persistent (DCMI) |
| `xsd:`, `rdfs:` | W3C | Persistent |
| `ex:` | `https://example.org/geluidsmeetnet/` | Tijdelijk (illustratief) |

IRI-patronen (alle deterministisch, geen blank nodes):

| Resource | Patroon |
|---|---|
| Meetpost / campagne / meter | `ex:meetpost-M072`, `ex:campagne-M072-2`, `ex:geluidsmeter-M072-2` |
| Event, eventcollectie | `ex:geluidsevent-<campagne>-<startUTC>`, `ex:eventcollectie-<campagne>-<startUTC>` |
| Eventobservatie / resultaat | `ex:obs-<event-id>-<LAeq\|LAmax\|SEL\|duur>`, `ex:resultaat-<event-id>-…` |
| Dagindicator | `ex:obs-<campagne>-20260929-<indicator>` |
| Vlucht / luchtvaartuig | `ex:vlucht-<ModeS>-<eersteplotUTC>`, `ex:luchtvaartuig-<ModeS>` |
| Tijd | `ex:instant-<UTC>`, `ex:interval-<event-id>`, `ex:interval-20260929-<periode>` |

Voor productie hoort `ex:` vervangen te worden door een gezaghebbende basis-URI van de
meetnetbeheerder (R10).

## 9. Inverse relaties

| Relatie | Inverse | Opgenomen in | Doel |
|---|---|---|---|
| `sosa:hosts` | `sosa:isHostedBy` | meetpost ↔ meter | Sensoren per meetpost en omgekeerd |
| `sosa:hasSubSystem` | `sosa:isSubSystemOf` | meetnet ↔ meters, rekenmodule | Samenstelling van het meetnet |
| `sosa:deployedSystem` (campagne → meter) | `sosa:hasDeployment` (meter → campagne; inverse van `sosa:deployedAsset`) | campagne ↔ meter | Campagnes per meter en omgekeerd; de meetpost wijst met `sosa:inDeployment` naar de campagne |
| `sosa:hasSample` | `sosa:isSampleOf` | omgeving ↔ meetpost | Sampling-keten in beide richtingen |
| `sosa:hasFeatureOfInterest` | `sosa:isFeatureOfInterestOf` | meetpost → dagcollectie, omgeving → sampling | Vanuit de meetpost de meetreeksen vinden |
| `sosa:hasMember` | `sosa:isMemberOf` | dag- ↔ eventcollectie ↔ observatie | Van een meting naar haar event en dag |
| `sosa:hasResult` | `sosa:isResultOf` | observatie ↔ resultaat, sampling ↔ meetpost | Van een inputwaarde terug naar haar observatie |

`sosa:wasOriginatedBy` (eventcollectie → event) en `sosa:isDetectedBy` (event → meter) staan maar in
één richting, zonder `sosa:originated` of `sosa:detects`: per meter zijn er honderden events per
dag, en die vraag je op via de collecties.

<!-- TODO: Moet 20260929_EBBR_Aeronautic_ByDay.csv mee omgezet worden (aantal events totaal/gecorreleerd, NAx-tellingen per drempel, beschikbaarheid 'act')? De tellingen zijn afgeleide observaties uit dezelfde events; 'act' is eerder kwaliteitsinformatie (sosa:resultQuality). -->
