# Kennisinventaris OSLOthema-SSNSOSA-VL

Doel: alle kennis in dit project in kaart brengen, zodat ze in een nieuw project herbruikbaar is.
Per item: **laag** (hoe algemeen) en **drager** (waar het naartoe moet).

Bronnen: `CLAUDE.md`, `.claude/commands/nieuw-voorbeeld.md`, de waterkwaliteit-documenten
(`stappenplan.md`, `beslisdocument.md`, `codelijsten.md`, `csor_iadopt.md`,
`featureofinterest.md`), de datavoorbeelden en het lokale Claude-geheugen
(`~/.claude/projects/-home-gehau-git-OSLOthema-SSNSOSA-VL/memory/`, niet in git).

Stand: 2026-10-11.

**Resultaat (2026-10-11):** de kennis staat in de kit [`milieuinfo/oslo-ld-kit`](https://github.com/milieuinfo/oslo-ld-kit) (in dit project als subtree `oslo-ld-kit/`, skills in `.claude/skills/`;
Brits Engels): de gids (`guide/`: linked data met R10/R15, SSN/SOSA met R1–R9 en R11–R14,
patronen, discussiedocument, oefening, diagrammen), zeven skills (W1–W6 en W10; W7–W9 zijn
onderdelen van de gids) en het SHACL-regelbestand (`rules/ssn-sosa-rules.ttl`). `CLAUDE.md` van dit
project is dun: projectprofiel, structuur, bestandsset en validatie, plus imports van de
gids. Wat hieronder "CM" heet, staat nu in de gids.

## Legende

| Laag | Betekenis |
|---|---|
| **LD** | algemeen linked data, geldt voor elk RDF-project |
| **SOSA** | SSN/SOSA 2023 met PROV-O, P-PLAN, QUDT, OWL-Time |
| **DOM** | een domein (waterkwaliteit, …) |
| **PROJ** | enkel dit repository; blijft hier |

| Drager | Betekenis |
|---|---|
| **MCP** | zit al in de `ld-vocab`-server (of hoort daar als tool) |
| **SHACL** | afdwingbaar: wordt een shape in een gedeeld regelbestand (`--shapes`) |
| **GIDS** | vraagt oordeel: modelleergids (tekst met voorbeelden) |
| **SKILL** | werkwijze: stappen, vragen, sjablonen |
| **CORPUS** | uitgewerkt voorbeeld met motivatie |
| **SCRIPT** | herbruikbaar hulpprogramma |
| **PATROON** | patroon dat domeinen overstijgt; patronencatalogus in de gids, met de voorbeelden die het gebruiken |
| **BLIJFT** | projectspecifiek |

Bron-afkortingen: CM = `CLAUDE.md`, NV = command `nieuw-voorbeeld`, BD = `beslisdocument.md`,
SP = `stappenplan.md`, CL = `codelijsten.md`, CI = `csor_iadopt.md`, GH = Claude-geheugen.

---

## 1. Algemeen linked data (LD)

