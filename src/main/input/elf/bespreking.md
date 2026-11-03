# Bespreking — ELF-meetnet

## 1. Wat stelt dit voorbeeld voor?

Het meetnet voor de blootstelling van burgers aan laagfrequente magnetische velden (*extremely low
frequency*, ELF) van hoogspanningsverbindingen en -stations (380, 150 en 70 kV). Het Departement
Omgeving richt het op in uitvoering van het besluit van de Vlaamse Regering van 29 maart 2024 over de
oprichting van een monitoringsnetwerk. Artikel 10 vraagt de meetgegevens en de simulaties van het
rekenmodel (art. 6) te publiceren, zodat de blootstelling inzichtelijk wordt, onafhankelijk van de
netbeheerders. ELF-nodes meten het veld langs drie assen en sturen elke minuut hun waarden naar
ThingsBoard. Elke plaatsing (een sensor op een adres, voor een periode) wordt geregistreerd als
Jira-ticket in het project SENS. Volgens de business case zal een publieke webapp per sensor de
actuele waarde tonen, het minimum en maximum per dag, week, maand en jaar, en de jaargemiddelde
blootstelling, op een kaart met de hoogspanningstrajecten.

Het voorbeeld mapt de registratie van 15 campagnes en de telemetrie van één campagne: ELF_C_0020 op
Obscurionweg 91 in Duisterwijk (SENS-269), van 26/11/2025 tot 26/01/2026. Het gaat om een interne,
gepseudonimiseerde export (`source/`); er is nog geen publieke IRI.

## 2. Kleurlegenda

