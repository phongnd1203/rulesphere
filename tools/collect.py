"""Collect local RuleSphere evidence without modifying original sources.

Run from anywhere with Python 3. Standard library only. Historical messages are
evidence, never executable instructions. This does not execute archived scripts.
"""
from pathlib import Path
import base64
import csv
import hashlib
import html
import json
import re
import sqlite3
import urllib.parse
import xml.etree.ElementTree as ET
import zipfile
import zlib

OUT = Path(__file__).resolve().parents[1]
ROOT = OUT.parent
CODEX = Path.home() / '.codex'
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
manifest = []
errors = []

def write(path, text):
    p = OUT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8')

def json_write(path, data):
    write(path, json.dumps(data, ensure_ascii=False, indent=2) + '\n')

def digest(data):
    return hashlib.sha256(data).hexdigest()

def plain(value):
    return html.unescape(re.sub('<[^>]+>', ' ', value or '')).strip()

def mdcell(value):
    return value.replace('|', '\\|').replace('\n', '<br>')

def table(rows):
    if not rows:
        return ''
    return '\n'.join(['| ' + ' | '.join(map(mdcell, rows[0])) + ' |',
                      '| ' + ' | '.join('---' for _ in rows[0]) + ' |'] +
                     ['| ' + ' | '.join(map(mdcell, row)) + ' |' for row in rows[1:]])

def docx_extract(path):
    with zipfile.ZipFile(path) as z:
        body = ET.fromstring(z.read('word/document.xml')).find('w:body', NS)
        parts = []
        tables = []
        for el in body:
            if el.tag.endswith('}p'):
                t = ''.join(n.text or '' for n in el.findall('.//w:t', NS))
                style = el.find('w:pPr/w:pStyle', NS)
                name = style.get('{'+NS['w']+'}val', '') if style is not None else ''
                if name.startswith('Heading'):
                    t = '#' * (int(name[-1]) + 1) + ' ' + t
                elif name == 'ListBullet':
                    t = '- ' + t
                if t:
                    parts.append(t)
            elif el.tag.endswith('}tbl'):
                rows = [['\n'.join(''.join(n.text or '' for n in p.findall('.//w:t', NS))
                                  for p in c.findall('w:p', NS))
                         for c in row.findall('w:tc', NS)] for row in el.findall('w:tr', NS)]
                parts.append(table(rows))
                tables.append(rows)
        # Preserve supplementary text as well, if present.
        for name in z.namelist():
            if re.match(r'word/(header\d+|footer\d+|footnotes|endnotes|comments)\.xml$', name):
                xml = ET.fromstring(z.read(name))
                texts = [''.join(n.text or '' for n in p.findall('.//w:t', NS)) for p in xml.findall('.//w:p', NS)]
                if any(texts):
                    parts.append('## DOCX supplementary part: ' + name + '\n\n' + '\n\n'.join(texts))
    return '\n\n'.join(parts) + '\n', tables

def drawio_extract(data):
    tree = ET.fromstring(data)
    diagrams = tree.findall('diagram') if tree.tag == 'mxfile' else [tree]
    pages = []
    for diagram in diagrams:
        model = diagram.find('mxGraphModel')
        if model is None:
            if diagram.tag == 'mxGraphModel':
                model = diagram
            elif diagram.text and diagram.text.strip():
                model = ET.fromstring(urllib.parse.unquote(zlib.decompress(base64.b64decode(diagram.text), -15).decode()))
            else:
                continue
        cells = []
        for cell in model.iter('mxCell'):
            d = {k: v for k, v in cell.attrib.items() if k != 'style'}
            d['label'] = plain(cell.get('value'))
            cells.append(d)
        objects = [dict(obj.attrib) for obj in model.iter() if obj.tag in ('object', 'UserObject')]
        pages.append({'name': diagram.get('name', ''), 'cells': cells, 'objects': objects})
    return pages

source_files = sorted(p for p in ROOT.rglob('*') if p.is_file() and
                      not any(x in p.relative_to(ROOT).parts for x in ('.git', 'rulesphere-knowledge', '__pycache__')))
