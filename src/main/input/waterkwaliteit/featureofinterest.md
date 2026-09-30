# FeatureOfInterest in de waterkwaliteit-mapping

Wat wordt er in de VMM-brondata eigenlijk geobserveerd? Dit document legt het
`sosa:FeatureOfInterest` (FOI) vast per soort meting, en de aansluiting op twee bestaande
modellen:

- **RIE-IEPR** (`~/git/RIE-IEPR`): daarin is `riepr:Emissie` het FOI van metingen aan een
  lozing of uitstoot.
- **VHA-waterlopen als LOD** (`~/git/shapefile_to_rdf/rdf`): de referentiedataset voor metingen
  in oppervlaktewater.

Aanvullend bij `codelijsten.md` (wat er gemeten wordt) en `brondata_Jurgen/README.md` (scope).
Alle cijfers zijn nagekeken op 2026-09-29.

---

## 1. Samenvatting

| Soort meting | Datasets | Rechtstreeks FOI | Ultiem FOI | Infrastructuur (sensor/platform) |
|---|---|---|---|---|
| Concentratie in afvalwater, per staal | `250108` | staal (`sosa:Sample`) | `riepr:Emissie` (de lozing) | `riepr:Meetpunt` (controle-inrichting) = VMM-meetput |
| Jaarvracht en jaardebiet van een lozing | `240426`, `250129`, `251013` | `riepr:Emissie` | idem | idem |
| Concentratie in oppervlaktewater, per staal | `250114` | staal (`sosa:Sample`) → meetplaats (`sosa:SpatialSample`) | VHA-waterloop (`code:Vhag`) | meetplaats als `sosa:Platform` |
| Waterbodem (fase 2) | `250124` | sedimentstaal → meetplaats | VHA-waterloop / waterlichaam | idem |

---

## 2. Afvalwater: aansluiten op RIE-IEPR

### 2.1 Het RIE-IEPR-model

Uit `riepr.ttl` (`~/git/RIE-IEPR/src/main/resources/be/vlaanderen/omgeving/riepr/data/ns/riepr/riepr.ttl`)
en `documentatie/datamodel/afname/observaties.md`:

- `riepr:Emissie` ⊂ `prov:Entity`, `sosa:FeatureOfInterest`. Een emissie is een gebeurtenis:
  het lozen van stoffen aan een emissiepunt. Ze is `prov:wasDerivedFrom` het emissieproces
  (verplicht) en heeft zelf geen tijd; die zit in de observaties. `riepr:Onttrekking` en
  `riepr:Verbruik` volgen hetzelfde patroon.
- `riepr:Emissiepunt` (bv. `dct:type …/emissiepunt-type/lozingspunt`) en `riepr:Meetpunt`
  (bv. `…/meetpunt-type/controleinrichting`) zijn `ssn:System`, gehost op de
  `riepr:Exploitatielocatie` (⊂ `sosa:Platform`).
- `riepr:Proces` (⊂ `pplan:Plan`, `pplan:Step`, `sosa:Procedure`) verbindt ze: een emissieproces
  wordt `ssn:implementedBy` het emissiepunt, een meetproces `ssn:implementedBy` het meetpunt.
- `riepr:Observatie` (⊂ `sosa:Observation`): `sosa:hasFeatureOfInterest` → Emissie (exact 1),
  `sosa:madeBySensor` → Meetpunt, `sosa:hasResult` → `riepr:Resultaat` (⊂ `sosa:Result`,
  `qb:Observation`, met een eigen URI). `riepr:ObservatieVerzameling` groepeert de observaties
  van één meting.

Het datavoorbeeld `documentatie/datamodel/datavoorbeelden/agc-glass_MJV_18-09-2026.ttl` bevat
enkel de structurele kant (21 installaties, 12 emissiepunten, 10 meetpunten, 50 processen). Er
zitten nog geen `Emissie`- of `Observatie`-instanties in. Het observatiepatroon staat enkel in
`observaties.md` §8.

### 2.2 Koppelsleutel: VMM-meetputnummer = `vmm:lozingspuntCode`

In het AGC-voorbeeld draagt elke controle-inrichting de VMM-meetput als identificator:

