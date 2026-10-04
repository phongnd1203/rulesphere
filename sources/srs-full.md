# SRS v1.0 Final — extracted source

Source: `RuleSphere_SRS_v1.0_Final.docx`. Tables and text extracted from DOCX; layout is not reproduced.

RuleSphereSoftware Requirements SpecificationEnterprise Business Decision Management Platform

| Document | Value |
| --- | --- |
| Document ID | RS-SRS-001 |
| Version | 1.0 Final |
| Baseline | B3 - Sponsor Sign-off |
| Status | FINAL / APPROVED REQUIREMENTS BASELINE |
| Date | 29 September 2026 |
| Primary audience | Project Sponsor, BA/SA, Solution Architects, Development, QA, Security, Compliance |
| Language | Vietnamese (technical terms retained in English where precise) |

Purpose: xác định đầy đủ yêu cầu phần mềm, ranh giới, hành vi, NFR và các architectural constraints của RuleSphere. Tài liệu này mô tả WHAT/MUST; các lựa chọn công nghệ chi tiết phải được quyết định qua ADR và phải trace về requirement/NFR tương ứng.

## Document Control

| Version | Status | Summary |
| --- | --- | --- |
| 0.1 | Draft | MVP BRMS baseline: atomic rules, simple governance. |
| 0.2 | Superseded draft | Enterprise scope introduced: Decision Graph, distributed Data Plane, enterprise governance. |
| 1.0 | Final | B3 Sponsor decisions AQ-01..AQ-06 and NFR guardrails incorporated. |

### Requirement Status Vocabulary

| Tag | Meaning |
| --- | --- |
| [Confirmed] | Sponsor-approved requirement/constraint/decision. |
| [Proposal] | Design recommendation; not mandatory unless later approved. |
| [Assumption] | Temporary premise requiring validation. |
| [Superseded] | Earlier baseline decision replaced by B3. |
| [Out of Scope] | Explicitly excluded from RuleSphere scope. |

## 1. Introduction

### 1.1 Purpose

RuleSphere is specified as an enterprise-grade Business Decision Management Platform that enables deterministic business decisions to be modeled, composed, governed, safely delivered, executed at low latency, and reconstructed for audit/compliance.

### 1.2 Business Problem Statement

Organizations with frequently changing policies face slow time-to-market because business decisions are embedded in application code, stored procedures and configuration, and therefore depend on software release cycles. At enterprise scale, decision logic is also composed from multiple dependent rules/contracts, executed across distributed infrastructure, and governed by multiple organizational and regulatory stakeholders. Without a unified platform, organizations face fragmented logic, inconsistent runtime state, governance risk, insufficient explainability and integration coupling.

### 1.3 Product Vision

RuleSphere shall provide a Control Plane for Decision Management, a Distribution/Delivery Plane for immutable artifact delivery and safe rollout, and a stateless Data Plane for deterministic REST/gRPC execution. The platform shall support multi-tenant isolation, composable DAG-based decisions, risk-based governance, schema evolution, shadow/canary release, distributed convergence and auditable execution evidence.

### 1.4 Business Outcomes

| ID | Outcome | Intent |
| --- | --- | --- |
| BO-01 | Reduce decision change lead time | Business policy changes shall not require consumer application redeployment. |
| BO-02 | Increase business autonomy | Domain experts can model, validate and test decisions using governed tooling. |
| BO-03 | Reduce operational blast radius | Risk-based approval, shadow/canary and rollback control production change. |
| BO-04 | Provide auditability | Historical decisions can be reconstructed from immutable version and execution evidence. |
| BO-05 | Enterprise runtime viability | Distributed Data Plane meets latency, throughput, availability and convergence guardrails. |

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

## 3. System Goals

| ID | Goal | Description |
| --- | --- | --- |
| G1 | Business Decision Autonomy | Model/test governed decisions without consumer release. |
| G2 | Enterprise Governance | Control decision change using risk-aware approval and separation of duties. |
| G3 | Decision Composition | Compose deterministic finite decisions from reusable decision nodes. |
| G4 | Explainability & Compliance | Reconstruct why and how a decision was produced. |
| G5 | High-performance Distributed Execution | Execute decisions at enterprise latency/throughput scale. |
| G6 | Safe Decision Delivery | Publish, shadow, canary, promote and rollback safely. |
| G7 | Tenant & Security Isolation | Prevent unauthorized cross-tenant/workspace access. |
| G8 | Contract Evolution | Version and evolve data contracts with compatibility controls. |
| G9 | Reliability & Fault Tolerance | Keep Data Plane serving through node/control-plane failures. |
| G10 | Integration Interoperability | Provide stable REST/gRPC integration contracts. |

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

