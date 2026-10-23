# Hulpmiddelen

Alles in dit werk kan met pen en papier. Hulpmiddelen maken het sneller en vangen fouten die een
mens mist. Deze bijlage beschrijft wat dit project gebruikt, en toont het op een voorbeeld.

## De validatieserver `ld-vocab`

[`milieuinfo/ld-mcp`](https://github.com/milieuinfo/ld-mcp) is een open-sourcehulpmiddel dat de
geladen vocabularia, de regels en de alignments van dit project kent. Het werkt op twee manieren:

- als **MCP-server** voor een AI-assistent (Claude Code en andere MCP-clients): opzoeken, zoeken en
  valideren tijdens het modelleren;
- als **opdrachtregelprogramma**, voor één bestand of alle voorbeelden in één keer, ook in een
  automatische controle.

Het vraagt Java 21 of later; de jar staat op de
[releasepagina](https://github.com/milieuinfo/ld-mcp/releases/latest).

### Wat het controleert

| Stap | Wat | Wat je ermee doet |
|---|---|---|
| `[VOCAB]` | bestaat elke term in het vocabularium dat hij noemt? juiste rol (klasse of eigenschap), datatype, niet verouderd, niet gemunt in een vreemde namespace? | elke `[error]` oplossen; elke `[suspect]` nakijken (vaak `http`/`https` of `#`/`/` in een prefix) |
| `[INFERENCE]` | afleidingen uit domein, bereik en subproperties | (informatief) |
| `[DISJOINTNESS]` | na afleiding: een resource in twee disjuncte klassen, zoals activiteit en entiteit | oplossen; hier wordt de [kaart](../kaart/index.md) een controle |
| `[SHACL]` | de regels van de kit (R2, R3, R5, R7 …) en de vormen die uit de OWL-restricties gegenereerd worden | elke schending oplossen; een `[warning]` mag blijven als de bron de informatie niet heeft, vermeld in de bespreking |

### Een voorbeeld

Een bestand met drie fouten: `qudt:unit` in plaats van `qudt:hasUnit`, een dagsom die naar een
**waarneming** verwijst als inputwaarde, en studieobject en eigenschap zonder type.

```turtle
ex:uurtelling-08 a sosa:Observation ;
    sosa:hasFeatureOfInterest ex:meetpunt ;
    sosa:observedProperty ex:verkeersintensiteit ;
    sosa:hasResult [ a qudt:QuantityValue ; qudt:numericValue 214 ; qudt:unit unit:NUM ] .

ex:dagsom a sosa:Observation ;
    sosa:hasFeatureOfInterest ex:meetpunt ;
    sosa:observedProperty ex:verkeersintensiteit ;
    sosa:hasInputValue ex:uurtelling-08 ;
    sosa:hasResult [ a qudt:QuantityValue ; qudt:numericValue 2541 ; qudt:hasUnit unit:NUM ] .
```

Het rapport (ingekort):

```text
[VOCAB] 1 error(s), 0 suspect, 0 hint(s)
- [error] Unknown property: http://qudt.org/schema/qudt/unit
    Same local name in another namespace: qudt:Unit

[INFERENCE] 100 inferred triples

[DISJOINTNESS] 1 violation(s)
- ex:uurtelling-08 is a http://www.w3.org/ns/prov#Activity (as a sosa:Observation)
  and a http://www.w3.org/ns/prov#Entity, which are disjoint classes

[SHACL] 9 violation(s), 4 warning(s) (13 of 174 shapes applied to 4 focus node(s) …)
- ex:uurtelling-08 — R7: sosa:hasInputValue points to a value (a result), not to an
  observation, collection or activity; use sosa:relatedObservation for those.
- ex:dagsom path: sosa:hasFeatureOfInterest — sosa:Observation: sosa:hasFeatureOfInterest
  needs every value is a sosa:FeatureOfInterest (generated from the OWL restrictions)
  (value: ex:meetpunt)
- ex:dagsom path: sosa:observedProperty — … needs every value is a sosa:Property …
- [warning] ex:dagsom — R2: sosa:madeBySensor is strongly recommended …
- [warning] ex:dagsom — R2: sosa:usedProcedure is strongly recommended …
```

Wat het zegt:

1. **`qudt:unit` bestaat niet** ([R3](../regels/r03.md)).
2. **De uurtelling is tegelijk activiteit en entiteit.** Ze is een waarneming (activiteit), en via
   `sosa:hasInputValue ⊂ prov:used` ook een entiteit. Dat is de alignment
   [SOSA en PROV-O](../kaart/sosa-prov.md) aan het werk. De regel R7 zegt het in mensentaal.
3. **Het meetpunt en de eigenschap hebben geen type.** SHACL ziet enkel wat er staat (plus de
   klassehiërarchie), niet wat een redeneerder zou afleiden. Type het studieobject en de eigenschap
   daarom expliciet. Zo blijft de data ook geldig voor een validator die niets afleidt.
4. **Sensor en procedure ontbreken**: een waarschuwing, geen fout ([R2](../regels/r02.md)).

### Alle voorbeelden in één keer

```bash
java -jar tools/ld-mcp-vocab.jar validate --ontologies src/main/resources \
    --rules src/main/resources/be/vlaanderen/ssnsosa/data/id/rule/domain-range-subproperty.rules \
    --generate-shapes --shapes oslo-ld-kit/rules/ssn-sosa-rules.ttl \
    --prefix-registry src/main/cc/prefix/prefix.cc.ttl --extensions ttl src/main/input
```

Exitcode 0 zonder fouten, 1 met fouten. `--extensions ttl` slaat de `.trig`-bestanden over
(ontvangen bronbestanden en volledige datasets). Dezelfde opdracht draait bij elke publicatie van
deze site: faalt ze, dan wordt de site niet bijgewerkt.

### Opzoeken en zoeken

Naast valideren kan de server een term opzoeken (type, labels, definitie, superklassen, domein,
bereik, SKOS-mappings van registerbegrippen) en termen zoeken op naam of label, ook eenheden.
Twee functies helpen bij [R17](../regels/r17.md): een zoekopdracht in Linked Open Vocabularies en
een profiel van een kandidaat-vocabularium (opvraagbaarheid, versie, licentie, gekende alignments).
Ze verzamelen feiten; kiezen doe je zelf.

## Werkwijzen als skills

De trajecten van [VI. Werkwijze](../werkwijze/index.md) bestaan ook als *skills* voor Claude Code,
in de kit [`milieuinfo/oslo-ld-kit`](https://github.com/milieuinfo/oslo-ld-kit/tree/main/skills):

| Skill | Traject |
|---|---|
| `new-example` | een nieuw voorbeeld: stappen 1–7 |
| `revise-mapping` | [een mapping herzien](../werkwijze/herzien.md) |
| `alternative-mapping` | [een alternatief uitwerken](../werkwijze/alternatief.md) |
| `map-source-data` | [brondata in fases mappen](../werkwijze/brondata.md) |
| `design-ontology` | [ontologie en toepassingsprofiel](../werkwijze/ontologie.md) |
| `align-ontologies` | [ontologieën aligneren](../werkwijze/aligneren.md) |
| `decision-document` | [het beslisdocument](../werkwijze/beslisdocument.md) |

Een skill volgt dezelfde regels en dezelfde stappen als een mens; het verschil is de snelheid.
Het oordeel (welke lezing, welk vocabularium, welk patroon) blijft bij de modelleerder en de
werkgroep.

## Ander gereedschap

| Hulpmiddel | Gebruik in de voorbeelden |
|---|---|
| [Apache Jena](https://jena.apache.org/) (`riot`, `sparql`, `shacl`) | omzetten tussen formaten, syntaxis controleren, queries, SHACL |
| XSLT (`xsltproc`) | XML-bronnen omzetten ([grondwaterpeilmetingen](../casussen/grondwaterpeilmetingen.md)) |
| Python, R | omzettingsscripts ([waterkwaliteit](../casussen/waterkwaliteit.md), [r-factor](../casussen/r-factor.md), [geluidsmeetnet](../casussen/geluidsmeetnet.md)) |
| [Mermaid](https://mermaid.js.org/) | diagrammen; te bekijken in de [Mermaid Live Editor](https://mermaid.live/) |
