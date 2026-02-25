# Paleo atmosfeer

De concentratie van CO₂ kan worden gemeten in luchtbellen in ijskernen, waarvan wordt aangenomen dat ze een steekproef vormen van de atmosfeer op een bepaald moment in het verleden. In dit geval zijn de concentratie en de leeftijd het resultaat van twee oorspronkelijke waarnemingen. Deze leveren de invoerwaarden voor de uiteindelijke waarneming.

## Alternatief 1
In dit voorbeeld zijn de 2 oorspronkelijke observaties (i.e de executions, de activiteiten) direct gelinkt met de uiteindelijke observatie.

```mermaid
%%flowchart TD
graph TD

%% Features of Interest & Samples
A["`AardKorst
(sosa:FeatureOfInterest)`"]
B["`IjsKern
(sosa:Sample+FeatureOfInterest)`"]
C["`IjsBel
(sosa:Sample+FeatureOfInterest)`"]
D["`AardAtmosfeer
(sosa:FeatureOfInterest)`"]

B -->|isSampleOf| A
C -->|isSampleOf| B
C -->|isSampleOf| D

%% Original Observations
O1["`(sosa:Observation)
C14Observatie
-observedProperty: C14Leeftijd
-result: 7530 YR   
  
   `"]
O2["`(sosa:Observation)
CO2Observatie
-observedProperty = CO2Concentratie
-result = 240 PPM`"]

O1 -->|hasFeatureOfInterest| C
O2 -->|hasFeatureOfInterest| C
O1 -->|hasUltimateFeatureOfInterest| D
O2 -->|hasUltimateFeatureOfInterest| D

%% Derived Paleo Observation
P["`(sosa:Observation)
PaleoCO2Observatie
-observedProperty = CO2Concentratie
-result = 240 PPM
-phenomenonTime = 7530 BP`"]

P -->|hasFeatureOfInterest| D

%% Input relations
P -->|hasInputValue| O1
P -->|hasInputValue| O2

%% Procedure
PR["`(sosa:Procedure)
ProcedurePaleoCO2Contentratie`"]

P -->|usedProcedure| PR
```

## Alternatief 2
In dit voorbeeld worden de resultaten van de 2 oorspronkelijke observaties gelinkt met de uiteindelijke observatie (niet de observaties zelf).
Deze 2 resultaten komen overeen met de input variabelen gedefinieerd in de procedure.

#### Opmerking:
De 2 input variabelen zijn in dit voorbeeld apart gedefinieerd. Dit is niet noodzakelijk. We zouden als input variabelen de 2 overeenkomende observedProperties kunnen specifieren.
- ex:VariabeleCO2Observatie --> ex:CO2Concentratie
- ex:VariabeleC14Observatie --> ex:C14Leeftijd

```mermaid
%%flowchart TD
graph TD

%% Features of Interest & Samples
A["`AardKorst
(sosa:FeatureOfInterest)`"]
B["`IjsKern
(sosa:Sample+FeatureOfInterest)`"]
C["`IjsBel
(sosa:Sample+FeatureOfInterest)`"]
D["`AardAtmosfeer
(sosa:FeatureOfInterest)`"]

B -->|isSampleOf| A
C -->|isSampleOf| B
C -->|isSampleOf| D

%% Observed properties
P1["`(sosa:Property)
C14Leeftijd`"]
P2["`(sosa:Property)
CO2Concentratie`"]

%% Original Observations
O1["`(sosa:Observation)
C14Observatie
-observedProperty = C14Leeftijd`"]
R1["`(sosa:Result)
-value = 7530
-unit = YR`"]
O2["`(sosa:Observation)
CO2Observatie
-observedProperty = CO2Concentratie`"]
R2["`(sosa:Result)
-value = 240
-unit = PPM`"]

O1 -->|hasFeatureOfInterest| C
O2 -->|hasFeatureOfInterest| C
O1 -->|hasUltimateFeatureOfInterest| D
O2 -->|hasUltimateFeatureOfInterest| D
O1 -->|hasResult| R1
O2 -->|hasResult| R2
R1 -->|correspondsToVariable| P1
R2 -->|correspondsToVariable| P2

%% Derived Paleo Observation
P["`(sosa:Observation)
PaleoCO2Observatie
-observedProperty = CO2Concentratie
-result = 240 PPM
-phenomenonTime = 7530 BP`"]

P -->|hasFeatureOfInterest| D

%% Input relations
P -->|hasInputValue| R1
P -->|hasInputValue| R2

%% Procedure
PR["`(sosa:Procedure)
ProcedurePaleoCO2Contentratie`"]

P -->|usedProcedure| PR

PR -->|hasInput| P1
PR -->|hasInput| P2

```

