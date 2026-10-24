# SSN/SOSA 2023 modelling rules

Rules for observation, actuation and sampling data with W3C SSN/SOSA 2023, PROV-O, P-PLAN, QUDT
and OWL-Time. General linked data rules (IRIs, R10; SKOS, R15; choosing vocabularies, R17; concept or class, R18; validation) are in
[`linked-data.md`](linked-data.md). Rules that can be checked automatically are also shapes in
`../rules/ssn-sosa-rules.ttl` (R2, R3, R5, R7, R9, R11, R12, R13, R15, R16).

## Prefixes

```turtle
@prefix sosa:   <http://www.w3.org/ns/sosa/> .
@prefix ssn:    <http://www.w3.org/ns/ssn/> .
@prefix prov:   <http://www.w3.org/ns/prov#> .
@prefix p-plan: <http://purl.org/net/p-plan#> .
@prefix time:   <http://www.w3.org/2006/time#> .
@prefix qudt:   <http://qudt.org/schema/qudt/> .
@prefix unit:   <http://qudt.org/vocab/unit/> .
@prefix geo:    <http://www.opengis.net/ont/geosparql#> .
@prefix xsd:    <http://www.w3.org/2001/XMLSchema#> .
@prefix rdf:    <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs:   <http://www.w3.org/2000/01/rdf-schema#> .
```

Declare only those used; `geo:` when the example uses `sosa:SpatialSample` or `geo:hasGeometry`
(R11). `qudt:` is for schema terms (`qudt:QuantityValue`, `qudt:hasUnit`, `qudt:numericValue`),
`unit:` for units (`unit:M` metre, `unit:PPM`, `unit:YR`, `unit:CCY_EUR` euro). QUDT unit names are
not predictable (the metre is `unit:M`, not `unit:Meter`): find them with `search_terms`.

**Flat models** use one `ex:` prefix. **Three-layer models** use one prefix per layer instead:

```turtle
@prefix plan:   <https://example.org/<domain>/plan/> .
@prefix step:   <https://example.org/<domain>/step/> .
@prefix var:    <https://example.org/<domain>/var/> .
@prefix exec:   <https://example.org/<domain>/exec/> .
@prefix ent:    <https://example.org/<domain>/ent/> .
@prefix inst:   <https://example.org/<domain>/inst/> .
@prefix prop:   <https://example.org/<domain>/prop/> .
```

Shared infrastructure that recurs across examples gets one extra prefix of its own (declared in the
project profile).

## R1 — Choosing the infrastructure class

- Physical location that hosts equipment → `sosa:Platform`
- Component of a larger system → `sosa:System`
- Agent (person, software, device) that makes observations → `sosa:Sensor`
- Agent that changes the world → `sosa:Actuator`
- Thing (physical or conceptual) being studied → `sosa:FeatureOfInterest`
- Proxy sample of a feature of interest → `sosa:Sample` (also a `sosa:FeatureOfInterest`)
- Spatial sub-sample of a larger area → `sosa:SpatialSample` (subclass of `sosa:Sample`): use it when
  the measuring point is a point or area sample of a larger zone (route, region, water body); see
  R11.

## R2 — Required properties of an observation

Every `sosa:Observation` has `sosa:observedProperty`, `sosa:hasFeatureOfInterest`, and at least one
of `sosa:hasResult` or `sosa:hasSimpleResult`. `sosa:usedProcedure` and `sosa:madeBySensor` are
strongly recommended. Members of a `sosa:ObservationCollection` inherit what the collection states
(SOSA 2023), so `observedProperty`, the feature of interest, the procedure and the sensor may be on
the collection instead.

## R3 — Result with a unit

For a numeric result with a physical unit, the object of `sosa:hasResult` is a `qudt:QuantityValue`
with `qudt:numericValue` and `qudt:hasUnit`: a blank node in small examples, an IRI when the result
must be referable from outside or in large datasets (a skolem IRI, R10).

