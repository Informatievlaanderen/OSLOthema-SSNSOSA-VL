# Beslisdocument: geurdata van E-Detect in SSN/SOSA

*Voorbereiding voor het overleg tussen E-Detect en het Expertisecentrum Interoperabiliteit. Versie
2026-11-12.*

## 0. Doel en werkwijze

De checklist interoperabiliteit van E-Detect (EFRO-project 2330, samengevat in de [README](README.md)) vraagt bij de vragen 16
tot 18:

- welke bestaande standaarden de sensor-, weer- en meldingsgegevens consistent interpreteerbaar
  maken;
- hoe het project er pragmatisch rekening mee kan houden.

Dit document geeft daarvoor een **uitgewerkt voorstel**. Per punt staan de vraag, het voorstel
zoals het in het datavoorbeeld [`e-detect.ttl`](e-detect.ttl) is uitgewerkt, de verworpen
alternatieven en de gevolgen.

| Deel | Voor wie | Inhoud |
|---|---|---|
| **A** | E-Detect en het Expertisecentrum | modelkeuzes |
| **B** | E-Detect en de leverancier | vragen over de data die het platform zal leveren |
| **C** | beheerders van registers en vocabularia | wijzigingen buiten dit model |
| **D** | later | wat nog niet gemodelleerd is |

**Status per punt:** *voorstel* (uitgewerkt, te bevestigen), *open* (geen voorstel), *beslist*
(na een sessie invullen, met datum en wie besliste).

**Basis.** Het datavoorbeeld gebruikt **fictieve data**, want de leverancier is nog niet aangesteld.
Het voorbeeld is gevalideerd met `validate_file` van ld-mcp, zonder fouten. Zodra er een export van
het platform is, volgt een mapping van de echte data (skill `map-source-data`), en dan wordt dit
document bijgewerkt.

---

## 1. Overzicht

| # | Onderwerp | Deel | Status |
|---|---|---|---|
| A1 | Eenheid voor de geurconcentratie: ouE/m³ (EN 13725:2022) | A | voorstel |
| A2 | Het studieobject: de plaats voor metingen en meldingen, de emissie voor de bronaanwijzing | A | voorstel |
| A3 | Ruwe sensorrespons en geschatte geurconcentratie als twee waarnemingen | A | voorstel |
| A4 | De geurmelding als menselijke waarneming | A | voorstel (deels open) |
| A5 | Alarmen en bronaanwijzing als afgeleide waarnemingen | A | voorstel |
| A6 | Standaarden voor model en uitwisseling | A | voorstel (deels open) |
| A7 | API's en ontsluiting: SensorThings API, LDES, opvraagbare IRI's, SPARQL | A | voorstel (deels open) |
| B1–B7 | Vragen aan de leverancier | B | open |
| C1–C4 | CSOR, QUDT, codelijsten voor geur, LDES (OpenLDES) en persistente IRI's | C | open |
| D1–D3 | Landbouwzones, normtoetsing, verspreidingsmodellen | D | later |

---

## 2. Deel A: modelkeuzes

### A1. Eenheid voor de geurconcentratie

**Vraag.** In welke eenheid en met welke IRI wordt een geurconcentratie uitgewisseld?

**Voorstel.** De Europese geureenheid per kubieke meter (ouE/m³) volgens EN 13725:2022. Tot CSOR ze
opneemt, staat ze als tijdelijke eenheid in een eigen namespace:

```turtle
eenheid:ouE-PER-M3 a qudt:Unit , skos:Concept ;
    qudt:symbol "ouE/m³" ;
    skos:definition "… volgens EN 13725:2022 …"@nl .
ex:result-G01-20261105T2214-geurconcentratie a qudt:QuantityValue ;
    qudt:numericValue 7.4 ; qudt:hasUnit eenheid:ouE-PER-M3 .
```

**Waarom.**
- QUDT 3.5.2 en het CSOR-eenhedenregister hebben geen eenheid voor geurconcentratie. QUDT heeft
  alleen `quantitykind:OlfactoryThreshold`, en dat is de drempel van één stof.
