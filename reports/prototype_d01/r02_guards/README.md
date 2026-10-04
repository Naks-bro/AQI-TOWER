# D01 R02G — independently attached fan guards

03 October 2026. **REVIEW ONLY: not released for manufacture or energizing.** Same integrated D01 assembly, continuing R02H. Physical prototypes: **0**.

## Deliverables

- [Two-sheet guard mounting drawing](D01_R02G_GUARD_MOUNTINGS.pdf)
- [Integrated FreeCAD assembly](D01_R02G_ASSEMBLY.FCStd) / [STEP](D01_R02G_ASSEMBLY.step)
- [Guard hardware delta BOM](GUARD_DELTA_BOM.csv)
- [Checks and source hash](checks.json) / [mount coordinates](mounts.json)

## Change and reason

DETECTED: R01 through R02H used four shared bolts to attach both upper and lower guard brackets. This coupled their retention. RECOMMENDATION implemented in CAD: four bolts per guard, with separate locations. Removing one set no longer removes the other's modeled attachment. This does not establish that either guard is safe or sufficiently strong.

Outer brackets now begin at y100 and220 mm, with bolt centres y120 and240. Inner brackets retain starts40 and280, bolt centres60 and300. Both sets use x105 and445. The9 mm fan plate gets four additional4.5 mm holes. Outer side skirts get a NEW blank hole pattern at y110/130/230/250,z590; omit historical y50/70/290/310 holes. The CAD fills the historical holes to describe this new blank, NOT a physical hole-plugging instruction. Bracket names retain old identifiers; use current coordinates, not the numeric name suffix.

Proposed hardware: eight M4x20 cap screws, eight7 mm AF x5 mm nuts and sixteen12 mm OD x1 mm washers. Washer bore4.3 mm remains assumed. These replace four shared M4x25 screws, four nut envelopes and eight earlier washers; do not add both hardware sets. Nominal screw projection beyond the nut is2 mm; actual locking engagement/tolerances unverified. Material, torque and reuse limits are not released.

## Verification

245 valid objects;8,641 changed-part pair checks have no positive-volume collision above0.05 mm3. Native reopen and STEP validity/volume checks pass. R02H source hash remains unchanged. Unchanged component pairs, reservation objects and inherited guard-to-guard seams are excluded.

Sixteen tool envelope checks clear: at each of eight mounts, an assumed4 mm diameter straight driver shaft extends100 mm above the screw; an assumed12 mm OD socket extends25 mm below the lower washer with clearance for the nut. Own fastening hardware is excluded. These are space reservations, not selected tools. No handles, hands, insertion trajectory, screw extraction motion, tolerance stack or physical access test is claimed. Guard-removal motion itself has not been verified. No new airflow, leakage, strength or physical result exists.

## Sources and evidence limits

Accessed2026-10-03:

- [Accu M4x20 cap screw](https://www.accu.co.uk/metric-cap-head-screws/250243-SSC-M4-20-A4-R360):20 mm under-head length,7 mm head diameter,4 mm head height,3 mm hex drive. Used only for dimensional reference; its coating/material and availability are not selected or verified for procurement.
- [Accu M4 nut](https://www.accu.co.uk/hexagon-nylon-locking-nuts/7958-HNN-M4-A4):7 mm across flats,5 mm height,0.7 mm pitch. Simplified envelope; no modeled threads/nylon insert.
- [Easyfix large M4 washer](https://www.screwfix.com/p/easyfix-steel-large-flat-washers-m4-x-1mm-100-pack/194ft):12 mm OD and1 mm thickness; bore remains assumed.
- [HSE machinery safety guidance](https://www.hse.gov.uk/work-equipment-machinery/introduction.htm) and [maintenance guidance](https://www.hse.gov.uk/work-equipment-machinery/maintenance.htm): supporting safety principles for guarding and isolation. UK guidance is NOT an Indian conformity determination, product certification or a completed risk assessment.

## Assembly review sequence and remaining gate

Prepare revised plate and outer skirt blanks, retaining other specified panel features. Complete reviewed guard face/skirt seams and bracket rivet joints. Fit inner guard independently, then outer guard. With power disconnected and reconnection prevented, verify each set remains retained when the other is removed. Collect loose hardware; these screws/nuts are not captive. Never perform this check with fans moving. Actual tool/reach and retention checks remain to be done physically by a qualified assembler/reviewer.

Unresolved: exact rivets/grip and their strength, skirt corners/face joins, guard deflection and reach protection, captive hardware or equivalent risk reduction, root radii, plate/joint strength, protected cable entry, remaining cabinet M5 hardware, filter resistance/sealing, rated isolation and restart protection. The earlier guard perforations remain a visual annotation; CAD sheets are envelopes. New bolt penetrations require sealing assessment. No physical release, outdoor/public robustness claim or India heat qualification follows from this revision.

The next useful digital closure is guard sheet/rivet joining and remaining cabinet hardware, alongside protective electrical access/isolation design. Filter pressure and seal evidence still block a defensible performance claim.

## Reproduce

From project root:

```powershell
& 'D:\Applications\FreeCAD 1.1.3\bin\python.exe' scripts/geometry/detail_d01_independent_guards.py
& 'C:\Users\G15 5530\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' scripts/reports/build_d01_guard_report.py
```
