# Quality, security, interfaces and acceptance

Authority: [SRS NFRs](baseline/09-8-non-functional-requirements.md), [audit/privacy](baseline/12-11-audit-privacy-and-retention.md), [interfaces](baseline/13-12-external-interface-requirements.md), [acceptance strategy](baseline/17-16-verification-and-acceptance-strategy.md).

## Performance and reliability targets

| Requirement | Exact baseline target |
| --- | --- |
| NFR-PERF-001 | gRPC p95 < 10 ms and p99 < 25 ms |
| NFR-PERF-002 | REST p95 < 25 ms and p99 < 50 ms |
| NFR-PERF-003 | At least 2,000 RPS per runtime node on 4 vCPU / 8 GB RAM |
| NFR-CONS-001 | 100% of active runtime nodes loaded/eligible on desired published/rollback artifact within ≤2 seconds of publication-event emission |
| NFR-AVAIL-001 | Data Plane availability target 99.99%, measured independently of Control Plane uptime |
| NFR-TRACE-001 | Full Trace Tree capture adds ≤10% latency penalty under defined benchmark workload |

Latency targets apply to graphs of at most ten nodes and payloads of at most 10 KB under the approved benchmark profile. They exclude uncontrolled public-Internet latency. Record topology, serialization, TLS, trace mode and client/server placement with results. The exact availability observation window and planned-maintenance exclusions belong in the operational SLO specification. These are requirements, not achieved benchmark measurements.

Remaining NFRs require serving through Control Plane failures/partitions, no mixed-snapshot execution, no cross-tenant leakage, no plaintext sensitive traces, immutable attributable audit evidence, telemetry for health/load/convergence/trace failures, horizontal scaling without semantic changes and versioned documented REST/gRPC contracts. The [14-row register](registers/nonfunctional-requirements.csv) preserves full wording.

## Access and isolation

Enforce tenant/workspace scope on management, runtime and audit paths. Tenant isolation covers business data, identities/memberships, credentials and audit records. Runtime credentials only authorize permitted decisions. Issuance and revocation are auditable. Shared-library publication is the controlled cross-workspace reuse mechanism; it never enables direct cross-tenant sharing.

Authorization and Maker-Checker constraints remain in force for every tier and every requested version. Actor generalization in a diagram is not permission inheritance beyond the intended use-case contract.

## Privacy and retention

| Store | Required content | Retention |
| --- | --- | --- |
| Hot Trace | Full protected execution trace tree | Configurable within 30–90 days |
| Compliance Ledger | ExecutionID, DecisionVersion, InputHash, Output, MatchedNodeIDs, Timestamp, approval/release evidence reference | Configurable within 5–7 years |

Schema fields marked `is_sensitive=true` must be masked, tokenized or hashed before persistence. Choose protection based on classification and retrieval needs. Apply protection to sensitive values wherever they occur in persisted execution evidence; a field called Output is not a license to retain sensitive plaintext. Evidence access is authorization-scoped and audited.

`ApprovedByTicket` was normalized to an approval/release evidence reference. An external ticketing system or ticket identifier format is not mandated. Retention ranges are sponsor-approved policy ranges, not a single universal deployment value.

## Interfaces

Management interfaces support administration, authoring, schemas, validation, governance, releases, audit queries and convergence inspection. Exact UI layouts are unspecified.

REST supports scoped authentication, evaluation input, subject/cohort context, `X-Decision-Version`, contract validation, explicit errors and execution IDs. gRPC provides equivalent capabilities with protocol-specific representation. The SRS fixes the REST pinned-version failure as 412 but leaves exact gRPC field/status representation to documented contracts. Endpoint paths, complete JSON/protobuf payloads, detailed error catalog and rate limits are not fully specified here.

Distribution communicates desired-state changes with no restart and bounded convergence. A broker is one possible mechanism; no broker product is required by the SRS. Identity federation and concrete authentication mechanisms remain ADR topics. IdP, CI/CD, observability and SIEM interactions in later diagrams describe expanded design context.

## Acceptance evidence required by the SRS

Verify cycle rejection; deterministic repeatability while publishing concurrently; risk tiers, quorum and maker exclusion; adversarial tenant isolation; Shadow response independence; sticky Canary routing; exact pin/error contracts for both protocols; full-fleet convergence; latency/throughput on baseline hardware; partition/failure availability; trace overhead with trace off/on; absence of sensitive plaintext; and retention configuration within approved ranges.

The workspace contains design and render-validation artifacts, not a runnable RuleSphere implementation or runtime benchmark evidence. Existing diagram validation must not be reported as system acceptance testing.
