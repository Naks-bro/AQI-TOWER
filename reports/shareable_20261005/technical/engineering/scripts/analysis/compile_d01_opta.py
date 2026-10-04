"""Compile the default disabled-output sketch using an already-installed Opta core.

No downloads, installation, upload, board discovery or hardware access.
The local toolchain and binary outputs remain Git-ignored.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / '.tools/arduino'
CLI = TOOLS / 'bin/arduino-cli.exe'
CONFIG = TOOLS / 'arduino-cli.yaml'
SKETCH = ROOT / 'firmware/d01_opta_review'
OUT = ROOT / 'reports/prototype_d01/electrical_package/OPTA_BOARD_BUILD.json'
BUILD = TOOLS / 'build/d01_opta_default'
if not CLI.is_file() or not CONFIG.is_file():
    raise SystemExit('Local Arduino CLI/config missing; this script does not install tools.')
assert not list(SKETCH.glob('*.cpp')), 'Host test source must stay outside the sketch'
cli_hash = hashlib.sha256(CLI.read_bytes()).hexdigest()
base = [str(CLI), '--config-file', str(CONFIG)]
version = subprocess.run(base + ['version'], capture_output=True, text=True, check=True).stdout.strip()
cores = json.loads(subprocess.run(base + ['core', 'list', '--json'], capture_output=True,
                                text=True, check=True).stdout)
installed = [{'id': p['id'], 'version': p.get('installed_version')}
             for p in cores['platforms'] if p.get('installed_version')]
assert {'id': 'arduino:mbed_opta', 'version': '4.6.0'} in installed, 'Expected official Opta core4.6.0'
archive_name = 'arduino-cli_1.5.1_Windows_64bit.zip'
archive_hash = hashlib.sha256((TOOLS / archive_name).read_bytes()).hexdigest()
expected_hash = next(line.split()[0] for line in (TOOLS / 'checksums.txt').read_text().splitlines()
                     if line.split()[-1] == archive_name)
assert archive_hash == expected_hash, 'Official CLI archive checksum mismatch'
index = json.loads((TOOLS / 'data/package_index.json').read_text(encoding='utf-8'))
opta_package = next(p for p in index['packages'] if p['name'] == 'arduino')
opta_platform = next(p for p in opta_package['platforms']
                     if p['architecture'] == 'mbed_opta' and p['version'] == '4.6.0')
BUILD.mkdir(parents=True, exist_ok=True)
command = base + ['compile', '--fqbn', 'arduino:mbed_opta:opta', '--warnings', 'all',
                  '--build-path', str(BUILD), str(SKETCH)]
result = subprocess.run(command, capture_output=True, text=True, errors='replace')
log = result.stdout + '\n' + result.stderr
(TOOLS / 'OPTA_COMPILE.log').write_text(log, encoding='utf-8')
record = dict(status='TARGET COMPILE PASS' if result.returncode == 0 else 'TARGET COMPILE FAILED',
              target_board_compiled=result.returncode == 0, returncode=result.returncode,
              fqbn='arduino:mbed_opta:opta', cli_version=version, cli_executable_sha256=cli_hash,
              installed_cores=installed, command=command, compile_output=log,
              authorized_download_sources=dict(
                  cli='https://github.com/arduino/arduino-cli/releases/download/v1.5.1/arduino-cli_1.5.1_Windows_64bit.zip',
                  cli_archive_sha256=archive_hash,
                  cli_checksum_verified=True, opta_core_url=opta_platform['url'],
                  opta_core_index_checksum=opta_platform['checksum'],
                  index='https://downloads.arduino.cc/packages/package_index.json'),
              source_sha256={str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                             for p in sorted(SKETCH.iterdir()) if p.suffix in ('.ino', '.h', '.cpp')},
              build_artifacts_sha256={p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                      for p in sorted(BUILD.iterdir())
                                      if p.is_file() and p.suffix in ('.elf', '.bin', '.hex')},
              relay_output_enabled_by_default=False, hardware_uploaded=False, physical_tests=0,
              construction_released=False, protective_function_validated=False,
              limitation='Compilation only; not electrical safety approval or hardware behavior validation.')
OUT.write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
print(log)
print(record['status'])
sys.exit(result.returncode)
