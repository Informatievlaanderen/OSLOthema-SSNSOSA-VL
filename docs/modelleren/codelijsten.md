# Codelijsten en registers

Veel waarden komen uit een lijst: een eigenschap, een eenheid, een status, een klasse, een
procedure, een matrix. In linked data is zo'n lijst een **SKOS-begrippenschema**, en elke waarde
een **begrip** met een eigen IRI.

## Eerst hergebruiken

1. **Bestaat er een register?** Vlaanderen beheert er veel: CSOR (parameters, eenheden, dragers),
   VHA (waterlopen), RIE-IEPR (inrichtingen), de VLAREM-indelingslijst, NACE-BEL
   (bedrijfsactiviteiten). Europese en internationale lijsten (QUDT-eenheden, INSPIRE-codelijsten)
   komen daarna. Verwijs naar hun begrippen.
2. **Pas dan een nieuwe lijst**, enkel voor waarden die geen register dekt, en enkel wanneer de
   mapping ze echt nodig heeft. Een codelijst is geen voorwaarde om resultaten te kunnen mappen.

```turtle
ex:waarneming sosa:observedProperty csor-parameteraspect:PAS_1789 .   # een begrip uit het register
ex:resultaat qudt:hasUnit csor-eenheid:E_131 .
```

## Een nieuwe lijst

```turtle
score:kansrijkheid a skos:ConceptScheme ;
    skos:prefLabel "Kansrijkheid peilgestuurde drainage"@nl .

score:kansrijk a skos:Concept ;
    skos:inScheme score:kansrijkheid ;
    skos:topConceptOf score:kansrijkheid ;
    skos:prefLabel "kansrijk"@nl ;
    skos:definition "…"@nl .
```

- elk begrip met `skos:prefLabel` en liefst `skos:definition`;
- `skos:inScheme` naar de lijst;
- een stabiele IRI onder een namespace van de beheerder.

## De data verwijst, het register beschrijft

!!! regel "Uitspraken over een begrip horen in het register"
    Data verwijst naar de IRI van een begrip. Ze kopieert het register niet en breidt het niet
    uit: labels, definities en mappings (`skos:exactMatch` naar QUDT, …) staan in het register,
    in zijn namespace. Ontbreekt een begrip of een mapping, dan is dat een vraag aan de beheerder.

Grote registers horen daarom niet tussen de datavoorbeelden. Is een lokaal uittreksel nodig
(voor documentatie), dan buiten de gevalideerde data. Een klein register waartegen de data
gecontroleerd moet worden (zoals de CSOR-eenheden), mag als vocabularium geladen worden.

## SKOS tussen begrippen, niet tussen klassen

SKOS-relaties (`skos:broader`, `skos:exactMatch`, …) zijn voor begrippen in codelijsten. Een
**klasse** is geen registerbegrip: klassen worden uitgelijnd met `rdfs:subClassOf` of OWL-axioma's,
of niet ([R15](../regels/r15.md)).

!!! valkuil "Eén IRI als klasse én als begrip"
    OGC HY_Features publiceert zijn featuretypes als `owl:Class` én als `skos:Concept`, met de
    hiërarchie enkel in `skos:broader`. Een redeneerder ziet dan geen subklassen; een mens twee
    betekenissen voor één IRI.

SKOS-documentatie-eigenschappen (`skos:definition`, `skos:scopeNote`, `skos:note`,
`skos:example`) mogen wel op klassen: SKOS geeft ze geen domein.

## Typeren: begrip of klasse?

De kernvocabularia zijn abstract: een systeem, een entiteit, een stap. De businesstaal (schouw,
huis, gaswasser, lozingspunt) komt erbij als **begrip**, met `dct:type` naar een codelijst, of als
**klasse**, een eigen subklasse met `rdf:type`. Vaak volstaat een begrip. Een klasse is nodig
zodra de soort eigen regels heeft: eigen eigenschappen, kardinaliteiten, of een eis zoals *een
emissieproces wordt uitgevoerd door een emissiepunt* ([R18](../regels/r18.md)).

Die keuze bepaalt de inhoud van de codelijst:

| Model | Typering | Wat in de codelijst staat |
|---|---|---|
| enkel abstracte klassen | `a sosa:System ; dct:type systeemtype:schouw` | alle soorten: schouw, installatie, emissiepunt, … |
| subklassen voor soorten met eigen regels | `a riepr:Emissiepunt , sosa:System ; dct:type emissiepunt-type:lozingspunt` | enkel de fijnere soorten binnen elke klasse |

```turtle
# abstract: de soort zit volledig in de codelijst
ex:schouw-12 a sosa:Platform ;
    dct:type platformtype:schouw .

# met subklassen: de klasse draagt de regels, het begrip verfijnt
ex:lozingspunt-LP01 a riepr:Emissiepunt , sosa:System ;
    dct:type emissiepunt-type:lozingspunt .
```

Een regel die aan een waarde van `dct:type` hangt, of een ontologie die begrippen uit een codelijst
kopieert om er regels aan te hangen, wijst op een begrip dat een klasse had moeten zijn. De
casus [RIE-IEPR](../casussen/riepr.md) toont beide, en de herziening.

## Een eigenschap als begrip

Een `sosa:Property` kan tegelijk een begrip uit een codelijst zijn. In CSOR is
`csor:ParameterAspect` een subklasse van `sosa:Property`, en elk parameteraspect een
`skos:Concept`. Dat is geen klasse-als-begrip: een parameteraspect is een individu (een
eigenschap), geen klasse van dingen.
