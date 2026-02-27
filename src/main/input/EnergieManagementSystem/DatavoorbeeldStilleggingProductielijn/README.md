# Productielijn Stillegging - Architecturale Verbetering

Dit voorbeeld demonstreert een productielijn stillegging systeem dat reageert op elektriciteitsprijzen, met een focus op architectonische verbeteringen volgens SOSA/PROV-O principes.

## Overzicht

Het scenario beschrijft een fabriek in Kortrijk waar een houtbewerkingsproductielijn automatisch wordt uitgeschakeld wanneer de elektriciteitsprijs een bepaalde drempel overschrijdt. Het systeem hanteert ook minimale en maximale stilleggingstijden.

## Oorspronkelijk Datavoorbeeld

### Structuur Problemen

Het originele voorbeeld (`source/DatavoorbeeldStilleggingProductielijn.ttl`) vertoont verschillende architectonische problemen:

1. **Gemengde Zaken (Separation of Concerns Violation)**
   - Mix van observatie (elektriciteitsprijs meting) en actuatie (productielijn uitschakelen)
   - Complexe geneste structuur met blank nodes
   - Moeilijk te begrijpen relaties

2. **Geen Lifecycle Scheiding**
   - Geen duidelijke scheiding tussen:
     - Plan (wat moet gebeuren)
     - Deployment (hoe het geïmplementeerd wordt)
     - Execution (concrete uitvoering)

3. **Variabelen vs Runtime Data Verwarring**
   - Concrete waarden (100 EUR drempel, 8hr max, 4hr min) direct in procedure
   - Geen abstracte variabelen gedefinieerd op plan niveau
   - Semantische fout: gebruikt `sosa:hasInput` voor concrete runtime data

4. **Slechte Traceerbaarheid**
   - Geen duidelijke keten van execution terug naar planning
   - Geen `p-plan:correspondsTo*` relaties
   - Moeilijk om wijzigingen door te voeren

5. **Semantische Problemen**
   - Overtreding van SOSA specificatie
   - `sosa:hasInput` is bedoeld voor procedure niveau, niet voor concrete instanties
   - Moet `prov:used` gebruiken voor execution entiteiten

### Code Voorbeeld (Problematisch)

```turtle
[ rdf:type sosa:Observation;
  # Mix van observatie en nested actuatie
  sosa:usedProcedure [ sosa:hasInput [ # Concrete data in procedure!
    seb:Input.referentie [ schema:value "100"^^rdfs:Literal ]
  ]];
  sosa:hasResult [ rdf:type utility-services:Connection, sosa:Actuation;
    # Actuatie genest in observatie - slechte scheiding
    sosa:hasResult toestelstatus:uit
  ]
]
```

## Verbeterd Datavoorbeeld

### Architectonische Principes

Het verbeterde voorbeeld (`DatavoorbeeldStilleggingProductielijn_herzien.ttl`) volgt deze principes:

1. **Duidelijke Scheiding van Zaken**
   - Observatie en actuatie zijn volledig gescheiden
   - Geen geneste complexiteit meer

2. **Drie-Niveau Architectuur**
   - **PLANNING**: Abstracte procedure definitie
   - **DEPLOYMENT**: Systeem implementatie
   - **EXECUTION**: Concrete uitvoering

3. **Variabelen vs Runtime Data Gescheiden**
   - Abstracte variabelen op plan niveau
   - Concrete entiteiten op execution niveau
   - Traceerbaarheid via `p-plan:correspondsToVariable`

4. **Correcte Semantiek**
   - Gebruikt `prov:used` voor concrete execution data
   - Volgt SOSA/PROV-O alignment principes
   - Proper gebruik van `sosa:hasInput` alleen op procedure niveau

### Verbeterde Structuur

```
PLANNING Level → DEPLOYMENT Level → EXECUTION Level
     ↑                    ↑                    ↑
  Abstract            Implementatie       Concrete Data
  Variables          Systems/Platforms    Entities/Activities
```

### Code Voorbeeld (Verbeterd)

```turtle
# PLANNING Level - Abstract
plan:productielijn_aansturing
  a p-plan:Plan, sosa:Procedure;
  sosa:hasInput var:elektriciteitsprijs_drempel, var:max_stillegging_duur;
  sosa:hasOutput var:toestel_status .

# DEPLOYMENT Level - Implementatie
actuator:productielijn_controller
  a sosa:Actuator;
  sosa:implements step:beslis_stillegging .

# EXECUTION Level - Concrete Uitvoering
exec:stillegging_20250214
  a sosa:Actuation;
  p-plan:correspondsToStep step:beslis_stillegging;
  prov:used ent:drempel_100eur, ent:prijs_105eur;  # Correct!
  sosa:hasResult ent:status_uit .

# Traceerbaarheid
ent:drempel_100eur
  a prov:Entity;
  p-plan:correspondsToVariable var:elektriciteitsprijs_drempel .
```

## Vergelijkingstabel

| Aspect | Oorspronkelijk | Verbeterd |
|--------|---------------|-----------|
| **Scheiding** | ❌ Gemengd | ✅ Gescheiden observatie/actuatie |
| **Architectuur** | ❌ Geen niveaus | ✅ Plan/Deploy/Execute |
| **Semantiek** | ❌ `sosa:hasInput` voor data | ✅ `prov:used` voor data |
| **Traceerbaarheid** | ❌ Poor | ✅ Complete chain |
| **Onderhoudbaarheid** | ❌ Moeilijk | ✅ Makkelijk |
| **SOSA Compliance** | ❌ Violations | ✅ Correct |

## Visualisatie

De bijgeleverde Mermaid diagram (`DatavoorbeeldStilleggingProductielijn_vergelijking.mmd`) toont:

- **Linkerkant**: Oorspronkelijke structuur met gemarkeerde violaties (rood)
- **Rechterkant**: Verbeterde drie-niveau architectuur (kleurgecodeerd)
- **Sleutelverschillen**: 6 belangrijke verbeterpunten
- **Legenda**: Uitleg van de kleurcodes

## Voordelen van de Verbeterde Versie

1. **Betere Onderhoudbaarheid**
   - Wijzigingen in procedure hebben geen impact op execution data
   - Makkelijker om nieuwe implementaties toe te voegen

2. **Duidelijke Traceerbaarheid**
   - Volledige keten van execution entiteiten terug naar planning variabelen
   - Makkelijk te auditen en valideren

3. **Correcte Semantiek**
   - Volgt SOSA en PROV-O specificaties nauwkeurig
   - Betere interoperabiliteit met andere systemen

4. **Schaalbaarheid**
   - Makkelijk uit te breiden met nieuwe variabelen of stappen
   - Kan meerdere implementaties van dezelfde procedure ondersteunen

5. **Flexibiliteit**
   - Procedure kan worden hergebruikt met verschillende deployment configuraties
   - Execution data kan variëren zonder procedure wijzigingen

## Conclusie

Het verbeterde voorbeeld toont hoe complex geneste SOSA structuren kunnen worden getransformeerd naar een schone, drie-niveau architectuur die:

- **Separation of Concerns** respecteert
- **Correcte semantiek** gebruikt volgens SOSA/PROV-O specificaties
- **Complete traceerbaarheid** biedt van execution naar planning
- **Betere onderhoudbaarheid** en schaalbaarheid mogelijk maakt

Deze benadering is consistent met de principes die ook zijn toegepast in het warmteverlies classificatie voorbeeld en volgt de best practices voor p-plan-SSN-SOSA-PROV-O alignment.