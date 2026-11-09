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
  volledigheidsonderzoek.
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

## Wat het AP Omgevingsvergunning mist

De casus laadt het AP-vocabularium en CPSV-AP 3.2.0 ([R17](../regels/r17.md)). Daarbij kwamen zes
verbeterpunten voor het AP naar boven. De belangrijkste: de rechtsgrond kan niet per stap, volgorde
en substappen ontbreken, en `ov:Vergunning` is tegelijk handeling en werk. De volledige lijst staat
in de README.

Volgorde en substappen lost de casus op met een alignering, als voorstel voor het AP:
`ov:Procedure ⊂ p-plan:Plan`, `ov:Procedurestap ⊂ p-plan:Step`, `ov:Zaakhandeling ⊂ prov:Activity`,
`ov:VergundeToestand ⊂ prov:Entity` en `ov:procedurestap ⊑ p-plan:correspondsToStep`
(`src/main/resources/be/vlaanderen/data/ns/omgevingsvergunning/alignments/ov-pplan-prov.ttl`).
Juridisch Werk en Rechtshandeling blijven bewust buiten de alignering: zolang `ov:Vergunning` zowel
handeling als werk is, zou een koppeling met PROV haar inconsistent maken.

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