```turtle
<https://data.mjv.omgeving.vlaanderen.be/id/meetpunt/019e9271-145f-75f2-8222-342e7028bb37/2026-01-01/2026-01-01T10:00:00Z>
    a riepr:Meetpunt, ssn:System ;
    dct:type <https://data.omgeving.vlaanderen.be/id/concept/riepr/meetpunt-type/controleinrichting> ;
    adms:identifier [ a adms:Identifier ; adms:schemaAgency "VMM" ;
                      skos:notation "2400006"^^vmm:lozingspuntCode ] ;
    rdfs:label "Controleinrichting LP01 Industrieel glasfabriek"@nl .
```

Diezelfde meetputten komen voor in de VMM-brondata:

| Meetput | RIE-IEPR (AGC-voorbeeld) | `250129` lozingsdebieten 2023 |
|---|---|---|
| `2400006` | Controleinrichting LP01 Industrieel glasfabriek | AGC GLASS EUROPE VESTIGING MOL: **244 378 m³/jaar** |
| `2400007` | Controleinrichting LP02 Industrieel Kempenglas | AGC FABRICATION - KEMPENGLAS: **27 784 m³/jaar** |
| `9991095` | Controleinrichting LP07 Industrieel Coater | niet in het uittreksel |

`Meetput Nummer` (`250129`, `240426`), `Sample Point ID`/`Naam` (`250108`, bv. `E3530025` /
`AW3530025`) en de `SPs`-lijst verwijzen dus naar hetzelfde object als `vmm:lozingspuntCode` in
RIE-IEPR. Het AGC-jaardebiet is daarmee een concreet, end-to-end voorbeeld dat RIE-IEPR (de
structuur) en de VMM-meetwaarden (de operationele kant) samenbrengt.

### 2.3 Voorstel voor vrachten en debieten (`240426`, `250129`, `251013`)

Een jaarvracht of jaardebiet gaat over de lozing als geheel. Het FOI is dus de `riepr:Emissie`,
precies zoals in RIE-IEPR:

```turtle
<…/id/emissie/…> a riepr:Emissie ;                          # lozing aan LP01
    prov:wasDerivedFrom <…/id/proces/…> .                    # emissieproces, implementedBy emissiepunt LP01

<…/observatie/…> a riepr:Observatie ;
    sosa:hasFeatureOfInterest <…/id/emissie/…> ;
    sosa:madeBySensor <…/id/meetpunt/019e9271-145f-…/2026-01-01/2026-01-01T10:00:00Z> ;   # meetput 2400006
    sosa:observedProperty <https://data.omgeving.vlaanderen.be/id/concept/csor/parameteraspect/…> ;  # Q (standaard in water): debiet
    sosa:phenomenonTime [ a time:Interval ;                  # R12: kalenderjaar 2023
        time:hasBeginning [ time:inXSDDate "2023-01-01"^^xsd:date ] ;
        time:hasEnd       [ time:inXSDDate "2024-01-01"^^xsd:date ] ] ;
    sosa:hasResult [ a riepr:Resultaat ; qudt:numericValue 244378 ;
                     qudt:hasUnit <https://data.omgeving.vlaanderen.be/id/concept/csor/eenheid/E_50> ] ;  # m³/jr
    prov:wasDerivedFrom <…databron IMJV/MNT…> .
```

De vracht is concentratie × debiet. Dat wordt een afgeleide observatie met `sosa:hasInputValue`
naar de concentratie- en debietobservaties (R7, R13). `251013` levert die drie grootheden per jaar.

### 2.4 Voorstel voor concentraties per staal (`250108`)

Een analyse gebeurt op een **staal** (`Sample ID`, `Aard Monstername` = schepmonster of
debietgebonden monster) dat op de meetput uit de lozing genomen is. Twee opties:

| | A. FOI = Emissie (RIE-IEPR as-is) | B. FOI = staal, ultiem FOI = Emissie (R8) |
|---|---|---|
| `sosa:hasFeatureOfInterest` | `riepr:Emissie` | `sosa:Sample` (het staal) |
| Staal | niet expliciet, of enkel als `prov:used` | `sosa:Sample` `sosa:isSampleOf` Emissie, `sosa:isResultOf` een `sosa:Sampling` met `sosa:usedProcedure` = soort monstername |
| `sosa:hasUltimateFeatureOfInterest` | niet nodig | Emissie |
| Past bij de SHACL van RIE-IEPR (FOI exact 1 Emissie) | ja | **nee**: RIE-IEPR moet dan ook `sosa:Sample` als FOI toelaten |
| Staalnametijd, soort monstername, herkomst staal (BEDR/VMM) | valt weg of komt op de observatie | natuurlijk op de `sosa:Sampling` |

