"""Check that relative README links and images exist and are tracked by Git."""
import re
import subprocess
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[2]
text = (ROOT / 'README.md').read_text(encoding='utf-8')
tracked = set(subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).decode().split('\0'))
failures=[]
checked=0
for target in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',text):
    if target.startswith(('https://','http://','mailto:','#')):
        continue
    relative=unquote(target.split('#',1)[0])
    path=(ROOT / relative).resolve()
    if not path.is_relative_to(ROOT):
        failures.append('Outside repository: '+relative)
    elif not path.exists():
        failures.append('Missing: '+relative)
    elif path.is_file() and path.relative_to(ROOT).as_posix() not in tracked:
        failures.append('Not tracked: '+relative)
    checked+=1
if failures:
    raise SystemExit('\n'.join(failures))
print(f'{checked} local README links/images exist and are tracked.')
