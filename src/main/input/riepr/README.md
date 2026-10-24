# RIE-IEPR — integraal milieujaarverslag van één exploitatie

Herziening van de RDF-export van RIE-IEPR voor het integraal milieujaarverslag (IMJV) 2021 van
AGC Glass Europe, vestiging Mol (exploitatie `01787986000160`). RIE-IEPR beschrijft per
exploitatie de processen (activiteiten, zuivering, uitstoot, lozing, grondwateronttrekking), de
installaties en punten die ze uitvoeren, en de waarden die de exploitant jaarlijks aangeeft:
debieten, concentraties en vrachten van stoffen, en kenmerken van emissiepunten en putten.

Samen met de data is ook de ontologie herzien, `riepr.ttl` (v1.0.1), omdat ze zelf termen
gebruikt die niet in SSN/SOSA 2023 staan.

## Bron

Ontvangen materiaal in `source/`, ongewijzigd (Turtle als `.trig`, zie `CLAUDE.md` §4):

| Bestand | Inhoud |
|---|---|
| `source/mjv_plan.trig` | planlaag: 34 processen (`riepr:Proces`) en hun procesvariabelen |
| `source/mjv_deployment.trig` | exploitant, exploitatielocatie, exploitatie 2021, installaties, emissie-, lozings-, onttrekkings- en meetpunten, filters |
| `source/mjv_execution.trig` | 75 observaties met 118 resultaten: kenmerken van punten en filters, en debieten, concentraties en vrachten van twee lozingen |
| `source/riepr.trig` | de ontologie `riepr.ttl` v1.0.1 zoals ontvangen ([`milieuinfo/RIE-IEPR`](https://github.com/milieuinfo/RIE-IEPR)) |

Herzien en geladen in `src/main/resources/`:

| Bestand | Inhoud |
|---|---|
| `be/vlaanderen/omgeving/data/ns/riepr/riepr.ttl` | de herziene ontologie (zie *Verbeterpunten aan de ontologie*) |
| `be/vlaanderen/omgeving/data/id/conceptscheme/riepr/rie-iepr.ttl` | de RIE-IEPR-codelijsten uit [`milieuinfo/codelijst-rie-iepr`](https://github.com/milieuinfo/codelijst-rie-iepr) (`src/main/resources/…/rie-iepr/rie-iepr.ttl`, commit `49c3de5` van 23 oktober 2026): statussen, installatie- en emissiepunttypes, eigenschappen, bepalingsmethodes |

## Transformatie

Bij RIE-IEPR: een export uit de RIE-IEPR-databank naar drie Turtle-bestanden, één per laag. Hier:
geen script. `riepr_herzien.ttl` is met de hand afgeleid uit de drie bronbestanden.

## Mappingkeuzes

Drielaags (R4): het proces van de exploitatie in 2021 is een `p-plan:Plan` met stappen per
activiteit, zuivering, uitstoot en lozing (PLANNING); de exploitatie 2021 is een `sosa:Deployment`
van de installaties en punten op de exploitatielocatie (DEPLOYMENT); de aangegeven waarden zijn
observaties (EXECUTION). De lozing is als `riepr:Emissie` de feature of interest (patroon
*Emissie als studieobject*); de jaarvracht is een afgeleide observatie uit concentratie en
jaardebiet.

`riepr_herzien.ttl` is een representatieve subset:

- **lucht:** etslijn 2 (installatie `activiteit/19105`) → gaswasser (`zuiveringsapparaat/13179`)
  → emissiepunt 13005, met diameter en hoogte van het emissiepunt;
- **water:** vormen en bewerken van vlakglas (`activiteit/323`) → lozingspunt LP01 (2400006),
  met het jaardebiet, de concentratie zink en de daaruit berekende jaarvracht zink.

De grondwaterkant (vijf pompputten, een peilput, filters met diepte, lengte en diameter) volgt
hetzelfde patroon als de kenmerken van het emissiepunt en is niet opgenomen.

## Diagram

- `riepr_herzien.mmd`: het herziene model.
- `riepr_vergelijking.mmd`: origineel en herziening naast elkaar.

## Outputbestanden

| Bestand | Inhoud |
|---|---|
| `riepr_herzien.ttl` | herziene subset (plan, exploitatie, systemen, lozing, observaties) |
| `riepr_herzien.mmd` | diagram van de herziene versie |
| `riepr_vergelijking.mmd` | vergelijkingsdiagram |
| `bespreking.md` | bespreking in negen secties |
| `opdracht.md` | oefening |

## Gebruik

```bash
riot --validate source/*.trig riepr_herzien.ttl
```

Valideren met `mcp__ld-vocab__validate_file` op `src/main/input/riepr/riepr_herzien.ttl`.

## Verbeterpunten aan de data

Diagnose van de bronbestanden met `validate_file`: `mjv_plan.trig` 37 fouten, `mjv_deployment.trig`
124 fouten en 12 verdachte meldingen, `mjv_execution.trig` 203 fouten en 42 verdachte meldingen.
Het merendeel komt uit twee oorzaken (punten 1 en 2). Elk punt: origineel → herzien → motivatie.

1. **SSN-termen van vóór 2023.** `ssn:System`, `ssn:Deployment`, `ssn:deployedSystem`,
   `ssn:deployedOnPlatform`, `ssn:hasDeployment`, `ssn:hasSubSystem`, `ssn:implements`,
   `ssn:hasProperty`, `ssn:Property` en `sosa:ObservableProperty` → de `sosa:`-termen en
   `sosa:Property` → R14: SSN/SOSA 2023 verplaatste deze termen naar `sosa:`; de oude bestaan niet
   meer (`Term only referenced, not defined`).

2. **Systemen zonder SOSA-type.** Installaties, emissie-, lozings- en meetpunten waren enkel
   `riepr:…` en `ssn:System` → ook `sosa:System` → de 37 fouten in de planlaag: `sosa:implementedBy`
   verwacht een `sosa:System`, en de ontologie maakte de RIE-IEPR-klassen een `ssn:System`
   (punt O1 hieronder).

3. **Termen die niet bestaan of in de namespace van de ontologie gemunt zijn.**
   `riepr:ProcesVariabele` → `riepr:Procesvariabele`; `riepr:EmissieObservatie` → `riepr:Observatie`;
   `riepr:ZuiveringsApparaat` → `riepr:Installatie` met `dct:type installatie-type/luchtzuivering`;
   `riepr:uitstootProces`, `riepr:zuiveringsProces`, `riepr:meetProces`, `riepr:onttrekkingsProces`
   (in de data getypeerd in de namespace van de ontologie) → de procedures die de ontologie zelf
   definieert: `riepr:emissieProcedure`, `riepr:verwerkingProcedure`, `riepr:meetProcedure`,
   `riepr:onttrekkingProcedure` → R10: geen resources munten in de namespace van een vocabularium.
   Een zuivering is een verwerking door een installatie; de codelijst `procedure_type` kent geen
   aparte zuivering.

4. **Plan in elkaar geschoven.** Zuivering `isStepOfPlan` uitstoot, uitstoot `isStepOfPlan`
   activiteit, activiteit `isStepOfPlan` het plan 2021; de uitstoot heeft dezelfde variabele als
   input en output → alle stappen zijn stap van het plan 2021, in volgorde met
   `p-plan:isPrecededBy`, en elke stap heeft een eigen output: rookgas → gezuiverd rookgas,
   proceswater → geloosd afvalwater → in P-PLAN beschrijft `isStepOfPlan` het lidmaatschap van
   een plan, niet de stroom. De stroom loopt via de variabelen, de volgorde via `isPrecededBy`. De
   twee nieuwe variabelen volgen het IRI-patroon van de bron.

5. **De exploitatie implementeert het proces.** `exploitatie/…/jaar/2021 ssn:implements
   proces/…_2021` → `prov:wasAssociatedWith <exploitant>` en `prov:qualifiedAssociation [
   prov:agent <exploitant> ; prov:hadPlan proces/…_2021 ]` → in SSN/SOSA 2023 is een
   `sosa:Deployment` een `prov:Activity`, en `sosa:implements` gaat van een systeem naar de
   procedure die het kan uitvoeren. De PROV-relatie tussen een activiteit en het plan dat ze volgt,
   is `prov:hadPlan` op de associatie met de agent.

6. **Resultaat in twee knopen.** `riepr:Resultaat` (⊂ `sosa:Result`, `qb:Observation`) met
   `qudt:quantityValue` naar een aparte `qudt:QuantityValue` → één knoop, `riepr:Resultaat` en
   `qudt:QuantityValue`, met `qudt:numericValue` en `qudt:hasUnit` → R3: het resultaat is de
   `qudt:QuantityValue`; `sosa:Result` is verouderd. De IRI's van de tussenknopen (`…/result/qv`)
   vervallen.

7. **Eenheden die niet bestaan.** `eenheid:mg_per_l`, `kg_per_jaar`, `m3_per_jaar`, `Meter`
   (`https://data.imjv.omgeving.vlaanderen.be/id/concept/eenheid/`, niet gepubliceerd) →
   CSOR: `csor-eenheid:E_1`, `E_12`, `E_50`, `E_59`, getypeerd `csor:Eenheid, qudt:Unit` → R3, met
   het domeinregister van het project; de QUDT-mapping staat in CSOR (bespreking §6).

8. **Eén eigenschap voor concentratie en vracht.** Beide observaties van een stof hadden de stof
   zelf als `sosa:observedProperty` (`…/concept/chemische_stof/HCHKCACWOHOZIP-UHFFFAOYSA-N`, zink),
   enkel de eenheid verschilde → CSOR-parameteraspecten: `PAS_861` *Zn t (totaal in water):
   massaconcentratie*, `PAS_863` *Zn t (totaal in water): vracht per tijd*, en `PAS_1838` *Q
   (standaard in water): debiet* voor `concept:debiet` → een eigenschap is stof én aspect; met
   alleen de stof zijn concentratie en vracht niet te onderscheiden zonder de eenheid te lezen.
   Zelfde keuze als in `../waterkwaliteit/`.

9. **De vracht is berekend, niet gemeten.** De jaarvracht had dezelfde procedure
   (`concept:meetgegevens`) als de concentratie → een afgeleide observatie met
   `sosa:hasInputValue` naar het resultaat van de concentratie en van het jaardebiet,
   `sosa:relatedObservation` naar die twee observaties, en de procedure `concept:vrachtberekening`
   (bepalingsmethode *berekend*) → R7, R13. De waarden bewijzen het: 0,00474 mg/L × 336 735 m³/jaar
   = 1,59612 kg/jaar, precies de aangegeven vracht. Voor de andere stoffen van LP01 klopt dezelfde
   rekensom, behalve voor barium: daar is de concentratie (0,02735 mg/L) afgerond uit de vracht
   (9,21105 kg/jaar ÷ 336 735 m³ = 0,027354 mg/L), wat erop wijst dat de vracht daar de
   oorspronkelijke waarde is.
   <!-- TODO: berekent IMJV de vracht uit concentratie en debiet, of de concentratie uit vracht en debiet, en verschilt dat per stof of per aangifte? -->



10. **Tijd.** `time:inXSDDateTime` zonder tijdzone; het jaar 2021 eindigde op
    `2021-12-31T23:59:59`; `sosa:resultTime` zonder tijdzone → `time:inXSDDateTimeStamp` met
    `+01:00`, einde `2022-01-01T00:00:00+01:00`; `resultTime` met `+01:00` → R12: verouderde term,
    tijdzone `Europe/Brussels`, halfopen intervallen (een einde op 23:59:59 laat de laatste seconde
    weg).

11. **Een fictieve sensor.** `sosa:madeBySensor agent:labo_mens_sensor_x` (een `prov:Agent` en
    `sosa:Sensor`, die de verzonnen `riepr:meetProces` implementeert) op elke observatie →
    weggelaten → de bron zegt niet wie mat; een plaatshouder als sensor beweert iets wat niet
    bekend is. De R2-waarschuwing (*madeBySensor strongly recommended*) blijft staan, zie bespreking
    §6.

12. **Geen aanmaakdatum op observaties.** De ontologie eist `dct:created` op een
    `riepr:Observatie`; de bron gaf die niet → `dct:created` gelijk aan `sosa:resultTime`
    (2022-01-01) → aanname, zie bespreking §7.

13. **Kubusmetadata op de observatie.** `qb:dataSet <…/kubus/vmm-wateremissie-detail>` op de
    jaarvracht → weggelaten → het domein van `qb:dataSet` is `qb:Observation`, een rij in een
    datakubus. Dat is een record over de waarneming, geen eigenschap van de waarneming (R16, punt 1).

14. **Exploitant en onderneming door elkaar.** De onderneming
    `https://data.vlaanderen.be/id/onderneming/0413638187` was zelf de `riepr:Exploitant`, met
    `imjv:kbonummer "0413.638.187"^^imjv:KBONummer` en een identificator met datatype
    `riepr:KboOndernemingsnummer` (bestaat niet) → een eigen exploitant
    `exploitant/0413638187` met `prov:hadPrimarySource` naar de onderneming (een
    `org:Organization`), en de notatie als gewone tekst → het profiel vraagt die bron (de VKBO);
    het KBO-nummer stond er drie keer.

15. **Adres.** `dbo:nisCode`, `adres:gemeentenaam`, `adres:Adresvoorstelling.huisnummer` (niet
    geladen; herhalen de `locn:`-velden), `locn:fullAddress` met taalcode → enkel de `locn:`-velden,
    als gewone tekst → het profiel verwacht `xsd:string`; de NIS-code is weggelaten.

16. **Geometrie.** `geo:asWKT "POINT(…)"^^virtrdf:Geometry` (een datatype van OpenLink Virtuoso)
    → `^^geo:wktLiteral`; de geometrieën `"EMPTY"` van emissie- en lozingspunten → weggelaten → R11:
    een lege geometrie is geen locatie; ook `POINT EMPTY` zou geen informatie toevoegen.

17. **Status.** `adms:status st:in_gebruik` (`https://data.riepr.omgeving.vlaanderen.be/id/concept/status/`,
    niet gepubliceerd) → `riepr-status:in_dienst` uit de codelijst `status_type` → bestaande
    codelijsten hergebruiken.

18. **Kenmerken van punten.** `ssn:hasProperty imjv:diameter, imjv:hoogte` en observaties van
    `imjv:diameter` (`https://data.imjv.omgeving.vlaanderen.be/ns/imjv#`, niet gepubliceerd) → de
    begrippen `emissiepunt-eigenschappen/diameter` en `/hoogte` uit de codelijst, als
    `sosa:Property` → bestaande begrippen hergebruiken; ze hebben in de codelijst al een eenheid
    (`qudt:relevantUnit csor-eenheid:E_59`).

19. **Labels.** Dubbele labels (met en zonder taalcode, `"AGC GLASS EUROPE"` en
    `"AGCGLASS EUROPE"`) en een tweede label `"exploitatie - … - rapporteringsjaar - 2025"` op een
    resource van 2021 → één label met `@nl`.

20. **Emissie zonder koppeling aan het proces.** De lozing had `pplan:correspondsToVariable`, maar
    niet de `prov:wasDerivedFrom` naar een `riepr:Proces` die het profiel eist → beide → het profiel
    volgen. `prov:wasDerivedFrom` naar het plan is een korte weg en geen nette afleidingsketen, maar
    niet fout: een `riepr:Proces` is een `p-plan:Plan`, dus een `prov:Entity`.

## Verbeterpunten aan de ontologie

Het origineel staat in `source/riepr.trig`; de herziene versie in
`src/main/resources/be/vlaanderen/omgeving/data/ns/riepr/riepr.ttl`. Voorstel voor
[`milieuinfo/RIE-IEPR`](https://github.com/milieuinfo/RIE-IEPR).

- **O1. SSN-termen van vóór 2023.** `rdfs:subClassOf ssn:System` (zes klassen), `ssn:Deployment`,
  `ssn:Property` en de restricties op `ssn:deployedSystem`, `deployedOnPlatform`,
  `hasDeployment`, `inDeployment`, `hasSubSystem`, `implements`, `implementedBy`, `hasProperty`
  → de `sosa:`-termen (R14). Zonder deze wijziging eisen de gegenereerde shapes termen die niet
  bestaan, en is geen enkele RIE-IEPR-installatie een `sosa:System`.
- **O2. `:Resultaat`.** `rdfs:subClassOf sosa:Result, qb:Observation` → `rdfs:subClassOf
  qudt:QuantityValue` (R3); de prefix `qb:` is weg.
- **O3. `:Proces` gelijk aan een unie.** `owl:equivalentClass [ owl:unionOf ( pplan:Step
  pplan:MultiStep pplan:Plan ) ]` → weggelaten → die equivalentie maakt elke p-plan-stap en elk
  plan, ook van een ander project, een `riepr:Proces` (R17, criterium 5: geen axioma's over andere
  vocabularia). De deelklassen `pplan:Plan, pplan:Step, sosa:Procedure` blijven.
- **O4. Disjunctie in een lege restrictie.** `rdfs:subClassOf [ a owl:Restriction ;
  owl:disjointWith :Exploitatie ]` (een restrictie zonder `owl:onProperty`) → `:Proces
  owl:disjointWith :Exploitatie`.
- **O5. Exploitatie en proces.** De restrictie `ssn:implements :Proces` (exact 1) op
  `:Exploitatie`, de unie `( ssn:System ssn:Deployment )` bij `sosa:implementedBy` en het axioma
  *hoofdactiviteit → implementedBy :Exploitatie* → `prov:wasAssociatedWith :Exploitant` (exact 1),
  met het plan via `prov:qualifiedAssociation`/`prov:hadPlan`; `implementedBy` enkel naar
  `sosa:System` → zie punt 5 bij de data.
- **O6. Axioma's per proceduretype.** `owl:someValuesFrom <…/procedure-type/emissie>` (een
  individu waar een klasse hoort; en `…/meet` waar de codelijst `…/meting` heeft) →
  `owl:hasValue :emissieProcedure` enz., met de procedures die de ontologie zelf definieert.
- **O7. `adms:Status`.** De statussen `:inGebruik` enz. en de restricties op `adms:status`
  gebruikten `adms:Status`, dat ADMS niet als klasse definieert (het bereik van `adms:status` is
  `skos:Concept`) → `skos:Concept`.
- **O8. `:inGebruikVanaf` verplicht.** Minimum 1 op installatie, emissie-, onttrekkings-,
  uitwissel- en meetpunt en filter → minimum 0. De IMJV-export levert die datum niet; met
  minimum 1 faalt elk systeem.
  <!-- TODO: is "in gebruik vanaf" een verplicht gegeven in RIE-IEPR zelf, en levert een latere export het wel? Zo ja: terug naar minimum 1. -->
- **O9. Restrictie op `:ingediend`.** Een restrictie zonder beperking op een property die nergens
  gedefinieerd is → weggelaten; `:aangifte` dekt de koppeling met een aangifte.
- **O10. `sosa:madeBySensor`.** `owl:someValuesFrom ssn:System` → `sosa:Sensor`.
- **O11. `:Uitwisselpunt`.** De dubbele `rdfs:subClassOf ssn:System, ogc:SpatialObject` → één keer.
- **O12. `:Emissie`, `:Onttrekking`, `:Verbruik`.** De verplichte `prov:wasDerivedFrom :Proces`
  blijft; erbij een optionele `pplan:correspondsToVariable :Procesvariabele` (maximum 1), de
  fijnere koppeling die de bron al gebruikte.

Niet gewijzigd, wel op te volgen (bespreking §8):

- de `hydra:IriTemplate`s gebruiken `https://data.mjv.omgeving.vlaanderen.be/id/…/{uuid}/…`; de
  data gebruikt `https://data.imjv.omgeving.vlaanderen.be/id/…` en
  `https://data.riepr.omgeving.vlaanderen.be/id/…` met andere sleutels;
- de procedures en statussen in de ontologie (`:emissieProcedure`, `:inGebruik`, …) zijn kopieën
  van begrippen uit de codelijst, gekoppeld met `skos:related`.
