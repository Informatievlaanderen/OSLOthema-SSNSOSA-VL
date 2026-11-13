# Drempelwaarden — alternatief: een drempel als Web Annotation

## Intentie

Geen herziening. Dit alternatief staat naast het hoofdmodel (`../drempelwaarden.ttl`,
`../toetsing.ttl`): twee verdedigbare lezingen van dezelfde drempels, voor de werkgroep. Status:
**open** (2026-11-13).

Het hoofdmodel maakt van een drempel een **ding van het register**: een `csor:Drempelwaarde`, een
`qudt:QuantityValue` met eigen eigenschappen naar groep, parameteraspect en type
(ontwerpvocabularium `csor-rapportering.ttl`). Dit alternatief leest een drempel als een **uitspraak
vanuit een context over iets in CSOR**: de rapporteringscontext (via haar groep) zegt over een
parameteraspect "boven deze hoeveelheid moet gerapporteerd worden". Zo'n uitspraak is een
`oa:Annotation` van het W3C [Web Annotation Data Model](https://www.w3.org/TR/annotation-model/):

| Rol in de annotatie | Hier |
|---|---|
| doel (`oa:hasTarget`) | een `oa:SpecificResource`: het parameteraspect (`oa:hasSource`), bekeken binnen de rapporteringsgroep en het drempelwaardetype (`oa:hasScope`) |
| body (`oa:hasBody`) | de drempel, een `qudt:QuantityValue` met `qudt:numericValue` en een CSOR-eenheid (R3) |
| motivatie (`oa:motivatedBy`) | `alt:rapporteringsdrempel`, een eigen `oa:Motivation` met `skos:broader oa:describing` |
| auteur (`dct:creator`) | de beheerder van het register (illustratief) |
| geldigheid (`dct:temporal`) | zoals het hoofdmodel: `dct:PeriodOfTime` met `dcat:startDate`/`dcat:endDate` |

Het alternatief volgt [`rdf-memory/`](../../rdf-memory/README.md), het andere voorbeeld met het
Web Annotation-model (een uitspraak van een agent over een doel), en het patroon van het hoofdmodel
en `E-detect/` voor de toets: de drempel is een `sosa:hasInputValue` (R13). Alleen wat die
inputwaarde is, verschilt: de body van de annotatie in plaats van de `csor:Drempelwaarde`.

## Bron en selectie

Dezelfde bron als het hoofdmodel (`../source/rapporterings_drempelwaarden.csv`). Selectie: de drie
drempels voor zink in water (PAS_862): E-PRTR lozend en transfer (100 kg, vanaf 2007) en IMJV Water
transfer en lozend (50 kg, vanaf 1996), en de twee toetsen van `../toetsing.ttl`. Met de hand
geschreven.

Daarnaast, om te tonen dat dezelfde structuur ook een **bereik** draagt: een lozingsvoorwaarde van
VLAREM II voor pH (PAS_2117), 6,5 tot en met 9, als annotatie met de body
`qudt:minInclusive 6.5 ; qudt:maxInclusive 9.0` en de motivatie `alt:toegelaten-bereik`, met een
**fictieve** pH-meting van LP01 (7,8 op 15 juni 2021) en een toets (*binnen het bereik*: waar).
Illustratief: de bron bevat geen lozingsvoorwaarden. Of de QUDT-facetten hiervoor correct zijn, staat
in de bespreking §6.

## Verschillen met het hoofdmodel

| Aspect | Hoofdmodel | Alternatief |
|---|---|---|
| wat een drempel is | een hoeveelheid van het register: `csor:Drempelwaarde ⊂ qudt:QuantityValue` | een uitspraak: `oa:Annotation` met de hoeveelheid als body |
| wie spreekt | impliciet het register | expliciet: `dct:creator`, en de context als scope |
| verband met groep en type | `csor:behoortTotRapporteringsGroep`, `csor:heeftDrempelwaardeType` | `oa:hasScope` op het doel (beide) |
| verband met het parameteraspect | `csor:voorParameterAspect` | `oa:hasSource` op het doel |
| wat voor uitspraak | de klasse `csor:Drempelwaarde` | de motivatie `alt:rapporteringsdrempel` |
| nieuwe termen | klasse `csor:Drempelwaarde` en drie eigenschappen | geen klassen of eigenschappen; één motivatie (een concept) |
| knopen per drempel | 2 (drempel, geldigheid) | 4 (annotatie, doel, body, geldigheid) |
| controle met de gegenereerde SHACL | `owl:someValuesFrom` op `csor:Drempelwaarde` (groep, aspect, type, eenheid, geldigheid) | geen: OA heeft geen restricties (zie bespreking §6, tussenvorm) |
| inputwaarde van de toets | de drempelwaarde zelf | de body; de context via `^oa:hasBody` |
| andere contexten (normen, vergunningen) die iets zeggen over hetzelfde parameteraspect | elk een eigen klasse en eigenschappen | dezelfde annotatie, een andere motivatie en scope |
| codelijsten (context, groep, type) | gedeeld | gedeeld |
| een bereik in plaats van een drempel (pH 6,5–9) | een eigen klasse nodig: `csor:Drempelwaarde` eist `qudt:numericValue` | dezelfde annotatie, een body met `qudt:minInclusive`/`qudt:maxInclusive` en een andere motivatie |

Gedeelde IRI's: de codelijsten en de parameteraspecten (CSOR), en `ex:` uit `../toetsing.ttl` (de
lozing, de jaarvracht, de procedure, de sensor). Wat verschilt, staat onder
`alt:` = `https://example.org/drempelwaarden/alternatief/`, zodat beide samen geladen kunnen worden.