**Voorstel: B.** Het staal draagt echte informatie: de soort monstername uit `codelijsten.md` §5
als procedure van de sampling, en het tijdstip. Eén staal levert ook tientallen parameters (1998
resultaten in `250108`), wat meteen een natuurlijke `ObservatieVerzameling` per staal geeft. Dit
vraagt een kleine uitbreiding van RIE-IEPR: FOI = Emissie **of** Sample met
`sosa:hasUltimateFeatureOfInterest` Emissie. Dat moet met het RIE-IEPR-team afgestemd worden.

### 2.5 Verschillen tussen RIE-IEPR en dit project die afgestemd moeten worden

| Onderwerp | RIE-IEPR | Dit project / voorstel | Actie |
|---|---|---|---|
| `sosa:observedProperty` | chemische stof via InChIKey (`…/id/concept/chemische_stof/<InChIKey>`) of een operationele codelijst | CSOR-parameteraspect (`codelijsten.md` §3.2) | Afstemmen. `riepr.ttl` kent zelf al `riepr:parameterAspect` met bereik `csor:ParameterAspect` (op `Systeemeigenschap`), dus CSOR is daar al aanwezig. Een InChIKey onderscheidt concentratie, vracht en debiet niet. |
| Eenheid | `qudt:hasUnit unit:MG-PER-M3` (rechtstreeks QUDT) | CSOR-eenheid, met QUDT via `skos:*Match` (`codelijsten.md` §3.3) | Afstemmen. Voor stofgekwalificeerde eenheden (`mgN/L`) volstaat QUDT niet. |
| SSN-namespace | `ssn:System`, `ssn:hasProperty`, `ssn:implementedBy`, `ssn:hasSubSystem` | de pipeline van dit project laadt SSN/SOSA 2023, waar o.a. `sosa:System`, `sosa:hasProperty` en `sosa:implements` gebruikt worden | Nagaan welke SSN-versie RIE-IEPR volgt. Wie beide modellen combineert, moet één versie kiezen. |
| Bereik van `sosa:madeBySensor` | verruimd tot `ssn:System` (het meetpunt) | SOSA 2023 geeft enkel `schema:rangeIncludes sosa:Sensor`, geen strikte `rdfs:range` | Geen hard conflict, maar de bedoeling van SOSA is een sensor. Het meetpunt ook als `sosa:Sensor` typeren maakt het expliciet. |
| IRI's | `https://data.mjv.omgeving.vlaanderen.be/id/<klasse>/<uuid>/<issued>/<created>` (geversioneerd) | `example.org` in dit project | Bij een echte koppeling de RIE-IEPR-IRI's overnemen. |

---

## 3. Oppervlaktewater: VHA-waterlopen als ultiem FOI

### 3.1 De waterlopen-LOD (`~/git/shapefile_to_rdf/rdf`)

| Bestand | Klasse | IRI-patroon | Aantal |
|---|---|---|---|
| `vhag.ttl` (44 MB) | `code:Vhag` VHA-waterloop (bron tot monding) | `https://data.omgeving.vlaanderen.be/id/waterloop/<n>` | 27 239 |
| `wlas.ttl` (89 MB) | `code:Wlas` VHA-waterloopsegment | `https://data.omgeving.vlaanderen.be/id/waterloop/waterloopsegment/<n>` | 64 863 |
| `vhacattraj.ttl` (47 MB) | `code:VhaCattraj` categorietraject | `https://data.omgeving.vlaanderen.be/id/waterloop/categorietraject/<n>` | |
| `ontology/*.ttl` | vocabularium en SKOS: bekken, categorie, beheerder | `https://data.omgeving.vlaanderen.be/ns/waterlopen#`, `…/id/concept/waterlopen/<lijst>/<code>` | |

Een segment verwijst naar zijn waterloop (`code:vhag`), bekken (`code:beknr`), stroomgebied
(`code:strmgeb`), categorie (`code:catc`), beheerder (`code:beheer`) en KRW-waterlichaam
(`code:wtrlichc`). De geometrie staat als `geosparql:asWKT` in WGS84 lon/lat.

