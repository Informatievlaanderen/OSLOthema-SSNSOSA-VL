---
name: map-source-data
description: Map a real source dataset (spreadsheets, CSV, JSON exports from a data owner) to SSN/SOSA in phases, with scripted and reproducible conversion, reuse of existing registers, and an explicit list of decisions and questions. Use when the user receives data from a data owner and asks to map it, or plans a larger mapping than a single example.
---

# Map source data

For a mapping of real data, larger than one illustrative example. Worked example
(OSLOthema-SSNSOSA-VL): `src/main/input/waterkwaliteit/` (`stappenplan.md`, `codelijsten.md`,
`featureofinterest.md`, `scripts/`). Rules: `../../guide/`.

## Principles

1. **Scope with the data owner first.** Ask what matters first and what not now. Typically: the
   measured results first; norms, assessments and interpretations later; full descriptions of
   companies, stations and other objects only as far as needed as feature of interest or
   identifier. Write the scope down with its source (who said it, when).
2. **Reuse before inventing.** Existing registers and code lists for what is measured and in which
   unit, existing datasets for features of interest (link to their IRIs), existing ontologies for
   the domain. New code lists only for what nothing covers, and only when the mapping needs them —
   a code list is not a prerequisite for mapping results. Choose an ontology outside the core under
   R17 (`linked-data.md`): compare candidates, do not take the first match.
3. **Script everything.** The conversion is a script that regenerates all output from the source
   files; a decision is changed in the script, then everything is regenerated and validated. No
   hand edits to generated Turtle.
4. **Full data and a validation subset.** The script writes the full dataset (skipped by bulk
   validation) and a small representative subset that is validated (guide: Large datasets),
   selected by a variable in the script.
5. **Project conventions apply** (guide): SSN/SOSA 2023 terms (R14), `qudt:numericValue` (R3),
   skolem IRIs for nested resources (R10), time zone (R12), every `[error]` under `[VOCAB]` fixed.

## Steps

1. **Inventory the source**: per file and sheet, what it contains and how many rows; which columns
   identify objects (keys for IRIs); units and signs (e.g. "<" values); time columns and whether
   they have a time zone.
2. **Plan in phases** in a plan document: phase 0 preparation, phase 1 the results (one step per
   result set), later phases for norms and characteristics. Per step: source file, target pattern,
   features of interest, open points.
3. **Decide the features of interest**: what each observation is about (a sample, a discharge, a
   measuring point), and how to link to external datasets (matching keys, e.g. a station number
   that equals an identifier in another register). Check external datasets for errors before
   reusing them; report the errors to their owners.
4. **Link to registers**: which register concept each source value maps to (parameter, unit,
   matrix, procedure). Make the linking reproducible (a query or script over the register), and
   list values that have no match.
5. **Map phase by phase**, one script per result set sharing a common module; validate the subset
   of each with `validate_file`.
6. **Record decisions and questions**: modelling choices as proposals with rejected alternatives
   (discussion §6 of each example, or a decision document — skill `decision-document`); questions
   about the meaning of the source data in a list for the data owner.

## Outputs

- a plan document with principles, phases and steps;
- one example directory per result set (Turtle subset, full data, diagram, README, discussion);
- the scripts and a shared module;
- documents for features of interest and code lists where they need explaining;
- a list of questions for the data owner;
- when a working group must decide: a decision document.
