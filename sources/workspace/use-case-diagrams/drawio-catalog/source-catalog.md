Dưới đây là **Use Case Catalog đề xuất cho RuleSphere**, được tổ chức theo **module**, sử dụng đúng 5 actor chính + actor phụ, đồng thời bổ sung **abstract actor** và các quan hệ `<<include>>`, `<<extend>>`, generalization giữa use case.

Tôi xem đây là **proposed use-case baseline** phục vụ SRS / Use Case Diagram; chưa mặc định tất cả đều là confirmed requirement.

## 1. Actor Model

### 1.1. Main Actors

| Actor | Responsibility |
|---|---|
| **Rule / Decision Author** | Author, modify, validate, test, simulate decision logic |
| **Reviewer / Approver** | Review, approve, reject governed changes |
| **Platform Administrator** | Platform configuration, IAM mapping, policy, environment administration |
| **Operations / SRE** | Deployment operations, runtime health, convergence, troubleshooting |
| **Decision Consumer / Client Application** | Invoke deployed decisions and consume results |

### 1.2. Supporting Actors

| Actor | Responsibility |
|---|---|
| **Identity Provider / IAM** | Authentication, identity assertion, possibly group/role information |
| **CI/CD & Automation** | Automated validation, test, build, publish, deployment |
| **Observability Platform** | Metrics, logs, traces, alerts |
| **Audit / SIEM** | Consume audit/security events |

---

# 2. Abstract Actors

Các actor abstract giúp diagram không bị lặp quan hệ.

```text
Platform User <<abstract>>
├── Rule / Decision Author
├── Reviewer / Approver
├── Platform Administrator
└── Operations / SRE
```

Có thể bổ sung:

```text
Decision API Consumer <<abstract>>
├── Decision Consumer / Client Application
└── CI/CD & Automation
```

Nhưng tôi khuyến nghị chỉ dùng actor abstract thứ hai khi CI/CD thực sự sử dụng cùng nhóm API/security contract với application consumer.

Một abstraction hữu ích khác:

```text
Governed User <<abstract>>
├── Rule / Decision Author
└── Reviewer / Approver
```

Tuy nhiên không nên lạm dụng. Với RuleSphere, actor hierarchy tối thiểu hợp lý là:

```text
                   Platform User
                        |
        +---------------+---------------+
        |               |               |
      Author        Reviewer        Administrator
                                        |
                                  Operations / SRE
```

Thực tế `Operations / SRE` và `Platform Administrator` không nhất thiết có inheritance relationship. Vì vậy mô hình đúng hơn là:

```text
Platform User <<abstract>>
├── Rule / Decision Author
├── Reviewer / Approver
├── Platform Administrator
└── Operations / SRE
```

---

# 3. Module A — Identity & Access Management

## Use Cases

| ID | Use Case | Actor |
|---|---|---|
| IAM-01 | Sign In | Platform User |
| IAM-02 | Sign Out | Platform User |
| IAM-03 | Authenticate User | Identity Provider / IAM |
| IAM-04 | Authorize Access | Platform User |
| IAM-05 | Manage Role Mappings | Platform Administrator |
| IAM-06 | Assign Platform Roles | Platform Administrator |
| IAM-07 | Revoke Platform Roles | Platform Administrator |
| IAM-08 | Manage Project Access | Platform Administrator |
| IAM-09 | Manage Service / Client Identity | Platform Administrator |
| IAM-10 | Validate Client Credential | Decision Consumer / Client Application |

### Relations

```text
Sign In
  <<include>> Authenticate User

Authorize Access
  <<include>> Resolve User Roles
  <<include>> Evaluate Access Policy

Manage Project Access
  <<include>> Authorize Access

Assign Platform Roles
  <<extend>> Manage Role Mappings

Revoke Platform Roles
  <<extend>> Manage Role Mappings

Validate Client Credential
  <<include>> Authenticate Client
```

Nếu authentication hoàn toàn delegated:

```text
Identity Provider / IAM --> Authenticate User
Identity Provider / IAM --> Authenticate Client
```

