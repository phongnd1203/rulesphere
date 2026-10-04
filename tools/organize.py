"""Build navigable indexes and small registers from collected evidence."""
from pathlib import Path
import csv
import json
import re
import shutil

OUT = Path(__file__).resolve().parents[1]

def write(path, text):
    p = OUT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8')

def table(rows):
    def cell(s):
        return str(s).replace('|', '\\|').replace('\n', '<br>')
    return '\n'.join(['| ' + ' | '.join(map(cell, rows[0])) + ' |',
                      '| ' + ' | '.join('---' for _ in rows[0]) + ' |'] +
                     ['| ' + ' | '.join(map(cell, row)) + ' |' for row in rows[1:]])

baseline = []
for p in sorted((OUT / 'baseline').glob('*.md')):
    if p.name == 'README.md':
        continue
    text = p.read_text(encoding='utf-8')
    heading = next((line.lstrip('# ') for line in text.splitlines() if line.startswith('## ')), p.stem)
    baseline.append(f'- [{heading}]({p.name})')
write('baseline/README.md', '# Approved SRS source sections\n\nExtracted from `RuleSphere_SRS_v1.0_Final.docx`, RS-SRS-001, v1.0 Final / B3. The first file is document metadata; subsequent files retain source headings and tables.\n\n' + '\n'.join(baseline) + '\n')

cat_root = OUT / 'sources/workspace/use-case-diagrams/drawio-catalog'
source = (cat_root / 'source-catalog.md').read_text(encoding='utf-8')
heads = list(re.finditer(r'^# \d+\. Module ([A-Q]) [^\n]+', source, re.M))
module_links = []
for i, match in enumerate(heads):
    # End at next module or at the cross-cutting section after Q.
    end = heads[i+1].start() if i+1 < len(heads) else source.index('# 20. Cross-Cutting')
    block = source[match.start():end].strip()
    label = match.group(0).lstrip('# ')
    fname = f'module-{match.group(1)}.md'
    write('catalog/' + fname, '# Proposed catalog source section\n\nStatus: **Proposed**, not automatically approved SRS requirements. Source: [full catalog](../sources/workspace/use-case-diagrams/drawio-catalog/source-catalog.md). Interpret relationships alongside [module notes](../sources/workspace/use-case-diagrams/drawio-catalog/module-notes.md), which contain later modeling refinements.\n\n' + block + '\n')
    module_links.append(f'- [{label}]({fname})')
write('catalog/README.md', '# Proposed 177-use-case catalog\n\nThe later A–Q catalog is distinct from the approved 27 core SRS use cases. IDs and names are preserved.\n\n' + '\n'.join(module_links) + '\n\n[Complete actor, cross-cutting, relationship and module source](../sources/workspace/use-case-diagrams/drawio-catalog/source-catalog.md).\n')
shutil.copyfile(cat_root / 'catalog-traceability.csv', OUT / 'registers/proposed-use-cases.csv')
with (cat_root / 'catalog-traceability.csv').open(encoding='utf-8-sig', newline='') as stream:
    catalog = list(csv.DictReader(stream))
write('registers/proposed-use-cases.json', json.dumps(catalog, ensure_ascii=False, indent=2) + '\n')

diagrams = json.loads((OUT / 'registers/diagram-content.json').read_text(encoding='utf-8'))
dfd = next(d for d in diagrams if d['source'] == 'dfd-diagrams/RuleSphere_Context_Yourdon_DeMarco.drawio')
flows = [obj for page in dfd['pages'] for obj in page['objects'] if obj.get('flowId')]
flow_rows = [['ID', 'Source', 'Destination', 'Name', 'Represents']] + [[o.get(k, '') for k in ('flowId', 'source', 'destination', 'dataFlowName', 'represents')] for o in flows]
write('registers/data-flows.md', '# All 57 context data flows\n\nExtracted from current Draw.io object metadata in [original](../../dfd-diagrams/RuleSphere_Context_Yourdon_DeMarco.drawio). These are context/model facts, not 57 separately approved SRS requirements.\n\n' + table(flow_rows) + '\n')
with (OUT / 'registers/data-flows.csv').open('w', encoding='utf-8', newline='') as stream:
    csv.writer(stream).writerows(flow_rows)
write('registers/data-flows.json', json.dumps(flows, ensure_ascii=False, indent=2) + '\n')

attachment = '2cb03736-48a8-4eb3-a940-5a7e2f8fcaaf'
state_text = (OUT / f'memory/attachments/{attachment}.md').read_text(encoding='utf-8')
state_table = re.search(r'\| Aggregate / Entity \| States \|\n(?:\|[^\n]*\n?)+', state_text).group(0)
write('registers/proposed-states.md', '# Recovered proposed state domains\n\nSource: [state proposal attachment](../memory/attachments/' + attachment + '.md), section 28. State names are preserved verbatim. This summary is not an approved replacement for SRS lifecycle rules; the full attachment includes additional transitions and execution-result discussion.\n\n' + state_table + '\n')

registers = [
 ('functional-requirements', '64 approved functional requirements'),
 ('nonfunctional-requirements', '14 approved NFRs'),
 ('core-use-cases', '27 approved core use cases with pre/postconditions'),
 ('architecture-constraints', '7 approved architecture constraints'),
 ('actors', '8 SRS actors'), ('goals', '10 system goals'),
 ('business-outcomes', '5 business outcomes'), ('adr-backlog', '10 open ADR candidates'),
 ('proposed-use-cases', '177 later proposed catalog items'),
 ('data-flows', '57 current DFD flows')]
write('registers/README.md', '# Structured knowledge registers\n\n' + table([['Register', 'CSV', 'JSON']] +
    [[description, f'[CSV]({name}.csv)', f'[JSON]({name}.json)'] for name, description in registers]) +
    '\n\n- [Proposed state-domain summary](proposed-states.md)\n- [Diagram labels, Draw.io cells/edges and object metadata](diagram-content.json)\n- [Workspace source manifest with SHA-256](source-manifest.json)\n- [Memory provenance](memory-manifest.json)\n- [Extraction report](extraction-report.json)\n- [Verification report](verification-report.json)\n')
print(json.dumps({'catalog_modules': len(heads), 'proposed_use_cases': len(catalog), 'dfd_flows': len(flows)}))
