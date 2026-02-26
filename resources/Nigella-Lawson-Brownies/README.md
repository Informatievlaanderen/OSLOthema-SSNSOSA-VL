# Nigella Lawson Brownies - p-plan/SSN-SOSA-PROV-O Alignment Demonstratie

Dit voorbeeld demonstreert een complete implementatie van het p-plan/SSN-SOSA-PROV-O alignment framework voor procesmodellering.

## Architectonische Niveaus

### 1. Planning Niveau
Het abstracte recept als herbruikbaar plan:
- `plan:nigella-brownies` - Het hoofdplan (recept)
- Stappen (`p-plan:Step`) die het proces decomponeren
- Variabelen (`p-plan:Variable`) voor ingrediënten, tussenproducten en eindproduct
- Procedures (`sosa:Procedure`) die geïmplementeerd moeten worden

### 2. Deployment Niveau
Concrete implementatie in specifieke context:
- `kitchen:keuken-geert` als platform
- Systemen (keukenapparatuur) die procedures implementeren
- Deployment van assets voor specifieke uitvoering

### 3. Execution Niveau
Daadwerkelijke uitvoering met traceerbaarheid:
- Activiteiten (`prov:Activity`) en actuaties (`sosa:Actuation`)
- Concrete entiteiten als instantiaties van plan variabelen
- Tijdsgebonden uitvoering met start/end tijden
- Traceerbaarheid via `p-plan:correspondsToStep`, `p-plan:correspondsToVariable` en 

## Belangrijke Concepten

### Variabelen en Entiteiten
- Variabelen op plan-niveau beschrijven abstracte requirements
- Entiteiten op execution-niveau zijn concrete instantiaties
- `p-plan:correspondsToVariable` legt relatie tussen abstract en concreet

### Procedures en Systemen
- Procedures gedefinieerd in plan
- Systemen implementeren procedures
- Actuatoren voeren procedures uit tijdens execution

### Tijd en Volgorde
- Expliciete start/end tijden
- `p-plan:isPrecededBy` voor stap volgorde
- `prov:wasInformedBy` voor activiteit afhankelijkheden

## Conformiteit

Volgt strikt:
- p-plan voor procesmodellering
- SSN-SOSA voor sensoren/actuatoren
- PROV-O voor herkomst
- Scheiding abstracte planning vs concrete uitvoering