# VLAREM-rubrieken, alternatief: een bereik per eenheid — bespreking

Status: **open** (2026-10-21). Dit alternatief staat naast het hoofdmodel
([`../bespreking.md`](../bespreking.md)), geen van beide is fout. De keuze is aan de werkgroep.

## 1. Wat stelt dit voorbeeld voor?

Hetzelfde criterium als het hoofdmodel: VLAREM-rubriek 17.4, versie 2017-02-23, opslag van
gevaarlijke stoffen van meer dan 50 en minder dan 5000 liter of kilogram
(<https://data.omgeving.vlaanderen.be/id/concept/vlaremrubrieken/3333>). Hier is elke alternatieve
uitdrukking van het criterium één **bereik**: 50–5000 l en 50–5000 kg, elk een `qudt:QuantityValue`
met een ondergrens en een bovengrens. Net als het hoofdmodel is het geen SSN/SOSA-voorbeeld.

## 2. Kleurlegenda

| Kleur | Concept | Betekenis in dit voorbeeld |
|---|---|---|
| Blauw (#60c4e4) | versie van een rubriek (register) | rubriek 17.4, versie 2017-02-23 |
| Paars (#7f59ae) | `vlarem:Criterium` | het criterium |
| Oranje (#f8b622) | `qudt:QuantityValue` | een bereik in één eenheid |

Subgraphs: `REGISTER` (lichtblauw), `CRITERIUM` (lichtpaars), `WAARDEN` (lichtgeel). Geen
oranjerode nodes: dit alternatief heeft geen operatorlijst.

## 3. Infrastructuur (blauwe nodes)

Geen infrastructuur. De versie van de rubriek, `…/vlaremrubrieken/3333/2017-02-23`, is dezelfde
als in het hoofdmodel en wordt ook hier niet beschreven: dat doet het register.

## 4. Observatie/Actuatie-structuur (roze nodes)

Geen observaties. De structuur van het criterium:

| IRI | type | ondergrens | bovengrens | eenheid |
|---|---|---|---|---|
| `…/3333/2017-02-23/01` | `vlarem:Criterium` | – | – | – |
| `…/01/bereik/L` | `qudt:QuantityValue` | `qudt:minExclusive 50.0` | `qudt:maxExclusive 5000.0` | `unit:L` |
| `…/01/bereik/KiloGM` | `qudt:QuantityValue` | `qudt:minExclusive 50.0` | `qudt:maxExclusive 5000.0` | `unit:KiloGM` |

Het criterium verwijst met `qudt:quantityValue` naar de bereiken; meerdere bereiken zijn
alternatieven ("50–5000 l **of** 50–5000 kg").

## 5. Procedure en Property

Geen `sosa:Procedure` of `sosa:Property`. Zoals in het hoofdmodel volgt de grootheid uit de eenheid
(`unit:L` → `quantitykind:Volume`, `unit:KiloGM` → `quantitykind:Mass`), en staat het onderwerp
enkel als `rdfs:label` op het criterium.

## 6. Modelleer-keuzes toegelicht

### Waarom een bereik per eenheid?

Verworpen alternatief (hier: het hoofdmodel): grenzen als eigen knopen (`vlarem:hasMin`,
`vlarem:hasMax`), elk met een operator en een waarde per eenheid. Gekozen aanpak: één
`qudt:QuantityValue` per eenheid, met de grenzen als properties. Rationale: zie de argumenten
hieronder; het is een keuze voor de werkgroep, niet een correctie.

**Volgt:** het patroon *Rapportagegrens* (`oslo-ld-kit/guide/patterns.md`), gebruikt in
`../../waterkwaliteit/`: een waarde onder de rapportagegrens is daar een `qudt:QuantityValue` met
`qudt:lowerBound` en `qudt:upperBound` en zonder `qudt:numericValue`. Dit alternatief gebruikt de
subproperties `qudt:minExclusive` en `qudt:maxExclusive` (⊂ `qudt:lowerBound`, `qudt:upperBound`)
om ook te zeggen dat de grenzen zelf niet meetellen.

**Argumenten voor**
- Geen nieuwe termen buiten `vlarem:Criterium` en `vlarem:hasCriterium`: geen grensklasse, geen
  `hasMin`/`hasMax`/`operator`, geen operatorlijst. Alles wat de grenzen uitdrukt, is QUDT (kern,
  R17 niveau 1).
- Minder knopen: 2 bereiken in plaats van 2 grenzen en 4 waarden.
- Een bereik zit in één eenheid, net als een gemeten waarde: of een opslag van 300 l onder het
  criterium valt, volgt uit één knoop (`…/bereik/L`), zonder de ondergrens en de bovengrens in
  dezelfde eenheid bij elkaar te zoeken.
- De richting en de inclusiviteit zitten in één term (`minExclusive`, `maxInclusive` …); een
  ondergrens met operator LT, die het hoofdmodel toelaat, kan hier niet.
- Eén patroon voor intervallen over de domeinen heen (rapportagegrens, criterium).

**Argumenten tegen**
- QUDT definieert `qudt:minExclusive` en verwanten als facetten van een *datatype* ("the
  exclusive lower bound of the value space for a datatype"), niet als grenzen van een hoeveelheid;
  het gebruik op een `qudt:QuantityValue` rekt die definitie op. `qudt:maxExclusive` heeft
  bovendien het bereik `xsd:string`, wat niet past bij `5000.0` (`validate_file` meldt het niet).
  `qudt:lowerBound` en `qudt:upperBound` zelf passen beter, maar zeggen niet of de grens
  meetelt.
- Een `qudt:QuantityValue` zonder `qudt:numericValue` is volgens QUDT geen waarde ("the product of
  a numerical value and a unit"), maar een interval. Het patroon *Rapportagegrens* aanvaardt dat al.
- De operator is geen code meer. Wie een koppeling met het omgevingsloket op codes (LT, GE …) wil,
  moet ze uit de property afleiden.
- Wijkt verder af van de ontvangen varianten, die beide per grens groeperen.

**Tussenvormen**
- Het hoofdmodel met `qudt:lowerBound`/`qudt:upperBound` in plaats van `qudt:numericValue`: houdt
  de grensknopen, maar maakt de operator overbodig als de inclusiviteit in de property zit.
- Een bereik per eenheid met twee grensknopen eronder (operator en waarde): bewaart de codes, maar
  voegt de knopen van het hoofdmodel weer toe.

**Discussievragen voor de werkgroep**
1. Waarvoor dient het criterium in de eerste plaats: een gemeten of aangevraagde hoeveelheid
   toetsen (pleit voor een bereik per eenheid), of de grenzen als codes doorgeven aan het
   omgevingsloket (pleit voor grenzen met een operator)?
2. Is het aanvaardbaar om de datatype-facetten van QUDT (`qudt:minExclusive` …) te gebruiken op een
   `qudt:QuantityValue`, of beperken we ons tot `qudt:lowerBound`/`qudt:upperBound` met een aparte
   aanduiding van de inclusiviteit?
3. Hebben de alternatieve eenheden van een rubriek altijd dezelfde getallen (50 l of 50 kg), of
   komen er criteria met verschillende grenzen per eenheid voor? Beide modellen kunnen het, maar
   het bepaalt welke groepering natuurlijker leest.
4. Moet het patroon *Rapportagegrens* in de gids veralgemeend worden tot een patroon *Interval van
   een hoeveelheid*, voor rapportagegrenzen en criteria samen?

### Wat er verandert als dit alternatief gekozen wordt

De restrictie op `vlarem:CriteriumConstraint` en de properties `vlarem:hasConstraint`, `hasMin`,
`hasMax` en `operator` vervallen, net als de lijst vergelijkingsoperatoren. Op `vlarem:Criterium`
kan dan een restrictie `qudt:quantityValue someValuesFrom qudt:QuantityValue` komen. Er is geen
script dat aangepast moet worden.

### Validatie

`validate_file` geeft op `vlarem_rubrieken_bereik.ttl` geen errors, suspects of warnings (4 van 173
shapes op 2 focus nodes).

## 7. Tijdsmodellering

Geen tijdsentiteiten; de geldigheid zit in de versie van de rubriek, zoals in het hoofdmodel.

## 8. Prefixen en IRI-structuur

| Prefix | Basis-IRI | Tijdelijk of persistent |
|---|---|---|
| `vlarem:` | `https://data.omgeving.vlaanderen.be/ns/vlaremrubrieken#` | persistent bedoeld; ontwerpversie, nog niet gepubliceerd |
| `qudt:` | `http://qudt.org/schema/qudt/` | persistent |
| `unit:` | `http://qudt.org/vocab/unit/` | persistent |
| `rdfs:` | `http://www.w3.org/2000/01/rdf-schema#` | persistent |
| – | `https://data.omgeving.vlaanderen.be/id/concept/vlaremrubrieken/` (rubrieken en versies) | persistent (register) |
| – | `https://data.omgeving.vlaanderen.be/id/criterium/vlaremrubrieken/` (criteria) | persistent bedoeld, uit de bron |

De rubriekversie en het criterium hebben dezelfde IRI als in het hoofdmodel. Een bereik krijgt
`…/{criterium}/bereik/{eenheid}` (QUDT-naam van de eenheid), zodat het niet botst met de
`…/min/…` en `…/max/…` van het hoofdmodel en beide samen geladen kunnen worden (R10).

## 9. Inverse relaties

Geen, om dezelfde reden als in het hoofdmodel.