| # | Kennis | Bron | Drager | Opmerking |
|---|---|---|---|---|
| L1 | Gezaghebbende basis-URI voor productiedata, `https://example.org/<domein>/` voor illustratie | CM R10 | GIDS | |
| L2 | Geen eigen resources in andermans namespace | MCP-sessie | **MCP** ✔ | `Resource minted in a vocabulary namespace` |
| L3 | `http`-IRI is de identifier, ook als de site naar `https` doorverwijst; `#` versus `/` | MCP-sessie | **MCP** ✔ | hint in `validate_file` |
| L4 | Bekend maar niet geladen vocabularium tegenover onbekende namespace | MCP-sessie | **MCP** ✔ | `--prefix-registry` |
| L5 | Geen blank nodes voor resources die extern gerefereerd worden; deterministische skolem-IRI's (`ex:interval-{obs-id}`, …) | CM R10, GH | GIDS (+ SHACL) | uitzondering: geometrie in een externe dataset, daar mag een blank node (GH) |
| L6 | Geen SKOS-relaties tussen klassen; SKOS-documentatieproperties (`skos:definition`, `scopeNote`) mogen wel | GH | **SHACL** | geldt voor ontologieën, niet voor data: vraagt een ontologie-lint (zie §7) |
| L7 | Codelijsten als SKOS; bestaande registers hergebruiken vóór nieuwe lijsten | SP §1, CL, BD A11 | GIDS | |
| L8 | Bestaande IRI's hergebruiken; nog niet finale externe IRI's via `rdfs:seeAlso` | BD A12 | GIDS | |
| L9 | Grote dataset: volledige versie apart, kleine representatieve subset om te valideren | GH | GIDS | het `.trig`-trucje zelf is PROJ (bulkvalidatie) |
| L10 | **Applicatieprofiel uit één bron**: OWL-restricties → gegenereerde SHACL, geen handgeschreven SHACL | BD A15 | GIDS + **MCP** ✔ | generator zit in de server |
| L11 | AP-beperkingen op **eigen subklassen**, nooit op hergebruikte klassen (anders gelden ze voor alle data) | BD A15 | GIDS | belangrijke, niet-evidente regel |
| L12 | SHACL valideert het niet-afgeleide model: data typeert de superklassen expliciet | BD A15, GH | GIDS | verklaart "Or at focusNode"-meldingen |
| L13 | Wat de OWL→SHACL-generator niet uitdrukt (keuze tussen properties, consistentie verzameling/leden) | BD A15 | GIDS | |
| L14 | Ontologie → UML-diagram | `scripts/ontologie_naar_uml.py` | SCRIPT (of MCP-tool) | |
| L15 | Bekende vals-positieven: OWLMiniReasoner, SHACL zonder inferentie | CM §4, GH | GIDS | hoort bij de documentatie van de server |
| L16 | Prefixconventies (`unit:` tegenover `qudt:`, vaste prefixlijst) | CM §10 | GIDS + MCP | projectprefixen kunnen een `--prefix-registry`-bestand worden |

## 2. SSN/SOSA en aanverwante vocabularia (SOSA)

| # | Kennis | Bron | Drager | Opmerking |
|---|---|---|---|---|
| S1 | Klasse-selectie infrastructuur (Platform, System, Sensor, Actuator, FOI, Sample, SpatialSample) | CM R1 | GIDS | |
| S2 | Verplichte properties per `sosa:Observation` (observedProperty, FOI, resultaat) | CM R2 | **SHACL** | |
| S3 | `qudt:numericValue`, niet `qudt:value` | CM R3, GH | **SHACL** | `qudt:value` bestaat wel; `lookup_term` vangt het niet |
| S4 | Resultaatstijl (QuantityValue of Result) niet mengen binnen één voorbeeld | CM R3 | SHACL (SPARQL-constraint) | |
| S5 | Wanneer drielaags (Planning/Deployment/Execution) | CM R4 | GIDS | |
| S6 | `sosa:hasInput` enkel op `sosa:Procedure`; `prov:used` op execution-niveau | CM R5 | **SHACL** | |
| S7 | ML-model als `prov:Entity`, de software als `sosa:Sensor` met `sosa:uses` | CM R6 | GIDS | |
| S8 | `sosa:hasInputValue` naar resultaten, nooit naar een observatie; `sosa:relatedObservation` naar de bronobservaties | CM R7, R13 | **SHACL** + MCP ✔ | `[MODEL INVALID]` vangt het al via disjunctie |
| S9 | Afgeleide observatie niet als `sosa:hasMember` in de broncollectie; verplichte properties expliciet | CM R13 | SHACL (SPARQL-constraint) | |
| S10 | Sampling-ketens met `sosa:isSampleOf`, `hasUltimateFeatureOfInterest` | CM R8, BD A4 | GIDS | |
| S11 | Niet-kalender TRS (`time:hasTRS`, TRS met `skos:prefLabel` en `skos:definition`) | CM R9 | GIDS + SHACL | |
| S12 | SpatialSample: drievoudige typering, `isSampleOf`, geometrie, FOI op de collectie naar het meetpunt | CM R11, BD A6 | GIDS + SHACL | |
| S13 | `time:Interval` voor periodes, half-open conventie | CM R12 | GIDS + SHACL | Interval heeft begin én einde |
| S14 | Tijdspatronen (resultTime, Instant, Interval, TRS) en het onderscheid phenomenonTime/resultTime | CM §5.7 | GIDS | |
| S15 | SSN 2023: `sosa:implements`, `sosa:hasProperty`, `sosa:Property` (niet `ssn:`/`ObservableProperty`) | GH | **MCP** ✔ | `lookup_term` geeft de suggestie |
| S16 | QUDT-eenheden zijn niet voorspelbaar (`unit:M`, `unit:CCY_EUR`): zoeken | NV | **MCP** ✔ | `search_terms` vindt individuen |
| S17 | Resultaat onder de rapportagegrens: `qudt:lowerBound`/`upperBound` in plaats van `numericValue` + teken | BD A3 | GIDS | algemeen bruikbaar QUDT-patroon |
| S18 | Staal als FOI, het bemonsterde ding als ultiem FOI; het FOI is tijdsloos | BD A4, A5 | GIDS | |
| S19 | Eenheid via een domeinregister met SKOS-mapping naar QUDT als QUDT ze niet kan uitdrukken (stofgekwalificeerd, "als N") | BD A2, CL §3.3, CM R3 | GIDS + SKILL (vraag 6) + MCP ✔ | mappings uit het register, nooit in de data |
| S20 | Variabele volgens I-ADOPT (eigenschap, object, matrix, constraints) | BD A16, CI | GIDS | |
| S21 | Kenmerken die in de tijd veranderen: op de observatie van dat jaar, of versies (`prov:specializationOf`) | BD A13 | GIDS | nog open |
| S22 | Inverse relaties opnemen voor query-efficiëntie | CM §5.9 | GIDS | |
| S23 | `p-plan:correspondsToStep`/`correspondsToVariable` op execution-niveau | CM §5.6, R13 | GIDS | |

