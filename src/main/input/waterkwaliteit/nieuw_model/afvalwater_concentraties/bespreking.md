# Bespreking: concentraties in afvalwater

## 1. Wat stelt dit voorbeeld voor?

De VMM neemt stalen van geloosd afvalwater aan de meetputten (controle-inrichtingen) van bedrijven
en rioolwaterzuiveringsinstallaties, en laat ze analyseren op een reeks parameters. Dit voorbeeld
modelleert die analyseresultaten als SSN/SOSA 2023-observaties. Bron: VMM-export
`250108_AW_Resultaat_Prompts_R_62-mtpn-UK-PFAS-AW_2024.xlsx`: 1998 resultaten uit 2024, 697
stalen, 60 meetpunten, 325 parameters. De validatie-subset (`afvalwater_concentraties.ttl`) toont
één staal: `M-AW-2024-006358-1`, een schepmonster van het effluent van RWZI Mechelen-Noord
(meetput `AW2800028`) op 27 maart 2024, met 15 resultaten.

## 2. Kleurlegenda

| Kleur | SOSA-concept | Domeinbetekenis |
|---|---|---|
| Blauw (#60c4e4) | `sosa:Sampler`, `sosa:FeatureOfInterest`, `prov:Organization` | meetput, lozing, exploitatie, VMM |
| Paars (#c6a0f5) | `sosa:SamplingProcedure` | soort monstername (WAC-compendium) |
| Oranje (#fe7130) | `sosa:Property` | CSOR-parameteraspect: wat er gemeten wordt |
| Roze (#e54b89) | `sosa:Sampling`, `sosa:ObservationCollection`, `sosa:Observation` | staalname, analyses van één staal |
| Geel-oranje (#f8b622) | `sosa:Sample`, `sosa:Result`, `time:Instant` | staal, meetwaarde, datum |

## 3. Infrastructuur (blauwe nodes)

- **`ex:meetpunt-2800028`**: `sosa:Sampler`. De VMM-meetput (controle-inrichting) waar het
  staal genomen wordt. Het label `AW2800028` en de omschrijving (`Effluent F203`) komen uit de
  bron. Het meetputnummer `2800028` is een `adms:Identifier` met `dct:creator` VMM. De geometrie
  staat in Lambert 72 (`EPSG:31370`), zoals aangeleverd. In RIE-IEPR is dit een `riepr:Meetpunt`
  (⊂ `ssn:System`) met `vmm:lozingspuntCode` (`../../featureofinterest.md` §2.2).
- **`ex:lozing-2800028`**: `wk:Emissie` (ontwerpversie, `../../beslisdocument.md` A14) +
  `sosa:FeatureOfInterest` + `prov:Entity`, `dct:type
  matrix:afvalwater`. De lozing aan die meetput: het ultieme onderwerp van de metingen. Dit komt
  overeen met `riepr:Emissie` (§6.2). Ze is **tijdsloos**: de tijd zit in de observaties (§6.8).
  `prov:wasAttributedTo` de exploitatie.
- **`ex:exploitatie-1498`** (RWZI Mechelen-Noord) en **`ex:organisatie-vmm`**:
  `prov:Organization`. De exploitatie is enkel een identificator (`dct:identifier` =
  `Exploitatie ID`). Bedrijfskenmerken vallen buiten de scope van deze stap. De VMM staat in het
  model als uitgever van de meetputcode en als uitvoerder van de staalname.

Er is geen `sosa:hosts`-hiërarchie: de bron vermeldt geen sensoren of labo-apparatuur.

## 4. Observatie/Actuatie-structuur (roze nodes)

| IRI | observedProperty | hasResult | hasFeatureOfInterest |
|---|---|---|---|
| `ex:observatie-16231-P_1017` | `csor-parameteraspect:PAS_1789` U t (totaal in water): massaconcentratie | 0.45 `csor-eenheid:E_4` µg/L | `ex:staal-16231` |
| `ex:observatie-16231-P_1100` | `csor-parameteraspect:PAS_1940` Bromoxyn (standaard in water): massaconcentratie | < 0.1 `E_4` µg/L | `ex:staal-16231` |
| `ex:observatie-16231-P_118` | `csor-parameteraspect:PAS_184` Atenolol (standaard in water): massaconcentratie | 0.303 `E_4` µg/L | `ex:staal-16231` |
| `ex:observatie-16231-P_1180` | `csor-parameteraspect:PAS_2076` Glyfosaat (standaard in water): massaconcentratie | 0.3 `E_4` µg/L | `ex:staal-16231` |
| `ex:observatie-16231-P_1188` | `csor-parameteraspect:PAS_2092` Mo t (totaal in water): massaconcentratie | 0.00244 `E_1` mg/L | `ex:staal-16231` |
| `ex:observatie-16231-P_1228` | `csor-parameteraspect:PAS_2163` P t (totaal in water): massaconcentratie fosfor | 0.59 `E_131` mgP/L | `ex:staal-16231` |
| `ex:observatie-16231-P_1238` | `csor-parameteraspect:PAS_2184` Prometryn (standaard in water): massaconcentratie | < 0.025 `E_4` µg/L | `ex:staal-16231` |
| `ex:observatie-16231-P_1442` | `csor-parameteraspect:PAS_2499` Oxadiazon (standaard in water): massaconcentratie | < 12.5 `E_2` ng/L | `ex:staal-16231` |
| `ex:observatie-16231-P_421` | `csor-parameteraspect:PAS_728` B t (totaal in water): massaconcentratie | 0.103 `E_1` mg/L | `ex:staal-16231` |
| `ex:observatie-16231-P_572` | `csor-parameteraspect:PAS_1005` PCNiBz (standaard in water): massaconcentratie | < 5 `E_2` ng/L | `ex:staal-16231` |
| `ex:observatie-16231-P_595` | `csor-parameteraspect:PAS_1041` Diuron (standaard in water): massaconcentratie | < 0.05 `E_4` µg/L | `ex:staal-16231` |
| `ex:observatie-16231-P_599` | `csor-parameteraspect:PAS_1049` Metoxur (standaard in water): massaconcentratie | < 0.05 `E_4` µg/L | `ex:staal-16231` |
| `ex:observatie-16231-P_813` | `csor-parameteraspect:PAS_1432` DCvos (standaard in water): massaconcentratie | < 0.0125 `E_4` µg/L | `ex:staal-16231` |
| `ex:observatie-16231-P_863` | `csor-parameteraspect:PAS_1507` tCdaan (standaard in water): massaconcentratie | < 5 `E_2` ng/L | `ex:staal-16231` |
| `ex:observatie-16231-P_866` | `csor-parameteraspect:PAS_1511` cCdaan (standaard in water): massaconcentratie | < 5 `E_2` ng/L | `ex:staal-16231` |

Geen enkele observatie heeft `sosa:usedProcedure` (analysemethode) of `sosa:madeBySensor`
(labo): de bron bevat die gegevens niet (§6.6). Elke observatie heeft ook
`sosa:hasUltimateFeatureOfInterest ex:lozing-2800028`.

**`ex:collectie-16231`** (`sosa:ObservationCollection`) groepeert de 15 analyses van één staal.
Op de collectie staat wat ze delen: het staal als FOI, de lozing als ultiem FOI en de
fenomeentijd. Daarnaast is er één **`sosa:Sampling`** (`ex:sampling-16231`) die het staal
oplevert: `sosa:hasResult ex:staal-16231`, `sosa:hasFeatureOfInterest ex:lozing-2800028`,
`sosa:madeBySampler ex:meetpunt-2800028`, `sosa:usedProcedure` = schepmonster en
`prov:wasAssociatedWith` = VMM.

## 5. Procedure en ObservableProperty

**SamplingProcedure.** De soort monstername verwijst naar de **jaarversie** van de
WAC-procedure die gold in het jaar van de staalname. De versies komen uit de VITO-lijst
observatiemethoden (`../../brondata_Jurgen/Lijst_observatiemethodes_VITO-v1/`). De jaarversie
verwijst met `dct:isVersionOf` naar de hoofdprocedure uit `codelijst-observatieprocedure`:

| Bron (`Aard Monstername`) | Jaarversie (`sosa:usedProcedure`) | Hoofdprocedure (`dct:isVersionOf`) | Stalen |
|---|---|---|---|
| Schepmonster | `procedure:WAC_I_A_003_2024` | `WAC_I_A_003` Ogenblikkelijke monstername (schepmonster) van water | 670 |
| Debietgebonden monster | `procedure:WAC_I_A_004_2024` | `WAC_I_A_004` Procedure voor het nemen van een verzamelmonster | 27 (bevestiging VMM nodig, `stappenplan.md` V1) |

De jaarversie krijgt ook `dct:issued "2024"^^xsd:gYear` en `prov:hadPrimarySource` (de pdf op
reflabos.vito.be) mee. Zo ligt vast volgens welke versie van het compendium er bemonsterd is.
Wie op hoofdprocedure zoekt, volgt `dct:isVersionOf`. Het script kiest de versie uit het jaar van
`Datum Dag` en stopt als die versie niet in de VITO-lijst staat.

De jaarversie-IRI's zijn nog een **voorstel van VITO** en niet gepubliceerd. De
hoofdprocedure-IRI's bestaan wel al. De VITO-lijst typeert alles als `sosa:Procedure`. Het type
`sosa:SamplingProcedure` komt uit dit voorbeeld (§6.7), omdat de lijst geen soort procedure
vermeldt.

De procedure wordt gebruikt door de `sosa:Sampling` en niet `sosa:implements` door het meetpunt.
De meetput laat beide soorten staalname toe.

**Property.** Elke `sosa:observedProperty` is een **CSOR-parameteraspect**. Dat combineert:

- een variabele (bv. Uranium);
- een drager (water);
- een soort waardebepaling (totaal / standaard);
- een kwantificeerbaar aspect (massaconcentratie, of "massaconcentratie fosfor" voor een
  resultaat uitgedrukt als P).

De 1998 rijen gebruiken 325 verschillende parameteraspecten. Ze zijn allemaal eenduidig gevonden
via `Parameter Code` en de eenheid (`../../codelijsten.md` §3.1–3.2). In de data krijgen ze enkel
een minimale type-assertie `sosa:Property` en hun label (§6.5).

## 6. Modelleer-keuzes toegelicht

### 6.1 Waarom het staal als FOI en de lozing als ultiem FOI?

> **Verworpen alternatief:** `sosa:hasFeatureOfInterest` rechtstreeks naar de lozing, zoals
> RIE-IEPR voorschrijft (FOI = exact één `riepr:Emissie`).
> **Gekozen aanpak:** FOI = `sosa:Sample` (het staal); `sosa:hasUltimateFeatureOfInterest` =
> de lozing; het staal `sosa:isSampleOf` de lozing en `sosa:isResultOf` een `sosa:Sampling`.
> **Motivatie:** de analyse gebeurt op het staal, niet op de lozing als geheel (SOSA:
> Sample/Sampling-patroon, R8). Het staal draagt informatie die anders verloren gaat: de soort
> monstername, wie het nam (VMM of het bedrijf), de datum. Eén staal levert ook meteen de
> natuurlijke `ObservationCollection`. Wie naar de lozing zoekt, vindt de observaties via
> `hasUltimateFeatureOfInterest` zonder de keten te volgen. Dit vraagt een kleine uitbreiding van
> RIE-IEPR (beslissing B4, `../../stappenplan.md`).

### 6.2 Waarom geen `riepr:`-types?

> **Verworpen alternatief:** `riepr:Emissie` en `riepr:Meetpunt` typeren en `riepr.ttl` aan
> `src/main/resources/` toevoegen.
> **Gekozen aanpak:** SOSA/PROV-types (`sosa:FeatureOfInterest` + `prov:Entity` voor de lozing,
> `sosa:Sampler` voor de meetput), met de overeenkomst gedocumenteerd.
> **Motivatie:** `riepr.ttl` bevat 220 OWL-restricties, ook op externe klassen (`adms:Identifier`,
> `locn:Address`). Die zouden als SHACL gelden voor alle voorbeelden in dit project. Een
> `riepr:Emissie` vraagt bovendien een `riepr:Proces` (`prov:wasDerivedFrom`, min 1), en de
> brondata beschrijft geen processen. De SOSA-types zijn de superklassen van de RIE-IEPR-klassen.
> De integratie volgt bij de afstemming met RIE-IEPR (B6).

### 6.3 Waarom de meetput als `sosa:Sampler`?

> **Verworpen alternatief:** meetput als `sosa:Platform` dat een sampler host, of als
> `sosa:Sensor` (zoals RIE-IEPR met `madeBySensor` → meetpunt).
> **Gekozen aanpak:** meetput = `sosa:Sampler` (⊂ `sosa:System`) en `madeBySampler` van de
> staalname. Wie de staalname uitvoerde, staat als `prov:wasAssociatedWith` (VMM of de
> exploitatie; `Sample Type Staal` VMM/BEDR).
> **Motivatie:** de controle-inrichting is de voorziening waarmee het staal genomen wordt, niet
> het meettoestel: de analyse gebeurt in een labo. `sosa:Sampler` sluit aan bij de RIE-IEPR-keuze
> "meetpunt = systeem" zonder `madeBySensor` te verbuigen. "Herkomst staal" wordt zo een agent en
> geen codelijst (`../../stappenplan.md` §2.2).

### 6.4 Waarom `qudt:lowerBound`/`qudt:upperBound` voor het teken `<`?

> **Verworpen alternatieven:** (a) `qudt:numericValue` = de grenswaarde plus een aparte
> tekencodelijst; (b) het CSOR kwalificeerbaar aspect "Aantoonbaarheid" als tweede observatie.
> **Gekozen aanpak:** bij `=` staat `qudt:numericValue`. Bij `<` staat er **geen**
> `numericValue`, maar `qudt:lowerBound 0` en `qudt:upperBound` = de rapportagegrens.
> **Motivatie:** de VMM levert het resultaat zelf al als interval aan (`Resultaat Ondergrens` /
> `Resultaat Bovengrens`: `[v, v]` bij `=`, `[0, X]` bij `<`). `numericValue` = X zou een meting
> suggereren die er niet is. Het teken is zo afleidbaar (wel of geen `numericValue`) zonder een
> nieuwe codelijst. De grens is in 1464 van de 1605 `<`-gevallen de aantoonbaarheidsgrens, in 139
> de bepaalbaarheidsgrens, en 2 keer iets anders.
> **Open (B3, `stappenplan.md` V2):** de aantoonbaarheids- en bepaalbaarheidsgrens zelf
> (`Resultaat Aantoonbaarheid`/`Bepaalbaarheid`) staan nog niet in het model. De SOSA-weg is
> `ssn-system:DetectionLimit`, maar die module zit niet in de pipeline. Bovendien variëren de
> grenzen per staal, niet per labo. De betekenis moet ook eerst bevestigd worden.

### 6.5 Waarom CSOR-concepten als `observedProperty` en `qudt:hasUnit`, met minimale type-asserties?

> **Verworpen alternatief:** eigen `ex:property-…` per parameter, en rechtstreeks QUDT-eenheden
> (R3).
> **Gekozen aanpak:** `sosa:observedProperty` → CSOR-parameteraspect; `qudt:hasUnit` →
> CSOR-eenheid (QUDT bereikbaar via de `skos:exactMatch`/`broadMatch` in CSOR). In de data enkel
> `a sosa:Property` en `rdfs:label` voor elk gebruikt parameteraspect.
> **Motivatie:** CSOR is het Vlaamse register voor parameters. Het parameteraspect onderscheidt
> concentratie, vracht en debiet van dezelfde stof. Stofgekwalificeerde eenheden zoals `mgP/L`
> (E_131) hebben enkel een `broadMatch` naar `unit:MilliGM-PER-L`; met QUDT alleen zou "als P"
> verloren gaan. De type-assertie is nodig omdat de pipeline SHACL valideert op het
> niet-geïnfereerde model. De CSOR-bestanden zelf zijn te groot en gebruiken `csor:`-properties
> die de pipeline niet kent (`../../codelijsten.md` §3, B1/B2).

### 6.6 Waarom geen `usedProcedure` en `madeBySensor` op de observaties?

> **Verworpen alternatief:** een illustratief labo en een analysemethode invullen.
> **Gekozen aanpak:** weglaten.
> **Motivatie:** de brondata bevat noch het labo, noch de analysemethode. R2 noemt beide sterk
> aanbevolen, maar niet verplicht. Gefabriceerde waarden zouden als echte gegevens gelezen kunnen
> worden. Zodra de VMM ze aanlevert, komen ze op de collectie (gedeeld per staal) of op de
> observatie.

### 6.7 Waarom expliciete supertypes (`sosa:Execution`, `sosa:ExecutionCollection`, `sosa:Procedure`, `sosa:FeatureOfInterest` op het staal)?

> **Verworpen alternatief:** enkel de specifieke klasse, en de SHACL-meldingen aanvaarden als
> vals-positief (zoals in `verkeersmetingen`).
> **Gekozen aanpak:** de supertypes die SOSA 2023 afleidt, expliciet vermelden.
> **Motivatie:** de pipeline valideert SHACL zonder subklasse-inferentie. Met de expliciete
> types is het voorbeeld echt conform, zodat een nieuwe SHACL-melding ook een echte fout is. In
> deze SOSA-versie is `sosa:Sample` enkel `prov:Entity`; als FOI moet het staal dus ook
> `sosa:FeatureOfInterest` zijn.

### 6.8 Waarom de matrix op het FOI (staal en lozing), en niet in de observedProperty?

> **Verworpen alternatieven:** (a) een samengestelde eigenschap "parameteraspect + matrix", bv.
> `[PAS_1432, afvalwater]`; (b) een FOI per periode ("lozing in 2024").
> **Gekozen aanpak:** `dct:type matrix:afvalwater` (`codelijst-matrix`) op het staal én op de
> lozing. De observedProperty is het CSOR-parameteraspect zoals het is. De lozing is tijdsloos,
> en de tijd staat in `sosa:phenomenonTime`.
> **Motivatie:**
> - De matrix beschrijft het bemonsterde materiaal, dus het FOI. `observedProperty` is een
>   eigenschap *van* het FOI: DCvos in water van een afvalwaterstaal is DCvos in afvalwater.
> - CSOR houdt drager (`water`, grof) en matrix bewust gescheiden. Een lokaal samenstel zou een
>   onbeheerd parallel register naast CSOR worden (parameteraspect × matrix).
> - Een FOI per periode legt de tijd dubbel vast (`phenomenonTime` is per definitie de tijd
>   waarop het resultaat op het FOI van toepassing is). Het zou alle observaties van een lozing
>   over jaren en voorbeelden heen versnipperen. RIE-IEPR modelleert `riepr:Emissie` ook
>   tijdsloos, zonder versiesegment in de IRI.
> - Veranderen de kenmerken van een lozing in de tijd (bv. vanaf een datum ook koelwater), dan
>   krijgt de lozing versies (`dct:isVersionOf`/`prov:specializationOf`), zoals RIE-IEPR voor
>   structurele elementen doet. Dat is fase 3.

### 6.9 Waarom een plat model en geen drielaags architectuur?

Eén staalname en één analyse per parameter, zonder meerstapsproces of herbruikbaar plan (R4).
`ObservationCollection` per staal volstaat.

## 7. Tijdsmodellering

| Element | Patroon | Bron |
|---|---|---|
| staalname en collectie | `sosa:phenomenonTime → time:Instant → time:inXSDDate` | `Datum Dag` (bv. `2024-03-27`) |

- Eén `time:Instant` per datum (`ex:tijdstip-2024-03-27`), gedeeld door alle stalen van die dag.
  Het krijgt een IRI en geen blank node (skolem-IRI's in grote datasets).
- De bron geeft enkel de dag, geen uur. Daarom `inXSDDate` en geen `inXSDDateTime`.
- `sosa:resultTime` (wanneer het labo het resultaat vrijgaf) staat niet in de bron en is
  weggelaten.
- De fenomeentijd staat op de collectie en de sampling, niet op elke observatie: alle analyses
  van een staal gaan over hetzelfde moment.

## 8. Prefixen en IRI-structuur

| Prefix | Base URI | Tijdelijk of persistent |
|---|---|---|
| `ex:` | `https://example.org/waterkwaliteit/afvalwater/` | tijdelijk (illustratief, R10) |
| `wk:` | `https://data.vlaanderen.be/ns/waterkwaliteit#` | ontwerpversie (`src/main/resources/be/vlaanderen/data/ns/waterkwaliteit/waterkwaliteit.ttl`), niet gepubliceerd |
| `csor-parameteraspect:` | `https://data.omgeving.vlaanderen.be/id/concept/csor/parameteraspect/` | persistent (CSOR) |
| `csor-eenheid:` | `https://data.omgeving.vlaanderen.be/id/concept/csor/eenheid/` | persistent (CSOR) |
| `procedure:` | `https://data.omgeving.vlaanderen.be/id/concept/observatieprocedure/` | persistent (hoofdprocedures); jaarversies = voorstel VITO. Prefix `procedure:` omdat de lijst zowel staalname- als observatieprocedures bevat. |
| `matrix:` | `https://data.omgeving.vlaanderen.be/id/concept/matrix/` | persistent |
| `sosa:` | `http://www.w3.org/ns/sosa/` | persistent |
| `qudt:` | `http://qudt.org/schema/qudt/` | persistent |
| `time:` | `http://www.w3.org/2006/time#` | persistent |
| `geo:` | `http://www.opengis.net/ont/geosparql#` | persistent |
| `prov:`, `dct:`, `adms:`, `skos:`, `rdfs:`, `xsd:` | W3C/DCMI/SEMIC | persistent |

`ex:`-IRI's worden uit de bronsleutels opgebouwd, zodat de volledige set en de subset dezelfde
IRI's geven:

| Resource | Patroon | Sleutel |
|---|---|---|
| meetput | `ex:meetpunt-<nr>` | nummer uit `Sample Point Naam` (`AW2800028` → `2800028`; V4) |
| lozing | `ex:lozing-<nr>` | idem |
| exploitatie | `ex:exploitatie-<id>` | `Exploitatie ID` |
| sampling, staal, collectie | `ex:sampling-<id>`, `ex:staal-<id>`, `ex:collectie-<id>` | `Sample ID` |
| observatie, resultaat | `ex:observatie-<id>-<P_code>`, `ex:resultaat-<id>-<P_code>` | `Sample ID` + `Parameter Code` |
| tijdstip | `ex:tijdstip-<datum>` | `Datum Dag` |

In productie komen hier de IRI's van RIE-IEPR (meetpunt, emissie) en een VMM-namespace (stalen,
observaties).

## 9. Inverse relaties

| Paar | Waarom |
|---|---|
| `sosa:hasResult` (sampling → staal) ↔ `sosa:isResultOf` (staal → sampling) | vanuit het staal de staalname vinden; `isResultOf` is verplicht op `sosa:Sample` (SHACL) |
| `sosa:hasResult` (observatie → resultaat) ↔ `sosa:isResultOf` | `isResultOf` is verplicht op `sosa:Result` (SHACL) |
| `sosa:hasSample` (lozing → staal) ↔ `sosa:isSampleOf` | alle stalen van een lozing vinden |
| `sosa:hasFeatureOfInterest` ↔ `sosa:isFeatureOfInterestOf` (lozing → sampling, staal → collectie) | `isFeatureOfInterestOf` is verplicht op `sosa:FeatureOfInterest` (SHACL) |

`sosa:hasMember` staat enkel op de collectie. Het omgekeerde `isMemberOf` is weggelaten: de
collectie is de enige ingang naar de analyses van een staal.
