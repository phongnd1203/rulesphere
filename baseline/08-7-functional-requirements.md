# SRS source section

Source: `RuleSphere_SRS_v1.0_Final.docx`. Requirements retain their original status; extraction is not a new approval.

## 7. Functional Requirements

| ID | Goal | Use Case | Requirement |
| --- | --- | --- | --- |
| FR-TEN-001 | G7 | UC-01 | The system shall implement a strict Tenant -> Workspace ownership hierarchy. |
| FR-TEN-002 | G7 | UC-01/02 | The system shall enforce hard Tenant isolation for business data, identities/memberships, API credentials and audit records. |
| FR-TEN-003 | G7 | UC-05/06 | Workspace-owned Decisions and Schemas shall be isolated by default from other Workspaces. |
| FR-TEN-004 | G7/G3 | UC-04/06 | The system shall prohibit direct cross-workspace references and shall permit reuse only through versioned immutable Tenant-level Shared Library assets. |
| FR-SEC-001 | G7 | UC-02 | The system shall enforce role and permission checks within Tenant and Workspace scope. |
| FR-SEC-002 | G7/G10 | UC-03/21/22 | Runtime credentials shall be scoped and shall not authorize access to Decisions outside their permitted Tenant/Workspace scope. |
| FR-SEC-003 | G7 | UC-03 | The system shall support credential issuance, revocation and auditable credential lifecycle events. |
| FR-DM-001 | G1/G3 | UC-05 | The system shall allow authorized authors to create and version Decisions within a Workspace. |
| FR-DM-002 | G3 | UC-06 | A Decision shall support a graph composed of Decision Table, Decision Tree, Scripted Expression and Rule Set node types. |
| FR-DM-003 | G3 | UC-06/08 | The Control Plane shall validate that each Decision Graph is a DAG and shall reject cycles before artifact build/publication. |
| FR-DM-004 | G3/G5 | UC-06/21/22 | Runtime shall support topological evaluation and may evaluate dependency-independent branches in parallel while preserving deterministic semantics. |
| FR-DM-005 | G3/G5 | UC-21/22 | Runtime shall short-circuit graph branches that are not activated by decision conditions. |
| FR-DM-006 | G3/G5 | UC-06/21/22 | Node evaluation shall fail-fast by default on contract or computation error. |
| FR-DM-007 | G3/G5 | UC-06/21/22 | Authors shall be able to configure a typed default fallback value per eligible node; when configured, a qualifying node exception shall resolve to the fallback and execution may continue. |
| FR-DM-008 | G3/G4 | UC-06/24 | Graph/node identifiers shall remain traceable across a Decision Version so execution evidence can identify evaluated and matched nodes. |
| FR-SCH-001 | G8 | UC-07 | The system shall maintain versioned input and output schemas for Decisions. |
| FR-SCH-002 | G8 | UC-07 | Schema fields shall support at least name, data type, required/optional semantics and is_sensitive metadata. |
| FR-SCH-003 | G8 | UC-08 | The system shall evaluate schema changes for configured backward/forward compatibility rules and identify breaking changes. |
| FR-SCH-004 | G2/G8 | UC-11 | Schema breaking-change status shall contribute to automatic Risk Tier calculation. |
| FR-SCH-005 | G8/G10 | UC-21/22 | Runtime shall validate request payloads against the schema version bound to the selected Decision Version. |
| FR-SCH-006 | G8/G4 | UC-14/24 | An executable artifact and execution evidence shall identify the exact schema version used. |
| FR-GOV-001 | G2 | UC-10/11 | Submitting a release shall trigger automatic Risk Tier calculation; the author shall not be able to self-declare a lower tier. |
| FR-GOV-002 | G2 | UC-11 | Risk calculation shall consider change scope, schema breaking-change status and the Decision's production traffic frequency over the previous 30 days. |
| FR-GOV-003 | G2 | UC-13 | An authorized Approver may increase a calculated Risk Tier but shall not decrease it. |
| FR-GOV-004 | G2 | UC-12 | Tier 1 releases shall require approval by one Domain Approver. |
| FR-GOV-005 | G2 | UC-12 | Tier 2 releases shall require sequential approval by Domain Peer Review followed by Workspace Owner approval. |
| FR-GOV-006 | G2 | UC-12 | Tier 3 releases shall require quorum including both Domain Owner and Compliance Officer approval. |
| FR-GOV-007 | G2 | UC-12 | The author of a release shall be excluded from every approval role for that release. |
| FR-GOV-008 | G2/G4 | UC-12 | The system shall record immutable approval/rejection evidence including actor, stage, decision, timestamp and supplied reason/comment where applicable. |
| FR-GOV-009 | G2/G6 | UC-12/14 | Only a release satisfying its required approval policy shall be eligible for production delivery. |
| FR-REL-001 | G6 | UC-14 | The system shall produce an immutable executable artifact from a validated and governed Decision Version. |
| FR-REL-002 | G6/G4 | UC-14 | Artifacts shall include integrity/version metadata sufficient to identify the exact Decision, dependencies, schemas and Shared Library versions. |
| FR-REL-003 | G6 | UC-15 | The system shall support Shadow deployment of an approved candidate against mirrored production inputs. |
| FR-REL-004 | G6 | UC-15 | Shadow candidate results shall not alter or replace the production response. |
| FR-REL-005 | G6/G4 | UC-16 | The system shall capture and expose diff analysis between Active and Shadow outcomes. |
| FR-REL-006 | G6 | UC-17 | The system shall support Canary rollout using deterministic sticky Subject-Key routing. |
| FR-REL-007 | G6 | UC-17 | Sticky percentage routing shall deterministically map the same subject key to the same rollout cohort for a fixed rollout configuration. |
| FR-REL-008 | G6 | UC-17 | The system shall additionally support targeted cohort routing based on configured request attributes/claims. |
| FR-REL-009 | G6 | UC-18 | The system shall support promotion of an eligible candidate to desired Active state. |
| FR-REL-010 | G6/G4 | UC-19 | The system shall support rollback by switching desired Active state to an eligible prior immutable version without cloning that version. |
| FR-REL-011 | G6/G4 | UC-18/19 | Publish, promotion and rollback actions shall be auditable with actor, from-version, to-version, timestamp and reason where required. |
| FR-DIST-001 | G6/G9 | UC-20 | The distribution mechanism shall notify active Runtime nodes of publish/rollback desired-state changes without requiring node restart. |
| FR-DIST-002 | G6/G9 | UC-20 | Runtime nodes shall load/validate a new artifact before serving executions from that artifact. |
| FR-DIST-003 | G6/G9 | UC-20/27 | The system shall expose fleet convergence state sufficient to determine desired version and loaded version for active nodes. |
| FR-DIST-004 | G9 | UC-20/21/22 | Loss of Control Plane connectivity shall not prevent a Runtime node from serving already-loaded eligible artifacts. |
| FR-DIST-005 | G9 | UC-20 | The Data Plane shall use bounded eventual consistency for artifact propagation while preserving atomic snapshot execution. |
| FR-RUN-001 | G5/G10 | UC-21 | The Data Plane shall expose a production REST evaluation API. |
| FR-RUN-002 | G5/G10 | UC-22 | The Data Plane shall expose a production gRPC evaluation API. |
| FR-RUN-003 | G5/G9 | UC-21/22 | Runtime execution nodes shall be stateless with respect to client sessions and long-running process state. |
| FR-RUN-004 | G3/G5 | UC-21/22 | A request shall execute a Decision Graph in one synchronous execution context. |
| FR-RUN-005 | G5/G9 | UC-21/22 | An unpinned request shall execute the latest Active version currently eligible and loaded on the serving node. |
| FR-RUN-006 | G5/G9 | UC-21/22/23 | The selected Decision Version and all graph dependencies shall be fixed as one atomic snapshot for the lifetime of an execution. |
| FR-RUN-007 | G10/G9 | UC-23 | Consumers may request an exact Decision Version using the defined REST header or equivalent gRPC request field. |
| FR-RUN-008 | G10/G9 | UC-23 | If the requested pinned version is not eligible/available on the serving Data Plane, REST shall return HTTP 412 Precondition Failed; gRPC shall return a documented semantically equivalent precondition error. |
| FR-RUN-009 | G5 | UC-21/22 | For identical executable snapshot and identical input/context, rule evaluation shall be deterministic. |
| FR-RUN-010 | G5/G4 | UC-21/22 | A successful evaluation response shall include an execution identifier and result; version/trace metadata shall be available according to API contract and authorization. |
| FR-AUD-001 | G4 | UC-24 | The system shall capture a Decision Execution Trace Tree identifying evaluated nodes, activated branches, relevant intermediate outcomes and final outcome. |
| FR-AUD-002 | G4/G7 | UC-24 | Fields marked is_sensitive shall be masked, tokenized or hashed before trace persistence and shall not be stored as plaintext. |
| FR-AUD-003 | G4 | UC-24/25 | Hot trace storage shall retain full trace trees for a configurable policy within the Sponsor-approved 30-90 day range. |
| FR-AUD-004 | G4 | UC-24/26 | Long-term compliance storage shall retain immutable execution metadata for a configurable policy within the Sponsor-approved 5-7 year range. |
| FR-AUD-005 | G4 | UC-24 | Long-term compliance metadata shall include at least ExecutionID, DecisionVersion, InputHash, Output, MatchedNodeIDs, Timestamp and approval/release evidence reference. |
| FR-AUD-006 | G4/G7 | UC-25/26 | Trace and compliance evidence access shall be authorization-scoped and auditable. |
| FR-AUD-007 | G4 | UC-25 | Authorized users shall be able to retrieve retained execution evidence by ExecutionID. |
| FR-AUD-008 | G4/G9 | UC-24 | Trace capture shall be designed so failure or backpressure of trace persistence does not silently change the business decision result; failure handling shall be observable and policy-controlled. |

