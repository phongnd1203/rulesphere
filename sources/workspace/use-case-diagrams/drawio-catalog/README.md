# RuleSphere - Business Rule Management Platform

Đây là bộ Draw.io cập nhật theo **catalog mới nhất bạn gửi**, gồm **17 module A–Q**, **177/177 use case có mã**, 5 main actors, 4 supporting actors và đúng 2 abstract actors: `Platform User`, `External System`.

Nguồn được lưu nguyên văn tại [source-catalog.md](source-catalog.md). Đây là **proposed use-case baseline**, không mặc định là requirement đã được phê duyệt. Catalog mới là nguồn cấu trúc và phạm vi; DFD trước đó tiếp tục là bối cảnh hệ thống, không giới hạn các chức năng mà catalog mới đã bổ sung.

## Mở từ đây

- [00 — System Overview](00_System_Overview.drawio): 25 use case tổng quan trên một diagram, chia vùng theo nhóm chức năng.
- [01 — Actor Model](01_Actor_Model.drawio): hai cây kế thừa actor, không tạo quan hệ kế thừa giữa Administrator và Operations.
- [02 — Cross-Cutting](02_Cross_Cutting.drawio): authorization, audit và version resolution dùng chung.

Mỗi file `.drawio` chỉ chứa **một diagram duy nhất**. Toàn bộ use case của module nằm trên cùng canvas; mỗi actor và mỗi mã use case chỉ xuất hiện một lần trong module. Mở bằng draw.io Desktop hoặc diagrams.net; hình, nhãn và đường nối đều chỉnh sửa được. Thư mục `previews/` chỉ chứa **một ảnh PNG tương ứng mỗi file**, không có PDF hoặc ảnh riêng theo trang. Tên hệ thống trên mọi sơ đồ là **RuleSphere - Business Rule Management Platform**.

Canvas được thu nhỏ khoảng **28% mỗi chiều**, giảm khoảng **48% diện tích**; chữ tên use case vẫn giữ cỡ 14. Diagram chỉ hiển thị tên actor/use case, không hiện ID hoặc `«abstract»`. Mã gốc vẫn được giữ trong metadata và CSV để truy vết. [size-validation.json](size-validation.json) ghi kích thước trước/sau.

Đường nối ưu tiên thẳng; chỉ dùng đoạn gấp chéo để tránh hình. Các đường có thể giao nhau nhưng không đi chung một đoạn. Nhãn quan hệ nằm ngay trên connector, không lệch xa đường nối. Connector chỉ hiển thị `«include»` hoặc `«extend»`; phần điều kiện được giữ trong bảng quan hệ, không in lên diagram. [routing-validation.json](routing-validation.json) ghi kết quả kiểm tra hình học; [routing.py](routing.py) chứa logic bố trí đường nối.

## Module