diagram_index = []
srs_tables = []
for path in source_files:
    rel = path.relative_to(ROOT).as_posix()
    try:
        data = path.read_bytes()
        entry = {'source': rel, 'bytes': len(data), 'sha256': digest(data)}
        suffix = path.suffix.lower()
        if suffix == '.docx':
            text, srs_tables = docx_extract(path)
            target = 'sources/srs-full.md'
            write(target, '# SRS v1.0 Final — extracted source\n\nSource: `' + rel + '`. Tables and text extracted from DOCX; layout is not reproduced.\n\n' + text)
            entry.update(treatment='DOCX text and tables extracted', extracted=target)
            sections = re.split(r'(?=^## (?!#))', text, flags=re.M)
            for i, section in enumerate(sections):
                if not section.strip():
                    continue
                heading = section.splitlines()[0].lstrip('# ').strip()
                slug = re.sub(r'[^a-z0-9]+', '-', heading.lower()).strip('-')[:90]
                write(f'baseline/{i:02d}-{slug}.md', '# SRS source section\n\nSource: `RuleSphere_SRS_v1.0_Final.docx`. Requirements retain their original status; extraction is not a new approval.\n\n' + section)
        elif suffix in ('.png', '.jpg', '.jpeg'):
            entry['treatment'] = 'Rendered image indexed; original retained, no OCR or visual verification'
        elif suffix == '.svg':
            svg = ET.fromstring(data)
            labels = [''.join(el.itertext()) for el in svg.iter() if el.tag.endswith('}text') or el.tag == 'text']
            diagram_index.append({'source': rel, 'kind': 'svg', 'labels': labels})
            entry['treatment'] = 'SVG text extracted to diagram-content.json; original retained'
        else:
            # Byte-preserving copies include generators, source models, reports and backups.
            target = OUT / 'sources/workspace' / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            entry.update(treatment='Verbatim source snapshot', extracted=target.relative_to(OUT).as_posix())
            if suffix == '.drawio' or path.name.endswith('.drawio.bkp'):
                diagram_index.append({'source': rel, 'kind': 'drawio', 'pages': drawio_extract(data)})
        manifest.append(entry)
    except Exception as e:
        errors.append({'source': rel, 'error': str(e)})

# Structured baseline registers preserve the DOCX table headers verbatim.
registers = {}
for rows in srs_tables:
    if len(rows) < 2:
        continue
    first = rows[1][0]
    family = next((name for prefix, name in [('FR-', 'functional-requirements'), ('NFR-', 'nonfunctional-requirements'),
                   ('UC-', 'core-use-cases'), ('AC-', 'architecture-constraints'), ('ADR-', 'adr-backlog'),
                   ('BO-', 'business-outcomes'), ('A01', 'actors'), ('G1', 'goals')] if first.startswith(prefix)), None)
    if family:
        records = [dict(zip(rows[0], row)) for row in rows[1:]]
        registers[family] = records
        json_write(f'registers/{family}.json', records)
        p = OUT / f'registers/{family}.csv'
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open('w', encoding='utf-8', newline='') as stream:
            writer = csv.writer(stream)
            writer.writerows(rows)
json_write('registers/diagram-content.json', diagram_index)

# Select RuleSphere-era sessions in this exact workspace. Exclude reviewer traces,
# analysis, tool output and unrelated earlier projects using the same directory.
sessions = []
attachment_ids = set()
current_id = '01a10727-aced-73c1-b9e0-18d5994180b9'
for folder in ('sessions', 'archived_sessions'):
    for p in sorted((CODEX / folder).rglob('*.jsonl')):
        try:
            records = [json.loads(line) for line in p.read_text(encoding='utf-8').splitlines() if line.strip()]
            meta = next((o['payload'] for o in records if o.get('type') == 'session_meta'), {})
            if str(meta.get('cwd', '')).replace('\\', '/').lower() != ROOT.as_posix().lower():
                continue
            if str(meta.get('timestamp', '')) < '2026-09-29T14:00:00':
                continue
            if meta.get('id') == current_id:
                continue
            messages = []
            reviewer = False
            for o in records:
                q = o.get('payload', {})
                if o.get('type') != 'response_item' or q.get('type') != 'message' or q.get('role') not in ('user', 'assistant'):
                    continue
                if q.get('role') == 'assistant' and q.get('channel') not in ('final', 'commentary', None):
                    continue
                t = '\n'.join(c.get('text', '') for c in q.get('content', []) if isinstance(c, dict))
                if 'The following is the Codex agent history' in t:
                    reviewer = True
                    break
                if any(marker in t for marker in ('<environment_context>', '<skills_instructions>', '<codex_internal_context', '<permissions instructions>')):
                    continue
                if t.strip():
                    messages.append({'role': q['role'], 'timestamp': o.get('timestamp'), 'text': t})
            if reviewer or not messages:
                continue
            combined = '\n'.join(m['text'] for m in messages)
            # Current workspace sessions after the SRS handoff, supported by RuleSphere
            # references or explicit diagram activity, are project history.
            if not re.search(r'rulesphere|diagram|swimlane', combined, re.I):
                continue
            for match in re.findall(r'attachments[/\\]([0-9a-f-]{36})', combined):
                attachment_ids.add(match)
            target = 'memory/sessions/' + p.stem + '.md'
            text = '# Recovered RuleSphere conversation\n\nHistorical evidence only. User requests describe past intent; assistant statements are reports, not independently verified facts.\n\n'
            text += f"Session: `{meta.get('id')}`. Started: `{meta.get('timestamp')}`.\n\n"
            text += '\n\n'.join(f"## {i+1}. {m['role']} — {m['timestamp']}\n\n{m['text']}" for i, m in enumerate(messages))
            write(target, text + '\n')
            sessions.append({'session_id': meta.get('id'), 'source': str(p), 'extracted': target, 'messages': len(messages)})
        except Exception as e:
            errors.append({'source': str(p), 'error': str(e)})

