# SRS source section

Source: `RuleSphere_SRS_v1.0_Final.docx`. Requirements retain their original status; extraction is not a new approval.

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