## 6. Core Use Case Catalog

| ID | Use Case | Primary actor | Precondition | Postcondition |
| --- | --- | --- | --- | --- |
| UC-01 | Manage Tenant & Workspaces | Enterprise Admin | Authenticated enterprise admin | Tenant/workspace configuration updated. |
| UC-02 | Manage Membership & Roles | Enterprise Admin | Tenant/workspace exists | Scoped role assignments updated. |
| UC-03 | Manage API Credentials | Enterprise Admin | Workspace exists | Credential issued/revoked with scope. |
| UC-04 | Publish Shared Library Asset | Authorized owner | Validated reusable asset | Immutable version becomes available tenant-wide. |
| UC-05 | Create/Edit Decision | Decision Author | Workspace author permission | Draft Decision Version stored. |
| UC-06 | Model Decision Graph | Decision Author | Draft exists | Valid node/dependency model stored. |
| UC-07 | Define/Version Schema | Decision Author | Draft/schema permission | Schema Version stored. |
| UC-08 | Validate Graph & Contracts | Decision Author | Draft graph/schema exists | Validation result produced; cycles/breaking issues identified. |
| UC-09 | Sandbox Execute | Decision Author | Executable draft is valid | Simulation result and trace produced without production effect. |
| UC-10 | Submit Release | Decision Author | Candidate passes required validation | Release enters governance. |
| UC-11 | Calculate Risk Tier | System | Release submitted | Risk tier calculated from change scope, compatibility and 30-day traffic. |
| UC-12 | Approve/Reject Release | Approver(s) | Required approval task exists | Approval evidence recorded; quorum progresses or release rejected. |
| UC-13 | Overrule Risk Upward | Approver | Calculated tier exists | Tier increased; never decreased. |
| UC-14 | Build Executable Artifact | System | Release satisfies governance | Immutable artifact produced and integrity metadata recorded. |
| UC-15 | Shadow Deploy | Approver/Release Manager | Approved artifact exists | Candidate evaluates mirrored traffic without affecting response. |
| UC-16 | Analyze Shadow Diff | Authorized user | Shadow data exists | Outcome differences are queryable. |
| UC-17 | Canary Deploy | Approver/Release Manager | Eligible candidate exists | Sticky/cohort routing activates candidate for controlled traffic. |
| UC-18 | Promote Active | Approver/Release Manager | Release meets policy | Candidate becomes desired Active version. |
| UC-19 | Rollback | Approver/Release Manager | Eligible prior version exists | Desired Active pointer switches to prior immutable version. |
| UC-20 | Synchronize Runtime Fleet | System | Publish/rollback event emitted | Active nodes converge to desired artifact within SLA. |
| UC-21 | Evaluate Decision REST | Consumer App | Valid credential + request contract | Decision result returned. |
| UC-22 | Evaluate Decision gRPC | Consumer App | Valid credential + request contract | Decision result returned. |
| UC-23 | Evaluate Pinned Version | Consumer App | Requested version supplied | Exact version executes or 412 returned. |
| UC-24 | Capture Execution Trace | System | Auditable execution occurs | Masked trace/ledger evidence persisted asynchronously/safely. |
| UC-25 | Explain Historical Decision | Authorized user | Execution retained | Decision/version/tree evidence returned per authorization. |
| UC-26 | Inspect Audit Evidence | Compliance/Security Auditor | Authorized scope | Governance/deployment/security evidence displayed/exportable. |
| UC-27 | Observe Fleet Convergence | Authorized operator/admin | Deployment in progress | Per-fleet desired/loaded state visible. |

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

## 8. Non-Functional Requirements

