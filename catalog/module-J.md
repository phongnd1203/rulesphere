# Proposed catalog source section

Status: **Proposed**, not automatically approved SRS requirements. Source: [full catalog](../sources/workspace/use-case-diagrams/drawio-catalog/source-catalog.md). Interpret relationships alongside [module notes](../sources/workspace/use-case-diagrams/drawio-catalog/module-notes.md), which contain later modeling refinements.

# 12. Module J — Progressive Delivery

## Use Cases

| ID | Use Case | Actor |
|---|---|---|
| PRG-01 | Perform Progressive Deployment | Operations / SRE |
| PRG-02 | Configure Canary Deployment | Operations / SRE |
| PRG-03 | Adjust Canary Allocation | Operations / SRE |
| PRG-04 | Promote Canary Version | Operations / SRE |
| PRG-05 | Abort Canary Deployment | Operations / SRE |
| PRG-06 | Configure Shadow Deployment | Operations / SRE |
| PRG-07 | Execute Shadow Evaluation | Decision Consumer / Client Application |
| PRG-08 | Compare Shadow Results | Operations / SRE |
| PRG-09 | Stop Shadow Deployment | Operations / SRE |

### Generalization

```text
Perform Progressive Deployment <<abstract>>
├── Perform Canary Deployment
└── Perform Shadow Deployment
```

### Relations

```text
Perform Canary Deployment
  <<include>> Configure Canary Deployment
  <<include>> Deploy Decision

Adjust Canary Allocation
  <<extend>> Perform Canary Deployment

Promote Canary Version
  <<extend>> Perform Canary Deployment

Abort Canary Deployment
  <<extend>> Perform Canary Deployment

Perform Shadow Deployment
  <<include>> Configure Shadow Deployment
  <<include>> Deploy Decision

Compare Shadow Results
  <<include>> Execute Shadow Evaluation
```

---
