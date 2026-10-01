# Jaardebieten van lozingen (VMM) als SSN/SOSA 2023

Stap 3 van `../../stappenplan.md`: het jaardebiet 2023 per lozing (meetput) als SSN/SOSA
2023-observatie. De lozing is het FeatureOfInterest, net als `riepr:Emissie` in RIE-IEPR. Het
subset-voorbeeld AGC Glass Mol verbindt de VMM-meetwaarden met de controle-inrichtingen uit het
RIE-IEPR-datavoorbeeld.

## Bron

| | |
|---|---|
| Bronbestand | `../../brondata_Jurgen/250129_AW_Lozingsdebieten_2023_geleverd.xlsx`, tab `Pagina2` |
| JSON | `../../brondata_Jurgen/250129_AW_Lozingsdebieten_2023_geleverd/Pagina2.json` |
| Inhoud | 1555 meetputten (één rij per meetput) met jaardebiet 2023 in m³/jaar, databron IMJV (874) of MNT (681) |
| RIE-IEPR | `~/git/RIE-IEPR/documentatie/datamodel/datavoorbeelden/agc-glass_MJV_18-09-2026.ttl` (koppeling via `vmm:lozingspuntCode`) |

## Bestanden

| Bestand | Inhoud |
|---|---|
| `afvalwater_debieten.ttl` | validatie-subset: AGC Glass Mol, meetputten `2400006` (244 378 m³) en `2400007` (27 784 m³); 98 triples |
| `afvalwater_debieten.trig` | volledige omzetting: 1555 observaties, 52 285 triples |
| `afvalwater_debieten.mmd` | Mermaid-diagram van de subset |
| `bespreking.md` | conceptmapping en modelleerkeuzes |

## Transformatie

```bash
python3 src/main/input/waterkwaliteit/scripts/afvalwater_debieten.py [--csor ~/git/csor] [--riepr <RIE-IEPR-voorbeeld>]
```

- **Wat gemeten wordt:** CSOR-parameteraspect `PAS_1838` "Q (standaard in water): debiet"; eenheid
  `m³/jaar` (bron) → CSOR `m³/jr` (E_50). Beide worden eenduidig gevonden.
- **Gedeelde IRI's:** dezelfde `ex:`-namespace als stap 1 (`../afvalwater_concentraties`). Meetput,
  lozing en exploitatie krijgen dezelfde IRI's en triples. Nagekeken: voor de 59 meetputten in
  beide bronnen zijn de exploitatie-ID's en -namen gelijk, en de coördinaten verschillen minder
  dan 0,52 m. De meetput krijgt hier geen geometrie; die staat in stap 1.
- **RIE-IEPR:** meetputten met een `vmm:lozingspuntCode` in het RIE-IEPR-voorbeeld krijgen
  `rdfs:seeAlso` naar het RIE-IEPR-meetpunt. In het huidige voorbeeld zijn dat er 2
  (`2400006`, `2400007`).
- **Ontbrekende namen:** 3 exploitaties zonder naam in de bron (ID 511, 104136, 2806) krijgen
  geen label.

## Validatie (2026-09-30)

- Applicatieprofiel (`../../beslisdocument.md` A15): observaties, verzamelingen, resultaten,
  stalen, staalnames, meetplaatsen en meetputten zijn ook getypeerd met hun wk-klasse
  (`wk:WaterkwaliteitObservatie`, `wk:Meetresultaat` …). De SHACL-shapes worden gegenereerd uit
  `src/main/resources/be/vlaanderen/data/ns/waterkwaliteit/waterkwaliteit.ttl`.

- `mvn compile exec:java`: subset zonder `[VOCAB ERROR]` of `[MODEL INVALID]`, conform SHACL.
- `shacl validate` op de volledige `.trig`: `sh:conforms true`.
- **Samengevoegd met stap 1** (`afvalwater_concentraties.trig` + `afvalwater_debieten.trig`):
  `sh:conforms true`, geen enkele resource met twee labels. 59 lozingen hebben zowel
  concentraties per staal (stap 1) als een jaardebiet (stap 3), en zijn dus samen te bevragen.
  Een vracht (concentratie × debiet) is hiermee **niet** correct te berekenen: de concentraties
  zijn van 2024, de debieten van 2023. Stap 4 gebruikt daarom `251013`, waar concentratie,
  debiet en vracht per jaar samen aangeleverd worden.