---

# 4. Module B — Decision Project & Asset Management

## Use Cases

| ID | Use Case | Actor |
|---|---|---|
| DAM-01 | Manage Decision Project | Rule / Decision Author |
| DAM-02 | Create Decision Project | Rule / Decision Author |
| DAM-03 | View Decision Project | Platform User |
| DAM-04 | Update Decision Project | Rule / Decision Author |
| DAM-05 | Archive Decision Project | Platform Administrator |
| DAM-06 | Search Decision Assets | Platform User |
| DAM-07 | View Asset Metadata | Platform User |
| DAM-08 | Manage Asset Metadata | Rule / Decision Author |
| DAM-09 | View Asset Dependencies | Rule / Decision Author |

### Relations

Use generalization:

```text
Create Decision Project ──|> Manage Decision Project
Update Decision Project ──|> Manage Decision Project
Archive Decision Project ──|> Manage Decision Project
```

Hoặc nếu muốn diagram đơn giản hơn:

```text
Manage Decision Project
  <<include>> View Decision Project

Create Decision Project
  <<extend>> Manage Decision Project

Update Decision Project
  <<extend>> Manage Decision Project

Archive Decision Project
  <<extend>> Manage Decision Project
```

Tuy nhiên về UML semantics, CRUD variants thường phù hợp với **generalization** hơn `extend`.

---

# 5. Module C — Decision Modeling & Rule Authoring

Đây là core module của **Decision Management / Control Plane**.

## Use Cases

| ID | Use Case | Actor |
|---|---|---|
| AUT-01 | Author Decision Model | Rule / Decision Author |
| AUT-02 | Create Decision Model | Rule / Decision Author |
| AUT-03 | Edit Decision Model | Rule / Decision Author |
| AUT-04 | Clone Decision Model | Rule / Decision Author |
| AUT-05 | Define Business Rule | Rule / Decision Author |
| AUT-06 | Edit Business Rule | Rule / Decision Author |
| AUT-07 | Define Decision Table | Rule / Decision Author |
| AUT-08 | Edit Decision Table | Rule / Decision Author |
| AUT-09 | Define Decision Expression | Rule / Decision Author |
| AUT-10 | Configure Rule Priority | Rule / Decision Author |
| AUT-11 | Enable / Disable Rule | Rule / Decision Author |
| AUT-12 | Define Rule Metadata | Rule / Decision Author |
| AUT-13 | View Rule Dependencies | Rule / Decision Author |
| AUT-14 | Compare Decision Versions | Rule / Decision Author |
| AUT-15 | Delete Draft Asset | Rule / Decision Author |

### Generalization

```text
Business Rule
Decision Table
Decision Expression
```

có thể được mô hình hóa dưới abstract use case:

```text
Author Decision Logic <<abstract>>
├── Define Business Rule
├── Define Decision Table
└── Define Decision Expression
```

### Relations

```text
Author Decision Model
  <<include>> Author Decision Logic
  <<include>> Define Rule Metadata
  <<include>> Validate Decision Model

Edit Decision Model
  <<include>> View Rule Dependencies

Define Business Rule
  <<include>> Define Rule Metadata

Configure Rule Priority
  <<extend>> Define Business Rule

Enable / Disable Rule
  <<extend>> Edit Business Rule

Clone Decision Model
  <<extend>> View Decision Model
```

---

# 6. Module D — Data Contract Management

## Use Cases

| ID | Use Case | Actor |
|---|---|---|
| DCM-01 | Manage Decision Contract | Rule / Decision Author |
| DCM-02 | Define Input Contract | Rule / Decision Author |
| DCM-03 | Define Output Contract | Rule / Decision Author |
| DCM-04 | Define Data Types | Rule / Decision Author |
| DCM-05 | Define Validation Constraints | Rule / Decision Author |
| DCM-06 | Validate Decision Contract | Rule / Decision Author |
| DCM-07 | Validate Contract Compatibility | Rule / Decision Author |
| DCM-08 | View Decision Contract | Decision Consumer / Client Application |
| DCM-09 | Export Decision Contract | Decision Consumer / Client Application |

