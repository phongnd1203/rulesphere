# Proposed catalog source section

Status: **Proposed**, not automatically approved SRS requirements. Source: [full catalog](../sources/workspace/use-case-diagrams/drawio-catalog/source-catalog.md). Interpret relationships alongside [module notes](../sources/workspace/use-case-diagrams/drawio-catalog/module-notes.md), which contain later modeling refinements.

# 17. Module O — Audit & Compliance

## Use Cases

| ID | Use Case | Actor |
|---|---|---|
| AUD-01 | View Audit Trail | Reviewer / Approver |
| AUD-02 | Search Audit Events | Reviewer / Approver |
| AUD-03 | View Rule Change History | Reviewer / Approver |
| AUD-04 | View Approval History | Reviewer / Approver |
| AUD-05 | View Deployment History | Operations / SRE |
| AUD-06 | Trace Decision Provenance | Reviewer / Approver |
| AUD-07 | Trace Decision to Rule Version | Reviewer / Approver |
| AUD-08 | Trace Rule Version to Deployment | Reviewer / Approver |
| AUD-09 | Export Audit Events | Audit / SIEM |
| AUD-10 | Configure Audit Policy | Platform Administrator |

### Relations

```text
Trace Decision Provenance
  <<include>> Trace Decision to Rule Version
  <<include>> Trace Rule Version to Deployment

View Rule Change History
  <<include>> View Audit Trail

View Approval History
  <<include>> View Audit Trail

View Deployment History
  <<include>> View Audit Trail

Export Audit Events
  <<include>> Record Audit Event
```

---
