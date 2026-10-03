# Package 1 — mechanical / D01 R03M

03 October 2026. **One mechanical design-review package. NOT a fabrication, safety or energization release.** Physical prototypes:0. Indoor experimental use only.

## Open these

- [Mechanical package PDF](AQI_D01_MECHANICAL_PACKAGE.pdf): assembly, exploded view, guard fabrication/joint route, fasteners, seals, support/stability, assembly sequence, release holds and10 current panel drawings.
- [Assembly CAD](D01_R03M_ASSEMBLY.FCStd), [STEP](D01_R03M_ASSEMBLY.step), [exploded native CAD](D01_R03M_EXPLODED.FCStd).
- [One mechanical ZIP](AQI_D01_MECHANICAL_PACKAGE.zip): current authored files with hashes; OEM source PDFs are not redistributed.
- [Fastener schedule](FASTENER_SCHEDULE.csv), [all modeled objects](CAD_PART_INVENTORY.csv), [guard blanks](GUARD_BLANKS.csv).
- [Assembly checks](checks.json), [service checks](service_checks.json), [mechanical arithmetic](mechanical_screen.json), [panel geometry](current_panels.json).

## Work completed in this batch

Same saved R02G cabinet/filter architecture, revised once as R03M; original R02G hash preserved. The model now includes proposed complete fan/cabinet through-bolt stacks, shorter M5 reducer rods and their nuts/washers, positive foot fixings and seal compression-limit sleeves/spacers. Two fabricated guard subassemblies replace the disconnected-sheet/rivet concept while retaining the independent four-bolt mounting of each guard. This is a proposed welded fabrication route, not an approved welding procedure.

493 valid CAD objects;119,805 pair checks clear with ONLY reservation pairs excluded. Both guards fuse into single nominal solids, so earlier guard-seam collision exclusions are no longer needed in the generator audit. Native reopen/STEP validity and volume checks pass. The separate panel-extraction audit excludes the one guard-to-guard pair by its legacy generic rule and therefore reports119,804; the generator explicitly checks that pair. Both200 mm filter withdrawal sweeps pass after retainer and service hardware removal. These are geometry checks, not safety tests.

A trial25 mm top wood screw crossed the M5 rod at the upper corner. Corrected to proposed20 mm top screws; base remains25 mm. Source pilot/core geometry is not full wood-screw thread geometry. End-grain withdrawal capacity and the10 mm nominal top penetration remain unverified; do not lift by the lid.

## Current mechanical dimensions and hardware

- Fan:16 proposed M4x50 screws with32 large washers and16 locknut envelopes;6 mm nominal thread projection. Head/washer stack clears the modeled cage; actual fan mounting corners and bearing loads need verification.
- Cabinet:32 proposed M4x40 through screws,64 washers and32 nuts;4 mm nominal projection. Real panel/cleat grades, bearing and preload remain unknown.
- Reducers:12 M5x60 side rods and4 M5x40 centre rods replace the earlier long projections.32 M5 nuts and32 large washers added. Front tip y=-21; inner ends39 or19 mm. Top centre inner end is only1 mm nominal from the guard-front plane: no tolerance or wrench-access approval. Assemble these nuts before the fan plate/inner guard.
- Seal stops:16 OD10/ID5.5 x3 mm outer spacers;8 OD6.5/ID4.5 x36 mm inner sleeves. These set the current assumed installed gaps only. They must NOT be manufactured unchanged if actual filter/gasket dimensions differ.
- Feet:4 proposed30x30x20 blocks with4.5 through bore and12 diameter x9 underside recess. Four M4x30 screws,8 washers and4 nuts; screw heads recessed4 mm above floor. Foot material, friction, bearing and tear capacity unselected.
- Retained R02H adapter hardware and R02G independent guard bolts remain, except guard rivets are superseded by the proposed fabricated joint route. Full object inventory prevents accidentally ordering both historical and replacement hardware.

Service hardware and inner stop sleeves are not captive; collect/support them during removal. Captive-retention risk remains a review hold. Fastener schedule includes both retained and replaced stacks; quantities are proposals, not an authorized order.

M4 washer12OD x1 uses assumed4.3 bore; M5 washer15OD x1.2 and5.3 bore follows a published dimensional reference. Nuts modeled as7AFx5 forM4 and8AFx5 forM5. Thread profiles, nylon inserts, real sockets, weld beads and manufacturing variation are omitted. No torque or material grade is released.

## Guard fabrication and pattern

PROPOSAL: steel sheet faces/skirts with welded corners, face perimeter and mounting-angle laps. W1=face perimeter; W2=four vertical corner joints; W3=each angle lap joined on its two short edges and upper edge. Continuous joint locations are defined; weld size, process, sequence, distortion control, inspection acceptance and strength must be set by a qualified thin-sheet fabrication review. Do not infer those from a fused CAD solid.

Face blanks320x320x1, quantity2. Outer side blanks320x50x1 quantity2, ends318x50x1 quantity2. Inner sides320x40x1 quantity2 and ends318x40x1 quantity2: start at z531 above the1 mm bottom face; the earlier41 mm sheet envelopes overlapped that face by1 mm. Independent mounting angles remain20x20x2 nominal by40 long; actual root geometry/weld clearances unverified. Old rivet holes are omitted in new blanks, not plugged in old parts.

