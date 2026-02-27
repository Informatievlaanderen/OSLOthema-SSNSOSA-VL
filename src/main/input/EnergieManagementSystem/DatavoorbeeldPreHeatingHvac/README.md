# HVAC Pre-Heating Voorbeeld - p-plan/SSN-SOSA-PROV-O Alignment

Dit voorbeeld demonstreert een complete implementatie van het p-plan/SSN-SOSA-PROV-O alignment framework voor een HVAC pre-heating scenario.

## Origineel Bestand

Het originele bestand (`source/DatavoorbeeldPreHeatingHvac.ttl`) beschrijft een HVAC pre-heating scenario met:

1. **Observaties**:
   - Tijdstip voorspelling via machine learning model
   - Bezettingsvoorspelling (80%)
   - Buitentemperatuur meting (1°C)
   - Observatieverzameling voor historische data

2. **Actuatie**:
   - HVAC systeem activatie op basis van voorspellingen

3. **Kenmerken**:
   - Gebruik van `it6:MachineLearningModel` voor AI-voorspelling
   - Tijdsgebonden observaties met `time:Instant`
   - Kwantitatieve resultaten met eenheden
   - Procedure inputs met referenties naar andere observaties

## Herschreven Versie

De herschreven versie (`DatavoorbeeldPreHeatingHvac_herzien.ttl`) implementeert een complete p-plan/SSN-SOSA-PROV-O structuur:

### 1. Planning Niveau (Abstract)

```turtle
# Abstracte procedure
plan:hvac_preheating
  a p-plan:Plan, sosa:Procedure;
  p-plan:hasStep step:voorspel_tijdstip, step:meet_omstandigheden, step:activeer_hvac;
  sosa:hasInput var:historische_data, var:doeltemperatuur, var:doeltijdstip;
  sosa:hasOutput var:voorspeld_tijdstip, var:activeringsresultaat .

# Stappen
step:voorspel_tijdstip
  a p-plan:Step;
  p-plan:isStepOfPlan plan:hvac_preheating;
  sosa:hasInput var:historische_data, var:doeltemperatuur, var:doeltijdstip;
  sosa:hasOutput var:voorspeld_tijdstip .

# Variabelen
var:historische_data
  a p-plan:Variable;
  p-plan:isInputVarOf step:voorspel_tijdstip;
  sosa:inputFor plan:hvac_preheating .
```

### 2. Deployment Niveau (Concrete Implementatie)

```turtle
# Platform
platform:belpaire_automatisering
  a sosa:Platform;
  sosa:hosts sensor:ml_model_preheating, sensor:buitentemperatuur_sensor, actuator:hvac_controller .

# Sensoren
sensor:ml_model_preheating
  a sosa:Sensor, it6:MachineLearningModel;
  sosa:implements step:voorspel_tijdstip;
  sosa:observes observeerbaar_kenmerk:tijdstip_start_HVAC .

# Deployment
deploy:hvac_preheating_2025
  a sosa:Deployment;
  sosa:implements plan:hvac_preheating;
  sosa:deployedOnPlatform platform:belpaire_automatisering;
  sosa:deployedAsset sensor:ml_model_preheating, sensor:buitentemperatuur_sensor, actuator:hvac_controller .
```

### 3. Execution Niveau (Concrete Uitvoering)

```turtle
# Concrete entiteiten
ent:historische_data_2025Q1
  a prov:Entity;
  p-plan:correspondsToVariable var:historische_data;
  seb:Input.referentie "_:OV001"^^xsd:anyURI .

# Observaties
exec:tijdstip_voorspelling_001
  a sosa:Observation;
  p-plan:correspondsToStep step:voorspel_tijdstip;
  sosa:usedProcedure plan:hvac_preheating;
  prov:used ent:historische_data_2025Q1, ent:doeltemperatuur_20c, ent:doeltijdstip_0800;
  sosa:hasResult ent:voorspeld_tijdstip_0530;
  sosa:madeBySensor sensor:ml_model_preheating .

# Actuatie
exec:hvac_actuatie_001
  a sosa:Actuation;
  p-plan:correspondsToStep step:activeer_hvac;
  sosa:usedProcedure plan:hvac_preheating;
  prov:used ent:voorspeld_tijdstip_0530, ent:buitentemperatuur_1c, ent:bezetting_80pct;
  sosa:hasResult ent:hvac_status_aan;
  sosa:madeByActuator actuator:hvac_controller .
```

## Belangrijkste Wijzigingen en Motivatie

### 1. Architectonische Scheiding

**Origineel**: Directe observaties en actuaties zonder abstractie

**Herschreven**: Drie duidelijke niveaus:
- **Plan**: Abstracte procedure en variabelen
- **Deployment**: Concrete implementatie op platform
- **Execution**: Specifieke uitvoering met traceerbaarheid

**Motivatie**: Betere herbruikbaarheid, duidelijke scheiding van concerns, en alignment met p-plan principes.

### 2. Variabelen Architectuur

**Origineel**: Directe koppeling aan concrete observaties via URI referenties

**Herschreven**: Abstracte variabelen op plan niveau, concrete entiteiten op execution niveau

**Motivatie**: 
- Abstracte variabelen kunnen hergebruikt worden in verschillende contexten
- Concrete entiteiten representeren specifieke uitvoeringen
- Expliciete koppeling via `p-plan:correspondsToVariable`

### 3. Semantische Correctheid

**Origineel**: Gebruik van `sosa:hasInput` voor concrete observaties

