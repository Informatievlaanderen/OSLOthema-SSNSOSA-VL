# E-Detect

*Geurhinder met elektronische neuzen, wind en meldingen van burgers: van sensorsignaal tot
mogelijke bron.*

| | |
|---|---|
| **Domein** | omgeving; geurhinder rond industrie en landbouw |
| **Model** | plat: meetpunt en meldplaats als ruimtelijk monster van de omgeving, een mens als sensor, drie afgeleide waarnemingen |
| **Bron** | de checklist interoperabiliteit van het EFRO-project E-Detect (Provincie West-Vlaanderen). Er is nog geen data: het voorbeeld is fictief |
| **Bestanden** | [README](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/E-detect/README.md) · [bespreking](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/E-detect/bespreking.md) · [beslisdocument](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/E-detect/beslisdocument.md) |

## De vraag

Kan een netwerk van geursensoren geurpieken sneller en objectiever vaststellen dan klachten en
momentopnames, en de bron helpen aanwijzen? E-Detect test dat in drie pilootzones. De checklist van
het project vraagt welke standaarden de sensor-, weer- en meldingsgegevens eenduidig maken. Dit
voorbeeld werkt één geurepisode van tien minuten uit als antwoord. Het beslisdocument zet de keuzes
klaar voor het overleg met het Expertisecentrum Interoperabiliteit.

## De keuzes

- **Een e-nose meet geen geur.** De sensor registreert veranderingen in de luchtsamenstelling, als
  een dimensieloze respons. De geurconcentratie in ouE/m³ is een *afgeleide* waarneming van een
  kalibratiemodel, met `sosa:hasInputValue` naar de responswaarden ([R7](../regels/r07.md),
  [R13](../regels/r13.md), [Afgeleide waarneming](../patronen/afgeleide-waarneming.md)). Zo blijft
  de kalibratie zichtbaar, wat het bestek ook vraagt.
- **Een eenheid die nergens staat.** De Europese geureenheid per kubieke meter (EN 13725:2022) staat
  niet in QUDT en niet in CSOR. QUDT kent enkel `quantitykind:OlfactoryThreshold`, de drempel van
  één stof. Het voorbeeld gebruikt een tijdelijke eenheid in een eigen namespace, tot CSOR ze
  opneemt ([R3](../regels/r03.md)).
- **De plaats voor de metingen, de emissie voor de bron.** Het meetpunt is platform, studieobject en
  ruimtelijk monster van de omgeving van de industriezone, zoals in [ELF-meetnet](elf.md)
  ([R11](../regels/r11.md), [Ruimtelijk monster](../patronen/ruimtelijk-monster.md)). De
  bronaanwijzing gaat over de geuremissie van een bedrijf
  ([Emissie en immissie](../patronen/emissie-immissie.md)).
- **Geen stimulus.** De e-nose meet continu; geen gebeurtenis zet een meting in gang, anders dan
  bij een geluidsevent in [Geluidsmeetnet](geluidsmeetnet.md)
  ([Stimulus](../patronen/stimulus.md)).
- **Een geurmelding is een waarneming.** De melder is een mens als sensor ([R1](../regels/r01.md)),
  zoals de veldwaarnemer in [Erosiepoel](erosiepoel.md). Soort geur, intensiteit (VDI 3882-1) en
  hedonische toon (VDI 3882-2) zijn begrippen uit kleine codelijsten. De meldplaats is persoonsgegeven
  en krijgt een veralgemeende geometrie.
- **Alarm en bronaanwijzing zijn afgeleid.** Het alarm is een booleaanse waarneming. De drempel is
  een input van de alarmprocedure, en elk alarm geeft met `sosa:hasInputValue` de drempelwaarde
  waarmee het berekend is, naast de geschatte concentratie. Zo is in de data te zien welke drempel
  gold, ook als hij later wijzigt. De bronaanwijzing combineert concentratie, wind en melding tot
  een waarschijnlijkheid per bron.

## Hoe de data naar buiten gaat

Vier kanalen, elk voor een andere afnemer:

| Kanaal | Voor wie | Rol |
|---|---|---|
| **OGC SensorThings API** | dashboard, meldingsapp, actuele waarden per sensor | operationeel, bij de leverancier; eigen model, geen RDF |
| **LDES** | andere systemen die de volledige geschiedenis overnemen | neutrale laag in SSN/SOSA, onafhankelijk van de leverancier |
| **Opvraagbare IRI's** | wie naar een meetpunt, sensor, procedure, drempel of eenheid verwijst | stabiele verwijzingen onder een basis-IRI van de opdrachtgever |
| **SPARQL** | analyse over sensor-, weer- en meldingsdata heen | optioneel, gevuld vanuit de LDES |

De SensorThings API sluit aan bij wat leveranciers aanbieden, maar alleen is ze niet genoeg. Een
afgeleide waarneming kan er niet naar haar inputwaarden verwijzen, en de identificatoren horen bij het
platform. De LDES met IRI's van de opdrachtgever houdt de data bruikbaar na een wissel van
leverancier. De componenten daarvoor (LDES-server, LDIO) zijn open source in
[OpenLDES](https://github.com/OpenLDES), beheerd door het Departement Omgeving. Een member van de
stroom is de waarneming zelf, zonder recordeigenschappen
([R16](../regels/r16.md), de les uit [Overstort](overstort.md)). Een herberekening met een nieuw
kalibratiemodel is een nieuwe afgeleide waarneming, geen overschreven waarde.

## Wat het beslisdocument vraagt

Zeven modelkeuzes (eenheid, studieobject, respons en concentratie, melding, afgeleiden, standaarden,
API's en ontsluiting), zeven vragen aan de leverancier (API en LDES, kalibratie, meldingsvelden,
uitvoer van de bronanalyse, identificatoren, onderhoud, afscherming) en vier verzoeken aan
registerbeheerders en beheerders van infrastructuur (CSOR, QUDT, codelijsten voor geur, OpenLDES
en persistente IRI's).

## Diagram

```mermaid
--8<-- "src/main/input/E-detect/e-detect.mmd"
```

## Turtle

??? example "e-detect.ttl"

    ```turtle
    --8<-- "src/main/input/E-detect/e-detect.ttl"
    ```
