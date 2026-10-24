# RIE-IEPR

*Een herziening van de RIE-IEPR-export van een integraal milieujaarverslag, en van de ontologie
erachter.*

| | |
|---|---|
| **Domein** | industriële emissies; integraal milieujaarverslag (IMJV) 2021 van AGC Glass Europe, vestiging Mol |
| **Model** | drielaags |
| **Bron** | de RDF-export van RIE-IEPR in drie lagen (plan, deployment, execution) en de ontologie `riepr.ttl` v1.0.1 ([`milieuinfo/RIE-IEPR`](https://github.com/milieuinfo/RIE-IEPR)) |
| **Bestanden** | [README met verbeterpunten](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/riepr/README.md) · [bespreking](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/riepr/bespreking.md) · [oefening](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/riepr/opdracht.md) |

## Waarom deze casus

Een productiemodel dat het drielaagse patroon al gebruikt: processen als plan en stappen,
installaties en punten als systemen, de exploitatie als inzet. Het toont wat er misloopt als de
ontologie zelf nog SSN-termen van vóór 2023 gebruikt: de shapes die eruit gegenereerd worden, eisen
termen die niet meer bestaan. Het toont ook dat een berekende waarde (de jaarvracht) zich verraadt
in de cijfers.

## De verbeterpunten

| # | Ontvangen | Herzien | Regel |
|---|---|---|---|
| 1 | `ssn:System`, `ssn:Deployment`, `ssn:implements`, `sosa:ObservableProperty`, … | `sosa:`-termen, `sosa:Property` | [R14](../regels/r14.md) |
| 2 | installaties en punten enkel `riepr:…` en `ssn:System` | ook `sosa:System` | [R1](../regels/r01.md) |
| 3 | `riepr:uitstootProces` enz. gemunt in de namespace van de ontologie | de procedures uit de ontologie | [R10](../regels/r10.md) |
| 4 | stappen genest met `isStepOfPlan`; één variabele als input én output | stappen van één plan, in volgorde, met eigen variabelen | [R4](../regels/r04.md), [plan](../modelleren/plan.md) |
| 5 | de exploitatie `ssn:implements` het proces | `prov:qualifiedAssociation` met `prov:hadPlan` | [R16](../regels/r16.md), [SOSA–PROV](../samenhang/sosa-prov.md) |
| 6 | `riepr:Resultaat` ⊂ `sosa:Result` met een aparte `qudt:QuantityValue` | één `qudt:QuantityValue` | [R3](../regels/r03.md) |
| 7 | eenheden `eenheid:mg_per_l` enz. (niet gepubliceerd) | CSOR-eenheden | [R3](../regels/r03.md) |
| 8 | de stof als eigenschap van zowel concentratie als vracht | CSOR-parameteraspecten | [R2](../regels/r02.md) |
| 9 | de jaarvracht als gewone meting | afgeleide observatie | [R7](../regels/r07.md), [R13](../regels/r13.md) |
| 10 | `time:inXSDDateTime` zonder tijdzone, einde 23:59:59 | `inXSDDateTimeStamp`, halfopen jaar | [R12](../regels/r12.md) |
| 11 | een fictieve sensor op elke observatie | geen sensor; R2-waarschuwing blijft | [R2](../regels/r02.md) |

De README telt twintig punten aan de data en twaalf aan de ontologie (O1–O12). De validatie van
de drie bronbestanden gaf samen 364 fouten, de meeste uit punt 1.

## De keuzes van de herziening

- **De lozing is het studieobject** ([Emissie als studieobject](../patronen/emissie.md)), zoals in
  [waterkwaliteit](waterkwaliteit.md), gekoppeld aan het proces met `prov:wasDerivedFrom` (een
  korte weg, wat het profiel eist) en aan de outputvariabele van de stap.
- **De jaarvracht is afgeleid** uit concentratie en jaardebiet ([Afgeleide waarneming](../patronen/afgeleide-waarneming.md)):
  0,00474 mg/L × 336 735 m³ = 1,59612 kg.
- **Kenmerken van punten zijn observaties** per rapporteringsjaar, niet vaste systeemeigenschappen.
- **Eenheden uit CSOR**, eigenschappen uit CSOR en uit de RIE-IEPR-codelijst.
- **De ontologie is mee herzien**: SSN/SOSA 2023-termen, `qudt:QuantityValue` als resultaat, geen
  equivalentie met de unie van p-plan-klassen, `prov:hadPlan` voor de exploitatie.

## Diagram: vóór en na

```mermaid
--8<-- "src/main/input/riepr/riepr_vergelijking.mmd"
```

## Diagram: de herziening

```mermaid
--8<-- "src/main/input/riepr/riepr_herzien.mmd"
```

## Turtle

??? example "riepr_herzien.ttl"

    ```turtle
    --8<-- "src/main/input/riepr/riepr_herzien.ttl"
    ```
