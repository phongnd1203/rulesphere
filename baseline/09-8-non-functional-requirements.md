# SRS source section

Source: `RuleSphere_SRS_v1.0_Final.docx`. Requirements retain their original status; extraction is not a new approval.

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

