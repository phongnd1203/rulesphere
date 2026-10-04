# Proposed catalog source section

Status: **Proposed**, not automatically approved SRS requirements. Source: [full catalog](../sources/workspace/use-case-diagrams/drawio-catalog/source-catalog.md). Interpret relationships alongside [module notes](../sources/workspace/use-case-diagrams/drawio-catalog/module-notes.md), which contain later modeling refinements.

# 7. Module E — Validation & Testing

## Use Cases

| ID | Use Case | Actor |
|---|---|---|
| VAL-01 | Validate Decision | Rule / Decision Author |
| VAL-02 | Validate Rule Syntax | Rule / Decision Author |
| VAL-03 | Validate Decision Structure | Rule / Decision Author |
| VAL-04 | Validate References | Rule / Decision Author |
| VAL-05 | Detect Rule Conflicts | Rule / Decision Author |
| VAL-06 | Detect Redundant / Unreachable Rules | Rule / Decision Author |
| TST-01 | Manage Test Cases | Rule / Decision Author |
| TST-02 | Create Test Case | Rule / Decision Author |
| TST-03 | Execute Decision Test | Rule / Decision Author |
| TST-04 | Execute Test Suite | Rule / Decision Author |
| TST-05 | View Test Result | Rule / Decision Author |
| TST-06 | Compare Expected vs Actual Result | Rule / Decision Author |
| TST-07 | Run Regression Test | Rule / Decision Author |
| TST-08 | Validate Release Candidate | Reviewer / Approver |

### Relations

```text
Validate Decision
  <<include>> Validate Rule Syntax
  <<include>> Validate Decision Structure
  <<include>> Validate References

Detect Rule Conflicts
  <<extend>> Validate Decision

Detect Redundant / Unreachable Rules
  <<extend>> Validate Decision

Execute Decision Test
  <<include>> Validate Decision

Execute Test Suite
  <<include>> Execute Decision Test

Compare Expected vs Actual Result
  <<include>> View Test Result

Run Regression Test
  <<include>> Execute Test Suite

Validate Release Candidate
  <<include>> Validate Decision
  <<include>> Execute Test Suite
```

---
