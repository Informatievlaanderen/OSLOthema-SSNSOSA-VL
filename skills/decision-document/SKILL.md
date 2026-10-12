---
name: decision-document
description: Write or update a decision document that puts modelling choices to a working group (e.g. an OSLO trajectory) - per point the question, the worked-out proposal, rejected alternatives, consequences and status, grouped by who must decide. Use when modelling choices need to be presented for decision, or when the user asks for a "beslisdocument" or decision list.
---

# Decision document

The final model is often decided by a working group (in Flanders: an OSLO trajectory). The
decision document prepares that: a **worked-out proposal**, not an open questionnaire. Worked
example (OSLOthema-SSNSOSA-VL): `src/main/input/waterkwaliteit/beslisdocument.md`.

## Structure

```markdown
# Decision document: <model>

## 0. Purpose and method
[who decides; the status values; what happens after a decision; which documents this replaces]
[the data examples the proposals are based on, with paths]

## 1. Overview
[table: point, short title, status, for whom]

## 2. Part A: modelling choices for the working group
### A1. <title>
### A2. …

## 3. Part B: questions for the data owner
## 4. Part C: registers and neighbouring projects
## 5. Part D: not yet modelled
```

Parts by **who must decide or answer**:

| Part | For whom | Contents |
|---|---|---|
| A | working group | modelling choices |
| B | data owner | the meaning of the source data |
| C | maintainers of registers and neighbouring projects | changes or alignment outside this model |
| D | later | what is not modelled yet |

## Per point (part A)

- **Question.** One sentence.
- **Proposal.** As worked out in the data examples, with a short Turtle fragment.
- **Why.** The arguments, with numbers from the data where they help ("1605 of the 1998 results are
  below the reporting limit").
- **Rejected alternatives.** Each with the reason.
- **Consequence.** What follows, including deviations from guide rules or from neighbouring
  projects (then also a point in part C).
- **Open.** What is still undecided within the point.
- **Detail:** where the full reasoning is (the example's discussion, a separate document).
- **Status:** *proposal* (worked out, to be confirmed), *open* (no proposal), *decided* (after a
  session, with date and who decided).

## Rules

- Proposals reflect the **current state of the examples**; when an example changes, update the
  point, and vice versa.
- A decision is applied in the conversion script, then everything is regenerated and validated
  (skill `map-source-data`).
- Keep rejected alternatives after a decision; they explain the choice. When two readings are both
  defensible, an alternative mapping (skill `alternative-mapping`) makes the comparison concrete.
- A point that touches a register or another project's model goes to part C, addressed to its
  maintainers, with a concrete request.
- Decisions that set a general convention go into the guide (rule or pattern) once decided.
