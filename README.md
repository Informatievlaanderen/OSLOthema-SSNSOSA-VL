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

De repository bevat uitgewerkte datavoorbeelden per domein onder `src/main/input/`. Een voorbeeld
omvat Turtle-data, een Mermaid-diagram, een README en meestal een `bespreking.md` die de
modelleerkeuzes in negen vaste secties toelicht. Sommige voorbeelden hebben daarnaast:

- een **oefening** (`opdracht.md`) voor workshops;
- een **herziening** (`<naam>_herzien.ttl`) van een ontvangen mapping met modelleerfouten, met de
  verbeterpunten in de README en het origineel in `source/`;
- een **alternatief** (`alternatief/`): een tweede verdedigbare lezing van dezelfde data, ter
  beslissing voor de werkgroep;
- een **beslisdocument** (`beslisdocument.md`) met modelleerkeuzes voor een OSLO-traject.

| Domein | Beschrijving | Architectuur | Extra |
|---|---|---|---|
| [`grondwaterpeilmetingen`](src/main/input/grondwaterpeilmetingen/) | DOV-grondwaterfiltermetingen | Plat model | bespreking |
| [`paleo`](src/main/input/paleo/) | Paleoklimaatdata met afgeleide observaties en een niet-kalender tijdreferentiesysteem | Plat model met afgeleide observaties | |
| [`Nigella-Lawson-Brownies`](src/main/input/Nigella-Lawson-Brownies/) | Procesmodellering als demonstratie van de p‑plan/SSN‑SOSA‑PROV‑O-alignering | Drielaags (Planning/Deployment/Execution) | |
| [`EnergieManagementSystem`](src/main/input/EnergieManagementSystem/) | Vier HVAC/energiescenario's | Drielaags | herzieningen |
| [`erosiepoel`](src/main/input/erosiepoel/) | Manuele veldmeting met ObservationCollection | Plat model | bespreking, oefening |
| [`temperatuur-raam`](src/main/input/temperatuur-raam/) | Sensor en actuator, vereenvoudigd (2 metingen) | Drielaags | bespreking, oefening |
| [`elektrisch-raam`](src/main/input/elektrisch-raam/) | Meerdere sensoren, afgeleide observatie en actuatie | Drielaags | bespreking |
| [`verkeersmetingen`](src/main/input/verkeersmetingen/) | Fietstellingen met SpatialSample, `time:Interval` en afgeleide dagsom | Plat model | bespreking, oefening |
| [`geluidsmeetnet`](src/main/input/geluidsmeetnet/) | Geluidsevents en dagindicatoren rond Brussels Airport (Aerovision); het geluidsevent als stimulus | Plat model, gescript | bespreking, alternatief (geluidsevent als emissie) |
| [`r-factor`](src/main/input/r-factor/) | Neerslagerosiviteit (RUSLE R-factor) van 53 KMI/VMM-stations: jaar-, maand- en 15-daagse waarden | Plat model, gescript | bespreking |
| [`waterkwaliteit`](src/main/input/waterkwaliteit/) | VMM-meetresultaten (concentraties, vrachten, debieten) met CSOR-codelijsten, staalnameketen, rapportagegrens en een applicatieprofiel | Plat model, gescript | beslisdocument |
| [`overstort`](src/main/input/overstort/) | Overstortsensoren en -events van Aquafin (LDES), [issue #1](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/issues/1) | Plat model | herziening, bespreking, alternatief (overstorting als emissie) |

[`PGD_geschiktheidskaart`](src/main/input/PGD_geschiktheidskaart/) bevat ontvangen materiaal
(geschiktheidskaart voor peilgestuurde drainage) dat nog niet gemodelleerd is.

De sub-scenario's van EnergieManagementSystem:

| Scenario | Beschrijving |
|---|---|
| [`DatavoorbeeldIsolatieadvies`](src/main/input/EnergieManagementSystem/DatavoorbeeldIsolatieadvies/) | Warmteverliesobservatie, geneste SOSA-structuur |
| [`DatavoorbeeldPreHeatingHvac`](src/main/input/EnergieManagementSystem/DatavoorbeeldPreHeatingHvac/) | HVAC-voorverwarming met p‑plan/SSN‑SOSA‑PROV‑O-alignering |
| [`DatavoorbeeldSGerealiseerdeBesparing`](src/main/input/EnergieManagementSystem/DatavoorbeeldSGerealiseerdeBesparing/) | Gerealiseerde energiebesparing |
| [`DatavoorbeeldStilleggingProductielijn`](src/main/input/EnergieManagementSystem/DatavoorbeeldStilleggingProductielijn/) | Stillegging van een productielijn op basis van elektriciteitsprijzen |

**`.ttl` en `.trig`.** De pipeline verwerkt alle `.ttl`-bestanden onder `src/main/input/` en slaat
`.trig` over. Ontvangen bronbestanden in Turtle staan daarom als `source/<naam>.trig`, en een grote
dataset staat volledig in `<naam>.trig` met een kleine `<naam>.ttl` als validatiesubset
(`geluidsmeetnet`, `r-factor`, `waterkwaliteit`).

## Modelleerregels

De modelleerregels (R1–R15), de terugkerende patronen en de werkwijzen staan in de kit
[`milieuinfo/oslo-ld-kit`](https://github.com/milieuinfo/oslo-ld-kit), als git-subtree in
`oslo-ld-kit/`:

- de gids in `oslo-ld-kit/guide/` (IRI's, SSN/SOSA 2023, tijd, eenheden, patronen, bespreking,
  diagrammen, oefeningen);
- de controleerbare regels als SHACL in `oslo-ld-kit/rules/ssn-sosa-rules.ttl`;
- de skills voor Claude Code, gekopieerd naar `.claude/skills/` (nieuw voorbeeld, herziening,
  alternatief, brondata mappen, beslisdocument, ontologie ontwerpen, ontologieën aligneren).

Een nieuwe algemene regel hoort in de kit, niet in deze repository.

## In deze repository

```
src/main/input/<domein>/     Datavoorbeelden per domein (Turtle, Mermaid, README, bespreking.md)
src/main/resources/          OWL-ontologieën (SSN/SOSA 2023, PROV-O, p-plan, QUDT, OWL-Time,
                             GeoSPARQL, SAREF, waterkwaliteit, CSOR-eenheden, …) en de
                             SSN/SOSA-uitlijningen sosa-prov en sosa-saref
src/main/output/             Gegenereerde output na inferentie (Turtle, JSON-LD); niet in git
src/main/scala/              Scala-evaluatiepipeline
oslo-ld-kit/                 Gids, regels en skills (git-subtree)
.claude/                     Skills en het commando /nieuw-voorbeeld voor Claude Code
CLAUDE.md                    Projectprofiel voor Claude Code
```

## Valideren

**Eén bestand** valideer je met de MCP-server `ld-vocab`
([`milieuinfo/ld-mcp`](https://github.com/milieuinfo/ld-mcp)), in Claude Code als
`validate_file`. Die controleert in één stap:

- of elke term bestaat in de geladen ontologieën;
- domein-, bereik- en subproperty-inferentie;
- OWL-consistentie;
- SHACL, met de shapes uit de ontologieën en de regels uit de kit.

De server staat in `.mcp.json` en verwacht de jar in `tools/`:

```bash
curl -L --create-dirs -o tools/ld-mcp-vocab.jar \
  https://github.com/milieuinfo/ld-mcp/releases/latest/download/ld-mcp-vocab.jar
```

Dat vraagt Java 21 of later.

**De volledige pipeline** is enkel nodig voor de output in `src/main/output/` of een bijgewerkte
`src/main/resources/generated-shapes.ttl`:

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
