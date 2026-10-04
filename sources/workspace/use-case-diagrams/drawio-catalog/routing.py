"""Straight-first UML routing. Crossings are allowed; shared line segments are not."""
import math
import heapq
import textwrap
import xml.etree.ElementTree as ET

def distance(a,b):return math.hypot(b[0]-a[0],b[1]-a[1])
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def box_hit(a,b,box,padding=0):
 x,y,w,h=box;x-=padding;y-=padding;w+=2*padding;h+=2*padding
 t0,t1=0.,1.;dx=b[0]-a[0];dy=b[1]-a[1]
 for p,q in [(-dx,a[0]-x),(dx,x+w-a[0]),(-dy,a[1]-y),(dy,y+h-a[1])]:
  if abs(p)<1e-10:
   if q<0:return False
  else:
   r=q/p
   if p<0:t0=max(t0,r)
   else:t1=min(t1,r)
   if t0>t1:return False
 return True

def hits(a,b,node,margin=8):
 x,y,w,h,ellipse=node
 if not box_hit(a,b,(x,y,w,h),margin):return False
 if not ellipse:return True
 cx,cy=x+w/2,y+h/2;rx,ry=w/2+margin,h/2+margin
 aa=((a[0]-cx)/rx,(a[1]-cy)/ry);bb=((b[0]-cx)/rx,(b[1]-cy)/ry)
 dx,dy=bb[0]-aa[0],bb[1]-aa[1];den=dx*dx+dy*dy
 t=max(0,min(1,-(aa[0]*dx+aa[1]*dy)/den)) if den else 0
 return (aa[0]+t*dx)**2+(aa[1]+t*dy)**2<1

def overlap(a,b,c,d):
 u=(b[0]-a[0],b[1]-a[1]);v=(d[0]-c[0],d[1]-c[1]);length=distance(a,b)
 if length<1:return False
 if abs(cross(u,v))>1e-7*max(1,length*distance(c,d)):return False
 if abs(cross(u,(c[0]-a[0],c[1]-a[1])))/length>0.5:return False
 projections=[((p[0]-a[0])*u[0]+(p[1]-a[1])*u[1])/length for p in [c,d]]
 return min(length,max(projections))-max(0,min(projections))>3

def boundary(node,toward):
 x,y,w,h,ellipse=node
 # Actor label is an obstacle; the actual actor connection stays on its upper body.
 ch=h if ellipse else h-50
 cx,cy=x+w/2,y+ch/2;dx,dy=toward[0]-cx,toward[1]-cy
 if ellipse:scale=1/math.sqrt((dx/(w/2))**2+(dy/(h/2))**2) if dx or dy else 0
 else:
  if dy<0 and abs(dx)<w/2:return cx,y
  return (x+w if dx>=0 else x),cy
 return cx+scale*dx,cy+scale*dy

