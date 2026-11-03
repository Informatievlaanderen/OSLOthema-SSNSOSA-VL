# ELF-meetnet

*De blootstelling aan het magnetische veld van hoogspanning, op een plaats, minuut per minuut.*

| | |
|---|---|
| **Domein** | omgeving; laagfrequente magnetische velden (ELF) van hoogspanningsverbindingen en -stations |
| **Model** | plat: de meetlocatie als ruimtelijk monster van de omgeving van de bron, een `sosa:Deployment` per meetcampagne, geneste collecties, uur- en dagindicatoren |
| **Bron** | ThingsBoard-telemetrie van ELF-node ELF_C_0020 (26/11/2025–26/01/2026) en de Jira-registratie van 15 meetcampagnes, gepseudonimiseerd; gescript |
| **Bestanden** | [README](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/elf/README.md) · [bespreking](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/elf/bespreking.md) · [opdracht](../oefenen/elf.md) |

## De vraag

Hoe sterk zijn burgers op een plaats blootgesteld aan het magnetische veld van een
hoogspanningsverbinding of -station, minuut per minuut, en wat zijn het minimum, het maximum en het
gemiddelde per uur en per dag? Het besluit van de Vlaamse Regering van 29 maart 2024 vraagt die
gegevens te publiceren, onafhankelijk van de netbeheerders.

## De keuzes

- **Een immissie op een plaats, zoals vliegtuiggeluid.** De meetlocatie is platform, studieobject en
  `sosa:SpatialSample` van de *omgeving* van de bron, zoals de geluidsmeetpost in
  [geluidsmeetnet](geluidsmeetnet.md) een monster is van de omgeving van de luchthaven
  ([R11](../regels/r11.md), [Ruimtelijk monster](../patronen/ruimtelijk-monster.md)).
- **Geen monster van de lijn, zoals een telpunt van een fietsroute.** Het veld op een plaats hangt af
  van de afstand tot de geleiders en is geen eigenschap van de lijn. Wat wél voor een stuk verbinding
  geldt, is de stroombelasting: een eigenschap van de bron, die een apart studieobject is.
- **Geen stimulus.** Een geluidsevent is een gebeurtenis die de meter laat meten; een ELF-veld is er
  continu. De omgeving verwijst naar de bron met `prov:wasInfluencedBy`.
- **Adres én geometrie.** `prov:atLocation` naar het adres, `geo:hasGeometry` naar een punt in
  Lambert 72, met de CRS-IRI in de literal. Een geocodeerde adrespositie is niet de plaats van de
  sensor; de herkomst van het punt staat erbij. In het voorbeeld is het punt fictief.
- **Een meetcampagne is een `sosa:Deployment`, geen `sosa:hosts`.** Een meter verhuist: ELF_C_0025
  stond eerst in Bloedhoven en daarna in Duisterwijk. De campagne heeft een begin en een einde
  (`prov:startedAtTime`, `prov:endedAtTime`; een `sosa:Deployment` is een `prov:Activity`,
  [R16](../regels/r16.md)).
- **Zeven eigenschappen, één per sleutel.** De betekenis van *low* en *high* is niet gedocumenteerd.
  Daarom blijft de data getrouw aan de bron en legt ze geen vectorinterpretatie op.
- **Geneste collecties.** Een uurcollectie met sensor, procedure en studieobject, en per bericht een
  collectie met de resultaattijd en zeven observaties.
- **Een eenheid die de bron niet geeft.** `unit:MicroT` is een aanname, gedocumenteerd als open vraag
  ([R3](../regels/r03.md)).
- **Geen fenomeentijd per minuut.** Een RMS-waarde geldt over een venster, dus een `time:Instant` zou
  fout zijn. De duur van het venster is niet gekend, dus enkel `sosa:resultTime`
  ([R12](../regels/r12.md)).
- **Indicatoren in een keten.** Per uur het minimum, het maximum en het gemiddelde uit de
  minuutwaarden, per dag dezelfde drie uit de uurindicatoren, zoals Lden uit Ld, Le en Ln. Week, maand
  en jaargemiddelde volgen op dezelfde manier ([R13](../regels/r13.md),
  [Afgeleide waarneming](../patronen/afgeleide-waarneming.md)).
- **De apparaatstatus is geen waarneming.** `active`, `lastConnectTime` en de andere statusvelden
  beschrijven de verbinding met ThingsBoard, niet het veld.

## Wat de data zelf vertelt

In alle 82 748 berichten geldt `RMStotal = 1,2374 × √(Xpeak_low² + Ypeak_low² + Zpeak_low²)`. De
meter berekent RMStotal dus zelf uit de drie *low*-componenten. Dat pleit ervoor om RMStotal als
afgeleide waarneming te modelleren, maar zolang de factor niet verklaard is, blijft het een output van
de meetprocedure.

## Diagram

```mermaid
--8<-- "src/main/input/elf/elf.mmd"
```

## Turtle

??? example "elf.ttl"

    ```turtle
    --8<-- "src/main/input/elf/elf.ttl"
    ```