### Relations

```text
Manage Decision Contract
  <<include>> Define Input Contract
  <<include>> Define Output Contract

Define Input Contract
  <<include>> Define Data Types

Define Output Contract
  <<include>> Define Data Types

Define Validation Constraints
  <<extend>> Define Input Contract
  <<extend>> Define Output Contract

Validate Contract Compatibility
  <<include>> Validate Decision Contract
```

---

# 7. Module E — Validation & Testing

## Use Cases

| ID | Use Case | Actor |
|---|---|---|
| VAL-01 | Validate Decision | Rule / Decision Author |
| VAL-02 | Validate Rule Syntax | Rule / Decision Author |
| VAL-03 | Validate Decision Structure | Rule / Decision Author |
| VAL-04 | Validate References | Rule / Decision Author |
| VAL-05 | Detect Rule Conflicts | Rule / Decision Author |
| VAL-06 | Detect Redundant / Unreachable Rules | Rule / Decision Author |
| TST-01 | Manage Test Cases | Rule / Decision Author |
| TST-02 | Create Test Case | Rule / Decision Author |
| TST-03 | Execute Decision Test | Rule / Decision Author |
| TST-04 | Execute Test Suite | Rule / Decision Author |
| TST-05 | View Test Result | Rule / Decision Author |
| TST-06 | Compare Expected vs Actual Result | Rule / Decision Author |
| TST-07 | Run Regression Test | Rule / Decision Author |
| TST-08 | Validate Release Candidate | Reviewer / Approver |

### Relations

```text
Validate Decision
  <<include>> Validate Rule Syntax
  <<include>> Validate Decision Structure
  <<include>> Validate References

Detect Rule Conflicts
  <<extend>> Validate Decision

Detect Redundant / Unreachable Rules
  <<extend>> Validate Decision

Execute Decision Test
  <<include>> Validate Decision

Execute Test Suite
  <<include>> Execute Decision Test

Compare Expected vs Actual Result
  <<include>> View Test Result

Run Regression Test
  <<include>> Execute Test Suite

Validate Release Candidate
  <<include>> Validate Decision
  <<include>> Execute Test Suite
```

---

# 8. Module F — Version & Change Management

## Use Cases

| ID | Use Case | Actor |
|---|---|---|
| VER-01 | Manage Decision Version | Rule / Decision Author |
| VER-02 | Create Decision Version | Rule / Decision Author |
| VER-03 | View Version History | Platform User |
| VER-04 | Compare Versions | Rule / Decision Author |
| VER-05 | Restore Draft Version | Rule / Decision Author |
| VER-06 | Create Release Version | Rule / Decision Author |
| VER-07 | Deprecate Decision Version | Platform Administrator |
| VER-08 | View Version Lineage | Platform User |

### Relations

```text
Create Decision Version
  <<include>> Validate Decision

Create Release Version
  <<include>> Validate Release Candidate

Restore Draft Version
  <<extend>> View Version History

Compare Versions
  <<include>> View Version History
```

---

# 9. Module G — Review & Approval Workflow

Lưu ý: đây là **decision governance workflow**, không phải BPM orchestration chung.

## Use Cases

| ID | Use Case | Actor |
|---|---|---|
| GOV-01 | Submit Change for Review | Rule / Decision Author |
| GOV-02 | Review Decision Change | Reviewer / Approver |
| GOV-03 | Approve Decision Change | Reviewer / Approver |
| GOV-04 | Reject Decision Change | Reviewer / Approver |
| GOV-05 | Request Rework | Reviewer / Approver |
| GOV-06 | Cancel Review Request | Rule / Decision Author |
| GOV-07 | View Review Status | Rule / Decision Author |
| GOV-08 | View Approval History | Reviewer / Approver |
| GOV-09 | Enforce Approval Policy | Platform Administrator |

### Relations

