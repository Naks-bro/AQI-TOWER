# Preliminary 3D packaging model — R00

Created 2 October 2026 using detected FreeCAD 1.1.3. NOT FOR FABRICATION. This is the next step beyond the two-dimensional schematics, not a complete product assembly.

## Files

- `cad/packaging/AQI_Cylindrical_Packaging_R00.FCStd`: editable FreeCAD document with spreadsheet-driven primitive/boolean features.
- `cad/packaging/AQI_Cylindrical_Packaging_R00_NOT_FOR_FABRICATION.step`: exchange file containing ten labeled physical/envelope objects; placeholders included, not a manufacturing export.
- `cad/packaging/PACKAGING_R00_AUDIT.json`: geometry and parameter checks, with limitations.
- `cad/parametric/cylindrical_packaging_r00.json`: versioned source dimensions and evidence labels.
- `scripts/geometry/create_cylindrical_packaging.py`: reproducible generator using the installed FreeCAD Python runtime.
- `scripts/geometry/view_cylindrical_packaging.FCMacro`: run in FreeCAD for a clean view of the generated model.

## What the model contains

Circular shell with two assumed service openings and separate curved door envelopes; 592 x 592 x 48 mm prefilter and 593 x 593 x 292 mm HEPA outer envelopes; full-width bulkheads with square openings; generic fan installation allowance; side electrical enclosure allowance; base envelope; and a HEPA removal-sweep reference volume.

The bulkhead is a geometric partition. It does not yet have a sealing ledge, compressed gasket, retaining clamps, rated filter tray or realistic airtight cassette interface. The filter blocks are outer dimensions only, not media or fluid domains. The base is a reserved envelope, not a specification to make a solid metal cylinder.

## Results of executed checks

- Generated shapes are valid according to FreeCAD's geometry checks.
- No positive-volume overlaps between the ten exported envelope objects at nominal R00 settings.
- Assumed HEPA removal sweep does not intersect the modeled shell once its service opening is cut. This does not check an operator, handling equipment, hinges or an actual cassette tray.
- Diameter change of +20 mm propagates from the spreadsheet to shell geometry; restored before saving.
- Native document saved, reopened and checked for the 292 mm HEPA depth.
- STEP exchange file separately reimported: valid shape, ten solids.
- Candidate HEPA square diagonal: 838.629 mm. Corner clearance to assumed 950 mm bore: 55.686 mm before cassette hardware.

## Open and edit

Open the FCStd in FreeCAD. For a clean visual view, open and run `view_cylindrical_packaging.FCMacro`; it hides construction tools, makes the shell transparent and colors candidates/allowances. The macro does not save changes. Toggle the doors to inspect access. The removal-sweep reference is hidden by default.

Edit the `Parameters` spreadsheet to explore dimensions. The saved assembly has native expression links; no custom Python proxy is required to recompute it. Re-run checks after changing dimensions: a valid solid is not necessarily a clash-free or buildable assembly. To persist a new reviewed baseline, edit the JSON and regenerate to an explicitly versioned output rather than silently treating a local spreadsheet edit as an approved change.

Generator command from project root:

```powershell
& 'D:\Applications\FreeCAD 1.1.3\bin\python.exe' scripts/geometry/create_cylindrical_packaging.py
```

Regeneration replaces derived R00 outputs; save intentional manual work under a new name first. Historical GEO_C and V00 documents are untouched.

## Not solved yet

Intake apertures/guard mesh and outlet guard have NOT been modeled. The closed shell is therefore not a working airflow path. The fan block is 550 x 550 x 600 mm ASSUMED space, not verified KVO geometry. Supports, fasteners, gasket compression, door hardware, electrical internals, acoustic treatment, weather protection and structure/stability calculations are absent. Horizontal filter orientation needs supplier approval.

No mass, stiffness, safety certification, airflow prediction or outdoor coverage can be inferred from this geometry. Previous GEO_C CFD is not evidence for this new arrangement.

## Next release gate

Obtain exact fan/filter installation drawings and confirm horizontal orientation, gasket details and service handling. Replace the generic fan block, design cassette supports/seals, then define intake/outlet openings and pressure losses together. Request faculty structural and electrical reviews before generating manufacturing or wire-by-wire drawings.
