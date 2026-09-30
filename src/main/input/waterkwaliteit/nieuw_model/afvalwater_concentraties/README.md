# Concentraties in afvalwater (VMM) als SSN/SOSA 2023

Stap 1 van `../../stappenplan.md`: de analyseresultaten van afvalwaterstalen van de VMM als
SSN/SOSA 2023. Dit is het kernvoorbeeld van de waterkwaliteit-mapping. Het bevat stalen,
meetpunten, rapportagegrenzen (teken `<`) en de koppeling aan CSOR.

## Bron

| | |
|---|---|
| Bronbestand | `../../brondata_Jurgen/250108_AW_Resultaat_Prompts_R_62-mtpn-UK-PFAS-AW_2024.xlsx`, tab `Pagina1` |
| JSON | `../../brondata_Jurgen/250108_AW_Resultaat_Prompts_R_62-mtpn-UK-PFAS-AW_2024/Pagina1.json` |
| Inhoud | 1998 analyseresultaten (2024) van 697 stalen op 60 meetpunten, 325 parameters |
| Aangeleverd door | VMM (zie `../../brondata_Jurgen/README.md`) |

## Bestanden

| Bestand | Inhoud |
|---|---|
| `afvalwater_concentraties.ttl` | validatie-subset: staal `M-AW-2024-006358-1` (RWZI Mechelen-Noord, 27/03/2024), 15 resultaten, teken `<` en `=`; 266 triples. Wordt door de Maven-pipeline gevalideerd. |
| `afvalwater_concentraties.trig` | volledige omzetting: 1998 observaties, 42 337 triples (Turtle-inhoud; `.trig` houdt het buiten de pipeline) |
| `afvalwater_concentraties.mmd` | Mermaid-diagram van de subset |
| `bespreking.md` | conceptmapping en modelleerkeuzes |

## Transformatie

```bash
python3 src/main/input/waterkwaliteit/scripts/afvalwater_concentraties.py [--csor ~/git/csor]
```

1. Het script leest de JSON-omzetting van de Excel (`brondata_Jurgen/xlsx_naar_json.py`).
2. Het laadt de CSOR-codelijsten parameter, parameteraspect, kwantificeerbaar aspect en eenheid
   uit `~/git/csor/codelijst-csor-*`, en de jaarversies van de observatieprocedures uit
   `brondata_Jurgen/Lijst_observatiemethodes_VITO-v1/Observatiemethoden.json`. Een staalname
   verwijst naar de versie van haar jaar (bv. `WAC_I_A_003_2024`).
3. Per rij:
   - parameter via `Parameter Code` (= CSOR `skos:notation`);
   - eenheid via `Eenheid` (= CSOR `csor:symbool`);
   - parameteraspect = het aspect van die parameter waarvan `csor:toepasbareEenheid` de eenheid
     bevat.

   Het script stopt als een rij geen eenduidig parameteraspect oplevert. Voor alle 1998 rijen
   lukt dat.
4. Het schrijft de volledige set (`.trig`) en de subset voor één staal (`.ttl`, `SUBSET_STAAL`
   in het script).

## Validatie (2026-09-29)

- `mvn compile exec:java`: subset zonder `[VOCAB ERROR]` of `[MODEL INVALID]`, conform SHACL.
- `shacl validate --shapes src/main/resources/generated-shapes.ttl` op de volledige `.trig`:
  `sh:conforms true`.
- Steekproef: voor alle 15 resultaten van het subset-staal kloppen parameteraspect en eenheid met
  de bron (bv. `P t` in `mgP/L` → "P t (totaal in water): massaconcentratie fosfor", eenheid
  E_131).

## Voorlopige keuzes

Het voorbeeld volgt de voorstellen B1–B5 uit `../../stappenplan.md` §3. Die zijn nog niet
definitief. Zie `bespreking.md` §6 voor de motivatie en de verworpen alternatieven.
