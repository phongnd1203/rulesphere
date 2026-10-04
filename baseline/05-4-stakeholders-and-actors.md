# SRS source section

Source: `RuleSphere_SRS_v1.0_Final.docx`. Requirements retain their original status; extraction is not a new approval.

## 4. Stakeholders and Actors

| ID | Actor | Type | Primary responsibility |
| --- | --- | --- | --- |
| A01 | Decision Author / Domain Expert | Human | Create/edit/test Decisions and schemas; submit releases. |
| A02 | Domain Approver / Decision Owner | Human | Review domain changes; approve according to risk policy; may overrule risk upward. |
| A03 | Workspace Owner | Human | Workspace governance participant for Tier-2+ approvals. |
| A04 | Compliance Officer | Human | Mandatory regulated/high-risk approval participant; audit/compliance review. |
| A05 | Enterprise Administrator | Human | Tenant/workspace/users/roles/credentials/shared-library administration. |
| A06 | Security Auditor | Human | Independent inspection of access, audit and security evidence. |
| A07 | Application Developer / Integrator | Human | Discover contracts and integrate consumer applications. |
| A08 | Consumer Application | External system | Invoke REST/gRPC evaluation, provide subject key/cohort/version pin. |

### 4.1 Actor-Goal Matrix

| Actor | G1 | G2 | G3 | G4 | G5 | G6 | G7 | G8 | G9 | G10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Decision Author | P | S | P | S | - | S | - | S | - | - |
| Domain Approver | - | P | S | S | - | P | - | - | - | - |
| Workspace Owner | - | P | - | S | - | P | S | - | - | - |
| Compliance Officer | - | P | - | P | - | S | - | - | - | - |
| Enterprise Admin | - | S | - | - | - | - | P | S | S | - |
| Security Auditor | - | S | - | P | - | - | P | - | - | - |
| Integrator | - | - | - | S | S | - | - | P | - | P |
| Consumer App | - | - | - | - | P | - | - | S | P | P |

