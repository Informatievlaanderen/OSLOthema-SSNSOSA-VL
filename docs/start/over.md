# Over dit werk

## Herkomst

Dit referentiewerk groeide uit het OSLO-thema *SSN/SOSA in Vlaanderen*
([`Informatievlaanderen/OSLOthema-SSNSOSA-VL`](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL)).
Dat project ontwikkelt richtlijnen voor de toepassing van de W3C-aanbeveling SSN/SOSA 2023 op
Vlaamse overheidsdomeinen en werkt ze uit in datavoorbeelden: grondwater, waterkwaliteit,
verkeer, geluid rond de luchthaven, erosie, energiebeheer in gebouwen en meer.

De kennis die daarbij opgebouwd werd, staat op drie plaatsen:

| Waar | Wat | Taal |
|---|---|---|
| de **modelleergids** in de kit [`milieuinfo/oslo-ld-kit`](https://github.com/milieuinfo/oslo-ld-kit) | de normatieve regels R1–R18, de patronen, de conventies voor documentatie en diagrammen, de werkwijzen | Engels |
| de **datavoorbeelden** in [`src/main/input/`](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/tree/main/src/main/input) | Turtle, diagram, README en bespreking per domein; herzieningen en alternatieven | Nederlands |
| de **ontologieën en uitlijningen** in [`src/main/resources/`](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/tree/main/src/main/resources) | de geladen vocabularia, de module P-PLAN–SOSA, ontwerpvocabularia | Engels en Nederlands |

Dit werk is de Nederlandse, didactische laag erbovenop: het legt uit, verbindt en verwijst.

## Eén bron

Om te vermijden dat twee teksten uit elkaar groeien, kopieert dit werk niets:

- De **normatieve regeltekst** komt bij het bouwen van de site rechtstreeks uit de gids; de
  versie van de kit staat bij elke regeltekst. Een controle bij het bouwen meldt een regel of
  patroon van de kit zonder pagina hier, of een pagina zonder regel in de kit.
- **Turtle en diagrammen** van de casussen worden rechtstreeks uit de datavoorbeelden ingevoegd.
  Wat je hier leest, is wat in de repository staat.
- Wat **in de datavoorbeelden** gevalideerd wordt, wordt bij elke publicatie opnieuw gevalideerd;
  faalt de validatie, dan wordt de site niet bijgewerkt.

## Bijdragen

- Opmerkingen en vragen: via de
  [issues](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/issues) van het project.
- Een tekst verbeteren: elke pagina heeft bovenaan een potloodicoon dat naar de bron op GitHub
  leidt.
- Een **nieuwe algemene regel of les** hoort in de gids van de kit, niet hier: dan is ze ook
  beschikbaar voor andere projecten. Dit werk volgt dan vanzelf, want de controle bij het bouwen
  vraagt om een pagina.

## Status

Dit werk is geen normatieve OSLO-specificatie. Het legt uit hoe de standaarden samen te gebruiken
zijn en welke keuzes in de voorbeelden gemaakt zijn. Waar een keuze nog open ligt voor een
werkgroep, staat dat erbij (*voorstel*, *open*, *beslist*).
