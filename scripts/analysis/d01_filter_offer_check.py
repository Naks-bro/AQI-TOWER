"""Compare a supplied per-filter curve with D01. Never extrapolate or approve purchase.
CSV headers: per_filter_flow_m3h,pressure_Pa. Provide --source and --part.
Only arithmetic/evidence transcription is checked; source authenticity remains a review task.
"""
import argparse, csv, json, math, hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[2]

def validate(points):
    if len(points)<2: raise ValueError('At least two measured/OEM curve points are required; a rated point alone is insufficient.')
    for q,dp in points:
        if not math.isfinite(q) or not math.isfinite(dp) or min(q,dp)<0:
            raise ValueError('Finite non-negative flow and pressure required.')
    if any(a[0]>=b[0] for a,b in zip(points,points[1:])):
        raise ValueError('Flows must be strictly increasing; no duplicate points.')
    if any(a[1]>b[1] for a,b in zip(points,points[1:])):
        raise ValueError('Pressure decreases with increasing flow; review the supplied curve.')

def interpolate(points,q):
    validate(points)
    if not points[0][0]<=q<=points[-1][0]:return None
    for x,y in points:
        if x==q:return y
    for (a,b),(x,y) in zip(points,points[1:]):
        if a<q<x:return b+(y-b)*(q-a)/(x-a)
    raise AssertionError('Interpolation bracket missing')

def assess(points,budgets):
    validate(points)
    rows=[]
    for r in budgets:
        q=r['each_filter_flow_m3h']; dp=interpolate(points,q)
        allowance=min(r['brochure_filter_headroom_Pa'],r['numeric_filter_headroom_Pa'])
        rows.append(dict(total_flow_m3h=2*q,each_filter_flow_m3h=q,
            supplied_curve_pressure_Pa=dp,smaller_of_two_model_allowances_Pa=allowance,
            remaining_model_margin_Pa=None if dp is None else allowance-dp,
            screening_status='UNKNOWN_OUTSIDE_SUPPLIED_CURVE' if dp is None else
              ('EXCEEDS_MODEL_ALLOWANCE' if dp>allowance else 'WITHIN_MODEL_ALLOWANCE_NOT_RELEASED')))
    return rows

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('csv',type=Path);parser.add_argument('--source',required=True)
    parser.add_argument('--part',required=True);parser.add_argument('--output',type=Path,required=True)
    a=parser.parse_args()
    if a.output.exists():parser.error('Output exists; choose a new filename to preserve evidence.')
    with a.csv.open(newline='',encoding='utf-8-sig') as f:
        points=[(float(r['per_filter_flow_m3h']),float(r['pressure_Pa'])) for r in csv.DictReader(f)]
    budget=json.loads((R/'reports/prototype_d01/component_validation/pressure_comparison.json').read_text())
    result=dict(part=a.part,source=a.source,input_sha256=hashlib.sha256(a.csv.read_bytes()).hexdigest(),
      status='CURVE SCREEN ONLY - NOT A FIT, PERFORMANCE OR PURCHASE APPROVAL',
      basis='R01 assumed installed losses; smaller allowance of two fan analyses is not a guaranteed bound.',
      results=assess(points,budget['filter_headroom']),
      open_gates=['Source/part/revision and actual curve units authenticated by reviewer',
      'Dimensions/tolerances, gasket landing and retainer fit','Efficiency test evidence and loading data',
      'India availability and quotation','Actual installation, seals, structure, guards and electrical release'])
    with a.output.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
