# Beslisdocument: SSN/SOSA-model waterkwaliteit

*Voorbereiding voor het OSLO-traject. Versie 2026-09-30.*

## 0. Doel en werkwijze

Het definitieve waterkwaliteitmodel wordt in een OSLO-traject van de Vlaamse overheid
vastgelegd. Dit document legt daarvoor een **uitgewerkt voorstel** voor: per beslispunt de
vraag, het voorstel zoals het in de datavoorbeelden is uitgewerkt, de verworpen alternatieven, de
gevolgen, en waar het voorbeeld te vinden is. De open punten zijn gegroepeerd naar wie ze moet
beslissen of beantwoorden:

| Deel | Voor wie | Inhoud |
|---|---|---|
| **A** | OSLO-werkgroep | modelkeuzes |
| **B** | VMM (databeheer) | vragen over de betekenis van de brondata |
| **C** | beheerders van registers en aanpalende projecten | wijzigingen of afstemming buiten dit model |
| **D** | later | wat nog niet gemodelleerd is (fase 2 en 3) |

**Status per punt:** *voorstel* (uitgewerkt, te bevestigen), *open* (geen voorstel), *beslist*
(na een sessie invullen, met datum).

**Na een beslissing:** de omzetting is volledig gescript (`scripts/`). Een beslissing wordt dus in
het betreffende script aangepast. Daarna worden alle voorbeelden opnieuw gegenereerd en
gevalideerd (`mvn compile exec:java`, `shacl validate`).

Dit document vervangt de beslissingstabellen in `stappenplan.md` §3, `codelijsten.md` §6 en
`featureofinterest.md` §4, en neemt de huidige toestand van de voorbeelden als voorstel.

### De datavoorbeelden (basis voor de sessies)

Alle voorbeelden gebruiken echte VMM-brondata (`brondata_Jurgen/`), zijn conform SHACL, zonder
`[VOCAB ERROR]`, en samengevoegd conflictvrij (1619 lozingen, geen dubbele labels).

| Voorbeeld | Bron | Wat het toont | Map |
|---|---|---|---|
| Concentraties afvalwater | `250108` | staal, staalname, meetput, CSOR-koppeling, teken `<` | `nieuw_model/afvalwater_concentraties/` |
| Concentraties oppervlaktewater | `250114` | meetplaats als ruimtelijk monster van een VHA-waterloop | `nieuw_model/oppervlaktewater_concentraties/` |
| Jaardebieten | `250129` | lozing als FOI, jaarinterval, koppeling met RIE-IEPR (AGC Glass Mol) | `nieuw_model/afvalwater_debieten/` |
| Vrachten | `251013`, `240426` | afgeleide observaties, berekeningsprocedure, groep van lozingen | `nieuw_model/afvalwater_vrachten/` |

---

## 1. Overzicht

| # | Onderwerp | Deel | Status | Detail |
|---|---|---|---|---|
| A1 | `observedProperty` = CSOR-parameteraspect | A | voorstel | §2 |
| A2 | Eenheid = CSOR-eenheid (QUDT via SKOS-mapping) | A | voorstel | §2 |
| A3 | Resultaat onder de rapportagegrens (`<`) | A | voorstel (deels open) | §2 |
| A4 | FOI van een concentratie: staal, lozing als ultiem FOI | A | voorstel | §2 |
| A5 | Lozing tijdsloos, matrix op het FOI | A | voorstel | §2 |
| A6 | Meetplaats oppervlaktewater als ruimtelijk monster van de VHA-waterloop | A | voorstel | §2 |
| A7 | Wanneer observaties koppelen; afgeleide observaties | A | voorstel | §2 |
| A8 | Groep van lozingen als FOI | A | voorstel | §2 |
| A9 | Meetput, staalnemer en databron | A | voorstel | §2 |
| A10 | Procedures: WAC/CMA-compendium, jaarversies, soort procedure | A | voorstel | §2 |
| A11 | Codelijsten: hergebruik tegenover nieuw | A | voorstel | §2 |
| A12 | IRI-strategie en namespaces | A | open | §2 |
| A13 | Kenmerken die in de tijd veranderen (versies van een lozing) | A | open (fase 3) | §2 |
| A14 | `wk:Emissie` herdefiniëren als subklasse van `prov:Entity` | A | beslist (projectteam), deelpunten open | §2 |
| A15 | Applicatieprofiel: `waterkwaliteit.ttl` als bron van de SHACL, AP-klassen, mapping van het AP 2023 | A | voorstel | §2 |
| V1–V10 | Vragen over de brondata | B | open | §3 |
| C1–C5 | CSOR, VITO-lijst, VHA-waterlopen, RIE-IEPR, codelijst-rie-iepr | C | open | §4 |
| D1–D3 | Normen en beoordelingen, waterlichamen, kenmerken | D | later | §5 |

---

## 2. Deel A: modelkeuzes voor de OSLO-werkgroep

### A1. Wat gemeten wordt: het CSOR-parameteraspect

**Vraag.** Waar verwijst `sosa:observedProperty` naar?

**Voorstel.** Naar het **CSOR-parameteraspect**: parameter (variabele + drager + soort
waardebepaling) × kwantificeerbaar aspect.

```turtle
ex:observatie-16231-P_1228 sosa:observedProperty csor-parameteraspect:PAS_2163 .
# PAS_2163 = "P t (totaal in water): massaconcentratie fosfor"
```

**Waarom.**
- Het parameteraspect onderscheidt concentratie, vracht en debiet van dezelfde stof. Een
  parameter of een stof-IRI kan dat niet: "Amidotriz: massaconcentratie" (PAS_182) tegenover
  "Amidotriz: vracht" (PAS_183).
- De vijf gemodelleerde VMM-datasets en de waterbodemdataset `250124` koppelen **eenduidig**:
  via `Parameter Code` of via symbool + drager + eenheid, voor 100 % van de rijen.

**Verworpen alternatieven.**
- De CSOR-parameter: geen onderscheid tussen grootheden.
- Een chemische stof via InChIKey, zoals nu in RIE-IEPR: idem, en niet voor fysische parameters
  (pH, geleidbaarheid).
- Eigen eigenschappen per dataset: dat dupliceert CSOR.

**Gevolg.**
- Elk datavoorbeeld typeert de gebruikte CSOR-concepten met hun CSOR-klasse: `csor:ParameterAspect`,
  `csor:Eenheid`, `csor:KwantificeerbaarAspect`. Omdat CSOR zelf de SOSA-klasse niet toekent,
  krijgen parameteraspecten daarnaast `sosa:Property` (met label).
- De CSOR-ontologie (klassen en properties) staat in de pipeline
  (`src/main/resources/be/vlaanderen/omgeving/data/ns/csor/csor.ttl`), en het
  waterkwaliteit-vocabularium importeert ze (`owl:imports`).
- **Vraag aan CSOR (C1):** kan `csor:ParameterAspect` ⊂ `sosa:Property` in de CSOR-ontologie? In
  afwachting staat die alignering in de ontwerpversie van het waterkwaliteit-vocabularium.

*Detail: `codelijsten.md` §3.2; alle `bespreking.md` §5.*

### A2. Eenheid: de CSOR-eenheid, met QUDT via SKOS-mapping

**Vraag.** Verwijst `qudt:hasUnit` naar de CSOR-eenheid of rechtstreeks naar een QUDT-eenheid?

**Voorstel.** Naar de **CSOR-eenheid**. QUDT is bereikbaar via de `skos:exactMatch`/`broadMatch`
in CSOR.

```turtle
ex:resultaat-16231-P_1228 qudt:numericValue 0.59 ; qudt:hasUnit csor-eenheid:E_131 .
# E_131 "milligram fosfor per liter"  skos:broadMatch unit:MilliGM-PER-L
```

**Waarom.**
- Van de 25 gebruikte eenheden hebben er 9 enkel een `broadMatch` (stofgekwalificeerd: `mgN/L`,
  `mgP/L`, `µg/kg ds`, …) en 3 geen QUDT-tegenhanger (`/100mL`, `meq/L`, Franse
  hardheidsgraden). Rechtstreeks QUDT zou het "als N/P" verliezen of onmogelijk zijn.
- CSOR legt dat vast via `csor:uitgedruktIn` en een interne `skos:broader`.

**Verworpen alternatief.** Rechtstreeks QUDT, zoals regel R3 van dit project en RIE-IEPR nu
doen.

**Gevolg.** Dit wijkt af van R3 en van RIE-IEPR. Afstemmen (C4).

*Detail: `codelijsten.md` §3.3.*

### A3. Resultaat onder de rapportagegrens (`<`)

