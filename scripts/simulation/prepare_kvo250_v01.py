"""Upgrade the unrun placeholder to KVO 250, preserving it and all V00 data.

Run with Windows Python. Uses only the six supplied SI curve points; no refitting.
The coded OpenFOAM boundary supplies a lumped terminal suction fan, not blades.
"""
from pathlib import Path
import json
import hashlib
import shutil

ROOT = Path(__file__).resolve().parents[2]
CASE = ROOT/'cfd/V01_fan'
SRC = ROOT/'cfd/V00'


def header(name, cls='dictionary'):
    return f'FoamFile {{ version 2.0; format ascii; class {cls}; object {name}; }}\n'


def main():
    if (CASE/'logs/foamRun_kvo.log').exists():
        raise RuntimeError('Protecting existing KVO run; no automatic reset')
    archive = CASE/'archive_placeholder'
    if not archive.exists():
        archive.mkdir(parents=True)
        for sub in ['0','constant','system']:
            if (CASE/sub).exists():
                shutil.copytree(CASE/sub,archive/sub)
        for path in ['cfd/V01_fan/README.md','docs/FAN_CFD_V01.md',
                     'results/CFD_V01_FAN_RESULTS.md','scripts/simulation/run_cfd_v01_fan.sh']:
            if (ROOT/path).exists():
                shutil.copy2(ROOT/path,archive/Path(path).name)
    (CASE/'logs').mkdir(exist_ok=True)
    data_path = ROOT/'data/fans/systemair_KVO_250.json'
    fan = json.loads(data_path.read_text(encoding='utf-8'))
    points = fan['fan_curve_points']
    assert len(points) == 6
    q = [p['Q_m3s'] for p in points]
    dp = [p['delta_P_static_Pa'] for p in points]
    assert q[0] == 0 and dp[-1] == 0
    assert all(a<b for a,b in zip(q,q[1:]))
    assert all(a>=b for a,b in zip(dp,dp[1:]))
    for p in points:
        assert abs(p['Q_m3s']*3600-p['Q_m3h']) < 1
    source_hash = hashlib.sha256(data_path.read_bytes()).hexdigest()
    mesh_hashes = {}
    for p in (SRC/'constant/polyMesh').iterdir():
        if p.is_file():
            dest = CASE/'constant/polyMesh'/p.name
            dest.parent.mkdir(exist_ok=True)
            shutil.copy2(p,dest)
            mesh_hashes[p.name] = hashlib.sha256(p.read_bytes()).hexdigest()
            assert hashlib.sha256(dest.read_bytes()).hexdigest() == mesh_hashes[p.name]
    shutil.copy2(SRC/'geometry_audit.json',CASE/'geometry_audit.json')
    # Keep native cells/points/faces unchanged. Only the existing terminal patch
    # receives an idealized fan pressure law; it is the fan's upstream boundary.
    curve = '\n'.join(f'({a:.10g} {b:.10g})' for a,b in zip(q,dp))
    (CASE/'constant/kvo250_static_curve_Pa').write_text('// Source SI values, unchanged\n(\n'+curve+'\n)\n',encoding='utf-8')
    cpp = r'''
        const auto& phi = patch().lookupPatchField<surfaceScalarField, scalar>("phi");
        const auto& U = patch().lookupPatchField<volVectorField, vector>("U");
        const scalar Q = gSum(phi);
        const scalar qs[] = {Q_VALUES};
        const scalar ps[] = {P_VALUES};
        const scalar x = max(min(Q, qs[5]), scalar(0));
        scalar Ps = ps[5];
        for (label j=0; j<5; ++j)
        {
            if (x <= qs[j+1])
            {
                Ps = ps[j] + (ps[j+1]-ps[j])*(x-qs[j])/(qs[j+1]-qs[j]);
                break;
            }
        }
        // p is kinematic. Fan static Ps = downstream static - upstream total.
        // Downstream ambient static is zero. Upstream patch is uniform static;
        // its net flux-weighted total is p + K. Thus p = -Ps/rho - K.
        const scalar K = Q > 1e-6 ? gSum(phi*0.5*magSqr(U))/Q : 0;
        const scalar target = Ps/1.20 + K;
        static label previousIndex = -1;
        static scalar applied = 0;
        const label index = this->db().time().timeIndex();
        if (previousIndex < 0)
            applied = -gSum(patch().magSf()*scalarField(*this))/gSum(patch().magSf());
        if (index != previousIndex)
        {
            applied = 0.9*applied + 0.1*target;
            previousIndex = index;
            if (index % 10 == 0)
                Info<< "KVO250 Q=" << Q << " Ps_Pa=" << Ps
                    << " K_m2s2=" << K << " applied_Pa=" << 1.20*applied
                    << " closure_Pa=" << 1.20*(applied-target)
                    << " outsideCurve=" << (Q < 0 || Q > qs[5]) << nl;
        }
        operator==(-applied);
'''.replace('Q_VALUES',', '.join(map(str,q))).replace('P_VALUES',', '.join(map(str,dp)))
    pressure = header('p','volScalarField') + '''dimensions [0 2 -2 0 0 0 0];
internalField uniform -15;
boundaryField
{
    AIR_INLET { type totalPressure; p0 uniform 0; value uniform 0; }
    AIR_OUTLET
    {
        type codedFixedValue;
        name kvo250TerminalSuction;
        value uniform -25;
        codeInclude
        #{
            #include "volFields.H"
            #include "surfaceFields.H"
            #include "Time.H"
        #};
        codeOptions
        #{
            -I$(LIB_SRC)/finiteVolume/lnInclude -I$(LIB_SRC)/meshTools/lnInclude
        #};
        codeLibs
        #{
            -lfiniteVolume -lmeshTools
        #};
        code
        #{
''' + cpp + '''
        #};
    }
    WALLS { type zeroGradient; }
}
'''
    (CASE/'0/p').write_text(pressure,encoding='utf-8')
    (CASE/'0/U').write_text(header('U','volVectorField')+'''dimensions [0 1 -1 0 0 0 0];
internalField uniform (0.9 0 0);
boundaryField
{
 AIR_INLET { type pressureInletOutletVelocity; value uniform (0.9 0 0); }
 AIR_OUTLET { type pressureInletOutletVelocity; value uniform (2.8 0 0); }
 WALLS { type noSlip; }
}
''',encoding='utf-8')
    # Retain V00's turbulence assumptions; these values never impose bulk flow.
    for f in ['k','epsilon','nut']:
        shutil.copy2(SRC/'0'/f,CASE/'0'/f)
    for f in ['physicalProperties','momentumTransport']:
        shutil.copy2(SRC/'constant'/f,CASE/'constant'/f)
    (CASE/'constant/fanProperties').write_text(header('fanProperties')+'''// Historical 300 Pa model superseded. This file is descriptive, not solver input.
fanModel KVO250;
curveSource "data/fans/systemair_KVO_250.json";
implementation "0/p AIR_OUTLET codedFixedValue";
rhoReference 1.20;
''',encoding='utf-8')
    # Fresh KVO case, not any continuation/re-execution of V00.
    control = (CASE/'system/controlDict').read_text()
    import re
    for key,value in [('startFrom','startTime'),('startTime','0'),('endTime','3000')]:
        control = re.sub(r'\b'+key+r'\s+[^;]+;',f'{key} {value};',control)
    (CASE/'system/controlDict').write_text(control,encoding='utf-8')
    (CASE/'V01.foam').touch()
    record = {'source_json_sha256':source_hash,'source_points_unchanged':points,
              'mesh_file_sha256':mesh_hashes,'mesh_change':'NONE; copied V00 mesh exactly',
              'fan_patch':'AIR_OUTLET; upstream suction plane at X=0.700 m',
              'fan_pressure_definition':'Ps = p_static_discharge - p_total_suction',
              'boundary_law':'uniform p/1.2 = -Ps(Q)/1.2 - sum(phi*|U|^2/2)/sum(phi)',
              'boundary_head_relaxation':0.1,'interpolation':'piecewise linear in Q_m3s; endpoint clamp flagged',
              'limits':'Ideal zero-total-loss adapter, uniform static suction; no physical 250mm duct modeled'}
    (CASE/'fan_implementation.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
    print('Prepared real KVO 250 case. Source JSON and all V00 files left unchanged.')


if __name__ == '__main__':
    main()