## Transformatie

Geen; met de hand geschreven. Als dit alternatief gekozen wordt, schrijft
`../scripts/drempelwaarden_to_rdf.py` per rij een annotatie, een doel, een body en een geldigheid
in plaats van een `csor:Drempelwaarde`, met IRI's onder
`https://data.omgeving.vlaanderen.be/id/csor/annotatie/{groep}/{parameteraspect}/{type}/{geldig-van}`
(en `…/doel`, `…/waarde`, `…/geldigheid`); de motivatie komt in het register.

## Diagram

- `drempelwaarden_annotatie.mmd` — dit alternatief.
- `drempelwaarden_vergelijking.mmd` — één drempel in het hoofdmodel en in het alternatief.

## Outputbestanden

| Bestand | Inhoud |
|---|---|
| `drempelwaarden_annotatie.ttl` | drie drempels als annotatie en twee toetsen; een pH-bereik als annotatie, een fictieve pH-meting en een bereiktoets |
| `drempelwaarden_annotatie.mmd` | diagram |
| `drempelwaarden_vergelijking.mmd` | vergelijkingsdiagram |
| `bespreking.md` | bespreking, met argumenten en discussievragen in §6 |

## Gebruik

De queries lezen drie bestanden samen: dit alternatief, `../toetsing.ttl` (de jaarvracht) en de
codelijsten (de naam van de context staat alleen in het register):

```bash
arq --data src/main/input/drempelwaarden/alternatief/drempelwaarden_annotatie.ttl \
    --data src/main/input/drempelwaarden/toetsing.ttl \
    --data src/main/resources/be/vlaanderen/omgeving/data/id/conceptscheme/csor/rapportering/rapportering.ttl \
    --query <query>.rq
```

### Wat zegt welke context over een parameteraspect?

Elke rij is één annotatie: de auteur, de context (via de groep in `oa:hasScope`), het type (de
tweede scope), het parameteraspect (`oa:hasSource` van het doel), de drempel (de body), de
geldigheid en de motivatie.