Proposed4 mm holes on6 mm staggered pitch with at least10 mm solid border are now provided in a review-only face DXF. Exact count and open area are in guard_pattern.json. This is not a perforated3D model or finger-protection approval. The earlier40% active-area pressure assumption must be updated to this exact pattern if adopted; the actual loss coefficient still needs evidence. No guard-strength or deflection result exists.

The generated face has2822 holes and0.0354623 m2 hole area, slightly below the previous0.036 m2 assumption. At unchanged flow and loss coefficient, the guard loss scales by the squared area ratio recorded in guard_pattern.json. Hole containment within the solid border is asserted; this does not establish a safe opening/strength criterion.

## Sealing and stability findings

Outer gasket remains495.3/475.3 square x3 installed; filter gasket370x290 outside/350x270 inside x3 installed. Actual material/free thickness/force and filter border remain unknown. A hypothetical39/40/41 mm filter in the fixed43 mm nominal gap gives0/25/50% compression for an assumed4 mm free gasket. This is why nominal stops are not a seal release. Seal all new penetrations and cabinet seams using compatible verified products; ordinary metal washers are not air seals.

The mass script assumes panel650, cleat600 and metal7850 kg/m3. The approximately12.19 kg subtotal excludes fans, filters, feet, seals and controls and overstates guard-sheet mass because holes are not in3D. It is neither total mass nor a safe handling rating. Illustrative whole-mass tipping cases assume centred CG and level feet, without safety factors, friction, impact or cable pull. A15 kg example balances a front/back top push at about38.5 N; do not present it as an actual push rating. Full stability and handling approval remain open.

## Assembly / inspection holds

The PDF gives a single assembly sequence. Before any cutting, the following holds remain:

1. **M1 materials/joints:** actual grades, wood bearing/withdrawal, plate and retainer bending, bracket/weld capacity and guard deflection. Fabricator/reviewer must approve a real joining process; ability to weld is not structural approval.
2. **M2 seals/fit:** filter landing/thickness/mass and gasket force/compression, final stop lengths and penetration sealing; inspect dry fit and then measure leakage.
3. **M3 access/stability:** tool/hand/guard probe checks, fastening retention, real whole-device mass/CG, tipping/sliding and safe handling. Filter sweep checks do not cover all hands/tools or retainer removal.

**Package2 interface:** exterior control box/cable corridor remain reservations. Exact enclosure, mounting, glands and strain relief depend on the selected protective electrical arrangement. No wiring/energizing approval is included here. Guarded access, isolation and manual restart are not waived. No college lab or optional friend is assumed for qualified physical work.

The first mechanical preparation batch is delivered; engineering release remains conditional on these exact inputs and physical checks. Do not call the design fully finished or claim a physical prototype. No purchase, install, supplier contact or public publication occurred.

## Sources

Accessed03 October2026. References are dimensional evidence, not procurement selections or confirmed India stock:

- [Accu M5 nylon-insert nut](https://www.accu.co.uk/hexagon-nylon-locking-nuts/7947-HNN-M5-A2):8 mm AF,5 mm height,0.8 mm pitch.
- [Belmetric WFE5X15SS drawing](https://belmetric.com/content/A-PDF_Drawings/WFE5X15SS.pdf):5.3 bore,15 OD,1.2 thickness. Manufacturer PDF not bundled; no licence to redistribute inferred.
- [Accu M4 nut](https://www.accu.co.uk/hexagon-nylon-locking-nuts/7958-HNN-M4-A4) and [cap-screw dimensional reference](https://www.accu.co.uk/metric-cap-head-screws/250243-SSC-M4-20-A4-R360): used for nominal head/nut envelopes, not coating/material selection.
- [ARCTIC P14 Max official drawings](https://support.arctic.de/p14-max) and [IKEA filter](https://www.ikea.com/in/en/p/starkvind-filter-for-particle-removal-10463330/): retained envelope references. IKEA intended use is STARKVIND only; custom filter fit is experimental, not endorsed and not a HEPA/MERV assembly claim.

The aqi-build-review skill required full assembly checks, source preservation, real-versus-assumed labels and explicit mechanical/electrical release boundaries.

## Reproduce in order, not concurrently

FreeCAD holds native files while open; finish the generator before read-only extraction/checks.

```powershell
& 'D:\Applications\FreeCAD 1.1.3\bin\python.exe' scripts/geometry/build_d01_mechanical_package.py
& 'D:\Applications\FreeCAD 1.1.3\bin\python.exe' scripts/geometry/audit_d01_current.py --source-dir reports/prototype_d01/mechanical_package --output-dir reports/prototype_d01/mechanical_package --cad-file D01_R03M_ASSEMBLY.FCStd
& 'D:\Applications\FreeCAD 1.1.3\bin\python.exe' scripts/geometry/check_d01_mechanical_service.py
& 'C:\Users\G15 5530\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' scripts/analysis/d01_mechanical_screen.py
& 'C:\Users\G15 5530\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' scripts/reports/build_d01_mechanical_report.py
```
