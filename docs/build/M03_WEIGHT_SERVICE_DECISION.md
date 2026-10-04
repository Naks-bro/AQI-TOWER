# M03 — weight and service-access decision sheet

2 October 2026. COMPARISON ONLY — NO MATERIAL, TOLERANCE OR DIMENSION RELEASE.

## The useful next direction

**RECOMMENDATION:** first investigate a lighter cosmetic outer casing while keeping the structural frame and sealed inner housing under separate review. Do not thin every part or change every part to aluminium just to reach a lighter number. Also reserve real space for inner-panel seals, latches and withdrawal—not just the filter envelope.

The current CAD is preserved. The following alternatives are calculations on its volumes or hypothetical service envelopes, not newly built or validated assemblies.

## Where the weight actually is

**DETECTED:** read-only extraction grouped 32 material-study shapes from the 36-solid independent-housing model. Four component envelopes were excluded. File hash unchanged.

| Group, existing geometry | Mass at assumed steel density |
|---|---:|
| Cosmetic casing and its two doors | 94.14 kg |
| Continuous frame routes | 39.73 kg |
| Inner housing panels | 36.30 kg |
| Filter seats and HEPA retainer | 12.37 kg |
| M04 air-path pieces | 8.73 kg |
| **Partial material total** | **191.27 kg** |

**ASSUMPTIONS:** steel 7,850 kg/m3; aluminium 2,700 kg/m3. No grade, temper, gauge change, strength equivalence or actual supply availability is implied. Current thicknesses remain geometry assumptions.

| Same-geometry material scenario | Partial material subtotal | What changes in the calculation |
|---|---:|---|
| All steel baseline | 191.27 kg | Nothing |
| Aluminium cosmetic casing only | 129.52 kg | Casing/outer door density only; all other groups still steel |
| Aluminium casing and inner panels | 105.70 kg | Casing and inner-panel densities only; frame, seats/retainer and M04 still steel |

The casing-only scenario reduces the subtotal by about **61.76 kg** without changing the primary frame in the calculation. It still needs casing stiffness, attachment, handling, electrical bonding and durability review. The second hybrid also changes the sealed housing and carries additional stiffness/joint/seal concerns; it is not preferred or approved merely because its subtotal is smaller.

**UNKNOWN:** complete machine weight. All scenarios exclude the actual fan, filters, gasket, base, mounts, fasteners, guards, electrical equipment and cables. Do not quote 129.52 or 105.70 kg as a finished product weight. Smaller mass also means less gravitational restoring weight; full stability must be recalculated.

Mixed aluminium/steel interfaces require a corrosion review, especially for eventual wet outdoor exposure. NASA describes galvanic corrosion between dissimilar metals where an electrolyte and conductive path are present, including aluminium/steel examples: [NASA forms of corrosion](https://public.ksc.nasa.gov/corrosion/forms-of-corrosion/) (source checked 2 October 2026). This is a general warning, not an approved coating/isolation detail. Mechanical isolation/coating decisions must be coordinated with the qualified electrical bonding design.

## Why the current service gap is not enough to freeze

**DETECTED geometry:** the assumed retainer is 633 mm wide and the inner service opening is 635 mm, giving only 1 mm nominal per side. Actual supplier tolerances and retainer hardware are UNKNOWN.

**ASSUMED sensitivity, not a tolerance specification:** opening total shortfall 1 mm; retainer total oversize 1 mm; lateral misalignment 1 mm; coating 0.2 mm on each confronting edge surface.

```text
Minimum illustrative side gap
  = (opening - shortfall - part - oversize) / 2
    - lateral offset - two confronting coating thicknesses
```

| Hypothetical opening | Nominal side gap | Gap with the assumed allowances |
|---|---:|---:|
| Existing 635 mm | 1.0 mm | -1.4 mm: potential interference |
| Comparison 645 mm | 6.0 mm | 3.6 mm: positive arithmetic clearance, not release approval |

The wider opening is not edited into the CAD. It does not establish enough room for fingers, tools, latch motion, the real gasket or safe handling. The front of the current 653 mm housing would have narrow remaining wall lands; a real flange/door construction must be designed rather than merely enlarging a cutout.

## Door/seal hardware can conflict with the round casing

Consider an **assumed** centred flat panel around a 645 mm opening, with 15 mm seal/flange land each side and 10 mm forward hardware projection from the 653 mm housing front. These are envelope examples, not OEM gasket or latch requirements.

The furthest front corner is at x = 337.5 mm and distance from the centreline in y = 336.5 mm. Its radius is about 476.59 mm.

| Hypothetical casing internal diameter | Nominal corner clearance |
|---|---:|
| Current 950 mm | -1.59 mm: this assumed envelope crosses the casing |
| Comparison 980 mm | 13.41 mm: clears only this nominal corner calculation |

Formula: casing radius - sqrt((opening/2 + flange land)^2 + (housing side/2 + forward projection)^2).

The 980 mm casing is NOT a selected dimension or a fully checked CAD branch. A larger diameter does not change the current housing-to-post gap (6 mm) unless the frame/housing arrangement also changes. Outer casing service openings, hinges, panels, assembly access and seal/latch envelopes all need an integrated check. The wider/larger examples do not belong to the existing 36-solid “no clash” result.

## Decision and next action

1. Put **lighter cosmetic cladding** first in the material comparison; do not select an alloy or reduced thickness yet.
2. Develop a real removable inner-panel flange/seal/latch concept with accessible clamps and supplier tolerances. Use the hypothetical 645 mm opening / 980 mm casing only as starting points to compare, not requirements.
3. Resolve the housing/post gap and ear/support joints with manufacturing/tooling allowances; leave no guessed fastener schedule.
4. Obtain OEM fan/filter drawings and qualified mechanical/electrical reviewers through the existing draft requests. The unresolved inputs are not fixed by another density calculation.
5. Recheck complete assembly fit, pressure losses, full mass/CG/stability and seal-plane stiffness after actual materials and geometry are chosen.

**Build status:** design development; none of the six [remaining build gates](BUILD_REMAINING.md) closes from this comparison. No material ordered, supplier contacted, CAD modified, FEA/CFD run or physical test performed.

## Reproduce

```powershell
& 'D:\Applications\FreeCAD 1.1.3\bin\python.exe' scripts/geometry/extract_housing_mass_groups.py
python scripts/analysis/weight_service_screen.py
python -m unittest discover -s scripts/analysis -p '*screen.py'
```

Outputs: `results/fan_selection/housing_mass_groups.json` and `weight_service_screen.json`. Six new unit tests check nominal/tolerance gaps, wider-opening arithmetic, shell-radius sensitivity, group-density substitutions and invalid-input handling. They validate arithmetic, not strength or manufacturability.
