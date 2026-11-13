# Drempelwaarden

*De rapporteringsdrempels van het CSO-register (E-PRTR, IMJV Water, IMJV Lucht) als linked data,
en de toets van een jaarvracht eraan.*

| | |
|---|---|
| **Domein** | omgeving; emissierapportering |
| **Model** | het register zonder SOSA (SKOS en QUDT, met een ontwerpvocabularium in `csor:`); de toets plat, met twee afgeleide waarnemingen |
| **Bron** | een export van 688 rijen uit CSOR en het ontwerp "Ontwerp Codelijsten"; de jaarvracht uit [RIE-IEPR](riepr.md) |
| **Bestanden** | [README](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/drempelwaarden/README.md) · [bespreking](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/drempelwaarden/bespreking.md) |

## Waarom deze casus

Een drempel is, zoals een criterium in [VLAREM-rubrieken](vlarem.md), een norm en geen waarneming.
Maar een norm wordt gebruikt: iemand toetst er een jaarvracht aan. Die toets is wel een waarneming,
afgeleid uit de jaarvracht, met de drempel als inputwaarde.

## De keuzes

- **Een drempel is een hoeveelheid, geen code**: `csor:Drempelwaarde ⊂ qudt:QuantityValue`, met
  `qudt:numericValue` en een CSOR-eenheid ([R3](../regels/r03.md), [R18](../regels/r18.md)).
  Contexten, groepen en types zijn wel codes, in SKOS.
- **Codelijsten als geladen register**: zo controleert de validatie dat een drempel naar een
  bestaande groep en een bestaand type verwijst
  ([Codelijsten en registers](../modelleren/codelijsten.md)).
- **Geldigheid met DCAT**: `dct:temporal` naar een `dct:PeriodOfTime` met `dcat:startDate` en
  `dcat:endDate` in jaren. Een `time:Interval` zonder einde past niet bij [R12](../regels/r12.md);
  DCAT 3 is na vergelijking geladen ([R17](../regels/r17.md)).
- **Volgorde als `skos:OrderedCollection`**, niet `schema:position` ([R17](../regels/r17.md)).
- **De toets als afgeleide waarneming** van de lozing van de hele exploitatie: eerst de som over
  de lozingspunten, dan per drempel waar of onwaar, met de drempel als `sosa:hasInputValue`
  ([R13](../regels/r13.md), [Afgeleide waarneming](../patronen/afgeleide-waarneming.md),
  [Emissie als studieobject](../patronen/emissie.md)), zoals het alarm in [E-Detect](e-detect.md).
- **Verbeterpunten voor het register**: de E-PRTR-drempels voor water staan in kg ("vracht"), die
  voor lucht in kg/jr ("vracht per tijd"); 1900 en 2099 als plaatshouders; acht rijen zonder
  parameteraspect.

## Alternatief: de drempel als annotatie

Een tweede lezing, voor de werkgroep (status *open*): een drempel is een uitspraak vanuit een
rapporteringscontext over een parameteraspect van CSOR. Elke drempel is dan een `oa:Annotation`
([W3C Web Annotation](https://www.w3.org/TR/annotation-model/)): het parameteraspect is het doel,
bekeken binnen de rapporteringsgroep en het drempelwaardetype (`oa:hasScope`), de hoeveelheid is de
body, en een eigen motivatie zegt dat het om een rapporteringsdrempel gaat. Er zijn geen eigen
klassen of eigenschappen nodig, en andere contexten (normen, vergunningsvoorwaarden) kunnen op
dezelfde manier iets zeggen over hetzelfde parameteraspect. Daartegenover: de gegenereerde SHACL
controleert de annotaties niet, en een drempel telt vier knopen in plaats van twee. Dezelfde
structuur draagt ook een bereik: een (illustratieve) lozingsvoorwaarde pH 6,5 tot en met 9 is een
annotatie met de body `qudt:minInclusive 6.5 ; qudt:maxInclusive 9.0`, zonder `qudt:numericValue`.
Die facetten zijn in QUDT bedoeld voor datatypes; de bespreking weegt dat af. De argumenten
en discussievragen staan in de
[bespreking van het alternatief](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/drempelwaarden/alternatief/bespreking.md).

```mermaid
--8<-- "src/main/input/drempelwaarden/alternatief/drempelwaarden_vergelijking.mmd"
```

## Diagram

```mermaid
--8<-- "src/main/input/drempelwaarden/drempelwaarden.mmd"
```

## Turtle

??? example "toetsing.ttl"

    ```turtle
    --8<-- "src/main/input/drempelwaarden/toetsing.ttl"
    ```

??? example "csor-rapportering.ttl (ontwerpvocabularium)"

    ```turtle
    --8<-- "src/main/resources/be/vlaanderen/omgeving/data/ns/csor/csor-rapportering.ttl"
    ```

`drempelwaarden.ttl` (390 drempelwaarden) en de codelijsten staan in de
[repository](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/tree/main/src/main/input/drempelwaarden).
