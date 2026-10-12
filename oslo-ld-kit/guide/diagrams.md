# Mermaid diagrams

Every data example has a Mermaid diagram (`<name>.mmd`). These conventions are normative.

Use `flowchart LR` for infrastructure-heavy diagrams and `flowchart RL` for three-layer diagrams.

## Palette

```
Subgraph INFRA:               fill:#b0d9e7,stroke:#2E5C8A,color:#000
Node Platform/System/Sensor:  fill:#60c4e4,stroke:#2E5C8A,color:#000
Subgraph PROC/PLANNING:       fill:#b8a2d4,stroke:#2E5C8A,color:#000
Node p-plan:Plan/Step:        fill:#7f59ae,stroke:#2E5C8A,color:#fff
Node sosa:Procedure:          fill:#c6a0f5,stroke:#2E5C8A,color:#000
Node Property/Variable:       fill:#fe7130,stroke:#2E5C8A,color:#000
Subgraph WAAR/EXECUTION:      fill:#e7a3be,stroke:#2E5C8A,color:#000
Node Observation/Activity:    fill:#e54b89,stroke:#2E5C8A,color:#fff
Node Result/Entity/Instant:   fill:#f8b622,stroke:#2E5C8A,color:#000
Subgraph DERIVATION:          fill:#f8e1ad,stroke:#2E5C8A,color:#000
```

Every node gets its own `style` line; no node may lack one. Styles come after the subgraph
definitions.

## Nesting

**Flat model**, three sibling subgraphs (labels in the project's language; Dutch OSLO projects use
the labels below):

```
subgraph PROC["PROCEDURE"] … end
subgraph INFRA["INFRASTRUCTUUR"] … end
subgraph WAAR["WAARNEMING"] … end
```

**Three-layer model**, three sibling subgraphs with a nested DERIVATION:

```
subgraph PLANNING["PLANNING"] … end
subgraph DEPLOYMENT["DEPLOYMENT"] … end
subgraph EXECUTION["EXECUTION"]
    subgraph DERIVATION["DERIVATION"] … end
end
```

Relations that cross subgraphs are written after all subgraph definitions.

## Labels

Use the short property name for readability: `-->|sosa:hosts|`, `-->|correspondsToStep|`, and a
dotted arrow for ordering: `-.->|isPrecededBy|`.

## Consistency with the Turtle

Every IRI in the diagram also occurs in the Turtle file. A comparison diagram
(`<name>_vergelijking.mmd` in Dutch projects) shows two models side by side, focused on what
differs: before and after a revision, or a main model and its alternative.
