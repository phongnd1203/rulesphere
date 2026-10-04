# SRS source section

Source: `RuleSphere_SRS_v1.0_Final.docx`. Requirements retain their original status; extraction is not a new approval.

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

