# Drempelwaarden — rapporteringsdrempels van het CSO-register en de toets van een jaarvracht

Exploitanten rapporteren hun emissies in rapporteringscontexten zoals E-PRTR, het IMJV Water en het
IMJV Lucht. Per context bepalen rapporteringsgroepen welke parameteraspecten (stof, drager, aspect)
gerapporteerd worden, en voor een deel ervan geldt een **drempelwaarde**: boven die jaarvracht moet
de exploitant rapporteren. Dit voorbeeld zet de drempelwaarden van het CSO-register om naar RDF,
volgens het ontwerp "Ontwerp Codelijsten", en toont met SSN/SOSA hoe een jaarvracht eraan getoetst
wordt.

Twee delen:

1. **Het register** (geen SSN/SOSA): rapporteringscontexten, -groepen en drempelwaardetypes als
   SKOS-codelijsten, en 390 drempelwaarden als `qudt:QuantityValue` met een geldigheidsperiode.
   Gescript uit de CSV.
2. **De toets** (plat SSN/SOSA): de jaarvracht zink van AGC Glass Europe, vestiging Mol, in 2021
   (uit het voorbeeld [`riepr/`](../riepr/README.md)), opgeteld over de lozingspunten en getoetst
   aan de E-PRTR-drempel en de IMJV Water-drempel. Met de hand geschreven.

## Bron

Ontvangen, ongewijzigd in `source/`:

| Bestand | Inhoud |
|---|---|
| `source/rapporterings_drempelwaarden.csv` | 688 rijen: rapporteringscontext, rapporteringsgroep (met volgnummer in de context), parameteraspect (CSOR-code, symbool, drager, omschrijving, aspect), drempelwaardetype, drempelwaarde, eenheid (CSOR-code en symbool), geldig van en tot (jaar) |
| `source/Ontwerp Codelijsten_….pdf` | ontwerp van de CSOR-codelijsten als linked data; het hoofdstuk *Rapporteringscontexten, -groepen en drempelwaarden* stelt de klassen en eigenschappen voor |

Inhoud van de CSV: 3 contexten (E-PRTR 224 rijen, IMJV Water 242, IMJV Lucht 222), 22 groepen,
458 parameteraspecten, 390 rijen met een drempel, 298 zonder (enkel lidmaatschap van een groep).

De jaarvracht zink komt uit `../riepr/riepr_herzien.ttl` (IMJV 2021, lozingspunt LP01).

## Transformatie

`scripts/drempelwaarden_to_rdf.py` (Python 3, zonder extra pakketten), vanuit deze map:

```bash
python3 scripts/drempelwaarden_to_rdf.py
```

Het schrijft twee bestanden:

| Bestand | Inhoud |
|---|---|
| `src/main/resources/be/vlaanderen/omgeving/data/id/conceptscheme/csor/rapportering/rapportering.ttl` | de drie codelijsten (SKOS) en per context de volgorde van de groepen (`skos:OrderedCollection`); geladen door `ld-vocab`, zodat de data naar bestaande codes moet verwijzen |
| `drempelwaarden.ttl` | de 390 drempelwaarden |

Opschoning in het script:

- 8 rijen zonder parameteraspect (E-PRTR: koolstofdioxide, distikstofmonoxide, PM10, NMVOS,
  zwaveloxiden, koolstofmonoxide, waterstofcyanide, chloor) worden overgeslagen en gemeld;
- geldig-van **1900** en geldig-tot **2099** zijn plaatshouders voor "geen grens" en geven geen
  `dcat:startDate` of `dcat:endDate`;
- de IRI van een drempelwaarde volgt uit groep, parameteraspect, type en geldig-van-jaar (de CSV
  heeft geen eigen code; R10).

