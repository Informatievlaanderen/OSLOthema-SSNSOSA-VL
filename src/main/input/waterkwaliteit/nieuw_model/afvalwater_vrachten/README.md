# Vrachten van lozingen (VMM) als SSN/SOSA 2023

Stap 4 van `../../stappenplan.md`: vrachten als **afgeleide observaties**, volgens de
ontwerpregel uit het stappenplan. Een vracht verwijst met `sosa:hasInputValue` naar de
resultaten (waarden) waaruit ze berekend is, en met `sosa:relatedObservation` naar de
observaties die ze opleverden. Haar procedure declareert de abstracte inputs
(`sosa:hasInput`). Bronobservaties onderling krijgen geen koppeling. Twee datasets:

| Dataset | FOI | Wat erin zit | Bestanden |
|---|---|---|---|
| `251013` contrastmiddelen | groep van lozingen (categorie lozer × type meetput) | concentratie, debiet, bruto en netto vracht per jaar: het volledige afleidingspatroon | `vrachten_contrastmiddelen.ttl` / `.trig` |
| `240426` PFAS | de lozing (zelfde IRI's als stap 1 en 3) | enkel de bruto jaarvracht, zonder inputs | `vrachten_pfas.ttl` / `.trig` |

## Bron

| | |
|---|---|
| `251013` | `../../brondata_Jurgen/251013_AW_Periodevracht DETS_Prompts_3-contrastmiddelen_geenInEx.xlsx`, tab `per type meetput`: 114 rijen = 5 groepen × jaren 2014–2025 (38 groep-jaren) × 3 contrastmiddelen (amidotrizoïnezuur, iopamidol, iopromide) |
| `240426` | `../../brondata_Jurgen/240426_AW_Vrachten-PFAS_Indaver_3M_excl-totaal-par.xlsx`, tab `Pagina1`: 500 bruto jaarvrachten van 5 PFAS op 256 meetputten, 2008–2023 |

## Bestanden

| Bestand | Inhoud |
|---|---|
| `vrachten_contrastmiddelen.ttl` | subset: bedrijven via riool, 2014. 1 debiet, 3 concentraties, 3 bruto- en 3 nettovrachten; 227 triples |
| `vrachten_contrastmiddelen.trig` | volledig: 380 observaties, waarvan 114 bruto vrachten met samen 228 `hasInputValue`-verwijzingen naar resultaten en 228 `relatedObservation`-verwijzingen naar bronobservaties; 6374 triples |
| `vrachten_pfas.ttl` | subset: meetput `2030042`, 3 jaarvrachten. De exploitant wisselt van Antwerp Waste Management (2009) naar Veolia ES MRC (2017, 2022). 114 triples |
| `vrachten_pfas.trig` | volledig: 500 observaties; 8656 triples |
| `afvalwater_vrachten.mmd` | Mermaid-diagram van het afleidingspatroon (contrastmiddelen) |
| `bespreking.md` | conceptmapping en modelleerkeuzes voor beide datasets |

## Transformatie

```bash
python3 src/main/input/waterkwaliteit/scripts/afvalwater_vrachten.py [--csor ~/git/csor]
```

Het script controleert vooraf twee dingen, en stopt als een ervan niet klopt:

- in `251013` is bruto vracht = concentratie × debiet (µg/L × m³ = mg); dat klopt voor alle 114
  rijen;
- het debiet is per groep en jaar gelijk voor de drie parameters, zodat één debietobservatie
  gedeeld kan worden.

CSOR-koppeling:

| Resultaat | Parameteraspect |
|---|---|
| concentratie | "…: massaconcentratie" (µg/L, E_4) |
| debiet | `PAS_1839` "Q (standaard in water): debiet (vracht)" (m³, E_32) |
| vracht | "…: vracht" (mg, E_37) |

De procedure-inputs en -output zijn CSOR kwantificeerbare aspecten: KWA_1 massaconcentratie,
KWA_10 debiet (vracht), KWA_5 vracht.

## Validatie (2026-09-30)

- Applicatieprofiel (`../../beslisdocument.md` A15): observaties, verzamelingen, resultaten,
  stalen, staalnames, meetplaatsen en meetputten zijn ook getypeerd met hun wk-klasse
  (`wk:WaterkwaliteitObservatie`, `wk:Meetresultaat` …). De SHACL-shapes worden gegenereerd uit
  `src/main/resources/be/vlaanderen/data/ns/waterkwaliteit/waterkwaliteit.ttl`.

- `mvn compile exec:java`: beide subsets zonder `[VOCAB ERROR]` of `[MODEL INVALID]`, conform
  SHACL.
- `shacl validate` op beide volledige `.trig`-bestanden: `sh:conforms true`.
- **Samengevoegd met stap 1 en 3** (alle vier de `.trig`-bestanden): `sh:conforms true`, geen
  enkele resource met twee labels. Van de 1619 lozingen hebben er 43 alle drie de soorten
  gegevens (stalen, jaardebiet en PFAS-jaarvrachten).
