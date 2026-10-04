# Proposed catalog source section

Status: **Proposed**, not automatically approved SRS requirements. Source: [full catalog](../sources/workspace/use-case-diagrams/drawio-catalog/source-catalog.md). Interpret relationships alongside [module notes](../sources/workspace/use-case-diagrams/drawio-catalog/module-notes.md), which contain later modeling refinements.

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
