# RuleSphere ? Activity Diagrams

Eight editable Draw.io activity diagrams arranged in vertical swimlanes by actor or component. Actions, conditions, loops, parallel work, responsibility labels and explanatory notes are preserved.

| Activity | Draw.io | PNG preview |
| --- | --- | --- |
| 01 Administration | [Open](01_Administration.drawio) | [Preview](previews/01_Administration.png) |
| 02 Decision Modeling | [Open](02_Decision_Modeling.drawio) | [Preview](previews/02_Decision_Modeling.png) |
| 03 Governance and Approval | [Open](03_Governance_and_Approval.drawio) | [Preview](previews/03_Governance_and_Approval.png) |
| 04 Shadow and Canary | [Open](04_Shadow_and_Canary.drawio) | [Preview](previews/04_Shadow_and_Canary.png) |
| 05 Deployment and Convergence | [Open](05_Deployment_and_Convergence.drawio) | [Preview](previews/05_Deployment_and_Convergence.png) |
| 06 Runtime Evaluation | [Open](06_Runtime_Evaluation.drawio) | [Preview](previews/06_Runtime_Evaluation.png) |
| 07 Trace Capture | [Open](07_Trace_Capture.drawio) | [Preview](previews/07_Trace_Capture.png) |
| 08 Historical Explain and Audit | [Open](08_Historical_Explain_and_Audit.drawio) | [Preview](previews/08_Historical_Explain_and_Audit.png) |

## Reading the diagrams

- Each vertical swimlane names the responsible actor or component. Actions and decisions are editable children of that lane; connectors cross lanes when responsibility changes.
- Rounded rectangles are actions; diamonds are decisions or merges, with conditions on outgoing connectors.
- Solid circles start an activity; a black circle inside a white ring ends it.
- Thick bars fork and join parallel work. Loop connectors return to the controlling decision.
- Shadow/canary and deployment diagrams each contain three independent activity flows.
- Numbered notes retain the source constraints and operational assumptions.

These diagrams preserve the restored activity baseline and its UC identifiers; they have not been remapped to the newer 177-use-case catalog.

## Regeneration

`activity-model.json` retains the structured flow data. Run `python activity-diagrams/generate.py` to regenerate the Draw.io files, then `python activity-diagrams/render.py` to export PNG previews with draw.io Desktop. Regeneration overwrites generated diagrams, so incorporate manual edits into the model first.

`validation.json` records structural checks; `render-validation.json` records successful PNG exports.
