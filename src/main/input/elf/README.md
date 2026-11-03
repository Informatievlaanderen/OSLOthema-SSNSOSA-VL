# ELF-meetnet — laagfrequente magnetische velden

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
2. **Telemetrie inlezen**, de zeven meetsleutels selecteren en per tijdstip één rij maken (er zijn
   geen dubbele tijdstippen per sleutel en geen ontbrekende waarden).
3. **Groeperen per lokaal uur.** Per uur een collectie met sensor, procedure en studieobject; per
   meetmoment een collectie met het resultaattijdstip en zeven observaties.
4. **Uurgemiddelde berekenen** van `RMStotal`: een afgeleide waarneming (R13). Het uurgemiddelde
   staat niet in de bron; het script berekent het en is daarom zelf de `sosa:Sensor`.
5. **Schrijven.** `elf.trig` bevat de lokale dag `VOLLEDIGE_DAG` (27/11/2025: 1 354 meetmomenten,
   ≈84 000 triples, 4,4 MB) en alle 15 meetcampagnes. De volledige meetperiode van twee maanden zou
   ≈250 MB Turtle geven; de parquet in `source/` blijft de volledige bron. `elf.ttl` bevat het uur
   `VALIDATIE_UUR` (27/11/2025 10:00–11:00, 60 meetmomenten, ≈3 800 triples) en de campagnes
   SENS-269, SENS-270 en SENS-229.

## Mappingkeuzes

**Plat model** (R4): één sensortype, één procedure, geen meerstappenproces dat in de bron
beschreven staat.

- **Sensor** (`ex:sensor-ELF_C_0020`): `sosa:Sensor`. Hij staat niet vast op één plaats:
  `ELF_C_0025` stond eerst in Bloedhoven (SENS-229) en daarna in Duisterwijk (SENS-270).
- **Meetlocatie** (`ex:meetlocatie-6839-obscurionweg-91`): `sosa:Platform` en
  `sosa:FeatureOfInterest`, met het adres als `prov:Location` (`prov:atLocation`). De bron heeft
  geen coördinaten.
- **Meetcampagne** (`ex:meetcampagne-SENS-269`): `sosa:Deployment` van de sensor op de meetlocatie,
  met `prov:startedAtTime` en `prov:endedAtTime`. In Duisterwijk staan twee sensoren tegelijk op
  hetzelfde adres (SENS-269 en SENS-270).
- **Zeven eigenschappen** (`ex:prop-RMStotal`, `ex:prop-Xpeak_low`, …), elk `sosa:Property` met
  `qudt:hasQuantityKind quantitykind:MagneticFluxDensity`.
- **Observaties**: per meetmoment een `sosa:ObservationCollection` met `sosa:resultTime` (UTC, zoals
  ThingsBoard het geeft), met zeven `sosa:Observation`s. Elke observatie heeft een `qudt:QuantityValue`
  in `unit:MicroT` met een skolem-IRI (R3, R10).
- **Uurgemiddelde**: afgeleide `sosa:Observation` buiten de collecties, met `sosa:hasInputValue` naar
  de 60 RMStotal-resultaten, `sosa:relatedObservation` naar de 60 RMStotal-observaties en een
  `time:Interval` van een lokaal uur als `sosa:phenomenonTime` (R7, R12, R13).

## Diagram

`elf.mmd` toont de infrastructuur, de meetcampagnes, één meetmoment met zijn zeven observaties en
het uurgemiddelde.

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
