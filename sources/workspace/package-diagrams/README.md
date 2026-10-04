# RuleSphere — Package Diagram

[Xem sơ đồ SVG](previews/01_RuleSphere_Packages.svg) · [Sửa nguồn PlantUML](01_RuleSphere_Packages.puml)

Sơ đồ tổ chức các module logic của RuleSphere thành **Control Plane**, **Delivery / Distribution Plane**, **Data Plane** và các module dùng chung. Nguồn: `RuleSphere_SRS_v1.0_Final.docx` (RS-SRS-001), đặc biệt mục 5–14, cùng bộ `class-diagrams` và `sequence-diagrams` hiện có.

Mũi tên nét đứt `A ..> B` nghĩa là **package A phụ thuộc hoặc sử dụng package B**. Đây không phải thứ tự xử lý hay hướng truyền dữ liệu. Hộp lồng nhau thể hiện package chứa package con; không biểu diễn máy chủ triển khai.

## Nội dung các package

| Plane / nhóm | Package | Lớp hoặc trách nhiệm tiêu biểu | Use case |
| --- | --- | --- | --- |
| Control Plane | Administration | Tenant, Workspace, User, Membership, Role, ApiCredential, SharedLibrary và version bất biến | UC-01–04 |
| Control Plane | Decision Modeling | DecisionVersion, DecisionGraph, DecisionNode, SchemaVersion, DecisionValidator, SandboxService | UC-05–09 |
| Control Plane | Governance and Approval | Release, GovernancePolicy, RiskAssessment, ApprovalStage, ApprovalEvidence, ArtifactBuilder | UC-10–14 |
| Control Plane | Evidence Queries | EvidenceQueryService; truy vấn execution, audit và fleet theo quyền | UC-25–27 |
| Delivery | Deployment Management | Deployment, RolloutPolicy, DesiredActiveState; Shadow, Canary, promote, rollback và xem diff | UC-15–19 |
| Delivery | Artifact Distribution | DistributionService; phát artifact và thay đổi desired state tới fleet | UC-20 |
| Data Plane | Runtime API and Execution | REST/gRPC adapter, EvaluationService, GraphExecutor, Execution; áp dụng routing, thực thi Shadow và tạo outcome comparison | UC-15–17, UC-21–24 |
| Data Plane | Local Artifact Management | RuntimeNode, LoadedArtifact, LocalArtifactStore, SnapshotResolver, AtomicSnapshot; load/validate và chọn snapshot khả dụng | UC-20–23, UC-27 |
| Shared | Security and Scope | AuthorizationService, AccessScope; hợp đồng kiểm tra quyền tenant/workspace và danh tính | Xuyên suốt |
| Shared | Versioned Contracts | Hợp đồng artifact/manifest, publication/rollout configuration, REST/gRPC, trace/ledger/telemetry | UC-14–24, NFR-INT-001 |
| Shared | Audit and Observability | TraceCaptureService, SensitiveDataProtector, ExecutionTraceTree, ComplianceRecord, AuditEvent, ShadowComparison và FleetConvergenceView | UC-16, UC-24–27 và audit xuyên suốt |

## Các quyết định thiết kế

- Package là ranh giới tổ chức mã và trách nhiệm được đề xuất, không phải danh sách microservice đã chốt. SRS bắt buộc tách trách nhiệm ba plane nhưng không quy định cấu trúc thư mục hoặc công nghệ.
- Một nhóm class diagram có thể được tách qua nhiều package: nhóm Deployment/Distribution tách phần điều phối rollout khỏi phần load artifact tại runtime; nhóm Audit tách giao diện truy vấn khỏi khả năng capture/lưu evidence.
- `Versioned Contracts` chứa các kiểu/hợp đồng chia sẻ để runtime đọc artifact và cấu hình đã phát mà không gọi module Governance hoặc Decision Modeling. Graph, schema và các dependency được cố định trong snapshot; Data Plane không đọc draft khi đang đánh giá.
- `Administration` quản lý membership/credential; `Security and Scope` cung cấp khả năng kiểm tra quyền. Runtime phải có triển khai kiểm tra quyền không phụ thuộc đồng bộ vào Control Plane. Cách phân phối credential/revocation cần thiết kế riêng theo ADR, không được sơ đồ này ngầm chốt.
- Distribution là phía phát và Local Artifact Management là phía nhận của hợp đồng distribution. Cả hai phụ thuộc `Versioned Contracts`; không vẽ mũi tên phụ thuộc package như thể đó là đường truyền artifact. Sequence diagram số 05 mô tả thứ tự truyền, load và xác nhận.
- `Audit and Observability` biểu diễn khả năng dùng chung và các triển khai phù hợp từng plane, không yêu cầu mọi thao tác gọi một dịch vụ tập trung. Trace capture phải bất đồng bộ/an toàn, bảo vệ dữ liệu nhạy cảm trước persistence và quan sát được lỗi/backpressure.
- Shadow/Canary được cấu hình ở Delivery và thực thi ở Data Plane. Shadow outcome không thay production response. Module audit giữ protected diff và evidence phục vụ truy vấn.
- Chỉ reference Shared Library cùng Tenant với version chính xác mới được phép tái sử dụng qua workspace; các mũi tên package không cấp quyền truy cập chéo tenant/workspace.

## Xem và xuất lại

Mở SVG bằng trình duyệt để phóng to hoặc mở `.puml` trong VS Code với extension PlantUML rồi nhấn `Alt+D`.

```powershell
java -jar path/to/plantuml.jar -charset UTF-8 -tsvg -o previews package-diagrams/*.puml
```

Yêu cầu kiến trúc chính được thể hiện: AC-01–07, FR-TEN-001–004, FR-SEC-001–003, FR-DIST-001–005, FR-RUN-005–008 và FR-AUD-001–008. Sơ đồ không chứng minh SLA/NFR đã đạt trong triển khai thực tế.
