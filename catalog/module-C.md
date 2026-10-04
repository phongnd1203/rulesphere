# Proposed catalog source section

Status: **Proposed**, not automatically approved SRS requirements. Source: [full catalog](../sources/workspace/use-case-diagrams/drawio-catalog/source-catalog.md). Interpret relationships alongside [module notes](../sources/workspace/use-case-diagrams/drawio-catalog/module-notes.md), which contain later modeling refinements.

# 5. Module C — Decision Modeling & Rule Authoring

Đây là core module của **Decision Management / Control Plane**.

## Use Cases

| ID | Use Case | Actor |
|---|---|---|
| AUT-01 | Author Decision Model | Rule / Decision Author |
| AUT-02 | Create Decision Model | Rule / Decision Author |
| AUT-03 | Edit Decision Model | Rule / Decision Author |
| AUT-04 | Clone Decision Model | Rule / Decision Author |
| AUT-05 | Define Business Rule | Rule / Decision Author |
| AUT-06 | Edit Business Rule | Rule / Decision Author |
| AUT-07 | Define Decision Table | Rule / Decision Author |
| AUT-08 | Edit Decision Table | Rule / Decision Author |
| AUT-09 | Define Decision Expression | Rule / Decision Author |
| AUT-10 | Configure Rule Priority | Rule / Decision Author |
| AUT-11 | Enable / Disable Rule | Rule / Decision Author |
| AUT-12 | Define Rule Metadata | Rule / Decision Author |
| AUT-13 | View Rule Dependencies | Rule / Decision Author |
| AUT-14 | Compare Decision Versions | Rule / Decision Author |
| AUT-15 | Delete Draft Asset | Rule / Decision Author |

### Generalization

```text
Business Rule
Decision Table
Decision Expression
```

có thể được mô hình hóa dưới abstract use case:

```text
Author Decision Logic <<abstract>>
├── Define Business Rule
├── Define Decision Table
└── Define Decision Expression
```

### Relations

```text
Author Decision Model
  <<include>> Author Decision Logic
  <<include>> Define Rule Metadata
  <<include>> Validate Decision Model

Edit Decision Model
  <<include>> View Rule Dependencies

Define Business Rule
  <<include>> Define Rule Metadata

Configure Rule Priority
  <<extend>> Define Business Rule

Enable / Disable Rule
  <<extend>> Edit Business Rule

Clone Decision Model
  <<extend>> View Decision Model
```

---