def route_diagram(diagram):
 model=diagram.find('mxGraphModel');root=model.find('root');nodes={};cells={c.get('id'):c for c in root.findall('mxCell')}
 for key,c in cells.items():
  style=c.get('style','');ellipse=style.startswith('ellipse');actor=style.startswith('shape=umlActor')
  if not(ellipse or actor):continue
  g=c.find('mxGeometry');x,y,w,h=[float(g.get(k,0)) for k in ['x','y','width','height']]
  nodes[key]=(x,y,w,h if ellipse else h+50,ellipse)
 edges=[c for c in cells.values() if c.get('edge')=='1']
 centers={k:(n[0]+n[2]/2,n[1]+(n[3]/2 if n[4] else (n[3]-50)/2)) for k,n in nodes.items()}
 paths=[];counts={'edges':len(edges),'straight':0,'bent':0,'overlapping_segments':0,'node_intersections':0,'label_node_overlaps':0,'label_label_overlaps':0}
 width=float(model.get('pageWidth'));height=float(model.get('pageHeight'))
 # Short edges first constrain long-edge detours without forcing shared channels.
 edges.sort(key=lambda e:distance(centers[e.get('source')],centers[e.get('target')]))
 for index,e in enumerate(edges):
  source,target=e.get('source'),e.get('target');a,b=centers[source],centers[target]
  obstacles=[n for k,n in nodes.items() if k not in [source,target]]
  def clear(p,q):
   return not any(hits(p,q,n) for n in obstacles) and not any(overlap(p,q,r,s) for path in paths for r,s in zip(path,path[1:]))
  def clip(route):return [boundary(nodes[source],route[1])]+route[1:-1]+[boundary(nodes[target],route[-2])]
  direct=clip([a,b])
  if clear(*direct):path=direct
  else:
   jitter=11+(index%17)*1.9;candidates=[]
   dx,dy=b[0]-a[0],b[1]-a[1];length=max(1,distance(a,b));normal=(-dy/length,dx/length)
   for fraction in [.25,.5,.75]:
    mid=(a[0]+fraction*dx,a[1]+fraction*dy)
    for offset in [45,90,160,260,420,650,900]:
     for sign in [-1,1]:candidates.append((mid[0]+normal[0]*(offset+jitter)*sign,mid[1]+normal[1]*(offset+jitter)*sign))
   for x,y,w,h,_ in obstacles:
    candidates.extend([(x-jitter,y-jitter),(x+w+jitter,y-jitter),(x-jitter,y+h+jitter),(x+w+jitter,y+h+jitter)])
   candidates=[p for p in candidates if 25<p[0]<width-25 and 115<p[1]<height-165 and not any(hits(p,p,n,3) for n in obstacles)]
   best=None;score=float('inf')
   for mid in candidates:
    proposed=clip([a,mid,b]);cost=sum(distance(p,q) for p,q in zip(proposed,proposed[1:]))
    if cost<score and all(clear(p,q) for p,q in zip(proposed,proposed[1:])):best=proposed;score=cost
   if best:path=best
   else:
    # Visibility graph fallback, still diagonal rather than orthogonal routing.
    points=[a,b]+candidates;queue=[(0,0)];costs={0:0};previous={};done=set()
    while queue:
     cost,u=heapq.heappop(queue)
     if u in done:continue
     done.add(u)
     if u==1:break
     for v in range(len(points)):
      if u==v or v in done:continue
      p=boundary(nodes[source],points[v]) if u==0 else points[u]
      q=boundary(nodes[target],points[u]) if v==1 else points[v]
      if not clear(p,q):continue
      new=cost+distance(p,q)+70
      if new<costs.get(v,float('inf')):costs[v]=new;previous[v]=u;heapq.heappush(queue,(new,v))
    if 1 not in costs:raise AssertionError('Cannot route '+str((source,target)))
    trail=[1]
    while trail[-1]!=0:trail.append(previous[trail[-1]])
    path=clip([points[v] for v in reversed(trail)])
  # Store precise perimeter anchors so checks match native Draw.io rendering.
  clean=[s for s in e.get('style','').split(';') if s and not s.startswith(('exit','entry','edgeStyle','curved','orthogonal','jetty','rounded','labelWidth','whiteSpace'))]
  for prefix,key,p in [('exit',source,path[0]),('entry',target,path[-1])]:
   x,y,w,h,ellipse=nodes[key];h=h if ellipse else h-50
   clean.extend([f'{prefix}X={(p[0]-x)/w}',f'{prefix}Y={(p[1]-y)/h}',f'{prefix}Perimeter=0'])
  e.set('style',';'.join(clean)+';edgeStyle=none;rounded=0;whiteSpace=wrap;labelWidth=270;')
  old=e.find('mxGeometry');e.remove(old);geometry=ET.SubElement(e,'mxGeometry',relative='1',attrib={'as':'geometry'})
  if len(path)>2:
   arr=ET.SubElement(geometry,'Array',attrib={'as':'points'})
   for x,y in path[1:-1]:ET.SubElement(arr,'mxPoint',x=str(x),y=str(y))
  e.set('routing','straight' if len(path)==2 else 'diagonal-detour')
  paths.append(path);counts['straight' if len(path)==2 else 'bent']+=1
  for p,q in zip(path,path[1:]):counts['node_intersections']+=sum(hits(p,q,n,0) for n in obstacles)
  counts['overlapping_segments']+=sum(overlap(p,q,r,s) for p,q in zip(path,path[1:]) for earlier in paths[:-1] for r,s in zip(earlier,earlier[1:]))
 # Keep every relationship label directly on its connector; only slide along the line.
 labels=[]
 allsegments=[(p,q) for path in paths for p,q in zip(path,path[1:])]
 for e,path in zip(edges,paths):
  value=e.get('value','')
  if not value:continue
  lines=[]
  for line in value.splitlines():lines.extend(textwrap.wrap(line,width=43) or [''])
  e.set('value','\n'.join(lines));w=max(len(line) for line in lines)*6.4+12;h=len(lines)*15+8
  lengths=[distance(p,q) for p,q in zip(path,path[1:])];total=sum(lengths);best=None;bestcost=float('inf')
  for fraction in [.5,.45,.55,.4,.6,.35,.65,.3,.7,.25,.75,.2,.8,.15,.85,.1,.9]:
   wanted=total*fraction;passed=0
   for j,segmentlength in enumerate(lengths):
    if wanted<=passed+segmentlength or j==len(lengths)-1:
     t=(wanted-passed)/max(1,segmentlength);p,q=path[j:j+2];point=(p[0]+t*(q[0]-p[0]),p[1]+t*(q[1]-p[1]));normal=(-(q[1]-p[1])/max(1,segmentlength),(q[0]-p[0])/max(1,segmentlength));break
    passed+=segmentlength
   for offset in [0]:
    cx,cy=point[0]+normal[0]*offset,point[1]+normal[1]*offset;box=(cx-w/2,cy-h/2,w,h)
    if box[0]<15 or box[1]<105 or box[0]+w>width-15 or box[1]+h>height-145:continue
    nodehits=sum(box_hit((box[0],box[1]),(box[0]+w,box[1]+h),n[:4]) or box_hit((box[0]+w,box[1]),(box[0],box[1]+h),n[:4]) for n in nodes.values())
    labelhits=sum(not (box[0]+w<r[0] or r[0]+r[2]<box[0] or box[1]+h<r[1] or r[1]+r[3]<box[1]) for r in labels)
    linehits=sum(box_hit(p,q,box) for p,q in allsegments)
    cost=nodehits*100000+labelhits*100000+linehits*120+abs(offset)*.1+abs(fraction-.5)*20
    if cost<bestcost:bestcost=cost;best=(fraction,cx-point[0],cy-point[1],box,nodehits,labelhits)
  fraction,dx,dy,box,nodehits,labelhits=best;geometry=e.find('mxGeometry');geometry.set('x',str(2*fraction-1));geometry.set('y','0');ET.SubElement(geometry,'mxPoint',x=str(dx),y=str(dy),attrib={'as':'offset'})
  labels.append(box);counts['label_node_overlaps']+=nodehits;counts['label_label_overlaps']+=labelhits
 assert counts['node_intersections']==0 and counts['overlapping_segments']==0,counts
 return counts
