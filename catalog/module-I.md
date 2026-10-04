# Proposed catalog source section

Status: **Proposed**, not automatically approved SRS requirements. Source: [full catalog](../sources/workspace/use-case-diagrams/drawio-catalog/source-catalog.md). Interpret relationships alongside [module notes](../sources/workspace/use-case-diagrams/drawio-catalog/module-notes.md), which contain later modeling refinements.

# 11. Module I — Environment & Deployment Management

## Use Cases

| ID | Use Case | Actor |
|---|---|---|
| DEP-01 | Manage Runtime Environment | Platform Administrator |
| DEP-02 | Create Environment | Platform Administrator |
| DEP-03 | Configure Environment | Platform Administrator |
| DEP-04 | Configure Deployment Policy | Platform Administrator |
| DEP-05 | Deploy Decision | Operations / SRE |
| DEP-06 | Promote Decision | Operations / SRE |
| DEP-07 | Roll Back Deployment | Operations / SRE |
| DEP-08 | Redeploy Decision | Operations / SRE |
| DEP-09 | Cancel Deployment | Operations / SRE |
| DEP-10 | View Deployment Status | Operations / SRE |
| DEP-11 | View Deployment History | Operations / SRE |
| DEP-12 | Validate Deployment | RuleSphere |
| DEP-13 | Distribute Artifact to Runtime | RuleSphere |
| DEP-14 | Verify Runtime Convergence | Operations / SRE |
| DEP-15 | Detect Version Drift | Operations / SRE |
| DEP-16 | Reconcile Runtime State | Operations / SRE |

### Relations

```text
Deploy Decision
  <<include>> Validate Deployment
  <<include>> Verify Artifact Integrity
  <<include>> Distribute Artifact to Runtime
  <<include>> Verify Runtime Convergence

Promote Decision
  <<include>> Deploy Decision

Redeploy Decision
  --|> Deploy Decision

Roll Back Deployment
  <<extend>> Deploy Decision

Detect Version Drift
  <<extend>> Verify Runtime Convergence

Reconcile Runtime State
  <<extend>> Detect Version Drift
```

`Rollback` không phải bước bắt buộc của deployment nên phù hợp với `<<extend>>`.

---
