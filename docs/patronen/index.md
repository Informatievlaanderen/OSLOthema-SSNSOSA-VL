# V. Patronen

Een patroon is een oplossing die in meer dan één domein terugkomt. Kijk vóór je een nieuw domein
modelleert, of een patroon past. Kies dan bewust: volg het patroon (samenhang over domeinen heen),
of modelleer de eigen lezing van het domein en leg uit waarom. Zijn beide verdedigbaar, werk dan
een [alternatief](../werkwijze/alternatief.md) uit in plaats van stil te kiezen.

| Patroon | Kern | Gebruikt in |
|---|---|---|
| [Emissie als studieobject](emissie.md) | de uitstoot is het studieobject, gegenereerd door een activiteit | [waterkwaliteit](../casussen/waterkwaliteit.md) (lozing), [geluidsmeetnet](../casussen/geluidsmeetnet.md) (alternatief), [overstort](../casussen/overstort.md) (alternatief) |
| [Stimulus](stimulus.md) | de gebeurtenis die een sensor doet meten; het studieobject blijft de plaats | [geluidsmeetnet](../casussen/geluidsmeetnet.md) (hoofdmodel) |
| [Emissie en immissie](emissie-immissie.md) | één keten: de emissie bij de bron, de immissie die er op een plaats van afgeleid is; elk het studieobject van een eigen vraag | [geluidsmeetnet](../casussen/geluidsmeetnet.md) (keten); tegenvoorbeeld [ELF-meetnet](../casussen/elf.md) |
| [Monster en uiteindelijk studieobject](monster.md) | het monster is het studieobject, het bemonsterde ding het uiteindelijke | [waterkwaliteit](../casussen/waterkwaliteit.md), [paleo](../casussen/paleo.md) |
| [Ruimtelijk monster](ruimtelijk-monster.md) | een meetpunt als monster van een groter gebied | [verkeersmetingen](../casussen/verkeersmetingen.md), [waterkwaliteit](../casussen/waterkwaliteit.md), [geluidsmeetnet](../casussen/geluidsmeetnet.md), [PGD](../casussen/pgd.md), [ELF-meetnet](../casussen/elf.md) |
| [Afgeleide waarneming](afgeleide-waarneming.md) | berekend uit de resultaten van andere waarnemingen | [verkeersmetingen](../casussen/verkeersmetingen.md), [geluidsmeetnet](../casussen/geluidsmeetnet.md), [ELF-meetnet](../casussen/elf.md), [paleo](../casussen/paleo.md), [waterkwaliteit](../casussen/waterkwaliteit.md) |
| [Rapportagegrens](rapportagegrens.md) | "< X" als interval, niet als waarde | [waterkwaliteit](../casussen/waterkwaliteit.md) |

## Eén keten, twee vragen

Twee patronen leken dezelfde vraag op een andere manier te beantwoorden: wat is het studieobject bij
een gebeurtenis die een meting veroorzaakt? Het patroon [Emissie en immissie](emissie-immissie.md)
toont dat het twee schakels van één keten zijn, elk met een eigen vraag.

```mermaid
flowchart LR
    v["vlucht<br/>prov:Activity"] -->|generated| e["geluidsemissie<br/>FOI: wat stoot de vlucht uit?"]
    i["geluidsevent bij de meetpost<br/>immissie · sosa:Stimulus"] -->|wasDerivedFrom| e
    i -->|isDetectedBy| s["geluidsmeter"]
    c["eventcollectie"] -->|wasOriginatedBy| i
    c -->|hasFeatureOfInterest| m["meetpost<br/>FOI: wat krijgt de plaats?"]

    style v fill:#e54b89,stroke:#2E5C8A,color:#fff
    style e fill:#f8b622,stroke:#2E5C8A,color:#000
    style i fill:#f8b622,stroke:#2E5C8A,color:#000
    style s fill:#60c4e4,stroke:#2E5C8A,color:#000
    style c fill:#e54b89,stroke:#2E5C8A,color:#fff
    style m fill:#60c4e4,stroke:#2E5C8A,color:#000
```

| | Emissie als studieobject | Stimulus |
|---|---|---|
| de vraag | wat stoot deze bron uit? | wat krijgt deze plaats te verduren? |
| studieobject | de emissie | de plaats (meetpost) |
| plaats in de keten | bronzijde | ontvangerzijde: de immissie bij de sensor |
| volgt | de lozingen in waterkwaliteit | de sensorketen van SOSA zelf |

In het geluidsmeetnet staan het hoofdmodel (stimulus), het alternatief (emissie) en de keten die ze
verbindt naast elkaar.

## Een nieuw patroon

Een patroon komt in de [gids](https://github.com/milieuinfo/oslo-ld-kit/blob/main/guide/patterns.md)
wanneer een werkgroep een keuze maakt die een algemene afspraak wordt. Dit werk volgt vanzelf: het
bouwen van de site faalt zolang een nieuw patroon van de gids hier geen pagina heeft.
