# Domain model and architecture

Sources: [SRS domain](baseline/06-5-conceptual-domain-model.md), [architecture constraints](baseline/14-13-architecture-constraints.md), [class models](sources/workspace/class-diagrams/README.md), [component source](sources/workspace/component-diagrams/01_RuleSphere_Components.puml), [task source](sources/workspace/concurrent-task-diagrams/01_Concurrent_Task_Architecture.puml), [deployment source](sources/workspace/deployment-diagrams/01_RuleSphere_Deployment.puml).

## Core concepts

| Concept | Meaning and constraints |
| --- | --- |
| Tenant | Top-level security and ownership boundary |
| Workspace | Tenant-owned business/domain boundary; isolated by default |
| Shared Library version | Immutable tenant-level asset; exact versions enable controlled cross-workspace reuse |
| Decision | Named workspace-owned business decision |
| Decision Version | Versioned content identifying exact graph, schemas and dependencies; approved/published snapshots immutable |
| Decision Graph | Strict DAG executed in one synchronous context |
| Decision Node | Decision Table, Decision Tree, Scripted Expression or Rule Set |
| Schema Version | Input/output contract with types, requiredness and sensitivity metadata |
| Governance Policy | Risk calculation and required approvals |
| Release | Governed candidate associated with deployment and rollout policy |
| Executable Artifact | Validated/compiled immutable runtime representation with integrity/version metadata |
| Execution / Atomic Snapshot | One evaluation bound to a fixed decision, graph, schemas, dependencies and library versions |
| Execution Trace Tree | Protected evidence of evaluated nodes, branches, intermediate and final outcomes |

## Detailed design concepts in the class sources

Administration adds User, Membership, RoleAssignment, Role, Permission, AccessScope, ApiCredential and AuthorizationService. Modeling adds NodeDependency, TypedFallback, SchemaField, LibraryReference, ValidationResult, DecisionValidator, SandboxService and SimulationResult. Governance adds RiskAssessment, immutable RiskOverride, ApprovalStage, ApprovalEvidence, ArtifactBuilder and ArtifactManifest.

Delivery distinguishes Deployment, RolloutPolicy, DesiredActiveState, immutable PublicationEvent, RuntimeNode, LoadedArtifact, DistributionService and ShadowComparison. Runtime adds protocol adapters, EvaluationRequest/Response, EvaluationService, SnapshotResolver, LocalArtifactStore, GraphExecutor, ApiContract and ContractDiscovery. Evidence adds TraceNode, ComplianceRecord, AuditEvent, RetentionPolicy, SensitiveDataProtector, TraceCaptureService, EvidenceQueryService and FleetConvergenceView.

Attributes, operations, cardinalities and associations remain available verbatim in the six detailed class sources. These design refinements are not all independent SRS requirements. In particular UUID formats, signatures, SHA-256 fields, subscription tiers and specific storage types need their own design authority.

## Three planes

| Plane | Responsibilities | Runtime relationship |
| --- | --- | --- |
| Control / Decision Management | Administration, authoring, schema validation, sandbox, governance, release/build management | Not a synchronous dependency of normal evaluation |
| Delivery / Distribution | Desired-state publication, immutable artifact distribution, rollout and convergence | Loads and validates new artifacts without node restart |
| Data / Decision Execution | REST/gRPC adapters, local snapshot selection, deterministic graph evaluation, trace handoff | Stateless regarding client sessions and long-running business state; horizontally scalable |

The normal serving path reads eligible artifacts locally/in memory. Losing the Control Plane or its connection must not stop already-loaded eligible decisions. New artifacts must be loaded and validated before serving. Desired state and observed node state are separate concepts; publication does not prove fleet convergence.

## Component and task proposals

The component view supplies management, authoring, validation, governance, builder, distribution, publication, REST/gRPC, snapshot, executor, trace and storage interfaces. Evidence storage separates hot trace trees from compliance metadata. The package view groups these responsibilities into the three planes and shared modules.

The task view proposes runtime worker pools, sync listeners, artifact loaders, trace ingestion workers, shadow evaluation workers and convergence heartbeats. Passive objects include local cache, immutable snapshot, trace buffer and shadow queue. Serving should not wait for background shadow evaluation or trace storage I/O; a safe handoff and explicit failure/backpressure policy still need design detail.

The physical view proposes control service hosts, database servers, broker infrastructure, runtime nodes and artifact/evidence stores. Its Java JAR names, PostgreSQL/JDBC, ports, S3 API, SHA-256 and protocol allocations are diagram-level choices, not a signed-off technology stack. Similarly the 500 ms heartbeat and concrete queue structures in the task diagram are proposals. See [open decisions](08-conflicts-and-open-decisions.md).