| ID | Category | Requirement |
| --- | --- | --- |
| NFR-PERF-001 | Performance | gRPC Data Plane latency shall achieve p95 < 10 ms and p99 < 25 ms for Decision Graph <=10 nodes and payload <=10 KB under the approved benchmark profile. |
| NFR-PERF-002 | Performance | REST Data Plane latency shall achieve p95 < 25 ms and p99 < 50 ms for Decision Graph <=10 nodes and payload <=10 KB under the approved benchmark profile. |
| NFR-PERF-003 | Throughput | A Runtime node shall sustain >=2,000 RPS on baseline hardware of 4 vCPU and 8 GB RAM under the benchmark workload. |
| NFR-CONS-001 | Consistency | 100% of active Runtime nodes shall converge to the desired published/rollback artifact within <=2 seconds measured from publication event emission. |
| NFR-AVAIL-001 | Availability | The production Data Plane shall target 99.99% availability, measured independently of Control Plane uptime. |
| NFR-TRACE-001 | Performance | Enabling Full Trace Tree capture shall add <=10% latency penalty under the defined benchmark workload. |
| NFR-REL-001 | Fault tolerance | Control Plane unavailability or Control-to-Data network partition shall not stop Data Plane execution using already-loaded eligible artifacts. |
| NFR-REL-002 | Consistency | No execution may mix Decision/dependency versions from different snapshots. |
| NFR-SEC-001 | Isolation | Cross-tenant data/access leakage shall be prohibited across management, runtime and audit paths. |
| NFR-SEC-002 | Data protection | Sensitive trace fields shall not be persisted in plaintext. |
| NFR-AUD-001 | Auditability | Governance, release, rollback and security-sensitive administrative actions shall produce immutable attributable audit evidence. |
| NFR-OBS-001 | Observability | The platform shall expose sufficient telemetry to identify runtime health, artifact load failures, convergence lag and trace-persistence failures. |
| NFR-SCALE-001 | Scalability | The Data Plane architecture shall support horizontal scaling by adding stateless Runtime nodes without changing Decision semantics. |
| NFR-INT-001 | Interoperability | REST and gRPC contracts shall be versioned and documented so consumer integrations can evolve under controlled compatibility rules. |

### 8.1 Measurement Notes

- Latency metrics exclude uncontrolled public-Internet latency; benchmark topology, serialization, TLS mode, trace mode and client/server placement shall be recorded with test results.

- Convergence <=2 seconds is measured from publication-event emission to all active Runtime nodes reporting the desired artifact loaded/eligible.

- 99.99% availability applies to the Data Plane service boundary; the exact observation window and excluded planned-maintenance policy shall be defined in the operational SLO specification.

- Retention values are policy ranges approved by Sponsor. Deployment configuration must choose a value inside the range; the SRS does not invent one universal retention period.

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

## 10. Runtime and Consistency Semantics

### 10.1 Atomic Snapshot

At request admission, Runtime resolves one eligible Decision snapshot. All graph nodes, schemas, dependency artifacts and Shared Library versions for that execution are bound to that snapshot. Mid-request publication events must not alter the executing snapshot.

### 10.2 Version Pinning

REST consumers may supply X-Decision-Version; gRPC exposes an equivalent request field. If the exact version is unavailable/ineligible on the serving Data Plane, the request must fail explicitly rather than silently falling back. REST uses 412 Precondition Failed.

### 10.3 Unpinned Requests During Convergence

Because B3 explicitly chooses bounded eventual consistency and prioritizes Data Plane availability, during the <=2-second convergence window different nodes may temporarily hold different latest eligible Active versions. An unpinned request executes the latest Active version currently loaded on its serving node. Consumers requiring strict version repeatability must use version pinning. Atomic Snapshot guarantees internal consistency within each execution.

### 10.4 Canary Routing

Percentage Canary routing shall be sticky and deterministic using a consumer-provided subject key. A stable mapping equivalent to Hash(subjectKey) mod 100 < CanaryPercentage shall be used conceptually; the exact hash algorithm is an ADR/API-contract concern but must preserve stable routing for a fixed rollout configuration. Targeted cohorts may additionally route by approved attributes such as staff cohort or region.

## 11. Audit, Privacy and Retention

| Store tier | Content | Retention baseline | Purpose |
| --- | --- | --- | --- |
| Hot Trace | Full masked/tokenized Execution Trace Tree | Configurable 30-90 days | Debug, dispute, near-term explainability |
| Compliance Ledger | ExecutionID, DecisionVersion, InputHash, Output, MatchedNodeIDs, Timestamp, approval/release evidence reference | Configurable 5-7 years | Legal/regulatory audit |

The Sponsor example 'ApprovedByTicket' is normalized in this SRS as an approval/release evidence reference because the existence and identifier format of an external ticketing system has not been mandated. If a future integration standardizes a ticket ID, that field can be bound through an API/ADR without changing the audit intent.

