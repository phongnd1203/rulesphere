# Proposed catalog source section

Status: **Proposed**, not automatically approved SRS requirements. Source: [full catalog](../sources/workspace/use-case-diagrams/drawio-catalog/source-catalog.md). Interpret relationships alongside [module notes](../sources/workspace/use-case-diagrams/drawio-catalog/module-notes.md), which contain later modeling refinements.

# 6. Module D — Data Contract Management

## Use Cases

| ID | Use Case | Actor |
|---|---|---|
| DCM-01 | Manage Decision Contract | Rule / Decision Author |
| DCM-02 | Define Input Contract | Rule / Decision Author |
| DCM-03 | Define Output Contract | Rule / Decision Author |
| DCM-04 | Define Data Types | Rule / Decision Author |
| DCM-05 | Define Validation Constraints | Rule / Decision Author |
| DCM-06 | Validate Decision Contract | Rule / Decision Author |
| DCM-07 | Validate Contract Compatibility | Rule / Decision Author |
| DCM-08 | View Decision Contract | Decision Consumer / Client Application |
| DCM-09 | Export Decision Contract | Decision Consumer / Client Application |

### Relations

```text
Manage Decision Contract
  <<include>> Define Input Contract
  <<include>> Define Output Contract

Define Input Contract
  <<include>> Define Data Types

Define Output Contract
  <<include>> Define Data Types

Define Validation Constraints
  <<extend>> Define Input Contract
  <<extend>> Define Output Contract

Validate Contract Compatibility
  <<include>> Validate Decision Contract
```

---