```text
Submit Change for Review
  <<include>> Validate Decision
  <<include>> Create Decision Version

Review Decision Change
  <<include>> View Version Changes

Approve Decision Change
  <<extend>> Review Decision Change

Reject Decision Change
  <<extend>> Review Decision Change

Request Rework
  <<extend>> Review Decision Change

Cancel Review Request
  <<extend>> View Review Status
```

Điểm quan trọng:

```text
Approve
Reject
Request Rework
```

là các **alternative outcomes** của `Review Decision Change`.

---

# 10. Module H — Build & Artifact Management

Đây là boundary giữa Control Plane và Distribution Plane.

## Use Cases

| ID | Use Case | Actor |
|---|---|---|
| ART-01 | Build Decision Artifact | Rule / Decision Author / CI/CD |
| ART-02 | Validate Build Inputs | RuleSphere |
| ART-03 | Package Decision Artifact | RuleSphere |
| ART-04 | Generate Artifact Metadata | RuleSphere |
| ART-05 | Publish Decision Artifact | Rule / Decision Author / CI/CD |
| ART-06 | View Published Artifact | Platform User |
| ART-07 | Verify Artifact Integrity | Operations / SRE |
| ART-08 | View Artifact Provenance | Reviewer / Approver |
| ART-09 | Deprecate Artifact | Platform Administrator |

### Relations

```text
Build Decision Artifact
  <<include>> Validate Build Inputs
  <<include>> Package Decision Artifact
  <<include>> Generate Artifact Metadata

Publish Decision Artifact
  <<include>> Build Decision Artifact
  <<include>> Verify Artifact Integrity

View Artifact Provenance
  <<include>> View Version Lineage
```

---

# 11. Module I — Environment & Deployment Management

## Use Cases

| ID | Use Case | Actor |
|---|---|---|
| DEP-01 | Manage Runtime Environment | Platform Administrator |
| DEP-02 | Create Environment | Platform Administrator |
| DEP-03 | Configure Environment | Platform Administrator |
| DEP-04 | Configure Deployment Policy | Platform Administrator |
| DEP-05 | Deploy Decision | Operations / SRE |
| DEP-06 | Promote Decision | Operations / SRE |
| DEP-07 | Roll Back Deployment | Operations / SRE |
| DEP-08 | Redeploy Decision | Operations / SRE |
| DEP-09 | Cancel Deployment | Operations / SRE |
| DEP-10 | View Deployment Status | Operations / SRE |
| DEP-11 | View Deployment History | Operations / SRE |
| DEP-12 | Validate Deployment | RuleSphere |
| DEP-13 | Distribute Artifact to Runtime | RuleSphere |
| DEP-14 | Verify Runtime Convergence | Operations / SRE |
| DEP-15 | Detect Version Drift | Operations / SRE |
| DEP-16 | Reconcile Runtime State | Operations / SRE |

### Relations

```text
Deploy Decision
  <<include>> Validate Deployment
  <<include>> Verify Artifact Integrity
  <<include>> Distribute Artifact to Runtime
  <<include>> Verify Runtime Convergence

Promote Decision
  <<include>> Deploy Decision

Redeploy Decision
  --|> Deploy Decision

Roll Back Deployment
  <<extend>> Deploy Decision

Detect Version Drift
  <<extend>> Verify Runtime Convergence

Reconcile Runtime State
  <<extend>> Detect Version Drift
```

`Rollback` không phải bước bắt buộc của deployment nên phù hợp với `<<extend>>`.

---

# 12. Module J — Progressive Delivery

## Use Cases

| ID | Use Case | Actor |
|---|---|---|
| PRG-01 | Perform Progressive Deployment | Operations / SRE |
| PRG-02 | Configure Canary Deployment | Operations / SRE |
| PRG-03 | Adjust Canary Allocation | Operations / SRE |
| PRG-04 | Promote Canary Version | Operations / SRE |
| PRG-05 | Abort Canary Deployment | Operations / SRE |
| PRG-06 | Configure Shadow Deployment | Operations / SRE |
| PRG-07 | Execute Shadow Evaluation | Decision Consumer / Client Application |
| PRG-08 | Compare Shadow Results | Operations / SRE |
| PRG-09 | Stop Shadow Deployment | Operations / SRE |

