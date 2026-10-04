# D01 R01 construction details

R01 continues the same D01 assembly. **Design review only; not released for fabrication, procurement or energizing.** R00 is preserved as historical evidence. Physical prototypes built: 0.

Start with `D01_R01_CONSTRUCTION_DETAILS.pdf` (five visually inspected drawing sheets). The updated native CAD is `D01_R01_ASSEMBLY.FCStd`; the neutral export is `D01_R01_ASSEMBLY.step`. The illustration comes from this CAD, not an AI concept image.

`BOM_R01.csv` consolidates the original product references and new hardware; `FASTENERS_R01.csv` gives locations and proposed sizes. The R01 ZIP includes these files and the R00 base needed to reproduce the revision. Do not treat the R00 report included for context as the latest cutting or pressure basis.

## Completed in R01

- Eight guard mounting angles with rivet holes, four shared guard bolts, washer/nut envelopes and corresponding holes through the fan plate. Actual rivets remain unselected/unmodeled.
- Thirty-two proposed M4 cabinet through-joints with matching holes in panels and cleats; eight top/base timber-fixing locations.
- Eight filter-shelf support angles with corresponding seat/ledge holes and proposed screw shafts. Flush head/countersink details await actual screws.
- Eleven revised panel-outline/drilling DXFs, replacing the R00 cutting geometry for review. Four separate shelf drawings avoid assuming front/rear/left/right hole patterns are identical.
- An external cable-routing reservation. **It is not a drilled gland hole or wiring release.**
- Revised guard resistance calculation: 10 mm solid border leaves a 300 x300 mm perforated field. At assumed40% field porosity, free area is0.036 m2 per face, versus0.04096 m2 in R00. Calculated low/middle/loaded flows are359.2 /337.1 /297.5 m3/h. These are unmeasured scenarios, not a guaranteed range or CADR.
- Conditional bracket-load arithmetic, explicitly without a material allowable or structural PASS. Do not treat its illustrative50N/2kg cases as a safety standard or validated design load.

The `aqi-build-review` procedure required the changed guard geometry to feed back into pressure screening, rather than silently retaining the higher R00 estimates.

## Checks and exclusions

`checks.json` records163 valid modeled objects,12,675 nominal pair checks with no positive-volume clashes, native reopen and STEP volume checks. R00's native assembly SHA256 is recorded and remains unchanged. `pressure_results.json` contains nine arithmetic checks; `load_screening.json` adds five checks. Nominal clearance does not establish tolerance or strength.

Excluded: cable/control reservation envelopes, inherited guard-to-guard seams, actual perforation geometry, screw threads, several heads/washers/nuts, extrusion bend fillets and rivet heads. Perforations in the rendered image are a visual annotation of the proposed pattern. Wood screw cores/pilots are layout envelopes, not verified thread engagement.

The full R00 product evidence and limitations remain in `../README.md`. No new OEM suitability, stock, price or licence claims were established this turn. No external party contacted, no software installed and no purchase made.

## Construction boundary

The new attachment geometry is prepared; these specific items remain open:

1. Exact fan/filter availability and revision, filter resistance curve and real frame/seal landing.
2. Angle and guard material/grade, bend fillets, cage seam method, rivet grip, final fastener products, joint bearing/pull-out, guard reach/deflection, mass/centre of gravity and stability.
3. Timber screw type/pilot and holding capacity, top-seam tape/product, permanent sealant and physical leakage checks. Carry from the base, not the unqualified lid or clamping frames.
4. Selected flush shelf-head geometry, remaining plywood thickness and flat filter seating; do not blindly countersink from a generic hole drawing.
5. Actual cable gland/entry that maintains guard protection, restraint and extension lengths, enclosure mounting, startup current and electrical commissioning.
6. Rated restart prevention remains missing. R01 does not implement or waive the existing manual-restart/interlock requirement. No unattended use or energization release.

Shared guard bolts require supporting both guards while dismantling, with power unplugged and rotation stopped. Actual joint/safety review may require separate retained guard attachments; no independent-access safety function is claimed.

## Reproduce

Run from project root using existing runtimes:

```powershell
& 'D:\Applications\FreeCAD 1.1.3\bin\python.exe' scripts/geometry/detail_d01_r01.py
& 'C:\Users\G15 5530\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' scripts/analysis/d01_r01_checks.py
& 'C:\Users\G15 5530\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' scripts/reports/build_d01_r01.py
```

R01 imports the saved R00 native assembly. Do not overwrite that base with another design. R01 currently uses explicit construction coordinates; it is reproducible geometry, not a fully constrained parametric production model.
