# SRS source section

Source: `RuleSphere_SRS_v1.0_Final.docx`. Requirements retain their original status; extraction is not a new approval.

## 2. Scope and Boundaries

### 2.1 In Scope

- Tenant -> Workspace hierarchical isolation and tenant-level immutable Shared Libraries.

- Decision modeling using Decision Graphs containing Decision Table, Decision Tree, Scripted Expression and Rule Set nodes.

- Strict DAG validation, deterministic execution, short-circuit semantics, fail-fast behavior and configurable node fallback.

- Versioned input/output schemas, sensitivity metadata and compatibility management.

- Dynamic risk classification and configurable multi-tier approval.

- Immutable executable artifacts, publication, rollback, Shadow and deterministic sticky Canary rollout.

- Distributed runtime synchronization with bounded eventual consistency.

- REST and gRPC Data Plane APIs, version pinning and atomic snapshot execution.

- Full Decision Execution Tree trace with sensitive-data protection and tiered retention.

- Enterprise audit, governance evidence and deployment convergence visibility.

### 2.2 Explicitly Out of Scope

- BPMN/business process orchestration, human-task inboxes, timers, long-running workflow state and compensation transactions.

- AI/ML black-box decisioning or non-deterministic decision models.

- Direct cross-tenant resource sharing.

- Direct cross-workspace Decision/Schema references; shared logic must be published as a versioned Tenant-level Shared Library.

- Mandating a specific event broker, cache technology, database, CQRS implementation or DMN engine in the SRS.

### 2.3 Superseded B2 Constraints

| B2 item | B3 disposition |
| --- | --- |
| One request evaluates one Rule | Superseded by Decision Graph execution. |
| Simple internal RBAC | Superseded by enterprise tenant/workspace scoped access model. |
| Fixed Maker-Checker approval | Superseded by dynamic risk matrix + multi-tier/quorum approval. |
| Basic Matched Row trace | Superseded by full Decision Execution Tree. |
| REST-only MVP acceptance | Extended to REST + gRPC. |
| Draft -> In Review -> Active as single lifecycle | Refined into Governance lifecycle and Deployment lifecycle. |

