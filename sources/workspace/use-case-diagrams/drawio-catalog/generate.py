"""One editable Draw.io diagram per module, without duplicate actor/use-case nodes."""
from catalog_model import *
from collections import defaultdict, deque

abstract.add('UC-X04')
locations=defaultdict(list);relations=[];module_notes=[]

def graph(groups):
 nodes=[];edges=[];assoc=[]
 for z in groups:
  base=z['root'];nodes.append(base)
  for k in z['v']:nodes.append(k);edges.append((k,base,'generalization',''))
  for k in z['i']:nodes.append(k);edges.append((base,k,'include',''))
  for k,c in z['e']:nodes.append(k);edges.append((k,base,'extend',c))
  assoc.extend((a,base) for a in z['actors']);assoc.extend(z['support'])
 return list(dict.fromkeys(nodes)),list(dict.fromkeys(edges)),list(dict.fromkeys(assoc))

def layout(keys,edges):
 children=defaultdict(set);parent=defaultdict(set);neighbors=defaultdict(set);order={k:i for i,k in enumerate(keys)}
 for a,b,kind,_ in edges:
  left,right=(a,b) if kind=='include' else (b,a)
  children[left].add(right);parent[right].add(left);neighbors[a].add(b);neighbors[b].add(a)
 unseen=set(keys);components=[]
 while unseen:
  start=min(unseen,key=order.get);stack=[start];unseen.remove(start);comp=[]
  while stack:
   n=stack.pop();comp.append(n)
   for nxt in sorted(neighbors[n],key=order.get):
    if nxt in unseen:unseen.remove(nxt);stack.append(nxt)
  components.append(comp)
 single=[c[0] for c in components if len(c)==1];components=[c for c in components if len(c)>1];ranks={};blocks=[]
 for comp in components:
  indeg={k:len(parent[k]) for k in comp};queue=deque(sorted([k for k in comp if not indeg[k]],key=order.get));rank={k:0 for k in comp};visited=0
  while queue:
   k=queue.popleft();visited+=1
   for child in sorted(children[k],key=order.get):
    rank[child]=max(rank[child],rank[k]+1);indeg[child]-=1
    if not indeg[child]:queue.append(child)
  assert visited==len(comp),'Layout dependency cycle'
  cols=defaultdict(list)
  for k in sorted(comp,key=order.get):cols[rank[k]].append(k)
  for _ in range(4):
   for depth in range(1,max(cols)+1):
    prev={k:i for i,k in enumerate(cols[depth-1])}
    cols[depth].sort(key=lambda k:sum(prev[p] for p in parent[k] if p in prev)/max(1,sum(p in prev for p in parent[k])))
   for depth in range(max(cols)-1,-1,-1):
    nxt={k:i for i,k in enumerate(cols[depth+1])}
    cols[depth].sort(key=lambda k:sum(nxt[c] for c in children[k] if c in nxt)/max(1,sum(c in nxt for c in children[k])))
  blocks.append(cols);ranks.update(rank)
 if single:
  cols=defaultdict(list)
  for j,k in enumerate(single):cols[j%2].append(k);ranks[k]=j%2
  blocks.append(cols)
 pos={};cursor=245
 for cols in blocks:
  bh=max(len(v) for v in cols.values())*185
  for depth,col in cols.items():
   for j,k in enumerate(col):pos[k]=(530+depth*680,cursor+(j+.5)*bh/len(col)-52)
  cursor+=bh+125
 return pos,ranks,cursor

