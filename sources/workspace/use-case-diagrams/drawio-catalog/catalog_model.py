"""Reproducible native Draw.io diagrams for the user-supplied A–Q catalog."""
from pathlib import Path
import re, csv, json, xml.etree.ElementTree as ET

OUT=Path(__file__).resolve().parent
SYSTEM_NAME='RuleSphere - Business Rule Management Platform'
ROUTING_REPORT={}
COMPACT_REPORT={}
source=(OUT/'source-catalog.md').read_text(encoding='utf-8')
catalog={m[0]:(m[1].strip(),m[2].strip()) for m in re.findall(r'^\| ((?:IAM|DAM|AUT|DCM|VAL|TST|VER|GOV|ART|DEP|PRG|EXE|EXP|SIM|OPS|AUD|CICD|ADM)-\d+) \| ([^|]+) \| ([^|]+) \|',source,re.M)}
A='Rule / Decision Author';R='Reviewer / Approver';P='Platform Administrator';O='Operations / SRE'
C='Decision Consumer / Client Application';I='Identity Provider / IAM';B='CI/CD & Automation';T='Observability Platform';S='Audit / SIEM'
U='Platform User';X='External System'
parents={U:[A,R,P,O],X:[C,I,B,T,S]}
aux={
 'AUX-IAM-01':'Resolve User Roles','AUX-IAM-02':'Evaluate Access Policy','AUX-IAM-03':'Authenticate Client',
 'AUX-AUT-01':'Author Decision Logic','AUX-AUT-02':'View Decision Model',
 'AUX-GOV-01':'View Version Changes',
 'AUX-PRG-01':'Perform Canary Deployment','AUX-PRG-02':'Perform Shadow Deployment',
 'AUX-EXE-01':'Evaluate Decision Expression','AUX-EXE-02':'Resolve Pinned Decision Version',
 'AUX-OPS-01':'Operational Inspection','AUX-AUD-01':'Inspect Audit History',
 'AUX-CICD-01':'Retrieve Automation Results',
 'UC-X01':'Authorize Operation','UC-X02':'Record Audit Event','UC-X04':'Resolve Decision Version',
 'AUX-X-01':'State-Changing Operation',
}
names={k:v[0] for k,v in catalog.items()}|aux
# UC-X03 in the prose names the existing VAL-01; do not duplicate its identity.
aliases={'UC-X03':'VAL-01','Validate Decision Model':'VAL-01'}

def g(root,actors=(),v=(),i=(),e=(),note='',support=(),abstract=False):
 return dict(root=root,actors=list(actors),v=list(v),i=list(i),e=list(e),note=note,support=list(support),abstract=abstract)

