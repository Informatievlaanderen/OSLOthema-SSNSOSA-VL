# Bespreking: vrachten van lozingen

## 1. Wat stelt dit voorbeeld voor?

Een vracht is de hoeveelheid van een stof die een lozing in een periode uitstoot:
concentratie × geloosd volume. De VMM berekent vrachten per lozing en per groep van lozingen.
Dit voorbeeld modelleert ze als **afgeleide** SSN/SOSA 2023-observaties, op basis van twee
VMM-exports:

- **`251013` contrastmiddelen:** periodevrachten van drie jodiumhoudende contrastmiddelen
  (amidotrizoïnezuur, iopamidol, iopromide) per groep van lozingen, 2014–2025, met de
  concentratie en het debiet waaruit ze berekend zijn.
- **`240426` PFAS:** bruto jaarvrachten van 5 PFAS op 256 meetputten, 2008–2023, zonder
  brongegevens.

De subsets tonen de lozingen van bedrijven via riool in 2014 (contrastmiddelen) en meetput
`2030042` (PFAS), waar de exploitant in de tijd wisselt.

## 2. Kleurlegenda

| Kleur | SOSA-concept | Domeinbetekenis |
|---|---|---|
| Blauw (#60c4e4) | `sosa:FeatureOfInterest` · `prov:Entity` | groep van lozingen, lozing |
| Paars (#c6a0f5) | `sosa:ObservingProcedure` | berekening van de bruto vracht |
| Oranje (#fe7130) | `sosa:Property`, CSOR kwantificeerbaar aspect | parameteraspecten; abstracte in- en uitvoertypes |
| Roze (#e54b89) | `sosa:ObservationCollection`, `sosa:Observation` | bronobservaties (concentratie, debiet), vrachten |
| Lichtgeel (#f8e1ad), subgraaf DERIVATION | afgeleide observaties | bruto en netto vracht |
| Geel-oranje (#f8b622) | `time:Interval` | kalenderjaar |

## 3. Infrastructuur (blauwe nodes)

- **`ex:lozingsgroep-bedrijven-rio`**: `wk:Emissie` (A14) + `sosa:FeatureOfInterest + prov:Entity`,
  `dct:type matrix:afvalwater`. Een **groep van lozingen**: alle lozingen van bedrijven via een
  meetput van type riool. `251013` geeft vrachten per categorie lozer (bedrijven/RWZI) × type
  meetput, niet per lozing. De vijf groepen in de data:

  | IRI | Groep |
  |---|---|
  | `ex:lozingsgroep-bedrijven-coll` | bedrijven, collector |
  | `ex:lozingsgroep-bedrijven-oppw` | bedrijven, oppervlaktewater |
  | `ex:lozingsgroep-bedrijven-rio` | bedrijven, riool |
  | `ex:lozingsgroep-rwzi-irwzi` | RWZI, influent |
  | `ex:lozingsgroep-rwzi-oppw` | RWZI, oppervlaktewater |

  De individuele lozingen in een groep kent de bron niet. De groep is daarom een eigen FOI en
  geen verzameling van gekende lozingen. De indeling (categorie, meetputtype) staat enkel in label
  en `dct:identifier`. De bijbehorende codelijsten zijn voor fase 3 (`../../stappenplan.md`
  §2.2).
- **`ex:lozing-2030042`** (PFAS): `wk:Emissie` (A14) + `sosa:FeatureOfInterest + prov:Entity`,
  `dct:type matrix:afvalwater`. Dezelfde IRI als in stap 1 en 3, bewust **zonder label** (§6.5).

## 4. Observatie/Actuatie-structuur (roze nodes)

**Contrastmiddelen, bedrijven via riool, 2014** (FOI = `ex:lozingsgroep-bedrijven-rio`):

| IRI | observedProperty | hasResult | Afleiding |
|---|---|---|---|
| `ex:observatie-debiet-bedrijven-rio-2014` | `PAS_1839` Q (standaard in water): debiet (vracht) | 856 553 m³ | bron |
| `ex:observatie-concentratie-bedrijven-rio-2014-P_117` | `PAS_182` Amidotriz: massaconcentratie | 322.35 µg/L | bron |
| `ex:observatie-concentratie-bedrijven-rio-2014-P_125` | Iopamidol: massaconcentratie | 0.0514 µg/L | bron |
| `ex:observatie-concentratie-bedrijven-rio-2014-P_126` | Iopromide: massaconcentratie | 686.68 µg/L | bron |
| `ex:observatie-brutovracht-bedrijven-rio-2014-P_117` | `PAS_183` Amidotriz: vracht | 276 107 193 mg | `hasInputValue` resultaat concentratie P_117 + resultaat debiet; `relatedObservation` de twee bronobservaties; `usedProcedure` bruto vracht |
| `ex:observatie-brutovracht-…-P_125`, `…-P_126` | Iopamidol / Iopromide: vracht | 44 065 / 588 180 005 mg | idem |
| `ex:observatie-nettovracht-…-P_117`, `-P_125`, `-P_126` | idem vracht | = bruto | `relatedObservation` → bruto; `usedProcedure` netto vracht |

**`ex:collectie-vrachtbronnen-bedrijven-rio-2014`** (`sosa:ObservationCollection`) bevat enkel
de **bronobservaties**: het debiet en de drie concentraties. Wat ze delen, staat op de
collectie: de groep als FOI en het jaar. De vrachten zijn **geen** lid (R13). Ze hebben zelf FOI,
eigenschap, fenomeentijd, procedure en resultaat.

**PFAS, meetput `2030042`** (FOI = `ex:lozing-2030042`): drie bruto jaarvrachten (PFOS 2009,
PFOA 2017, PFHpA 2022), elk met `usedProcedure ex:procedure-bruto-vracht`, zonder
`hasInputValue`.

## 5. Procedure en ObservableProperty

**`ex:procedure-bruto-vracht`** (`sosa:ObservingProcedure`): "concentratie × debiet over de
periode".

- `sosa:hasInput` → `csor-kwa:KWA_1` *massaconcentratie* en `csor-kwa:KWA_10` *debiet (vracht)*;
- `sosa:hasOutput` → `csor-kwa:KWA_5` *vracht*.

Dat zijn de **abstracte** types: CSOR kwantificeerbare aspecten, onafhankelijk van de stof. De
**concrete** waarden staan op de uitvoering: `sosa:hasInputValue` naar het concentratie- en het
debietresultaat (`wk:Meetresultaat`, R5). De observaties die die resultaten opleverden, staan als
`sosa:relatedObservation`. Een observatie is zelf geen waarde maar een activiteit
(`sosa:Execution ⊂ prov:Activity`). De waarden zijn consistent met de inputs, want het
parameteraspect van elke bronobservatie heeft precies dat kwantificeerbaar aspect
(`csor:heeftAspect`). Dat is wat SOSA
2023 vraagt ("hasInputValue MUST be consistent with a hasInput definition from the corresponding
Procedure"). Het script heeft voor alle 114 rijen nagekeken dat bruto vracht = concentratie ×
debiet (µg/L × m³ = mg).

**`ex:procedure-netto-vracht`**: enkel `hasOutput` vracht. De berekeningswijze staat niet in de
bron.

**Properties.** De stofspecifieke parameteraspecten "…: massaconcentratie" en "…: vracht"
(via `Parameter Code` of symbool + drager `water` + eenheid), en `PAS_1839` "Q (standaard in
water): debiet (vracht)" voor het volume in m³. Dat is een ander aspect dan het debiet per
tijdseenheid (`PAS_1838`, m³/jr) van stap 3.

## 6. Modelleer-keuzes toegelicht

### 6.1 Waarom `hasInputValue` naar de resultaten, en geen link tussen concentratie en debiet?

> **Verworpen alternatieven:** (a) `sosa:relatedObservation` tussen de concentratie- en de
> debietobservatie omdat ze dezelfde groep en hetzelfde jaar betreffen; (b) `sosa:hasInputValue`
> naar de bronobservaties.
> **Gekozen aanpak:** enkel de afgeleide observatie verwijst naar haar bronnen:
> `sosa:hasInputValue` naar de bronresultaten (de waarden), `sosa:relatedObservation` naar de
> bronobservaties (R7, R13). Bronobservaties onderling krijgen geen koppeling.
> **Motivatie bij (b):** SOSA 2023 definieert `hasInputValue` als "assigns a value to an input
> defined by the Procedure". Een observatie is een activiteit (`sosa:Execution ⊂ prov:Activity`),
> geen waarde. Voor de band met een observatie heeft SOSA 2023 `sosa:relatedObservation`
> ("relation from an Execution … to an Observation").
> **Motivatie:** de ontwerpregel uit het stappenplan (stap 4). Het verband tussen bronnen is af
> te leiden via FOI + tijd. Een link ertussen voegt niets toe en kan uit de pas raken met wat
> eruit af te leiden is. De betekenisvolle relatie is de afhankelijkheid, en die ligt vast in
> de vracht.

### 6.2 Waarom een procedure met `hasInput` naar CSOR kwantificeerbare aspecten?

> **Verworpen alternatief:** `hasInputValue` zonder procedure, of een procedure per stof met
> stofspecifieke inputs.
> **Gekozen aanpak:** één berekeningsprocedure; `hasInput`/`hasOutput` naar KWA_1, KWA_10 en
> KWA_5.
> **Motivatie:** SOSA 2023 verbindt `hasInputValue` met een `hasInput` van de gebruikte
> procedure. R5: `hasInput` beschrijft abstracte types op de procedure, de concrete waarden
> staan op de uitvoering. De kwantificeerbare aspecten zijn precies die abstracte types, en
> gelden voor elke stof. Zo volstaat één procedure voor alle vrachten, ook voor PFAS.

### 6.3 Waarom één debietobservatie per groep en jaar?

> **Gekozen aanpak:** `ex:observatie-debiet-<groep>-<jaar>`, gedeeld door de drie vrachten van
> die groep en dat jaar.
> **Motivatie:** het debiet is een eigenschap van de groep in dat jaar, niet van een stof. In de
> bron is het voor de drie parameters identiek (nagekeken; het script stopt als dat niet zo is).
> Eén observatie met drie vrachten die ernaar verwijzen, geeft het werkelijke
> afhankelijkheidsnetwerk weer.

### 6.4 Waarom een groep van lozingen als FOI?

> **Verworpen alternatief:** de vracht toekennen aan een fictieve "totale lozing", of aan elk van
> de (onbekende) individuele lozingen.
> **Gekozen aanpak:** een eigen FOI per groep (categorie lozer × type meetput), tijdsloos, met
> `dct:type matrix:afvalwater`.
> **Motivatie:** de bron aggregeert per groep. Het studieobject is dus de groep. Ze is tijdsloos
> zoals de lozing (`../afvalwater_concentraties/bespreking.md` §6.8), en het jaar staat in
> `phenomenonTime`. Wanneer de VMM de samenstelling van een groep kan leveren, kunnen de leden
> gekoppeld worden, en kunnen groepsvrachten vergeleken worden met de som van de
> lozingsvrachten.

### 6.5 Waarom staat de exploitant bij PFAS op de observatie en niet op de lozing?

> **Verworpen alternatief:** `prov:wasAttributedTo` en een label met de exploitantnaam op de
> lozing, zoals in stap 1 en 3.
> **Gekozen aanpak:** de lozing heeft hier geen label en geen exploitant. De naam van het
> betreffende jaar staat in het label van de observatie.
> **Motivatie:** `240426` heeft geen exploitatie-ID, en de naam verandert in de tijd. Voor meetput
> `2030042` is dat Antwerp Waste Management in 2009 en Veolia ES MRC in 2017 en 2022; drie
> meetputten hebben meerdere namen. Voor 11 meetputten verschilt de naam van die in `250129`.
> Een label op de tijdsloze lozing zou botsen met stap 1 en 3 (samengevoegd: twee labels). Dit
> is precies het geval uit de discussie over de tijdsloze lozing: de *kenmerken* (hier de
> exploitant) veranderen in de tijd. De structurele oplossing is een geversioneerde toekenning
> (fase 3, zoals RIE-IEPR met geversioneerde exploitatielocaties).

### 6.6 Waarom de netto vracht als eigen observatie, met `relatedObservation`?

> **Verworpen alternatief:** netto vracht weglaten omdat ze in deze export gelijk is aan de bruto
> vracht, of `hasInputValue` naar de bruto vracht.
> **Gekozen aanpak:** eigen observatie met `usedProcedure ex:procedure-netto-vracht` en
> `sosa:relatedObservation` naar de bruto vracht.
> **Motivatie:** de bron levert beide grootheden. Dat ze gelijk zijn, is een eigenschap van deze
> export ("geenInEx": vermoedelijk zonder verrekening van innamewater), niet van het begrip.
> Omdat de berekening onbekend is, geen `hasInputValue` (dat zou een afleiding beweren), maar
> enkel een associatie (V10).

### 6.7 Waarom geen `hasInputValue` bij PFAS, ook niet naar de jaardebieten van stap 3?

> **Gekozen aanpak:** `usedProcedure ex:procedure-bruto-vracht` zonder `hasInputValue`.
> **Motivatie:** de concentraties en debieten waaruit de PFAS-vrachten berekend werden, zijn niet
> aangeleverd. De procedure zegt welke inputs nodig zijn; welke waarden gebruikt werden, is
> onbekend. Voor 2023 bestaan er wel jaardebieten (stap 3), maar niets bevestigt dat de VMM
> precies die waarde gebruikte. Een `hasInputValue` ernaar zou een afleiding beweren die niet
> vaststaat (V10).

### 6.8 "OG" in de bronkolommen

`Conc OG`, `Bruto Vracht OG`, `Meetput JV M Bruto Vracht OG DTS`: "OG" is vermoedelijk de
ondergrensbenadering. Niet-aantoonbare concentraties tellen dan als 0; 72 van de 114
concentraties in `251013` zijn 0. De concentratie is dan zelf een geaggregeerde waarde (een
periodegemiddelde volgens de OG-methode), geen enkelvoudige meting. Omdat de bron de methode
niet expliciet noemt, heeft de concentratieobservatie geen `usedProcedure`. Te bevestigen (V10).

### 6.9 Expliciete supertypes, CSOR-eenheid, plat model

Zoals in stap 1 (`../afvalwater_concentraties/bespreking.md` §6.5, §6.7, §6.9). De subgraaf
DERIVATION in het diagram groepeert de afgeleide observaties; het model zelf blijft plat
(geen p-plan-lagen).

## 7. Tijdsmodellering

| Element | Patroon |
|---|---|
| collectie bronobservaties, vrachten | `sosa:phenomenonTime → time:Interval (ex:periode-<jaar>) → time:hasBeginning/hasEnd → time:Instant → time:inXSDDateTime` |

- Dezelfde `ex:periode-<jaar>`-IRI's en triples als stap 3. Samengevoegd delen alle
  jaarobservaties hetzelfde interval. Half-open interval (R12).
- De vrachten hebben de fenomeentijd zelf, omdat ze geen lid zijn van de collectie. De
  bronobservaties hebben ze via de collectie.
- Bij `251013` gaat het om een periodevracht. Dat het kalenderjaren zijn, volgt uit de kolom
  `Jaar`.

## 8. Prefixen en IRI-structuur

| Prefix | Base URI | Tijdelijk of persistent |
|---|---|---|
| `ex:` | `https://example.org/waterkwaliteit/afvalwater/` | tijdelijk (R10); gedeeld met stap 1 en 3 |
| `wk:` | `https://data.vlaanderen.be/ns/waterkwaliteit#` | ontwerpversie (`src/main/resources/be/vlaanderen/data/ns/waterkwaliteit/waterkwaliteit.ttl`), niet gepubliceerd |
| `csor-parameteraspect:`, `csor-eenheid:` | `https://data.omgeving.vlaanderen.be/id/concept/csor/…` | persistent (CSOR) |
| `csor-kwa:` | `https://data.omgeving.vlaanderen.be/id/concept/csor/kwantificeerbaaraspect/` | persistent (CSOR) |
| `matrix:` | `https://data.omgeving.vlaanderen.be/id/concept/matrix/` | persistent |
| `sosa:`, `qudt:`, `time:`, `prov:`, `dct:`, `skos:`, `rdfs:`, `xsd:` | W3C/QUDT/DCMI | persistent |

| Resource | Patroon |
|---|---|
| groep van lozingen | `ex:lozingsgroep-<categorie>-<meetputtype>` |
| bronobservaties | `ex:observatie-debiet-<groep>-<jaar>`, `ex:observatie-concentratie-<groep>-<jaar>-<P_code>` |
| vrachten (groep) | `ex:observatie-brutovracht-<groep>-<jaar>-<P_code>`, `ex:observatie-nettovracht-…` |
| vrachten (PFAS) | `ex:observatie-brutovracht-<meetput>-<jaar>-<PAS_code>` |
| collectie, periode | `ex:collectie-vrachtbronnen-<groep>-<jaar>`, `ex:periode-<jaar>` |
| procedures | `ex:procedure-bruto-vracht`, `ex:procedure-netto-vracht` |

## 9. Inverse relaties

| Paar | Waarom |
|---|---|
| `sosa:hasFeatureOfInterest` ↔ `sosa:isFeatureOfInterestOf` | alle observaties van een groep of lozing, over stap 1, 3 en 4 heen; `isFeatureOfInterestOf` is verplicht (SHACL) |
| `sosa:hasResult` ↔ `sosa:isResultOf` | `isResultOf` is verplicht op `sosa:Result` (SHACL) |

`sosa:hasInputValue` en `sosa:relatedObservation` hebben bewust geen inverse in de data: de
richting (van afgeleide naar bronresultaat en bronobservatie, van netto naar bruto) is de
betekenis. De inverse van
`relatedObservation` (`sosa:observationRelatedTo`) is met OWL-inferentie af te leiden.
