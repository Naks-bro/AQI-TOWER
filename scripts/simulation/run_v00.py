"""Archive every mesh attempt, including missing dependencies; never run a flow solver."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts/geometry'))
from build_v00 import build


def main():
    sid = dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '-' + uuid.uuid4().hex[:8]
    attempt = ROOT / 'results' / sid
    attempt.mkdir(parents=True)
    report = {'simulation_id': sid, 'design_version': 'V00', 'classification': 'SIMULATION',
              'attempt_type': 'mesh_only', 'status': 'STARTED', 'warnings': [], 'errors': [],
              'solver_settings': {'solver': None, 'turbulence_model': None},
              'convergence_status': 'NOT_APPLICABLE_NO_FLOW_SOLVER', 'commands': [],
              'environment': {'platform': sys.platform, 'WM_PROJECT_VERSION': os.getenv('WM_PROJECT_VERSION')},
              'outputs': {k: None for k in ['pressure_field','velocity_field','velocity_vectors',
                  'volume_flow_rate','mass_flow_rate','pressure_drop','maximum_velocity',
                  'minimum_velocity','average_velocity','possible_recirculation_zones','plots_images']}}
    try:
        report['geometry_parameters'] = json.loads((ROOT / 'cad/parametric/v00.json').read_text())
        shutil.copy2(ROOT / 'cad/parametric/v00.json', attempt / 'v00.json')
        build()
        case = attempt / 'case'
        shutil.copytree(ROOT / 'cfd/V00_empty_tower/system', case / 'system')
        (case / 'constant').mkdir()
        report['input_sha256'] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in (case / 'system').iterdir()}
        report['input_sha256']['v00.json'] = hashlib.sha256((attempt / 'v00.json').read_bytes()).hexdigest()
        for command in [['blockMesh'], ['checkMesh', '-allTopology', '-allGeometry']]:
            executable = shutil.which(command[0])
            if not executable:
                raise RuntimeError(f'{command[0]} unavailable. Activate an OpenFOAM installation in this shell.')
            log = attempt / ('log.' + command[0])
            with log.open('w') as stream:
                run = subprocess.run([executable, *command[1:]], cwd=case, stdout=stream, stderr=subprocess.STDOUT, timeout=300)
            report['commands'].append({'command': command, 'executable': executable, 'returncode': run.returncode, 'log': log.name})
            if run.returncode:
                raise RuntimeError(f'{command[0]} failed; inspect {log.name}')
        mesh_log = (attempt / 'log.checkMesh').read_text(errors='replace')
        if 'Mesh OK.' not in mesh_log:
            raise RuntimeError('checkMesh did not explicitly report Mesh OK.; manual investigation required')
        (case / 'V00.foam').touch()
        report['status'] = 'MESH_CHECK_PASSED_NOT_FLOW_VALIDATED'
        report['mesh_information'] = {'path': 'case/constant/polyMesh', 'check_log': 'log.checkMesh'}
        report['warnings'].append('No flow solution. Inspect patch orientation and geometry in ParaView before accepting V00.')
    except Exception as exc:
        report['status'] = 'INCOMPLETE'
        report['errors'].append(str(exc))
    finally:
        report['finished_utc'] = dt.datetime.now(dt.timezone.utc).isoformat()
        (attempt / 'manifest.json').write_text(json.dumps(report, indent=2))
        print(json.dumps({'status': report['status'], 'manifest': str(attempt / 'manifest.json'), 'errors': report['errors']}, indent=2))
    return 0 if report['status'] == 'MESH_CHECK_PASSED_NOT_FLOW_VALIDATED' else 1


if __name__ == '__main__':
    sys.exit(main())