**Vraag.** Hoe modelleer je "< 0.0125 µg/L"?

**Voorstel.** Geen `qudt:numericValue`, maar het interval dat de VMM zelf aanlevert:

```turtle
ex:resultaat-16231-P_813 qudt:lowerBound 0.0 ; qudt:upperBound 0.0125 ; qudt:hasUnit csor-eenheid:E_4 .
```

**Waarom.**
- `250108` levert elk resultaat al als interval (ondergrens/bovengrens): `[v, v]` bij `=`,
  `[0, X]` bij `<`.
- Een `numericValue` gelijk aan X zou een meting suggereren die er niet is.
- Het teken is afleidbaar (wel of geen `numericValue`), zonder aparte codelijst.
- De omvang is groot: 1605 van de 1998 afvalwaterresultaten en 834 van de 999
  oppervlaktewaterresultaten.

**Verworpen alternatieven.**
- `numericValue` = grens + een tekencodelijst.
- Een tweede observatie met het CSOR kwalificeerbaar aspect "Aantoonbaarheid".

**Open.** De **aantoonbaarheids- en bepaalbaarheidsgrens** zelf (per resultaat in `250108`)
staan nog niet in het model.
- Kandidaat: `ssn-system:DetectionLimit`. Die module is niet geladen, en de grenzen variëren per
  staal, niet per labo.
- Alternatief: eigen eigenschappen op het resultaat.
- Eerst de betekenis bevestigen (V2).

*Detail: `nieuw_model/afvalwater_concentraties/bespreking.md` §6.4.*

### A4. FOI van een concentratie: het staal, de lozing als ultiem FOI

**Vraag.** Is het FeatureOfInterest van een analyse het staal of de lozing?

**Voorstel.** Het **staal** (`sosa:Sample`) als FOI. De **lozing** is
`sosa:hasUltimateFeatureOfInterest`. Het staal is het resultaat van een `sosa:Sampling`.

```turtle
ex:sampling-16231 a sosa:Sampling ; sosa:hasFeatureOfInterest ex:lozing-2800028 ;
    sosa:usedProcedure procedure:WAC_I_A_003_2024 ; sosa:hasResult ex:staal-16231 .
ex:staal-16231 a sosa:Sample ; sosa:isSampleOf ex:lozing-2800028 .
ex:collectie-16231 sosa:hasFeatureOfInterest ex:staal-16231 ;
    sosa:hasUltimateFeatureOfInterest ex:lozing-2800028 .
```

**Waarom.**
- De analyse gebeurt op het staal.
- Het staal draagt de soort monstername, de staalnemer en het tijdstip.
- Eén staal levert tientallen parameters en dus een natuurlijke `ObservationCollection`.
- De lozing blijft bereikbaar via `hasUltimateFeatureOfInterest`.

**Verworpen alternatief.** FOI = de lozing rechtstreeks, zoals RIE-IEPR: FOI = exact één
`riepr:Emissie`.

**Gevolg.** Dit is een **afwijking van RIE-IEPR**, waar het FOI van een observatie de Emissie
is (of Onttrekking, Verbruik, Productie). De huidige restrictie in `riepr.ttl` eist sinds een
opschoning in juli enkel nog `some sosa:FeatureOfInterest`. Dat is vermoedelijk onbedoeld en geen
ontwerpkeuze (C4.1). RIE-IEPR moet dus expliciet beslissen of een `sosa:Sample` met ultiem FOI =
Emissie toegelaten wordt (C4.4).

*Detail: `featureofinterest.md` §2.4; `nieuw_model/afvalwater_concentraties/bespreking.md` §6.1.*

### A5. De lozing is tijdsloos; de matrix staat op het FOI

**Vraag.** Hoort de periode (bv. "lozing in 2023") of de matrix (afvalwater) bij het FOI of bij
de eigenschap?

**Voorstel.**
- De lozing is **tijdsloos**; de periode staat in `sosa:phenomenonTime`.
- De matrix staat als `dct:type matrix:afvalwater` op het FOI (lozing, staal).
- De eigenschap blijft het CSOR-parameteraspect zoals het is.

```turtle
ex:lozing-2400006 a sosa:FeatureOfInterest, prov:Entity ; dct:type matrix:afvalwater .
ex:collectie-jaardebieten-2023 sosa:phenomenonTime ex:periode-2023 .
```

**Waarom.**
- `phenomenonTime` is per definitie de tijd waarop het resultaat op het FOI van toepassing is.
  Een FOI per periode legt de tijd dubbel vast, en versnippert de observaties van een lozing.
- RIE-IEPR modelleert `riepr:Emissie` ook tijdsloos.
- CSOR houdt drager (grof: `water`) en matrix bewust gescheiden. Een samengestelde eigenschap
  "parameteraspect + matrix" zou een onbeheerd parallel register naast CSOR worden.
- Resultaat: 1619 lozingen verzamelen hun concentraties, debieten en vrachten op één IRI.

**Zie ook A14:** de lozing wordt een `wk:Emissie`, en de eigenschap `wk:periode` van het huidige
AP vervalt.

**Verworpen alternatieven.**
- FOI "lozing in periode X".
- Een samengestelde observedProperty `[PAS_1838 + afvalwater]`.

*Detail: `nieuw_model/afvalwater_concentraties/bespreking.md` §6.8.*

### A6. Meetplaats oppervlaktewater: ruimtelijk monster van de VHA-waterloop

**Vraag.** Wat is het studieobject van een meting in oppervlaktewater?

**Voorstel.** De keten **staal → meetplaats → VHA-waterloop**:
- de meetplaats is `sosa:Platform + sosa:FeatureOfInterest + sosa:SpatialSample`, en
  `sosa:isSampleOf` de VHA-waterloop;
- de waterloop (VHA-gewestcode) is het ultieme FOI;
- de meetplaats is het resultaat van een eigen `sosa:Sampling`: de keuze van de meetplaats op de
  waterloop.

```turtle
ex:meetplaats-OW12000 a sosa:Platform, sosa:FeatureOfInterest, sosa:SpatialSample ;
    sosa:isSampleOf waterloop:2801 ; sosa:isResultOf ex:sampling-meetplaats-OW12000 .
```

**Waarom.**
- R8 en R11: de meetplaats vertegenwoordigt de waterloop.
- Een segment is enkel een geometrisch aanknopingspunt.
- Het KRW-waterlichaam is het beoordelingsobject (fase 2).

**Te beslissen.**
- Referentie voor **stilstaand water** (De Nekker, Blaarmeersen: geen VHA-waterloop): de
  KRW-waterlichamen of de VHA-plassen?
- Behandeling van **grensoverschrijdende meetplaatsen**: `OW12000` ligt in Philippine (NL) aan het
  Leopoldkanaal.

*Detail: `featureofinterest.md` §3; `nieuw_model/oppervlaktewater_concentraties/bespreking.md` §6.1–6.5.*

### A7. Wanneer observaties koppelen; afgeleide observaties

**Vraag.** Koppel je observaties aan elkaar, bijvoorbeeld een concentratie en een debiet van
dezelfde lozing en hetzelfde jaar?

**Voorstel.**
- **Geen** koppeling op basis van plaats en tijd alleen: dat verband volgt uit FOI +
  `phenomenonTime`.
- **Wel** waar het ene resultaat van het andere afhangt:

| Situatie | Koppeling |
|---|---|
| berekening (vracht = concentratie × debiet) | `sosa:hasInputValue` op de vracht naar de **resultaten** van de bronobservaties (de waarden), `sosa:relatedObservation` naar de bronobservaties zelf. De `sosa:usedProcedure` declareert de abstracte inputs met `sosa:hasInput` (CSOR kwantificeerbare aspecten). De vracht is geen lid van de collectie van de bronnen. |
| context bij één staalname (debiet tijdens een debietgebonden staalname) | `sosa:relatedObservation` van de `sosa:Sampling` naar de debietobservatie |

```turtle
ex:observatie-brutovracht-bedrijven-rio-2014-P_117
    sosa:usedProcedure ex:procedure-bruto-vracht ;
    sosa:hasInputValue      ex:resultaat-concentratie-bedrijven-rio-2014-P_117 ,
                            ex:resultaat-debiet-bedrijven-rio-2014 ;
    sosa:relatedObservation ex:observatie-concentratie-bedrijven-rio-2014-P_117 ,
                            ex:observatie-debiet-bedrijven-rio-2014 .
ex:procedure-bruto-vracht sosa:hasInput csor-kwa:KWA_1 , csor-kwa:KWA_10 ; sosa:hasOutput csor-kwa:KWA_5 .
```

