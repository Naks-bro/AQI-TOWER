# D01 indoor demonstrator engineering package

**Latest continuation: [R01 attachment and construction details](r01/README.md).** Updated assembly, guard/cabinet/shelf fastenings, eleven revised drilling DXFs and reduced airflow screening for the guard's solid rim. R00 below is preserved; its hole drawings and airflow numbers must not be mixed with R01.

3 October 2026. R00 is a **design-review deliverable, not a fabrication, procurement or energization release**. Physical prototypes built: **0**.

Open **AQI_D01_ENGINEERING_PACKAGE.pdf** first. The first two pages explain the proposal to stakeholders; the remaining pages show the actual assembly, drawings, pressure budget, electrical connection plan, BOM and physical test procedure.

## Recommended route

Build a custom low-voltage indoor particle demonstrator before committing to the large cylindrical tower. Two opposed MERV13 filters and four top-mounted PC fans share a sealed, serviceable panel enclosure. Our work is the mechanical integration, seals, control integration, measurements and validation; it is not an off-the-shelf purifier or a claim of inventing PC-fan filtration.

This is a **recommended reduction in first-demonstrator scope**, not evidence that the larger HEPA tower is ready or that the user has approved procurement. MERV13 is not HEPA. No gas, biochar, water, solar or outdoor cleaning claim is made. The previous full-size tower route is retained, not silently replaced or released.

## Delivered files

- `D01_ASSEMBLY.FCStd` and `D01_EXPLODED.FCStd`: same assembly in native FreeCAD, 73 objects. Regenerated solid features; not a fully constrained production feature tree.
- `D01_ASSEMBLY.step`: vendor-neutral assembly geometry.
- `D01_ASSEMBLY.png` and `D01_EXPLODED.png`: renders from that CAD tessellation. Pleat markings and perforations are visual annotations; CAD filters and guard faces are envelopes. No AI concept rendering or physical photograph.
- `panel_dxf_REVIEW_ONLY/`: eight 1:1 millimetre panel/guard-outline files. No kerf compensation, guard perforation holes, unmodeled screw schedules or attachment flanges. **Do not send directly to a cutter.**
- `panel_geometry.json`: dimension and hole-coordinate data matching the generated panels.
- `D01_BOM.csv`: exact OEM reference products separated from proposed/unresolved hardware and services. No guessed prices or stock claims.
- `pressure_results.json` and `pressure_curves.csv`: reproducible screening and nine arithmetic checks; not physical results.
- `geometry_checks.json`: 435 panel/filter/support pair checks and 1,280 hardware-to-part checks; zero checked positive-volume clashes. Nuts/washers, guard-to-guard overlaps and control reservation excluded; no strength approval.

## What is fixed in this proposal

- Cabinet 550 wide x360 deep, top at580 above floor. Top guard raises height to631. Filter/retainer depth472.90 excluding studs; stud envelope reaches490. External control reservation raises width to590. No outdoor weatherproofing.
- OEM reference filter 495.3 square x44.45 deep. Sealed470 square seat aperture. Retainer550 square with475 aperture and eight5.5 clearance holes per face; minimum retainer hole centre-to-edge20. Seat edge centres minimum11; check plywood bearing and reinforcement with reviewer.
- Two235 x47.45 x9 ledges per filter, separated by20 to clear the bottom centre stud. Filter support does not rely only on gasket friction.
- Side studs: twelve M5x100; centre studs: four M5x80. Sixteen proposed M4x50 fan bolts. These lengths require delivered stack/washer/nut and thread-engagement checks; fasteners are not strength-released.
- Four P14 Max140 square x27 fans;125 mounting pitch and134.2 fan aperture from OEM drawing/template. Native fan rotors are simplified proxies.
- The Noctua NV-PS1 / included NA-AC10 / NA-FC1 / NA-FH1 chain is an OEM-documented combination, with third-party fan compatibility still to check. Four fans nominally1.4A/16.8W versus supply2A/24W; startup and auxiliary loads unmeasured.

## What was actually learned

Existing CAD/CFD and measurement scripts are reusable evidence and tools, but not one released physical machine. The full-size fan does not satisfy every assumed loaded duty point. Repeated outer-casing and closure branches advanced packaging but did not resolve component procurement or electrical release.

D01 trades HEPA and full-size flow for much simpler integration. Screening intersections are376.7,352.1 and308.7m3/h for **assumed** filter-resistance scenarios. They are not a guaranteed interval. The exact S&P filter pressure curve was not obtained; fan curve values are visually digitized. Two filters in parallel each carry half the flow; four parallel fan pressures do not add.

During this turn, review found and corrected narrow retainer ligaments, side-stud length, central-stud/inner-guard interference and lower-stud/shelf interference. Nominal clearance is not the same as a tolerance, load, seal or safety pass.

