# Wat bestudeer ik?

De belangrijkste keuze van elk model, en de keuze waar het vaakst over gediscussieerd wordt.
SOSA noemt het *feature of interest*, in het Nederlands het **studieobject**: "de entiteit die
het doelwit is van een uitvoering, waarvan de eigenschap geschat, gewijzigd of bemonsterd wordt".

## De toets

Stel bij elke waarde de vraag: **van welk ding is dit een eigenschap?**

| Waarde | Eigenschap | Studieobject | Niet het studieobject |
|---|---|---|---|
| 1,23 m grondwaterpeil | peil | de filter in de put (of het grondwaterlichaam) | de sonde, de gemeente |
| 0,42 mg P/L | massaconcentratie totaal fosfor | het staal afvalwater | het labo, het bedrijf |
| 214 fietsers 08–09 u | verkeersintensiteit | het telpunt op de route | de teller |
| 74 dB(A) LAmax | geluidsniveau | de meetpost (of het geluidsevent, zie onder) | het vliegtuig |
| 2,4 m³ sediment | sedimentvolume | de erosiepoel | de waarnemer |

Wie het studieobject verwart met het toestel (de sonde, de teller), modelleert een eigenschap van
de sensor in plaats van van de wereld. Wie het verwart met een veel groter gebied (de gemeente),
verliest wat er precies gemeten werd.

## Monsters

Vaak meet je niet het ding zelf, maar een representatief deel ervan: een staal water uit een
lozing, een luchtbel uit een ijskern, een telpunt op een route. SOSA heeft daarvoor
`sosa:Sample`, met drie subklassen:

| Klasse | Wanneer | Voorbeeld |
|---|---|---|
| `sosa:MaterialSample` | een fysiek deel | een staal afvalwater, een bodemmonster, een ijskern |
| `sosa:SpatialSample` | een plaats binnen een groter gebied | een telpunt, een meetplaats op een waterloop, een rastercel |
| `sosa:StatisticalSample` | een statistische steekproef | een selectie van huishoudens |

Wanneer waarnemingen over een monster gaan, is het monster ook een studieobject. SOSA 2023 maakt
`sosa:Sample` geen subklasse van `sosa:FeatureOfInterest`; type het daarom expliciet met beide
([R1](../regels/r01.md)). Het monster verwijst met `sosa:isSampleOf` naar wat het
vertegenwoordigt, en dat is verplicht: een monster is altijd een monster *van* iets.

```turtle
ex:staal-1 a sosa:MaterialSample , sosa:FeatureOfInterest ;
    sosa:isSampleOf ex:lozing-2400006 ;
    sosa:isResultOf ex:staalname-1 .        # de bemonstering die het monster opleverde

ex:waarneming-1 sosa:hasFeatureOfInterest ex:staal-1 ;
    sosa:hasUltimateFeatureOfInterest ex:lozing-2400006 .
```

- Het **studieobject** van de waarneming is het monster: dat werd geanalyseerd.
- Het **uiteindelijke studieobject** (`sosa:hasUltimateFeatureOfInterest`) is wat het monster
  vertegenwoordigt. Het is af te leiden uit de keten, maar expliciet maakt het queries kort.
- Monsters kunnen ketens vormen: een luchtbel is een monster van een ijskern, die een monster is
  van de aardkorst ([R8](../regels/r08.md)).
- `sosa:isSampleOf` is een subproperty van `prov:wasDerivedFrom`: de keten is ook herkomst.

Het patroon staat in [Monster en uiteindelijk studieobject](../patronen/monster.md) en
[Ruimtelijk monster](../patronen/ruimtelijk-monster.md).

## Eén ding, meerdere rollen

Een meetpunt is vaak tegelijk een plaats die toestellen herbergt en het ding waarover gemeten
wordt. SOSA laat meerdere types toe, en dat is geen fout maar precisie:

```turtle
ex:meetpunt a sosa:Platform , sosa:FeatureOfInterest , sosa:SpatialSample .
```

- `sosa:Platform`: het herbergt de teller (`sosa:hosts`);
- `sosa:FeatureOfInterest`: de waarnemingen gaan erover;
- `sosa:SpatialSample`: het staat voor een groter gebied.

Leg in de bespreking uit waarom een resource meerdere types heeft ([De bespreking](../werkwijze/bespreking.md), sectie 3).

## Plaats of oorzaak?

Bij gebeurtenissen (een overvliegend toestel, een overstorting, een lozing) zijn twee lezingen
verdedigbaar:

| Lezing | Studieobject | Patroon | Kies het wanneer |
|---|---|---|---|
| de toestand van een plaats | de meetpost, het meetpunt | [Stimulus](../patronen/stimulus.md) | de vraag gaat over de plaats: hoeveel geluid krijgt deze wijk? |
| de uitstoot zelf | de emissie (het geluidsevent, de lozing) | [Emissie als studieobject](../patronen/emissie.md) | de vraag gaat over de bron: hoeveel geluid maakt deze vlucht? |

Beide lezingen staan in dit project naast elkaar uitgewerkt, voor de werkgroep om te kiezen
([geluidsmeetnet](../casussen/geluidsmeetnet.md), [overstort](../casussen/overstort.md)). Een
alternatief uitwerken is beter dan stil kiezen ([Een alternatief uitwerken](../werkwijze/alternatief.md)).

## De eigenschap

Het studieobject en de eigenschap horen samen: een eigenschap is "een identificeerbare kwaliteit
van studieobjecten". Kies ze op het niveau dat waarnemingen vergelijkbaar maakt:

- **specifiek genoeg**: "massaconcentratie totaal fosfor in water", niet "fosfor";
- **zonder eenheid**: "temperatuur", niet "temperatuur in °C";
- **zonder methode of toestel**: die horen bij de procedure en de sensor;
- **uit een register** waar er een is (een CSOR-parameteraspect), anders als `sosa:Property` met
  een eigen IRI ([Register en I-ADOPT](../kaart/register-iadopt.md)).

!!! valkuil "Verouderde klassen voor de eigenschap"
    `sosa:ObservableProperty` en `sosa:ActuatableProperty` bestaan in SSN/SOSA 2023 niet meer als
    aparte klassen: het is `sosa:Property`, voor beide ([R14](../regels/r14.md)).

## Samengevat

1. Het studieobject is het ding waarvan de waarde een eigenschap is.
2. Meet je een representatief deel, dan is dat deel (het monster) het studieobject, en het geheel
   het uiteindelijke studieobject.
3. Eén resource mag meerdere rollen hebben; zeg waarom.
4. Bij gebeurtenissen: kies tussen plaats en bron op basis van de vraag, of werk beide uit.