### 3.2 Voorstel

```
staal (sosa:Sample) ──isSampleOf──▶ meetplaats OWxxxx (sosa:SpatialSample + sosa:Platform, geo:hasGeometry)
                                        └──isSampleOf──▶ VHA-waterloop (code:Vhag)   ← sosa:hasUltimateFeatureOfInterest
```

- Dat is R11 (meetpunt als `sosa:Platform + sosa:FeatureOfInterest + sosa:SpatialSample`) en R8
  (een keten van samples).
- De waterloop (`code:Vhag`) is het ultieme FOI, en niet het segment. Een meetplaats
  vertegenwoordigt de waterloop. Het segment is enkel het geometrische aanknopingspunt.
- Het KRW-waterlichaam (`code:wtrlichc` op het segment) is het beoordelingsobject voor de
  normtoetsing en het SGBP. Het wordt pas FOI in fase 2 (normen en beoordelingen, `250124`).

### 3.3 Koppeling van de 54 VMM-meetplaatsen (`250114/SamplePoints`)

| Methode | Resultaat |
|---|---|
| `Waterloop`-naam = VHA-roepnaam (`rdfs:label`, hoofdletterongevoelig) | 30/54. Samengestelde VMM-namen zoals `GROTE NETE - NETE` of `LEIE - GRENSLEIE` matchen niet. |
| Dichtstbijzijnd segment (Lambert 72 → segment in EPSG:31370) | mediaan **7 m**, 44/54 binnen 50 m, maximum 1142 m (`OW179000`) |
| Dichtstbijzijnd segment én zijn roepnaam komt voor in de VMM-naam | **48/54** |

Aanbevolen koppelregel: het dichtstbijzijnde segment waarvan de roepnaam in de VMM-waterloopnaam
voorkomt. Is er geen, of ligt het verder dan een drempel (bv. 100 m), dan manueel nakijken.
Voorbeeld van een twijfelgeval: `OW162000` (Hemiksem) heet bij de VMM "ZEESCHELDE -
BENEDEN-ZEESCHELDE", maar ligt het dichtst (159 m) bij een segment van de Boven-Zeeschelde.

De koppeling is uitgevoerd met `scripts/waterlopen_subset.py` (zoekstraal 2 km, drempel 100 m).
Resultaat in `waterlopen/meetplaats_waterloop.csv`: 54 meetplaatsen gekoppeld aan 54 segmenten en
37 waterlopen. 9 meetplaatsen staan op `controle = ja`:

| Meetplaats | VMM-waterloop | Gekoppeld segment | Afstand | Opmerking |
|---|---|---|---|---|
| OW12000 | LEOPOLDKANAAL | Leopoldkanaal | 629 m | naam klopt, maar ver |
| OW179000 | BOVENSCHELDE | Bovenschelde | 1142 m | naam klopt, maar ver |
| OW72000 | MARK - DE MARK | Mark | 113 m | naam klopt, net boven de drempel |
| OW804000 | HAVENDOK - KANAALDOK B1 - KANAALDOK B2 | Havendok | 183 m | naam klopt; dok |
| OW162000 | ZEESCHELDE - BENEDEN-ZEESCHELDE | Boven-Zeeschelde | 159 m | Beneden of Boven? |
| OW164000 | ZEESCHELDE - BENEDEN-ZEESCHELDE | Boven-Zeeschelde | 5 m | Beneden of Boven? |
| OW851700 | ZUIDWILLEMSVAART (NOORD) | Zuid-Willemsvaart | 10 m | schrijfwijze verschilt, koppeling lijkt juist |
| OW377220 | DE NEKKER | Platte Beek | 169 m | **stilstaand water** (recreatieplas), geen VHA-waterloop |
| OW570150 | BLAARMEERSEN | Leiearm | 416 m | **stilstaand water**, geen VHA-waterloop |

Voor stilstaande wateren is de VHA-waterlopen-LOD niet het juiste ultieme FOI. Daarvoor is een
aparte referentie nodig, bv. de KRW-waterlichamen of de VHA-plassen.

