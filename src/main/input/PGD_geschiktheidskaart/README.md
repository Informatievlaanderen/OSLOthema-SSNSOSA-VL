# PGD_geschiktheidskaart — Geschiktheidskaart voor peilgestuurde drainage

## Bronbestand

Geschiktheidskaart voor peilgestuurde drainage (PGD) voor het Vlaams Gewest, opgesteld door de
Bodemkundige Dienst van België (BDB) in WP1 van het VLAIO-project OP-PEIL (versie augustus 2024).
De kaart schat per rastercel van 100 m x 100 m in hoe kansrijk peilgestuurde drainage is, op basis
van drie factoren: waterdoorlaatbaarheid van de bodem, grondwateraanvoer en helling.

- Kaart: [waterradar.be](https://waterradar.be/map) (Scenario's en kaarten > Andere kaarten >
  Peilgestuurde drainage geschiktheidskaart)
- Dataset (kaartlagen, opmaakbestanden, QGIS-modellen): Zenodo,
  DOI [10.5281/zenodo.17803699](https://doi.org/10.5281/zenodo.17803699)
- Ontvangen, in `source/`: `mail.txt` (aanbod van het datavoorbeeld voor de OSLO-werkgroep) en
  `WP1_PGDkaart_technischefiche.pdf` (technische fiche met inputlagen en beoordelingsregels)

## Transformatieproces

Geen. De Turtle is met de hand opgesteld uit de technische fiche. Het voorbeeld beschrijft één
illustratieve rastercel; de waarden zijn niet uit het raster op Zenodo gelezen.

## Mapping-keuzes

**Architectuur: drielaags (Planning / Deployment / Execution).**

De kaart is het resultaat van een meerstapsproces: drie factorscores, elk uit een andere
kaartlaag, en een beslissingsmodel dat ze combineert (R4a). Twee QGIS-modellen, voor
Binnen-Vlaanderen en voor de poldergebieden, delen de stappen voor de helling en de samengestelde
score (R4b), en de herkomst van elke cel moet tot het plan te herleiden zijn (R4c).

- **Planning:** twee `p-plan:Plan`'s (één per QGIS-model) met hun stappen en variabelen.
- **Deployment:** de QGIS-modellen als `sosa:Sensor`; de uitvoering voor Binnen-Vlaanderen als
  `sosa:Deployment`, met de gebruikte kaartlagen en het gegenereerde raster als `prov:Entity`.
- **Execution:** per factor een `sosa:Observation` van de rastercel (een `sosa:SpatialSample`
  van Binnen-Vlaanderen), en een afgeleide observatie voor de kansrijkheid (R13). Scores en
  kansrijkheid verwijzen naar twee kleine SKOS-codelijsten.

## Grafische voorstelling

Zie `pgd-geschiktheidskaart.mmd`.

## Gebruik

Valideren: `mcp__ld-vocab__validate_file` op
`src/main/input/PGD_geschiktheidskaart/pgd-geschiktheidskaart.ttl`, of zonder MCP-client:

```bash
java -jar tools/ld-mcp-vocab.jar validate --ontologies src/main/resources \
    --rules src/main/resources/be/vlaanderen/ssnsosa/data/id/rule/domain-range-subproperty.rules \
    --generate-shapes --shapes oslo-ld-kit/rules/ssn-sosa-rules.ttl \
    --prefix-registry src/main/cc/prefix/prefix.cc.ttl --extensions ttl \
    src/main/input/PGD_geschiktheidskaart
```