| Kleur | SOSA-begrip | Betekenis in het domein |
|---|---|---|
| Blauw (#60c4e4) | `sosa:Sensor`, `sosa:Platform` / `sosa:SpatialSample`, `sosa:FeatureOfInterest`, `prov:Location` | ELF-node, conversiescript, meetlocatie, omgeving van de bron, bron, adres |
| Paars (#c6a0f5) | `sosa:ObservingProcedure` | de meting door de node, minimum, maximum, uur- en daggemiddelde |
| Oranje (#fe7130) | `sosa:Property` | RMStotal, de zes aswaarden, de stroombelasting van de bron |
| Roze (#e54b89) | `sosa:Deployment`, `sosa:Sampling`, `sosa:ObservationCollection`, `sosa:Observation` | meetcampagne, keuze van de meetlocatie, uur- en minuutcollectie, observaties, uur- en dagindicatoren |
| Geel (#f8b622) | `qudt:QuantityValue`, `time:Interval`, `geo:Geometry` | meetwaarden in µT, het uur of de dag van een indicator, de positie van de meetlocatie |

## 3. Infrastructuur (blauwe nodes)

**`ex:sensor-ELF_C_0020`, `ex:sensor-ELF_C_0025`, …: `sosa:Sensor`.** Een ELF-node is een
apparaat dat waarneemt (R1). Het ID uit de registratie (`ELF_C_0020`) staat als `dcterms:identifier`.
De sensor `sosa:implements` de meetprocedure en `sosa:observes` de zeven eigenschappen. Er is geen
`sosa:hosts`: een sensor verhuist (zie §6).

<!-- TODO: wat onderscheidt een ELF_C-node van een ELF_L-node (bv. continu en laboratorium, of een ander type sonde)? Als het type eigen regels heeft, wordt het een subklasse; anders een begrip met dct:type (R18). -->

**`ex:verbinding-duisterwijk`: `sosa:FeatureOfInterest`.** De bron van het veld: een
hoogspanningsverbinding of een hoogspanningsstation (`ex:station-bloedhoven`). Ze heeft een eigen
eigenschap, de stroombelasting (`ex:prop-stroombelasting`). Die is langs een verbinding tussen twee
stations dezelfde, en volgens de business case wil men ze tonen als duiding bij de jaargemiddelde
blootstelling. In dit voorbeeld zijn de bronnen **fictief**: één per gemeente, met een spanningsniveau
dat uit een hash volgt.

<!-- TODO: hoe koppelt de registratie een sensor aan de verbinding of het station (veld in de enquêtetool, ID van de netbeheerder)? En welke IRI krijgt een verbinding: een ID van ELIA, of een IRI van het departement? -->

**`ex:omgeving-verbinding-duisterwijk`: `sosa:FeatureOfInterest`.** Het gebied waarin de bron het
magnetische veld en dus de blootstelling bepaalt. Het is het uiteindelijke studieobject (het geheel
waarvan de meetlocaties monsters zijn), zoals `ex:omgeving-EBBR` in `geluidsmeetnet/`. Het verwijst
met `prov:wasInfluencedBy` naar de bron, en met `sosa:hasSample` naar zijn meetlocaties.

**`ex:meetlocatie-6839-obscurionweg-91`: `sosa:Platform`, `sosa:FeatureOfInterest` en
`sosa:SpatialSample`.** Drie rollen, zoals de meetpost in `geluidsmeetnet/` en het telpunt in
`verkeersmetingen/` (R11):

- **platform**, omdat de meter er opgesteld staat (`sosa:deployedOnPlatform` in de campagne);
- **studieobject**, omdat de waarnemingen de blootstelling *op die plaats* beschrijven;
- **ruimtelijk monster** van de omgeving van de bron (`sosa:isSampleOf`): het veld varieert binnen die
  omgeving, en een meting geeft een waarde op één plek. Dat is precies de definitie van
  `sosa:SpatialSample` in SOSA 2023.

De meetlocatie is het resultaat van een `sosa:Sampling` (`ex:sampling-meetlocatie-…`): de keuze van
de plaats in de omgeving van de bron. Ze heeft twee plaatsbepalingen: het adres
(`prov:atLocation`) en een geometrie (`geo:hasGeometry`), zie §6. De IRI volgt uit postcode, straat en
huisnummer, zodat twee campagnes op hetzelfde adres dezelfde meetlocatie delen (SENS-269 en SENS-270
in Duisterwijk, SENS-96 en SENS-97 in Grimoorwoud).

<!-- TODO: staan ELF_C_0020 en ELF_C_0025 in Duisterwijk op dezelfde plek (dubbele meting, vergelijking van toestellen) of op verschillende plekken in het gebouw (binnen en buiten, verschillende verdiepingen)? In het laatste geval krijgt elke plek een eigen meetlocatie en een eigen geometrie. -->

**`ex:adres-6839-obscurionweg-91`: `prov:Location`.** Het adres zoals de registratie het geeft.

**`ex:geom-6839-obscurionweg-91`: `geo:Geometry`.** Een punt in Lambert 72 (EPSG:31370). In dit
voorbeeld **fictief** (zie §6).

**`ex:conversiescript`: `sosa:Sensor`.** Software die de uur- en dagindicatoren berekent. Een
softwareagent die waarnemingen maakt is een `sosa:Sensor` (R1), zoals de Aerovision-rekenmodule in
`geluidsmeetnet/`. In productie is dat de verwerking op het dataplatform.

**`ex:meetcampagne-SENS-269`: `sosa:Deployment`.** Eén Jira-ticket is één inzet van één sensor op
één meetlocatie, met `sosa:deployedSystem`, `sosa:deployedOnPlatform`, `sosa:hasFeatureOfInterest`
(de meetlocatie), `sosa:hasUltimateFeatureOfInterest` (de omgeving van de bron), `prov:startedAtTime`
en `prov:endedAtTime`. `sosa:Deployment` is in SSN/SOSA 2023 een `prov:Activity`, dus de PROV-tijden
passen (R16). De Jira-sleutel staat als `dcterms:identifier`.

## 4. Observatie/Actuatie-structuur (roze nodes)

Vier niveaus:

1. **Uurcollectie** `ex:collectie-ELF_C_0020-20251127T10` (`sosa:ObservationCollection`): sensor,
   procedure en studieobject, met de minuutcollecties van dat lokale uur als leden.
2. **Minuutcollectie** `ex:meting-ELF_C_0020-20251127T090049427Z`: één ThingsBoard-bericht, met het
   `sosa:resultTime` en zeven observaties als leden.
3. **Observatie** `ex:obs-…-RMStotal`: eigenschap, studieobject en resultaat.
4. **Indicatoren**: per uur het minimum, het maximum en het gemiddelde van RMStotal uit de
   minuutwaarden; per dag dezelfde drie uit de uurindicatoren (alleen in `elf.trig`).

| IRI | observedProperty | usedProcedure | hasResult | hasFeatureOfInterest |
|---|---|---|---|---|
| `ex:obs-ELF_C_0020-20251127T090049427Z-RMStotal` | `ex:prop-RMStotal` | `ex:procedure-elf-meting` (uurcollectie) | `ex:result-…-RMStotal`: 0.68249 `unit:MicroT` | `ex:meetlocatie-6839-obscurionweg-91` |
| `ex:obs-ELF_C_0020-20251127T090049427Z-Xpeak_low` (en de vijf andere aswaarden) | `ex:prop-Xpeak_low` … | idem | `ex:result-…-Xpeak_low` … | idem |
| `ex:obs-ELF_C_0020-20251127T10-minimum` | `ex:prop-RMStotal` | `ex:procedure-minimum` | 0.58806 `unit:MicroT` | idem |
| `ex:obs-ELF_C_0020-20251127T10-maximum` | `ex:prop-RMStotal` | `ex:procedure-maximum` | 0.77332 `unit:MicroT` | idem |
| `ex:obs-ELF_C_0020-20251127T10-gemiddelde` | `ex:prop-RMStotal` | `ex:procedure-uurgemiddelde` | 0.67729 `unit:MicroT` | idem |
| `ex:obs-ELF_C_0020-20251127-minimum`, `-maximum`, `-gemiddelde` (`elf.trig`) | `ex:prop-RMStotal` | `ex:procedure-minimum`, `-maximum`, `-daggemiddelde` | 0.3387, 1.00089, 0.71152 `unit:MicroT` | idem |
| `ex:sampling-meetlocatie-6839-obscurionweg-91` (`sosa:Sampling`) | — | — | `ex:meetlocatie-6839-obscurionweg-91` | `ex:omgeving-verbinding-duisterwijk` |

**Wat op de collecties staat.** SOSA 2023 laat leden de eigenschappen van een
`sosa:ExecutionCollection` erven, ook over geneste collecties. Op de uurcollectie: wat voor alle
leden gelijk is (sensor, procedure, studieobject). Op de minuutcollectie: wat zeven observaties
delen (het resultaattijdstip). Op de observatie: wat verschilt (eigenschap en resultaat).
`sosa:hasFeatureOfInterest` staat toch ook op elke observatie (zie §6).

**De indicatoren** zijn afgeleide waarnemingen (R13): ze staan niet in een collectie, hebben alle
verplichte eigenschappen expliciet en een eigen `sosa:phenomenonTime`. Een uurindicator heeft
`sosa:hasInputValue` naar de RMStotal-*resultaten* van dat uur en `sosa:relatedObservation` naar de
RMStotal-*observaties* (R7). Een dagindicator heeft de 24 uurindicatoren van dezelfde soort als
input: een afgeleide van afgeleiden, zoals Lden uit Ld, Le en Ln in `geluidsmeetnet/`.

## 5. Procedure en Property

| Procedure | Wat | Geïmplementeerd door |
|---|---|---|
| `ex:procedure-elf-meting` | driedimensionale meting door de ELF-node; `sosa:hasOutput` de zeven eigenschappen | elke ELF-sensor |
| `ex:procedure-minimum` | kleinste inputwaarde: minuutwaarden van een uur, of uurminima van een dag | `ex:conversiescript` |
| `ex:procedure-maximum` | grootste inputwaarde: minuutwaarden van een uur, of uurmaxima van een dag | `ex:conversiescript` |
| `ex:procedure-uurgemiddelde` | rekenkundig gemiddelde van de minuutwaarden met resultaattijd in het lokale uur [hh:00, hh+1:00) | `ex:conversiescript` |
| `ex:procedure-daggemiddelde` | gemiddelde van de uurgemiddelden: elk uur met metingen weegt even zwaar | `ex:conversiescript` |

Minimum en maximum zijn één procedure voor beide niveaus: het minimum van de uurminima is het
dagminimum. Het gemiddelde zijn twee procedures, omdat het daggemiddelde de uren gelijk weegt en niet
de minuten (zie §6). Alle vier hebben `sosa:hasInput` en `sosa:hasOutput` `ex:prop-RMStotal`.

| Property | Betekenis |
|---|---|
| `ex:prop-RMStotal` | effectieve waarde (RMS) van de grootte van de magnetische fluxdichtheid over de drie assen |
| `ex:prop-Xpeak_low`, `ex:prop-Ypeak_low`, `ex:prop-Zpeak_low` | component per as, kanaal *low* (altijd positief in de data) |
| `ex:prop-Xpeak_high`, `ex:prop-Ypeak_high`, `ex:prop-Zpeak_high` | component per as, kanaal *high* (ook negatieve waarden) |
| `ex:prop-stroombelasting` | stroom door de geleiders van de bron (`quantitykind:ElectricCurrent`); eigenschap van de verbinding of het station, geen data in dit voorbeeld |

De zeven eigenschappen van de meetlocatie hebben `qudt:hasQuantityKind
quantitykind:MagneticFluxDensity` en `skos:notation` met de sleutel uit ThingsBoard.

**Een verband in de data.** Voor alle 82 748 meetmomenten geldt
`RMStotal = 1,2374 × √(Xpeak_low² + Ypeak_low² + Zpeak_low²)` (spreiding van de factor < 0,00002).
RMStotal is dus de grootte van de *low*-vector, geschaald met een vaste factor; het apparaat berekent
die zelf.

<!-- TODO: wat betekenen 'low' en 'high' (frequentieband, bv. 5 Hz–2 kHz en 2–400 kHz; of minimum en maximum binnen het meetvenster)? Waarom zijn de 'high'-waarden vaak negatief? En waar komt de factor 1,2374 vandaan (kalibratie, piek-naar-RMS)? -->

## 6. Modelleer-keuzes toegelicht

**Waarom blootstelling op een plaats, zoals de geluidsimmissie in geluidsmeetnet?**
Verworpen alternatieven: (a) de meetlocatie als monster *van de lijn*, zoals een telpunt een monster
is van een fietsroute; (b) het veld van de bron als studieobject, zoals de emissie in
`geluidsmeetnet/alternatief/` en `overstort/alternatief/`. Gekozen: de meetlocatie als ruimtelijk
monster van de *omgeving* van de bron, met de bron als apart studieobject. Motivering:

- De vraag van het BVR en de business case is de **blootstelling van burgers op een plaats**,
  onafhankelijk van de netbeheerder. Dat is een immissievraag, zoals het vliegtuiggeluid op een
  meetpost in `geluidsmeetnet/`.
- (a) past niet. Het veld op een plaats is geen eigenschap van de lijn: het hangt af van de afstand
  tot de geleiders (snel afnemend), de doorhang, de fasevolgorde en andere bronnen. De eigenschap van
  de lijn is de stroombelasting, en die is wél representatief voor een stuk verbinding. Het veld langs
  de hele lijn is het werk van het rekenmodel (art. 6 van het BVR); de metingen toetsen het lokaal.
  Bovendien kan de bron een station zijn, en een station heeft geen "stuk lijn".
- (b) past niet. Het studieobject zou dan per bron gedefinieerd zijn, terwijl de vraag over de plaats
  gaat; een plaats kan het veld van meer dan één bron ondergaan.
- De *omgeving* van de bron werkt voor verbindingen én stations, en sluit aan bij `geluidsmeetnet/`
  (`ex:omgeving-EBBR`) en bij de definitie van `sosa:SpatialSample` (een deel van een feature, gebruikt
  wanneer een eigenschap binnen de feature varieert).

**Waarom geen `sosa:Stimulus`, zoals in geluidsmeetnet?**
In `geluidsmeetnet/` is het geluidsevent een `sosa:Stimulus`: een afgebakend voorval dat de meter
laat meten, met `sosa:wasOriginatedBy` vanaf de eventcollectie. Een ELF-veld is er continu, zonder
gebeurtenis die een meting veroorzaakt; de node meet elke minuut. Het stimuluspatroon valt dus weg.
De koppeling met de bron loopt via de bemonsterde omgeving (`prov:wasInfluencedBy`).

**Waarom `prov:wasInfluencedBy` tussen omgeving en bron?**
PROV-O definieert invloed als het vermogen van een entiteit om het karakter van een andere te
beïnvloeden: de bron bepaalt het veld in haar omgeving. PROV-O vraagt een specifiekere deeleigenschap
te gebruiken waar die past, maar geen ervan past: de omgeving is niet afgeleid van de bron
(`prov:wasDerivedFrom`) en niet door haar gegenereerd. Verworpen: `dcterms:relation`, die niets zegt
over de richting van de invloed. Beide zijn kernvocabularium (R17, niveau 1).

**Waarom het veld geen afgeleide is, niet van de flux en niet van een emissie?**
"Afgeleide" betekent hier twee verschillende dingen, en enkel de tweede hoort in de data.

- *Een wiskundige relatie tussen grootheden.* De meter meet de magnetische fluxdichtheid B (tesla).
  De magnetische flux Φ (weber) door een oppervlak is de integraal van B over dat oppervlak; B is de
  flux per oppervlakte-eenheid (dΦ/dA, 1 T = 1 Wb/m²). QUDT kent ze als twee grootheden,
  `quantitykind:MagneticFluxDensity` (hier gebruikt) en `quantitykind:MagneticFlux`. Het zijn twee
  beschrijvingen van hetzelfde veld: het ene ontstaat niet uit het andere. Zo'n relatie hoort bij
  de grootheden (de dimensievectoren van QUDT), niet tussen resources in de data, en dus niet als
  `prov:wasDerivedFrom`, dat een omzetting of constructie van een entiteit door een activiteit vraagt.
- *Een berekening in de data* (R7, R13). Een waarneming is afgeleid wanneer haar resultaat berekend
  is uit andere resultaten. Het veld van een hoogspanningslijn volgt uit de stroom in de geleiders en
  de geometrie (Biot-Savart: voor één rechte geleider B = μ₀·I / (2π·r), voor een driefasige lijn een
  som over de geleiders); de flux volgt op haar beurt uit B. Een *berekend* veld, zoals het rekenmodel
  van art. 6 van het BVR het geeft, is dus een afgeleide waarneming van de meetlocatie, met
  `sosa:hasInputValue` naar het resultaat van de stroombelasting van de bron. Een *gemeten* veld is
  dat niet: het is een rechtstreekse waarneming van de plaats.

Ook een emissie die elders als immissie aankomt (zoals geluid of fijnstof, waar de immissie als
entiteit `prov:wasDerivedFrom` de emissie zou zijn) past hier niet. Bij 50 Hz is de golflengte
ongeveer 6 000 km en ligt een meetlocatie op tientallen meters in het quasistatische nabije veld:
er reist niets van de bron naar de plaats; het veld bestaat zolang de stroom loopt. Daarom
`prov:wasInfluencedBy` tussen omgeving en bron, en geen afleiding.

De flux komt wel voor *binnen* de meetprocedure. Een meter met inductiespoelen meet een spanning die
volgens de wet van Faraday evenredig is met de verandering van de flux door de spoel (−dΦ/dt), en
rekent die om naar B. Die stap hoort in de beschrijving van `ex:procedure-elf-meting`, niet als een
aparte waarneming, net zoals de factor 1,2374 van RMStotal (§5): wat het toestel intern rekent, is
output van de meetprocedure.

<!-- TODO: welk type sonde gebruikt de ELF-node (inductiespoel, fluxgate, Hall-sensor), welke frequentieband en welk meetvenster? Dat bepaalt de beschrijving van ex:procedure-elf-meting en verklaart mogelijk 'low', 'high' en de factor 1,2374. -->

**Waarom een `sosa:Deployment` per meetcampagne, en geen `sosa:hosts`?**
Verworpen alternatief: `ex:meetlocatie-… sosa:hosts ex:sensor-…`. Gekozen: een `sosa:Deployment`
per Jira-ticket. Motivering: `sosa:hosts` is tijdloos, maar een ELF-node verhuist (ELF_C_0025:
Bloedhoven van april tot september 2025, daarna Duisterwijk). Met `sosa:hosts` zou ELF_C_0025 op twee
plaatsen tegelijk staan. De campagne geeft de periode en verbindt sensor, platform en studieobject
(SOSA 2023: *arrangement of assets … with respect to designated features of interest*). Het
uiteindelijke doel van de campagne is de omgeving van de bron (`sosa:hasUltimateFeatureOfInterest`).

**Waarom een adres én een geometrie?**
Gekozen: `prov:atLocation` naar het adres (`prov:Location`) en `geo:hasGeometry` naar een punt met een
CRS in de `geo:wktLiteral`. R11 (*Where a feature of interest is*): de geometrie maakt de meetlocatie
ruimtelijk bevraagbaar (afstand tot een verbinding, kaart in de webapp), het adres is de plaats zoals de
registratie ze geeft. Verworpen: enkel het adres (geen ruimtelijke bevraging, en een SHACL-warning van
R11 op het ruimtelijk monster), of enkel de geometrie (de link met de registratie gaat verloren).

- **Herkomst van het punt.** In productie is het de exacte locatie uit de registratie (de enquêtetool
  van de business case), of, tot die er is, de adrespositie uit het Adressenregister. Die laatste is
  de positie van het adres, niet van de sensor, en kan tientallen meters afwijken. Bij een veld dat
  snel afneemt met de afstand maakt dat uit. De geometrie zegt daarom in een `rdfs:comment` hoe ze
  bepaald is. In dit voorbeeld is het punt **fictief**: deterministisch afgeleid uit het
  gepseudonimiseerde adres, ergens in de omhullende van Vlaanderen. Echte adressen geocoderen zou de
  pseudonimisering ongedaan maken.
- **Referentiestelsel.** Lambert 72 (EPSG:31370), als CRS-IRI vooraan in de literal. Zonder CRS-IRI
  betekent een `geo:wktLiteral` lengte en breedte in CRS84.
- **Adres.** In productie verwijst de meetlocatie naar de IRI van het adres in het Adressenregister
  (`https://data.vlaanderen.be/id/adres/…`) in plaats van een eigen `ex:adres-…`; dat adres kan met
  OSLO Adres (`locn:Address`, geladen) beschreven worden. Hier is het een `prov:Location` met het
  gepseudonimiseerde adres als label.
- **Privacy.** Een meetlocatie is vaak een woning; de business case noemt de weergave van
  locatiegegevens uitdrukkelijk als gevoelig. Voor publieke ontsluiting is een veralgemeende
  geometrie (afgerond, of op straatniveau) een tweede `geo:hasGeometry`, of een apart dataproduct.

<!-- TODO: met welke nauwkeurigheid mag de positie van een meetlocatie publiek getoond worden? En geeft de enquêtetool een punt in Lambert 72, Lambert 2008 of WGS84? -->

**Waarom microtesla, en waarom een `qudt:QuantityValue`?**
Gekozen: `sosa:hasResult` naar een `qudt:QuantityValue` met `qudt:numericValue` en
`qudt:hasUnit unit:MicroT` (R3). Verworpen: `sosa:hasSimpleResult` met een kaal getal: de eenheid gaat
verloren, en de indicatoren hebben benoemde resultaten nodig als inputwaarde. De eenheid is een
**aanname**: de bron en de business case vermelden ze niet. Het bereik van RMStotal (0,20–1,72) past bij
µT voor een woonomgeving bij hoogspanning, en niet bij nT of mT. QUDT volstaat; er is geen
registereenheid nodig.

<!-- TODO: bevestiging door de beheerder van het meetnet: zijn alle zeven waarden in µT? -->

**Waarom zeven eigenschappen, en niet één vectoreigenschap?**
Verworpen alternatief: één eigenschap *magnetische fluxdichtheid* met een vectorresultaat, of
`RMStotal` als afgeleide waarneming uit de drie *low*-componenten. Gekozen: zeven `sosa:Property`'s,
één per ThingsBoard-sleutel, elk met `quantitykind:MagneticFluxDensity`. Motivering: de betekenis van
*low* en *high* is niet gedocumenteerd (§5). Elke sleutel apart houdt de data getrouw aan de bron
zonder een interpretatie op te leggen. RMStotal is weliswaar berekend (§5), maar door het apparaat
zelf, in hetzelfde bericht. Het hoort bij de output van de meetprocedure, niet bij een aparte afleiding
achteraf. Een alternatieve mapping kan RMStotal wél als afgeleide waarneming modelleren
(`sosa:hasInputValue` naar de drie *low*-resultaten), zodra de factor 1,2374 verklaard is.

**Waarom uur- en dagindicatoren, en welke?**
De business case vraagt per sensor het minimum en maximum per dag, week, maand en jaar, en de
jaargemiddelde blootstelling. Die indicatoren staan niet in de bron: het dataplatform berekent ze, in
dit voorbeeld het script. Het script is daarom de sensor, niet de ELF-node: de herkomst blijft
zichtbaar. Gekozen: een keten in twee stappen (R13), zoals de dagindicatoren en Lden in
`geluidsmeetnet/`:

- **uur**, uit de minuutwaarden: minimum, maximum en gemiddelde;
- **dag**, uit de uurindicatoren: minimum van de uurminima, maximum van de uurmaxima, gemiddelde van de
  uurgemiddelden.

Week, maand en jaar volgen op dezelfde manier uit de dagindicatoren. Het jaargemiddelde is dan het
gemiddelde van de daggemiddelden. In dit voorbeeld staat die stap er niet: de telemetrie dekt twee
maanden, en `elf.trig` bevat één dag.

- **Gelijk gewicht per uur.** Het daggemiddelde weegt elk uur met metingen even zwaar, ook als er
  minuten ontbreken (bv. 34 van de 60 op 27/11 tussen 7 en 8 uur). Zo krijgt een uur met een
  storing niet minder gewicht dan het in de tijd heeft: een tijdgewogen gemiddelde. Het aantal
  minuutwaarden van elk uur staat in `rdfs:comment` bij de uurindicator.
- **Dezelfde eigenschap.** De indicatoren hebben `ex:prop-RMStotal` als `sosa:observedProperty`, zoals
  de dagsom in `verkeersmetingen/`. Wat ze onderscheidt, is de procedure (minimum, maximum,
  gemiddelde) en de duur van de `sosa:phenomenonTime` (uur of dag). Verworpen: aparte eigenschappen
  per statistiek (*daggemiddelde RMS*, …), zoals Ld en Lden in `geluidsmeetnet/`. Daar hebben de
  indicatoren een eigen naam en definitie in de norm; hier niet.
- **Afrondingen** zijn die van de berekening (vijf decimalen); de minuutwaarden zijn die van de bron.

<!-- TODO: welk gemiddelde gebruikt het BVR of de beheerder voor de jaargemiddelde blootstelling (rekenkundig gemiddelde van RMS, tijdgewogen, kwadratisch), en hoeveel ontbrekende data is aanvaardbaar voor een dag of een jaar? -->

**Waarom geneste collecties?**
Gekozen: een uurcollectie met minuutcollecties, elk met zeven observaties. Verworpen: losse
observaties met sensor, procedure en resultaattijd op elk van de zeven herhaald, of één collectie per
campagne (82 748 leden, onhandig in een bestand per dag). Het lokale uur is ook de periode van de
uurindicatoren.

**Waarom `sosa:hasFeatureOfInterest` toch op elke observatie?**
SOSA 2023 laat de leden het studieobject van de collectie erven. De SHACL die ld-mcp uit de
OWL-restrictie op `sosa:Execution` (`someValuesFrom sosa:FeatureOfInterest`) genereert, ziet die
overerving echter niet. Daarom staat het studieobject op elk lid, zoals in `brdr/` en
`geluidsmeetnet/`.

**Waarom de apparaatstatus niet mappen?**
`lastConnectTime`, `lastActivityTime`, `lastDisconnectTime`, `lastInactivityAlarmTime`,
`inactivityTimeout` en `active` beschrijven de verbinding van het apparaat met ThingsBoard, niet het
magnetische veld. Als observaties van de meetlocatie zouden ze een verkeerd studieobject krijgen. Als
eigenschappen van de sensor horen ze bij het assetbeheer van de business case, niet bij de
waarnemingsdata (R16, in de geest: gegevens over het record of het apparaat zijn geen waarneming). De
perioden waarin `active` onwaar is, verklaren de gaten in de reeks (de grootste duurt ruim 11 uur).

**Waarom geen persoonsgegevens, en wat is fictief?**
De registratie bevat e-mailadressen, namen en voornamen van contactpersonen, en soms de naam van een
bedrijf of een site. Die worden niet overgenomen: ze zijn niet nodig voor de waarnemingen. De
bronbestanden zelf zijn bovendien gepseudonimiseerd met namen uit De Rode Ridder
(`scripts/anonimiseer.py`, zie README). Gemeenten, straten, postcodes, personen en e-mailadressen zijn
fictief, en dus ook de adressen en de IRI's van de meetlocaties (`ex:meetlocatie-6839-obscurionweg-91`).
Fictief zijn ook de bronnen (verbinding of station en spanningsniveau) en de geometrieën: de
registratie bevat ze niet, en het script leidt ze af uit de gepseudonimiseerde waarden. Meetwaarden,
datums, sensor-ID's en Jira-sleutels zijn echt.

**Waarom geen `prov:endedAtTime` voor SENS-320?**
Het einde (31/12/2026) ligt na de peildatum van de export (`PEILDATUM` in het script). Een gepland
einde is geen afgelopen activiteit; het staat als commentaar.

**Patronen.** *Ruimtelijk monster* gevolgd (de meetlocatie in de omgeving van de bron, R11).
*Afgeleide waarneming* gevolgd (uur- en dagindicatoren, met een keten zoals Lden). *Stimulus* niet
gevolgd: een continu veld heeft geen gebeurtenis. *Emissie* verworpen: de vraag gaat over de plaats,
niet over de bron (zie hoger).

**Vocabularia.** Enkel de kern (R17, niveau 1): SOSA/SSN 2023, PROV-O, QUDT, OWL-Time, GeoSPARQL,
DCTERMS, SKOS, RDFS. Geen afweging buiten de kern nodig.

**Validatie.** `elf.ttl` en `elf.trig`: geen fouten, geen suspects, geen SHACL-warnings.

## 7. Tijdsmodellering

- **Resultaattijd van een meetmoment:** `sosa:resultTime` op de minuutcollectie, als
  `xsd:dateTimeStamp` in UTC met milliseconden, zoals ThingsBoard de tijdstempel geeft (R12: een
  gegeven tijdzone blijft behouden). Het is het tijdstip waarop het resultaat beschikbaar werd.
- **Fenomeentijd van een meetmoment:** niet opgenomen. RMS- en piekwaarden gelden over een
  meetvenster, dus een `time:Instant` zou fout zijn (R12), en de duur van het venster is niet gekend.

  <!-- TODO: over welk venster berekent de node RMStotal en de piekwaarden (de minuut vóór de tijdstempel, enkele seconden)? Dan krijgt elke minuutcollectie een time:Interval als sosa:phenomenonTime. -->

- **Indicatoren:** `sosa:phenomenonTime` naar een `time:Interval` van een lokaal uur of een lokale
  dag, halfopen, met `time:Instant`s in `time:inXSDDateTimeStamp` (`2025-11-27T10:00:00+01:00` →
  `2025-11-27T11:00:00+01:00`; `2025-11-27T00:00:00+01:00` → `2025-11-28T00:00:00+01:00`). De drie
  indicatoren van een uur of een dag delen één interval. Lokale tijd, omdat uur- en dagwaarden zo
  gelezen worden; een dag eindigt op de volgende lokale middernacht, ook bij een zomertijdwissel.
  Skolem-IRI's (R10). Een minuut hoort bij het uur van haar resultaattijd: `09:00:49Z` is 10:00:49
  lokale tijd.
- **Meetcampagne:** `prov:startedAtTime` en `prov:endedAtTime` (`xsd:dateTime`) op middernacht
  lokale tijd. De registratie geeft enkel datums (`26/nov/25 12:00 AM`). Aanname: de datums zijn in
  `Europe/Brussels`, met `+01:00` in de winter en `+02:00` tijdens de zomertijd.
  De ThingsBoard-export voor SENS-269 begint om 09:00 UTC. Dat is het venster van de export, geen
  begin van de campagne; de eerste meting volgt om 09:07 UTC.

## 8. Prefixen en IRI-structuur

| Prefix | Basis-IRI | Tijdelijk of persistent |
|---|---|---|
| `sosa:` | `http://www.w3.org/ns/sosa/` | persistent (W3C) |
| `prov:` | `http://www.w3.org/ns/prov#` | persistent (W3C) |
| `time:` | `http://www.w3.org/2006/time#` | persistent (W3C) |
| `geo:` | `http://www.opengis.net/ont/geosparql#` | persistent (OGC) |
| `qudt:` | `http://qudt.org/schema/qudt/` | persistent |
| `unit:` | `http://qudt.org/vocab/unit/` | persistent |
| `quantitykind:` | `http://qudt.org/vocab/quantitykind/` | persistent |
| `dcterms:` | `http://purl.org/dc/terms/` | persistent |
| `skos:` | `http://www.w3.org/2004/02/skos/core#` | persistent (W3C) |
| `rdfs:` | `http://www.w3.org/2000/01/rdf-schema#` | persistent (W3C) |
| `xsd:` | `http://www.w3.org/2001/XMLSchema#` | persistent (W3C) |
| `ex:` | `https://example.org/elf/` | tijdelijk (illustratief) |

IRI-patronen onder `ex:`, allemaal deterministisch (R10, *stabiele IRI's in pijplijnen*):

| Resource | Patroon | Sleutel |
|---|---|---|
| sensor | `sensor-{ID}` | titel van het ticket |
| bron, omgeving | `verbinding-{gemeente}` of `station-{gemeente}`, `omgeving-{bron}` | (fictief) gemeente |
| meetlocatie, keuze, adres, geometrie | `meetlocatie-{postcode}-{straat}-{nr}`, `sampling-meetlocatie-…`, `adres-…`, `geom-…` | adresvelden |
| meetcampagne | `meetcampagne-{ticket}` | Jira-sleutel |
| uurcollectie | `collectie-{ID}-{jjjjmmdd}T{uu}` | sensor en lokaal uur |
| minuutcollectie, observatie, resultaat | `meting-{ID}-{UTC-tijdstempel met ms}`, `obs-…-{sleutel}`, `result-…-{sleutel}` | sensor, tijdstip, sleutel |
| uurindicator, interval, instants | `obs-{ID}-{jjjjmmdd}T{uu}-{minimum\|maximum\|gemiddelde}`, `interval-{ID}-{jjjjmmdd}T{uu}`, `instant-…-begin` / `-einde` | sensor, lokaal uur, statistiek |
| dagindicator, interval, instants | `obs-{ID}-{jjjjmmdd}-{statistiek}`, `interval-{ID}-{jjjjmmdd}`, … | sensor, lokale dag, statistiek |

Geen blanke knopen: het is een grote, gescripte dataset (R10).

<!-- TODO: welke persistente basis-IRI krijgt het meetnet in productie (bv. https://data.omgeving.vlaanderen.be/id/…)? -->

## 9. Inverse relaties

- `sosa:hasDeployment` (sensor → campagne) en `sosa:inDeployment` (meetlocatie → campagne): opgenomen.
  Zo vind je vanuit een sensor of een adres snel alle campagnes, en dat is de vraag die de registratie
  beantwoordt.
- `sosa:hasSample` (omgeving → meetlocaties) naast `sosa:isSampleOf`, en `sosa:isResultOf`
  (meetlocatie → keuze): opgenomen. Zo toont de kaart van de webapp vanuit een verbinding of station
  meteen de meetlocaties in de omgeving.
- `sosa:isMemberOf`, `sosa:isResultOf` en `sosa:isFeatureOfInterestOf` op minuutniveau: **niet**
  opgenomen. Ze zouden per meetmoment 22 triples toevoegen (8 `isMemberOf`, 7 `isResultOf`,
  7 `isFeatureOfInterestOf`). Een SPARQL-endpoint met inferentie of een omgekeerd pad
  (`^sosa:hasMember`) bereikt hetzelfde.
