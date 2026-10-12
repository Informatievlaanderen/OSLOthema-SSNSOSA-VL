---
name: new-example
description: Create a new SSN/SOSA data example (Turtle, Mermaid diagram, README, discussion, optional exercise) following the OSLO modelling guide, and validate it. Use when the user asks for a new data example, a mapping of a small dataset to SSN/SOSA, or a revision or alternative of an existing example.
---

<!-- Copied from oslo-ld-kit by sync.py. Do not edit here: change the kit (https://github.com/milieuinfo/oslo-ld-kit) and run sync.py again. -->

# New SSN/SOSA data example

Create all files for one data example and validate them. The rules are in the guide
(`../../../oslo-ld-kit/guide/`); the project's `CLAUDE.md` has the **project profile**: examples directory, file
names, document language, time zone, unit registry, extra prefixes and how to validate. Read both
before starting. Write all documents in the project's language.

## Step 1 — Ask before creating anything

Ask with `AskUserQuestion` (at most four questions per round; ask the modelling choices, 3 and 6,
in the same round):

1. **Domain name** — becomes the directory name (e.g. `air-quality`).
2. **Data source or scenario** — one sentence on what is modelled.
3. **Architecture** — `flat` (single sensor, `sosa:ObservationCollection`) or `three-layer`
   (multi-step process: Planning / Deployment / Execution); see R4.
4. **Kind of example**:
   - **New** — build from scratch;
   - **Revision, source supplied** — the user shares a file with modelling errors; wait for it;
     then follow the skill `revise-mapping`;
   - **Revision, synthetic** — create an illustrative "before" file with typical architectural
     errors and a corrected "after" version (skill `revise-mapping`);
   - **Alternative next to an existing example** — a second defensible reading, not a revision;
     follow the skill `alternative-mapping`.
5. **Training exercise** — also create an exercise ([`exercise.md`](../../../oslo-ld-kit/guide/exercise.md))?
6. **Source of units** — only when the example has numeric results with a unit (R3): **QUDT**
   (default) or **a domain register** (the project profile names it). Otherwise note "n/a".

## Step 2 — Create the files, in this order

Finish each file before starting the next.

### 2a. README

Sections: **Source** (IRI or description of the original data), **Transformation** (steps such as
XSLT, `riot`, SPARQL or a script; "none" if there is none), **Mapping choices** (flat or
three-layer, in brief), **Diagram** (refers to the `.mmd`), **Output files**, **Usage** (commands).

### 2b. Turtle

A skeleton in blocks separated by `###` comment headers:

```turtle
### INFRASTRUCTURE
# sosa:Platform, sosa:System, sosa:Sensor / sosa:Actuator

### PROCEDURE AND PROPERTIES
# sosa:ObservingProcedure / sosa:ActuatingProcedure, sosa:Property

### OBSERVATIONS / ACTUATIONS
# sosa:Observation, sosa:ObservationCollection, sosa:Actuation, sosa:Result
```

For a three-layer model add `### PLANNING` (`p-plan:Plan`, `p-plan:Step`, `p-plan:Variable`),
`### DEPLOYMENT` (`sosa:Deployment`) and `### EXECUTION` (`prov:Activity`, `prov:Entity`,
`p-plan:correspondsToStep`, `p-plan:correspondsToVariable`), with one prefix per layer
([`ssn-sosa.md`](../../../oslo-ld-kit/guide/ssn-sosa.md#prefixes)).

Apply the rules of [`ssn-sosa.md`](../../../oslo-ld-kit/guide/ssn-sosa.md) and
[`linked-data.md`](../../../oslo-ld-kit/guide/linked-data.md); in particular R2 (required properties), R3
(`qudt:numericValue`, one unit source), R5, R7 and R13 (derived observations), R10 (IRIs), R11
(spatial samples), R12 (time zone) and R14 (SSN/SOSA 2023 terms). Check
[`patterns.md`](../../../oslo-ld-kit/guide/patterns.md): does a recurring pattern fit?

**Vocabulary check with the `ld-vocab` MCP server**, before writing the file:
- `lookup_term` on every class, predicate and vocabulary object, units included, with the **full
  IRI** written out with the file's own prefixes. Example terms (`ex:`, `plan:`, …) need no check.
- Check domain and range. Take the suggestion when a term does not exist (e.g. the `sosa:` variant
  of an `ssn:` term), or search with `search_terms`. Never invent a term.
- Deprecated terms are not used; tell the user and take the replacement (e.g.
  `time:inXSDDateTime` → `time:inXSDDateTimeStamp`, R12).
- Units according to question 6: QUDT via `search_terms` (`metre` → `unit:M`); a register unit via
  `search_terms` on its label, and `lookup_term` for its mapping to QUDT, which goes into the
  discussion (§6), not into the data.

Every IRI in the diagram must also be in the Turtle.

### 2c. Diagram

Follow [`diagrams.md`](../../../oslo-ld-kit/guide/diagrams.md): palette, one `style` line per node, flat or
three-layer nesting, relations after the subgraphs.

### 2d. Discussion document

All nine sections of [`discussion-document.md`](../../../oslo-ld-kit/guide/discussion-document.md), with the
project's file name and section titles. Unknown answers become a concrete `<!-- TODO: … -->`
question, never a generic placeholder.

### 2e. Exercise (if asked in question 5)

Structure of [`exercise.md`](../../../oslo-ld-kit/guide/exercise.md); the questions in steps 1, 2 and 4 steer to
the example's decision points.

**Two defensible readings?** When a choice can be defended in two ways — for instance because the
domain's natural reading differs from a pattern in another example — do not choose silently. Model
the main reading, record the other as a rejected alternative in §6 of the discussion, and propose an
alternative mapping in the final report.

## Step 3 — Validate

Run `validate_file` on every new Turtle file and act on the report (see
[`linked-data.md`](../../../oslo-ld-kit/guide/linked-data.md#validation)): fix every `[VOCAB ERROR]` and every rule
violation; investigate `[MODEL INVALID]`; report the remaining SHACL messages; a rule `[warning]`
may stay when the source lacks the information, documented in §6. Repeat until there is no
`[VOCAB ERROR]` left. Run the project's own pipeline only when the project profile says it is
needed (e.g. for generated output).

## Step 4 — Final report

```
Created:
  [x] README
  [x] <name>.ttl
  [x] <name>.mmd
  [x] discussion
  [x / n/a] exercise

Units: [QUDT / register <name>, N units without a QUDT mapping / n/a]
Validation: [ok / N [VOCAB ERROR] fixed; open [MODEL INVALID] / SHACL messages / warnings kept]
Pipeline: [not needed / run because …]

Discussion sections:
  [x] 1. …  (one line per section, [TODO] where open)

Possible alternative readings:
  - [choice — main model versus alternative — follows …] / none

Open TODOs in the discussion:
  - §3: [specific question]
```
