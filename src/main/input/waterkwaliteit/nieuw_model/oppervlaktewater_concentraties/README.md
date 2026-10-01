# Concentraties in oppervlaktewater (VMM) als SSN/SOSA 2023

Stap 2 van `../../stappenplan.md`: analyseresultaten van stalen oppervlaktewater op een
VMM-meetplaats, met de VHA-waterloop als ultiem studieobject. Hetzelfde observatiepatroon als
stap 1 (`../afvalwater_concentraties`), maar met een meetplaats als ruimtelijk monster van een
waterloop (R8, R11).

## Bron

| | |
|---|---|
| Bronbestand | `../../brondata_Jurgen/250114_Analyseresultaten per meetplaats_OW.xlsx`, tabs `Resultaten` en `SamplePoints` |
| JSON | `../../brondata_Jurgen/250114_Analyseresultaten_per_meetplaats_OW/` |
| Inhoud | 999 analyseresultaten van 3 stalen (28/01, 25/02 en 26/03/2019) op meetplaats `OW12000` (Philippine, Isabellahaven, Leopoldkanaal), 344 parameteraspecten |
| Koppeling met de waterloop | `../../waterlopen/meetplaats_waterloop.csv` (`scripts/waterlopen_subset.py`) |

## Bestanden

| Bestand | Inhoud |
|---|---|
| `oppervlaktewater_concentraties.ttl` | validatie-subset: staal van 28/01/2019 13:01, 14 representatieve parameters (pH, geleidbaarheid, temperatuur, zuurstof, BZV5, KjN, nitraat, fosfor, hardheid, chloride, opgelost zink en koper, en twee `<`-resultaten); 310 triples. Een volledig staal (331 resultaten) duurde minuten in de OWL-validatie van de pipeline. Door de Maven-pipeline gevalideerd. |
| `oppervlaktewater_concentraties.trig` | volledige omzetting: 999 observaties, 3 stalen, 14 989 triples |
| `oppervlaktewater_concentraties.mmd` | Mermaid-diagram van de subset |
| `bespreking.md` | conceptmapping en modelleerkeuzes |

## Transformatie

```bash
python3 src/main/input/waterkwaliteit/scripts/oppervlaktewater_concentraties.py [--csor ~/git/csor]
```

1. **Staal:** de bron heeft geen staal-ID. Een staal is daarom (meetplaats, datum, tijdstip).
   Het tijdstip wordt afgerond op de seconde: Excel levert `12:50:59.999` voor 12:51.
2. **Parameter:** de bron heeft geen parametercode. De parameter volgt uit CSOR-symbool + drager
   `water`, en het parameteraspect uit de eenheid (`../../codelijsten.md` §3.1–3.2). Het script
   stopt als dat niet eenduidig is. Voor alle 999 rijen is het eenduidig.
3. **Waterloop:** uit `meetplaats_waterloop.csv`. Het script stopt als een meetplaats geen
   waterloop heeft. De waterloop is een `waterlopen:Vhag`. Het script neemt de volledige
   VHA-beschrijving (label, lengte, geometrie als `geo:hasGeometry` naar een blank node) over uit `../../waterlopen/waterlopen_meetplaatsen.ttl`
   (`../../beslisdocument.md` A15.6).
4. De CSOR-code wordt gedeeld met stap 1 via `scripts/waterkwaliteit_gemeen.py`.

## Validatie (2026-09-30)

- Applicatieprofiel (`../../beslisdocument.md` A15): observaties, verzamelingen, resultaten,
  stalen, staalnames, meetplaatsen en meetputten zijn ook getypeerd met hun wk-klasse
  (`wk:WaterkwaliteitObservatie`, `wk:Meetresultaat` …). De SHACL-shapes worden gegenereerd uit
  `src/main/resources/be/vlaanderen/data/ns/waterkwaliteit/waterkwaliteit.ttl`.

- `mvn compile exec:java`: subset zonder `[VOCAB ERROR]` of `[MODEL INVALID]`, conform SHACL.
- `shacl validate` op de volledige `.trig`: `sh:conforms true`.
- 834 resultaten met teken `<` (`qudt:upperBound`) en 165 met `=` (`qudt:numericValue`), zoals
  in de bron.

## Aandachtspunten

- **`OW12000` ligt in Nederland** (Philippine, Isabellahaven), vlak over de grens, aan het
  Leopoldkanaal. De VHA-waterlopen dekken enkel Vlaanderen. Het dichtstbijzijnde VHA-segment van
  het Leopoldkanaal ligt daardoor op 629 m, en de koppeling staat op `controle = ja`. De
  waterloop is inhoudelijk juist; de afstand volgt uit de grens.
- Staalnameprocedure en staalnemer staan niet in de bron (§6.4 van `bespreking.md`).
