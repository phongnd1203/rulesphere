"""Generate editable Draw.io activity diagrams from the retained structured model."""
from pathlib import Path
import json
import re
import html
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
W, GAP, STEP = 300, 70, 125


def guard(node, label):
    if node['kind'] == 'fork':
        return ''
    condition = node['text'].rstrip('?').replace('\n', ' ')
    if node['kind'] == 'switch':
        return f'[{condition} = {label}]'
    return f'[{condition}]' if label == 'yes' else f'[not ({condition})]'


def workflows(model):
    groups = []
    for node in model['items']:
        if node['kind'] == 'start':
            groups.append([])
        groups[-1].append(node)
    titles = {
        '04': ['Rollout Configuration', 'Production Evaluation and Shadow', 'Diff Analysis Query'],
        '05': ['Promotion or Rollback', 'Fleet Synchronization', 'Fleet Status Query'],
    }
    for index, items in enumerate(groups):
        page = dict(model, items=items)
        page['page_name'] = titles.get(model['name'][:2], [model['name'][3:].replace('_', ' ')])[index]
        page['page_index'] = index
        if len(groups) > 1:
            page['title'] = model['title'] + ' — ' + page['page_name']
        yield page


class Parser:
    def __init__(self, text):
        self.lines = [line.strip() for line in text.splitlines() if line.strip()]
        self.i = 0
        self.owner = ''
        self.notes = []

    def block(self, ends=()):
        out = []
        while self.i < len(self.lines):
            line = self.lines[self.i]
            if any(line.startswith(end) for end in ends):
                break
            self.i += 1
            if line.startswith('|'):
                self.owner = line.strip('|')
            elif line.startswith(':'):
                out.append(dict(kind='action', text=line[1:-1].replace('\\n', '\n'), owner=self.owner))
            elif line in ('start', 'stop'):
                out.append(dict(kind=line, text='', owner=self.owner))
            elif line.startswith('if ('):
                match = re.match(r'if \((.*)\) then \((.*)\)', line)
                node = dict(kind='if', text=match[1], owner=self.owner, branches=[])
                node['branches'].append(dict(label=match[2], items=self.block(('else', 'endif'))))
                if self.lines[self.i].startswith('else'):
                    label = self.lines[self.i][6:-1]
                    self.i += 1
                    node['branches'].append(dict(label=label, items=self.block(('endif',))))
                else:
                    node['branches'].append(dict(label='no', items=[]))
                self.i += 1
                out.append(node)
            elif line.startswith('switch ('):
                node = dict(kind='switch', text=line[8:-1], owner=self.owner, branches=[])
                while self.lines[self.i].startswith('case ('):
                    label = self.lines[self.i][6:-1]
                    self.i += 1
                    node['branches'].append(dict(label=label, items=self.block(('case (', 'endswitch'))))
                assert self.lines[self.i] == 'endswitch'
                self.i += 1
                out.append(node)
            elif line.startswith('while ('):
                match = re.match(r'while \((.*)\) is \((.*)\)', line)
                node = dict(kind='while', text=match[1], owner=self.owner, yes=match[2])
                node['items'] = self.block(('endwhile',))
                node['no'] = self.lines[self.i][10:-1]
                self.i += 1
                out.append(node)
            elif line == 'fork':
                node = dict(kind='fork', text='', owner=self.owner, branches=[])
                while True:
                    node['branches'].append(dict(label='', items=self.block(('fork again', 'end fork'))))
                    end = self.lines[self.i]
                    self.i += 1
                    if end == 'end fork':
                        break
                out.append(node)
            elif line.startswith(('note ', 'legend ')):
                end = 'end note' if line.startswith('note ') else 'endlegend'
                lines = []
                while self.lines[self.i] != end:
                    lines.append(self.lines[self.i])
                    self.i += 1
                self.i += 1
                self.notes.append('\n'.join(lines))
                if out and line.startswith('note '):
                    out[-1].setdefault('notes', []).append(len(self.notes))
            elif line.startswith(('@', 'title ', 'skinparam ', "'")):
                pass
            else:
                raise ValueError(f'Unsupported source line: {line}')
        return out


def measure(items):
    return max([size(n)[0] for n in items] + [W]), sum(size(n)[1] for n in items)