Do not type the result `sosa:Result`: SSN/SOSA 2023 declares it `owl:deprecated`
(w3c/sdw-sosa-ssn #113, #163), and it adds nothing. `sosa:hasResult` is a subproperty of
`prov:generated` (range `prov:Entity`), so any result is a `prov:Entity` already, and so not an
activity, an instantaneous event or a literal (R16). A profile that needs a class of its own for its
results makes it a subclass of `qudt:QuantityValue`; the data types both (as for other reused classes,
see *Ontologies and application profiles* in [`linked-data.md`](linked-data.md)).

The numeric value is always in `qudt:numericValue`, never in `qudt:value`. `qudt:value` exists (so
the vocabulary check does not flag it), but it is not the QUDT pattern for a numeric measurement.

**Source of the unit** (`qudt:hasUnit`), one choice per example:
- **QUDT** (default): `unit:M`, `unit:MilliGM-PER-L`, …
- **A domain register** (e.g. CSOR in the Flemish environment domain), when QUDT cannot express the
  unit (substance-qualified such as "mg P/L", `/100mL`, `meq/L`) or when the domain has a register
  of its own (the project profile names it):
  - find the unit with `search_terms`; `lookup_term` shows the register's own
    `skos:exactMatch`/`broadMatch` to QUDT; mention that mapping in the discussion (§6);
  - do **not** add SKOS mappings to the data: they are statements about the register's concepts,
    in its namespace. A missing mapping is a point for the register's maintainers;
  - every value of `qudt:hasUnit` is a `qudt:Unit` (its range, and `allValuesFrom` on
    `qudt:Quantifiable`). Inference makes a register unit one, but SHACL sees only the asserted
    graph (*Validation* in [`linked-data.md`](linked-data.md)): when the data describes the unit
    (types it with the register's class), type it `qudt:Unit` as well, e.g.
    `csor-eenheid:… a csor:Eenheid , qudt:Unit`. A unit the data only refers to needs no typing;
  - QUDT requires a `qudt:hasQuantityKind` and a `qudt:hasDimensionVector` on every `qudt:Unit`,
    which a register unit usually lacks. Do not add them to the data (they belong in the register);
    relax them in the profile's ontology with `owl:minCardinality 0` on `qudt:Unit` for both
    properties, which makes them not required in the generated SHACL (see *Ontologies and
    application profiles* in [`linked-data.md`](linked-data.md)).

A value below the reporting limit ("< 0.0125 µg/L") has no `qudt:numericValue`: give the interval
with `qudt:lowerBound` and `qudt:upperBound` (see [`patterns.md`](patterns.md)).

## R4 — When to use the three-layer architecture

Use Planning / Deployment / Execution when (a) the process has several steps, (b) the same procedure
can run on several platforms or data, or (c) traceability to an abstract plan is required. For
single-sensor observation scenarios the flat model with a `sosa:ObservationCollection` suffices.

## R5 — `sosa:hasInput` versus `prov:used`

`sosa:hasInput` belongs **only** on `sosa:Procedure` nodes, to describe abstract input types. At
execution level, use `prov:used` on the activity, observation or actuation to refer to concrete
`prov:Entity` instances. Violation: putting `sosa:hasInput` with a concrete value directly on an
observation.

## R6 — Machine learning model as an artefact

A machine learning model is a `prov:Entity` (optionally also `it6:MachineLearningModel`), generated
by a training `prov:Activity`. The software component that uses the model to make predictions is
the `sosa:Sensor`. Each prediction (an observation or actuation) refers to the model with
`prov:used`: the model is not a value for an input of the procedure, so not `sosa:hasInputValue`
(R5, R13). SSN/SOSA 2023 has no property that links a sensor to a model it uses (there is no
`sosa:uses`).

```turtle
model:my_ml_model a it6:MachineLearningModel, prov:Entity ;
  prov:wasGeneratedBy [ a prov:Activity ; prov:used ent:training_data ] .

sensor:predictor a sosa:Sensor ;
  sosa:implements step:predict .

exec:prediction_001 a sosa:Observation ;
  sosa:madeBySensor sensor:predictor ;
  sosa:usedProcedure step:predict ;
  prov:used model:my_ml_model ;
  sosa:hasInputValue ent:historical_data ;
  sosa:hasResult ent:predicted_time .
```

## R7 — Derived observations

When an observation's result depends on earlier observations, point `sosa:hasInputValue` at the
**results** of the source observations (the values), and `sosa:relatedObservation` at the source
observations themselves. Never `sosa:hasInputValue` to an observation: SOSA 2023 defines it as
"assigns a value to an input defined by the Procedure", and an observation is an activity
(`sosa:Execution ⊂ prov:Activity`), not a value. The PROV alignment of SSN/SOSA 2023 (`sosa-prov`)
makes this checkable: `sosa:hasInputValue` is a subproperty of `prov:used` (range `prov:Entity`),
the counterpart of `sosa:hasResult ⊂ prov:generated` (w3c/sdw-sosa-ssn#556), so an observation as
input value is a `[DISJOINTNESS]` violation (R16). In a three-layer model, prefer concrete entities
with `p-plan:correspondsToVariable` at execution level.

## R8 — Sampling chains

`sosa:isSampleOf` chains upwards: `IceBubble isSampleOf IceCore isSampleOf EarthCrust`. An
observation on a sample may state `sosa:hasUltimateFeatureOfInterest` on the root feature of
interest for efficient query paths.

## R9 — Non-calendar temporal reference systems

Use `time:inTimePosition` with `time:hasTRS` pointing to a named `time:TRS` instance (e.g. `ex:BP`
for Before Present). Describe the TRS with `skos:prefLabel` and `skos:definition`.

## R11 — SpatialSample and GeoSPARQL

When a measuring point is a spatial sub-sample of a larger object of study (route, water body,
municipality):
- type it `sosa:Platform`, `sosa:FeatureOfInterest` and `sosa:SpatialSample`;
- link it to the ultimate feature of interest with `sosa:isSampleOf` (required: a sample is always
  a sample *of* something);
- give it a geometry, `geo:hasGeometry [ geo:asWKT "Point(lon lat)"^^geo:wktLiteral ]` (strongly
  recommended; when the source gives no location, say so in the discussion rather than inventing
  one);
- put `sosa:hasFeatureOfInterest` on the `ObservationCollection` to the **measuring point** (the
  direct object of study), not to the wider area; the wider area is reachable through the sampling
  chain.

**Where a feature of interest is.** Any `sosa:FeatureOfInterest` with a known position, not only
a sample, can carry a geometry directly: `geo:hasGeometry` (domain `geo:Feature`) makes it a
GeoSPARQL feature that can be queried spatially. Two resources at the same place may share one
`geo:Geometry` IRI. `prov:atLocation` (range `prov:Location`) is not wrong, but it is the choice
when the position is given by an address or a description, or by another resource that is a place
in its own right, rather than by coordinates.

## R12 — Time

**Periods.** When a measurement covers a span of time (hourly count, daily total, period
measurement):
- use `sosa:phenomenonTime → time:Interval` with `time:hasBeginning` and `time:hasEnd`, each a
  `time:Instant` (inline blank node in small examples, skolem IRI in large datasets, R10);
- use a `time:Instant` only for point measurements, where the phenomenon has no duration;
- intervals are half-open: beginning inclusive, end exclusive (08:00–09:00 is hour 08).

**Instants with a time of day**, for every `time:Instant`:
- use `time:inXSDDateTimeStamp "…"^^xsd:dateTimeStamp`, never `time:inXSDDateTime`: OWL-Time
  deprecates it because `xsd:dateTime` does not require a time zone;
- when the source gives no time zone, assume the project's local time zone (project profile; for
  Flanders `Europe/Brussels`: `+01:00` in winter, `+02:00` during summer time, from the last Sunday
  of March to the last Sunday of October) and state that assumption in the discussion (§7); when
  the source does give one (`Z`, `+00:00`, …), keep it;
- a date only: `time:inXSDDate`; a year only: `time:inXSDgYear`.

**Time patterns**

| Pattern | When |
|---|---|
| `sosa:resultTime "…"^^xsd:dateTime` | a plain timestamp, no separate temporal entity needed |
| `sosa:phenomenonTime → time:Instant → time:inXSDDate` | calendar date |
| `sosa:phenomenonTime → time:Instant → time:inXSDDateTimeStamp` | calendar date and time, always with a time zone |
| `sosa:phenomenonTime → time:Interval → time:hasBeginning/hasEnd → time:Instant` | period observation |
| `sosa:phenomenonTime → time:Instant → time:inTimePosition → time:hasTRS ex:BP` | non-calendar TRS (R9) |

Distinguish `sosa:phenomenonTime` (when the phenomenon took place), `sosa:resultTime` (when the
result became available) and, for predictions, a result that may lie in the future.

## R13 — Derived and aggregated observations

When an observation is computed from other observations (daily total from hourly counts, a
deviation from a raw measurement):
- do **not** make it a `sosa:hasMember` of the source observations' collection;
- link it with `sosa:hasInputValue` to the **results** of the source observations (each input value
  matches a `sosa:hasInput` of the procedure), not to the observations or the collection: those are
  activities, not values;
- link it with `sosa:relatedObservation` to the source observations or collection;
- state all required properties (`sosa:madeBySensor`, `sosa:usedProcedure`,
  `sosa:hasFeatureOfInterest`, `sosa:observedProperty`) explicitly on the derived observation: it
  does not inherit them from a collection;
- in a three-layer model, use `sosa:hasInputValue` (⊂ `prov:used`) on the execution-level
  observation or actuation for the concrete entities that fill an input variable
  (`p-plan:correspondsToVariable`), not `sosa:hasInput` (R5); use `prov:used` only for what is not an
  input variable of the step (e.g. a machine learning model, R6).

## R14 — SSN/SOSA 2023 terms

SSN/SOSA 2023 moved and renamed terms from `ssn:` to `sosa:`. Older examples and literature still
use the old form, which gives an unknown-term error:

| Old (do not use) | SSN/SOSA 2023 |
|---|---|
| `ssn:implements` | `sosa:implements` |
| `ssn:implementedBy` | `sosa:implementedBy` |
| `ssn:hasProperty` | `sosa:hasProperty` |
| `ssn:System` | `sosa:System` |
| `sosa:ObservableProperty`, `sosa:ActuatableProperty` | `sosa:Property` (for both observed and actuated properties) |

Remove `@prefix ssn:` when no other `ssn:` terms remain. When in doubt, `lookup_term` suggests the
`sosa:` variant of an old term.

## R16 — Keep activities and entities apart

SSN/SOSA 2023 builds on PROV-O: a `sosa:Execution` (observation, actuation, sampling) is a
`prov:Activity`; a `sosa:System` (sensor, actuator, sampler), a `sosa:Platform` and a
`sosa:FeatureOfInterest` are `prov:Entity`. PROV-O declares the two classes disjoint, so a property
whose domain belongs to the other side makes the resource inconsistent (`[DISJOINTNESS]` in the
report of `validate_file`, with `--rules`). Two
mistakes recur:

**1. Record metadata on an observation.** A published data object (an LDES member, a version, a
database row) is not the observation it describes. The observation is the act of observing during
its `sosa:phenomenonTime`; the record was generated later by a pipeline. Properties of the record
(`prov:generatedAtTime`, `prov:invalidatedAtTime`, `prov:wasGeneratedBy`, `prov:wasAttributedTo`,
`prov:wasDerivedFrom`, `prov:wasRevisionOf`; and in spirit also `dct:isVersionOf`, validity periods
and deletion flags) do not belong on a `sosa:Observation`. Two solutions:

- **A. The observation is the published resource.** Keep only properties without a PROV domain,
  e.g. `dct:modified` as `ldes:timestampPath` and `dct:isVersionOf` for the version chain; no
  `prov:generatedAtTime`. Consistent and compatible with LDES version materialisation (a client
  receives observations), but record and observation still coincide.
- **B. A separate record.** The published resource is a `prov:Entity` that carries the record
  properties and points to the observation, e.g. with `foaf:primaryTopic`. Not with
  `prov:wasDerivedFrom`, whose range is `prov:Entity`. Every property sits on the right object, but
  version materialisation yields records, not observations.

Choose consciously and state the choice in the discussion (§6).

**2. Execution properties on a system or platform.** `sosa:hasFeatureOfInterest` is a
subproperty of `prov:used` (domain `prov:Activity`); `sosa:usedProcedure`, `sosa:hasResult` and
`prov:startedAtTime`/`prov:endedAtTime` also describe an activity. On a sensor or a platform they
make an entity an activity. The same goes, without an OWL inconsistency but against their
definition, for `sosa:observedProperty` and `sosa:actsOnProperty` on a sensor or actuator. Instead:
`sosa:observes` (sensor), `sosa:actsOn` (actuator) or the general `sosa:forProperty` for the property
a system handles; a `sosa:Deployment`
(`sosa:deployedSystem`, `sosa:deployedOnPlatform`, `sosa:hasFeatureOfInterest`) for what it is aimed
at; `sosa:hosts` for where it stands.

**3. The wrong thing as a result.** `sosa:hasResult` is a subproperty of `prov:generated` (domain
`prov:Activity`, range `prov:Entity`), so the result of an observation or actuation may be any
`prov:Entity`, but nothing that PROV-O declares disjoint with it: not another observation or any
other execution or activity (for a derived observation, point `sosa:relatedObservation` at the
source observation and `sosa:hasInputValue` at its result, R7), and not a PROV instantaneous event
(`prov:Generation`, `prov:Usage`, …). Nor a literal: `sosa:hasResult` is an object property; a bare
value goes in `sosa:hasSimpleResult`. The result of a sampling is a `sosa:Sample`.

## Decision points

Every example's discussion (§6) explains its non-trivial choices. These recur:

- `sosa:hasSimpleResult` versus `sosa:hasResult` with a separate result, a `qudt:QuantityValue` (use
  the result object when a unit, uncertainty or provenance is needed; R3);
- `sosa:ObservationCollection` versus loose observations (use a collection for shared metadata);
- flat versus three-layer model (R4);
- `sosa:hasInput` versus `prov:used` (R5);
- a machine learning model as `prov:Entity` versus as `sosa:Sensor` (R6);
- `p-plan:correspondsToVariable` and `p-plan:correspondsToStep` from abstract to concrete;
- `sosa:SpatialSample` versus a plain `sosa:FeatureOfInterest` for a measuring point (R11);
- `time:Instant` versus `time:Interval` for `sosa:phenomenonTime` (R12);
- a derived observation versus an ordinary collection member (R7, R13);
- QUDT unit versus register unit (R3);
- the observation itself or a separate record as the published resource (R16);
- which vocabulary for a term outside the core (R17, in [`linked-data.md`](linked-data.md));
- a domain kind as a concept (`dct:type`) or as a subclass (R18, in [`linked-data.md`](linked-data.md));
- which recurring pattern to follow, or why not (see [`patterns.md`](patterns.md)).
