# D01 R02H — adapter hardware and service detail

Continued by [R02G independent guard mountings](../../r02_guards/README.md), which retains this adapter hardware and revises the fan guard fixings. Use its integrated CAD for latest assembly review. This revision remains preserved as evidence.

03 October 2026. **REVIEW ONLY. Not released for fabrication or energizing.**

This is a detail revision of the same R02 cabinet, not a new tower concept. Original R02 is preserved. Physical prototypes: **0**.

- [Dimensioned review sheet](D01_R02H_FASTENING_SERVICE.pdf)
- [Integrated FreeCAD assembly](D01_R02H_ASSEMBLY.FCStd) / [STEP](D01_R02H_ASSEMBLY.step)
- [Hardware delta BOM](HARDWARE_DELTA_BOM.csv) / [checks](checks.json)

## What changed

Eight proposed M4x80 studs replace the70 mm shaft envelopes. Four proposed M4x25 cap screws replace the20 mm ledge shaft envelopes. Added28 nut and32 metal washer shapes. The larger backing washers support the existing assumed sealing washers. Opposed fixed nuts retain each stud at the reducer; separate outer service nuts clamp the removable retainer. Actual installation torque and seal compression are UNKNOWN: tightening blindly may distort the plate or crush the filter border.

229 valid CAD objects. All checked changed-part pairs have no positive-volume collision above0.05 mm3. Native reopen and STEP volume match pass. Exact counts and preserved source SHA256 are in checks.json. This is nominal geometry, not toleranced fabrication verification.

## Dimensions and sources

Sources accessed2026-10-03; specification references only, NOT a purchased or India-stock-confirmed selection:

- [Accu HNN-M4-A4](https://www.accu.co.uk/hexagon-nylon-locking-nuts/7958-HNN-M4-A4): published7 mm across flats,5 mm overall height and0.7 mm pitch. CAD uses a simplified full-height hex envelope with nominal thread bore; no actual threads or nylon insert.
- [Accu M4x25 cap screw dimensional reference](https://www.accu.co.uk/metric-cap-head-screws/250079-SSC-M4-25-A2-R360): head7 mm diameter x4 mm high;3 mm drive. Reference coating/thread-locking treatment is NOT selected for this project. CAD omits the socket and threads.
- [Easyfix large M4 washer](https://www.screwfix.com/p/easyfix-steel-large-flat-washers-m4-x-1mm-100-pack/194ft): published12 mm outside diameter and1 mm thickness. CAD bore4.3 mm is an ASSUMPTION. Grade/coating/product availability remain unselected.

Front stud runs y=-72..8 mm. Stack: service nut -70..-65; washer -65..-64; retainer -64..-55; fixed outer nut -19..-14; washer -14..-13; seal -13..-12; reducer -12..-3; washer -3..-2; inner nut -2..3. Nominal projections2 mm and5 mm. Proposed ledge screw head -20..-16;25 mm under-head length ends at9; inner nut ends at3, leaving6 mm. Comparing these with two pitches (1.4 mm) is only a provisional geometric check, not certified locking engagement. Exact nut locking-element engagement and tolerances need verification.

## Filter replacement and checks

With power isolated and fans stopped, remove four outer service nuts and washers and then the retainer; support the filter while withdrawing it. CAD tests a200 mm outward filter translation on each side after these parts are removed. Both nominal swept volumes are clear of fixed modeled components. This does not check retainer removal motion, hand/tool access, filter deformation, adhesive sticking, dust containment or actual working space. Loose nuts/washers require collection; they are not captive. No powered access is authorized. Serviceability must be proven in a physical dry fit.

## Still open

Inherited M5 hardware/guards and joints are not completed by this revision. Seal product/compression, filter landing width, plate/bracket strength, manufacture tolerances, protected stud ends and qualified physical review remain open. Electrical protective access and manual-restart requirements remain unresolved. No leak, airflow, particle, strength or outdoor claim follows from these checks. The new filter/reducer still invalidates old pressure predictions. IKEA specifies STARKVIND-only intended use; this is experimental custom fit, not OEM endorsement.

Next release gate: complete inherited fastening/guard access protection and resolve installed filter pressure/sealing evidence; do not treat this sheet as permission to cut, buy or energize.

## Reproduce

From project root:

```powershell
& 'D:\Applications\FreeCAD 1.1.3\bin\python.exe' scripts/geometry/detail_d01_adapter_hardware.py
& 'C:\Users\G15 5530\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' scripts/reports/build_d01_hardware_report.py
```
