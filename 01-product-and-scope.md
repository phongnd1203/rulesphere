# Product, scope and actors

Authority: [SRS sections 1–6 and 18](sources/srs-full.md); naming preference: [recovered history](07-history-and-memory.md). Expanded actor names below come from the [proposed catalog](sources/workspace/use-case-diagrams/drawio-catalog/source-catalog.md).

## Purpose and business need

RuleSphere separates changing business policy from consumer application release cycles. Authors model reusable decisions, validate their contracts, test them, obtain risk-based approvals and deliver immutable executable versions to a distributed runtime. Consumers obtain deterministic results; authorized investigators can reconstruct the executed version and decision path from retained evidence.

The problems are slow policy changes embedded in application code/stored procedures/configuration, fragmented and dependent rules, inconsistent distributed runtime versions, governance risk, weak explainability and integration coupling. The five business outcomes are reduced change lead time, business autonomy, reduced operational blast radius, auditability and enterprise runtime viability.

The ten goals are business decision autonomy, enterprise governance, decision composition, explainability/compliance, high-performance distributed execution, safe delivery, tenant/security isolation, contract evolution, reliability/fault tolerance and integration interoperability. Exact descriptions: [goal register](registers/goals.csv), [business outcomes](registers/business-outcomes.csv).

## Included in B3

Tenant → Workspace isolation; immutable tenant Shared Libraries; deterministic DAGs containing Decision Tables, Decision Trees, Scripted Expressions and Rule Sets; contract versioning and sensitivity metadata; risk classification and multi-tier approval; immutable builds; Shadow, sticky Canary, promotion and rollback; bounded runtime convergence; REST and gRPC execution with exact version pinning and atomic snapshots; full protected execution traces and long-term compliance evidence.

## Excluded from B3

General BPM/business-process orchestration, human-task inboxes, timers for long-running business workflows, compensation transactions, AI/ML black-box or nondeterministic decisions, direct cross-tenant sharing and direct cross-workspace Decision/Schema references. A workflow engine can be a consumer of decisions without moving process ownership into RuleSphere.

The SRS does not select Kafka, Redis, a database, CQRS implementation, DMN engine, proxy or cache product. Technical timers for runtime monitoring are design mechanisms, distinct from excluded business workflow timers.

## Approved actor vocabulary

| SRS ID | Actor | Responsibility |
| --- | --- | --- |
| A01 | Decision Author / Domain Expert | Author, edit, test and submit decisions and schemas |
| A02 | Domain Approver / Decision Owner | Domain approval and upward risk override |
| A03 | Workspace Owner | Workspace governance and Tier-2+ participation |
| A04 | Compliance Officer | Regulated/high-risk approval and compliance review |
| A05 | Enterprise Administrator | Tenant/workspace, membership, credentials and libraries |
| A06 | Security Auditor | Independent access, security and audit inspection |
| A07 | Application Developer / Integrator | Discover contracts and integrate applications |
| A08 | Consumer Application | Evaluate over REST/gRPC with context and optional pin |

The first seven are human roles; A08 is an external system. Release Manager and Authorized Operator labels in diagrams describe authorized role groupings, not new SRS actor IDs. Exact scope and the actor-goal matrix are preserved in [SRS actor section](baseline/05-4-stakeholders-and-actors.md).

## Expanded proposed actor vocabulary

The later catalog has five main actors: Rule / Decision Author; Reviewer / Approver; Platform Administrator; Operations / SRE; Decision Consumer / Client Application. Four supporting actors are Identity Provider / IAM, CI/CD & Automation, Observability Platform and Audit / SIEM.

`Platform User` abstracts the four human main actors. `External System` abstracts Consumer plus the four supporting systems. Consumer remains a main actor. This taxonomy does not imply identical privileges or a shared credential contract. Runtime nodes, distributor and policy engine are internal RuleSphere parts in the current catalog.

## Baseline evolution

B3 supersedes one-rule-per-request, simple internal RBAC, fixed Maker-Checker approval, matched-row-only trace, REST-only acceptance and a single Draft → In Review → Active lifecycle. Their replacements are composed DAGs, tenant/workspace scope, dynamic risk/quorum, full execution trees, REST plus gRPC and separate governance/deployment lifecycles.
