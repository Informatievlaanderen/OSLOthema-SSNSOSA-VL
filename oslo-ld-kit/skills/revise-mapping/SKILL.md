---
name: revise-mapping
description: Revise a received RDF data file or mapping that contains modelling errors - keep the original, write a corrected version, and document every improvement with its rationale. Use when the user supplies an existing example or mapping to correct, or asks to improve an existing mapping.
---

# Revise an existing mapping

A revision **replaces** a model that is wrong. When the existing model is defensible and only a
different reading is possible, use the skill `alternative-mapping` instead.

File names come from the project profile in `CLAUDE.md` (Dutch OSLO projects: `<name>_herzien.ttl`,
`<name>_vergelijking.mmd`, section "Verbeterpunten"). Rules: `../../guide/`.

## Steps

1. **Keep the original** in a `source/` directory, in the format it was received in (e.g.
   `.jsonld`). Store Turtle so that the project's bulk validation skips it but RDF tools still read
   it (OSLO projects: `source/<name>.trig`; Turtle is valid TriG). A Turtle version derived from
   another format (e.g. with `riot`) is stored the same way. Never edit the original.
2. **Diagnose.** Run `validate_file` on the original: the `[VOCAB ERROR]`, `[MODEL INVALID]` and
   rule messages (R-numbers) are the first list of problems. Then read it against the guide for
   what validation cannot see: class choice (R1), required properties (R2), units (R3), `hasInput`
   versus `prov:used` (R5), derived observations (R7, R13), IRIs and blank nodes (R10), time (R12),
   old SSN terms (R14), `http`/`https` in prefixes.
3. **Write the revised file** with the corrected modelling, following the skill `new-example`
   step 2b (vocabulary check with full IRIs).
4. **Document the improvements** in the README, section *Improvements* (Dutch: *Verbeterpunten*):
   a numbered list `original approach → corrected approach → rationale`, the rationale citing the
   SOSA / PROV-O specification or the rule number.
5. **Comparison diagram** when the architecture changes significantly: both models side by side,
   focused on what differs ([`diagrams.md`](../../guide/diagrams.md)).
6. **Discussion document** describing the corrected version
   ([`discussion-document.md`](../../guide/discussion-document.md)).
7. **Validate** the revised file with `validate_file`; every `[VOCAB ERROR]` and rule violation must
   be fixed.

## Synthetic revision

For training material, create an illustrative "before" file that shows typical architectural
errors (e.g. `sosa:hasInput` on an observation, `sosa:hasInputValue` to an observation,
`ssn:implements`, `qudt:value`, a blank node for an externally referenced resource) and the
corrected "after" file, documented as above.

## Note on received material

A received file may come from a source the project does not endorse. Correct it in the revised
file; do not report its errors again in later analyses unless asked.
