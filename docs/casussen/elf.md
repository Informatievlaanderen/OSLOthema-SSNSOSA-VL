# ELF-meetnet

*Minuutwaarden van het laagfrequente magnetische veld, met meetcampagnes als inzet.*

| | |
|---|---|
| **Domein** | omgeving; laagfrequente magnetische velden (ELF) |
| **Model** | plat, met geneste collecties, een `sosa:Deployment` per meetcampagne en een afgeleid uurgemiddelde |
| **Bron** | ThingsBoard-telemetrie van ELF-node ELF_C_0020 (Duisterwijk, 26/11/2025–26/01/2026) en de Jira-registratie van 15 meetcampagnes; gescript |
| **Bestanden** | [README](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/elf/README.md) · [bespreking](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/elf/bespreking.md) · [opdracht](../oefenen/elf.md) |

## De vraag

Hoe sterk is het laagfrequente magnetische veld op een adres, minuut per minuut en per uur, en welke
meter stond wanneer waar?

## De keuzes

- **Een meetcampagne is een `sosa:Deployment`, geen `sosa:hosts`.** Een meter verhuist: ELF_C_0025
  stond eerst in Bloedhoven en daarna in Duisterwijk. Een tijdloze `sosa:hosts` zou hem op twee plaatsen
  tegelijk zetten. De campagne heeft een begin en een einde (`prov:startedAtTime`,
  `prov:endedAtTime`; een `sosa:Deployment` is een `prov:Activity`, [R16](../regels/r16.md)).
- **De meetlocatie is platform en studieobject, geen ruimtelijk monster.** De bron noemt geen groter
  studieobject, dus geen `sosa:isSampleOf` naar een verzonnen gebied ([R11](../regels/r11.md)). Het
  adres is een `prov:Location`, omdat de bron geen coördinaten geeft.
- **Zeven eigenschappen, één per sleutel.** De betekenis van *low* en *high* is niet gedocumenteerd.
  Daarom blijft de data getrouw aan de bron en legt ze geen vectorinterpretatie op.
- **Geneste collecties.** Een uurcollectie met sensor, procedure en studieobject, en per bericht een
  collectie met de resultaattijd en zeven observaties.
- **Een eenheid die de bron niet geeft.** `unit:MicroT` is een aanname, gedocumenteerd als open vraag
  ([R3](../regels/r03.md)).
- **Geen fenomeentijd per minuut.** Een RMS-waarde geldt over een venster, dus een `time:Instant` zou
  fout zijn. De duur van het venster is niet gekend, dus enkel `sosa:resultTime`
  ([R12](../regels/r12.md)).
- **Het uurgemiddelde is een afgeleide waarneming van het script**, niet van de meter, met
  `sosa:hasInputValue` naar de 60 resultaten ([R13](../regels/r13.md),
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
