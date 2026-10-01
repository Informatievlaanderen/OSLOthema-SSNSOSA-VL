# Brondata waterkwaliteit (aangeleverd door Jurgen)

Voorbeelddatasets van de VMM om de mapping naar SSN/SOSA uit te werken. De originele
Excel-bestanden staan in deze map. Per bestand staat er een subdirectory met één JSON per tab,
aangemaakt met `xlsx_naar_json.py`.

## Begeleidend bericht

> Geert, Pieter,
>
> In bijlage zitten een aantal datasets die jullie kunnen gebruiken om de mapping te doen voor
> SSN-SOSA.
>
> Er zit een beetje variatie in: afvalwater met bedrijven en meetpunten en concentraties en
> vrachten als meetwaarden. Oppervlaktewater met resultaten en ook beoordelingen tov de norm. De
> normen zelf passen denk ik niet in SSN-SOSA maar moeten mogelijk apart gemodelleerd worden net
> als de status beoordeling.
>
> Het is denk ik op dit moment niet noodzakelijk om alle eigenschappen van de bedrijven of sample
> points/meetputten/waterlopen mee te modelleren. Dat kan in een andere oefening verder uitgewerkt
> worden.
>
> Ik zou in de eerste plaats focussen op de resultaten en eventueel nadien de normen en
> beoordelingen toevoegen.
>
> Laat gerust weten als jullie nog vragen hebben.

## Afgesproken scope

1. **Eerst:** de meetresultaten (concentraties, vrachten, debieten) als SOSA-observaties.
2. **Nadien:** de normen en de beoordelingen ten opzichte van die normen. Die worden
   waarschijnlijk apart gemodelleerd, buiten SSN/SOSA.
3. **Niet nu:** alle kenmerken van bedrijven, meetputten, sample points en waterlopen.
   Die zijn enkel nodig als identificator of FeatureOfInterest.

## Overzicht van de datasets

| Bestand (subdirectory) | Tab | Records | Domein | Inhoud | Prioriteit |
|---|---|---|---|---|---|
| `250108_AW_Resultaat_Prompts_R_62-mtpn-UK-PFAS-AW_2024` | `Pagina1` | 1998 | Afvalwater | Individuele analyseresultaten 2024 op 60 meetpunten (RWZI-effluent en andere), 325 parameters. Per resultaat: sample (schepmonster / debietgebonden), datum, teken (`<` of `=`), waarde, eenheid, onder- en bovengrens, aantoonbaarheids- en bepaalbaarheidsgrens. De kolommen zijn gegroepeerd per exploitatie, sample point, sample, tijd en parameter. | **1: resultaten** |
| | `SPs` | 62 | Afvalwater | Lijst van de meetpuntnummers met `AW`-code (zonder kop) | hulplijst |
| `250114_Analyseresultaten_per_meetplaats_OW` | `Resultaten` | 999 | Oppervlaktewater | Analyseresultaten op meetplaats `OW12000` (3 monsternames in 2019): datum, tijdstip, parameter, teken, resultaat, eenheid | **1: resultaten** |
| | `Parameters` | 647 | Oppervlaktewater | Parameterlijst: symbool, omschrijving, eenheid | codelijst |
| | `SamplePoints` | 54 | Oppervlaktewater | Meetplaatsen met Lambert-coördinaten, waterloop, bekken, gemeente | FOI, beperkt |
| `240426_AW_Vrachten-PFAS_Indaver_3M_excl-totaal-par` | `Pagina1` | 500 | Afvalwater | Jaarvrachten (bruto, mg) van 5 PFAS (PFOS, PFOA, PFNA, PFHpA, PFDA) per meetput en per jaar, 2008–2023 | **1: vrachten (afgeleid)** |
| `251013_AW_Periodevracht_DETS_Prompts_3-contrastmiddelen_geenInEx` | `per_type_meetput` | 114 | Afvalwater | Jaarvracht van 3 jodiumhoudende contrastmiddelen per type meetput (oppervlaktewater, riool, collector, influent RWZI), voor bedrijven en RWZI's, 2014–2025: concentratie, debiet (m³), bruto en netto vracht | **1: vrachten (afgeleid)** |
| `250129_AW_Lozingsdebieten_2023_geleverd` | `Pagina2` | 1555 | Afvalwater | Jaardebiet 2023 per meetput (bron IMJV of MNT), met veel kenmerken van exploitatie en meetput (adres, zuiveringsgebied, lozingstype, NACE-sector en -code) | **1: debieten**; bedrijfskenmerken niet nu |
| `250124_Beoordeling_gevaarlijke_stoffen_WB_voor_SGBP` | `Beoordeling_Vlarem_Trigger` | 249 | Waterbodem (sediment, `µg/kg ds`) | Meting per meetpunt en parameter (2020, 2024) vergeleken met een Vlarem-norm of triggerwaarde: norm, meting, beoordeling (`goed`, `niet goed`, `geen beoordeling`), overschrijding | 2: normen en beoordelingen |
| | `Vlaremnormen_sediment` | 54 | Waterbodem | Vlarem-normen per parameter: eenheid, toetswijze (`MAX`), norm (`<=0,1`) | 2: normen |
| | `Triggerwaarden` | 73 | Waterbodem | Triggerwaarden per parameter, in dezelfde structuur | 2: normen |

