# Module notes and UML clarifications

## A Identity Access Management

**IAM-01 — Sign In**: Platform User generalization is defined in 01_Actor_Model. Authentication is delegated to Identity Provider / IAM.

**IAM-04 — Authorize Access**: Internal authorization behavior invoked by protected operations; Platform User is the subject, not an actor who manually runs the policy engine.

**IAM-10 — Validate Client Credential**: Internal credential check for client requests; Authenticate Client uses delegated IAM. Consumer participation is through EXE-01.

## B Decision Project Asset Management

**DAM-01 — Manage Decision Project**: Actor links terminate on the permitted variants: Author creates/updates; Administrator archives. No Author association on the abstract parent, so archive permission is not inherited.

## C Decision Modeling Rule Authoring

**AUT-01 — Author Decision Model**: The model-authoring transaction includes logic, metadata and validation. VAL-01 is the catalog relation named Validate Decision Model.

**AUX-AUT-01 — Author Decision Logic**: Reusable logic-authoring behavior included by AUT-01; concrete rule/table/expression variants inherit this contract.

**AUT-03 — Edit Decision Model**: Detailed behavior of Edit Decision Model; actor association is inherited from AUT-01.

**AUT-15 — Delete Draft Asset**: Precondition: draft asset; released assets are immutable.

## D Data Contract Management

**DCM-01 — Manage Decision Contract**: Complete contract-definition transaction includes both input and output contracts, as specified in this proposed catalog.

## E Validation Testing

**TST-01 — Manage Test Cases**: Only Create Test Case is named as a detailed management variant in the catalog; edit/delete variants are not invented.

**TST-08 — Validate Release Candidate**: Reviewer can initiate the release-candidate check; Author release creation also invokes it internally through VER-06. This does not confer approval rights on Author.

## F Version Change Management

**VER-06 — Create Release Version**: Creates a release version, not a governance approval. Release eligibility and immutability constraints apply.

**VER-03 — View Version History**: Viewing history is shared; restoring a draft remains Author-only. Extension permissions do not follow the base use case automatically.

## G Review Approval Governance

**GOV-02 — Review Decision Change**: Outcome extensions are mutually exclusive for a review decision. This is decision governance, not general-purpose BPM orchestration.

**GOV-03 — Approve Decision Change**: Enforce Approval Policy is internal enforcement configured by Administrator through platform policies. Administrator is not a manual policy-execution actor.

## H Build Artifact Management

**ART-05 — Publish Decision Artifact**: Catalog models publish as build-and-publish. Every invocation includes Build. A publish-existing-artifact API would need a distinct behavior if later required. Published artifacts are immutable.

**ART-07 — Verify Artifact Integrity**: Integrity verification can also be initiated directly by Operations; build/deploy reuse it internally.

## I Environment Deployment Management

**DEP-05 — Deploy Decision**: Deployment includes asynchronous convergence verification before lifecycle completion. Rollback extend is limited to recovery within this lifecycle; a later independent rollback remains directly invocable by Operations.

**DEP-05 — Deploy Decision**: Redeploy specializes deployment and inherits its includes. Separate page for readability; same DEP-05 identity.

**DEP-14 — Verify Runtime Convergence**: Base convergence verification checks the desired/observed state. Detailed drift diagnosis is conditional.

**DEP-07 — Roll Back Deployment**: Explicit association supports independent rollback requests. The conditional recovery extension is shown on the DEP-05 detail page.

## J Progressive Delivery

**AUX-PRG-01 — Perform Canary Deployment**: Perform Canary Deployment spans the rollout lifecycle, so later control interactions occur at named extension points.

**PRG-08 — Compare Shadow Results**: This comparison use case launches a shadow evaluation as specified by the catalog. Comparing only previously captured results would be a separate contract.

**EXE-01 — Execute Decision**: Runtime reference: Consumer triggers shadow evaluation indirectly through the real decision request. Shadow result never replaces the active result.

## K Decision Execution

**EXE-01 — Execute Decision**: UC-X04 selects EXE-04 for default execution or exact pinned resolution for EXE-12. Refinement: do not require active resolution in every specialization. Later successful-path includes are skipped after a terminating error.

**EXE-05 — Evaluate Decision Logic**: Concrete evaluators specialize the evaluation behavior; activated model nodes may use more than one evaluator.

**EXE-01 — Execute Decision**: EXE-12 inherits Execute Decision with the version-resolution variation explicitly overridden. Authorization still applies to the requested version.

**EXE-12 — Execute Specific Decision Version**: Resolve the exact requested version; never fall back silently to active. Overrides EXE-04 inside the inherited UC-X04 resolution strategy.

**EXE-02 — Authenticate Decision Request**: Decision-request authentication reuses the client credential validation defined in module A.

**UC-X04 — Resolve Decision Version**: Default execution resolves the active version. EXE-12 selects the exact pinned-version strategy; both strategies specialize UC-X04.

## L Explainability Decision Trace

**EXP-01 — Request Decision Explanation**: Resolve the version bound to the recorded execution, not the current active version.

**EXP-02 — Generate Decision Explanation**: Optional evidence views are scoped by permissions, masking and retention. Author may inspect all listed detail views; Operations may inspect the evaluation trace. No consumer access to sensitive fields is implied.

## M Simulation Impact Analysis

**SIM-07 — Evaluate Decision against Dataset**: Dataset evaluation repeats simulation for supplied inputs. No production replay or batch API requirement is inferred.

## N Runtime Operations Observability

**OPS-10 — Diagnose Execution Failure**: The catalog assumes diagnosis retrieves logs and traces; unavailable/expired evidence must be handled explicitly in the detailed specification.

**OPS-12 — Export Telemetry**: Triggered internally by telemetry production or an external scrape/query. Observability Platform is the receiving/supporting actor; RuleSphere is not an actor of itself.

## O Audit Compliance

**AUD-06 — Trace Decision Provenance**: Resolve the exact historical version tied to execution evidence.

**AUD-05 — View Deployment History**: Operations receives deployment-scoped audit evidence only; reusing AUD-01 does not grant unrestricted Reviewer audit access.

**AUD-09 — Export Audit Events**: Record Audit Event here records the export operation itself. The exported events already exist; exporting does not recreate historical audit events. SIEM receives the export.

## P Automation CI CD Integration



## Q Platform Administration

**ADM-07 — Manage Runtime Nodes**: Modeling correction: View Runtime Node Status is a read-only specialization, not an include of all runtime-node management. Register/deregister do not run when viewing status.

## 02 Cross Cutting

**UC-X01 — Authorize Operation**: Authorization delegates to IAM-04. Protected goals keep authorization requirements when repeated edges are omitted.

**AUX-X-01 — State-Changing Operation**: Architecture-level contract for state-changing operations; no business-process orchestration.

**UC-X04 — Resolve Decision Version**: Active/pinned resolution depends on execution context. Simulation and historical evidence resolve their bound version. UC-X03 aliases VAL-01.
