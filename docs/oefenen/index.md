# VIII. Oefenen

Modelleren leer je door te modelleren. Drie oefeningen, elk bij een casus die als
referentieoplossing dient. Ze zijn gemaakt voor een workshop van ongeveer een uur, in vier stappen:

| Stap | Vorm | Duur | Wat |
|---|---|---|---|
| 1 | individueel | 10 min | de SOSA-begrippen herkennen: wat is het studieobject, de eigenschap, de sensor …? |
| 2 | in paren | 15 min | een diagram schetsen, met drie sturende vragen |
| 3 | individueel of in groep | 20 min | de Turtle schrijven, met minimale eisen |
| 4 | plenair | 15 min | de keuzes bespreken |

## De oefeningen

| Oefening | Niveau | Wat ze oefent | Referentie |
|---|---|---|---|
| [Erosiepoel](erosiepoel.md) | instap | het skelet van een waarneming, een mens als sensor, een collectie, een resultaat met eenheid | [casus](../casussen/erosiepoel.md) |
| [Verkeersmetingen](verkeersmetingen.md) | gevorderd | ruimtelijk monster, intervallen, een afgeleide dagsom | [casus](../casussen/verkeersmetingen.md) |
| [Temperatuur en raam](temperatuur-raam.md) | gevorderd | het drielaagse model: plan, stappen, variabele, actuatie | [casus](../casussen/temperatuur-raam.md) |

## Voor lesgevers

- De vragen van stap 1, 2 en 4 sturen naar de beslispunten van de casus: waarom `hasResult` en niet
  `hasSimpleResult`, waarom een ruimtelijk monster, waarom een interval. Laat deelnemers de keuze
  **verdedigen**, niet enkel maken.
- Stap 3 vraagt de minimale Turtle, niet de volledige oplossing.
- Laat de deelnemers hun Turtle toetsen ([Hulpmiddelen](../bijlagen/hulpmiddelen.md)); een
  disjunctiefout is een goed vertrekpunt voor de plenaire bespreking.
- Een herziening is ook goed oefenmateriaal: geef de ontvangen versie van de
  [erosiepoel](../casussen/erosiepoel.md) of een stuk van de [overstort](../casussen/overstort.md)-mapping,
  en laat de deelnemers de fouten zoeken.

## Een eigen oefening maken

Elke oefening heeft dezelfde opbouw: een use case (context, beschrijving van het systeem, concrete
metingen), dan de vier stappen, en een verwijzing naar de referentieoplossing. Gebruik in stap 1
enkel de namen van SSN/SOSA 2023 (`Property`, niet `ObservableProperty`).