### Referentielijst observatiemethoden (VITO)

| Bestand (subdirectory) | Tab | Records | Inhoud |
|---|---|---|---|
| `Lijst_observatiemethodes_VITO-v1` | `Observatiemethoden` | 939 | Voorstel van VITO voor de codelijst observatieprocedures: 313 hoofdprocedures (CMA 164, WAC 109, LUC 38, BOC 2) en per hoofdprocedure een jaarversie 2024 en 2025 (626). Per versie: URI (`…/observatieprocedure/<code>_<jaar>`), label, notation, `Is versie van` → hoofdprocedure, jaar, pdf op reflabos.vito.be. `Definition` is nog leeg. |
| | `Eindresultaat` | 3 | Voorbeeld van het gevraagde eindformaat (WAC/IV/A/007), met een extra kolom voor de meetbare parameters (pipe-gescheiden URI's) |
| | `Toelichting` | 22 | Uitleg per kolom en de opdracht aan VITO. Geen koprij, dus sleutels `kolom_A`–`kolom_C`. |

De hoofdprocedures gebruiken dezelfde URI's als `codelijst-observatieprocedure`
(bv. `WAC_I_A_003` schepmonster en `WAC_I_A_004` verzamelmonster, gebruikt in
`../nieuw_model/afvalwater_concentraties`). De jaarversies (`WAC_I_A_003_2024`, `…_2025`) zijn
nieuw.

## Eerste modelleeraandachtspunten

- **Teken `<`:** een resultaat onder de aantoonbaarheids- of bepaalbaarheidsgrens. Dat komt veel
  voor: 1605 van de 1998 resultaten in afvalwater en 834 van de 999 in oppervlaktewater. Het teken
  moet dus bij het resultaat bewaard blijven en niet enkel als getal.
- **Monster en meetpunt:** een sample (staal) wordt genomen op een sample point, en op dat staal
  worden meerdere parameters bepaald. Dat past bij `sosa:Sample` → `sosa:isSampleOf`, met het
  meetpunt als `sosa:SpatialSample` (R1, R8, R11). Eén staal met meerdere parameters is een
  kandidaat voor een `sosa:ObservationCollection`.
- **Vrachten:** vracht = concentratie × debiet. Dat is een afgeleide observatie met
  `sosa:hasInputValue` naar de bronresultaten en `sosa:relatedObservation` naar de
  bronobservaties, niet als lid van de collectie (R7, R13). De
  periode is een jaar, dus `time:Interval` (R12).
- **Eenheden:** meerdere eenheden, waarvan sommige met een "als"-element (`mgN/L`, `mgP/L`,
  `mgO2/L`, `ngSn/L`, `µg/kg ds`). Die hebben een QUDT-eenheid nodig, of een eenheid plus
  specificatie van de grootheid.
- **NACE:** de NACE-codes in `250129` sluiten aan bij `../nacebel/` (NACE-BEL 2008/2025).
- **Coördinaten:** afvalwater en oppervlaktewater gebruiken Lambert 72. In de waterbodemdataset
  lijken de Lambert-waarden (≈ 728000 / 719000) Lambert 2008 te zijn. Die dataset bevat ook
  ETRS89-coördinaten. Dit moet nog nagevraagd worden.
