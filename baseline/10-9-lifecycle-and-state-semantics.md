# SRS source section

Source: `RuleSphere_SRS_v1.0_Final.docx`. Requirements retain their original status; extraction is not a new approval.

## 9. Lifecycle and State Semantics

### 9.1 Governance Lifecycle

Draft -> In Review -> Approved, with Reject returning the candidate to Draft. Approved means governance requirements are satisfied; it does not imply 100% production activation.

### 9.2 Deployment Lifecycle

Approved -> Shadow and/or Canary -> Active -> Superseded/Archived. Rollback changes desired Active state to an eligible previously approved immutable version. A candidate may be stopped before Active without mutating its immutable artifact.

### 9.3 Risk and Approval Rules

| Risk Tier | System-derived basis | Required approval |
| --- | --- | --- |
| Tier 1 - Low | Change scope + compatibility + 30-day traffic | 1 Domain Approver |
| Tier 2 - Medium | Higher calculated risk | Sequential: Domain Peer Review -> Workspace Owner |
| Tier 3 - High/Regulated | High blast radius/regulatory impact | Quorum: Domain Owner AND Compliance Officer |

Approvers may overrule risk upward only. Maker-Checker applies to every tier.

