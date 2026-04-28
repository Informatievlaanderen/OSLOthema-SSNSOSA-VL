# Modelleeroefening: Temperatuurgestuurde raambesturing

## Use case

### Context

Zaal 01.16 (Rik Wouters) in het Herman Teirlinck gebouw te Brussel is uitgerust met een
elektrische raamopener. Om oververhitting te vermijden zonder continu menselijke tussenkomst,
is een eenvoudig automatisch besturingssysteem geïnstalleerd.

### Beschrijving van het systeem

Het systeem bestaat uit twee componenten:

- Een **thermometer** die de luchttemperatuur in de zaal meet.
- Een **elektrische raamopener** die het raam volledig opent of sluit op basis van de gemeten
  temperatuur.

De besturingslogica werkt met twee drempelwaarden (hysterese):

| Conditie | Actie |
|---|---|
| Gemeten temperatuur **> 20 °C** | Raam volledig **open** (100 %) |
| Gemeten temperatuur **< 18 °C** | Raam volledig **gesloten** (0 %) |
| Temperatuur tussen 18 en 20 °C | Raam blijft in huidige stand |

### Concrete meetgegevens

Op 27 april 2025 worden twee metingen geregistreerd:

| Tijdstip | Gemeten temperatuur | Verwachte raamactie |
|---|---|---|
| 09:00:00 UTC | 22,3 °C | Raam opent (> 20 °C) |
| 10:00:00 UTC | 17,5 °C | Raam sluit (< 18 °C) |

De raamopener reageert telkens 5 seconden na de meting.

---

## Stap 1 — Identificeer de SOSA-concepten

*Individueel — 10 minuten*

Lees de use case en vul onderstaande tabel in. Gebruik de SOSA-klassen `Platform`,
`FeatureOfInterest`, `Sensor`, `Actuator`, `ObservingProcedure`, `ActuatingProcedure`,
`ObservableProperty`, `Observation`, `Actuation` en `Result`.

| Vraag | Antwoord |
|---|---|
| Wat zijn de **platforms** in dit systeem? | |
| Wat is het **ding dat bestudeerd wordt** (FeatureOfInterest) voor de temperatuurmeting? | |
| Wat is het **ding dat geactueerd wordt** voor de raamstand? | |
| Welke **sensor** produceert observaties? | |
| Welke **actuator** voert acties uit? | |
| Wat is de **observeerbare eigenschap** van de zaal? | |
| Wat is de **actueerbare eigenschap** van het raam? | |
| Hoeveel **observaties** zijn er in de concrete dataset? | |
| Hoeveel **actuaties** zijn er? | |

---

## Stap 2 — Schets een diagram

*In groepjes van 2 — 15 minuten*

Teken een diagram met de volgende drie lagen:

- **PLANNING** — het abstracte plan met stappen en variabelen
  (`p-plan:Plan`, `p-plan:Step`, `p-plan:Variable`)
- **DEPLOYMENT** — de concrete fysieke opstelling (platforms, sensor, actuator)
- **EXECUTION** — de twee concrete meetmomenten met hun resultaten

Gebruik pijlen om relaties te tonen en label elke pijl met de bijhorende property
(bijv. `sosa:madeBySensor`, `prov:used`).

Beantwoord bij het tekenen:

- Hoe toon je de data-afhankelijkheid tussen een temperatuurresultaat en de bijhorende
  raamactuatie?
- Welke property gebruik je op execution-niveau voor die koppeling: `sosa:hasInput` of
  `prov:used`? Waarom?

---

## Stap 3 — Schrijf de Turtle

*Individueel of in groepjes — 20 minuten*

Schrijf een Turtle-bestand met minstens:

1. De twee `p-plan:Step`-resources (één `ObservingProcedure`, één `ActuatingProcedure`)
2. De twee platforms (`gebouw` en `zaal`) en de twee instrumenten (`thermometer`,
   `raamopener`)
3. Eén volledige `sosa:Observation` met alle verplichte properties
4. Eén volledige `sosa:Actuation` die verwijst naar het temperatuurresultaat

Gebruik `https://example.org/temperatuur-raam/` als basis-IRI.

---

## Stap 4 — Plenaire bespreking

*Plenair — 15 minuten*

1. Waarom is het temperatuurresultaat een benoemde IRI-resource en geen
   `sosa:hasSimpleResult`?
2. Wat is het verschil tussen `sosa:phenomenonTime` en `sosa:resultTime`?
   Welke waarden krijgen ze in dit voorbeeld?
3. Stel dat morgen een tweede zaal met dezelfde opstelling bijkomt. Wat hergebruik je
   uit het model, en wat voeg je toe?

---

*Referentieoplossing: `temperatuur-raam.ttl` en `temperatuur-raam.mmd`*