## 3. Werkwijzen (SKILL)

| # | Werkwijze | Bron | Wat de skill moet bevatten |
|---|---|---|---|
| W1 | **Nieuw datavoorbeeld** | NV, CM §3, §5 | vijf vragen vooraf, bestandsset en volgorde, Turtle-skelet per architectuur, vocabulaire-check met MCP, validatie, eindchecklist |
| W2 | **Bestaande mapping herzien** | CM §8, NV vraag 4 | origineel bewaren, `_herzien`, Verbeterpunten (`origineel → gecorrigeerd → motivatie met spec`), vergelijkingsdiagram |
| W3 | **Brondata mappen naar een model** | SP, BD §0, CL | scope met de databeheerder; eerst de resultaten; bestaande registers eerst; de omzetting volledig scripten; na een beslissing alles opnieuw genereren en valideren |
| W4 | **Beslisdocument voor een standaardisatietraject** | BD §0 | per punt vraag, voorstel, verworpen alternatieven, gevolg, status (voorstel/open/beslist); gegroepeerd per beslisser (werkgroep, databeheer, registers, later) |
| W5 | **Ontologie of applicatieprofiel ontwerpen** | BD A15 | L10–L13; eigen subklassen; UML genereren; mapping oud AP → nieuw |
| W6 | **Ontologieën aligneren** | CI, `csor_iadopt_toets.py` | structurele vergelijking, kwantitatieve toets per element, knelpunten, voorstel |
| W7 | **Bespreking schrijven** (9 secties) | CM §5 | sjabloon; `### Waarom …?` met verworpen alternatief |
| W8 | **Trainingsopdracht** | CM §9, NV 2e | sjabloon met vier stappen en tijden |
| W10 | **Alternatieve mapping** ✔ | geluidsmeetnet, CM §8b (2026-10-11) | twee verdedigbare lezingen naast elkaar, geen herziening; submap `alternatief/`, verschillentabel, vergelijkingsdiagram, argumenten vóór/tegen, discussievragen, status, verwijzing in beide richtingen; na beslissing het andere als verworpen alternatief bewaren. In NV: optie bij vraag 4 + actief signaleren |
| W9 | **Mermaid-diagram** | CM §6 | kleurpalet, nesting plat/drielaags, labels; deterministisch te controleren (zie §7) |

## 4. Voorbeelden als corpus (CORPUS)

Elk voorbeeld toont patronen die een nieuw project als referentie kan opvragen.

