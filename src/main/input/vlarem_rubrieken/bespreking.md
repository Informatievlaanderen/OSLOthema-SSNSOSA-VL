# VLAREM-rubrieken — bespreking

Status: **voorstel** (2026-10-21). Naast dit model staat een alternatief,
[`alternatief/`](alternatief/bespreking.md); de keuze is aan de werkgroep.

## 1. Wat stelt dit voorbeeld voor?

Het criterium van VLAREM-rubriek 17.4 in de versie van 2017-02-23: een inrichting valt eronder bij
een opslag van gevaarlijke stoffen van meer dan 50 l of 50 kg en minder dan 5000 l of 5000 kg. Het
criterium is extra informatie bij een rubriek uit het register
<https://data.omgeving.vlaanderen.be/id/conceptscheme/vlaremrubrieken>, rubriek
<https://data.omgeving.vlaanderen.be/id/concept/vlaremrubrieken/3333>. Het voorbeeld herziet de twee
ontvangen varianten in `source/` (zie README, *Verbeterpunten*).

Het is geen SSN/SOSA-voorbeeld: er wordt niets waargenomen of aangestuurd. Wel kan een waarneming
(de opslagcapaciteit van een inrichting, een `qudt:QuantityValue` in dezelfde eenheid) later met
deze grenzen vergeleken worden.

<!-- TODO: zijn de grenzen van 17.4 in de versie 2017-02-23 echt "> 50" en "< 5000" (strikt)? De
waarden en operatoren komen uit het ontvangen voorbeeld, niet uit de VLAREM-tekst. -->

## 2. Kleurlegenda

Het palet van de gids, toegepast op een model zonder waarnemingen:

| Kleur | Concept | Betekenis in dit voorbeeld |
|---|---|---|
| Blauw (#60c4e4) | versie van een rubriek (register) | rubriek 17.4, versie 2017-02-23 |
| Paars (#7f59ae) | `vlarem:Criterium`, `vlarem:CriteriumConstraint` | het criterium en zijn grenzen (normatief niveau) |
| Oranjerood (#fe7130) | `skos:Concept` uit de lijst vergelijkingsoperatoren | `operator:GT`, `operator:LT` |
| Oranje (#f8b622) | `qudt:QuantityValue` | de grenswaarden met hun eenheid |

Subgraphs: `REGISTER` (lichtblauw), `CRITERIUM` (lichtpaars), `WAARDEN` (lichtgeel).

## 3. Infrastructuur (blauwe nodes)

Geen infrastructuur: er is geen platform, systeem of sensor. De enige blauwe node is de **versie
van de rubriek**, `…/vlaremrubrieken/3333/2017-02-23`. Ze komt uit het register, dat haar ook
beschrijft (de rubriek verwijst ernaar met `pav:hasVersion` en `pav:hasCurrentVersion`). Dit
bestand beschrijft haar niet opnieuw (geen type, label of versierelaties): uitspraken over de
concepten van een register horen in het register (*Code lists and registers* in de gids).

<!-- TODO: is een versie van een rubriek (…/3333/2017-02-23) in het register zelf een skos:Concept,
en met welke property hangt ze aan de rubriek behalve pav:hasVersion (bv. dct:isVersionOf)? Op
2026-10-21 gaf content negotiation enkel documentmetadata. -->

## 4. Observatie/Actuatie-structuur (roze nodes)

Geen observaties of actuaties. De plaats van de observatiestructuur neemt de structuur van het
criterium in:

| IRI | type | operator | waarden (`qudt:quantityValue`) |
|---|---|---|---|
| `…/3333/2017-02-23/01` | `vlarem:Criterium` | – | via `vlarem:hasMin` en `vlarem:hasMax` |
| `…/01/min` | `vlarem:CriteriumConstraint` | `operator:GT` | `…/01/min/L` (50 l), `…/01/min/KiloGM` (50 kg) |
| `…/01/max` | `vlarem:CriteriumConstraint` | `operator:LT` | `…/01/max/L` (5000 l), `…/01/max/KiloGM` (5000 kg) |

Elke waarde is een `qudt:QuantityValue` met `qudt:numericValue` en `qudt:hasUnit` (R3). De waarden
van één grens zijn **alternatieven**: dezelfde grens in een andere eenheid.

<!-- TODO: valt een inrichting onder de rubriek als ze in één van de eenheden binnen de grenzen
valt, of bepaalt de aggregatietoestand welke eenheid geldt (vloeistof in l, vaste stof in kg)? In
het tweede geval hoort bij elke alternatieve waarde een voorwaarde, die het model nu niet heeft. -->

## 5. Procedure en Property

Geen `sosa:Procedure` of `sosa:Property`. Wat in een waarneming de property zou zijn, is hier het
**onderwerp** van het criterium: de opslagcapaciteit voor gevaarlijke stoffen. Het staat enkel als
`rdfs:label` op het criterium; een code ontbreekt (§6, *Waarom geen onderwerpcode?*). De grootheid
volgt uit de eenheid: `unit:L` heeft in QUDT `qudt:hasQuantityKind quantitykind:Volume` (en
`quantitykind:LiquidVolume`), `unit:KiloGM` heeft `quantitykind:Mass`.

## 6. Modelleer-keuzes toegelicht

### Waarom geen SSN/SOSA?

Verworpen alternatief: het criterium als `sosa:Observation` of als `sosa:Procedure` met een
drempel. Gekozen aanpak: een eigen klasse `vlarem:Criterium` met grenzen in QUDT. Rationale: de
bron zegt het uitdrukkelijk (`source/duiding`), en een criterium is een norm, geen handeling van
waarnemen (`sosa:Observation ⊂ prov:Activity`, R16) en geen werkwijze. QUDT (kern, niveau 1 van
R17) volstaat voor de hoeveelheden.

### Waarom het criterium op de versie van de rubriek?

Verworpen alternatief: `vlarem:hasCriterium` op de rubriek zelf, zoals in beide ontvangen
varianten. Gekozen aanpak: op de versie `…/3333/2017-02-23`. Rationale: de grenzen veranderen
tussen VLAREM-versies, en de IRI van het criterium bevat al de versiedatum. Op de rubriek zou een
criterium van 2017 ook voor de versie van 1995 lijken te gelden.

### Waarom een grens met operator en alternatieve waarden (variant 2) en niet de tussenlaag van variant 1?

Verworpen alternatief: variant 1, waarin elke grens via `vlarem:alternatieveKwantiteit` naar een
`vlarem:CriteriumKwantiteit` wijst, die een grootheid en een waarde draagt. Gekozen aanpak: de grens
wijst met `qudt:quantityValue` rechtstreeks naar haar waarden, zoals in variant 2. Rationale: de
tussenlaag diende om de grootheid bij de waarde te zetten, maar met een QUDT-eenheid volgt de
grootheid al uit de eenheid. Variant 2 zette de grootheden los naast de waarden op de grens; dat is
weggelaten (README, verbeterpunt 3).

### Waarom QUDT-eenheden en geen register?

Verworpen alternatief: de eenheden van het omgevingsloket als eigen lijst (de eerste optie in de
TODO van de bron), of CSOR-eenheden. Gekozen aanpak: `unit:L` en `unit:KiloGM` uit QUDT (R3,
standaard). Rationale: liter en kilogram zijn gewone eenheden die QUDT dekt; een register is enkel
nodig voor eenheden die QUDT niet kan uitdrukken. Dit volgt de tweede optie in de bron:
"standaardeenheden uit een bestaande lijst en een eigen lijst van subject-, parameter- of
criteriumcodes". Een koppeling met het omgevingsloket gebeurt dan op eenheid en onderwerpcode.

### Waarom geen onderwerpcode?

De bron vraagt "idealiter een code die het subject aanduidt" (`dcterms:subject`). Zo'n lijst
bestaat nog niet. Het criterium heeft daarom enkel een `rdfs:label`; `dc:subject` met een literal is
weggelaten (README, verbeterpunt 6).

<!-- TODO: welke lijst levert de onderwerpcode van een criterium (opslagcapaciteit, vermogen,
aantal dieren …): een nieuwe lijst bij de VLAREM-rubrieken, de parametercodes van het omgevingsloket
of CSOR-parameters? -->

### Waarom een lijst vergelijkingsoperatoren?

Verworpen alternatief: `dcterms:type` met een blank node (`_:LT`), zoals in de bron, of een boolean
"inclusief". Gekozen aanpak: `vlarem:operator` naar een concept uit een nieuwe, kleine SKOS-lijst
(`operator:LT`, `LE`, `GT`, `GE`). Rationale: een code is een IRI waarnaar andere data kan verwijzen
(R10); `dcterms:type` heeft bereik `rdfs:Class` en zou van de operator een klasse maken. In de
geladen vocabularia is geen lijst van vergelijkingsoperatoren gevonden; QUDT heeft wel
`qudt:minExclusive`, `qudt:maxInclusive` … als properties, en die gebruikt het alternatief. De
lijst is een ontwerpversie in `src/main/resources/be/vlaanderen/omgeving/data/id/conceptscheme/vergelijkingsoperator/`.

De operator maakt de richting van `vlarem:hasMin` en `vlarem:hasMax` dubbel: een ondergrens heeft
GT of GE, een bovengrens LT of LE. Die samenhang staat in de definities van de properties, maar de
gegenereerde SHACL controleert hem niet.

### Waarom een eigen vocabularium `vlarem:`?

De namespace `https://data.omgeving.vlaanderen.be/ns/vlaremrubrieken#` komt uit de bron, maar gaf
op 2026-10-21 een 404. De termen die het voorbeeld gebruikt, staan als ontwerpversie in
`src/main/resources/be/vlaanderen/omgeving/data/ns/vlaremrubrieken/vlaremrubrieken.ttl`, met label,
definitie en OWL-restricties op de eigen klasse `vlarem:CriteriumConstraint` (precies één operator,
minstens één `qudt:QuantityValue`). Geen `rdfs:domain` op de properties. `vlarem:hasConstraint` is
een subproperty van `dct:hasPart`, zoals de bron in commentaar voorstelde.

Een restrictie "een criterium heeft minstens één grens" staat er bewust niet in: het alternatief
drukt de grenzen anders uit, en een restrictie op één van beide zou het andere model ongeldig
maken zolang de werkgroep niet gekozen heeft.

### Waarom de rubriek niet in de data?

De bron typeerde de rubriek en gaf haar label en versies (`pav:hasVersion`, `pav:hasCurrentVersion`).
Dat zijn uitspraken van het register over zijn eigen concepten; de data verwijst enkel naar de
versie. PAV is ook niet geladen (R17).

### Alternatief: een bereik per eenheid

Hetzelfde criterium kan per eenheid gegroepeerd worden in plaats van per grens: één
`qudt:QuantityValue` per eenheid met `qudt:minExclusive 50.0` en `qudt:maxExclusive 5000.0`, naar het
patroon *Rapportagegrens* (`oslo-ld-kit/guide/patterns.md`, waterkwaliteit). Dat is even
verdedigbaar en staat in [`alternatief/`](alternatief/README.md), met de argumenten voor en tegen.

### Validatie

`validate_file` geeft op `vlarem_rubrieken.ttl` geen errors, suspects of warnings. De SHACL raakt de
twee grenzen en de vier waarden (5 van 173 shapes op 6 focus nodes).

## 7. Tijdsmodellering

Geen tijdsentiteiten. De geldigheid in de tijd zit in de versie van de rubriek
(`…/3333/2017-02-23`), en dus in het register; het criterium erft ze door aan die versie te hangen.

## 8. Prefixen en IRI-structuur

| Prefix | Basis-IRI | Tijdelijk of persistent |
|---|---|---|
| `vlarem:` | `https://data.omgeving.vlaanderen.be/ns/vlaremrubrieken#` | persistent bedoeld; ontwerpversie, nog niet gepubliceerd |
| `operator:` | `https://data.omgeving.vlaanderen.be/id/concept/vergelijkingsoperator/` | persistent bedoeld; ontwerpversie, nog niet gepubliceerd |
| `qudt:` | `http://qudt.org/schema/qudt/` | persistent |
| `unit:` | `http://qudt.org/vocab/unit/` | persistent |
| `rdfs:` | `http://www.w3.org/2000/01/rdf-schema#` | persistent |
| – | `https://data.omgeving.vlaanderen.be/id/concept/vlaremrubrieken/` (rubrieken en versies) | persistent (register) |
| – | `https://data.omgeving.vlaanderen.be/id/criterium/vlaremrubrieken/` (criteria) | persistent bedoeld, uit de bron |

De IRI's van rubrieken, versies en criteria zijn voluit geschreven: hun lokale namen bevatten `/`,
dat in een Turtle-prefixnaam ge-escapet moet worden. Een criterium-IRI volgt de bron:
`…/criterium/vlaremrubrieken/{rubriek}/{versie}/{volgnummer}`; een grens voegt `/min` of `/max`
toe, een waarde de QUDT-naam van haar eenheid (`/L`, `/KiloGM`). Zo zijn alle IRI's
deterministisch (R10), en kan een waarde van buitenaf aangesproken worden, bv. door een
koppeling met het omgevingsloket.

## 9. Inverse relaties

Geen. `vlarem:hasCriterium`, `vlarem:hasMin`, `vlarem:hasMax` en `vlarem:operator` lopen van de
rubriekversie naar de waarden, de richting waarin de vraag "welke grenzen gelden voor deze rubriek?"
gesteld wordt. De omgekeerde vraag (welke rubrieken hebben een grens in kg?) is in SPARQL met een
omgekeerd pad op te lossen; een inverse property zou het vocabularium groter maken zonder nieuwe
informatie.
