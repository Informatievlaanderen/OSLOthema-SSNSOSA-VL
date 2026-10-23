# Register en I-ADOPT

**Wat is de waargenomen eigenschap precies?** Bij een fosformeting in afvalwater kan de
`sosa:observedProperty` "fosfor" zijn, of "fosfor in water", of "totaal fosfor, massaconcentratie,
in afvalwater". I-ADOPT ontleedt zo'n variabele in componenten. Dit hoofdstuk vat samen hoe het
Vlaamse parameterregister CSOR daarop aansluit, en wat dat betekent voor de keuze van de
eigenschap.

| | |
|---|---|
| **Soort** | analyse en voorstel (nog geen gepubliceerde module) |
| **I-ADOPT** | RDA-werkgroep *InteroperAble Descriptions of Observable Property Terminology*, `https://w3id.org/iadopt/ont/` |
| **Volledige analyse** | [`csor_iadopt.md`](https://github.com/Informatievlaanderen/OSLOthema-SSNSOSA-VL/blob/main/src/main/input/waterkwaliteit/csor_iadopt.md), met een script dat alle registerelementen toetst |

## 1. I-ADOPT in het kort

| Component | Klasse / eigenschap | Voorbeeld |
|---|---|---|
| de variabele | `iadopt:Variable` | totaal fosfor, massaconcentratie, in water |
| de eigenschap (grootheid) | `iadopt:hasProperty` → `iadopt:Property` | massaconcentratie |
| het object | `iadopt:hasObjectOfInterest` → `iadopt:Entity` | fosfor |
| de matrix | `iadopt:hasMatrix` → `iadopt:Entity` | water |
| een beperking | `iadopt:hasConstraint` → `iadopt:Constraint` | totaal, opgelost |
| een statistiek | `iadopt:hasStatisticalModifier` | jaargemiddelde, maximum |

I-ADOPT laat eenheden, instrumenten, methoden en plaats **uitdrukkelijk buiten** de variabele. Die
horen in de waarneming: het resultaat, de procedure, de sensor, het studieobject. Dat past precies
bij SOSA.

I-ADOPT bevat zelf geen alignment met SOSA of QUDT. De natuurlijke lezing: een `iadopt:Variable`
is wat SOSA een `sosa:Property` noemt, op het niveau van detail dat de waarneming nodig heeft.

## 2. Wat de analyse vond

**Het juiste niveau voor `sosa:observedProperty` is het CSOR-parameteraspect.** Een
parameteraspect combineert precies één grootheid met wat gemeten wordt, in een matrix, eventueel
met een soort waardebepaling. Dat is de opbouw van een I-ADOPT-variabele. Niet de parameter
("fosfor") en niet de variabele van CSOR, maar het parameteraspect is dus de eigenschap van de
waarneming. In het register is `csor:ParameterAspect` al een subklasse van `sosa:Property`.

**De facetten passen maar deels.** De matrix en de grootheid passen goed. Twee facetten wijken af:

- de CSOR-*variabele* is meestal een stof (I-ADOPT: object), maar soms zelf een eigenschap
  (debiet, temperatuur, pH);
- de *soort waardebepaling* is een mengvorm: beperkingen (opgelost, totaal) staan er naast
  voorbehandelingen, toestellen en methoden, die I-ADOPT uit de variabele weert.

**Voor de waterkwaliteitsdata is de aansluiting goed.** Van de 452 gebruikte parameteraspecten
zijn er 347 (77 %) rechtstreeks om te zetten. Over het hele register bevatten 336 van de 8179
actieve parameteraspecten minstens één element dat niet op zijn plaats staat.

## 3. Het voorstel

- In CSOR de klassen aligneren met **subklassen**, niet met SKOS: `csor:ParameterAspect ⊂
  iadopt:Variable`, de aspecten ⊂ `iadopt:Property` ([R15](../regels/r15.md)).
- De I-ADOPT-beschrijving per parameteraspect **genereren** waar ze eenduidig is.
- De herstructurering van de soort waardebepaling is een punt voor de beheerder van het register.

Status: *voorstel*, voorgelegd in het [beslisdocument](../werkwijze/beslisdocument.md) van
waterkwaliteit (deel C).

## 4. Wat je eruit meeneemt, ook buiten waterkwaliteit

- **Kies de eigenschap op het niveau van de variabele**, niet op dat van de stof: "massaconcentratie
  totaal fosfor in water", niet "fosfor". Twee waarnemingen met dezelfde eigenschap moeten
  vergelijkbaar zijn.
- **Eenheid, methode en toestel horen niet in de eigenschap.** De eenheid hoort bij het resultaat
  ([SOSA en QUDT](sosa-qudt.md)), de methode bij de procedure, het toestel bij de sensor.
- **Een alignment met een register toets je met een script** over alle elementen, niet met een
  handvol voorbeelden ([Ontologieën aligneren](../werkwijze/aligneren.md)).
