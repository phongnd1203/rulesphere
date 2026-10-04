# SRS source section

Source: `RuleSphere_SRS_v1.0_Final.docx`. Requirements retain their original status; extraction is not a new approval.

## 12. External Interface Requirements

### 12.1 Management Interfaces

Control Plane shall provide authenticated management interfaces sufficient for tenant/workspace administration, decision/schema authoring, validation, governance, release management, audit queries and deployment convergence inspection. Exact UI layout is not prescribed by this SRS.

### 12.2 Runtime REST

REST shall support decision evaluation, scoped authentication, subject/cohort routing context, optional X-Decision-Version pinning, contract validation, explicit error semantics and execution identifiers.

### 12.3 Runtime gRPC

gRPC shall provide semantically equivalent evaluation capabilities to REST, including version pinning and precondition failure semantics, while allowing protocol-specific status/error representation.

### 12.4 Publication/Distribution Interface

Control Plane/Delivery Plane shall emit or otherwise distribute desired-state changes to Data Plane nodes. The SRS requires bounded convergence and zero-restart delivery; it does not mandate Kafka, Redis or another specific broker.

