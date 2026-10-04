# RuleSphere — Communication Diagrams

Bộ 8 sơ đồ giao tiếp bao phủ UC-01–27, đối chiếu với bộ `sequence-diagrams` và yêu cầu SRS RS-SRS-001 v1.0 Final. Mỗi sơ đồ tập trung vào **đối tượng nào trao đổi với nhau và thông điệp nào được gửi trước**, thay vì trục thời gian dọc của sequence diagram.

| Luồng | Use case | Xem SVG | Nguồn PlantUML |
| --- | --- | --- | --- |
| 01. Administration | UC-01–04 | [SVG](previews/01_Administration.svg) | [PlantUML](01_Administration.puml) |
| 02. Decision Modeling | UC-05–09 | [SVG](previews/02_Decision_Modeling.svg) | [PlantUML](02_Decision_Modeling.puml) |
| 03. Governance and Approval | UC-10–14 | [SVG](previews/03_Governance_and_Approval.svg) | [PlantUML](03_Governance_and_Approval.puml) |
| 04. Shadow and Canary | UC-15–17 | [SVG](previews/04_Shadow_and_Canary.svg) | [PlantUML](04_Shadow_and_Canary.puml) |
| 05. Deployment and Convergence | UC-18–20, UC-27 | [SVG](previews/05_Deployment_and_Convergence.svg) | [PlantUML](05_Deployment_and_Convergence.puml) |
| 06. Runtime Evaluation | UC-21–24 | [SVG](previews/06_Runtime_Evaluation.svg) | [PlantUML](06_Runtime_Evaluation.puml) |
| 07. Trace Capture | UC-24 | [SVG](previews/07_Trace_Capture.svg) | [PlantUML](07_Trace_Capture.puml) |
| 08. Historical Explain and Audit | UC-25–26 | [SVG](previews/08_Historical_Explain_and_Audit.svg) | [PlantUML](08_Historical_Explain_and_Audit.puml) |

## Cách đọc

- Hộp `tênĐốiTượng : Kiểu` biểu diễn một đối tượng/vai trò tham gia tương tác, không phải package hoặc bảng database. `actor` và `boundary` là stereotype để phân biệt vai trò bên ngoài và giao diện.
- Mũi tên có số là thông điệp từ bên gửi tới bên nhận. `1.1` diễn ra trong tương tác `1`; `1.2` tiếp theo `1.1`; `1.2.1` là bước lồng trong `1.2`. Đọc theo số, không theo vị trí trái/phải của hộp.
- `[điều kiện]` là guard. Nhánh không thỏa guard không chạy. Khi authorization, validation hoặc snapshot resolution thất bại, không thực hiện các lời gọi phụ thuộc vào kết quả thành công; phản hồi lỗi được đưa về qua API.
- `*` biểu diễn lặp. Ở sơ đồ 06, lặp cả cặp evaluate-node và xử lý outcome theo thứ tự topo khi execution còn hợp lệ.
- Hậu tố `a/b/...` là các nhánh thay thế nếu không ghi khác. Riêng `1.2a` và `1.2b` ở sơ đồ 07 được ghi `parallel`: cả hai nhánh có thể chạy đồng thời sau khi bảo vệ dữ liệu.
- `async` là nhãn cho gửi bất đồng bộ. Các thông điệp con của nhánh bất đồng bộ không bắt buộc hoàn thành trước bước tiếp theo của bên gửi. Hai nhánh bất đồng bộ độc lập không được ngầm hiểu là có thứ tự hoàn thành cố định.
- Các phản hồi thông thường giữa service được lược bỏ cho dễ đọc; mũi tên nét đứt tới actor biểu diễn phản hồi được hiển thị. Số thông điệp ở đây là riêng cho communication diagram, không phải số `autonumber` trong sequence diagram.

PlantUML dùng các đối tượng và mũi tên có nhãn số để biểu diễn Communication Diagram. Mũi tên nối hai đối tượng vừa chỉ đường giao tiếp vừa chỉ hướng gửi thông điệp; đây không phải sơ đồ phụ thuộc tĩnh. Không dùng lifeline, activation bar hay trục thời gian của sequence diagram.

## Phạm vi và giả định

Đây là thiết kế tương tác đề xuất từ SRS và các sơ đồ hiện có, không phải mô hình trích xuất từ code. Tên API, service và store là tên logic; chưa chốt công nghệ triển khai hoặc transaction boundary.

Các luồng giữ các ràng buộc chính: scope Tenant/Workspace; maker exclusion; duyệt đúng tier; artifact bất biến; Shadow không đổi production response; version pin chính xác hoặc REST 412/gRPC tương đương; snapshot cố định; runtime không gọi Control Plane đồng bộ; bảo vệ evidence trước persistence; lỗi trace quan sát được; convergence <=2 giây từ publication event.

Các request quản trị, review, truy vấn và sandbox là những lần tương tác riêng. Đặt chúng trong cùng một sơ đồ không có nghĩa giữ kết nối HTTP mở để chờ người duyệt. Build được thể hiện như bước logic sau khi đủ điều kiện; triển khai có thể lập lịch build theo ADR.

Sơ đồ 04 lược phần load artifact thành thông điệp delivery qua local artifact management; xem sơ đồ 05 để biết thứ tự fetch/validate/eligible. Sơ đồ 07 bổ sung guard không lưu evidence nếu bước bảo vệ dữ liệu thất bại, nhằm bảo toàn yêu cầu không lưu plaintext nhạy cảm; cơ chế phục hồi vẫn cần thiết kế riêng.

Chi tiết xử lý lỗi và các nhánh đầy đủ hơn nằm ở [bộ sequence diagram](../sequence-diagrams/README.md). Các quyết định chưa chốt gồm thuật toán Canary/cohort precedence, approval reuse sau nâng tier, lịch chạy Active baseline khi Shadow/Canary cùng bật, cơ chế retry/delivery và trace backpressure.

## Xuất hình

Mở SVG bằng trình duyệt để phóng to hoặc mở `.puml` bằng extension PlantUML trong VS Code rồi nhấn `Alt+D`.

```powershell
java -jar path/to/plantuml.jar -charset UTF-8 -tsvg -o previews communication-diagrams/*.puml
java -jar path/to/plantuml.jar -charset UTF-8 -tpng -o previews communication-diagrams/*.puml
```

PNG cùng tên được đặt trong `previews/` để chèn vào báo cáo. Việc render kiểm tra cú pháp; không thay thế kiểm thử nghiệp vụ và NFR của hệ thống thực tế.