modules=[
('A_Identity_Access_Management','IAM',[
 g('IAM-01',[U],i=['IAM-03'],support=[(I,'IAM-03')],note='Platform User generalization is defined in 01_Actor_Model. Authentication is delegated to Identity Provider / IAM.'),
 g('IAM-04',i=['AUX-IAM-01','AUX-IAM-02'],note='Internal authorization behavior invoked by protected operations; Platform User is the subject, not an actor who manually runs the policy engine.'),
 g('IAM-05',[P],e=[('IAM-06','role mapping: assign requested'),('IAM-07','role mapping: revoke requested')]),
 g('IAM-08',[P],i=['IAM-04']),
 g('IAM-10',i=['AUX-IAM-03'],support=[(I,'AUX-IAM-03')],note='Internal credential check for client requests; Authenticate Client uses delegated IAM. Consumer participation is through EXE-01.'),
 g('IAM-02',[U]),g('IAM-09',[P]),
]),
('B_Decision_Project_Asset_Management','DAM',[
 g('DAM-01',v=['DAM-02','DAM-04','DAM-05'],i=['UC-X01'],support=[(A,'DAM-02'),(A,'DAM-04'),(P,'DAM-05')],abstract=True,note='Actor links terminate on the permitted variants: Author creates/updates; Administrator archives. No Author association on the abstract parent, so archive permission is not inherited.'),
 g('DAM-03',[U]),g('DAM-06',[U],e=[('DAM-07','search results: metadata inspection requested')]),
 g('DAM-08',[A]),g('DAM-09',[A]),
]),
('C_Decision_Modeling_Rule_Authoring','AUT',[
 g('AUT-01',[A],v=['AUT-02','AUT-03'],i=['AUX-AUT-01','AUT-12','VAL-01','UC-X01'],abstract=True,note='The model-authoring transaction includes logic, metadata and validation. VAL-01 is the catalog relation named Validate Decision Model.'),
 g('AUX-AUT-01',v=['AUT-05','AUT-07','AUT-09'],abstract=True,note='Reusable logic-authoring behavior included by AUT-01; concrete rule/table/expression variants inherit this contract.'),
 g('AUT-03',i=['AUT-13'],note='Detailed behavior of Edit Decision Model; actor association is inherited from AUT-01.'),
 g('AUT-05',i=['AUT-12'],e=[('AUT-10','rule definition: priority configuration requested')]),
 g('AUT-06',[A],e=[('AUT-11','rule editing: enable/disable requested')]),
 g('AUX-AUT-02',[A],e=[('AUT-04','model inspection: clone requested')]),
 g('AUT-08',[A]),g('AUT-14',[A]),g('AUT-15',[A],note='Precondition: draft asset; released assets are immutable.'),
]),
('D_Data_Contract_Management','DCM',[
 g('DCM-01',[A],i=['DCM-02','DCM-03'],note='Complete contract-definition transaction includes both input and output contracts, as specified in this proposed catalog.'),
 g('DCM-02',i=['DCM-04'],e=[('DCM-05','input schema: additional constraints specified')]),
 g('DCM-03',i=['DCM-04'],e=[('DCM-05','output schema: additional constraints specified')]),
 g('DCM-07',[A],i=['DCM-06']),
 g('DCM-08',[C],e=[('DCM-09','contract inspection: export requested')]),
]),
('E_Validation_Testing','VAL/TST',[
 g('VAL-01',[A],i=['VAL-02','VAL-03','VAL-04'],e=[('VAL-05','validation options: conflict analysis enabled'),('VAL-06','validation options: redundancy analysis enabled')]),
 g('TST-01',[A],v=['TST-02'],abstract=True,note='Only Create Test Case is named as a detailed management variant in the catalog; edit/delete variants are not invented.'),
 g('TST-03',[A],i=['VAL-01']),
 g('TST-04',[A],i=['TST-03']),
 g('TST-06',[A],i=['TST-05']),
 g('TST-07',[A],i=['TST-04']),
 g('TST-08',[R],i=['VAL-01','TST-04'],note='Reviewer can initiate the release-candidate check; Author release creation also invokes it internally through VER-06. This does not confer approval rights on Author.'),
]),
('F_Version_Change_Management','VER',[
 g('VER-01',[A],v=['VER-02','VER-06'],abstract=True),
 g('VER-02',i=['VAL-01']),
 g('VER-06',i=['TST-08','VAL-01'],note='Creates a release version, not a governance approval. Release eligibility and immutability constraints apply.'),
 g('VER-03',[U],e=[('VER-05','history inspection: authorized Author requests draft restore')],support=[(A,'VER-05')],note='Viewing history is shared; restoring a draft remains Author-only. Extension permissions do not follow the base use case automatically.'),
 g('VER-04',[A],i=['VER-03']),g('VER-07',[P]),g('VER-08',[U]),
]),
('G_Review_Approval_Governance','GOV',[
 g('GOV-01',[A],i=['VAL-01','VER-02','UC-X01']),
 g('GOV-02',[R],i=['AUX-GOV-01'],e=[('GOV-03','review outcome: approve selected'),('GOV-04','review outcome: reject selected'),('GOV-05','review outcome: rework selected')],note='Outcome extensions are mutually exclusive for a review decision. This is decision governance, not general-purpose BPM orchestration.'),
 g('GOV-03',i=['GOV-09','UC-X01','UC-X02'],note='Enforce Approval Policy is internal enforcement configured by Administrator through platform policies. Administrator is not a manual policy-execution actor.'),
 g('GOV-07',[A],e=[('GOV-06','review status: review pending and cancellation requested')]),
 g('GOV-08',[R]),
]),
('H_Build_Artifact_Management','ART',[
 g('ART-01',[A,B],i=['ART-02','ART-03','ART-04','VAL-01']),
 g('ART-05',[A,B],i=['ART-01','ART-07','VAL-01','UC-X01'],note='Catalog models publish as build-and-publish. Every invocation includes Build. A publish-existing-artifact API would need a distinct behavior if later required. Published artifacts are immutable.'),
 g('ART-06',[U]),g('ART-07',[O],note='Integrity verification can also be initiated directly by Operations; build/deploy reuse it internally.'),
 g('ART-08',[R],i=['VER-08']),g('ART-09',[P]),
]),
('I_Environment_Deployment_Management','DEP',[
 g('DEP-01',[P],v=['DEP-02','DEP-03','DEP-04'],abstract=True),
 g('DEP-05',[O],i=['DEP-12','ART-07','DEP-13','DEP-14','UC-X01'],e=[('DEP-07','rollout recovery: failure or authorized reversal within deployment lifecycle')],note='Deployment includes asynchronous convergence verification before lifecycle completion. Rollback extend is limited to recovery within this lifecycle; a later independent rollback remains directly invocable by Operations.'),
 g('DEP-05',[O],v=['DEP-08'],note='Redeploy specializes deployment and inherits its includes. Separate page for readability; same DEP-05 identity.'),
 g('DEP-06',[O],i=['DEP-05']),
 g('DEP-14',[O],e=[('DEP-15','convergence verification: drift inspection enabled')],note='Base convergence verification checks the desired/observed state. Detailed drift diagnosis is conditional.'),
 g('DEP-15',e=[('DEP-16','drift detected: reconciliation authorized')]),
 g('DEP-10',[O],e=[('DEP-09','deployment status: cancellable operation and cancel requested')]),
 g('DEP-07',[O],note='Explicit association supports independent rollback requests. The conditional recovery extension is shown on the DEP-05 detail page.'),g('DEP-11',[O]),
]),
('J_Progressive_Delivery','PRG',[
 g('PRG-01',[O],v=['AUX-PRG-01','AUX-PRG-02'],abstract=True),
 g('AUX-PRG-01',i=['PRG-02','DEP-05'],e=[('PRG-03','canary running: allocation change requested'),('PRG-04','canary running: promotion criteria satisfied'),('PRG-05','canary running: abort requested')],note='Perform Canary Deployment spans the rollout lifecycle, so later control interactions occur at named extension points.'),
 g('AUX-PRG-02',i=['PRG-06','DEP-05'],e=[('PRG-09','shadow running: stop requested')]),
 g('PRG-08',[O],i=['PRG-07'],note='This comparison use case launches a shadow evaluation as specified by the catalog. Comparing only previously captured results would be a separate contract.'),
 g('EXE-01',[C],e=[('PRG-07','evaluation dispatch: shadow enabled and request eligible')],note='Runtime reference: Consumer triggers shadow evaluation indirectly through the real decision request. Shadow result never replaces the active result.'),
]),
('K_Decision_Execution','EXE',[
 g('EXE-01',[C],i=['EXE-02','EXE-03','EXE-05','EXE-08','UC-X04'],support=[(I,'EXE-02')],note='UC-X04 selects EXE-04 for default execution or exact pinned resolution for EXE-12. Refinement: do not require active resolution in every specialization. Later successful-path includes are skipped after a terminating error.'),
 g('EXE-01',[C],e=[('EXE-09','response enrichment: metadata requested or response policy requires it'),('EXE-10','request validation: request invalid'),('EXE-11','evaluation: evaluation failed'),('EXP-01','response enrichment: explanation requested and permitted')]),
 g('EXE-05',v=['EXE-06','EXE-07','AUX-EXE-01'],abstract=True,note='Concrete evaluators specialize the evaluation behavior; activated model nodes may use more than one evaluator.'),
 g('EXE-01',v=['EXE-12'],note='EXE-12 inherits Execute Decision with the version-resolution variation explicitly overridden. Authorization still applies to the requested version.'),
 g('EXE-12',i=['AUX-EXE-02'],note='Resolve the exact requested version; never fall back silently to active. Overrides EXE-04 inside the inherited UC-X04 resolution strategy.'),
 g('EXE-02',i=['IAM-10'],note='Decision-request authentication reuses the client credential validation defined in module A.'),
 g('UC-X04',v=['EXE-04','AUX-EXE-02'],abstract=True,note='Default execution resolves the active version. EXE-12 selects the exact pinned-version strategy; both strategies specialize UC-X04.'),
]),
('L_Explainability_Decision_Trace','EXP',[
 g('EXP-01',[C],i=['EXP-02','UC-X04'],note='Resolve the version bound to the recorded execution, not the current active version.'),
 g('EXP-02',i=['EXP-07'],e=[('EXP-03','explanation evidence: matched rules requested'),('EXP-04','explanation evidence: trace requested'),('EXP-05','explanation evidence: input values requested'),('EXP-06','explanation evidence: output derivation requested')],note='Optional evidence views are scoped by permissions, masking and retention. Author may inspect all listed detail views; Operations may inspect the evaluation trace. No consumer access to sensitive fields is implied.'),
 g('EXP-07',[U]),g('EXP-04',[A,O]),g('EXP-08',[O]),
 # Explicit author inspection entry points preserve catalog actor rights on optional evidence views.
 g('EXP-03',[A]),g('EXP-05',[A]),g('EXP-06',[A]),
]),
('M_Simulation_Impact_Analysis','SIM',[
 g('SIM-01',[A],v=['SIM-02'],i=['UC-X04']),
 g('SIM-03',[A],i=['SIM-01']),g('SIM-04',[A]),
 g('SIM-05',[A],i=['SIM-06']),g('SIM-07',[A],i=['SIM-01'],note='Dataset evaluation repeats simulation for supplied inputs. No production replay or batch API requirement is inferred.'),
]),
('N_Runtime_Operations_Observability','OPS',[
 g('OPS-01',[O],i=['OPS-02','OPS-03'],e=[('OPS-11','runtime monitoring: alert condition detected')]),
 g('OPS-03',i=['OPS-04','OPS-05','OPS-06']),
 g('OPS-10',[O],i=['OPS-08','OPS-09'],note='The catalog assumes diagnosis retrieves logs and traces; unavailable/expired evidence must be handled explicitly in the detailed specification.'),
 g('OPS-07',[O]),g('OPS-12',support=[(T,'OPS-12')],note='Triggered internally by telemetry production or an external scrape/query. Observability Platform is the receiving/supporting actor; RuleSphere is not an actor of itself.'),
]),
('O_Audit_Compliance','AUD',[
 g('AUD-01',[R],e=[('AUD-02','audit inspection: search/filter requested')]),
 g('AUD-06',[R],i=['AUD-07','AUD-08','UC-X04'],note='Resolve the exact historical version tied to execution evidence.'),
 g('AUD-03',[R],i=['AUD-01']),g('AUD-04',[R],i=['AUD-01']),g('AUD-05',[O],i=['AUD-01'],note='Operations receives deployment-scoped audit evidence only; reusing AUD-01 does not grant unrestricted Reviewer audit access.'),
 g('AUD-09',i=['UC-X02'],support=[(S,'AUD-09')],note='Record Audit Event here records the export operation itself. The exported events already exist; exporting does not recreate historical audit events. SIEM receives the export.'),
 g('AUD-10',[P]),
]),
('P_Automation_CI_CD_Integration','CICD',[
 g('CICD-01',[B],i=['VAL-01']),g('CICD-02',[B],i=['TST-04']),
 g('CICD-03',[B],i=['ART-01']),g('CICD-04',[B],i=['ART-05']),
 g('CICD-05',[B],i=['DEP-05']),g('CICD-06',[B],i=['DEP-10']),
 g('CICD-07',[B],i=['TST-05']),g('CICD-08',[B]),
]),
('Q_Platform_Administration','ADM',[
 g('ADM-01',[P],i=['ADM-02','UC-X01']),
 g('ADM-02',e=[('ADM-03','policy configuration: execution limits selected'),('ADM-04','policy configuration: retention selected'),('ADM-05','policy configuration: audit selected'),('ADM-06','policy configuration: deployment selected')]),
 g('ADM-07',[P],v=['ADM-08','ADM-09','ADM-10'],abstract=True,note='Modeling correction: View Runtime Node Status is a read-only specialization, not an include of all runtime-node management. Register/deregister do not run when viewing status.'),
 g('ADM-11',[P]),g('ADM-12',[P]),
]),
]

