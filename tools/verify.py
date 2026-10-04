"""Check completeness of extraction, source preservation, counts and authored links."""
from pathlib import Path
import hashlib
import json
import re
from urllib.parse import unquote

OUT = Path(__file__).resolve().parents[1]
ROOT = OUT.parent
errors = []
checks = {}

def load(path):
    return json.loads((OUT / path).read_text(encoding='utf-8'))

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

manifest = load('registers/source-manifest.json')
for row in manifest:
    path = ROOT / row['source']
    if not path.exists() or sha(path) != row['sha256']:
        errors.append('Original source changed or missing: ' + row['source'])
    if row['treatment'] == 'Verbatim source snapshot':
        if sha(OUT / row['extracted']) != row['sha256']:
            errors.append('Source copy mismatch: ' + row['source'])
checks['original_files_unchanged'] = len(manifest)
checks['byte_preserved_textual_sources'] = sum(r['treatment'] == 'Verbatim source snapshot' for r in manifest)
expected = {'functional-requirements': 64, 'nonfunctional-requirements': 14,
            'core-use-cases': 27, 'architecture-constraints': 7, 'actors': 8,
            'goals': 10, 'business-outcomes': 5, 'adr-backlog': 10,
            'proposed-use-cases': 177, 'data-flows': 57}
for register, count in expected.items():
    rows = load('registers/' + register + '.json')
    checks[register] = len(rows)
    if len(rows) != count:
        errors.append(f'{register}: expected {count}, found {len(rows)}')
    keys = list(rows[0])
    id_key = 'flowId' if register == 'data-flows' else keys[0]
    if len({r[id_key] for r in rows}) != len(rows):
        errors.append('Duplicate identifiers: ' + register)

memory = load('registers/memory-manifest.json')
checks['recovered_sessions'] = len(memory['sessions'])
checks['recovered_attachments'] = len(memory['attachments'])
for row in memory['attachments']:
    raw = Path(row['source']).read_text(encoding='utf-8-sig')
    if not (OUT / row['extracted']).read_text(encoding='utf-8').endswith(raw):
        errors.append('Attachment text mismatch: ' + row['source'])

# Only newly authored links are checked: original evidence may intentionally
# contain stale links, which must not be silently rewritten in an archive.
authored = list(OUT.glob('*.md')) + list((OUT / 'baseline').glob('*.md')) + list((OUT / 'catalog').glob('*.md'))
authored += [OUT / 'memory/README.md', OUT / 'registers/README.md', OUT / 'registers/data-flows.md', OUT / 'registers/proposed-states.md']
link_count = 0
for p in authored:
    for link in re.findall(r'\]\(([^)]+)\)', p.read_text(encoding='utf-8')):
        if re.match(r'^[a-zA-Z]+://', link) or link.startswith('#'):
            continue
        dest = (p.parent / unquote(link.split('#')[0])).resolve()
        # This report is written at the end of this same check.
        if dest == OUT / 'registers/verification-report.json':
            continue
        link_count += 1
        if not dest.exists():
            errors.append(f'Broken authored link in {p.relative_to(OUT)}: {link}')
checks['authored_links_checked'] = link_count
extraction = load('registers/extraction-report.json')
errors.extend(extraction['errors'])
report = {'status': 'passed' if not errors else 'failed', 'checks': checks, 'errors': errors,
          'limits': ['No UML semantic certification or fresh image rendering',
                     'No runtime implementation or performance testing',
                     'PNG sources indexed without OCR or independent visual verification',
                     'Historical source claims retain original authority/status']}
(OUT / 'registers/verification-report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=True))
raise SystemExit(1 if errors else 0)
