# SRS source section

Source: `RuleSphere_SRS_v1.0_Final.docx`. Requirements retain their original status; extraction is not a new approval.

## 11. Audit, Privacy and Retention

| Store tier | Content | Retention baseline | Purpose |
| --- | --- | --- | --- |
| Hot Trace | Full masked/tokenized Execution Trace Tree | Configurable 30-90 days | Debug, dispute, near-term explainability |
| Compliance Ledger | ExecutionID, DecisionVersion, InputHash, Output, MatchedNodeIDs, Timestamp, approval/release evidence reference | Configurable 5-7 years | Legal/regulatory audit |

The Sponsor example 'ApprovedByTicket' is normalized in this SRS as an approval/release evidence reference because the existence and identifier format of an external ticketing system has not been mandated. If a future integration standardizes a ticket ID, that field can be bound through an API/ADR without changing the audit intent.

### 11.1 Sensitive Data

Schema fields marked is_sensitive=true must be protected before persistence. The protection mechanism may be masking, tokenization or hashing according to data classification and retrieval requirements. Plaintext sensitive values are prohibited in persisted execution traces.

