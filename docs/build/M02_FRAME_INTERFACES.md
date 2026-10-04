# M02 frame routing and mounting interfaces

2 October 2026. SPATIAL STUDY ONLY — NOT FOR FABRICATION.

## What we now have

Follow-on option: [M02/M03 segmented capped-post branch](M02_M03_SEGMENTED_INTERFACE.md) removes the eight nominal clashes without cutting the plates, but changes load transfer. This document records the earlier continuous-post study; it is preserved for comparison.

A separate 3D frame-routing study shows where four upright supports and four levels of connecting rails could fit. It does not alter R02 or the M04 air-path CAD. Read the [visual layout](M02_FRAME_LAYOUT.html) alongside the [weight/stability review](M02_WEIGHT_STABILITY.md).

**DETECTED:** twenty valid hollow-profile solids, native FreeCAD reopen and STEP reimport passed. Thirteen existing reference objects were checked for positive-volume interference. No nominal interference was found with the shell, service-door pieces, filter envelopes, gasket/retainer envelopes, fan bounding box or M04 air-path study. No route-to-route positive-volume clashes occurred. The assumed lifted HEPA sweep also cleared the frame.

**ASSUMPTIONS:** upright centres x = +/-350 mm, y = +/-200 mm; start/end z = 150/2,050 mm. A 35 mm square profile with 3 mm wall was used ONLY to give the routing a visible volume. Neither those dimensions nor the material is selected. Rail top levels are 185, 445, 640 and 1,190 mm. Frame envelope is 735 x 435 mm; nominal clearance from the 593 mm filter side to the posts is 36 mm. Real assembly/tool/handling tolerances remain unassessed.

The assumed steel routes alone weigh **47.75 kg**, excluding base, feet, joints, gussets and actual mounts. This does not solve the weight problem merely by adding an independent frame. Compare revised section sizes/topologies and lighter cladding with the reviewer; do not purchase this profile from the study.

## Important fit failure — not hidden

**DETECTED:** each of the four continuous posts intersects each of the two existing filter bulkhead plates: eight clashes, each 1,920 mm3 of solid overlap. The routing model therefore CANNOT be assembled with the current unmodified plates. Those plates remain unchanged.

Do not just drill square clearance holes and call it finished. The HEPA plate separates dirty air from clean air. Gaps around posts could bypass the HEPA. A hollow post can also communicate between dirty and clean zones through open ends or unsealed joints, even if its outside perimeter looks sealed. None of these interfaces is modeled as leak-tight or tested.

**RECOMMENDATION:** compare these routes before freezing M02/M03 together:

| Route | Advantage to investigate | Unresolved issue |
|---|---|---|
| Continuous internal posts | Direct support path and compact casing | Plate penetrations AND hollow-post air paths need a reviewed sealing solution; intake/free-area effects remain unmeasured |
| External frame supporting sealed enclosure | Could keep primary members outside the pressure boundary | Larger footprint, appearance, door access and mounting arrangement change; not modeled here |
| Segmented supports joined at a sealed structural boundary | Could avoid an open tube across the HEPA boundary | Boundary must transfer structural loads and retain flatness/sealing; connection design not complete |

Camfil's [GlidePack housing information](https://www.camfil.com/en-ca/products/housings-frames--louvers/ducted-housing/glidepack) distinguishes filter-to-track sealing from housing pressure-boundary integrity in its commercial assembly (reviewed 2 October 2026). It is a useful interface example, not certification of our cassette, posts or frame. The exact filter's installation instructions remain necessary.

## Frame/base and mounting interface register

| ID | What connects | Geometry currently available | Before this can be released |
|---|---|---|---|
| M02-01 | Uprights to base | Four assumed routes; base only a reserved volume in R02 | Choose actual base/feet/contact polygon, joint detail, floor/handling loads and corrosion arrangement |
| M02-02 | Prefilter tray to frame | Rail top z445; old plate intersects posts | Actual filter mass/frame/ledge, tray clearance, seals, loaded differential and removal method |
| M02-03 | HEPA seat/retainer to frame | Rail top z640; illustrative R01 seat and gasket | Resolve penetrations, gasket preload/flatness, filter orientation, supports and bypass integrity |
| M02-04 | Fan to frame | Rail top z1190; candidate bounding envelope | OEM mounting holes/feet, permitted upright orientation, load/CG, vibration isolation and removal access |
| M02-05 | Casing/doors to frame | Casing and door volumes clear nominally | Attachments, seams, latches/hinges, corrosion and filter-service access; no live/spinning-part exposure |
| M02-06 | Outlet and guards to frame | Separate M04 study clears routes | Real fan port axes/flanges, adapter attachments, guard geometry/losses and service support |
| M02-07 | Electrical enclosure to frame | Not included in this routing fit check | Locate actual enclosure, confirm access/cooling/cables and qualified bonding/protection design |

Do not bolt through a fan casing, clamp a filter media pack, or use the airflow adapter as the fan's support without component-specific approval. The current rails do not constitute a fan cradle. Base/feet, lifting points, wheels, fasteners and structural load ratings are still UNKNOWN.

## What the checks do NOT establish

No member stress/deflection/buckling analysis, vibration assessment, weld/bolt/anchor sizing, complete mass/CG, actual tipping/sliding approval, seal integrity, guard accessibility or outdoor weather performance. Touching surfaces are not proven joints. A geometric service sweep is not a safe lifting/removal procedure. Exact OEM fan service envelope and true filter frame/gasket are unavailable. Positive-volume clearance does not establish acceptable airflow obstruction or installation effect.

## Files and reproduction

- `cad/parametric/frame_route_m02.json`: explicit routing assumptions.
- `scripts/geometry/create_frame_route_study.py`: standalone study generator; preserves earlier CAD.
- `cad/packaging/AQI_M02_Frame_Routing_STUDY.FCStd`: editable shape snapshots, not spreadsheet-parametric members. Edit the JSON and regenerate for dimensional changes.
- `cad/packaging/AQI_M02_Frame_Routing_NOT_FOR_FABRICATION.step`: exchange geometry.
- `cad/packaging/M02_FRAME_ROUTING_AUDIT.json`: valid solids, reference clashes, assumed removal sweep, mass and clearances.

```powershell
& 'D:\Applications\FreeCAD 1.1.3\bin\python.exe' scripts/geometry/create_frame_route_study.py
```

Regeneration replaces these derived study outputs; preserve manual edits before running it. It does not replace R02 or M04 files.

**Next release gate:** obtain OEM filter/fan mounting information, select the frame-to-sealed-cassette architecture with the mechanical reviewer, then produce integrated assembly CAD and dimensioned frame/base/connection drawings. Resolve all eight plate clashes and every potential HEPA bypass path before fabrication. No parts ordered or supplier messages sent.