- ouE/m³ is operationeel gedefinieerd: verdunning tot de detectiedrempel van een panel, waar de
  concentratie per definitie 1 ouE/m³ is.
- De referentie 1 ouE ≙ 1 EROM = 123 µg n-butanol geldt alleen voor n-butanol. Een omrekening
  naar een massaconcentratie is voor een geurmengsel dus niet mogelijk.

**Verworpen alternatieven.**
- `unit:NUM-PER-M3`: telt deeltjes of organismen. Een afnemer zou de waarden kunnen optellen of
  omrekenen alsof het tellingen zijn.
- Een massaconcentratie (`unit:MicroGM-PER-M3`) met een n-butanol-equivalent: suggereert een
  stofconcentratie die niet gemeten is.
- Een eenheid als vrije tekst ("OU/m3") in de CSV: niet eenduidig. Sommige bronnen schrijven OU of
  OUE zonder de Europese normering.

**Gevolg.** Een verzoek aan CSOR (C1). Na opname vervangt de CSOR-IRI de tijdelijke IRI.

**Status:** voorstel.

### A2. Het studieobject

**Vraag.** Waarover gaat een meting, een melding en een bronaanwijzing?

**Voorstel.** Volgens het patroon *Emissie en immissie* van het referentiewerk:

- **Metingen** gaan over het meetpunt: platform, studieobject en ruimtelijk monster van de omgeving
  van de industriezone.
- **Meldingen** gaan over de meldplaats, een ruimtelijk monster met veralgemeende geometrie.
- **De bronaanwijzing** gaat over de geuremissie van een bedrijf: een `prov:Entity`, voortgebracht
  door de productie.

```turtle
ex:meetpunt-G01 a sosa:Platform , sosa:FeatureOfInterest , sosa:SpatialSample ;
    sosa:isSampleOf ex:omgeving-industriezone .
ex:omgeving-industriezone prov:wasInfluencedBy ex:geuremissie-bedrijf-A .
ex:obs-bedrijf-A-20261105T2210-bron sosa:hasFeatureOfInterest ex:geuremissie-bedrijf-A .
```

**Waarom.**
- De vraag bepaalt het studieobject. "Hoeveel geur krijgt deze plaats?" gaat over de plaats.
  "Welke bron veroorzaakt de geur?" gaat over de emissie.
- Zo blijven klachtenbehandeling en handhaving (over de plaats) gescheiden van bedrijfsvoering en
  vergunning (over de bron). De checklist noemt beide (vragen 7 en 10).
- Hetzelfde patroon staat in `geluidsmeetnet/` (vliegtuiggeluid) en `elf/` (magnetische velden).

**Verworpen alternatieven.**
- Het bedrijf als studieobject van de metingen: de sensor meet de lucht op het meetpunt, niet het
  bedrijf. Geur kan bovendien van meerdere bronnen komen (vraag 15).
- De geurpiek als `sosa:Stimulus`: de e-nose meet continu, er is geen gebeurtenis die een meting in
  gang zet.

**Open.** Een immissie-entiteit (de geur van bedrijf A zoals ze het meetpunt bereikt) is pas nodig
als er meerdere bronnen zijn. Dat geldt voor de landbouwzones (D1).

**Status:** voorstel.

### A3. Ruwe sensorrespons en geschatte geurconcentratie

**Vraag.** Hoe worden het signaal van de e-nose en de geschatte geurconcentratie uitgewisseld?

**Voorstel.** Als twee waarnemingen:

1. de sensorrespons (dimensieloos), gemaakt door de e-nose;
2. de geurconcentratie in ouE/m³, een afgeleide waarneming gemaakt door het kalibratiemodel. Die
   verwijst met `sosa:hasInputValue` naar de responswaarden en met `sosa:relatedObservation` naar
   de waarnemingen.

**Waarom.**
- De sensor meet veranderingen in de luchtsamenstelling, geen geurconcentratie en geen
  geurbeleving (checklist vragen 12 en 15).
