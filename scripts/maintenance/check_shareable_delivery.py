"""Check current two-audience ZIPs and source provenance; no physical validation."""
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[2]
DELIVERY = ROOT / 'reports/shareable_20261005'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    count = 0
    for audience in ('stakeholder', 'technical'):
        folder = DELIVERY / audience
        manifest = json.loads((folder / 'MANIFEST.json').read_text(encoding='utf-8'))
        archive = DELIVERY / f'AQI_TOWER_{audience.upper()}_BUNDLE.zip'
        with zipfile.ZipFile(archive) as z:
            assert set(z.namelist()) == set(manifest) | {'MANIFEST.json'}
            assert json.loads(z.read('MANIFEST.json')) == manifest
            for name, expected in manifest.items():
                assert '..' not in Path(name).parts and not Path(name).is_absolute()
                assert sha(z.read(name)) == expected, f'ZIP mismatch: {name}'
                assert sha((folder / name).read_bytes()) == expected, f'Folder mismatch: {name}'
                count += 1
        assert (folder / 'AQI_TOWER_3D_REVIEW.html').read_bytes() == (DELIVERY / 'AQI_TOWER_3D_REVIEW.html').read_bytes()
    relative = Path('reports/prototype_d01/mechanical_package/D01_R03M_ASSEMBLY.FCStd')
    expected = 'fb28a31315968509dcdbbb2caac8c6d69c84ecb94a35ccd75937a5d9ecaa33a6'
    assert sha((ROOT / relative).read_bytes()) == expected
    assert sha((DELIVERY / 'technical/engineering' / relative).read_bytes()) == expected
    assert (DELIVERY / 'technical/AQI_R03M_REVIEW.blend').read_bytes() == (DELIVERY / 'visuals/AQI_R03M_REVIEW.blend').read_bytes()
    print(f'PASS: {count} packaged payload files; both manifests, offline viewer copies and CAD/Blender provenance agree.')
    print('Digital integrity only. No construction release or physical performance validation.')


if __name__ == '__main__':
    main()
