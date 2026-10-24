# Modelleeroefening: Een lozing in het integraal milieujaarverslag

## Use case

### Context

Een glasfabriek in Mol dient elk jaar een integraal milieujaarverslag (IMJV) in bij het
Departement Omgeving. Daarin beschrijft ze haar processen, de installaties en lozingspunten die ze
gebruikt, en de hoeveelheden stoffen die ze in het afgelopen jaar loosde. De overheid wil per
lozing weten welk proces ze veroorzaakte en hoeveel van elke stof er in het water terechtkwam.

### Beschrijving van het systeem

| Component | Kenmerken |
|---|---|
| Exploitatielocatie | AGC Glass Europe, vestiging Mol, Voortstraat 27; punt 5,1621 O, 51,1940 N |
| Exploitant | AGC Glass Europe (KBO 0413.638.187) |
| Installatie *vormen en bewerken van vlakglas* | produceert proceswater |
| Lozingspunt LP01 | loost het afvalwater van de glasfabriek; heeft een meetpunt |
| Rapporteringsjaar | 2021 |

Het proces: de installatie levert proceswater, dat via lozingspunt LP01 geloosd wordt.

### Concrete meetgegevens

Aangegeven voor LP01 over het jaar 2021:

| Gegeven | Waarde | Hoe bepaald |
|---|---|---|
| Jaardebiet | 336 735 m³/jaar | debietmeting |
| Concentratie zink | 0,00474 mg/L | meetgegevens |
| Jaarvracht zink | 1,59612 kg/jaar | concentratie × jaardebiet |

---

## Stap 1 — Identificeer de SOSA-concepten

*Individueel — 10 minuten*

Gebruik de klassen `FeatureOfInterest`, `Property`, `Sensor`, `System`, `Platform`, `Deployment`,
`Observation`, `ObservingProcedure`, `Plan`, `Step`, `Variable` en `qudt:QuantityValue`.

| Vraag | Antwoord | Klasse |
|---|---|---|
| Wat is het **studieobject** van de drie aangegeven waarden: het lozingspunt of de lozing? | | |
| Welke **eigenschappen** worden geobserveerd? Zijn concentratie en vracht van zink dezelfde eigenschap? | | |
| Wat is het **plan**, en uit welke **stappen** bestaat het? | | |
| Welke **variabele** verbindt de stappen? | | |
| Welk **systeem** voert elke stap uit? | | |
| Wat is het **platform** dat de systemen herbergt? | | |
| Wat stelt de **exploitatie 2021** voor, en hoe hangt ze aan het plan? | | |
| Welke van de drie waarden is een **afgeleide** observatie? Uit welke resultaten? | | |
| Wie is de **sensor**? Weet je dat uit de gegevens? | | |

---

## Stap 2 — Schets een diagram

*In groepjes van 2 — 15 minuten*

Teken drie lagen:

- **PLANNING** — het plan 2021, de stappen *vlakglas* en *lozing LP01*, hun volgorde en hun
  variabelen.
- **DEPLOYMENT** — de exploitatielocatie, de exploitant, de exploitatie 2021, de installatie, het
  lozingspunt en het meetpunt.
- **EXECUTION** — de lozing, de drie observaties, hun resultaten en het jaar 2021; de vracht in
  een aparte afleidingslaag.

Beantwoord bij het tekenen:

- Is de stap *lozing* een stap van de stap *vlakglas*, of volgt ze erop? Hoe toon je dat?
- Kan een `sosa:Deployment` een procedure implementeren? Welke PROV-relatie verbindt een activiteit
  met het plan dat ze volgt?
- Waar komt de eenheid vandaan: QUDT of het CSOR-register?

---

## Stap 3 — Schrijf de Turtle

*Individueel of in groepjes — 20 minuten*

Schrijf een Turtle-bestand met minstens:

1. het plan met twee `p-plan:Step`s, in volgorde (`p-plan:isPrecededBy`), en de procesvariabelen
   *proceswater* en *afvalwater*;
2. de exploitatielocatie (`sosa:Platform`), het lozingspunt (`sosa:System`, dat de stap *lozing*
   implementeert) en de exploitatie (`sosa:Deployment`) met `prov:hadPlan`;
3. de lozing als studieobject, gekoppeld aan de variabele *afvalwater*;
4. de observaties van jaardebiet en concentratie, met een `qudt:QuantityValue` als resultaat en
   een CSOR-eenheid;
5. de jaarvracht als afgeleide observatie, met `sosa:hasInputValue` en
   `sosa:relatedObservation`;
6. het jaar 2021 als `time:Interval` met een tijdzone.

Gebruik `https://example.org/riepr/` als basis-IRI.

---

## Stap 4 — Plenaire bespreking

*Plenair — 15 minuten*

1. Waarom is de lozing, en niet het lozingspunt, het studieobject? Wanneer zou je het omgekeerde
   kiezen?
2. Wat verlies je als concentratie en vracht dezelfde `sosa:observedProperty` krijgen, en enkel
   de eenheid verschilt?
3. Waarom wijst `sosa:hasInputValue` naar de resultaten en niet naar de observaties?
4. Is een fictieve sensor beter dan geen sensor? Wat zegt de validatie, en wat zegt de bron?
5. De ontologie eiste `prov:wasDerivedFrom` van de lozing naar het proces. Is dat fout, een korte
   weg, of allebei? Wat zou de volledige PROV-keten zijn?

---

*Referentieoplossing: `riepr_herzien.ttl` en `riepr_herzien.mmd`*