### 11.1 Sensitive Data

Schema fields marked is_sensitive=true must be protected before persistence. The protection mechanism may be masking, tokenization or hashing according to data classification and retrieval requirements. Plaintext sensitive values are prohibited in persisted execution traces.

## 12. External Interface Requirements

### 12.1 Management Interfaces

Control Plane shall provide authenticated management interfaces sufficient for tenant/workspace administration, decision/schema authoring, validation, governance, release management, audit queries and deployment convergence inspection. Exact UI layout is not prescribed by this SRS.

### 12.2 Runtime REST

REST shall support decision evaluation, scoped authentication, subject/cohort routing context, optional X-Decision-Version pinning, contract validation, explicit error semantics and execution identifiers.

### 12.3 Runtime gRPC

gRPC shall provide semantically equivalent evaluation capabilities to REST, including version pinning and precondition failure semantics, while allowing protocol-specific status/error representation.

### 12.4 Publication/Distribution Interface

Control Plane/Delivery Plane shall emit or otherwise distribute desired-state changes to Data Plane nodes. The SRS requires bounded convergence and zero-restart delivery; it does not mandate Kafka, Redis or another specific broker.

## 13. Architecture Constraints

| ID | Constraint |
| --- | --- |
| AC-01 | Responsibilities shall be separated into Decision Management (Control Plane), Decision Delivery/Distribution, and Decision Execution (Data Plane). |
| AC-02 | Published runtime artifacts shall be immutable. |
| AC-03 | Production Runtime nodes shall be horizontally scalable and stateless with respect to client sessions/long-running process state. |
| AC-04 | Runtime shall use local/in-memory access to eligible artifacts on the critical execution path; Control Plane must not be a synchronous dependency for normal evaluation. |
| AC-05 | Artifact synchronization shall be event/desired-state driven or use an equivalent mechanism that satisfies <=2s convergence and no-restart delivery. |
| AC-06 | Decision composition shall remain synchronous deterministic DAG-based decision orchestration and shall not expand into BPM/long-running workflow orchestration. |
| AC-07 | Technology choices such as Kafka, Redis, CQRS, a DMN engine, database product, reverse proxy or cache product require ADR justification and are not fixed by this SRS. |

## 14. Error and Failure Semantics

| Condition | Required behavior |
| --- | --- |
| Invalid input contract | Reject before decision evaluation with protocol-appropriate client error. |
| Cycle detected | Reject validation/build; artifact shall not become publishable. |
| Node computation failure, no fallback | Fail-fast execution with attributable error. |
| Node computation failure, valid fallback | Use configured fallback; record fallback use in trace. |
| Pinned version unavailable/ineligible | REST 412; gRPC equivalent precondition error. |
| Control Plane unavailable | Data Plane continues using loaded eligible artifacts. |
| Publication propagation delayed | Existing eligible artifact continues serving; convergence lag is observable. |
| Trace persistence degraded | Decision outcome must not be silently changed; degradation/failure is observable and governed by operational policy. |
| Artifact integrity/load failure | Node shall not serve the failed artifact; report unhealthy/non-converged state. |

## 15. Requirements Traceability Matrix

| Problem/Need | Goals | Use Cases | Requirement families |
| --- | --- | --- | --- |
| BP-01 Slow release dependency | G1,G6,G10 | UC-05,09,10,15-23 | FR-DM-001; FR-REL-001..011; FR-RUN-001..010 |
| BP-02 Fragmented/unexplainable decisions | G3,G4,G8 | UC-06-08,24-26 | FR-DM-002..008; FR-SCH-*; FR-AUD-* |
| BP-03 Operational change risk | G2,G6,G9 | UC-11-20,27 | FR-GOV-*; FR-REL-*; FR-DIST-* |
| Enterprise isolation risk | G7 | UC-01-04,26 | FR-TEN-*; FR-SEC-* |
| Distributed consistency risk | G6,G9 | UC-18-23,27 | FR-DIST-*; FR-RUN-005..008; NFR-CONS-001 |
| Regulatory/audit obligation | G2,G4,G7 | UC-12,24-26 | FR-GOV-008; FR-AUD-*; NFR-AUD-001 |

## 16. Verification and Acceptance Strategy

