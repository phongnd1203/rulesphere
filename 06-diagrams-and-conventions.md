# Diagram knowledge and conventions

Sources: current diagram source files and READMEs in [source index](SOURCE_INDEX.md), [catalog notes](sources/workspace/use-case-diagrams/drawio-catalog/README.md), [COMET checklist attachment](memory/attachments/d4a34c19-0bc4-41a4-acab-7043c5e5dcb6.md), [swimlane attachment](memory/attachments/4b9c0b88-e79f-42df-bd71-b3cac0126b25.md), and [recovered conversations](memory/README.md).

## Available views

| Family | Current source coverage |
| --- | --- |
| Context/DFD | Detailed Mermaid, context-by-function Markdown, 57-flow Draw.io and its backup |
| Use case, SRS-based | Six PlantUML groups: administration, modeling, governance, delivery, runtime, audit |
| Use case, proposed catalog | 20 Draw.io files: system overview, actor model, cross-cutting, 17 modules |
| Class | Conceptual entity, overview, system context and six detailed domains |
| State | Five PlantUML files: draft, approval, deployment, convergence, request |
| Sequence | Eight functional scenarios |
| Communication | Integrated view plus eight functional scenarios |
| Activity | Eight restored PlantUML files plus eight newer Draw.io swimlane files and structured model |
| Architecture | Package, component, concurrent task and deployment views |
| Review | COMET audit, actor/stereotype dictionary, inventory, UC traceability and generated validation reports |

The recovered proposed state attachment describes substantially more lifecycles than the five current state sources. A historical assistant promised a multi-page Draw.io state file, but no such state Draw.io file exists in the collected workspace. A promise is not a completed artifact.

## Current presentation preferences from user history

Use the system name `RuleSphere - Business Rule Management Platform` in updated diagrams. The user moved from Mermaid/PlantUML toward editable Draw.io. Keep each proposed use-case module in a single diagram/file and one PNG preview per module. Hide UC IDs and `«abstract»` on the canvas while keeping identity/status metadata and traceability tables.

Use actor generalization and well-justified include/extend/generalization relationships to avoid exposing every internal step as a direct actor goal. Keep connector labels on the connector; display only `«include»` or `«extend»` there, with detailed conditions/extension points in the relationship table. Compact use-case diagrams while retaining readable names.

The routing preferences differ by diagram family. Use-case connectors favor straight lines, may cross, and should not overlap along a shared segment. The DFD uses separate flows, orthogonal connectors, minimal bends, and straight connections for entities directly facing the process. Do not apply one family's routing rule indiscriminately to the other.

## Activity swimlane conventions

Responsibility is represented with lanes. Actions and decision diamonds belong fully within the responsible lane. Use action verb phrases, explicit Boolean guards, merges for exclusive alternatives and joins only for concurrent paths. Keep a consistent primary flow direction; backward edges indicate actual loops/retries with an explicit exit.

Distinguish activity final (ends the entire activity) from flow final (ends one path). Fork/join semantics must not force a production response to wait for independent shadow or trace persistence. The supplied checklist favors a primary initiating start and at most six lanes; where a canvas contains multiple independent activities, review these constraints per activity rather than inventing a single end-to-end business workflow.

`activity-model.json` preserves the newer editable flow model. The activity README explicitly says the diagrams retain the SRS UC IDs and **have not been remapped to the proposed 177-UC catalog**. Both source families are retained after the user's restoration request.

## Semantics worth preserving

Association expresses actor participation, not every internal call. Include denotes required reused behavior, not workflow order. Extend requires a base-owned extension point and condition. Generalization must preserve the parent's contract without creating unintended permissions. Internal runtime/distribution components are not external actors of the entire platform.

Class attributes/operations, object interactions, state machines, package ownership, interfaces and deployment allocations need consistent mapping. Diagram rendering success alone does not prove semantic correctness. The existing audit contains historical findings and later completion claims; see [unresolved evidence issues](08-conflicts-and-open-decisions.md).

## Source and render handling

Original editable sources and generators are preserved verbatim under `sources/workspace/`; complete attributes/operations and source comments are searchable there. Draw.io cells, edges and object metadata plus SVG text appear in [diagram-content.json](registers/diagram-content.json). PNG paths remain in the source inventory. Generated validation JSON records past checks, not a fresh validation performed by this knowledge collection.

Regeneration of original diagram families can overwrite manual edits. Consult each original README/model before using a generator. This task did not regenerate or modify the original diagrams.