**Waarom.**
- SOSA 2023: `hasInputValue` "assigns a value to an input defined by the Procedure" en "MUST be
  consistent with a hasInput definition from the corresponding Procedure". Een inputwaarde is dus
  een waarde (`wk:Meetresultaat`). Een observatie is een activiteit (`sosa:Execution ⊂
  prov:Activity`), en een activiteit als inputwaarde is betekenisloos. De band met de
  bronobservatie loopt via `sosa:relatedObservation` ("relation from an Execution … to an
  Observation"). Dit wijkt af van het eerdere projectpatroon (paleo, R7/R13 in CLAUDE.md,
  bijgewerkt 2026-10-01).
- R5 en R13.
- De afhankelijkheid is de betekenisvolle relatie. Links op basis van plaats en tijd zouden
  honderden relaties per staal opleveren zonder extra betekenis.

*Detail: `stappenplan.md` stap 4; `nieuw_model/afvalwater_vrachten/bespreking.md` §6.1–6.2.*

### A8. Groep van lozingen als FOI

**Vraag.** Wat is het FOI van een vracht per categorie lozer × type meetput (`251013`)?

**Voorstel.** Een eigen, tijdsloos FOI per groep, bv. `ex:lozingsgroep-bedrijven-rio` "lozingen
van bedrijven via riool". De leden zijn niet gekend.

**Te beslissen.**
- Moet de groep een verzameling van lozingen worden (met leden) zodra de VMM die kan leveren?
- Moeten de indelingscriteria (categorie lozer, meetputtype) codelijsten worden (A11)?

*Detail: `nieuw_model/afvalwater_vrachten/bespreking.md` §6.4.*

### A9. Meetput, staalnemer en databron

**Voorstel.**

| Element | Model | In plaats van |
|---|---|---|
| meetput (controle-inrichting) | `sosa:System` via `sosa:Sampler` (staalname), met agency zoals in RIE-IEPR; `sosa:Sensor` + `madeBySensor` alleen als de bron vermeldt dat de meetput mat; `prov:Location` (plaats van een debiet); `rdfs:seeAlso` naar het RIE-IEPR-meetpunt (A15.5) | een passieve plaats waar iets of iemand anders meet |
| wie het staal nam (VMM/bedrijf) | `prov:wasAssociatedWith` op de `sosa:Sampling` | een codelijst "herkomst staal" |
| databron van een jaardebiet (IMJV/MNT) | `prov:used` op de observatie (R5) | een codelijst "databron" |
| labo, analysemethode | niet ingevuld: niet in de bron | illustratieve waarden |

**Te beslissen.** Beide zijn verenigbaar: de meetput is een systeem (A15.5). `madeBySampler` →
meetput voor een staalname; `madeBySensor` → meetput voor een meting, wanneer de bron zegt dat
de meetput mat (dan is de meetput ook `sosa:Sensor`, zoals SOSA 2023 met `schema:rangeIncludes
sosa:Sensor` verwacht). Open: moet de VMM-data dat onderscheid leveren (C4)?

*Detail: `nieuw_model/afvalwater_concentraties/bespreking.md` §6.3, §6.6;
`nieuw_model/afvalwater_debieten/bespreking.md` §6.3–6.4.*

### A10. Procedures: compendium, jaarversies, soort procedure

**Voorstel.**
- De staalname verwijst naar de **jaarversie** van de compendiumprocedure die gold in het jaar van
  de staalname: `procedure:WAC_I_A_003_2024`, met `dct:isVersionOf` naar `WAC_I_A_003`.
- Een berekening heeft een eigen `sosa:ObservingProcedure` met `hasInput`/`hasOutput` (A7).

**Te beslissen.**
- Is de jaarversie het juiste niveau, of volstaat de hoofdprocedure?
- De VITO-lijst typeert alles als `sosa:Procedure`. Het onderscheid `sosa:SamplingProcedure` /
  `sosa:ObservingProcedure` komt nu uit de voorbeelden. Hoort het in de lijst (C2)?

*Detail: `nieuw_model/afvalwater_concentraties/bespreking.md` §5.*

### A11. Codelijsten: hergebruik tegenover nieuw

**Voorstel.**
- **Hergebruiken:** CSOR (10 lijsten), `codelijst-matrix`, `codelijst-observatieprocedure` (met
  de VITO-jaarversies), NACE-BEL **2008** (dat is de versie in de data), VHA-waterlopen (bekken,
  categorie, beheerder).
- **Nieuw, in fase 3, in `codelijst-rie-iepr`:**
  - meetputtype (uitbreiding van de lozingsplaats-lijst: collector, kunstmatige afvoer
    hemelwater, influent RWZI);
  - soort afvalwater;
  - DWA/RWA;
  - lozingswijze;
  - positie in de zuivering;
  - categorie lozer;
  - VMM-sectorindeling (JV/EIW) met `skos:narrowMatch` naar NACE-BEL 2008.
- **Geen codelijst:** herkomst staal en databron (A9); het resultaatteken (A3).

**Te beslissen.** De verdeling tussen hergebruik en nieuw, en waar de nieuwe lijsten beheerd
worden.

*Detail: `codelijsten.md` §4–5; `stappenplan.md` §2.*

### A12. IRI-strategie en namespaces

**Stand.** De voorbeelden gebruiken `https://example.org/waterkwaliteit/…` voor eigen instanties
(R10). Bestaande IRI's worden hergebruikt: CSOR, NACE-BEL, VHA-waterloop, matrix,
observatieprocedure, en RIE-IEPR-meetpunten via `rdfs:seeAlso`. De sleutels voor de IRI's komen
uit de VMM-data: meetputnummer, `Sample ID`, exploitatie-ID.

**Open.**
- De namespace voor observaties, stalen en lozingen.
- De verhouding tot de RIE-IEPR-IRI's (`https://data.mjv.omgeving.vlaanderen.be/id/…`, nu nog
  "niet finaal").
- Versionering van IRI's zoals RIE-IEPR (`{uuid}/{issued}/{created}`) of stabiele IRI's op basis
  van de VMM-sleutels.

### A13. Kenmerken die in de tijd veranderen

**Vaststelling.** De exploitant van een lozing wisselt in de tijd. In `240426` hebben 3
meetputten meerdere exploitantnamen (meetput `2030042`: Antwerp Waste Management in 2009, Veolia
ES MRC vanaf 2017), en voor 11 verschilt de naam met `250129`. In de PFAS-voorbeelden staat de naam
daarom op de observatie van dat jaar.

**Open (fase 3).** Versies van een lozing (`dct:isVersionOf`/`prov:specializationOf`, zoals
RIE-IEPR voor structurele elementen), of een toekenning met een geldigheidsperiode.

### A14. `wk:Emissie` als subklasse van `prov:Entity`

**Beslissing (projectteam, 2026-09-30; ter bevestiging in het OSLO-traject).** De klasse
`https://data.vlaanderen.be/ns/waterkwaliteit#Emissie` wordt in de nieuwe versie geherdefinieerd
als subklasse van `prov:Entity`. In het huidige AP (kandidaatstandaard 2023-06-01) is het een
subklasse van `Object` (`gfi:GFI_Feature`, uit de verwijderde ISO-namespace;
`bestaand_model/bestaand_model.md` §3.6). De IRI blijft; de betekenis verschuift van een
"object" naar een entiteit die het resultaat is van een proces (PROV).

**Waarom dit past.**
- Dezelfde keuze als `riepr:Emissie` (⊂ `prov:Entity`, `sosa:FeatureOfInterest`).
- Dezelfde keuze als de lozing in de datavoorbeelden (`ex:lozing-<nr>` a `prov:Entity`,
  `sosa:FeatureOfInterest`).
- De verwijzing naar de verwijderde ISO-klasse `GFI_Feature` verdwijnt (het probleem uit
  `bestaand_model.md` §4.1).

**Deelpunten, open.**

