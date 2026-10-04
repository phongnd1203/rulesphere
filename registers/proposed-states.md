# Recovered proposed state domains

Source: [state proposal attachment](../memory/attachments/2cb03736-48a8-4eb3-a940-5a7e2f8fcaaf.md), section 28. State names are preserved verbatim. This summary is not an approved replacement for SRS lifecycle rules; the full attachment includes additional transitions and execution-result discussion.

| Aggregate / Entity | States |
|---|---|
| **Decision** | Active, Archived, Deleted |
| **Decision Version** | Draft, Validating, Validated, InReview, ChangesRequested, Reviewed, AwaitingApproval, Rejected, Approved, Superseded, Retired |
| **Validation Run** | NotValidated, Validating, Valid, Invalid |
| **Review Request** | Open, InProgress, ChangesRequested, Accepted, Cancelled |
| **Approval Request** | Pending, InProgress, Approved, Rejected, Cancelled |
| **Test Run** | Queued, Running, Passed, Failed, Error, Cancelled |
| **Artifact Build** | Queued, Building, Validating, Ready, Published, Failed, Cancelled, Deprecated, Retired |
| **Release** | Draft, Validating, Ready, Releasing, Released, Failed, Cancelled, Superseded, Retired |
| **Promotion** | NotPromoted, PromotionPending, Approved, Rejected, Deploying, Promoted, Failed, Cancelled |
| **Deployment** | Pending, Scheduled, Deploying, Verifying, Active, Updating, RollingBack, VerifyingRollback, RolledBack, Undeploying, Undeployed, Failed, Cancelled |
| **Runtime Instance Sync** | Unknown, Syncing, InSync, OutOfSync, Failed, Unavailable |
| **Rollout** | Pending, Initializing, Canary/Shadow/FullRollout, Verifying, Completed, Rollback, RolledBack, Cancelled |
| **Canary** | Pending, DeployingCanary, Observing, Paused, Promoting, Expanding, Completed, RollingBack, RolledBack, Failed |
| **Shadow** | Pending, Deploying, Shadowing, Evaluating, Accepted, Rejected, PromotionReady, Cancelled, Failed |
| **Runtime Artifact** | NotLoaded, Loading, Loaded, Active, Draining, Unloaded, Failed |
| **Execution Request** | Received, ValidatingInput, ResolvingDecision, Evaluating, Completed, Rejected, Failed, TimedOut |
| **Audit Delivery** | Captured, Persisting, Persisted, Failed, ExportPending, Exported, ExportFailed |
| **Webhook Delivery** | Pending, Delivering, Delivered, RetryPending, Failed, DeadLettered |
| **Import Job** | Uploaded, Parsing, Validating, Ready, Importing, Imported, Invalid, Failed |
| **Export Job** | Requested, Generating, Ready, Downloaded, Expired, Failed |
| **API Credential** | Active, Rotating, Suspended, Revoked, Expired |
| **Access Binding** | Active, Suspended, Revoked |
| **Automation Job** | Requested, Queued, Running, Succeeded, Failed, Cancelled |