abstract={'DAM-01','AUT-01','AUX-AUT-01','TST-01','VER-01','DEP-01','PRG-01','EXE-05','ADM-07','AUX-X-01','UC-X01','UC-X02'}
coverage={k:[] for k in catalog};rel_rows=[];stats=dict(files=0,pages=0,include=0,extend=0,generalization=0,association=0)

class Diagram:
 def __init__(self,name,w=1680,h=980):
  self.d=ET.Element('diagram',name=name,id=re.sub(r'[^a-zA-Z0-9]','_',name));self.w=w;self.h=h
  self.m=ET.SubElement(self.d,'mxGraphModel',grid='1',gridSize='10',guides='1',tooltips='1',connect='1',arrows='1',fold='1',page='1',pageScale='1',pageWidth=str(w),pageHeight=str(h),math='0',shadow='0')
  self.r=ET.SubElement(self.m,'root');ET.SubElement(self.r,'mxCell',id='0');ET.SubElement(self.r,'mxCell',id='1',parent='0');self.n=0
 def cell(self,label,x,y,w,h,style):
  self.n+=1;key='n'+str(self.n);c=ET.SubElement(self.r,'mxCell',id=key,value=label,style=style,vertex='1',parent='1')
  ET.SubElement(c,'mxGeometry',x=str(x),y=str(y),width=str(w),height=str(h),attrib={'as':'geometry'});return key
 def text(self,label,x,y,w,h,size=14):return self.cell(label,x,y,w,h,f'text;html=0;whiteSpace=wrap;align=left;verticalAlign=middle;fontSize={size};fontFamily=Helvetica;fontColor=#334155;')
 def actor(self,name,x,y):
  return self.cell(name,x,y,120,82,'shape=umlActor;html=0;whiteSpace=wrap;verticalLabelPosition=bottom;verticalAlign=top;fontSize=13;fontFamily=Helvetica;strokeColor=#334155;fillColor=#ffffff;')
 def uc(self,key,x,y):
  ident=self.cell(re.sub(r'\n\[Module [^\]]+\]','',names[key]),x,y,290,104,'ellipse;html=0;whiteSpace=wrap;align=center;verticalAlign=middle;spacing=9;fontSize=14;fontFamily=Helvetica;strokeColor=#334155;strokeWidth=1.5;fillColor='+('#eff6ff' if key in abstract else '#ffffff')+';')
  self.r[-1].set('catalogId',key)
  return ident
 def edge(self,s,t,kind='',condition=''):
  self.n+=1;label='';style='edgeStyle=none;html=0;rounded=0;fontSize=12;fontFamily=Helvetica;labelBackgroundColor=#ffffff;strokeColor=#475569;strokeWidth=1.3;'
  if kind in ['include','extend']:
   style+='dashed=1;endArrow=open;endFill=0;';label='«'+kind+'»'
  elif kind=='generalization':style+='endArrow=block;endFill=0;endSize=16;'
  else:style+='endArrow=none;'
  c=ET.SubElement(self.r,'mxCell',id='e'+str(self.n),value=label,style=style,edge='1',parent='1',source=s,target=t)
  ET.SubElement(c,'mxGeometry',relative='1',attrib={'as':'geometry'});stats[kind or 'association']+=1
 def append(self,root):root.append(self.d);stats['pages']+=1