| # | Vraag | Voorstel |
|---|---|---|
| A14.1 | Ook `rdfs:subClassOf sosa:FeatureOfInterest`? | **Ja**, zoals `riepr:Emissie`. Een emissie is in dit model altijd het (ultieme) FOI van metingen. SOSA 2023 kent voor `hasFeatureOfInterest` enkel `rangeIncludes`, dus de FOI-rol volgt niet automatisch uit het gebruik. En SHACL zonder inferentie vraagt de expliciete klasse. |
| A14.2 | Verhouding tot `riepr:Emissie` | Eén begrip, twee IRI's vermijden. Voorstel: `riepr:Emissie rdfs:subClassOf wk:Emissie`. De RIE-IEPR-emissie is de specialisatie met een verplicht proces (`prov:wasDerivedFrom` een `riepr:Proces`). `wk:Emissie` is het algemene begrip, ook voor lozingen zonder gekende procesketen (VMM-data, groepen van lozingen). Alternatief: `owl:equivalentClass`, maar dan geldt de procesverplichting ook voor `wk:Emissie`. |
| A14.3 | `wk:periode` (0..*, `TM_Period`) | **Vervalt.** De emissie is tijdsloos (A5); de tijd staat in `sosa:phenomenonTime` van de observaties. Moet het bestaan van een emissie begrensd worden, dan kunnen `prov:generatedAtTime`/`prov:invalidatedAtTime` of versies (A13) dat doen. |
| A14.4 | `wk:matrix` (0..*, `skos:Concept`) | Vervangen door `dct:type` naar `codelijst-matrix` (A5), of behouden als `rdfs:subPropertyOf dct:type`. |
| A14.5 | `dct:type` (EmissieType) | Behouden. Nagaan of de RIE-IEPR-lijst `emissie_type` (geleid, niet-geleid, abnormaal, lekverlies, …) de VMM-typering dekt, in plaats van een eigen EmissieType-lijst. |
| A14.6 | `wk:uitgestotenDoor` → `wk:Emissiebron` | Aligneren met PROV zoals RIE-IEPR: `prov:wasDerivedFrom` het (emissie)proces dat door het emissiepunt uitgevoerd wordt, en `prov:wasAttributedTo` de exploitant. Te beslissen: blijft `wk:Emissiebron` een eigen klasse, of valt ze samen met `riepr:Emissiepunt`/`riepr:Installatie`? |
| A14.7 | Definitie: een emissie is **geen handeling** | **Beslist (projectteam, 2026-09-30).** `prov:Activity` en `prov:Entity` zijn disjunct (PROV-O), en "uitstoot of lozing" leest als een handeling. `wk:Emissie` is daarom expliciet **wat de handeling oplevert**: gegenereerd door een activiteit (`prov:wasGeneratedBy some prov:Activity`), het resultaat van een actuatie (`sosa:isResultOf some sosa:Actuation`) en afgeleid van een proces (`prov:wasDerivedFrom some sosa:Procedure`). De restricties hebben `owl:minCardinality 0`: ze definiëren de klasse, maar zijn niet verplicht in de data zolang activiteit en proces niet gekend zijn (VMM-data). |
| A14.8 | Reikwijdte van de definitie | **Verbreed (projectteam, 2026-09-30).** Niet enkel "via een emissie- of lozingspunt": de definitie dekt **geleide** emissies (schoorsteen, lozing van afvalwater), **niet-geleide** emissies (lekverliezen, opslag- en overslagverliezen, fakkel) en **diffuse** emissies (landbouw: sproeien van gewasbeschermingsmiddelen, bemesting; uitstoot van dieren). **Geen afbakening van "wat"** in de definitie: "stoffen" is zelf moeilijk af te bakenen (micro-organismen, warmte, groepsparameters, fysische eigenschappen). Wat vrijkomt en hoeveel, beschrijven de observaties (`observedProperty` = CSOR-parameteraspect; CSOR beheert de variabelen). Definitie: "Wat door een bron of activiteit in de omgeving (lucht, water of bodem) terechtkomt, beschouwd als entiteit: het resultaat van het uitstoten, lozen, weglekken of verspreiden, niet die handeling zelf. Wat er vrijkomt en in welke hoeveelheid, beschrijven de observaties van de emissie; de geobserveerde eigenschap is een CSOR-parameteraspect." Typering met `dct:type`; de RIE-IEPR-lijst `emissie_type` dekt geleid/niet-geleid/abnormaal, maar **geen diffuse bronnen**. De vraag "enkel stoffen of ook warmte, geluid, trillingen (IED)" wordt zo geen vraag over de definitie, maar over welke CSOR-parameteraspecten op een emissie geobserveerd worden. |
| A14.9 | Kloppen de restricties van A14.7 nog voor de bredere reikwijdte? | **Open.** `prov:wasGeneratedBy some prov:Activity` geldt voor elke emissie (lekken bij opslag, bemesten, dieren houden zijn activiteiten). `sosa:isResultOf some sosa:Actuation` en `prov:wasDerivedFrom some sosa:Procedure` beweren in OWL dat **elke** emissie het resultaat is van een actuatie en afgeleid van een proces. Voor een lekverlies (onbedoeld) of de uitstoot van dieren is dat twijfelachtig: een actuatie is een bedoelde handeling om de toestand te wijzigen. Voorstel: `wasGeneratedBy some prov:Activity` behouden; voor actuatie en proces overschakelen naar `owl:allValuesFrom` ("*als* een emissie het resultaat is van een uitvoering, dan van een actuatie"), of beide enkel in de toelichting laten. |

**De volledige keten (A14.7), met het RIE-IEPR-voorbeeld van AGC Glass Mol.** De handeling
(de actuatie) en haar resultaat (de emissie) zijn gescheiden:

```turtle
<…/proces/019e9271-1475-…>  a riepr:Proces ;                 # "Proces emissiepunt LP01" (⊂ sosa:Procedure)
    ssn:implementedBy <…/emissiepunt/019e9271-145b-…> .      # lozingspunt LP01 (voert de actuatie uit)

ex:lozing-actuatie-2400006-2023 a sosa:Actuation ;           # de handeling: lozen in 2023 (⊂ prov:Activity)
    sosa:usedProcedure <…/proces/019e9271-1475-…> ;
    sosa:madeByActuator <…/emissiepunt/019e9271-145b-…> ;
    sosa:hasResult ex:lozing-2400006 .

ex:lozing-2400006 a wk:Emissie ;                             # het resultaat (⊂ prov:Entity)
    prov:wasGeneratedBy ex:lozing-actuatie-2400006-2023 ;
    sosa:isResultOf ex:lozing-actuatie-2400006-2023 ;
    prov:wasDerivedFrom <…/proces/019e9271-1475-…> ;
    sosa:isFeatureOfInterestOf ex:observatie-jaardebiet-2400006-2023 .
```

Open bij deze keten:
- Is de actuatie per periode (bv. per jaar), terwijl de emissie tijdsloos blijft? Of genereert
  één doorlopende actuatie de emissie?
- Is het lozingspunt de `sosa:Actuator`? In RIE-IEPR is het nu een `ssn:System` dat het proces
  implementeert.
- De koppeling tussen VMM-meetput en lozingspunt moet machineleesbaar worden (C4.4).

**Gevolg voor de datavoorbeelden (doorgevoerd 2026-09-30).**
- De ontwerpversie van het vocabularium staat in
  `src/main/resources/be/vlaanderen/data/ns/waterkwaliteit/waterkwaliteit.ttl`: `wk:Emissie` ⊂
  `prov:Entity`, `sosa:FeatureOfInterest`, met de definitie en de drie restricties van A14.7.
- Alle lozingen (stap 1, 3 en 4) en de groepen van lozingen hebben `a wk:Emissie`. Na
  samenvoegen zijn dat 1624 emissies, conform SHACL.
- De actuatie en het proces staan nog niet in de voorbeelden. De VMM-data bevat ze niet; ze
  komen er bij de koppeling met RIE-IEPR (C4.2).

### A15. Applicatieprofiel: ontologie en SHACL uit één bron

**Doel.** `src/main/resources/be/vlaanderen/data/ns/waterkwaliteit/waterkwaliteit.ttl` bevat de
nieuwe waterkwaliteitontologie en is tegelijk de bron van het applicatieprofiel dat het AP
Waterkwaliteit (kandidaatstandaard 2023-06-01) vervangt. De pipeline (`OwlToShaclGenerator`)
zet de OWL-restricties om naar SHACL in `src/main/resources/generated-shapes.ttl`. Er is geen
apart, met de hand onderhouden SHACL-bestand.

**Omzetting OWL → SHACL.**

| OWL-restrictie | SHACL |
|---|---|
| `owl:someValuesFrom C` | `sh:class C` (of `sh:datatype`) + `sh:minCount 1` |
| `owl:allValuesFrom C` | `sh:class C` (of `sh:datatype`), niet verplicht |
| `owl:maxCardinality n` | `sh:maxCount n` |
| `owl:unionOf ( A B )` als waarde | `sh:or ( [sh:class A] [sh:class B] )` |
| `owl:minCardinality 0` op een property | een `someValuesFrom` op die property wordt niet verplicht (C1) |

Alle restricties van een klasse op hetzelfde pad worden samengevoegd tot **één** property shape
(grootste minimum, kleinste maximum, alle waardebeperkingen). Het AP 2023 had per eigenschap twee
property shapes (`bestaand_model.md` §3).

