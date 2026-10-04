# Proposed catalog source section

Status: **Proposed**, not automatically approved SRS requirements. Source: [full catalog](../sources/workspace/use-case-diagrams/drawio-catalog/source-catalog.md). Interpret relationships alongside [module notes](../sources/workspace/use-case-diagrams/drawio-catalog/module-notes.md), which contain later modeling refinements.

# 13. Module K — Decision Execution

Đây là core **Data Plane**.

## Use Cases

| ID | Use Case | Actor |
|---|---|---|
| EXE-01 | Execute Decision | Decision Consumer / Client Application |
| EXE-02 | Authenticate Decision Request | Identity Provider / IAM |
| EXE-03 | Validate Decision Request | Decision Consumer / Client Application |
| EXE-04 | Resolve Active Decision Version | RuleSphere |
| EXE-05 | Evaluate Decision Logic | RuleSphere |
| EXE-06 | Evaluate Business Rules | RuleSphere |
| EXE-07 | Evaluate Decision Table | RuleSphere |
| EXE-08 | Produce Decision Result | RuleSphere |
| EXE-09 | Return Execution Metadata | Decision Consumer / Client Application |
| EXE-10 | Handle Invalid Request | Decision Consumer / Client Application |
| EXE-11 | Handle Evaluation Failure | Decision Consumer / Client Application |
| EXE-12 | Execute Specific Decision Version | Decision Consumer / Client Application |

### Generalization

```text
Evaluate Decision Logic <<abstract>>
├── Evaluate Business Rules
├── Evaluate Decision Table
└── Evaluate Decision Expression
```

### Relations

```text
Execute Decision
  <<include>> Authenticate Decision Request
  <<include>> Validate Decision Request
  <<include>> Resolve Active Decision Version
  <<include>> Evaluate Decision Logic
  <<include>> Produce Decision Result

Return Execution Metadata
  <<extend>> Execute Decision

Handle Invalid Request
  <<extend>> Execute Decision

Handle Evaluation Failure
  <<extend>> Execute Decision

Execute Specific Decision Version
  --|> Execute Decision
```

---