### Generalization

```text
Perform Progressive Deployment <<abstract>>
├── Perform Canary Deployment
└── Perform Shadow Deployment
```

### Relations

```text
Perform Canary Deployment
  <<include>> Configure Canary Deployment
  <<include>> Deploy Decision

Adjust Canary Allocation
  <<extend>> Perform Canary Deployment

Promote Canary Version
  <<extend>> Perform Canary Deployment

Abort Canary Deployment
  <<extend>> Perform Canary Deployment

Perform Shadow Deployment
  <<include>> Configure Shadow Deployment
  <<include>> Deploy Decision

Compare Shadow Results
  <<include>> Execute Shadow Evaluation
```

---

# 13. Module K — Decision Execution

Đây là core **Data Plane**.

## Use Cases

| ID | Use Case | Actor |
|---|---|---|
| EXE-01 | Execute Decision | Decision Consumer / Client Application |
| EXE-02 | Authenticate Decision Request | Identity Provider / IAM |
| EXE-03 | Validate Decision Request | Decision Consumer / Client Application |
| EXE-04 | Resolve Active Decision Version | RuleSphere |
| EXE-05 | Evaluate Decision Logic | RuleSphere |
| EXE-06 | Evaluate Business Rules | RuleSphere |
| EXE-07 | Evaluate Decision Table | RuleSphere |
| EXE-08 | Produce Decision Result | RuleSphere |
| EXE-09 | Return Execution Metadata | Decision Consumer / Client Application |
| EXE-10 | Handle Invalid Request | Decision Consumer / Client Application |
| EXE-11 | Handle Evaluation Failure | Decision Consumer / Client Application |
| EXE-12 | Execute Specific Decision Version | Decision Consumer / Client Application |

### Generalization

```text
Evaluate Decision Logic <<abstract>>
├── Evaluate Business Rules
├── Evaluate Decision Table
└── Evaluate Decision Expression
```

### Relations

```text
Execute Decision
  <<include>> Authenticate Decision Request
  <<include>> Validate Decision Request
  <<include>> Resolve Active Decision Version
  <<include>> Evaluate Decision Logic
  <<include>> Produce Decision Result

Return Execution Metadata
  <<extend>> Execute Decision

Handle Invalid Request
  <<extend>> Execute Decision

Handle Evaluation Failure
  <<extend>> Execute Decision

Execute Specific Decision Version
  --|> Execute Decision
```

---

# 14. Module L — Explainability & Decision Trace

## Use Cases

| ID | Use Case | Actor |
|---|---|---|
| EXP-01 | Request Decision Explanation | Decision Consumer / Client Application |
| EXP-02 | Generate Decision Explanation | RuleSphere |
| EXP-03 | View Matched Rules | Rule / Decision Author |
| EXP-04 | View Evaluation Trace | Rule / Decision Author / Operations |
| EXP-05 | View Input Values Used | Rule / Decision Author |
| EXP-06 | View Output Derivation | Rule / Decision Author |
| EXP-07 | View Executed Decision Version | Platform User |
| EXP-08 | Retrieve Execution Trace | Operations / SRE |

### Relations

```text
Request Decision Explanation
  <<include>> Generate Decision Explanation

Generate Decision Explanation
  <<include>> View Executed Decision Version

View Matched Rules
  <<extend>> Generate Decision Explanation

View Evaluation Trace
  <<extend>> Generate Decision Explanation

View Input Values Used
  <<extend>> Generate Decision Explanation

View Output Derivation
  <<extend>> Generate Decision Explanation
```

---

# 15. Module M — Simulation & Impact Analysis

## Use Cases

