# VLAREM-rubrieken — alternatief: een bereik per eenheid

## Intentie

Geen herziening. Dit alternatief staat naast het hoofdmodel (`../vlarem_rubrieken.ttl`): twee
verdedigbare lezingen van hetzelfde criterium, voor de werkgroep. Status: **open** (2026-10-21).

Het hoofdmodel groepeert per **grens** (ondergrens, bovengrens), elk met een operator en een waarde
per eenheid. Dit alternatief groepeert per **eenheid**: elke alternatieve uitdrukking van het
criterium is één bereik, een `qudt:QuantityValue` met een onder- en een bovengrens. Het volgt het
patroon *Rapportagegrens* (`oslo-ld-kit/guide/patterns.md`), waarin `../../waterkwaliteit/` een
waarde onder de rapportagegrens als interval `qudt:lowerBound`/`qudt:upperBound` geeft.

## Bron en selectie

Dezelfde bron als het hoofdmodel (`../source/`): rubriek 17.4, versie 2017-02-23, criterium 01. De
volledige selectie, met de hand geschreven.

## Verschillen met het hoofdmodel

| Aspect | Hoofdmodel | Alternatief |
|---|---|---|
| groepering | per grens: `vlarem:hasMin`, `vlarem:hasMax` | per eenheid: `qudt:quantityValue` op het criterium |
| knopen per criterium (2 grenzen, 2 eenheden) | 2 grenzen + 4 waarden | 2 bereiken |
| inclusief of exclusief | `vlarem:operator` naar een concept (`operator:GT`, …) | de property: `qudt:minExclusive`, `qudt:minInclusive`, `qudt:maxExclusive`, `qudt:maxInclusive` |
| nieuwe termen | `vlarem:CriteriumConstraint`, `hasConstraint`, `hasMin`, `hasMax`, `operator`, lijst vergelijkingsoperatoren | geen (enkel `vlarem:Criterium` en `vlarem:hasCriterium`, gedeeld) |
| alternatieve eenheden | per grens, meerdere waarden | per criterium, meerdere bereiken |
| andere grenzen per eenheid (bv. 50 l of 100 kg) | mogelijk | mogelijk |
| één grens in maar één eenheid | mogelijk | een bereik zonder onder- of bovengrens |

Gedeelde IRI's: de rubriekversie en het criterium (`…/3333/2017-02-23/01`). Wat verschilt, heeft een
eigen pad: `…/01/bereik/L` en `…/01/bereik/KiloGM` (het hoofdmodel gebruikt `…/01/min/…` en
`…/01/max/…`). Beide bestanden kunnen dus samen geladen worden.

## Transformatie

Geen; met de hand geschreven.

## Diagram

- `vlarem_rubrieken_bereik.mmd` — dit alternatief.
- `vlarem_rubrieken_vergelijking.mmd` — hoofdmodel en alternatief naast elkaar.

## Outputbestanden

| Bestand | Inhoud |
|---|---|
| `vlarem_rubrieken_bereik.ttl` | het criterium met twee bereiken (l en kg) |
| `vlarem_rubrieken_bereik.mmd` | diagram |
| `vlarem_rubrieken_vergelijking.mmd` | vergelijkingsdiagram |
| `bespreking.md` | bespreking, met argumenten en discussievragen in §6 |
