# Proposed catalog source section

Status: **Proposed**, not automatically approved SRS requirements. Source: [full catalog](../sources/workspace/use-case-diagrams/drawio-catalog/source-catalog.md). Interpret relationships alongside [module notes](../sources/workspace/use-case-diagrams/drawio-catalog/module-notes.md), which contain later modeling refinements.

# 4. Module B — Decision Project & Asset Management

## Use Cases

| ID | Use Case | Actor |
|---|---|---|
| DAM-01 | Manage Decision Project | Rule / Decision Author |
| DAM-02 | Create Decision Project | Rule / Decision Author |
| DAM-03 | View Decision Project | Platform User |
| DAM-04 | Update Decision Project | Rule / Decision Author |
| DAM-05 | Archive Decision Project | Platform Administrator |
| DAM-06 | Search Decision Assets | Platform User |
| DAM-07 | View Asset Metadata | Platform User |
| DAM-08 | Manage Asset Metadata | Rule / Decision Author |
| DAM-09 | View Asset Dependencies | Rule / Decision Author |

### Relations

Use generalization:

```text
Create Decision Project ──|> Manage Decision Project
Update Decision Project ──|> Manage Decision Project
Archive Decision Project ──|> Manage Decision Project
```

Hoặc nếu muốn diagram đơn giản hơn:

```text
Manage Decision Project
  <<include>> View Decision Project

Create Decision Project
  <<extend>> Manage Decision Project

Update Decision Project
  <<extend>> Manage Decision Project

Archive Decision Project
  <<extend>> Manage Decision Project
```

Tuy nhiên về UML semantics, CRUD variants thường phù hợp với **generalization** hơn `extend`.

---