**Keuze: eigen wk-subklassen, geen restricties op de SOSA-klassen.** Een restrictie op
`sosa:Observation` geldt voor alle SOSA-data: voor de andere voorbeelden in dit project, en voor
elk ander profiel dat SOSA hergebruikt. De AP-beperkingen staan daarom op wk-subklassen. Data
typeert de wk-klasse én de SOSA-superklassen expliciet, omdat SHACL het niet-afgeleide model
valideert.

Verworpen alternatief: de beperkingen direct op de SOSA-klassen zetten, zoals OSLO-AP's
gewoonlijk doen. In een afzonderlijk gepubliceerd AP kan dat. In dit project valideert één
SHACL-bestand alle voorbeelden, en ook in een gepubliceerd AP maakt een subklasse duidelijk welke
data het profiel volgt. *Te beslissen in de werkgroep.*

| Klasse | Superklassen | Kernbeperkingen |
|---|---|---|
| `wk:WaterkwaliteitObservatie` | `sosa:Observation` | FOI 1..1; `observedProperty` 1..1 → `csor:ParameterAspect`; `hasResult` 1..1 → `wk:Meetresultaat`; `phenomenonTime` 0..1 → Instant ∪ Interval; `resultTime` 0..1; `usedProcedure` 0..1; `madeBySensor` 0..* (aanbevolen); `hasInputValue`, `relatedObservation` → `sosa:Observation`; `prov:used` → `prov:Entity`; `prov:atLocation` → `prov:Location` |
| `wk:WaterkwaliteitObservatieVerzameling` | `sosa:ObservationCollection` | `hasMember` 1..* → `wk:WaterkwaliteitObservatie`; FOI, ultiem FOI, `observedProperty`, `phenomenonTime` elk 0..1 |
| `wk:Meetresultaat` | `sosa:Result` | `qudt:hasUnit` 1..1 → `csor:Eenheid`; `numericValue`, `lowerBound`, `upperBound` 0..1 `xsd:decimal` |
| `wk:Staal` | `sosa:Sample` | `isSampleOf` 1..*; `isResultOf` 1..1 → `sosa:Sampling`; `dct:type` → `skos:Concept` (matrix) |
| `wk:Staalname` | `sosa:Sampling` | FOI 1..1; `hasResult` 1..* → `wk:Staal`; `madeBySampler` 0..1; `usedProcedure` 0..1 → `sosa:SamplingProcedure` |
| `wk:Meetplaats` | `sosa:SpatialSample`, `sosa:Platform`, `geo:Feature` | `isSampleOf` 1..* → `waterlopen:VhaWaterloopobject` (A15.6); `geo:hasGeometry` 1..1 |
| `wk:Meetput` | `sosa:Sampler`, `prov:Location`, `geo:Feature` | `adms:identifier`; `geo:hasGeometry` 0..1 |
| `wk:Meetnet` | `sosa:SampleCollection` | `hasMember` 1..* → `wk:Meetplaats` (nog niet in de voorbeelden) |
| `wk:Emissie` | `prov:Entity`, `sosa:FeatureOfInterest` | A14; `dct:type` → `skos:Concept`; `prov:wasAttributedTo` → `prov:Agent`; `dct:identifier` 0..1 |

**UML.** `waterkwaliteit_uml.mmd` (Mermaid) en `waterkwaliteit_uml.svg` tonen de klassen, overerving
en eigenschappen met hun multipliciteit, zoals de gegenereerde SHACL ze afdwingt. Ze worden
gegenereerd uit `waterkwaliteit.ttl` met `scripts/ontologie_naar_uml.py`.

**Mapping AP 2023 → nieuw profiel.**

| AP 2023 | Nieuw profiel |
|---|---|
| Observatie (`om:OM_Observation`), Meting | `wk:WaterkwaliteitObservatie` |
| ChemischAgensConcentratieObservatie, ChemischAgensVrachtObservatie, WaterkwaliteitParameterObservatie, BiotischeIndexObservatie, BioIndicatorObservatie, HydromorfologischeIndexObservatie | `wk:WaterkwaliteitObservatie`. Het soort observatie volgt uit het CSOR-parameteraspect (A1). Agens en soort zitten in de CSOR-variabele. |
| StatistischeObservatie | afgeleide `wk:WaterkwaliteitObservatie`: `sosa:hasInputValue` naar de bronresultaten, `sosa:relatedObservation` naar de bronobservaties (A7) |
| eigen resultaatproperties per subklasse (`iso19103:Measure`) | `sosa:hasResult` → `wk:Meetresultaat` (A2, A3) |
| WaterkwaliteitObservatieVerzameling | zelfde IRI, als `sosa:ObservationCollection` |
| GeobserveerdWeer, refGeobserveerdWeer | vervalt; weer als observatie, gekoppeld met `sosa:relatedObservation` |
| Meetpunt (`ssf:SF_SpatialSamplingFeature`) | `wk:Meetplaats` (oppervlaktewater) of `wk:Meetput` (afvalwater) |
| Meetnet (`sf:SF_SamplingFeatureCollection`) | zelfde IRI, als `sosa:SampleCollection` |
| WaterObject (`water:WaterFeature`) | `waterlopen:VhaWaterloopobject` ⊂ `sosa:FeatureOfInterest`, met subklassen `waterlopen:Vhag`, `waterlopen:Wlas`, `waterlopen:VhaCattraj` (A15.6, C3) |
| Emissie (⊂ Object) | `wk:Emissie` ⊂ `prov:Entity`, `sosa:FeatureOfInterest` (A14) |
| `wk:matrix`, `wk:periode` op Emissie | `dct:type` → codelijst-matrix (A5); periode in `sosa:phenomenonTime` van de observatie |
| Emissiebron, `wk:uitgestotenDoor`, `wk:ontvanger` | **open**: via A14.7 (`prov:wasGeneratedBy` een activiteit, uitgevoerd door een installatie; zie RIE-IEPR C4). Voorlopig geen wk-klasse. |
| `uitgevoerdMetSensor` 1..1 | `sosa:madeBySensor`, aanbevolen (0..*) |
| `fenomeentijd`, `resultaattijd` 1..1 (ISO 19108) | `sosa:phenomenonTime` 0..1 (OWL-Time; mag op de verzameling), `sosa:resultTime` 0..1 |
| codelijst-shapes (`sh:targetClass skos:Concept`) | CSOR (parameteraspect, eenheid), codelijst-matrix, VITO-compendium (A10, A11) |

**Wat de generator niet uitdrukt.**
- "`numericValue` óf `upperBound`" op een meetresultaat (een keuze tussen properties).
- Consistentie tussen verzameling en leden (SOSA 2023: waarden op de verzameling gelden voor
  alle leden).
- Labels en definities van properties in de AP-context (`sh:name`, `sh:description`).

Wil de werkgroep die toch in de SHACL, dan komt er een uitbreiding van de generator of een klein,
met de hand onderhouden aanvullend bestand.

**Open.**
- A15.1: wk-subklassen (voorstel) of restricties op de SOSA-klassen?
- A15.2: Emissiebron: wk-klasse, of verwijzing naar de RIE-IEPR-installatie?
- A15.3: `wk:Meetpunt` uit het AP 2023 vervalt ten voordele van `wk:Meetplaats` en `wk:Meetput`.
  Of blijft het als gemeenschappelijke superklasse?
- A15.4: `sosa:phenomenonTime` op de observatie verplicht maken wanneer de verzameling ze niet
  draagt (niet uit te drukken met klasse-restricties).
- A15.5: **meetput als systeem, meetplaats niet.** Voorstel:
  - *Meetput.* Een meetput is geen gat in de grond. Het is een verplichte controle-inrichting
    (VLAREM) met meetgoot, debietmeter en eventueel een staalnameautomaat. Dat is infrastructuur
    die een procedure uitvoert, en precies waarvoor `sosa:System` bedoeld is.
    - Via `sosa:Sampler ⊂ sosa:System ⊂ prov:Agent, prov:Entity` heeft de meetput agency, zoals
      de systemen in RIE-IEPR.
    - SSN beschrijft systemen op elk abstractieniveau (`sosa:hasSubSystem`). Een meting kan dus
      aan de meetput als geheel worden toegeschreven, ook als het onderdeel niet bekend is.
    - Een meetput die zelf meet, is ook `sosa:Sensor` (`madeBySensor`), maar enkel als de bron dat
      vermeldt. Een IMJV-jaardebiet is een aangifte (`prov:used`), dus daar blijft
      `prov:atLocation` het minimum.
  - *Meetplaats.* De meetplaats blijft `sosa:SpatialSample` + `sosa:Platform`, zonder
    `sosa:System`.
    - Ze staat aan de geobserveerde kant; als systeem zou ze waarnemer van zichzelf worden.
    - Een meetstation op een meetplaats is een apart `sosa:System`/`sosa:Sensor`, gehost door de
      meetplaats (`sosa:hosts`).
  - *Verworpen alternatieven:* de meetput als passieve plaats (`sosa:Platform`, geen agent), en
    de meetplaats als systeem.
