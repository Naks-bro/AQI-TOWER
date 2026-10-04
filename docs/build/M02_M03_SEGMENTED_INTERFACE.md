# M02/M03 — segmented support / sealed-boundary fit branch

2 October 2026. OPTION STUDY — NOT APPROVED FOR FABRICATION OR OPERATION.

## In simple language

Instead of running one hollow post through the filter plates, this branch stops the post at each plate and starts another closed-ended section above it. The plates have no new post holes. This removes the earlier solid overlaps and avoids modeling an open post bore straight through the HEPA boundary.

The plates now become part of the load path. That is a trade-off, not a completed structural solution. Their thickness, stiffness and connections are not approved. Keep the earlier continuous-frame study for comparison; this branch is not a final architecture selection.

See the [interface illustration](M02_M03_SEGMENTED_INTERFACE.html).

## Evidence from the executed CAD checks

**DETECTED:**

- 28 valid frame-route solids: twelve capped upright segments plus sixteen horizontal rails.
- Zero positive-volume clashes with the thirteen checked R02/M04 reference objects; zero route-to-route clashes.
- Zero frame clashes with the previous assumed lifted HEPA service sweep. This is not an operator handling assessment.
- Sixteen calculated post-cap/plate face contacts, each 1,225 mm2, at z445, 450, 640 and 645 mm. Contact area is geometry, not joint strength.
- Separate frame FreeCAD/STEP and combined 41-solid snapshot FreeCAD/STEP reopened/reimported successfully.
- SHA256 checks confirm the R02 casing/cassette CAD and M04 air-path CAD were not changed.

**ASSUMPTIONS:** profile outer size 35 mm, wall/end closure 3 mm; same post x/y centres and rail levels as the previous study. Upright intervals are z150–445, z450–640 and z645–2,050 mm. The two existing plates occupy z445–450 and z640–645 mm. These are study coordinates, not toleranced manufacture dimensions. Nominal zero-gap face contact is not a practical joint or assembly clearance specification.

Using assumed steel density 7,850 kg/m3, the segmented routes weigh **48.10 kg**, compared with 47.75 kg for the earlier continuous routes. This is a replacement frame option, not an additional frame to add to it. It excludes base, feet, joints, gussets, mounting hardware and coating. Weight optimization remains unfinished.

**UNKNOWN:** assembled leakage, actual weld quality, plate/load capacity, approved material/profile, fan cradle, real OEM installation fit, total mass/CG and base stability.

## What is resolved, and what is not

| Issue | This branch does | Still required |
|---|---|---|
| Eight post/plate CAD clashes | Stops each post at existing plate faces; no overlap in tested geometry | Dimensioned joints, stack tolerance and manufacturing review |
| Open vertical bore crossing HEPA plate | Models ideal solid end closures on every upright segment and leaves plate unperforated at posts | Review real welded/closed joint details and leak-test the assembled boundary |
| Filter removal | Preserves assumed filter-envelope sweep clearance | Actual filter/retainer handling, tray/latches and OEM tolerances |
| Structural load path | Routes upper loads through post caps, plates and lower segments | Bearing, bending, deflection/flatness, buckling and joint-load calculations |
| Fan support | Keeps the candidate envelope and lower rail route | Actual mounting feet/holes, allowed orientation, vibration isolation and cradle |

Horizontal rails still have modeled open ends; there is no declared airtight welded frame assembly. The caps represent ideal geometry, not a weld/cap fabrication detail. No fastener holes have been drawn through the plates. Future holes, threads, seams, pressure taps and cable passages must be reviewed as potential leaks; added cuts require repeat fit and seal checks.

The HEPA seat/gasket/retainer are still illustrative R01 geometry, not supplier-approved hardware. The bulkhead-to-casing perimeter joint and service-door seams are also unvalidated. Removing one potential post bypass does not establish whole-device HEPA performance. The prior [Camfil commercial housing example](https://www.camfil.com/en-ca/products/housings-frames--louvers/ducted-housing/glidepack) distinguishes filter-to-track sealing from housing integrity; it was reviewed in the preceding step on 2 October 2026, but the current refetch timed out. It is not approval of this branch.

## Load-transfer review before committing to this route

Follow-on [plate load/connection sensitivity](M02_PLATE_LOAD_REVIEW.md) now calculates partial above-plane masses and illustrative reactions. It does not approve the plates. Resting contact cannot establish shear/uplift restraint; compare a separately sealed housing with a continuous surrounding frame before freezing this option.

The reviewer must assess vertical loads, fan vibration, lateral loads and uplift/retention separately. Face-to-face contact does not restrain tension, sliding or lateral motion. No plate penetration or bolt size is authorized here.

1. Obtain exact fan/filter masses, CG/mounting drawings and permitted orientation.
2. Evaluate load transfer through each plate, including local bearing, plate bending, seal-plane deflection and the interruptions caused by the filter opening.
3. Decide whether reviewed segmented connections can retain alignment/sealing, or an external frame with a separate sealed housing is preferable.
4. Design base, actual floor contacts, joints and handling arrangements; calculate full mass/CG and service-state tipping/sliding.
5. Complete assembly drawings, structural review and installed leak-test plan before fabrication release.

No plate size, frame section, welding process, mains wiring or anchor is approved by this fit study. An indoor-first build remains the recommendation; outdoor design and cleaning-zone claims need separate evidence.

## Files and repeatability

- `cad/parametric/frame_route_m02_segmented.json`: branch inputs.
- `cad/packaging/AQI_M02_Segmented_Frame_STUDY.FCStd`: standalone frame snapshot.
- `cad/packaging/AQI_M02_Segmented_Frame_NOT_FOR_FABRICATION.step`: frame exchange geometry.
- `cad/packaging/AQI_M02_M03_Integrated_Fit_STUDY.FCStd`: casing/doors, filter/gasket/retainer envelopes, fan bounding box, M04 and frame snapshots together.
- `cad/packaging/AQI_M02_M03_Integrated_NOT_FOR_FABRICATION.step`: combined exchange geometry.
- `cad/packaging/M02_SEGMENTED_FRAME_AUDIT.json`: fit/contact/mass/roundtrip evidence.

The combined snapshot excludes base/electrical allowances, guards, exact OEM hardware and actual joint details. It is not a complete manufacturing assembly. Its shape snapshots are not spreadsheet-parametric; change JSON and regenerate. Save manual edits elsewhere first: regeneration replaces only the derived branch outputs. Default generator operation still creates the earlier continuous routing study.

```powershell
& 'D:\Applications\FreeCAD 1.1.3\bin\python.exe' scripts/geometry/create_frame_route_study.py --config cad/parametric/frame_route_m02_segmented.json
python -m unittest discover -s scripts/analysis -p 'test_segmented_frame_audit.py'
```

No supplier messages, purchases, CFD runs or physical tests were performed.
