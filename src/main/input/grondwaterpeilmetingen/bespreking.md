# Grondwaterpeilmeting gemodelleerd in SOSA/SSN

## 1. Wat stelt dit diagram voor?

Het diagram toont één veldronde van grondwatermetingen op **20 oktober 2006** bij grondwaterfilter
`2005-007247` in DOV (Databank Ondergrond Vlaanderen).

De put en filter zijn terug te vinden via:
<https://www.dov.vlaanderen.be/data/filter/2005-007247>

De modellering gebruikt het **SOSA/SSN**-vocabularium (Sensor, Observations, Samples and Actuators /
Semantic Sensor Network) – een W3C-standaard voor het beschrijven van observaties, sensoren en
meetprocedures.

---

## 2. Kleurlegenda

| Kleur | SOSA-concept | Betekenis in DOV-context |
|-------|-------------|--------------------------|
| **Blauw** (#60c4e4) | Platform, System, Sensor | Infrastructuur: put, filter, beheerder |
| **Roze** (#e54b89) | ObservationCollection, Observation | De peilmeting zelf en haar deelwaarnemingen |
| **Oranje** (#f8b622) | Result, time:Instant | Gemeten waarden en het meetmoment |

---

## 3. Infrastructuur (blauwe nodes)

De fysieke infrastructuur wordt uitgedrukt met drie SOSA-klassen:

**`put:2017-003450`** — de grondwaterput — krijgt een dubbele typering:
- `sosa:Platform`: de put *herbergt* de filter (`sosa:hosts filter:2005-007247`)
- `sosa:FeatureOfInterest`: de put *is zelf ook onderwerp van meting* (peil en diepte worden ten
  opzichte van de put gemeten)

**`filter:2005-007247`** — het grondwaterfilter — is een `sosa:System` met drie sub-systemen, en
ook een `sosa:FeatureOfInterest`: filterstatus en filtertoestand zijn waarnemingen over de filter:
- `/zandvang` (van 26 m tot 27 m)
- `/filter` (van 24 m tot 26 m, materiaal: pvc)
- `/stijgbuis` (van 0 m tot 24 m, materiaal: pvc)

Al deze sub-systemen zijn verbonden via `sosa:hasSubSystem` / `sosa:isSubSystemOf`.

**`agent:Beheerder`** — de medewerker die de metingen uitvoert — is gemodelleerd als `sosa:Sensor`.
Dat klinkt technisch, maar SOSA staat dit toe: een persoon die systematisch meetprocedures toepast,
vervult de rol van sensor. Via `sosa:implements` is vastgelegd welke procedures de beheerder uitvoert.

---

## 4. Peilmeting als ObservationCollection (roze nodes)

Eén veldronde op 20 oktober 2006 bestaat uit **vijf afzonderlijke waarnemingen**, gebundeld in:

```
ex:peilmeting_2006-10-20  a sosa:ObservationCollection
```

**Gedeelde metadata** (éénmaal op collection-niveau, niet herhaald per observatie):
- `sosa:madeBySensor agent:Beheerder`
- `sosa:phenomenonTime` → `time:Instant` met `time:inXSDDate "2006-10-20"`
- `sosa:hasFeatureOfInterest put:2017-003450, filter:2005-007247`

### De vijf observaties

| Observatie-IRI | Gemeten eigenschap | Procedure | Resultaat | FOI |
|---|---|---|---|---|
| `…zoet` | `ex:zoet` | `ex:smaaktest` | `"N"` | put |
| `…filterstatus` | `ex:filterstatus` | `ex:visuele_controle` | `"in rust"` | filter |
| `…filtertoestand` | `ex:filtertoestand` | `ex:visueel_methode` | `1` | filter |
| `…peil_mtaw` | `ex:peil_mtaw` | `ex:peillint_methode` | `7.53 m` | put |
| `…diepte_tov_referentiepunt` | `ex:diepte_tov_referentiepunt` | `ex:peillint_methode` | `2.25 m` | put |

Elk resultaat is een apart object: een `qudt:QuantityValue` voor meetwaarden met een eenheid (peil
en diepte, met `qudt:numericValue` en `qudt:hasUnit unit:M`), een `prov:Entity` met `rdf:value` voor de andere (smaak, filterstatus,
filtertoestand). Niet `sosa:Result`: dat is in SSN/SOSA 2023 `owl:deprecated` (R3).

---

## 5. Modelleer-keuzes toegelicht

### Waarom ObservationCollection?

Vijf metingen op dezelfde dag, door dezelfde beheerder, op hetzelfde object vormen logisch één
veldronde. Door ze te bundelen in een `sosa:ObservationCollection` vermijden we herhaling van
gedeelde metadata en maken we de samenhang expliciet. Optioneel kan, voor systemen die de collectie niet begrijpen,
voor iedere observatie alle relaties en eigenschappen redundant herhaald worden.


### Resultaat als apart object

In plaats van een eenvoudige waarde is elk resultaat een object (een `qudt:QuantityValue` als er
een eenheid is). Dit maakt het mogelijk om naast de waarde ook eenheid, onzekerheid of provenance
toe te voegen:

```turtle
sosa:hasResult [
    a qudt:QuantityValue ;
    qudt:numericValue 7.53 ;
    qudt:hasUnit unit:M
]
```

### Procedures als herbruikbare objecten

`ex:smaaktest`, `ex:visuele_controle`, `ex:visueel_methode` en `ex:peillint_methode` zijn getypeerd
als `sosa:ObservingProcedure`. Ze worden door de beheerder geïmplementeerd (`sosa:implements`) en
door elke observatie gebruikt (`sosa:usedProcedure`). Zo kunnen meerdere metingen naar dezelfde
gestandaardiseerde procedure verwijzen.

---

## 6. Technische noot 

### Prefixen en IRI-structuur

De IRI-structuur weerspiegelt de DOV-organisatie:
- `put:` → `https://www.dov.vlaanderen.be/data/put/`
- `filter:` → `https://www.dov.vlaanderen.be/data/filter/`
- `agent:` → `http://example.org/agent/` (tijdelijk voorbeeld-prefix)
- `ex:` → `http://example.org/` (tijdelijk voorbeeld-prefix voor observaties en eigenschappen)

### Inverse relaties

De modellering gebruikt zowel de voorwaartse als de inverse richting expliciet:
- `put:2017-003450 sosa:hosts filter:2005-007247`
- `filter:2005-007247 sosa:isHostedBy put:2017-003450`

Hetzelfde geldt voor `sosa:hasFeatureOfInterest` (op observatie) en `sosa:isFeatureOfInterestOf`
(op de put en filter). Beide richtingen zijn in de Turtle opgenomen voor query-efficiëntie.


