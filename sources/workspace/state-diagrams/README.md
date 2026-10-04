# RuleSphere — State diagrams (PlantUML)

Bộ sơ đồ trạng thái chi tiết, mỗi file `.puml` có thể mở và render độc lập. Nhãn dùng tiếng Anh để đồng nhất với bộ use case hiện có.

| File | Đối tượng và nội dung |
| --- | --- |
| [01_Decision_Draft.puml](01_Decision_Draft.puml) | Draft: chỉnh sửa, kiểm tra DAG/contract, sandbox, lỗi và chạy lại; UC-05–09 |
| [02_Release_Approval.puml](02_Release_Approval.puml) | Release candidate: tính risk, duyệt Tier 1/2/3, từ chối, nâng tier, build immutable artifact; UC-10–14 |
| [03_Deployment.puml](03_Deployment.puml) | Artifact trong một môi trường: Shadow, Canary, Active, phiên bản trước và rollback; UC-15–19 |
| [04_Runtime_Convergence.puml](04_Runtime_Convergence.puml) | Runtime node: so sánh desired/loaded version, đồng bộ, lỗi và thử lại; UC-20, UC-27 |
| [05_Runtime_Request.puml](05_Runtime_Request.puml) | Request: quyền truy cập, version pin, routing, contract, thực thi DAG, fallback và trace; UC-21–24 |

## Cách đọc

Mũi tên có dạng `event [guard] / effect`: sự kiện kích hoạt, điều kiện cần đúng và hành động khi chuyển trạng thái. Chấm đen là điểm bắt đầu; vòng tròn kép là kết thúc vòng đời đang xét. Hình thoi phân nhánh theo điều kiện. Hộp lớn chứa các trạng thái con. Dòng sự kiện bên trong một trạng thái biểu diễn xử lý không rời trạng thái đó.

Các sơ đồ theo dõi những đối tượng khác nhau, không ghép chúng thành một trạng thái chung của toàn hệ thống. Draft có thể tiếp tục tồn tại sau khi tạo candidate; hoàn tất build chỉ kết thúc phạm vi governance. Artifact Active có thể trở thành phiên bản trước và được chọn lại khi rollback, nên không có trạng thái kết thúc ở đó.

## Nguồn và giới hạn

Nguồn trực tiếp đã đọc: `../use-case-diagrams/*.puml`, `../use-case-diagrams/README.md`, `../RuleSphere_Context_Diagram_By_Function.md` và `../RuleSphere_Context_Diagram_Detailed.mmd`. Các tài liệu này tham chiếu SRS RS-SRS-001 v1.0 Final. File DOCX bị tiến trình khác khóa khi soạn sơ đồ, nên chưa đối chiếu trực tiếp nội dung SRS.

Tên trạng thái và các bước xử lý nội bộ là cách mô hình hóa, không khẳng định đây là các enum đã được SRS định nghĩa. Những điểm cần xác nhận khi đối chiếu SRS:

- Validation gắn với revision; chỉnh sửa làm mất hiệu lực kết quả cũ. Không đặt sandbox thành gate bắt buộc.
- Release candidate cố định theo revision; sửa release bị từ chối tạo candidate mới. Build lại chỉ dùng cùng revision đã duyệt.
- Nâng risk tier bắt đầu lại đánh giá yêu cầu phê duyệt; bằng chứng cũ vẫn được giữ. Chính sách tái sử dụng approval chưa được xác định.
- Tier 2 duyệt tuần tự Domain Peer → Workspace Owner; Tier 3 cần cả Domain Owner và Compliance Officer. Maker không được tự duyệt.
- Các mode triển khai được biểu diễn loại trừ nhau trong một môi trường. Tài liệu đọc được chưa bắt buộc chuỗi Shadow → Canary → Active; các đường trực tiếp vẫn có guard theo chính sách triển khai.
- Các bước fetch/check/load và retry là chi tiết đề xuất. Chưa ấn định thời gian retry, liveness hoặc cách phục vụ khi load thất bại.
- Request pin không khả dụng/không hợp lệ trả REST 412 hoặc lỗi tương đương gRPC; không âm thầm chuyển sang Active. Thứ tự ưu tiên cohort/percentage chưa được xác định.
- Chính sách lỗi lưu trace phải quan sát được và không âm thầm thay đổi kết quả quyết định; chưa tự đặt cơ chế queue, retry hay mã phản hồi cụ thể.

Không tự thêm trạng thái Archived/Deleted cho Decision hoặc vòng đời Tenant/User vì các nguồn hiện có không mô tả đủ quy tắc chuyển trạng thái. UC-25/26 là truy vấn bằng chứng, không được ép thành vòng đời đối tượng mới.

## Xem sơ đồ

Mở file `.puml` bằng extension PlantUML trong VS Code rồi chọn **Preview Current Diagram** (`Alt+D`). Có thể xuất SVG bằng PlantUML CLI:

```powershell
java -jar path/to/plantuml.jar -charset UTF-8 -tsvg state-diagrams/*.puml
```
