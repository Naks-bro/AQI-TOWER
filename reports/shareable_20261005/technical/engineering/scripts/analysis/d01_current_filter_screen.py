"""Compare an evidenced per-filter curve with the current R03M pressure screen.

CSV columns: per_filter_flow_m3h,pressure_Pa. No extrapolation or purchase approval.
Run from the repository (or the handoff's engineering folder). Standard library only.
"""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import d01_validation


def validate(points):
    if len(points) < 2:
        raise ValueError('At least two curve points required')
    if any(not math.isfinite(x) or x < 0 for pair in points for x in pair):
        raise ValueError('Curve values must be finite and nonnegative')
    if any(a[0] >= b[0] for a,b in zip(points,points[1:])):
        raise ValueError('Flow points must be strictly increasing')
    if any(a[1] > b[1] for a,b in zip(points,points[1:])):
        raise ValueError('Decreasing resistance needs source review before this screen')


def interpolate(points, flow):
    if not points[0][0] <= flow <= points[-1][0]:
        return None
    for q,dp in points:
        if flow == q:
            return dp
    for (qa,pa),(qb,pb) in zip(points,points[1:]):
        if qa < flow < qb:
            return pa+(pb-pa)*(flow-qa)/(qb-qa)
    raise AssertionError('No interpolation bracket')


def assess(points, budget):
    validate(points)
    rows=[]
    for case in budget['rows']:
        dp=interpolate(points,case['per_filter_m3h'])
        margin=None if dp is None else case['filter_allowance_Pa']-dp
        status=('OUTSIDE_CURVE_RANGE' if margin is None else
                'NO_POSITIVE_MODEL_MARGIN' if margin <= 0 else
                'POSITIVE_MODEL_MARGIN_REQUIRES_VALIDATION')
        rows.append(dict(total_flow_m3h=case['total_m3h'],
                         per_filter_flow_m3h=case['per_filter_m3h'],
                         reducer_K=case['reducer_K'],fan_available_Pa=case['fan_Pa'],
                         other_model_losses_Pa=case['nonfilter_Pa'],
                         supplied_per_filter_pressure_Pa=dp,
                         remaining_model_margin_Pa=margin,status=status))
    return rows


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('csv',type=Path)
    parser.add_argument('--part',required=True,help='Exact part and revision')
    parser.add_argument('--source',required=True,help='OEM document/page or physical test record')
    parser.add_argument('--evidence',choices=['OEM','PHYSICAL'],required=True)
    parser.add_argument('--condition',choices=['CLEAN','LOADED'],required=True)
    parser.add_argument('--condition-ref',required=True,help='Documented loading/conditioning definition; no universal loaded threshold assumed')
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    if any(not x.strip() for x in (args.part,args.source,args.condition_ref)):
        parser.error('Part, source and condition references cannot be blank')
    if args.output.exists():
        parser.error('Output exists; choose a new filename')
    with args.csv.open(newline='',encoding='utf-8-sig') as f:
        reader=csv.DictReader(f)
        if not {'per_filter_flow_m3h','pressure_Pa'} <= set(reader.fieldnames or []):
            parser.error('CSV must use per-filter m3/h and Pa columns')
        points=[(float(r['per_filter_flow_m3h']),float(r['pressure_Pa'])) for r in reader]
    budget=d01_validation.pressure_rows()
    result=dict(geometry='R03M',part=args.part,source=args.source,evidence=args.evidence,
                condition=args.condition,condition_ref=args.condition_ref,
                source_csv_sha256=hashlib.sha256(args.csv.read_bytes()).hexdigest(),
                budget_input_hashes=budget['input_hashes'],
                screening_assumptions=budget['assumptions'],results=assess(points,budget),
                status='CONDITIONAL PRESSURE SCREEN ONLY',
                limits='User-supplied evidence labels are not authentication. Curves apply to one exact filter and stated condition. Two parallel filters are assumed equal; their losses are not added. Positive margin does not prove operating flow, reserve, efficiency, seal, safety or availability. Assess clean and loaded evidence separately; one condition cannot establish the other.')
    with args.output.open('x',encoding='utf-8') as f:
        json.dump(result,f,indent=2)
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
