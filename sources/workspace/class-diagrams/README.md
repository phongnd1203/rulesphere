# RuleSphere — Class diagram chia theo nhóm

Bộ sơ đồ lớp được thiết kế từ **SRS RS-SRS-001 v1.0 Final**, đã đọc trực tiếp `../RuleSphere_SRS_v1.0_Final.docx`, đặc biệt các mục 5–14. Chia thành 6 nhóm tương ứng bộ use case hiện có. Tên lớp và phương thức dùng tiếng Anh để thống nhất thuật ngữ.

Đây là **mô hình phân tích và thiết kế đề xuất**, không phải sơ đồ trích xuất từ mã nguồn hay thiết kế database đã chốt. Các lớp phụ trợ, tên thuộc tính, kiểu dữ liệu, chữ ký phương thức và bội số là cách cụ thể hóa yêu cầu; SRS không quy định toàn bộ chi tiết này.

| Nhóm | Nội dung | Use case chính | Xem hình | Sửa nguồn |
| --- | --- | --- | --- | --- |
| Tổng quan | Quan hệ giữa các lớp chính trong 6 nhóm | UC-01–27 | [SVG](previews/00_Overview.svg) | [PlantUML](00_Overview.puml) |
| 01. Administration | Tenant, Workspace, User, quyền, credential, Shared Library | UC-01–04 | [SVG](previews/01_Administration.svg) | [PlantUML](01_Administration.puml) |
| 02. Decision Modeling | Decision/version, DAG, 4 loại node, schema, fallback, validation, sandbox | UC-05–09 | [SVG](previews/02_Decision_Modeling.svg) | [PlantUML](02_Decision_Modeling.puml) |
| 03. Governance and Approval | Release, risk, approval, maker exclusion, artifact bất biến | UC-10–14 | [SVG](previews/03_Governance_and_Approval.svg) | [PlantUML](03_Governance_and_Approval.puml) |
| 04. Deployment and Distribution | Shadow/Canary, desired Active, rollback, runtime load | UC-15–20 | [SVG](previews/04_Deployment_and_Distribution.svg) | [PlantUML](04_Deployment_and_Distribution.puml) |
| 05. Runtime and Integration | REST/gRPC, request/response, atomic snapshot, execution, API contract | UC-21–23; NFR-INT-001 | [SVG](previews/05_Runtime_and_Integration.svg) | [PlantUML](05_Runtime_and_Integration.puml) |
| 06. Audit and Observability | Trace tree, compliance ledger, audit, retention, fleet convergence | UC-24–27 | [SVG](previews/06_Audit_and_Observability.svg) | [PlantUML](06_Audit_and_Observability.puml) |

## Cách đọc

- `-` là thuộc tính private; `+` là phương thức/thuộc tính public.
- `1`, `0..1`, `0..*`, `1..*` biểu diễn bội số ở mỗi đầu quan hệ.
- Hình thoi đặc: composition, bộ phận thuộc một chủ sở hữu. Hình thoi rỗng: aggregation, tập hợp các đối tượng có vòng đời riêng.
- Tam giác rỗng với đường liền: kế thừa. Đường nét đứt với tam giác rỗng: triển khai interface. Mũi tên nét đứt thường: dependency.
- `external` chỉ cùng một lớp được định nghĩa trong nhóm khác, không phải hệ thống bên ngoài hoặc lớp trùng mới.
- `service`, `boundary`, `DTO`, `value object`, `read model`, `immutable` là stereotype mô tả vai trò thiết kế.
- `UUID`, `Value`, `Map`, `Expression`, các kiểu danh sách và cấu trúc rule là kiểu ký hiệu. Không áp đặt ngôn ngữ, database hoặc rule engine.

## Các quyết định mô hình hóa

1. Actor như Decision Author, Domain Approver, Workspace Owner được biểu diễn bằng vai trò của User, không tạo cây kế thừa User theo chức danh. User trong sơ đồ là danh tính trong một Tenant; liên kết tới nhà cung cấp danh tính nằm ngoài phạm vi này.
2. DecisionVersion có thể sửa ở Draft, đóng băng khi approved/published. Release giữ revision được xét duyệt; ApprovalEvidence bất biến ghi revision đó. Reject trả candidate về Draft theo SRS 9.1; việc sửa không làm bằng chứng cũ trở thành approval cho revision mới.
3. GovernanceStatus tách khỏi DeploymentStatus. Shadow và Canary là cấu hình độc lập để cho phép “Shadow and/or Canary” theo SRS 9.2. `RollingOut` và đối tượng môi trường/desired pointer là cách thiết kế đề xuất.
4. NodeDependency chỉ nối node cùng graph; DAG không có chu trình. Schema trực tiếp phải ở cùng Workspace. Cross-workspace reuse chỉ thông qua Shared Library cùng Tenant với version chính xác.
5. Artifact giữ manifest các version chính xác. AtomicSnapshot cố định tập artifact/schema/dependency trong suốt Execution. LoadedArtifact có thể chứa nhiều version trên một runtime để hỗ trợ pin và rollback.
6. Trace tree khác Decision Graph. Execution là đối tượng runtime ngắn hạn; trace/ledger có vòng đời lưu trữ riêng nên không dùng composition từ Execution. Bội số `0..1` phản ánh chưa lưu, lỗi lưu hoặc hết retention; hệ thống vẫn phải capture các execution thuộc diện audit.
7. Hot trace lưu 30–90 ngày, compliance metadata 5–7 năm theo policy. Các giá trị nhạy cảm phải được bảo vệ trước persistence. FleetConvergenceView là mô hình đọc so sánh desired state và loaded state, không phải nguồn trạng thái triển khai thứ hai.

## Phạm vi và đối chiếu

Các nhóm bao phủ đủ UC-01–27; UC-24 đặt ở nhóm Audit vì trách nhiệm chính là capture bằng chứng, còn nhóm Runtime cung cấp Execution. Mỗi sơ đồ chi tiết có thuộc tính, phương thức và quan hệ phù hợp với trách nhiệm lớp; các lớp evidence bất biến chủ yếu chứa dữ liệu.

SRS là nguồn ưu tiên khi có khác biệt với sơ đồ cũ. Không sửa bộ state/use-case trong lần này. Không chốt broker, cache, cơ sở dữ liệu, rule syntax, thuật toán hash Canary, chính sách tái sử dụng approval sau khi tăng tier, hoặc thứ tự ưu tiên cohort/percentage; các điểm đó cần quyết định thiết kế riêng theo ADR backlog.

## Render

Mỗi file `.puml` độc lập, mở bằng PlantUML trong VS Code rồi nhấn `Alt+D`. Xuất lại SVG:

```powershell
java -jar path/to/plantuml.jar -charset UTF-8 -tsvg -o previews class-diagrams/*.puml
```

Các SVG nằm trong `previews/`; mở bằng trình duyệt và phóng to để đọc chi tiết.

Đã render thành công cả 7 sơ đồ bằng PlantUML; kiểm tra các đầu quan hệ đều tham chiếu lớp đã khai báo và các SVG không có lỗi cú pháp. Có thêm [PNG tổng quan](previews/00_Overview.png).
