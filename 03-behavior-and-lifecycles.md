# Behavior, lifecycles and failure semantics

Authority: [SRS functional requirements](baseline/08-7-functional-requirements.md), [lifecycles](baseline/10-9-lifecycle-and-state-semantics.md), [runtime semantics](baseline/11-10-runtime-and-consistency-semantics.md), [failure semantics](baseline/15-14-error-and-failure-semantics.md). Detailed interactions are preserved in the activity, sequence, communication and state source snapshots.

## Administration and modeling

Administrators manage tenant/workspace hierarchy, scoped memberships and roles, API credential issuance/revocation and shared-library publication. Library versions are immutable; decisions may reuse them through exact tenant-level version references. Direct references across workspaces and access across tenants are prohibited.

An authorized author creates or edits a draft decision, graph and versioned schemas. Validation rejects cycles and identifies contract incompatibilities. Schemas specify name, type, required/optional status and `is_sensitive`. Sandbox execution uses valid draft content without production effects. The current request must be authorized even if the actor previously had permission to edit the same draft.

Graph execution follows dependency order, may parallelize independent branches while retaining deterministic semantics, and skips inactive branches. Node errors fail fast unless an eligible node has a valid typed fallback for the qualifying exception. A fallback is part of modeled behavior and must be visible in execution evidence.

## Governance

Submission calculates risk from change scope, breaking schema changes and the previous 30 days of production traffic. The maker cannot self-declare a lower tier. An authorized approver may increase risk, never decrease it.

| Tier | Required approval |
| --- | --- |
| 1 | One Domain Approver |
| 2 | Sequential Domain Peer Review, then Workspace Owner |
| 3 | Quorum including both Domain Owner AND Compliance Officer |

The maker is excluded from every approval role for that release. Approval/rejection evidence is immutable and attributable, including actor, stage, decision, timestamp and applicable reason/comment. Only a release satisfying its policy is eligible for production delivery.

Governance is `Draft → In Review → Approved`, with rejection returning the candidate to Draft. Approval alone does not mean the version serves all production traffic. Review-attempt identity and mutable candidate revisions must be reconciled with immutable historical evidence; alternative proposed lifecycles must not erase the approved reject-to-Draft rule.

## Build and delivery

Build produces an immutable executable artifact with exact decision, dependency, schema, library and integrity metadata. Delivery supports `Approved → Shadow and/or Canary → Active → Superseded/Archived`. Shadow and Canary may coexist. A candidate can be stopped before Active without changing its immutable artifact.

Shadow mirrors production input into an approved candidate, records differences from Active and never replaces the production response. Canary routes actual production traffic to a candidate using deterministic sticky subject-key mapping and optionally approved attribute/claim cohorts. A conceptual percentage rule is `Hash(subjectKey) mod 100 < CanaryPercentage`; the exact algorithm remains an ADR/API-contract decision.

Promotion changes desired Active state. Rollback points desired Active at an eligible prior approved immutable version; it does not clone or modify that version. Publish/promotion/rollback evidence includes actor, from/to versions, timestamp and applicable reason.

## Distribution and convergence

Desired-state changes notify active runtime nodes. Nodes fetch/load/validate artifacts and expose observed loaded and eligible state. All active nodes must converge within two seconds from publication-event emission. In-progress executions retain their original snapshot. Failed artifacts must not serve requests; load failures and lag are observable while an existing eligible artifact can continue serving.

During the bounded convergence interval, nodes may temporarily hold different eligible Active versions. This is allowed by the chosen consistency model; it does not permit mixed versions within a single execution.

## Evaluation

1. Receive REST/gRPC evaluation with scoped credential, input, subject/cohort context and optional exact version pin.
2. Authorize access and bind an eligible atomic snapshot at admission, including schemas and dependencies.
3. For a pin, use the exact requested eligible/available version or fail explicitly. REST uses HTTP 412; gRPC uses a documented equivalent precondition error. Never silently substitute Active.
4. Without a pin, use the latest Active version currently loaded and eligible on the serving node, subject to configured rollout behavior.
5. Validate input against the selected snapshot's schema, evaluate active graph branches, apply only valid configured fallbacks and produce the outcome.
6. Return result and execution identifier on success. Version/trace metadata exposure depends on the API contract and authorization. Capture protected evidence through a safe, observable path.

Identical executable snapshot and input/context must produce deterministic rule evaluation. A publication arriving midway cannot change nodes, schemas, library versions or dependencies of that execution.

## Evidence and historical explanation

Record evaluated nodes, activated branches, relevant intermediate values, final outcome and fallback use. Protect sensitive fields before persistence. Hot storage keeps full trees; long-term storage keeps the required immutable metadata and approval/release reference. Query historical evidence by ExecutionID using the recorded version, not today's Active version. Access and export are scoped and auditable.

Trace backpressure/failure cannot silently change the business decision result. Error handling is observable and policy-controlled. The sources do not settle every queue overflow, retry, loss-prevention or fail-open/fail-closed detail.

## Failure outcomes

| Condition | Required behavior |
| --- | --- |
| Invalid input | Protocol-appropriate client error before decision evaluation |
| Cyclic graph | Validation/build rejection; cannot publish |
| Node failure, no valid fallback | Fail fast with attributable error |
| Qualifying failure with valid fallback | Use typed fallback and record it |
| Unavailable/ineligible pinned version | REST 412 / equivalent gRPC precondition failure |
| Control Plane unavailable | Keep serving already-loaded eligible artifacts |
| Delayed propagation | Keep eligible artifact available and expose lag |
| Bad integrity/load | Do not serve failed artifact; report non-convergence/unhealthy state |
| Trace degradation | Observable, policy-controlled handling without silently changing result |

## Additional recovered state proposals

The [state attachment](memory/attachments/2cb03736-48a8-4eb3-a940-5a7e2f8fcaaf.md) separates Decision, Decision Version, Validation, Review, Approval, Test, Artifact Build, Release, Promotion, Deployment, per-instance sync, Rollout, Canary, Shadow, Runtime Artifact, Execution Request/Result, Audit, Webhook, Import, Export, Credential, Access Binding and Automation lifecycles. [State register](registers/proposed-states.md) preserves its aggregate/state table. This expands the design vocabulary; it is not evidence that these states were approved or implemented.