De klassen en eigenschappen (`csor:Drempelwaarde`, `csor:RapporteringsGroep`, …) staan als
**ontwerpvoorstel** in `src/main/resources/be/vlaanderen/omgeving/data/ns/csor/csor-rapportering.ttl`,
naast de CSOR-ontologie. Voor de geldigheid is DCAT 3 geladen
(`src/main/resources/org/w3/www/ns/dcat/dcat3.ttl`, <https://www.w3.org/ns/dcat.ttl>, versie 3).

## Mappingkeuzes

- **Register:** contexten, groepen en types zijn `skos:Concept`s (met een eigen subklasse van
  `skos:Concept`, R18). Een drempelwaarde is geen code maar een hoeveelheid: een
  `csor:Drempelwaarde ⊂ qudt:QuantityValue` met `qudt:numericValue` en `qudt:hasUnit` (CSOR-eenheid,
  R3), de groep, het parameteraspect, het type en `dct:temporal` naar een `dct:PeriodOfTime` met
  `dcat:startDate`/`dcat:endDate` als `xsd:gYear`.
- **Toets:** plat model met twee afgeleide observaties (R13). Het studieobject is de lozing van de
  hele exploitatie (patroon *emissie als feature of interest*), want een drempel geldt per
  exploitatie. Eerst de jaarvracht als som over de lozingspunten, dan per drempel een toets met de
  jaarvracht en de drempelwaarde als `sosa:hasInputValue` en `sosa:hasSimpleResult` waar of onwaar,
  zoals het alarm in [`E-detect/`](../E-detect/README.md).

Zie `bespreking.md`.

**Alternatief:** [`alternatief/`](alternatief/README.md) leest een drempel als een uitspraak vanuit
een rapporteringscontext over een CSOR-parameteraspect: een `oa:Annotation` (W3C Web Annotation)
met het parameteraspect als doel, de groep en het type als scope en de hoeveelheid als body. Status:
open, voor de werkgroep.

## Verbeterpunten

Punten voor het CSO-register en het ontwerp, niet opgelost in de data:

1. **Eenheden van de E-PRTR-drempels zijn inconsistent.** Voor lucht: aspect "vracht per tijd" in
   kg/jr; voor water: aspect "vracht" in kg. E-PRTR (Verordening (EG) nr. 166/2006, bijlage II)
   geeft alle drempels in kg per jaar. De jaarvracht in het IMJV (en in `riepr/`) is "vracht per
   tijd" (PAS_863, kg/jr), terwijl de drempel voor zink in water voor PAS_862 ("vracht", kg) geldt:
   een toets moet dus van parameteraspect wisselen. Voorstel: drempels voor water ook als "vracht
   per tijd" in kg/jr.
2. **Plaatshouders als jaartal.** 1900 en 2099 betekenen "geen grens"; leeg betekent hetzelfde
   voor geldig-tot bij water. Eén conventie (leeg) volstaat.
3. **8 rijen zonder parameteraspect** in E-PRTR (o.a. CO₂, N₂O, PM10, SOx): de stof staat er, het
   aspect niet, en er is geen drempel. Ontbreekt de koppeling met CSOR?
4. **Geen code voor een drempelwaarde.** Het ontwerp voorziet `RD_n`; de export heeft er geen. De
   IRI is hier afgeleid uit groep, parameteraspect, type en geldig-van.
5. **"Transfer en Lozend" (RDT_3)** combineert twee types in één code. Geldt de drempel voor elk
   apart of voor de som? Zie de TODO in `bespreking.md` §6.
6. **Ontwerp, punt per punt** (bespreking §6): `rdf:value` → `qudt:numericValue` (R3);
   `csor:heeftEenheid` → `qudt:hasUnit`; `csor:geldigVan`/`geldigTot` als `xsd:gYear` →
   `dct:temporal` met `dcat:startDate`/`endDate` (`csor:geldigTot` bestaat al met bereik
   `xsd:date`); `schema:position` → `skos:OrderedCollection` (R17); de drempelwaarde geen
   `skos:Concept`.

## Diagram

`drempelwaarden.mmd` — de twee zink-drempels in het register en de toets van de jaarvracht van
AGC Glass Europe Mol, 2021.

## Outputbestanden

| Bestand | Inhoud |
|---|---|
| `drempelwaarden.ttl` | gegenereerd: 390 drempelwaarden (4 423 triples) |
| `toetsing.ttl` | met de hand: jaarvracht van de exploitatie en twee toetsen |
| `drempelwaarden.mmd` | diagram |
| `bespreking.md` | bespreking in negen secties |
| `scripts/drempelwaarden_to_rdf.py` | omzetting van de CSV |
| `../../resources/…/conceptscheme/csor/rapportering/rapportering.ttl` | gegenereerd: codelijsten |
| `../../resources/…/ns/csor/csor-rapportering.ttl` | ontwerpvocabularium |

## Gebruik

```bash
# opnieuw genereren
cd src/main/input/drempelwaarden && python3 scripts/drempelwaarden_to_rdf.py

# valideren (MCP): validate_file op src/main/input/drempelwaarden/drempelwaarden.ttl en toetsing.ttl

# welke drempels gelden in 2021 voor zink in water?
```

```sparql
PREFIX csor: <https://data.omgeving.vlaanderen.be/ns/csor#>
PREFIX dcat: <http://www.w3.org/ns/dcat#>
PREFIX dct:  <http://purl.org/dc/terms/>
PREFIX qudt: <http://qudt.org/schema/qudt/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>
SELECT ?context ?type ?waarde ?eenheid WHERE {
  ?d csor:voorParameterAspect <https://data.omgeving.vlaanderen.be/id/concept/csor/parameteraspect/PAS_862> ;
     csor:behoortTotRapporteringsGroep/csor:behoortTotRapporteringsContext/skos:prefLabel ?context ;
     csor:heeftDrempelwaardeType/skos:prefLabel ?type ;
     qudt:numericValue ?waarde ; qudt:hasUnit ?eenheid ; dct:temporal ?p .
  OPTIONAL { ?p dcat:startDate ?van } OPTIONAL { ?p dcat:endDate ?tot }
  FILTER ((!BOUND(?van) || ?van <= "2021"^^xsd:gYear) && (!BOUND(?tot) || ?tot >= "2021"^^xsd:gYear))
}
```

De query leest de codelijsten mee: laad `rapportering.ttl` en `drempelwaarden.ttl` samen.
