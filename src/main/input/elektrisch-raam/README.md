# elektrisch-raam — Automatische raambesturing Herman Teirlinck

## Bronbestand

Illustratief voorbeeld. Er is geen extern bronbestand; het scenario is ontworpen op basis van
de beschrijving van de raamautomatisering in zaal 01.16 (Rik Wouters) van het Herman Teirlinck
gebouw in Brussel. De windmeter is gesitueerd aan de gevel van het gebouw.

Referentie achtergrondcontext: Geran Handel B.V. — elektrische raamopeners met spindel- of
kettingaandrijving.

## Transformatieproces

Er is geen extern bronbestand. De Turtle is rechtstreeks opgesteld op basis van het scenario.
Geen XSLT, RIOT of SPARQL-transformatiestap nodig.

## Mapping-keuzes

**Architectuur: drielaags (Planning / Deployment / Execution)**

Het scenario bevat 5 procedures met een duidelijke gegevensstroom:
- Stappen 1–4 produceren meetwaarden (temperatuur, windsnelheid, lichtintensiteit, regen).
- Stap 5a (afgeleide observatie) berekent de afwijking t.o.v. de ideale temperatuur van 20°C.
- Stap 5b (actuatie) bepaalt de raamstand op basis van stap 5a en stappen 2–4.

Omdat dezelfde procedure herbruikbaar is op meerdere platforms en traceerbaarheid naar het
abstracte plan vereist is, is het drielaags model van toepassing.

Elke sensor implementeert één stap die tegelijk `p-plan:Step` en `sosa:Procedure` is.
Resultaten zijn benoemde IRI-entiteiten met `p-plan:correspondsToVariable` zodat ze
extern gerefereerd kunnen worden.

## Grafische voorstelling

Zie `elektrisch-raam.mmd` voor het Mermaid-diagram.

## Outputbestanden

- `src/main/output/elektrisch-raam/elektrisch-raam.ttl` — Turtle na inferentie
- `src/main/output/elektrisch-raam/elektrisch-raam.jsonld` — JSON-LD na framing

## Gebruik

```bash
mvn compile exec:java
```
