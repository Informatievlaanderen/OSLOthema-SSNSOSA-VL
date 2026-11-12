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
- **Alarm en bronaanwijzing zijn afgeleid.** Het alarm is een booleaanse waarneming, met de drempel
  in de procedure. De bronaanwijzing combineert concentratie, wind en melding tot een
  waarschijnlijkheid per bron.

## Wat het beslisdocument vraagt

Zes modelkeuzes (eenheid, studieobject, respons en concentratie, melding, afgeleiden, standaarden),
zes vragen aan de leverancier (API, kalibratie, meldingsvelden, uitvoer van de bronanalyse,
identificatoren, onderhoud) en drie verzoeken aan registerbeheerders (CSOR, QUDT, codelijsten voor
geur).

## Diagram

```mermaid
--8<-- "src/main/input/E-detect/e-detect.mmd"
```

## Turtle

??? example "e-detect.ttl"

    ```turtle
    --8<-- "src/main/input/E-detect/e-detect.ttl"
    ```
