# Proposed catalog source section

Status: **Proposed**, not automatically approved SRS requirements. Source: [full catalog](../sources/workspace/use-case-diagrams/drawio-catalog/source-catalog.md). Interpret relationships alongside [module notes](../sources/workspace/use-case-diagrams/drawio-catalog/module-notes.md), which contain later modeling refinements.

# 15. Module M — Simulation & Impact Analysis

## Use Cases

| ID | Use Case | Actor |
|---|---|---|
| SIM-01 | Simulate Decision | Rule / Decision Author |
| SIM-02 | Simulate Draft Version | Rule / Decision Author |
| SIM-03 | Compare Decision Outputs | Rule / Decision Author |
| SIM-04 | Compare Decision Versions | Rule / Decision Author |
| SIM-05 | Analyze Rule Change Impact | Rule / Decision Author |
| SIM-06 | Identify Dependent Decisions | Rule / Decision Author |
| SIM-07 | Evaluate Decision against Dataset | Rule / Decision Author |

### Relations

```text
Simulate Draft Version
  --|> Simulate Decision

Compare Decision Outputs
  <<include>> Simulate Decision

Analyze Rule Change Impact
  <<include>> Identify Dependent Decisions

Evaluate Decision against Dataset
  <<include>> Simulate Decision
```

---