def make(filename,groups):
 keys,edges,associations=graph(groups);pos,ranks,bottom=layout(keys,edges)
 primary={a for z in groups for a in z['actors']};targets=defaultdict(list)
 for a,k in associations:targets[a].append(k)
 right=[a for a in targets if a not in primary];rightedge=max(x for x,y in pos.values())+365
 width=max(1750,rightedge+(315 if right else 55));height=max(1000,bottom+245)
 d=Diagram(filename.replace('_',' '),width,height);header(d,filename.replace('_',' '))
 d.cell('RuleSphere — '+filename.split('_')[0]+' / all module use cases',465,140,rightedge-465,bottom-90,'swimlane;html=0;startSize=40;fillColor=#eff6ff;swimlaneFillColor=#ffffff;strokeColor=#94a3b8;fontSize=20;fontStyle=1;align=left;spacingLeft=20;')
 ids={k:d.uc(k,*pos[k]) for k in keys}
 for a,b,kind,condition in edges:
  d.edge(ids[a],ids[b],kind,condition)
  relations.append((filename,a,kind,b,condition))
 for onright in [False,True]:
  roles=[a for a in targets if (a not in primary)==onright];roles.sort(key=lambda a:sum(pos[k][1] for k in targets[a])/len(targets[a]));previous=155
  for actor in roles:
   y=max(previous+170,sum(pos[k][1] for k in targets[actor])/len(targets[actor]));previous=y
   aid=d.actor(actor,rightedge+110 if onright else 125,y)
   for k in targets[actor]:d.edge(aid,ids[k])
   height=max(height,y+230)
 d.h=height;d.m.set('pageHeight',str(height))
 d.text('Solid line: association | Hollow triangle: specialized → general | «include»: base → required behavior | «extend»: conditional behavior → base',30,height-150,width-60,45,14)
 d.text('Each actor and catalog use case appears once in this module. Cross-module IDs reference reusable behavior. Actor inheritance: 01_Actor_Model.\nConditions, permissions and UML clarifications: module-notes.md. Proposed baseline; runtime is inside RuleSphere.',30,height-95,width-60,75,14)
 root=mxfile();d.append(root);save(root,filename)
 for k in keys:
  if k in catalog:locations[k].append(filename+'.drawio')
 module_notes.append('## '+filename.replace('_',' ')+'\n\n'+'\n\n'.join('**'+z['root']+' — '+names[z['root']]+'**: '+z['note'] for z in groups if z['note']))

for filename,prefix,groups in modules:
 own={key for key in catalog if key.split('-')[0] in prefix.split('/')}
 assert own<=set(graph(groups)[0]),(filename,'missing home-module use cases',own-set(graph(groups)[0]))
 make(filename,groups)
make('02_Cross_Cutting',[
 g('UC-X01',i=['IAM-04'],note='Authorization delegates to IAM-04. Protected goals keep authorization requirements when repeated edges are omitted.'),
 g('AUX-X-01',i=['UC-X01','UC-X02'],abstract=True,note='Architecture-level contract for state-changing operations; no business-process orchestration.'),
 g('UC-X04',v=['EXE-04','AUX-EXE-02'],abstract=True,note='Active/pinned resolution depends on execution context. Simulation and historical evidence resolve their bound version. UC-X03 aliases VAL-01.')])

d=Diagram('RuleSphere Actor Model',1800,1250);header(d,'RuleSphere — Actor Model')
for row,(parent,children) in enumerate(parents.items()):
 y=180+row*475;pa=d.actor(parent,820,y)
 for j,a in enumerate(children):d.edge(d.actor(a,70+j*1560/(len(children)-1),y+220),pa,'generalization')
d.text('5 main actors: Author, Reviewer / Approver, Platform Administrator, Operations / SRE, Decision Consumer / Client Application.\n4 supporting actors: Identity Provider / IAM, CI/CD & Automation, Observability Platform, Audit / SIEM.\nPlatform User provides only common account/read capabilities. External System grants no shared API permissions. Operations does not inherit Administrator.',40,1090,1720,125,17)
root=mxfile();d.append(root);save(root,'01_Actor_Model')

