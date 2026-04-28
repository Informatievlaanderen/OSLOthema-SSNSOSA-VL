# temperatuur-raam — Temperatuurgestuurde raambesturing

## Bronbestand

Illustratief voorbeeld. Er is geen extern bronbestand; het scenario is een vereenvoudigde
variant van het `elektrisch-raam`-voorbeeld. Er is slechts één sensor (een thermometer)
en de raamopener reageert direct op twee temperatuurdrempels:
- **> 20 °C** → raam volledig open
- **< 18 °C** → raam gesloten
- **18–20 °C** → raam blijft in de huidige stand (hysterese)

## Transformatieproces

Er is geen extern bronbestand. De Turtle is rechtstreeks opgesteld op basis van het scenario.
Geen XSLT, RIOT of SPARQL-transformatiestap nodig.

## Mapping-keuzes

**Architectuur: drielaags (Planning / Deployment / Execution)**

Het scenario heeft twee procedures met een expliciete gegevensstroom:
- Stap 1 (temp-meting) produceert de gemeten temperatuur.
- Stap 2 (raam-actuatie) neemt op basis van die temperatuur een open/dicht-beslissing.

Dezelfde procedure is herbruikbaar op andere kamers of gebouwen, en de dataflow van
meting naar actuatie vereist traceerbaarheid naar een abstract plan (R4). Er is geen
afgeleide observatie nodig: de drempellogica zit volledig in de `step:raam-actuatie`-procedure.

## Grafische voorstelling

Zie `temperatuur-raam.mmd` voor het Mermaid-diagram.

## Outputbestanden

- `src/main/output/temperatuur-raam/temperatuur-raam.ttl` — Turtle na inferentie
- `src/main/output/temperatuur-raam/temperatuur-raam.jsonld` — JSON-LD na framing

## Gebruik

```bash
mvn compile exec:java
```
