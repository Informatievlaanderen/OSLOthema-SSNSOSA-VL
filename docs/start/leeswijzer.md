# Leeswijzer

Het werk is opgebouwd als leerpad: van het waarom (I), over de samenhang van de vocabularia (II)
en het modelleren per vraag (III), naar regels (IV), patronen (V), werkwijze (VI), casussen (VII)
en oefeningen (VIII). Je hoeft het niet van voor naar achter te lezen.

## Routes

| Je bent … | Lees eerst | Dan |
|---|---|---|
| **nieuw in linked data voor waarnemingen** | [I. Waarom](../inleiding/index.md), [De kernvocabularia](../inleiding/kernvocabularia.md) | [Casus erosiepoel](../casussen/erosiepoel.md), [III. Modelleren](../modelleren/index.md), [Oefening erosiepoel](../oefenen/erosiepoel.md) |
| **modelleerder met een concrete dataset** | [III. Modelleren](../modelleren/index.md), [Werkwijze](../werkwijze/index.md) | de [patronen](../patronen/index.md), de casus die het dichtst bij je domein ligt ([overzicht](../casussen/index.md)) |
| **ontoloog** | [II. Samenhang](../samenhang/index.md), [Een alignment vinden en beoordelen](../samenhang/alignment-vinden.md) | [R15](../regels/r15.md), [R16](../regels/r16.md), [R17](../regels/r17.md), [Ontologie en toepassingsprofiel](../werkwijze/ontologie.md) |
| **data-architect** | [Plaats binnen OSLO](../inleiding/oslo.md), [R17](../regels/r17.md) | [Waarneming of record?](../modelleren/record.md), [IRI's](../modelleren/iris.md), [Codelijsten en registers](../modelleren/codelijsten.md) |
| **lid van een OSLO-werkgroep** | [Het beslisdocument](../werkwijze/beslisdocument.md) | de casussen [waterkwaliteit](../casussen/waterkwaliteit.md), [overstort](../casussen/overstort.md) en [geluidsmeetnet](../casussen/geluidsmeetnet.md) |
| **lesgever** | [VIII. Oefenen](../oefenen/index.md) | de casussen die bij de oefeningen horen |

## Conventies in de tekst

**Termen.** Een klasse of eigenschap staat in code met haar gebruikelijke prefix:
`sosa:Observation`, `prov:used`. De Nederlandse benaming volgt de labels van de
Nederlandse vertaling in dit project (*waarneming*, *studieobject*, *monster*); de
[woordenlijst](../bijlagen/woordenlijst.md) zet ze naast de Engelse. Waar het Engelse woord in
Vlaanderen gangbaar is (*feature of interest*, *sensor*), staat het er soms naast.

**Regels en patronen** hebben vaste nummers en namen (R1–R18), dezelfde als in de
[modelleergids](https://github.com/milieuinfo/oslo-ld-kit/tree/main/guide) waar ze normatief
beschreven staan. Elke regelpagina bevat die normatieve tekst (Engels) in een uitklapbaar kader.

**Kaders.**

!!! regel "Regel"
    Een regel uit de gids, kort samengevat.

!!! valkuil "Valkuil"
    Een fout die in de praktijk terugkomt, meestal uit een herziene mapping.

!!! hulpmiddel "Hulpmiddel"
    Waar een hulpmiddel het werk verlicht. Nooit een voorwaarde: elke stap kan ook zonder.

**Diagrammen** volgen één kleurconventie ([Diagrammen](../werkwijze/diagrammen.md)):

| Kleur | Wat |
|---|---|
| <span class="swatch" style="background:#60c4e4"></span> blauw | infrastructuur en studieobject: platform, systeem, sensor |
| <span class="swatch" style="background:#e54b89"></span> roze | uitvoering: waarneming, actuatie, bemonstering, activiteit |
| <span class="swatch" style="background:#f8b622"></span> oranje | waarden en tijdstippen: resultaat, entiteit, `time:Instant` |
| <span class="swatch" style="background:#c6a0f5"></span> lila | procedure |
| <span class="swatch" style="background:#7f59ae"></span> paars | plan en stap (P-PLAN) |
| <span class="swatch" style="background:#fe7130"></span> oranjerood | eigenschap of variabele |

**Turtle.** Fragmenten laten de `@prefix`-regels weg; de [prefixtabel](../bijlagen/prefixen.md)
geeft ze. `ex:` staat voor een illustratieve namespace onder `https://example.org/`.
