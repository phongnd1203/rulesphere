"""Export the editable activity diagrams to PNG with draw.io Desktop."""
from pathlib import Path
import json
import subprocess
import tempfile
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
APP = Path(r'C:\Program Files\draw.io\draw.io.exe')
PREVIEWS = HERE/'previews'
PREVIEWS.mkdir(exist_ok=True)
report = []
with tempfile.TemporaryDirectory(prefix='rulesphere-activity-') as profile:
    for source in sorted(HERE.glob('*.drawio')):
        pages = ET.parse(source).getroot().findall('diagram')
        for index, page in enumerate(pages):
            suffix = f'_{index+1:02}' if len(pages)>1 else ''
            target = PREVIEWS/(source.stem+suffix+'.png')
            result = subprocess.run(
                [str(APP), '--no-sandbox', '--disable-gpu', f'--user-data-dir={profile}',
                 '--export', '--format', 'png', '--scale', '1', '--border', '20',
                 '--page-index', str(index+1), '--output', str(target), str(source)],
                capture_output=True, text=True, timeout=90,
                creationflags=subprocess.CREATE_NO_WINDOW)
            assert result.returncode == 0 and target.exists(), result.stdout + result.stderr
            assert target.stat().st_size > 100
            report.append(dict(source=source.name, page=page.get('name'), preview=target.name, bytes=target.stat().st_size))
            print('Rendered '+source.name+' / '+page.get('name'), flush=True)
(HERE/'render-validation.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