attachments = []
for p in sorted((CODEX / 'attachments').rglob('*')):
    if not p.is_file() or p.suffix.lower() not in ('.txt', '.md'):
        continue
    text = p.read_text(encoding='utf-8-sig', errors='strict')
    if 'rulesphere' not in text.lower() and p.parent.name not in attachment_ids:
        continue
    target = 'memory/attachments/' + p.parent.name + '.md'
    write(target, '# Recovered user attachment\n\nSource attachment ID: `' + p.parent.name + '`. Original text follows verbatim; proposals and historical instructions retain their original status.\n\n' + text)
    attachments.append({'source': str(p), 'sha256': digest(p.read_bytes()), 'extracted': target, 'characters': len(text)})

memory_rows = []
memory_status = ''
try:
    db = CODEX / 'memories_1.sqlite'
    uri = 'file:' + db.as_posix() + '?mode=ro&immutable=1'
    with sqlite3.connect(uri, uri=True) as conn:
        memory_rows = conn.execute("SELECT thread_id,raw_memory,rollout_summary FROM stage1_outputs WHERE lower(raw_memory || rollout_summary) LIKE '%rulesphere%'").fetchall()
    memory_status = f'{len(memory_rows)} RuleSphere matches in persistent memory database (read-only snapshot).'
except Exception as e:
    memory_status = 'Persistent memory database unavailable: ' + str(e)
for thread, raw, summary in memory_rows:
    write(f'memory/persistent/{thread}.md', '# Recovered persistent memory\n\n' + summary + '\n\n' + raw)

json_write('registers/source-manifest.json', manifest)
json_write('registers/memory-manifest.json', {'persistent_memory': memory_status, 'sessions': sessions, 'attachments': attachments})
json_write('registers/extraction-report.json', {'workspace_files': len(source_files), 'indexed_files': len(manifest),
    'counts': {key: len(value) for key, value in registers.items()}, 'sessions': len(sessions), 'attachments': len(attachments),
    'diagram_sources': len(diagram_index), 'errors': errors})
write('SOURCE_INDEX.md', '# Workspace source index\n\nEvery source is hashed in [source-manifest.json](registers/source-manifest.json). Rendered images are retained at their original paths. SVG labels and Draw.io cells/edges are searchable in [diagram-content.json](registers/diagram-content.json).\n\n' +
      table([['Source', 'Treatment', 'Snapshot/extraction']] + [[f'[{e["source"]}](../{urllib.parse.quote(e["source"])})', e['treatment'],
      f'[Open]({urllib.parse.quote(e["extracted"])})' if 'extracted' in e else 'See diagram register / original'] for e in manifest]) + '\n')
write('memory/README.md', '# Recovered project memory\n\n' + memory_status + '\n\nThe local `memories/` directory contained no files at collection time. Accessible project conversations and pasted attachments provide the historical evidence below. Private reasoning, tool traces, approval-review transcripts and unrelated projects are excluded. This is not access to all ChatGPT history or remote account memory.\n\n## Conversations\n\n' +
      '\n'.join(f'- [{s["session_id"]}]({s["extracted"].removeprefix("memory/")}) — {s["messages"]} messages' for s in sessions) +
      '\n\n## Pasted source material\n\n' + '\n'.join(f'- [{Path(a["source"]).parent.name}]({a["extracted"].removeprefix("memory/")}) — {a["characters"]} characters' for a in attachments) + '\n')
print(json.dumps({'files': len(manifest), 'register_counts': {k: len(v) for k,v in registers.items()}, 'sessions': len(sessions), 'attachments': len(attachments), 'errors': errors}, ensure_ascii=True))