**Herschreven**: Gebruik van `prov:used` voor concrete entiteiten

**Motivatie**: 
- `sosa:hasInput` is bedoeld voor `sosa:Procedure` (niet voor concrete observaties)
- `prov:used` is de correcte property voor wat een activiteit gebruikt
- Betere alignment met PROV-O specificatie

### 4. Traceerbaarheid

**Origineel**: Losse observaties met URI referenties

**Herschreven**: Complete traceerbaarheidsketen:
- `p-plan:correspondsToStep` voor koppeling aan stappen
- `p-plan:correspondsToVariable` voor koppeling aan variabelen
- `prov:used` voor input entiteiten

**Motivatie**: Volledige traceerbaarheid van abstract plan naar concrete uitvoering.

### 5. Sensor/Actuator Modellering

**Origineel**: Impliciete sensoren/actuatoren

**Herschreven**: Expliciete modellering:
- Machine learning model als `sosa:Sensor`
- HVAC controller als `sosa:Actuator`
- Sensoren en actuatoren implementeren specifieke stappen

**Motivatie**: Duidelijk maken welke componenten welke stappen uitvoeren.

## Voordelen van de Herschreven Versie

1. **Herbruikbaarheid**: Abstracte procedure kan hergebruikt worden in verschillende gebouwen
2. **Traceerbaarheid**: Complete keten van plan naar execution
3. **Semantische correctheid**: Juiste toepassing van SOSA/SSN/PROV-O concepten
4. **Uitbreidbaarheid**: Eenvoudig toe te voegen stappen of variabelen
5. **Alignment**: Volgt p-plan/SSN-SOSA-PROV-O alignment principes

## Bestanden

- **Origineel**: `source/DatavoorbeeldPreHeatingHvac.ttl` (1.5 KB)
- **Herschreven**: `DatavoorbeeldPreHeatingHvac_herzien.ttl` (11 KB)

De herschreven versie is significant groter vanwege de toegevoegde architectonische structuur, variabelen definitie, en complete traceerbaarheid.

## Tijdsmodellering van Voorspellingen

Een belangrijk aspect van dit voorbeeld is de correcte modellering van tijdsaspecten bij voorspellingen:

1. **Observatie tijd** (`sosa:phenomenonTime`):
   - Wanneer de voorspelling gemaakt werd
   - Altijd in het verleden ten opzichte van de voorspelling zelf
   - Bijv: "2025-04-01T05:00:00" (wanneer het model draaide)

2. **Voorspeld tijdstip** (`sosa:hasResult`):
   - Wat er voorspeld wordt
   - Kan in de toekomst liggen
   - Bijv: "2025-04-01T05:30:00" (wanneer HVAC aan moet)

3. **Resultaat tijd** (`sosa:resultTime`):
   - Wanneer het resultaat beschikbaar was
   - Meestal gelijk aan observatie tijd

### Voorbeeld:

```turtle
exec:tijdstip_voorspelling_001
  sosa:phenomenonTime [ time:inXSDDateTime "2025-04-01T05:00:00"^^xsd:dateTime ];  # Wanneer voorspeld
  sosa:hasResult [ time:inXSDDateTime "2025-04-01T05:30:00"^^xsd:dateTime ];       # Wat voorspeld
  sosa:resultTime "2025-04-01T05:00:00"^^xsd:dateTime .      # Wanneer resultaat bekend
```

Deze benadering houdt rekening met:
- **Temporale logica**: Verleden (observatie) vs toekomst (voorspelling)
- **SOSA semantiek**: Correct gebruik van phenomenonTime
- **Traceerbaarheid**: Duidelijk wanneer wat gebeurde

## Machine Learning Model Modellering

Een belangrijk correctie in de herschreven versie betreft de modellering van het machine learning model:

### Origineel (conceptueel incorrect):
```turtle
sensor:ml_model_preheating
  a sosa:Sensor, it6:MachineLearningModel .
```

Probleem: Een ML model is een **artefact** (getraind bestand), geen **sensor** (agent die observeert).

### Herschreven (conceptueel correct):
```turtle
# Model als artefact
model:preheating_ml_model
  a it6:MachineLearningModel, prov:Entity;
  prov:wasGeneratedBy [ a prov:Activity;
                        prov:used [ a prov:Entity;
                                    dct:type inputtype:observatieverzameling;
                                    seb:Input.referentie "_:OV001"^^xsd:anyURI ] ] .

# Sensor die het model gebruikt
sensor:temperatuur_voorspeller
  a sosa:Sensor;
  sosa:implements step:voorspel_tijdstip;
  sosa:observes observeerbaar_kenmerk:tijdstip_start_HVAC;
  sosa:uses model:preheating_ml_model .
```

### Voordelen:
1. **Conceptuele correctheid**: Model is een artefact, sensor is de gebruiker
2. **Betere semantiek**: Duidelijke scheiding tussen model en agent
3. **Traceerbaarheid**: Expliciete keten van training → model → gebruik
4. **Alignment**: Past beter bij SOSA/SSN/PROV-O specificaties

### Gebruik in observatie:
```turtle
exec:tijdstip_voorspelling_001
  a sosa:Observation;
  prov:used model:preheating_ml_model;  # Model als input
  sosa:madeBySensor sensor:temperatuur_voorspeller .  # Sensor maakt de observatie
```

Deze correctie verbetert de semantische nauwkeurigheid zonder de architectuur te verstoren.