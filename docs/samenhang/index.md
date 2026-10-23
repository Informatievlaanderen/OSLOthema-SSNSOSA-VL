# II. Samenhang: hoe de vocabularia op elkaar aansluiten

Zes vocabularia naast elkaar zijn nog geen model. Ze worden er een door **alignments**: uitspraken
die een begrip van het ene vocabularium verbinden met een begrip van het andere. *Een waarneming
is een PROV-activiteit.* *Het resultaat van een waarneming wordt door die waarneming gegenereerd.*
*Een stap uit een plan is een procedure.* Dit hoofdstuk is het hart van het werk: wie de
alignments begrijpt, begrijpt waarom de [regels](../regels/index.md) zijn wat ze zijn.

## Overzicht

```mermaid
flowchart LR
    subgraph KERN["Kern"]
        sosa["SOSA/SSN 2023"]
        prov["PROV-O"]
        pplan["P-PLAN"]
        qudt["QUDT"]
        geo["GeoSPARQL"]
        time["OWL-Time"]
    end
    subgraph REG["Registers en domeinmodellen"]
        csor["CSOR-eenheden"]
        csorp["CSOR-parameteraspecten"]
        iadopt["I-ADOPT"]
        saref["SAREF / SAREF4SYST"]
    end

    sosa ==>|"sosa-prov · W3C"| prov
    pplan ==>|"pplan-sosa · dit project"| sosa
    pplan ==>|"P-PLAN zelf"| prov
    sosa -.->|"patroon R3"| qudt
    sosa -.->|"patroon R11"| geo
    sosa -.->|"bereik + patroon R12"| time
    csor -.->|"skos:exactMatch · register"| qudt
    csorp -.->|"voorstel"| iadopt
    csorp ==>|"⊂ sosa:Property"| sosa
    sosa ==>|"sosa-saref · W3C"| saref

    style KERN fill:#e7a3be,stroke:#2E5C8A,color:#000
    style REG fill:#b0d9e7,stroke:#2E5C8A,color:#000
    style sosa fill:#e54b89,stroke:#2E5C8A,color:#fff
    style prov fill:#e54b89,stroke:#2E5C8A,color:#fff
    style pplan fill:#7f59ae,stroke:#2E5C8A,color:#fff
    style qudt fill:#f8b622,stroke:#2E5C8A,color:#000
    style geo fill:#f8b622,stroke:#2E5C8A,color:#000
    style time fill:#f8b622,stroke:#2E5C8A,color:#000
    style csor fill:#60c4e4,stroke:#2E5C8A,color:#000
    style csorp fill:#60c4e4,stroke:#2E5C8A,color:#000
    style iadopt fill:#60c4e4,stroke:#2E5C8A,color:#000
    style saref fill:#60c4e4,stroke:#2E5C8A,color:#000
```

Een **dikke pijl** is een formele uitlijning: OWL-axioma's in een gepubliceerd bestand, die een
redeneerder kan gebruiken. Een **stippellijn** is een afspraak: de vocabularia passen samen, maar
de koppeling ligt in de manier waarop je ze gebruikt, niet in een axioma.

| Hoofdstuk | Soort | Kern | Gepubliceerd door |
|---|---|---|---|
| [SOSA en PROV-O](sosa-prov.md) | formeel | uitvoeringen zijn activiteiten; studieobjecten, monsters, eigenschappen en platformen zijn entiteiten; het resultaat wordt gegenereerd, het studieobject en de inputwaarde gebruikt | W3C (module `sosa-prov` van SSN/SOSA 2023) |
| [P-PLAN en SOSA](pplan-sosa.md) | formeel | plannen en stappen zijn procedures; ketens van variabelen naar procedure | dit project (`pplan-sosa.ttl`) |
| [SOSA en QUDT](sosa-qudt.md) | afspraak | het resultaat is een `qudt:QuantityValue` met getal en eenheid | regel R3 |
| [SOSA en GeoSPARQL](sosa-geosparql.md) | afspraak, met een domein | een studieobject met een plaats is een `geo:Feature` met een geometrie | regel R11 |
| [SOSA en OWL-Time](sosa-time.md) | bereik en afspraak | de fenomeentijd is een OWL-Time-entiteit: tijdstip of interval | SOSA (bereik), regel R12 |
| [Register en QUDT](register-qudt.md) | mapping in het register | een CSOR-eenheid verwijst met `skos:exactMatch` naar een QUDT-eenheid | het register (CSOR) |
| [Register en I-ADOPT](register-iadopt.md) | voorstel | een parameteraspect is een I-ADOPT-variabele | analyse in dit project |
| [SOSA en SAREF](sosa-saref.md) | formeel | systemen, eigenschappen, uitvoeringen gelijkgesteld met SAREF | W3C (module `sosa-saref`) |

