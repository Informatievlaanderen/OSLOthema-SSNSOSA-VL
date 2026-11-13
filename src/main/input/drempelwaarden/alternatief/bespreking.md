# Bespreking — drempelwaarden, alternatief: een drempel als Web Annotation

## 1. Wat stelt dit voorbeeld voor?

Dezelfde rapporteringsdrempels van het CSO-register als het hoofdmodel (`../bespreking.md`), anders
gelezen: een drempel is een **uitspraak vanuit een rapporteringscontext over een parameteraspect van
CSOR**. E-PRTR zegt over "zink totaal in water, vracht" (PAS_862): wie in de rol *lozend* meer dan
100 kg loost, rapporteert. Het W3C [Web Annotation Data Model](https://www.w3.org/TR/annotation-model/)
heeft voor zo'n uitspraak een klasse: `oa:Annotation`, met een doel (waarover), een body (wat gezegd
wordt), een motivatie (waarom) en een auteur (wie).

Selectie: de drie drempels voor zink in water (E-PRTR lozend en transfer, 100 kg; IMJV Water
transfer en lozend, 50 kg) en de twee toetsen van de jaarvracht 2021 van AGC Glass Europe Mol uit
`../toetsing.ttl`. Daarnaast een **bereik**: een lozingsvoorwaarde van VLAREM II zegt over de pH
(PAS_2117) dat ze tussen 6,5 en 9 moet liggen, grenzen inbegrepen; een fictieve pH-meting van LP01
(7,8) wordt eraan getoetst. Status: **open** (2026-11-13), voor de werkgroep; het hoofdmodel is niet
fout.

## 2. Kleurlegenda