| ID | Use Case | Actor |
|---|---|---|
| SIM-01 | Simulate Decision | Rule / Decision Author |
| SIM-02 | Simulate Draft Version | Rule / Decision Author |
| SIM-03 | Compare Decision Outputs | Rule / Decision Author |
| SIM-04 | Compare Decision Versions | Rule / Decision Author |
| SIM-05 | Analyze Rule Change Impact | Rule / Decision Author |
| SIM-06 | Identify Dependent Decisions | Rule / Decision Author |
| SIM-07 | Evaluate Decision against Dataset | Rule / Decision Author |

### Relations

```text
Simulate Draft Version
  --|> Simulate Decision

Compare Decision Outputs
  <<include>> Simulate Decision

Analyze Rule Change Impact
  <<include>> Identify Dependent Decisions

Evaluate Decision against Dataset
  <<include>> Simulate Decision
```

---

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

# 17. Module O — Audit & Compliance

## Use Cases

| ID | Use Case | Actor |
|---|---|---|
| AUD-01 | View Audit Trail | Reviewer / Approver |
| AUD-02 | Search Audit Events | Reviewer / Approver |
| AUD-03 | View Rule Change History | Reviewer / Approver |
| AUD-04 | View Approval History | Reviewer / Approver |
| AUD-05 | View Deployment History | Operations / SRE |
| AUD-06 | Trace Decision Provenance | Reviewer / Approver |
| AUD-07 | Trace Decision to Rule Version | Reviewer / Approver |
| AUD-08 | Trace Rule Version to Deployment | Reviewer / Approver |
| AUD-09 | Export Audit Events | Audit / SIEM |
| AUD-10 | Configure Audit Policy | Platform Administrator |

### Relations

```text
Trace Decision Provenance
  <<include>> Trace Decision to Rule Version
  <<include>> Trace Rule Version to Deployment

View Rule Change History
  <<include>> View Audit Trail

View Approval History
  <<include>> View Audit Trail

View Deployment History
  <<include>> View Audit Trail

Export Audit Events
  <<include>> Record Audit Event
```

---

# 18. Module P — Automation & CI/CD Integration

## Use Cases

| ID | Use Case | Actor |
|---|---|---|
| CICD-01 | Validate Decision via API | CI/CD & Automation |
| CICD-02 | Execute Tests via API | CI/CD & Automation |
| CICD-03 | Build Artifact via API | CI/CD & Automation |
| CICD-04 | Publish Artifact via API | CI/CD & Automation |
| CICD-05 | Trigger Deployment | CI/CD & Automation |
| CICD-06 | Query Deployment Status | CI/CD & Automation |
| CICD-07 | Retrieve Test Result | CI/CD & Automation |
| CICD-08 | Retrieve Validation Result | CI/CD & Automation |

### Relations

Các use case automation nên reuse business use cases hiện tại:

```text
Validate Decision via API
  <<include>> Validate Decision

Execute Tests via API
  <<include>> Execute Test Suite

Build Artifact via API
  <<include>> Build Decision Artifact

Publish Artifact via API
  <<include>> Publish Decision Artifact

Trigger Deployment
  <<include>> Deploy Decision

Query Deployment Status
  <<include>> View Deployment Status
```

Điều này tránh tạo hai implementation semantics khác nhau giữa UI và API.

---

# 19. Module Q — Platform Administration

## Use Cases

| ID | Use Case | Actor |
|---|---|---|
| ADM-01 | Manage Platform Configuration | Platform Administrator |
| ADM-02 | Configure Platform Policies | Platform Administrator |
| ADM-03 | Configure Execution Limits | Platform Administrator |
| ADM-04 | Configure Retention Policy | Platform Administrator |
| ADM-05 | Configure Audit Policy | Platform Administrator |
| ADM-06 | Configure Deployment Policy | Platform Administrator |
| ADM-07 | Manage Runtime Nodes | Platform Administrator |
| ADM-08 | Register Runtime Node | Platform Administrator |
| ADM-09 | Deregister Runtime Node | Platform Administrator |
| ADM-10 | View Runtime Node Status | Platform Administrator |
| ADM-11 | View Platform Health | Platform Administrator |
| ADM-12 | View Platform Usage | Platform Administrator |

