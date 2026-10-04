# RuleSphere — Yourdon–DeMarco Context Diagram by Function

Nguồn: `RuleSphere_SRS_v1.0_Final.docx` (RS-SRS-001, v1.0 Final), mục 2, 4, 6 và 7.

Mỗi hình dưới đây là một **góc nhìn của cùng tiến trình 0: RuleSphere**. Hình chữ nhật là thực thể ngoài; hình tròn là toàn bộ hệ thống. Các nhãn trên mũi tên là dữ liệu trao đổi qua ranh giới hệ thống.

## 1. Thiết kế, kiểm tra và chạy thử quyết định

```mermaid
flowchart LR
    A01["A01<br/>Decision Author / Domain Expert"]
    RS0(("0<br/>RuleSphere"))

    A01 -->|"Decision draft, graph, schema version"| RS0
    A01 -->|"Test cases, sandbox input"| RS0
    RS0 -->|"Graph and contract validation results"| A01
    RS0 -->|"Sandbox decision result and trace"| A01
```

SRS: UC-05 đến UC-09; FR về Decision Graph, schema và sandbox execution.

## 2. Quản trị phê duyệt

```mermaid
flowchart LR
    A01["A01<br/>Decision Author"]
    A02["A02<br/>Domain Approver / Decision Owner"]
    A03["A03<br/>Workspace Owner"]
    A04["A04<br/>Compliance Officer"]
    RS0(("0<br/>RuleSphere"))

    A01 -->|"Release candidate and submission"| RS0
    RS0 -->|"Calculated risk tier and release status"| A01

    RS0 -->|"Risk tier and approval package"| A02
    A02 -->|"Approval or rejection; upward risk override"| RS0
    RS0 -->|"Approval and release status"| A02

    RS0 -->|"Tier-2+ approval task and release evidence"| A03
    A03 -->|"Workspace approval decision"| RS0

    RS0 -->|"Tier-3 review package and compliance evidence"| A04
    A04 -->|"Compliance approval decision"| RS0
```

SRS: UC-10 đến UC-14; risk-based approval và immutable artifact.

## 3. Triển khai an toàn và đồng bộ runtime

```mermaid
flowchart LR
    RM["Authorized Approver / Release Manager<br/>(UC-15 to UC-19)"]
    A05["A05<br/>Enterprise Administrator"]
    RS0(("0<br/>RuleSphere"))

    RM -->|"Shadow and canary rollout settings"| RS0
    RM -->|"Promote or rollback instruction"| RS0
    RS0 -->|"Shadow differences and canary status"| RM
    RS0 -->|"Active version and deployment status"| RM

    A05 -->|"Fleet convergence query"| RS0
    RS0 -->|"Desired and loaded artifact state by runtime node"| A05
```

SRS: UC-15 đến UC-20 và UC-27; shadow, canary, promotion, rollback và convergence.

## 4. Quản trị tenant, bảo mật và kiểm toán

```mermaid
flowchart LR
    A05["A05<br/>Enterprise Administrator"]
    A06["A06<br/>Security Auditor"]
    A04["A04<br/>Compliance Officer"]
    RS0(("0<br/>RuleSphere"))

    A05 -->|"Tenant and workspace settings; memberships and roles"| RS0
    A05 -->|"API credential and shared-library administration"| RS0
    RS0 -->|"Configuration, credential and library status"| A05

    A06 -->|"Access, security and audit evidence query"| RS0
    RS0 -->|"Access, security and governance evidence"| A06

    A04 -->|"Compliance and historical-decision query"| RS0
    RS0 -->|"Authorized audit evidence and masked trace"| A04
```

SRS: UC-01 đến UC-04, UC-25 và UC-26; tenant isolation, trace và audit evidence.

## 5. Tích hợp và đánh giá quyết định tại runtime

```mermaid
flowchart LR
    A07["A07<br/>Application Developer / Integrator"]
    A08["A08<br/>Consumer Application"]
    RS0(("0<br/>RuleSphere"))

    A07 -->|"Contract discovery request"| RS0
    RS0 -->|"Versioned REST and gRPC contracts"| A07

    A08 -->|"REST or gRPC evaluation request and input data"| RS0
    A08 -->|"Subject key, cohort and optional version pin"| RS0
    RS0 -->|"Decision result and execution reference"| A08
    RS0 -->|"Contract or pinned-version error, including 412"| A08
```

SRS: UC-21 đến UC-24; REST/gRPC API, sticky cohort, version pinning và trace capture.
