# Grondwaterpeilmetingen

*Een veldronde van grondwatermetingen bij een filter uit de Databank Ondergrond Vlaanderen (DOV),
omgezet uit XML met XSLT.*

| | |
|---|---|
| **Domein** | grondwater, DOV |
| **Model** | plat, met een collectie per veldronde |
| **Bron** | XML-export van DOV; filter [2005-007247](https://www.dov.vlaanderen.be/data/filter/2005-007247) |
| **Transformatie** | XSLT naar RDF/XML, daarna Apache Jena `riot` naar Turtle, een SPARQL-query naar CSV |
| **Bestanden** | [README](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/grondwaterpeilmetingen/README.md) · [bespreking](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/grondwaterpeilmetingen/bespreking.md) · [XSLT](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/grondwaterpeilmetingen/bash/transformatie.xslt) |

## Waarom deze casus

Het oudste voorbeeld van het project, en het enige met een productiebron (DOV) en een
gezaghebbende IRI-basis (`https://www.dov.vlaanderen.be/data/…`). Het toont een volledige
omzettingsketen met standaardgereedschap: XSLT, `riot`, SPARQL.

## De keuzes

- **De put is platform én studieobject**: ze herbergt de filter, en peil en diepte worden
  tegenover de put gemeten ([R1](../regels/r01.md)).
- **De filter is een systeem met drie deelsystemen** (zandvang, filter, stijgbuis), elk met hun
  diepte en materiaal (`sosa:hasSubSystem`).
- **De beheerder is een sensor**: een persoon die systematisch meetprocedures toepast.
- **Vijf waarnemingen in één collectie** (veldronde van 20 oktober 2006): zoet, filterstatus,
  filtertoestand, peil (mTAW) en diepte tegenover het referentiepunt. Sensor, datum en
  studieobject staan op de collectie.
- **Elk resultaat een object**: een grootheidswaarde voor peil en diepte, een entiteit voor de
  kwalitatieve waarden.
- **De filter is ook een studieobject**: filterstatus en filtertoestand zijn waarnemingen over de
  filter, dus de filter is `sosa:System` én `sosa:FeatureOfInterest`.

## Diagram

```mermaid
--8<-- "src/main/input/grondwaterpeilmetingen/grondwaterpeilmetingen.mmd"
```
