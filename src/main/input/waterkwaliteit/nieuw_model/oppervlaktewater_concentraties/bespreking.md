# Bespreking: concentraties in oppervlaktewater

## 1. Wat stelt dit voorbeeld voor?

De VMM bemonstert oppervlaktewater op vaste meetplaatsen en laat de stalen analyseren op een
brede reeks parameters: fysisch-chemisch, nutriënten, metalen, organische microverontreinigingen.
Dit voorbeeld modelleert die resultaten als SSN/SOSA 2023-observaties, met de meetplaats als
ruimtelijk monster van een VHA-waterloop. Bron: VMM-export
`250114_Analyseresultaten per meetplaats_OW.xlsx`: 999 resultaten van 3 stalen uit 2019 op
meetplaats `OW12000` (Isabellahaven, Philippine, Leopoldkanaal). De VHA-waterloop komt uit de
herstelde waterlopen-LOD (`../../waterlopen/`). De subset toont het staal van 28 januari 2019
13:01 (331 resultaten), beperkt tot 14 representatieve parameters. Een volledig staal is te zwaar
voor de OWL-validatie van de pipeline; de volledige set staat in de `.trig`.

## 2. Kleurlegenda

| Kleur | SOSA-concept | Domeinbetekenis |
|---|---|---|
| Blauw (#60c4e4) | `sosa:Platform` · `sosa:SpatialSample` · `sosa:FeatureOfInterest` | meetplaats, VHA-waterloop |
| Oranje (#fe7130) | `sosa:Property` | CSOR-parameteraspect: wat er gemeten wordt |
| Roze (#e54b89) | `sosa:Sampling`, `sosa:ObservationCollection`, `sosa:Observation` | keuze van de meetplaats, staalname, analyses van één staal |
| Geel-oranje (#f8b622) | `sosa:Sample`, `sosa:Result`, `time:Instant` | staal, meetwaarde, tijdstip |

## 3. Infrastructuur (blauwe nodes)

- **`waterloop:2801`** (Leopoldkanaal): `waterlopen:Vhag + sosa:FeatureOfInterest`. De VHA-waterloop
  is het ultieme studieobject; `waterlopen:Vhag ⊂ sosa:FeatureOfInterest` staat in
  `waterkwaliteit.ttl` (`../../beslisdocument.md` A15.6). De IRI komt uit de herstelde
  waterlopen-LOD (gewestcode 2801). De volledige VHA-beschrijving (label, lengte, geometrie,
  notaties) is overgenomen uit `../../waterlopen/waterlopen_meetplaatsen.ttl`, met daarbij
  `sosa:hasSample` en `sosa:isFeatureOfInterestOf` (§6.3).
- **`ex:meetplaats-OW12000`**: **drievoudige typering** `sosa:Platform + sosa:FeatureOfInterest +
  sosa:SpatialSample` (R11), plus `sosa:Sample` expliciet (§6.6).
  - *SpatialSample*: de meetplaats is een puntmonster van de waterloop (`sosa:isSampleOf
    waterloop:2801`).
  - *FeatureOfInterest*: ze is het bemonsterde object van de staalnames.
  - *Platform*: de vaste locatie waar bemonsterd wordt.
  - Geometrie in Lambert 72 (`EPSG:31370`), zoals aangeleverd.
  - De meetplaats ligt in Nederland, vlak over de grens (§6.5).

Er is geen `sosa:hosts`: de bron vermeldt geen sensoren of staalnemers.

## 4. Observatie/Actuatie-structuur (roze nodes)

Selectie uit de observaties van het subset-staal (alle met `hasFeatureOfInterest` =
`ex:staal-OW12000-2019-01-28T130100` en `hasUltimateFeatureOfInterest` = `waterloop:2801`):

| IRI | observedProperty | hasResult |
|---|---|---|
| `ex:observatie-OW12000-2019-01-28T130100-PAS_2117` | `csor-parameteraspect:PAS_2117` pH (standaard in water): geen | 7.68 `csor-eenheid:E_74` Geen |
| `ex:observatie-OW12000-2019-01-28T130100-PAS_2119` | `csor-parameteraspect:PAS_2119` EC 20 (standaard in water): geleidbaarheid | 2650 `E_72` µS/cm |
| `ex:observatie-OW12000-2019-01-28T130100-PAS_2115` | `csor-parameteraspect:PAS_2115` O2 verz (verzadiging in water): percentage | 68 `E_43` % |
| `ex:observatie-OW12000-2019-01-28T130100-PAS_1067` | `csor-parameteraspect:PAS_1067` BZV5 (standaard in water): massaconcentratie zuurstof | 2.7 `E_102` mgO2/L |
| `ex:observatie-OW12000-2019-01-28T130100-PAS_2155` | `csor-parameteraspect:PAS_2155` KjN (standaard in water): massaconcentratie stikstof | 2.61 `E_103` mgN/L |
| `ex:observatie-OW12000-2019-01-28T130100-PAS_2163` | `csor-parameteraspect:PAS_2163` P t (totaal in water): massaconcentratie fosfor | 1.1 `E_131` mgP/L |
| `ex:observatie-OW12000-2019-01-28T130100-PAS_636` | `csor-parameteraspect:PAS_636` H t (totaal in water): hardheid | 57 `E_75` Franse hardheidsgraden |
| `ex:observatie-OW12000-2019-01-28T130100-PAS_2138` | `csor-parameteraspect:PAS_2138` TBySn (standaard in water): massaconcentratie tin | < 0.01 `E_135` ngSn/L |
| `ex:observatie-OW12000-2019-01-28T130100-PAS_1131` | `csor-parameteraspect:PAS_1131` 1112CEa (standaard in water): massaconcentratie | < 0.125 `E_4` µg/L |

In het volledige staal hebben 266 van de 331 resultaten teken `<`; in de subset 2 van de 14
(TBySn, 1112CEa). In de volledige set zijn dat er 834 van de 999.

**`ex:collectie-OW12000-2019-01-28T130100`** (`sosa:ObservationCollection`) groepeert de analyses
van één staal. Staal (FOI), waterloop (ultiem FOI) en tijdstip staan op de collectie. Daarnaast
zijn er **twee soorten `sosa:Sampling`**:

- **`ex:sampling-OW12000-2019-01-28T130100`**: de staalname. FOI = de meetplaats, resultaat =
  het staal, fenomeentijd = het tijdstip van staalname.
- **`ex:sampling-meetplaats-OW12000`**: de ruimtelijke bemonstering (keuze van de meetplaats).
  FOI = de waterloop, resultaat = de meetplaats (§6.3).

## 5. Procedure en ObservableProperty

**Procedures.** De bron vermeldt geen staalnameprocedure en geen analysemethode. Daarom heeft
geen enkele `sosa:Sampling` of `sosa:Observation` een `sosa:usedProcedure` (§6.4). Kandidaten
uit de VITO-lijst zijn `procedure:WAC_I_A_003` (schepmonster) en `CMA/1/A.11`
(oppervlaktewater), maar die zijn niet uit de data af te leiden.

**Property.** Zoals in stap 1 is elke `sosa:observedProperty` een CSOR-parameteraspect. Het wordt
gevonden via symbool + drager `water` + eenheid; alle 999 rijen koppelen eenduidig, aan 344
verschillende parameteraspecten. De dataset toont goed waarom het parameteraspect het juiste
niveau is:

- de grootheid verschilt per parameter: pH dimensieloos (E_74 "Geen"), geleidbaarheid (µS/cm),
  verzadiging (%), hardheid (Franse graden);
- de stofkwalificatie van de eenheid zit in het aspect: "massaconcentratie stikstof" voor KjN in
  mgN/L, "massaconcentratie tin" voor organotin in ngSn/L.

## 6. Modelleer-keuzes toegelicht

### 6.1 Waarom de meetplaats als `sosa:SpatialSample` van de waterloop?

> **Verworpen alternatief:** de meetplaats als FOI zonder band met de waterloop, of de waterloop
> rechtstreeks als FOI van de observaties.
> **Gekozen aanpak:** meetplaats = `Platform + FeatureOfInterest + SpatialSample`,
> `sosa:isSampleOf` de VHA-waterloop. Het staal is een monster van de meetplaats. De waterloop
> staat als `sosa:hasUltimateFeatureOfInterest` op collectie en observaties.
> **Motivatie:** R11 en R8. De meetplaats is een puntmonster van een groter studieobject. Het
> staal is genomen op de meetplaats. De keten staal → meetplaats → waterloop maakt de
> ruimtelijke representativiteit expliciet. `hasUltimateFeatureOfInterest` geeft een kort
> query-pad naar de waterloop.

### 6.2 Waarom de VHA-waterloop en niet het segment of het waterlichaam?

> **Gekozen aanpak:** ultiem FOI = de VHA-waterloop (`code:Vhag`, gewestcode 2801).
> **Motivatie:** het segment is enkel het geometrische aanknopingspunt. De meetplaats
> vertegenwoordigt de waterloop, niet één segment. Het KRW-waterlichaam is het
> beoordelingsobject voor normtoetsing en komt in fase 2, zodra er een waterlichamenlijst is
> (`../../featureofinterest.md` §3.2).

### 6.3 Waarom een aparte `sosa:Sampling` voor de keuze van de meetplaats?

> **Verworpen alternatief:** enkel `sosa:isSampleOf`, en de SHACL-melding aanvaarden dat de
> waterloop als `sosa:FeatureOfInterest` geen `isFeatureOfInterestOf` heeft.
> **Gekozen aanpak:** `ex:sampling-meetplaats-OW12000` (`sosa:Sampling`) met FOI = de waterloop
> en resultaat = de meetplaats.
> **Motivatie:** in SOSA is een (ruimtelijk) monster het resultaat van een bemonstering. Voor
> een SpatialSample is dat de keuze van de meetlocatie op het studieobject. Zo is de waterloop
> FOI van een echte Execution, en blijft het voorbeeld conform zonder vals-positieven. De
> sampling heeft geen tijd of procedure: de bron kent die niet.

### 6.4 Waarom geen `usedProcedure`, `madeBySampler` of `madeBySensor`?

> **Gekozen aanpak:** weglaten.
> **Motivatie:** de bron vermeldt geen staalnameprocedure, staalnemer, labo of analysemethode.
> In tegenstelling tot stap 1 is er ook geen `Aard Monstername`. Gefabriceerde waarden zouden
> als echte gegevens gelezen worden. R2 noemt `usedProcedure` en `madeBySensor` sterk aanbevolen,
> maar niet verplicht.

### 6.5 Waarom mag een meetplaats in Nederland aan een Vlaamse waterloop gekoppeld worden?

> **Gekozen aanpak:** `OW12000` (Isabellahaven, Philippine, NL) `sosa:isSampleOf` het
> Leopoldkanaal (VHA 2801).
> **Motivatie:** de VMM noemt het Leopoldkanaal als waterloop van deze meetplaats, en die ligt
> net over de grens (reverse geocoding van de Lambert-coördinaten: Isabellahaven, Philippine,
> Terneuzen). De VHA dekt enkel Vlaanderen, dus het dichtstbijzijnde VHA-segment ligt 629 m
> verderop. Daarom staat de koppeling op `controle = ja` in
> `meetplaats_waterloop.csv`. De waterloop is inhoudelijk juist; de afstand volgt uit de grens.
> Een grensoverschrijdende waterlichaamreferentie (KRW) zou dit in fase 2 zuiverder oplossen.

### 6.6 Waarom expliciete supertypes?

Zoals in stap 1 (`../afvalwater_concentraties/bespreking.md` §6.7): de pipeline valideert SHACL
zonder subklasse-inferentie. Dus `sosa:Execution` op de samplings en observaties,
`sosa:ExecutionCollection` op de collectie, en `sosa:Sample` + `sosa:FeatureOfInterest` op
meetplaats en staal. `sosa:SpatialSample` is een subklasse van `sosa:Sample`, maar dat wordt
niet afgeleid.

### 6.7 Waarom staal = (meetplaats, datum, tijdstip)?

> **Gekozen aanpak:** één `sosa:Sample` per unieke combinatie van meetplaats, datum en tijdstip;
> IRI `ex:staal-OW12000-2019-01-28T130100`.
> **Motivatie:** de bron heeft geen staal-ID. Alle parameters met dezelfde meetplaats, datum en
> tijd horen bij dezelfde monstername: per combinatie komt elke parameter precies één keer
> voor. Het tijdstip wordt afgerond op de seconde (Excel: `12:50:59.999` → `12:51:00`), zodat de
> IRI stabiel en leesbaar blijft.

### 6.8 Teken `<`, CSOR-eenheid, plat model

Identiek aan stap 1 (`../afvalwater_concentraties/bespreking.md` §6.4, §6.5, §6.9). Bij `<` is er
geen `numericValue`, maar `qudt:lowerBound 0` en `qudt:upperBound` = de gerapporteerde grens.
De bron levert hier geen expliciete onder- en bovengrens, zoals in 250108; het interval `[0, X]`
is afgeleid uit het teken. De eenheid is de CSOR-eenheid.

## 7. Tijdsmodellering

| Element | Patroon | Bron |
|---|---|---|
| staalname en collectie | `sosa:phenomenonTime → time:Instant → time:inXSDDateTime` | `Sample Datum Monstername` + `Sample Tijdstip Monstername` |

- `inXSDDateTime` en geen `inXSDDate`, omdat de bron een uur van staalname geeft.
- Er is geen tijdzone: de bron vermeldt er geen. Het gaat vermoedelijk om lokale tijd. Met een
  tijdzone zou `inXSDDateTimeStamp` gebruikt worden.
- `sosa:resultTime` staat niet in de bron.
- De meetplaatskeuze (`ex:sampling-meetplaats-OW12000`) heeft geen tijd.

## 8. Prefixen en IRI-structuur

| Prefix | Base URI | Tijdelijk of persistent |
|---|---|---|
| `ex:` | `https://example.org/waterkwaliteit/oppervlaktewater/` | tijdelijk (illustratief, R10) |
| `waterloop:` | `https://data.omgeving.vlaanderen.be/id/waterloop/` | persistent-bedoeld (VHA-gewestcode; herstelde LOD) |
| `waterlopen:` | `https://data.omgeving.vlaanderen.be/ns/waterlopen#` | persistent (waterlopen-vocabularium) |
| `csor-parameteraspect:`, `csor-eenheid:` | `https://data.omgeving.vlaanderen.be/id/concept/csor/…` | persistent (CSOR) |
| `matrix:` | `https://data.omgeving.vlaanderen.be/id/concept/matrix/` | persistent |
| `sosa:`, `qudt:`, `time:`, `geo:`, `dct:`, `skos:`, `rdfs:`, `xsd:` | W3C/QUDT/DCMI | persistent |

| Resource | Patroon |
|---|---|
| meetplaats, keuze meetplaats | `ex:meetplaats-<SP>`, `ex:sampling-meetplaats-<SP>` |
| staal, staalname, collectie, tijdstip | `ex:staal-<SP>-<datumTtijd>`, `ex:sampling-…`, `ex:collectie-…`, `ex:tijdstip-<datumTtijd>` |
| observatie, resultaat | `ex:observatie-<SP>-<datumTtijd>-<PAS_code>`, `ex:resultaat-…` |

De observatie-IRI gebruikt de code van het CSOR-parameteraspect (`PAS_…`), omdat de bron geen
parametercode heeft.

## 9. Inverse relaties

| Paar | Waarom |
|---|---|
| `sosa:hasSample` ↔ `sosa:isSampleOf` (waterloop → meetplaats → staal) | de keten in beide richtingen doorlopen: alle meetplaatsen van een waterloop, alle stalen van een meetplaats |
| `sosa:hasResult` ↔ `sosa:isResultOf` (sampling → staal/meetplaats; observatie → resultaat) | `isResultOf` is verplicht op `sosa:Result` en aanwezig op `sosa:Sample` (SHACL) |
| `sosa:hasFeatureOfInterest` ↔ `sosa:isFeatureOfInterestOf` (waterloop, meetplaats, staal) | `isFeatureOfInterestOf` is verplicht op `sosa:FeatureOfInterest` (SHACL) |

`sosa:hasMember` staat enkel op de collectie.
