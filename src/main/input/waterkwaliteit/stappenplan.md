# Stappenplan: SSN/SOSA-mapping van de VMM-waterkwaliteitsdata

Dit document bundelt het advies over de codelijsten en de stappen voor de volledige mapping van
`brondata_Jurgen/` naar SSN/SOSA 2023. Het bouwt voort op:

| Document | Inhoud |
|---|---|
| `bestaand_model/bestaand_model.md` | waarom het huidige OSLO-AP Waterkwaliteit niet volstaat |
| `brondata_Jurgen/README.md` | de datasets en de scope volgens de VMM |
| `codelijsten.md` | koppeling aan CSOR, NACE-BEL en de nieuwe lijsten |
| `featureofinterest.md` | FOI per soort meting; afstemming met RIE-IEPR en de VHA-waterlopen |

*Opgesteld 2026-09-29.*

---

## 1. Uitgangspunten

1. **Eerst de resultaten.** De mapping begint met de meetwaarden (concentraties, debieten,
   vrachten). Normen en beoordelingen komen in fase 2. Kenmerken van bedrijven, meetputten en
   waterlopen worden nu enkel gemodelleerd voor zover ze als FOI of identificator nodig zijn
   (scope van de VMM, zie `brondata_Jurgen/README.md`).
2. **Bestaande lijsten en modellen hergebruiken.** CSOR voor wat gemeten wordt en in welke eenheid,
   `codelijst-matrix` en `codelijst-observatieprocedure` voor matrix en staalname, NACE-BEL
   2008, RIE-IEPR voor lozingen (`riepr:Emissie`), en de herstelde VHA-waterlopen voor
   oppervlaktewater.
