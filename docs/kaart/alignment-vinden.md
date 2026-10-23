# Een alignment vinden en beoordelen

Vroeg of laat kan de kern een betekenis niet uitdrukken: de fabrikant van een toestel, de status
van een meetpunt, een bedrijfsactiviteit, een waterloop. Dan komt er een term uit een ander
vocabularium bij. Dit hoofdstuk beschrijft hoe je die kiest zonder de samenhang van de kaart te
breken: eerst zoeken naar wat er is, dan beoordelen, dan verantwoorden. De normatieve versie is
regel [R17](../regels/r17.md).

## 1. De volgorde van voorkeur

Gebruik een term van een later niveau enkel wanneer de vroegere niveaus de betekenis niet kunnen
uitdrukken:

1. de geladen kern: SOSA/SSN, PROV-O, QUDT, OWL-Time, GeoSPARQL, SKOS, DCTERMS, RDFS;
2. andere W3C- en OGC-modellen;
3. vocabularia en registers van overheden: OSLO (data.vlaanderen.be), de SEMIC Core Vocabularies,
   de registers van het domein (CSOR, …);
4. normen van andere instanties (ISO, ETSI);
5. al de rest.

**Linked Open Vocabularies (LOV) is om te verkennen, niet om te kiezen.** LOV toont kandidaten en
hoe anderen ze gebruiken, maar de rangschikking is tekstueel: een zoekopdracht naar `Sample` zet
`sp:Sample` (SPIN, een SPARQL-vocabularium) naast `sosa:Sample`. Een treffer is een kandidaat,
nooit een aanbeveling.

**schema.org enkel als laatste uitweg.** schema.org dient voor webmarkup voor zoekmachines, niet
voor datamodellen: de term-IRI's geven HTML terug, `http://schema.org/` en `https://schema.org/`
worden door elkaar gebruikt, en er is geen uitlijning met PROV-O of SOSA (behalve een voorlopige
module van SSN/SOSA 2023).

## 2. Een alignment zoeken

Een alignment is een uitspraak over twee vocabularia, en kan door een van beide gepubliceerd zijn,
of door geen van beide. De uitlijning van SOSA met SAREF staat in SSN/SOSA, niet in SAREF, en LOV
kent ze niet ([SOSA en SAREF](sosa-saref.md)). **Afwezigheid in de kandidaat is dus geen
afwezigheid.** Zoek in deze volgorde:

1. het **register van gekende alignments** van de kit,
   [`registers/alignments.ttl`](https://github.com/milieuinfo/oslo-ld-kit/blob/main/registers/alignments.ttl);
2. de **kandidaat zelf**: verwijst hij naar de kern?
3. de **specificatie en repository van elk kernvocabularium** (voor SSN/SOSA 2023: hoofdstuk 7 en
   `ssn/rdf/ontology/alignments/` in `w3c/sdw-sosa-ssn`);
4. de **uitbreidingsmodules en documentatie** van de kandidaat;
5. een **code-zoekopdracht** naar bestanden die beide namespaces gebruiken.

Schrijf in de bespreking waar je zocht en wat je vond. Dan is een ontbrekende alignment een
vastgestelde afwezigheid, geen vergetelheid. Voeg elke gevonden alignment toe aan het register,
zodat het volgende project ze niet opnieuw moet ontdekken.

### Het register van gekende alignments

| Module | Verbindt | Uitgever |
|---|---|---|
| `sosa-prov` | SOSA ↔ PROV-O | W3C (SSN/SOSA 2023) |
| `sosa-saref` | SOSA ↔ SAREF core, SAREF4SYST | W3C (SSN/SOSA 2023) |
| `sosa-oboe` | SOSA ↔ OBOE (ecologie) | W3C (SSN/SOSA 2023) |
| `sosa-dul`, `sosa-dolce`, `sosa-bfo`, `sosa-ido` | SOSA ↔ funderingsontologieën (DUL, DOLCE, BFO en CCO, ISO 23726-3) | W3C (SSN/SOSA 2023) |
| `sosa-sdo` | SOSA ↔ schema.org (voorlopig) | W3C (SSN/SOSA 2023) |
| `pplan-sosa` | P-PLAN ↔ SOSA ↔ PROV-O | dit project |

De SensorThings API van OGC heeft een mappingtabel, maar geen RDF-module, en staat er daarom niet
in.

## 3. Een kandidaat beoordelen

Vijftien criteria, in vier groepen. Ze zijn geen puntentelling: meestal beslissen er twee of drie.

| # | Criterium | Wat je nagaat |
|---|---|---|
| | ***Technisch*** | |
| 1 | Als RDF opvraagbaar | de namespace en een term geven RDF terug (Turtle, RDF/XML, JSON-LD); een HTML-pagina of enkel een JSON-LD-`@context` volstaat niet |
| 2 | Persistente namespace | w3id, purl of het domein van een standaardisatie-instelling; `http` en `https` consequent |
| 3 | Versies | `owl:versionIRI` of `owl:versionInfo`, een wijzigingslog, ingetrokken termen `owl:deprecated` |
| 4 | Licentie | expliciet en open |
| 5 | Formeel degelijk | termen getypeerd, met labels en definities; domein en bereik zinvol waar ze er zijn; geen SKOS tussen klassen; geen axioma's over termen van andere vocabularia |
| 6 | Consistent met de kern | na het laden geven de bestaande voorbeelden geen disjunctiefouten |
| | ***Semantisch*** | |
| 7 | Past bij het domein | beoordeeld op de *definitie*, niet op het label |
| 8 | Uitgelijnd met de kern | subklasse of subproperty van SOSA of PROV, of minstens niets wat ermee botst (zoek zoals in §2) |
| 9 | Verbintenis | wat domein, bereik en afleidingen van die ene term aan de data toevoegen, samen gelezen met de alignment |
| 10 | Granulariteit | niet gebonden aan één project of toepassing |
| | ***Beheer*** | |
| 11 | Uitgever | een standaardisatie-instelling, een overheid of een actieve gemeenschap, eerder dan een afgerond onderzoeksproject |
| 12 | Onderhoud | recente versie, een gebruikte issuetracker |
| 13 | Gebruik | gebruikt in de doelgemeenschap (OSLO, SEMIC, INSPIRE, datasets) |
| 14 | Labels in het Nederlands | aanwezig, of toe te voegen |
| | ***Verhouding*** | |
| 15 | Is het het waard? | één term uit een groot vocabularium moet de verbintenissen waard zijn die hij meebrengt; in twijfel: geen vocabularium toevoegen |

!!! valkuil "Een gedocumenteerde IRI is nog geen vocabularium"
    Sommige termensets publiceren per term een IRI met een HTML-pagina of een JSON-LD-context,
    maar geen enkele RDF-beschrijving. Smart Data Models is het voorbeeld:
    `https://smartdatamodels.org/dataModel.Environment/deviceName` bestaat, maar geeft ook met
    `Accept: text/turtle` HTML terug, en er is geen OWL-bestand. Na JSON-LD-expansie is het wel
    een RDF-predicaat, maar een zonder definitie: niet te controleren (criterium 1).

## 4. Een voorbeeld: de overstortmeter

De mapping van Aquafins overstortsensoren gebruikte termen van Smart Data Models voor de naam, het
model en de status van een toestel. De herziening ([casus overstort](../casussen/overstort.md))
volgde de stappen hierboven:

| Betekenis | Bron | Kandidaten | Beslissend | Keuze |
|---|---|---|---|---|
| naam van het toestel | `environment:deviceName`, `dct:description` | — | de kern volstaat (niveau 1) | `rdfs:label` |
| fabrikant | `environment:deviceModel "Ijinus"` (eigenlijk het merk) | `saref:hasManufacturer`, `schema:manufacturer`, `am:manufacturer` (OSLC), `era:manufacturer`, `dbpedia-owl:manufacturer`, geen fabrikant opnemen | ETSI-norm met versies (3, 11), uitgelijnd met SOSA via `sosa-saref` (8), het domein voegt niets nieuws toe (9); schema.org geeft geen RDF (1), OSLC heeft een formeel fout bereik (5), ERA is spoorwegspecifiek (10) | `saref:hasManufacturer` |
| beheerstatus | `environment:deviceStatus "ACTIEF"` | `adms:status`, `saref:State`, een eigen eigenschap, de status als waarneming | ADMS: W3C/SEMIC (11), RDF (1), breed hergebruikt in DCAT-AP en OSLO (13); `saref:State` is de operationele toestand, niet de beheerstatus (7); een eigen vocabularium voor één eigenschap is het niet waard (15) | `adms:status` naar een SKOS-begrip |
| eigenaar | `sdm:owner "AQUAFIN"` | — | de definitie ("de dienst die verantwoordelijk is voor het beheer van de account") past niet (7) | niet overgenomen; vraag aan de bron |

Beide keuzes hebben status *voorstel*: kiest het OSLO-traject een toestelmodel uit OSLO of SEMIC
(voorkeursniveau 3), dan vervangt dat beide termen (ETSI is niveau 4).

## 5. Verantwoorden

Een vocabularium wordt pas gebruikt nadat het geladen is (met bron en versie) en nadat alle
voorbeelden nog consistent zijn. In de bespreking krijgt elke term buiten de kern een paragraaf
**Waarom dit vocabularium?**:

```markdown
> **Waarom `saref:hasManufacturer`?**
> Kandidaten: geladen ontologieën en LOV (`manufacturer`: 79 treffers).
> Beslissend: SAREF is een ETSI-norm met versies (3, 11) en een SOSA-alignment (8); het domein
> `saref:FeatureOfInterest` voegt niets nieuws toe, want `sosa-saref` maakt elk systeem al
> een `saref:FeatureOfInterest` (9). Verworpen: `schema:manufacturer` (geen RDF bij content
> negotiation, 1), `am:manufacturer` (formeel fout bereik, 5), `era:manufacturer` (spoorwegen, 10).
> Gezocht naar alignments: register van de kit, SAREF, SSN/SOSA hoofdstuk 7.
```

Zo wordt zichtbaar dat de term gekozen werd, niet geplukt.

## Verder

- [R17 Vocabularia kiezen](../regels/r17.md): de normatieve tekst.
- [Ontologieën aligneren](../werkwijze/aligneren.md): een volledige analyse van twee modellen
  (zoals [Register en I-ADOPT](register-iadopt.md)).