```sparql
PREFIX oa:   <http://www.w3.org/ns/oa#>
PREFIX csor: <https://data.omgeving.vlaanderen.be/ns/csor#>
PREFIX dcat: <http://www.w3.org/ns/dcat#>
PREFIX dct:  <http://purl.org/dc/terms/>
PREFIX qudt: <http://qudt.org/schema/qudt/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
# Wie zegt vanuit welke context wat over welk parameteraspect?
SELECT ?auteur ?context ?groep ?type ?parameteraspect ?waarde ?eenheid ?vanaf ?motivatie WHERE {
  ?a a oa:Annotation ;
     dct:creator/rdfs:label ?auteur ;
     oa:motivatedBy/skos:prefLabel ?motivatie ;
     oa:hasTarget ?doel ;
     oa:hasBody [ qudt:numericValue ?waarde ; qudt:hasUnit/rdfs:label ?eenheid ] ;
     dct:temporal/dcat:startDate ?vanaf .
  ?doel oa:hasSource/rdfs:label ?parameteraspect ;
        oa:hasScope ?g , ?t .
  ?g a csor:RapporteringsGroep ; rdfs:label ?groep ;
     csor:behoortTotRapporteringsContext/skos:prefLabel ?context .
  ?t a csor:DrempelwaardeType ; rdfs:label ?type .
}
ORDER BY ?context ?type
```

| auteur | context | groep | type | parameteraspect | waarde | eenheid | vanaf | motivatie |
|---|---|---|---|---|---|---|---|---|
| Beheerder van het CSO-register (illustratief) | E-PRTR | Zware metalen (E-PRTR) | Lozend | Zn t (totaal in water): vracht | 100.0 | kilogram | 2007 | rapporteringsdrempel |
| Beheerder van het CSO-register (illustratief) | E-PRTR | Zware metalen (E-PRTR) | Transfer | Zn t (totaal in water): vracht | 100.0 | kilogram | 2007 | rapporteringsdrempel |
| Beheerder van het CSO-register (illustratief) | IMJV Water | IMJV - zware metalen (IMJV Water) | Transfer en Lozend | Zn t (totaal in water): vracht | 50.0 | kilogram | 1996 | rapporteringsdrempel |

Dezelfde PAS_862 krijgt vanuit twee contexten drie drempels: E-PRTR zegt 100 kg (voor lozen en voor
transfer apart), het IMJV Water 50 kg. In het hoofdmodel geeft de query in `../README.md` hetzelfde
via `csor:voorParameterAspect`, `csor:behoortTotRapporteringsGroep` en `csor:heeftDrempelwaardeType`.

### Aan welke drempel is getoetst?

Vanuit de toets: de inputwaarde is de body; de context staat op de annotatie, dus de query gaat
terug via `oa:hasBody` (argument tegen 4 in de bespreking).

```sparql
PREFIX oa:   <http://www.w3.org/ns/oa#>
PREFIX csor: <https://data.omgeving.vlaanderen.be/ns/csor#>
PREFIX qudt: <http://qudt.org/schema/qudt/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX sosa: <http://www.w3.org/ns/sosa/>
# Aan welke drempel, vanuit welke context, is getoetst? Van de toets via de body terug naar de annotatie.
SELECT ?toets ?context ?type ?drempel ?jaarvracht ?boven WHERE {
  ?toets a sosa:Observation ;
         sosa:hasSimpleResult ?boven ;
         sosa:hasInputValue ?body ;
         sosa:relatedObservation/sosa:hasResult/qudt:numericValue ?jaarvracht .
  ?a oa:hasBody ?body ;                               # ^oa:hasBody: van de waarde naar de uitspraak
     oa:hasTarget/oa:hasScope ?g , ?t .
  ?body qudt:numericValue ?drempel .
  ?g a csor:RapporteringsGroep ; csor:behoortTotRapporteringsContext/skos:prefLabel ?context .
  ?t a csor:DrempelwaardeType ; rdfs:label ?type .
}
ORDER BY ?context
```

