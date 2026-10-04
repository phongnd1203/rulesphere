# Proposed catalog source section

Status: **Proposed**, not automatically approved SRS requirements. Source: [full catalog](../sources/workspace/use-case-diagrams/drawio-catalog/source-catalog.md). Interpret relationships alongside [module notes](../sources/workspace/use-case-diagrams/drawio-catalog/module-notes.md), which contain later modeling refinements.

# 8. Module F — Version & Change Management

## Use Cases

| ID | Use Case | Actor |
|---|---|---|
| VER-01 | Manage Decision Version | Rule / Decision Author |
| VER-02 | Create Decision Version | Rule / Decision Author |
| VER-03 | View Version History | Platform User |
| VER-04 | Compare Versions | Rule / Decision Author |
| VER-05 | Restore Draft Version | Rule / Decision Author |
| VER-06 | Create Release Version | Rule / Decision Author |
| VER-07 | Deprecate Decision Version | Platform Administrator |
| VER-08 | View Version Lineage | Platform User |

### Relations

```text
Create Decision Version
  <<include>> Validate Decision

Create Release Version
  <<include>> Validate Release Candidate

Restore Draft Version
  <<extend>> View Version History

Compare Versions
  <<include>> View Version History
```

---
