# Modelleeroefening: ELF-meetnet

## Use case

### Context

De Vlaamse overheid meet de blootstelling van burgers aan het laagfrequente magnetische veld (ELF,
*extremely low frequency*) van hoogspanningsverbindingen en -stations. Een meter wordt voor enkele
weken of maanden op een adres in de buurt van een verbinding of station geplaatst en stuurt elke
minuut zijn meetwaarden naar een IoT-platform. Elke plaatsing wordt geregistreerd als ticket, met de
meter, het adres en de periode. Een publieke webapp toont per meter onder meer het minimum, het
maximum en het gemiddelde per dag.

### Beschrijving van het systeem

| Onderdeel | Kenmerken |
|---|---|
| Bron | een 150 kV-verbinding bij Duisterwijk |
| Meter `ELF_C_0020` | driedimensionale magnetometer; stuurt elke minuut een bericht met zeven waarden |
| Meter `ELF_C_0025` | hetzelfde type; stond eerst in Bloedhoven (28/04–10/09/2025), daarna in Duisterwijk |
| Adres | Obscurionweg 91, 6839 Duisterwijk; geocodering geeft het punt (81177, 208128) in Lambert 72 |
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

Gevraagd: de drie berichten en de **uurindicatoren** van RMStotal tussen 10:00 en 11:00 lokale tijd,
berekend uit 60 berichten: minimum 0.58806 µT, maximum 0.77332 µT, gemiddelde 0.67729 µT.

---

## Stap 1 — Identificeer de SOSA-concepten

*Individueel — 10 minuten*

| Vraag | Jouw antwoord (SOSA 2023-klasse of -eigenschap) |
|---|---|
| Wat is het studieobject (*feature of interest*) van de minuutwaarden: de verbinding, het adres, de meter of de plaats waar de meter staat? | |
| Welke rol(len) speelt de plaats waar de meter staat? | |
| Welke rol speelt de 150 kV-verbinding, en welke eigenschap heeft zij zelf? | |
| Hoe leg je vast dat `ELF_C_0025` eerst in Bloedhoven en daarna in Duisterwijk stond? | |
| Wat is een ticket zoals SENS-269 in SOSA-termen? | |
| Is `active` een waarneming van het studieobject? | |
| Wie of wat is de sensor van de uurindicatoren? | |
| Kies je voor de minuutwaarden `phenomenonTime`, `resultTime` of beide? | |

Beschikbare klassen: `sosa:Sensor`, `sosa:Platform`, `sosa:FeatureOfInterest`, `sosa:SpatialSample`,
`sosa:Sampling`, `sosa:Deployment`, `sosa:Observation`, `sosa:ObservationCollection`,
`sosa:ObservingProcedure`, `sosa:Property`, `qudt:QuantityValue`, `time:Interval`, `time:Instant`,
`prov:Location`, `geo:Geometry`.

## Stap 2 — Schets een diagram

*In paren — 15 minuten*

Teken drie blokken: **PROCEDURE**, **INFRASTRUCTUUR** en **WAARNEMING**. Zet daarin de verbinding,
de meetlocatie met adres en geometrie, de twee meters, de twee tickets, één bericht met zijn
observaties en de drie uurindicatoren.

Sturende vragen:
1. Vergelijk met het telpunt op een fietsroute (`verkeersmetingen`) en de geluidsmeetpost bij een
   luchthaven (`geluidsmeetnet`). Is de meetlocatie een monster van de verbinding, of van iets anders?
2. Staat de meter met `sosa:hosts` op de meetlocatie, of loopt de koppeling via iets anders? Wat gaat
   er mis met `sosa:hosts` voor `ELF_C_0025`?
3. Waar wijst `sosa:hasInputValue` van een uurindicator naartoe: naar de observaties, de collectie of
   de resultaten? En die van een dagindicator?

## Stap 3 — Schrijf de Turtle

*Individueel of in groep — 20 minuten*

Basis-IRI: `https://example.org/elf/`. Minimale eisen:

1. De verbinding, haar omgeving en de meetlocatie als ruimtelijk monster van die omgeving, met
   `prov:atLocation` naar het adres en `geo:hasGeometry` naar het punt (met de CRS-IRI van Lambert 72
   in de `geo:wktLiteral`).
2. De meter `ELF_C_0020` als `sosa:Sensor`, en ticket SENS-269 als `sosa:Deployment` met systeem,
   platform, studieobject en begin- en eindtijdstip (lokale tijd met tijdzone).
3. Minstens `ex:prop-RMStotal` en `ex:prop-Xpeak_low` als `sosa:Property`.
4. Eén bericht als `sosa:ObservationCollection` met `sosa:resultTime`, en daarin minstens de
   observaties voor RMStotal en Xpeak_low.
5. Resultaten als `qudt:QuantityValue` met `qudt:numericValue` en `qudt:hasUnit` (zoek de QUDT-eenheid
   voor microtesla op).
6. Het uurmaximum als afgeleide waarneming, met `sosa:hasInputValue`, `sosa:relatedObservation` en
   een `sosa:phenomenonTime` als `time:Interval`.
7. Geen statusvelden als observatie.

Valideer je bestand met `validate_file`.

## Stap 4 — Plenaire bespreking

*Plenair — 15 minuten*

1. Een telpunt staat voor een stuk fietsroute. Waarom staat een ELF-meting niet voor een stuk
   hoogspanningslijn, en welke grootheid doet dat wel? Wat betekent dat voor het rekenmodel dat het
   veld langs de hele lijn berekent?
2. Het adres geeft een punt via geocodering. Hoe nauwkeurig is dat punt voor een veld dat snel afneemt
   met de afstand? Wat leg je vast over de herkomst van de geometrie, en wat mag publiek getoond
   worden?
3. De bron vermeldt geen eenheid. Mag je µT aannemen? Waar documenteer je die aanname, en wat als ze
   fout blijkt?
4. Het daggemiddelde kan je berekenen uit de minuutwaarden of uit de uurgemiddelden. Wanneer verschillen
   die twee, en welke is het eerlijkste als er minuten ontbreken?
5. In de data geldt `RMStotal = 1,2374 × √(Xpeak_low² + Ypeak_low² + Zpeak_low²)`. Is RMStotal dan
   een afgeleide waarneming? Wat pleit ervoor en wat ertegen?

---

*Referentieoplossing: `elf.ttl` en `elf.mmd`*
