# Conflicts, evidence gaps and open decisions

This collection preserves disagreements without silently resolving them into new requirements. The SRS is the declared approved baseline; later catalog/state material retains its explicit proposed status.

## Issues found in the collected evidence

| Issue | Source evidence | Interpretation for reuse |
| --- | --- | --- |
| Conflicting UC identifiers | SRS `UC-01` means tenant/workspace management; earlier candidate `UC-01` means project creation | Always qualify IDs by catalog; no automatic numeric mapping |
| Product naming varies | SRS says Business Decision Management Platform; current user naming says Business Rule Management Platform | Use current display name while preserving the SRS's enterprise decision scope |
| Activity catalog mismatch | Activity README explicitly retains the restored SRS IDs, not the 177-item catalog | Do not claim completed traceability between these families |
| Review report contains both findings and blanket completion claims | COMET audit retains F-01–F-20 and later claims all P1/P2 resolved, 49 sources checked/rendered | Treat as historical claims requiring fresh evidence, not current certification |
| Deployment state source still has guarded initial transitions | `state-diagrams/03_Deployment.puml` has three `[*]` transitions inside TestingCandidate with guards | Conflicts with the same file/audit's claimed removal of initial guards; requires a later semantic review |
| Immutable version wording versus rejection | Conceptual entity note says permanently frozen upon submission/approval; SRS rejection returns candidate to Draft | Specify decision version, candidate revision and review-attempt identity before adopting this wording |
| Concrete technology without ADR evidence | Deployment source names Java JARs, PostgreSQL/JDBC, S3 APIs and specific ports; task source sets 500 ms heartbeat | These are design proposals, not confirmed SRS constraints |
| Generic sub-10 ms labels | Task/deployment sources label responses/evaluation as sub-10 ms | Use exact protocol-specific percentile targets and benchmark conditions from SRS; do not generalize gRPC p95 to every request |
| Proposed runtime actor boundary | Earlier 201-item attachment lists Decision Runtime Node as external; later catalog says runtime is internal | Preserve earlier claim as historical; current whole-system boundary treats runtime as internal |
| Expanded state proposals overlap confirmed rules | State attachment marks a broad set proposed, including multi-approver details; SRS already confirms tiered/quorum approval | Keep additional states proposed without downgrading confirmed SRS approval rules |
| State Draw.io not present | Recovered state conversation contains a creation plan; current workspace has no state `.drawio` | Preserve the source attachment; do not report the planned artifact as delivered |
| Archived/Superseded design detail | SRS names both; diagram adds expiry/cold-storage transitions | Do not infer artifact-retention or deletion policy directly from trace/ledger retention ranges |
| Older top-level count inconsistent | Earlier attachment heading says 15, list and conclusion say 19 | Preserve raw text, label discrepancy, avoid citing 15 as verified |

Sources: [audit](sources/workspace/diagram-review/COMET_UML_Audit.md), [deployment state](sources/workspace/state-diagrams/03_Deployment.puml), [conceptual entity source](sources/workspace/class-diagrams/00_Conceptual_Entity_Model.puml), [physical deployment](sources/workspace/deployment-diagrams/01_RuleSphere_Deployment.puml), [task view](sources/workspace/concurrent-task-diagrams/01_Concurrent_Task_Architecture.puml), [memory](memory/README.md).

## Approved ADR backlog

| ID | Decision still to make |
| --- | --- |
| ADR-001 | Executable decision representation / DMN adoption level |
| ADR-002 | Distribution backbone |
| ADR-003 | Runtime artifact cache and eviction strategy |
| ADR-004 | Control Plane persistence / CQRS boundaries |
| ADR-005 | Trace ingestion and hot/cold storage architecture |
| ADR-006 | Physical tenant isolation model |
| ADR-007 | Stable Canary hash and cohort expression model |
| ADR-008 | Schema compatibility model and registry implementation |
| ADR-009 | Identity federation and enterprise authentication |
| ADR-010 | Data Plane HA topology and SLO measurement |

Exact drivers: [ADR register](registers/adr-backlog.csv). These are solution-space choices; the SRS states they do not block its requirements sign-off.

## Details not settled by available sources

Precise risk thresholds/weights; complete schema compatibility rules; scripted-expression language and sandbox limits; pin/Canary precedence and missing-subject-key handling; active-node membership during failures; artifact cache eligibility/eviction and rollback retention; queue capacity/overflow and trace delivery guarantees; precise endpoint/protobuf schemas; detailed role/permission matrix; SLO observation window; selected retention values; and full mapping of proposed catalog items to approved requirements need further specification or source confirmation.

These are identified gaps, not permission to weaken B3 invariants or invent product behavior. The knowledge collection verifies extraction, source preservation and counts. It does not establish production readiness, implementation security, benchmark success or full UML compliance.
