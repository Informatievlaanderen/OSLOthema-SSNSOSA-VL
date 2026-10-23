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

## Een eigenschap als begrip

Een `sosa:Property` kan tegelijk een begrip uit een codelijst zijn. In CSOR is
`csor:ParameterAspect` een subklasse van `sosa:Property`, en elk parameteraspect een
`skos:Concept`. Dat is geen klasse-als-begrip: een parameteraspect is een individu (een
eigenschap), geen klasse van dingen.
