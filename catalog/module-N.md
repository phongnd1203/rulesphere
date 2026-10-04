# Proposed catalog source section

Status: **Proposed**, not automatically approved SRS requirements. Source: [full catalog](../sources/workspace/use-case-diagrams/drawio-catalog/source-catalog.md). Interpret relationships alongside [module notes](../sources/workspace/use-case-diagrams/drawio-catalog/module-notes.md), which contain later modeling refinements.

# 16. Module N — Runtime Operations & Observability

## Use Cases

| ID | Use Case | Actor |
|---|---|---|
| OPS-01 | Monitor Decision Runtime | Operations / SRE |
| OPS-02 | View Runtime Health | Operations / SRE |
| OPS-03 | View Decision Metrics | Operations / SRE |
| OPS-04 | View Request Volume | Operations / SRE |
| OPS-05 | View Decision Latency | Operations / SRE |
| OPS-06 | View Error Rate | Operations / SRE |
| OPS-07 | View Runtime Version | Operations / SRE |
| OPS-08 | View Runtime Logs | Operations / SRE |
| OPS-09 | View Runtime Traces | Operations / SRE |
| OPS-10 | Diagnose Execution Failure | Operations / SRE |
| OPS-11 | Receive Runtime Alert | Operations / SRE |
| OPS-12 | Export Telemetry | Observability Platform |

### Relations

```text
Monitor Decision Runtime
  <<include>> View Runtime Health
  <<include>> View Decision Metrics

View Decision Metrics
  <<include>> View Request Volume
  <<include>> View Decision Latency
  <<include>> View Error Rate

Diagnose Execution Failure
  <<include>> View Runtime Logs
  <<include>> View Runtime Traces

Receive Runtime Alert
  <<extend>> Monitor Decision Runtime

RuleSphere --> Export Telemetry --> Observability Platform
```

---
