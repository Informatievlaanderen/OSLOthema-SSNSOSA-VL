---
name: design-ontology
description: Design a domain ontology that is at the same time the source of its application profile - OWL classes and restrictions from which the SHACL is generated, constraints on own subclasses only, a generated UML diagram, and a mapping from an older profile. Use when the user asks to design or revise an ontology, an application profile, or SHACL shapes for a domain.
---

# Design an ontology and application profile

Worked example (OSLOthema-SSNSOSA-VL):
`src/main/resources/be/vlaanderen/data/ns/waterkwaliteit/waterkwaliteit.ttl` and decision document
A14–A15 in `src/main/input/waterkwaliteit/beslisdocument.md`. Rules:
[`linked-data.md`](../../guide/linked-data.md#ontologies-and-application-profiles).

## Principles

1. **One source.** The ontology file holds the classes, properties and the profile's constraints as
   OWL restrictions; the SHACL is generated from it (the `ld-vocab` server does so with
   `--generate-shapes`). No hand-maintained SHACL beside it.
2. **Reuse, then specialise.** Reuse SSN/SOSA, PROV-O, QUDT, OWL-Time, GeoSPARQL and existing
   registers. Define a class of your own only where the domain needs constraints or meaning of its
   own, as a subclass of the reused class (`wk:WaterkwaliteitObservatie ⊂ sosa:Observation`).
   A kind without rules of its own stays a concept in a code list, with `dct:type` (R18); a rule
   hung on a `dct:type` value means the kind should be a subclass.
3. **Constrain your own subclasses, never reused classes.** A restriction on `sosa:Observation`
   would apply to every SOSA dataset. Data types the subclass and the reused superclasses
   explicitly (SHACL validates the non-inferred graph).
4. **Align with subclassing and OWL**, not SKOS (R15). A class that is also a register concept is a
   modelling smell.
5. **Be explicit about what the generator cannot express** (a choice between properties,
   collection–member consistency, labels in the profile's context) and document it.

## Steps

1. **Collect requirements** from the data examples: which classes the examples type, which
   properties they use, with which cardinalities.
2. **Write classes and restrictions**: per class its superclasses and, per property, a restriction
   that yields the intended SHACL (see the table in the guide): `owl:someValuesFrom` for required
   with a type, `owl:allValuesFrom` for optional with a type, cardinalities for counts,
   `owl:unionOf` for a choice of types, `owl:minCardinality 0` to make an inherited
   `someValuesFrom` optional.
3. **Check every term** with `lookup_term` (reused classes and properties exist, are not
   deprecated, and their domain and range fit). A reused term from a vocabulary outside the core is
   chosen under R17 (`linked-data.md`), with the candidates considered.
4. **Validate the examples** against the generated shapes with `validate_file`; every violation
   either shows an error in an example or a restriction that is too strict.
5. **Validate the ontology itself** with `validate_file` too: rule R15 (no SKOS between classes)
   applies to ontology files.
6. **Generate the UML diagram** from the ontology (classes, inheritance, properties with
   multiplicity as the SHACL enforces them) instead of drawing it.
7. **Map the old profile**, if one exists: a table *old class or property → new*, including what
   disappears and what is still open. Modelling choices that need a decision go into the decision
   document (skill `decision-document`).

## Outputs

The ontology file (in the project's ontology directory, so that it is loaded), the generated UML,
the mapping table from the old profile, and the decision points.
