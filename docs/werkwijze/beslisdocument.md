# Het beslisdocument

Het definitieve model wordt vaak beslist door een werkgroep, in Vlaanderen een OSLO-traject. Het
beslisdocument bereidt dat voor: een **uitgewerkt voorstel**, geen open vragenlijst. Een werkgroep
die moet kiezen tussen twee uitgewerkte modellen met hun gevolgen, beslist sneller en beter dan een
die een blanco blad krijgt. Het voorbeeld is het
[beslisdocument waterkwaliteit](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/waterkwaliteit/beslisdocument.md).

## Opbouw

```markdown
# Beslisdocument: <model>
## 0. Doel en werkwijze
[wie beslist; de statuswaarden; wat er na een beslissing gebeurt; welke documenten dit vervangt]
[de datavoorbeelden waarop de voorstellen steunen, met paden]
## 1. Overzicht
[tabel: punt, korte titel, status, voor wie]
## 2. Deel A: modelkeuzes voor de werkgroep
### A1. <titel>
## 3. Deel B: vragen voor de databeheerder
## 4. Deel C: registers en aanpalende projecten
## 5. Deel D: nog niet gemodelleerd
```

De delen zijn geordend naar **wie moet beslissen of antwoorden**:

| Deel | Voor wie | Inhoud |
|---|---|---|
| A | de werkgroep | modelkeuzes |
| B | de databeheerder | de betekenis van de brondata |
| C | beheerders van registers en aanpalende projecten | wijzigingen of afstemming buiten dit model |
| D | later | wat nog niet gemodelleerd is |

## Per punt

- **Vraag.** Eén zin.
- **Voorstel.** Zoals in de datavoorbeelden uitgewerkt, met een kort Turtle-fragment.
- **Waarom.** De argumenten, met cijfers uit de data waar ze helpen.
- **Verworpen alternatieven.** Elk met de reden.
- **Gevolg.** Wat eruit volgt, ook afwijkingen van regels of van aanpalende projecten (dan ook
  een punt in deel C).
- **Open.** Wat binnen het punt nog niet beslist is.
- **Detail.** Waar de volledige redenering staat.
- **Status.** *voorstel* (uitgewerkt, te bevestigen), *open* (geen voorstel), *beslist* (na een
  sessie, met datum en wie besliste).

## Regels

- Voorstellen weerspiegelen de **huidige toestand van de voorbeelden**; verandert een voorbeeld,
  dan het punt ook, en omgekeerd.
- Een beslissing wordt in het omzettingsscript toegepast; daarna wordt alles opnieuw gegenereerd
  en getoetst.
- Verworpen alternatieven blijven na een beslissing staan: ze verklaren de keuze. Zijn twee
  lezingen verdedigbaar, dan maakt een [alternatief](alternatief.md) de vergelijking concreet.
- Een punt dat een register of het model van een ander project raakt, gaat naar deel C, met een
  concreet verzoek.
- Beslissingen die een algemene afspraak worden, komen in de gids (als regel of patroon).

## Een voorbeeld uit waterkwaliteit

| # | Onderwerp | Status |
|---|---|---|
| A1 | `sosa:observedProperty` = CSOR-parameteraspect | voorstel |
| A2 | eenheid = CSOR-eenheid (QUDT via SKOS-mapping in het register) | voorstel |
| A3 | resultaat onder de rapportagegrens | voorstel (deels open) |
| A4 | studieobject van een concentratie: het staal, de lozing als uiteindelijk studieobject | voorstel |
| A6 | meetplaats oppervlaktewater als ruimtelijk monster van de VHA-waterloop | voorstel |
| A12 | IRI-strategie en namespaces | open |
| A13 | kenmerken die in de tijd veranderen (versies van een lozing) | open (fase 3) |