| Module | Draw.io | Preview |
|---|---|---|
| A — Identity & Access Management | [Mở](A_Identity_Access_Management.drawio) | [PNG](previews/A_Identity_Access_Management.png) |
| B — Decision Project & Asset Management | [Mở](B_Decision_Project_Asset_Management.drawio) | [PNG](previews/B_Decision_Project_Asset_Management.png) |
| C — Decision Modeling & Rule Authoring | [Mở](C_Decision_Modeling_Rule_Authoring.drawio) | [PNG](previews/C_Decision_Modeling_Rule_Authoring.png) |
| D — Data Contract Management | [Mở](D_Data_Contract_Management.drawio) | [PNG](previews/D_Data_Contract_Management.png) |
| E — Validation & Testing | [Mở](E_Validation_Testing.drawio) | [PNG](previews/E_Validation_Testing.png) |
| F — Version & Change Management | [Mở](F_Version_Change_Management.drawio) | [PNG](previews/F_Version_Change_Management.png) |
| G — Review & Approval Governance | [Mở](G_Review_Approval_Governance.drawio) | [PNG](previews/G_Review_Approval_Governance.png) |
| H — Build & Artifact Management | [Mở](H_Build_Artifact_Management.drawio) | [PNG](previews/H_Build_Artifact_Management.png) |
| I — Environment & Deployment Management | [Mở](I_Environment_Deployment_Management.drawio) | [PNG](previews/I_Environment_Deployment_Management.png) |
| J — Progressive Delivery | [Mở](J_Progressive_Delivery.drawio) | [PNG](previews/J_Progressive_Delivery.png) |
| K — Decision Execution | [Mở](K_Decision_Execution.drawio) | [PNG](previews/K_Decision_Execution.png) |
| L — Explainability & Decision Trace | [Mở](L_Explainability_Decision_Trace.drawio) | [PNG](previews/L_Explainability_Decision_Trace.png) |
| M — Simulation & Impact Analysis | [Mở](M_Simulation_Impact_Analysis.drawio) | [PNG](previews/M_Simulation_Impact_Analysis.png) |
| N — Runtime Operations & Observability | [Mở](N_Runtime_Operations_Observability.drawio) | [PNG](previews/N_Runtime_Operations_Observability.png) |
| O — Audit & Compliance | [Mở](O_Audit_Compliance.drawio) | [PNG](previews/O_Audit_Compliance.png) |
| P — Automation & CI/CD Integration | [Mở](P_Automation_CI_CD_Integration.drawio) | [PNG](previews/P_Automation_CI_CD_Integration.png) |
| Q — Platform Administration | [Mở](Q_Platform_Administration.drawio) | [PNG](previews/Q_Platform_Administration.png) |

## Actor và quan hệ UML

`Platform User` là cha của Author, Reviewer / Approver, Platform Administrator và Operations / SRE. Các use case chung chỉ nối với actor cha. `External System` là cha của Consumer, IAM, CI/CD, Observability và SIEM; đây là phân loại, không cấp chung quyền gọi API. Decision Consumer vẫn là **main actor**.

Các module tham chiếu cây kế thừa trong file 01, không vẽ lại toàn bộ actor hierarchy trong mỗi module. Không bổ sung `Decision API Consumer` vì catalog chưa xác nhận CI/CD và Consumer dùng chung security contract.

- **Association:** đường liền không mũi tên, dùng cho mục tiêu actor khởi tạo hoặc hành vi external service hỗ trợ. Không expose mọi bước nội bộ ra actor.
- **Include:** nét đứt từ base đến hành vi bắt buộc. Không biểu diễn thứ tự workflow; một lỗi kết thúc luồng có thể ngăn các bước thành công phía sau.
- **Extend:** nét đứt từ phần mở rộng về base, chỉ ghi `«extend»`. Extension point và điều kiện được giữ tại `relationships.csv`. Các nhánh approve/reject/rework loại trừ nhau trong một quyết định review.
- **Generalization:** tam giác rỗng hướng từ use case/actor chuyên biệt về cha. CRUD dùng generalization khi là những biến thể của mục tiêu tổng quát.
- **Ellipse xanh:** mục tiêu trừu tượng. Một mã được tham chiếu ở nhiều module vẫn là cùng use case, không phải bản sao nghiệp vụ.

Runtime, distributor và policy engine nằm trong RuleSphere, không phải actor ngoài. Audit/SIEM và Observability có association nhận dữ liệu, không đồng nghĩa chúng khởi tạo hành vi xuất bản. Không chuyển sơ đồ lifecycle thành BPM orchestration.

## Các điểm được làm rõ khi chuyển catalog thành UML

Giữ nguyên 177 mã và tên trong các bảng. Những điểm dưới đây và [module-notes.md](module-notes.md) giải thích cách diễn giải UML. Ghi chú dài được tách khỏi sơ đồ để diagram gộp dễ đọc:

1. **Archive project:** không nối Author với cha `Manage Decision Project` vì sẽ làm actor đó kế thừa khả năng archive. Author nối Create/Update, Administrator nối Archive; cả ba vẫn generalize về DAM-01.
2. **Rollback:** giữ `DEP-07 extend DEP-05` cho phục hồi trong vòng đời deployment. Thêm association trực tiếp với Operations để hỗ trợ một yêu cầu rollback độc lập sau đó. Việc một hành vi “không bắt buộc” tự nó chưa đủ để kết luận quan hệ extend.
3. **Active và pinned version:** EXE-01 include `UC-X04 Resolve Decision Version`; EXE-04 và pinned resolver là các chiến lược chuyên biệt. EXE-12 vẫn generalize EXE-01 và chọn exact version. Không bắt pinned execution phải resolve active version cùng lúc. Đây là tinh chỉnh quan hệ include trực tiếp EXE-01 → EXE-04 của bản đề xuất.
4. **View Runtime Node Status:** ADM-10 generalize về ADM-07, thay cho include toàn bộ Manage Runtime Nodes. Xem trạng thái không chạy hành vi register/deregister.
5. **Enforce Approval Policy / Authorize Access / Validate Client Credential:** là các hành vi nội bộ dùng lại. Admin cấu hình policy; người dùng/client là đối tượng được kiểm tra. Chỉ vẽ IdP là actor hỗ trợ authentication, không vẽ hệ thống tự làm actor của mình.
6. **Export Audit Events include Record Audit Event:** ghi nhận chính lần export. Không hiểu là ghi lại các sự kiện lịch sử trước khi xuất chúng.
7. **Publish include Build:** giữ nguyên nghĩa “build-and-publish” của catalog. Một API chỉ publish artifact có sẵn cần use case/contract riêng nếu được yêu cầu sau này.
8. **View/restore và evidence:** quyền đọc chung từ Platform User không tự cấp quyền restore draft hoặc xem dữ liệu nhạy cảm. Actor của từng optional evidence view vẫn được giữ rõ.

Các quan hệ bổ sung như Export Contract extend View Contract, Create/Edit generalize Author Model, client authentication dùng lại IAM-10 được liệt kê trong [relationships.csv](relationships.csv). Chúng là phân rã UML đề xuất, không tự trở thành yêu cầu đã chốt.

## Mã và đối chiếu

- [catalog-traceability.csv](catalog-traceability.csv): đủ 177 mã gốc → file, tên và actor gốc trong catalog.
- [relationships.csv](relationships.csv): source/target, loại quan hệ, điều kiện và vị trí.
- [supporting-use-cases.csv](supporting-use-cases.csv): mã `AUX-*` cho hành vi có tên trong phần quan hệ nhưng không có mã bảng, hoặc phần làm rõ UML.
- `UC-X03 Validate Decision` là alias của **VAL-01**, không tạo hai use case nghiệp vụ khác nhau. “Validate Decision Model” trong quan hệ AUT-01 cũng tham chiếu VAL-01.
- `UC-01–25` chỉ là mã tổng quan theo mục 21 của catalog; không thay thế mã chi tiết `IAM-*`, `DAM-*`… hoặc mã của bộ SRS cũ.
- Các mã trùng nghĩa giữa module, ví dụ `AUD-10 / ADM-05`, `DEP-04 / ADM-06`, được giữ nguyên theo catalog; đây là các góc nhìn của cùng capability, không yêu cầu hai implementation độc lập.

## Kiểm tra và tái tạo

```powershell
python -B use-case-diagrams/drawio-catalog/generate.py
python -B use-case-diagrams/drawio-catalog/render.py
```

Generator kiểm tra coverage đủ 177 UC, mỗi file có đúng một diagram, không trùng actor/use case trong module, cell IDs, endpoint và giới hạn canvas. [validation.json](validation.json) ghi kết quả. Render script dùng draw.io Desktop xuất 20 file thành đúng 20 PNG cùng tên; không có PDF hoặc ảnh lẻ theo trang. Kết quả ở [render-validation.json](render-validation.json). Nội dung và quan hệ được khai báo tại [catalog_model.py](catalog_model.py).

Chạy lại generator sẽ ghi đè file được sinh. Nếu chỉnh trực tiếp bằng Draw.io, lưu bản riêng hoặc cập nhật generator trước. `source-catalog.md` là bản nguồn nguyên văn, không sửa tên trong trích dẫn lịch sử.