# Single system overview: six subject regions on one canvas.
d=Diagram('RuleSphere System Overview',3450,3260);header(d,'RuleSphere — 25 system-level use cases')
d.cell(SYSTEM_NAME,400,135,2710,3010,'swimlane;html=0;startSize=45;fillColor=#eff6ff;swimlaneFillColor=#ffffff;strokeColor=#64748b;fontSize=23;fontStyle=1;align=left;spacingLeft=20;')
bands=[(450,170,1130,1440),(1640,170,1190,1110),(1640,1320,1190,470),(450,1650,1130,650),(450,2340,1130,650),(1640,1830,1190,1030)]
ov_assoc=[]
for (plane,goals),(x,y,w,h) in zip(overview,bands):
 y+=50
 d.cell(plane,x,y,w,h,'swimlane;html=0;startSize=42;fillColor=#f1f5f9;swimlaneFillColor=#ffffff;strokeColor=#cbd5e1;fontSize=21;align=left;spacingLeft=18;')
 for j,(key,title,aa,mod) in enumerate(goals):
  names[key]=title+'\n[Module '+mod+']';gx=x+250;gy=y+70+j*145;node=d.uc(key,gx,gy)
  for a in aa:ov_assoc.append((a,node,gx,gy))
roles=list(dict.fromkeys(a for a,_,__,___ in ov_assoc))
actor_positions={A:(105,520),P:(105,2620),R:(105,1810),O:(3240,1030),B:(3240,520),C:(3240,1550),T:(3240,2080),S:(3240,2470)}
roleids={a:d.actor(a,*actor_positions[a]) for a in roles}
for a,node,gx,gy in ov_assoc:d.edge(roleids[a],node)
d.text('Overview of system capabilities. Detailed permissions and relationships are defined in the module diagrams.\nActor inheritance is defined in the actor model. This is not a lifecycle sequence or a business-process workflow.',35,3170,3350,75,16)
root=mxfile();d.append(root);save(root,'00_System_Overview')

assert set(locations)>=set(catalog),set(catalog)-set(locations)
with (OUT/'catalog-traceability.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(['Catalog ID','Use case','Catalog actor','Status','Diagram files'])
 for k,(title,actor) in catalog.items():w.writerow([k,title,actor,'Proposed baseline','; '.join(locations[k])])
with (OUT/'relationships.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(['Module file','Source UC','UML relation','Target UC','Extension point / condition']);w.writerows(relations)
used={k for row in relations for k in [row[1],row[3]]}
with (OUT/'supporting-use-cases.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(['Analysis ID','Name']);w.writerows((k,title) for k,title in aux.items() if k in used)
(OUT/'module-notes.md').write_text('# Module notes and UML clarifications\n\n'+'\n\n'.join(module_notes)+'\n',encoding='utf-8')
page_counts={}
for path in OUT.glob('*.drawio'):
 pages=ET.parse(path).findall('diagram');assert len(pages)==1,(path,'expected one diagram');page_counts[path.name]=1
 m=pages[0].find('mxGraphModel');cells=m.findall('./root/mxCell');ids=[c.get('id') for c in cells];assert len(ids)==len(set(ids))
 for prefix in ['ellipse','shape=umlActor']:
  labels=[c.get('catalogId',c.get('value')) for c in cells if c.get('style','').startswith(prefix)];assert len(labels)==len(set(labels)),(path,'duplicate nodes')
 for c in cells:
  if c.get('edge')=='1':assert c.get('source') in ids and c.get('target') in ids
  if c.get('vertex')=='1':
   z=c.find('mxGeometry');x,y,w,h=[float(z.get(k,0)) for k in ['x','y','width','height']]
   assert x>=0 and y>=0 and x+w<=float(m.get('pageWidth')) and y+h<=float(m.get('pageHeight')),(path,c.get('value'),'out of bounds')
stats.update(catalog_use_cases=len(catalog),catalog_covered=len(catalog),main_actors=5,supporting_actors=4,abstract_actors=2,modules=17,pages_by_file=page_counts)
(OUT/'routing-validation.json').write_text(json.dumps(ROUTING_REPORT,indent=2),encoding='utf-8')
(OUT/'size-validation.json').write_text(json.dumps(COMPACT_REPORT,indent=2),encoding='utf-8')
(OUT/'validation.json').write_text(json.dumps(stats,indent=2),encoding='utf-8');print(json.dumps(stats,indent=2))
