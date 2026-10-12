# The discussion document

Every data example has a discussion document that answers nine questions in order, one level-2
heading per question: `## <number>. <title>`. The file name and the language of the titles come
from the project profile. In Dutch-language OSLO projects the file is `bespreking.md` and the
titles are:

| # | English | Dutch (OSLO) |
|---|---|---|
| 1 | What does this example represent? | Wat stelt dit voorbeeld voor? |
| 2 | Colour legend | Kleurlegenda |
| 3 | Infrastructure (blue nodes) | Infrastructuur (blauwe nodes) |
| 4 | Observation/actuation structure (pink nodes) | Observatie/Actuatie-structuur (roze nodes) |
| 5 | Procedure and Property | Procedure en Property |
| 6 | Modelling choices explained | Modelleer-keuzes toegelicht |
| 7 | Time modelling | Tijdsmodellering |
| 8 | Prefixes and IRI structure | Prefixen en IRI-structuur |
| 9 | Inverse relations | Inverse relaties |

## 1. What does this example represent?

The domain in two to four sentences: which real system, dataset or process is modelled. Give a
concrete IRI of the data source where there is one.

## 2. Colour legend

A table: colour (hex) → SOSA class → meaning in the domain. At least:

| Colour | SOSA concept | Domain meaning |
|---|---|---|
| Blue (#60c4e4) | Platform / System / Sensor | infrastructure |
| Pink (#e54b89) | Observation / Actuation / Activity | observation or actuation |
| Orange (#f8b622) | Result / time:Instant | values and instants |

For a three-layer model also: Purple (#7f59ae), `p-plan:Plan` / `p-plan:Step`, planning level.

## 3. Infrastructure (blue nodes)

Per blue node: which SOSA class and why. Explain double typings (e.g. `sosa:Platform` and
`sosa:FeatureOfInterest`) and triple typings (e.g. a measuring point that is also a
`sosa:SpatialSample`). Describe the `sosa:hosts` / `sosa:hasSubSystem` hierarchies.

## 4. Observation/actuation structure (pink nodes)

A table per `sosa:Observation` or `sosa:Actuation`:

| IRI | observedProperty / actsOnProperty | usedProcedure | hasResult | hasFeatureOfInterest |
|---|---|---|---|---|

When a `sosa:ObservationCollection` groups the observations, explain which shared metadata sits on
the collection and why.

## 5. Procedure and Property

Per procedure (`sosa:ObservingProcedure`, `sosa:ActuatingProcedure`, …): which sensor implements it
(`sosa:implements`) and which observations use it (`sosa:usedProcedure`). Per `sosa:Property`: its
physical or domain meaning.

## 6. Modelling choices explained

One subsection per non-trivial design decision, with a fixed structure:

> **Why [chosen approach]?**
> Rejected alternative: … Chosen approach: … Rationale: … (with a reference to the SOSA / PROV-O
> specification or a rule number)

Cover the decision points of [`ssn-sosa.md`](ssn-sosa.md#decision-points) that apply. Also state
here: register units and their QUDT mapping (R3), `[warning]` messages deliberately left (e.g. no
geometry because the source has no location), and any alternative mapping, with a link to it.

## 7. Time modelling

Which time pattern (see R12) and why. Distinguish `sosa:phenomenonTime`, `sosa:resultTime` and,
for predictions, a future result. State the time zone assumption if the source gave none.

## 8. Prefixes and IRI structure

A table of all prefixes:

| Prefix | Base IRI | Temporary or persistent |
|---|---|---|

Persistent IRIs for production data, `https://example.org/` sub-paths for illustrative instances,
no blank nodes for resources referred to from outside (R10).

## 9. Inverse relations

Which inverse pairs are included and why (query efficiency), e.g. `sosa:hosts` ↔
`sosa:isHostedBy`, `sosa:hasFeatureOfInterest` ↔ `sosa:isFeatureOfInterestOf`.

## Placeholders

When an answer is not known yet, write a concrete question, never a generic placeholder:

```markdown
<!-- TODO: is the sampling well the same object as the discharge point in RIE-IEPR? -->
```
