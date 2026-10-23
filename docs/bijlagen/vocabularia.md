# Geladen vocabularia

Een vocabularium wordt in dit project pas gebruikt nadat het geladen is, met bron en versie, en
nadat alle voorbeelden ermee nog consistent zijn ([R17](../regels/r17.md)). Ze staan in
[`src/main/resources/`](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/tree/main/src/main/resources),
in een map die het domein van de namespace volgt.

## Kern

| Vocabularium | Bestand | Versie / bron |
|---|---|---|
| SSN/SOSA 2023 | `org/w3/www/ns/sosa/ssn-sosa_2023.ttl` | samengevoegd uit `w3c/sdw-sosa-ssn` |
| SOSA–PROV-alignment | `org/w3/www/ns/sosa/alignments/sosa-prov.ttl` | `w3c/sdw-sosa-ssn`, commit van 2026-10-21 (met `hasInputValue ⊂ prov:used`) |
| SOSA–SAREF-alignment | `org/w3/www/ns/sosa/alignments/sosa-saref.ttl` | `w3c/sdw-sosa-ssn` |
| PROV-O | `org/w3/www/ns/prov/prov-o.ttl` | W3C |
| P-PLAN | `org/purl/net/p-plan/p-plan.ttl` | purl.org/net/p-plan |
| P-PLAN–SOSA-alignment | `ontologies/pplan-sosa.ttl` | dit project |
| Nederlandse labels (SOSA, PROV-O, P-PLAN, GeoSPARQL) | `ontologies/ssn-sosa-fullprov-o-p-plan-geosparql-dbo.ttl` | vertaling in dit project |
| QUDT schema en eenheden | `org/qudt/…`, `qudt/…` | 3.5.2 |
| OWL-Time | `org/w3/www/2006/time/time.ttl` | W3C |
| GeoSPARQL | in het bestand met Nederlandse labels | 1.0 |
| SKOS | `org/w3/www/2004/02/skos/core/skos.ttl` | W3C |
| DCTERMS | `org/purl/dc/terms/dcterms.ttl` | DCMI |

## Registers en Vlaamse vocabularia

| Vocabularium | Bestand | Gebruik |
|---|---|---|
| CSOR-vocabularium | `be/vlaanderen/omgeving/data/ns/csor/csor.ttl` | klassen van het register (`csor:ParameterAspect ⊂ sosa:Property`, `csor:Eenheid`) |
| CSOR-eenheden | `be/vlaanderen/omgeving/data/id/conceptscheme/csor/eenheid/eenheid.ttl` | 360 eenheden, 163 met een QUDT-mapping |
| Waterkwaliteit | `be/vlaanderen/data/ns/waterkwaliteit/waterkwaliteit.ttl` | ontwerp: ontologie en bron van het toepassingsprofiel |
| Waterlopen | `be/vlaanderen/omgeving/data/ns/waterlopen/waterlopen.ttl` | klassen voor VHA-waterlopen |
| VLAREM-rubrieken | `be/vlaanderen/omgeving/data/ns/vlaremrubrieken/vlaremrubrieken.ttl` | ontwerpvocabularium `vlarem:` |
| Vergelijkingsoperatoren | `be/vlaanderen/omgeving/data/id/conceptscheme/vergelijkingsoperator/vergelijkingsoperator.ttl` | nieuwe SKOS-lijst |
| Gebouw | `be/vlaanderen/data/ns/gebouw/gebouw.ttl` | OSLO-gebouw (energiemanagement) |

## Andere

| Vocabularium | Bestand | Gebruik |
|---|---|---|
| SAREF core, SAREF4SYST | `org/etsi/saref/…` | energiemanagement; fabrikant van een toestel |
| ADMS | `org/w3/www/ns/adms/adms.ttl` | identificaties, beheerstatus |
| W3C Organization | `org/w3/www/ns/org/org.ttl` | organisaties |
| LOCN | `org/w3/www/ns/locn/…` | adressen |
| IT6 | `eu/europa/data/it6/it6.ttl` | `it6:MachineLearningModel` |
| Web Annotation, DQV, WAC | `org/w3/www/ns/oa/`, `dqv/`, `auth/acl/` | geheugen van een AI-agent (`rdf-memory`) |
| DBpedia-ontologie | `org/dbpedia/ontology/dbo.ttl` | |
| schema.org (enkele termen) | `org/schema/…` | `QuantitativeValue`, `unitCode`, `value`, voor vergelijking |

## Wat er niet bij hoort

Grote registers (alle CSOR-parameters, NACE-BEL) staan niet als vocabularium geladen: ze worden
enkel waar nodig als uittreksel gebruikt, buiten de gevalideerde data
([Codelijsten en registers](../modelleren/codelijsten.md)).
