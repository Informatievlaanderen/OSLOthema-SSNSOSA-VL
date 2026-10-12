# Training exercise

An optional exercise that accompanies a data example, for workshops. It has a use case and four
steps, and refers to the example's Turtle and diagram as the reference solution. File name and
language from the project profile (Dutch OSLO projects: `opdracht.md`, titles in Dutch).

## Structure

```markdown
# Modelling exercise: <title>

## Use case
### Context
[two to four sentences on the domain]

### Description of the system
[table or list of components and their characteristics]

### Concrete measurements
[table with data points]

---

## Step 1 — Identify the SOSA concepts
*Individually — 10 minutes*
[table to fill in: six to eight domain-specific questions, e.g. "What is the feature of interest?"]

## Step 2 — Sketch a diagram
*In pairs — 15 minutes*
[instructions for the three or four layers + three guiding questions]

## Step 3 — Write the Turtle
*Individually or in groups — 20 minutes*
[numbered minimum requirements; base IRI https://example.org/<domain>/]

## Step 4 — Plenary discussion
*Plenary — 15 minutes*
[four or five discussion questions about the modelling choices]

---

*Reference solution: `<name>.ttl` and `<name>.mmd`*
```

## Guidelines

- The questions in steps 1, 2 and 4 are domain-specific and steer towards the example's key
  decisions (the decision points in [`ssn-sosa.md`](ssn-sosa.md#decision-points) and §6 of its
  discussion): why `hasResult` rather than `hasSimpleResult`, why a SpatialSample, why an interval.
- Step 3 lists the minimum Turtle requirements, not the full solution.
- The list of SOSA classes offered in step 1 uses current SSN/SOSA 2023 names (`Property`, not
  `ObservableProperty`; R14).
