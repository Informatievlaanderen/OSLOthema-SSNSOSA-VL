# Geluidsmeetnet

*Geluidsevents van overvliegende toestellen en dagindicatoren (Ld, Le, Ln, Lden) rond Brussels
Airport, uit het verwerkingsplatform Aerovision.*

| | |
|---|---|
| **Domein** | omgevingsgeluid, luchtvaart |
| **Model** | plat, met geneste collecties en afgeleide waarnemingen; een alternatieve lezing |
| **Bron** | Aerovision-export van 29 september 2026: 4 CSV's, 13 meetcampagnes, 1818 events, 627 vluchten |
| **Transformatie** | Python-script → `.trig` (alle campagnes, ~145 000 triples) en `.ttl` (campagne M072-2) |
| **Bestanden** | [README](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/geluidsmeetnet/README.md) · [bespreking](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/geluidsmeetnet/bespreking.md) · [alternatief](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/geluidsmeetnet/alternatief/README.md) |

## Waarom deze casus

Ze stelt de vraag die bij elke gebeurtenis terugkomt (**plaats of bron?**), en werkt beide
antwoorden uit. Ze bevat ook de langste rekenketen van het project: events → dagindicatoren →
Lden.

## De keuzes (hoofdmodel)

- **Plat, niet drielaags.** De export bevat de *resultaten* van een meerstappenketen
  (eventdetectie, vluchtcorrelatie, dagaggregatie), maar niets over de stappen zelf: geen
  drempels, geen correlatievenster, geen uitsluitingsregels. Een plan zou verzonnen zijn
  ([R4](../regels/r04.md)).
- **De meetpost is een ruimtelijk monster** van de omgeving van de luchthaven; een meetcampagne is
  een `sosa:Deployment` van de geluidsmeter op de meetpost ([R11](../regels/r11.md)).
- **Het geluidsevent is een `sosa:Stimulus`**, gegenereerd door een vlucht (`prov:Activity`) die
  een luchtvaartuig gebruikt ([Stimulus](../patronen/stimulus.md)).
- **Per event een collectie** van vier waarnemingen (LAeq, LAmax, SEL, duur), veroorzaakt door het
  event (`sosa:wasOriginatedBy`); alle eventcollecties van een campagne in één dagcollectie.
- **Dagindicatoren als afgeleide waarnemingen** van de Aerovision-rekenmodule (software als
  sensor), buiten de collectie, met `sosa:hasInputValue` naar de eventresultaten. Lden is een
  afgeleide van afgeleiden. De afleiding is nagerekend voor alle 13 campagnes
  ([R13](../regels/r13.md), [Afgeleide waarneming](../patronen/afgeleide-waarneming.md)).
- **Eén stijl voor resultaten**: `qudt:QuantityValue` met `unit:DeciB_A` of `unit:SEC`
  ([R3](../regels/r03.md)).
- **Tijdstempels genormaliseerd**: sommige kolommen hadden een offset (`+02:00`), andere stonden
  zonder offset in UTC; alles omgezet naar lokale tijd met offset ([R12](../regels/r12.md)).

## Twee lezingen

| | Hoofdmodel | Alternatief |
|---|---|---|
| geluidsevent | `sosa:Stimulus` | emissie (`wk:Emissie`), studieobject |
| studieobject van de eventwaarnemingen | de meetpost | het geluidsevent |
| studieobject van de dagindicatoren | de meetpost | de meetpost |
| patroon | [Stimulus](../patronen/stimulus.md) | [Emissie als studieobject](../patronen/emissie.md), zoals de lozing in waterkwaliteit |
| de vraag die het best beantwoord wordt | wat krijgt deze plaats? | wat maakt deze vlucht? |

Het alternatief werkt één vlucht uit (TRA15N, vier emissies, zestien waarnemingen), met argumenten
voor en tegen, een tussenvorm (één emissie per vlucht, het event als monster) en discussievragen
voor de werkgroep. Status: beide *voorstel*.

## Diagram

```mermaid
--8<-- "src/main/input/geluidsmeetnet/geluidsmeetnet.mmd"
```

## Vergelijking met het alternatief

```mermaid
--8<-- "src/main/input/geluidsmeetnet/alternatief/geluidsmeetnet_vergelijking.mmd"
```

## Turtle

Het toetsdeel van het hoofdmodel (`geluidsmeetnet.ttl`, campagne M072-2, 275 KB) is te groot om
hier in te voegen: [op GitHub bekijken](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/geluidsmeetnet/geluidsmeetnet.ttl).

??? example "alternatief/geluidsmeetnet_emissie.ttl"

    ```turtle
    --8<-- "src/main/input/geluidsmeetnet/alternatief/geluidsmeetnet_emissie.ttl"
    ```
