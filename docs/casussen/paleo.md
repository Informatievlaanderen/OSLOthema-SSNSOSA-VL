# Paleoklimaat

*De CO₂-concentratie van de atmosfeer, 7530 jaar geleden, gemeten in een luchtbel in een ijskern.*

| | |
|---|---|
| **Domein** | paleoklimatologie |
| **Model** | plat, met een monsterketen en een afgeleide waarneming; twee alternatieven |
| **Bron** | illustratief |
| **Bestanden** | [README](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/paleo/README.md) (met de diagrammen) · [alternatief 1](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/paleo/paleo_atmosfeer.ttl) · [alternatief 2](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/paleo/paleo_atmosfeer_alt.ttl) |

## De vraag

Een luchtbel in een ijskern wordt verondersteld een monster te zijn van de atmosfeer op een moment
in het verleden. Twee waarnemingen op de luchtbel leveren de CO₂-concentratie en de C14-leeftijd;
een reconstructiemodel combineert ze tot de concentratie in de atmosfeer op die leeftijd.

## De keuzes

- **Een monsterketen**: luchtbel *isSampleOf* ijskern *isSampleOf* aardkorst, en de luchtbel ook
  *isSampleOf* de atmosfeer. Elk monster is het resultaat van een bemonstering (de boring, de
  extractie) ([R8](../regels/r08.md), [Monster en uiteindelijk studieobject](../patronen/monster.md)).
- **Niet-kalendertijd**: de fenomeentijd is 7530 jaar *Before Present*, met een benoemd
  tijdreferentiesysteem `ex:BP` ([R9](../regels/r09.md)).
- **Software als sensor**: het reconstructiemodel maakt de afgeleide waarneming.
- **De afgeleide waarneming** gebruikt de *resultaten* van de twee bronwaarnemingen
  (`sosa:hasInputValue`) en verwijst naar de bronwaarnemingen met `sosa:relatedObservation`
  ([R7](../regels/r07.md)).

## Twee alternatieven

| | Alternatief 1 | Alternatief 2 |
|---|---|---|
| inputwaarden | de twee resultaten | idem |
| procedure | beschrijft haar inputs in tekst | heeft inputvariabelen (`sosa:hasInput`) |
| koppeling waarde → variabele | — | `p-plan:correspondsToVariable` |
| wat het oplevert | eenvoud | de gebruikte procedure is afleidbaar ([P-PLAN en SOSA](../samenhang/pplan-sosa.md)) |

## De fout die rechtgezet werd

De vorige versie van alternatief 1 gaf de **bronwaarnemingen** als inputwaarde. Een waarneming is
een activiteit; met `sosa:hasInputValue ⊂ prov:used` wordt ze ook een entiteit, en PROV-O
verklaart die twee disjunct. Rechtgezet op 2026-10-01, en mee de aanleiding voor de opname van
het axioma in de W3C-module ([SOSA en PROV-O](../samenhang/sosa-prov.md#5-inputwaarde-en-resultaat-een-spiegel)).

```turtle
# fout                                          # juist
ex:Paleo sosa:hasInputValue ex:C14Observatie .  ex:Paleo sosa:hasInputValue ex:ResultaatC14Observatie ;
                                                         sosa:relatedObservation ex:C14Observatie .
```

## Turtle

??? example "paleo_atmosfeer.ttl (alternatief 1)"

    ```turtle
    --8<-- "src/main/input/paleo/paleo_atmosfeer.ttl"
    ```

??? example "paleo_atmosfeer_alt.ttl (alternatief 2)"

    ```turtle
    --8<-- "src/main/input/paleo/paleo_atmosfeer_alt.ttl"
    ```