## Een alignment lezen

Een alignment bestaat uit een handvol soorten axioma's. Elk heeft een eigen gevolg.

| Axioma | Voorbeeld | Wat een redeneerder eruit afleidt |
|---|---|---|
| `rdfs:subClassOf` | `sosa:Observation rdfs:subClassOf prov:Activity` | elke waarneming is ook een activiteit; een PROV-query vindt ze |
| `rdfs:subPropertyOf` | `sosa:hasResult rdfs:subPropertyOf prov:generated` | uit *waarneming heeft resultaat r* volgt *waarneming genereerde r*, met domein en bereik van `prov:generated` erbij |
| `owl:equivalentClass` / `owl:equivalentProperty` | `sosa:Observation owl:equivalentClass saref:Observation` | beide namen zijn uitwisselbaar |
| `owl:propertyChainAxiom` | `sosa:usedProcedure` ← `p-plan:correspondsToStep` ∘ `p-plan:isDecomposedAsPlan` | een eigenschap volgt uit een pad van andere |
| `owl:disjointWith` | `prov:Activity owl:disjointWith prov:Entity` | niets is beide; een resource die beide wordt, maakt het model **inconsistent** |

Het laatste axioma is wat alignments zo waardevol maakt. Een subklasse of subproperty voegt
afgeleide feiten toe; samen met een disjunctie maakt ze **fouten aantoonbaar**. Wie een waarneming
als inputwaarde van een andere waarneming opgeeft, maakt ze via de alignment tot entiteit, terwijl
ze als waarneming een activiteit is. Dat is een tegenspraak, geen kwestie van smaak.

!!! hulpmiddel "Afgeleide feiten zichtbaar maken"
    Een redeneerder met regels voor domein, bereik, subklasse en subproperty (RDFS-niveau) volstaat
    voor de meeste gevolgen in dit hoofdstuk; samen met een controle op disjuncte klassen vindt hij
    de fouten. Ketens van eigenschappen (`owl:propertyChainAxiom`) vragen een OWL 2 RL- of
    DL-redeneerder. De [bijlage Hulpmiddelen](../bijlagen/hulpmiddelen.md) toont hoe de validatie in
    dit project dat doet.

## Wat een alignment niet doet

- **Het verplicht niets.** OWL is open: dat een waarneming een activiteit *is*, betekent niet dat
  je ze ook zo moet typeren, en een ontbrekende eigenschap is in OWL nooit een fout. Verplichtingen
  komen uit een toepassingsprofiel (SHACL), niet uit een alignment.
- **Het staat niet altijd in een van beide vocabularia.** De uitlijning van SOSA met SAREF is een
  aparte module van SSN/SOSA 2023, niet van SAREF; het register van Linked Open Vocabularies kent
  ze niet. Afwezigheid in een vocabularium bewijst dus niet dat er geen alignment is
  ([Een alignment vinden en beoordelen](alignment-vinden.md)).
- **Het is niet altijd normatief.** De PROV-module van SSN/SOSA 2023 is een niet-normatieve
  bijlage van de specificatie. Ze wordt in dit werk toch als fundament gebruikt, omdat ze de
  lezing vastlegt die de definities van SOSA zelf al maken.
