"""Exactly one PNG preview for each single-diagram Draw.io file."""
from pathlib import Path
import subprocess, json, sys
HERE=Path(__file__).resolve().parent
APP=Path(r'C:\Program Files\draw.io\draw.io.exe')
PREVIEWS=HERE/'previews';PREVIEWS.mkdir(exist_ok=True)
PROFILE=HERE.parents[1]/'scratch'/'drawio-catalog-profile'
selected=set(sys.argv[1:]);report_path=HERE/'render-validation.json'
reports=json.loads(report_path.read_text(encoding='utf-8')) if selected and report_path.exists() else []
if not selected:
 for old in PREVIEWS.iterdir():
  assert old.resolve().parent==PREVIEWS.resolve()
  if old.is_file() and old.suffix.lower() in {'.pdf','.png'}:old.unlink()
for src in sorted(HERE.glob('*.drawio')):
 if selected and src.stem not in selected:continue
 dest=PREVIEWS/(src.stem+'.png')
 result=subprocess.run([str(APP),'--no-sandbox','--disable-gpu',f'--user-data-dir={PROFILE}','-x','-f','png','-o',str(dest),str(src)],capture_output=True,text=True,timeout=90)
 assert result.returncode==0 and dest.exists() and dest.stat().st_size>100,result.stdout+'\n'+result.stderr
 reports[:]=[r for r in reports if r['source']!=src.name];reports.append(dict(source=src.name,output=dest.name,ok=True,bytes=dest.stat().st_size))
 print('Exported '+dest.name,flush=True)
report_path.write_text(json.dumps(reports,indent=2),encoding='utf-8')
if not selected:assert {p.stem for p in PREVIEWS.iterdir()}=={p.stem for p in HERE.glob('*.drawio')}
print(f'{len(reports)} diagrams; one PNG each.',flush=True)
