# Plaats binnen OSLO

## OSLO in het kort

OSLO (*Open Standaarden voor Linkende Organisaties*) is het programma van de Vlaamse overheid dat
semantische standaarden vastlegt in co-creatie met overheden, bedrijven en kennisinstellingen. Een
OSLO-traject levert een **vocabularium** (de begrippen, met URI's onder `data.vlaanderen.be`) en
een **toepassingsprofiel** (de afspraken over welke begrippen een toepassing gebruikt, met welke
kardinaliteit), gepubliceerd in het [Standaardenregister](https://data.vlaanderen.be/standaarden).

OSLO hergebruikt internationale standaarden waar dat kan, en legt eigen begrippen enkel vast waar
nodig. SSN/SOSA, PROV-O, QUDT, GeoSPARQL en OWL-Time passen in die lijn: het zijn de
internationale standaarden voor waarnemingen en hun context.

## Wat dit werk toevoegt

Een OSLO-toepassingsprofiel zegt *welke* begrippen een toepassing gebruikt. Het zegt minder over
*hoe* je een concrete dataset in die begrippen giet: of een meetpunt een platform of een
studieobject is, wat je doet met een waarde onder de rapportagegrens, of een berekende dagsom een
waarneming is. Dit werk vult die laag in:

| Laag | Wat | Waar |
|---|---|---|
| internationale standaard | definities en uitlijningen | W3C, OGC (SOSA, PROV-O, …) |
| **toepassingsrichtlijnen** | **regels, patronen, uitgewerkte voorbeelden, werkwijze** | **dit werk** |
| OSLO-vocabularium en -toepassingsprofiel | begrippen en afspraken per domein | Standaardenregister |
| dataset | concrete data | de databeheerder |

Een domeintraject (bijvoorbeeld waterkwaliteit) kan zo vertrekken van een uitgewerkt voorstel in
plaats van een blanco blad. De casus [waterkwaliteit](../casussen/waterkwaliteit.md) toont hoe:
echte brondata, gemapt volgens de regels, met een [beslisdocument](../werkwijze/beslisdocument.md)
voor de werkgroep.

## Registers

Vlaanderen beheert registers die de kernvocabularia aanvullen. Ze worden **hergebruikt, niet gekopieerd**:
data verwijst naar de begrippen van het register, het breidt ze niet uit.

| Register | Wat | Gebruik in dit werk |
|---|---|---|
| **CSOR** (Departement Omgeving) | codelijsten voor omgevingsmetingen: parameters en parameteraspecten, eenheden, dragers (matrices), procedures | waargenomen eigenschap en eenheid in waterkwaliteitsdata ([Register en QUDT](../kaart/register-qudt.md)) |
| **VHA** (Vlaamse Hydrografische Atlas) | waterlopen en segmenten | uiteindelijk studieobject van een meetplaats oppervlaktewater |
| **RIE-IEPR** | inrichtingen, exploitanten, emissiepunten | de lozing en het bedrijf achter een afvalwaterstaal |
| **VLAREM-indelingslijst** | rubrieken van hinderlijke inrichtingen | de casus [VLAREM-rubrieken](../casussen/vlarem.md) |
| **Rioolinventaris** | overstorten, meetpunten | de casus [overstort](../casussen/overstort.md) |

Een begrip dat ontbreekt, of een mapping die niet klopt, is een punt voor de beheerder van het
register, niet iets om in de data op te lossen ([Codelijsten en registers](../modelleren/codelijsten.md)).

## Europese afspraken

- **INSPIRE** gebruikt voor waarnemingen het model *Observations and Measurements* (ISO 19156).
  SOSA is daar de linked-datavorm van: OGC en W3C hebben beide samen ontwikkeld, en de begrippen
  komen overeen (studieobject, eigenschap, procedure, resultaat, fenomeentijd).
- **SEMIC Core Vocabularies** (Core Location, Core Business, …) zijn de Europese tegenhanger van de
  OSLO-basisvocabularia. Ze komen in beeld wanneer een studieobject een organisatie, adres of
  locatie is.
- **I-ADOPT** (RDA) ontleedt een variabele in eigenschap, object, matrix en beperking. Het helpt
  om de waargenomen eigenschap te structureren ([Register en I-ADOPT](../kaart/register-iadopt.md)).

## Verhouding tot de kit

De normatieve regels van dit werk staan in de modelleergids van
[`milieuinfo/oslo-ld-kit`](https://github.com/milieuinfo/oslo-ld-kit), in het Engels, zodat
andere projecten ze kunnen overnemen. Dit werk is de Nederlandse uitleg erbij, met de Vlaamse
voorbeelden. Een nieuwe algemene regel komt in de kit; een pagina hier volgt vanzelf
([Over dit werk](../start/over.md)).