3. **Projectconventies** (`CLAUDE.md`):
   - SSN/SOSA 2023 zoals in de pipeline geladen (`sosa:Property`, `sosa:hasProperty`,
     `sosa:implements`);
   - `qudt:numericValue`;
   - geen blank nodes voor `time:Interval`/`time:Instant`, resultaten of geometrie in grote
     datasets (skolem-IRI's);
   - grote datasets als `.trig` met een kleine `.ttl` als validatie-subset;
   - alle `[VOCAB ERROR]`s opgelost vóór een commit.

---

## 2. Advies: codelijsten, eerst of niet?

**Advies: de nieuwe codelijsten níét eerst maken.** Voor de mapping van de resultaten (fase 1) is
geen enkele nieuwe lijst nodig. Soort afvalwater, DWA/RWA, lozingswijze en meetputtype zijn
kenmerken van de meetput of het lozingspunt, niet van de observatie. Volgens de scope van de VMM
vallen ze nu buiten de mapping.

### 2.1 Wat fase 1 nodig heeft, en waar het al bestaat

| Nodig voor de resultaten | Bestaande lijst | Status |
|---|---|---|
| `sosa:observedProperty` | CSOR-parameteraspect (`~/git/csor/codelijst-csor-parameteraspect`) | sluit 100 % aan (`codelijsten.md` §3.2) |
| eenheid van het resultaat | CSOR-eenheid (`~/git/csor/codelijst-csor-eenheid`) | alle 25 eenheden gevonden (`codelijsten.md` §3.3) |
| matrix (afvalwater, oppervlaktewater, waterbodem) | `~/git/codelijst-matrix` | bestaat |
| soort monstername = procedure van de `sosa:Sampling` | `~/git/codelijst-observatieprocedure`: `WAC/I/A/003` "Ogenblikkelijke monstername (schepmonster)", `WAC/I/A/004` "verzamelmonster" | bestaat; bij de VMM bevestigen dat "debietgebonden monster" = WAC/I/A/004 |
| activiteit van de exploitatie of meetput | NACE-BEL 2008 (`nacebel/nace2008_volledig.trig`) | 24/24 en 247/248 codes gevonden |

**Enige echte leemte: het resultaatteken** (`<`, `=`). Dat is eerst een modelleerbeslissing
(`codelijsten.md` §3.4); een lijst is maar een van de opties (zie B3 in §3).

### 2.2 Wat later nodig is, en waar het hoort

| Voorgestelde lijst | Hergebruik of nieuw | Waar |
|---|---|---|
| meetputtype (COLL, KAH, OPPW, RIO, IRWZI, Grondwater) | **uitbreiden**: `codelijst-rie-iepr` heeft al `lozingspunt_lozingsplaats` (oppervlaktewater, riool, grondwater); collector, kunstmatige afvoer hemelwater en influent RWZI toevoegen | `codelijst-rie-iepr` |
| soort afvalwater (bedrijfsafvalwater, huishoudelijk afvalwater, koelwater, hemelwater) | nieuw. Let op de overlap met `koelwater` in `codelijst-matrix`: kiezen of dit een matrix of een afvalwatersoort is. | `codelijst-rie-iepr`, bij de lozingspunt-eigenschappen |
| afvoertype DWA/RWA/NVT | nieuw | idem |
| lozingswijze (OW DIR, OW INDIR, onbekend) | nieuw | idem |
| positie in de zuivering (influent, effluent, andere) | nieuw; overlapt met meetputtype `IRWZI` | idem |
| databron (IMJV, MNT) | nieuw, of als `prov:Entity`/`dct:source` in plaats van een codelijst | te bespreken |
| categorie lozer (bedrijven, RWZI) | nieuw | te bespreken |
| herkomst staal (BEDR, VMM) | waarschijnlijk geen lijst: dit is wie de staalname uitvoerde (`sosa:Sampler`/`prov:Agent`) | te bespreken |
| bevestigingscode (R) | betekenis onbekend | navragen |
| normtype, toetswijze, beoordeling | nieuw | fase 2 |
| NACE-sector EIW/JV en subsector EIW (VMM-indeling) | nieuw: geen NACE-codes maar VMM-groeperingen van NACE-codes (JV `21` Voeding = NACE-afdelingen 10–12, niet NACE `21` farmaceutisch). Eenduidig afleidbaar uit de NACE-code (248/248). Als SKOS-lijst met `skos:narrowMatch` naar NACE-BEL 2008 (`codelijsten.md` §4.1). | bedrijfskenmerken, fase 3 |

`codelijst-rie-iepr` is de logische plaats: de CSV-naar-SKOS-pipeline bestaat daar al, en de
lijsten beschrijven dezelfde lozingspunten als RIE-IEPR (`featureofinterest.md` §2). Wanneer de
lijsten gemaakt worden, vraag je best **de volledige waardenlijsten** op bij de VMM. De uittreksels
bevatten enkel de waarden die toevallig voorkomen.

---

## 3. Beslissingen vóór of tijdens de mapping

| # | Beslissing | Voorstel | Nodig vóór | Bron |
|---|---|---|---|---|
| B1 | `sosa:observedProperty` = CSOR-parameteraspect? | ja | stap 1 | `codelijsten.md` §3.2 |
| B2 | `qudt:hasUnit` → CSOR-eenheid (QUDT via `skos:*Match`) of rechtstreeks QUDT? | CSOR-eenheid; dit wijkt af van R3 en moet bevestigd worden | stap 1 | `codelijsten.md` §3.3 |
| B3 | Hoe het resultaatteken `<` en de aantoonbaarheids-/bepaalbaarheidsgrens modelleren? | te beslissen: eigen lijst, CSOR kwalificeerbaar aspect `Aantoonbaarheid`, of grenzen als eigenschappen van het resultaat | stap 1 | `codelijsten.md` §3.4 |
| B4 | FOI van een concentratie op een afvalwaterstaal | staal (`sosa:Sample`) als FOI, `riepr:Emissie` als `sosa:hasUltimateFeatureOfInterest`; afstemmen met RIE-IEPR | stap 1 | `featureofinterest.md` §2.4 |
| B5 | IRI's | illustratief `https://example.org/waterkwaliteit/…` (R10); bestaande IRI's hergebruiken waar ze bestaan (CSOR, NACE, VHA, codelijsten) | stap 1 | `codelijsten.md` §6 |
| B6 | Afstemming met RIE-IEPR (observedProperty, eenheid, SSN-versie) | met het RIE-IEPR-team, parallel aan stap 1–3 | stap 3 | `featureofinterest.md` §2.5 |
| B7 | Referentie voor stilstaand water (De Nekker, Blaarmeersen) | KRW-waterlichamen of VHA-plassen | stap 2 | `featureofinterest.md` §3.3 |

---

## 4. Stappen

### Fase 0: voorbereiding (afgerond)

- [x] Excel naar JSON per tab (`brondata_Jurgen/xlsx_naar_json.py`)
- [x] NACE-BEL 2008 en 2025 volledig opgehaald (`scripts/nace_ophalen.py`)
- [x] Koppeling van de brondata aan CSOR-parameter, -parameteraspect en -eenheid geanalyseerd (`codelijsten.md`)
- [x] Bekende CSOR-kwaliteitspunten nagekeken op impact (`codelijsten.md` §3.5)
- [x] FOI-strategie en aansluiting op RIE-IEPR uitgewerkt (`featureofinterest.md`)
- [x] VHA-waterlopen-LOD hersteld (`scripts/waterlopen_herstel.py`) en validatie-subset voor de 54 meetplaatsen gemaakt (`scripts/waterlopen_subset.py`)
- [x] Waterlopen-vocabularium met OWL-restricties in `src/main/resources/` (gegenereerde SHACL, getest)

### Fase 1: resultaten

Elke stap levert een datavoorbeeld in `nieuw_model/<voorbeeld>/`, met de verplichte bestandsset
uit `CLAUDE.md` §3:

```
<naam>.ttl        kleine, representatieve subset, door de pipeline gevalideerd
<naam>.trig       volledige omzetting (buiten de pipeline), indien groot
<naam>.mmd        Mermaid-diagram (CLAUDE.md §6)
README.md         intent, bronbestand, transformatiepipeline
bespreking.md     de 9 verplichte secties (CLAUDE.md §5)
```

De omzetting gebeurt met een script in `scripts/` (brondata-JSON → RDF), zodat ze herhaalbaar is
en de subset en de volledige set uit dezelfde code komen.

#### Stap 1: concentraties in afvalwater (`250108`)

> **Status (2026-09-29): eerste versie klaar** in `nieuw_model/afvalwater_concentraties/`
> (script `scripts/afvalwater_concentraties.py`). Subset en volledige set zijn conform SHACL,
> zonder `[VOCAB ERROR]`. Voorlopig volgens de voorstellen B1, B2 en B4. B3 is deels ingevuld:
> teken via `qudt:lowerBound`/`upperBound`; de aantoonbaarheids- en bepaalbaarheidsgrens zijn nog
> open. Zie `bespreking.md` §6.

De kern van het voorbeeld: de rijkste structuur (staal, meetpunt, grenzen, teken).

- **Infrastructuur:** meetpunt (VMM-meetput; sleutel = het nummer uit `Sample Point Naam`, zie V4)
  als `riepr:Meetpunt`, met de VMM-code als `adms:identifier` (`featureofinterest.md` §2.2);
  exploitatie enkel als identificator.
- **Bemonstering:** per `Sample ID` een `sosa:Sampling` (datum; procedure = soort monstername uit
  `codelijst-observatieprocedure`) en een `sosa:Sample` (het staal) `sosa:isSampleOf` de
  `riepr:Emissie` (B4).
- **Observaties:** één `sosa:Observation` per parameter per staal, gegroepeerd in een
  `sosa:ObservationCollection` per staal. De gedeelde metadata (FOI, tijd, sampling) staan op
  de collectie.
  - `observedProperty` = CSOR-parameteraspect: via `Parameter Code` (`P_…`) en de eenheid
    (`codelijsten.md` §3.1–3.2);
  - resultaat met `qudt:numericValue` en de eenheid (B2), plus het teken en de grenzen (B3);
  - matrix via `codelijst-matrix` (`afvalwater`).
- **Tijd:** `phenomenonTime` = moment van staalname (`time:Instant`, `Datum Dag`).
- **Subset voor `.ttl`:** één staal van één meetpunt, met zowel `<`- als `=`-resultaten.
- **Controle:** pipeline zonder `[VOCAB ERROR]`; SHACL conform.

#### Stap 2: concentraties in oppervlaktewater (`250114`)

> **Status (2026-09-30): eerste versie klaar** in `nieuw_model/oppervlaktewater_concentraties/`
> (script `scripts/oppervlaktewater_concentraties.py`; gedeelde CSOR-code in
> `scripts/waterkwaliteit_gemeen.py`). 999 observaties, 3 stalen. Subset en volledige set zijn
> conform SHACL, zonder `[VOCAB ERROR]`.
> - De meetplaats is het resultaat van een eigen `sosa:Sampling` (keuze van de meetplaats), zodat
>   ook de waterloop FOI van een Execution is.
> - `OW12000` ligt in Nederland (Philippine); de koppeling met het Leopoldkanaal (629 m) is
>   inhoudelijk juist.
> - Procedure en staalnemer ontbreken in de bron.

- **Keten:** staal → meetplaats `OWxxxx` (`sosa:Platform + sosa:FeatureOfInterest + sosa:SpatialSample`,
  `geo:hasGeometry` uit Lambert 72) → VHA-waterloop (`code:Vhag`) als ultiem FOI (R8, R11;
  `featureofinterest.md` §3).
- **Koppeling:** `waterlopen/meetplaats_waterloop.csv`. De 9 meetplaatsen met `controle = ja`
  worden eerst nagekeken (B7 voor de twee meren).
- **Validatie:** met `waterlopen/waterlopen_meetplaatsen.ttl`, die mee gevalideerd wordt.
- **Hergebruik:** hetzelfde observatiepatroon als stap 1: `observedProperty`, eenheid, teken.
- **Subset:** één staal (de uittreksels bevatten 3 staalnamedata op `OW12000`).

#### Stap 3: jaardebieten van lozingen (`250129`)

> **Status (2026-09-30): eerste versie klaar** in `nieuw_model/afvalwater_debieten/` (script
> `scripts/afvalwater_debieten.py`). 1555 observaties. Subset (AGC Glass Mol) en volledige set
> zijn conform SHACL, zonder `[VOCAB ERROR]`; samengevoegd met stap 1 ook conform.
> - Dezelfde IRI's voor meetput, lozing en exploitatie als stap 1; 59 lozingen hebben zowel
>   stalen als een jaardebiet.
> - De AGC-meetputten verwijzen met `rdfs:seeAlso` naar de RIE-IEPR-controle-inrichtingen.
> - Databron IMJV/MNT als `prov:used`.
> - Let op: de concentraties (stap 1) zijn van 2024, de debieten van 2023. Voor vrachten dus
>   `251013` gebruiken (stap 4).

- **FOI:** `riepr:Emissie` (de lozing), `madeBySensor` = de controle-inrichting (`riepr:Meetpunt`)
  (`featureofinterest.md` §2.3).
- **Wat gemeten wordt:** `observedProperty` = "Q (standaard in water): debiet"; eenheid
  `m³/jr` (CSOR E_50, via een labelmapping van `m³/jaar`).
- **Tijd:** `phenomenonTime` = `time:Interval` van het kalenderjaar (R12).
- **Herkomst:** `Databron Jaardebiet` (IMJV/MNT) als provenance.
- **End-to-end voorbeeld met RIE-IEPR:** AGC Glass Mol, meetputten `2400006` en `2400007`,
  sluit aan op `~/git/RIE-IEPR/documentatie/datamodel/datavoorbeelden/agc-glass_MJV_18-09-2026.ttl`.

#### Stap 4: vrachten (`251013`, `240426`)

- **`251013` contrastmiddelen:** per type meetput en jaar staan concentratie, debiet en
  bruto/netto vracht in de data. Dat is een volledig voorbeeld van een **afgeleide observatie**:
  de vracht met `sosa:hasInputValue` naar de concentratie- en debietobservaties, en
  `sosa:relatedObservation`. De vracht is geen lid van de collectie (R7, R13).
  `observedProperty` = het parameteraspect "…: vracht".
- **`240426` PFAS-jaarvrachten:** enkel de vracht, zonder brongegevens. Modelleren als observatie
  met een berekeningsprocedure (`sosa:usedProcedure`) en `phenomenonTime` = jaar. De inputs zijn
  niet beschikbaar; documenteren in `bespreking.md`.

### Fase 2: normen en beoordelingen (`250124`)

- **Modelleren buiten SSN/SOSA** (zoals de VMM voorstelt): de norm (Vlarem, triggerwaarde,
  toetswijze MAX/MIN) als eigen resource, gekoppeld aan het CSOR-parameteraspect en de eenheid.
- **Beoordeling:** het oordeel over een jaarmeting ten opzichte van een norm. Uit te werken:
  een `sosa:Observation` met een kwalitatief resultaat (goed / niet goed / geen beoordeling), of
  een eigen beoordelingsklasse die met `prov:used` naar meting en norm verwijst.
- **FOI:** waterbodem op de meetplaats, met het KRW-waterlichaam als ultiem FOI.
  Voorwaarde: een waterlichamenlijst (`featureofinterest.md` §3.4, punt 3).
- **Nieuwe lijsten:** normtype, toetswijze, beoordeling.
- **Coördinaten:** eerst nagaan of de Lambert-waarden in deze dataset Lambert 2008 zijn.

### Fase 3: kenmerken en afstemming (later)

- Meetpunt-, lozingspunt- en bedrijfskenmerken modelleren (soort afvalwater, DWA/RWA,
  lozingswijze, meetputtype, NACE-sector), met de lijsten uit §2.2 in `codelijst-rie-iepr`.
- Het resultaat terugkoppelen aan het RIE-IEPR-model (B6) en aan de herziening van het OSLO-AP
  Waterkwaliteit (`bestaand_model/bestaand_model.md` §6).

---

## 5. Vragen voor de VMM

| # | Vraag | Nodig voor |
|---|---|---|
| V1 | Is "debietgebonden monster" hetzelfde als een verzamelmonster (WAC/I/A/004)? Welke andere soorten monstername komen voor? | stap 1 |
| V2 | Wat is de exacte betekenis van `<` samen met `Resultaat Aantoonbaarheid` en `Resultaat Bepaalbaarheid`: is de gerapporteerde waarde dan de aantoonbaarheids- of de bepaalbaarheidsgrens? | stap 1 (B3) |
| V3 | Wat betekent `Bevestiging Code` = `R`? | stap 1 |
| V4 | Het nummer in `Sample Point Naam` (`AW1850022` → `1850022`) komt overeen met `Meetput Nummer`: 59 van de 60 meetpunten uit `250108` staan ook in `250129`, 44 in `240426`. `Sample Point ID` volgt dat nummer niet altijd (`E9992055` hoort bij `AW1850022`). Wat is `Sample Point ID`, en is `Sample Point Naam` de juiste sleutel naar de meetput? | stap 1, 3 |
| V5 | `OW162000` en `OW164000`: Beneden- of Boven-Zeeschelde? | stap 2 |
| V6 | Welke referentie gebruikt de VMM voor meetplaatsen in stilstaand water? | stap 2 (B7) |
| V7 | Zijn de coördinaten in `250124` Lambert 2008? | fase 2 |
| V8 | Volledige waardenlijsten van meetputtype, lozingswijze, DWA/RWA, soort afvalwater, positie in de zuivering | fase 3 |
| V9 | Wat betekent databron "MNT" bij het jaardebiet (naast IMJV)? En met welke procedure wordt het debiet bepaald (kandidaat `WAC/I/1/012`)? | stap 3 |

Voor het VHA-beheer (en niet voor de VMM-data): 133 `code:vhag`-verwijzingen in de segmenten
verwijzen naar waterlopen die niet in de VHA-waterlopen voorkomen
(`featureofinterest.md` §3.4).
