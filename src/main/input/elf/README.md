# ELF-meetnet — laagfrequente magnetische velden

## Context

Het Departement Omgeving bouwt een meetnet voor de blootstelling van burgers aan laagfrequente
magnetische velden van hoogspanningsverbindingen en -stations (380, 150 en 70 kV). Dat gebeurt in
uitvoering van het besluit van de Vlaamse Regering van 29 maart 2024 over de oprichting van een
monitoringsnetwerk. Artikel 10 vraagt de meetgegevens en de simulaties van het rekenmodel te
publiceren, onafhankelijk van de netbeheerders. Volgens de business case van het project (*IMPL –
ELF-magnetische veldmetingen aan transmissielijnen, realisatie sensor roadmap 2026*) loopt de keten
als volgt:

- **Sensoren** sturen hun metingen via MQTTS naar ThingsBoard.
- **Registratie:** een enquêtetool en Jira beheren de sensoren en hun plaatsing, met assetbeheer.
- **Dataplatform:** de dataingest brengt meetdata en registratie naar het dataplatform, waar ze naar
  SSN/SOSA getransformeerd worden.
- **Publieke webapp:** een kaart met de hoogspanningstrajecten en de sensoren. Per sensor: de actuele
  waarde, het minimum en maximum per dag, week, maand en jaar, en de jaargemiddelde blootstelling,
  met de stroombelasting als mogelijke duiding.

Dit voorbeeld is een eerste mapping van die gegevens naar SSN/SOSA. De business case zelf zit niet
in de repository: ze bevat namen van medewerkers.

## Bronbestanden

Twee bestanden in `source/`:

| Bestand | Inhoud | Omvang |
|---|---|---|
| `elf_sensors_registratie.csv` | Export uit Jira (project SENS): één ticket per meetcampagne, met de sensor (titel, bv. `ELF_C_0020`), het adres (straat, huisnummer, postcode, gemeente), de start- en einddatum van de metingen, contactpersoon en status | 15 tickets, 14 sensoren (12 `ELF_C_…`, 2 `ELF_L_…`), 13 adressen |
| `_meetperiode_SENS-269_ELF_C_0020_Duisterwijk.parquet` | Telemetrie uit ThingsBoard van ELF-node `ELF_C_0020` tijdens campagne SENS-269 (Obscurionweg 91, Duisterwijk), van 26/11/2025 09:00 tot 26/01/2026 09:00 UTC, in sleutel-waardevorm: één rij per tijdstip en sleutel | 1 001 452 rijen |

**Gepseudonimiseerd.** Beide bestanden zijn bewerkt met `scripts/anonimiseer.py`, met namen uit
De Rode Ridder. Gemeenten (`Duisterwijk`), straten (`Obscurionweg`), postcodes, namen en
e-mailadressen van contactpersonen (`…@graalburcht.example`) zijn fictief. Ook de gemeente in de
kolom `meetperiode` en in de naam van de parquet is vervangen. De afbeelding volgt uit een hash van de
echte waarde: dezelfde gemeente krijgt in de CSV en in de parquet dezelfde fictieve naam. Er wordt
geen sleutel bewaard. Huisnummers, sensor-ID's, Jira-sleutels, datums en meetwaarden zijn
ongewijzigd.

**Niet in de bron, en dus fictief in dit voorbeeld:** de koppeling van een meetlocatie aan een
hoogspanningsverbinding of -station, en de coördinaten van de meetlocaties. Het conversiescript
leidt beide deterministisch af uit de gepseudonimiseerde waarden: één bron per gemeente en een punt in
Lambert 72 per adres.

De telemetrie bevat dertien sleutels:

| Sleutels | Aard | Frequentie | Omgezet |
|---|---|---|---|
| `RMStotal`, `Xpeak_low`, `Ypeak_low`, `Zpeak_low`, `Xpeak_high`, `Ypeak_high`, `Zpeak_high` | meetwaarden (`dbl_v`) | ongeveer elke minuut, 82 748 meetmomenten | ja |
| `lastConnectTime`, `lastActivityTime`, `lastDisconnectTime`, `lastInactivityAlarmTime`, `inactivityTimeout` | verbindingsstatus van het apparaat (`long_v`, epoch-ms) | bij elk bericht | nee |
| `active` | apparaat actief of niet (`bool_v`) | 466 wijzigingen | nee |

De bron vermeldt **geen eenheid**. Dit voorbeeld neemt microtesla (µT) aan, de gebruikelijke eenheid
voor de magnetische fluxdichtheid van laagfrequente velden; zie `bespreking.md` §6.

## Transformatie

```
(echte export) ─► scripts/anonimiseer.py --apply ─► source/  (eenmalig, al gebeurd)

source/elf_sensors_registratie.csv ─┐
source/_meetperiode_…parquet ───────┴► scripts/elf_to_rdf.py ─► elf.trig  (één dag, alle campagnes)
                                                             └► elf.ttl   (één uur, drie campagnes)
```

1. **Registratie inlezen.** Per ticket een meetcampagne; de datums (`26/nov/25 12:00 AM`) worden
   middernacht lokale tijd (`Europe/Brussels`, R12). Contactpersoon, naam en voornaam worden **niet**
   overgenomen (persoonsgegevens). Het label `offline` en de Jira-status ook niet.
