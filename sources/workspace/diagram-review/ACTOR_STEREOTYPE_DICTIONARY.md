# RuleSphere — Actor & Stereotype Common Dictionary (F-17)

Tài liệu này chuẩn hóa và hợp nhất toàn bộ Actor, Stereotype, và Phân loại thành phần được sử dụng xuyên suốt bộ mô hình UML & COMET của RuleSphere.

---

## 1. Bảng chuẩn hóa Actor (Actor ID → Role → Kind → Scope)

| Actor ID | Tên vai trò (Role) | Loại Actor (Kind) | Phạm vi & Trách nhiệm chính (Scope) | View áp dụng |
| :--- | :--- | :--- | :--- | :--- |
| **A01** | Decision Author / Domain Expert | `Human Actor` | Tạo, chỉnh sửa đồ thị quyết định (DAG), bảng quyết định, cây quyết định, biểu thức, fallback có kiểu; định nghĩa schema hợp đồng; chạy kiểm thử sandbox. | Use Case (02), Sequence (02, 03), Communication (02), Activity (02), Context Class |
| **A02** | Workspace Owner | `Human Actor` | Quản lý thành viên, gán vai trò trong Workspace; phê duyệt kiểm duyệt quản trị cấp 2 (Tier 2 Peer Review). | Use Case (01, 03), Sequence (01, 03), Context Class |
| **A03** | Enterprise Admin | `Human Actor` | Quản trị Tenant/Workspace, cấp phát/thu hồi thông tin xác thực (API credentials), phát hành thư viện dùng chung (Shared Library). | Use Case (01), Sequence (01), Context Class |
| **A04** | Release Manager | `Human Actor` | Nộp phiên bản ứng viên phát hành, cấu hình chính sách Shadow/Canary, kích hoạt promote lên Active hoặc rollback phiên bản trước. | Use Case (03, 04), Sequence (03, 04, 05), Activity (03, 04, 05), Context Class |
| **A05** | Compliance Officer | `Human Actor` | Phê duyệt quyết định rủi ro cao/quy định (Tier 3 Approval); tra cứu dữ liệu sổ cái tuân thủ (Compliance Ledger). | Use Case (03, 06), Sequence (03, 08), Context Class |
| **A06** | Security Auditor | `Human Actor` | Tra cứu vết kiểm toán bất biến (Audit Evidence), giám sát ranh giới cô lập Tenant và bảo vệ dữ liệu nhạy cảm. | Use Case (06), Sequence (08), Context Class |
| **A07** | Application Developer / Integrator | `Human Actor` | Khám phá hợp đồng API phiên bản hóa (REST/gRPC schema discovery - F34); tích hợp hệ thống tiêu thụ. | Use Case (05), Context Class |
| **A08** | Consumer Application | `External System Actor` | Gọi thực thi quyết định trực tiếp qua REST hoặc gRPC với yêu cầu độ trễ thấp (<10ms); tùy chọn gắn ghim phiên bản (X-Decision-Version). | Use Case (05), Sequence (04, 06), Communication (06), Component, Deployment, Context Class |

---

## 2. Bảng Stereotype chuẩn hóa theo chuẩn OMG UML 2.5.1 & COMET

| Stereotype | Định nghĩa & Ý nghĩa | Mức độ / View áp dụng | Ví dụ trong RuleSphere |
| :--- | :--- | :--- | :--- |
| `<<software system>>` | Hệ thống phần mềm trung tâm trong phạm vi thiết kế. | System Context Class Diagram | `RuleSphere` |
| `<<external, human>>` | Tác nhân con người bên ngoài hệ thống. | Context Class, Use Case | `A01: Decision Author`, `A04: Release Manager` |
| `<<external, system>>` | Hệ thống phần mềm hoặc dịch vụ bên ngoài giao tiếp với hệ thống. | Context Class, Sequence, Communication | `A08: Consumer Application` |
| `<<boundary>>` | Đối tượng hoặc thành phần giao tiếp tại ranh giới hệ thống (API, Adapter, UI). | Sequence, Communication, Component | `ManagementAPI`, `REST/gRPC Adapter` |
| `<<coordinator>>` | Đối tượng điều phối luồng xử lý hoặc trường hợp sử dụng (COMET Coordinator). | Communication, Class | `EvaluationService` |
| `<<service>>` | Lớp/thành phần cung cấp dịch vụ tính toán, xử lý nghiệp vụ hoặc xác thực. | Class, Component, Communication | `DecisionValidator`, `SnapshotResolver`, `ArtifactBuilder` |
| `<<state dependent control>>` | Đối tượng điều khiển có hành vi phụ thuộc vào trạng thái và máy trạng thái (COMET). | Class, State Machine, Communication | `GovernanceController`, `ReleaseCandidate`, `Deployment` |
| `<<entity>>` | Đối tượng miền bài toán có định danh (identity), thuộc tính và vòng đời lưu trữ. | Domain Class Model, Communication | `Tenant`, `DecisionVersion`, `Release`, `LoadedArtifact` |
| `<<value object>>` | Đối tượng giá trị bất biến, nhận diện qua giá trị thuộc tính thay vì ID. | Class Diagram, Domain Model | `TypedFallback`, `LibraryReference` |
| `<<active task>>` | Tác vụ đồng thời độc lập có luồng điều khiển riêng (thread of control - COMET Task Design). | Concurrent Task Architecture | `RuntimeWorkerTask`, `TraceIngestionWorkerTask`, `ArtifactSyncListenerTask` |
| `<<passive object>>` | Cấu trúc dữ liệu hoặc bộ nhớ dùng chung, an toàn luồng, không có luồng riêng. | Concurrent Task Architecture | `LocalArtifactCache`, `AtomicSnapshot`, `TraceBufferQueue` |
| `<<timer task>>` | Tác vụ định kỳ được kích hoạt theo bộ định thời hệ thống. | Concurrent Task Architecture | `ConvergenceHeartbeatTask` |
| `<<execution environment>>` | Nút hoặc môi trường thực thi phần mềm vật lý/ảo hóa (OS, JVM, Container). | Deployment Diagram | `ControlHost`, `RuntimeNodeHost`, `BrokerNode` |
| `<<artifact>>` | Thành phần vật lý được triển khai lên nút thực thi (file JAR, bundle, binary). | Deployment Diagram | `rulesphere-management.jar`, `rulesphere-runtime-engine.jar` |

---

## 3. Quy ước và Invariant kiến trúc cốt lõi

1. **Phân biệt User miền bài toán và Actor bên ngoài:**
   - `User` trong Entity Model là thực thể tài khoản nội bộ thuộc về `Tenant`.
   - `A01..A07` là các vai trò tác nhân bên ngoài hệ thống tương tác với giao diện Control Plane.
2. **Ký hiệu Package và Plane (AC-01):**
   - Ba plane: Control Plane (Quản lý), Delivery Plane (Phân phối), Data Plane (Thực thi).
   - Đường phụ thuộc giữa các package (`..>`) là quan hệ logic/biên dịch, không phải là RPC đồng bộ.
3. **Bất biến độc lập Data Plane (AC-04):**
   - Không có phụ thuộc mạng đồng bộ nào từ Data Plane tới Control Plane trong luồng đánh giá quyết định thông thường.
