# Een alternatief uitwerken

Een herziening vervangt een fout model. Een **alternatief** staat naast een model dat niet fout
is: twee verdedigbare lezingen van dezelfde data, die elkaar niet uitsluiten. De keuze ligt bij de
werkgroep, niet bij wie het voorbeeld schrijft.

## Wanneer

Een keuze is op twee manieren te verdedigen, typisch wanneer:

- de natuurlijke lezing van het domein verschilt van een patroon dat andere voorbeelden al volgen
  (het eigen karakter van het domein tegenover samenhang over domeinen);
- de keuze een beslispunt is voor een werkgroep.

Is het alternatief duidelijk zwakker, dan volstaat een "verworpen alternatief" in de bespreking.
Een uitgewerkt alternatief is voor keuzes die echt open liggen.

## Stappen

1. **Bepaal** welk voorbeeld, welke keuze anders gelezen wordt, en welk ander voorbeeld of patroon
   het alternatief volgt.
2. **Een map** `alternatief/` in het voorbeeld (bij meerdere: `alternatief-<kern>/`), met:
    - een README met **Bedoeling** ("geen herziening; beide lezingen naast elkaar voor de
      werkgroep"), de bron en de selectie, en een tabel **Verschillen met het hoofdmodel**
      (aspect → hoofdmodel → alternatief);
    - de Turtle en het diagram;
    - een vergelijkingsdiagram, gericht op wat verschilt;
    - een bespreking in negen vragen; sectie 6 met de argumenten **voor** en **tegen**,
      tussenvormen en **discussievragen** voor de werkgroep.
3. **Een kleine, representatieve selectie** volstaat (bv. één vlucht): het doel is vergelijken, niet
   volledigheid. Zeg welke wijziging het genererende script zou vragen als het alternatief gekozen
   wordt.
4. **IRI's**: hergebruik die van het hoofdmodel voor wat gedeeld is; geef wat verschilt een eigen
   prefix (`alt:`), zodat beide samen geladen kunnen worden.
5. **Noem het verband**: welk voorbeeld of patroon het alternatief volgt.
6. **Neutraal**: het hoofdmodel heet niet fout. Beide krijgen een status zoals in een
   beslisdocument (*voorstel*, *open*, *beslist* met datum).
7. **Verwijs in beide richtingen**: de bespreking van het hoofdmodel noemt het alternatief bij de
   betrokken keuze, en omgekeerd.
8. **Toets** beide.

## Na een beslissing

Het gekozen model wordt het hoofdmodel (pas het script aan indien nodig). Het andere blijft als
gedocumenteerd verworpen alternatief, met status *beslist* en de datum: waarom de keuze gemaakt
werd, is ook kennis. Verwijder het niet. Zet een beslissing een patroon, dan komt dat in de gids.

## Casussen

| Voorbeeld | Hoofdmodel | Alternatief | Volgt |
|---|---|---|---|
| [geluidsmeetnet](../casussen/geluidsmeetnet.md) | geluidsevent als [stimulus](../patronen/stimulus.md), meetpost als studieobject | geluidsevent als [emissie](../patronen/emissie.md) en studieobject | de lozing in waterkwaliteit |
| [overstort](../casussen/overstort.md) | overstortevent als waarneming van het meetpunt | overstorting als emissie, resultaat van een actuatie | idem |
| [VLAREM-rubrieken](../casussen/vlarem.md) | één criterium met grenzen per operator | één bereik per eenheid (`qudt:minExclusive` …) | — |
