# SRS source section

Source: `RuleSphere_SRS_v1.0_Final.docx`. Requirements retain their original status; extraction is not a new approval.

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

