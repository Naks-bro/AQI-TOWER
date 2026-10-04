"""Read-only engineering/handoff provenance audit; never a physical release.

Optional pypdf enables PDF page/text checks. Use --write-results only to refresh
the audit-owned batch_review outputs. Other project files are never modified.
"""
import argparse
import csv
import hashlib
import io
import itertools
import json
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[2]
TOWER = 'reports/prototype_d01/mechanical_package/D01_R03M_ASSEMBLY.FCStd'
TOWER_HASH = 'fb28a31315968509dcdbbb2caac8c6d69c84ecb94a35ccd75937a5d9ecaa33a6'
CONTROL = 'reports/prototype_d01/electrical_package/control_module/'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def exact_case_exists(root, relative):
    """Check case-sensitive link spelling even on Windows."""
    directory = root
    for segment in Path(relative).parts:
        names = {p.name for p in directory.iterdir()} if directory.is_dir() else set()
        if segment not in names:
            return False
        directory = directory / segment
    return directory.is_file()


def audit(root):
    checks, findings, provenance = [], [], {}

    def read(name):
        data = (root / name).read_bytes()
        provenance[name] = digest(data)
        return data

    def check(name, condition, detail):
        checks.append({'check': name, 'passed': bool(condition), 'detail': detail})

    def finding(code, priority, file, detail, action):
        findings.append(dict(id=code, priority=priority, file=file, finding=detail,
                             integration_action=action))

    tower = read(TOWER)
    check('native_tower_hash', digest(tower) == TOWER_HASH, TOWER)
    with zipfile.ZipFile(io.BytesIO(tower)) as z:
        doc = ET.fromstring(z.read('Document.xml'))
        objects = doc.find('Objects')
        count = len(objects.findall('Object'))
        check('native_tower_493_objects', count == 493, f'{count} objects')

    ctrl = json.loads(read(CONTROL + 'CURRENT_CONTROL_CHECKS.json'))
    check('control_review_not_release', ctrl['release'] is False and
          ctrl['physical_tests'] == 0 and ctrl['actual_routing_verified'] is False,
          'Assumed reservations only; physical 0; actual wiring unverified')
    check('control_revision_current', ctrl['revision'] == 'E05' and ctrl['objects'] == 18,
          'Current same-module E05, 18 proxy objects')
    with zipfile.ZipFile(io.BytesIO(read(CONTROL + 'D01_E05_CURRENT_CONTROL_LAYOUT.FCStd'))) as z:
        control_doc = ET.fromstring(z.read('Document.xml'))
        check('current_control_18_native_objects',
              len(control_doc.find('Objects').findall('Object')) == 18,
              '18 original proxy objects; not OEM manufacturing geometry')
    check('all_12_box_body_reservations_clear', len(ctrl['actual_box_checks']) == 12 and
          all(not row['hits'] for row in ctrl['actual_box_checks']),
          'Twelve modeled volumes checked against OEM box except mounting panel')
    expected_buttons = {'START': ('ZB5AA3','ZBE1016','NO','I1','A0'),
                        'STOP': ('ZB5AA4','ZBE1026','NC','I2','A1'),
                        'RESET': ('ZB5AA6','ZBE1016','NO','I3','A2')}
    check('ordinary_button_candidate_identity', len(ctrl['buttons']) == 3 and
          all(b['name'] in expected_buttons and
              tuple(b[k] for k in ('head','contact','contact_type','terminal','firmware_pin')) ==
              expected_buttons[b['name']] and b['collar'] == 'ZB5AZ009'
              for b in ctrl['buttons']),
          'Exact candidate sensing chain only; not low-current release or safety isolation')
    for button in ctrl['buttons']:
        check(f"{button['name']}_assumed_service_clear",
              all(v < .01 for v in button['assumed_service_overlap_mm3'].values()),
              'Reservation intersection only, not real connector fit')
    expected_pairs = {frozenset(p) for p in itertools.combinations(
        ['CTRL1_WIRE_SPACE_ASSUMED', 'H1_CONNECTOR_SPACE_ASSUMED',
         'SC1_CONNECTOR_SPACE_ASSUMED'], 2)}
    actual_pairs = {frozenset(p['objects']) for p in ctrl['service_pair_checks']}
    valid_pairs = actual_pairs == expected_pairs and all(
        len(set(p['objects'])) == 2 for p in ctrl['service_pair_checks'])
    check('all_three_service_pair_labels', valid_pairs,
          'Every unordered pair must appear exactly once; self-pair invalid')
    if not valid_pairs:
        finding('A01', 'HIGH', 'scripts/geometry/close_d01_control_layout.py',
                'service_pairs.append is outside the inner loop. Evidence omits CTRL1/H1 '
                'and records SC1/SC1 with a stale 10mm gap. Inner-loop overlap checks '
                'still ran, but reported pair labels are inaccurate.',
                'Indent append into inner loop; rerun geometry/report/bundles; retain old snapshots.')

    build = json.loads(read('reports/prototype_d01/electrical_package/OPTA_BOARD_BUILD.json'))
    check('target_build_claim_boundary', build['target_board_compiled'] is True and
          build['relay_output_enabled_by_default'] is False and
          build['hardware_uploaded'] is False and build['physical_tests'] == 0 and
          build['construction_released'] is False, 'Compile only, never hardware proof')
    for name, expected in build['source_sha256'].items():
        name = name.replace('\\', '/')
        check('target_build_source:' + name, digest(read(name)) == expected,
              'Board compilation evidence matches actual current source')
    sketch = read('firmware/d01_opta_review/d01_opta_review.ino').decode('utf-8')
    check('firmware_default_disabled', bool(re.search(
        r'#define\s+AQI_BENCH_LAMP_OUTPUT_ENABLED\s+0\b', sketch)),
          'Default ordinary output disabled; macro override requires separate reviewed bench')

    budget_path = 'reports/prototype_d01/batch_summary/CURRENT_PRESSURE_BUDGET.json'
    if not (root / budget_path).exists():
        budget_path = 'reports/prototype_d01/validation_package/R03M_PRESSURE_BUDGET.json'
    budget = json.loads(read(budget_path))
    for name, expected in budget['input_hashes'].items():
        name = name.replace('\\', '/')
        check('pressure_input:' + name, digest(read(name)) == expected, 'OEM curve/pattern provenance')
    screen = [r for r in budget['rows'] if r['total_m3h'] == 300 and r['reducer_K'] == 1]
    check('pressure_screen_identity', len(screen) == 1 and
          abs(screen[0]['filter_allowance_Pa'] - 14.316) < .01,
          '300 m3/h / K1 assumed screen only; not measured operating point')

    delivery = root / 'reports/shareable_20261005'
    compared, missing = 0, []
    for audience in ('stakeholder', 'technical'):
        folder = delivery / audience
        manifest = json.loads(read(f'reports/shareable_20261005/{audience}/MANIFEST.json'))
        archive = delivery / f'AQI_TOWER_{audience.upper()}_BUNDLE.zip'
        with zipfile.ZipFile(archive) as z:
            check(f'{audience}_zip_members', set(z.namelist()) == set(manifest) | {'MANIFEST.json'},
                  f'{len(manifest)} payload files')
            check(f'{audience}_zip_manifest', json.loads(z.read('MANIFEST.json')) == manifest,
                  'Embedded and external manifest agree')
            bad = []
            generated = []
            for name, expected in manifest.items():
                if digest(z.read(name)) != expected or digest((folder / name).read_bytes()) != expected:
                    bad.append(name)
                if name.startswith('engineering/'):
                    source = name[len('engineering/'):]
                    # This audit report is a snapshot of an earlier package check.
                    # Hashing it into itself causes endless recursive provenance churn.
                    if source in ('reports/prototype_d01/batch_review/HANDOFF_CONSISTENCY.json',
                                  'reports/prototype_d01/batch_review/AUDIT_FINDINGS.csv'):
                        continue
                    if '__pycache__' in Path(source).parts or source.lower().endswith(('.pyc', '.fcbak')):
                        generated.append(source)
                        continue
                    if (root / source).is_file():
                        compared += 1
                        current = read(source)
                        packed = (folder / name).read_bytes()
                        text_suffixes = {'.py','.ino','.h','.md','.json','.csv','.step','.dxf','.txt'}
                        normalized_equal = (Path(source).suffix.lower() in text_suffixes and
                            current.replace(b'\r\n', b'\n') == packed.replace(b'\r\n', b'\n'))
                        check('packaged_source:' + source,
                              digest(current) == expected or normalized_equal,
                              'Byte-identical' if digest(current) == expected else
                              ('Content-identical; LF/CRLF differs' if normalized_equal else 'Current root differs'))
                    else:
                        missing.append(source)
            check(f'{audience}_all_payload_hashes', not bad, json.dumps(bad))
            check(f'{audience}_no_generated_caches_or_backups', not generated, json.dumps(generated))
    check('packaged_engineering_sources_resolve', not missing, json.dumps(missing))
    if 'batch_summary' in budget_path:
        check('current_pressure_top_level_copy',
              (delivery / 'technical/CURRENT_PRESSURE_BUDGET.json').read_bytes() == (root / budget_path).read_bytes(),
              'Current top-level pressure screen equals newly regenerated root evidence')

    parts_path = 'reports/prototype_d01/batch_review/CURRENT_COMBINED_PARTS_REGISTER.csv'
    if (root / parts_path).exists():
        parts = list(csv.DictReader(io.StringIO(read(parts_path).decode('utf-8-sig'))))
        check('current_parts_register_links', all((root / p['Evidence']).exists() for p in parts),
              f'{len(parts)} candidate/proposed/unselected lines; source paths resolve')
        wrong_case = [p['Evidence'] for p in parts if not exact_case_exists(root, p['Evidence'])]
        check('current_parts_register_case_sensitive_links', not wrong_case,
              json.dumps(wrong_case))
        check('current_parts_no_duplicate_ids', len({p['ID'] for p in parts}) == len(parts),
              'No duplicated scheduled quantities')
        top_parts = delivery / 'technical/CURRENT_COMBINED_PARTS_REGISTER.csv'
        check('current_parts_top_level_copy', top_parts.exists() and
              top_parts.read_bytes() == (root / parts_path).read_bytes(),
              'Current consolidated candidate register at technical entry point')
        package_missing = sorted({p['Evidence'] for p in parts
                                  if not (delivery / 'technical/engineering' / p['Evidence']).is_file()})
        check('current_parts_packaged_evidence_paths', not package_missing,
              json.dumps(package_missing))

    try:
        from pypdf import PdfReader
    except ImportError:
        finding('A04', 'INFO', 'reports/shareable_20261005/technical/AQI_TOWER_TECHNICAL_HANDOFF.pdf',
                'PDF extraction skipped: pypdf not in this runtime.',
                'Run existing bundled report Python; do not install software for this audit.')
    else:
        pdf_path = 'reports/shareable_20261005/technical/AQI_TOWER_TECHNICAL_HANDOFF.pdf'
        pdf = PdfReader(io.BytesIO(read(pdf_path)))
        page_text = [p.extract_text() or '' for p in pdf.pages]
        check('pdf_current_prefix', len(pdf.pages) >= 56 and 'E05' in '\n'.join(page_text[:6]),
              f'{len(pdf.pages)} pages; current E05 material must precede snapshots')
        stale = [{'page': i+1, 'text': ' '.join(t.split())[:180]}
                 for i, t in enumerate(page_text)
                 if i >= 6 and ('140 x 100 x 40' in t or '140x100x40' in t or
                                'not target' in t.lower() or 'not board' in t.lower())]
        if stale:
            finding('A02', 'MEDIUM', pdf_path,
                    'Preserved reference pages contain superseded enclosure/build wording: '
                    + json.dumps(stale),
                    'Keep originals unchanged; current consolidated parts/status sheet '
                    'must take precedence over embedded historical snapshots.')

    bom = read('reports/prototype_d01/internal_handoff_20261005/COMBINED_PARTS_REGISTER.csv').decode('utf-8-sig')
    check('historical_exact_fan_filter_identifiers', 'ACFAN00287A' in bom and '104.633.30' in bom,
          'Experimental IKEA reference, not manufacturer-approved custom purifier use')
    if '140x100x40' in bom and '1554XA2GY' not in bom:
        finding('A03', 'MEDIUM', 'reports/prototype_d01/internal_handoff_20261005/COMBINED_PARTS_REGISTER.csv',
                'Preserved IH02 parts register still has unselected 140x100x40 BOX and '
                'does not contain current Opta, Hammond box/panel, buttons/collars/contacts.',
                'Do not rewrite IH02 snapshot. Publish CURRENT_COMBINED_PARTS_REGISTER.csv '
                'at bundle entry point with quantities/status and links to current exact evidence.')
    return dict(status='PASS' if all(c['passed'] for c in checks) else 'FAIL',
                scope='Digital evidence/packaging consistency only; no construction approval',
                physical_tests=0, checks=checks, findings=findings,
                packaged_current_sources_compared=compared, source_sha256=provenance)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--write-results', action='store_true')
    args = parser.parse_args()
    result = audit(args.root.resolve())
    if args.write_results:
        out = args.root / 'reports/prototype_d01/batch_review'
        out.mkdir(parents=True, exist_ok=True)
        (out / 'HANDOFF_CONSISTENCY.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
        with (out / 'AUDIT_FINDINGS.csv').open('w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['id','priority','file','finding','integration_action'])
            writer.writeheader(); writer.writerows(result['findings'])
    failed = [c for c in result['checks'] if not c['passed']]
    print(f"{result['status']}: {len(result['checks'])} checks; {len(failed)} failures; "
          f"{result['packaged_current_sources_compared']} root/package comparisons")
    for c in failed:
        print(f"FAIL {c['check']}: {c['detail']}")
    print('Not fabrication, energization or physical-performance approval.')
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
