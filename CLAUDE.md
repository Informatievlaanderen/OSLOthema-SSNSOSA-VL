# CLAUDE.md — OSLOthema-SSNSOSA-VL

## §1 — Projectidentiteit

Dit is een Vlaamse overheidsproject (Informatie Vlaanderen / OSLO) dat normatieve richtlijnen
ontwikkelt voor de toepassing van de W3C SSN/SOSA 2023-standaard op Vlaamse overheidsdomeinen.
Het project combineert SSN/SOSA met PROV-O, P-PLAN, QUDT en OWL-TIME en documenteert concrete
datavoorbeelden per domein. De output dient als referentie voor toepassingsprofiel-ontwikkelaars.

**Modelleerregels, patronen en werkwijzen** staan in de kit
[`milieuinfo/oslo-ld-kit`](https://github.com/milieuinfo/oslo-ld-kit) (Engelstalig), als
git-subtree in `oslo-ld-kit/`:
de gids (`guide/`, regels R1–R15, onderaan geïmporteerd) en de skills, gekopieerd naar
`.claude/skills/` (`new-example`, `revise-mapping`, `alternative-mapping`, `map-source-data`,
`decision-document`, `design-ontology`, `align-ontologies`). Dit bestand bevat enkel wat eigen is
aan dit project. Een nieuwe algemene regel of les hoort in de kit, niet hier. Wijzig nooit
`oslo-ld-kit/` of de gekopieerde skills in dit project, maar de repo van de kit (§6).

---

## §2 — Projectprofiel

| Instelling | Waarde |
|---|---|
| Voorbeelden | `src/main/input/<domein>/` |
| Ontologieën | `src/main/resources/` (ook geladen door `ld-vocab` en de pipeline) |
| Documenttaal | Nederlands (README, bespreking, opdracht, beslisdocumenten) |
| Bestandsnamen | bespreking `bespreking.md`, oefening `opdracht.md`, herziening `<naam>_herzien.ttl`, vergelijking `<naam>_vergelijking.mmd`, alternatief `alternatief/`, sectie *Verbeterpunten* in de README |
| Sectietitels bespreking | de Nederlandse titels uit `guide/discussion-document.md` (`## 1. Wat stelt dit voorbeeld voor?` …) |
| Labels in diagrammen | `PROCEDURE`, `INFRASTRUCTUUR`, `WAARNEMING` (plat); `PLANNING`, `DEPLOYMENT`, `EXECUTION`, `DERIVATION` |
| Tijdzone (R12) | `Europe/Brussels`: `+01:00` in de winter, `+02:00` tijdens de zomertijd |
| Eenhedenregister (R3) | CSOR, prefix `csor-eenheid:` (`<https://data.omgeving.vlaanderen.be/id/concept/csor/eenheid/>`), geladen uit `src/main/resources/be/vlaanderen/omgeving/data/id/conceptscheme/csor/eenheid/eenheid.ttl` |
| Extra prefixen | per domein; gedeelde infrastructuur met een eigen prefix (bv. `htg:` voor het Herman Teirlinck-gebouw) |
| Validatie | `mcp__ld-vocab__validate_file` (§5); de Scala-pipeline enkel voor output |
| Bronbestanden | in `source/`, Turtle als `.trig` (§4) |

---

## §3 — Repository-structuur

| Pad | Rol |
|---|---|
| `src/main/input/<domein>/` | Één directory per datavoorbeeld |
| `src/main/resources/` | OWL-ontologieën (SSN/SOSA 2023, PROV-O, P-PLAN, QUDT, TIME, SAREF met SAREF4SYST, …), en de uitlijningsmodules `sosa-prov` en `sosa-saref` van SSN/SOSA 2023 in `org/w3/www/ns/sosa/alignments/` (uit `w3c/sdw-sosa-ssn`) |
| `src/main/resources/generated-shapes.ttl` | Auto-gegenereerde SHACL-shapes — **nooit manueel bewerken** |
| `src/main/cc/prefix/prefix.cc.ttl` | Prefixregister van prefix.cc voor `validate_file` (`getPrefixes.sh` om te vernieuwen) |
| `src/main/resources/be/vlaanderen/ssnsosa/data/id/jsonld/frame.json` | JSON-LD framing-template |
| `src/main/resources/be/vlaanderen/ssnsosa/data/id/rule/domain-range-subproperty.rules` | Jena-inferentieregels |
| `src/main/scala/be/vlaanderen/ssnsosa/` | Scala-evaluatiepipeline |
| `src/main/output/` | Gegenereerde output (Turtle na inferentie, JSON-LD) |
| `oslo-ld-kit/` | Git-subtree van [`milieuinfo/oslo-ld-kit`](https://github.com/milieuinfo/oslo-ld-kit): gids, skills, SHACL-regels — niet hier wijzigen |
| `.claude/skills/` | Skills uit de kit, gekopieerd door `oslo-ld-kit/sync.py` (versie in `.oslo-ld-kit.json`) — niet hier wijzigen |
| `.mcp.json` | MCP-server `ld-vocab` ([`milieuinfo/ld-mcp`](https://github.com/milieuinfo/ld-mcp)) met de regels uit de kit; jar in `tools/` (§6) |
| `.claude/commands/nieuw-voorbeeld.md` | `/nieuw-voorbeeld`: start de skill `new-example` met dit profiel |
| `kennisinventaris.md` | Inventaris van de kennis in dit project en waar ze naartoe ging |

Bestaande datavoorbeelden:
- `grondwaterpeilmetingen/` — DOV grondwaterfiltermetingen (plat model)
- `paleo/` — paleoklimaatdata met afgeleide observaties en niet-kalender TRS
- `Nigella-Lawson-Brownies/` — procesmodellering met drielaags architectuur
- `EnergieManagementSystem/` — vier HVAC/energie-scenario's met herzieningsworkflow
- `erosiepoel/` — manuele veldmeting met ObservationCollection; incl. opdracht.md
- `temperatuur-raam/` — drielaags met sensor+actuator, vereenvoudigd (2 metingen); incl. opdracht.md
- `elektrisch-raam/` — drielaags met meerdere sensoren, afgeleide observatie en actuatie
- `verkeersmetingen/` — plat model met SpatialSample, time:Interval en afgeleide dagsom; incl. opdracht.md
- `geluidsmeetnet/` — geluidsevents en dagindicatoren rond Brussels Airport (Aerovision-CSV's, gescript);
  alle campagnes als `.trig`, één campagne als `.ttl`-validatiesubset; `alternatief/` modelleert het
  geluidsevent als emissie (alternatieve mapping naast het hoofdmodel)
- `r-factor/` — neerslagerosiviteit (RUSLE R-factor) van 53 KMI/VMM-stations, jaar-, maand- en
  15-daagse waarden; grote dataset als `.trig` met `.ttl`-subset, skolem-IRI's (R-script)
- `waterkwaliteit/` — VMM-meetresultaten (concentraties, vrachten, debieten) met CSOR-codelijsten,
  sampling-keten, rapportagegrens en een applicatieprofiel uit `waterkwaliteit.ttl`; gescript, met
  `beslisdocument.md` als voorstel voor het OSLO-traject
- `overstort/` — herziening van Aquafins LDES-mapping van overstortsensoren en -events (issue #1):
  bron in `source/`, `overstort_herzien.ttl` met meetpunt als Platform+FOI, `sosa:Deployment` en
  event als `phenomenonTime`-interval; `alternatief/` leest een overstorting als emissie (`wk:Emissie`,
  resultaat van een `sosa:Actuation`)
- `PGD_geschiktheidskaart/` — geschiktheidskaart voor peilgestuurde drainage (OP-PEIL), afgeleid uit
  andere kaartlagen: drielaags met twee QGIS-modellen als plan en sensor, één rastercel als
  `sosa:SpatialSample`, drie factorscores en een afgeleide kansrijkheid (SKOS-codelijsten)

---

## §4 — Bestandsset per voorbeeld

```
<naam>.ttl of .trig          primaire RDF-data
<naam>.mmd                   Mermaid-diagram (guide/diagrams.md)
README.md                    intent, bronbestand, transformatiepipeline
bespreking.md                negen secties (guide/discussion-document.md)
opdracht.md                  optioneel: trainingsexercitie (guide/exercise.md)
bash/ of scripts/            optioneel: transformatiescripts (xsltproc, riot, SPARQL, Python, R)
source/                      optioneel: ontvangen brondata vóór revisie
<naam>_herzien.ttl           indien brondata modelleringfouten bevatte (skill revise-mapping)
<naam>_vergelijking.mmd      vergelijkingsdiagram bij een significante architectuurwijziging
alternatief/                 optioneel: tweede verdedigbare lezing (skill alternative-mapping)
```

**`.ttl` en `.trig`:** de pipeline verwerkt alle `.ttl`-bestanden recursief in `src/main/input/`,
ook in `source/`, en slaat `.trig` over. Daarom:
- een ontvangen bronbestand blijft in zijn oorspronkelijke formaat; Turtle als `source/<naam>.trig`
  (geldige TriG, dus `riot` en `validate_file` lezen het nog, maar de bekende fouten geven geen
  `[VOCAB ERROR]` in de pipeline);
- een grote dataset staat volledig in `<naam>.trig`, met een kleine `<naam>.ttl` als
  validatiesubset (zie `r-factor/`, `geluidsmeetnet/`, `waterkwaliteit/`);
- grote registers (CSOR-parameters, NACE-BEL) staan niet als `.ttl` onder `src/main/input/`.

---

## §5 — Valideren

**Eén bestand:** `mcp__ld-vocab__validate_file` (server in `.mcp.json`, ld-mcp 0.4.0 of later). Wat
de meldingen betekenen en wat je ermee doet, staat in `guide/linked-data.md` (Validation) en in de
README van ld-mcp. De server laadt `src/main/resources/`, genereert de SHACL-shapes zelf uit de
ontologie (een profiellezing van de OWL-restricties, niet meer hetzelfde als `generated-shapes.ttl`
van de pipeline, zie de verschillen hieronder), gebruikt de regels uit
`oslo-ld-kit/rules/ssn-sosa-rules.ttl` en het prefixregister, en leest gewijzigde bestanden
automatisch opnieuw in. Na een nieuwe jar: `/mcp` → `ld-vocab` → Reconnect.

Het rapport:

| Marker | Betekenis |
|---|---|
| `[VOCAB] n error(s), m suspect, k hint(s)` | termen, rollen, datatypes, verouderde termen en gemunte resources; elke regel begint met `[error]`, `[suspect]` of `[hint]` |
| `[INFERENCE]` | aantal triples afgeleid met de regels uit `domain-range-subproperty.rules` |
| `[DISJOINTNESS]` | klassedisjunctie na inferentie, met de klassehiërarchie; geen volledige OWL-consistentie |
| `[SHACL] … (a of n shapes applied to k focus node(s); graph: …)` | SHACL op de data plus de klassehiërarchie en de types van verwezen termen (geen afgeleide triples); de dekking zegt hoeveel shapes de data raakten |

Alle `[error]`-meldingen (onder `[VOCAB]`, `[DISJOINTNESS]` en de SHACL-violations) worden opgelost
vóór een commit; `[suspect]`-meldingen en SHACL-warnings worden nagekeken, en als ze bewust blijven
staan, vermeld in de bespreking (§6).

**Alle voorbeelden in één keer**, zonder MCP-client (exitcode 0 zonder fouten, 1 bij fouten, 2 bij
een configuratie- of parsefout):

```bash
java -jar tools/ld-mcp-vocab.jar validate --ontologies src/main/resources \
    --rules src/main/resources/be/vlaanderen/ssnsosa/data/id/rule/domain-range-subproperty.rules \
    --generate-shapes --shapes oslo-ld-kit/rules/ssn-sosa-rules.ttl \
    --prefix-registry src/main/cc/prefix/prefix.cc.ttl --extensions ttl src/main/input
```

`--extensions ttl` volgt de pipeline: zonder die optie valideert het ook de `.jsonld`-bestanden,
waaronder de volledige `r-factor/rfactor.jsonld` (34 MB).

**Volledige pipeline**, enkel wanneer de output in `src/main/output/` of een bijgewerkt
`generated-shapes.ttl` nodig is:

```bash
mvn compile exec:java
```

1. **OntologySorter** laadt alle `.ttl`-bestanden uit `src/main/resources/` in `completeOntology`
   (alles), `structuralSubset` (subClassOf, subPropertyOf, inverseOf, domain, range) en
   `disjointSubset` (disjointWith).
2. **OwlToShaclGenerator** schrijft `src/main/resources/generated-shapes.ttl`.
3. Per `.ttl`-bestand in `src/main/input/`: vocabulaire-check (predicaten en `rdf:type`-doelen;
   `WARN [VOCAB ERROR]`), regelinferentie, OWL-validatie met OWLMiniReasoner
   (`WARN [MODEL INVALID]`), SHACL tegen `generated-shapes.ttl`, JSON-LD-conversie met `frame.json`.

Alle `[VOCAB ERROR]`-waarschuwingen van de pipeline moeten opgelost worden vóór een commit.

Verschillen met `validate_file`, die gelden zolang de pipeline bestaat:
- de pipeline controleert geen objecten (bv. eenheden), gemunte resources, datatypes, rollen of
  verouderde termen, en gebruikt de regels uit de kit niet. Dat de pipeline geen eenheden
  controleert, is een bewuste keuze: dat doet `validate_file`;
- de pipeline zet `owl:AllDisjointClasses` en `owl:disjointUnionOf` niet om naar disjunctieparen,
  en ziet de klassehiërarchie niet zonder regels;
- de pipeline valideert SHACL op de letterlijke data; `validate_file` ziet ook de klassehiërarchie
  en de types van verwezen termen;
- `generated-shapes.ttl` (`OwlToShaclGenerator`) vertaalt `owl:someValuesFrom C` als `sh:class C`
  op alle waarden plus `sh:minCount 1`; ld-mcp als "minstens één waarde is een C", en vertaalt ook
  gekwalificeerde cardinaliteiten, `owl:hasValue` en restricties in `owl:intersectionOf`. De
  shapes van ld-mcp zelf schrijven: `java -jar tools/ld-mcp-vocab.jar generate-shapes
  --ontologies src/main/resources --prefix-registry src/main/cc/prefix/prefix.cc.ttl --out <bestand>`.

---

## §6 — Opzet voor een nieuwe gebruiker

1. **Java 21 of later** installeren, bv. [Eclipse Temurin](https://adoptium.net) (installatieprogramma
   voor Windows, macOS en Linux); controleren met `java -version`.
2. **Het project** ophalen: `git clone <url van dit project>`. De kit en de skills zitten erin.
3. **De validatieserver** downloaden:
   [`ld-mcp-vocab.jar`](https://github.com/milieuinfo/ld-mcp/releases/latest/download/ld-mcp-vocab.jar)
   en opslaan als `tools/ld-mcp-vocab.jar` in het project (map aanmaken; `tools/` staat in
   `.gitignore`). Claude kan dat ook doen:
   `curl -L --create-dirs -o tools/ld-mcp-vocab.jar https://github.com/milieuinfo/ld-mcp/releases/latest/download/ld-mcp-vocab.jar`.
   Een nieuwere versie: opnieuw downloaden, dan `/mcp` → `ld-vocab` → Reconnect.

Wie ld-mcp zelf ontwikkelt (clone van [`milieuinfo/ld-mcp`](https://github.com/milieuinfo/ld-mcp),
`mvn package`), zet `LD_MCP_JAR` op het volledige pad van `ld-mcp-vocab/target/ld-mcp-vocab.jar`,
of legt in `tools/` een symbolische link naar die jar.

- Bij het openen van het project vraagt Claude Code om de imports hieronder te laden.
- Bijwerken: `git pull`. `ld-vocab` leest gewijzigde regels en ontologieën zelf opnieuw in.
- Installeer de plugin `oslo-ld` niet in dit project: de skills staan er al, en zouden dan twee
  keer bestaan, mogelijk in verschillende versies.

**De kit bijwerken** (enkel wie het project onderhoudt; werkboom zonder openstaande wijzigingen):

```bash
git subtree pull --prefix oslo-ld-kit https://github.com/milieuinfo/oslo-ld-kit.git main --squash
python oslo-ld-kit/sync.py
git add .claude/skills && git commit -m "oslo-ld-kit <versie>"
```

Kijk de wijzigingen aan gids en regels na en valideer de voorbeelden opnieuw. Een wijziging aan de
kit zelf gebeurt in de repo van de kit (README van de kit, *Keeping it up to date*), nooit in
`oslo-ld-kit/` of `.claude/skills/` hier: die worden bij de volgende update overschreven.

---

## §7 — Gids

@oslo-ld-kit/guide/README.md
@oslo-ld-kit/guide/linked-data.md
@oslo-ld-kit/guide/ssn-sosa.md
@oslo-ld-kit/guide/patterns.md
@oslo-ld-kit/guide/discussion-document.md
@oslo-ld-kit/guide/diagrams.md
@oslo-ld-kit/guide/exercise.md