### Relations

```text
Manage Platform Configuration
  <<include>> Configure Platform Policies

Configure Execution Limits
  <<extend>> Configure Platform Policies

Configure Retention Policy
  <<extend>> Configure Platform Policies

Configure Audit Policy
  <<extend>> Configure Platform Policies

Configure Deployment Policy
  <<extend>> Configure Platform Policies

Register Runtime Node
  --|> Manage Runtime Nodes

Deregister Runtime Node
  --|> Manage Runtime Nodes

View Runtime Node Status
  <<include>> Manage Runtime Nodes
```

---

# 20. Cross-Cutting Abstract Use Cases

Đây là phần rất hữu ích để giảm số lượng `include` bị lặp.

## UC-X01 — Authorize Operation

```text
Authorize Operation <<abstract>>
```

Được include bởi:

```text
Manage Decision Project
Author Decision Model
Submit Change for Review
Approve Decision Change
Publish Decision Artifact
Deploy Decision
Manage Platform Configuration
...
```

Nhưng trên **high-level use case diagram**, không nên nối mọi UC với nó vì diagram sẽ thành spaghetti.

---

## UC-X02 — Record Audit Event

```text
Record Audit Event <<abstract>>
```

Có thể được include bởi các state-changing use case:

```text
Create / Update Decision
Approve Decision
Publish Artifact
Deploy Decision
Roll Back Deployment
Modify Platform Configuration
Modify Access Control
```

Về diagram architecture-level:

```text
State-Changing Operation
    <<include>>
Record Audit Event
```

Thay vì nối 30 use cases riêng lẻ.

---

## UC-X03 — Validate Decision

Một use case reusable rất quan trọng:

```text
Validate Decision
```

được include bởi:

```text
Execute Decision Test
Submit Change for Review
Create Release Version
Build Decision Artifact
Publish Decision Artifact
```

---

## UC-X04 — Resolve Decision Version

```text
Resolve Decision Version
```

được include bởi:

```text
Execute Decision
Simulate Decision
Request Decision Explanation
Trace Decision Provenance
```

---

# 21. Recommended top-level Use Case Diagram

Nếu vẽ diagram chính của toàn hệ thống, tôi không khuyến nghị đưa toàn bộ ~150 detailed UC vào một diagram.

Nên giữ khoảng **20–25 system-level use cases**:

```text
Decision Management
-------------------
UC-01  Manage Decision Projects
UC-02  Author Decision Models
UC-03  Manage Business Rules
UC-04  Manage Decision Contracts
UC-05  Validate Decisions
UC-06  Test Decisions
UC-07  Manage Decision Versions
UC-08  Review & Approve Changes
UC-09  Simulate & Analyze Decisions

Decision Delivery
-----------------
UC-10  Build Decision Artifact
UC-11  Publish Decision Artifact
UC-12  Manage Runtime Environments
UC-13  Deploy Decisions
UC-14  Perform Progressive Delivery
UC-15  Manage Deployment State

Decision Execution
------------------
UC-16  Execute Decision
UC-17  Explain Decision Result

Operations
----------
UC-18  Monitor Decision Runtime
UC-19  Diagnose Runtime Issues
UC-20  Audit Decision Lifecycle

Administration
--------------
UC-21  Manage Identity & Access
UC-22  Manage Platform Configuration
UC-23  Manage Runtime Nodes

Integration
-----------
UC-24  Integrate CI/CD Automation
UC-25  Export Telemetry & Audit Events
```

---

# 22. Actor → Module mapping

