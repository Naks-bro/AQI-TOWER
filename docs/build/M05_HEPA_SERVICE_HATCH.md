# M05 — removable HEPA service hatch

2 October 2026. GEOMETRY / LOCATION STUDY — NOT HARDWARE SELECTION OR FABRICATION RELEASE.

## What was added

This new CAD branch replaces the inner HEPA access-panel piece with an illustrative mounting flange, gasket-space ring and removable cover. Eight generic latch-location blocks and two handle-location blocks reserve space; they are NOT functioning mechanisms or CAD of a purchasable latch/handle. No catches, cams, fasteners, preload settings or rated retention are modeled.

The comparison branch also changes the cylindrical internal diameter from 950 to **980 mm**, inner HEPA opening from 635 to **645 mm**, and outer HEPA access width from 650 to **700 mm**. These are new branch assumptions, not final specifications. R02 and the original independent-housing CAD remain unchanged on disk.

See the [hatch layout illustration](M05_HEPA_SERVICE_HATCH.html).

## Modeled stack

```text
Inner housing edge -> illustrative flange -> gasket envelope -> removable cover
                                      ↑ eight latch locations, not actual closing mechanisms

Remove outer decorative access piece first.
Support cover; release reviewed future closing mechanism; remove cover forward.
Remove retainer clamps/retainer; lift HEPA clear of its seat before withdrawing.
```

**ASSUMPTIONS:** clear opening 645 x 310 mm, z650–960 mm; flange outside 675 x 340 mm, 15 mm land and 3 mm thickness; gasket outside 665 x 330 mm with 10 mm land and 3 mm installed space; cover outside 675 x 340 mm, 2 mm thick. Cover material/grade not selected. A 3 mm installed gasket envelope is NOT its free thickness, compression, hardness or sealing specification.

The flange extends beyond the 653 mm inner housing face. Housing wall land beside the opening is narrow. Its weld/fold/joint/load path, flatness and edge reinforcement need review. No mounting holes have been invented; future penetrations must be sealed and rechecked.

## Executed checks

**DETECTED:**

- 48 valid solids in the combined snapshot; zero positive-volume pairwise clashes.
- Assumed lifted HEPA and retainer sweeps clear with inner cover/latch/handle envelopes and outer access piece removed; retainer clamps already removed.
- A 400 mm straight-forward withdrawal envelope for the cover and its attached location blocks clears fixed modeled parts after outer access removal. It is not a latch-unlocking motion, hand/tool check or full handling maneuver.
- Nominal retainer side margin is 6 mm versus the previous 1 mm; real tolerance/coat/deflection margins still need review.
- Native FreeCAD reopen and STEP reimport passed. Both source CAD hashes are unchanged.

The enlarged casing/opening examples from the preceding calculation are now actual shapes in this separate study. The earlier 950 mm model and its audits remain historical evidence. The housing-to-post gap remains only **6 mm**: a larger casing does not move the frame automatically.

The prefilter service panel remains at its earlier preliminary detail. This branch develops HEPA access only; neither access closure is released.

## Pressure and handling are separate from gasket compression

At an **assumed local door differential of 500 Pa**, 645 x 310 mm gives about **100 N** pressure force. This is not the measured door differential, HEPA filter pressure drop, fan shutoff load or required gasket preload. Sign matters: a suction-side pressure can load the cover inward; other cases must be assessed from the actual system. Do NOT divide 100 N by eight and select eight latches from that arithmetic.

The 2 mm cover would weigh about **3.60 kg if steel density were 7,850 kg/m3**, excluding handles, latches and stiffeners. Its vertical gravity load, panel bowing, gasket force distribution and accidental release need separate checks. Positive retention/support against panel drop has NOT been designed. Handle blocks do not provide that safeguard.

The previous 129.52 kg hybrid subtotal belongs to the unchanged M03 geometry. It is NOT a recalculated weight for this enlarged hatch/casing branch. Complete tower weight, mass/CG and stability are still unknown.

## Real hardware information required

The [Southco compression-latch family](https://southco.com/latches/compression-latches) provides examples of gasket-compressing closures and adjustable grip options (reviewed 2 October 2026). It is a reference family, NOT a chosen supplier, SKU, availability claim or endorsement of the eight location blocks. A latch marked sealed does not certify the whole housing.

Before selection, request a dimensioned CAD/drawing and confirm grip, travel, panel thickness range, mounting/catch detail, published load limits, working clearance, environmental limitations and adjustment/retention method. Obtain gasket material/profile and a force-versus-compression requirement from the seal supplier. Review gasket corners, joints, compression stops, cover flatness/stiffening and closing-force distribution together.

Preserve reviewed protective bonding where required; coating/isolation and removable-panel attachment must be coordinated with the electrical reviewer. No bonding conductor sizes or mains wiring are specified here.

## Safe service procedure still to finalize

1. Isolate power by the approved method; verify fan stopped and access safe before releasing panels.
2. Remove/retain the outer decorative access piece using its future reviewed attachments.
3. Support the inner cover before unlocking its actual closure; prevent a dropped panel. The support/retention arrangement is still missing.
4. Remove HEPA retainer hardware first, then lift and withdraw the filter using a reviewed tray/handling method. Filter weight and allowed handling/orientation remain OEM questions.
5. Inspect/replace the seal as specified, refit the filter/retainer, close with reviewed gasket compression, inspect access/guards and perform required integrity checks before operation.

This sequence is a planning checklist, not authorization to operate an unguarded assembly.

## Release gaps and next step

Real latch/catch CAD and mounting; gasket data; cap/cover/flange strength and flatness; latch working sweep; panel drop retention; actual service tools/handling; casing attachments; prefilter hatch development; fan/frame/base connections; full mass/CG; electrical guarding/isolation; installed leakage tests remain unresolved.

**Next:** turn these into a component-specific closure/connection review package using OEM drawings and mentor input. Do not select latch count, clamp force or gasket compression from the location study. All six [build gates](BUILD_REMAINING.md) remain open. No purchase, supplier message, FEA/CFD run or physical test performed.

## Files and reproduction

- `cad/parametric/hepa_service_hatch_m05.json`: explicit assumptions.
- `cad/packaging/AQI_M05_HEPA_Service_Hatch_STUDY.FCStd`: combined shape snapshots, not a complete manufacturing assembly.
- `cad/packaging/AQI_M05_HEPA_Service_Hatch_NOT_FOR_FABRICATION.step`: exchange study.
- `cad/packaging/M05_HEPA_HATCH_AUDIT.json`: clashes, service sweeps, dimensions, pressure/cover-mass illustration and source hashes.

```powershell
& 'D:\Applications\FreeCAD 1.1.3\bin\python.exe' scripts/geometry/create_service_hatch_study.py
python -m unittest discover -s scripts/analysis -p 'test_service_hatch_audit.py'
```

Regeneration replaces this branch's derived outputs. Preserve manual edits first. Original CAD is opened/recomputed in memory for the casing branch but never saved; hashes verify preservation.
