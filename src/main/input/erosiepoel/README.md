# Erosiepoel — veldobservaties ter ondersteuning van erosiebeheer

## Bronbestand

Ontvangen Turtle-bestand: `source/erosiepoel2.ttl.bak`. Aangeleverd scenario: veldobservatie
van een erosiepoel beheerd door Stad Mechelen. Geen persistente externe databron-URI; de herziene
versie gebruikt `https://example.org/erosiepoel/` als basis voor illustratieve IRIs.

## Transformatieproces

Geen automatische transformatie vereist. De herziene Turtle-data is rechtstreeks als voorbeeld
aangemaakt op basis van het ontvangen bronbestand. Het bronbestand staat in
`source/erosiepoel2.ttl.bak`; dit bestand wordt niet door de pipeline verwerkt (`.bak`-extensie).

## Mapping-keuzes

Plat model met `sosa:ObservationCollection`. De erosiepoel fungeert zowel als `sosa:Platform`
(host van de veldwaarnemer) als `sosa:FeatureOfInterest` (het object van de observatie).
Één observatie meet het sedimentvolume na een nachtelijke regenbui.

## Verbeterpunten

Vergeleken met het ontvangen bronbestand (`source/erosiepoel2.ttl.bak`) zijn de volgende
fouten gecorrigeerd:

1. **`ep:Erosiepoel` (domein-klasse) → `sosa:Platform + sosa:FeatureOfInterest`** — de
   erosiepoel moet getypeerd worden met SSN/SOSA-klassen. `sosa:Platform` is vereist omdat
   de poel de veldwaarnemer host; `sosa:FeatureOfInterest` omdat de poel het bestudeerde
   object is.

2. **`sosa:ObservableProperty` (niet herkend door pipeline) → `sosa:Property`** — de geladen
   SSN/SOSA 2023-ontologie definieert `sosa:Property` als basisklasse; `sosa:ObservableProperty`
   is een afgeleid concept dat niet als OWL-klasse aanwezig is in de geladen ontologie.

3. **`qudt:unit` → `qudt:hasUnit`** — het correcte predikaat voor eenheidsannotatie in QUDT
   is `qudt:hasUnit`; `qudt:unit` bestaat niet in de geladen QUDT-ontologie.

4. **`prov:startedAtTime` / `prov:endedAtTime` → `sosa:phenomenonTime` + `sosa:resultTime`** —
   PROV-O tijdsproperties beschrijven activiteiten in provenance-context; SSN/SOSA voorziet
   aparte properties voor fenomeentijd en resultaattijd.

5. **Geen `sosa:Sensor` gedefinieerd** → `ex:Waarnemer_X a sosa:Sensor` toegevoegd.
   `sosa:Sensor` is vereist als subject van `sosa:implements` en als value van `sosa:madeBySensor`.

6. **Geen `sosa:ObservationCollection`** → toegevoegd om gedeelde metadata (sensor, procedure,
   tijdstip) op collection-niveau te bundelen en uitbreiding naar meerdere observaties te
   ondersteunen.

7. **Geen `sosa:usedProcedure`** → `ex:VeldmeetProcedure` toegevoegd met typering
   `sosa:ObservingProcedure`. `sosa:usedProcedure` is sterk aanbevolen voor
   reproducibiliteitsclaims.

## Grafische voorstelling

- Herziene modellering: [erosiepoel_herzien.mmd](erosiepoel_herzien.mmd)
- Vergelijking voor/na: [erosiepoel_vergelijking.mmd](erosiepoel_vergelijking.mmd)

## Outputbestanden

- `erosiepoel_herzien.ttl` — gecorrigeerde primaire RDF-data
- `src/main/output/erosiepoel/erosiepoel_herzien.jsonld` — gegenereerde JSON-LD

## Gebruik

```bash
mvn compile exec:java
```