| Module | Author | Reviewer | Admin | Ops/SRE | Consumer | External Actors |
|---|:---:|:---:|:---:|:---:|:---:|---|
| Identity & Access | ✓ | ✓ | ✓ | ✓ | ✓ | IAM |
| Project Management | ✓ | ○ | ✓ | | | |
| Rule Authoring | ✓ | ○ | | | | |
| Data Contract | ✓ | ○ | | | ✓ | |
| Validation & Testing | ✓ | ✓ | | | | CI/CD |
| Version Management | ✓ | ✓ | ○ | | | |
| Governance | ✓ | ✓ | ○ | | | |
| Artifact Management | ✓ | ○ | | ✓ | | CI/CD |
| Deployment | | | ○ | ✓ | | CI/CD |
| Progressive Delivery | | | | ✓ | ○ | |
| Decision Execution | | | | ○ | ✓ | IAM |
| Explainability | ✓ | ○ | | ✓ | ✓ | |
| Simulation | ✓ | ○ | | | | |
| Observability | | | ○ | ✓ | | Observability |
| Audit | ○ | ✓ | ✓ | ✓ | | SIEM |
| Platform Administration | | | ✓ | ○ | | IAM |

`✓` = primary interaction  
`○` = secondary/supporting interaction.

---

# 23. Core cross-module relationships

Ở mức toàn hệ thống, lifecycle chính nên thể hiện như sau:

```text
Author Decision
    |
    +-- <<include>> Validate Decision
    |
    v
Test Decision
    |
    v
Submit for Review
    |
    v
Review Decision
    |
    +--> Reject / Request Rework
    |
    +--> Approve
             |
             v
      Create Release Version
             |
             v
      Build Decision Artifact
             |
             v
      Publish Artifact
             |
             v
        Deploy Decision
             |
             v
      Verify Convergence
             |
             v
       Execute Decision
             |
             +-- <<extend>> Explain Decision
             |
             v
     Monitor / Audit Runtime
```

Nhưng cần lưu ý: **đây không phải BPM workflow do RuleSphere execute như một business process**. Đây chỉ là relationship/lifecycle giữa system use cases.

---

# 24. `include`, `extend`, generalization nên dùng thế nào

Để giữ consistency trong SRS:

| Relation | Dùng khi |
|---|---|
| `<<include>>` | Sub-flow bắt buộc, reusable và luôn được gọi |
| `<<extend>>` | Optional/conditional behavior |
| Use Case Generalization | Một use case là specialization của use case tổng quát |
| Actor Generalization | Nhiều actor chia sẻ cùng capability chung |

Ví dụ đúng:

```text
Deploy Decision
  <<include>> Validate Deployment
```

vì deployment luôn phải được validate.

```text
Roll Back Deployment
  <<extend>> Deploy Decision
```

vì rollback chỉ xảy ra trong điều kiện cụ thể.

```text
Execute Specific Decision Version
  --|> Execute Decision
```

vì đây là specialization của execution.

```text
Rule / Decision Author
  --|> Platform User
```

vì Author là một loại Platform User.

---

## Recommended actor hierarchy cuối cùng

Tôi đề xuất chốt hierarchy đơn giản:

```text
                  <<abstract>>
                  Platform User
                       ^
        +--------------+--------------+--------------+
        |              |              |              |
 Rule / Decision   Reviewer /     Platform       Operations /
     Author         Approver     Administrator       SRE


                  <<abstract>>
             External System Actor
                       ^
        +--------------+--------------+--------------+-------------+
        |              |              |              |             |
 Identity Provider   CI/CD &      Observability   Audit / SIEM   Decision
      / IAM         Automation      Platform                    Consumer /
                                                               Client App
```

Tuy nhiên **Decision Consumer / Client Application** nên giữ là **main actor**, dù về UML inheritance nó có thể inherit từ `External System Actor`.

Do đó actor model cuối cùng có thể thể hiện:

```text
<<abstract>> Platform User
 ├── Rule / Decision Author
 ├── Reviewer / Approver
 ├── Platform Administrator
 └── Operations / SRE

<<abstract>> External System
 ├── Decision Consumer / Client Application
 ├── Identity Provider / IAM
 ├── CI/CD & Automation
 ├── Observability Platform
 └── Audit / SIEM
```

Đây là cấu trúc phù hợp nhất để tiếp tục sang **module-level PlantUML Use Case Diagram**, vì mỗi module có thể reuse cùng actor hierarchy mà không phải vẽ lại logic actor.