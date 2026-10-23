# Prefixen

De Turtle-fragmenten in dit werk laten de prefixen weg. Dit zijn ze.

## Kern

```turtle
@prefix sosa:   <http://www.w3.org/ns/sosa/> .
@prefix ssn:    <http://www.w3.org/ns/ssn/> .
@prefix prov:   <http://www.w3.org/ns/prov#> .
@prefix p-plan: <http://purl.org/net/p-plan#> .
@prefix time:   <http://www.w3.org/2006/time#> .
@prefix qudt:   <http://qudt.org/schema/qudt/> .
@prefix unit:   <http://qudt.org/vocab/unit/> .
@prefix geo:    <http://www.opengis.net/ont/geosparql#> .
@prefix skos:   <http://www.w3.org/2004/02/skos/core#> .
@prefix dct:    <http://purl.org/dc/terms/> .
@prefix rdf:    <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs:   <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl:    <http://www.w3.org/2002/07/owl#> .
@prefix xsd:    <http://www.w3.org/2001/XMLSchema#> .
```

- `qudt:` voor schematermen (`qudt:QuantityValue`, `qudt:hasUnit`, `qudt:numericValue`), `unit:`
  voor eenheden (`unit:M`, `unit:PPM`).
- `geo:` is GeoSPARQL, niet het oudere WGS84 Basic Geo.
- `ssn:` enkel voor termen die nog in SSN staan; de verhuisde termen gebruiken `sosa:`
  ([R14](../regels/r14.md)).
- Alles is `http`, niet `https`: zo definiëren de uitgevers hun termen.

## Registers en Vlaamse vocabularia

```turtle
@prefix csor:                 <https://data.omgeving.vlaanderen.be/ns/csor#> .
@prefix csor-eenheid:         <https://data.omgeving.vlaanderen.be/id/concept/csor/eenheid/> .
@prefix csor-parameteraspect: <https://data.omgeving.vlaanderen.be/id/concept/csor/parameteraspect/> .
@prefix wk:                   <https://data.vlaanderen.be/ns/waterkwaliteit#> .
```

## Andere

```turtle
@prefix adms:   <http://www.w3.org/ns/adms#> .
@prefix foaf:   <http://xmlns.com/foaf/0.1/> .
@prefix saref:  <https://saref.etsi.org/core/> .
@prefix s4syst: <https://saref.etsi.org/saref4syst/> .
@prefix it6:    <http://data.europa.eu/it6/> .
@prefix iadopt: <https://w3id.org/iadopt/ont/> .
```

## Voorbeelden

Illustratieve resources gebruiken deelpaden van `https://example.org/`
([R10](../regels/r10.md)):

```turtle
@prefix ex:     <https://example.org/<domein>/> .
```

Drielaagse voorbeelden geven elke laag een eigen prefix:

```turtle
@prefix plan:   <https://example.org/<domein>/plan/> .
@prefix step:   <https://example.org/<domein>/step/> .
@prefix var:    <https://example.org/<domein>/var/> .
@prefix exec:   <https://example.org/<domein>/exec/> .
@prefix ent:    <https://example.org/<domein>/ent/> .
@prefix inst:   <https://example.org/<domein>/inst/> .
@prefix prop:   <https://example.org/<domein>/prop/> .
```

Gedeelde infrastructuur die in meerdere voorbeelden terugkomt, krijgt een eigen prefix, bv.
`htg:` voor het Herman Teirlinckgebouw.
