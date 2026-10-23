# VII. Casussen

Veertien uitgewerkte voorbeelden uit Vlaamse domeinen. Elke casus toont de vraag, de keuzes, de
valkuilen en de alignments die ze gebruikt, met het diagram en de Turtle rechtstreeks uit de
repository. De volledige README en bespreking staan op GitHub; de casuspagina is de leeswijzer
erbij.

## Leesvolgorde

Van eenvoudig naar complex. Wie de eerste vijf gelezen heeft, kent de kern.

| # | Casus | Wat je leert |
|---|---|---|
| 1 | [Erosiepoel](erosiepoel.md) | het skelet van een waarneming; een mens als sensor; een ontvangen versie herzien |
| 2 | [Verkeersmetingen](verkeersmetingen.md) | ruimtelijk monster, intervallen, een afgeleide dagsom |
| 3 | [Temperatuur en raam](temperatuur-raam.md) | het drielaagse model in zijn eenvoudigste vorm, met een actuatie |
| 4 | [Paleoklimaat](paleo.md) | monsterketens, niet-kalendertijd, de fout *waarneming als inputwaarde* |
| 5 | [Waterkwaliteit](waterkwaliteit.md) | echte brondata in fases, registers, rapportagegrens, emissie, een beslisdocument |
| 6 | [Overstort](overstort.md) | een LDES-mapping herzien: record of waarneming, vocabulariumkeuze, twee lezingen |
| 7 | [Geluidsmeetnet](geluidsmeetnet.md) | stimulus of emissie, ketens van afgeleiden, een grote dataset |

Daarna, naar interesse:

| Casus | Wat je leert |
|---|---|
| [Elektrisch raam](elektrisch-raam.md) | drielaags met meerdere sensoren, een afgeleide waarneming en een actuatie |
| [Grondwaterpeilmetingen](grondwaterpeilmetingen.md) | een XML-bron omzetten met XSLT; filters als systemen |
| [R-factor](r-factor.md) | een gescripte grote dataset, skolem-IRI's, een eigen eenheid |
| [Geschiktheidskaart PGD](pgd.md) | een kaartlaag als waarneming; QGIS-modellen als plan en sensor |
| [Brownies](brownies.md) | het volledige drielaagse patroon met deelplannen, uitgelegd met een recept |
| [Energiemanagement](ems.md) | HVAC-scenario's, een ML-model als artefact, herzieningen |
| [VLAREM-rubrieken](vlarem.md) | QUDT en SKOS buiten SSN/SOSA: een norm is geen waarneming |

## Matrix

| Casus | Model | Patronen | Kernregels | Alignments | Herziening / alternatief | Oefening |
|---|---|---|---|---|---|---|
| [erosiepoel](erosiepoel.md) | plat | — | R1, R2, R3, R12, R14 | PROV, QUDT, Time | herziening | ✔ |
| [verkeersmetingen](verkeersmetingen.md) | plat | ruimtelijk monster, afgeleide | R7, R11, R12, R13 | PROV, QUDT, GeoSPARQL, Time | — | ✔ |
| [temperatuur-raam](temperatuur-raam.md) | drielaags | — | R4, R5 | P-PLAN, PROV | — | ✔ |
| [elektrisch-raam](elektrisch-raam.md) | drielaags | afgeleide | R4, R5, R13 | P-PLAN, PROV, QUDT | — | |
| [paleo](paleo.md) | plat | monster, afgeleide | R7, R8, R9 | PROV, Time | gecorrigeerd | |
| [grondwaterpeilmetingen](grondwaterpeilmetingen.md) | plat | — | R1, R3 | QUDT, GeoSPARQL | — | |
| [r-factor](r-factor.md) | plat | ruimtelijk monster, afgeleide | R10, R11, R12, R13 | QUDT, GeoSPARQL, Time | — | |
| [geluidsmeetnet](geluidsmeetnet.md) | plat | stimulus / emissie, ruimtelijk monster, afgeleide | R4, R11, R12, R13, R17 | PROV, QUDT, GeoSPARQL, Time | alternatief | |
| [waterkwaliteit](waterkwaliteit.md) | plat | monster, emissie, ruimtelijk monster, afgeleide, rapportagegrens | R3, R8, R10, R11, R13, R15, R17 | PROV, QUDT, register–QUDT, register–I-ADOPT | — | |
| [overstort](overstort.md) | plat | emissie (alternatief) | R10, R12, R16, R17 | PROV, GeoSPARQL, Time, SAREF | herziening, alternatief | |
| [pgd](pgd.md) | drielaags | ruimtelijk monster, afgeleide | R4, R11, R13 | P-PLAN, PROV, QUDT | — | |
| [brownies](brownies.md) | drielaags | — | R4, R5 | P-PLAN, PROV | — | |
| [ems](ems.md) | drielaags | — | R5, R6, R16 | P-PLAN, PROV, SAREF | herzieningen | |
| [vlarem](vlarem.md) | geen SOSA | — | R3, R15, R17 | QUDT | herziening, alternatief | |
