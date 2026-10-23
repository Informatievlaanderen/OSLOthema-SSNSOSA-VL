# IRI's

Elke resource die je beschrijft, heeft een naam nodig. In linked data is dat een IRI, en de keuze
bepaalt of anderen ernaar kunnen verwijzen, of de naam stabiel blijft, en wie hem beheert
([R10](../regels/r10.md)).

## Welke basis?

| Situatie | Basis | Voorbeeld |
|---|---|---|
| productiedata | de gezaghebbende namespace van het domein | `https://www.dov.vlaanderen.be/data/filter/…`, `https://data.omgeving.vlaanderen.be/id/…` |
| illustratieve voorbeelden | deelpaden van `https://example.org/` met betekenisvolle namen | `https://example.org/verkeersmetingen/meetpunt-FMN-021` |
| begrippen van een register | de IRI's van het register | `https://data.omgeving.vlaanderen.be/id/concept/csor/eenheid/E_131` |
| termen van een vocabularium | precies de IRI die de uitgever definieert | `http://www.w3.org/ns/sosa/Observation` |

Niet `example.com`, en geen IRI's verzinnen in de namespace van een ander.

## Blanco knoop of IRI?

- **Een IRI** voor alles waar van buitenaf naar verwezen moet worden: een meetpunt, een sensor,
  een waarneming, een resultaat dat inputwaarde wordt.
- **Een blanco knoop** mag voor kleine, geneste dingen in een handgeschreven voorbeeld: een
  interval, een tijdstip, een resultaat, een geometrie.
- **In grote, gescripte datasets** krijgen ook die geneste dingen een deterministische IRI, een
  *skolem-IRI*, afgeleid van de ouder: `ex:interval-{waarneming}`, `ex:tijdstip-{waarneming}-begin`,
  `ex:resultaat-{waarneming}`, `ex:geometrie-{station}`. Blanco knopen zijn moeilijk te bevragen
  en voegen slecht samen over grafen heen.
- **Uitzondering**: wie een extern dataset beschrijft dat hij niet beheert, verzint geen IRI's in
  de namespace van een ander; daar is een blanco knoop aanvaardbaar.

## Stabiel over runs heen

Een script leidt elke IRI af van een **deterministische sleutel**: een identificatie uit de bron,
of een hash van de velden die de resource identificeren. Nooit van een willekeurige waarde per run
(`STRUUID()`, `UUID()`).

```text
fout:  https://aquafin.be/id/sensor/{STRUUID()}          → elke run een andere IRI
goed:  https://aquafin.be/id/sensor/{MD5(toestelnummer)}  → altijd dezelfde
```

Een IRI die bij elke run verandert, kan niet als doel van een verwijzing dienen, en breekt een
versieketen ([casus overstort](../casussen/overstort.md), verbeterpunt 3).

## Niet in de namespace van een vocabularium

Beschrijf geen nieuwe resources in de namespace van een geladen vocabularium: geen
`unit:EUR a qudt:Unit` (QUDT heeft `unit:CCY_EUR`), geen gebouw in de namespace van een
gebouwontologie. Gebruik een eigen IRI of een bestaande term.

## `http` of `https`, `#` of `/`

De identificatie van een term is precies de IRI van de uitgever. `http://qudt.org/schema/qudt/Unit`
is de term; `https://qudt.org/schema/qudt/Unit` is een andere IRI, ook al stuurt de website door.
Hetzelfde voor een namespace met `#` of `/`. Controleer eerst de `@prefix`-regel: één fout prefix
breekt elke term die het gebruikt.

## Prefixen

- Declareer elk prefix dat het bestand gebruikt, en enkel die.
- Gebruik het gangbare prefix voor een namespace ([prefix.cc](http://prefix.cc)); een prefix dat
  gewoonlijk iets anders betekent (`geo:` voor WGS84 in plaats van GeoSPARQL), verwart.
- Onderscheid de schema-namespace van de data-namespaces: `qudt:` voor `qudt:hasUnit`, `unit:` voor
  `unit:M`.

De [prefixtabel](../bijlagen/prefixen.md) geeft de prefixen van dit werk.
