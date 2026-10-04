# RuleSphere knowledge base

Collected on 2026-10-04 from this workspace, accessible local RuleSphere conversation history, and user attachments. This collection preserves source evidence and adds a navigable synthesis; it does not approve new requirements.

**Product:** RuleSphere - Business Rule Management Platform. The approved SRS describes its scope as an enterprise deterministic Business Decision Management Platform. The product covers decision management, delivery and execution.

## Start here

| File | Contents |
| --- | --- |
| [Product and scope](01-product-and-scope.md) | Purpose, boundaries, goals, actors and baseline authority |
| [Domain and architecture](02-domain-and-architecture.md) | Concepts, ownership, three planes, components and design proposals |
| [Behavior and lifecycles](03-behavior-and-lifecycles.md) | Authoring, approval, deployment, execution, trace and failures |
| [Quality, security and interfaces](04-quality-security-interfaces.md) | Exact NFR targets, APIs, isolation, privacy, retention and verification |
| [Catalogs and data flows](05-catalogs-and-data-flows.md) | Approved 27 UCs, proposed 177 UCs, historical 201 UCs and 57 DFD flows |
| [Diagram knowledge](06-diagrams-and-conventions.md) | Available models, drawing preferences, notation and source relationships |
| [Recovered decisions and history](07-history-and-memory.md) | User preferences, timeline, recovered attachments and memory limits |
| [Conflicts and open decisions](08-conflicts-and-open-decisions.md) | Source disagreements, proposal boundaries and ADR backlog |
| [Source index](SOURCE_INDEX.md) | All 245 workspace sources, treatment and snapshot links |
| [Memory index](memory/README.md) | Eight historical conversations and six attachments |

## Full detail and machine-readable knowledge

- [Full SRS extraction](sources/srs-full.md) preserves paragraphs and tables from the DOCX. [Baseline section index](baseline/README.md) breaks it into smaller files.
- [Proposed catalog index](catalog/README.md) separates the 17 modules A–Q without changing their status. The complete original catalog and its relationship tables are preserved under `sources/workspace/use-case-diagrams/drawio-catalog/`.
- [Data-flow register](registers/data-flows.md) records all 57 named flows, endpoints and represented data.
- [Proposed state register](registers/proposed-states.md) preserves the recovered state-domain summary, including proposals absent from current diagrams.
- [Registers](registers/README.md) provide CSV/JSON requirements, actors, goals, use cases, constraints, ADRs, diagram text, cells and edges.
- `sources/workspace/` contains byte-preserving copies of textual sources, editable diagrams, model data, scripts, reports and the Draw.io backup. These are reference snapshots; do not run the archived generators to update the originals.

## How to interpret the evidence

The SRS identifies itself as RS-SRS-001, v1.0 Final, B3 Sponsor Sign-off, dated 29 September 2026. Its confirmed requirements take priority when summarizing the approved baseline. Later user instructions establish naming and presentation preferences; the supplied expanded catalog and state attachment explicitly remain proposals. Diagram details, past assistant reports and review checkboxes do not independently establish approval or implementation.

Use source-qualified IDs: `SRS:UC-01` is Manage Tenant & Workspaces; the older candidate catalog's `UC-01` is Create Decision Project. Do not merge these identities. The 177-item catalog uses module prefixes such as IAM, AUT and EXE.

## Coverage and limits

All 245 current project files outside `.git` and this output directory are inventoried and SHA-256 hashed. Text sources were preserved, DOCX tables extracted, and Draw.io/SVG text and metadata made searchable. PNG previews are indexed at their original locations; they were not OCR-transcribed or independently visually verified. This is a knowledge collection, not a new UML conformance or rendering audit.

Eight accessible RuleSphere-era conversations and six pasted attachments were recovered. The local memory directory was empty and the persistent-memory database contained zero RuleSphere matches. Historical conversation exports include user messages and visible assistant responses; they exclude private reasoning, tool traces, approval-review transcripts and unrelated projects. Earlier BRMDM/BPM/Lighthouse work is not silently adopted into RuleSphere B3.

Remote Drive files, other machines, inaccessible ChatGPT history, Git object history and permanently deleted untracked files were not searched. Full completeness beyond the identified local evidence cannot be claimed. [Extraction report](registers/extraction-report.json) and [verification report](registers/verification-report.json) record actual coverage.

## Refresh

Run `python rulesphere-knowledge/tools/collect.py`, then `python rulesphere-knowledge/tools/organize.py`, then `python rulesphere-knowledge/tools/verify.py` from the project root. These write only inside `rulesphere-knowledge/`. The narrative topic files are curated and need review when source facts change; refreshing extraction does not update them automatically.
