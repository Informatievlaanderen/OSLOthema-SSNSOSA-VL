# Bespreking: jaardebieten van lozingen

## 1. Wat stelt dit voorbeeld voor?

Van elke vergunde lozing kent de VMM een jaardebiet: het volume afvalwater dat in een jaar via
een meetput geloosd werd. Het komt uit het integraal milieujaarverslag (IMJV) van de exploitant
of uit de bron "MNT". Dit voorbeeld modelleert het jaardebiet 2023 als één SSN/SOSA
2023-observatie per lozing. Bron: VMM-export `250129_AW_Lozingsdebieten_2023_geleverd.xlsx`, met
1555 meetputten. De subset toont AGC Glass Mol, de exploitatie uit het RIE-IEPR-datavoorbeeld
(`agc-glass_MJV_18-09-2026.ttl`), met de meetputten `2400006` (244 378 m³) en `2400007`
(27 784 m³).

## 2. Kleurlegenda

| Kleur | SOSA-concept | Domeinbetekenis |
|---|---|---|
| Blauw (#60c4e4) | `sosa:Sampler`/`prov:Location`, `sosa:FeatureOfInterest`, `prov:Organization` | meetput, lozing, exploitatie; RIE-IEPR-meetpunt |
| Oranje (#fe7130) | `sosa:Property` | CSOR-parameteraspect "Q (standaard in water): debiet" |
| Roze (#e54b89) | `sosa:ObservationCollection`, `sosa:Observation` | jaardebieten 2023, jaardebiet van één lozing |
| Geel-oranje (#f8b622) | `sosa:Result`, `time:Interval`, `prov:Entity` (databron) | debiet, kalenderjaar, IMJV/MNT |

## 3. Infrastructuur (blauwe nodes)

- **`ex:meetpunt-2400006`**: `sosa:Sampler + prov:Location`. Dezelfde meetput-IRI als in stap 1,
  waar ze de staalname uitvoert (`sosa:Sampler`). Hier is ze de plaats waar het debiet bepaald
  wordt (`prov:Location`, doel van `prov:atLocation`). `rdfs:seeAlso` verwijst naar het
  RIE-IEPR-meetpunt "Controleinrichting LP01 Industrieel glasfabriek", dat dezelfde VMM-code
  `2400006` als `vmm:lozingspuntCode` draagt.
- **`ex:lozing-2400006`**: `sosa:FeatureOfInterest + prov:Entity`. De lozing aan die meetput. Dit
  komt overeen met `riepr:Emissie` (`../afvalwater_concentraties/bespreking.md` §6.2), en het is
  dezelfde IRI als het ultieme FOI van de concentraties in stap 1.
- **`ex:exploitatie-696`** (AGC Glass Europe vestiging Mol) en **`ex:exploitatie-102767`** (AGC
  Fabrication - Kempenglas): `prov:Organization`, enkel als identificator.

## 4. Observatie/Actuatie-structuur (roze nodes)

| IRI | observedProperty | hasResult | hasFeatureOfInterest |
|---|---|---|---|
| `ex:observatie-jaardebiet-2400006-2023` | `csor-parameteraspect:PAS_1838` Q (standaard in water): debiet | 244 378 `csor-eenheid:E_50` m³/jr | `ex:lozing-2400006` |
| `ex:observatie-jaardebiet-2400007-2023` | `csor-parameteraspect:PAS_1838` Q (standaard in water): debiet | 27 784 `csor-eenheid:E_50` m³/jr | `ex:lozing-2400007` |

Beide observaties hebben ook `prov:atLocation` (de meetput) en `prov:used` (databron IMJV).

**`ex:collectie-jaardebieten-2023`** (`sosa:ObservationCollection`) groepeert alle jaardebieten
van 2023. Wat ze delen, staat op de collectie: de geobserveerde eigenschap en de fenomeentijd
(het kalenderjaar). Het FOI verschilt per lid en staat dus op de observaties.

## 5. Procedure en ObservableProperty

**Procedure.** Geen `sosa:usedProcedure`: de bron vermeldt niet hoe het debiet bepaald werd. Een
kandidaat is `procedure:WAC_I_1_012` "Bepaling van het debiet in controle-inrichtingen voor
afvalwater" uit de VITO-lijst. Dat moet de VMM bevestigen.

**Property.** `csor-parameteraspect:PAS_1838` "Q (standaard in water): debiet" is het
parameteraspect van CSOR-parameter P_1043 "Debiet in water" met het kwantificeerbaar aspect
*debiet* (toepasbare eenheden o.a. m³/jr, m³/d, L/u). CSOR kent ook `PAS_1839` "Q (standaard in
water): debiet (vracht)" met volume-eenheden (m³, L). Dat is het periodedebiet dat in stap 4
(`251013`, "Debiet (m³)") nodig is.

## 6. Modelleer-keuzes toegelicht

### 6.1 Waarom de lozing als FOI, zonder staal?

> **Verworpen alternatief:** een `sosa:Sample` zoals bij de concentraties.
> **Gekozen aanpak:** `sosa:hasFeatureOfInterest` rechtstreeks naar de lozing.
> **Motivatie:** een jaardebiet gaat over de lozing als geheel over een jaar, niet over een
> genomen staal. Dit is precies het RIE-IEPR-patroon (FOI = `riepr:Emissie`,
> `../../featureofinterest.md` §2.3).

### 6.2 Waarom dezelfde IRI's als stap 1?

> **Gekozen aanpak:** namespace `https://example.org/waterkwaliteit/afvalwater/` voor stap 1 en
> stap 3; meetput, lozing en exploitatie krijgen identieke IRI's en triples.
> **Motivatie:** het zijn dezelfde objecten in dezelfde VMM-registratie. Voor de 59 meetputten
> in beide bronnen zijn de exploitatie-ID's en -namen identiek, en verschillen de coördinaten
> minder dan 0,52 m. Samengevoegd zijn de twee voorbeelden conform SHACL, zonder dubbele labels.
> Zo vind je voor een lozing zowel haar stalen als haar jaardebiet. De meetputgeometrie staat
> enkel in stap 1, om twee licht verschillende geometrieën op dezelfde IRI te vermijden.

### 6.3 Waarom `prov:atLocation` naar de meetput, en niet `sosa:madeBySensor`?

> **Verworpen alternatief:** de meetput als `sosa:Sensor` en `madeBySensor` (RIE-IEPR).
> **Gekozen aanpak:** `prov:atLocation` op de observatie; de meetput ook als `prov:Location`.
> **Motivatie:** de bron zegt niet waarmee het debiet gemeten of berekend werd. Een IMJV-waarde
> is door de exploitant gerapporteerd, geen meetresultaat van de controle-inrichting. De meetput
> is wel met zekerheid de plaats waarop het debiet betrekking heeft. Een Observation is een
> `prov:Activity` (SOSA–PROV-alignering), dus `prov:atLocation` is toepasbaar.

### 6.4 Waarom `prov:used` voor de databron?

> **Verworpen alternatief:** een codelijst "databron" als `dct:type` of `dct:source`.
> **Gekozen aanpak:** `prov:used ex:databron-IMJV` / `ex:databron-MNT` (`prov:Entity`).
> **Motivatie:** R5: op uitvoeringsniveau verwijst `prov:used` naar de concrete entiteit waarop de
> observatie steunt. De databron wordt zo provenance en geen codelijstwaarde
> (`../../stappenplan.md` §2.2). De betekenis van "MNT" moet de VMM nog bevestigen (V9).

### 6.5 Waarom een `time:Interval` en een collectie per jaar?

> **Gekozen aanpak:** `sosa:phenomenonTime → ex:periode-2023` (`time:Interval`,
> 2023-01-01T00:00 → 2024-01-01T00:00, half-open), op de collectie.
> **Motivatie:** R12: een jaardebiet beslaat een periode. De periode en de eigenschap zijn voor
> alle 1555 observaties gelijk. Ze staan daarom één keer op de collectie
> (`sosa:ObservationCollection`: gedeelde metadata), terwijl het FOI per lid verschilt.

### 6.6 Waarom `rdfs:seeAlso` en niet `owl:sameAs` naar RIE-IEPR?

> **Gekozen aanpak:** `ex:meetpunt-2400006 rdfs:seeAlso riepr-meetpunt:019e9271-145f-…`.
> **Motivatie:** het RIE-IEPR-voorbeeld markeert zijn IRI's als "niet finaal" en zijn data als
> "GEEN ECHTE DATA". `owl:sameAs` zou alle beweringen van beide kanten samenvoegen, ook de
> RIE-IEPR-typering (`riepr:Meetpunt`, `ssn:System`) die in dit project niet geladen is (§6.2
> van stap 1). `rdfs:seeAlso` legt de koppeling vast zonder die gevolgen. Bij de afstemming met
> RIE-IEPR (B6) worden de ex:-meetputten vervangen door de RIE-IEPR-IRI's.

### 6.7 Expliciete supertypes, CSOR-eenheid, plat model

Zoals in stap 1 (`../afvalwater_concentraties/bespreking.md` §6.5, §6.7, §6.9).

## 7. Tijdsmodellering

| Element | Patroon |
|---|---|
| collectie jaardebieten | `sosa:phenomenonTime → time:Interval → time:hasBeginning/time:hasEnd → time:Instant → time:inXSDDateTime` |

- `ex:periode-2023`: begin `2023-01-01T00:00:00` (inclusief), einde `2024-01-01T00:00:00`
  (exclusief, R12).
- Er is geen tijdzone: de bron vermeldt enkel het jaar.
- `sosa:resultTime` (wanneer het IMJV ingediend of het debiet berekend werd) staat niet in de
  bron.

## 8. Prefixen en IRI-structuur

| Prefix | Base URI | Tijdelijk of persistent |
|---|---|---|
| `ex:` | `https://example.org/waterkwaliteit/afvalwater/` | tijdelijk (illustratief, R10); gedeeld met stap 1 |
| `riepr-meetpunt:` | `https://data.mjv.omgeving.vlaanderen.be/id/meetpunt/` | RIE-IEPR, "niet finaal" |
| `csor-parameteraspect:`, `csor-eenheid:` | `https://data.omgeving.vlaanderen.be/id/concept/csor/…` | persistent (CSOR) |
| `sosa:`, `qudt:`, `time:`, `prov:`, `adms:`, `dct:`, `skos:`, `rdfs:`, `xsd:` | W3C/QUDT/DCMI/SEMIC | persistent |

| Resource | Patroon |
|---|---|
| meetput, lozing, exploitatie | `ex:meetpunt-<nr>`, `ex:lozing-<nr>`, `ex:exploitatie-<id>` (zoals stap 1) |
| observatie, resultaat | `ex:observatie-jaardebiet-<nr>-<jaar>`, `ex:resultaat-jaardebiet-<nr>-<jaar>` |
| collectie, periode, tijdstip | `ex:collectie-jaardebieten-<jaar>`, `ex:periode-<jaar>`, `ex:tijdstip-<jaar>-01-01T000000` |
| databron | `ex:databron-IMJV`, `ex:databron-MNT` |

## 9. Inverse relaties

| Paar | Waarom |
|---|---|
| `sosa:hasFeatureOfInterest` ↔ `sosa:isFeatureOfInterestOf` (lozing) | alle observaties van een lozing, over stap 1 en 3 heen; `isFeatureOfInterestOf` is verplicht (SHACL) |
| `sosa:hasResult` ↔ `sosa:isResultOf` | `isResultOf` is verplicht op `sosa:Result` (SHACL) |

`sosa:hasMember` staat enkel op de collectie.