| Voorbeeld | Patronen |
|---|---|
| `grondwaterpeilmetingen` | plat model, blank-node resultaten (`qudt:QuantityValue` / `prov:Entity`), persistente DOV-IRI's |
| `paleo` | `qudt:QuantityValue` met IRI, niet-kalender TRS (BP), afgeleide observaties |
| `Nigella-Lawson-Brownies` | drielaags procesmodel |
| `EnergieManagementSystem` | herzieningsworkflow, vier scenario's (bron is overgenomen; niet als norm gebruiken) |
| `erosiepoel` | manuele veldmeting, `ObservationCollection`, opdracht |
| `temperatuur-raam` | drielaags met sensor en actuator, opdracht |
| `elektrisch-raam` | meerdere sensoren, afgeleide observatie, actuatie |
| `verkeersmetingen` | SpatialSample, `time:Interval`, afgeleide dagsom, opdracht |
| `geluidsmeetnet` (+ `alternatief/`) | CSV-export (Aerovision), events en dagindicatoren, twee modelvarianten |
| `r-factor` | grote dataset (`.trig` + subset), skolem-IRI's, R-script |
| `waterkwaliteit` | codelijsten (CSOR, NACE-BEL), sampling-ketens, rapportagegrens, AP uit ontologie, I-ADOPT, beslisdocument |

## 4b. Patronen over domeinen heen (PATROON)

Begin van een patronencatalogus voor de modelleergids. Per patroon: de voorbeelden die het
gebruiken, zodat een nieuw domein bewust kan kiezen tussen aansluiten en een eigen lezing (met
eventueel een alternatieve mapping, W10).

| Patroon | Kern | Gebruikt in |
|---|---|---|
| Emissie als FOI | de emissie is `prov:Entity` en `sosa:FeatureOfInterest`, `prov:wasGeneratedBy` een activiteit (bedrijfsactiviteit, vlucht); meetplaats via `prov:atLocation` | waterkwaliteit (lozing, BD A5, A14), geluidsmeetnet `alternatief/` |
| Stimulus | het voorval dat een sensor laat meten is `sosa:Stimulus` (`sosa:wasOriginatedBy`); FOI is de plaats waar het effect gemeten wordt | geluidsmeetnet (hoofdmodel) |
| Staal → ultiem FOI | staal als FOI, het bemonsterde object via `isSampleOf` / `hasUltimateFeatureOfInterest` | waterkwaliteit (BD A4), paleo |
| Ruimtelijk monster | meetpunt als `sosa:SpatialSample` van een groter gebied (R11) | verkeersmetingen, waterkwaliteit (meetplaats), geluidsmeetnet |
| Afgeleide observatie | `hasInputValue` naar resultaten, `relatedObservation` naar bronnen, niet in de broncollectie (R7, R13) | verkeersmetingen (dagsom), geluidsmeetnet (Lden), paleo, waterkwaliteit |
| Rapportagegrens | `qudt:lowerBound`/`upperBound` in plaats van `numericValue` + teken | waterkwaliteit (BD A3) |

## 5. Domeinkennis (DOM)

Waterkwaliteit: BD A1, A5–A10, A13–A16, deel B–D, `featureofinterest.md`, `codelijsten.md`,
`csor_iadopt.md`, de ontologie `waterkwaliteit.ttl` en de scripts. Dit is als geheel
meeneembaar naar een OSLO-traject waterkwaliteit. Wat algemeen is, staat hierboven al apart
(S17–S21, L10–L13, W3–W6).

Externe afhankelijkheden die een nieuw project moet kennen: `~/git/csor`, `~/git/RIE-IEPR`,
`~/git/shapefile_to_rdf` (VHA-waterlopen, met de gekende IRI-fout), `codelijst-matrix`,
`codelijst-observatieprocedure`.

## 6. Blijft in dit project (PROJ)

- CM §2 (paden), §3 (bestandsset, `source/`-opmerking), §4 (Scala-pipeline, `generated-shapes.ttl` nooit bewerken; pipeline geschrapt op 2026-10-23, vervangen door ld-mcp).
- `.trig` om de bulkvalidatie te omzeilen (de techniek; het principe is L9).
- EMS-bronnen zijn overgenomen en niet normatief (GH).
- Waterkwaliteit-scope en betrokken personen (GH).

---

## 7. Wat dit oplevert voor de dragers