- Het bestek vraagt transparantie over verwerkingsstappen, omzettingen, aggregaties, drempels en
  modellen (vraag 16). Een afgeleide waarneming met een eigen procedure maakt dat zichtbaar en
  herleidbaar in de data zelf.

**Verworpen alternatief.** Enkel de geschatte concentratie exporteren. Dan is niet meer na te gaan
welke kalibratie gebruikt werd, en worden twee leveranciers onvergelijkbaar.

**Gevolg.** De leverancier beschrijft het kalibratiemodel als procedure (B2), en de export bevat
beide waarden.

**Status:** voorstel.

### A4. De geurmelding

**Vraag.** Hoe wordt een geurmelding van een burger gemodelleerd?

**Voorstel.**
- Een melding is een collectie van waarnemingen (soort geur, intensiteit, hedonische toon) door een
  mens als sensor, gepseudonimiseerd.
- Het tijdstip van de waarneming en het moment van melden staan apart (`sosa:phenomenonTime`,
  `sosa:resultTime`).
- De meldplaats krijgt een veralgemeende geometrie.
- De resultaten zijn begrippen uit SKOS-codelijsten: intensiteit volgens VDI 3882-1 (0–6),
  hedonische toon volgens VDI 3882-2 (−4…+4).

**Waarom.**
- Een melding is een menselijke waarneming en geen klacht-dossier. Ze kan zo samen met de
  sensordata geanalyseerd worden (vraag 12).
- De locatie kan iemands woning zijn, en dus persoonsgegevens (AVG, vraag 27).

**Verworpen alternatief.** De melding als vrije tekst of als record zonder SOSA-structuur. Dan kan
ze niet als inputwaarde van een bronanalyse dienen.

**Open.**
- Welke veralgemening is nodig (vak van 100 m, buurt)?
- Welke schalen gebruikt de meldingsapp (B3)?
- Bestaat er een register voor de schalen of voor soorten geur (C3)?

**Status:** voorstel (deels open).

### A5. Alarmen en bronaanwijzing

**Vraag.** Hoe worden de verwerkte gegevens uitgewisseld: afwijkingen, alarmen, trends en analyses
van bronnen (vraag 12)?

**Voorstel.**
- Elk verwerkt gegeven is een afgeleide waarneming met een eigen procedure, sensor (het model van
  het platform) en invoer.
- Een alarm is een booleaanse waarneming. De drempel is een input van de alarmprocedure, en elk
  alarm geeft de drempelwaarde waarmee het berekend is:

```turtle
ex:procedure-drempel sosa:hasInput ex:prop-geurconcentratie , ex:prop-alarmdrempel .
ex:drempel-5-ouE a qudt:QuantityValue ; qudt:numericValue 5 ; qudt:hasUnit eenheid:ouE-PER-M3 .
ex:obs-G01-20261105T2214-alarm
    sosa:hasInputValue ex:result-G01-20261105T2214-geurconcentratie , ex:drempel-5-ouE .
```

- De bronaanwijzing is een waarschijnlijkheid per bron, met de geuremissie als studieobject.

**Waarom.** Drempels en modellen moeten transparant zijn (vraag 16). Met de drempel als
inputwaarde is in de data zelf te zien met welke drempel elk alarm berekend is. Een gewijzigde
drempel is een nieuwe waarde, geen nieuwe procedure, en oude en nieuwe alarmen blijven
onderscheiden.

**Verworpen alternatieven.**
- Alarmen als statusveld van de sensor: dan verdwijnt de koppeling met de waarde en de drempel die
  het alarm veroorzaakten.
- De drempel enkel als tekst in de procedure, of een procedure per drempel: niet leesbaar door een
  machine, of een nieuwe procedure bij elke wijziging.

**Open.** Geeft het bronanalysemodel een waarschijnlijkheid, een bijdrage in ouE/m³ of een
rangorde (B4)? Een bijdrage is een afgeleide waarneming van de *plaats* per bron.

