# Bespreking — drempelwaarden

## 1. Wat stelt dit voorbeeld voor?

De rapporteringsdrempels van het CSO-register (CSOR) van het Departement Omgeving: per
rapporteringscontext (E-PRTR, IMJV Water, IMJV Lucht) en rapporteringsgroep, de jaarvracht van een
parameteraspect boven welke een exploitant moet rapporteren. Bron is een export van 688 rijen
(`source/rapporterings_drempelwaarden.csv`) en het ontwerp "Ontwerp Codelijsten", dat de publicatie
als linked data voorstelt. Het register zelf is geen waarneming; het voorbeeld toont daarom ook hoe
een jaarvracht eraan getoetst wordt: de jaarvracht zink 2021 van AGC Glass Europe, vestiging Mol,
uit [`riepr/`](../riepr/README.md), tegen de E-PRTR-drempel (100 kg) en de IMJV Water-drempel
(50 kg). Beide toetsen geven *onwaar* (1,6 kg).

Een drempelwaarde, bv.
`https://data.omgeving.vlaanderen.be/id/csor/drempelwaarde/RG_5/PAS_862/RDT_1/2007` (E-PRTR, zink
totaal in water, lozend, vanaf 2007: 100 kg), is een voorstel: de IRI's zijn niet gepubliceerd.

## 2. Kleurlegenda

