# VLAREM-rubrieken — hoeveelheden in de criteria van een rubriek

De VLAREM-indelingslijst deelt hinderlijke inrichtingen in rubrieken in. Een eindrubriek legt
criteria vast die bepalen of een inrichting eronder valt, en die criteria gaan altijd over
hoeveelheden: een minimum, een maximum of beide, soms in alternatieve eenheden ("meer dan 50 l of
50 kg"). Dit voorbeeld modelleert die hoeveelheden als extra informatie bij een rubriek. Het is
**geen SSN/SOSA-mapping**: een criterium is een norm, geen waarneming. De rubrieken zelf zijn
`skos:Concept`s in een SKOS-lijst.

## Bron

- Register: <https://data.omgeving.vlaanderen.be/id/conceptscheme/vlaremrubrieken>, rubriek 17.4
  (<https://data.omgeving.vlaanderen.be/id/concept/vlaremrubrieken/3333>). Op 2026-10-21 gaf
  content negotiation op de rubriek en op haar versie `…/3333/2017-02-23` enkel de beschrijving
  van de documenten (`rdfs:isDefinedBy`, `foaf:page`), geen label of versies.
- Ontvangen voorstel, ongewijzigd in `source/`:

| Bestand | Inhoud |
|---|---|
| `source/duiding` | toelichting bij het voorstel (tekst) |
| `source/hoeveelheden_alt1.trig` | variant 1: grens → `vlarem:alternatieveKwantiteit` → `vlarem:CriteriumKwantiteit` (grootheid + waarde) |
| `source/hoeveelheden_alt2.trig` | variant 2: de grens draagt de grootheden en de waarden zelf |

De twee varianten zijn ontvangen als `.ttl` en hernoemd naar `.trig` (geldige TriG, inhoud
ongewijzigd), zodat de pipeline ze niet valideert (CLAUDE.md §4).

## Transformatie

Geen. De herziene versie is met de hand afgeleid uit de twee varianten.

## Mappingkeuzes

Geen SSN/SOSA. Een criterium (`vlarem:Criterium`) hangt aan de **versie** van de rubriek waarvoor
het geldt. Het heeft een ondergrens (`vlarem:hasMin`) en een bovengrens (`vlarem:hasMax`), elk een
`vlarem:CriteriumConstraint` met een vergelijkingsoperator (`vlarem:operator`, een concept uit de
nieuwe lijst vergelijkingsoperatoren) en per alternatieve eenheid één `qudt:QuantityValue`
(`qudt:numericValue`, `qudt:hasUnit` met een QUDT-eenheid). De grootheid volgt uit de eenheid. Zie
`bespreking.md`.

De termen van `vlarem:` en de operatorlijst staan als ontwerpversie in
`src/main/resources/be/vlaanderen/omgeving/data/ns/vlaremrubrieken/vlaremrubrieken.ttl` en
`src/main/resources/be/vlaanderen/omgeving/data/id/conceptscheme/vergelijkingsoperator/vergelijkingsoperator.ttl`.

**Alternatief:** in [`alternatief/`](alternatief/README.md) staat hetzelfde criterium gegroepeerd
**per eenheid**: één bereik per eenheid, met `qudt:minExclusive`/`qudt:maxExclusive`, naar het
patroon *Rapportagegrens* uit `../waterkwaliteit/`. Het staat naast dit model, voor de werkgroep.

## Verbeterpunten

1. `qudt:value 5000` → `qudt:numericValue 5000.0` → R3: `qudt:value` bestaat, maar is niet het
   QUDT-patroon voor een numerieke waarde (SHACL-regel R3 gaf een violation).
2. `qudt:hasUnit "_:liter"` (een literal) en `schema:unitText "liter"` → `qudt:hasUnit unit:L`
   en `unit:KiloGM` → `qudt:hasUnit` is een object property met bereik `qudt:Unit`; een literal is
   geen eenheid (SHACL-violation op `qudt:Quantifiable`). `schema:unitText` herhaalt de eenheid als
   tekst, het label staat al in QUDT; bovendien gebruikte het `http://schema.org/` en niet de vorm
   die de geladen schema.org-termen gebruiken (`https://`, R17).
3. `qudt:hasQuantityKind _:volume, _:massa` (blank nodes) → weggelaten → de grootheid volgt uit de
   QUDT-eenheid (`unit:L qudt:hasQuantityKind quantitykind:Volume`, `unit:KiloGM` →
   `quantitykind:Mass`). In variant 2 stonden twee grootheden en twee waarden los naast elkaar op
   de grens, zonder te zeggen welke grootheid bij welke waarde hoort; in variant 1 bij
   `…/min/waarde` ook.
4. Tussenlaag `vlarem:CriteriumKwantiteit` en `vlarem:alternatieveKwantiteit` (variant 1) →
   weggelaten: de grens verwijst rechtstreeks naar haar waarden met `qudt:quantityValue`
   (variant 2) → zonder de grootheid (punt 3) draagt de tussenlaag niets meer; elke waarde is al een
   alternatieve uitdrukking van de grens.
5. `dcterms:type _:LT` → `vlarem:operator operator:LT`, een concept in de nieuwe lijst
   vergelijkingsoperatoren → een blank node is geen code waarnaar andere data kan verwijzen (R10);
   `dcterms:type` heeft bereik `rdfs:Class` en zou van de operator een klasse maken.
6. `dc:subject "Maximale opslag van gevaarlijke stoffen"` → `rdfs:label "Opslag van gevaarlijke
   stoffen"@nl` → `dc:subject` (DC Elements) is niet geladen en wijst naar het onderwerp, niet naar
   de naam van het criterium; "maximale" klopt niet voor een criterium met ook een ondergrens. De
   code voor het onderwerp (de TODO in de bron) blijft open, zie `bespreking.md` §6.
7. `vlarem:hasCriterium` op de rubriek (`…/3333`) → op de versie (`…/3333/2017-02-23`) → de IRI van
   het criterium bevat de versiedatum; grenzen veranderen tussen VLAREM-versies, dus het criterium
   hoort bij één versie.
8. Rubriek beschreven in de data (`a skos:Concept`, `rdfs:label`, `pav:hasVersion`,
   `pav:hasCurrentVersion`) → weggelaten → dat zijn uitspraken van het register over zijn eigen
   concepten (*Code lists and registers* in de gids); PAV is ook niet geladen.
9. Termen in `vlarem:` zonder definitie (onbekend voor `validate_file`) → ontwerpversie van het
   vocabularium in `src/main/resources/`, met label, definitie en OWL-restricties waaruit de SHACL
   gegenereerd wordt.

## Diagram

- `vlarem_rubrieken.mmd` — het herziene model.
- `vlarem_rubrieken_vergelijking.mmd` — de ontvangen varianten en de herziening naast elkaar.

## Outputbestanden

| Bestand | Inhoud |
|---|---|
| `vlarem_rubrieken.ttl` | herziene versie: criterium van rubriek 17.4 met twee grenzen in l en kg |
| `vlarem_rubrieken.mmd` | diagram |
| `vlarem_rubrieken_vergelijking.mmd` | vergelijkingsdiagram |
| `bespreking.md` | bespreking in negen secties |
| `alternatief/` | alternatieve mapping: een bereik per eenheid |

## Gebruik

```bash
# één bestand (MCP): mcp__ld-vocab__validate_file src/main/input/vlarem_rubrieken/vlarem_rubrieken.ttl
java -jar tools/ld-mcp-vocab.jar validate --ontologies src/main/resources \
    --rules src/main/resources/be/vlaanderen/ssnsosa/data/id/rule/domain-range-subproperty.rules \
    --generate-shapes --shapes oslo-ld-kit/rules/ssn-sosa-rules.ttl \
    --prefix-registry src/main/cc/prefix/prefix.cc.ttl --extensions ttl src/main/input/vlarem_rubrieken
```
