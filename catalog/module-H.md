# Proposed catalog source section

Status: **Proposed**, not automatically approved SRS requirements. Source: [full catalog](../sources/workspace/use-case-diagrams/drawio-catalog/source-catalog.md). Interpret relationships alongside [module notes](../sources/workspace/use-case-diagrams/drawio-catalog/module-notes.md), which contain later modeling refinements.

# 10. Module H — Build & Artifact Management

Đây là boundary giữa Control Plane và Distribution Plane.

## Use Cases

| ID | Use Case | Actor |
|---|---|---|
| ART-01 | Build Decision Artifact | Rule / Decision Author / CI/CD |
| ART-02 | Validate Build Inputs | RuleSphere |
| ART-03 | Package Decision Artifact | RuleSphere |
| ART-04 | Generate Artifact Metadata | RuleSphere |
| ART-05 | Publish Decision Artifact | Rule / Decision Author / CI/CD |
| ART-06 | View Published Artifact | Platform User |
| ART-07 | Verify Artifact Integrity | Operations / SRE |
| ART-08 | View Artifact Provenance | Reviewer / Approver |
| ART-09 | Deprecate Artifact | Platform Administrator |

### Relations

```text
Build Decision Artifact
  <<include>> Validate Build Inputs
  <<include>> Package Decision Artifact
  <<include>> Generate Artifact Metadata

Publish Decision Artifact
  <<include>> Build Decision Artifact
  <<include>> Verify Artifact Integrity

View Artifact Provenance
  <<include>> View Version Lineage
```

---
