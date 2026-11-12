# E-Detect — geurhinder met sensornetwerken, weergegevens en meldingen

## Context

E-Detect (EFRO-project 2330, Provincie West-Vlaanderen, met VITO, Stad Roeselare, Inagro en
Gezondheidsmakers) zet geursensornetwerken in, in drie pilootzones: één industriële en twee
landbouwzones. De sensoren ("e-noses") registreren veranderingen in de samenstelling van de
omgevingslucht. Een dataplatform combineert die metingen met weergegevens (windrichting en
windsnelheid) en met geurmeldingen van burgers. Zo wil het project geurpieken sneller en
objectiever detecteren en mogelijke bronnen aanwijzen.

Volgens de checklist interoperabiliteit van het project (vragen 16 tot 18) is nog niet bepaald welke
OSLO- of internationale standaarden van toepassing zijn. De leverancier van sensornetwerk,
dataplatform en meldingsapplicatie is nog niet aangesteld, en er is dus nog geen data.

Dit voorbeeld toont met **fictieve data** hoe zulke gegevens in SSN/SOSA 2023 passen. Het is de
basis van het [beslisdocument](beslisdocument.md) voor het overleg met het Expertisecentrum
Interoperabiliteit.

## Bron

*E-Detect – Checklist Interoperabiliteit* (Provincie West-Vlaanderen, november 2026, 13 pagina's):
de ingevulde checklist van het Expertisecentrum Interoperabiliteit, met 30 vragen in zes delen:

| Deel | Vragen | Wat erin staat |
|---|---|---|
| Algemene informatie | 1–7 | geurhinder waar wonen en industrie of landbouw dicht bij elkaar liggen; proefopstelling in Roeselare-Rumbeke; doel: continue monitoring, een draaiboek, open standaarden en geen afhankelijkheid van één leverancier |
| Projectpartners en stakeholders | 8–9 | Provincie West-Vlaanderen (coördinatie, aanbesteding), VITO, Stad Roeselare, Inagro, Gezondheidsmakers; een externe leverancier voor sensornetwerk, dataplatform en meldingsapp |
| Proces- en organisatorische interoperabiliteit | 10–11 | de sensoren vullen klachtenbehandeling, terreinonderzoek en klassieke geurmetingen aan, ze vervangen ze niet |
| Data en technologie | 12–25 | sensor-, weer-, geografische en meldingsgegevens, en verwerkte gegevens (afwijkingen, alarmen, analyses van bronnen); de sensoren meten geen geurbeleving; export in machineleesbare formaten (CSV voor de industriële zone), een API telt mee in de gunning; welke standaarden van toepassing zijn, is nog open (16–19) |
| Juridische interoperabiliteit | 26–28 | overheidsopdrachten, AVG (locatie van meldingen), vertrouwelijke bedrijfsgegevens, rol- en rechtenbeheer |
| Governance | 29–30 | overdraagbaarheid via een draaiboek, niet via één platform |

Het bestand staat lokaal in `source/` maar niet in versiebeheer (`.gitignore`): het bevat de naam en
het e-mailadres van de contactpersoon van het project.

## Transformatie

Geen. `e-detect.ttl` is met de hand opgesteld. Het bedrijf, de meetpunten, de melder, de
geometrieën en alle waarden zijn fictief.

## Mappingkeuzes

Plat model, zoals [`elf/`](../elf/) en [`geluidsmeetnet/`](../geluidsmeetnet/):

- **Meetpunt.** Het meetpunt is platform, studieobject en ruimtelijk monster van de *omgeving* van
  de industriezone (R11). De geursensor (e-nose) staat erop.
- **Geurmelding.** Een geurmelding is een waarneming door een mens als sensor (R1). De meldplaats is
  een ruimtelijk monster met een veralgemeende geometrie, omdat het om persoonsgegevens gaat.
- **Afgeleide waarnemingen** (R7, R13):
  - de geschatte geurconcentratie in ouE/m³, uit de sensorrespons;
  - het alarm bij een overschrijding van de drempel;
  - de bronaanwijzing. Die heeft als studieobject de *geuremissie* van het bedrijf (patroon
    *Emissie als studieobject*).
- **Eenheid.** De eenheid ouE/m³ (EN 13725:2022) staat niet in QUDT en niet in CSOR. Daarom staat
  ze tijdelijk in een eigen namespace, met een TODO voor CSOR.

De keuzes en hun alternatieven staan in [`bespreking.md`](bespreking.md).

## Diagram

[`e-detect.mmd`](e-detect.mmd) (Mermaid): procedure, infrastructuur en waarneming, met de afgeleide
waarnemingen in DERIVATION.

## Uitvoerbestanden

| Bestand | Inhoud |
|---|---|
| `e-detect.ttl` | De data: tijdelijke eenheid, bron en omgeving, infrastructuur, procedures, codelijsten voor de melding, waarnemingen en afgeleide waarnemingen |
| `e-detect.mmd` | Het diagram |
| `bespreking.md` | De bespreking (negen secties) |
| `beslisdocument.md` | Beslispunten voor E-Detect, het Expertisecentrum en de registerbeheerders |

## Gebruik

Valideren met de MCP-server `ld-vocab` (`validate_file` op `src/main/input/E-detect/e-detect.ttl`),
of met de bulkvalidatie uit `CLAUDE.md` §5.
