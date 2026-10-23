# Waterkwaliteit

*Meetresultaten van de Vlaamse Milieumaatschappij (VMM): concentraties in afvalwater en
oppervlaktewater, jaardebieten en vrachten van lozingen. Echte brondata, in fases gemapt, met een
toepassingsprofiel en een beslisdocument voor het OSLO-traject.*

| | |
|---|---|
| **Domein** | waterkwaliteit, lozingen, VMM |
| **Model** | plat, vier resultaatsets |
| **Bron** | exports van de VMM (2024–2025), gekoppeld aan CSOR, VHA en RIE-IEPR |
| **Transformatie** | Python-scripts met een gedeelde module; volledige data als `.trig`, toetsdelen als `.ttl` |
| **Ontologie** | [`waterkwaliteit.ttl`](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/resources/be/vlaanderen/data/ns/waterkwaliteit/waterkwaliteit.ttl): klassen, restricties, bron van de SHACL |
| **Bestanden** | [beslisdocument](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/waterkwaliteit/beslisdocument.md) · [stappenplan](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/waterkwaliteit/stappenplan.md) · [codelijsten](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/waterkwaliteit/codelijsten.md) · [studieobjecten](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/waterkwaliteit/featureofinterest.md) · [CSOR en I-ADOPT](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/waterkwaliteit/csor_iadopt.md) |

## Waarom deze casus

Ze toont het hele traject van [VI. Werkwijze](../werkwijze/index.md) op echte data: scope met de
eigenaar, plan in fases, registers hergebruiken, alles in scripts, een ontologie die ook het
profiel is, een alignmentanalyse en een beslisdocument. Bijna elke regel en elk patroon komt
erin voor.

## De vier resultaatsets

| Set | Wat het toont | Map |
|---|---|---|
| concentraties afvalwater | staal, staalname, meetput, CSOR-koppeling, teken `<` | `nieuw_model/afvalwater_concentraties/` |
| concentraties oppervlaktewater | meetplaats als ruimtelijk monster van een VHA-waterloop | `nieuw_model/oppervlaktewater_concentraties/` |
| jaardebieten | lozing als studieobject, jaarinterval, koppeling met RIE-IEPR | `nieuw_model/afvalwater_debieten/` |
| vrachten | afgeleide waarnemingen, berekeningsprocedure, groep van lozingen | `nieuw_model/afvalwater_vrachten/` |

## De keuzes

- **De eigenschap is een CSOR-parameteraspect** (`csor:ParameterAspect ⊂ sosa:Property`), niet de
  parameter en niet de stof; een analyse tegen I-ADOPT bevestigt dat niveau (beslispunt A1,
  [Register en I-ADOPT](../kaart/register-iadopt.md)).
- **De eenheid is een CSOR-eenheid**, met de mapping naar QUDT in het register, niet in de data
  (A2, [Register en QUDT](../kaart/register-qudt.md)).
- **Onder de rapportagegrens**: `qudt:lowerBound` en `qudt:upperBound`, geen `numericValue` (A3,
  [Rapportagegrens](../patronen/rapportagegrens.md)).
- **Het staal is het studieobject van een concentratie, de lozing het uiteindelijke** (A4,
  [Monster en uiteindelijk studieobject](../patronen/monster.md)); de meetput is de bemonsteraar.
- **De lozing is een emissie**, tijdloos, met de matrix als kenmerk (A5,
  [Emissie als studieobject](../patronen/emissie.md)).
- **De meetplaats oppervlaktewater is een ruimtelijk monster van de VHA-waterloop** (A6,
  [Ruimtelijk monster](../patronen/ruimtelijk-monster.md)).
- **Vrachten zijn afgeleide waarnemingen** uit concentratie en debiet (A7,
  [R13](../regels/r13.md)).
- **Eigen klassen als subklassen**: `wk:WaterkwaliteitObservatie ⊂ sosa:Observation`,
  `wk:Meetresultaat ⊂ qudt:QuantityValue`, `wk:Emissie ⊂ sosa:FeatureOfInterest`; de data typeert
  beide ([Ontologie en toepassingsprofiel](../werkwijze/ontologie.md)).
- **Naar externe datasets met `rdfs:seeAlso`**, niet `owl:sameAs`, zolang hun IRI's niet definitief
  zijn ([Codelijsten en registers](../modelleren/codelijsten.md)).

## Eén les uit de ontologie

`waterkwaliteit.ttl` zette `owl:maxCardinality 1` op `sosa:usedProcedure`. Omdat die eigenschap
een keten van eigenschappen heeft (in `sosa-prov`), mag dat in OWL 2 DL niet. De restrictie is op
2026-10-14 verwijderd; een profiel dat één procedure wil, doet dat met SHACL
([P-PLAN en SOSA](../kaart/pplan-sosa.md#4-wat-de-ketens-nog-niet-doen)).

## Diagram: concentraties afvalwater

```mermaid
--8<-- "src/main/input/waterkwaliteit/nieuw_model/afvalwater_concentraties/afvalwater_concentraties.mmd"
```

## Diagram: vrachten

```mermaid
--8<-- "src/main/input/waterkwaliteit/nieuw_model/afvalwater_vrachten/afvalwater_vrachten.mmd"
```

## UML van de ontologie

Gegenereerd uit `waterkwaliteit.ttl`, niet getekend:

```mermaid
--8<-- "src/main/input/waterkwaliteit/waterkwaliteit_uml.mmd"
```

## Turtle

??? example "afvalwater_concentraties.ttl (toetsdeel)"

    ```turtle
    --8<-- "src/main/input/waterkwaliteit/nieuw_model/afvalwater_concentraties/afvalwater_concentraties.ttl"
    ```

??? example "afvalwater_debieten.ttl (toetsdeel)"

    ```turtle
    --8<-- "src/main/input/waterkwaliteit/nieuw_model/afvalwater_debieten/afvalwater_debieten.ttl"
    ```
