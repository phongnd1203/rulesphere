# Proposed catalog source section

Status: **Proposed**, not automatically approved SRS requirements. Source: [full catalog](../sources/workspace/use-case-diagrams/drawio-catalog/source-catalog.md). Interpret relationships alongside [module notes](../sources/workspace/use-case-diagrams/drawio-catalog/module-notes.md), which contain later modeling refinements.

# 14. Module L — Explainability & Decision Trace

## Use Cases

| ID | Use Case | Actor |
|---|---|---|
| EXP-01 | Request Decision Explanation | Decision Consumer / Client Application |
| EXP-02 | Generate Decision Explanation | RuleSphere |
| EXP-03 | View Matched Rules | Rule / Decision Author |
| EXP-04 | View Evaluation Trace | Rule / Decision Author / Operations |
| EXP-05 | View Input Values Used | Rule / Decision Author |
| EXP-06 | View Output Derivation | Rule / Decision Author |
| EXP-07 | View Executed Decision Version | Platform User |
| EXP-08 | Retrieve Execution Trace | Operations / SRE |

### Relations

```text
Request Decision Explanation
  <<include>> Generate Decision Explanation

Generate Decision Explanation
  <<include>> View Executed Decision Version

View Matched Rules
  <<extend>> Generate Decision Explanation

View Evaluation Trace
  <<extend>> Generate Decision Explanation

View Input Values Used
  <<extend>> Generate Decision Explanation

View Output Derivation
  <<extend>> Generate Decision Explanation
```

---
