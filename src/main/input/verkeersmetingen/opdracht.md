# Modelleeroefening: Automatische fietstelpost

## Use case

### Context

Op fietsroute F1 in Antwerpen, naast de spoorweg tussen Antwerpen-Centraal en station Berchem, staat een vaste
automatische fietstelpost. Het meetpunt draagt de code **FMN-021** en is gelegen op de hoek
van de Mercatorstraat met de Van Den Nestlei (coördinaten: lat 51.20910, lon 4.423123).
Beheerder is de Provincie Antwerpen.

### Beschrijving van het systeem

De telpost bestaat uit één component:

- Een **automatische teller** die het tweerichtingsverkeer van lichte voertuigen detecteert
  en telt. Onder "lichte voertuigen" vallen fietsen, steps en motorfietsen.

De teller registreert continu. Elke periode van één uur wordt een absolute telling opgeslagen
(aantal voertuigen dat het meetpunt passeerde in dat uur). Naast de 24 uurtellingen wordt
ook een dagsom bijgehouden die de volledige dag samenvat.

De gebruikte detectiemethode is geautomatiseerd (inductielus of radarsensor); er is geen
menselijke tussenkomst bij de meting.

### Concrete meetgegevens

Dinsdag 28 april 2026 werden de volgende tellingen geregistreerd (selectie):

| Periode | Begin | Einde | Absolute telling |
|---|---|---|---|
| Dagsom | 28/04 00:00 | 29/04 00:00 | 2541 voertuigen |
| Uur 00:00 | 28/04 00:00 | 28/04 01:00 | 15 voertuigen |
| Uur 07:00 | 28/04 07:00 | 28/04 08:00 | 134 voertuigen |
| Uur 08:00 | 28/04 08:00 | 28/04 09:00 | 291 voertuigen *(ochtendspits)* |
| Uur 12:00 | 28/04 12:00 | 28/04 13:00 | 128 voertuigen |
| Uur 17:00 | 28/04 17:00 | 28/04 18:00 | 279 voertuigen *(avondspits)* |
| Uur 23:00 | 28/04 23:00 | 29/04 00:00 | 41 voertuigen |

De volledige dataset bevat 24 uurtellingen (00:00–23:00) voor dezelfde dag.

De dagsom (2541) is een **afgeleid gegeven**: ze is berekend op basis van de 24 uurtellingen,
niet rechtstreeks geregistreerd door de teller.

---

## Stap 1 — Identificeer de SOSA-concepten

*Individueel — 10 minuten*

Lees de use case en vul onderstaande tabel in. Gebruik de SOSA-klassen `Platform`,
`FeatureOfInterest`, `Sample`, `Sensor`, `ObservingProcedure`, `ObservableProperty`,
`Observation` en `ObservationCollection`.

| Vraag | Antwoord |
|---|---|
| Wat is het **platform** dat de sensor draagt? | |
| Wat is het **directe studieobject** van de metingen? | |
| Wat is het **bredere studieobject** waarvan het meetpunt een deelmonster is? | |
| Welke **sensor** produceert de observaties? | |
| Wat is de **observeerbare eigenschap**? | |
| Hoeveel **observaties** bevat de dataset voor 28 april 2026? | |
| Waarom is een `ObservationCollection` hier zinvol? | |
| Wat is de relatie tussen de **dagsom** en de 24 uurtellingen? | |

---

## Stap 2 — Schets een diagram

*In groepjes van 2 — 15 minuten*

Teken een diagram met de volgende drie zones:

- **PROCEDURE** — de telmethode en de observeerbare eigenschap
- **INFRASTRUCTUUR** — het meetpunt, de teller en de fietsroute
- **WAARNEMING** — de collectie en de individuele observaties

Gebruik pijlen om relaties te tonen en label elke pijl met de bijhorende property
(bijv. `sosa:madeBySensor`, `sosa:hasMember`).

Beantwoord bij het tekenen:

- Het meetpunt is tegelijk platform, studieobject én ruimtelijk monster. Welke drie
  SOSA-klassen ken je er dan aan toe? Welke extra property legt de band met de fietsroute?
- Een telling beslaat een periode, geen puntmoment. Welk OWL-Time-concept gebruik je voor
  `sosa:phenomenonTime`?
- De dagsom is afgeleid van de uurtellingen. Staat ze als gewoon lid in de collectie, of
  heeft ze een andere relatie? Welke properties gebruik je?

---

## Stap 3 — Schrijf de Turtle

*Individueel of in groepjes — 20 minuten*

Schrijf een Turtle-bestand met minstens:

1. Het meetpunt met drievoudige typering en de `sosa:isSampleOf`-koppeling aan de fietsroute
2. De teller met `sosa:implements` en `sosa:observes`
3. Een `sosa:ObservationCollection` met de gedeelde metadata op collectieniveau
4. Drie volledige uurobservaties (kies zelf welke) met `sosa:phenomenonTime` als
   `time:Interval` (half-open interval: begin inclusief, einde exclusief)
5. De dagobservatie als afgeleid gegeven met de juiste koppeling aan de collectie

Gebruik `https://example.org/verkeersmetingen/` als basis-IRI.

---

## Stap 4 — Plenaire bespreking

*Plenair — 15 minuten*

1. Het meetpunt heeft drie SOSA-typeringen: `sosa:Platform`, `sosa:FeatureOfInterest` en
   `sosa:SpatialSample`. Wat voegt elke typering toe? Welke property koppelt het meetpunt
   aan de fietsroute, en waarom is dat semantisch nauwkeuriger dan de fietsroute direct als
   `hasFeatureOfInterest` op de collectie te zetten?
2. Waarom gebruik je `time:Interval` met `time:hasBeginning` en `time:hasEnd` in plaats van
   een eenvoudige `time:Instant`? Wat is het verschil tussen `sosa:phenomenonTime` en
   `sosa:resultTime` in dit voorbeeld?
3. De dagsom is berekend uit de 24 uurtellingen. Hoe modelleer je die afhankelijkheid?
   Welke properties gebruik je, en waarom staat de dagsom **niet** als `sosa:hasMember` in
   de collectie?
4. Wanneer kies je voor `sosa:hasSimpleResult` en wanneer voor `sosa:hasResult` met een
   apart `qudt:QuantityValue`-object? Wat zou je hier anders doen als de eenheid
   (voertuigen/uur vs voertuigen/dag) extern gerefereerd moet worden?

---

*Referentieoplossing: `verkeersmetingen.ttl` en `verkeersmetingen.mmd`*