def mxfile():return ET.Element('mxfile',host='app.diagrams.net',agent='Codex',version='26.0.0',type='device',compressed='false')
def save(root,file):
 from routing import route_diagram
 for diagram in root.findall('diagram'):
  model=diagram.find('mxGraphModel');scale=.72
  old_width=float(model.get('pageWidth'));old_height=float(model.get('pageHeight'))
  for cell in diagram.findall('.//mxCell'):
   if cell.get('vertex')!='1':continue
   geometry=cell.find('mxGeometry');style=cell.get('style','')
   for key in ['x','y','width','height']:geometry.set(key,str(round(float(geometry.get(key,0))*scale,2)))
   if style.startswith('ellipse'):
    geometry.set('width','240');geometry.set('height','90');style=style.replace('spacing=9;','spacing=5;')
   elif style.startswith('shape=umlActor'):
    geometry.set('width','100');geometry.set('height','70');style=style.replace('fontSize=13;','fontSize=12;')
   else:
    style=re.sub(r'fontSize=(\d+)',lambda match:'fontSize='+str(max(11,round(int(match[1])*.83))),style)
    style=re.sub(r'startSize=(\d+)',lambda match:'startSize='+str(round(int(match[1])*scale)),style)
   cell.set('style',style)
  model.set('pageWidth',str(round(old_width*scale)));model.set('pageHeight',str(round(old_height*scale)))
  COMPACT_REPORT[file]={'before':[old_width,old_height],'after':[round(old_width*scale),round(old_height*scale)],'use_case_font_size':14}
  diagram.set('name',SYSTEM_NAME+' | '+file.replace('_',' '))
  for cell in diagram.findall('.//mxCell'):
   if cell.get('style','').startswith('swimlane') and cell.get('value','').startswith('RuleSphere'):cell.set('value',SYSTEM_NAME)
   elif cell.get('value'):cell.set('value',re.sub(r'RuleSphere(?! - Business Rule Management Platform)',SYSTEM_NAME,cell.get('value')))
  ROUTING_REPORT[file]=route_diagram(diagram)
 ET.indent(root);ET.ElementTree(root).write(OUT/(file+'.drawio'),encoding='utf-8',xml_declaration=True);stats['files']+=1
