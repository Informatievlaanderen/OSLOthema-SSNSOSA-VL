# De bespreking in negen vragen

Elk model krijgt een bespreking (`bespreking.md`) die negen vragen beantwoordt, in vaste volgorde,
met één kop per vraag. De vaste vorm maakt besprekingen vergelijkbaar: wie de keuzes van twee
voorbeelden naast elkaar wil leggen, vindt ze op dezelfde plaats.

| # | Kop | Wat erin staat |
|---|---|---|
| 1 | **Wat stelt dit voorbeeld voor?** | het domein in twee tot vier zinnen: welk systeem, welke dataset, welk proces; een IRI van de bron als die er is |
| 2 | **Kleurlegenda** | een tabel kleur → SOSA-klasse → betekenis in het domein |
| 3 | **Infrastructuur (blauwe nodes)** | per blauwe node welke klasse en waarom; meervoudige types uitgelegd; de hiërarchieën van `sosa:hosts` en `sosa:hasSubSystem` |
| 4 | **Observatie/Actuatie-structuur (roze nodes)** | een tabel per waarneming of actuatie: eigenschap, procedure, resultaat, studieobject; wat op de collectie staat en waarom |
| 5 | **Procedure en Property** | per procedure welke sensor ze implementeert en welke waarnemingen ze gebruiken; per eigenschap de betekenis |
| 6 | **Modelleer-keuzes toegelicht** | een paragraaf per niet-triviale keuze (zie onder) |
| 7 | **Tijdsmodellering** | welk tijdpatroon en waarom; fenomeentijd, resultaattijd; de tijdzoneaanname |
| 8 | **Prefixen en IRI-structuur** | een tabel prefix → basis-IRI → tijdelijk of persistent |
| 9 | **Inverse relaties** | welke inverse paren opgenomen zijn en waarom (`sosa:hosts` ↔ `sosa:isHostedBy`, …) |

## Sectie 6: keuzes toelichten

Het hart van de bespreking. Elke keuze in dezelfde vorm:

```markdown
> **Waarom een interval voor de fenomeentijd?**
> Verworpen alternatief: een `time:Instant` op het begin van het uur.
> Gekozen aanpak: een `time:Interval` met begin en einde, halfopen.
> Motivatie: de waarde dekt een uur; een query naar waarnemingen binnen een periode moet ze
> vinden (R12).
```

Behandel de beslispunten die van toepassing zijn:

- `sosa:hasSimpleResult` of `sosa:hasResult` met een `qudt:QuantityValue` ([R3](../regels/r03.md));
- een collectie of losse waarnemingen;
- plat of drielaags ([R4](../regels/r04.md));
- `sosa:hasInput` of `prov:used` ([R5](../regels/r05.md));
- een ML-model als entiteit of als sensor ([R6](../regels/r06.md));
- `p-plan:correspondsToVariable` en `p-plan:correspondsToStep`;
- een ruimtelijk monster of een gewoon studieobject voor een meetpunt ([R11](../regels/r11.md));
- tijdstip of interval ([R12](../regels/r12.md));
- een afgeleide waarneming of een gewoon collectielid ([R7](../regels/r07.md), [R13](../regels/r13.md));
- QUDT-eenheid of register-eenheid ([R3](../regels/r03.md));
- de waarneming of een apart record als gepubliceerde resource ([R16](../regels/r16.md));
- welk vocabularium voor een term buiten de kern ([R17](../regels/r17.md)), met een paragraaf
  *Waarom dit vocabularium?*;
- welk patroon gevolgd is, of waarom niet ([V. Patronen](../patronen/index.md)).

Vermeld er ook: de register-eenheden en hun QUDT-mapping, de waarschuwingen die bewust blijven
staan (bv. geen geometrie omdat de bron geen plaats geeft), en een eventueel alternatief, met een
link.

## Plaatshouders

Een vraag die nog open ligt, wordt een concrete vraag in een HTML-commentaar:

```markdown
<!-- TODO: is de meetput hetzelfde object als het lozingspunt in RIE-IEPR? -->
```

Nooit "nog aan te vullen".

## Voorbeelden

Elke casus in [VII](../casussen/index.md) verwijst naar haar bespreking op GitHub. Goede
uitgangspunten om te lezen: [verkeersmetingen](../casussen/verkeersmetingen.md) (plat, met een
afgeleide waarneming), [overstort](../casussen/overstort.md) (een herziening met vocabulariumkeuzes)
en [elektrisch raam](../casussen/elektrisch-raam.md) (drielaags).