| Kleur | SOSA-concept | Betekenis in het domein |
|---|---|---|
| Blauw (#60c4e4) | `sosa:Sensor`, `sosa:FeatureOfInterest` | de rapporteringstoepassing; de lozing van de exploitatie en van lozingspunt LP01 |
| Roze (#e54b89) | `sosa:Observation` | jaarvracht LP01 (riepr), jaarvracht van de exploitatie, twee toetsen |
| Oranje (#f8b622) | `qudt:QuantityValue`, `time:Interval`, `dct:PeriodOfTime` | jaarvrachten, drempelwaarden, het rapporteringsjaar, de geldigheid van een drempel |
| Lila (#c6a0f5) | `sosa:Procedure`, `skos:Concept` | de twee procedures; contexten, groepen en drempelwaardetypes van het register |
| Oranjerood (#fe7130) | `sosa:Property` | parameteraspecten, rapporteringsdrempel, "boven de rapporteringsdrempel" |
| Zandkleur (#f8e1ad) | DERIVATION | afgeleide observaties (R13) |

Het register staat in een eigen subgraph *CSO-REGISTER (ontwerp)* binnen PROCEDURE: de
drempelwaarden zijn de waarden van een input van de toetsprocedure.

## 3. Infrastructuur (blauwe nodes)

- **`ex:rapporteringstoepassing`** — `sosa:Sensor` en `sosa:System`: de software die de jaarvracht
  van een exploitatie optelt en aan een drempel toetst; `sosa:implements` beide procedures. De bron
  zegt niet wie de toets uitvoert (de exploitant in zijn aangifte, de administratie bij de
  controle); de sensor is illustratief.
  <!-- TODO: wie toetst de jaarvracht aan de drempel: het e-loket van het IMJV bij de aangifte, of de afdeling bij de verwerking? Dat wordt de sensor. -->
- **`ex:lozing-agc-mol-2021`** — `prov:Entity` en `sosa:FeatureOfInterest`: de lozing van
  afvalwater door de hele exploitatie in 2021. `dct:hasPart` naar de lozing van lozingspunt LP01
  uit `riepr/`; `prov:wasAttributedTo` de exploitant. Geen platform: er staat niets op.

Er is geen `sosa:Platform` en geen `sosa:hosts`: de toets is een berekening, geen meting op een
plaats.

## 4. Observatie/Actuatie-structuur (roze nodes)

| IRI | observedProperty | usedProcedure | resultaat | hasFeatureOfInterest |
|---|---|---|---|---|
| `ex:jaarvracht-zn-agc-mol-2021` | `csor-parameteraspect:PAS_863` (Zn t: vracht per tijd) | `ex:procedure-som-lozingspunten` | `ex:result-jaarvracht-zn-agc-mol-2021` (1,59612 `csor-eenheid:E_12`, kg/jr) | `ex:lozing-agc-mol-2021` |
| `ex:toets-eprtr-zn-agc-mol-2021` | `ex:prop-boven-rapporteringsdrempel` | `ex:procedure-drempeltoets` | `sosa:hasSimpleResult false` | `ex:lozing-agc-mol-2021` |
| `ex:toets-imjvwater-zn-agc-mol-2021` | `ex:prop-boven-rapporteringsdrempel` | `ex:procedure-drempeltoets` | `sosa:hasSimpleResult false` | `ex:lozing-agc-mol-2021` |

Alle drie zijn afgeleide observaties (R7, R13), met alle verplichte eigenschappen expliciet:

- de jaarvracht van de exploitatie: `sosa:hasInputValue` naar het resultaat van de jaarvracht van
  LP01, `sosa:relatedObservation` naar die observatie;
- elke toets: `sosa:hasInputValue` naar het resultaat van de jaarvracht van de exploitatie **en**
  naar de drempelwaarde, `sosa:relatedObservation` naar de jaarvracht.

Geen `sosa:ObservationCollection`: drie losse afgeleide observaties, elk met een andere
procedure of andere inputwaarden.

## 5. Procedure en Property

**`ex:procedure-som-lozingspunten`** (`sosa:ObservingProcedure`) — de jaarvracht van een exploitatie
is de som van de jaarvrachten van haar lozingspunten. Input en output: PAS_863. Geïmplementeerd door
de rapporteringstoepassing; gebruikt door `ex:jaarvracht-zn-agc-mol-2021`.

**`ex:procedure-drempeltoets`** (`sosa:ObservingProcedure`) — kies de drempelwaarde (context, vracht-
aspect van dezelfde stof en drager, type dat past bij de bestemming, geldig in het jaar), vergelijk,
en geef *waar* als de jaarvracht groter is dan de drempel. Inputs: PAS_863 en
`ex:prop-rapporteringsdrempel`; output: `ex:prop-boven-rapporteringsdrempel`. Gebruikt door de twee
toetsen. De drempel is een input van de procedure, niet een deel ervan: een gewijzigde drempel vraagt
geen nieuwe procedure, zoals de alarmdrempel in [`E-detect/`](../E-detect/README.md).

| Property | Betekenis |
|---|---|
| `csor-parameteraspect:PAS_863` | Zn t (totaal in water): vracht per tijd, in kg/jr; zo rapporteert het IMJV de jaarvracht |
| `csor-parameteraspect:PAS_862` | Zn t (totaal in water): vracht, in kg; het aspect waarvoor de drempels voor zink in water gelden |
| `ex:prop-rapporteringsdrempel` | de drempel zelf, als input van de toets; de waarde is een `csor:Drempelwaarde` |
| `ex:prop-boven-rapporteringsdrempel` | of de jaarvracht de drempel overschrijdt; welke drempel volgt uit de inputwaarde |

## 6. Modelleer-keuzes toegelicht

### Waarom een drempelwaarde als `qudt:QuantityValue` en niet als `skos:Concept`?

Verworpen alternatief: het ontwerp maakt van een drempelwaarde een concept in een conceptschema
(`skos:notation RD_n`, `skos:topConceptOf`), met de waarde in `rdf:value` en de eenheid in
`csor:heeftEenheid`. Gekozen: `csor:Drempelwaarde ⊂ qudt:QuantityValue`, met `qudt:numericValue` en
`qudt:hasUnit`. Motivering: een codelijst bevat soorten of codes; een drempel is een hoeveelheid met
een eenheid (R3, R18: de drempel heeft regels van zichzelf, geen soort binnen een klasse).
`rdf:value` zegt niet wat de waarde is; `qudt:numericValue` met een eenheid wel, en zo vergelijkt
een toets een jaarvracht en een drempel met dezelfde termen. Een `qudt:QuantityValue` is ook een
`prov:Entity` zodra hij als `sosa:hasInputValue` gebruikt wordt (⊂ `prov:used`): geen conflict
(R16). Zo deden ook `E-detect/` (alarmdrempel) en `brdr/` (overlapdrempel).

Een tweede verdedigbare lezing staat in [`alternatief/`](alternatief/README.md) (status *open*): de
drempel als uitspraak van een rapporteringscontext over een CSOR-parameteraspect, een
`oa:Annotation` (W3C Web Annotation) met het parameteraspect als doel, de groep en het type als
scope en de hoeveelheid als body. Zonder eigen klassen of eigenschappen, maar ook zonder controle
met de gegenereerde SHACL; de argumenten en discussievragen staan in `alternatief/bespreking.md` §6.

### Waarom de contexten, groepen en types wel als `skos:Concept`?

Het zijn codes, zonder eigen regels per waarde: de test van R18 maakt er concepten van. Elk soort
code krijgt een eigen subklasse van `skos:Concept` (`csor:RapporteringsContext`, …) zoals
`csor:ParameterAspect`, omdat de soort wel eigen regels heeft (een groep behoort tot één context).
Een groep hangt aan haar context met `csor:behoortTotRapporteringsContext`, niet met
`skos:broader`: ze staan in verschillende conceptschema's en een groep is geen nauwer begrip dan een
context.

### Waarom de codelijsten in `src/main/resources/`?

Ze zijn een klein register waartegen de data gecontroleerd moet worden (*Code lists and registers*):
zo meldt `validate_file` een drempelwaarde met een niet-bestaande groep of een niet-bestaand type.
Als data gaven de conceptschema's de fout *Resource minted in a vocabulary namespace*, omdat
`…/id/conceptscheme/csor/` de naamruimte is van het geladen eenhedenregister.

### Waarom een geldigheidsperiode met DCAT?

Verworpen alternatieven: (a) `csor:geldigVan`/`csor:geldigTot` als `xsd:gYear`, zoals het ontwerp
(dat zelf vraagt "Is gYear het correcte type?") — `csor:geldigTot` bestaat al met bereik `xsd:date`;
(b) een `time:Interval` met `time:hasBeginning`/`time:hasEnd` — de meeste drempels gelden zonder
einde, en R12 vraagt van een `time:Interval` een begin en een einde (381 SHACL-violations); een
halfopen jaar als einde ("tot en met 2005" als einde 2006) is bovendien een conventie die de lezer
moet kennen. Gekozen: `dct:temporal` (bereik `dct:PeriodOfTime`) met `dcat:startDate` en
`dcat:endDate` als `xsd:gYear`. Een open einde is gewoon een ontbrekende `dcat:endDate`, en
`dcat:endDate` is inclusief, zoals de bron.

#### Waarom dit vocabularium? (DCAT 3)

- *Kandidaten:* OWL-Time (geladen; zie hierboven), `csor:geldigTot` (geladen; verkeerd bereik),
  `dct:valid` (een literal, geen begin en einde), `schema:validFrom`/`validThrough` (schema.org,
  laatste keuze volgens R17), `dcat:startDate`/`dcat:endDate`.
- *Doorslaggevend:* W3C-aanbeveling (niveau 2 van R17), persistente naamruimte
  `http://www.w3.org/ns/dcat#` (2), versie 3 met `owl:versionIRI` (3), juist bedoeld voor een
  `dct:PeriodOfTime` met begin en einde in jaren (7), breed gebruikt in OSLO en DCAT-AP (13).
  Geen axioma's over SOSA- of PROV-termen (5); na het laden geven alle voorbeelden nog 0 fouten en
  geen `[DISJOINTNESS]` (6).
- *Gevolg:* DCAT 3 is geladen in `src/main/resources/org/w3/www/ns/dcat/dcat3.ttl`.

### Waarom de volgorde van de groepen als `skos:OrderedCollection`?

Verworpen alternatief: `schema:position` op de groep (ontwerp, met de vraag "is schema:position het
juiste concept?"). Gekozen: per context een `skos:OrderedCollection` met `skos:memberList`, in
`https://data.omgeving.vlaanderen.be/id/collection/csor/rapporteringsgroep/RC_n` (het ontwerp
voorziet `/id/collection/` voor collecties). Motivering: SKOS is geladen en heeft hiervoor een
klasse (R17, niveau 1); schema.org is een laatste keuze. Het volgnummer zelf gaat verloren, de
volgorde niet.

### Waarom de termen in de naamruimte `csor:`, als aparte module?

Het ontwerp plaatst de klassen in `csor:`. Ze staan in een eigen bestand
(`ns/csor/csor-rapportering.ttl`), zodat `csor.ttl` ongewijzigd blijft en het voorstel apart
besproken kan worden. Zoals `csor.ttl`: geen kardinaliteiten, wel `owl:someValuesFrom` en
`owl:FunctionalProperty`; de restricties staan alleen op de eigen klassen.

### Waarom een toets als afgeleide observatie?

Verworpen alternatief: de toets als `prov:Activity` die een "rapporteringsplicht" genereert, buiten
SOSA. Gekozen: een `sosa:Observation` van de eigenschap "boven de rapporteringsdrempel" van de
lozing, met `sosa:hasSimpleResult` waar of onwaar (R2, R13). Motivering: de toets schat een
eigenschap van het studieobject, uit de resultaten van andere observaties en een parameter van de
procedure; dat is een afgeleide observatie, net als het alarm in `E-detect/`. De drempelwaarde is
een `sosa:hasInputValue`: SOSA 2023 noemt een input uitdrukkelijk "a calibration or conditioning
parameter".

### Waarom één eigenschap "boven de rapporteringsdrempel" en niet één per context en stof?

Welke drempel getoetst is, staat al in de inputwaarde (context, stof, type, geldigheid). Een
eigenschap per combinatie zou het register herhalen. Nadeel: de vraag "welke exploitaties
overschrijden de E-PRTR-drempel voor zink" gaat via `sosa:hasInputValue` naar de drempelwaarde.

### Waarom de lozing van de exploitatie als studieobject, en niet die van LP01?

Een rapporteringsdrempel geldt voor de exploitatie (E-PRTR: per inrichting), niet per lozingspunt.
Daarom eerst de som over de lozingspunten, met de lozing van de exploitatie als studieobject
(patroon *emissie als feature of interest*). Het riepr-voorbeeld bevat enkel LP01, dus de som heeft
één term.
<!-- TODO: heeft AGC Glass Europe Mol in 2021 nog andere lozingspunten met zink? Zo ja, horen hun jaarvrachten als inputwaarde bij ex:jaarvracht-zn-agc-mol-2021. -->

### Waarom PAS_863 toetsen aan een drempel voor PAS_862?

De drempels voor water staan in het register voor het aspect "vracht" (PAS_862, kg), de jaarvracht
in het IMJV voor "vracht per tijd" (PAS_863, kg/jr). Over het rapporteringsjaar zijn beide dezelfde
hoeveelheid. De procedure zegt hoe ze omzet; de data verandert de drempel niet. Dit is verbeterpunt
1 in de README: E-PRTR geeft alle drempels in kg per jaar.

### Welk drempelwaardetype?

De E-PRTR-toets gebruikt *Lozend* (RDT_1), omdat het riepr-voorbeeld de jaarvracht onder `…/lozend/…`
publiceert. *Transfer* (RDT_2) geldt voor afvalwater naar een zuivering buiten de exploitatie.
<!-- TODO: loost LP01 rechtstreeks in oppervlaktewater (lozend) of in de riolering naar een RWZI (transfer)? Dat bepaalt de E-PRTR-drempel. -->
<!-- TODO: geldt de IMJV Water-drempel van type "Transfer en Lozend" (RDT_3) voor elk apart, of voor de som van lozing en transfer? -->

### Geen vergelijkingsoperator op de drempel

`vlarem_rubrieken/` geeft een grens een operator (`vlarem:operator`). Hier staat de vergelijking
("groter dan", E-PRTR art. 5) in de procedure: de bron geeft geen operator per drempel, en alle
drempels worden op dezelfde manier gebruikt.

### Eenheden (R3)

CSOR, prefix `csor-eenheid:`. De register-mapping naar QUDT (in het register, niet in de data):

| CSOR | label | QUDT |
|---|---|---|
| `csor-eenheid:E_38` | kilogram | `skos:exactMatch unit:KiloGM` |
| `csor-eenheid:E_12` | kilogram per jaar | `skos:exactMatch unit:KiloGM-PER-YR` |
| `csor-eenheid:E_15` | ton per jaar | zie het register (geen mapping in de geladen versie) |

De gebruikte eenheden zijn in de data getypeerd als `csor:Eenheid , qudt:Unit`: `qudt:hasUnit`
vraagt een `qudt:Unit`, en SHACL ziet geen afgeleide types (390 violations zonder).
<!-- TODO: heeft E_15 (ton per jaar) een mapping naar unit:TONNE-PER-YR in het register? De geladen eenheid.ttl toont er geen. -->

### Gerefereerde registerconcepten

De parameteraspecten zijn in de data enkel getypeerd (`a csor:ParameterAspect`), zodat de shape van
`csor:Drempelwaarde` ze herkent; hun labels staan in CSOR. In `toetsing.ttl` heeft PAS_863 ook een
label, voor de leesbaarheid, zoals in `riepr/`.

### Validatie

`drempelwaarden.ttl` en `toetsing.ttl`: 0 fouten, 0 suspects, 0 SHACL-warnings. Er bleven geen
meldingen bewust staan.

## 7. Tijdsmodellering

- **Toets en jaarvracht:** `sosa:phenomenonTime` is het rapporteringsjaar 2021, het `time:Interval`
  `https://data.riepr.omgeving.vlaanderen.be/id/tijd/jaar/2021` uit `riepr/` (2021-01-01T00:00+01:00
  tot 2022-01-01T00:00+01:00, halfopen, R12). Geen `sosa:resultTime`: de bron zegt niet wanneer
  getoetst is.
- **Drempelwaarde:** geen waarnemingstijd maar een geldigheid, `dct:temporal` naar een
  `dct:PeriodOfTime` met `dcat:startDate` en `dcat:endDate` (`xsd:gYear`, einde inclusief, zoals de
  bron). Geen tijdzone: de bron geeft jaren.

## 8. Prefixen en IRI-structuur

| Prefix | Basis-IRI | Tijdelijk of persistent |
|---|---|---|
| `csor:` | `https://data.omgeving.vlaanderen.be/ns/csor#` | persistent; de rapporteringstermen zijn een ontwerp |
| `csor-eenheid:` | `https://data.omgeving.vlaanderen.be/id/concept/csor/eenheid/` | persistent (CSOR) |
| `csor-parameteraspect:` | `https://data.omgeving.vlaanderen.be/id/concept/csor/parameteraspect/` | persistent (CSOR) |
| — | `https://data.omgeving.vlaanderen.be/id/concept/csor/rapporteringscontext/`, `…/rapporteringsgroep/`, `…/drempelwaardetype/` | voorstel volgens het ontwerp (codes uit de bron) |
| — | `https://data.omgeving.vlaanderen.be/id/conceptscheme/csor/…` en `…/id/collection/csor/rapporteringsgroep/` | voorstel volgens het ontwerp |
| — | `https://data.omgeving.vlaanderen.be/id/csor/drempelwaarde/{groep}/{parameteraspect}/{type}/{geldig-van}` | voorstel; afgeleid uit de bron (R10) |
| — | `https://data.imjv.omgeving.vlaanderen.be/id/…`, `https://data.riepr.omgeving.vlaanderen.be/id/…` | overgenomen uit `riepr/` |
| `ex:` | `https://example.org/drempelwaarden/` | tijdelijk, illustratief |
| `dcat:` | `http://www.w3.org/ns/dcat#` | persistent (W3C) |
| `dct:`, `prov:`, `qudt:`, `rdfs:`, `skos:`, `sosa:`, `xsd:`, `owl:` | standaard | persistent |

De drempelwaarde staat niet onder `/id/concept/`: ze is geen concept. Het ontwerp voorziet een code
`RD_n`; de export heeft die niet, dus volgt de IRI uit de sleutel van de rij. Zonder lege knopen:
ook de geldigheid heeft een IRI (`…/geldigheid`), omdat de dataset gescript is (R10).

## 9. Inverse relaties

Geen. `csor:behoortTotRapporteringsContext` staat alleen op de groep (het ontwerp leidt
`csor:heeftRapporteringsGroep` af bij publicatie); `sosa:isFeatureOfInterestOf` en
`sosa:isHostedBy` zijn weggelaten omdat het voorbeeld klein is en de queries vanuit de observatie
vertrekken.
