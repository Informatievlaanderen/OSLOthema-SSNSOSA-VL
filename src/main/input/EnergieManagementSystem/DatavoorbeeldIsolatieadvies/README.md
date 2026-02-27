# Warmteverlies Observatie - Geneste SOSA Structuur

Dit voorbeeld demonstreert een geneste observatie structuur voor warmteverlies classificatie, met verbeterpunten voor betere architectonische scheiding.

## Huidige Structuur

### Hoofd Observatie
Observatie van warmteverlies klasse:
- Feature of Interest: Gebouw
- Observed Property: Warmteverlies klasse
- Used Procedure: Bevat input variabelen en geneste observaties
- Result: Geclassificeerde warmteverlies klasse

### Procedure Structuur
De `usedProcedure` bevat:
- Input variabelen (drempelwaarde + geneste observatie)
- Output: Warmteverlies classificatie

### Geneste Observatie
Input observatie van gemiddeld nachtelijk warmteverlies:
- Feature of Interest: Hetzelfde gebouw
- Observed Property: Gemiddeld nachtelijk warmteverlies
- Eigen procedure met inputs
- Kwantitatief resultaat met eenheid

## Verbeterpunten

### 1. Separation of Concerns
**Huidig**: Procedure bevat zowel abstracte variabelen als concrete observaties
**Verbetering**: Scheid planning (abstracte procedure definitie) van execution (concrete observaties)

### 2. Lifecycle Scheiding
**Huidig**: Geen duidelijke scheiding tussen:
- Plan (wat moet gebeuren)
- Deployment (hoe het geïmplementeerd wordt)
- Execution (concrete uitvoering)

**Verbetering**: Introduceer drie niveaus:
- Plan niveau: Abstracte procedure met variabelen
- Deployment niveau: Hoe procedure geïmplementeerd wordt
- Execution niveau: Concrete uitvoering met traceerbaarheid

### 3. Variabelen vs Runtime Data
**Huidig**: Inputs zijn direct concrete waarden/observaties in procedure
**Verbetering**:
- Gebruik variabelen op plan niveau
- Maak concrete entiteiten op execution niveau
- Leg relatie met `p-plan:correspondsToVariable`

### 4. Tijdsmodellering
**Huidig**: Tijdsaspecten aanwezig maar niet gestructureerd
**Verbetering**:
- Expliciete start/end tijden voor execution
- Scheid phenomenonTime (wat gemeten wordt) van execution tijd

### 5. Traceerbaarheid
**Huidig**: Geneste structuur maar geen duidelijke traceerbaarheid
**Verbetering**:
- Gebruik `p-plan:correspondsToStep` voor stap traceerbaarheid
- Gebruik `prov:wasDerivedFrom` voor data afhankelijkheden

## Voorgestelde Architectuur

```turtle
# Plan niveau
:classificatie-procedure
  a sosa:Procedure ;
  sosa:hasInput :drempelwaarde-variabele, :meting-variabele ;
  sosa:hasOutput :klasse-variabele .

# Execution niveau
:concrete-observatie
  a sosa:Observation ;
  sosa:usedProcedure :classificatie-procedure ;
  prov:used :concrete-drempelwaarde, :concrete-meting ;
  sosa:hasResult :concrete-klasse .

:concrete-drempelwaarde
  a prov:Entity ;
  p-plan:correspondsToVariable :drempelwaarde-variabele .

:concrete-meting
  a sosa:Observation ;
  p-plan:correspondsToVariable :meting-variabele .
```

## Semantische Keuzes en Alignment

### Gebruik van `prov:used` in plaats van `sosa:hasInput`

In de herschreven versie gebruiken we `prov:used` voor het koppelen van concrete entiteiten aan observaties, in plaats van `sosa:hasInput`. Deze keuze is gebaseerd op:

1. **SOSA Specificatie**:
   - `sosa:hasInput` is specifiek bedoeld voor `sosa:Procedure` (domainIncludes)
   - Het beschrijft "inputs required for its execution" op procedure niveau
   - Bedoeld voor type-beschrijving van inputs, niet concrete instanties

2. **Correcte Semantiek**:
   - `sosa:Observation` is een subclass van `prov:Activity`
   - `prov:used` is de juiste property voor wat een activiteit gebruikt
   - Concrete entiteiten horen thuis op execution niveau, niet procedure niveau

3. **Alignment Principes**:
   - Op plan niveau: `sosa:hasInput` voor abstracte variabelen
   - Op execution niveau: `prov:used` voor concrete entiteiten
   - Dit volgt het p-plan/SSN-SOSA-PROV-O alignment patroon

### Stappen en Traceerbaarheid

De herschreven versie voegt expliciete stappen toe en verbetert de traceerbaarheid:

1. **Stap definitie op plan niveau**:
   ```turtle
   step:warmteverlies-classificatie
     a p-plan:Step ;
     p-plan:isStepOfPlan plan:warmteverlies-classificatie ;
     p-plan:correspondsToProcedure plan:warmteverlies-classificatie .
   ```

2. **Sensor implementeert stap**:
   ```turtle
   sensor:temperatuur-sensor-001
     sosa:implements step:warmteverlies-classificatie .
   ```

3. **Complete traceerbaarheid in execution**:
   ```turtle
   exec:classificatie-uitvoering-20250315
     sosa:usedProcedure plan:warmteverlies-classificatie ;
     p-plan:correspondsToStep step:warmteverlies-classificatie .
   ```

### Voorbeeld van correct gebruik:

```turtle
# Plan niveau - abstracte procedure met variabelen
plan:warmteverlies-classificatie
  sosa:hasInput var:drempelwaarde, var:meting .

# Stap niveau - concrete stap in het plan
step:warmteverlies-classificatie
  p-plan:isStepOfPlan plan:warmteverlies-classificatie .

# Execution niveau - concrete observatie met entiteiten
exec:classificatie-uitvoering-20250315
  prov:used ent:drempelwaarde-001, ent:meting-001 ;
  p-plan:correspondsToStep step:warmteverlies-classificatie .
```

Deze benadering zorgt voor:
- Duidelijke scheiding tussen abstracte planning en concrete uitvoering
- Correcte toepassing van SOSA en PROV-O semantiek
- Betere alignment met het p-plan framework
- Complete traceerbaarheid van execution naar stap naar procedure

## Conclusie

Het bestaande model werkt functioneel maar kan verbeterd worden door:
1. Duidelijkere architectonische scheiding
2. Betere lifecycle modellering
3. Explicietere traceerbaarheid tussen niveaus
4. Scheiding tussen abstracte planning en concrete uitvoering