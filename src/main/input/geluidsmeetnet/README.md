# Geluidsmeetnet Brussels Airport — geluidsevents en dagindicatoren

## Bronbestand

Export uit **Aerovision** (het verwerkingsplatform van het geluidsmeetnet rond Brussels Airport,
ICAO-code EBBR) voor de meetdag **29 september 2026**, ontvangen als
`brondata/voorbeeld_aerovision_data_20260929.zip`. De zip bevat vier CSV-bestanden
(scheidingsteken `;`), die ook uitgepakt in `brondata/` staan:

| Bestand | Inhoud | Rijen |
|---|---|---|
| `20260929_EBBR_NoiseEvents.csv` | Geluidsevents per meetcampagne, gekoppeld aan een vlucht: start, einde, tijdstip maximum, duur, periode (D/E/N), LAeq, LAmax, SEL, vluchtgegevens, positie en afstand van het toestel | 1 818 |
| `20260929_EBBR_NoiseIndicators_Aeronautic_ByDay.csv` | Dagindicatoren vliegtuiggeluid per campagne (lang formaat): L24, Ld, Le, Ln, Lden, LAeq, LAmax, SEL | 104 |
| `20260929_EBBR_Aeronautic_ByDay.csv` | Dezelfde dagindicatoren in breed formaat, aangevuld met eventtellingen (alle/gecorreleerde events, drempeloverschrijdingen LAmax/SEL 45–100 dB, NAx) en beschikbaarheid | 13 |
| `20260929_EBBR_Flights.csv` | Radarsporen van vertrekkende en aankomende vluchten (callsign, Mode S, registratie, type, herkomst/bestemming, baan, route) | 627 |

`brondata/projectbeschrijving/geluidsmeetnet_luchthaven.xlsx` is de projectplanning van het
data-platformtraject; de taak "Omvormen tot SSN:SOSA model" is het vertrekpunt van dit voorbeeld.

De vier CSV's dekken 13 meetcampagnes (`F003-3`, `F040-2`, …, `M071-1`, `M072-2`).

## Transformatieproces

```
brondata/*.csv ──► scripts/geluidsmeetnet_to_rdf.py ──► geluidsmeetnet.trig  (alle 13 campagnes)
                                                    └─► geluidsmeetnet.ttl   (validatie-subset M072-2)
```

1. **Inlezen**: `NoiseEvents`, `NoiseIndicators_Aeronautic_ByDay` en `Flights`.
2. **Tijdstempels normaliseren**: de kolommen *Start/End/Maximum* hebben een expliciete offset
   (`+02:00`), *First plot/Last plot* in `NoiseEvents` staan zonder offset in UTC. Alles wordt
   omgezet naar `xsd:dateTimeStamp` in lokale tijd met offset.
3. **Vluchtkoppeling**: een event wordt aan een vlucht gekoppeld via (Mode S-adres, eerste
   radarplot in UTC). 1 811 van de 1 818 events vinden zo hun vlucht in `Flights`; de 7 overige
   vluchten (radarspoor vóór 07:00) worden opgebouwd uit de vluchtkolommen van `NoiseEvents`.
4. **Generatie**: één `.trig` met de volledige dataset (≈145 000 triples; Turtle-syntaxis, maar
   via de extensie uitgesloten van de pipeline) en één `.ttl` met campagne `M072-2` (58 events,
   ≈5 400 triples) als gevalideerde subset. De subset wordt gekozen met `VALIDATIE_CAMPAGNE` in
   het script.

`20260929_EBBR_Aeronautic_ByDay.csv` wordt (nog) niet omgezet: de indicatoren erin zijn identiek
aan die in `NoiseIndicators`; de eventtellingen en beschikbaarheid zijn een mogelijke uitbreiding
(zie `bespreking.md`).

## Mapping-keuzes

**Plat SSN/SOSA-model** met geneste `sosa:ObservationCollection`s en afgeleide observaties. Een
drielaags model (Planning/Deployment/Execution) is onderzocht maar niet gekozen: de export bevat
wel de *resultaten* van een meerstappenketen (eventdetectie → vluchtcorrelatie → dagaggregatie),
maar geen expliciete gegevens over de stappen zelf (detectiedrempels, correlatievenster,
uitsluitingsregels). Een plan zou dus volledig verzonnen zijn. Wat wél expliciet is, is de
rekenkundige afleiding van de dagindicatoren uit de events — die is voor alle 13 campagnes
nagerekend (op twee campagnes na exact; zie `bespreking.md` §6) en gemodelleerd met
`sosa:hasInputValue` (R13).

- **Meetpost** (`ex:meetpost-M072`): `sosa:Platform + sosa:FeatureOfInterest + sosa:SpatialSample`
  van `ex:omgeving-EBBR` (R11). De **meetcampagne** (`ex:campagne-M072-2`) is een
  `sosa:Deployment` van de **geluidsmeter** (`sosa:Sensor`) op die meetpost.
- **Geluidsevent** (`ex:geluidsevent-…`): een `sosa:Stimulus` — het reële voorval dat de meter
  triggert — gegenereerd door een **vlucht** (`prov:Activity`) die een **luchtvaartuig**
  (`prov:Entity`, geïdentificeerd door het Mode S-adres) gebruikt.
- Per event een `sosa:ObservationCollection` (`sosa:wasOriginatedBy` het event) met vier
  observaties: LAeq, LAmax, SEL en duur. Alle eventcollecties van een campagne zitten in één
  dagcollectie.
- **Dagindicatoren** (L24, Ld, Le, Ln, SEL, LAmax, LAeq, Lden) zijn afgeleide observaties van de
  **Aerovision-rekenmodule** (`sosa:Sensor`, software), buiten de collectie, met
  `sosa:hasInputValue` naar de event-resultaten en `sosa:relatedObservation` naar de dagcollectie.
  Lden is een afgeleide van afgeleiden: input Ld, Le en Ln.
- Resultaten als benoemde `sosa:Result` met `qudt:numericValue` + `qudt:hasUnit unit:DeciB_A`
  (of `unit:SEC` voor de duur) — één stijl (R3).

## Grafische voorstelling

Zie `geluidsmeetnet.mmd`. Het diagram toont één representatief event (het nachtelijke vertrek
BCS6TP om 01:23) en de afleiding van Ln en Lden; de overige 57 events zijn samengevat.

## Outputbestanden

- `geluidsmeetnet.ttl` — validatie-subset (campagne M072-2), door de pipeline verwerkt
- `geluidsmeetnet.trig` — volledige dataset (13 campagnes), niet door de pipeline verwerkt
- `src/main/output/turtle/geluidsmeetnet/geluidsmeetnet.ttl` — subset na inferentie

## Gebruik

```bash
cd src/main/input/geluidsmeetnet
python3 scripts/geluidsmeetnet_to_rdf.py      # genereert .ttl en .trig
cd ../../../..
mvn compile exec:java                         # validatie (vocabulaire, OWL, SHACL, JSON-LD)
```