## Remaining work, specific to this assembly

1. **Obtainable parts:** resolve the P14 Max SKU/revision conflict (current PDF versus older drawing/store identity), stock and delivered manual. Checked Indian listings were out of stock. Confirm a traceable MERV13 filter with matching actual dimensions and pressure curve. India availability of S&P 990303 and the Noctua chain is UNKNOWN. A substitute requires geometry, current and pressure recalculation.
2. **Digital detailing:** complete guard flanges/fixing holes, cleat screw schedule, shelf support detail, top seam/gasket, external enclosure/gland/cable layout, washers/nuts and compression stops as appropriate. The JSON captures R00 inputs, but some construction coordinates are explicit in the generator; changing JSON alone does not update every detail.
3. **Mechanical release:** specify actual plywood, adhesive, fasteners, gasket force/landing and guard sheet; check retainer bending, joint capacity, total mass/centre of gravity, tip/slide resistance and guard reach/deflection. Then inspect dimensions and seals physically.
4. **Electrical release:** confirm actual Indian socket/approved plug adaptation, OEM connector chain, 4-fan startup current, protection and restraint. This chain does NOT implement the existing tower manual-restart/interlock requirement. Either implement a reviewed rated restart-inhibit arrangement or obtain an explicit guarded bench-only exception from the qualified reviewer; do not silently waive it. No unattended operation. Unplug before service and verify all fans stopped.
5. **Physical demonstration:** authorized purchase -> delivery -> local fabrication -> commissioning -> repeated trials with rented/paid instruments. No college lab or optional ENTC friend is assumed. Record total flow, filter pressure, watts, noise and matched room particle-decay data. Low-cost PM readings do not certify HEPA/MERV efficiency.

These are concrete remaining interfaces, not closed gates. No supplier, reviewer or workshop was contacted. No lead time, total budget or completion date is confirmed.

## Evidence and licences

Sources checked3 October2026:

- [ARCTIC manual, 2025 drawing and mounting template](https://support.arctic.de/p14-max). Dimensions140x140x27;125mm pitch. Drawing says ACFAN00287A; current spec sheet associates colour/revision differently. Do not assume an older shop listing resolves this.
- [ARCTIC P14 Max specification and chart](https://www.arctic.de/media/8a/18/01/1710507321/Spec_Sheet_P14_Max_EN.pdf). Digitization is approximate, not an OEM numeric table.
- [S&P MERV filter submittal](https://www.solerpalau-usa.com/documents/Submittal/trc-merv.pdf). Part 990303 is the MERV13 dimensional reference, not evidence of India stock or resistance. The archived file name abbreviates the part number; the full OEM part is 990303.
- [Noctua NV-PS1](https://www.noctua.at/en/products/nv-ps1), [specifications](https://www.noctua.at/en/products/nv-ps1/specifications), [NA-FH1](https://www.noctua.at/en/products/na-fh1/specifications), [NA-FC1 total-current FAQ](https://www.noctua.at/en/support/faqs/how-many-fans-can-i-connect-to-the-na-fc1-controller). OEM system ratings do not certify our assembled purifier.
- [MDComputers P14 Max listing](https://mdcomputers.in/product/arctic-p14-max-140mm-case-fan-acfan00287a): out of stock when checked, not a quotation. No claimed India-wide unavailability.
- [Tempest Brisa open-source build](https://github.com/obife29/Tempest-Brisa-Open-Source), [CC0 licence](https://github.com/obife29/Tempest-Brisa-Open-Source/blob/main/LICENSE). A DXF and licence are archived as a precedent, not reused as this CAD or treated as independent performance proof. Repository credits Maria Boavida/OMA, Shawn Santos/Ar Limpo Lisboa, Florian Festi/Boxes.py and Naomi Wu/Nukit. Credit retained; no patentability or trademark-rights claim.

Archived references are under `data/prototype_d01/sources`. `ARCTIC_P14_Max_PQ.pdf` is a failed HTML download despite its extension; it is **not evidence**. Use the valid `ARCTIC_P14_Max_Spec.pdf` chart. `MeanWell_GST60A.pdf` was screened but is not selected. Do not treat OEM documents as open-source CAD licences. The downloaded Brisa reference is the only archived construction precedent carrying the inspected CC0 licence.

## Reproduce inside this workspace

```powershell
& 'D:\Applications\FreeCAD 1.1.3\bin\python.exe' scripts/geometry/build_d01.py
& 'C:\Users\G15 5530\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' scripts/analysis/d01_pressure.py
& 'C:\Users\G15 5530\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' scripts/reports/build_d01_delivery.py
```

No new software was installed. Historical documents and models remain untouched except for navigation/status additions.
