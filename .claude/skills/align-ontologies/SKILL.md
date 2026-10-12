---
name: align-ontologies
description: Analyse how two ontologies or a register and an ontology align (e.g. a parameter register against I-ADOPT) - structural comparison, a quantitative test per element, bottlenecks per component, consequences for the model, and a proposal. Use when the user asks whether a register or vocabulary fits another model, or to align two vocabularies.
---

<!-- Copied from oslo-ld-kit by sync.py. Do not edit here: change the kit (https://github.com/milieuinfo/oslo-ld-kit) and run sync.py again. -->

# Align ontologies

Worked example (OSLOthema-SSNSOSA-VL): `src/main/input/waterkwaliteit/csor_iadopt.md` and
`scripts/csor_iadopt_toets.py`, the alignment of the CSOR parameter register with I-ADOPT. Rules:
`../../../oslo-ld-kit/guide/` (R15: align classes with subclassing or OWL, never with SKOS relations).

## Structure of the analysis

```markdown
# <A> and <B>: analysis of the alignment

## 1. Summary                       [conclusion first: what fits, what does not, the proposal]
## 2. <B> in brief                  [the target model, as far as needed]
## 3. Structural comparison         [component by component: A's notion ↔ B's notion]
## 4. Quantitative test             [how many elements of A fit B, by a script]
## 5. Bottlenecks per component     [one subsection each, with real examples]
## 6. Consequences for the model    [per affected decision point]
## 7. Proposal for the alignment    [classes and properties; what is generated; what A's
                                     maintainers should restructure later]
## 8. Open points
## 9. Test per element              [which elements are not in their place, and why]
```

## Steps

1. **Understand both models** from their sources (ontology files, specifications), not from
   memory. Load them so that `lookup_term` and `search_terms` work on them. Assess a model that is
   new to the project on the criteria of R17 (`linked-data.md`) before aligning with it.
2. **Compare structurally**: map each component of one model to the other (e.g. property, object of
   interest, matrix, constraint), noting where one model mixes what the other separates.
3. **Test quantitatively with a script** over the actual data (all register entries), so that the
   analysis rests on numbers ("x of y entries fit directly") and can be repeated after changes.
4. **List the bottlenecks** per component with concrete entries as evidence.
5. **Propose the alignment** in OWL terms: subclassing, a direct property, or a generated
   description per entry; no SKOS relations between classes (R15). Separate what can be done now
   from what needs the register's maintainers.
6. **Trace the consequences** to the decision points of the model being built (decision document)
   and to open questions.

## Rules

- Conclusions first; evidence after.
- Every claim about a model is checked against its source.
- What the other model's maintainers must change becomes a concrete request (decision document,
  part C).
