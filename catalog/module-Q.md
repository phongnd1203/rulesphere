# Proposed catalog source section

Status: **Proposed**, not automatically approved SRS requirements. Source: [full catalog](../sources/workspace/use-case-diagrams/drawio-catalog/source-catalog.md). Interpret relationships alongside [module notes](../sources/workspace/use-case-diagrams/drawio-catalog/module-notes.md), which contain later modeling refinements.

# 19. Module Q — Platform Administration

## Use Cases

| ID | Use Case | Actor |
|---|---|---|
| ADM-01 | Manage Platform Configuration | Platform Administrator |
| ADM-02 | Configure Platform Policies | Platform Administrator |
| ADM-03 | Configure Execution Limits | Platform Administrator |
| ADM-04 | Configure Retention Policy | Platform Administrator |
| ADM-05 | Configure Audit Policy | Platform Administrator |
| ADM-06 | Configure Deployment Policy | Platform Administrator |
| ADM-07 | Manage Runtime Nodes | Platform Administrator |
| ADM-08 | Register Runtime Node | Platform Administrator |
| ADM-09 | Deregister Runtime Node | Platform Administrator |
| ADM-10 | View Runtime Node Status | Platform Administrator |
| ADM-11 | View Platform Health | Platform Administrator |
| ADM-12 | View Platform Usage | Platform Administrator |

### Relations

```text
Manage Platform Configuration
  <<include>> Configure Platform Policies

Configure Execution Limits
  <<extend>> Configure Platform Policies

Configure Retention Policy
  <<extend>> Configure Platform Policies

Configure Audit Policy
  <<extend>> Configure Platform Policies

Configure Deployment Policy
  <<extend>> Configure Platform Policies

Register Runtime Node
  --|> Manage Runtime Nodes

Deregister Runtime Node
  --|> Manage Runtime Nodes

View Runtime Node Status
  <<include>> Manage Runtime Nodes
```

---
