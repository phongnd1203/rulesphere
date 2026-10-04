# SRS source section

Source: `RuleSphere_SRS_v1.0_Final.docx`. Requirements retain their original status; extraction is not a new approval.

## 5. Conceptual Domain Model

The conceptual hierarchy and ownership model is authoritative for requirements; it is not a physical database schema.

| Concept | Definition / invariant |
| --- | --- |
| Tenant | Enterprise/legal entity boundary. Hard isolation for data, users, API keys and audit. |
| Workspace | Business/domain boundary owned by one Tenant; isolated by default. |
| Shared Library | Tenant-level immutable, versioned reusable asset; only approved cross-workspace reuse mechanism. |
| Decision | Named business decision owned by a Workspace. |
| Decision Version | Versioned immutable snapshot once approved/published; references exact graph/schema/dependencies. |
| Decision Graph | Strict directed acyclic graph of decision nodes executed in one synchronous context. |
| Decision Node | Decision Table, Decision Tree, Scripted Expression or Rule Set. |
| Schema Version | Versioned input/output data contract including type, requiredness and sensitivity metadata. |
| Governance Policy | Risk calculation and approval requirements. |
| Release | Governed candidate plus deployment state and rollout policy. |
| Executable Artifact | Validated/compiled immutable representation consumed by Data Plane. |
| Execution | One evaluation context bound to an atomic Decision snapshot. |
| Execution Trace Tree | Auditable tree of evaluated nodes/branches/intermediate/final outcomes after masking. |

### 5.1 Core Invariants

- Tenant resources shall never be directly accessible from another Tenant.

- Direct cross-workspace references are prohibited; only version-pinned Tenant Shared Library assets may be consumed.

- Decision Graphs shall be acyclic.

- One execution shall use one atomic version snapshot for the entire graph and its resolved dependencies.

- A Maker shall never approve the same release they authored.

- Published executable artifacts shall be immutable.

- Shadow result shall never affect the production response.

- Sensitive fields shall not be persisted as plaintext in execution traces.

