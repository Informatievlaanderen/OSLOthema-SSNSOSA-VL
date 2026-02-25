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
  sosa:hasInput :concrete-drempelwaarde, :concrete-meting ;
  sosa:hasResult :concrete-klasse .

:concrete-drempelwaarde
  a prov:Entity ;
  p-plan:correspondsToVariable :drempelwaarde-variabele .

:concrete-meting
  a sosa:Observation ;
  p-plan:correspondsToVariable :meting-variabele .
```

## Conclusie

Het huidige model werkt functioneel maar kan verbeterd worden door:
1. Duidelijkere architectonische scheiding
2. Betere lifecycle modellering
3. Explicietere traceerbaarheid tussen niveaus
4. Scheiding tussen abstracte planning en concrete uitvoering