def size(n):
    if n['kind'] in ('if', 'switch', 'fork'):
        dimensions = [measure(b['items']) for b in n['branches']]
        return sum(w for w, h in dimensions) + GAP * (len(dimensions)-1), max(h for w, h in dimensions) + 2 * STEP
    if n['kind'] == 'while':
        w, h = measure(n['items'])
        return w + 2 * GAP, h + 3 * STEP
    return W, STEP


class Drawing:
    def __init__(self, title, width, height):
        self.doc = ET.Element('mxfile', host='app.diagrams.net')
        diagram = ET.SubElement(self.doc, 'diagram', id='activity', name=title)
        model = ET.SubElement(diagram, 'mxGraphModel', grid='1', gridSize='10', page='0', pageWidth=str(width), pageHeight=str(height), arrows='1', connect='1')
        self.root = ET.SubElement(model, 'root')
        ET.SubElement(self.root, 'mxCell', id='0')
        ET.SubElement(self.root, 'mxCell', id='1', parent='0')
        self.counter = 1
        self.bounds = {}
        self.owners = {}
        self.kinds = {}

    def cell(self, text, x, y, w, h, style):
        self.counter += 1
        key = str(self.counter)
        cell = ET.SubElement(self.root, 'mxCell', id=key, value=text, style=style, vertex='1', parent='1')
        ET.SubElement(cell, 'mxGeometry', x=str(x), y=str(y), width=str(w), height=str(h), **{'as': 'geometry'})
        self.bounds[key] = (x, y, w, h)
        return key

    def edge(self, a, b, label='', points=None, loop=False):
        if not a or not b:
            return
        self.counter += 1
        style = 'edgeStyle=orthogonalEdgeStyle;rounded=0;jumpStyle=arc;jumpSize=8;html=1;endArrow=block;endFill=1;strokeColor=#526579;fontSize=12;labelBackgroundColor=#FFFFFF;exitX=0.5;exitY=1;entryX=0.5;entryY=0;'
        if loop:
            style += 'entryX=0;entryY=0.5;'
        cell = ET.SubElement(self.root, 'mxCell', id=str(self.counter), value=html.escape(label), style=style, edge='1', parent='1', source=a, target=b)
        geom = ET.SubElement(cell, 'mxGeometry', relative='1', **{'as': 'geometry'})
        if points:
            array = ET.SubElement(geom, 'Array', **{'as': 'points'})
            for x, y in points:
                ET.SubElement(array, 'mxPoint', x=str(x), y=str(y))

    def node(self, n, cx, y, kind=None):
        key = self.raw_node(n, cx, y, kind)
        self.owners[key] = n['owner']
        self.kinds[key] = kind or n['kind']
        return key

    def raw_node(self, n, cx, y, kind=None):
        kind = kind or n['kind']
        common = 'html=1;whiteSpace=wrap;fontFamily=Arial;fontSize=13;strokeWidth=1.5;'
        if kind == 'start':
            return self.cell('', cx-13, y+25, 26, 26, common+'ellipse;fillColor=#243746;strokeColor=#243746;')
        if kind == 'stop':
            outer = self.cell('', cx-16, y+25, 32, 32, common+'ellipse;fillColor=#FFFFFF;strokeColor=#243746;')
            inner = self.cell('', 6, 6, 20, 20, common+'ellipse;fillColor=#243746;strokeColor=none;')
            self.root.find(f"mxCell[@id='{inner}']").set('parent', outer)
            return outer
        if kind in ('fork', 'join'):
            return self.cell('', cx-110, y+35, 220, 9, common+'fillColor=#243746;strokeColor=#243746;')
        if kind == 'merge':
            return self.cell('', cx-18, y+22, 36, 36, common+'rhombus;fillColor=#FFF4D9;strokeColor=#AD8B3A;')
        text = html.escape(n['text']).replace('\n', '<br>')
        if n.get('notes'):
            text += '<br><i>Note '+', '.join(map(str, n['notes']))+'</i>'
        if n.get('calls'):
            text += '<br><i>Sub-activity '+html.escape(n['calls'])+'</i><div style="text-align:right">&#9282;</div>'
        if kind in ('if', 'switch', 'while'):
            return self.cell(text, cx-145, y, 290, 100, common+'rhombus;fillColor=#FFF4D9;strokeColor=#AD8B3A;fontSize=12;spacing=5;')
        return self.cell(text, cx-W/2, y, W, 88, common+'rounded=1;arcSize=14;fillColor=#EDF5FF;strokeColor=#496477;spacing=9;')

    def block(self, items, x, y, width):
        first, previous = None, None
        for n in items:
            nw, nh = size(n)
            entry, end = self.part(n, x+(width-nw)/2, y, nw)
            if previous:
                self.edge(previous, entry)
            if first is None:
                first = entry
            previous = end
            y += nh
        return first, previous

    def part(self, n, x, y, width):
        kind = n['kind']
        cx = x+width/2
        entry = self.node(n, cx, y)
        if kind == 'stop':
            return entry, None
        if kind in ('if', 'switch', 'fork'):
            height = size(n)[1]
            end_y = y+height-STEP
            merge = self.node(n, cx, end_y, 'join' if kind == 'fork' else 'merge')
            bx = x
            live = False
            for branch in n['branches']:
                bw, bh = measure(branch['items'])
                branch_cx = bx+bw/2
                first, last = self.block(branch['items'], bx, y+STEP, bw)
                if first:
                    self.edge(entry, first, guard(n, branch['label']), [(cx,y+110),(branch_cx,y+110)])
                    if last:
                        self.edge(last, merge, points=[(branch_cx,end_y-15),(cx,end_y-15)])
                        live = True
                else:
                    self.edge(entry, merge, guard(n, branch['label']), [(cx,y+110),(branch_cx,y+110),(branch_cx,end_y-15),(cx,end_y-15)])
                    live = True
                bx += bw+GAP
            return entry, merge if live else None
        if kind == 'while':
            # A distinct loop-entry merge combines the first entry and repeat path.
            decision = entry
            entry = self.node(n, cx, y, 'merge')
            decision_cell = self.root.find(f"mxCell[@id='{decision}']")
            decision_cell.find('mxGeometry').set('y', str(y+STEP))
            dx, dy, dw, dh = self.bounds[decision]
            self.bounds[decision] = (dx, dy+STEP, dw, dh)
            self.edge(entry, decision)
            bw, bh = measure(n['items'])
            first, last = self.block(n['items'], x+GAP, y+2*STEP, bw)
            merge_y = y+size(n)[1]-STEP
            merge = self.node(n, cx, merge_y, 'merge')
            self.edge(decision, first, guard(n, n['yes']))
            self.edge(last, entry, 'repeat', [(cx,merge_y-20),(x+15,merge_y-20),(x+15,y+50)], loop=True)
            self.edge(decision, merge, guard(n, n['no']), [(cx,y+STEP+110),(x+width-15,y+STEP+110),(x+width-15,merge_y+40)], loop=False)
            return entry, merge
        return entry, entry

    def simplify_merges(self):
        # A sole surviving alternative needs no merge (e.g. fail-fast guards).
        for key in list(self.owners):
            if self.kinds[key] != 'merge':
                continue
            edges = [c for c in self.root.findall('mxCell') if c.get('edge') == '1']
            incoming = [e for e in edges if e.get('target') == key]
            outgoing = [e for e in edges if e.get('source') == key]
            if len(incoming) == 1 and len(outgoing) == 1:
                incoming[0].set('target', outgoing[0].get('target'))
                self.root.remove(outgoing[0])
            elif not incoming and not outgoing:
                pass
            else:
                continue
            self.root.remove(self.root.find(f"mxCell[@id='{key}']"))
            del self.owners[key]
            del self.kinds[key]

    def validate_uml(self):
        edges = [c for c in self.root.findall('mxCell') if c.get('edge') == '1']
        assert list(self.kinds.values()).count('start') == 1
        for key, kind in self.kinds.items():
            ins = [e for e in edges if e.get('target') == key]
            outs = [e for e in edges if e.get('source') == key]
            if kind in ('if', 'switch', 'while'):
                assert len(ins) == 1 and len(outs) >= 2, (kind, key, len(ins), len(outs))
                assert all(e.get('value', '').startswith('[') and e.get('value', '').endswith(']') for e in outs)
                assert len({e.get('value') for e in outs}) == len(outs)
            elif kind == 'merge':
                assert len(ins) >= 2 and len(outs) == 1, (kind, key, len(ins), len(outs))
            elif kind == 'fork':
                assert len(ins) == 1 and len(outs) >= 2
            elif kind == 'join':
                assert len(ins) >= 2 and len(outs) == 1
            elif kind == 'action':
                assert len(ins) == 1 and len(outs) == 1, (kind, key, len(ins), len(outs))
            elif kind == 'start':
                assert not ins and len(outs) == 1
            elif kind == 'stop':
                assert len(ins) == 1 and not outs
        assert list(self.kinds.values()).count('fork') == list(self.kinds.values()).count('join')

    def swimlanes(self, height):
        """Place native nodes inside responsibility containers and reroute flows."""
        owner_names = list(dict.fromkeys(self.owners.values()))
        cells = {c.get('id'): c for c in self.root.findall('mxCell')}
        edges = [c for c in cells.values() if c.get('edge') == '1']
        lane_info = {}
        left = 50
        for owner in owner_names:
            keys = [k for k in self.owners if self.owners[k] == owner]
            occupied = []
            preferred = {}
            assigned = {}
            for key in sorted(keys, key=lambda k: (self.bounds[k][1], self.bounds[k][0])):
                x, y, w, h = self.bounds[key]
                old_center = round(x+w/2)
                options = [i for i, bottom in enumerate(occupied) if bottom+20 <= y]
                previous = preferred.get(old_center)
                track = previous if previous in options else (options[0] if options else len(occupied))
                if track == len(occupied):
                    occupied.append(0)
                occupied[track] = y+h
                preferred[old_center] = track
                assigned[key] = track
            long_count = sum(1 for e in edges if e.get('source') in keys and abs(self.bounds[e.get('target')][1]-self.bounds[e.get('source')][1]) > STEP*1.5)
            gutter = max(65, 25+long_count*12)
            width = len(occupied)*(W+65)+2*gutter
            lane = self.cell(html.escape(owner), left, 140, width, height+140,
                             'swimlane;html=1;horizontal=1;startSize=55;container=1;collapsible=0;recursiveResize=0;whiteSpace=wrap;fontFamily=Arial;fontSize=17;fontStyle=1;fillColor=#DCE8F4;swimlaneFillColor=#FAFCFF;strokeColor=#8B9DAF;strokeWidth=1.5;')
            lane_cell = self.root.find(f"mxCell[@id='{lane}']")
            self.root.remove(lane_cell)
            self.root.insert(2+len(lane_info), lane_cell)
            lane_info[owner] = (left, width, gutter)
            for key in keys:
                _, y, w, h = self.bounds[key]
                nx = left+gutter+assigned[key]*(W+65)+(W+65-w)/2
                ny = y+70
                cell = cells[key]
                cell.set('parent', lane)
                geom = cell.find('mxGeometry')
                geom.set('x', str(nx-left))
                geom.set('y', str(ny-140))
                self.bounds[key] = (nx, ny, w, h)
                assert nx >= left and nx+w <= left+width
                assert ny >= 195 and ny+h <= height+280
            left += width
        used_channels = {owner: 0 for owner in owner_names}
        for edge in edges:
            a, b = edge.get('source'), edge.get('target')
            ax, ay, aw, ah = self.bounds[a]
            bx, by, bw, bh = self.bounds[b]
            sx, sy, tx = ax+aw/2, ay+ah, bx+bw/2
            geom = edge.find('mxGeometry')
            for child in list(geom):
                geom.remove(child)
            style = edge.get('style').split('exitX=')[0]
            points = []
            if by <= ay:
                owner = self.owners[a]
                lx, lw, gutter = lane_info[owner]
                used_channels[owner] += 1
                channel = lx+15+used_channels[owner]*10
                points = [(sx, sy+18), (channel, sy+18), (channel, by+bh/2)]
                style += 'exitX=0.5;exitY=1;entryX=0;entryY=0.5;'
            elif by-sy > STEP:
                owner = self.owners[a]
                lx, lw, gutter = lane_info[owner]
                used_channels[owner] += 1
                channel = lx+lw-15-used_channels[owner]*10
                points = [(sx, sy+18), (channel, sy+18), (channel, by-20), (tx, by-20)]
                style += 'exitX=0.5;exitY=1;entryX=0.5;entryY=0;'
            else:
                middle = (sy+by)/2
                points = [(sx, middle), (tx, middle)]
                style += 'exitX=0.5;exitY=1;entryX=0.5;entryY=0;'
            edge.set('style', style)
            array = ET.SubElement(geom, 'Array', **{'as': 'points'})
            for px, py in points:
                ET.SubElement(array, 'mxPoint', x=str(px), y=str(py))
        # Check that sibling nodes do not overlap inside any lane.
        for i, a in enumerate(self.owners):
            ax, ay, aw, ah = self.bounds[a]
            for b in list(self.owners)[i+1:]:
                bx, by, bw, bh = self.bounds[b]
                assert not (ax < bx+bw and bx < ax+aw and ay < by+bh and by < ay+ah), (a, b)
        return left-50, owner_names


