# SRS source section

Source: `RuleSphere_SRS_v1.0_Final.docx`. Requirements retain their original status; extraction is not a new approval.

## 10. Runtime and Consistency Semantics

### 10.1 Atomic Snapshot

At request admission, Runtime resolves one eligible Decision snapshot. All graph nodes, schemas, dependency artifacts and Shared Library versions for that execution are bound to that snapshot. Mid-request publication events must not alter the executing snapshot.

### 10.2 Version Pinning

REST consumers may supply X-Decision-Version; gRPC exposes an equivalent request field. If the exact version is unavailable/ineligible on the serving Data Plane, the request must fail explicitly rather than silently falling back. REST uses 412 Precondition Failed.

### 10.3 Unpinned Requests During Convergence

Because B3 explicitly chooses bounded eventual consistency and prioritizes Data Plane availability, during the <=2-second convergence window different nodes may temporarily hold different latest eligible Active versions. An unpinned request executes the latest Active version currently loaded on its serving node. Consumers requiring strict version repeatability must use version pinning. Atomic Snapshot guarantees internal consistency within each execution.

### 10.4 Canary Routing

Percentage Canary routing shall be sticky and deterministic using a consumer-provided subject key. A stable mapping equivalent to Hash(subjectKey) mod 100 < CanaryPercentage shall be used conceptually; the exact hash algorithm is an ADR/API-contract concern but must preserve stable routing for a fixed rollout configuration. Targeted cohorts may additionally route by approved attributes such as staff cohort or region.

