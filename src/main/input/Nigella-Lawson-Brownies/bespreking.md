# Bespreking: Nigella Lawson Brownies

## 1. Wat stelt dit voorbeeld voor?

Het bakken van brownies volgens het recept van Nigella Lawson
(<https://www.nigella.com/recipes/brownies>), als voorbeeld van een proces in drie lagen:

- het recept als abstract plan (p-plan en `sosa:Procedure`);
- de inzet van het keukengerei in één keuken (`sosa:Deployment`);
- één concrete uitvoering op 10 februari 2026, met de herkomst van elk tussenproduct.

Het domein is bewust alledaags: zo gaat de aandacht naar het patroon, niet naar de vakkennis. Het
patroon is hetzelfde als bij een laboratoriumanalyse of een productieproces: stappen, variabelen,
systemen die stappen uitvoeren, en een afleidingsketen van grondstof tot eindproduct.

## 2. Kleurlegenda

| Kleur | SOSA-concept | Betekenis in het domein |
|---|---|---|
| Paars (#7f59ae) | `p-plan:Plan` / `p-plan:Step` | het recept en zijn stappen |
| Lila (#c6a0f5) | `sosa:Procedure` (deelplan) | de uitwerking van een stap: smelten, hakken, mengen, bakken |
| Oranje-rood (#fe7130) | `p-plan:Variable` | ingrediënten en tussenproducten als abstracte variabelen |
| Blauw (#60c4e4) | Platform / System / Deployment | de keuken, het keukengerei, de inzet ervan |
| Roze (#e54b89) | Actuation / Observation / Activity | smelten, hakken, mengen, bakken, de kleurcontrole |
| Oranje (#f8b622) | Result / `prov:Entity` | concrete ingrediënten, tussenproducten, brownies, kleur |
| Lichtgeel (#f8e1ad) | subgraph DERIVATION | de afleidingsketen (`prov:wasDerivedFrom`) |

## 3. Infrastructuur (blauwe nodes)

- **`kitchen:kitchen-geert`**: `sosa:Platform`, de plaats waar het gerei staat. De relatie met de
  gebruiker is een gekwalificeerde toeschrijving (`prov:qualifiedAttribution` →
  `attr:relation-kitchen-geert`, rol `role:user`).
- **`exec:brownies-baking-for-demo-on-wednesday`**: `sosa:Deployment` van tien stuks gerei op de
  keuken, sinds 2010-01-01 (`sosa:startTime`). De inzet is duurzaam, niet beperkt tot dit ene
  bakmoment.
- **Samengestelde systemen** (`sosa:System`, `sosa:Actuator`), elk met `sosa:implements` naar een
  deelplan:

  | Systeem | Implementeert | Deelsystemen (`sosa:hasSubSystem`) |
  |---|---|---|
  | `inst:melting-system-geert` | `plan:melting` | pan, garde, gasfornuis |
  | `inst:chopping-system-geert` | `plan:chopping` | snijplank, mes |
  | `inst:kitchen-robot-geert` | `plan:mixing` | — |
  | `inst:oven-geert` | `plan:baking` | — |

- **Enkelvoudig gerei** (`sosa:System`): pan, garde, gasfornuis en bakvorm implementeren elk een
  bladstap (`step:…`); mes en snijplank enkel als deelsysteem.
- **`agent:geert`**: `prov:Agent`, `sosa:Sensor` en `sosa:System`. Hij implementeert de
  kleurcontrole (`step:bake_until_light_brown_top`): een mens is hier de sensor. Alle gerei handelt
  in zijn naam (`prov:actedOnBehalfOf`).

## 4. Observatie/Actuatie-structuur (roze nodes)

| IRI | actsOnProperty / observedProperty | usedProcedure | hasResult | hasFeatureOfInterest |
|---|---|---|---|---|
| `exec:melting-2026-02-10` | `prop:state-butter-chocolate` | `plan:melting` | `ent:melted-mixture_001` | `ent:mixture_001` |
| `exec:chopping-2026-02-10` | `prop:state-walnuts` | `plan:chopping` | `ent:chopped-walnuts_001` | `ent:walnuts_001` |
| `exec:mixing-2026-02-10` | `prop:state-components` | `plan:mixing` | `ent:batter_001` | `ent:mixture_002` |
| `exec:baking-2026-02-10` | `prop:state-batter`, `parameter:the_colour_of_the_top_of_the_brownie` | `plan:baking` | `ent:brownies_001` | `ent:batter_001` |
| `exec:check_when_brownies_are_done` (observatie) | `parameter:the_colour_of_the_top_of_the_brownie` | `plan:bake_until_light_brown_top` | `ent:colour_001` | `ent:brownies_001` |

De vier actuaties zijn lid van **`exec:brownies-baking-2026-02-10`** (`sosa:ActuationCollection`).
Die draagt wat ze delen: de procedure van het hele recept (`plan:nigella-brownies`), de uitvoerder
(`prov:wasAssociatedWith agent:geert`), de begin- en eindtijd, en de brownies als ultiem
studieobject (`sosa:hasUltimateFeatureOfInterest`). De observatie is geen lid: een
`ActuationCollection` bevat actuaties.

Elke actuatie en de observatie is ook expliciet `sosa:Execution`: SHACL valideert de niet-afgeleide
graaf, en zonder die typering gelden de shapes van `sosa:Execution` niet (zie *Validation* in de
gids).

**Deelactiviteiten.** Smelten bestaat uit drie `prov:Activity`'s (recipiënt zijn, verwarmen,
homogeniseren), elk geassocieerd met één stuk gerei. De actuatie verwijst ernaar met
`prov:wasInformedBy`. Ze zijn geen lid van de collectie.

## 5. Procedure en Property

**Procedures.** Elk deelplan is `p-plan:Plan` én `sosa:Procedure`, en daarnaast
`sosa:ActuatingProcedure` of, voor de kleurcontrole, `sosa:ObservingProcedure`:

| Procedure | Soort | Geïmplementeerd door | Gebruikt door |
|---|---|---|---|
| `plan:nigella-brownies` | actuerend | — | de collectie |
| `plan:melting` | actuerend | `inst:melting-system-geert` | `exec:melting-2026-02-10` |
| `plan:chopping` | actuerend | `inst:chopping-system-geert` | `exec:chopping-2026-02-10` |
| `plan:mixing` | actuerend | `inst:kitchen-robot-geert` | `exec:mixing-2026-02-10` |
| `plan:baking` | actuerend | `inst:oven-geert` | `exec:baking-2026-02-10` |
| `plan:bake_until_light_brown_top` | observerend | (via de stap) `agent:geert` | `exec:check_when_brownies_are_done` |
| `plan:remove_from_oven_and_cool_down` | actuerend | — | — (niet uitgevoerd in de data) |

Volgens `pplan-sosa.ttl` is elke `p-plan:Step` een `sosa:Procedure`. Expliciet getypeerd zijn enkel
de bladstappen die rechtstreeks door gerei uitgevoerd worden (`step:butter_and_chocolate_in_pan`,
`step:heat_pan`, `step:stir_until_homogeneous_liquid_mixture`, `step:batter_in_baking_tin`), omdat
het bereik van `sosa:implements` een procedure is en SHACL zonder inferentie werkt.

**Variabelen.** Elf `p-plan:Variable`'s: zes ingrediënten met hoeveelheid (QUDT, gram; eieren
`unit:UNITLESS`), vier tussen- en eindproducten, en de kleur. Ze hangen aan de stappen
(`p-plan:isInputVarOf`/`isOutputVarOf`) en aan de procedures (`sosa:inputFor`/`outputFor`).

**Properties.**

| Property | Betekenis |
|---|---|
| `prop:state-butter-chocolate` | toestand van boter en chocolade: vast → vloeibaar |
| `prop:state-walnuts` | toestand van de walnoten: heel → gehakt |
| `prop:state-components` | toestand van de componenten: gescheiden → gemengd |
| `prop:state-batter` | toestand van het beslag: rauw → gebakken |
| `parameter:the_colour_of_the_top_of_the_brownie` | kleur van de bovenkant, veranderd door het bakken en vastgesteld in de kleurcontrole |

## 6. Modelleer-keuzes toegelicht

### Waarom drie lagen en geen plat model?

> **Verworpen alternatief:** een plat model met een `ObservationCollection` en losse actuaties.
> **Gekozen aanpak:** planning, deployment en uitvoering (R4).
> **Motivatie:** het proces heeft meerdere stappen in een vaste volgorde, hetzelfde recept kan in
> elke keuken uitgevoerd worden, en elke uitvoering moet terug te leiden zijn tot het recept. Dat
> zijn de drie voorwaarden van R4.

### Waarom is een `p-plan:Plan` ook een `sosa:Procedure`?

> **Verworpen alternatief:** enkel p-plan voor de planning, met SOSA alleen op uitvoeringsniveau.
> **Gekozen aanpak:** elk deelplan is `p-plan:Plan` en `sosa:Procedure`.
> **Motivatie:** de definities overlappen ("set of instructions"). De uitlijning van dit project,
> `src/main/resources/ontologies/pplan-sosa.ttl`, legt dat formeel vast: `p-plan:Plan`,
> `p-plan:Step` en `p-plan:MultiStep` ⊂ `sosa:Procedure`, en `sosa:inputFor`/`outputFor` als
> eigenschapsketen over `p-plan:isInputVarOf`/`isOutputVarOf` en `p-plan:isStepOfPlan`. De
> expliciete typering in de data is nodig omdat SHACL de niet-afgeleide graaf valideert. Zo kunnen
> `sosa:usedProcedure` en `sosa:implements` rechtstreeks naar het plan wijzen, en heeft de uitvoering
> twee verbindingen met de planning heeft: `p-plan:correspondsToStep` (welke stap, voor
> volledigheid en volgorde) en `sosa:usedProcedure` (welke instructies, voor herkomst).

### Waarom een stap én een deelplan, en niet `p-plan:MultiStep`?

> **Verworpen alternatief:** `p-plan:MultiStep`, tegelijk stap en plan, in één resource.
> **Gekozen aanpak:** twee resources (`step:melting` en `plan:melting`), verbonden met
> `p-plan:isDecomposedAsPlan`.
> **Motivatie:** het onderscheid tussen de plaats in het recept en de uitgewerkte instructies blijft
> zichtbaar. Beide vormen zijn conform p-plan; de prijs is wat redundantie.

### Waarom het gerei als `sosa:System` met eigen handelingsvermogen?

> **Verworpen alternatief:** `agent:geert` als enige agent, met het gerei als `prov:Entity` dat
> gebruikt wordt (`prov:used inst:whisk-geert`).
> **Gekozen aanpak:** elk stuk gerei is een `sosa:System` dat een stap implementeert, de agent is
> van zijn deelactiviteit (`prov:wasAssociatedWith`) en handelt namens Geert
> (`prov:actedOnBehalfOf`).
> **Motivatie:** het onderscheid tussen een systeem dat *handelt* en een entiteit *waarop*
> gehandeld wordt, en een zuivere afleidingsketen: `prov:used` en `sosa:hasResult` bevatten enkel
> wat omgevormd wordt, zodat de herkomst van de brownies uit die twee relaties alleen te
> reconstrueren is.

### Waarom een `prov:Collection` als studieobject van smelten en mengen?

> **Verworpen alternatief:** meerdere `sosa:hasFeatureOfInterest` per actuatie (boter én
> chocolade).
> **Gekozen aanpak:** één FOI per actuatie, een `prov:Collection` van de ingrediënten
> (`ent:mixture_001`, `ent:mixture_002`, met `prov:hadMember`).
> **Motivatie:** de gegenereerde shapes laten één FOI per uitvoering toe, en de actuatie werkt in op
> het geheel (het mengsel wordt vloeibaar), niet op elk ingrediënt apart. De ingrediënten zelf staan
> in `prov:used`.

### Waarom is de kleurcontrole een observatie met een mens als sensor?

> **Verworpen alternatief:** de kleur als eigenschap van het bakresultaat, zonder aparte uitvoering.
> **Gekozen aanpak:** `sosa:Observation` volgens een `sosa:ObservingProcedure`, gemaakt door
> `agent:geert` als `sosa:Sensor`, met de kleur als resultaat (`ent:colour_001`,
> `dct:type colour:light-brown`).
> **Motivatie:** het recept zegt "bak tot de bovenkant lichtbruin is": dat is een beslissing op basis
> van een waarneming. De kleur is daarna invoer van de volgende stap (`var:colour`).

### Vocabularia (R17)

Enkel de kern en p-plan: SOSA, PROV-O, OWL-Time, QUDT, DCTERMS, SKOS, RDFS. p-plan staat niet in
niveau 1 van R17, maar is een uitbreiding van PROV-O die al geladen is en die dit voorbeeld juist
wil demonstreren. De uitlijning met PROV-O zit in p-plan zelf (`p-plan:Plan ⊂ prov:Plan`,
`p-plan:Entity ⊂ prov:Entity`), die met SOSA in de projectmodule `pplan-sosa.ttl` (zie hierboven).
Die module staat in het register van uitlijningen van de kit (`registers/alignments.ttl`, sinds
0.3.2). De codelijsten (ingrediënten, producten, kleuren) zijn eigen
SKOS-concepten onder `https://example.org/concept/`.

### Open punten

<!-- TODO: hakken eindigt om 20:50 (resultTime), mengen om 20:45, maar mengen gebruikt de gehakte walnoten. Is de resultTime van hakken 20:40 bedoeld? -->
<!-- TODO: de README zegt dat een stap met isDecomposedAsPlan niet zelf sosa:Procedure is, maar pplan-sosa.ttl maakt elke p-plan:Step een sosa:Procedure, en step:bake_until_light_brown_top is ook expliciet zo getypeerd. De regel in de README bijstellen? -->
<!-- TODO: plan:bake_until_light_brown_top en plan:remove_from_oven_and_cool_down zijn isSubPlanOfPlan plan:nigella-brownies, terwijl hun stappen bij plan:baking horen. Moeten ze deelplan van plan:baking zijn? -->
<!-- TODO: het bakken actsOnProperty ook de kleur, die dezelfde property is als de geobserveerde. Is dat bedoeld (het bakken verandert de kleur, de controle stelt ze vast)? -->

## 7. Tijdsmodellering

| Element | Patroon |
|---|---|
| Collectie (het hele bakmoment) | `sosa:startTime` / `sosa:endTime`, 20:00–21:30 |
| Actuaties | `sosa:resultTime`: wanneer het tussenproduct klaar was |
| Kleurcontrole | `sosa:startTime`/`endTime` (21:29:30–21:30) en `sosa:phenomenonTime` → `time:Instant` met `time:inXSDDateTimeStamp` |
| Deployment | `sosa:startTime` 2010-01-01: sinds wanneer het gerei in de keuken staat |

- **Tijdzone:** alle tijden staan in UTC (`Z`). Volgens R12 blijft een gegeven tijdzone behouden;
  20:00Z is 21:00 in Brussel.
- **`phenomenonTime` versus `resultTime`:** bij de kleurcontrole vallen ze samen (21:30): de kleur
  wordt vastgesteld op het moment dat ze waargenomen wordt.
- De actuaties hebben geen `phenomenonTime`; hun duur volgt enkel uit de collectie en de
  `resultTime`.

## 8. Prefixen en IRI-structuur

| Prefix | Base IRI | Tijdelijk of persistent |
|---|---|---|
| `plan:`, `step:`, `var:` | `https://example.org/plan/`, `…/step/`, `…/variable/` | Tijdelijk (illustratief) |
| `exec:`, `ent:`, `attr:` | `https://example.org/execution/`, `…/entity/`, `…/attribution/` | Tijdelijk |
| `inst:`, `kitchen:`, `agent:` | `https://example.org/installation/`, `…/platform/`, `…/agent/` | Tijdelijk |
| `ingredient:`, `intermediateproduct:`, `finalproduct:`, `parameter:`, `prop:`, `colour:`, `attribute:`, `role:` | `https://example.org/concept/…/` | Tijdelijk |
| `p-plan:` | `http://purl.org/net/p-plan#` | Persistent (purl) |
| `sosa:` | `http://www.w3.org/ns/sosa/` | Persistent (W3C) |
| `prov:` | `http://www.w3.org/ns/prov#` | Persistent (W3C) |
| `time:` | `http://www.w3.org/2006/time#` | Persistent (W3C) |
| `qudt:`, `unit:` | `http://qudt.org/schema/qudt/`, `http://qudt.org/vocab/unit/` | Persistent (QUDT) |
| `dct:`, `skos:`, `rdf:`, `rdfs:`, `xsd:` | DCMI, W3C | Persistent |

Elke laag heeft een eigen prefix (drielaagsconventie). Blank nodes komen enkel voor bij de
hoeveelheden (`qudt:quantityValue [ … ]`), die niet van buitenaf aangesproken worden (R10). De
deployment staat onder `exec:`, hoewel hij tot de deploymentlaag hoort.

## 9. Inverse relaties

| Relatie | Inverse | Opgenomen in | Doel |
|---|---|---|---|
| `sosa:hasFeatureOfInterest` | `sosa:isFeatureOfInterestOf` | de studieobjecten (mengsels, walnoten, beslag, brownies) | uitvoeringen per studieobject; de gegenereerde shapes vragen de inverse |
| `sosa:hasResult` | `sosa:isResultOf` | alle resultaten | uitvoering per product; vereist door de shapes |
| `p-plan:isStepOfPlan` | (geen `hasStep` in de data) | stappen | de diagrammen tonen `hasStep` voor de leesbaarheid |
| `p-plan:isSubPlanOfPlan` | — | deelplannen | idem `hasSubPlan` |
| `sosa:hasSubSystem` | — | samengestelde systemen | van systeem naar onderdelen |

De zijde die opgenomen is, is die waarop de shapes en de typische vragen ("welke stap hoort bij
welk plan?", "welke uitvoering leverde dit product?") steunen.