| Area | Verification approach | Key acceptance evidence |
| --- | --- | --- |
| DAG correctness | Automated structural validation tests | Cycle rejected; valid DAG accepted. |
| Determinism/snapshot | Repeatability + concurrent publish test | No mixed versions inside one execution. |
| Governance | Role/risk/quorum scenario tests | Maker excluded; tiers enforced; upward-only override. |
| Tenant isolation | Authorization and adversarial isolation tests | No cross-tenant access/data leakage. |
| Shadow | Production-mirroring test | Candidate result recorded; production response unchanged. |
| Canary | Stable-subject routing test | Same subject maps consistently under fixed rollout config. |
| Version pinning | REST/gRPC contract tests | Exact version or explicit precondition failure. |
| Convergence | Distributed publish/rollback load test | 100% active nodes converge <=2s. |
| Performance | Benchmark on 4 vCPU/8GB node | Meets REST/gRPC latency and >=2,000 RPS/node. |
| Availability | Failure/partition tests | Data Plane continues without Control Plane; SLO measurement supports 99.99% target. |
| Trace overhead | A/B benchmark trace off/on | <=10% latency penalty. |
| Privacy | Trace inspection/security test | is_sensitive values absent as plaintext. |
| Audit retention | Policy/configuration tests | Hot and ledger retention policies enforce approved ranges. |

## 17. Open Implementation Decisions (ADR Backlog)

The problem space is signed off; the following are solution-space decisions and do not block SRS v1.0. Each shall be resolved through an ADR against the requirements above.

| ADR Candidate | Decision to make | Primary drivers |
| --- | --- | --- |
| ADR-001 | Executable decision representation / DMN adoption level | G3, performance, interoperability |
| ADR-002 | Distribution backbone: Kafka vs Redis-class mechanism vs alternative | <=2s convergence, availability, operations |
| ADR-003 | Runtime artifact cache and eviction strategy | latency, pinning, rollback eligibility |
| ADR-004 | Control Plane persistence/CQRS boundaries | auditability, scale, consistency |
| ADR-005 | Trace ingestion and hot/cold storage architecture | <=10% overhead, retention, compliance |
| ADR-006 | Tenant isolation physical model | security, cost, scalability |
| ADR-007 | Canary stable hash algorithm and cohort expression model | determinism, interoperability |
| ADR-008 | Schema compatibility model and registry implementation | G8, integration safety |
| ADR-009 | Identity federation and enterprise authentication | G7, enterprise integration |
| ADR-010 | Data Plane HA topology and SLO measurement | 99.99%, fault tolerance |

## 18. Final Baseline Statement

This SRS v1.0 is the final requirements baseline derived from Sponsor-approved Baseline B3. It supersedes earlier MVP-specific simplifications where explicitly noted. Future architecture and implementation decisions shall not weaken the confirmed invariants, NFR guardrails or system boundaries without formal change control.

The final product boundary remains: RuleSphere is an enterprise deterministic Business Decision Management Platform. It orchestrates decisions, not long-running business processes; it governs and executes explainable rules/decision graphs, not AI/ML black-box decisions.

## Appendix A - Glossary

| Term | Definition |
| --- | --- |
| Control Plane | Authoring, governance, schema, release and administrative responsibilities. |
| Distribution/Delivery Plane | Artifact publication, rollout and fleet convergence responsibilities. |
| Data Plane | Low-latency stateless decision execution. |
| Decision Graph | Strict DAG of decision nodes evaluated in one synchronous context. |
| Atomic Snapshot | Exact immutable set of Decision/dependency/schema versions used for one execution. |
| Shadow | Candidate evaluation on mirrored real traffic without affecting production response. |
| Canary | Controlled real production routing to a candidate version. |
| Sticky Subject Key | Business identifier used for deterministic cohort assignment. |
| Risk Tier | System-calculated release risk classification driving approval requirements. |
| Quorum | Required set of independent approvals for a release. |
| Shared Library | Immutable tenant-level reusable asset for controlled cross-workspace reuse. |
| Bounded Eventual Consistency | Nodes may temporarily differ but must converge within a defined maximum interval. |

## Appendix B - Requirement Counts

| Category | Count |
| --- | --- |
| Functional Requirements | 64 |
| Non-Functional Requirements | 14 |
| Architecture Constraints | 7 |
| Core Use Cases | 27 |
| System Goals | 10 |

## DOCX supplementary part: word/header1.xml

RuleSphere - Software Requirements Specification (SRS) v1.0
