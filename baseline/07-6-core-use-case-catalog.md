# SRS source section

Source: `RuleSphere_SRS_v1.0_Final.docx`. Requirements retain their original status; extraction is not a new approval.

## 6. Core Use Case Catalog

| ID | Use Case | Primary actor | Precondition | Postcondition |
| --- | --- | --- | --- | --- |
| UC-01 | Manage Tenant & Workspaces | Enterprise Admin | Authenticated enterprise admin | Tenant/workspace configuration updated. |
| UC-02 | Manage Membership & Roles | Enterprise Admin | Tenant/workspace exists | Scoped role assignments updated. |
| UC-03 | Manage API Credentials | Enterprise Admin | Workspace exists | Credential issued/revoked with scope. |
| UC-04 | Publish Shared Library Asset | Authorized owner | Validated reusable asset | Immutable version becomes available tenant-wide. |
| UC-05 | Create/Edit Decision | Decision Author | Workspace author permission | Draft Decision Version stored. |
| UC-06 | Model Decision Graph | Decision Author | Draft exists | Valid node/dependency model stored. |
| UC-07 | Define/Version Schema | Decision Author | Draft/schema permission | Schema Version stored. |
| UC-08 | Validate Graph & Contracts | Decision Author | Draft graph/schema exists | Validation result produced; cycles/breaking issues identified. |
| UC-09 | Sandbox Execute | Decision Author | Executable draft is valid | Simulation result and trace produced without production effect. |
| UC-10 | Submit Release | Decision Author | Candidate passes required validation | Release enters governance. |
| UC-11 | Calculate Risk Tier | System | Release submitted | Risk tier calculated from change scope, compatibility and 30-day traffic. |
| UC-12 | Approve/Reject Release | Approver(s) | Required approval task exists | Approval evidence recorded; quorum progresses or release rejected. |
| UC-13 | Overrule Risk Upward | Approver | Calculated tier exists | Tier increased; never decreased. |
| UC-14 | Build Executable Artifact | System | Release satisfies governance | Immutable artifact produced and integrity metadata recorded. |
| UC-15 | Shadow Deploy | Approver/Release Manager | Approved artifact exists | Candidate evaluates mirrored traffic without affecting response. |
| UC-16 | Analyze Shadow Diff | Authorized user | Shadow data exists | Outcome differences are queryable. |
| UC-17 | Canary Deploy | Approver/Release Manager | Eligible candidate exists | Sticky/cohort routing activates candidate for controlled traffic. |
| UC-18 | Promote Active | Approver/Release Manager | Release meets policy | Candidate becomes desired Active version. |
| UC-19 | Rollback | Approver/Release Manager | Eligible prior version exists | Desired Active pointer switches to prior immutable version. |
| UC-20 | Synchronize Runtime Fleet | System | Publish/rollback event emitted | Active nodes converge to desired artifact within SLA. |
| UC-21 | Evaluate Decision REST | Consumer App | Valid credential + request contract | Decision result returned. |
| UC-22 | Evaluate Decision gRPC | Consumer App | Valid credential + request contract | Decision result returned. |
| UC-23 | Evaluate Pinned Version | Consumer App | Requested version supplied | Exact version executes or 412 returned. |
| UC-24 | Capture Execution Trace | System | Auditable execution occurs | Masked trace/ledger evidence persisted asynchronously/safely. |
| UC-25 | Explain Historical Decision | Authorized user | Execution retained | Decision/version/tree evidence returned per authorization. |
| UC-26 | Inspect Audit Evidence | Compliance/Security Auditor | Authorized scope | Governance/deployment/security evidence displayed/exportable. |
| UC-27 | Observe Fleet Convergence | Authorized operator/admin | Deployment in progress | Per-fleet desired/loaded state visible. |