| toets | context | type | drempel | jaarvracht | boven |
|---|---|---|---|---|---|
| `alt:toets-eprtr-zn-agc-mol-2021` | E-PRTR | Lozend | 100.0 | 1.59612 | false |
| `alt:toets-imjvwater-zn-agc-mol-2021` | IMJV Water | Transfer en Lozend | 50.0 | 1.59612 | false |

De jaarvracht (kg/jr) en de drempel (kg) staan in een andere eenheid; de procedure zet ze om
(`../bespreking.md` §6, *Waarom PAS_863 toetsen aan een drempel voor PAS_862?*).

### Ligt een gemeten waarde binnen het toegelaten bereik?

Het bereik is de body, zonder `qudt:numericValue`. De query leest de grenzen, inclusief
(`qudt:minInclusive`, `qudt:maxInclusive`) of exclusief (`qudt:minExclusive`, `qudt:maxExclusive`),
rekent zelf na of de gemeten waarde erbinnen ligt (`?binnen`) en zet dat naast het resultaat van de
toets (`?toets`). Een ontbrekende grens beperkt niet. Alleen dit bestand is nodig.

```sparql
PREFIX oa:   <http://www.w3.org/ns/oa#>
PREFIX qudt: <http://qudt.org/schema/qudt/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX sosa: <http://www.w3.org/ns/sosa/>
# Ligt een gemeten waarde binnen het toegelaten bereik? De query rekent het na uit de body,
# met inclusieve (minInclusive, maxInclusive) en exclusieve (minExclusive, maxExclusive) grenzen.
SELECT ?parameteraspect ?scope ?ondergrens ?bovengrens ?gemeten ?binnen ?toets WHERE {
  ?a oa:motivatedBy/skos:prefLabel "toegelaten bereik"@nl ;
     oa:hasTarget [ oa:hasSource ?pa ; oa:hasScope/rdfs:label ?scope ] ;
     oa:hasBody ?bereik .
  ?pa rdfs:label ?parameteraspect .
  OPTIONAL { ?bereik qudt:minInclusive ?minI }
  OPTIONAL { ?bereik qudt:minExclusive ?minE }
  OPTIONAL { ?bereik qudt:maxInclusive ?maxI }
  OPTIONAL { ?bereik qudt:maxExclusive ?maxE }
  ?obs sosa:observedProperty ?pa ; sosa:hasResult/qudt:numericValue ?gemeten .
  # een ontbrekende grens beperkt niet
  BIND ( (!BOUND(?minI) || ?gemeten >= ?minI) && (!BOUND(?minE) || ?gemeten > ?minE)
      && (!BOUND(?maxI) || ?gemeten <= ?maxI) && (!BOUND(?maxE) || ?gemeten < ?maxE) AS ?binnen )
  # leesbare grenzen: "≥ 6.5", "> 6.5", "≤ 9.0", "< 9.0"
  BIND ( COALESCE(CONCAT("≥ ", STR(?minI)), CONCAT("> ", STR(?minE)), "geen") AS ?ondergrens )
  BIND ( COALESCE(CONCAT("≤ ", STR(?maxI)), CONCAT("< ", STR(?maxE)), "geen") AS ?bovengrens )
  OPTIONAL { ?t sosa:hasInputValue ?bereik ; sosa:hasSimpleResult ?toets }
}
```

| parameteraspect | scope | ondergrens | bovengrens | gemeten | binnen | toets |
|---|---|---|---|---|---|---|
| pH (standaard in water): geen | VLAREM II, algemene lozingsvoorwaarden voor bedrijfsafvalwater in oppervlaktewater (illustratief) | ≥ 6.5 | ≤ 9.0 | 7.8 | true | true |

Getest met twee varianten van het bereik: met een exclusieve bovengrens `qudt:maxExclusive 7.8` wordt
`?binnen` onwaar (`< 7.8`), zonder ondergrens blijft het waar (`geen`).
