# Codelijsten en registers

Veel waarden komen uit een lijst: een eigenschap, een eenheid, een status, een klasse, een
procedure, een matrix. In linked data is zo'n lijst een **SKOS-begrippenschema**, en elke waarde
een **begrip** met een eigen IRI.

## Een abstracte kern, businesstaal erbij

SOSA, PROV-O en P-PLAN zijn bewust abstract. Ze kennen systemen, entiteiten, activiteiten,
procedures, stappen en variabelen, maar geen schouwen, lozingen of brownies. Dat is geen gemis:
precies daardoor passen ze op elk domein, en sluiten de domeinen op elkaar aan. Een vraag als
"welke waarnemingen hangen af van deze meting?" werkt in waterkwaliteit en in verkeer op dezelfde
manier, omdat beide dezelfde abstracte structuur gebruiken ([II. Samenhang](../samenhang/index.md)).

De businesstaal komt er pas bij, en op twee manieren:

- **in een codelijst**, als begrippen waarnaar de data verwijst. Dat is de gewone weg: het model
  blijft abstract, en de lijst kan groeien zonder dat het model verandert;
- **in een eigen ontologie**, als subklassen met eigen regels. Dat is de uitzondering, voor soorten
  die meer moeten dan een naam dragen ([Typeren: begrip of klasse?](#typeren-begrip-of-klasse)).

Waar de businesstaal terechtkomt, bepaalt wat er in de codelijsten staat. Wat in de ontologie als
klasse staat, hoort niet nog eens als begrip in een lijst.

## Waar begrippen in het model staan

Een begrip uit een codelijst kan op drie plaatsen staan:

- als **type**: `dct:type` zegt wat voor iets een resource is (een lozingspunt, een geleide
  emissie, een ingrediënt);
- als **waarde van een rol**: het begrip *is* de eigenschap, de eenheid of de procedure
  (`sosa:observedProperty`, `qudt:hasUnit`, `sosa:usedProcedure`);
- als **resultaat**: de uitkomst van een waarneming is zelf een begrip (een score, een klasse).

Over de lagen heen, met voorbeelden uit de casussen:

| Laag | Resource | Type (`dct:type`) | Waarde van een rol | Resultaat |
|---|---|---|---|---|
| plan | stap, procedure | soort proces zonder eigen regels: hoofdactiviteit, transport (voorzien in de ontologie van [RIE-IEPR](../casussen/riepr.md)); bepalingsmethode *berekend* op een procedure (RIE-IEPR) | | |
| plan | variabele | soort ingrediënt: `ingredient:butter` op `var:butter` ([Brownies](../casussen/brownies.md)) | | |
| inzet | systeem, platform | installatietype, emissiepunttype (RIE-IEPR); toesteltype en energiebron van een warmtepomp ([Energiemanagement](../casussen/ems.md)); meetputtype (voorstel bij [Waterkwaliteit](../casussen/waterkwaliteit.md)) | | |
| studieobject | emissie, staal | emissietype `riepr-emissie:geleide` (RIE-IEPR); matrix `matrix:afvalwater` (Waterkwaliteit) | | |
| uitvoering | waarneming | | eigenschap: een CSOR-parameteraspect (Waterkwaliteit, RIE-IEPR); procedure: een analysemethode, `procedure:WAC_I_A_003_2024` (Waterkwaliteit) | |
| uitvoering | resultaat | | eenheid: `qudt:hasUnit csor-eenheid:…` (Waterkwaliteit) | score of kansrijkheid: `rdf:value cl:kansrijkheid-kansrijk` ([Geschiktheidskaart PGD](../casussen/pgd.md)) |

Het patroon: **typen** staan vooral in plan, inzet en studieobject, waar dingen benoemd worden;
**rollen en resultaten** in de uitvoering, waar ze gemeten worden. Een activiteit krijgt zelden
een `dct:type`: wat ze doet, zegt haar procedure.

## Eerst hergebruiken

1. **Bestaat er een register?** Vlaanderen beheert er veel: CSOR (parameters, eenheden, dragers),
   VHA (waterlopen), RIE-IEPR (inrichtingen), de VLAREM-indelingslijst, NACE-BEL
   (bedrijfsactiviteiten). Europese en internationale lijsten (QUDT-eenheden, INSPIRE-codelijsten)
   komen daarna. Verwijs naar hun begrippen.
2. **Past het register bij je model?** Een register is opgesteld voor een bepaald model. Toets
   zijn granulariteit aan je klassen: bevat het soorten die jouw model als subklasse heeft, dan
   gebruik je die begrippen niet als type, enkel de fijnere ([Typeren: begrip of
   klasse?](#typeren-begrip-of-klasse)). Een register met de verkeerde granulariteit is een vraag
   aan de beheerder, geen reden om het te kopiëren.
3. **Pas dan een nieuwe lijst**, enkel voor waarden die geen register dekt, en enkel wanneer de
   mapping ze echt nodig heeft. Een codelijst is geen voorwaarde om resultaten te kunnen mappen.

```turtle
ex:waarneming sosa:observedProperty csor-parameteraspect:PAS_1789 .   # een begrip uit het register
ex:resultaat qudt:hasUnit csor-eenheid:E_131 .
```

## Een nieuwe lijst

**Eerst het model, dan de lijst.** Welke begrippen een lijst nodig heeft, hangt af van welke soorten
het model al als klasse kent. Stel de lijst dus op nadat de klassen vastliggen, en onderhoud
ontologie en lijst samen: een nieuwe subklasse kan begrippen overbodig maken, een klasse die
vervalt kan er nieuwe vragen.

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

De businesstaal (schouw, huis, gaswasser, lozingspunt) komt erbij als **begrip**, met `dct:type`
naar een codelijst, of als **klasse**, een eigen subklasse met `rdf:type`. Vaak volstaat een
begrip. Een klasse is nodig zodra de soort eigen regels heeft: eigen eigenschappen, kardinaliteiten, of een eis zoals *een
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
kopieert om er regels aan te hangen, wijst op een begrip dat een klasse had moeten zijn.

### Voorbeeld: de soorten processen van RIE-IEPR

De codelijst `procedure_type` van RIE-IEPR heeft zeven begrippen. Welke ervan het model nodig
heeft, hangt af van hoe het model processen typeert:

| Begrip in `procedure_type` | Ontvangen model: één klasse `riepr:Proces`, soort via `dct:type` | Herzien model: subklassen voor soorten met eigen regels |
|---|---|---|
| emissie | begrip (met een regel eraan gehangen) | klasse `riepr:Emissieproces`, uitgevoerd door een emissiepunt |
| verwerking | begrip (idem) | klasse `riepr:Verwerkingsproces`, uitgevoerd door een installatie |
| onttrekking | begrip (idem) | klasse `riepr:Onttrekkingsproces`, uitgevoerd door een onttrekkingspunt |
| meting | begrip (idem) | klasse `riepr:Meetproces`, uitgevoerd door een meetpunt |
| uitwissel | begrip (idem) | klasse `riepr:Uitwisselproces`, uitgevoerd door een uitwisselpunt |
| hoofdactiviteit | begrip | begrip (`dct:type`) |
| transport | begrip | begrip (`dct:type`) |

Het ontvangen model had alle zeven nodig, en hing aan vijf ervan toch een regel, in axioma's die
niet gecontroleerd werden. Het herziene model heeft er twee nodig. De andere vijf zeggen nu
hetzelfde als de klassen; of ze in de lijst blijven, voor andere gebruikers, is een vraag aan de
beheerder van de lijst ([casus RIE-IEPR](../casussen/riepr.md)).

## Een eigenschap als begrip

Een `sosa:Property` kan tegelijk een begrip uit een codelijst zijn. In CSOR is
`csor:ParameterAspect` een subklasse van `sosa:Property`, en elk parameteraspect een
`skos:Concept`. Dat is geen klasse-als-begrip: een parameteraspect is een individu (een
eigenschap), geen klasse van dingen.
