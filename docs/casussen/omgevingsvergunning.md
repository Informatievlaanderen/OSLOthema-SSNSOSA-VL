# Omgevingsvergunning

*De gewone vergunningsprocedure als plan met procedurestappen, gekoppeld aan de dienst en het
product uit de producten- en dienstencatalogus, met een fictief dossier dat haar uitvoert.*

| | |
|---|---|
| **Domein** | omgevingsvergunning; procedures en publieke dienstverlening |
| **Model** | drielaags, zonder deploymentlaag |
| **Bron** | Omgevingsvergunningsdecreet (art. 18-36), [AP Omgevingsvergunning](https://data.vlaanderen.be/doc/applicatieprofiel/omgevingsvergunning/), PDC van het Departement Omgeving (CPSV-AP) |
| **Bestanden** | [README met verbeterpunten](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/omgevingsvergunning/README.md) · [bespreking](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/omgevingsvergunning/bespreking.md) · [stand van een zaak (SPARQL)](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/omgevingsvergunning/stand-van-de-zaak.rq) |

## Waarom deze casus

Zijn procedurestappen een codelijst? Deze casus zegt nee. Een stap heeft een volgorde, een
termijn, een rechtsgrond, substappen en in- en uitvoer: regels van zichzelf, dus een resource en
geen concept ([R18](../regels/r18.md)). De casus brengt drie modellen samen op één IRI per begrip.
Het AP Omgevingsvergunning levert de begrippen van het domein, P-PLAN de structuur van het plan, en
SOSA zegt wat een stap met de werkelijkheid doet. Ze toont ook dat een toestand als "in
voorbereiding" geen procedurestap is: die volgt uit de stappen die al uitgevoerd zijn.

## De keuzes

- **Procedure = plan.** `plan:gewone-procedure` is `ov:Procedure`, `p-plan:Plan`,
  `sosa:Procedure` en `cpsv:Rule`. De dienst volgt haar (`cpsv:follows`).
- **Procedurestap = stap,** met volgorde (`p-plan:isPrecededBy`), termijn (`ov:termijn`, een
  `time:Duration`) en rechtsgrond per artikel (`dct:source`).
- **Substappen** als `p-plan:MultiStep` met een deelplan: het ontvankelijkheids- en
  volledigheidsonderzoek. In het dossier is de uitvoering ervan één activiteit die het deelplan
  volgt, met de handelingen van de substappen als delen.
- **Een advies is een waarneming** van de verenigbaarheid van het project, het GOVC-advies een
  afgeleide ([R13](../regels/r13.md)). **De beslissing is een actuatie** op de vergunde toestand,
  met een `ov:VergundeToestand` als resultaat en het besluit als apart document
  ([R16](../regels/r16.md)).
- **Eén ambt, twee rollen.** De omgevingsambtenaar onderzoekt én beslist: een `sosa:System` met een
  sensor en een actuator als deelsystemen ([R1](../regels/r01.md)).
- **Het product is een variabele** van de procedure: het besluit
  `p-plan:correspondsToVariable output:P-0098`.
- **Geen deploymentlaag:** de regelgeving wijst de actoren aan; de zaak draagt het plan
  (`prov:hadPlan`).
- **De zaak komt overeen met haar blauwdruk:** de zaak met het plan (`prov:hadPlan`), elke
  zaakhandeling met een stap (`p-plan:correspondsToStep`), elk document met een variabele
  (`p-plan:correspondsToVariable`).

## P-PLAN en de PDC

De PDC (CPSV-AP) en P-PLAN beschrijven allebei typeniveau: wat bij elke aanvraag gebeurt. Het
dossier is één uitvoering daarvan. Zes links verbinden de drie lagen:

| Van | Eigenschap | Naar | Niveau |
|---|---|---|---|
| `publicservice:D3-0098` | `cpsv:produces` | `output:P-0098` | dienst (overgenomen uit de PDC) |
| `publicservice:D3-0098` | `cpsv:follows` | `plan:gewone-procedure` | dienst (voorstel voor de PDC) |
| `publicservice:D3-0098` | `cv:hasLegalResource` | `wet:ovd` | dienst (voorstel voor de PDC) |
| `step:beslissing` | `sosa:hasOutput` | `output:P-0098` | plan |
| `output:P-0098` | `p-plan:isOutputVarOf` / `p-plan:isInputVarOf` | `step:beslissing` / `step:bekendmaking`, `step:beroep-rvvb` | plan |
| `ent:besluit-1` | `p-plan:correspondsToVariable` | `output:P-0098` | dossier |

Er zijn twee bruggen. De eerste is het product: `output:P-0098` is zowel `cv:Output` van de dienst
als `p-plan:Variable` van de beslissing. Dat kan omdat beide op typeniveau staan: de variabele
is een plaatshouder die elk besluit invult. De tweede is `cpsv:follows`: de dienst volgt de
procedure, en de regel is dezelfde IRI als het plan. Een dossier bereikt de dienst zo langs twee
wegen. Langs het product loopt de weg van het besluit (`correspondsToVariable`, dan
`cpsv:produces`). Langs de procedure loopt hij van de zaak (`ov:procedure`, dan `cpsv:follows`).
Geen van beide vocabularia legt op dat het product van de dienst ook de uitvoer van een stap uit
haar plan is. Een SPARQL-controle in de bespreking doet dat wel. De invoerkant is niet gekoppeld:
de PDC beschrijft het aanvraagdossier niet als `cv:hasInput` van de dienst.

## Wat het AP Omgevingsvergunning mist

De casus laadt het AP-vocabularium en CPSV-AP 3.2.0 ([R17](../regels/r17.md)). Daarbij kwamen zes
verbeterpunten voor het AP naar boven. De belangrijkste: de rechtsgrond kan niet per stap, volgorde
en substappen ontbreken, en `ov:Vergunning` is tegelijk handeling en werk. De volledige lijst staat
in de README.

Voor het AP en de PDC samen: een zaak verwijst niet naar de dienst die ze levert. De enige
rechtstreekse link van een dossier naar de PDC is die van het besluit naar het product
(`p-plan:correspondsToVariable output:P-0098`). De zaak bereikt de dienst enkel via de procedure
die de dienst volgt, en dat breekt zodra meerdere diensten dezelfde procedure volgen. CPSV-AP en
het AP hebben geen eigenschap van een zaak naar een dienst; de casus stelt er een voor.

Volgorde en substappen lost de casus op met een alignering, als voorstel voor het AP:
`ov:Procedure ⊂ p-plan:Plan`, `ov:Procedurestap ⊂ p-plan:Step`, `ov:Zaakhandeling ⊂ prov:Activity`,
`ov:VergundeToestand ⊂ prov:Entity` en `ov:procedurestap ⊑ p-plan:correspondsToStep`
(`src/main/resources/be/vlaanderen/data/ns/omgevingsvergunning/alignments/ov-pplan-prov.ttl`).
Juridisch Werk en Rechtshandeling blijven bewust buiten de alignering: zolang `ov:Vergunning` zowel
handeling als werk is, zou een koppeling met PROV haar inconsistent maken.

## Zaak en blauwdruk: wat het AP Dossier mist

Het AP Omgevingsvergunning steunt op het [AP Dossier](https://data.vlaanderen.be/doc/applicatieprofiel/dossier/)
(`ov:dossier` heeft als bereik `dossier:Dossier`). Daar is een Zaak een *Eenheid van werk*
(`dbo:UnitOfWork`), die volgens de definitie "verschilt van Activiteit". Activiteiten "vinden
plaats tijdens" een zaak, en de procedure van een zaak is een string. Zo kan een zaak niet
overeenkomen met de blauwdruk die ze uitvoert. Het enige middel in de kern om een uitvoering als
geheel aan een plan te binden, `prov:hadPlan`, vraagt een activiteit. Een string heeft geen
stappen om mee te vergelijken.

Ook "Procedurestap" betekent in beide AP's iets anders:

| AP Omgevingsvergunning | AP Dossier |
|---|---|
| "een voorgeschreven handeling binnen een Procedure": de blauwdruk | "het geheel aan werk gedaan binnen een […] onderdeel van een procedure", met datums: de uitvoering, zonder link naar de voorgeschreven stap |

Het voorstel legt de blauwdruk in de kern en het domein eronder:

| Laag | Blauwdruk | Uitvoering → blauwdruk |
|---|---|---|
| kern | `p-plan:Plan`, `p-plan:Step` (ook `sosa:Procedure`, `prov:Plan`) | zaak `prov:hadPlan`, handeling `p-plan:correspondsToStep` |
| AP Dossier | bereik `p-plan:Plan` en `p-plan:Step` | Zaak → plan, Activiteit `p-plan:correspondsToStep` |
| AP Omgevingsvergunning | `ov:Procedure ⊂ p-plan:Plan`, `ov:Procedurestap ⊂ p-plan:Step` | `ov:procedure` en `ov:procedurestap` als subproperty |

Een `sosa:ExecutionCollection` is geen alternatief voor de zaak. Ze bevat enkel waarnemingen,
actuaties en bemonsteringen, en een procedure op de collectie moet voor elk lid gelden. De
uitwerking staat in de bespreking (§6) en als verbeterpunten 10 tot 13 in de README.

**Deelhandelingen.** De uitvoering van een stap met substappen omvat de handelingen van die
substappen. PROV heeft daar bewust geen eigenschap voor en raadt `dcterms:hasPart` aan (Moreau 2015,
*The rationale of PROV*, Requirement VI8). `sosa:hasMember` past niet: het verbindt een collectie met
uitvoeringen, niet een activiteit met haar delen. Omdat `dct:hasPart` zelf niets zegt over tijd of
plan, controleert `samenhang-deelhandelingen.rq` twee regels. Een deel valt binnen de tijd van het
geheel, en komt overeen met een stap van het plan dat het geheel volgt.

## Diagram

```mermaid
--8<-- "src/main/input/omgevingsvergunning/omgevingsvergunning.mmd"
```

## Turtle

??? example "omgevingsvergunning.ttl"

    ```turtle
    --8<-- "src/main/input/omgevingsvergunning/omgevingsvergunning.ttl"
    ```

??? example "stand-van-de-zaak.rq"

    ```sparql
    --8<-- "src/main/input/omgevingsvergunning/stand-van-de-zaak.rq"
    ```

??? example "samenhang-deelhandelingen.rq"

    ```sparql
    --8<-- "src/main/input/omgevingsvergunning/samenhang-deelhandelingen.rq"
    ```
