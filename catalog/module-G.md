# Proposed catalog source section

Status: **Proposed**, not automatically approved SRS requirements. Source: [full catalog](../sources/workspace/use-case-diagrams/drawio-catalog/source-catalog.md). Interpret relationships alongside [module notes](../sources/workspace/use-case-diagrams/drawio-catalog/module-notes.md), which contain later modeling refinements.

# 9. Module G — Review & Approval Workflow

Lưu ý: đây là **decision governance workflow**, không phải BPM orchestration chung.

## Use Cases

| ID | Use Case | Actor |
|---|---|---|
| GOV-01 | Submit Change for Review | Rule / Decision Author |
| GOV-02 | Review Decision Change | Reviewer / Approver |
| GOV-03 | Approve Decision Change | Reviewer / Approver |
| GOV-04 | Reject Decision Change | Reviewer / Approver |
| GOV-05 | Request Rework | Reviewer / Approver |
| GOV-06 | Cancel Review Request | Rule / Decision Author |
| GOV-07 | View Review Status | Rule / Decision Author |
| GOV-08 | View Approval History | Reviewer / Approver |
| GOV-09 | Enforce Approval Policy | Platform Administrator |

### Relations

```text
Submit Change for Review
  <<include>> Validate Decision
  <<include>> Create Decision Version

Review Decision Change
  <<include>> View Version Changes

Approve Decision Change
  <<extend>> Review Decision Change

Reject Decision Change
  <<extend>> Review Decision Change

Request Rework
  <<extend>> Review Decision Change

Cancel Review Request
  <<extend>> View Review Status
```

Điểm quan trọng:

```text
Approve
Reject
Request Rework
```

là các **alternative outcomes** của `Review Decision Change`.

---