| Kleur | Concept | Betekenis in het domein |
|---|---|---|
| Blauw (#60c4e4) | `sosa:Sensor`, `sosa:FeatureOfInterest`, `prov:Organization` | de rapporteringstoepassing; de lozing van de exploitatie; de beheerder van het register |
| Roze (#e54b89) | `sosa:Observation` | de jaarvracht (uit `../toetsing.ttl`) en de twee toetsen |
| Oranje (#f8b622) | `oa:Annotation`, `oa:SpecificResource`, `qudt:QuantityValue`, `dct:PeriodOfTime`, `time:Interval` | de annotaties, hun doel, body en geldigheid; de jaarvracht; het rapporteringsjaar |
| Lila (#c6a0f5) | `sosa:Procedure`, `skos:Concept`, `oa:Motivation` | de toetsprocedure; groepen en drempelwaardetypes; de motivatie |
| Oranjerood (#fe7130) | `sosa:Property` | PAS_862 en "boven de rapporteringsdrempel" |
| Zandkleur (#f8e1ad) | DERIVATION | de toetsen (R13) |

De annotaties staan in een eigen subgraph *ANNOTATIES* binnen PROCEDURE, naast de gedeelde
codelijsten: ze leveren, zoals de drempelwaarden in het hoofdmodel, de waarde van een input van de
toetsprocedure.

## 3. Infrastructuur (blauwe nodes)

- **`ex:rapporteringstoepassing`**, **`ex:lozing-agc-mol-2021`** — gedeeld met het hoofdmodel; in
  dit bestand alleen getypeerd, zodat de validatie de toetsen kan controleren. Zie `../bespreking.md`
  §3.
- **`alt:csor-beheer`** — `prov:Organization` (en `prov:Agent`): de auteur van de annotaties
  (`dct:creator`). Illustratief: wie de drempels vastlegt, de beheerder van CSOR of die van elke
  rapporteringscontext, is een discussievraag (§6).
- **`alt:labo`** — `sosa:Sensor`: het laboratorium dat de pH meet (illustratief), implementeert
  `procedure:CMA_2_I_A.1` (zuurtegraad, compendium voor de monsterneming en analyse).
- **`alt:toezichtstoepassing`** — `sosa:Sensor`: de software die een meetwaarde aan een toegelaten
  bereik toetst (illustratief); implementeert `alt:procedure-bereiktoets`.
- **De lozing van LP01** (`https://data.imjv.omgeving.vlaanderen.be/id/lozing/01787986000160/2400006/2021`,
  uit `riepr/`) — `prov:Entity` en `sosa:FeatureOfInterest` van de pH-meting en de bereiktoets. Een
  lozingsvoorwaarde geldt per lozingspunt, niet per exploitatie (anders dan een rapporteringsdrempel).

## 4. Observatie/Actuatie-structuur (roze nodes)

| IRI | observedProperty | usedProcedure | resultaat | hasFeatureOfInterest |
|---|---|---|---|---|
| `alt:toets-eprtr-zn-agc-mol-2021` | `ex:prop-boven-rapporteringsdrempel` | `ex:procedure-drempeltoets` | `sosa:hasSimpleResult false` | `ex:lozing-agc-mol-2021` |
| `alt:toets-imjvwater-zn-agc-mol-2021` | `ex:prop-boven-rapporteringsdrempel` | `ex:procedure-drempeltoets` | `sosa:hasSimpleResult false` | `ex:lozing-agc-mol-2021` |
| `alt:ph-lp01-2021-06-15` (fictief) | `csor-parameteraspect:PAS_2117` (pH) | `procedure:CMA_2_I_A.1` | `alt:ph-lp01-2021-06-15-resultaat` (7,8, `csor-eenheid:E_74`) | lozing LP01 2021 |
| `alt:toets-ph-lp01-2021-06-15` | `alt:prop-binnen-toegelaten-bereik` | `alt:procedure-bereiktoets` | `sosa:hasSimpleResult true` | lozing LP01 2021 |

Gelijk aan het hoofdmodel, op één punt na: de tweede `sosa:hasInputValue` is de **body** van de
annotatie (`…-waarde`, een `qudt:QuantityValue`), niet een `csor:Drempelwaarde`. De annotatie zelf
is geen inputwaarde: ze is de uitspraak waarin de waarde gegeven wordt, geen waarde.

De bereiktoets volgt hetzelfde patroon (R13): `sosa:hasInputValue` naar het resultaat van de
pH-meting en naar de body van de annotatie (het bereik), `sosa:relatedObservation` naar de meting.

De annotaties zijn geen observaties: niemand heeft iets waargenomen. Ze staan in §6.

## 5. Procedure en Property

Gedeeld met het hoofdmodel (`../bespreking.md` §5). Eén nuance: de definitie van
`ex:prop-rapporteringsdrempel` zegt daar "de waarde is een `csor:Drempelwaarde`"; in dit alternatief
is de waarde de body van een annotatie met de motivatie `alt:rapporteringsdrempel`. Als dit
alternatief gekozen wordt, verandert die zin, niet de procedure.

**`alt:rapporteringsdrempel`** (`oa:Motivation`, een `skos:Concept`) — de reden van de annotatie:
"de body is de hoeveelheid van het doel boven welke gerapporteerd wordt". Web Annotation laat eigen
motivaties toe als verfijning van een bestaande, met `skos:broader` (Data Model §3.3.5); hier
`oa:describing`.

**`alt:toegelaten-bereik`** (`oa:Motivation`) — "de body is het bereik waarbinnen de waarde van het
doel moet liggen". Ook een verfijning van `oa:describing`.

**`procedure:CMA_2_I_A.1`** (`sosa:ObservingProcedure`) — de meetmethode voor zuurtegraad van het
compendium (CMA), uit de lijst observatiemethoden van `waterkwaliteit/`; output PAS_2117.

**`alt:procedure-bereiktoets`** (`sosa:ObservingProcedure`) — kies het bereik voor het gemeten
parameteraspect, en geef *waar* als de waarde binnen het bereik ligt; een ontbrekende grens beperkt
niet, en inclusief of exclusief volgt uit de property (`qudt:minInclusive`, `qudt:minExclusive`, …).
Inputs: PAS_2117 en `alt:prop-toegelaten-bereik`; output `alt:prop-binnen-toegelaten-bereik`.

| Property | Betekenis |
|---|---|
| `csor-parameteraspect:PAS_2117` | pH (standaard in water), zonder eenheid |
| `alt:prop-toegelaten-bereik` | het bereik zelf, als input van de toets; de waarde is de body van een annotatie |
| `alt:prop-binnen-toegelaten-bereik` | of de gemeten waarde binnen het bereik ligt. *Waar* betekent "voldoet"; bij de rapporteringsdrempel betekent *waar* "moet rapporteren" |

## 6. Modelleer-keuzes toegelicht

### Waarom een drempel als `oa:Annotation`?

Verworpen in dit alternatief: een eigen klasse `csor:Drempelwaarde` met drie eigen eigenschappen
(het hoofdmodel). Gekozen: een `oa:Annotation`, met het parameteraspect als doel, de hoeveelheid als
body en een motivatie. Motivering: de drempel is niet iets *van* het parameteraspect (CSOR beschrijft
zink, niet wanneer je zink moet rapporteren) maar iets dat een context *erover zegt*. Het Web
Annotation-model is een W3C-aanbeveling (R17, niveau 2), al geladen voor `rdf-memory/`, en heeft
voor precies die structuur een klasse: een uitspraak van iemand, over iets, met een reden.

### Waarom het doel een `oa:SpecificResource` met `oa:hasScope`?

Een drempel geldt niet voor PAS_862 zonder meer, maar voor PAS_862 binnen een rapporteringsgroep en
voor een drempelwaardetype. `oa:hasScope` is "the scope or context in which the resource is used
within the Annotation", met als domein `oa:SpecificResource`. Het doel is daarom een
`oa:SpecificResource` met PAS_862 als `oa:hasSource` en de groep en het type als `oa:hasScope`.
De context zelf (E-PRTR) volgt uit de groep (`csor:behoortTotRapporteringsContext`).

Kanttekening: de twee scopes hebben een andere rol, en alleen hun klasse
(`csor:RapporteringsGroep`, `csor:DrempelwaardeType`) houdt ze uit elkaar. Zie discussievraag 4.

### Waarom de scopes in de data getypeerd?

Om dezelfde reden: de rol van een scope volgt uit haar klasse. Als de groepen en types alleen als
object voorkomen, staat die klasse enkel in het register, en dan ziet een gebruiker van het bestand
alleen niet welke scope de groep is. De vijf scopes zijn daarom getypeerd
(`csor:RapporteringsGroep` of `csor:DrempelwaardeType`, en `skos:Concept`), met een label. Bij de
groepen staat ook `csor:behoortTotRapporteringsContext`: de shape van `csor:RapporteringsGroep`
vraagt die (2 violations zonder), en het is precies de context waarvanuit de annotatie spreekt.
Notatie, volgorde en de volledige labels blijven in het register, zoals bij PAS_862 en E_38
(*Code lists and registers*: de data kopieert het register niet).

### Waarom de hoeveelheid als body, en niet als `oa:TextualBody`?

Een body mag elke resource zijn. Een `qudt:QuantityValue` met `qudt:numericValue` en een eenheid
blijft vergelijkbaar met de jaarvracht (R3), zoals in het hoofdmodel. Een `oa:TextualBody` met
`rdf:value "100 kg"` zou de toets dwingen tekst te ontleden.

### Waarom de geldigheid op de annotatie?

Web Annotation heeft geen geldigheidsperiode: `oa:TimeState` gaat over de versie van het doel die
bedoeld is, niet over hoe lang de uitspraak geldt. De geldigheid volgt daarom het hoofdmodel
(`dct:temporal` naar een `dct:PeriodOfTime` met `dcat:startDate`, zie `../bespreking.md` §6) en
staat op de annotatie: de uitspraak geldt vanaf 2007, niet de hoeveelheid 100 kg.

### Een bereik: `qudt:minInclusive` en verwanten op de body

Een lozingsvoorwaarde geeft geen drempel maar een bereik: de pH moet tussen 6,5 en 9 liggen. Met
annotaties verandert alleen de body: `qudt:minInclusive 6.5 ; qudt:maxInclusive 9.0` in plaats van
`qudt:numericValue`, en een andere motivatie. Er zijn geen nieuwe klassen of eigenschappen nodig. In
het hoofdmodel eist `csor:Drempelwaarde` een `qudt:numericValue` (`owl:someValuesFrom`), dus daar is
een eigen klasse voor een bereik nodig.

Zijn de facetten van QUDT hier correct? Nagekeken in de geladen QUDT 3.5.2:

| Property | subPropertyOf | Bereik | Opmerking |
|---|---|---|---|
| `qudt:minInclusive`, `qudt:minExclusive` | `qudt:lowerBound` | geen | — |
| `qudt:maxInclusive` | `qudt:upperBound` | geen | — |
| `qudt:maxExclusive` | `qudt:upperBound` | `xsd:string` | ook `owl:FunctionalProperty` |
| `qudt:lowerBound`, `qudt:upperBound` | — | geen, resp. `xsd:anySimpleType` | geen definitie |

- **Bedoeld voor datatypes.** De definitie is telkens "the … bound of the value space for a
  *datatype*"; de termen staan in de datatype-module van QUDT, en de SHACL van QUDT gebruikt ze enkel
  op `qudt:ScalarDatatype` (bv. `minInclusive -128 ; maxInclusive 127` voor een 8-bit integer). De
  shapes van `qudt:QuantityValue` kennen ze niet. Het gebruik op een hoeveelheid rekt de definitie
  op.
- **Formeel niet fout.** Geen `rdfs:domain`, dus geen tegenstrijdige afleidingen op een
  `qudt:QuantityValue`; `validate_file` meldt niets.
- **`qudt:maxExclusive` heeft een fout in QUDT:** het bereik `xsd:string` botst met een getal; een
  OWL-reasoner vindt dan een datatypeconflict. De eigen shape van QUDT laat wel getallen toe
  (`sh:or qudt:NumericTypeUnion`). Dit voorbeeld gebruikt het niet (de pH-grenzen zijn inclusief).
  <!-- TODO: het bereik xsd:string van qudt:maxExclusive melden bij QUDT (github.com/qudt/qudt-public-repo). -->
- **Een precedent:** het patroon *Rapportagegrens* van de kit (`waterkwaliteit/`) gebruikt
  `qudt:lowerBound`/`qudt:upperBound` al op een `qudt:QuantityValue` zonder `qudt:numericValue`; de
  facetten zijn er subproperties van en zeggen bovendien of de grens meetelt. Zo ook
  `vlarem_rubrieken/alternatief/` (`qudt:minExclusive`, `qudt:maxExclusive`).
- **Andere kandidaten:** `schema:minValue`/`schema:maxValue` (geladen, wel bedoeld voor een
  hoeveelheid, maar schema.org is een laatste keuze volgens R17, en inclusief of exclusief is niet
  vastgelegd); twee grenzen met elk een `qudt:numericValue` en een operator (hoofdmodel van
  `vlarem_rubrieken/`); een OWL-datatype met `xsd:minInclusive` (exact, maar zonder eenheid);
  `ssn-system:MeasurementRange` (wat een sensor kan meten, geen norm).

Gekozen: `qudt:minInclusive`/`qudt:maxInclusive` (en `qudt:minExclusive` waar nodig), met deze
kanttekening; `qudt:maxExclusive` alleen met de kanttekening over het bereik. Het bereik heeft geen
`qudt:numericValue`: 6,5 tot 9 is geen getal.

De **toets draait om**: bij een rapporteringsdrempel betekent *waar* een plicht, bij een toegelaten
bereik betekent *waar* dat de lozing voldoet. Dat staat in de procedure en de property, niet in de
annotatie. De **scope** is hier geen CSOR-code maar de regelgeving zelf
(`alt:vlarem-ii-lozingsvoorwaarden-oppervlaktewater`, illustratief): een derde soort scope, wat
argument tegen 5 versterkt.
<!-- TODO: welk artikel van VLAREM II legt pH 6,5–9 vast voor bedrijfsafvalwater in oppervlaktewater, en welke ELI- of Codex-IRI hoort erbij? -->

### Argumenten voor

1. **Geen nieuwe klassen of eigenschappen.** `csor:Drempelwaarde`, `csor:voorParameterAspect`,
   `csor:behoortTotRapporteringsGroep` en `csor:heeftDrempelwaardeType` vallen weg; er komt één
   concept bij (de motivatie). Het ontwerpvocabularium krimpt tot de drie codelijstklassen.
2. **Eén patroon voor elke context.** Ook andere contexten zeggen iets over parameteraspecten:
   milieukwaliteitsnormen, rapportagegrenzen van een labo (`waterkwaliteit/`), lozingsvoorwaarden in
   een vergunning, criteria van een VLAREM-rubriek (`vlarem_rubrieken/`). In dit alternatief is elk
   daarvan een annotatie met een andere motivatie en scope; in het hoofdmodel een klasse en
   eigenschappen per soort. Het pH-bereik toont het: dezelfde structuur, een andere body.
3. **CSOR blijft ongewijzigd.** Annotaties kunnen in een aparte dataset per context staan, beheerd
   door wie de context beheert, en verwijzen naar CSOR zonder het te wijzigen (*Code lists and
   registers*: uitspraken over een register horen niet in de data, maar deze zijn geen uitspraken
   van het register).
4. **Wie het zegt is expliciet.** `dct:creator` en eventueel `dct:created` en `as:generator` geven
   de herkomst van elke drempel, wat het hoofdmodel alleen voor de hele dataset kan.

### Argumenten tegen

1. **Web Annotation is gemaakt voor annotaties op webinhoud** (een tekstfragment, een beeld) door
   gebruikers. Een wettelijke drempel als "annotatie" rekt het model op; de motivaties beschrijven de
   bedoeling van een gebruiker, en `oa:describing` past maar losjes bij een norm.
2. **Geen controle met de gegenereerde SHACL.** OA heeft geen OWL-restricties: een annotatie zonder
   body, met een tekst als body of zonder scope valideert. Het hoofdmodel controleert met
   `csor:Drempelwaarde` dat er een groep, een aspect, een type, een eenheid en een geldigheid is.
3. **Meer knopen en langere queries.** Vier knopen per drempel in plaats van twee; de query in de
   README gaat via doel, bron en scope.
4. **De toets wijst naar de body.** Welke context, stof en welk type getoetst zijn, staat op de
   annotatie en is vanuit de toets alleen via `^oa:hasBody` bereikbaar. In het hoofdmodel staat het
   op de inputwaarde zelf.
5. **`oa:hasScope` met twee rollen** (groep en type), alleen te onderscheiden door de klasse van de
   waarde.

### Tussenvormen

- **Een profiel van OA:** `csor:Drempelannotatie ⊂ oa:Annotation` met restricties (`oa:motivatedBy`
  `owl:hasValue` de motivatie, `oa:hasBody` `owl:someValuesFrom qudt:QuantityValue`, een
  geldigheid). Dat herstelt de SHACL-controle (argument tegen 2), maar brengt een eigen klasse terug;
  de eigenschappen blijven die van OA.
- **Het hoofdmodel met herkomst:** `csor:Drempelwaarde` behouden en `prov:wasAttributedTo` of
  `dct:creator` toevoegen. Dat geeft argument voor 4, niet 2 en 3.
- **Ook het lidmaatschap als annotatie:** "PAS_862 wordt gerapporteerd in RG_5" is evengoed een
  uitspraak van een context (motivatie `oa:classifying`, body de groep). In het hoofdmodel en hier is
  het `csor:teRapporterenParameterAspect` in het register; dit alternatief laat dat ongemoeid.

### Discussievragen voor de werkgroep

1. Is een rapporteringsdrempel een gegeven van CSOR, of een uitspraak van de regelgeving (E-PRTR,
   IMJV) over een CSOR-parameteraspect? Wie beheert de drempels: CSOR of de beheerder van elke
   rapporteringscontext?
2. Komen er andere contexten die iets over parameteraspecten zeggen (normen, rapportagegrenzen,
   vergunningsvoorwaarden)? Zo ja, weegt één patroon voor allemaal op tegen de nadelen?
3. Welke motivatie: een verfijning van `oa:describing`, van `oa:assessing`, of zonder `skos:broader`?
   En waar staat ze: in CSOR of in een eigen lijst van motivaties?
4. Het drempelwaardetype als tweede `oa:hasScope`, of elders (bv. `dct:type` op de annotatie)?
5. Is controle met SHACL nodig (dan de tussenvorm met een profielklasse), of volstaat de structuur
   van OA?
6. Ook het lidmaatschap van een groep als annotatie?
7. Mogen de datatype-facetten van QUDT (`qudt:minInclusive` …) een bereik van een hoeveelheid
   uitdrukken, zoals in `vlarem_rubrieken/alternatief/`? Zo ja, wordt het patroon *Rapportagegrens*
   in de kit veralgemeend tot *Interval van een hoeveelheid* (ook de vraag van VLAREM)?
8. Welke scope krijgt regelgeving zonder CSOR-code: een ELI-IRI van het artikel, of een eigen lijst
   van contexten in CSOR?

### Waarom dit vocabularium? (Web Annotation)

- *Kandidaten:* een eigen klasse in `csor:` (het hoofdmodel); PROV-O alleen (`prov:Entity` met
  `prov:wasAttributedTo`, maar zonder doel en scope); Web Annotation; nanopublicaties (assertion,
  provenance en publicatie-info in named graphs; geen W3C-aanbeveling, en vraagt TriG).
- *Doorslaggevend:* W3C-aanbeveling (2017, niveau 2), persistente naamruimte
  `http://www.w3.org/ns/oa#` (2), al geladen en gebruikt in `rdf-memory/` (13), een structuur die
  overeenkomt met de lezing (7). Geen axioma's over SOSA- of PROV-termen (5); `oa:Annotation` is niet
  disjunct met iets uit de kern (6). Zwak op 5 en 7: weinig formele semantiek (geen restricties,
  `oa:hasBody` zonder bereik) en ontworpen voor webinhoud.
- *Uitlijning:* geen uitlijning van OA met PROV-O of SOSA gevonden in het register van de kit
  (`oslo-ld-kit/registers/alignments.ttl`), in `oa.ttl` zelf of in de specificatie van SSN/SOSA 2023.

### Eenheden (R3)

Zoals het hoofdmodel: `csor-eenheid:E_38` (kilogram, `skos:exactMatch unit:KiloGM` in het
register), in de data getypeerd als `csor:Eenheid , qudt:Unit`. Voor pH: `csor-eenheid:E_74`
("Geen", `skos:exactMatch unit:UNITLESS`), zoals in `waterkwaliteit/`. QUDT heeft ook `unit:PH`;
het register koppelt E_74 niet daaraan, en dat is een punt voor het register, niet voor de data.

### Validatie

`drempelwaarden_annotatie.ttl`: 0 fouten, 0 suspects; SHACL conform (26 shapes op 28 focusknopen).
De gedeelde resources van `../toetsing.ttl` zijn hier opnieuw getypeerd (zonder beschrijving),
omdat de validatie per bestand werkt: zonder die types gaven de toetsen 14 violations
(`sosa:hasFeatureOfInterest`, `sosa:madeBySensor`, … naar een resource zonder type). De SHACL
controleert de toetsen en de bodies, niet de annotaties (argument tegen 2).

## 7. Tijdsmodellering

- **Toetsen:** zoals het hoofdmodel, `sosa:phenomenonTime` het rapporteringsjaar 2021 uit `riepr/`.
- **pH-meting en bereiktoets:** `sosa:phenomenonTime` een `time:Instant`
  (`2021-06-15T10:00:00+02:00`, fictief, zomertijd, R12): een steekmonster heeft geen duur. De toets
  krijgt hetzelfde tijdstip: ze gaat over de toestand op dat moment.
- **Annotaties:** `dct:temporal` naar een `dct:PeriodOfTime` met `dcat:startDate` (`xsd:gYear`);
  geen `dcat:endDate`, de drie drempels gelden zonder einde. De pH-annotatie heeft geen geldigheid:
  de bron ervan is illustratief. Geen `dct:created`: de bron zegt niet
  wanneer een drempel vastgelegd is.

## 8. Prefixen en IRI-structuur

| Prefix | Basis-IRI | Tijdelijk of persistent |
|---|---|---|
| `alt:` | `https://example.org/drempelwaarden/alternatief/` | tijdelijk, illustratief: annotaties, doelen, bodies, geldigheid, motivaties, auteur, toetsen, labo, pH-meting, de VLAREM-scope |
| `ex:` | `https://example.org/drempelwaarden/` | tijdelijk; gedeeld met `../toetsing.ttl` |
| `oa:` | `http://www.w3.org/ns/oa#` | persistent (W3C) |
| `csor:`, `csor-eenheid:`, `csor-parameteraspect:` | zie `../bespreking.md` §8 | persistent (CSOR) |
| `rapporteringsgroep:`, `drempelwaardetype:` | `https://data.omgeving.vlaanderen.be/id/concept/csor/rapporteringsgroep/`, `…/drempelwaardetype/` | voorstel volgens het ontwerp; gedeeld |
| `procedure:` | `https://data.omgeving.vlaanderen.be/id/concept/observatieprocedure/` | voorstel, uit `waterkwaliteit/` (observatiemethoden) |
| `dcat:`, `dct:`, `prov:`, `qudt:`, `rdfs:`, `skos:`, `sosa:`, `time:`, `xsd:` | standaard | persistent |

Doel, body en geldigheid hebben een eigen IRI, afgeleid van die van de annotatie (`…-doel`,
`…-waarde`, `…-geldigheid`), geen lege knoop: de body is een inputwaarde van de toets en moet van
buiten bereikbaar zijn (R10). Bij publicatie: zie de README (*Transformatie*).

## 9. Inverse relaties

Geen. Web Annotation definieert geen inverse van `oa:hasBody` of `oa:hasTarget`; de context van een
inputwaarde vraagt daarom `^oa:hasBody` in SPARQL (argument tegen 4).
