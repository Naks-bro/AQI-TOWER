# M02 — weight, support and stability review

2 October 2026. PRELIMINARY SCREENING — NOT A STRUCTURAL DRAWING OR FABRICATION RELEASE.

## In simple words

The tower must not just fit together: it must carry its own weight, hold the fan and filters securely, and not fall over during use or maintenance. The current thick metal packaging study could be unnecessarily heavy. Do not order its sheet metal yet.

## What was actually checked

**DETECTED:** nine explicitly identified shapes were read from the existing R02 FreeCAD model and the separate M04 air-path study. Their solid volumes and geometric centroids were extracted. Source file hashes were checked before and after; the CAD files were not changed.

**ASSUMPTIONS:** density 7,850 kg/m3 for a steel scenario and 2,700 kg/m3 for an aluminium scenario. No alloy or grade has been selected. Existing geometry assumes a 2 mm cylindrical wall, 5 mm bulkheads/retainer and offset M04 profiles. Those thicknesses were packaging inputs, not engineering sizing. M04's profile offset is not a uniform normal sheet thickness.

| Modeled geometry only | All-steel scenario | All-aluminium scenario |
|---|---:|---:|
| Outer casing and two service-door pieces | 94.14 kg | 32.38 kg |
| Two filter bulkhead plates | 29.45 kg | 10.13 kg |
| Illustrative HEPA retainer | 3.29 kg | 1.13 kg |
| Separate transition, inlet neck and outlet study | 8.73 kg | 3.00 kg |
| **Partial material total** | **135.60 kg** | **46.64 kg** |

These are alternative material calculations on the same geometry, not two approved constructions. Independent M04 parts have not been verified against the real fan installation. A fabricated assembly may differ substantially.

**OEM INFORMATION:** the unselected S&P TD2000/315 SILENT ECOWATT candidate is listed at 14 kg in the archived [official catalogue](https://statics.solerpalau.com/media/import/documentation/EN_TD-SILENT-ECOWATT.pdf), technical table on printed page 188. Source reviewed 2 October 2026. If that candidate and all these study shapes were used unchanged in steel, their combined subtotal would be about 149.6 kg—still not the complete machine.

**UNKNOWN:** total machine weight and centre of gravity. Actual filters, structural frame/base, mounts, guards, louvres, hinges, fasteners, seals and electrical equipment are missing from the mass calculation. Fan centre of gravity is unknown. The partial homogeneous-material centroid at z = 1,074 mm is NOT the whole tower's centre of gravity.

Full-solid fan/filter/base/electrical allowance boxes were deliberately excluded. They represent occupied space, not solid blocks of metal. Gasket mass is also excluded until its real material/profile is known.

## Recommended load path

This is a support concept, not a dimensioned frame or connection design:

```text
Fan -> OEM-approved cradle/mounts ------+
HEPA -> cassette seat/support ring ----+-> independent frame -> base -> actual floor supports
Prefilter -> cassette support ---------+
Casing and doors -> frame attachments -+

Filter pressure -> seat + removable retainer -> frame
Outdoor lateral load -> casing attachments -> frame -> reviewed anchors/foundation
```

**RECOMMENDATION:** compare an independently supported frame with a lighter casing, rather than making the casing carry the fan. Consider steel-frame/lightweight-cladding and revised formed/stiffened plate options with a mechanical mentor and fabricator. Do not infer that aluminium of the same thickness has equivalent stiffness, joint strength, corrosion behavior or outdoor durability. No reduced gauge, tube size, bolt size, weld size or anchor is approved here.

The base in R02 is only a space reservation. It must not be manufactured as a solid metal disk. Actual feet/castors and their contact positions define stability; the 1,050 mm base-envelope diameter does not establish the support polygon. Do not substitute a wheel lock for an assessed anti-tip arrangement.

## Loads the reviewer must close

| Load/interface | Current evidence | Required input/check |
|---|---|---|
| Casing and bulkheads | Partial geometric masses above | Selected materials, stiffening, openings, fabrication tolerances and attachment loads |
| Fan support | Candidate catalogue 14 kg; position is an envelope | Exact fan/mount drawing, permitted orientation, actual CG, vibration/start/stop reactions |
| Filter support | Actual masses UNKNOWN | Dry/loaded masses, supplier frame drawing, removable cassette/tray mass |
| HEPA retainer and seat | Example: 500 Pa x 0.593² m2 = 175.8 N gross-face force | Actual allowable differential, effective area, load directions, gasket compression, clamp distribution and plate deflection |
| Service condition | Filter lifted and pulled sideways in CAD | Door-open/filter-removed cases, extended tray position, operator handling and lifting plan |
| Floor and base | Contact geometry UNKNOWN | Actual support polygon, floor capacity/friction/slope, anchoring permission and transport method |
| Outdoor enclosure | Site UNKNOWN | Site-specific wind and other applicable loads, weather panels, public interaction, anchoring/foundation review |

The 500 Pa force example is not an approved operating differential or clamp preload. Gasket preload and fan dynamics cannot be obtained from that single force calculation.

## Why a wide-looking base does not prove safety

For a simplified static lateral load:

- Restoring moment = mass x 9.81 x distance from the weight's vertical projection to the tipping edge.
- Overturning moment = lateral force x load height.

For an **unrelated example only**, 100 kg and a 0.4 m support-edge distance give 392.4 N m restoring moment; a 200 N push at 1.5 m gives 300 N m overturning moment. This is not a PASS: the example has no approved factors, sliding check, connection assessment, real support polygon or actual tower CG. Unknown inputs are rejected by the calculator, not silently replaced with zero.

Illustrative uniform wind on a 0.954 m x 2.215 m cylinder silhouette, with assumed air density 1.2 kg/m3 and drag coefficient 1.2:

| Example wind speed, NOT design wind | Lateral force | Moment at half height |
|---|---:|---:|
| 10 m/s | 152 N | 168 N m |
| 20 m/s | 609 N | 674 N m |
| 30 m/s | 1,369 N | 1,516 N m |

Formula: force = 0.5 x density x speed² x assumed drag coefficient x projected area. These examples only show how quickly loads grow. They omit actual site gust criteria, terrain, shape/opening effects, dynamics and applicable load combinations/factors. They do not specify anchors or an allowable wind speed. Making the housing lighter also reduces unanchored restoring weight; reassess the entire support system.

Wind assessment involves speed and aerodynamic pressure coefficients, among other issues, as discussed in [NIST Technical Note 1738](https://www.nist.gov/publications/assessment-methods-determining-wind-loads-nist-tn-1738) (reviewed 2 October 2026). This general reference is not an Indian site-design approval or a substitute for a qualified reviewer applying the relevant requirements.

## Reproduce and inspect

From the repository root in PowerShell:

```powershell
& 'D:\Applications\FreeCAD 1.1.3\bin\python.exe' scripts/geometry/extract_material_inventory.py
python scripts/analysis/mass_stability_screen.py
python -m unittest discover -s scripts/analysis -p '*screen.py'
```

- `results/fan_selection/material_inventory.json`: source hashes, actual shape volumes and geometric centroids.
- `results/fan_selection/material_mass_screen.csv`: individual part mass sensitivities.
- `results/fan_selection/mass_stability_screen.json`: partial totals, explicit unknowns and example moments.

**Next release gate:** obtain actual component masses/mounting drawings; choose a frame/cladding approach with the reviewer; create dimensioned M02 frame/base/support drawings and complete whole-device mass/CG, service-state stability, member/joint, floor and handling assessments. Outdoor release additionally requires the actual site and anchoring/weather review. No fabrication, electrical energization or outdoor operating approval is given by this sheet.
