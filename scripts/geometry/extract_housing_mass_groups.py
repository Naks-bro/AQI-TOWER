"""Read current inner-housing CAD volumes by role, without changing the model."""
import hashlib
import json
from pathlib import Path
import FreeCAD as App

ROOT=Path(__file__).resolve().parents[2]


def extract():
    path=ROOT/'cad/packaging/AQI_M03_Independent_Housing_STUDY.FCStd'
    digest=hashlib.sha256(path.read_bytes()).hexdigest()
    doc=App.openDocument(str(path))
    rows=[]
    try:
        for o in doc.Objects:
            if not hasattr(o,'Shape') or o.StudyKind!='assumed_material':
                continue
            if o.Name in ('Shell','HEPAServiceDoor','PrefilterServiceDoor'):
                group='cosmetic_casing'
            elif o.Name.startswith(('Post','Rail')):
                group='frame'
            elif o.Name in ('IndependentHEPASeat','IndependentPrefilterSeat','HEPARetainerEnvelope'):
                group='seats_and_retainer'
            elif o.Name in ('Transition','InletNeck','StraightOutlet'):
                group='airpath'
            else:
                group='inner_housing_panels'
            rows.append({'part':o.Name,'group':group,'volume_mm3':o.Shape.Volume})
    finally:
        App.closeDocument(doc.Name)
    assert hashlib.sha256(path.read_bytes()).hexdigest()==digest
    output={'status':'CAD VOLUMES ONLY; MATERIAL/GRADE NOT SELECTED',
            'source':str(path.relative_to(ROOT)).replace('\\','/'),'sha256_unchanged':digest,'parts':rows}
    target=ROOT/'results/fan_selection/housing_mass_groups.json'
    target.write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print('Read-only grouped inventory:',len(rows),'material shapes')


if __name__=='__main__':
    extract()