- A15.6: **VHA-waterlopen in het profiel.** Voorstel:
  - Het waterlopen-vocabularium krijgt een gemeenschappelijke superklasse
    `waterlopen:VhaWaterloopobject`. Daaronder vallen `waterlopen:Vhag` (waterloop),
    `waterlopen:Wlas` (waterloopsegment) en `waterlopen:VhaCattraj` (categorietraject).
  - `waterkwaliteit.ttl` importeert het vocabularium en aligneert die superklasse:
    `waterlopen:VhaWaterloopobject` ⊂ `sosa:FeatureOfInterest`. Die alignering hoort op termijn in
    het waterlopen-vocabularium zelf, zoals C1 voor CSOR.
  - `wk:Meetplaats`: `sosa:isSampleOf` alleen naar een VHA-waterloopobject (`owl:allValuesFrom
    waterlopen:VhaWaterloopobject` → `sh:class`). Dat vervangt de eerdere `owl:unionOf` van de drie
    klassen: een nieuwe VHA-klasse valt er vanzelf onder, als ze subklasse van het waterloopobject
    is.
  - De data typeert de waterloop als `waterlopen:Vhag` en, expliciet voor de SHACL-validatie op het
    niet-afgeleide model, ook als `waterlopen:VhaWaterloopobject`. Ze krijgt de volledige VHA-beschrijving (label,
    lengte, geometrie) uit `waterlopen/waterlopen_meetplaatsen.ttl`, zodat ze ook aan de VHA-shape
    voldoet.
  - Ze zijn ook `geo:Feature`, met de geometrie via `geo:hasGeometry` (zie C3).
  - Open: een meetplaats in een KRW-waterlichaam (D2), een stilstaand water of een kustwater past
    nog niet. Een klasse daarvoor moet dan ook onder de superklasse vallen, of de restrictie moet
    ruimer worden. Of kiest de werkgroep
    liever een ruimer bereik (`sosa:FeatureOfInterest`), met de VHA-klassen enkel als aanbeveling?

- A15.7: **hoe smal mag het bereik van een restrictie zijn?** Een wk-subklasse als bereik
  (`owl:allValuesFrom wk:Staal` i.p.v. `sosa:Sample`) wordt in de SHACL `sh:class wk:Staal`. De
  data moet het object dan expliciet zo typeren; validatie gebeurt op het niet-afgeleide model. In
  OWL (open wereld) volgt eruit dat het object een `wk:Staal` *is*, met alle verplichtingen van die
  klasse. Voorstel, als vuistregel:

  | Soort relatie | Bereik | Voorbeelden |
  |---|---|---|
  | binnen het profiel: beide kanten zijn wk-klassen die samen in dezelfde data zitten | de wk-subklasse | `Staalname hasResult wk:Staal`, `Staal isResultOf wk:Staalname`, `Observatie hasResult wk:Meetresultaat`, `Verzameling hasMember wk:WaterkwaliteitObservatie` |
  | naar een gedeeld of extern register | de klasse van dat register, geen eigen subklasse | `observedProperty csor:ParameterAspect`, `hasUnit csor:Eenheid`, `isSampleOf waterlopen:VhaWaterloopobject` |
  | naar iets wat ook van buiten het profiel kan komen | de algemene klasse | `hasFeatureOfInterest`, `hasUltimateFeatureOfInterest`, `usedProcedure`, `madeBySensor`, `prov:wasAttributedTo` |

  - **Toegepast:** `wk:Staal sosa:isResultOf some wk:Staalname` (2026-10-01), want staal en
    staalname zijn een koppel binnen het profiel. Aandachtspunt: een deelstaal uit het labo
    (`sosa:hasOriginalSample`) moet dan ook uit een `wk:Staalname` komen.
  - **Bewust niet toegepast:** `wk:Emissie sosa:hasSample` blijft `owl:allValuesFrom sosa:Sample`,
    niet `wk:Staal`. `wk:Emissie` is een gedeelde klasse: `riepr:Emissie ⊂ wk:Emissie` (A14.2). Een
    versmalling zou elk staal van een RIE-IEPR-emissie, bv. een gasstaal van een schoorsteen,
    verplichten om `wk:Staal` te zijn. `wk:Staal` wordt afgedwongen waar het profiel de staalname
    zelf beschrijft (`Staalname hasResult wk:Staal`).
  - **Niet aan te raden:** een unie van wk-klassen als bereik van `hasFeatureOfInterest`
    (staal, emissie, meetplaats). Elke nieuwe soort studieobject (waterlichaam D2, biota-staal …)
    zou bestaande data ongeldig maken.
  - **Te beslissen in de werkgroep:** is `wk:Emissie` een klasse van dit profiel, of een gedeelde
    klasse waarvoor restricties ook voor RIE-IEPR moeten kloppen? Dezelfde vraag geldt voor elke
    wk-klasse die een ander profiel als superklasse gebruikt.

