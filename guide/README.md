# Modelling guide

The knowledge behind the OSLO SSN/SOSA data examples, written down so that any project can reuse it:
how to model observations, samples, time and units; how to construct IRIs; how to document and
validate an example; and which patterns other domains have already used.

## Parts

| File | Contents | Scope |
|---|---|---|
| [`linked-data.md`](linked-data.md) | IRIs, blank nodes, prefixes, code lists, application profiles, large datasets, choosing vocabularies, validation (R10, R15, R17) | any RDF project |
| [`ssn-sosa.md`](ssn-sosa.md) | modelling rules for SSN/SOSA 2023 with PROV-O, P-PLAN, QUDT and OWL-Time (R1–R9, R11–R14, R16), time patterns, decision points | observation data |
| [`patterns.md`](patterns.md) | patterns that recur across domains, with the examples that use them | observation data |
| [`discussion-document.md`](discussion-document.md) | the nine-section discussion that accompanies every example | documentation |
| [`exercise.md`](exercise.md) | the structure of a training exercise | documentation |
| [`diagrams.md`](diagrams.md) | Mermaid conventions: palette, nesting, labels | documentation |

The skills in `../skills/` describe the workflows (new example, revision, alternative mapping, source
data mapping, decision document, ontology design, ontology alignment) and refer to this guide for
the rules. The enforceable rules are also SHACL shapes in `../rules/ssn-sosa-rules.ttl`.

## Rule numbers

Rules are numbered R1–R17 across the guide. The numbers are stable: data examples, discussion
documents and scripts refer to them. A new rule gets the next free number; a withdrawn rule keeps
its number with the note *withdrawn* and the reason.

## Project profile

The guide is project-neutral. Everything that differs per project is declared in the project's
`CLAUDE.md`, in a section **Project profile**:

| Setting | Example (OSLOthema-SSNSOSA-VL) |
|---|---|
| Examples directory | `src/main/input/<domain>/` |
| Ontology directory | `src/main/resources/` |
| Document language | Dutch |
| File names | discussion `bespreking.md`, exercise `opdracht.md`, revision `<name>_herzien.ttl`, comparison `<name>_vergelijking.mmd`, alternative `alternatief/` |
| Section titles of the discussion document | Dutch titles, see [`discussion-document.md`](discussion-document.md) |
| Local time zone (R12) | `Europe/Brussels` |
| Unit registry (R3) | CSOR (`csor-eenheid:`) |
| Validation | MCP server `ld-vocab` (`validate_file`), plus the project's own pipeline if any |
| Extra prefixes | domain prefixes, shared infrastructure (e.g. `htg:`) |

When the guide says "the discussion document" or "the revision file", use the project's file name.

## Keeping it current

A lesson learnt in a project — a correction, a new convention — goes into this guide (or into the
rules file if it can be checked), not into a project's private notes. That is what makes it
available to the next project.

Write in British English.
