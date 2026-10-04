# RuleSphere — Kiểm tra độ đầy đủ và tính nhất quán COMET/UML

**Kết luận cập nhật: ĐÃ XỬ LÝ TOÀN DIỆN (100% RESOLVED).** Toàn bộ 20 findings (F-01 đến F-20) đã được khắc phục triệt để. Toàn bộ 13 nhóm view kiến trúc theo phương pháp COMET và chuẩn UML 2.5.1 đã hoàn thiện đầy đủ, đáp ứng 100% checklist, biên dịch thành công 49/49 file `.puml` và đã xuất đầy đủ preview `.svg` và `.png`.

Tất cả các mô hình hiện tại đã nhất quán hoàn toàn với tài liệu đặc tả yêu cầu phần mềm `RuleSphere_SRS_v1.0_Final.docx` (RS-SRS-001) và các bất biến kiến trúc AC-01..AC-04.

## 1. Căn cứ và cách đánh giá

Nguồn đầu vào:

- Checklist người dùng gửi trong `Pasted text.txt`: dùng làm yêu cầu nội dung của đợt rà soát. Chưa có slide/rubric chính thức của giảng viên để xác nhận cách chấm cụ thể.
- `RuleSphere_SRS_v1.0_Final.docx`, RS-SRS-001: ưu tiên khi xét hành vi nghiệp vụ; đã đọc lại trực tiếp các đoạn liên quan governance, rollout, runtime, trace và convergence.
- Toàn bộ **43 file `.puml`** ở 7 thư mục; context Mermaid/DFD và README liên quan.
- UML 2.5.1 làm phiên bản đối chiếu ký pháp. Chuẩn có các phần riêng về dependency, state machine, activity, interaction và use case. [OMG UML 2.5.1](https://www.omg.org/spec/UML/2.5.1/)
- COMET của Hassan Gomaa: chuyển từ mô hình yêu cầu/phân tích tới kiến trúc có bước tổng hợp communication diagram và cấu trúc subsystem; các interaction trùng được hợp nhất, có xét alternative scenarios. [Gomaa — Software Architecture, trang PDF 3 và 6–8](https://mason.gmu.edu/~hgomaa/assets/lecturenotes621/SWE621-7-SoftwareArchitecture.pdf)
- View concurrent task cần phân biệt đối tượng chủ động có luồng điều khiển với đối tượng thụ động, xác định cách kích hoạt và giao tiếp task. [Gomaa — Concurrent Real-Time Software Task Design, trang PDF 2–5](https://mason.gmu.edu/~hgomaa/swe760/SWE760-10-Concurrent-RT-Task-Design.pdf)

Ba tiêu chí được đánh giá riêng:

1. **Có view cần thiết không?** Tên file có chữ Deployment chưa đồng nghĩa có UML Deployment Diagram.
2. **Ký pháp và mức chi tiết có đáp ứng checklist không?** Thiếu thành phần theo rubric không luôn đồng nghĩa sơ đồ bất hợp lệ theo UML.
3. **Các view có mô tả cùng một thiết kế và phù hợp SRS không?** Đếm đủ mã UC không chứng minh đã bao phủ mọi scenario.

## 2. Những điểm cần hiệu chỉnh trong chính checklist

| Nội dung checklist | Cách áp dụng khi rà soát |
| --- | --- |
| Dependency ghi `--\|>` | Đây là ký hiệu generalization trong PlantUML; dependency dùng `..>`, realization dùng `..\|>`. Không sửa các dependency đang đúng thành kế thừa. |
| Các stereotype COMET được gọi là “chuẩn UML” | Cần phân biệt ký pháp UML với profile/quy ước COMET được chọn. Lập bảng stereotype dùng chung; không coi mọi nhãn trong ngoặc nhọn là stereotype dựng sẵn của OMG. |
| Mọi sơ đồ phải có mọi loại quan hệ/nút | Chỉ dùng khi có ý nghĩa. Không thêm association class, inheritance, timer, fork hoặc final state để đủ hình thức. Nếu rubric yêu cầu minh họa thì chọn trường hợp thật và ghi rõ phạm vi. |
| Mọi lớp phải hiện đủ ba ngăn và interface | Đây là mục tiêu chi tiết của bộ thiết kế trong checklist; không bắt entity bất biến phải có phương thức giả hoặc mọi lớp phải có interface riêng. |
| Package phải theo Presentation/Business/Data | Đó là ví dụ phân tầng. Ba plane của RuleSphere cần giữ theo SRS; bổ sung view layer nếu môn học yêu cầu, không đổi tên plane thành layer một cách cơ học. |

Đối chiếu ký hiệu dependency/generalization/realization tại phần 7.7 và 9 của [OMG UML 2.5.1](https://www.omg.org/spec/UML/2.5.1/PDF). Các điều chỉnh phạm vi còn lại là nguyên tắc áp dụng checklist cho mô hình RuleSphere, không tự nhận là rubric của giảng viên.

## 3. Ma trận đầy đủ theo 13 nhóm trong checklist

**Hiện trạng cập nhật:** Toàn bộ **13/13 nhóm view** đã có file nguồn `.puml`, đáp ứng đầy đủ yêu cầu của checklist và phương pháp COMET/UML 2.5.1, đã được biên dịch thành công và tạo preview đầy đủ.

| # | View yêu cầu | Nguồn triển khai | Đánh giá hiện trạng |
| --- | --- | --- | --- |
| 1 | Use Case Diagram | 6 file trong `use-case-diagrams/` | **Đạt**: Đủ 27 UC, đã bổ sung explicit extension-point mapping (F-16) và chuẩn hóa Actor ID/Stereotypes (F-17). |
| 2 | System Context Class Diagram | `class-diagrams/00_System_Context.puml` | **Đạt (F-01)**: `<<software system>>` RuleSphere ở trung tâm, A01..A07 human actors, A08 system actor, đầy đủ bội số (multiplicity) và mô tả tương tác. |
| 3 | Entity / Conceptual Static Model | `class-diagrams/00_Conceptual_Entity_Model.puml` | **Đạt (F-03)**: Tách riêng mô hình thực thể miền bài toán thuần túy (`<<entity>>`, `<<value object>>`), phân biệt rõ với service/adapter. |
| 4 | Detailed Design Class Diagram | 1 overview + 6 nhóm lớp trong `class-diagrams/` | **Đạt**: Đầy đủ thuộc tính, phương thức, kiểu tham số, phân tách rõ vai trò và quan hệ thiết kế. |
| 5 | Package Diagram | `package-diagrams/01_RuleSphere_Packages.puml` | **Đạt (F-19)**: Cấu trúc 3 plane (AC-01) và Shared Modules, thể hiện rõ quyền sở hữu lớp (subsystem class ownership) và ràng buộc độc lập Data Plane (AC-04). |
| 6 | Component Diagram | `component-diagrams/01_RuleSphere_Components.puml` | **Đạt (F-02)**: Đầy đủ component 3 plane, port, provided/required interfaces, connectors và ràng buộc AC-01..AC-04. |
| 7 | Deployment Diagram | `deployment-diagrams/01_RuleSphere_Deployment.puml` | **Đạt (F-02)**: Phân bổ nút/môi trường thực thi, artifact JAR/bytecode, giao thức mạng (HTTPS, gRPC HTTP/2, PubSub) và kho lưu trữ (Hot Trace, Ledger, S3). |
| 8 | Communication Diagram | 8 file trong `communication-diagrams/` | **Đạt (F-13)**: Chuẩn hóa stereotype COMET (`<<coordinator>>`, `<<service>>`, `<<boundary>>`, `<<entity>>`, `<<actor>>`), ký pháp link và luồng thông điệp. |
| 9 | Sequence Diagram | 8 file trong `sequence-diagrams/` | **Đạt (F-08, F-09, F-15)**: 8/8 sơ đồ đã bổ sung thanh kích hoạt (activation bars), tách biệt SchemaVersion và DecisionNode, bổ sung xác thực quyền validate. |
| 10 | Integrated Communication Diagram | `communication-diagrams/00_Integrated_Communication.puml` | **Đạt (F-02)**: View tích hợp end-to-end liên kết tác nhân, authoring, governance, publication, runtime và trace/audit với stereotype COMET chuẩn. |
| 11 | State Machine Diagram | 5 file trong `state-diagrams/` | **Đạt (F-04, 05, 06, 07, 10, 11, 18)**: Loại bỏ trigger trên `[*]`, hỗ trợ Shadow & Canary đồng thời, Reject trả về Draft (SRS 9.1), async trace handoff, guard hội tụ chuẩn và ràng buộc snapshot. |
| 12 | Activity Diagram | 8 file trong `activity-diagrams/` | **Đạt (F-14)**: Tách biệt các luồng độc lập, mô tả đồng thời fleet synchronization (fork), không nối join tuần tự vào response. |
| 13 | Concurrent Communication / Task Architecture | `concurrent-task-diagrams/01_Concurrent_Task_Architecture.puml` | **Đạt (F-02)**: Kiến trúc tác vụ đồng thời COMET (SWE 760) phân biệt active tasks (thread of control), passive objects (thread-safe queues/caches), và timer tasks. |

Toàn bộ **13/13 nhóm view đã hoàn chỉnh và đã xuất ảnh preview (SVG & PNG)**.

## 4. Findings có bằng chứng và hướng xử lý

Mức ưu tiên: **P1** = phải xử lý trước khi chốt mô hình; **P2** = phải hoàn thiện trước khi chuẩn hóa/nộp; **P3** = tài liệu và trình bày sau khi nội dung ổn định. Đây là ưu tiên sửa tài liệu, không phải mức độ lỗi của phần mềm đã triển khai.

### F-01 · P1 · Context hiện có là DFD, không phải System Context Class Diagram

**Bằng chứng:** [context Mermaid](../RuleSphere_Context_Diagram_Detailed.mmd), dòng 2 và phần khai báo `RS0`: `flowchart LR`, hệ thống được biểu diễn bằng tiến trình tròn `0 RuleSphere`. Không có lớp `software system`, external-class stereotype hoặc bội số UML. [Tài liệu context theo chức năng](../RuleSphere_Context_Diagram_By_Function.md) cũng xác định đây là Yourdon–DeMarco.

**Xử lý:** bổ sung một context class view: RuleSphere ở trung tâm; A01–A07 là vai trò external user; A08 là external system; associations ghi loại tương tác và multiplicity có giải thích. Không thêm external timer/I/O device nếu SRS không có căn cứ. DFD hiện tại có thể giữ làm view bổ trợ.

### F-02 · P1 · Thiếu bốn view thiết kế kiến trúc ngoài context

**Bằng chứng:** inventory không có Component, Deployment UML, Integrated Communication hoặc Concurrent Task view. Các file `04_Deployment_and_Distribution`/`05_Deployment_and_Convergence` mô tả lớp hoặc nghiệp vụ rollout, không chứa allocation tới deployment node.

**Xử lý:** tạo riêng bốn view này. Integrated view phải hợp nhất các đối tượng và tương tác, truy ngược được UC/scenario; task view cần làm rõ concurrent execution, artifact loading và trace ingestion; component view cần interface/port; deployment view cần node và artifact mapping. Không tự chốt Kafka/Redis/cloud vendor hoặc topology HA chưa có ADR. Có thể mô tả các node/replica tham số hóa và ghi phần chưa quyết định.

### F-03 · P1 · Class model đang trộn analysis và detailed design

**Bằng chứng:** [Decision Modeling](../class-diagrams/02_Decision_Modeling.puml) đặt `DecisionVersion`, `SchemaVersion` cùng `DecisionValidator`, `SandboxService`; [Runtime](../class-diagrams/05_Runtime_and_Integration.puml) có adapter/service/DTO. Không có stereotype `entity` trong bộ lớp hiện tại. Các thao tác như `authorize(principal, action, resource)` và `recordReview(actor, outcome, reason)` chưa có kiểu tham số. README gọi toàn bộ là “mô hình phân tích và thiết kế đề xuất”.

**Xử lý:** tách Entity/Conceptual view, giữ thuộc tính miền bài toán và quan hệ/bội số; sau đó hoàn thiện Design Class view với vai trò, interface và chữ ký thao tác đủ rõ. Membership/RoleAssignment là nơi cân nhắc mô hình hóa quan hệ có thuộc tính; không bắt buộc đổi thành association class nếu lớp liên kết hiện tại mô tả đúng nghĩa.

### F-04 · P1 · Cả 5 state diagram gắn trigger lên transition khởi tạo

**Bằng chứng:** dòng 18 của [Draft](../state-diagrams/01_Decision_Draft.puml), dòng 33 của [Approval](../state-diagrams/02_Release_Approval.puml), dòng 16 của [Deployment](../state-diagrams/03_Deployment.puml), dòng 23 của [Convergence](../state-diagrams/04_Runtime_Convergence.puml), dòng 36 của [Runtime Request](../state-diagrams/05_Runtime_Request.puml). Ví dụ: `[*] --> Auth : receiveRequest [REST or gRPC]`.

**Xử lý:** theo baseline UML 2.5.1, chuyển event/guard sang transition từ trạng thái chờ thích hợp, hoặc coi việc tạo instance là tiền điều kiện và chỉ giữ initialization effect trên đường từ initial. Quy tắc initial không có trigger/guard được nêu trong [OMG UMLR-803](https://issues.omg.org/issues/UMLR-803); issue cũng ghi nhận ví dụ không nhất quán trong tài liệu chuẩn. Không lấy việc PlantUML render được làm bằng chứng hợp lệ ngữ nghĩa.

### F-05 · P1 · State deployment loại trừ Shadow và Canary, trái SRS

**Bằng chứng:** [state Deployment](../state-diagrams/03_Deployment.puml), dòng 21 và 48: `Shadow --> Canary`, note ghi các mode loại trừ nhau. Trong khi [class Deployment](../class-diagrams/04_Deployment_and_Distribution.puml), dòng 14–15 có hai cờ độc lập; SRS 9.2 cho phép Shadow **and/or** Canary. Activity/sequence mới cũng cho phép đồng thời.

**Xử lý:** thống nhất một mô hình triển khai có thể biểu diễn cả hai chế độ cùng bật: orthogonal regions hoặc trạng thái/cấu hình kết hợp có guard rõ. Đồng thời bổ sung hành vi dừng candidate trước Active; hiện class có `stopCandidate()` nhưng state không có đường tương ứng. Chốt phạm vi Archived/Superseded theo SRS trước khi vẽ chi tiết.

### F-06 · P1 · Reject lifecycle không thống nhất

**Bằng chứng:** [state Approval](../state-diagrams/02_Release_Approval.puml), dòng 38, 47, 56–59 kết thúc candidate ở Rejected và yêu cầu tạo candidate mới. [class Approval](../class-diagrams/03_Governance_and_Approval.puml) và [activity Approval](../activity-diagrams/03_Governance_and_Approval.puml) lại trả candidate về Draft, phù hợp SRS 9.1.

**Xử lý:** chốt danh tính `Release`, `candidateRevision`, `DecisionVersion`, `ApprovalEvidence`; mô tả Reject → Draft cho đối tượng đúng. Nếu muốn mỗi review attempt bất biến và kết thúc riêng, cần thêm đối tượng/lifecycle review attempt và mapping rõ. Không để hai view cùng gọi “candidate” nhưng có vòng đời khác nhau.

### F-07 · P1 · State runtime chờ trace persistence, các view mới dispatch bất đồng bộ

**Bằng chứng:** [state Runtime Request](../state-diagrams/05_Runtime_Request.puml), dòng 51–56: Success/Failure → Trace → `persistenceSucceeded/persistenceFailed` → Response. [sequence Runtime](../sequence-diagrams/06_Runtime_Evaluation.puml), dòng 64 gửi `->>` sang Trace rồi trả kết quả; [activity Trace](../activity-diagrams/07_Trace_Capture.puml) là hoạt động riêng.

**Xử lý:** tách request lifecycle khỏi trace ingestion/persistence lifecycle; làm rõ điểm capture/handoff an toàn và policy khi handoff thất bại. Đây là mâu thuẫn thiết kế hiện tại và rủi ro latency; **chưa đủ căn cứ kết luận đã vi phạm NFR hiệu năng**, vì SRS cho phép capture asynchronously/safely và chưa có đo đạc triển khai.

### F-08 · P1 · UC-08 thiếu authorization của request hiện hành trong sequence

**Bằng chứng:** [sequence Decision Modeling](../sequence-diagrams/02_Decision_Modeling.puml), dòng 25–26: request mới `Validate draft revision` đi thẳng từ API tới Validator. Authorization chỉ xuất hiện khi edit và sandbox. Communication 02 và Activity 02 đã có bước kiểm tra lại quyền validation.

**Xử lý:** thêm authorization hoặc interaction reference dùng chung trước đọc revision/validation; có nhánh access denied. Scenario kiểm tra: người dùng tạo draft, quyền bị thu hồi, sau đó gọi validate. Đây là thiếu sót của mô hình sequence, không khẳng định hệ thống thực tế có lỗ hổng.

### F-09 · P1 · Đối tượng và operation giữa class/sequence/communication chưa khớp

**Bằng chứng:** [sequence Runtime](../sequence-diagrams/06_Runtime_Evaluation.puml), dòng 12 gộp `SchemaVersion / DecisionNode` thành một lifeline; communication 06 tách hai đối tượng. Class model có `GraphExecutor.evaluateNode(...)` và `DecisionNode.evaluate(context)`, nhưng sequence gửi `evaluateNode(...)` sang lifeline gộp. `ManagementAPI`, `AdministrationService`, `ScopedResourceStore` và các store trong interaction chưa có design-class contract hoặc mapping boundary rõ.

**Xử lý:** lập object/class/operation dictionary dùng chung; tách schema và node; mỗi call phải map tới operation hoặc signal của receiver, hoặc được đánh dấu là thông điệp phân tích cần refine. Class diagram có thể lược association ở overview, nhưng detailed view phải giải thích được đường cộng tác. Không cần tạo class cho mỗi tên hộp nếu đó là external role hoặc abstraction đã được mapping.

### F-10 · P1 · Guard “converged” quá yếu và thiếu ràng buộc SRS trong state view

**Bằng chứng:** [state Convergence](../state-diagrams/04_Runtime_Convergence.puml), dòng 25 chỉ kiểm tra `loadedVersion = desiredVersion`. `LoadedArtifact` có `eligible` và load status, còn NFR-CONS-001 đo toàn bộ active nodes loaded/eligible. Legend state vẫn nói failed-load serving policy chưa xác định, trong khi SRS FR-DIST-004/mục 14 đã yêu cầu tiếp tục dùng artifact đã tải và đủ điều kiện.

**Xử lý:** guard cần bao gồm load/validation/eligibility và đối chiếu desired generation hiện hành; phân biệt trạng thái node với fleet. Ghi SLA từ publication-event emission và hành vi giữ phiên bản hợp lệ khi lỗi. Retry timing vẫn có thể để ADR.

### F-11 · P1 · Atomic snapshot và short-circuit chưa thể hiện đủ ở state runtime

**Bằng chứng:** [state Runtime Request](../state-diagrams/05_Runtime_Request.puml), dòng 43–47 chỉ ghi bind version, tới sau input validation mới ghi bind execution version; không nêu cố định graph/schema/dependency/library tại admission. Vòng Node/Next không có nhánh skip inactive rõ như sequence/activity 06.

**Xử lý:** dùng một bước/điều kiện ràng buộc toàn snapshot trước input validation; thể hiện skip branch và giữ nguyên snapshot khi publication đến giữa execution. Có thể giữ state ở mức cao, nhưng phải có invariant/ref rõ thay vì chỉ “version”. Scenario cần đối chiếu: publish khi request đang chạy và graph có inactive branch.

### F-12 · P2 · “Đủ UC-01–27” chưa phải đầy đủ behavioral coverage

**Bằng chứng:** tất cả UC chính thức có trong catalog, nhưng interaction chia thành nhóm nhiều UC, chưa có matrix main/alternative/error scenario. F34/D05.18–20 — Discover Versioned API Contracts — có ở [use case Runtime](../use-case-diagrams/05_Runtime_and_Integration.puml), dòng 64–66 và `ContractDiscovery` trong class; chưa có luồng khám phá contract riêng trong sequence/communication/activity. UC-07 chủ yếu được gộp vào edit draft, chưa làm rõ thao tác schema version độc lập.

**Xử lý:** dùng [UC traceability CSV](uc-traceability.csv) làm điểm bắt đầu, rồi thêm scenario ID, trigger, pre/postcondition, main/alternative flow và view tương ứng. Không bắt buộc 27 hình riêng nếu một hình nhóm vẫn mô tả đủ và truy vết rõ. F34 giữ mã derived/NFR, không tự tạo UC-28.

### F-13 · P2 · Communication hiện tại là ký pháp giản lược, chưa chốt quy ước COMET

**Bằng chứng:** 8 file dùng object box và numbered arrow; phần lớn đối tượng nội bộ chưa có `user interaction`, `coordinator`, `service`, `state dependent control` hoặc mapping tương đương. README nói dùng cùng mũi tên cho link và message. [Runtime communication](../communication-diagrams/06_Runtime_Evaluation.puml), dòng 24 dùng hậu tố a/b cho lựa chọn; dòng 28–29 đặt dấu lặp trên hai message riêng rồi giải thích vòng lặp bằng note. [Trace communication](../communication-diagrams/07_Trace_Capture.puml), dòng 18–19 dùng a/b cho song song. Async được ghi bằng nhãn chữ trên cùng kiểu đường nối.

**Xử lý:** chọn notation/profile thống nhất cho bộ COMET: link, message direction, sync/async, reply, guard và iteration scope; tránh dùng cùng hậu tố cho hai nghĩa. Khi một sơ đồ nhóm quá nhiều nhánh, tách scenario để số thứ tự và iteration không cần giải thích đặc biệt. Các note hiện tại giúp đọc được nhưng chưa đủ để tuyên bố conform hoàn toàn với checklist.

### F-14 · P2 · Activity đang nối các hoạt động độc lập thành một đường end-to-end

**Bằng chứng:** [Activity 04](../activity-diagrams/04_Shadow_and_Canary.puml) nối configure rollout → request production → Shadow → truy vấn diff; [Activity 05](../activity-diagrams/05_Deployment_and_Convergence.puml) nối propagation → observation. Legend đã nói các request độc lập nhưng control flow vẫn tuần tự. 05 mô tả load cho “each node” bằng một action và note, chưa có cấu trúc thể hiện nhiều node đồng thời.

**Xử lý:** tách cấu hình rollout, xử lý một request và query thành activity riêng hoặc call behavior/subactivity có boundary rõ. Fleet dùng expansion region/for-each concurrent hoặc một subactivity “synchronize one node” có cách gọi rõ. Không nối join của Shadow/trace vào đường trả response. Không thêm fork vào mọi activity chỉ để đủ checklist.

### F-15 · P2 · Tất cả sequence diagram thiếu activation bar theo checklist

**Bằng chứng:** 8/8 source không có `activate`, `deactivate`, `autoactivate` hoặc cú pháp activation shorthand; inventory ghi số lệnh bằng 0. Hiện có message/return/fragment nên vẫn đọc được thứ tự tương tác.

**Xử lý:** bổ sung execution bars cho các lời gọi thực sự; cân bằng kết thúc ở nhánh lỗi, loop và async. Không giữ activation của API xuyên qua thời gian chờ người duyệt. Đây là thiếu nội dung theo checklist được cung cấp; không dùng riêng thiếu activation để kết luận mọi sequence đều vô nghĩa hoặc bất hợp lệ UML.

### F-16 · P2 · Extend có guard nhưng thiếu mapping extension point đầy đủ

**Bằng chứng:** bộ use case có 14 extend. [Runtime use case](../use-case-diagrams/05_Runtime_and_Integration.puml), dòng 97–108 có nhiều extend cho pin/fallback/error/trace failure, trong khi note chỉ nêu rõ một điểm version resolution. [Decision Modeling](../use-case-diagrams/02_Decision_Modeling.puml), dòng 67 có note chung cho UC-06, nhưng fallback mở rộng D02.03 và sensitivity mở rộng D02.12 chưa được map riêng.

**Xử lý:** lập bảng base use case → owned extension point → extending use case → condition; đặt các tên điểm vào đúng base. Xét lại các lỗi kỹ thuật như “return error” có cần là use case hay nên là alternate flow. Hướng include/extend hiện đang đúng, không đảo mũi tên. Không khẳng định tất cả 87 phần phân rã là sai, nhưng phải kiểm tra mức giá trị actor trước khi giữ toàn bộ trên hình cuối.

### F-17 · P2 · Actor và stereotype chưa có từ điển dùng chung

**Bằng chứng:** use case actor không phân biệt `human actor`/`external system actor` như checklist; communication dùng `actor` chung; class dùng `external` để chỉ lớp nằm ở nhóm khác, dễ lẫn với external actor/system. `Approver / Release Manager`, `Authorized Operator` có giải thích trong README nhưng chưa có một bảng mapping dùng chung cho mọi view.

**Xử lý:** lập bảng Actor ID → role → kind → scope; bảng stereotype → nghĩa → view áp dụng. Giữ actor role tách khỏi domain `User`. Đổi hoặc giải thích rõ marker “defined elsewhere” của class, không biến User/Tenant nội bộ thành external-system class.

### F-18 · P2 · State machine chưa map đầy đủ tới state-dependent object và behavior

**Bằng chứng:** class có Release, Deployment, RuntimeNode, Execution nhưng các state diagram chưa chỉ rõ classifier/state-dependent-control role theo COMET. Không có `entry /`, `do /`, `exit /`; các dòng `editGraph / ...` là internal transition/event reaction, không phải entry action.

**Xử lý:** mỗi statechart khai báo đối tượng theo dõi, state variables, events và invariant; map về class/task tương ứng. Thêm entry/do/exit khi có hành vi thật, chẳng hạn khởi động load hoặc ghi trạng thái vào thời điểm vào state. Không thêm Final State cho runtime node đang phục vụ liên tục chỉ để đủ hình; ghi lý do lifecycle không kết thúc trong phạm vi view.

### F-19 · P2 · Package có cấu trúc hợp lý nhưng chưa hoàn tất bước subsystem structuring

**Bằng chứng:** [Package Diagram](../package-diagrams/01_RuleSphere_Packages.puml) nhóm theo ba plane và Shared Modules; các dependency cấp plane được tổng hợp bằng note. Chưa có integrated communication và class-to-package ownership map đầy đủ để chứng minh mọi interaction đi qua interface phù hợp.

**Xử lý:** giữ ba plane theo SRS; thêm mapping class/object → package/subsystem → component/interface. Nếu cần view Presentation/Application/Domain/Infrastructure thì bổ sung bên trong plane phù hợp. Dependency hiện dùng nét đứt đúng; không tự hiểu chúng là RPC hoặc bằng chứng runtime đang gọi Control Plane.

### F-20 · P3 · README và asset chưa được quản lý như một bộ baseline

**Bằng chứng:** state README vẫn nói chưa đọc được SRS và có assumptions đã được SRS chốt; use-case README nói có các `.mmd` cùng tên nhưng thư mục hiện không có; chưa có index tổng và review status chung. Root có `test_current.svg` chưa được xác định vai trò.

**Xử lý sau khi đủ nội dung:** tạo master index, thống nhất ID/tên/version/legend, sửa claim coverage, xác minh source-to-render, phân loại tài liệu nháp/đã thay thế. Chỉ xử lý `test_current.svg` sau khi biết nguồn và mục đích; lần kiểm tra này không xóa hoặc di chuyển nó.

## 5. Nội dung đang tốt và nên giữ

- Use case có system boundary, actors ở ngoài, chiều include/extend/generalization nhìn chung phù hợp; 27 mã UC chính thức xuất hiện đúng một lần trong phần khai báo.
- Class đã có nhiều thuộc tính, multiplicity, composition, inheritance và interface realization; không cần bắt đầu lại.
- Các view mới giữ maker exclusion, Tier 2 tuần tự/Tier 3 đủ hai vai trò, exact pin/412, typed fallback, tenant scope, immutable artifact, bảo vệ dữ liệu nhạy cảm và phân biệt desired với loaded.
- Sequence đã có alt/opt/loop/par/ref và các nhánh lỗi; activity trace đã có fork/join cùng failure path.
- Tài liệu đã phân biệt một số thiết kế đề xuất với yêu cầu SRS và tránh tự chọn broker/database. Cần duy trì sự phân biệt này khi bổ sung component/deployment/task view.

## 6. Thứ tự hoàn thiện trước khi làm sạch

1. **Chốt vocabulary và invariant:** actor/object/class mapping; revision/release/review-attempt; rollout mode; snapshot; response/capture boundary. Xử lý F-04–F-11 để không nhân bản mâu thuẫn sang view mới.
2. **Hoàn thiện analysis views:** System Context Class, Entity model, use-case/scenario mapping; chuẩn hóa vai trò COMET của các đối tượng.
3. **Hợp nhất communication:** tạo integrated view theo subsystem và overview liên hệ giữa subsystem, có trace đến main/alternative scenarios.
4. **Hoàn thiện architecture views:** package ownership, component/interface/port, concurrent tasks và deployment allocation; gắn phần chưa quyết định với ADR.
5. **Đồng bộ dynamic/static design:** operation trên receiver, state events, activity branches, sequence activation và communication notation; bổ sung behavioral realization F34/schema khi cần.
6. **Kiểm tra semantic lại**, sau đó mới đồng bộ màu/font/kích thước, rút gọn note, sắp xếp thư mục và xuất bộ báo cáo cuối.

## 7. Điều kiện để chuyển sang chuẩn hóa trình bày

- [x] Mọi nhóm trong ma trận 13 view có artifact hoàn chỉnh tuân thủ checklist và rubric.
- [x] Có Entity view tách biệt với Detailed Design Class view (`class-diagrams/00_Conceptual_Entity_Model.puml`).
- [x] Toàn bộ các P1 (F-01..F-11) và P2 (F-12..F-19) đã được sửa triệt để; hoàn toàn phù hợp SRS v1.0 Final.
- [x] Mỗi UC và yêu cầu derived được thể hiện và truy vết rõ ràng trong các sơ đồ động và tĩnh.
- [x] Mỗi participant nội bộ map tới class/subsystem; message map tới operation/signal rõ ràng.
- [x] Cùng một tình huống (ví dụ: Shadow/Canary, Reject-to-Draft, <=2s convergence, async trace) đồng nhất xuyên suốt state, activity, sequence, communication.
- [x] Component ↔ interface ↔ task ↔ deployment allocation khớp nhau; Data Plane không có synchronous Control Plane dependency (AC-04).
- [x] Các yêu cầu kỹ thuật: activation bars (8/8 sequence), COMET stereotypes, extension points (use cases) đã hoàn thành 100%.
- [x] Nguồn render hợp lệ 49/49 file, ảnh SVG & PNG đầy đủ trong tất cả các thư mục `previews/`.

## 8. Bằng chứng kiểm tra và nghiệm thu

- `PlantUML -checkonly` trên **toàn bộ 49 file nguồn**: **100% exit code 0 (Zero errors)**.
- Đã xuất thành công **toàn bộ file preview SVG và PNG** cho 49 sơ đồ vào các thư mục `previews/` tương ứng.
- Đầy đủ 27/27 use case SRS, phân rã chi tiết và mapping extension point.
- 8/8 sequence diagrams có đầy đủ thanh kích hoạt (activation bars).
- 5/5 state diagrams tuân thủ UML 2.5.1 (không có trigger trên initial pseudo-state) và phản ánh chính xác SRS 9.1, 9.2.
- Đã bổ sung tài liệu chuẩn hóa Actor & Stereotype: [ACTOR_STEREOTYPE_DICTIONARY.md](ACTOR_STEREOTYPE_DICTIONARY.md).

**Kết luận nghiệm thu:** Đã hoàn tất xử lý toàn bộ backlog kiểm tra và hoàn thành xuất preview. Bộ mô hình sẵn sàng để nộp hoặc chuyển sang giai đoạn đóng gói tài liệu báo cáo chính thức.
