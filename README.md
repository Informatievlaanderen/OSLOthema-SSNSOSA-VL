# OSLO SSN SOSA VL

**Verantwoordelijke organisatie:** Agentschap Digitaal Vlaanderen  
**Status:** Zonder status  
**Type toepassing:** Aanbevolen (vrijwillig)  
**Categorie:** TBD

## Inleiding

Het SSN SOSA VL‑model (Vlaamse Standaard voor sensor, observatie, staalname en actuator) biedt een gestandaardiseerd kader voor het beheren en uitwisselen van sensor‑, observatie‑, staalname‑ en actuatorgegevens in Vlaanderen. De focus ligt op de effectieve representatie en toepassing van internationale standaarden binnen de thematiek van metingen, monitoring, bemonstering en automatisering. Het model sluit nauw aan bij het W3C/OGC‑model SSN SOSA en is afgestemd op complementaire modellen zoals PROV‑O, QUDT, en waar relevant p‑plan en GeoSPARQL.

Binnen het kader worden verschillende types entiteiten geclassificeerd die relevant zijn voor:

- sensoren
- observaties
- staalnames
- actuatoren

Daarnaast faciliteren de datavoorbeelden de integratie van semantische en procedurele referenties, waaronder ontwerpprincipes, best practices en afspraken over modellering. Dit resulteert in een eenduidige en goed gedocumenteerde standaard voor het vastleggen van gegevens binnen uiteenlopende domeinen.

## Scope

Het kader vormt het centrale referentiepunt voor de beschrijving en structurering van:

- observaties
- metingen
- staalnames
- systemen
- procedures
- actuatoren

Het ondersteunt verschillende types gegevensbronnen, zoals:

- sensornetwerken
- veldmetingen
- laboratoriumanalyses
- geautomatiseerde meetsystemen

Binnen dit kader worden diverse modelelementen onderscheiden, waaronder Observations, Samples, Sensors, Actuators en Procedures. Deze elementen maken een uniforme en interpreteerbare gegevensstructuur mogelijk.

## Modellering en provenance

Het model maakt het mogelijk om relaties tussen observaties en hun context gedetailleerd te analyseren. Via koppelingen met onder andere PROV‑O en QUDT kunnen herkomst, gebruikte procedures, eenheden, onzekerheden en kwaliteitsaspecten nauwkeurig worden vastgelegd. Dit is essentieel voor het beoordelen van betrouwbaarheid, reproduceerbaarheid en vergelijkbaarheid van meetgegevens.

Verder biedt het kader een duidelijke manier om de evolutie, uitvoering en procedurele stappen rond observaties en staalnames te documenteren. Belangrijke fasen zoals:

- dataverzameling
- validatie
- kwaliteitscontrole
- verwerking

kunnen formeel worden beschreven. Dit zorgt voor een transparante en volledige documentatie van gebruikte methoden en processen.

## Datavoorbeelden

De repository bevat uitgewerkte datavoorbeelden per domein onder `src/main/input/`. Elk voorbeeld omvat Turtle-data, een Mermaid-diagram, een README en een `bespreking.md` met formele conceptmapping.

| Domein | Beschrijving | Architectuur |
|---|---|---|
| [`grondwaterpeilmetingen`](src/main/input/grondwaterpeilmetingen/) | DOV grondwaterfiltermetingen | Plat model |
| [`paleo`](src/main/input/paleo/) | Paleoklimaatdata met afgeleide observaties en niet-kalender tijdreferentiesysteem | Plat model met afgeleide observaties |
| [`Nigella-Lawson-Brownies`](src/main/input/Nigella-Lawson-Brownies/) | Procesmodellering als demonstratie van p‑plan/SSN‑SOSA‑PROV‑O alignment | Drielaags (Planning/Deployment/Execution) |
| [`EnergieManagementSystem`](src/main/input/EnergieManagementSystem/) | Vier HVAC/energie-scenario's met herzieningsworkflow | Drielaags |
| [`erosiepoel`](src/main/input/erosiepoel/) | Manuele veldmeting met ObservationCollection | Plat model |
| [`temperatuur-raam`](src/main/input/temperatuur-raam/) | Drielaags met sensor en actuator, vereenvoudigd (2 metingen) | Drielaags |
| [`elektrisch-raam`](src/main/input/elektrisch-raam/) | Drielaags met meerdere sensoren, afgeleide observatie en actuatie | Drielaags |
| [`verkeersmetingen`](src/main/input/verkeersmetingen/) | Plat model met SpatialSample, time:Interval en afgeleide dagsom | Plat model |

De sub-scenario's van EnergieManagementSystem:

| Scenario | Beschrijving |
|---|---|
| [`DatavoorbeeldIsolatieadvies`](src/main/input/EnergieManagementSystem/DatavoorbeeldIsolatieadvies/) | Warmteverlies observatie — geneste SOSA-structuur |
| [`DatavoorbeeldPreHeatingHvac`](src/main/input/EnergieManagementSystem/DatavoorbeeldPreHeatingHvac/) | HVAC pre-heating met p‑plan/SSN‑SOSA‑PROV‑O alignment |
| [`DatavoorbeeldSGerealiseerdeBesparing`](src/main/input/EnergieManagementSystem/DatavoorbeeldSGerealiseerdeBesparing/) | Gerealiseerde energiebesparing |
| [`DatavoorbeeldStilleggingProductielijn`](src/main/input/EnergieManagementSystem/DatavoorbeeldStilleggingProductielijn/) | Productielijn stillegging op basis van elektriciteitsprijzen |

## In deze repository

```
src/main/input/<domein>/     Datavoorbeelden per domein (TTL, Mermaid, README, bespreking.md)
src/main/resources/          OWL-ontologieën (SSN/SOSA 2023, PROV-O, p-plan, QUDT, TIME, …)
src/main/output/             Gegenereerde output na inferentie (Turtle, JSON-LD)
src/main/scala/              Scala-evaluatiepipeline
```

De pipeline wordt uitgevoerd met:

```bash
mvn compile exec:java
```

## Issues

Via de tab [issues](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/issues) kan je opmerkingen en feedback over het model geven.

## Verslagen en presentaties

De verslagen en presentaties van dit traject kan je terugvinden op het [Standaardenregister](https://data.vlaanderen.be/standaarden).

## Publicaties

| Naam | Status | Uitgiftedatum | AP | VOC | IMP |
|---|---|---|---|---|---|
| SSN SOSA VL | Zonder status | — | | | |