**Validatie (2026-09-30).** De vier scripts typeren de wk-klassen. Alle vijf subsets zijn conform
in `mvn compile exec:java`, zonder `[VOCAB ERROR]` of `[MODEL INVALID]`. De vijf volledige
`.trig`-bestanden samen (131 124 triples) zijn conform `generated-shapes.ttl`. Een negatieve test
(observatie zonder resultaat, twee FOI's, niet-CSOR-eigenschap, twee waarden) geeft de verwachte
schendingen.

---

## 3. Deel B: vragen aan de VMM

| # | Vraag | Voor |
|---|---|---|
| V1 | Is "debietgebonden monster" hetzelfde als een verzamelmonster (WAC/I/A/004)? Welke andere soorten monstername komen voor? | A10 |
| V2 | Is bij `<` de gerapporteerde waarde de aantoonbaarheids- of de bepaalbaarheidsgrens? In `250108` is ze 1464 keer de aantoonbaarheidsgrens, 139 keer de bepaalbaarheidsgrens en 2 keer iets anders. | A3 |
| V3 | Wat betekent `Bevestiging Code` = `R`? | – |
| V4 | Is `Sample Point Naam` (`AW1850022` → `1850022`) de juiste sleutel naar de meetput, en wat is `Sample Point ID` (`E9992055`)? | A12 |
| V5 | `OW162000` en `OW164000`: Beneden- of Boven-Zeeschelde? | A6 |
| V6 | Welke referentie gebruikt de VMM voor meetplaatsen in stilstaand water? | A6 |
| V7 | Zijn de coördinaten in `250124` (waterbodem) Lambert 2008? | D1 |
| V8 | Volledige waardenlijsten van meetputtype, lozingswijze, DWA/RWA, soort afvalwater, positie in de zuivering | A11 |
| V9 | Wat betekent databron "MNT"? Met welke procedure wordt het debiet bepaald (kandidaat `WAC/I/1/012`)? | A9, A10 |
| V10 | Hoe berekent de VMM een vracht (welke concentraties, welk debiet)? Wat betekent "OG" (ondergrensbenadering?) en "geenInEx"? Wat is het verschil tussen bruto en netto vracht? | A7 |

---

## 4. Deel C: registers en aanpalende projecten

### C1. CSOR (`~/git/csor`)

- **Stand in dit project (2026-09-30).** De CSOR-ontologie (`src/main/resources/be/vlaanderen/omgeving/data/ns/csor/csor.ttl`) bevat
  geen kardinaliteitsrestricties meer, enkel semantische:
  - `cardinality 1`/`minCardinality 1` → `owl:someValuesFrom <bereik>`;
  - `maxCardinality 1` → `owl:allValuesFrom <bereik>`;
  - "hoogstens één" als `owl:FunctionalProperty` (26 CSOR-properties, nagekeken op de actuele
    CSOR-data: 0 schendingen);
  - de restrictie op PubChem-`compound` (zonder bereik) is weggelaten.

  `waterkwaliteit.ttl` herhaalt de existentiële restricties voor `csor:ParameterAspect`,
  `csor:Eenheid` en `csor:KwantificeerbaarAspect` met `owl:minCardinality 0`. `OwlToShaclGenerator`
  leest dat als "niet verplicht in de data": `someValuesFrom` krijgt dan geen `sh:minCount 1`, de
  klassecontrole blijft. Zo verwijzen de voorbeelden naar CSOR-concepten zonder registergegevens
  te dupliceren. **Voorstel aan CSOR:** deze omzetting overnemen, en volledigheidscontroles van
  het register in de SHACL-profielen per codelijst (`csor-*-ap-constraints.ttl`) houden.
- Kan `csor:ParameterAspect` ⊂ `sosa:Property` (A1) en `csor:Eenheid` ⊂ `qudt:Unit` (A2) in de
  CSOR-ontologie, zodat de voorbeelden die typering niet zelf hoeven toe te voegen? De eerste
  staat voorlopig in `waterkwaliteit.ttl`. De tweede niet: `qudt:Unit` veronderstelt QUDT-kenmerken
  (grootheid, conversie) die stofgekwalificeerde eenheden zoals `mgN/L` niet hebben.
- De ontbrekende QUDT-koppelingen aanvullen voor de gebruikte eenheden: E_67 `meq/L` →
  `unit:MilliEQ-PER-L` (suggestie van `csor-testing`); E_54 `/100mL` zonder kandidaat; E_75 Franse
  hardheidsgraden bewust zonder.
- De bevindingen uit `csor-testing` die de voorbeelden raken, zijn beperkt (`codelijsten.md`
  §3.5): V_378, V_403 en V_47 (chemische identificatie). Het hergebruik van V_2043–V_2240 raakt
  geen enkele gebruikte variabele.
- Waardenlijsten van kwalificeerbare aspecten als SKOS-enumeratie (relevant voor A3).

### C2. VITO-lijst observatiemethoden (`brondata_Jurgen/Lijst_observatiemethodes_VITO-v1`)

- Een kolom **soort procedure** (staalname, observatie/analyse, richtlijn zoals WAC/VI
  prestatiekenmerken) (A10).
- **Unieke `skos:notation`** per jaarversie: nu heeft `WAC_I_A_003_2024` dezelfde notation
  `WAC/I/A/003` als de hoofdprocedure.
- **Definities** invullen: nu leeg voor alle 313 hoofdprocedures.
- De jaarversie-IRI's publiceren in `codelijst-observatieprocedure`.

### C3. VHA-waterlopen-LOD (`~/git/shapefile_to_rdf`)

- **IRI-fout in de bron herstellen.** De IRI van een waterloop is het objectnummer, maar
  verwijzingen gebruiken de gewestcode. In dit project is dat opgelost met
  `scripts/waterlopen_herstel.py`; de bron moet nog volgen.
- 133 verwijzingen naar gewestcodes die niet in `vhag` voorkomen.
- `code:vhazonenr` een eigen namespace geven (in de herstelde kopie gebeurd).
- **Waterlichamen en stroomgebieden** als conceptschema publiceren. Nu verwijzen 2040 IRI's naar
  niets. Dat is nodig voor fase 2.
- Het vocabularium: `code:vhag`/`code:beknr`/`code:geo` hebben een verkeerd bereik (in de kopie
  in `src/main/resources/` gecorrigeerd, met OWL-restricties).
- **Geometrie via `geo:hasGeometry`.** De bron zet `geo:asWKT` rechtstreeks op de waterloop, het
  segment en het categorietraject. Het domein van `geo:asWKT` is `geo:Geometry`, dat disjunct is
  met `geo:Feature`, dus het object wordt formeel een geometrie. In dit project hersteld:
  - *Data:* `scripts/waterlopen_herstel.py` stap 4 maakt van elk object `a geo:Feature ;
    geo:hasGeometry [ a geo:Geometry ; geo:asWKT … ]`, met de geometrie als blank node. Het gaat om
    27 239 waterlopen, 64 863 segmenten en 30 028 categorietrajecten.
  - *Vocabularium:* in `waterlopen.ttl` vallen `code:Vhag`, `code:Wlas` en `code:VhaCattraj` onder
    `code:VhaWaterloopobject` ⊂ `geo:Feature`, met de restricties `geo:hasGeometry` 1..1 →
    `geo:Geometry`.
  - *Validatie:* de drie bestanden samen zijn conform, op de 133 gekende verwijzingen naar
    ontbrekende waterlopen na.
  - *Nog te doen:* de bron (`shapefile_to_rdf`) moet volgen.
- De superklasse `code:VhaWaterloopobject` (in de kopie toegevoegd) en de alignering
  `code:VhaWaterloopobject` ⊂ `sosa:FeatureOfInterest` in het vocabularium opnemen (A15.6).
- **Alignering met een bestaande hydrografische ontologie (open).** Onderzochte kandidaten:
  - *OGC HY_Features* (`https://www.opengis.net/def/schema/hy_features/hyf/`): volledig
    gedereferenced en bewaard als `src/main/resources/net/opengis/www/def/schema/hy_features/hy_features.trig`
    (script `scripts/hyfeatures_ophalen.py`; 79 IRI's, 1106 triples, 2026-10-01). Bewust `.trig`, dus
    niet ingeladen door de pipeline. De publicatie:
    - heeft status *experimental*;
    - is maar half OWL: van de 34 feature types zijn er 19 `owl:Class`. Net de
      oppervlaktewaterklassen (`HY_WaterBody`, `HY_River`, `HY_Channel`, `HY_Canal`, `HY_Lake`) zijn
      enkel `skos:Concept`, met `skos:broader` in plaats van `rdfs:subClassOf`;
    - gebruikt punning: dezelfde IRI is `owl:Class` én `skos:Concept`/`FeatureType`, dus klasse én
      registerterm, zonder semantisch verband;
    - importeert via ShapeChange de ISO 19115-omzetting van seegrid.
  - *INSPIRE Hydrografie* (`Watercourse`, `WatercourseLink`, `SurfaceWater`): inhoudelijk de beste
    match, want de VHA is de Vlaamse INSPIRE-bron. Er is wel geen gezaghebbende RDF-namespace.
  - *Voorstel:* geen formele alignering (`rdfs:subClassOf`) zolang er geen volledige,
    niet-experimentele OWL-versie bestaat. Ook geen SKOS-mappingrelaties (`skos:closeMatch` …):
    op klasseniveau gebruiken we geen SKOS-relaties (projectregel, 2026-10-01). Hooguit
    `rdfs:seeAlso` als verwijzing.

### C4. RIE-IEPR (`~/git/RIE-IEPR`)

*Getoetst op 2026-09-30. De voorbeelden van dit voorstel zijn vergeleken met de OWL-restricties in
`riepr.ttl` (versie 14/09/2026) en met het datavoorbeeld `agc-glass_MJV_18-09-2026.ttl`.*

**Samenvatting.** Het voorstel is een specialisatie van hetzelfde SOSA-patroon als RIE-IEPR.
Conceptueel sluit het aan: de lozing is de emissie, het observatie-, collectie- en
resultaatpatroon is hetzelfde, en de koppeling loopt via de VMM-code. Om als RIE-IEPR-data te
valideren, zijn vooral **administratieve toevoegingen** nodig (C4.2). De inhoudelijke verschillen
(C4.3) zijn bewuste keuzes en liggen voor als A-punten.

#### C4.1 Wat overeenkomt

| RIE-IEPR (`riepr.ttl`) | Dit voorstel | Oordeel |
|---|---|---|
| `riepr:Emissie` ⊂ `prov:Entity`, `sosa:FeatureOfInterest`; tijdsloos (geen versiesegment in de IRI) | `ex:lozing-<nr>`: exact die twee types, tijdsloos (A5) | zelfde concept en superklassen |
| `riepr:Observatie` ⊂ `sosa:Observation`: `hasFeatureOfInterest` exact 1, `hasResult` exact 1, `observedProperty`/`usedProcedure`/`phenomenonTime`/`resultTime` hoogstens 1 | idem | past op alle kardinaliteiten |
| `riepr:ObservatieVerzameling` ⊂ `sosa:ObservationCollection`: `hasMember` minstens 1, `hasFeatureOfInterest` exact 1 | collectie per staal of per jaar | past |
| `riepr:Resultaat` ⊂ `sosa:Result` met eigen IRI; `qudt:numericValue` (decimal) en `qudt:hasUnit` hoogstens 1 | `ex:resultaat-…` met eigen IRI | past. Resultaten onder de rapportagegrens (A3: grenzen, zonder `numericValue`) zijn toegelaten, want `numericValue` is optioneel. |
| `phenomenonTime` als `time:TemporalEntity` (instant of interval) | `time:Instant`, `time:Interval` | past |
| meetpunt als systeem met agency (`madeBySensor` → meetpunt, bereik `ssn:System`) | meetput ⊂ `sosa:Sampler` ⊂ `sosa:System` (A15.5); `madeBySampler` voor de staalname, `madeBySensor` wanneer de bron zegt dat de meetput mat, anders `prov:atLocation` | zelfde concept. Verschil alleen in wat de VMM-bron toelaat te beweren (A9). |
| VMM-meetputcode als `adms:identifier` met `vmm:lozingspuntCode` | `rdfs:seeAlso` naar het RIE-IEPR-meetpunt, automatisch gevonden via die code | werkend voor AGC Glass Mol (2400006 → Controleinrichting LP01, 2400007 → LP02) |

**Het FOI in RIE-IEPR is de Emissie.** Staal als FOI (A4) is daarvan een echte afwijking. De
restrictie liet het ooit expliciet zien, en de huidige, ruimere restrictie is vermoedelijk een
bijwerking van een opschoning:

| Datum | Commit | FOI van een observatie in `riepr.ttl` |
|---|---|---|
| 17/05/2026 | `5cec2a5` "SOSA-semantiek gecorrigeerd" | subklassen `EmissieObservatie`, `OnttrekkingObservatie`, `ProductieObservatie` met `hasFeatureOfInterest some :Emissie` (enz.) |
| 13/07/2026 | `229ffaa` "docs: cleanup" | subklassen verwijderd; `riepr:Observatie` eist nog `some sosa:FeatureOfInterest` |
| 14/09/2026 | huidige versie, ook `documentatie/datamodel/generated/shacl/schema.ttl` | `sosa:FeatureOfInterest`, met als commentaar "Een observatie is gekoppeld aan een Emissie of Onttrekking" |

Een staal als FOI valideert daardoor vandaag tegen `riepr.ttl`, maar dat is toeval en geen
compatibiliteit.

#### C4.2 Wat ontbreekt om als RIE-IEPR-data te valideren

| Vereist in RIE-IEPR | In dit voorstel | Oplossing |
|---|---|---|
| `dct:created` exact 1 op `riepr:Observatie` en `riepr:ObservatieVerzameling` | ontbreekt | Administratief registratieveld, niet afleidbaar uit de VMM-data. Toevoegen bij de omzetting (tijdstip van registratie). |
| RIE-IEPR-types (`riepr:Observatie`, `riepr:Resultaat`, `riepr:ObservatieVerzameling`, `riepr:Emissie`) | enkel de SOSA-/PROV-types | Een extra type-assertie volstaat: de RIE-IEPR-klassen zijn subklassen van de gebruikte types. `riepr.ttl` staat bewust niet in de pipeline van dit project (zie C4.4). |
| `riepr:Emissie` `prov:wasDerivedFrom` minstens 1 `riepr:Proces` | geen proces, want de VMM-data beschrijft er geen | Het pad bestaat in RIE-IEPR: meetput 2400006 = "Controleinrichting LP01", verbonden met lozingspunt LP01, uitgevoerd door "Proces emissiepunt LP01" (`dct:type` emissie). De lozing wordt dan `prov:wasDerivedFrom` dat proces. Voorwaarde: de koppeling tussen meetpunt en lozingspunt machineleesbaar maken (C4.4). |
| `riepr:Meetpunt`: `inGebruikVanaf`, `adms:status`, `dct:issued`, `dct:created`, `rdfs:label` verplicht | `ex:meetpunt-<nr>` is een verwijzing met label, identificator en geometrie | Bij integratie vervangt het RIE-IEPR-meetpunt `ex:meetpunt`. De verplichte velden staan dan al in RIE-IEPR. |

#### C4.3 Bewuste verschillen (te beslissen in de werkgroep)

| Onderwerp | RIE-IEPR | Dit voorstel | Motivatie | A-punt |
|---|---|---|---|---|
| wat gemeten wordt | chemische stof (InChIKey) of operationele codelijst | CSOR-parameteraspect | onderscheidt concentratie, vracht en debiet; `riepr.ttl` kent zelf al `riepr:parameterAspect` met bereik `csor:ParameterAspect` (op Systeemeigenschap) | A1 |
| eenheid | rechtstreeks QUDT (documentatie) | CSOR-eenheid, QUDT via `skos:*Match` | "als N/P", eenheden zonder QUDT-tegenhanger. De RIE-IEPR-restrictie legt het bereik van `qudt:hasUnit` niet vast, dus dit is formeel compatibel. | A2 |
| FOI van een analyse op een staal | Emissie (bedoeling en documentatie; de restrictie is sinds juli ruimer, zie C4.1) | staal, met ultiem FOI = Emissie | de analyse gebeurt op het staal; het staal draagt de staalname-informatie | A4 |
| collectielidmaatschap | `sosa:isMemberOf` op de observatie (hoogstens 1) | `sosa:hasMember` op de collectie | inverse van elkaar, afleidbaar; eventueel beide richtingen opnemen | – |
| SSN-namespace | mengt `ssn:System`, `ssn:hasProperty`, `ssn:implementedBy` met `sosa-2023:` | SOSA/SSN 2023 (`sosa:System`, `sosa:hasProperty`, `sosa:implements`) | één versie kiezen | – |

#### C4.4 Punten voor het RIE-IEPR-team

1. **`generated-shapes.ttl` is verouderd.** De shapes (13/07) lopen achter op `riepr.ttl` (14/09).
   Ze eisen dat het FOI van een Observatie een `ssn:System` is, en verwijzen naar een klasse
   `riepr:MeetInstrument` die niet meer in de ontologie staat. Daardoor zou ook het
   documentatievoorbeeld (FOI = Emissie) niet conform zijn. Opnieuw genereren volstaat.
2. **Koppeling tussen meetpunt en lozingspunt machineleesbaar maken.** In het AGC-voorbeeld staat
   de koppeling tussen controle-inrichting en lozingspunt enkel in commentaar ("afgeleid:
   gelijkgezet aan gekoppeld lozingspunt …"). Een expliciete relatie is nodig om van een
   VMM-meetput naar de emissie en haar proces te komen (C4.2).
3. **De FOI-restrictie opnieuw expliciet maken.** Sinds de opschoning van 13/07 (`229ffaa`) laat
   de restrictie elk `sosa:FeatureOfInterest` toe; de bedoeling is Emissie, Onttrekking, Verbruik
   of Productie. Herstel de expliciete restrictie, en beslis daarbij over A4: ook een
   `sosa:Sample` van een emissie toelaten, met `sosa:hasUltimateFeatureOfInterest` naar de
   emissie (bv. `owl:unionOf` of een aparte klasse voor observaties op stalen).
4. **Restricties op externe klassen.** `riepr.ttl` legt restricties op `adms:Identifier` en
   `locn:Address`. Wie de ontologie laadt, legt die op aan alle data. Dat is de reden waarom ze
   niet in dit project geladen wordt. Voorstel: die restricties in een applicatieprofiel of
   SHACL-shapes onderbrengen, niet in de ontologie.
5. **SSN-versie** eenduidig op SOSA/SSN 2023 zetten (C4.3).

### C5. `codelijst-rie-iepr`

De nieuwe lijsten voor lozingspunten (A11), met de volledige waardenlijsten van de VMM (V8).

### Buiten scope, ter info: het huidige OSLO-AP Waterkwaliteit

Het bestaande AP (kandidaatstandaard 2023-06-01) steunt op
`http://def.isotc211.org/` (verwijderd), `observaties-en-metingen#` (deprecated), `generiek#`
(niet gereviewd) en het Europese ODALA `water:`-vocabularium (geen machineleesbare definitie). Zie
`bestaand_model/bestaand_model.md`. Het voorstel in dit document vervangt die basis door SOSA
2023 + CSOR.

---

## 5. Deel D: nog niet gemodelleerd

| # | Onderwerp | Bron | Voorwaarde |
|---|---|---|---|
| D1 | **Normen en beoordelingen** (Vlarem-normen, triggerwaarden, toetswijze MAX/MIN, oordeel goed/niet goed): volgens de VMM buiten SSN/SOSA, apart te modelleren | `250124` | waterlichamenlijst (C3), V7 |
| D2 | **KRW-waterlichaam** als beoordelingsobject | VHA `code:wtrlichc` | conceptschema waterlichamen (C3) |
| D3 | **Kenmerken** van lozingspunten, meetputten en bedrijven (soort afvalwater, DWA/RWA, lozingswijze, sector) en versies van een lozing | `250108`, `250129` | nieuwe codelijsten (A11, C5), A13 |

---

*Bronnen: `stappenplan.md`, `codelijsten.md`, `featureofinterest.md`, `bestaand_model/bestaand_model.md`
en de `bespreking.md` per datavoorbeeld in `nieuw_model/`.*
