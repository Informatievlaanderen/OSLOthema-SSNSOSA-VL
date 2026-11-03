# Modelleeroefening: ELF-meetnet

## Use case

### Context

Een overheidsdienst meet het laagfrequente magnetische veld (ELF, *extremely low frequency*) op
adressen in Vlaanderen, bijvoorbeeld bij een woning naast een elektrische installatie. Een draagbare
meter wordt voor enkele weken of maanden op een adres geplaatst en stuurt elke minuut zijn
meetwaarden naar een IoT-platform. Elke plaatsing wordt geregistreerd als ticket, met de meter, het
adres en de periode.

### Beschrijving van het systeem

| Onderdeel | Kenmerken |
|---|---|
| Meter `ELF_C_0020` | driedimensionale magnetometer; stuurt elke minuut een bericht met zeven waarden |
| Meter `ELF_C_0025` | hetzelfde type; stond eerst in Bloedhoven (28/04–10/09/2025), daarna in Duisterwijk |
| Adres | Obscurionweg 91, 6839 Duisterwijk (geen coördinaten gekend) |
| Ticket SENS-269 | `ELF_C_0020` op het adres in Duisterwijk, 26/11/2025 – 26/01/2026 |
| Ticket SENS-270 | `ELF_C_0025` op hetzelfde adres, zelfde periode |
| Bericht | tijdstempel in UTC; `RMStotal` en per as (X, Y, Z) een waarde `peak_low` en `peak_high`; daarnaast statusvelden (`active`, `lastConnectTime`, …) |

### Concrete metingen

De eerste drie berichten van `ELF_C_0020` na 10:00 lokale tijd op 27/11/2025 (waarden in µT):

| Tijdstempel (UTC) | RMStotal | Xpeak_low | Ypeak_low | Zpeak_low | Xpeak_high | Ypeak_high | Zpeak_high |
|---|---|---|---|---|---|---|---|
| 2025-11-27T09:00:49.427Z | 0.68249 | 0.20027 | 0.11435 | 0.50101 | -0.17789 | -0.29618 | 0.20453 |
| 2025-11-27T09:01:49.598Z | 0.66268 | 0.19813 | 0.10800 | 0.48567 | -0.17789 | -0.31147 | 0.17446 |
| 2025-11-27T09:02:49.815Z | 0.68142 | 0.20027 | 0.11012 | 0.50101 | -0.17789 | -0.29618 | 0.20453 |

Elk bericht bevat daarnaast statusvelden, bv. `active = true` en `inactivityTimeout = 600000`.

Gevraagd: de drie berichten en het **uurgemiddelde** van RMStotal tussen 10:00 en 11:00 lokale tijd
(0.67729 µT, berekend uit 60 berichten).

---

## Stap 1 — Identificeer de SOSA-concepten

*Individueel — 10 minuten*

| Vraag | Jouw antwoord (SOSA 2023-klasse of -eigenschap) |
|---|---|
| Wat is het studieobject (*feature of interest*)? Het adres, de meter, of het magnetische veld? | |
| Welke rol speelt de meter: `Sensor`, `Platform` of `System`? | |
| Hoe leg je vast dat `ELF_C_0025` eerst in Bloedhoven en daarna in Duisterwijk stond? | |
| Wat is een ticket zoals SENS-269 in SOSA-termen? | |
| Hoeveel `Property`'s heeft één bericht, en welke `quantitykind` hebben ze? | |
| Is `active` een waarneming van het studieobject? | |
| Wie of wat is de sensor van het uurgemiddelde? | |
| Kies je voor de minuutwaarden `phenomenonTime`, `resultTime` of beide? | |

Beschikbare klassen: `sosa:Sensor`, `sosa:Platform`, `sosa:FeatureOfInterest`, `sosa:Deployment`,
`sosa:Observation`, `sosa:ObservationCollection`, `sosa:ObservingProcedure`, `sosa:Property`,
`sosa:SpatialSample`, `qudt:QuantityValue`, `time:Interval`, `time:Instant`, `prov:Location`.

## Stap 2 — Schets een diagram

*In paren — 15 minuten*

Teken drie blokken: **PROCEDURE**, **INFRASTRUCTUUR** en **WAARNEMING**. Zet daarin de twee meters,
het adres, de twee tickets, één bericht met zijn observaties en het uurgemiddelde.

Sturende vragen:
1. Staat de meter met `sosa:hosts` op het adres, of loopt de koppeling via iets anders? Wat gaat er
   mis met `sosa:hosts` voor `ELF_C_0025`?
2. Wat delen de zeven waarden van één bericht, en wat delen alle berichten van een uur? Waar zet je
   dat gedeelde?
3. Waar wijst `sosa:hasInputValue` van het uurgemiddelde naartoe: naar de observaties, de collectie
   of de resultaten?

## Stap 3 — Schrijf de Turtle

*Individueel of in groep — 20 minuten*

Basis-IRI: `https://example.org/elf/`. Minimale eisen:

1. De meter `ELF_C_0020` als `sosa:Sensor` en het adres als meetlocatie, met de juiste typering.
2. Ticket SENS-269 als `sosa:Deployment`, met systeem, platform, studieobject en begin- en
   eindtijdstip (lokale tijd met tijdzone).
3. Minstens `ex:prop-RMStotal` en `ex:prop-Xpeak_low` als `sosa:Property`.
4. Eén bericht als `sosa:ObservationCollection` met `sosa:resultTime`, en daarin minstens de
   observaties voor RMStotal en Xpeak_low.
5. Resultaten als `qudt:QuantityValue` met `qudt:numericValue` en `qudt:hasUnit` (zoek de QUDT-eenheid
   voor microtesla op).
6. Het uurgemiddelde als afgeleide waarneming, met `sosa:hasInputValue`,
   `sosa:relatedObservation` en een `sosa:phenomenonTime` als `time:Interval`.
7. Geen statusvelden als observatie.

Valideer je bestand met `validate_file`.

## Stap 4 — Plenaire bespreking

*Plenair — 15 minuten*

1. Het studieobject is de meetlocatie, geen ruimtelijk monster. Wat zou je extra moeten weten om er
   een `sosa:SpatialSample` van te maken, en van welk groter object?
2. De bron vermeldt geen eenheid. Mag je µT aannemen? Waar documenteer je die aanname, en wat als ze
   fout blijkt?
3. In de data geldt `RMStotal = 1,2374 × √(Xpeak_low² + Ypeak_low² + Zpeak_low²)`. Is RMStotal dan
   een afgeleide waarneming? Wat pleit ervoor en wat ertegen?
4. Een RMS-waarde geldt over een meetvenster. Waarom is een `time:Instant` als `phenomenonTime` dan
   fout, en wat doe je als de duur van het venster niet gekend is?
5. Het uurgemiddelde staat niet in de bron. Wat moet je in het model vastleggen om eerlijk te zijn
   over de herkomst ervan?

---

*Referentieoplossing: `elf.ttl` en `elf.mmd`*