**Status:** voorstel.

### A6. Standaarden voor model en uitwisseling

**Vraag.** Welke standaarden past E-Detect toe, en hoe vraagt het die aan de leverancier
(vragen 17 tot 19 en 22)?

**Voorstel.**

| Laag | Standaard | Rol |
|---|---|---|
| Semantiek | W3C SSN/SOSA 2023, met PROV-O, QUDT, OWL-Time en GeoSPARQL, toegepast volgens dit referentiewerk (OSLOthema SSN/SOSA-VL) | betekenis van waarneming, sensor, studieobject, procedure, resultaat, eenheid, tijd en plaats |
| Eenheden | CSOR (met QUDT-mapping waar die bestaat) | eenduidige eenheden, ouE/m³ inbegrepen (A1) |
| Meetnorm | EN 13725:2022 | de definitie van de geurconcentratie en de kalibratiereferentie |
| Uitwisseling | OGC SensorThings API, LDES, opvraagbare IRI's, SPARQL | elk voor een andere afnemer, zie A7 |
| Export | CSV (bestek), met een gepubliceerde mapping naar het SSN/SOSA-model | lage drempel, maar met vastgelegde betekenis per kolom |
| Tijd | ISO 8601 met tijdzone | tijdstippen zonder dubbelzinnigheid rond de zomertijd |
| Plaats | coördinaten met CRS (Lambert 72 of WGS84) | geometrieën van meetpunten en meldplaatsen |

**Waarom.**
- Het bestek legt geen standaard op, maar vraagt open of gangbare standaarden en vermijdt
  leveranciersafhankelijkheid (vraag 20).
- SSN/SOSA is het model waarop dit referentiewerk de Vlaamse toepassingen afstemt.
- OSLO Observaties en Metingen is deprecated (zie `../waterkwaliteit/bestaand_model/`) en is dus
  geen basis voor nieuw werk.

**Verworpen alternatief.** Een eigen datamodel per leverancier. Dan is de data na afloop van de
opdracht moeilijk herbruikbaar, en dat wil het project vermijden (vraag 13).

**Open.**
- Welke API of export biedt de gekozen leverancier (B1)? De ontsluiting zelf staat in A7.
- Bestaat er een lopend OSLO-traject rond luchtkwaliteit of omgevingsmeldingen waarbij E-Detect kan
  aansluiten? Dat is een vraag aan Digitaal Vlaanderen.

**Status:** voorstel (deels open).

### A7. API's en ontsluiting

**Vraag.** Via welke kanalen worden de gegevens ontsloten, en wie levert of beheert elk kanaal
(checklist vragen 13, 22 en 28)?

**Voorstel.** Vier kanalen, elk voor een andere afnemer. Ze vervangen elkaar niet:

| Kanaal | Voor wie | Model | Sterk | Zwak |
|---|---|---|---|---|
| **OGC SensorThings API** | dashboard, meldingsapp, toepassingen die per sensor of meetpunt actuele en recente waarden opvragen | eigen model: Thing, Location, Datastream, Sensor, ObservedProperty, Observation, FeatureOfInterest; JSON over REST, met MQTT voor realtime | gangbaar bij leveranciers van sensorplatformen; filteren en pagineren zijn gestandaardiseerd | geen RDF; een afgeleide waarneming kan niet naar haar inputwaarden verwijzen (geen `sosa:hasInputValue`); een melder als Thing is onnatuurlijk; IRI's en identificatoren zijn die van het platform |
| **LDES** (Linked Data Event Streams) | andere systemen die alle waarnemingen willen overnemen en bijhouden: provincie, VMM, een volgend platform | SSN/SOSA zoals in `e-detect.ttl` | volledige geschiedenis, incrementeel te synchroniseren, onafhankelijk van de leverancier; in Vlaanderen al gebruikt (zie `overstort/`) | geen bevraging; afnemers bouwen zelf een opslag |
| **Opvraagbare IRI's** (resource endpoints) | iedereen die naar een meetpunt, sensor, procedure, drempel of eenheid verwijst | SSN/SOSA, met content negotiation (HTML voor mensen, Turtle of JSON-LD voor machines) | stabiele verwijzingen, ook na wissel van leverancier; de procedure van een kalibratie of drempel blijft opvraagbaar (A3, A5) | vraagt een persistente basis-IRI en een beheerder (C4) |
| **SPARQL** | analyse over bronnen heen: alarmen naast meldingen en wind, vergelijking van pilootzones, evaluatie door VITO | SSN/SOSA, gevuld vanuit de LDES | vrije combinatie van sensor-, weer- en meldingsdata | zwaar om openbaar te garanderen; geen operationeel kanaal |

