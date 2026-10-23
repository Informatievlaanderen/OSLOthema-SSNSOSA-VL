# Ontologieën aligneren

Past een register op een ander model? Kan een domeinvocabularium op SOSA aansluiten? Zo'n vraag
verdient een analyse met cijfers, niet een indruk op basis van drie voorbeelden. Het uitgewerkte
voorbeeld is de alignment van het CSOR-parameterregister met I-ADOPT
([Register en I-ADOPT](../samenhang/register-iadopt.md)).

## Opbouw van de analyse

```markdown
# <A> en <B>: analyse van de alignment
## 1. Samenvatting                [eerst de conclusie: wat past, wat niet, het voorstel]
## 2. <B> in het kort             [het doelmodel, voor zover nodig]
## 3. Structurele vergelijking    [component per component: begrip van A ↔ begrip van B]
## 4. Kwantitatieve toets         [hoeveel elementen van A passen op B, met een script]
## 5. Knelpunten per component    [een paragraaf per knelpunt, met echte voorbeelden]
## 6. Gevolgen voor het model     [per betrokken beslispunt]
## 7. Voorstel voor de alignment  [klassen en eigenschappen; wat gegenereerd wordt;
                                   wat de beheerders van A later moeten herstructureren]
## 8. Open punten
## 9. Toets per element           [welke elementen niet op hun plaats staan, en waarom]
```

## Stappen

1. **Begrijp beide modellen** uit hun bronnen (ontologiebestanden, specificaties), niet uit het
   geheugen. Laad ze, zodat je termen kan opzoeken. Beoordeel een nieuw model eerst op de
   criteria van [R17](../regels/r17.md).
2. **Vergelijk structureel**: elke component van het ene model tegenover het andere (eigenschap,
   object, matrix, beperking), met aandacht voor waar het ene model mengt wat het andere scheidt.
3. **Toets kwantitatief met een script** over alle elementen van het register, zodat de analyse
   op cijfers rust ("x van y passen rechtstreeks") en herhaalbaar is na wijzigingen.
4. **Lijst de knelpunten** per component, met concrete elementen als bewijs.
5. **Stel de alignment voor** in OWL-termen: subklassen, een rechtstreekse eigenschap, of een
   gegenereerde beschrijving per element; geen SKOS tussen klassen ([R15](../regels/r15.md)).
   Scheid wat nu kan van wat de beheerders van het register moeten doen.
6. **Volg de gevolgen** tot in de beslispunten van het model in opbouw, en tot de open vragen.

## Regels

- Eerst de conclusie, dan het bewijs.
- Elke uitspraak over een model is nagekeken in zijn bron.
- Wat de beheerders van het andere model moeten veranderen, wordt een concreet verzoek
  (beslisdocument, deel C).
- Een gevonden alignment komt in het [register van alignments](../samenhang/alignment-vinden.md#het-register-van-gekende-alignments).
