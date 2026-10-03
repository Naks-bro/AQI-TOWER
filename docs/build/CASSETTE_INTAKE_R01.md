# Filter cassette and intake development — R01

2 October 2026. PRELIMINARY, NOT FOR FABRICATION. Current model: `cad/packaging/AQI_Cylindrical_Packaging_R01.FCStd`. R00 remains unchanged.

## What changed physically in the CAD

Eight radial intake openings are now cut into the lower shell. The HEPA bulkhead has an illustrative supporting ledge rather than a full-size hole. A gasket envelope lies between the assumed filter-frame underside and this ledge. A separate removable top hold-down ring shows the retention concept. Service space assumes removal of this ring and a small filter lift before sliding out.

This is still an interface study: the actual candidate filter's frame profile, gasket position, allowable mounting orientation and clamp loads are UNKNOWN. The shape does not prove sealing, guard safety or air-cleaning performance.

## M03-R01: assumed filter seat section

```text
                       CLEAN SIDE / FAN SUCTION
                removable hold-down / retainer
                ↓ reviewed clamp force (UNKNOWN)
             ┌───────────────────────────────┐
             │ filter frame     filter media │  outer size 593 mm candidate
             └───────┐                ┌──────┘
                     ▓ gasket         ▓          illustrative envelope only
        sealed plate ━━━━━┓      ┏━━━━━ sealed plate
                           ↑ air
                         DIRTY SIDE

The full-width plate closes the route around the filter.
Support and clamping act on the filter FRAME, never fragile media.
```

Illustrative seat opening: 563 mm square; assumed frame/ledge allowance 15 mm per side. Gasket envelope: 583 mm outer, 563 mm inner, 3 mm installed height. Retainer: 633 mm outer, 563 mm inner, 5 mm modeled thickness. These are not supplier dimensions or fabrication tolerances. A 3 mm installed envelope is NOT a gasket compression requirement; uncompressed size and material curve are unknown.

Check that the actual clear media area is not obstructed by this frame/retainer. An OEM frame with a different seal plane can invalidate this entire arrangement. Ask for an approved installation drawing before machining or cutting the cassette.

## Retention load: why the seal cannot rely on gravity

Pressure below the horizontal filter is higher than above it in this upward-flow arrangement. That pushes the filter upward, tending to unload the lower gasket. Screening pressure force is ΔP x projected area. At an explicitly assumed 500 Pa across a 593 mm square envelope, force is about 176 N (approximately 18 kg-force). This is NOT a measured operating pressure, clamp rating or design load.

The reviewer must combine pressure loading, filter mass, gasket seating/compression, frame stiffness, handling loads and appropriate factors. Determine failure behaviour during blockage and fan operation. Do not divide 176 N by four and buy four clamps: compression load, force distribution and actual pressure limits still need data. The retaining arrangement requires positively retained, reviewed hardware and should not depend on the service door alone.

## Safe service sequence to develop

Isolate power and verify fan stopped. Remove/open the reviewed service door; release/remove the retainer; lift filter off its gasket before sliding onto a rated tray/support. In this study the lift is 5 mm, an ASSUMPTION. Do not drag the gasket sideways under compression. Refit, inspect the seal, reclamp according to the supplier method, close access and conduct the specified integrity checks before operation.

Retainer fasteners, lift mechanism, rails, tray, filter mass, handling method and door hinges/latches are not designed. The geometric removal sweep excludes the retainer because it has to be removed first; it is not proof that maintenance is safe or convenient.

## Intake sizing screen

Eight assumed 160 x 140 mm openings provide 0.1792 m2 total projected gross area. The actual curved surface area differs slightly; guard/louvre clear area is smaller still.

At the illustrative 1,300 m3/h screening flow:

| Assumed guard free-area fraction | Effective area m2 | Mean passage velocity m/s | Dynamic pressure Pa, rho=1.2 assumed |
|---|---:|---:|---:|
| 100%, no guard (not safe to operate) | 0.1792 | 2.02 | 2.44 |
| 70% | 0.12544 | 2.88 | 4.97 |
| 50% | 0.0896 | 4.03 | 9.75 |

Dynamic pressure is NOT the guard pressure drop. Loss = K x dynamic pressure only with a defensible coefficient for the actual geometry, or use the supplier's measured loss curve. Select a finger-safe guard, account for dust/loading and rain protection, and recheck the full fan/system operating point. The model currently has unguarded openings and is not approved for use.

## Executed CAD checks

Valid generated geometry; no positive-volume clashes among twelve exported envelope objects; nominal lifted HEPA sweep clears the shell, gasket and bulkhead after removal of the retainer. Diameter expression propagation passed. Native file was reopened; STEP was reimported with twelve valid solids. These checks do not cover actual hardware, stress, leakage, airflow or weather resistance.

Source and audit: `cad/parametric/cylindrical_packaging_r01.json`, `cad/packaging/PACKAGING_R01_AUDIT.json`. Reproduce:

```powershell
& 'D:\Applications\FreeCAD 1.1.3\bin\python.exe' scripts/geometry/create_cylindrical_packaging.py --config cad/parametric/cylindrical_packaging_r01.json
```

Derived R01 files are replaced on regeneration; save intentional manual edits under a different revision first. The viewing macro now opens R01. For the preserved R00 file, manually open it and hide the construction tools.

## Official source checks and remaining data

Reviewed 2 October 2026:

- [Camfil CamSafe installation manual](https://www.camfil.com/dam/files/21962/1672906/Instruction_CamSafe-2-Installation-and-Operating-Manual-ENG.pdf): illustrates engineered filter-seat integrity provisions and specific gasket/housing combinations. It does not approve our fabricated cassette.
- [Camfil GlidePack housing family](https://www.camfil.com/en-ca/products/housings-frames--louvers/ducted-housing/glidepack): provides commercial examples of side-access service, flat sealing edges and pressure test ports. Its load/pressure figures are not our design specifications.
- [Systemair AC fan instruction manual](https://shop.systemair.com/upload/assets/202341_FANS_INSTRUCTIONS_CE__A016_.PDF) distinguishes fan families and wiring diagrams; [EC-family manual](https://shop.systemair.com/upload/assets/EC_FANS_OPERATION_AND_MAINTENANCE_INSTR__206268_CE_A017_20190426_193821977.PDF) includes KVO EC models. Neither check establishes the exact historical KVO 250/L unit's purchased geometry or availability.

Do not use unrelated fuel-cell filter gasket instructions as HEPA requirements. Exact fan and filter data requests are in [supplier release questions](SUPPLIER_RELEASE_QUESTIONS.md). No requests sent and no parts purchased.