def main():
    sources = sorted(HERE.glob('*.puml'))
    model_path = HERE/'activity-model.json'
    if sources:
        models = []
        for source in sources:
            text = source.read_text(encoding='utf-8')
            parser = Parser(text)
            items = parser.block()
            title = next(line[6:] for line in text.splitlines() if line.startswith('title ')).replace('\\n', ' — ')
            models.append(dict(name=source.stem, title=title, items=items, notes=parser.notes))
        model_path.write_text(json.dumps(models, ensure_ascii=False, indent=2), encoding='utf-8')
    else:
        models = json.loads(model_path.read_text(encoding='utf-8'))
    report = []
    documents = {}
    for model in [page for source in models for page in workflows(source)]:
        width, height = measure(model['items'])
        drawing = Drawing(model['title'], width+100, height+600)
        drawing.block(model['items'], 50, 150, width)
        drawing.simplify_merges()
        drawing.validate_uml()
        width, lanes = drawing.swimlanes(height)
        assert 3 <= len(lanes) <= 6, (model['page_name'], lanes)
        drawing.cell(html.escape(model['title']), 50, 20, width, 65, 'text;html=1;whiteSpace=wrap;fontSize=22;fontStyle=1;fontColor=#243746;align=center;')
        drawing.cell('Swimlanes identify responsibility. Diamonds: decision / merge. Bars: parallel fork / join.', 50, 85, width, 40, 'text;html=1;whiteSpace=wrap;fontSize=12;align=center;')
        note_y = height+305
        for index, note in enumerate(model['notes'], 1):
            note_h = 35+22*len(note.splitlines())
            drawing.cell('<b>Note '+str(index)+'</b><br>'+html.escape(note).replace('\n','<br>'), 50, note_y, width, note_h, 'shape=note;html=1;whiteSpace=wrap;align=left;spacing=12;fillColor=#FFF9E8;strokeColor=#D5BD72;fontSize=13;')
            note_y += note_h+15
        target = HERE/(model['name']+'.drawio')
        document = documents.setdefault(model['name'], ET.Element('mxfile', host='app.diagrams.net'))
        page = drawing.doc.find('diagram')
        page.set('id', 'workflow-'+str(model['page_index']))
        page.set('name', model['page_name'])
        document.append(page)
        ET.indent(document)
        ET.ElementTree(document).write(target, encoding='utf-8', xml_declaration=True)
        cells = drawing.root.findall('mxCell')
        ids = {c.get('id') for c in cells}
        assert len(ids) == len(cells)
        edges = [c for c in cells if c.get('edge') == '1']
        assert all(c.get('source') in ids and c.get('target') in ids for c in edges)
        actions = [c for c in cells if 'rounded=1' in c.get('style','')]
        if sources:
            original = (HERE/(model['name']+'.puml')).read_text(encoding='utf-8')
            assert len(actions) == sum(line.strip().startswith(':') for line in original.splitlines())
        report.append(dict(file=target.name, page=model['page_name'], swimlanes=lanes, actions=len(actions), connectors=len(edges), notes=len(model['notes']), uml_degrees_valid=True, valid=True))
    (HERE/'validation.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
