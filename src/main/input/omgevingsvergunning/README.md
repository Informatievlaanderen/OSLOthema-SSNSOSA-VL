# Omgevingsvergunning — de gewone procedure als plan, gekoppeld aan dienst en product

Hoe modelleer je een vergunningsprocedure en haar procedurestappen? Een gewone codelijst is te
weinig. Een procedure heeft een volgorde, substappen, termijnen, een rechtsgrond, een bevoegde
overheid en wat elke stap nodig heeft en oplevert. En ze moet aansluiten bij de dienst uit de
producten- en dienstencatalogus én bij de dossiers die haar uitvoeren.

Dit voorbeeld werkt de **gewone vergunningsprocedure in eerste administratieve aanleg voor een
project op de Vlaamse lijst** uit. Het brengt drie modellen samen op één IRI per begrip:

| Model | Wat het bijdraagt | Hier |
|---|---|---|
| [AP Omgevingsvergunning](https://data.vlaanderen.be/doc/applicatieprofiel/omgevingsvergunning/) (`ov:`) | de begrippen van het domein: Procedure, Procedurestap, Beroepsmogelijkheid, Zaak, Zaakhandeling, Vergunning, Vergunde Toestand, rechtsgrond, termijn, bevoegde overheid | elke procedure, stap en zaakhandeling |
| [P-PLAN](http://purl.org/net/p-plan) (`p-plan:`) | de structuur: stappen van een plan, volgorde (`isPrecededBy`), substappen (`MultiStep`, `isDecomposedAsPlan`), in- en uitvoer (`Variable`), uitgevoerde stappen (`correspondsToStep`) | wat het AP niet kan uitdrukken |
| [SSN/SOSA 2023](https://www.w3.org/TR/vocab-ssn-2023/) (`sosa:`) | wat een stap met de werkelijkheid doet: een advies is een **waarneming** van het project, de beslissing een **actuatie** op zijn vergunde toestand | adviezen, ontvankelijkheid, beslissing |

[CPSV-AP 3.2.0](https://semiceu.github.io/CPSV-AP/releases/3.2.0/) (`cpsv:`, `cv:`) koppelt de
dienst `publicservice:D3-0098` uit de PDC van het Departement Omgeving aan de procedure
(`cpsv:follows`), en het product `output:P-0098` aan de stap die het oplevert.

## Bron

Geen ontvangen data: het voorbeeld is opgesteld uit de regelgeving en de bestaande datasets.

| Bron | Gebruikt voor |
|---|---|
| Omgevingsvergunningsdecreet (OVD), 25 april 2014, titel III, hoofdstuk II, afdeling 2 *Gewone vergunningsprocedure* (art. 18-36), geconsolideerd na het decreet van 26 januari 2024 ([tekst](https://www.kustcodex.be/kustcodex-consult/plainWettekstServlet?wettekstId=61396&lang=nl)) | stappen, volgorde, termijnen, rechtsgrond per stap |
| Omgevingsvergunningsbesluit (OVB), 27 november 2015, art. 16, 56-63 en 67 ([Vlaamse Codex](https://codex.vlaanderen.be/portals/codex/documenten/1026496.html)) | openbaar onderzoek, adviestermijnen, bekendmaking |
| OVD art. 52 en 105 ([Vlaamse Codex](https://codex.vlaanderen.be/Portals/Codex/documenten/1024690.html)); DBRC-decreet, 4 april 2014 | geen administratief beroep, beroep bij de Raad voor Vergunningsbetwistingen (45 dagen), rechtspleging |
| [AP Omgevingsvergunning](https://data.vlaanderen.be/ns/omgevingsvergunning) (vocabularium, Turtle) | klassen en eigenschappen `ov:` |
| `codelijst-producten_en_diensten` (PDC Departement Omgeving): `publicservice:D3-0098` *verlenen omgevingsvergunning voor projecten op Vlaamse lijst*, `output:P-0098` *beslissing omgevingsvergunning projecten op Vlaamse lijst*, `ovo:OVO003323` Departement Omgeving | de dienst en het product |

Het dossier (zaak OMV_2026000001) is **fictief**; de termijnen kloppen met het OVD.

## Transformatie

Geen: met de hand opgesteld.

Twee vocabularia zijn hiervoor geladen in `src/main/resources/`:

| Bestand | Bron | Versie |
|---|---|---|
| `be/vlaanderen/data/ns/omgevingsvergunning/omgevingsvergunning.ttl` | content negotiation op `https://data.vlaanderen.be/ns/omgevingsvergunning` (`Accept: text/turtle`), 9 november 2026 | geen versie-IRI (`dc:issued "TODO"`) |
| `eu/europa/data/m8g/cpsvap/3.2.0/cpsv-ap.ttl` | `SEMICeu/CPSV-AP`, `releases/3.2.0/rdf/cpsv-ap.ttl` | 3.2.0 (`owl:versionIRI`) |
| `be/vlaanderen/data/ns/omgevingsvergunning/alignments/ov-pplan-prov.ttl` | dit project: alignering van het AP met P-PLAN en PROV-O (bespreking §6) | voorstel, 9 november 2026 |

Met beide geladen geeft de validatie van alle voorbeelden geen fouten meer (35 bestanden, 0
fouten); geen enkel ander voorbeeld kreeg er een melding bij.

## Mappingkeuzes

Drielaags (R4: meerdere stappen, herbruikbaar plan, traceerbaarheid naar het plan), maar **zonder
deploymentlaag**: de actoren worden door de regelgeving aangewezen, niet ingezet. De zaak zelf
draagt het plan (`prov:hadPlan`). In het kort:

- **Procedure = plan.** `plan:gewone-procedure` is `ov:Procedure`, `p-plan:Plan`, `sosa:Procedure`
  en `cpsv:Rule`: één IRI voor het AP, P-PLAN, SOSA en CPSV-AP.
- **Procedurestap = stap.** Elke stap is `ov:Procedurestap` en `p-plan:Step`, met volgorde,
  termijn (`ov:termijn`, een `time:Duration` in dagen) en rechtsgrond per artikel (`dct:source`).
- **Substappen** van het ontvankelijkheids- en volledigheidsonderzoek: een `p-plan:MultiStep` met
  een deelplan (onderzoek, m.e.r.-screening, mededeling). In het dossier heeft de MultiStep een
  eigen uitvoering (`exec:ontvankelijkheid-1`), die het deelplan volgt en de handelingen van de
  substappen als delen heeft.
- **De zaak komt overeen met het plan.** Ze is een `prov:Activity` met `prov:hadPlan` (en
  `ov:procedure`) naar de procedure, geen "eenheid van werk" zoals in het AP Dossier (zie
  verbeterpunten 10 tot 12).
- **Een advies is een waarneming** (`sosa:Observation`) van de verenigbaarheid van het project;
  **de beslissing is een actuatie** (`sosa:Actuation`) op de vergunde toestand, met een
  `ov:VergundeToestand` als resultaat en het besluit als document.
- **Zaakhandeling = uitgevoerde stap.** Elke zaakhandeling verwijst naar haar stap met
  `ov:procedurestap` (AP) én `p-plan:correspondsToStep` (P-PLAN).
- **Dienst en product.** De dienst volgt de procedure (`cpsv:follows`); het product is de
  uitvoervariabele van de beslissing; het concrete besluit `p-plan:correspondsToVariable` het
  product. De links tussen dienst, plan en dossier staan in een tabel in de bespreking (§6, *Hoe
  verbindt het voorbeeld P-PLAN met de PDC?*).
- **Een status als "in voorbereiding" is geen procedurestap.** Ze volgt uit de zaakhandelingen die
  al gebeurd zijn (zie *Gebruik*).

De motivering per keuze staat in [`bespreking.md`](bespreking.md) §6.

## Diagram

[`omgevingsvergunning.mmd`](omgevingsvergunning.mmd): planning (dienst, procedure, stappen,
deelplan, variabelen), infrastructuur (de actoren) en execution (de zaak en haar
zaakhandelingen).

## Uitvoerbestanden

| Bestand | Inhoud |
|---|---|
| `omgevingsvergunning.ttl` | procedure, stappen, dienst, actoren en het fictieve dossier (gevalideerd) |
| `omgevingsvergunning.mmd` | diagram |
| `stand-van-de-zaak.rq` | SPARQL: welke stappen van een zaak nu aan de beurt zijn |
| `bespreking.md` | de negen secties |

## Gebruik

Valideren:

```bash
java -jar tools/ld-mcp-vocab.jar validate --ontologies src/main/resources \
    --rules src/main/resources/be/vlaanderen/ssnsosa/data/id/rule/domain-range-subproperty.rules \
    --generate-shapes --shapes oslo-ld-kit/rules/ssn-sosa-rules.ttl \
    --prefix-registry src/main/cc/prefix/prefix.cc.ttl --extensions ttl \
    src/main/input/omgevingsvergunning
```

**De stand van een zaak afleiden** in plaats van een status bij te houden:
[`stand-van-de-zaak.rq`](stand-van-de-zaak.rq) geeft de stappen die nu aan de beurt zijn (alle
voorgangers uitgevoerd, zelf nog niet).

```bash
sparql --data omgevingsvergunning.ttl --query stand-van-de-zaak.rq
```

```sparql
PREFIX ov:     <https://data.vlaanderen.be/ns/omgevingsvergunning#>
PREFIX p-plan: <http://purl.org/net/p-plan#>
PREFIX rdfs:   <http://www.w3.org/2000/01/rdf-schema#>

# Een stap is uitgevoerd als een zaakhandeling ermee overeenkomt. Ook een stap met substappen
# (p-plan:MultiStep) heeft zo'n zaakhandeling: de activiteit die het deelplan volgt.
SELECT ?zaak ?volgendeStap ?label WHERE {
  ?zaak ov:procedure ?plan .
  ?volgendeStap p-plan:isStepOfPlan ?plan ; rdfs:label ?label .
  FILTER NOT EXISTS { ?h ov:zaak ?zaak ; p-plan:correspondsToStep ?volgendeStap }   # zelf nog niet uitgevoerd
  FILTER NOT EXISTS {                                                               # een voorganger nog niet uitgevoerd
    ?volgendeStap p-plan:isPrecededBy ?voor .
    FILTER NOT EXISTS { ?h ov:zaak ?zaak ; p-plan:correspondsToStep ?voor }
  }
}
```

Voor het fictieve dossier geeft dit *Jurisdictioneel beroep bij de Raad voor
Vergunningsbetwistingen*: de beslissing is bekendgemaakt, de beroepstermijn loopt. Een zaak met
enkel `exec:indiening-1` geeft het ontvankelijkheids- en volledigheidsonderzoek, wat een
applicatie als "in behandeling" of "in voorbereiding" kan tonen. Zo'n weergavestatus hoort in de
applicatie of in een eigen codelijst van statussen, niet bij de procedurestappen.

## Verbeterpunten

Voor het AP Omgevingsvergunning (OSLO):

1. **Rechtsgrond per stap.** `ov:rechtsgrond` heeft als domein `ov:Procedure`. Op een
   Procedurestap maakt het de stap een Procedure. Hier staat de rechtsgrond per stap daarom in
   `dct:source`. Voorstel: domein Procedure *of* Procedurestap.
2. **Volgorde en substappen** ontbreken: het AP kent enkel `dcterms:hasPart` van Procedure naar
   Procedurestap. Voorstel: P-PLAN hergebruiken via een alignering: `ov:Procedure ⊂ p-plan:Plan`,
   `ov:Procedurestap ⊂ p-plan:Step`, `ov:Zaakhandeling ⊂ prov:Activity`,
   `ov:VergundeToestand ⊂ prov:Entity` en `ov:procedurestap ⊑ p-plan:correspondsToStep`. Uitgewerkt
   in `src/main/resources/be/vlaanderen/data/ns/omgevingsvergunning/alignments/ov-pplan-prov.ttl`
   (bespreking §6).
3. **Handeling en werk.** `ov:Vergunning` en `ov:Aanvraag` zijn tegelijk Zaakhandeling (een
   handeling) en, via Rechtshandeling, Juridisch Werk (een werk). PROV-O houdt activiteit en
   entiteit gescheiden. Hier is de zaakhandeling de activiteit en het besluit of het
   aanvraagdossier een apart document (`ov:document`).
4. **Het type hangt af van de uitkomst.** De beslissing is een `ov:Vergunning`, maar bij een
   weigering is er geen passende klasse. Voorstel: een klasse Beslissing (een
   BestuurlijkeRechtshandeling en Zaakhandeling) met de strekking als codelijst.
5. **Aanwendingstermijn** heeft dezelfde IRI als termijn (`ov:termijn`).
6. **Het vocabularium** heeft geen versie (`dc:issued "TODO"`) en zet een Nederlands label op
   `prov:atLocation`.

Voor de PDC:

7. `cpsv:follows` van `publicservice:D3-0098` naar de procedure en `cv:hasLegalResource` naar het
   OVD toevoegen. Het product `output:P-0098` krijgt de typering `p-plan:Variable`.
8. De PDC noemt het Departement Omgeving als `cv:hasCompetentAuthority`; het OVD (art. 15) en het
   AP noemen de Vlaamse Regering als bevoegde overheid. Beide kunnen kloppen, maar de PDC moet
   kiezen welke rol ze bedoelt.

Voor het AP en de PDC samen:

9. **Geen link van een zaak naar de dienst.** In de data is de enige rechtstreekse link van een
   dossier naar de PDC `ent:besluit-1 p-plan:correspondsToVariable output:P-0098`. De zaak
   bereikt de dienst enkel via de procedure (`ov:procedure`, waarna de dienst die procedure volgt
   met `cpsv:follows`). Dat volstaat zolang één procedure bij één dienst hoort. Volgen meerdere
   diensten dezelfde procedure, dan zegt de data niet meer welke dienst een zaak levert. CPSV-AP
   beschrijft de dienst enkel op typeniveau en heeft geen eigenschap van een uitvoering naar een
   dienst; het AP Omgevingsvergunning evenmin. Voorstel: een eigenschap in het AP van Zaak naar
   `cpsv:PublicService` (bv. "levert dienst"). Niet gekozen: `dct:relation` (zegt niets),
   `prov:hadPlan` naar de dienst (een dienst is geen plan), en het besluit typeren als `cv:Output`
   (dan is `cv:Output` tegelijk het product en elk exemplaar ervan). Hetzelfde geldt voor de
   aanvraag: de PDC kan het aanvraagdossier als invoer van de dienst beschrijven (`cv:hasInput`,
   een `cv:Evidence`), maar heeft daar nu niets voor.

Voor het [AP Dossier](https://data.vlaanderen.be/doc/applicatieprofiel/dossier/), waarop het AP
Omgevingsvergunning steunt (`ov:dossier` heeft als bereik `dossier:Dossier`). Een uitvoering moet
overeenkomen met de blauwdruk die ze uitvoert: de zaak met de procedure, een handeling met een
procedurestap. Het AP Dossier maakt dat onmogelijk:

10. **De procedure is een string.** Een Zaak heeft `dbo:procedure`, "de naam die verwijst naar de
    formele definitie van een verzameling stappen". Zonder resource zijn er geen stappen, volgorde
    of termijnen om de zaak mee te vergelijken. Voorstel: een objecteigenschap van Zaak naar
    `p-plan:Plan`, de korte vorm van `prov:qualifiedAssociation` met `prov:hadPlan`. Het bereik
    is P-PLAN en geen klasse van één domein: het AP Dossier is generiek, en een domein-AP hangt zijn
    eigen klassen eronder (`ov:Procedure ⊂ p-plan:Plan`, `ov:Procedurestap ⊂ p-plan:Step`, zoals in
    `ov-pplan-prov.ttl`). `prov:Plan` is te arm (geen stappen), `sosa:Procedure` te ruim (ook de
    werkwijze van een sensor); via pplan-sosa en sosa-prov volgen beide vanzelf.
11. **Een zaak is geen activiteit.** Zaak, Procedurestap en Project zijn een *Eenheid van werk*
    (`dbo:UnitOfWork`), die "verschilt van Activiteit" (in het AP `prov:Activity`) "in die zin dat
    het een duidelijk einde heeft en gemeten wordt". Ook de Activiteit van het AP heeft een
    verplichte einddatum, dus het criterium onderscheidt niets. En `prov:hadPlan`, de enige
    eigenschap in de kern die een uitvoering als geheel aan een plan bindt, vraagt een
    `prov:Activity`. Voorstel: een zaak is de uitvoering van een plan, een `prov:Activity`; de
    handelingen erin blijven activiteiten met `p-plan:correspondsToStep` naar hun stap.
    `sosa:ExecutionCollection` is geen alternatief: ze bevat enkel waarnemingen, actuaties en
    bemonsteringen, en een procedure op de collectie moet gelden voor elk lid.
12. **Twee betekenissen van "Procedurestap".** In het AP Omgevingsvergunning is het "een
    voorgeschreven handeling binnen een Procedure" (de blauwdruk). In het AP Dossier is het "het
    geheel aan werk gedaan binnen een […] onderdeel van een procedure", met start- en einddatum (de
    uitvoering), zonder link naar de voorgeschreven stap. Voorstel: in het AP Dossier een
    Activiteit met `p-plan:correspondsToStep` naar de stap (voor een stap met substappen: een
    activiteit die het deelplan volgt, zoals `exec:ontvankelijkheid-1`), of ten minste een ander
    label en die link. Het AP Omgevingsvergunning neemt dan de alignering over en hangt
    `ov:procedure` en `ov:procedurestap` onder de eigenschappen van het AP Dossier.
