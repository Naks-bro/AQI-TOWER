# M02 — plate loads and connection decision

2 October 2026. PRELIMINARY SENSITIVITY CALCULATIONS — NOT PLATE SIZING OR FABRICATION APPROVAL.

## Plain-language conclusion

The segmented posts solve the CAD clash, but they are not yet connected parts. Resting one post on a plate cannot by itself resist sliding or lifting. A small average pressure number does not prove that the plate, cap, weld, gasket surface or complete frame is strong enough.

**RECOMMENDATION:** do not freeze the segmented-post branch yet. Compare a continuous frame surrounding a separately sealed inner filter housing. This could separate structural connections from the HEPA air seal without putting the primary posts through its pressure boundary. It may fit inside the decorative round casing; that fit has NOT yet been modeled. An external full-tower frame is not the only alternative.

The segmented branch remains an option if a mechanical reviewer approves its actual load-transfer joints and the plates' structural/sealing behavior. No architecture has been finally selected.

## Detected geometry and explicit load assumptions

**DETECTED:** a read-only FreeCAD extraction clips the modeled frame, M04 air-path material, HEPA retainer and (where applicable) HEPA plate above each boundary's upper face. All source hashes remain unchanged.

| Boundary | Partial CAD material above the plane, assumed steel | Plus 14 kg unselected fan candidate |
|---|---:|---:|
| HEPA plate upper face, z645 mm | 35.33 kg | 49.33 kg |
| Prefilter plate upper face, z450 mm | 59.37 kg | 73.37 kg |

**ASSUMPTIONS:** homogeneous steel density 7,850 kg/m3 and routing those listed loads through the posts. Fan mass comes from the previously archived S&P candidate catalogue; its actual mounting and CG remain unknown. The clipped subtotal does not include that boundary plate itself. It is not the full plate free-body load, a rating or complete machine weight. Loads above successive boundaries overlap: do NOT add 49.33 and 73.37 kg.

**UNKNOWN / EXCLUDED:** shell/door attachment load path, actual filter masses, clamps, mounts, joints, guards, cables/electronics, coating and other hardware. They have not been assigned zero mass. The 20 kg addition below is an arbitrary sensitivity input, NOT an estimate or maximum for all missing items.

## Four-contact sensitivity model

Assume a rigid plane on four equal-stiffness contacts at x = +/-0.350 m and y = +/-0.200 m. Use gravity 9.81 m/s2. Assume aligned 35 x 35 mm closed caps, with nominal area 1,225 mm2 each.

Weight W = mass x gravity. For contact signs sx, sy:

```text
R = W/4 + sx * My/(4a) + sy * Mx/(4b)
My = W * ex + added reaction first moment about y
Mx = W * ey + added reaction first moment about x
a = 0.350 m; b = 0.200 m
```

Here the moments describe the required first moments of vertical reactions; they are not a complete signed external-load specification. Force and first-moment equilibrium are tested. Equal stiffness, rigid load distribution and maintained contact are assumptions—not verified properties of the actual frame/plate assembly.

| Example only | Model mass | Lowest / highest post reaction | Interpretation |
|---|---:|---:|---|
| Partial HEPA subtotal, centred | 49.33 kg | 121 / 121 N | Missing loads and all lateral effects excluded |
| Partial prefilter subtotal, centred | 73.37 kg | 180 / 180 N | Separate boundary calculation, not additive weight |
| HEPA subtotal + assumed 20 kg, centred | 69.33 kg | 170 / 170 N | Sensitivity case only |
| Same mass, assumed 150 mm x 100 mm load offset | 69.33 kg | 12 / 328 N | Near twice the centred reaction at one contact |
| Same mass, assumed 200 N lateral force at z1,200 mm | 69.33 kg | 31 / 309 N | Assumed HEPA-plane moment: 111 N m |
| Same mass, assumed 300 N lateral force at z1,200 mm | 69.33 kg | -38 / 378 N | Contact-only linear model invalid: tension/restraint or a different contact distribution required |

