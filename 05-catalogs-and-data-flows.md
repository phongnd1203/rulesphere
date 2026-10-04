# Use-case catalogs and data flows

## Three distinct catalogs

| Catalog | Status | Identity and coverage |
| --- | --- | --- |
| SRS v1.0 Final | Approved baseline as declared by the document | 27 core UCs; `UC-01` through `UC-27` |
| Earlier pasted catalog | Historical candidate/proposal | 201 numbered UCs over 20 groups; repeats `UC-*` identifiers with different meanings |
| Later A–Q catalog | Proposed use-case baseline | 177 coded UCs over 17 modules; module-prefixed IDs plus supporting/cross-cutting constructs |

The [approved UC register](registers/core-use-cases.csv) preserves actors, preconditions and postconditions. The [201-item attachment](memory/attachments/3eb187d5-da72-4da3-ae8d-421a44267f3a.md) includes broader ideas such as batch execution and webhook integration that cannot be promoted to confirmed B3 requirements. Its heading suggests 15 top-level UCs, while its subsequent list and conclusion actually give 19; preserve this as a source inconsistency.

The [later catalog](sources/workspace/use-case-diagrams/drawio-catalog/source-catalog.md), [177-row traceability](sources/workspace/use-case-diagrams/drawio-catalog/catalog-traceability.csv), [relationships](sources/workspace/use-case-diagrams/drawio-catalog/relationships.csv) and [supporting UCs](sources/workspace/use-case-diagrams/drawio-catalog/supporting-use-cases.csv) are separate evidence. Reusing old UC numbers as if these catalogs were one set would produce incorrect traceability.

## Approved use-case groups

| Core IDs | Coverage |
| --- | --- |
| UC-01–04 | Tenants/workspaces, membership/roles, credentials, shared libraries |
| UC-05–09 | Create/edit decision, model graph, version schemas, validate, sandbox |
| UC-10–14 | Submit, calculate risk, approve/reject, upward override, build |
| UC-15–20 | Shadow, compare, Canary, promote, rollback, synchronize fleet |
| UC-21–23 | REST, gRPC and pinned execution |
| UC-24–27 | Trace capture, historical explanation, audit inspection, convergence visibility |

## Proposed modules

| Module | Scope |
| --- | --- |
| A | Identity & Access Management |
| B | Decision Project & Asset Management |
| C | Decision Modeling & Rule Authoring |
| D | Data Contract Management |
| E | Validation & Testing |
| F | Version & Change Management |
| G | Review & Approval Governance; source heading also says Workflow |
| H | Build & Artifact Management |
| I | Environment & Deployment Management |
| J | Progressive Delivery |
| K | Decision Execution |
| L | Explainability & Decision Trace |
| M | Simulation & Impact Analysis |
| N | Runtime Operations & Observability |
| O | Audit & Compliance |
| P | Automation & CI/CD Integration |
| Q | Platform Administration |

[Module index](catalog/README.md) links each module's original prose, use-case table and proposed relationships. Four cross-cutting identities are UC-X01 Authorize Operation, UC-X02 Record Audit Event, UC-X03 Validate Decision and UC-X04 Resolve Decision Version. The implementation notes alias UC-X03 to VAL-01 and add supporting abstractions; these are not extra approved SRS UCs.

## Important catalog interpretations

The [module notes](sources/workspace/use-case-diagrams/drawio-catalog/module-notes.md) preserve these distinctions:

- Author can create/update a decision project; Administrator archives it. Do not associate Author with an abstract parent in a way that grants archive implicitly.
- Approval/reject/rework are mutually exclusive review outcomes. Internal authorization, approval-policy enforcement and credential validation are reusable behaviors, not manual user goals.
- The proposed publish UC is build-and-publish. Publishing an existing artifact would need a separate contract. Similarly its shadow comparison launches evaluation; querying historical comparisons is a distinct contract.
- Active and pinned execution specialize version resolution. Pinned execution must not first require Active resolution or silently fall back. Historical explanation resolves the execution's original version.
- Rollback can be recovery inside deployment and also an independently initiated later request. An optional behavior alone does not prove an extend relationship.
- Viewing runtime status does not include registering/deregistering nodes. Audit export records the export operation, not a recreation of all historical events.
- Dataset simulation does not establish a production batch/replay API. Actor inheritance does not grant unrestricted audit, execution or sensitive-data access.

## DFD context

The current Draw.io context is one RuleSphere process with nine external entities and **57 individual named flows**. The [flow register](registers/data-flows.md) captures each ID, source, destination, name and represented data from its object metadata. The [original flow inventory](memory/attachments/fdda4c66-6c59-478c-8808-76f029d0d6c3.md) is also retained.

External participants are Author, Reviewer/Approver, Administrator, Operations/SRE, Consumer, IdP/IAM, CI/CD, Observability and Audit/SIEM. Exchanges cover definitions, validation/test requests and results, lifecycle state, review packages/decisions, administration, deployment/health/convergence, evaluation contracts/results/errors, identity assertions, automation, telemetry and audit export.

Older SRS-based [context-by-function Markdown](sources/workspace/RuleSphere_Context_Diagram_By_Function.md) and [detailed Mermaid](sources/workspace/RuleSphere_Context_Diagram_Detailed.mmd) remain historical views. They use the SRS actor vocabulary and do not override the later diagram presentation or expand approved requirements automatically.