De validatie-subset `waterlopen/waterlopen_meetplaatsen.ttl` (1383 triples, 1,9 MB) bevat de 54
segmenten en 37 waterlopen. Het vocabularium staat in
`src/main/resources/be/vlaanderen/omgeving/data/ns/waterlopen/waterlopen.ttl`, met de bereiken
van `code:vhag` en `code:beknr` verbeterd. De subset gaat door de pipeline zonder
`[VOCAB ERROR]` en conform SHACL.

`Bekken` in de VMM-data gebruikt andere labels dan de bekkenlijst (`Bekken van de Brugse Polders`
tegenover `Bekken Brugse polders`, `Dijle- en Zennebekken` tegenover `Dijlebekken`). Via het
segment krijg je het bekken rechtstreeks (`code:beknr`); een labelmapping is dan niet nodig.

### 3.4 Problemen in de waterlopen-dataset (op te lossen vóór hergebruik)

1. **De IRI van een waterloop is niet de VHA-code.** Een `code:Vhag` krijgt als IRI zijn
   objectnummer, terwijl `code:vhag` (ook op zichzelf) naar de gewestcode verwijst:

   | Verwijzing vanuit een segment | Bedoeld | Maar `waterloop:<n>` is |
   |---|---|---|
   | `waterloop:6551` (segment van de Dijle) | Dijle, gewestcode 6551 | Stratenbeek (de Dijle heeft IRI `waterloop:4520`) |
   | `waterloop:2802` (segment Zwartesluisbeek) | Zwartesluisbeek, gewestcode 2802 | Vrouwenhofbeek |
   | `waterloop:1` (segment Bovenschelde) | Bovenschelde, gewestcode 1 | Kanaal Leuven-Dijle |

   Van de 27 372 verschillende `code:vhag`-verwijzingen in `wlas.ttl` komen er 17 457 uit bij een
   bestaand `code:Vhag`-subject, maar door toeval van nummers bij de **verkeerde** waterloop. De
   overige 9 915 wijzen naar niets. **Oplossing:** de `code:Vhag`-IRI maken uit de gewestcode
   (`waterloop:<vhag>`), die stabiel is en door andere bronnen gebruikt wordt.
   Dit gebeurt met `scripts/waterlopen_herstel.py`: het leest de originelen uit `~/git/shapefile_to_rdf/rdf` en schrijft `waterlopen/<naam>.trig`. Na het
   herstel verwijzen alle 27 239 verwijzingen uit `vhacattraj` naar een bestaande waterloop. In
   `wlas` blijven er 133 verwijzingen over naar gewestcodes die niet in `vhag` voorkomen (bv.
   `waterloop:46801`, `waterloop:71657`); die moeten in de bron nagekeken worden.
2. `code:vhazonenr` (bv. `waterloop:080`, `waterloop:12`) gebruikt dezelfde `waterloop:`-namespace
   als de waterlopen zelf, met kans op botsingen. Die hoort een eigen namespace of codelijst te
   krijgen.
3. De 2040 `waterlichaam:`-IRI's (`…/id/concept/waterlopen/waterlichaam/<code>`) en de
   `stroomgebied:`-concepten zijn nergens als concept gedefinieerd: er is geen ConceptScheme in
   `ontology/`. Voor fase 2 is een waterlichamenlijst nodig, idealiter afgestemd op de officiële
   KRW-waterlichamen.
4. De dataset is groot (`all.ttl` 179 MB). Gebruik in dit project enkel een uittreksel van de
   gebruikte waterlopen en segmenten, als `.trig` buiten de Maven-validatie.

---

## 4. Open beslissingen

| # | Vraag | Voorstel |
|---|---|---|
| 1 | FOI van een concentratie op een afvalwaterstaal | B: staal als FOI, Emissie als ultiem FOI (§2.4); afstemmen met RIE-IEPR |
| 2 | observedProperty en eenheid gelijk trekken met RIE-IEPR | CSOR-parameteraspect en CSOR-eenheid (§2.5) |
| 3 | SSN-versie en `madeBySensor`-bereik | één versie kiezen (SOSA/SSN 2023); meetpunt ook als `sosa:Sensor` typeren |
| 4 | Ultiem FOI in oppervlaktewater | VHA-waterloop; waterlichaam pas in fase 2 (§3.2) |
| 5 | IRI-fout in de waterlopen-LOD | eerst herstellen in `shapefile_to_rdf` (§3.4) |
