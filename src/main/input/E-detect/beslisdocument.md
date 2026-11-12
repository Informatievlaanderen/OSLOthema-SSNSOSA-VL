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
| B1–B6 | Vragen aan de leverancier | B | open |
| C1–C3 | CSOR, QUDT, codelijsten voor geur | C | open |
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
- Een alarm is een booleaanse waarneming. De drempel staat in de procedure.
- De bronaanwijzing is een waarschijnlijkheid per bron, met de geuremissie als studieobject.

**Waarom.** Drempels en modellen moeten transparant zijn (vraag 16). Een gewijzigde drempel geeft
een andere procedure, zodat oude en nieuwe alarmen onderscheiden blijven.

**Verworpen alternatief.** Alarmen als statusveld van de sensor. Dan verdwijnt de koppeling met de
waarde en de drempel die het alarm veroorzaakten.

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
| Uitwisseling (API) | OGC SensorThings API, als kandidaat | gangbare REST-API voor sensordata, met een eigen model (Thing, Datastream, Observation) |
| Export | CSV (bestek), met een gepubliceerde mapping naar het SSN/SOSA-model | lage drempel, maar met vastgelegde betekenis per kolom |
| Tijd | ISO 8601 met tijdzone | tijdstippen zonder dubbelzinnigheid rond de zomertijd |
| Plaats | coördinaten met CRS (Lambert 72 of WGS84) | geometrieën van meetpunten en meldplaatsen |

**Waarom.**
- Het bestek legt geen standaard op, maar vraagt open of gangbare standaarden en vermijdt
  leveranciersafhankelijkheid (vraag 20).
- SSN/SOSA is het model waarop dit referentiewerk de Vlaamse toepassingen afstemt.
- OSLO Observaties en Metingen is deprecated (zie `../waterkwaliteit/bestaand_model/`) en is dus
  geen basis voor nieuw werk.
- SensorThings API is een van de gangbare API's voor sensordata. Het heeft een mappingtabel naar
  SOSA, maar geen RDF-module.

**Verworpen alternatief.** Een eigen datamodel per leverancier. Dan is de data na afloop van de
opdracht moeilijk herbruikbaar, en dat wil het project vermijden (vraag 13).

**Open.**
- Welke API of export biedt de gekozen leverancier (B1)?
- Is een publicatie als linked data (bv. LDES) nodig, of volstaan CSV plus mapping?
- Bestaat er een lopend OSLO-traject rond luchtkwaliteit of omgevingsmeldingen waarbij E-Detect kan
  aansluiten? Dat is een vraag aan Digitaal Vlaanderen.

**Status:** voorstel (deels open).

---

## 3. Deel B: vragen aan de leverancier

| # | Vraag |
|---|---|
| B1 | Welke API en welke exportformaten levert het platform? Is SensorThings API mogelijk? Wat is de structuur van de CSV (kolommen, eenheden, tijdzone)? |
| B2 | Hoe wordt de sensorrespons omgezet naar een geurconcentratie? Met welk model, welke kalibratie (EN 13725-olfactometrie, waar en wanneer) en welke foutenmarge? |
| B3 | Welke velden en schalen gebruikt de meldingsapplicatie: soort geur, intensiteit, hedonische toon, duur, locatie? |
| B4 | Wat geeft de bronanalyse als uitvoer: waarschijnlijkheid, bijdrage of rangorde? Welke invoer gebruikt ze (wind, stabiliteit, meldingen)? |
| B5 | Welke identificatoren krijgen sensoren, meetpunten en meldingen? Blijven ze stabiel bij vervanging van een sensor? |
| B6 | Hoe worden sensoruitval, onderhoud en kalibratie geregistreerd (vraag 24)? |

## 4. Deel C: registers en vocabularia

| # | Aan wie | Verzoek |
|---|---|---|
| C1 | Beheerders van CSOR | De eenheid ouE/m³ opnemen, met de definitie uit EN 13725:2022. Eventueel ook ouE/s (geuremissiedebiet). |
| C2 | QUDT (`qudt/qudt-public-repo`) | Een eenheid en een grootheid voor geurconcentratie voorstellen. `quantitykind:OlfactoryThreshold` dekt dat niet. |
| C3 | VMM / Departement Omgeving | Is er een register voor soorten geur, geurintensiteit of hedonische toon? Anders de codelijsten van A4 als register voorstellen. |

## 5. Deel D: later

| # | Onderwerp |
|---|---|
| D1 | De landbouwpilootzones: meerdere bronnen (stallen), dus mogelijk een immissie-entiteit per bron (A2) |
| D2 | Toetsing aan geurnormen of richtwaarden (bv. percentielwaarden in ouE/m³): een norm is geen waarneming (zie `vlarem_rubrieken/`) |
| D3 | Verspreidingsmodellen: een berekende geurconcentratie als afgeleide waarneming van de plaats, uit emissieresultaten (ouE/s) |
