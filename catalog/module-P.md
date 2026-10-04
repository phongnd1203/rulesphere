# Proposed catalog source section

Status: **Proposed**, not automatically approved SRS requirements. Source: [full catalog](../sources/workspace/use-case-diagrams/drawio-catalog/source-catalog.md). Interpret relationships alongside [module notes](../sources/workspace/use-case-diagrams/drawio-catalog/module-notes.md), which contain later modeling refinements.

# 18. Module P — Automation & CI/CD Integration

## Use Cases

| ID | Use Case | Actor |
|---|---|---|
| CICD-01 | Validate Decision via API | CI/CD & Automation |
| CICD-02 | Execute Tests via API | CI/CD & Automation |
| CICD-03 | Build Artifact via API | CI/CD & Automation |
| CICD-04 | Publish Artifact via API | CI/CD & Automation |
| CICD-05 | Trigger Deployment | CI/CD & Automation |
| CICD-06 | Query Deployment Status | CI/CD & Automation |
| CICD-07 | Retrieve Test Result | CI/CD & Automation |
| CICD-08 | Retrieve Validation Result | CI/CD & Automation |

### Relations

Các use case automation nên reuse business use cases hiện tại:

```text
Validate Decision via API
  <<include>> Validate Decision

Execute Tests via API
  <<include>> Execute Test Suite

Build Artifact via API
  <<include>> Build Decision Artifact

Publish Artifact via API
  <<include>> Publish Decision Artifact

Trigger Deployment
  <<include>> Deploy Decision

Query Deployment Status
  <<include>> View Deployment Status
```

Điều này tránh tạo hai implementation semantics khác nhau giữa UI và API.

---
