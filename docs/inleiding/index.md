# I. Waarom deze vocabularia de eerste reflex zijn

## Het probleem: elk domein vindt hetzelfde opnieuw uit

Kijk naar de gegevens die een Vlaamse overheidsdienst publiceert: een grondwaterpeil in een
filter, een fosforconcentratie in een staal afvalwater, het aantal fietsers per uur op een
telpost, het geluidsniveau van een overvliegend toestel, de erosiviteit van neerslag per
station, een geschiktheidsscore per rastercel. Het zijn verschillende domeinen, maar de gegevens
hebben dezelfde vorm:

- er is iets waarover de waarde gaat (een filter, een staal, een telpost, een rastercel);
- er is een eigenschap die bepaald wordt (peil, concentratie, intensiteit, score);
- iemand of iets heeft de waarde bepaald, volgens een werkwijze (een sonde, een labo-analyse,
  een teller, een rekenmodel);
- de waarde heeft een eenheid, een tijdstip of periode, en een plaats;
- vaak is de waarde afgeleid uit andere waarden (een dagsom, een jaargemiddelde, een vracht).

Zonder afspraak geeft elk domein die vorm zijn eigen namen: `meetwaarde`, `peilmeting`,
`resultaat`, `datum_meting`, `eenheid_code`, `meetpunt_id`. Wie twee datasets wil combineren,
moet eerst uitzoeken dat ze hetzelfde bedoelen. Wie een nieuwe dataset ontwerpt, beslist opnieuw
over vragen die al beantwoord zijn: is een meetpunt een plaats of een toestel? Hoort de eenheid
bij de waarde of bij de eigenschap? Is een berekend gemiddelde een meting?

## Het antwoord: een gedeelde, afgestemde stapel

Voor elk van die vragen bestaat een open standaard, door W3C of OGC gepubliceerd en internationaal
gebruikt:

| Vraag | Vocabularium | Kern |
|---|---|---|
| Wat wordt waargenomen, gewijzigd of bemonsterd, waarover, door wie, volgens welke werkwijze? | **SOSA/SSN 2023** (W3C/OGC) | waarneming, actuatie, bemonstering, studieobject, eigenschap, sensor, procedure |
| Waar komt het vandaan, wie was verantwoordelijk, wat werd gebruikt? | **PROV-O** (W3C) | activiteit, entiteit, agent; gebruikt, gegenereerd, afgeleid van |
| Volgens welk plan, in welke stappen, met welke variabelen? | **P-PLAN** | plan, stap, variabele; overeenkomst tussen uitvoering en plan |
| Welke waarde, in welke eenheid? | **QUDT** | grootheidswaarde, eenheid, grootheidssoort |
| Waar? | **GeoSPARQL** (OGC) | feature, geometrie, WKT |
| Wanneer? | **OWL-Time** (W3C/OGC) | tijdstip, interval, begin en einde, tijdreferentiesysteem |

Het belangrijkste is niet dat die standaarden bestaan, maar dat ze **op elkaar afgestemd** zijn.
SSN/SOSA 2023 publiceert zelf een uitlijning met PROV-O: een waarneming *is* een PROV-activiteit,
een sensor *is* een PROV-entiteit of -agent, het resultaat *wordt gegenereerd* door de
waarneming. Wie SOSA gebruikt, krijgt de herkomstvragen van PROV-O er dus gratis bij. Dat is wat
we bedoelen met één model in plaats van zes vocabularia. Hoofdstuk [II](../kaart/index.md) werkt
die verbanden uit.

## Waarom een reflex, en niet een keuze per project

Een *reflex* betekent: je begint met deze stapel, en je zoekt pas verder wanneer ze een betekenis
niet kan uitdrukken. Daar zijn vier redenen voor.

1. **De vragen zijn al beantwoord.** Of een meetpunt een plaats of een toestel is, of een
   berekend gemiddelde een waarneming is, of een resultaat onder de rapportagegrens een getal is:
   de definities en de uitlijningen geven het antwoord, of laten zien welke keuzes verdedigbaar
   zijn. Dit werk documenteert die antwoorden als [regels](../regels/index.md) en
   [patronen](../patronen/index.md).
2. **Fouten worden zichtbaar.** Omdat de vocabularia formeel uitgelijnd zijn, maakt een
   redeneerder sommige modelleerfouten aantoonbaar. Een waarneming die als inputwaarde van een
   andere waarneming opgegeven wordt, is tegelijk een activiteit en een entiteit, en PROV-O
   verklaart die twee disjunct. Dat is geen stijlkwestie meer, het is een tegenspraak.
3. **Datasets worden combineerbaar.** Een fietstelling, een waterstaal en een geluidsevent
   beantwoorden dezelfde query: *geef alle waarnemingen van studieobjecten binnen deze gemeente in
   april, met hun eenheid*. Over domeinen heen, zonder vertaaltabel.
4. **Keuzes worden uitlegbaar.** Een model dat de stapel volgt, legt een keuze uit met een
   verwijzing naar een definitie of een axioma, niet met een voorkeur. Dat maakt een bespreking in
   een werkgroep korter.

## Wanneer verder zoeken

De stapel dekt niet alles. Een verontreinigende stof, een bedrijfsactiviteit, een VLAREM-rubriek
of een waterloop is geen begrip van SOSA. Dan zoek je verder, in een vaste volgorde: eerst andere
W3C- en OGC-modellen, dan Vlaamse en Europese overheidsvocabularia en registers (OSLO, SEMIC,
CSOR), dan normen van andere instanties, en pas dan iets anders. Elke term buiten de kern is het
resultaat van een vergelijking, niet van de eerste zoekhit. Regel [R17](../regels/r17.md) en het
hoofdstuk [Een alignment vinden en beoordelen](../kaart/alignment-vinden.md) beschrijven hoe.

Ook wanneer je verder zoekt, blijft de stapel het geraamte. Een stof wordt dan een studieobject of
een eigenschap in een SOSA-waarneming; een waterloop wordt het uiteindelijke studieobject van een
meetplaats. De nieuwe term vult een plaats in het model in, hij vervangt het model niet.

## Verder

- [De stapel vocabularia](stapel.md): elk vocabularium in één pagina, met wat het wel en niet doet.
- [Plaats binnen OSLO](oslo.md): hoe dit werk zich verhoudt tot de OSLO-standaarden, de registers
  en Europese afspraken.
