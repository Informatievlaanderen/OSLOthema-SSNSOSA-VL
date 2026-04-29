# Modelleeroefening: Erosiepoel Mechelen

## Use case

### Context

Stad Mechelen beheert op haar grondgebied een aantal **erosiepoelen**: retentiebekkens die
erosiemateriaal (slib, modder) opvangen dat tijdens regenepisodes van omliggende percelen
afspoelt. Na elke significante neerslagepisode controleert een veldwaarnemer de
vullingsgraad van de poel. Op basis van die metingen beslist de dienst Groenbeheer of een
ruimingsoperatie noodzakelijk is.

### Beschrijving van het systeem

De erosiepoel aan de Mechelse ringweg heeft volgende afmetingen en kenmerken:

| Eigenschap | Waarde |
|---|---|
| Afmetingen | 10 m × 5 m × 5 m |
| Maximaal volume | 250.000 liter |
| Beheerder | Stad Mechelen |

De veldwaarnemer (aangeduid als **Waarnemer X**) voert ter plaatse een visuele schatting
uit van het sedimentvolume. Er is geen elektronische sensor: de meting is volledig manueel,
gebaseerd op een gestandaardiseerde **visuele veldmeetprocedure** (peilmarkering aan de
wand, vuistregels voor dichtheid).

### Concrete meetgegevens

Op 1 september 2024, na een nachtelijke regenbui, voert Waarnemer X 's ochtends een
controle uit:

| Tijdstip | Gemeten sedimentvolume | Opmerking |
|---|---|---|
| 2024-09-01 09:00 | **245.000 liter** | Bijna volledige capaciteit bereikt |

De meting wordt onmiddellijk geregistreerd. Het resultaat wordt gebruikt om een
spoedruiming te plannen.

---

## Stap 1 — Identificeer de SOSA-concepten

*Individueel — 10 minuten*

Lees de use case en vul onderstaande vragen in. Geef waar van toepassing de bijbehorende klasse aan en maak hierbij gebruik van de volgende SOSA-klassen `Platform`,
`FeatureOfInterest`, `Sensor`, `System`, `ObservingProcedure`, `ObservableProperty`,
`Observation` en `Result`.

| Vraag                                                  | Antwoord | Klasse |
|--------------------------------------------------------|---|--------|
| Wat is het **geobserveerde object**?                   | |        |
| Wat is het **geobserveerde kenmerk**?                  | |        |
| Welk **systeem** doet de observatie?                   | |        |
| Welke **procedure** volgt de waarnemer?                | |        |
| Wat is het **resultaat** van de observatie?            | |        |
| Hoeveel **observaties** zijn er in deze dataset?       | |        |
| Kan de erosiepoel ook als `Platform` fungeren? Waarom? | |        |


---

## Stap 2 — Schets een diagram

*In groepjes van 2 — 15 minuten*

Teken een diagram met de volgende drie zones:

- **PROCEDURE** — procedure en observeerbare eigenschap
- **INFRASTRUCTUUR** — platform, feature of interest, sensor
- **WAARNEMING** — observatie, resultaat, tijdstip

Gebruik pijlen om relaties te tonen en label elke pijl met de bijhorende property.
(bijv. `sosa:hasFeatureOfInterest`, `sosa:observedProperty`, `sosa:usedProcedure`, `sosa:madeBySensor`, `sosa:hasResult`, `sosa:hasProperty`, `sosa:phenomenonTime`).

Beantwoord bij het tekenen:

- Kan de erosiepoel tegelijk `sosa:Platform` **en** `sosa:FeatureOfInterest` zijn?
- Waarnemer X is een persoon, geen elektronisch instrument. Welke klasse ken je toe?

---

## Stap 3 — Schrijf de Turtle

*Individueel of in groepjes — 20 minuten*

Schrijf een Turtle-bestand met minstens:

1. De erosiepoel als `sosa:Platform` én `sosa:FeatureOfInterest`
2. Waarnemer X als `sosa:Sensor` die de veldmeetprocedure implementeert
3. De `sosa:ObservationCollection` met gedeelde metadata
   (`sosa:hasFeatureOfInterest`, `sosa:madeBySensor`, `sosa:usedProcedure`,
   `sosa:phenomenonTime`, `sosa:resultTime`)
4. Één volledige `sosa:Observation` met `sosa:observedProperty` en `sosa:hasResult`
5. Het resultaat als `qudt:QuantityValue` met waarde 245.000 en eenheid `unit:L`
6. Het tijdstip als `time:Instant` met `time:inXSDDateTime`

Gebruik `https://example.org/erosiepoel/` als basis-IRI.

---

## Stap 4 — Plenaire bespreking

*Plenair — 15 minuten*

1. De erosiepoel is tegelijk `sosa:Platform` en `sosa:FeatureOfInterest`. Wanneer is
   zo'n dubbele typering zinvol? Wat zou er ontbreken als je de Platform-rol weglaat?
2. Waarom is Waarnemer X een `sosa:Sensor` en geen `prov:Agent`?
   Wat win je daarmee ten opzichte van een generieke agentrol?
3. Waarom `sosa:hasResult` met een `qudt:QuantityValue`-object in plaats van
   `sosa:hasSimpleResult "245000"^^xsd:decimal`?
4. De `sosa:ObservationCollection` bevat nu één observatie (sedimentvolume). Stel dat
   de veldwaarnemer ook de troebelheid en de waterstand noteert. Wat moet je aanpassen
   in het model?

---

*Referentieoplossing: `erosiepoel.ttl` en `erosiepoel.mmd`*