def header(d,title):
 d.text(SYSTEM_NAME,30,18,d.w-60,40,23)
 d.text(title.replace('RuleSphere — ','')+' | Proposed baseline',30,64,d.w-60,40,18)
def footer(d,note):
 d.text(note or 'Reusable behavior is expanded on its home-module page. Actor associations are shown at goal level; internal subflows are reached through use-case relationships.',540,d.h-220,d.w-585,85,13)
 d.text('Solid line: participation | Hollow triangle: child → parent | «include»: base → required behavior | «extend»: optional behavior → base\nBracketed labels: extension point and condition. Shared authorization/audit rules: 02_Cross_Cutting. Full system boundary includes the runtime.',30,d.h-110,d.w-60,75,13)

overview=[
 ('Decision Management',[
 ('UC-01','Manage Decision Projects',[A,P],'B'),('UC-02','Author Decision Models',[A],'C'),('UC-03','Manage Business Rules',[A],'C'),('UC-04','Manage Decision Contracts',[A],'D'),('UC-05','Validate Decisions',[A],'E'),('UC-06','Test Decisions',[A],'E'),('UC-07','Manage Decision Versions',[A],'F'),('UC-08','Review & Approve Changes',[R],'G'),('UC-09','Simulate & Analyze Decisions',[A],'M')]),
 ('Decision Delivery',[
 ('UC-10','Build Decision Artifact',[A,B],'H'),('UC-11','Publish Decision Artifact',[A,B],'H'),('UC-12','Manage Runtime Environments',[P],'I'),('UC-13','Deploy Decisions',[O],'I'),('UC-14','Perform Progressive Delivery',[O],'J'),('UC-15','Manage Deployment State',[O],'I')]),
 ('Decision Execution',[
 ('UC-16','Execute Decision',[C],'K'),('UC-17','Explain Decision Result',[C],'L')]),
 ('Operations',[
 ('UC-18','Monitor Decision Runtime',[O],'N'),('UC-19','Diagnose Runtime Issues',[O],'N'),('UC-20','Audit Decision Lifecycle',[R,O],'O')]),
 ('Administration',[
 ('UC-21','Manage Identity & Access',[P],'A'),('UC-22','Manage Platform Configuration',[P],'Q'),('UC-23','Manage Runtime Nodes',[P],'Q')]),
 ('Integration',[
 ('UC-24','Integrate CI/CD Automation',[B],'P'),('UC-25','Export Telemetry & Audit Events',[T,S],'N/O')]),
]