2. **Bron en geometrie afleiden** (fictief): per gemeente een verbinding of station met een
   spanningsniveau, per adres een punt in Lambert 72.
3. **Telemetrie inlezen**, de zeven meetsleutels selecteren en per tijdstip één rij maken (er zijn
   geen dubbele tijdstippen per sleutel en geen ontbrekende waarden).
4. **Groeperen per lokaal uur.** Per uur een collectie met sensor, procedure en studieobject; per
   meetmoment een collectie met het resultaattijdstip en zeven observaties.
5. **Indicatoren berekenen** van `RMStotal`, als afgeleide waarnemingen (R13): per uur het minimum,
   het maximum en het gemiddelde uit de minuutwaarden; per dag dezelfde drie uit de uurindicatoren.
   Ze staan niet in de bron. Het script berekent ze en is daarom zelf de `sosa:Sensor`; in productie
   is dat het dataplatform.
6. **Schrijven.** `elf.trig` bevat de lokale dag `VOLLEDIGE_DAG` (27/11/2025: 1 354 meetmomenten,
   72 uur- en 3 dagindicatoren, ≈86 000 triples, 4,8 MB) en alle 15 meetcampagnes. De volledige
   meetperiode van twee maanden zou ≈250 MB Turtle geven; de parquet in `source/` blijft de volledige
   bron. `elf.ttl` bevat het uur `VALIDATIE_UUR` (27/11/2025 10:00–11:00, 60 meetmomenten, 3
   uurindicatoren, ≈4 200 triples) en de campagnes SENS-269, SENS-270 en SENS-229.

## Mappingkeuzes

**Plat model** (R4): één sensortype, één meetprocedure, geen meerstappenproces dat in de bron
beschreven staat. De lezing is die van een **immissie op een plaats**, zoals het vliegtuiggeluid in
`geluidsmeetnet/`: de vraag is de blootstelling van burgers waar de meter staat.

- **Bron** (`ex:verbinding-duisterwijk`, `ex:station-bloedhoven`): `sosa:FeatureOfInterest` met de
  eigenschap stroombelasting. **Omgeving** (`ex:omgeving-verbinding-duisterwijk`):
  `sosa:FeatureOfInterest`, met `prov:wasInfluencedBy` naar de bron.
- **Meetlocatie** (`ex:meetlocatie-6839-obscurionweg-91`): `sosa:Platform`, `sosa:FeatureOfInterest`
  en `sosa:SpatialSample` van de omgeving (R11), resultaat van een `sosa:Sampling`. Het adres staat erbij
  als `prov:Location` (`prov:atLocation`), de positie als `geo:Geometry` in Lambert 72
  (`geo:hasGeometry`).
- **Sensor** (`ex:sensor-ELF_C_0020`): `sosa:Sensor`. Hij staat niet vast op één plaats:
  `ELF_C_0025` stond eerst in Bloedhoven (SENS-229) en daarna in Duisterwijk (SENS-270).
- **Meetcampagne** (`ex:meetcampagne-SENS-269`): `sosa:Deployment` van de sensor op de meetlocatie,
  met de omgeving van de bron als `sosa:hasUltimateFeatureOfInterest`, en `prov:startedAtTime` en
  `prov:endedAtTime`. In Duisterwijk staan twee sensoren tegelijk op hetzelfde adres (SENS-269 en
  SENS-270).
- **Zeven eigenschappen** (`ex:prop-RMStotal`, `ex:prop-Xpeak_low`, …), elk `sosa:Property` met
  `qudt:hasQuantityKind quantitykind:MagneticFluxDensity`.
- **Observaties**: per meetmoment een `sosa:ObservationCollection` met `sosa:resultTime` (UTC, zoals
  ThingsBoard het geeft), met zeven `sosa:Observation`s. Elke observatie heeft een `qudt:QuantityValue`
  in `unit:MicroT` met een skolem-IRI (R3, R10).
- **Indicatoren**: afgeleide `sosa:Observation`s buiten de collecties (R7, R13), met een
  `time:Interval` van een lokaal uur of een lokale dag als `sosa:phenomenonTime` (R12). Een
  uurindicator gebruikt de minuutresultaten als `sosa:hasInputValue`, een dagindicator de
  uurindicatoren: een afgeleide van afgeleiden, zoals Lden in `geluidsmeetnet/`.

## Diagram

`elf.mmd` toont de bron en haar omgeving, de meetlocatie met adres en geometrie, de meetcampagnes,
één meetmoment met zijn zeven observaties, en de uur- en dagindicatoren.

## Outputbestanden

- `elf.ttl`: validatiesubset, verwerkt door de bulkvalidatie
- `elf.trig`: één volledige dag met alle meetcampagnes, niet verwerkt door de bulkvalidatie (§4 van
  `CLAUDE.md`)

## Gebruik

```bash
cd src/main/input/elf
pip install pandas pyarrow          # eenmalig, bij voorkeur in een virtuele omgeving
python3 scripts/elf_to_rdf.py       # genereert elf.ttl en elf.trig
```

Valideren: `mcp__ld-vocab__validate_file` op `src/main/input/elf/elf.ttl`, of alle voorbeelden
samen met het commando in §5 van `CLAUDE.md`. De `.trig` kan je apart valideren met hetzelfde commando,
met `--extensions trig src/main/input/elf`.
