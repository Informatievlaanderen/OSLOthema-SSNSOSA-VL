# Brondata in fases mappen

Voor een mapping van echte data, groter dan één illustratief voorbeeld: spreadsheets, CSV- of
JSON-exports van een databeheerder. Het uitgewerkte voorbeeld is
[waterkwaliteit](../casussen/waterkwaliteit.md).

## Principes

1. **Eerst de scope, met de eigenaar.** Wat telt eerst, wat niet nu? Typisch: eerst de gemeten
   resultaten; normen, beoordelingen en interpretaties later; beschrijvingen van bedrijven en
   stations enkel voor zover nodig als studieobject of identificatie. Schrijf de scope op met haar
   bron (wie, wanneer).
2. **Hergebruiken vóór uitvinden.** Registers voor wat gemeten wordt en in welke eenheid,
   bestaande datasets voor de studieobjecten (verwijs naar hun IRI's), bestaande ontologieën voor
   het domein. Een nieuwe codelijst enkel voor wat niets dekt, en enkel als de mapping ze nodig
   heeft. Een ontologie buiten de kern na een vergelijking ([R17](../regels/r17.md)).
3. **Alles in een script.** De omzetting is een script dat alle uitvoer opnieuw maakt uit de
   bronbestanden. Een beslissing wordt in het script veranderd, daarna wordt alles opnieuw
   gegenereerd en getoetst. Geen handmatige wijzigingen aan gegenereerde Turtle.
4. **Volledige data en een toetsdeel.** Het script schrijft de volledige dataset (in Vlaamse
   projecten als `.trig`, buiten de bulkvalidatie) en een klein, representatief deel als `.ttl`
   dat getoetst wordt, gekozen met een variabele in het script.
5. **De conventies gelden**: termen van SSN/SOSA 2023, `qudt:numericValue`, skolem-IRI's voor
   geneste resources, tijdzone.

## Stappen

1. **Inventariseer de bron**: per bestand en tabblad de inhoud en het aantal rijen; welke kolommen
   objecten identificeren (sleutels voor IRI's); eenheden en tekens (`<`-waarden); tijdkolommen
   en of ze een tijdzone hebben.
2. **Plan in fases**, in een plandocument: fase 0 voorbereiding, fase 1 de resultaten (één stap per
   resultaatset), latere fases voor normen en kenmerken. Per stap: bronbestand, doelpatroon,
   studieobjecten, open punten.
3. **Beslis de studieobjecten**: waarover elke waarneming gaat (een staal, een lozing, een
   meetplaats), en hoe je koppelt aan externe datasets (een stationsnummer dat gelijk is aan een
   identificatie in een ander register). Controleer externe datasets op fouten voor je ze
   hergebruikt, en meld die fouten aan hun eigenaar.
4. **Koppel aan registers**: met welk registerbegrip elke bronwaarde overeenkomt (parameter,
   eenheid, matrix, procedure). Maak de koppeling reproduceerbaar (een query of script over het
   register) en lijst de waarden zonder overeenkomst op.
5. **Map fase per fase**, één script per resultaatset met een gedeelde module; toets het toetsdeel
   van elk.
6. **Noteer beslissingen en vragen**: modelkeuzes als voorstel met verworpen alternatieven (in de
   bespreking of een [beslisdocument](beslisdocument.md)); vragen over de betekenis van de
   brondata in een lijst voor de eigenaar.

## Wat het oplevert

- een plandocument met principes, fases en stappen;
- een map per resultaatset (toetsdeel, volledige data, diagram, README, bespreking);
- de scripts en een gedeelde module;
- documenten over studieobjecten en codelijsten waar uitleg nodig is;
- een vragenlijst voor de eigenaar;
- wanneer een werkgroep moet beslissen: een beslisdocument.

## Grote datasets

Een toetsing wordt onpraktisch traag bij bestanden van tientallen megabytes. Houd de volledige
dataset in een bestand dat de bulkvalidatie overslaat, en een klein representatief deel (één
station, één staal) als bestand dat getoetst wordt. [R-factor](../casussen/r-factor.md) (42 MB),
[geluidsmeetnet](../casussen/geluidsmeetnet.md) (145 000 triples) en
[waterkwaliteit](../casussen/waterkwaliteit.md) doen dat.
