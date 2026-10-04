# RuleSphere — Sequence diagrams

Bộ 8 sơ đồ trình tự bao phủ UC-01–27, đọc trực tiếp từ **RuleSphere_SRS_v1.0_Final.docx (RS-SRS-001)**, đặc biệt mục 5–14; tham chiếu tên lớp từ bộ `class-diagrams`. Nhãn tiếng Anh thống nhất với các sơ đồ hiện có.

| Sơ đồ | Use case | Xem hình | Sửa nguồn |
| --- | --- | --- | --- |
| 01. Quản trị và Shared Library | UC-01–04 | [SVG](previews/01_Administration.svg) | [PlantUML](01_Administration.puml) |
| 02. Soạn Decision, kiểm tra và sandbox | UC-05–09 | [SVG](previews/02_Decision_Modeling.svg) | [PlantUML](02_Decision_Modeling.puml) |
| 03. Gửi duyệt, risk tier và build artifact | UC-10–14 | [SVG](previews/03_Governance_and_Approval.svg) | [PlantUML](03_Governance_and_Approval.puml) |
| 04. Shadow, phân tích diff và Canary | UC-15–17 | [SVG](previews/04_Shadow_and_Canary.svg) | [PlantUML](04_Shadow_and_Canary.puml) |
| 05. Promote, rollback và đồng bộ fleet | UC-18–20, UC-27 | [SVG](previews/05_Deployment_and_Convergence.svg) | [PlantUML](05_Deployment_and_Convergence.puml) |
| 06. Thực thi REST/gRPC và version pin | UC-21–24 | [SVG](previews/06_Runtime_Evaluation.svg) | [PlantUML](06_Runtime_Evaluation.puml) |
| 07. Bảo vệ và lưu execution evidence | UC-24 | [SVG](previews/07_Trace_Capture.svg) | [PlantUML](07_Trace_Capture.puml) |
| 08. Giải thích quyết định và xem audit | UC-25–26 | [SVG](previews/08_Historical_Explain_and_Audit.svg) | [PlantUML](08_Historical_Explain_and_Audit.puml) |

## Ký hiệu

Đọc từ trên xuống. `->` là lời gọi, `-->` là phản hồi, `->>` là gửi bất đồng bộ. `alt/else` mô tả các nhánh loại trừ; `opt` là bước có điều kiện; `loop` là lặp; `par` là xử lý song song; `break` kết thúc tương tác đang mô tả khi điều kiện xảy ra; `ref` dẫn tới luồng chi tiết khác. Số thứ tự giúp đối chiếu các thông điệp.

Các lệnh quản trị và review là những request riêng biệt. Việc đặt chúng trên cùng một sơ đồ không có nghĩa giữ HTTP request mở trong thời gian chờ người phê duyệt hoặc xây dựng một BPM workflow.

## Đối chiếu yêu cầu

| Sơ đồ | Yêu cầu chính |
| --- | --- |
| 01 | FR-TEN-001–004, FR-SEC-001–003, NFR-AUD-001 |
| 02 | FR-DM-001–003, FR-DM-008, FR-SCH-001–004, FR-TEN-004 |
| 03 | FR-GOV-001–009, FR-REL-001–002, mục 9.1 và 9.3 |
| 04 | FR-REL-003–008, mục 9.2 và 10.4 |
| 05 | FR-REL-009–011, FR-DIST-001–005, NFR-CONS-001, NFR-OBS-001 |
| 06 | FR-RUN-001–010, FR-DM-004–007, FR-SCH-005, FR-SEC-002, AC-04 |
| 07 | FR-AUD-001–005, FR-AUD-008, FR-SCH-006, mục 11 |
| 08 | FR-AUD-006–007, mục 11 và 12.1 |

## Phạm vi thiết kế

Đây là mô hình tương tác đề xuất từ yêu cầu, không phải sơ đồ trích xuất từ mã nguồn. `Management API`, service điều phối, kho dữ liệu và telemetry là thành phần logic; không chốt công nghệ database, broker, queue, giao dịch hoặc chữ ký phương thức. Nhánh lỗi tập trung vào nghiệp vụ và các tình huống bắt buộc trong SRS mục 14, không liệt kê mọi lỗi hạ tầng có thể xảy ra.

- Mỗi lệnh phải kiểm tra quyền theo scope hiện hành. Runtime authorization không tạo phụ thuộc đồng bộ tới Control Plane.
- Validation gắn với revision; việc gửi duyệt và build phải dùng đúng revision. Sandbox là thao tác tùy chọn. Breaking schema change ảnh hưởng risk tier và được xét theo policy.
- Tier 2 bắt buộc Domain Peer trước Workspace Owner; Tier 3 cần cả Domain Owner và Compliance Officer, không tự quy định thứ tự. Maker không được duyệt ở bất kỳ vai trò nào. Tái sử dụng approval sau nâng tier cần quyết định policy/ADR.
- Shadow và Canary có thể cùng bật. Khi production dùng Canary, sơ đồ đề xuất một lần đánh giá Active baseline riêng để so sánh Active/Shadow; cơ chế lập lịch và correlation cần ADR. Mọi giá trị được lưu trong diff phải được bảo vệ.
- Desired Active khác loaded Active. Mốc <=2 giây tính từ lúc phát publication event tới khi toàn bộ active nodes báo loaded/eligible, không phải từ lúc nhận lệnh. Đây là yêu cầu cần kiểm thử hệ thống, không phải kết quả đo của sơ đồ.
- Version pin phải trả đúng phiên bản hoặc REST 412/lỗi gRPC tương đương. Unpinned dùng loaded Active của node, có xét routing Canary đã cấu hình. Không thay snapshot giữa execution.
- Thuật toán hash Canary, thứ tự ưu tiên cohort/percentage, lỗi thiếu subject key, retry đồng bộ, gRPC status cụ thể và chiến lược trace backpressure chưa được SRS chốt.
- Capture bất đồng bộ cần thiết kế độ tin cậy riêng; các mũi tên không chứng minh bảo đảm delivery. Lỗi lưu evidence phải quan sát được và theo policy, không âm thầm đổi kết quả nghiệp vụ.
- Khi full trace hết retention, chỉ trả evidence còn giữ được và báo rõ giới hạn; không dựng lại các bước trung gian không còn dữ liệu.

## Xem và xuất lại

Mở SVG bằng trình duyệt để phóng to, hoặc mở `.puml` bằng extension PlantUML trong VS Code rồi nhấn `Alt+D`.

```powershell
java -jar path/to/plantuml.jar -charset UTF-8 -tsvg -o previews sequence-diagrams/*.puml
```

Cả 8 sơ đồ đã được render bằng PlantUML và kiểm tra SVG không chứa lỗi cú pháp. Việc render xác nhận cú pháp, không thay thế kiểm thử nghiệp vụ hoặc đo NFR của hệ thống triển khai.