De samenhang:

```
e-nose, windmeter, meldingsapp
        │
        ▼
platform van de leverancier ──► SensorThings API (operationeel, eigen model)
        │                  └─► CSV-export (bestek)
        ▼  mapping naar SSN/SOSA (gepubliceerd)
LDES-stroom (waarnemingen, afgeleide waarnemingen)
        │
        ├─► opvraagbare IRI's: meetpunten, sensoren, procedures, drempels, eenheid
        └─► SPARQL-endpoint voor analyse (optioneel)
```

- **De leverancier** levert een API, liefst de SensorThings API, plus de CSV-export uit het bestek.
  Daarnaast levert hij een LDES-stroom in SSN/SOSA, of een stroom waaruit die met een gepubliceerde
  mapping gebouwd kan worden. Daarvoor bestaan open componenten: de LDES-server en de pipelines
  van LDIO (Linked Data Interactions) van [OpenLDES](https://github.com/OpenLDES), beheerd door het
  Departement Omgeving (EUPL-1.2). Aquafin gebruikt LDIO voor zijn overstortdata (`overstort/`).
- **In de SensorThings API** verwijzen `unitOfMeasurement.definition` en
  `ObservedProperty.definition` naar de IRI's van de eenheid en de eigenschap. Zo blijft de koppeling
  met het SOSA-model in de API zelf zichtbaar.
- **De opdrachtgever** beheert de IRI's van meetpunten, sensoren, procedures en drempels onder een
  eigen, persistente basis-IRI, niet onder het domein van de leverancier.
- **SPARQL** is een optie voor de analysefase, gevuld vanuit de LDES. Het is geen vereiste voor de
  leverancier.

**Waarom.**
- Het project wil dat de data bruikbaar blijft na afloop van de opdracht en buiten het
  leveranciersplatform (vragen 13 en 28). Een LDES in SSN/SOSA met IRI's van de opdrachtgever maakt
  de data overdraagbaar; een API van het platform alleen doet dat niet.
- De transparantie van de verwerking (vraag 16) vraagt dat een alarm naar zijn drempel en een
  geschatte concentratie naar haar inputwaarden verwijst. Dat kan in SSN/SOSA, niet in het model van
  SensorThings.
- Leveranciers van sensorplatformen bieden vaak SensorThings of een eigen REST-API. Die vragen als
  operationeel kanaal sluit aan bij de markt. Een tweede, neutrale laag beschermt tegen
  afhankelijkheid.

**Verworpen alternatieven.**
- *Alleen de SensorThings API.* Geen RDF, geen verwijzing naar inputwaarden, en IRI's en
  identificatoren van het platform. Bij een wissel van leverancier verandert alles.
- *Alleen CSV.* Laagdrempelig, maar zonder vastgelegde betekenis per kolom en zonder incrementele
  synchronisatie.
- *SPARQL als enige API.* Niet incrementeel, zwaar om openbaar te garanderen, en ongeschikt voor
  realtime toepassingen.

**Gevolg.**
- **Herziene en herberekende waarden.** Een LDES-member wordt niet overschreven. Een herberekening
  met een nieuw kalibratiemodel is dus een nieuwe afgeleide waarneming met een nieuwe procedure, geen
  wijziging van de oude.
- **Waarneming of record.** De member van de LDES is de waarneming zelf (oplossing A van
  [R16](https://informatievlaanderen.github.io/OSLOthema-SSNSOSA-VL/regels/r16/)): zonder
  `prov:generatedAtTime` op de waarneming. Dat is de les uit `overstort/`.
- **Toegang.** Bedrijfsgevoelige gegevens en meldingen (AVG) gaan niet in een openbare stroom. Ofwel
  komen er twee stromen (openbaar en afgeschermd), ofwel worden meldplaatsen veralgemeend en
  bedrijfsgevoelige analyses weggelaten vóór publicatie.

**Open.**
- Wie beheert de persistente IRI's en de LDES: de provincie zelf, met de componenten van OpenLDES,
  of een gedeelde LDES-infrastructuur (C4)?
- Is een SPARQL-endpoint nodig voor de evaluatie door VITO, of volstaat een eigen opslag gevuld
  vanuit de LDES?
- Welke gegevens zijn openbaar, welke afgeschermd (B7)?

**Status:** voorstel (deels open).

---

## 3. Deel B: vragen aan de leverancier

| # | Vraag |
|---|---|
| B1 | Welke API en welke exportformaten levert het platform? Is de SensorThings API mogelijk, met `unitOfMeasurement.definition` en `ObservedProperty.definition` als IRI's? Kan het platform een LDES-stroom leveren, of een stroom waaruit die gebouwd kan worden? Wat is de structuur van de CSV (kolommen, eenheden, tijdzone)? |
| B2 | Hoe wordt de sensorrespons omgezet naar een geurconcentratie? Met welk model, welke kalibratie (EN 13725-olfactometrie, waar en wanneer) en welke foutenmarge? |
| B3 | Welke velden en schalen gebruikt de meldingsapplicatie: soort geur, intensiteit, hedonische toon, duur, locatie? |
| B4 | Wat geeft de bronanalyse als uitvoer: waarschijnlijkheid, bijdrage of rangorde? Welke invoer gebruikt ze (wind, stabiliteit, meldingen)? |
| B5 | Welke identificatoren krijgen sensoren, meetpunten en meldingen? Blijven ze stabiel bij vervanging van een sensor? |
| B6 | Hoe worden sensoruitval, onderhoud en kalibratie geregistreerd (vraag 24)? |
| B7 | Welke gegevens mogen openbaar, welke enkel voor aangeduide derden (rol- en rechtenbeheer, vraag 25)? Kan het platform per kanaal afschermen? |

## 4. Deel C: registers en vocabularia

| # | Aan wie | Verzoek |
|---|---|---|
| C1 | Beheerders van CSOR | De eenheid ouE/m³ opnemen, met de definitie uit EN 13725:2022. Eventueel ook ouE/s (geuremissiedebiet). |
| C2 | QUDT (`qudt/qudt-public-repo`) | Een eenheid en een grootheid voor geurconcentratie voorstellen. `quantitykind:OlfactoryThreshold` dekt dat niet. |
| C3 | VMM / Departement Omgeving | Is er een register voor soorten geur, geurintensiteit of hedonische toon? Anders de codelijsten van A4 als register voorstellen. |
| C4 | Departement Omgeving (OpenLDES) | Kan E-Detect de LDES-server en LDIO van OpenLDES gebruiken, als gedeelde infrastructuur of zelf geïnstalleerd door de provincie of de leverancier? Onder welke persistente basis-IRI komen meetpunten, sensoren, procedures en drempels? |

## 5. Deel D: later

| # | Onderwerp |
|---|---|
| D1 | De landbouwpilootzones: meerdere bronnen (stallen), dus mogelijk een immissie-entiteit per bron (A2) |
| D2 | Toetsing aan geurnormen of richtwaarden (bv. percentielwaarden in ouE/m³): een norm is geen waarneming (zie `vlarem_rubrieken/`) |
| D3 | Verspreidingsmodellen: een berekende geurconcentratie als afgeleide waarneming van de plaats, uit emissieresultaten (ouE/s) |
