# Een mapping herzien

Een **herziening vervangt** een model dat fout is. Is het bestaande model verdedigbaar en is
enkel een andere lezing mogelijk, dan is het een [alternatief](alternatief.md), geen herziening.

In Vlaanderen komt dit vaak voor: een dienst of bedrijf maakte een eerste mapping (een LDES-stroom,
een export), en vraagt of ze klopt. De herziening is dan het antwoord, en tegelijk lesmateriaal.

## Stappen

1. **Bewaar het origineel**, ongewijzigd, in `source/`, in het formaat waarin het binnenkwam. Een
   ontvangen Turtle-bestand krijgt de extensie `.trig` (geldige TriG, dus leesbaar voor elk
   RDF-hulpmiddel, maar overgeslagen bij de validatie van alle voorbeelden samen). Een origineel
   wordt nooit bewerkt.
2. **Stel een diagnose.** Eerst de automatische: onbekende termen, inconsistenties, regels die
   niet voldaan zijn. Dan wat geen controle ziet, regel per regel:

    | Kijk naar | Regel |
    |---|---|
    | klassekeuze | [R1](../regels/r01.md) |
    | verplichte eigenschappen | [R2](../regels/r02.md) |
    | eenheden, `qudt:value`, `qudt:unit` | [R3](../regels/r03.md) |
    | `sosa:hasInput` met een waarde op een waarneming | [R5](../regels/r05.md) |
    | `sosa:hasInputValue` naar een waarneming | [R7](../regels/r07.md), [R13](../regels/r13.md) |
    | blanco knopen voor wat aanspreekbaar moet zijn, willekeurige IRI's | [R10](../regels/r10.md) |
    | tijd zonder zone, eigen start- en eindvelden | [R12](../regels/r12.md) |
    | oude `ssn:`-termen | [R14](../regels/r14.md) |
    | recordgegevens op een waarneming, uitvoeringseigenschappen op een sensor | [R16](../regels/r16.md) |
    | termen zonder RDF-definitie, `http`/`https` in prefixen | [R17](../regels/r17.md) |

3. **Schrijf de herziene versie** (`<naam>_herzien.ttl`), met elke term opgezocht.
4. **Documenteer de verbeterpunten** in de README, sectie *Verbeterpunten*: een genummerde lijst
   *origineel → herzien → motivatie*, met de motivatie verwijzend naar de specificatie of het
   regelnummer.
5. **Vergelijkingsdiagram** (`<naam>_vergelijking.mmd`) als de architectuur grondig verandert.
6. **Bespreking** van de herziene versie, in [negen vragen](bespreking.md).
7. **Toets** de herziene versie; elke fout opgelost.

## Een verbeterpunt, zoals het moet

> **5. Studieobject op de sensor.** `sensor sosa:hasFeatureOfInterest meetpunt` →
> `meetpunt sosa:hosts sensor` plus een `sosa:Deployment` met `sosa:deployedSystem`,
> `sosa:deployedOnPlatform` en `sosa:hasFeatureOfInterest meetpunt` → in SOSA 2023 gaat
> `sosa:hasFeatureOfInterest` van een uitvoering of inzet naar haar doelwit. Ze is een subproperty
> van `prov:used` (domein `prov:Activity`), dus maakt ze de sensor een activiteit, terwijl een
> sensor een `prov:Entity` is (R16).

*Uit de herziening van de [overstort](../casussen/overstort.md)-mapping.*

## Synthetische herziening

Voor lesmateriaal: een illustratief "voor"-bestand met typische fouten (`sosa:hasInput` op een
waarneming, `sosa:hasInputValue` naar een waarneming, `ssn:implements`, `qudt:value`, een blanco
knoop voor een aanspreekbare resource) en een gecorrigeerd "na"-bestand, gedocumenteerd zoals
hierboven.

## Een woord over ontvangen materiaal

Een ontvangen bestand komt van iemand die er werk in stak. De herziening is geen oordeel over de
maker, maar een uitleg die de volgende mapping beter maakt. Schrijf de verbeterpunten zo dat de
maker ze kan volgen: met de reden, niet enkel met de correctie.

## Casussen

- [Overstort](../casussen/overstort.md): een LDES-mapping van Aquafin, met negen verbeterpunten.
- [Erosiepoel](../casussen/erosiepoel.md): zeven verbeterpunten aan een aangeleverd scenario.
- [VLAREM-rubrieken](../casussen/vlarem.md): twee ontvangen varianten, één herziening.
- [Energiemanagement](../casussen/ems.md): drie scenario's met `_herzien`-versies.