The lateral cases use height above HEPA upper face: 1.200 - 0.645 = 0.555 m. These are NOT selected public push loads, design wind loads, safety limits or verified load combinations. They exclude actual friction, frame racking and joint behavior. No whole-tower tipping/sliding judgment follows from them.

When a reaction is negative, do not treat it as a real tensile force carried by an unbolted resting contact or continue using the four-contact compression model as valid. Actual contact can lift, redistribute or need a designed restraint; that behavior is not solved here.

## Why force divided by area is not enough

In the centred HEPA-subtotal example, 121 N / 1,225 mm2 is about 0.099 MPa nominal average compression. In the offset sensitivity example, the maximum is about 0.268 MPa. Neither is peak bearing stress or a structural approval. No material allowable, safety factor, cap bending, local hollow-section wall loading, weld capacity or plate deflection calculation is established.

For exactly aligned upper and lower caps, some axial load can transfer locally through the plate thickness. Do not automatically model the full load as a long-span plate-bending problem. Conversely, do not assume local bearing alone covers the plate's filter opening, rail loads, misalignment, shear, moment transfer or seal-plane flatness.

For equal x/y misalignment of ideal square footprints, purely projected overlap falls from 1,225 mm2 at zero offset to 1,156 at 1 mm, 1,024 at 3 mm and 900 at 5 mm. These are not tolerances to specify; real bearing depends on contact flatness, cap geometry and deformation. The CAD end closures are 3 mm assumptions, not reviewed weld/cap details.

The [Steel Tube Institute's HSS connection discussion](https://steeltubeinstitute.org/resources/axially-loaded-hss-column-base-plate-connections/) distinguishes compression transfer, plate behavior and connection requirements for shear/uplift (reviewed 2 October 2026). It concerns building column bases, NOT our filter plate. Its numerical sizing provisions are not transferred to this tower.

## Separate filter-pressure load

An assumed 500 Pa across a 593 x 593 mm gross filter face gives 175.8 N. This is a pressure-force illustration, not an operating limit or approved clamp preload. Define the actual filter/plate free body, pressure surfaces and reactions before combining this with gravity. Internal pressure forces on other enclosure surfaces may oppose it; blindly adding it to whole-device weight would be incorrect. Supplier terminal differential, gasket preload and allowable sealing-plane movement remain unknown.

## Required connection information — no guessed bolts or welds

| Review item | Input still required | Calculation/detail required |
|---|---|---|
| Loads | Actual component masses, locations/CG, fan reactions and approved load cases | Complete plate/frame free bodies and combined forces/moments |
| Plate and caps | Material grade, real geometry, support arrangement and allowable seal movement | Bearing, bending/deflection, local tube/cap behavior and buckling where applicable |
| Post/plate joints | Manufacturing process, cap detail and restraint arrangement | Shear/uplift/moment transfer, joint strength, assembly tolerance and inspectability |
| Air seal | Exact OEM filter frame/gasket and enclosure seams | Compression/flatness requirements, bypass review and installed leak testing |
| Base/floor | Actual feet/contact polygon, floor condition and anchoring permission | Whole-device/service-state stability, sliding, floor and handling checks |

**Next design action:** study a continuous support frame around an independent sealed cassette/plenum, preserving removal access; compare weight and geometric fit. In parallel, obtain the exact component and material information through the existing draft supplier/reviewer questions. No supplier message has been sent. A calculation script cannot substitute for that information or qualified review.

## Reproduction

```powershell
& 'D:\Applications\FreeCAD 1.1.3\bin\python.exe' scripts/geometry/extract_support_load_inventory.py
python scripts/analysis/plate_load_screen.py
python -m unittest discover -s scripts/analysis -p '*screen.py'
```

Outputs: `results/fan_selection/support_load_inventory.json` and `plate_load_screen.json`. Six new unit tests check centred reactions, force/moment equilibrium, contact loss, unknown-input rejection, nominal pressure units and alignment arithmetic. These tests validate calculations—not the tower's strength. Existing CAD unchanged; no FEA, CFD, fabrication, energization or physical test performed.