**SHACL-regelbestand** ✔ (2026-10-11): `src/main/shacl/modelleerregels.ttl`, via `--shapes` in
`.mcp.json`. Dekt R2 (met erfenis via de collectie; sensor/procedure als warning), R3 (`qudt:value`),
R5, R7, R9 (warning), R11, R12 (interval, deprecated `inXSDDateTime`, datatype), R13 en R15. Getest:
geen violations op de bestaande voorbeelden, elke regel slaat aan op een foutbestand. Niet gedaan:
S4 (stijlen mengen) en L5 (blank nodes in grote datasets): niet eenduidig te toetsen.
Oorspronkelijk plan: **SHACL-regelbestand** (nieuw, gedeeld): S2, S3, S4, S6, S8, S9, S11, S12, S13, en L5 als
optionele waarschuwing. Ongeveer de helft van R1–R15 wordt daarmee afgedwongen in plaats van
onthouden. S4 en S9 vragen SPARQL-constraints (`sh:sparql`); Jena SHACL ondersteunt die.

**Nieuwe MCP-tools** (deterministisch, nu proza):
- ontologie-lint voor L6 (SKOS op klassen), L11 (restricties op hergebruikte klassen);
- Mermaid-lint voor W9 (elke node een stijl, palet, nesting);
- voorbeelden opzoeken in het corpus (§4): fragment + motivatie uit `bespreking.md`.

**Modelleergids**: de GIDS-items, in drie delen (LD, SOSA, DOM), met verwijzingen naar het corpus.

**Skills**: W1–W9, die naar de gids en de MCP-tools verwijzen in plaats van regels te herhalen.

## 8. Tegenstrijdigheden en verouderde punten (eerst rechtzetten)

1. ✔ **CM gebruikte `sosa:ObservableProperty`** (§5 sectie 5, §6 palet). Bestaat niet in de
   geladen SSN 2023; het is `sosa:Property` (GH). Rechtgezet (2026-10-11) in CM, NV, de 11
   besprekingen, `grondwaterpeilmetingen.mmd` en de drie opdrachten (ook `ActuableProperty`,
   die evenmin bestaat).
2. ✔ **CM R12 en de tijdtabel (§5.7) schreven `time:inXSDDateTime` voor**, die in OWL-Time
   deprecated is. Rechtgezet (2026-10-11): `time:inXSDDateTimeStamp`; zonder tijdzone in de bron
   Belgische tijd (`+01:00`/`+02:00`), vermeld in bespreking §7. Omgezet: 110 waarden in
   verkeersmetingen, erosiepoel, EMS `_herzien` en waterkwaliteit (via de scripts), plus de
   teksten en `frame.json`.
3. ✔ **R3 (eenheid rechtstreeks uit QUDT) botste met BD A2** (eenheid via CSOR). Opgelost
   (2026-10-11): R3 kent twee bronnen (QUDT of domeinregister), te kiezen met vraag 6 in NV.
   SKOS-mappings naar QUDT komen uit het register, niet uit de data; ontbrekende mappings zijn
   een punt voor registerbeheer. De CSOR-eenhedenlijst is geladen (360 eenheden, 163 met een
   QUDT-mapping, alle doelen bestaan); `lookup_term` toont nu SKOS-mappings.
4. ✔ **Originele bestanden:** CM §3/§8 zei `source/<naam>.ttl`, NV `source/<naam>.ttl.bak`.
   Opgelost (2026-10-11): ontvangen formaat behouden, Turtle als `source/<naam>.trig` (geldige
   RDF voor `riot` en `validate_file`, de pipeline slaat het over). De vier EMS-bronbestanden en
   `getSource.sh` zijn aangepast.
5. ✔ **CM §2 miste voorbeelden.** Aangevuld (2026-10-11) met `geluidsmeetnet`, `r-factor`,
   `waterkwaliteit` en het nog niet uitgewerkte `PGD_geschiktheidskaart`.
6. ✔ **Kennis stond enkel in het lokale geheugen (GH).** Overgezet naar CLAUDE.md (2026-10-11):
   `qudt:numericValue` (R3), skolem-IRI's en de uitzondering (R10), SSN/SOSA 2023-termen (R14,
   nieuw), geen SKOS-relaties op klassen (R15, nieuw), grote datasets als `.trig` + subset en
   SHACL zonder inferentie (§4). De overeenkomstige geheugennotities zijn verwijderd.
